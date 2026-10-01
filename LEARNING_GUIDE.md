# A learning plan you can finish in small sessions

Choose the first session for an introduction. Add the next two when you want to understand the
calculations or build something. Times below are study estimates; take longer when an idea is new.

## Session 1: explain one decision

**Suggested time: 15–25 minutes. No coding required.**

1. Read [00 · Start here](00_start_here.ipynb). Explain the difference between an estimate and an action.
2. Read the plain-language introduction, question-type table, and sections 1–5 in
   [01 · Jev basics](01_jev_basics.ipynb). Skip equations if they interrupt your understanding.
3. Try questions 1–8 in [guided practice](PRACTICE.md). You can finish the last four later.
4. Read the main workflow in [04 · Workflows](04_workflows_and_related_models.ipynb).

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

1. In [02 · A model from scratch](02_decision_model_from_scratch.ipynb), begin with the handmade
   calculation. Follow two feature contributions, the bias, the score, and the probability.
2. Read sections 1–4 to see how training changes weights. Keep the gradient check for another session.
3. In [03 · Calibration](03_calibration_and_decisions.ipynb), start with ten invented outcomes.
   Then read the reliability diagram and its denominators.
4. In the [playground](playground.html), predict the effect of changing temperature. Then change
   the review cost while keeping the probability fixed.

**Your checkpoint:** explain why the winning label can stay the same while probabilities change,
and why the most likely outcome need not be the cheapest action.

If you run cells, follow [SETUP.md](SETUP.md). Change one parameter, predict, rerun, and explain.
Keep the complete folder together and use Restart Kernel and Run All for a fresh result.

## Session 3: build and inspect a small system

**Suggested time: 45–60 minutes. Basic Python and sessions 1–2 help.**

1. Run [07 · Text routing](07_text_routing_capstone.ipynb) with its original settings.
2. Identify what is fitted on training, selected on validation, and measured on test.
3. Read the stress cases and the two messages with identical bag-of-words features.
4. Finish guided-practice questions 9–12, then choose one exercise in
   [08 · Worked exercises](08_exercises_and_solutions.ipynb).

**Your checkpoint:** describe one failure, its cause, and what evidence you would need before
using the system on real messages. Include the test denominator when mentioning accuracy.

For deeper mechanisms, continue to [06 · Architecture lab](06_architecture_and_training_lab.ipynb).
For a real request, continue to [05 · Optional API](05_optional_real_jev_api.ipynb).
For a side-by-side local comparison, continue to [09 · Related-models lab](09_related_models_lab.ipynb).
Use the [quick reference](QUICK_REFERENCE.md) for definitions, calculations, and common confusions.

## When an idea feels difficult

| If you are stuck on… | Try this |
|---|---|
| The symbols | Read the words beside them, then calculate one row by hand. |
| The code | Hide it in the browser and inspect the saved result first. |
| An incorrect practice answer | Explain why the tempting answer fails; follow the lesson link. |
| A surprising result | Check the denominator, data split, and stated assumptions. |
| Which model did what | Label the claim: documented Jev behavior, general ML mechanism, or invented teaching example. |

You are making progress when you can predict a small change and explain a limitation. Rerunning
cells is useful, but the explanation is the stronger check.

## For study groups or instructors

Use [PRACTICE.md](PRACTICE.md) as a printable companion. Let people answer alone first, compare
reasoning in pairs, then reveal the explanation. Ask “What information did the model receive?”
and “Which part is our application rule?” throughout the support-message example.

For the numeric lab, have learners calculate one score on paper before revealing the table.
For the project, discuss the word-order failure even when time is too short to run training.
Let learners finish at a checkpoint instead of rushing through every notebook.

[Course home](README.md) · [Guided practice](PRACTICE.md) · [Glossary](GLOSSARY.md)
