# See the idea before the code

[Course home](../README.md) · [Start lesson 00](../notebooks/00_start_here.ipynb) · [Quick reference](QUICK_REFERENCE.md)

These diagrams use invented examples. They describe the decision interface and application rules;
they do not show Jev's proprietary architecture or measure its accuracy.

## Follow one ticket

Give the message as **evidence**, then ask a **question** with clear **criteria**:
technical means broken product behavior, billing means charges or invoices, and other means
neither listed queue fits or the evidence is insufficient.

<img src="../assets/decision-flow.svg" alt="Evidence: the export button crashes. Question: which queue fits? Invented probabilities: technical 90%, billing 6%, other 4%. A threshold of 0.85 routes to technical; 0.95 sends the same estimate to review." width="660">

Changing the threshold changes the action, while the estimate stays the same.
The thresholds are teaching choices, not recommendations for a real support system.
Permissions remain separate: a refund prediction cannot authorize a payment.

**Predict:** at threshold 0.92, what happens? Then explain why.

<details><summary>Check your answer</summary>
<p>The case goes to review because 0.90 is below 0.92. Technical remains the most likely queue.</p>
</details>

Continue with [lesson 01](../notebooks/01_jev_basics.ipynb).

## Ask three different questions

The same message can support several judgments. Choose the answer type to match the question.

<img src="../assets/question-types.svg" alt="Choice selects among named queues with probabilities. Score averages ordered rubric levels: 5% at level 0, 25% at level 1, and 70% at level 2 give 1.65. Noul provides a yes probability, illustrated as 12% for an explicit refund request." width="600">

- **Choice:** which named alternative fits? Here, technical is most likely.
- **Score:** where is the expected position on an ordered rubric? Here, 1.65 differs from the most likely level, 2.
- **Noul:** how likely is the positive answer? Here, 12% is an estimate of an explicit refund request.

The numbers are authored illustrations, not three outputs from a real Jev call.
[Choice reference](https://docs.typesafe.ai/primitives/choice) ·
[Score reference](https://docs.typesafe.ai/primitives/score) ·
[Noul reference](https://docs.typesafe.ai/primitives/noul).

**Predict:** would “Can you refund yesterday's duplicate charge?” ask a different Noul question
from “Which support queue fits?” Explain the difference before reading the notebook.

## Compare predictions with outcomes

An 80% estimate does not make any one outcome certain. Calibration concerns patterns across
many predictions and their observed outcomes.

<img src="../assets/calibration-counts.svg" alt="Ten invented cases each receive a predicted yes probability of 80%. Eight are yes and two are no, so observed frequency is 8 divided by 10, or 80%. A single agreeing group does not prove calibration." width="600">

**Predict:** change one yes to no. The observed frequency becomes 70% while the predictions stay 80%.
One finite group can fluctuate; evaluate many groups and their sample sizes before judging calibration.
Continue with [lesson 03](../notebooks/03_calibration_and_decisions.ipynb).

## Know when you understand

You can separate the evidence, the question, the estimated answer, and the action.
You can explain why changing an application rule does not change a model's estimate.
You can name one result these illustrations do **not** establish.

[Try the practice questions](PRACTICE.md) · [Choose your learning path](COURSE.md)
