# Guided practice: predict, check, explain

Try each question before opening the explanation. All numbers and messages are teaching examples.

[Course home](../README.md) · [Course outline](COURSE.md)

For the optional interactive copy, download the course and open `site/practice.html` locally. The questions below work directly in GitHub’s Markdown viewer.

The three sections move from the interface to probabilities and then to building a system. You can use this page for individual study or print it for a group.

## 1. Understand the interface

A customer writes “The export button crashes.” What belongs in the state?

- **A.** The customer message and relevant evidence
- **B.** The answer “technical” that we want the model to choose
- **C.** Our routing threshold of 0.85 alone

<details><summary>Hint</summary><p>State is what the model gets to examine.</p></details>

<details><summary>Answer and explanation</summary><p><strong>A.</strong> State supplies evidence. The question and criteria describe the judgment. The routing threshold belongs to the application policy.</p></details>

[Review 01 · State and typed questions](../notebooks/01_jev_basics.ipynb)

## 2. Understand the interface

You need one primary queue: billing, technical, or other. Which question type fits?

- **A.** Score
- **B.** Choice
- **C.** Noul

<details><summary>Hint</summary><p>The alternatives are named categories, with no low-to-high order.</p></details>

<details><summary>Answer and explanation</summary><p><strong>B.</strong> Choice compares the supplied alternatives and returns a selected option plus probabilities. Write descriptions that distinguish the queues.</p></details>

[Review 01 · Choice](../notebooks/01_jev_basics.ipynb)

## 3. Understand the interface

You ask “Does this message explicitly request a refund?” Which type fits?

- **A.** Choice over all support queues
- **B.** Score from 0 to 2
- **C.** Noul

<details><summary>Hint</summary><p>Think about whether the question has a positive and a negative answer.</p></details>

<details><summary>Answer and explanation</summary><p><strong>C.</strong> Noul reports the probability of the positive answer to a yes/no question. The program can apply a threshold to that number.</p></details>

[Review 01 · Noul](../notebooks/01_jev_basics.ipynb)

## 4. Understand the interface

A rubric has 0 = no disruption, 1 = partial disruption, 2 = fully blocked. Which type fits?

- **A.** Score
- **B.** Noul
- **C.** Choice with alphabetically ordered queue names

<details><summary>Hint</summary><p>These labels are levels along an ordered scale.</p></details>

<details><summary>Answer and explanation</summary><p><strong>A.</strong> Score uses ordered rubric levels and returns their expected position. The meaning of each level should be clear.</p></details>

[Review 01 · Score](../notebooks/01_jev_basics.ipynb)

## 5. Read the numbers

The probabilities for levels 0, 1, and 2 are 5%, 25%, and 70%. What is the expected score?

- **A.** 2, because it is the most likely level
- **B.** 1.65, from 0 × 0.05 + 1 × 0.25 + 2 × 0.70
- **C.** 0.70, the probability of level 2

<details><summary>Hint</summary><p>Average the levels using their probabilities as weights.</p></details>

<details><summary>Answer and explanation</summary><p><strong>B.</strong> The weighted average is 1.65. The most likely level is 2, but selecting that level and averaging the distribution are different calculations.</p></details>

[Review 01 · Calculate a Score](../notebooks/01_jev_basics.ipynb)

## 6. Read the numbers

Technical has probability 0.90. Our rule routes only when the largest probability is at least 0.95. What happens?

- **A.** Route to technical because it is largest
- **B.** Change the model estimate to 0.95
- **C.** Send the case for review

<details><summary>Hint</summary><p>Compare 0.90 with the threshold before taking the action.</p></details>

<details><summary>Answer and explanation</summary><p><strong>C.</strong> The estimate stays 0.90 and the winning queue stays technical. The application sends the case for review because 0.90 is below 0.95.</p></details>

[Review 01 · Prediction and policy](../notebooks/01_jev_basics.ipynb)

## 7. Read the numbers

“billing” is an allowed output, but the message describes an export crash. What did the type check establish?

