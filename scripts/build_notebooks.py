"""Build the complete course. Regeneration clears outputs; execute afterwards."""
from pathlib import Path
from textwrap import dedent
import nbformat as nbf
from lesson_upgrades import enrich
from public_course import prepare_public

from course_paths import ROOT, NOTEBOOKS, NOTEBOOK_SETUP, rewrite_legacy_markdown
NOTEBOOKS.mkdir(exist_ok=True)

def md(text):
    return nbf.v4.new_markdown_cell(dedent(text).strip())

def code(text):
    return nbf.v4.new_code_cell(dedent(text).strip())

def save(name, cells):
    cells = enrich(name, cells, md, code)
    cells = prepare_public(name, cells, md, code)
    notebook = nbf.v4.new_notebook(cells=cells, metadata={
        'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
        'language_info': {'name': 'python'},
    })
    first_code = next(cell for cell in notebook.cells if cell.cell_type == 'code')
    first_code.source = NOTEBOOK_SETUP + '\n' + first_code.source
    for cell in notebook.cells:
        if cell.cell_type == 'markdown':
            cell.source = rewrite_legacy_markdown(cell.source, 'notebooks/' + name)
    first_markdown = next(cell for cell in notebook.cells if cell.cell_type == 'markdown')
    first_markdown.source = (
        '[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)]'
        f'(https://colab.research.google.com/github/Optimizer077/jev-learning-course/blob/main/notebooks/{name})\n\n'
        + first_markdown.source
    )
    nbf.validate(notebook)
    nbf.write(notebook, NOTEBOOKS / name)

SETUP = '''
import numpy as np
import matplotlib.pyplot as plt
from tutorial_utils import setup, show_figure, table, BLUE, ORANGE, GREY
setup()
'''

