# How Jev and related approaches fit together

Start with the job your program needs to do. Then identify what each component supplies.
The examples below explain roles; performance depends on the actual task and evaluation.

## Three parts of a decision system

| Part | Question it answers | Example |
|---|---|---|
| Representation | What information can the computation use? | Words present in a message; or a contextual language representation |
| Scoring mechanism | How are candidate answers compared? | Rules, similarity, a learned classifier, or a service answering typed questions |
| Application policy | What should happen after the estimate? | Route, ask for clarification, retrieve evidence, or request review |

Changing one part does not automatically repair the others. A threshold can send difficult cases
to review, but it cannot recover word order discarded by a bag-of-words representation.

## Follow the same support message through different approaches

Message: **“The payment failed, not the export.”** Intended primary queue: **billing**.

| Approach | What it could examine | What you need to inspect |
|---|---|---|
| Keyword rule | Words such as payment and export | Tie handling, precedence, negation, and missing keywords |
| Lexical similarity | Overlap with weighted word vectors | Whether overlap captures meaning; how an unseen message is handled |
| Learned linear classifier | A weighted sum of input features | What features encode, training coverage, held-out errors, and calibration |
| Contextual encoder plus classifier | Context-dependent representations plus a learned task head | Whether training and evaluation cover this distinction |
| Generative language model | The input and instructions while generating answer tokens | Answer correctness, requested structure, uncertainty, and workflow behavior |
| Jev / System One | Supplied state and typed questions with criteria | The documented output contract and measured performance on your task |

The two sentences in [lesson 09](09_related_models_lab.ipynb) use identical words in a different
order. The local word-presence methods receive identical features. A representation that retains
context can express more distinctions, but its existence alone does not establish that the system
will answer this case correctly. [BERT's primary paper](https://aclanthology.org/N19-1423/) explains
one contextual encoder and its task adaptation.

Jev exposes a typed decision interface. Its [official System One definition](https://docs.typesafe.ai/concepts/system-one)
describes that behavior. Our local experiments do not supply Jev's model weights or proprietary
training implementation. They help explain the roles a decision mechanism can play.

The local learned classifier has a fixed three-class output head. The prototypes also represent
three classes, built from labeled training examples. Jev's [Choice contract](https://docs.typesafe.ai/primitives/choice)
instead lets the request supply named alternatives and their descriptions. That interface
flexibility is distinct from changing the number of columns in a trained classifier. Evaluate
the actual candidate set and criteria you intend to use.

## Classification, retrieval, and generation answer different questions

| Job | Example question | Typical result | Where it appears in the course |
|---|---|---|---|
| Classification | Which queue fits the message? | A label, possibly with probabilities | Lessons 01, 02, 07, 09 |
| Retrieval | Which reference documents are relevant? | Ranked documents or passages | Workflow discussion in lesson 04 |
| Generation | How should we explain the solution? | Newly generated text | Conceptual comparison in lesson 04 |
| Typed judgment | Does the evidence satisfy the stated criterion? | A bounded answer in the requested type | Jev's interface in lessons 01 and 05 |

Retrieval can supply evidence for a judgment; it does not itself establish the answer.
Generation can explain a result; it still needs to be checked against the evidence.
A pipeline may use all these roles. Lesson 09's class prototypes demonstrate lexical matching
inside a classifier, rather than a complete document-retrieval or generation system.

## Compare outputs with their actual meaning

| Output | What it tells you | What to avoid assuming |
|---|---|---|
| Keyword count | How many specified triggers matched | That it is a probability |
| Cosine similarity | How closely vector directions align | That 0.80 means 80% correct |
| Softmax probability | A model's normalized distribution over its labels | That normalization guarantees calibration |
| Selected class | Which candidate won the scoring rule | That the program must act on it |
| Jev confidence | The documented distribution-derived summary | That it equals the largest probability or our entropy calculation |

Read the [official confidence page](https://docs.typesafe.ai/confidence) for Jev's stated meaning.
Use the complete output distribution and evaluation results when designing a policy.

## What the local comparison can establish

Lesson 09 reports three methods on the same twelve fixed fictional test messages. It makes review
counts and automatic-error denominators explicit. That lets you compare **those implementations
on those cases** and inspect concrete disagreements.

It cannot establish performance on real customer traffic, the quality of a whole model family,
or a Jev benchmark. For a broader comparison, define the task, collect independently labeled
examples, freeze settings before test, and measure the complete workflow. Lesson 04 lists what
to hold fixed and what to record.

[Try the comparison lab](09_related_models_lab.ipynb) · [Quick reference](QUICK_REFERENCE.md) · [Sources](SOURCES.md)
