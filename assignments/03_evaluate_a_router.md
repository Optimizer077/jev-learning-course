# Assignment 3 · Evaluate a router

**Preparation:** [03](../notebooks/03_calibration_and_decisions.ipynb) and
[07](../notebooks/07_text_routing_capstone.ipynb). Reading saved outputs is enough for the core task.

## Your task

1. Identify what the project fits on training, chooses on validation, and measures on test.
2. Report the delivered test results with denominators. Separate classification accuracy from
   automatic coverage and error among automatic routes.
3. Read the two messages “The payment failed, not the export.” and “The export failed, not the payment.”
   Explain their intended labels and why the current representation cannot distinguish them.
4. Choose another stress case. Describe the model's estimate, the policy's action, and the limitation you see.
5. Write a five-sentence evaluation note: the task, dataset size and source, observed result,
   an important limitation, and a next evaluation step.

## Result template

| Quantity | Numerator / denominator | What population does it describe? |
|---|---|---|
| Classification accuracy | Fill in from the saved output | |
| Automatic coverage | | |
| Error among automatic cases | | |

Do not fill an undefined denominator with zero. Describe it explicitly.

## Success criteria

- Use the actual saved result and its denominator.
- Keep reference labels out of prediction input.
- Explain how a feature limitation creates the minimal-pair failure.
- Distinguish fictional teaching data from real customer traffic.
- Propose new held-out examples for assessment rather than repeatedly tuning on the existing test set.

<details><summary>Optional coding extension</summary>
<p>Inspect a different message's word contributions, or create a new stress pair. Keep the original
test split fixed. If you tune a model or policy after inspecting test cases, record that change and
reserve fresh cases for the next assessment.</p>
</details>

For another view, compare methods in [lesson 09](../notebooks/09_related_models_lab.ipynb).

[All assignments](README.md) · [Course outline](../docs/COURSE.md)