save('01_jev_basics.ipynb', [
md(r'''
# 1 · Jev: decisions your code can use

## Goal
Understand the interface before thinking about the neural network.
**Jev is a model from TypeSafe AI; “System One” is the company's name for its model class.**
It evaluates supplied context against bounded questions. It does not write a free-form reply.
[Official definition](https://docs.typesafe.ai/concepts/system-one).

Imagine a support inbox. A chatbot might write an explanation of where to send a ticket.
A decision interface gives your program an allowed queue and probabilities, so a normal
`if` statement can choose the next step.

All numbers below are **handmade illustrations**, not Jev outputs. Public documentation checked 2026-10-01.

## Setup
Run cells from top to bottom. No API key or model download is needed.
'''), code(SETUP),
md(r'''
## Steps
### 1. Separate state from the question
The **state** is the evidence. The **question** tells the model what judgment to make.
The **criteria** define the permitted answers and their meanings. A useful abstract view is
$p_\theta(a\mid s,q,C)$: probabilities over answers $a$, given state $s$, question $q$,
and criteria $C$, using learned parameters $\theta$.

This notation describes the interface, not the implementation of Jev's neural network.
'''), code('''
state = {'message': 'The export button crashes every time I click it.'}
question = {
    'type': 'choice',
    'instructions': 'Which support queue best matches the reported problem?',
    'criteria': {
        'billing': 'Charges, invoices, or refunds',
        'technical': 'Broken product behavior',
        'other': 'No listed queue fits or the information is insufficient',
    },
}
print('Evidence:', state['message'])
print('Question:', question['instructions'])
table(['Allowed key', 'Meaning'], question['criteria'].items())
'''),
md(r'''
### 2. Choice: pick from named alternatives
A Choice returns the highest-probability key and the distribution over the options.
Options are relative alternatives; include an escape option when none may fit.
[Choice reference](https://docs.typesafe.ai/primitives/choice).
'''), code('''
choice_probabilities = {'billing': 0.06, 'technical': 0.90, 'other': 0.04}
selected = max(choice_probabilities, key=choice_probabilities.get)
fig, ax = plt.subplots()
ax.barh(list(choice_probabilities), list(choice_probabilities.values()), color=BLUE)
ax.set(xlim=(0, 1), xlabel='Illustrative probability', title='Choice: which queue?')
for i, value in enumerate(choice_probabilities.values()):
    ax.text(value + 0.015, i, f'{value:.0%}', va='center')
show_figure('01_choice')
print('Selected key:', selected)
'''),
md(r'''
### 3. Score: an expectation over ordered levels
A Score uses an ordered list of descriptions. Indices start at 0.
With three levels the result is between 0 and 2, and can be fractional:
$$\text{score}=\sum_{k=0}^{K-1} k\,p(k).$$
This is a rubric position, not an exact measurement of an underlying physical quantity.
[Score reference](https://docs.typesafe.ai/primitives/score).
'''), code('''
levels = ['No disruption', 'Partial disruption', 'Work fully blocked']
probabilities = np.array([0.05, 0.25, 0.70])
score = np.dot(np.arange(len(levels)), probabilities)
table(['Level', 'Description', 'Probability'],
      [(i, label, f'{p:.0%}') for i, (label, p) in enumerate(zip(levels, probabilities))])
print(f'Score = {score:.2f} on a 0–2 scale')

# The same mean can conceal very different distributions.
print('Certain middle level:', np.dot([0, 1, 2], [0, 1, 0]))
print('Split across extremes:', np.dot([0, 1, 2], [0.5, 0, 0.5]))
'''),
md(r'''
Both final examples give 1.0. Inspect the distribution when the difference matters.

### 4. Noul: a yes/no probability
A Noul returns a number from 0 to 1 representing the probability of “yes.” It is not
itself a Boolean; your code selects an action threshold.
[Noul reference](https://docs.typesafe.ai/primitives/noul).
'''), code('''
# An invented answer to: "Does the message explicitly request a refund?"
noul = 0.12
threshold = 0.80  # Teaching policy, not a recommended production threshold.
print('Refund-request probability:', noul)
print('Meets our threshold:', noul >= threshold)
'''),
md(r'''
### 5. Keep three ideas separate
**Probability** describes an outcome. The API's **confidence** summarizes distribution shape for
Choice and Score; Noul has no separate confidence field. **Calibration** describes agreement
between predicted probabilities and observed frequencies across many cases.
The confidence documentation does not specify its exact formula; do not substitute `max(p)`
and label it Jev confidence. [Confidence reference](https://docs.typesafe.ai/confidence).

## Checks
Type safety constrains answer shape. It does not prove that the chosen answer is true.
'''), code('''
assert selected in question['criteria']
assert np.isclose(sum(choice_probabilities.values()), 1)
assert np.isclose(score, 1.65)
assert 0 <= noul <= 1

wrong_but_valid = 'billing'
assert wrong_but_valid in question['criteria']
print('"billing" passes the type check even though this ticket describes a product bug.')
'''),
md(r'''
## Next Steps
Try moving 0.20 probability mass from “Work fully blocked” to “Partial disruption.”
Predict the new score before running the cell: it should decrease from 1.65 to 1.45.

Next: [build a tiny decision model](02_decision_model_from_scratch.ipynb) and see where probabilities can come from.
''')])

