# Questions you may have

## Is this an official Jev course?

No. It is an independent educational course based on linked public documentation. TypeSafe AI
provides Jev; this folder provides explanations and experiments. [SOURCES.md](SOURCES.md)
distinguishes provider descriptions from general ML concepts and authored examples.

## Do I need to know Python or machine learning?

Not for the beginner reading path: 00 → 01 → 04. Read the explanations and saved results, then
try the playground. Running the mathematical experiments is easier with basic Python.
You can return to those lessons later.

## Does the code implement Jev?

No. The course includes transparent NumPy classifiers and, in lesson 10, small PyTorch models
trained from scratch. They explain scores, probabilities, learning, calibration, representations,
and routing. They do not reproduce Jev's weights, proprietary training recipe, architecture, or
reported performance. Lesson 06 labels its mechanisms as illustrations.

## What does “typed” mean here?

It describes the form of the answer. For example, a Choice question asks for a distribution over
specified options. That helps software consume outputs. It does not guarantee that the selected
answer is true, safe, or appropriate to act on.

## Is the largest probability the same as Jev's confidence field?

Do not assume that. The course calls the largest class probability exactly that. Entropy measures
how spread out a distribution is. Neither is presented as the provider's confidence formula.
See the linked official confidence documentation for its stated meaning.

## Why are there notebooks and HTML pages?

HTML lets you read immediately. Turn on **Show Python code** to inspect the implementation.
Notebooks let you execute and change it. Editing a notebook does not update its exported HTML page.

## Why does the text project look so accurate?

Its 54 messages are authored, tiny, and deliberately simple. The splits are separate but come from
the same narrow teaching design. The minimal-pair example exposes a failure: bag-of-words features
lose word order. These results are not a Jev benchmark or evidence of readiness for real customers.

## Why train six PyTorch models on another toy dataset?

[Lesson 10](../notebooks/10_pytorch_models_lab.ipynb) makes a controlled comparison: identify which
issue failed when a sentence names two issues. Reversing “The payment failed, not the export”
changes its meaning while leaving the bag of words unchanged. That exposes a limit of the
representation, even if you add more training or a nonlinear layer.

The linear model and MLP receive word-presence features; averaged token embeddings also discard
order. The CNN, GRU, and Transformer with position embeddings receive sequence information.
The lab reports what these particular training runs learned. A model's capacity to use order is
different from evidence that it successfully learned this task.

The sentences are authored synthetic data, generated for teaching. They are separate from the
54-ticket project and do not establish a general ranking of neural models. Compare all reported
seeds and inspect failures, not just the highest accuracy.

## Why are reversed sentence pairs kept in one split?

They are closely related examples. Keeping each pair together prevents its counterpart from
appearing in training while the reversed wording appears in validation or test. The split checks
also reject duplicate text across splits. Other shared templates and topic words remain in the
generator, so this is still a controlled toy test, not a test of broad language generalization.

## Do more parameters guarantee better predictions?

No. More parameters change what a model can represent and how it learns, but data, training
budget, initialization, and evaluation all matter. Compare the delivered results under their
stated settings. A larger model cannot recover information removed before its input, and a tiny
synthetic dataset cannot prove that an architecture is best for a real application.

## Do I need a Jev account, GPU, or internet connection?

No Jev account or GPU is needed for local lessons. Package installation requires internet; exported
formulas may use a MathJax CDN. Colab needs a Google sign-in when prompted and internet for the initial
course download. The optional live call in lesson 05 needs a Jev key and network access; it is disabled
in the supplied notebook. See [setup](SETUP.md).

Lesson 10 additionally needs PyTorch to run; reading its saved results requires no installation.
Its models train locally on a CPU without an API key or pretrained-weight download. Initial
package installation may download a substantial wheel and still needs internet.

## How should I use the exercises?

Predict or explain the result before revealing an answer. Try the self-check at the end of each
lesson, then a relevant exercise in lesson 08. Explain why the result happens and when the
conclusion would fail, rather than only giving a number.

## I changed a setting. Why did the answer change?

That is the purpose of an experiment. Change one parameter at a time and rerun from a clean kernel.
Saved conclusions and checks describe the delivered settings; deliberate changes can require a
different interpretation or expected value.

For a training experiment, record the setting and seed before comparing results. Select changes
using training and validation data. If test results influence your next change, note that the test
set is now development data and use fresh held-out cases for the next assessment.

[Course home](../README.md) · [Setup help](SETUP.md) · [Glossary](GLOSSARY.md)
