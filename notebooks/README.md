# Pick a lesson

[← Course home](../README.md) · [Full curriculum](../docs/COURSE.md) · [Setup help](../docs/SETUP.md)

Read saved results on GitHub, or choose **Colab** to run a lesson without a local installation.
Use **Runtime → Run all**. The first cell fetches the companion teaching code, fictional data, and artwork.
No GPU or Jev key is needed for the local examples.

| Lesson | What you learn | Run |
|---|---|---|
| [00 · Start here](00_start_here.ipynb) | Choose a path, understand the evidence labels, and check your setup. | [Colab](https://colab.research.google.com/github/Optimizer077/jev-learning-course/blob/main/notebooks/00_start_here.ipynb) |
| [01 · The decision interface](01_jev_basics.ipynb) | State, Choice, Score, and Noul. Valid output can still be wrong. | [Colab](https://colab.research.google.com/github/Optimizer077/jev-learning-course/blob/main/notebooks/01_jev_basics.ipynb) |
| [02 · Build a decision model](02_decision_model_from_scratch.ipynb) | Train with NumPy, inspect tensor shapes, and see the decision boundaries. | [Colab](https://colab.research.google.com/github/Optimizer077/jev-learning-course/blob/main/notebooks/02_decision_model_from_scratch.ipynb) |
| [03 · Trust the probability?](03_calibration_and_decisions.ipynb) | Fit temperature on separate data and explore the costs of acting or reviewing. | [Colab](https://colab.research.google.com/github/Optimizer077/jev-learning-course/blob/main/notebooks/03_calibration_and_decisions.ipynb) |
| [04 · Compose the workflow](04_workflows_and_related_models.ipynb) | Separate judgment, evidence retrieval, permissions, and deterministic rules. | [Colab](https://colab.research.google.com/github/Optimizer077/jev-learning-course/blob/main/notebooks/04_workflows_and_related_models.ipynb) |
| [05 · Call real Jev, optionally](05_optional_real_jev_api.ipynb) | Inspect the official request, validate answers, and enable a live call yourself. | [Colab](https://colab.research.google.com/github/Optimizer077/jev-learning-course/blob/main/notebooks/05_optional_real_jev_api.ipynb) |
| [06 · Inside the mechanisms](06_architecture_and_training_lab.ipynb) | Candidate scoring, isolated attention, shared work, and learning objectives. | [Colab](https://colab.research.google.com/github/Optimizer077/jev-learning-course/blob/main/notebooks/06_architecture_and_training_lab.ipynb) |
| [07 · Build the complete system](07_text_routing_capstone.ipynb) | Train a local text router on fictional tickets, then inspect held-out results and failures. | [Colab](https://colab.research.google.com/github/Optimizer077/jev-learning-course/blob/main/notebooks/07_text_routing_capstone.ipynb) |
| [08 · Check your understanding](08_exercises_and_solutions.ipynb) | Worked answers with runnable checks, from softmax to label leakage. | [Colab](https://colab.research.google.com/github/Optimizer077/jev-learning-course/blob/main/notebooks/08_exercises_and_solutions.ipynb) |
| [09 · Compare related approaches](09_related_models_lab.ipynb) | Try rules, lexical prototypes, and a learned classifier on the same fictional messages. | [Colab](https://colab.research.google.com/github/Optimizer077/jev-learning-course/blob/main/notebooks/09_related_models_lab.ipynb) |
| [10 · Train six PyTorch models](10_pytorch_models_lab.ipynb) | Trace updates, compare order-sensitive inputs, evaluate all three seeds, and reload small checkpoints. | [Colab](https://colab.research.google.com/github/Optimizer077/jev-learning-course/blob/main/notebooks/10_pytorch_models_lab.ipynb) |

Each notebook runs independently. Choose a **CPU runtime**; a GPU is unnecessary.
Teaching diagrams are saved inside the notebook, so you can inspect them before running anything.
Colab needs internet access for the initial repository clone. A local checkout needs no clone.
See [the setup guide](../docs/SETUP.md) for prerequisites and troubleshooting.
Lesson 10 needs PyTorch only when you run it. Its saved figures and results can be read without installing anything.