save('02_decision_model_from_scratch.ipynb', [
md(r'''
# 2 · Build a tiny decision model from scratch

## Goal
Learn the general machinery behind **direct scoring**: features → logits → probabilities → decision.
We will train a three-class linear model using NumPy, so every operation is visible.

**This is not Jev, a replica of Jev, or RLCD.** Our toy is a supervised classifier on synthetic numeric
features. It does not understand text or new question descriptions.

TypeSafe reports a new architecture, parallel sampler, and Reinforcement Learning for Calibrated
Decisions (RLCD). It describes producing decision probabilities in parallel instead of decoding
answer text token by token. The reviewed public pages do not specify the architecture or a reproducible
training recipe. [Announcement](https://typesafe.ai/blog/introducing-system-one-models-and-jev).

## Setup
No GPU, downloaded weights, or API access.
'''), code(SETUP),
md(r'''
## Steps
### 1. Make a visible learning problem
Each point has two invented features and one of three classes. We generate independent training
and test examples from the same known process. Classes overlap, so perfect classification is not expected.
These coordinates are a teaching stand-in for a learned representation, not a proposed Jev encoding.
'''), code('''
rng = np.random.default_rng(42)
centers = np.array([[-1.5, -0.6], [1.5, -0.6], [0, 1.5]])

def sample(n):
    labels = rng.integers(0, 3, n)
    features = centers[labels] + rng.normal(0, 0.85, (n, 2))
    return features, labels

X_train, y_train = sample(600)
X_test, y_test = sample(600)
fig, ax = plt.subplots()
for k, (color, marker) in enumerate(zip([BLUE, ORANGE, GREY], ['o', '^', 's'])):
    mask = y_train == k
    ax.scatter(*X_train[mask].T, s=16, alpha=0.55, color=color, marker=marker, label=f'Class {k}')
ax.set(xlabel='Synthetic feature 1', ylabel='Synthetic feature 2', title='Training data: 600 synthetic examples')
ax.legend()
show_figure('02_training_data')
'''),
md(r'''
### 2. Convert logits into probabilities
A **logit** is an unconstrained score. For a feature vector $x$, our model computes
$z=xW+b$. Softmax turns the three scores into a distribution:
$$p_k=\frac{\exp(z_k/T)}{\sum_j\exp(z_j/T)}.$$
The temperature $T>0$ controls concentration. Lower temperature makes the distribution sharper;
it does not make the answers more correct. Subtracting the maximum logit prevents overflow without
changing the answer. This is general classifier mathematics, not a disclosed Jev formula.
'''), code('''
def softmax(logits, temperature=1.0):
    if temperature <= 0:
        raise ValueError('Temperature must be positive')
    scaled = logits / temperature
    shifted = scaled - scaled.max(axis=-1, keepdims=True)
    values = np.exp(shifted)
    return values / values.sum(axis=-1, keepdims=True)

table(['Temperature', 'Class probabilities'],
      [(t, np.round(softmax(np.array([0.2, 1.4, -0.3]), t), 3)) for t in [0.5, 1, 2]])
'''),
md(r'''
### 3. Train by penalizing the wrong distribution
Cross-entropy loss is $-\frac{1}{N}\sum_i\log p_{i,y_i}$. It penalizes assigning low probability
to the correct class. For this linear-softmax model the gradient of the logits is $(p-Y)/N$,
where $Y$ contains one-hot labels. We take small steps opposite the gradient.

This ordinary supervised objective teaches probabilistic prediction. It is **not** an implementation
of RLCD; TypeSafe describes RLCD's objective at a high level as calibrated decisions.
[AI primer](https://docs.typesafe.ai/introduction/machine-learning-primer).
'''), code('''
weights = np.zeros((2, 3))
bias = np.zeros(3)
targets = np.eye(3)[y_train]
losses = []
for step in range(500):
    p = softmax(X_train @ weights + bias)
    losses.append(-np.log(p[np.arange(len(y_train)), y_train].clip(1e-12, 1)).mean())
    gradient = (p - targets) / len(y_train)
    weights -= 0.15 * X_train.T @ gradient
    bias -= 0.15 * gradient.sum(axis=0)

test_probabilities = softmax(X_test @ weights + bias)
accuracy = (test_probabilities.argmax(axis=1) == y_test).mean()
print(f'Test accuracy on this synthetic problem: {accuracy:.1%}')
fig, ax = plt.subplots()
ax.plot(losses, color=BLUE)
ax.set(xlabel='Gradient step', ylabel='Training cross-entropy (nats)', title='Learning to score three alternatives')
show_figure('02_training_loss')
'''),
md(r'''
### 4. Inspect one forward pass
All three option scores are computed by one matrix operation. A new input still needs inference,
but this toy does not run a loop to generate an answer string.
'''), code('''
example = np.array([[1.0, -0.5]])
logits = example @ weights + bias
probabilities = softmax(logits)[0]
table(['Class', 'Logit', 'Probability'],
      [(k, f'{logits[0, k]:.3f}', f'{p:.3f}') for k, p in enumerate(probabilities)])
print('Predicted class:', int(probabilities.argmax()))
'''),
md(r'''
### 5. Why skipping output-token decoding can help
A simplified latency model is:
$$t_{\text{text}}=t_{\text{input}}+L\,t_{\text{token}},\qquad
t_{\text{decision}}=t_{\text{input}}+t_{\text{head}}.$$
$L$ is generated output length. This only illustrates a possible source of savings.
Real latency also depends on hardware, input length, batching, architecture, and network overhead.
The next chart uses **invented constants**, not measured Jev or LLM performance.
'''), code('''
output_tokens = np.arange(1, 101)
input_ms, token_ms, decision_ms = 40, 8, 12  # Assumed, for illustration only.
fig, ax = plt.subplots()
ax.plot(output_tokens, input_ms + output_tokens * token_ms, color=BLUE, label='Sequential text decoding')
ax.axhline(input_ms + decision_ms, color=ORANGE, linestyle='--', label='Fixed decision head')
ax.set(xlabel='Generated output tokens in the text example', ylabel='Hypothetical latency (ms)',
       title='Illustrative latency model — not a benchmark', ylim=(0, 900))
ax.legend()
show_figure('02_latency_illustration')
'''),
md(r'''
## Checks
The loss should fall, rows should sum to 1, and test accuracy should beat the roughly one-third
chance baseline on this deliberately easy synthetic task. None of these checks establishes calibration.
'''), code('''
assert losses[-1] < losses[0]
assert np.allclose(test_probabilities.sum(axis=1), 1)
assert np.isfinite(test_probabilities).all()
assert accuracy > 0.65
print(f'Loss: {losses[0]:.3f} → {losses[-1]:.3f}; checks passed.')
'''),
md(r'''
## Next Steps
Increase noise from 0.85 to 1.5 and rerun. Why is certainty harder when the classes overlap?
Try multiplying all test logits by 3: the predicted classes stay the same, but probabilities change.
That is why accuracy alone is insufficient. Continue to [calibration](03_calibration_and_decisions.ipynb).
''')])

