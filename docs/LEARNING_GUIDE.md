# A learning plan you can finish in small sessions

Choose the first session for an introduction. Add the next two when you want to understand the
calculations or build something. Times below are study estimates; take longer when an idea is new.

The lesson numbers are reference labels: you do not need to finish every notebook in order.
Start with one outcome and stop when you can explain it in your own words.

| Your goal today | Follow this route | You have finished when… |
|---|---|---|
| Understand Jev without coding | Session 1 | You can separate a question, an estimate, and an action. |
| Understand probabilities and training | Sessions 1–2 | You can trace one prediction and explain a probability's limits. |
| Build a small text router | Sessions 1–3 | You can report a held-out result and explain one failure. |
| Train several PyTorch models | Session 4 after lessons 02 and 07 | You can compare models without tuning on the test set. |

Reading the saved outputs counts as learning. Running the code is a separate choice; use
[setup help](SETUP.md) when you are ready. Keep the [visual guide](VISUAL_GUIDE.md) beside
the lesson if the written explanation feels abstract.

## Session 1: explain one decision

**Suggested time: 15–25 minutes. No coding required.**

1. Read [00 · Start here](../notebooks/00_start_here.ipynb). Explain the difference between an estimate and an action.
2. Read the plain-language introduction, question-type table, and sections 1–5 in
   [01 · Jev basics](../notebooks/01_jev_basics.ipynb). Skip equations if they interrupt your understanding.
3. Try questions 1–6 in [guided practice](PRACTICE.md).
4. Read the main workflow in [04 · Workflows](../notebooks/04_workflows_and_related_models.ipynb).
   Then try question 7. Save calibration and cost questions 8–9 for session 2.

**Your checkpoint:** given an export-crash message, choose a question type, name the evidence,
and say what the program should do if the estimate is uncertain.

Write your own answer to this small design problem:

> A customer says, “My invoice is wrong and the export button is broken.” Your application needs
> a primary queue, a disruption level, and whether a refund was explicitly requested.
> What are the three questions? Which answer types fit?

<details><summary>One possible design</summary>
<p>Ask a Choice for the primary queue with clear criteria; a Score for disruption with ordered
rubric levels; and a Noul for an explicit refund request. The message supplies evidence. Your
policy can ask for review when one primary queue cannot adequately represent a multi-issue message.</p>
</details>

## Session 2: trace the numbers

**Suggested time: 30–45 minutes. Reading saved results is enough; basic Python helps with edits.**

1. In [02 · A model from scratch](../notebooks/02_decision_model_from_scratch.ipynb), begin with the handmade
   calculation. Follow two feature contributions, the bias, the score, and the probability.
2. Read sections 1–4 to see how training changes weights. Keep the gradient check for another session.
3. In [03 · Calibration](../notebooks/03_calibration_and_decisions.ipynb), start with ten invented outcomes.
   Then read the reliability diagram and its denominators.
4. In the [playground](../site/playground.html), predict the effect of changing temperature. Then change
   the review cost while keeping the probability fixed.
5. Try guided-practice questions 8–9 and explain the cost assumptions.

**Your checkpoint:** explain why the winning label can stay the same while probabilities change,
and why the most likely outcome need not be the cheapest action.

If you run cells, follow [SETUP.md](SETUP.md). Change one parameter, predict, rerun, and explain.
Keep the complete folder together and use Restart Kernel and Run All for a fresh result.

## Session 3: build and inspect a small system

**Suggested time: 45–60 minutes. Basic Python and sessions 1–2 help.**

1. Run [07 · Text routing](../notebooks/07_text_routing_capstone.ipynb) with its original settings.
2. Identify what is fitted on training, selected on validation, and measured on test.
3. Read the stress cases and the two messages with identical bag-of-words features.
4. Finish guided-practice questions 10–12, then choose one exercise in
   [08 · Worked exercises](../notebooks/08_exercises_and_solutions.ipynb).

**Your checkpoint:** describe one failure, its cause, and what evidence you would need before
using the system on real messages. Include the test denominator when mentioning accuracy.

