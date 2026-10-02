# Read the equations, then choose a paper

[Course home](../README.md) · [Notebook catalog](../notebooks/README.md) · [Source evidence](SOURCES.md)

Every notebook includes **math companions beside the examples** and a **Paper references**
section. You can finish a first reading without studying every equation or reading every paper.
Choose one formula that explains a result you already saw, then follow its source.

For historical context and nearby research directions, use the
[model history and comparison guide](MODEL_HISTORY.md). It connects Sentence-BERT, entailment-based
classification, SetFit, and RoBERTa to the representations and decisions taught here.

## A small symbol key

| Symbol | Meaning in this course |
|---|---|
| $N$, $K$ | Number of cases, number of answer classes |
| $x$, $X$ | One feature vector, the matrix of feature vectors |
| $W$, $b$, $\theta$ | Learned weights, bias, all model parameters |
| $z$, $p$ | Raw class scores (logits), probabilities after normalization |
| $y$, $Y$ | Reference class index, matrix of one-hot reference labels |
| $L$, $\eta$ or $\alpha$ | Mean loss, learning rate |
| $T$, $c$ or $\tau$ | Temperature, a cutoff used by an application policy |
| $\mathbf{1}[\cdot]$ | 1 if the condition holds, otherwise 0 |
| $\odot$, $\lVert\cdot\rVert_2$ | Elementwise multiplication, Euclidean vector length |
| $\nabla$, $\partial$, $\leftarrow$ | Gradient, partial derivative, assign the updated value |

Symbols are also defined locally. In the neural sequence lab, $\ell$ is the real token count;
it is separate from loss $L$. Indices start at zero for answer classes. The row-vector formulas
use the transpose of PyTorch's stored `nn.Linear.weight`.

## Find the equation that answers your question

| Notebook | Equations beside the worked examples | Read first |
|---|---|---|
| [00 · Start here](../notebooks/00_start_here.ipynb) | Probability sums and bounds | Guo 2017 when you reach calibration |
| [01 · Jev basics](../notebooks/01_jev_basics.ipynb) | Choice selection, expected rubric score, yes/no probability and threshold | Provider documentation for the API; Guo for evaluation |
| [02 · From scratch](../notebooks/02_decision_model_from_scratch.ipynb) | Softmax, cross-entropy, weight updates, finite differences | Rumelhart 1986; Gneiting 2007 |
| [03 · Calibration](../notebooks/03_calibration_and_decisions.ipynb) | Reliability bins, binary Brier, temperature, costs, bootstrap means | Guo 2017; Efron 1979 |
| [04 · Workflows](../notebooks/04_workflows_and_related_models.ipynb) | Conditional probability, joint bounds, allowed actions and expected cost | Chow 1970 for rejection decisions |
| [05 · Optional API](../notebooks/05_optional_real_jev_api.ipynb) | Probability and score validity checks | Provider documentation for the contract |
| [06 · Architecture](../notebooks/06_architecture_and_training_lab.ipynb) | Attention and masks, shared work, proper-loss derivative | Vaswani 2017; Gneiting 2007 |
| [07 · Project](../notebooks/07_text_routing_capstone.ipynb) | Regularized training, validation searches, multiclass Brier, selective error | Guo 2017; Chow 1970 |
| [08 · Solutions](../notebooks/08_exercises_and_solutions.ipynb) | Softmax shift cancellation, review interval, work-sharing limit | Revisit the paper for the exercise you attempted |
| [09 · Related methods](../notebooks/09_related_models_lab.ipynb) | Smoothed IDF, normalized prototypes, cosine, route accounting | Salton 1988 for term weighting |
| [10 · PyTorch](../notebooks/10_pytorch_models_lab.ipynb) | Linear/MLP, mean pooling, CNN, GRU, attention, Adam, case and pair metrics | One architecture paper matching the model you inspect |

The notebooks contain complete titles, publication years, source links, and a sentence explaining
each reference's role. **BERT is background reading; the course does not train or download BERT.**

## How to read one equation

1. Say what it computes in ordinary words: a probability, a loss, an update, or an action.
2. Locate its inputs in the nearby code. Check the shapes and the denominator.
3. Substitute the lesson's numbers: for example, $(0.8-1)^2=0.04$ for a binary Brier contribution.
4. Predict a change before rerunning: does it alter the representation, weights, probability, or policy?
5. Read the paper's method section and compare its settings with this course's smaller implementation.

The code uses a **mean** loss over cases; some papers write a sum. Binary one-probability Brier
and summed multiclass Brier have different scales. PyTorch's GRU resets after the hidden affine
map, while Cho's original equation resets before the projection. The tiny Transformer uses learned
positions, two small heads, and one encoder layer. These distinctions are written beside the formulas.

## What a citation establishes

A paper supports the method it actually studies. It does not establish that Jev uses that method,
that our toy implementations reproduce the paper's experiment, or that success on authored sentences
predicts real-world performance. The exact smoothing, masks, cost grids, data, and small-model settings
in this course are identified as implementation choices.

Paper verification is recorded in [SOURCES.md](SOURCES.md). Primary PDFs and bibliographic APIs were
accessed without opening browser webpages. The paper list is a reading path, not a new Jev bibliography
claiming publication of proprietary internals.