save('03_calibration_and_decisions.ipynb', [
md(r'''
# 3 · When should you believe a probability?

## Goal
Separate **classification accuracy**, **calibration**, and **the decision your application takes**.
An 80% prediction means that comparable predictions should come true about 80% of the time,
not that this one is guaranteed. TypeSafe describes calibration as a training goal;
we do not measure its model here. [System One](https://docs.typesafe.ai/concepts/system-one).

## Setup
The following data are synthetic. Because we know how they are generated, we can construct an
oracle predictor and compare it with a deliberately overconfident version.
'''), code(SETUP),
md(r'''
## Steps
### 1. Generate outcomes with known probabilities
For each fictional case draw a probability $p$, then a yes/no outcome with that chance of “yes.”
Our oracle reports $p$. The overconfident predictor multiplies log-odds by three, pushing values
toward 0 and 1 while preserving which side of 0.5 they lie on.
'''), code('''
rng = np.random.default_rng(2026)
n = 12000
p_true = rng.uniform(0.03, 0.97, n)
y = rng.binomial(1, p_true)
log_odds = np.log(p_true / (1 - p_true))
p_overconfident = 1 / (1 + np.exp(-3 * log_odds))

def metrics(p):
    return ((p >= 0.5) == y).mean(), ((p - y) ** 2).mean()

table(['Predictor', 'Accuracy at 0.5', 'Brier score (lower is better)'],
      [(name, f'{metrics(p)[0]:.3f}', f'{metrics(p)[1]:.3f}')
       for name, p in [('Oracle', p_true), ('Overconfident', p_overconfident)]])
'''),
md(r'''
### 2. Read a reliability diagram
Group predictions into probability bins. Compare their mean predicted probability with their
observed fraction of positive outcomes. Perfect population calibration follows the diagonal;
finite samples still fluctuate. The Brier score is the mean of $(p-y)^2$. It evaluates overall
probabilistic prediction quality, including calibration and discrimination, rather than calibration alone.
'''), code('''
def reliability(p, outcomes, bins=10):
    bucket = np.minimum((p * bins).astype(int), bins - 1)
    rows = []
    for k in range(bins):
        mask = bucket == k
        if mask.any():
            rows.append((p[mask].mean(), outcomes[mask].mean(), mask.sum()))
    return np.array(rows)

fig, ax = plt.subplots()
ax.plot([0, 1], [0, 1], '--', color=GREY, label='Perfect calibration')
for label, p, color, marker in [('Oracle', p_true, BLUE, 'o'),
                                ('Overconfident', p_overconfident, ORANGE, 's')]:
    points = reliability(p, y)
    ax.plot(points[:, 0], points[:, 1], marker=marker, color=color, label=label)
ax.set(xlim=(0, 1), ylim=(0, 1), xlabel='Mean predicted probability in bin',
       ylabel='Observed positive fraction in bin', title='Reliability on 12,000 synthetic cases')
ax.legend()
show_figure('03_reliability')
table(['Oracle bin mean', 'Observed positive rate', 'Cases'],
      [(f'{a:.2f}', f'{b:.2f}', int(c)) for a, b, c in reliability(p_true, y)])
'''),
md(r'''
The two predictors have identical class decisions at 0.5. Their probability quality differs.
At high predicted probabilities, the overconfident curve falls below the diagonal: fewer positives
occur than promised. The bin counts above make the denominators visible; these are descriptive
estimates, with no confidence intervals shown.

### 3. Derive a threshold from the consequences
Suppose a false positive costs 4 units and a false negative costs 1 unit; correct actions cost zero.
Act “yes” when its expected cost is smaller:
$$(1-p)C_{FP}<pC_{FN}\quad\Longrightarrow\quad p>\frac{C_{FP}}{C_{FP}+C_{FN}}.$$
This assumes probabilities are appropriate for the current population and the costs describe the task.
It is not a general threshold for Jev's separate `confidence` field.
'''), code('''
false_positive_cost, false_negative_cost = 4, 1
threshold = false_positive_cost / (false_positive_cost + false_negative_cost)

def average_cost(p, cutoff):
    action = p > cutoff
    return np.mean(false_positive_cost * (action & (y == 0))
                   + false_negative_cost * (~action & (y == 1)))

print(f'Cost-derived threshold: {threshold:.2f}')
table(['Probability source', 'Threshold', 'Observed cost per case'],
      [(name, t, f'{average_cost(p, t):.3f}')
       for name, p in [('Oracle', p_true), ('Overconfident', p_overconfident)]
       for t in [0.5, threshold]])
'''),
md(r'''
### 4. Trade automation coverage for review
For this binary example define **maximum outcome probability** as $\max(p,1-p)$.
Only automate cases above a selected cutoff; review the rest. This is our own statistic, **not Jev's
confidence formula**. We report the error rate only among automated cases and the fraction automated.
'''), code('''
max_probability = np.maximum(p_true, 1 - p_true)
cutoffs = np.linspace(0.50, 0.95, 10)
coverage, error = [], []
for cutoff in cutoffs:
    automatic = max_probability >= cutoff
    coverage.append(automatic.mean())
    error.append(((p_true[automatic] >= 0.5) != y[automatic]).mean()
                 if automatic.any() else np.nan)
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].plot(cutoffs, coverage, 'o-', color=BLUE)
axes[1].plot(cutoffs, error, 's-', color=ORANGE)
for ax in axes:
    ax.set(xlabel='Maximum outcome probability cutoff', ylim=(0, 1))
axes[0].set(ylabel='Fraction of all cases', title='Automation coverage')
axes[1].set(ylabel='Error fraction among automated cases', title='Selective error rate')
show_figure('03_coverage_error')
'''),
md(r'''
Higher cutoffs reduce coverage here. The error rate improves in this constructed population,
but that behavior is not guaranteed under distribution shift or miscalibration.
Review cost and reviewer accuracy are omitted from this illustration.

## Checks
'''), code('''
assert np.array_equal(p_true >= 0.5, p_overconfident >= 0.5)
assert metrics(p_true)[1] < metrics(p_overconfident)[1]
assert np.all(np.diff(coverage) <= 0)
assert average_cost(p_true, threshold) < average_cost(p_true, 0.5)
print('Accuracy equality, Brier comparison, coverage, and cost checks passed.')
'''),
md(r'''
## Next Steps
Change the false-positive cost to 9. Predict the threshold before running: 0.9.

For real Jev evaluation, collect labeled examples for your exact questions; tune on a validation set
and evaluate once on a separate test set. Track calibration, mistakes by category, coverage, latency,
and cost. Recheck after changing prompts, model version, or population. Do not infer real Jev
accuracy from this synthetic experiment. Continue to [workflows](04_workflows_and_related_models.ipynb).
''')])