For deeper mechanisms, continue to [06 · Architecture lab](../notebooks/06_architecture_and_training_lab.ipynb).
For a real request, continue to [05 · Optional API](../notebooks/05_optional_real_jev_api.ipynb).
For a side-by-side local comparison, continue to [09 · Related-models lab](../notebooks/09_related_models_lab.ipynb).
Use the [quick reference](QUICK_REFERENCE.md) for definitions, calculations, and common confusions.

## Session 4: train several models and compare fairly

**Suggested time: 45–75 minutes. Optional. Basic Python and lessons 02 and 07 help.**
Reading the saved comparison is enough for the core questions. PyTorch is required to run training;
a CPU is sufficient. These experiments start with small randomly initialized models, not downloaded
language-model weights.

1. Open [10 · PyTorch models lab](../notebooks/10_pytorch_models_lab.ipynb). Read the task and
   source label first: its authored synthetic sentences are a new dataset, separate from the 54 tickets.
2. Read one reversed sentence pair. Predict which models can distinguish it before looking at results.
3. Inspect the split checks. Vocabulary comes from training; reversed pairs stay in the same split.
   Validation selects training checkpoints; the frozen comparison uses test data afterward.
4. Follow one training loop: input → scores → loss → gradients → weight update.
   You can skip the deeper layer code on your first pass.
5. Compare all six models and all reported seeds. Read accuracy with the test denominator,
   inspect the pair result, and explain what the loss curves show.
6. Complete [Assignment 4 · Compare PyTorch models](../assignments/04_compare_torch_models.md).

**Your checkpoint:** explain why adding a nonlinear layer to the same word-presence features
cannot recover lost word order, and why a high score on generated sentences is not evidence of
general language understanding.

The six models serve different teaching purposes: two use bag-of-words features, one averages
token embeddings, and three preserve sequence information through a CNN, GRU, or Transformer
with position embeddings. Access to word order helps only if the training procedure learns to use it.
Do not assume a model will succeed just because its architecture can represent the distinction.

## Keep a four-line experiment note

First run or read the delivered settings. Then choose **one** change and predict its effect.
Keep the original test results as a reference; use validation to investigate a changed setting.

| Write down… | Example |
|---|---|
| My change | Reduce the training examples; leave the model and split seed fixed. |
| My prediction | Validation loss may increase because the model sees fewer examples. |
| What happened | Copy the observed value, seed, split, and denominator. |
| My explanation and limit | Describe the pattern; a single run is not a general model ranking. |

If you use a test result to decide the next change, that test has become development data.
Record that explicitly and reserve fresh held-out cases for a later assessment.

## When an idea feels difficult

| If you are stuck on… | Try this |
|---|---|
| The symbols | Read the words beside them, then calculate one row by hand. |
| The code | Read the paragraph and saved result first; use the optional HTML copy's code toggle if helpful. |
| An incorrect practice answer | Explain why the tempting answer fails; follow the lesson link. |
| A surprising result | Check the denominator, data split, and stated assumptions. |
| Which model did what | Label the claim: documented Jev behavior, general ML mechanism, or invented teaching example. |
| A model-comparison table | Find the task, data source, split, denominator, training budget, and seeds before choosing a favorite. |

You are making progress when you can predict a small change and explain a limitation. Rerunning
cells is useful, but the explanation is the stronger check.

## For study groups or instructors

Use [PRACTICE.md](PRACTICE.md) as a printable companion. Let people answer alone first, compare
reasoning in pairs, then reveal the explanation. Ask “What information did the model receive?”
and “Which part is our application rule?” throughout the support-message example.

For the numeric lab, have learners calculate one score on paper before revealing the table.
For the project, discuss the word-order failure even when time is too short to run training.
Let learners finish at a checkpoint instead of rushing through every notebook.

For the PyTorch lab, assign one model to each pair of learners. Have them explain what information
their model receives, then compare the saved results together. Ask “Could this model represent the
distinction?” before “Did this training run learn it?” Keep those two questions separate.

[Course home](../README.md) · [Guided practice](PRACTICE.md) · [Glossary](GLOSSARY.md)
