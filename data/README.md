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
