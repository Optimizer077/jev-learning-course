# Teaching data

`tickets.json` contains 54 author-written fictional English support tickets: 24 training,
12 validation, 12 test, and 6 stress examples. No customer records or Jev outputs are included.

The three classes are billing, technical, and account. The labels express the author's
intended primary routing topic; mixed-topic labels are inherently policy-dependent.
These are the project options. The introductory illustration uses billing, technical, and other
to show that a Choice's options come from its question, rather than a fixed universal label list.
Stress cases deliberately include negation, mixed intent, irrelevant instructions, and an
out-of-domain request. The out-of-domain row uses `other`, outside the trained classes.

Splits are fixed before fitting. The vocabulary and weights use training only; temperature
and routing policy use validation only; test is reserved for the final evaluation. This
tiny, manually authored dataset is not representative of real support traffic. Shared topic
words make it deliberately approachable, while unseen wording exposes the baseline's limits.
Do not use its accuracy to compare Jev with any other model.

See [the split diagram](../docs/VISUAL_GUIDE.md#keep-fitting-tuning-and-testing-separate)
before running the project. The figure's counts are read from this JSON file when rebuilt.

## Separate PyTorch toy task

`torch_toy.json` contains **864 authored synthetic sentences** for lesson 10: **520 train,
172 validation, and 172 test**. These are generated learning inputs, separate from `tickets.json`.
There are 432 reversed sentence pairs. Both partners stay in the same split and have different
reference queues. Training uses 260 pairs; validation and test use 86 each.

The task identifies the issue described as failing, using three billing terms, three technical
terms, three account terms, four grammatical templates, and four prefixes. Swapping the two issue
terms changes the reference label while preserving the complete token counts. The split is fixed
with seed 314 at the pair level. Vocabulary fitting uses training text only; labels and split IDs
are never text features. The checked generator is `scripts/build_torch_dataset.py`, with its
construction and models in `src/torch_lab.py`.

Templates and issue words are shared across splits. This tests held-out combinations within an
authored grammar, not unseen grammar or realistic support traffic. No real customer records,
Jev responses, pretrained weights, or external corpus are included. Perfect toy-task accuracy
would not establish general language understanding. See [lesson 10](../notebooks/10_pytorch_models_lab.ipynb)
and [Assignment 4](../assignments/04_compare_torch_models.md).
