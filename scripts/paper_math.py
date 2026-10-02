"""Add optional, code-matched math companions and primary papers to every lesson.

The builder uses enrich_math; running this file updates Markdown only in saved
notebooks, preserving executed code and outputs. Paper evidence is in SOURCES.md.
"""
from textwrap import dedent
import re

PAPERS = {
    'guo': ('Guo et al. (2017)', 'On Calibration of Modern Neural Networks',
            'ICML, PMLR 70:1321–1330', 'https://proceedings.mlr.press/v70/guo17a.html',
            'Temperature scaling and the difference between accuracy and calibration.'),
    'brier': ('Brier (1950)', 'Verification of Forecasts Expressed in Terms of Probability',
              'Monthly Weather Review 78(1):1–3',
              'https://doi.org/10.1175/1520-0493(1950)078%3C0001:VOFEIT%3E2.0.CO;2',
              'The original probability-forecast scoring paper; this course states its binary and multiclass conventions explicitly.'),
    'proper': ('Gneiting and Raftery (2007)', 'Strictly Proper Scoring Rules, Prediction, and Estimation',
               'Journal of the American Statistical Association 102(477):359–378',
               'https://doi.org/10.1198/016214506000001437',
               'Why proper probability losses reward honest probability forecasts.'),
    'chow': ('Chow (1970)', 'On Optimum Recognition Error and Reject Tradeoff',
             'IEEE Transactions on Information Theory 16(1):41–46',
             'https://doi.org/10.1109/TIT.1970.1054406',
             'The recognition-versus-rejection problem; our review costs and policy are authored teaching choices.'),
    'attention': ('Vaswani et al. (2017)', 'Attention Is All You Need',
                  'Advances in Neural Information Processing Systems 30',
                  'https://arxiv.org/abs/1706.03762',
                  'Scaled dot-product attention and the need to supply position information.'),
    'bert': ('Devlin et al. (2019)', 'BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding',
             'NAACL-HLT:4171–4186', 'https://aclanthology.org/N19-1423/',
             'Contextual language representations and downstream classification; BERT is not run in this course.'),
    'cnn': ('Kim (2014)', 'Convolutional Neural Networks for Sentence Classification',
            'EMNLP:1746–1751', 'https://aclanthology.org/D14-1181/',
            'Local convolutional features and max pooling for sentence classification; our tiny CNN uses different settings.'),
    'gru': ('Cho et al. (2014)', 'Learning Phrase Representations using RNN Encoder–Decoder for Statistical Machine Translation',
            'EMNLP:1724–1734', 'https://aclanthology.org/D14-1179/',
            'Historical gated recurrent units; the PyTorch reset-gate variant is identified beside our equations.'),
    'adam': ('Kingma and Ba (2015)', 'Adam: A Method for Stochastic Optimization',
             'ICLR; arXiv preprint first posted in 2014', 'https://arxiv.org/abs/1412.6980',
             'Adaptive moment estimates, bias correction, and the optimizer used in lesson 10.'),
    'tfidf': ('Salton and Buckley (1988)', 'Term-weighting approaches in automatic text retrieval',
              'Information Processing & Management 24(5):513–523',
              'https://doi.org/10.1016/0306-4573(88)90021-0',
              'Term weighting and vector-space retrieval; our exact smoothed binary variant is an implementation convention.'),
    'backprop': ('Rumelhart, Hinton, and Williams (1986)', 'Learning representations by back-propagating errors',
                 'Nature 323:533–536', 'https://doi.org/10.1038/323533a0',
                 'Historical background for learning weights through propagated derivatives; our linear gradient is derived in the lesson.'),
    'bootstrap': ('Efron (1979)', 'Bootstrap Methods: Another Look at the Jackknife',
                  'The Annals of Statistics 7(1):1–26', 'https://doi.org/10.1214/aos/1176344552',
                  'Resampling with replacement; the lesson explicitly uses a percentile interval rather than claiming all bootstrap methods are the same.'),
    'sbert': ('Reimers and Gurevych (2019)', 'Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks',
              'EMNLP-IJCNLP:3982–3992', 'https://aclanthology.org/D19-1410/',
              'Trained contextual sentence embeddings; mean pooling alone does not reproduce Sentence-BERT.'),
    'nli': ('Yin, Hay, and Roth (2019)', 'Benchmarking Zero-shot Text Classification: Datasets, Evaluation and Entailment Approach',
            'EMNLP-IJCNLP:3914–3923', 'https://aclanthology.org/D19-1404/',
            'Candidate labels as hypotheses; the reviewed paper uses binary entailment/non-entailment models.'),
    'setfit': ('Tunstall et al. (2022)', 'Efficient Few-Shot Learning Without Prompts',
               'arXiv preprint 2209.11055', 'https://arxiv.org/abs/2209.11055',
               'SetFit: contrastive adaptation of a pretrained Sentence Transformer, then a task classifier.'),
    'roberta': ('Liu et al. (2019)', 'RoBERTa: A Robustly Optimized BERT Pretraining Approach',
                'arXiv preprint 1907.11692', 'https://arxiv.org/abs/1907.11692',
                'Changes to BERT pretraining; a research comparison, not a model executed here.'),
}

