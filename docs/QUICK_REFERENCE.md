# Keep this beside your notebook

Prefer diagrams first? Use [the visual guide](VISUAL_GUIDE.md), then return here for exact formulas.

## One decision in four steps

1. **Evidence:** what information should the judgment use?
2. **Question:** what exactly are we asking, and what do the allowed answers mean?
3. **Estimate:** what output did the model or scoring rule produce?
4. **Action:** what does our program do, given costs, uncertainty, and permissions?

Running example: an export crash is evidence; “Which queue?” is a question; probabilities are
estimates; routing or review is an application action.

## Choose a question type

| Need | Type | Remember |
|---|---|---|
| One category from named alternatives | Choice | The output includes a selected option and probabilities over the options. |
| A position on an ordered rubric | Score | The expected level can lie between rubric levels. |
| Whether a statement is true | Noul | The output is a probability for the positive answer. |

[Choice](https://docs.typesafe.ai/primitives/choice) · [Score](https://docs.typesafe.ai/primitives/score) ·
[Noul](https://docs.typesafe.ai/primitives/noul). Examples and formulas in this reference are teaching examples.

## Read three calculations

| Calculation | Plain-language reading | Worked example |
|---|---|---|
| Score = sum of level × probability | Average the possible levels using their probabilities. | 0 × 0.05 + 1 × 0.25 + 2 × 0.70 = **1.65** |
| Logit = sum of feature × weight + bias | Add the contributions to an option's score. | 2 × 0.8 + 1 × (−0.2) + 0.1 = **1.5** |
| Observed yes frequency = yes outcomes / cases | Count how often yes happened in that group. | 8 / 10 = **80%** |

A single group agreeing with its predicted frequency does not establish calibration across a population.

## Train a small model in PyTorch

The [PyTorch lab](../notebooks/10_pytorch_models_lab.ipynb) makes this loop visible:

**message → features or token IDs → logits → loss → gradients → updated weights**.

| Step | What to inspect | Common mistake |
|---|---|---|
| Prepare input | Vocabulary learned from training text; padding excluded where needed | Learning preprocessing from validation or test data |
| Predict | One raw logit per class; shape `[batch, 3]` for this task | Treating logits as probabilities |
| Compute loss | `CrossEntropyLoss(logits, labels)` with integer class labels | Applying softmax before this loss, which already combines log-softmax and negative log likelihood |
| Update | Clear old gradients, call `loss.backward()`, then `optimizer.step()` | Accidentally accumulating gradients across independent steps |
| Validate | `model.eval()` with gradient tracking disabled | Leaving dropout active or choosing an epoch using test loss |
| Evaluate | Load the validation-selected checkpoint and assess the frozen system | Keeping the seed or model settings with the best test result |

Use softmax when displaying the predicted distribution, after computing raw logits. A training
loss curve shows fit; it does not by itself establish test accuracy or calibration.

## Choose an action using costs

In the binary teaching example, correct actions cost zero and review is perfectly accurate.
If `p` is the calibrated probability of yes:

| Action | Expected cost |
|---|---|
| Act yes | (1 − p) × false-positive cost |
| Act no | p × false-negative cost |
| Review | Review cost |

At p = 0.90, false-positive cost = 4, false-negative cost = 1, and review cost = 0.20,
the costs are **0.40**, **0.90**, and **0.20**. Review is cheapest under these assumptions.
Real review can make mistakes; evaluate that behavior before using the same rule.

## Keep these distinctions clear

| Common confusion | What to say instead | Revisit |
|---|---|---|
| The output is allowed, so it is right. | Validity checks the form; accuracy checks the judgment. | 01, 04 |
| The largest probability grants permission. | The application enforces permissions separately. | 04 |
| A normalized distribution is calibrated. | Calibration requires comparison with outcomes. | 03 |
| A similarity of 0.80 means 80% correct. | Similarity is a geometric score with a different meaning. | 09 |
| Review makes error vanish. | Review is an action with its own accuracy and cost. | 03 |
| Parallel evaluation makes events independent. | Scheduling and statistical independence are different. | 04, 06 |
| Better-looking test results justify more tuning. | Use validation for tuning; assess a frozen system on fresh test data. | 07 |
| The toy reveals Jev's architecture. | The toy establishes a property of our constructed example. | 06, 09 |

## Evaluate with explicit denominators

- **Label accuracy:** correct classifier labels / evaluated cases, before applying a review policy.
- **Automatic coverage:** automatic cases / all cases.
- **Selective error:** wrong automatic cases / automatic cases.
- **Review rate:** reviewed cases / all cases.
- **Both-correct pair rate:** pairs with both labels correct / evaluated pairs.

When there are no automatic cases, selective error is undefined, rather than evidence of zero
error. A tiny authored test set can illustrate calculations but cannot establish broad reliability.

**Probability losses have their own definitions:** log loss averages `−log(p of the reference class)`
over cases. The binary Brier score averages `(p − y)²` and ranges from 0 to 1. The multiclass
Brier convention in our labs sums squared errors across classes before averaging over cases,
so its range is 0 to 2. Do not compare these raw Brier values as though the conventions were equal.
Both losses measure probabilistic prediction quality, including factors beyond calibration.

For several random seeds, show each result and a summary across those runs. That spread describes
training variability on the fixed dataset; it is not a confidence interval for future accuracy.
Once test results guide another change, that test set has become development data. Reserve fresh
examples for the next independent assessment.

## Study without getting lost

Start with **00 → 01 → 04** for the main idea. Use **02 → 03 → 07** to build a local system.
Try **09** to compare mechanisms, then **10** to train small PyTorch models. In the optional HTML
exports, use the code toggle to read explanations first, then inspect the Python when ready.

For an experiment: **predict → change one thing → restart and run → explain → state a limitation**.

[Course home](../README.md) · [Guided practice](PRACTICE.md) · [Model guide](MODEL_GUIDE.md) · [Glossary](GLOSSARY.md)