save('04_workflows_and_related_models.ipynb', [
md(r'''
# 4 · Put decisions inside a software workflow

## Goal
Combine narrow judgments with ordinary code, and understand how Jev relates to other model families.

TypeSafe documents evaluation of multiple questions against one shared state in parallel and isolation.
This is an execution/interface property, **not a guarantee that the real-world events are statistically
independent**. [Introduction](https://docs.typesafe.ai/introduction).

## Setup
All answers below are invented. The code only returns route names; it does not send messages or execute actions.
'''), code(SETUP),
md(r'''
## Steps
### 1. Decompose a broad judgment
Instead of “handle this ticket,” ask separately about topic, blocking impact, and missing information.
Then implement policy in code. A later question that needs an earlier answer requires another stage;
putting it in the same parallel call does not create that dependency.
'''), code('''
tickets = [
    {'id': 'A', 'queue': 'technical', 'topic_max_p': 0.94, 'blocked_p': 0.90, 'missing_p': 0.05},
    {'id': 'B', 'queue': 'billing', 'topic_max_p': 0.91, 'blocked_p': 0.10, 'missing_p': 0.10},
    {'id': 'C', 'queue': 'technical', 'topic_max_p': 0.52, 'blocked_p': 0.70, 'missing_p': 0.15},
    {'id': 'D', 'queue': 'other', 'topic_max_p': 0.88, 'blocked_p': 0.20, 'missing_p': 0.85},
]

def route(ticket):
    # These arbitrary teaching thresholds use probabilities, not API confidence.
    if ticket['missing_p'] >= 0.60:
        return 'collect_more_information'
    if ticket['topic_max_p'] < 0.85 or ticket['queue'] == 'other':
        return 'human_review'
    if ticket['queue'] == 'technical' and ticket['blocked_p'] >= 0.80:
        return 'priority_technical_queue'
    return ticket['queue'] + '_queue'

table(['Ticket', 'Suggested route'], [(ticket['id'], route(ticket)) for ticket in tickets])
'''),
md(r'''
### 2. Do not multiply unrelated marginal probabilities blindly
If $P(A)=0.8$ and $P(B)=0.7$, then $P(A\cap B)$ is between
$\max(0,P(A)+P(B)-1)$ and $\min(P(A),P(B))$. Multiplication gives 0.56 only under independence.
Parallel model evaluation does not establish that assumption.
'''), code('''
p_a, p_b = 0.8, 0.7
lower, upper = max(0, p_a + p_b - 1), min(p_a, p_b)
print(f'Possible joint probability: {lower:.2f} to {upper:.2f}')
print(f'If independent: {p_a * p_b:.2f}')
'''),
md(r'''
### 3. Compare related approaches
These are conceptual distinctions, not benchmark rankings.

| Approach | Typical input → output | Relationship to this lesson |
|---|---|---|
| Deterministic rules | Explicit fields → computed result | Best for exact arithmetic, permissions, and known conditions |
| Supervised classifier | Features/text → fixed training labels | Notebook 2; new classes normally require adapting training or the head |
| Encoder with a classification head | Text representation → labels | Can also score categories directly without generating prose |
| Embeddings and similarity | Text → vectors → similarity | Useful for retrieval; cosine similarity is not automatically a probability |
| Pairwise/cross-encoder scorer | Query and candidate → relevance score | Useful for reranking; score calibration requires separate evaluation |
| Generative language model | Context → token sequence | Can generate text and code; constrained decoding can enforce output schemas |
| Jev's documented interface | State + typed questions → decisions and probabilities | Natural-language criteria define the bounded judgments for each request |

The existence of typed output alone does not prove a novel architecture: classifiers and constrained
decoders already constrain outputs. Jev's claimed contribution combines a decision-oriented interface,
training, and execution. The exact comparison needs task-matched measurements, not labels.

An LLM can use constrained decoding and return valid JSON. That addresses syntax, not automatically
truth or calibration. Conversely, a classifier's softmax numbers are not automatically calibrated.

### 4. What should stay in code?
TypeSafe lists weaknesses in exact arithmetic, long irrelevant context, adversarial text, and consistency
between differently phrased questions. Use explicit criteria, filter evidence, and enforce required
identities in software. It also warns against treating rubric scores as precise numerical reconstruction.
[Known limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13).
'''), code('''
# Exact money arithmetic belongs in code; integers represent cents.
unit_price_cents, quantity = 1299, 3
total_cents = unit_price_cents * quantity
print(f'Exact total: {total_cents / 100:.2f}')

# If these are exact complements in our application, derive the complement.
refund_requested_p = 0.72
no_refund_requested_p = 1 - refund_requested_p
print('Complement computed in code:', round(no_refund_requested_p, 2))
'''),
md(r'''
## Checks
'''), code('''
assert [route(t) for t in tickets] == [
    'priority_technical_queue', 'billing_queue', 'human_review', 'collect_more_information']
assert np.isclose(lower, 0.5) and np.isclose(upper, 0.7)
assert total_cents == 3897
print('Routing examples, probability bounds, and exact arithmetic passed.')
'''),
md(r'''
## Next Steps
Add a “security” topic. Decide which deterministic rule should force review regardless of probability.
Then write down examples where two topics overlap, and decide how your criteria resolve them.

The final notebook translates these ideas into an [optional official API call](05_optional_real_jev_api.ipynb).
''')])