READINGS = {
    '00': ('guo', 'brier'), '01': ('guo', 'brier'),
    '02': ('backprop', 'guo', 'proper'), '03': ('guo', 'brier', 'chow', 'bootstrap'),
    '04': ('chow', 'bert'), '05': ('guo', 'brier'),
    '06': ('attention', 'bert', 'proper', 'sbert', 'nli', 'setfit'), '07': ('guo', 'brier', 'chow'),
    '08': ('guo', 'chow', 'attention'), '09': ('tfidf', 'bert', 'chow', 'roberta', 'sbert', 'nli', 'setfit'),
    '10': ('cnn', 'gru', 'attention', 'adam', 'brier', 'proper', 'bert', 'roberta', 'sbert'),
}

# Anchors are checked exactly once so a renamed section cannot silently lose math.
COMPANIONS = {
    '00': [('## Try one decision', r'''
**Math companion · optional first look**

For $K$ mutually exclusive answers, a probability vector satisfies
$$p_k\geq0,\qquad \sum_{k=0}^{K-1}p_k=1.$$
Here $k$ is an answer index and $p_k$ is its probability. A larger value means more
probability on that answer. This equation checks accounting, not truth or calibration.
For example, $(0.06,0.90,0.04)$ sums to one but can still predict the wrong queue.
The distinction between accurate labels and calibrated probabilities is studied by
[Guo et al. (2017)](https://proceedings.mlr.press/v70/guo17a.html).
''')],
    '01': [('### 2. Choice:', r'''
**Math companion · choosing from a distribution**

$$\hat{k}\in\operatorname*{arg\,max}_{k\in\{0,\ldots,K-1\}}p_k.$$
$K$ is the number of options, $p_k$ the probability of option $k$, and $\hat{k}$ an
index with the largest probability; map it back to the option key.
The set notation allows ties. In our Python illustration, `max` retains the first
encountered key in a tie; this is not a claim about an undocumented API tie rule.
The selected probability is $p_{\hat{k}}$, not Jev's separate `confidence` field.
'''), ('### 3. Score:', r'''
**Math companion · read the existing expectation equation**

In the equation above, $K$ is the number of rubric levels, $k$ their zero-based index,
and $p(k)$ the probability of level $k$. The result weights each index by its probability.
Here $K=3$ and $0(0.05)+1(0.25)+2(0.70)=1.65$; it is an expected index, not a new level.
'''), ('### 4. Noul:', r'''
**Math companion · a probability and an action are different objects**

$$P(Y=1)=p,\qquad P(Y=0)=1-p,\qquad
\text{our action}=\mathbf{1}[p\geq\tau].$$
$Y=1$ means “yes,” $p$ is the Noul result, $\tau$ is our chosen policy threshold,
and $\mathbf{1}[\cdot]$ is 1 when its condition holds and 0 otherwise.
At $p=0.12$ and $\tau=0.80$, the probability remains 0.12 while the policy returns false.
Probability-forecast evaluation goes back to [Brier (1950)](https://doi.org/10.1175/1520-0493(1950)078%3C0001:VOFEIT%3E2.0.CO;2);
it does not determine this application's threshold.
''')],
    '02': [('### 3. Train by penalizing', r'''
**Math companion · connect the loss to the update**

With training temperature $T=1$, let $P$ be the $N\times K$ predicted-probability
matrix and $Y$ the one-hot target matrix. For the mean cross-entropy $L$ above,
$$\nabla_W L=X^\top(P-Y)/N,\qquad
\nabla_b L=\frac{1}{N}\sum_{i=1}^{N}(P_i-Y_i).$$
$$W\leftarrow W-\eta\nabla_W L,\qquad b\leftarrow b-\eta\nabla_b L.$$
$X$ contains $N$ examples and $D$ features, $W$ has shape $D\times K$, $b$ has
$K$ entries, and $\eta>0$ is the learning rate. This notebook uses no weight penalty.
At a different fixed temperature, the logit derivative also includes a factor $1/T$.
These are supervised classifier equations, not RLCD. [Rumelhart, Hinton, and Williams (1986)](https://doi.org/10.1038/323533a0)
provide historical backpropagation background. Log loss belongs to the proper-scoring
framework discussed by [Gneiting and Raftery (2007)](https://doi.org/10.1198/016214506000001437).
'''), ('### 8. Verify one gradient', r'''
**Math companion · an independent slope estimate**

$$\frac{\partial L}{\partial W_{jk}}\approx
\frac{L(W+\varepsilon E_{jk})-L(W-\varepsilon E_{jk})}{2\varepsilon}.$$
$E_{jk}$ is zero except for a 1 at weight $(j,k)$; $\varepsilon$ is a small positive
perturbation. The code compares this finite-difference slope with the analytic gradient.
An excessively small perturbation amplifies floating-point noise; this is a numerical
check of our implementation, not a formula quoted from a Jev paper.
''')],
    '03': [('### 2. Read a reliability diagram', r'''
**Math companion · define the plotted quantities**

For a nonempty bin $B_m$ of predictions,
$$\bar p_m=\frac{1}{|B_m|}\sum_{i\in B_m}p_i,\qquad
\bar y_m=\frac{1}{|B_m|}\sum_{i\in B_m}y_i.$$
The plot compares mean prediction $\bar p_m$ with observed positive frequency $\bar y_m$.
Here $y_i\in\{0,1\}$, $m$ indexes a bin, and $|B_m|$ is its number of cases;
empty bins are omitted. $N$ is the total number of evaluated cases.
For the binary outcome probability, this course uses
$$\operatorname{BS}_{binary}=\frac{1}{N}\sum_{i=1}^{N}(p_i-y_i)^2.$$
It ranges from 0 to 1. A single forecast $p=0.8$ followed by $y=1$ contributes 0.04.
[Brier (1950)](https://doi.org/10.1175/1520-0493(1950)078%3C0001:VOFEIT%3E2.0.CO;2)
introduced probability scoring. A two-category squared-error sum gives twice this
one-probability score: $(p-y)^2+((1-p)-(1-y))^2=2(p-y)^2$.
[Guo et al. (2017)](https://proceedings.mlr.press/v70/guo17a.html)
discuss modern calibration. The Brier score is not a calibration-only metric.
'''), ('### 5. Repair overconfidence', r'''
**Math companion · the temperature search actually used here**

$$p_i(T)=\sigma(z_i/T),\qquad \sigma(u)=\frac{1}{1+e^{-u}}.$$
$$T^*=\operatorname*{arg\,min}_{T\in\mathcal T}
-\frac{1}{N_{cal}}\sum_{i\in cal}
\left[y_i\log p_i(T)+(1-y_i)\log(1-p_i(T))\right].$$
$z_i$ is the overconfident binary logit, $N_{cal}$ is the number of calibration cases,
the index set $cal$ contains those cases, and $\mathcal T$ is this notebook's
121-point logarithmic grid from 0.25 to 6.
The code clips probabilities when taking logs for numerical safety. It searches a finite
grid; it does not train the classifier or optimize temperature on the held-out evaluation set.
This adapts the temperature-scaling idea in [Guo et al. (2017)](https://proceedings.mlr.press/v70/guo17a.html).
'''), ('### 6. An uncertainty interval', r'''
**Math companion · what is resampled**

For each bootstrap replicate $b$, sample $N$ case indices $I_{b,1},\ldots,I_{b,N}$
independently with replacement from $\{1,\ldots,N\}$, then compute
$$\widehat{\operatorname{BS}}^{(b)}=\frac1N\sum_{j=1}^{N}
\left(p_{I_{b,j}}-y_{I_{b,j}}\right)^2.$$
The plotted 95% percentile interval is the 2.5th–97.5th percentile range of the replicate means.
$N$ is the held-out sample size, not the number of bootstrap replicates. This interval estimates
sampling variation of a mean under the stated independent-case assumption; it does not cover
unknown distribution shifts or give an interval for a single prediction.
[Efron (1979)](https://doi.org/10.1214/aos/1176344552) introduces the bootstrap framework.
''')],
    '04': [('### 2. Do not multiply', r'''
**Math companion · dependence has a precise place**

$$P(A\cap B)=P(A)P(B\mid A),\qquad P(A)>0.$$
$A$ and $B$ are two events; $P(B\mid A)$ is the chance of $B$ among cases where $A$ occurs.
Independence would require $P(B\mid A)=P(B)$. Without it,
$$\max(0,P(A)+P(B)-1)\leq P(A\cap B)\leq\min(P(A),P(B)).$$
For 0.8 and 0.7, the valid intersection range is 0.5–0.7. The bounds follow from
$P(A\cup B)\leq1$ and $A\cap B\subseteq A,B$; they are elementary probability identities,
not evidence about how Jev batches questions.
'''), ('### 4. What should stay in code?', r'''
**Math companion · choose an allowed action by modeled cost**

$$a^*\in\operatorname*{arg\,min}_{a\in\mathcal A(s)}
\sum_y C(a,y)\,p(y\mid s).$$
$s$ is the supplied state, $\mathcal A(s)$ is the set of actions allowed by explicit
permissions, $C(a,y)$ is the cost of action $a$ when outcome $y$ occurs, and
$p(y\mid s)$ is the probability of outcome $y$ given state $s$.
The sum is expected cost. A probability does not add a forbidden action to $\mathcal A(s)$.
This is a general decision-theory view; [Chow (1970)](https://doi.org/10.1109/TIT.1970.1054406)
studies rejection alongside recognition. It does not specify our workflow or permissions.
''')],
    '05': [('### 2. Check the response', r'''
**Math companion · what the validator can establish**

For a Choice or Score distribution, the numeric checks require
$$0\leq p_k\leq1,\qquad
\left|\sum_{k=0}^{K-1}p_k-1\right|\leq\delta.$$
For an ordered Score, they also compare the returned score with
$$s_{expected}=\sum_{k=0}^{K-1}k\,p_k;$$
for a Noul they require $0\leq p\leq1$. $K$ is the number of options or levels, and
$p_k$ is the probability of option or level $k$. Here $\delta=10^{-5}$ is the absolute
probability-sum tolerance. The Python validator also uses `math.isclose`'s small default
relative tolerance when comparing numeric results. Ordered indices start at zero.
For $(0.05,0.25,0.70)$, the expected score is 1.65. These invariants follow the
[documented primitives](https://docs.typesafe.ai/primitives/score); passing them does not
establish accuracy or calibration. See [Guo et al. (2017)](https://proceedings.mlr.press/v70/guo17a.html)
for that separate empirical question. There is no published confidence formula asserted here.
''')],
    '06': [('### 3. An attention mechanism', r'''
**Math companion · dimensions and the paper connection**

In this single-head toy, $Q,K,V$ each have shape $n\times d$, with $n=8$ positions
and $d=6$ features. Thus $QK^\top$ and mask $M$ have shape $n\times n$, and the
attention output has shape $n\times d$. Softmax normalizes each query row over keys.
The factor $\sqrt d$ rescales dot-product scores. The scaled-attention expression follows
[Vaswani et al. (2017), section 3.2.1](https://arxiv.org/abs/1706.03762).
Our isolated-question mask is authored course material, not a mask specified in that paper
or a disclosed Jev architecture. Every row must allow at least one key.
'''), ('### 6. Why rewarding only', r'''
**Math companion · show why the minimum is honest**

Differentiating the expected binary Brier loss shown above gives
$$\frac{dL}{dp}=2(p-q),\qquad \frac{d^2L}{dp^2}=2>0.$$
Here $q$ is the true positive-outcome rate and $p$ is the reported probability.
The unique minimum occurs at $p=q$, including boundary rates 0 and 1.
For $q=0.7$, the minimum is $q(1-q)=0.21$; irreducible outcome randomness leaves positive
expected loss. This is a worked example of strict propriety, as discussed by
[Gneiting and Raftery (2007)](https://doi.org/10.1198/016214506000001437), not the RLCD reward.
''')],
    '07': [('### 3. Train a regularized', r'''
**Math companion · the complete training objective**

$$L(W,b)=-\frac{1}{N_{train}}\sum_{i\in train}\log p_{i,y_i}
+\frac{\lambda}{2}\lVert W\rVert_F^2,\qquad
P=\operatorname{softmax}(XW+b).$$
$$\nabla_W L=X^\top(P-Y)/N_{train}+\lambda W.$$
$Y$ contains one-hot labels, $\lVert W\rVert_F^2$ sums all squared weights, and
$\lambda=0.02$ in the delivered baseline. The bias has no weight penalty.
Throughout these companions, $N_{train}=24$, $N_{val}=12$, and $N=12$ for test evaluation;
$z_i$ is a row of logits, $p_{ik}$ a class probability, $y_i$ its reference class index,
and $\hat y_i=\operatorname*{arg\,max}_k p_{ik}$ the predicted class (first index on a tie).
Vocabulary, $W$, and $b$ are fitted using training cases only. The helper clips very small
probabilities for numeric log-loss reporting; the update is the standard cross-entropy gradient.
'''), ('### 4. Select temperature', r'''
**Math companion · keep the two searches separate**

$$T^*=\operatorname*{arg\,min}_{T\in\mathcal T}
-\frac{1}{N_{val}}\sum_{i\in val}
\log\!\left[\operatorname{softmax}(z_i/T)_{y_i}\right].$$
$\mathcal T$ has 121 logarithmically spaced values from 0.25 to 5 in `lab_core.py`.
After temperature is frozen, let $A_i(c)=\mathbf{1}[\max_k p_{ik}\geq c]$ indicate automation.
For cutoff candidates $c$ in the validation grid,
$$\widehat C(c)=\frac{1}{N_{val}}\sum_{i\in val}
\left[C_E A_i(c)\mathbf{1}[\hat y_i\ne y_i]+C_R(1-A_i(c))\right].$$
The policy chooses the first cutoff minimizing this estimated cost, with $C_E=1$ and
$C_R=0.2$. Both searches use validation labels, not test labels. Temperature scaling follows
[Guo et al. (2017)](https://proceedings.mlr.press/v70/guo17a.html); our cutoff grid and
perfect-review assumption are teaching choices in the recognition/rejection setting of
[Chow (1970)](https://doi.org/10.1109/TIT.1970.1054406).
'''), ('### 5. Evaluate the frozen', r'''
**Math companion · name the denominators**

$$\operatorname{BS}_{multi}=\frac1N\sum_{i=1}^{N}\sum_{k=0}^{K-1}
\left(p_{ik}-\mathbf{1}[y_i=k]\right)^2.$$
The reference label $y_i$ is an integer class index; $K=3$ here. This sum-over-classes
convention ranges from 0 to 2. For $(0.8,0.15,0.05)$ and class 0, its contribution is 0.065.
This extends the probability-scoring idea in [Brier (1950)](https://doi.org/10.1175/1520-0493(1950)078%3C0001:VOFEIT%3E2.0.CO;2).
For automation indicators $A_i$,
$$\operatorname{coverage}=\frac{\sum_i A_i}{N},\qquad
\operatorname{selective\ error}=\frac{\sum_i A_i\mathbf{1}[\hat y_i\ne y_i]}{\sum_i A_i}.$$
Selective error is undefined when no case is automated; the code returns `None`.
Coverage and error describe different quantities. Review quality is assumed, not measured.
''')],
    '08': [('### 2. Shift and scale', r'''
**Math companion · write out the cancellation**

For one common constant $c$,
$$\frac{e^{z_k+c}}{\sum_j e^{z_j+c}}
=\frac{e^c e^{z_k}}{e^c\sum_j e^{z_j}}
=\frac{e^{z_k}}{\sum_j e^{z_j}}.$$
This explains the stable-softmax subtraction in the code. Positive scaling $a$ instead gives
$\operatorname{softmax}(az)=\operatorname{softmax}(z/T)$ with $T=1/a$.
It preserves ranking, not probabilities. Compare with the temperature-scaling method in
[Guo et al. (2017)](https://proceedings.mlr.press/v70/guo17a.html).
'''), ('### 3. Derive the review', r'''
**Math companion · find the review interval from costs**

Perfect review beats both automatic actions when
$$C_R\leq pC_{FN},\qquad C_R\leq(1-p)C_{FP}.$$
For positive error costs, this gives
$$\frac{C_R}{C_{FN}}\leq p\leq1-\frac{C_R}{C_{FP}},$$
intersected with $[0,1]$. With $(C_{FP},C_{FN},C_R)=(4,1,0.2)$ the interval is
$[0.2,0.95]$, including cost ties. If the lower endpoint exceeds the upper endpoint,
review is never cheapest. The code resolves ties by its stated action order.
$C_{FP}$ is false-positive cost, $C_{FN}$ false-negative cost, and $C_R$ perfect-review cost.
This is our cost-based derivation in the rejection setting studied by
[Chow (1970)](https://doi.org/10.1109/TIT.1970.1054406).
''')],
    '09': [('### 3. Match lexical', r'''
**Math companion · follow the exact vector pipeline**

Let $x_{dw}=\mathbf{1}[\text{word }w\text{ occurs in document }d]$.
With the smoothed training IDF above and $\epsilon=10^{-12}$, define
$$u_d=x_d\odot\operatorname{idf},\qquad
v_d=\frac{u_d}{\max(\lVert u_d\rVert_2,\epsilon)}.$$
For the training documents $D_k$ in class $k$,
$$\bar v_k=\frac1{|D_k|}\sum_{d\in D_k}v_d,\qquad
c_k=\frac{\bar v_k}{\max(\lVert\bar v_k\rVert_2,\epsilon)},\qquad s_{dk}=v_d^\top c_k.$$
$\odot$ means elementwise multiplication, $\lVert\cdot\rVert_2$ Euclidean vector length,
$c_k$ the normalized class prototype, and $s_{dk}$ its similarity to document $d$.
The code normalizes individual documents
**before** averaging and then normalizes each prototype. For nonzero unit vectors,
the dot product is cosine similarity. With our nonnegative lexical features it lies in 0–1;
general cosine similarity can be negative. Zero inputs produce zero scores by this explicit
implementation rule; mathematical cosine is undefined for a zero vector.
[Salton and Buckley (1988)](https://doi.org/10.1016/0306-4573(88)90021-0) discuss term weighting.
Our exact smoothed binary IDF convention is from the linked feature-extraction documentation,
not an equation claimed to be identical to the paper's weighting schemes.
'''), ('### 4. Compare behavior', r'''
**Math companion · account for every case**

$$N=N_{correct}+N_{wrong}+N_{review},\qquad
\operatorname{coverage}=\frac{N_{correct}+N_{wrong}}N.$$
$$\operatorname{automatic\ accuracy}=\frac{N_{correct}}{N_{correct}+N_{wrong}}.$$
$N_{correct}$ and $N_{wrong}$ count **automatically routed** cases; $N_{review}$ counts reviewed cases.
The accuracy denominator excludes reviewed cases and is undefined if all cases are reviewed.
This is accounting for the authored experiment, not a model-family benchmark.
Keyword ties lead to review. Positive lexical-similarity ties instead follow `argmax`'s
first-class ordering; the two implementations deliberately have different tie rules.
''')],
    '10': [('### 3. Trace one real', r'''
**Math companion · the loss used by `CrossEntropyLoss`**

$$p_{ik}=\frac{e^{z_{ik}}}{\sum_j e^{z_{ij}}},\qquad
L=-\frac1N\sum_{i=1}^{N}\log p_{i,y_i}.$$
$z_{ik}$ is the raw logit for case $i$ and class $k$; $y_i$ is the reference class index.
$N$ is the current batch size and $p_{ik}$ is its predicted class probability.
The library combines log-softmax with this loss numerically. Pass raw logits into the loss;
use softmax probabilities for reporting. This PyTorch experiment uses no L2 penalty.
Log loss is a proper scoring rule; see [Gneiting and Raftery (2007)](https://doi.org/10.1198/016214506000001437).
'''), ('### 4. Choose six ways', r'''
**Math companion · how each `nn.Module` computes its scores**

You can read one model at a time. Here $x$ is a row vector of word-presence features,
$e_t$ a learned 16-dimensional vector for token position $t$, and $\ell$ the number of
real tokens. Each $W$ and $b$ is a learned weight matrix or bias with compatible dimensions.
These equations use row vectors. PyTorch stores `nn.Linear.weight` as output-by-input,
so the mathematical $W$ is the transpose of that stored weight.
Every pooled representation below is passed through a learned linear head to get three logits.

**Linear and MLP:** the hidden layer in this implementation uses `Tanh`.
$$z=xW+b,\qquad
z_{MLP}=\tanh(xW_1+b_1)W_2+b_2.$$
Identical word-presence vectors remain identical through either deterministic network.

**Mean embeddings:** exclude padding from the sum and the denominator.
$$\bar e=\frac1\ell\sum_{t=1}^{\ell}e_t,\qquad z=\bar eW+b.$$
The average retains word multiplicity but discards order. Reordering the same tokens does not
change its value, apart from floating-point summation noise.

**CNN:** 24 three-token filters create 24 local features, followed by ReLU and max pooling.
$$f_t=\operatorname{ReLU}\!\left(b_c+\sum_{\Delta=-1}^{1}e_{t+\Delta}U_\Delta\right),
\qquad h_j=\max_{1\leq t\leq\ell}f_{tj}.$$
$\Delta$ is a filter offset; $U_\Delta$ is its weight matrix, $b_c$ the convolution bias,
$f_t$ the local feature vector, $j$ a feature index, and $h_j$ its pooled feature.
Vectors outside the real sequence are zero. PyTorch `Conv1d` performs this cross-correlation;
pooling includes only real-token centers. [Kim (2014)](https://aclanthology.org/D14-1181/)
provides the sentence-CNN background; our dimensions and training setup differ.

**GRU:** let $a_r,a_u,a_n$ map the current token vector and $b_r,b_u,b_n$ map the previous
hidden state. All six functions are separate learned affine maps, including biases.
$$\begin{aligned}
r_t&=\sigma(a_r(e_t)+b_r(h_{t-1})),\\
u_t&=\sigma(a_u(e_t)+b_u(h_{t-1})),\\
\tilde h_t&=\tanh(a_n(e_t)+r_t\odot b_n(h_{t-1})),\\
h_t&=(1-u_t)\odot\tilde h_t+u_t\odot h_{t-1}.
\end{aligned}$$
$r_t$ is a reset gate, $u_t$ an update gate, $\sigma$ the sigmoid, and $\odot$ elementwise
multiplication. $h_t$ is the hidden-state vector after token $t$, with initial $h_0=0$ here.
The packed GRU uses $h_\ell$, not a state after padding. These equations match
[PyTorch's GRU variant](https://docs.pytorch.org/docs/stable/generated/torch.nn.GRU.html).
In [Cho et al. (2014)](https://aclanthology.org/D14-1179/), the reset is applied before the
hidden-state projection; PyTorch applies it after that affine map. This lab is not an exact
reproduction of that paper.

**Transformer:** add learned position vectors, then contextualize with the encoder.
$$H=\operatorname{Encoder}(E+P_{position},M),\qquad
h=\frac1\ell\sum_{t=1}^{\ell}H_t.$$
Within each attention head,
$$\operatorname{Attention}(Q,K,V)=
\operatorname{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}+M\right)V.$$
$E$ is the token-embedding matrix, $P_{position}$ the learned position matrix, and
$H$ the contextualized token vectors; $h$ is their masked average.
$Q,K,V$ are projected queries, keys, and values; $d_k=8$ per head here.
The additive mask $M$ is zero for permitted keys and $-\infty$ for padded keys. The PyTorch
Boolean padding mask uses `True` for **blocked**, unlike the allowed-connection mask in lesson 06.
The encoder also includes two heads, a GELU feedforward block, residual connections, and layer
normalization; attention alone is not the whole encoder. [Vaswani et al. (2017)](https://arxiv.org/abs/1706.03762)
introduce the Transformer. Our one-layer classifier uses learned positions and different dimensions
from their translation model. It does not reproduce or establish Jev's unpublished architecture.
'''), ('### 5. Train, validate, and freeze', r'''
**Math companion · what Adam updates**

With loss gradient $g_t=\nabla_\theta L_t$ and initial $m_0=v_0=0$,
$$m_t=\beta_1m_{t-1}+(1-\beta_1)g_t,\qquad
v_t=\beta_2v_{t-1}+(1-\beta_2)g_t^2.$$
$$\hat m_t=\frac{m_t}{1-\beta_1^t},\qquad
\hat v_t=\frac{v_t}{1-\beta_2^t},\qquad
\theta_t=\theta_{t-1}-\alpha\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}.$$
$\theta$ collects all trainable parameters, $t$ numbers optimizer updates, $m_t$ smooths
gradients, and $v_t$ smooths squared gradients. $\beta_1,\beta_2$ control that smoothing.
All operations are elementwise. The defaults used here are $\beta_1=0.9$, $\beta_2=0.999$,
$\epsilon=10^{-8}$, with $\alpha=0.01$, zero weight decay, and no AMSGrad.
The epsilon is **outside** the square root. The moving moments adapt the update size;
the bias corrections account for starting at zero. See [Kingma and Ba (2015)](https://arxiv.org/abs/1412.6980),
Algorithm 1. Our full-batch toy task is separate from the paper's experiments.
'''), ('### 7. Evaluate every seed', r'''
**Math companion · sentence and pair accuracy measure different things**

$$\operatorname{accuracy}=\frac1N\sum_{i=1}^{N}\mathbf{1}[\hat y_i=y_i].$$
$$\operatorname{pair\ accuracy}=\frac1{N_{pairs}}\sum_{j=1}^{N_{pairs}}
\mathbf{1}[\hat y_{j,a}=y_{j,a}\ \text{and}\ \hat y_{j,b}=y_{j,b}].$$
$N=172$ sentences and $N_{pairs}=86$ reversed pairs in the test set.
$\hat y$ is a prediction, $y$ a reference label, $j$ indexes a pair, and $a,b$ identify its two members.
A pair with one wrong prediction contributes zero to pair accuracy, even when its other member is right.
Probability quality uses the mean NLL above and the summed multiclass Brier convention:
$$\operatorname{BS}_{multi}=\frac1N\sum_i\sum_{k=0}^{2}
\left(p_{ik}-\mathbf{1}[y_i=k]\right)^2.$$
For identical deterministic inputs with opposite reference labels, at most one member per pair
can be right: $\operatorname{accuracy}\leq1/2$ and $\operatorname{pair\ accuracy}=0$.
This is an information limitation, not a statement that all sequence models must succeed.
''')],
}


