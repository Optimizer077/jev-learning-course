# Assignment 1 · Design a decision

**Preparation:** [00](../00_start_here.ipynb) and [01](../01_jev_basics.ipynb). No coding required.

## Scenario

A fictional customer writes:

> My invoice is wrong, and the export button crashes whenever I try to download it. I need a
> corrected invoice today.

Your program needs a primary queue, a disruption level, and whether a refund was explicitly requested.
An action also requires trusted account permission supplied by the application.

## Your task

1. Write three precise questions. Choose Choice, Score, or Noul for each and explain why.
2. Define queue criteria and a 0–2 disruption rubric. State how you will handle a mixed-topic message.
3. List the evidence supplied to the model. Identify information that belongs in trusted application state.
4. Write an action rule in words or pseudocode. Include a review route for unclear cases.
5. Explain what your program should do when the predicted queue is technical with probability 0.90,
   but the required account permission is false. The number is invented for this assignment.

## Success criteria

- Each question asks one bounded judgment and matches its answer type.
- Criteria are specific enough to label a boundary case consistently.
- A request for a corrected invoice is distinguished from an explicit request to return money.
- The policy separates uncertainty handling from permission enforcement.
- You explain why an allowed label does not establish correctness.

## Hints and review

<details><summary>Hint: separate topic from requested action</summary>
<p>A message can mention an invoice while describing a product failure. Define the primary-queue
policy explicitly. A requested correction is not automatically a request to return money.</p>
</details>

<details><summary>Hint: permission</summary>
<p>A model estimate cannot grant application permission. Explain the rule that prevents an
unauthorized action, and where that rule lives.</p>
</details>

Review [lesson 04](../04_workflows_and_related_models.ipynb) and the first section of
[the practice questions](../PRACTICE.md) after writing your answer.

[All assignments](README.md) · [Course outline](../COURSE.md)
