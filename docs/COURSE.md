# Course outline

[Course home](../README.md) · [Setup](SETUP.md) · [Assignments](../assignments/README.md) · [Reference](QUICK_REFERENCE.md)

Read the beginner modules first. Add the coding and advanced modules according to your goal.
Each checkpoint describes something you should be able to explain or demonstrate.

## Module 1 · Understand the interface

**Lessons:** [00 · Start here](../notebooks/00_start_here.ipynb), [01 · Jev basics](../notebooks/01_jev_basics.ipynb)

**Before you start:** no machine-learning background. Read saved outputs; code is optional.

By the end, you can:

- Separate evidence, a question, an estimated answer, and an application action.
- Match a categorical, ordered, or yes/no question to Choice, Score, or Noul.
- Explain why a valid output can still be wrong.

**Checkpoint:** complete [Assignment 1](../assignments/01_design_a_decision.md).
Then attempt questions 1–8 in [the practice companion](PRACTICE.md).

## Module 2 · Follow the calculations

**Lessons:** [02 · Model from scratch](../notebooks/02_decision_model_from_scratch.ipynb),
[03 · Calibration](../notebooks/03_calibration_and_decisions.ipynb)

**Before you start:** lesson 01. Basic Python helps with edits; percentages and multiplication
are enough to follow the first worked examples. The notebooks explain the array operations.

By the end, you can:

- Trace features → weighted scores → probabilities → a winning label.
- Explain what training changes and what softmax normalization establishes.
- Distinguish accuracy from calibration across many outcomes.
- Compare automatic actions with review using explicit costs and assumptions.

**Checkpoint:** complete [Assignment 2](../assignments/02_probabilities_and_actions.md).
Temperature fitting and gradient checks can wait until a second pass.

## Module 3 · Build the workflow

**Lesson:** [04 · Workflows](../notebooks/04_workflows_and_related_models.ipynb)

**Before you start:** lesson 01. Understand an if statement if you run code.

By the end, you can:

- Rewrite a vague request into focused questions with clear criteria.
- Identify dependencies between questions and evidence retrieval.
- Keep arithmetic, permissions, and action rules in ordinary code.
- Explain why parallel computation does not imply statistical independence.

**Checkpoint:** draw a short workflow for your assignment-1 questions. Label which boxes are
model judgments and which boxes are application rules. You can finish the beginner track here.

## Module 4 · Build and evaluate a project

**Lesson:** [07 · Text-routing project](../notebooks/07_text_routing_capstone.ipynb)

**Before you start:** lessons 02 and 03; basic lists, dictionaries, and arrays.

By the end, you can:

- Fit on training, choose settings on validation, and assess a frozen system on test.
- Report coverage and selective error with their denominators.
- Inspect a prediction through its contributing words.
- Explain why identical bag-of-words features cannot resolve the supplied word-order pair.

**Checkpoint:** complete [Assignment 3](../assignments/03_evaluate_a_router.md).
Include one limitation and one next evaluation step alongside your results.

## Module 5 · Choose a deeper topic

| Optional lesson | Learning outcome | Preparation |
|---|---|---|
| [05 · Real API](../notebooks/05_optional_real_jev_api.ipynb) | Identify the request, validate a response, and plan a real evaluation | Lessons 01 and 04; Python dictionaries |
| [06 · Mechanisms](../notebooks/06_architecture_and_training_lab.ipynb) | Trace generic scoring and attention while distinguishing the demo from Jev | Lesson 02; arrays and softmax |
| [09 · Related approaches](../notebooks/09_related_models_lab.ipynb) | Compare rules, similarities, and probabilities on fixed cases | Lesson 07; basic arrays |

Lesson 05 can be read and run offline with its fixture. Only enable the live flag when you intend
to call the provider. Lesson 09 measures local examples, not Jev or other neural model families.

Use [08 · Exercises and solutions](../notebooks/08_exercises_and_solutions.ipynb) throughout the course.
Attempt an exercise before reading its solution.

## Your course checklist

- [ ] I can identify the evidence and the question separately.
- [ ] I can choose the appropriate answer type.
- [ ] I can explain a valid-but-wrong answer.
- [ ] I can trace a small numerical prediction.
- [ ] I can distinguish normalization from calibration.
- [ ] I can justify an action using costs and permissions.
- [ ] I can keep fitting, tuning, and testing separate.
- [ ] I can state a representation failure and an evaluation limitation.

Copy this checklist into your own notes to track progress. No account, submission, or certificate
is required to use the course.