def reference_text(number):
    lines = ['## Paper references',
             'Read these for the general methods used or contrasted in this lesson. '
             'They do not establish Jev’s unpublished architecture or RLCD algorithm. '
             'The formulas above are code-matched teaching notation unless explicitly attributed.']
    for key in READINGS[number]:
        author, title, venue, url, relevance = PAPERS[key]
        lines.append(f'- **{author}.** [{title}]({url}). {venue}. {relevance}')
    lines.append('[Paper reading guide and equation map](PAPER_GUIDE.md) · [Jev documentation and source limits](SOURCES.md).')
    return '\n\n'.join(lines)


def enrich_math(name, cells, md):
    number = name[:2]
    if number not in COMPANIONS:
        raise ValueError(f'No mathematical companion for {name}')
    # This owned metadata makes direct updates idempotent without altering code cells.
    result = [cell for cell in cells if not cell.get('metadata', {}).get('course_math')]
    for index, (anchor, text) in enumerate(COMPANIONS[number]):
        matches = [i for i, cell in enumerate(result)
                   if cell.cell_type == 'markdown' and anchor in cell.source]
        if len(matches) != 1:
            raise ValueError(f'{name}: expected one math anchor {anchor!r}; found {len(matches)}')
        chunks = re.split(r'\n\n(?=\*\*(?:Linear and MLP|Mean embeddings|CNN|GRU|Transformer):\*\*)',
                          dedent(text).strip())
        for part, chunk in enumerate(chunks):
            cell = md(chunk)
            cell.metadata['course_math'] = f'{number}-{index}-{part}'
            cell.id = f'math-{number}-{index}-{part}'
            result.insert(matches[0]+1+part, cell)
    references = md(reference_text(number))
    references.metadata['course_math'] = 'references'
    references.id = f'math-{number}-papers'
    result.append(references)
    return result


def main():
    import nbformat
    from course_paths import NOTEBOOKS, rewrite_legacy_markdown
    for path in sorted(NOTEBOOKS.glob('[0-9][0-9]_*.ipynb')):
        nb = nbformat.read(path, as_version=4)
        previous_code = [cell for cell in nb.cells if cell.cell_type == 'code']
        nb.cells = enrich_math(path.name, nb.cells, nbformat.v4.new_markdown_cell)
        for cell in nb.cells:
            if cell.metadata.get('course_math'):
                cell.source = rewrite_legacy_markdown(cell.source, 'notebooks/'+path.name)
        assert previous_code == [cell for cell in nb.cells if cell.cell_type == 'code']
        nbformat.validate(nb)
        nbformat.write(nb, path)
        print(f'{path.name}: math and papers added; code and saved outputs preserved.')


if __name__ == '__main__':
    main()
