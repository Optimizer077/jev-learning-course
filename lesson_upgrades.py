"""Additional explanation and experiments for the original five notebooks."""

def enrich(name, cells, md, code):
    additions = []
    number = name[:2]
    objectives = {
        '01': ('20 min · beginner', 'Choose the right primitive; distinguish output validity from correctness.'),
        '02': ('35 min · intermediate', 'Trace tensor shapes; train a model; inspect a decision boundary and gradient.'),
        '03': ('40 min · intermediate', 'Fit temperature on validation data; evaluate uncertainty and decision costs.'),
        '04': ('25 min · practical', 'Design atomic questions and audit a workflow with failure cases.'),
        '05': ('25 min · practical', 'Validate an API contract and inspect a live response when you opt in.'),
    }
    if number in objectives:
        duration, objective = objectives[number]
        cells.insert(1, md(f'**Study guide:** {duration}. **You should be able to:** {objective}\n\n'
                           '[Course map](00_start_here.ipynb) · [Interactive playground](playground.html) · '
                           '[Worked answers](08_exercises_and_solutions.ipynb)'))
    if number == '01':
        additions = [md(r'''
### 6. Follow the full request through the system
This diagram is the **documented interface**, not a picture of proprietary layers.
The model estimates; the policy decides what happens. Notice that a confident topic prediction
does not by itself authorize sending a message, granting access, or changing a record.
'''), code('''
from tutorial_utils import flow_diagram
flow_diagram(['State\\nEvidence', 'Question\\nAllowed answers', 'Model\\nProbabilities', 'Policy\\nRoute / review'],
             '01_request_flow', 'A decision request inside an application')
'''), md(r'''
### 7. Choice versus several Nouls
“Which topic is primary?” requires one winner; “Which topics are present?” may have several positives.
Choice probabilities share a denominator. Separate yes/no probabilities do not need to add to one.
The following handmade example mentions a broken export and a refund. It is perfectly reasonable
for both attributes to be present, even though only one queue must own the case.
'''), code('''
multi_label = {'mentions_bug': 0.90, 'requests_refund': 0.85}
primary_topic = {'technical': 0.60, 'billing': 0.35, 'other': 0.05}
print('Sum of separate yes/no probabilities:', sum(multi_label.values()))
print('Sum over mutually exclusive primary topics:', sum(primary_topic.values()))
assert sum(multi_label.values()) > 1
assert np.isclose(sum(primary_topic.values()), 1)
'''), md(r'''
### 8. Known, claimed, and unknown

| Evidence level | What we can say | What we must not infer |
|---|---|---|
| Documented interface | State and typed questions produce bounded outputs | The answer is always true |
| Provider description | RLCD targets calibrated decisions; questions run in parallel | Calibration holds on every future dataset |
| Provider performance report | Published workflows show speed/cost advantages | The same ratio holds on your hardware and workload |
| Not disclosed in the reviewed pages | Exact weights, layer design, detailed RLCD objective and sampler | A softmax toy or attention mask reproduces Jev |

The final row matters: explaining a useful analogy is possible without inventing an architecture.
The [launch article](https://typesafe.ai/blog/introducing-system-one-models-and-jev) itself qualifies its benchmark claims.

**Predict first — exercise 1:** Which primitive fits each request?
1. Pick one support queue. 2. Is a refund explicitly requested? 3. Rate disruption against three ordered descriptions.
4. Write a reassuring email. Explain why the fourth needs a different kind of output.
''')]
    elif number == '02':
        additions = [md(r'''
### 6. Keep track of the tensor dimensions
Our training matrix $X$ has one row per example. Multiplying by $W$ produces one score per class.
Bias adds one learned offset to each class, repeated across rows by NumPy broadcasting.
'''), code('''
table(['Tensor', 'Shape', 'Meaning'], [
    ('X_train', X_train.shape, '600 examples × 2 features'),
    ('weights', weights.shape, '2 features × 3 classes'),
    ('bias', bias.shape, 'one offset per class'),
    ('logits', (X_train @ weights + bias).shape, '600 examples × 3 class scores'),
])
'''), md(r'''
### 7. See what the classifier learned
Background colors mark the most likely class; dashed contours show the maximum class probability.
Each panel comes from the same trained model. The numeric features are meaningful only inside
this synthetic world. Far from the training clouds, a linear classifier can still be extremely confident.
That is an important limitation: low uncertainty is not an out-of-distribution detector.
'''), code('''
from matplotlib.colors import ListedColormap
gx, gy = np.meshgrid(np.linspace(-5, 5, 200), np.linspace(-5, 5, 200))
grid = np.column_stack([gx.ravel(), gy.ravel()])
grid_prob = softmax(grid @ weights + bias)
fig, ax = plt.subplots(figsize=(8, 5))
ax.contourf(gx, gy, grid_prob.argmax(axis=1).reshape(gx.shape),
            levels=[-0.5, 0.5, 1.5, 2.5], cmap=ListedColormap(['#dce9f7', '#fae4d0', '#e5e5e5']))
contours = ax.contour(gx, gy, grid_prob.max(axis=1).reshape(gx.shape),
                      levels=[0.6, 0.8, 0.95], colors=GREY, linestyles='--', linewidths=0.8)
ax.clabel(contours, fmt='%.2f')
for k, (color, marker) in enumerate(zip([BLUE, ORANGE, GREY], ['o', '^', 's'])):
    points = X_test[y_test == k]
    ax.scatter(*points.T, s=13, alpha=.45, color=color, marker=marker, label=f'Test class {k}')
ax.set(xlabel='Synthetic feature 1', ylabel='Synthetic feature 2', title='Decision regions and maximum class probability')
ax.legend(loc='upper left')
show_figure('02_decision_regions')
far_away = np.array([[20., -10.]])
print('Probabilities far outside the training cloud:', softmax(far_away @ weights + bias).round(4))
'''), md(r'''
### 8. Verify one gradient by finite differences
For one weight, perturb it slightly in both directions and estimate the slope of the loss.
This is an independent numerical check of the analytic update used above, not a second copy of its formula.
'''), code('''
def loss_for(W):
    pp = softmax(X_train @ W + bias)
    return -np.log(pp[np.arange(len(y_train)), y_train]).mean()

epsilon = 1e-5
plus, minus = weights.copy(), weights.copy()
plus[0, 0] += epsilon
minus[0, 0] -= epsilon
numeric_gradient = (loss_for(plus) - loss_for(minus)) / (2 * epsilon)
analytic_gradient = (X_train.T @ (softmax(X_train @ weights + bias) - targets) / len(y_train))[0, 0]
print(f'Numerical: {numeric_gradient:.8f}; analytic: {analytic_gradient:.8f}')
assert np.isclose(numeric_gradient, analytic_gradient, atol=1e-7)
'''), md(r'''
**Predict first — exercise 2:** Add 100 to every logit in a row. Do the probabilities change?
Then multiply all logits by 3. Does the most likely class change? Do the probabilities change?
Use the [playground](playground.html) to test your predictions.

**Connection to Jev:** this model learns a fixed three-column head. A service that accepts new
natural-language criteria needs a way to condition the judgment on those criteria. Notebook 6
explores that distinction and shows a generic attention mechanism without claiming Jev uses it.
''')]
    elif number == '03':
        additions = [md(r'''
### 5. Repair overconfidence using a separate calibration set
So far we compared known distributions. Now pretend we only see the overconfident logits and labels.
Use the **first 6,000 cases to fit temperature** and reserve the remaining 6,000 for evaluation.
No weights are trained in this experiment. A trained model would additionally need its own training set.

We select $T$ by minimizing binary log loss on the calibration split. Temperature scaling is a
post-processing method studied by [Guo et al. (2017)](https://proceedings.mlr.press/v70/guo17a.html).
It is not RLCD and not a Jev API parameter. A positive $T$ preserves the class ranking.
'''), code('''
from lab_core import softmax as categorical_softmax, nll
calibration_ids = np.arange(6000)
evaluation_ids = np.arange(6000, n)
raw_logits = np.column_stack([np.zeros(n), 3 * log_odds])
temperatures = np.geomspace(.25, 6, 121)
calibration_losses = np.array([nll(categorical_softmax(raw_logits[calibration_ids], t), y[calibration_ids])
                              for t in temperatures])
fitted_temperature = temperatures[calibration_losses.argmin()]
fixed = categorical_softmax(raw_logits[evaluation_ids], fitted_temperature)[:, 1]
before = p_overconfident[evaluation_ids]
y_eval = y[evaluation_ids]
print(f'Validation-selected temperature: {fitted_temperature:.3f}')
table(['Held-out predictor', 'Brier score', 'Accuracy'], [
    (label, f'{np.mean((p-y_eval)**2):.4f}', f'{np.mean((p>=.5)==y_eval):.3f}')
    for label, p in [('Before scaling', before), ('After scaling', fixed)]])
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].plot(temperatures, calibration_losses, color=BLUE)
axes[0].axvline(fitted_temperature, color=ORANGE, linestyle='--')
axes[0].set(xlabel='Temperature T', ylabel='Calibration log loss (nats)', title='Fit on 6,000 cases only')
axes[1].plot([0, 1], [0, 1], '--', color=GREY)
for label, pp, col, marker in [('Before', before, ORANGE, 's'), ('After', fixed, BLUE, 'o')]:
    points = reliability(pp, y_eval)
    axes[1].plot(points[:, 0], points[:, 1], marker=marker, color=col, label=label)
axes[1].set(xlabel='Mean predicted probability', ylabel='Observed positive fraction',
            title='Evaluate on 6,000 different cases', xlim=(0,1), ylim=(0,1))
axes[1].legend()
show_figure('03_temperature_fit')
assert np.array_equal(before >= .5, fixed >= .5)
'''), md(r'''
The fitted temperature should be near 3 because we deliberately multiplied the true log-odds by 3.
This unusually clean repair is built into the experiment. Real miscalibration need not be fixable
with one parameter. Sparse bins and changing populations can also mislead a reliability diagram.

### 6. An uncertainty interval and a distribution shift
Estimate uncertainty in the held-out **mean Brier score** by resampling cases with replacement.
The 95% percentile bootstrap interval assumes the sampled cases are independent and representative.
It is not a probability interval for one model answer.
'''), code('''
bootstrap_rng = np.random.default_rng(91)
squared_errors = (fixed - y_eval) ** 2
bootstrap_means = [squared_errors[bootstrap_rng.integers(0, len(y_eval), len(y_eval))].mean()
                   for _ in range(500)]
low, high = np.quantile(bootstrap_means, [.025, .975])
print(f'Held-out Brier = {squared_errors.mean():.4f}; 95% bootstrap interval [{low:.4f}, {high:.4f}]')

# Change the outcome relationship, while leaving the predictor unchanged.
shifted_true_p = 1 / (1 + np.exp(-(log_odds[evaluation_ids] + 1.5)))
shifted_y = bootstrap_rng.binomial(1, shifted_true_p)
print(f'Original positive rate: {y_eval.mean():.3f}; shifted positive rate: {shifted_y.mean():.3f}')
print(f'Brier after this synthetic shift: {np.mean((fixed-shifted_y)**2):.4f}')
'''), md(r'''
### 7. Include the cost of review
If perfect review costs $C_R$ and correct automatic actions cost zero, compare three expected costs:
$C_{yes}=(1-p)C_{FP}$, $C_{no}=pC_{FN}$, and $C_{review}=C_R$.
Real reviewers also make mistakes; the flat review-cost assumption below is deliberately idealized.
'''), code('''
probability_grid = np.linspace(0, 1, 301)
costs = np.column_stack([4*(1-probability_grid), probability_grid, np.full(301, .2)])
fig, ax = plt.subplots()
for i, (label, col, style) in enumerate(zip(['Act yes', 'Act no', 'Perfect review'],
                                         [ORANGE, BLUE, GREY], ['-', '-', '--'])):
    ax.plot(probability_grid, costs[:, i], color=col, linestyle=style, label=label)
ax.set(xlabel='Probability of yes', ylabel='Expected cost (arbitrary units)', ylim=(0, 1.05),
       title='Choose the action with the lowest expected cost')
ax.legend()
show_figure('03_review_cost')
print('At p=0.5, cheapest action:', ['yes', 'no', 'review'][costs[150].argmin()])
'''), md(r'''
**Predict first — exercise 3:** With costs $C_{FP}=4$, $C_{FN}=1$, and $C_R=0.2$,
find the two probability boundaries between “no,” “review,” and “yes.”
What happens if review costs 0.8 instead? See the worked solution after attempting it.
''')]
    elif number == '04':
        additions = [md(r'''
### 5. Rewrite vague questions into testable contracts
The criteria should tell a reader how to label a boundary case. These are authored examples;
we are not claiming the rewrite improves Jev without running an evaluation.

| Vague | More testable | Edge case to include |
|---|---|---|
| Is this bad? | Does the reported bug prevent completion of the named task without a workaround? | Inconvenient but a workaround exists |
| Handle the refund | Does the message explicitly ask to return money already paid? | A price question is not a refund request |
| Choose the right team | Choose the primary queue using the stated precedence rules | A failed export of an invoice |
| Is the customer verified? | Does the supplied trusted account record have `verified=true`? | This is a code check, not a model question |

Write exclusions as well as inclusions. Keep each probability attached to its precise question;
changing the definition changes what the number means.

### 6. Demonstrate an order-sensitive pipeline
In a two-stage workflow, the first answer can choose which evidence to retrieve for the second.
Questions that depend on that retrieved evidence cannot be answered using the earlier, incomplete state.
'''), code('''
documents = {
    'billing': 'Billing policy: duplicate charges can be investigated using a transaction ID.',
    'technical': 'Technical checklist: browser version, error text, and reproduction steps.',
}
first_stage_choice = 'technical'  # Hand-authored stand-in for a model result.
second_stage_state = {'message': 'CSV export crashes.', 'reference': documents[first_stage_choice]}
print(second_stage_state)
print('The second stage now has evidence that was absent from the first.')
'''), md(r'''
### 7. Design a fair comparison before collecting results

| Hold fixed | Record | Report |
|---|---|---|
| Task definitions and input cases | Model version, prompt version, dataset split | Accuracy and per-class errors |
| Allowed candidate set | Raw probabilities and answer validity | Calibration and log loss |
| Hardware/service conditions where possible | Input size, wall time, failures, retries | Median and p95 latency |
| Evaluation labels | Per-case usage and retry costs | Coverage, review rate, cost per resolved case |

Do not compare Jev's task probabilities with an LLM merely saying “I am 95% confident” as though
the two measurements have identical meaning. Benchmark the actual outputs and complete workflow.
Provider benchmarks are useful hypotheses to test; they do not replace measurements on your task.

**Predict first — exercise 4:** Your topic probability is 0.96, but required account permission is false.
Should the system act? Which part of the implementation should enforce the answer?
''')]
    elif number == '05':
        additions = [md(r'''
### 5. Inspect the complete decision without losing uncertainty
This cell works with the explicit teaching fixture in offline mode. It shows the **selected probability**
separately from the **API confidence** so they cannot be accidentally treated as the same field.
The confidence value shown offline remains invented.
'''), code('''
from tutorial_utils import table
active_response = live_response if live_response is not None else fixture
active_answers = validate_response(active_response, payload)
queue = active_answers['queue']
table(['Source', 'Choice', 'Selected probability', 'Confidence'], [[
    'LIVE' if live_response is not None else 'HANDMADE FIXTURE',
    queue['choice'], queue['probabilities'][queue['choice']], queue['confidence']]])
'''), md(r'''
### 6. Test several failure modes locally
An integration should fail visibly on a broken contract. Transport success alone is insufficient.
These mutations exercise different invariants, without contacting the API.
'''), code('''
import copy
mutations = {
    'missing question': lambda r: r['answers'].pop('queue'),
    'unknown option': lambda r: r['answers']['queue'].update(choice='invented_queue'),
    'bad sum': lambda r: r['answers']['queue']['probabilities'].update(technical=.5),
    'nonfinite value': lambda r: r['answers']['refund_requested'].update(noul=float('nan')),
    'incorrect expectation': lambda r: r['answers']['disruption'].update(score=.1),
}
rejected = []
for label, mutate in mutations.items():
    example = copy.deepcopy(fixture)
    mutate(example)
    try:
        validate_response(example, payload)
    except ValueError:
        rejected.append(label)
assert len(rejected) == len(mutations)
print('Rejected invalid cases:', ', '.join(rejected))
'''), md(r'''
### 7. Prepare an evaluation request without sending it
The capstone dataset can also become a small real-model evaluation. This cell prepares a request
for one case. Do not accidentally send the answer label or split to the model. A proper live study
would run all selected cases, record costs/errors, and compare against held-out human labels.
'''), code('''
from lab_core import load_tickets
evaluation_case = next(r for r in load_tickets() if r['split'] == 'test')
evaluation_request = copy.deepcopy(payload)
evaluation_request['state'] = {'customer_message': evaluation_case['text']}
evaluation_request['questions'] = {'queue': {
    'type': 'choice', 'instructions': 'Select the primary support topic. Broken product behavior takes precedence over the document topic.',
    'criteria': {'billing': 'Charges, invoices, refunds, payment or price questions',
                 'technical': 'Broken application behavior, crashes, failed features',
                 'account': 'Identity, passwords, sign-in, access or email changes'}}}
assert 'label' not in evaluation_request['state']
print('Prepared, NOT SENT:', evaluation_case['id'])
print(json.dumps(evaluation_request, indent=2))
'''), md(r'''
**Predict first — exercise 5:** Why is copying the entire dataset row into `state` an evaluation leak?
How would you separate a legitimate policy reference from the hidden answer label?
''')]

    if additions:
        insertion = next(i for i, cell in enumerate(cells)
                         if cell.cell_type == 'markdown' and '## Checks' in cell.source)
        # Some original cells introduce Checks at the end of an explanatory paragraph.
        cell = cells[insertion]
        prefix, suffix = cell.source.split('## Checks', 1)
        replacement = ([md(prefix)] if prefix.strip() else []) + additions + [md('## Checks' + suffix)]
        cells[insertion:insertion+1] = replacement
    return cells
