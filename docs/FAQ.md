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

No. The local models are transparent NumPy classifiers. They explain scores, probabilities,
learning, calibration, and routing. They do not reproduce Jev's weights, proprietary training
recipe, architecture, or reported performance. Lesson 06 labels its mechanisms as illustrations.

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

## Do I need a Jev account, GPU, or internet connection?

No Jev account or GPU is needed for local lessons. Package installation requires internet; exported
formulas may use a MathJax CDN. Colab needs a Google sign-in when prompted and internet for the initial
course download. The optional live call in lesson 05 needs a Jev key and network access; it is disabled
in the supplied notebook. See [setup](SETUP.md).

## How should I use the exercises?

Predict or explain the result before revealing an answer. Try the self-check at the end of each
lesson, then a relevant exercise in lesson 08. Explain why the result happens and when the
conclusion would fail, rather than only giving a number.

## I changed a setting. Why did the answer change?

That is the purpose of an experiment. Change one parameter at a time and rerun from a clean kernel.
Saved conclusions and checks describe the delivered settings; deliberate changes can require a
different interpretation or expected value.

[Course home](../README.md) · [Setup help](SETUP.md) · [Glossary](GLOSSARY.md)