save('05_optional_real_jev_api.ipynb', [
md(r'''
# 5 · Optional: call the real Jev API

## Goal
Inspect one real request and validate the response contract. **The saved run is offline.**
It validates handmade fixtures; it contains no live Jev result.

## Setup
You need an API key from the [official console](https://console.typesafe.ai/) only for the live step.
This uses Python's standard HTTP library and the [official API](https://docs.typesafe.ai/api).
Live usage may be billed. The only data sent are the fictional state and questions shown below.

The model is pinned to `jev-1.13.0`, listed when documentation was checked on 2026-10-01.
Aliases can move; check [Models](https://docs.typesafe.ai/models) if that version becomes unavailable.
The model card currently describes text input, including structured text, rather than image/audio input.
'''), code('''
import json
import math
import os
from getpass import getpass
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

RUN_LIVE = False  # Set True yourself to send one request.
MODEL = 'jev-1.13.0'
ENDPOINT = 'https://api.typesafe.ai/v1/systemone'
'''),
md(r'''
## Steps
### 1. Build the request
Each answer is returned under its question ID. Meaning belongs in `instructions` and `criteria`;
the question ID is a lookup key, not a substitute for asking the question.
'''), code('''
payload = {
    'model': MODEL,
    'state': {'customer_message': 'My CSV export crashes in every browser. I cannot finish my report.'},
    'questions': {
        'queue': {
            'type': 'choice',
            'instructions': 'Which support queue best matches the customer_message?',
            'criteria': {
                'technical': 'Broken application behavior',
                'billing': 'Payments, invoices, or refunds',
                'other': 'Neither listed topic applies, or information is insufficient',
            },
        },
        'disruption': {
            'type': 'score',
            'instructions': 'How much does the reported issue disrupt the stated task?',
            'criteria': ['No disruption', 'Some disruption but task can continue', 'Task is blocked'],
        },
        'refund_requested': {
            'type': 'noul',
            'instructions': 'Does customer_message explicitly ask for a refund?',
        },
    },
}
print(json.dumps(payload, indent=2))
'''),
md(r'''
### 2. Check the response where it enters your application
The following checks cover the fields this tutorial uses. They check structure and arithmetic,
not whether a judgment is correct. The tolerance allows minor floating-point differences.
'''), code('''
def require(condition, message):
    if not condition:
        raise ValueError(message)

def finite_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)

def probability(value):
    return finite_number(value) and 0 <= value <= 1

def validate_response(response, request):
    require(isinstance(response, dict), 'Response must be an object')
    require(isinstance(response.get('model'), str), 'Missing model identity')
    answers = response.get('answers')
    require(isinstance(answers, dict), 'Missing answers object')
    require(set(answers) == set(request['questions']), 'Answer IDs do not match questions')
    for name, question in request['questions'].items():
        answer = answers[name]
        require(isinstance(answer, dict), f'{name}: answer must be an object')
        kind = question['type']
        require(answer.get('type') == kind, f'{name}: unexpected answer type')
        if kind == 'noul':
            require(probability(answer.get('noul')), f'{name}: invalid Noul')
            continue
        distribution = answer.get('probabilities')
        require(isinstance(distribution, dict), f'{name}: missing distribution')
        expected = (set(question['criteria']) if kind == 'choice'
                    else {str(k) for k in range(len(question['criteria']))})
        require(set(distribution) == expected, f'{name}: unexpected options')
        require(all(probability(v) for v in distribution.values()), f'{name}: invalid probability')
        require(math.isclose(sum(distribution.values()), 1, abs_tol=1e-5), f'{name}: invalid sum')
        require(probability(answer.get('confidence')), f'{name}: invalid confidence')
        if kind == 'choice':
            selected = answer.get('choice')
            require(selected in expected, f'{name}: invalid choice')
            require(math.isclose(distribution[selected], max(distribution.values()), abs_tol=1e-5),
                    f'{name}: choice is not a highest-probability option')
        else:
            score = answer.get('score')
            require(finite_number(score), f'{name}: invalid score')
            expected_score = sum(int(k) * v for k, v in distribution.items())
            require(math.isclose(score, expected_score, abs_tol=1e-5), f'{name}: inconsistent score')
            legend = answer.get('legend')
            require(isinstance(legend, dict) and set(legend) == expected, f'{name}: invalid legend')
    return answers
'''),
md(r'''
### 3. Exercise the checks without calling a model
This fixture is entirely handmade, including the confidence values. It is not a cached API response,
and does not demonstrate TypeSafe's confidence calculation.
'''), code('''
fixture = {
    'model': 'HANDMADE-TEACHING-FIXTURE',
    'answers': {
        'queue': {'type': 'choice', 'choice': 'technical',
                  'probabilities': {'technical': 0.90, 'billing': 0.03, 'other': 0.07},
                  'confidence': 0.80},
        'disruption': {'type': 'score', 'score': 1.75,
                       'probabilities': {'0': 0.05, '1': 0.15, '2': 0.80},
                       'legend': {str(i): label for i, label in enumerate(payload['questions']['disruption']['criteria'])},
                       'confidence': 0.65},
        'refund_requested': {'type': 'noul', 'noul': 0.04},
    },
}
validated = validate_response(fixture, payload)
print('Handmade fixture passed local checks. No API request was made.')
'''),
md(r'''
### 4. Enable one live request when ready
The key is read from the environment or requested with hidden input. It is never printed.
No network call occurs with `RUN_LIVE = False`. This small teaching client has a timeout and stops
on HTTP failures; for repeated workloads use the official SDK's retry handling.
'''), code('''
def call_jev(request_payload, api_key):
    request = Request(
        ENDPOINT, data=json.dumps(request_payload).encode('utf-8'), method='POST',
        headers={'Authorization': 'Bearer ' + api_key, 'Content-Type': 'application/json'},
    )
    try:
        with urlopen(request, timeout=45) as result:
            return json.load(result)
    except HTTPError as error:
        hints = {401: 'Check the API key.', 422: 'Check request fields and current docs.',
                 429: 'Rate limited; wait before retrying.', 529: 'Service overloaded; retry later.'}
        raise RuntimeError(f'HTTP {error.code}. ' + hints.get(error.code, 'Check the service status.')) from None
    except (URLError, TimeoutError):
        raise RuntimeError('Network request failed or timed out; check connectivity.') from None

live_response = None
if RUN_LIVE:
    key = os.environ.get('TYPESAFE_API_KEY') or getpass('TypeSafe API key (hidden): ')
    try:
        if not key.strip():
            raise ValueError('An API key is required for a live request.')
        live_response = call_jev(payload, key.strip())
        live_answers = validate_response(live_response, payload)
        print('Actual responding model:', live_response['model'])
        print(json.dumps(live_answers, indent=2))
    finally:
        del key
else:
    print('LIVE REQUEST SKIPPED. Set RUN_LIVE = True and rerun to call Jev.')
'''),
md(r'''
## Checks
Deliberately corrupt one probability and verify that our integration rejects it.
'''), code('''
import copy
broken = copy.deepcopy(fixture)
broken['answers']['refund_requested']['noul'] = 1.4
try:
    validate_response(broken, payload)
except ValueError as error:
    print('Expected rejection:', error)
else:
    raise AssertionError('Invalid probability was accepted')
print('Live call completed:', live_response is not None)
'''),
md(r'''
## Next Steps
Change the fictional message and predict how each answer should move. Then compare the actual response
if you have enabled live access. One successful request validates connectivity, not model quality.

Build a labeled evaluation set before choosing operating thresholds. Preserve the actual model ID,
question definitions, and input version so comparisons are interpretable. Keep exact calculations and
action permissions in code. Return to [README](README.md) for the full learning path and source list.
''')])

from extra_lessons import build_extra
build_extra(save, md, code, SETUP)
from related_lessons import build_related
build_related(save, md, code, SETUP)
from torch_lessons import build_torch
build_torch(save, md, code)
print('Created the expanded notebook course in', ROOT)