- **A.** The output has an allowed form
- **B.** The model understood the message correctly
- **C.** The program is authorized to issue a refund

<details><summary>Hint</summary><p>A format check can inspect the allowed values without knowing the right answer.</p></details>

<details><summary>Answer and explanation</summary><p><strong>A.</strong> The output is structurally valid. Accuracy needs a reference judgment, and authorization needs the application’s permission rules.</p></details>

[Review 04 · Judgments and rules](../notebooks/04_workflows_and_related_models.ipynb)

## 8. Read the numbers

A calibrated model repeatedly gives 80% for comparable yes/no cases. What should happen across many such cases?

- **A.** Every case is yes
- **B.** About 80% are yes, with sampling variation
- **C.** Exactly 80 out of every 100 are yes

<details><summary>Hint</summary><p>A probability describes a pattern across outcomes, not a promise for one outcome.</p></details>

<details><summary>Answer and explanation</summary><p><strong>B.</strong> Calibration compares stated probabilities with observed frequencies across many predictions. Individual cases can be negative, and finite groups fluctuate.</p></details>

[Review 03 · Calibration](../notebooks/03_calibration_and_decisions.ipynb)

## 9. Build and evaluate

p(yes) = 0.90. Acting yes costs 4 if wrong; acting no costs 1 if wrong. Perfect review costs 0.20. Correct actions cost 0. Which is cheapest in expectation?

- **A.** Act yes: expected cost 0.40
- **B.** Act no: expected cost 0.90
- **C.** Review: cost 0.20

<details><summary>Hint</summary><p>Compare (1 − 0.90) × 4, 0.90 × 1, and 0.20.</p></details>

<details><summary>Answer and explanation</summary><p><strong>C.</strong> Review has the lowest expected cost: 0.20 versus 0.40 and 0.90. This result assumes calibrated probabilities and perfectly accurate review.</p></details>

[Review 03 · Expected action costs](../notebooks/03_calibration_and_decisions.ipynb)

## 10. Build and evaluate

You have trained the model and need to choose a routing threshold. Which split should you use?

- **A.** Validation; then assess the frozen system on test
- **B.** Test; keep changing the threshold until the mistakes disappear
- **C.** All labeled examples, then report the same examples as a fresh test

<details><summary>Hint</summary><p>Keep the final assessment separate from decisions about settings.</p></details>

<details><summary>Answer and explanation</summary><p><strong>A.</strong> Use validation data to choose the threshold. Reserve test data to assess the frozen model and policy. Repeated tuning on test examples weakens that assessment.</p></details>

[Review 07 · Training, validation, and test](../notebooks/07_text_routing_capstone.ipynb)

## 11. Build and evaluate

“The payment failed, not the export.” and “The export failed, not the payment.” have identical bag-of-words features. Can a deterministic classifier using only those features distinguish them?

- **A.** Yes, if we lower temperature enough
- **B.** No; the representation removed the distinguishing word order
- **C.** Yes, by increasing the confidence threshold

<details><summary>Hint</summary><p>The classifier sees the same feature vector for both messages.</p></details>

<details><summary>Answer and explanation</summary><p><strong>B.</strong> Identical input features produce identical outputs in this deterministic model. Word order and the scope of “not” matter here; temperature or thresholds cannot restore discarded information.</p></details>

[Review 07 · Inspect the minimal-pair failure](../notebooks/07_text_routing_capstone.ipynb)

## 12. Build and evaluate

Our local classifier scores every option in one matrix operation. What does that experiment establish?

- **A.** That Jev must use our exact weight matrix and training method
- **B.** That our local accuracy is a Jev benchmark
- **C.** How one small teaching classifier can compute bounded decisions

<details><summary>Hint</summary><p>Ask which system was actually measured.</p></details>

<details><summary>Answer and explanation</summary><p><strong>C.</strong> The experiment demonstrates our constructed classifier. The provider documentation describes Jev’s external behavior; the toy does not establish proprietary internals or performance.</p></details>

[Review 06 · Mechanisms and evidence](../notebooks/06_architecture_and_training_lab.ipynb)
