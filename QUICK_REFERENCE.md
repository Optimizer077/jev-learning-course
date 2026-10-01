# Keep this beside your notebook

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

- **Accuracy:** correct labels / evaluated cases.
- **Automatic coverage:** automatic cases / all cases.
- **Selective error:** wrong automatic cases / automatic cases.
- **Review rate:** reviewed cases / all cases.

When there are no automatic cases, selective error is undefined, rather than evidence of zero
error. A tiny authored test set can illustrate calculations but cannot establish broad reliability.

## Study without getting lost

Start with **00 → 01 → 04** for the main idea. Use **02 → 03 → 07** to build a local system.
Try **09** when you want to compare mechanisms. Use the browser's code toggle to read explanations
first, then inspect the Python when ready.

For an experiment: **predict → change one thing → restart and run → explain → state a limitation**.

[Course home](README.md) · [Guided practice](PRACTICE.md) · [Model guide](MODEL_GUIDE.md) · [Glossary](GLOSSARY.md)
