# Assignment 4 · Compare PyTorch models

**Preparation:** [02 · From scratch](../notebooks/02_decision_model_from_scratch.ipynb),
[07 · Text routing](../notebooks/07_text_routing_capstone.ipynb), and
[10 · PyTorch models lab](../notebooks/10_pytorch_models_lab.ipynb).
Reading saved outputs is enough for the core task. The optional experiment requires PyTorch and a CPU.

**What you will make:** a short comparison note explaining the task, inputs, training procedure,
observed results, and limits. Use the actual saved values; there is no required winning model.

## Begin with one sentence pair

Read “The payment failed, not the export” and “The export failed, not the payment.”
Write the intended class for each. Name the words shared by both messages and the information
that changes when their order changes.

Before reading the comparison, predict whether each model can distinguish the pair:

| Model | What it receives | Your prediction and reason |
|---|---|---|
| Bag-of-words linear classifier | Word-presence features | |
| Bag-of-words MLP | The same word-presence features | |
| Mean-embedding classifier | An average of learned token embeddings | |
| Small 1D CNN | A sequence of learned token embeddings | |
| GRU | A sequence of learned token embeddings | |
| Tiny Transformer | Token embeddings with position information | |

Separate **can represent the distinction** from **did learn it in this run**. You will check the
second question using saved predictions. Do not change your written prediction after seeing them.

## Trace one training update

Explain these five steps in one sentence each:

1. The model turns its input into class scores, also called logits.
2. The loss compares those scores with the reference label.
3. `backward()` computes how each trainable weight affects the loss.
4. The optimizer updates the weights; the next prediction may change.
5. Validation chooses a checkpoint without updating weights on validation examples.

Find the corresponding operations in the lesson. State why the loss receives logits and why the
reference label is used during training but must not be given to the prediction function as evidence.

## Inspect the experiment before reporting a score

Record the dataset source, exact split sizes, class names, and training seeds from the notebook.
Identify the checks that reject duplicate texts and keep reversed sentence pairs in a single split.
Explain which data supplies the vocabulary and which data selects the saved checkpoint.

Then fill this table for **all six models**, using the delivered comparison. Keep the seed variation
beside the average. State the common test denominator rather than reporting a bare percentage.

| Model | Test accuracy and denominator | Variation across seeds | Pair result or one observed failure |
|---|---|---|---|
| Bag-of-words linear | | | |
| Bag-of-words MLP | | | |
| Mean embeddings | | | |
| CNN | | | |
| GRU | | | |
| Transformer | | | |

Use the loss curves to describe one training pattern. If a model gets the toy test right, say
“on these generated test sentences,” then identify a capability this test does not measure.
If two models tie, report the tie. Training time and parameter counts describe this experiment;
neither is a general measure of intelligence.

## Write your comparison note

Use five sentences: the task and source; the split and checkpoint rule; the observed comparison;
one representation or training limitation; and the fresh evidence needed for a broader claim.
Include the distinction between these models and Jev: this lab uses general ML mechanisms and
authored synthetic data, not Jev's weights or unpublished training method.

## Success criteria

- Explain why identical word-presence inputs produce identical deterministic predictions even through an MLP.
- Distinguish the architecture's available information from what training actually learned.
- Trace a weight update and keep training, validation, and test roles separate.
- Report all six models, seeds, and denominators instead of selecting the most flattering run.
- State that shared generation patterns remain across splits; grouped pairs alone do not prove broad generalization.
- Describe one limitation and propose fresh held-out examples for a future assessment.

<details><summary>A hint for the input-information question</summary>
<p>If two messages become the same vector, every later deterministic layer receives the same input.
Changing that layer's size cannot restore the missing order. An unpositioned mean of the same token
embeddings is also unchanged by token order. A sequence model has access to more information, but
still needs enough suitable training to use it.</p>
</details>

## Optional: one controlled experiment

Choose one model and one change, such as a smaller training subset or fewer training epochs.
Write your prediction first, keep the original split assignment fixed, then inspect training and
validation results across the same seeds. Record the changed setting and any data-selection seed.
Do not use the original test scores to choose a favorable change.

After selecting a change, describe what fresh test examples you would reserve to assess it.
If you already inspected those test examples while tuning, disclose that and do not treat their
score as an untouched final assessment.

[All assignments](README.md) · [Study plan](../docs/LEARNING_GUIDE.md) · [Course outline](../docs/COURSE.md)
