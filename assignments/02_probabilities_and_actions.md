# Assignment 2 · Probabilities and actions

**Preparation:** [02](../notebooks/02_decision_model_from_scratch.ipynb) and
[03](../notebooks/03_calibration_and_decisions.ipynb). You can calculate by hand or use a notebook.

All values below are invented teaching examples.

## Your task

1. Compute the expected score for levels 0, 1, and 2 with probabilities 0.05, 0.25, and 0.70.
   Explain how the expectation differs from the most likely level.
2. Compute a logit from features 2 and 1, weights 0.8 and −0.2, and bias 0.1.
   Explain why this result is not yet a probability.
3. Ten cases each receive a predicted yes probability of 0.80. Eight outcomes are yes.
   Calculate the observed frequency and explain why this single group does not establish calibration.
4. With p(yes) = 0.90, false-positive cost = 4, false-negative cost = 1, and perfect-review cost = 0.20,
   compare expected costs for yes, no, and review. Correct automatic actions cost zero.
5. Change review cost to 0.80. Choose an action again and explain why the probability stayed the same.
6. Name two assumptions that could fail in a real system.

## Success criteria

- Show the multiplication and addition, rather than only final numbers.
- Distinguish scores, probabilities, observed frequencies, and actions.
- Identify the effect of sampling variation.
- Choose the action with the lowest expected cost under the stated assumptions.
- State that calibration, costs, and reviewer behavior need evaluation.

<details><summary>Hint: expected action costs</summary>
<p>Compare (1 − p) × false-positive cost, p × false-negative cost, and review cost.
Use the quick reference after attempting the calculations.</p>
</details>

Check your reasoning with [the quick reference](../docs/QUICK_REFERENCE.md) and
[the worked notebook exercises](../notebooks/08_exercises_and_solutions.ipynb).

[All assignments](README.md) · [Course outline](../docs/COURSE.md)
