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

The optional [history and primary-paper guide](MODEL_HISTORY.md) follows these ideas through
Sentence-BERT, entailment-based classification, SetFit, and RoBERTa. It compares their mechanisms
with Jev's documented interface without inferring its private model lineage.

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

The two sentences in [lesson 09](../notebooks/09_related_models_lab.ipynb) use identical words in a different
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

## Learn PyTorch by changing the information a model can use

The [PyTorch training lab](../notebooks/10_pytorch_models_lab.ipynb) trains small models from scratch
on an authored routing task. No pretrained language weights or Jev service are involved.
Its useful question is: **what happens when the answer depends on word order?**

Read the bag-of-words baseline first. Then compare the sequence models. You do not need to
understand all six architectures before running the lesson.

| Model | How it represents a message | What the comparison teaches |
|---|---|---|
| Bag-of-words linear | One feature per known word, followed by a learned weighted sum | A transparent baseline; changing order leaves its input unchanged |
| Bag-of-words MLP | The same word features, followed by nonlinear hidden layers | More flexible scoring cannot restore discarded order |
| Mean-embedding classifier | Learned word vectors averaged over non-padding tokens | Averaging also loses order; learning vectors does not remove that limitation |
| Small CNN | Learned filters over neighboring token vectors | Local token arrangements can become features; the window size limits direct local context |
| GRU | A recurrent hidden state updated along the token sequence | Sequence order can affect the representation; useful behavior still has to be learned |
| Tiny Transformer | Token and position embeddings processed with attention | Attention with position information can distinguish order; a tiny trained model is not a pretrained language system |

The first three representations are unchanged when the same tokens are rearranged. If two such
messages have different reference labels, those models must give the same distribution to both
and therefore cannot get both labels right. Adding layers, training longer, or changing a threshold
does not repair this representation collision. A CNN, GRU, or Transformer can distinguish the
inputs, but that capability alone does not guarantee a correct learned answer.

That mean-pooling statement applies to our noncontextual token-embedding toy. In Sentence-BERT,
token representations depend on the sequence before pooling, so their average need not have
the same permutation invariance. See the [Sentence-BERT discussion](MODEL_HISTORY.md#sentence-bert--represent-sentences-for-comparison).

All six models still use a fixed three-label task head. They do not accept arbitrary new question
descriptions in the way Jev's typed request interface does. PyTorch supplies tensor operations and
automatic differentiation; using it does not make a model calibrated or reproduce RLCD.

## Read a training result without overclaiming

1. **Check the split.** Learn vocabulary and weights from training examples. Select checkpoints
   on validation examples. Keep both members of a reversed-message pair in the same split so a
   paired construction does not cross the boundary.
2. **Read both loss curves.** Falling training loss shows that the optimizer fits the training
   task. If validation loss rises while training loss falls, generalization on that split is getting
   worse; the final epoch need not be the best checkpoint.
3. **Count ordinary and paired mistakes.** Report correct labels / test messages, then pairs
   where both labels are correct / test pairs. One correct member does not resolve the pair.
4. **Compare every seed.** Different initial weights can produce different learned behavior.
   Report all fixed runs rather than selecting the most flattering test result. Variation across
   seeds measures training variability on this fixed task, not uncertainty about real traffic.
5. **State the task's boundary.** A generated dataset can reuse vocabulary, grammar, and templates
   across splits. Separate examples under the same construction test that synthetic distribution;
   they do not establish understanding of unfamiliar language or customer messages.

The models have different parameter counts and computation costs. An equal epoch budget keeps
the exercise bounded; it does not make this a controlled comparison of whole architecture families.

The multiclass log loss and Brier score assess probability quality. They are not pure calibration
metrics, and a lower loss is not proof of calibration. Inspect reliability, subgroup errors, and
out-of-domain cases on suitable separate data before choosing a real automation policy.

[Try the comparison lab](../notebooks/09_related_models_lab.ipynb) · [Quick reference](QUICK_REFERENCE.md) · [Sources](SOURCES.md)
