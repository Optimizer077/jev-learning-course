"""Orientation, architecture lab, capstone, and worked exercises."""

def build_extra(save, md, code, setup):
    save('00_start_here.ipynb', [md(r'''
# Start here · Understanding Jev through experiments

## Goal
Build a useful answer to four questions: **What does Jev return? How can a model score decisions?
What makes probabilities trustworthy? How do I put the result into software?**

This course has three evidence levels. **Documented Jev behavior** is linked to official sources.
**General ML mechanisms** are implemented in small, inspectable experiments. **Unknown internals**
stay unknown. The examples are not a reverse-engineered Jev model.

## Choose a path

| Path | Read in this order | Approximate time |
|---|---|---|
| Intuition first | 01 → 04 → playground | 45–60 minutes |
| Build and understand | 01 → 02 → 03 → 06 → 07 | 2–3 hours |
| Real integration | 01 → 04 → 05 → 07 | 1–2 hours, API optional |
| Full course | 01 through 08 | Several short sessions |

The times are study estimates, not measured completion times.

## Setup
Open the notebooks in JupyterLab or VS Code. Select a Python environment with `requirements.txt`
installed, then use **Restart Kernel and Run All**. Every lesson is independent; no previous kernel
state is required. The saved outputs let you read immediately. The only live API call is in lesson 5,
and it is disabled until you explicitly enable it.

For a reading-only experience, open [the course home page](index.html) in a browser.
The [interactive playground](playground.html) works without Python or an API key.
'''), code(setup), md(r'''
## Steps
### 1. Locate the model inside a larger system
The output is an estimate. Your program decides what to do with it. This separation is the main
idea to carry into every example.
'''), code('''
from tutorial_utils import flow_diagram
flow_diagram(['Evidence\\nWhat is known?', 'Judgment\\nWhat is likely?', 'Policy\\nWhat should happen?', 'Evaluation\\nWas it useful?'],
             '00_course_map', 'A complete decision system')
'''), md(r'''
### 2. Preview the learning sequence

| Lesson | The question it answers | Hands-on output |
|---|---|---|
| [01 · Basics](01_jev_basics.ipynb) | What are Choice, Score, and Noul? | Typed decisions, expected scores, request flow |
| [02 · From scratch](02_decision_model_from_scratch.ipynb) | Where can probabilities come from? | Trained classifier, decision regions, checked gradient |
| [03 · Calibration](03_calibration_and_decisions.ipynb) | When does 80% mean 80%? | Temperature fitting, bootstrap interval, review policy |
| [04 · Workflows](04_workflows_and_related_models.ipynb) | Where does model judgment belong? | Routing rules, dependency example, evaluation design |
| [05 · API](05_optional_real_jev_api.ipynb) | How do I call real Jev? | Request, contract validation, optional live response |
| [06 · Architecture lab](06_architecture_and_training_lab.ipynb) | How could direct scoring and parallel questions work? | Attention-mask experiment, candidate scoring, loss curves |
| [07 · Text capstone](07_text_routing_capstone.ipynb) | Can I build and evaluate a complete local system? | Trained text router, held-out evaluation, error analysis |
| [08 · Solutions](08_exercises_and_solutions.ipynb) | Did I understand the ideas? | Worked answers and executable checks |

### 3. Learn only the math you need
**A vector** is an ordered list of numbers. **A matrix** is a rectangular table of them.
**A logit** is a score before normalization. **A probability distribution** assigns nonnegative
numbers summing to one across mutually exclusive alternatives. **A loss** measures how much we
want a prediction to change during learning. **A gradient** gives the local direction of change.

There is no need to understand transformers before lesson 1. Lesson 6 introduces attention with
small arrays; lesson 2 introduces the training math one operation at a time.

## Checks
Verify that the local teaching data and supporting files are present.
'''), code('''
from pathlib import Path
from lab_core import load_tickets
from collections import Counter
rows = load_tickets()
assert len({r['id'] for r in rows}) == len(rows)
assert len({r['text'] for r in rows}) == len(rows)
print('Fictional tickets:', len(rows))
print('Fixed splits:', dict(Counter(r['split'] for r in rows)))
print('Live API required for this course: no')
'''), md(r'''
## Next Steps
Start at [01](01_jev_basics.ipynb). For each “predict first” exercise, write down an answer before
running the experiment, then consult [08](08_exercises_and_solutions.ipynb). If you only read the
solutions, you miss the useful moment where the result disagrees with your intuition.

**Common misunderstandings to watch for:** type-safe does not mean correct; confidence does not mean
permission; normalization does not mean calibration; parallel execution does not mean statistical
independence; a working tutorial does not establish production performance.
''')])

    save('06_architecture_and_training_lab.ipynb', [md(r'''
# 6 · Architecture and training: what we can actually explain

## Goal
Connect the interface to concrete computational ideas while keeping the evidence boundary visible.
**35–45 minutes · intermediate.** Prerequisites: vectors, matrix multiplication, and softmax from lesson 2.

TypeSafe describes parallel question evaluation and decision-oriented training.
Its public overview does not supply the full architecture or RLCD algorithm.
[AI primer](https://docs.typesafe.ai/introduction/machine-learning-primer) ·
[Parallel questions pattern](https://docs.typesafe.ai/patterns/fan-out).

We will build **our own generic mechanisms**: score descriptions, isolate questions with an attention
mask, and compare objectives. These are demonstrations of possibilities, not claims about Jev's implementation.

## Setup
All computations use NumPy, random or author-chosen toy vectors, and no downloaded model weights.
'''), code(setup + '\nfrom lab_core import softmax'), md(r'''
## Steps
### 1. Fixed class heads versus scoring descriptions
The linear model in lesson 2 has one trained column per class. It cannot suddenly learn a fourth
class merely because you add a new name. An alternative pattern embeds **both the state and the
candidate description**, then computes compatibility. Changing descriptions changes the scored inputs.

The simple example below is only word overlap. A learned encoder or cross-encoder can be much
richer. [BERT](https://aclanthology.org/N19-1423/) is a primary example of a pretrained language
representation adapted for downstream classification; it is not evidence that Jev is BERT.
'''), code('''
from lab_core import vocabulary, vectorise
state = 'the export button crashes and the browser freezes'
descriptions = {
    'billing': 'invoice payment refund charge card',
    'technical': 'export button crashes browser freezes error',
    'account': 'login password email access verification',
}
# There is no fitting here: this vocabulary only defines common coordinates for a lexical demo.
vocab = vocabulary([state, *descriptions.values()])
state_vector = vectorise([state], vocab)[0]
candidate_vectors = vectorise(list(descriptions.values()), vocab)
overlap_scores = candidate_vectors @ state_vector
relative_weights = softmax(overlap_scores)
table(['Candidate', 'Shared-word count', 'Softmax weight (not calibrated)'],
      [(key, int(score), f'{p:.3f}') for key, score, p in zip(descriptions, overlap_scores, relative_weights)])
'''), md(r'''
### 2. Change the answer set
Softmax probabilities are relative to the available candidates. Duplicating a strong option divides
probability mass even though the evidence has not changed. This is a generic softmax property;
we are not asserting how Jev responds to duplicate descriptions.
'''), code('''
duplicate_scores = np.append(overlap_scores, overlap_scores[1])
duplicate_weights = softmax(duplicate_scores)
print('Technical weight before duplicate:', round(float(relative_weights[1]), 3))
print('Technical weight after duplicate:', round(float(duplicate_weights[1]), 3))
print('Duplicate technical weight:', round(float(duplicate_weights[-1]), 3))
assert duplicate_weights[1] < relative_weights[1]
'''), md(r'''
This explains why closed-set selection and “does any candidate fit?” are different questions.
If every option is poor, a normalized distribution still sums to one. Add a none-of-the-above
option or use a separate applicability test, and evaluate it on out-of-domain inputs.

### 3. An attention mechanism in one equation
For query vectors $Q$, key vectors $K$, and value vectors $V$:
$$\operatorname{Attention}(Q,K,V)=\operatorname{softmax}(QK^T/\sqrt{d}+M)V.$$
$QK^T$ scores compatibility. The mask $M$ is zero for allowed connections and $-\infty$ for blocked
ones. Softmax operates across keys in each row. This is the scaled dot-product attention pattern
from [Attention Is All You Need](https://arxiv.org/abs/1706.03762).

Our invented sequence contains four state tokens and two two-token question blocks. State tokens
read only state. Each question reads state and itself, never the other question. An autoregressive
causal mask instead allows each position to read only earlier positions and itself.
'''), code('''
state_length, question_length = 4, 2
length = state_length + 2 * question_length
allowed = np.zeros((length, length), dtype=bool)
allowed[:state_length, :state_length] = True
for start in [4, 6]:
    allowed[start:start+2, :state_length] = True
    allowed[start:start+2, start:start+2] = True
causal = np.tril(np.ones((length, length), dtype=bool))
labels = ['s0', 's1', 's2', 's3', 'qA0', 'qA1', 'qB0', 'qB1']
fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
for ax, mask, title in zip(axes, [causal, allowed], ['Generic causal mask', 'Our illustrative isolated-question mask']):
    ax.imshow(mask, cmap='Blues', vmin=0, vmax=1)
    ax.set_xticks(range(length), labels, rotation=45)
    ax.set_yticks(range(length), labels)
    ax.set(xlabel='Key: where information comes from', ylabel='Query: position receiving information', title=title)
    for row in range(length):
        for col in range(length):
            ax.text(col, row, str(int(mask[row,col])), ha='center', va='center',
                    fontsize=8, color='white' if mask[row,col] else GREY)
show_figure('06_attention_masks')
'''), md(r'''
### 4. Verify isolation by changing the other question
The next function is one attention layer with random, untrained weights. It is not a useful language
model. It lets us verify an information-flow claim exactly: changing question B must not change
question A's output under our mask. Remove the mask and that guarantee disappears.
'''), code('''
rng = np.random.default_rng(12)
dimension = 6
embeddings = rng.normal(size=(length, dimension))
Wq, Wk, Wv = [rng.normal(size=(dimension, dimension)) / np.sqrt(dimension) for _ in range(3)]

def attention(x, mask):
    q, k, v = x @ Wq, x @ Wk, x @ Wv
    scores = q @ k.T / np.sqrt(dimension)
    masked_scores = np.where(mask, scores, -np.inf)
    attention_weights = softmax(masked_scores)
    return attention_weights @ v

changed = embeddings.copy()
changed[6:] += 10
isolated_before = attention(embeddings, allowed)
isolated_after = attention(changed, allowed)
full_mask = np.ones_like(allowed)
full_before, full_after = attention(embeddings, full_mask), attention(changed, full_mask)
isolated_change = np.max(np.abs(isolated_before[4:6] - isolated_after[4:6]))
unmasked_change = np.max(np.abs(full_before[4:6] - full_after[4:6]))
print(f'Question A change with our mask: {isolated_change:.12f}')
print(f'Question A change with all connections: {unmasked_change:.4f}')
assert np.allclose(isolated_before[4:6], isolated_after[4:6])
assert not np.allclose(full_before[4:6], full_after[4:6])
'''), md(r'''
We also blocked state from reading questions. Otherwise question B could affect state in one layer
and reach question A through state in a later layer. Isolation must hold across the full computation,
not just the final row of one attention matrix. Whether a particular architecture caches, batches,
or computes these blocks efficiently is a separate implementation question.

### 5. Shared computation can reduce repeated work
Suppose state encoding costs $S$ units and each question costs $Q$ units. Repeating everything
for $m$ questions costs $m(S+Q)$. An idealized reusable state costs $S+mQ$.
This models work, not latency; parallel hardware does not make additional computation free.
'''), code('''
questions = np.arange(1, 17)
state_work, question_work = 100, 8
fig, ax = plt.subplots()
ax.plot(questions, questions * (state_work + question_work), 'o-', color=ORANGE, label='Repeat state for each question')
ax.plot(questions, state_work + questions * question_work, 's-', color=BLUE, label='Idealized shared state')
ax.set(xlabel='Number of questions', ylabel='Assumed work units', title='Sharing input work — conceptual, not a Jev benchmark', ylim=(0, 1800))
ax.legend()
show_figure('06_shared_work')
'''), md(r'''
### 6. Why rewarding only the chosen answer can overstate certainty
Let the true chance of a positive outcome be $q=0.7$. If your objective only rewards choosing the
correct binary label, reporting $p=0.51$ and $p=0.99$ produces the same “yes” action and expected
accuracy. A probabilistic loss also cares how certain you were.

The expected Brier loss is
$$L(p)=q(1-p)^2+(1-q)p^2=(p-q)^2+q(1-q).$$
Its unique minimum is at $p=q$. This is a derivation of a general proper scoring rule.
It helps explain the motivation for calibrated prediction, but does not reveal the RLCD loss or reward.
'''), code('''
true_rate = .7
reported = np.linspace(.001, .999, 500)
expected_brier = true_rate * (1-reported)**2 + (1-true_rate) * reported**2
expected_log_loss = -true_rate*np.log(reported) - (1-true_rate)*np.log(1-reported)
expected_accuracy = np.where(reported >= .5, true_rate, 1-true_rate)
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].plot(reported, expected_brier, color=BLUE, label='Expected Brier loss')
axes[0].plot(reported, expected_log_loss, color=ORANGE, linestyle='--', label='Expected log loss')
axes[0].axvline(true_rate, color=GREY, linestyle=':')
axes[0].set(xlabel='Reported probability p', ylabel='Expected loss', ylim=(0, 2), title='Probabilistic losses prefer honest probability')
axes[0].legend()
axes[1].plot(reported, expected_accuracy, color=BLUE)
axes[1].set(xlabel='Reported probability p', ylabel='Expected accuracy', ylim=(0,1), title='Label accuracy cannot distinguish 0.51 from 0.99')
show_figure('06_objectives')
'''), md(r'''
### 7. Place RLCD claims in context
RLHF uses human-preference signals; RLVR uses verifiable outcomes; TypeSafe describes RLCD as targeting
calibrated decisions. These are high-level objective descriptions, not complete mutually exclusive
training recipes. A real system may combine multiple training stages and losses.

Without the detailed RLCD algorithm we cannot specify its reward estimator, optimizer, sampling procedure,
or how its calibration generalizes. We can still test the externally visible contract and evaluate its outputs.

## Checks
'''), code('''
assert np.all(allowed.sum(axis=1) > 0)
assert np.isclose(expected_brier.min(), true_rate*(1-true_rate), atol=1e-5)
assert np.isclose(softmax(overlap_scores).sum(), 1)
print('Candidate normalization, attention isolation, and scoring-rule minimum checked.')
'''), md(r'''
## Next Steps
**Exercise 6:** Unblock question A's attention to question B and rerun the isolation test.
Predict which assertion will fail. Explain why “parallel” does not by itself imply “isolated.”

**Exercise 7:** For the assumed work model, derive the speedup in work units as $m$ grows very large.
Why should you avoid interpreting that limit as a promised wall-clock speedup?

Continue to the [text-routing capstone](07_text_routing_capstone.ipynb).
''')])

    save('07_text_routing_capstone.ipynb', [md(r'''
# 7 · Capstone: train, calibrate, route, and inspect failures

## Goal
Build a complete local text decision system: **text → features → probabilities → review policy → evaluation**.
**40–50 minutes · practical.** No API key, pretrained weights, or GPU required.

This is a small bag-of-words baseline, **not Jev**. Its limitations are part of the lesson.
The 54 tickets are authored fictional examples; performance is not a real-world benchmark.

**New question, new options:** this project routes to **billing, technical, or account**.
The introductory illustration used **billing, technical, or other**. Options belong to the task;
they are not fixed model categories. Here, `other` appears only as an out-of-domain stress label.

## Setup
The data file includes 24 training, 12 validation, 12 test, and 6 stress cases.
We fit vocabulary/weights on training, choose temperature/policy on validation, and evaluate once on test.
The stress set probes deliberately difficult inputs separately.
'''), code(setup + '''
from collections import Counter
from lab_core import (LABELS, WORD_ORDER_PAIR, load_tickets, vocabulary, vectorise, fit_linear, softmax,
                      nll, multiclass_brier, split_arrays, choose_temperature,
                      selective_metrics, confusion_counts)
rows = load_tickets()
'''), md(r'''
## Steps
### 1. Inspect examples and validate the split
![Training, validation, test, and stress have distinct roles. Counts come from the fictional course data.](assets/data-splits.svg)

The answer labels are for learning and evaluation, never model input. The small sample sizes mean
one test mistake changes accuracy by 8.3 percentage points. Do not treat the displayed decimals as precision.
'''), code('''
table(['Split', 'Count', 'Labels'], [(split, sum(r['split']==split for r in rows),
      dict(Counter(r['label'] for r in rows if r['split']==split)))
      for split in ['train','validation','test','stress']])
table(['Example', 'Text', 'Label'], [(r['id'],r['text'],r['label']) for r in rows[:3]])
assert len({r['id'] for r in rows}) == len(rows)
assert len({r['text'] for r in rows}) == len(rows)
assert all(r['label'] in LABELS for r in rows if r['split'] != 'stress')
'''), md(r'''
### 2. Turn text into visible features
A vocabulary maps training words to columns. Each entry is 1 if the word appears, otherwise 0.
This representation forgets word order, repeated occurrences, and most semantics.
“Export does not crash” and “export does crash” differ only by one feature for “not.”
Unknown words contribute no evidence. A modern language encoder is much richer.
'''), code('''
training = [r for r in rows if r['split']=='train']
vocab = vocabulary([r['text'] for r in training])
train_rows, X_train, y_train = split_arrays(rows, 'train', vocab)
validation_rows, X_validation, y_validation = split_arrays(rows, 'validation', vocab)
test_rows, X_test, y_test = split_arrays(rows, 'test', vocab)
print('Training vocabulary size:', len(vocab))
print('Training matrix:', X_train.shape)
print('Active words in first example:', [word for word,index in vocab.items() if X_train[0,index]])
'''), md(r'''
### 3. Train a regularized linear classifier
As in lesson 2, the loss is cross-entropy. We add $\lambda\lVert W\rVert^2/2$ so the model is penalized
for very large weights. Hyperparameters are fixed for this teaching example rather than selected on test.
The implementation is small enough to inspect in `src/lab_core.py`.
'''), code('''
weights, bias, training_loss = fit_linear(X_train, y_train)
fig, ax = plt.subplots()
ax.plot(training_loss, color=BLUE)
ax.set(xlabel='Gradient step', ylabel='Cross-entropy + L2 penalty', title='Training the local text baseline')
show_figure('07_text_training')
index_to_word = {index:word for word,index in vocab.items()}
table(['Class', 'Highest-weight training words'], [
    (label, ', '.join(index_to_word[i] for i in np.argsort(weights[:, k])[-6:][::-1]))
    for k,label in enumerate(LABELS)])
'''), md(r'''
### 4. Select temperature and review policy using validation only
Temperature minimizes validation log loss. The policy chooses a maximum-probability cutoff to minimize
validation cost: one unit per wrong automatic route, 0.2 per reviewed case, and zero per correct automatic route.
Review is assumed to resolve the case correctly. Ties prefer the first, lower cutoff in the grid.

Twelve validation examples are far too few for a dependable deployment threshold. This demonstrates
the procedure and its fragility. Fitting calibration and policy on the same small validation set can overfit it.
'''), code('''
validation_logits = X_validation @ weights + bias
temperature, temperature_grid, validation_losses = choose_temperature(validation_logits, y_validation)
validation_p = softmax(validation_logits, temperature)
candidate_cutoffs = np.linspace(.34, .99, 34)
policy_candidates = [selective_metrics(validation_p, y_validation, t) for t in candidate_cutoffs]
policy = min(policy_candidates, key=lambda result: result['cost'])
cutoff = policy['cutoff']
print(f'Chosen temperature: {temperature:.3f}; chosen cutoff: {cutoff:.3f}')
print('Validation policy:', policy)
if temperature in (temperature_grid[0], temperature_grid[-1]):
    print('Temperature hit the search boundary: do not interpret it as a well-determined optimum.')
'''), md(r'''
### 5. Evaluate the frozen system on test
The multiclass Brier score here **sums over classes before averaging over cases** (range 0–2).
That convention differs from the binary Brier score in lesson 3. Do not compare the raw values directly.
The majority-class baseline breaks training-count ties in label order.
'''), code('''
test_logits = X_test @ weights + bias
raw_p = softmax(test_logits)
test_p = softmax(test_logits, temperature)
predicted = test_p.argmax(axis=1)
majority = np.bincount(y_train, minlength=3).argmax()
table(['Method', 'Test accuracy', 'Test log loss', 'Multiclass Brier'], [
    ('Majority class', f'{np.mean(y_test==majority):.3f}', 'not a probability model', 'not computed'),
    ('Raw text classifier', f'{np.mean(raw_p.argmax(1)==y_test):.3f}', f'{nll(raw_p,y_test):.3f}', f'{multiclass_brier(raw_p,y_test):.3f}'),
    ('Temperature-scaled', f'{np.mean(predicted==y_test):.3f}', f'{nll(test_p,y_test):.3f}', f'{multiclass_brier(test_p,y_test):.3f}'),
])
test_policy = selective_metrics(test_p, y_test, cutoff)
print('Frozen policy on test:', test_policy)
print('Automatically routed denominator:', test_policy['automatic'], '/', test_policy['total'])
'''), md(r'''
With the delivered data and parameters, the classifier gets all 12 test cases right. That is a
statement about twelve short, authored examples with familiar topic words, not broad language ability.
The tiny validation set selects a temperature below 1, making predictions sharper. A larger,
representative set might select something different. The next stress tests expose what this score misses.

### 6. Inspect errors by class and by case
Rows in the confusion matrix are reference labels; columns are predictions. Counts are shown in
every cell. The per-case table keeps the text next to the model's uncertainty so you can inspect mistakes.
'''), code('''
matrix = confusion_counts(y_test, predicted)
fig, ax = plt.subplots(figsize=(6,4))
ax.imshow(matrix, cmap='Blues', vmin=0, vmax=max(1,matrix.max()))
ax.set_xticks(range(3), LABELS)
ax.set_yticks(range(3), LABELS)
ax.set(xlabel='Predicted class', ylabel='Reference class', title='Held-out test: 12 fictional tickets')
for row in range(3):
    for column in range(3):
        ax.text(column,row,str(matrix[row,column]),ha='center',va='center',fontsize=16,
                color='white' if matrix[row,column] > matrix.max()/2 else GREY)
show_figure('07_confusion')
table(['Text', 'Reference', 'Prediction', 'Max probability', 'Action'], [
    (r['text'], r['label'], LABELS[pred], f'{p.max():.3f}', 'auto-route' if p.max() >= cutoff else 'review')
    for r,pred,p in zip(test_rows,predicted,test_p)])
'''), md(r'''
### 7. Stress the assumptions
The six stress cases include negation, mixed intent, instruction-like text, and a request outside our
three trained labels. They are not representative samples, so report their cases rather than combining
them with test accuracy. The closed-set classifier must choose a known label even for “other.”
'''), code('''
stress = [r for r in rows if r['split']=='stress']
stress_X = vectorise([r['text'] for r in stress], vocab)
stress_p = softmax(stress_X @ weights + bias, temperature)
table(['Stress text', 'Intended topic', 'Predicted topic', 'Max probability'], [
    (r['text'],r['label'],LABELS[p.argmax()],f'{p.max():.3f}') for r,p in zip(stress,stress_p)])
print('Stress labels include other; the model has no other output column.')
'''), md(r'''
### 7b. Construct a failure the representation cannot solve
![The messages have different intended queues but identical binary features. Lost word order cannot be recovered by changing a threshold.](assets/word-order.svg)

These two messages contain the same words but negate different problems. A binary bag of words
maps them to exactly the same feature vector. No amount of training this same representation can
make it assign different outputs to the pair. At least one primary-topic answer must be wrong.
This is an architectural limitation of our baseline, not a measured Jev failure.
'''), code('''
minimal_pair = [message for message, _ in WORD_ORDER_PAIR]
pair_reference = [reference for _, reference in WORD_ORDER_PAIR]
pair_X = vectorise(minimal_pair, vocab)
pair_p = softmax(pair_X @ weights + bias, temperature)
table(['Message', 'Intended topic', 'Prediction'],
      [(message,reference,LABELS[p.argmax()]) for message,reference,p in zip(minimal_pair,pair_reference,pair_p)])
assert np.array_equal(pair_X[0], pair_X[1])
assert np.allclose(pair_p[0], pair_p[1])
print('Identical features force identical probabilities despite different intended meanings.')
'''), md(r'''
### 8. Inspect one prediction through its word contributions
For a linear model the logit equals the sum of active word weights plus bias. This is an exact
decomposition of our toy computation. It is not a causal explanation of a person's intent, and it
does not imply that an opaque model's natural-language explanation would be equally faithful.
'''), code('''
example_index = 2
chosen_class = int(predicted[example_index])
active = np.flatnonzero(X_test[example_index])
ordered = sorted(active, key=lambda i: abs(weights[i,chosen_class]), reverse=True)[:8]
print('Text:',test_rows[example_index]['text'])
table(['Word', 'Contribution to chosen-class logit'],
      [(index_to_word[i],f'{weights[i,chosen_class]:+.3f}') for i in ordered])
assert np.isclose(test_logits[example_index,chosen_class],
                  weights[active,chosen_class].sum()+bias[chosen_class])
'''), md(r'''
## Checks
'''), code('''
assert np.isfinite(test_p).all() and np.allclose(test_p.sum(axis=1),1)
assert np.array_equal(raw_p.argmax(axis=1), test_p.argmax(axis=1))
assert matrix.sum() == len(test_rows)
assert test_policy['automatic'] <= len(test_rows)
assert training_loss[-1] < training_loss[0]
print('Feature, probability, matrix, policy-denominator, and training checks passed.')
'''), md(r'''
## Next Steps
**Exercise 8:** Create an out-of-domain message using only unseen words. What feature vector reaches
the classifier? Why can softmax still return a normal-looking answer?

**Exercise 9:** Add bigram features to distinguish “not locked” from “locked.” Keep the split fixed.
Report what improves and what still fails; do not repeatedly tune on the test set.

**To replace this baseline with Jev:** keep labels hidden, reuse the three class definitions, record the
actual version and probabilities, then apply the same evaluation and policy procedure. The [API lesson](05_optional_real_jev_api.ipynb)
prepares a matching request without sending it. The dataset remains too small for production claims.
''')])

    save('08_exercises_and_solutions.ipynb', [md(r'''
# 8 · Worked exercises and explanations

## Goal
Check whether you can reason about the output contract, the math, and the software policy.
Try each exercise in its lesson before reading this notebook. These are worked solutions, not a graded test.

## Setup
This notebook is independent of previous kernels and makes no API calls.
'''), code(setup + '\nfrom lab_core import softmax'), md(r'''
## Steps
### 1. Choose a primitive
One queue → **Choice**. Explicit refund request → **Noul**. Ordered disruption levels → **Score**.
Writing an email requires generation; a bounded decision interface can choose a template or route
to a generative model, but cannot directly supply arbitrary new prose.

### 2. Shift and scale logits
Adding the same constant to every score cancels between numerator and denominator in softmax.
Multiplying by a positive constant preserves ranking, but changes concentration. A negative
multiplier would reverse ranking; multiplying by zero gives a uniform distribution.
'''), code('''
z = np.array([.2, 1.4, -.3])
assert np.allclose(softmax(z), softmax(z+100))
assert softmax(z).argmax() == softmax(3*z).argmax()
assert not np.allclose(softmax(z), softmax(3*z))
table(['Transformation', 'Probability vector'], [('original',softmax(z).round(3)),
      ('add 100',softmax(z+100).round(3)),('multiply by 3',softmax(3*z).round(3))])
'''), md(r'''
### 3. Derive the review region
“No” costs $p$, so it ties review at $p=0.2$. “Yes” costs $4(1-p)$, so it ties review at $p=0.95$.
Thus choose no below 0.2, review between 0.2 and 0.95, and yes above 0.95. At boundaries either tied
action has equal modeled cost. If review costs 0.8, the review region disappears except a three-way
tie at $p=0.8$: the best binary action already costs at most 0.8.
'''), code('''
def cheapest_action(p, review_cost):
    values = {'yes':4*(1-p),'no':p,'review':review_cost}
    return min(values,key=values.get)
table(['p','Review costs 0.2','Review costs 0.8'],
      [(p,cheapest_action(p,.2),cheapest_action(p,.8)) for p in [.1,.5,.9,.99]])
assert cheapest_action(.5,.2)=='review'
'''), md(r'''
### 4. Confidence is not authorization
A high topic probability is irrelevant to a required permission check. The application must enforce
the permission deterministically before action. The model can supply a recommendation, while code
enforces which recommendations are allowed to be acted on.
'''), code('''
def may_act(topic_probability, has_permission):
    return has_permission and topic_probability >= .9
assert may_act(.96,False) is False
assert may_act(.96,True) is True
'''), md(r'''
### 5. Avoid label leakage
The `label` field is the desired answer. Supplying it to the model lets the model copy the reference
instead of inferring it. A legitimate policy describes general rules available at deployment time;
it does not reveal this example's hidden answer. Restrict state to an explicit allowlist of input fields.
'''), code('''
row = {'text':'Please reset my password.','label':'account','split':'test'}
safe_state = {'customer_message':row['text']}
assert set(safe_state)=={'customer_message'}
print(safe_state)
'''), md(r'''
### 6. Explain the attention isolation test
Unblocking A→B lets A use B's key/value vectors, so perturbing B can change A. The equality assertion
will generally fail. “Parallel” describes scheduling; “isolated” describes allowed information flow.
State also must not absorb question information if it is reused across layers.

### 7. Work-sharing limit
The ratio is $m(S+Q)/(S+mQ)$. As $m$ tends to infinity, it approaches $(S+Q)/Q$.
For $S=100$, $Q=8$, the limit is 13.5. Memory bandwidth, latency, scheduling, and other overheads
are absent, so this does not establish a real model's speedup.
'''), code('''
S,Q = 100,8
print('Limit of the assumed work ratio:',(S+Q)/Q)
print('Ratio at 16 questions:',16*(S+Q)/(S+16*Q))
'''), md(r'''
### 8. An all-unknown input
With no recognized words, the feature vector is zero. The output is softmax of the bias alone.
Nothing in that operation detects that the request is out of domain.
'''), code('''
from lab_core import train_text_baseline, vectorise
_,vocab,weights,bias,_ = train_text_baseline()
unknown = vectorise(['quasar nebula supernova'],vocab)
assert unknown.sum()==0
assert np.allclose(softmax(unknown@weights+bias),softmax(bias))
print('Probabilities with zero recognized features:',softmax(bias).round(3))
'''), md(r'''
### 9. Bigram extension: one possible implementation
Append adjacent token pairs to the unigram features. This gives “not locked” a different feature
from “locked,” but only training examples can teach the model what that feature means.
Sparse bigrams do not solve language understanding or generalize automatically to all paraphrases.
'''), code('''
from lab_core import tokenise
def unigram_and_bigram_features(text):
    tokens = tokenise(text)
    return tokens + [a+'__'+b for a,b in zip(tokens,tokens[1:])]
print(unigram_and_bigram_features('My account is not locked'))
assert 'not__locked' in unigram_and_bigram_features('My account is not locked')
'''), md(r'''
## Checks
You should now be able to explain why each of these implications is false:

1. Valid schema ⇒ correct answer.
2. Higher probability ⇒ permission to act.
3. Good accuracy ⇒ good calibration.
4. Parallel questions ⇒ independent events.
5. One successful API call ⇒ production readiness.
6. A generic attention demo ⇒ Jev's published architecture.

## Next Steps
Pick your own bounded task, write the answer space, collect labeled examples, and establish a
simple baseline before increasing complexity. Keep test examples held out. Use real Jev calls only
when you want to measure Jev, and keep the model's predictions separate from your operating policy.

[Return to the course map](00_start_here.ipynb).
''')])
