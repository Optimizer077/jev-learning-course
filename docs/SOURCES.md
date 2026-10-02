# Primary sources

Checked 2026-10-01. These are TypeSafe's own statements, not independent replication. No third-party Jev-branded API is used.

| Source | Used for |
|---|---|
| [Announcement](https://typesafe.ai/blog/introducing-system-one-models-and-jev) | Introduction, architecture/sampler/RLCD claims and benchmark caveats |
| [Introduction](https://docs.typesafe.ai/introduction) | Interface and parallel question evaluation |
| [System One](https://docs.typesafe.ai/concepts/system-one) | Product definition and calibration qualification |
| [AI primer](https://docs.typesafe.ai/introduction/machine-learning-primer) | Stated RLCD objective, distinct from our toy supervised training |
| [Choice](https://docs.typesafe.ai/primitives/choice) | Categorical decisions |
| [Score](https://docs.typesafe.ai/primitives/score) | Ordered levels and expectation |
| [Noul](https://docs.typesafe.ai/primitives/noul) | Yes/no probabilities |
| [Confidence](https://docs.typesafe.ai/confidence) | Distribution-derived confidence; no Noul confidence field |
| [Models](https://docs.typesafe.ai/models) | Version pinning and text-only input |
| [API](https://docs.typesafe.ai/api) | Request and response contract |
| [Known limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13) | Numeric precision, context distraction, adversarial input, and cross-question consistency |
| [Structured questions](https://docs.typesafe.ai/primitives/advanced) | Structured rubrics |
| [Speculative fan-out](https://docs.typesafe.ai/patterns/fan-out) | Provider-described question batching |
| [Guo et al., 2017](https://proceedings.mlr.press/v70/guo17a.html) | Temperature scaling, not RLCD |
| [Vaswani et al., 2017](https://arxiv.org/abs/1706.03762) | Generic attention, not Jev's architecture |
| [Devlin et al., 2019](https://aclanthology.org/N19-1423/) | BERT as a related language representation |
| [scikit-learn feature-extraction documentation](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction) | TF–IDF conventions; lesson 09 implements a binary term-presence variant in NumPy |

All datasets, toy logits, timing constants, and workflow answers in this folder are invented educational examples. They are not exported Jev responses. Calibration experiments illustrate general probability mathematics and do not measure Jev. The direct-scoring toy demonstrates an idea, not TypeSafe's architecture.

The research papers describe related methods and do not establish Jev's unpublished implementation.
Probability bounds, expected-cost thresholds, and the Brier-loss minimum are derived in the notebooks.

## Paper references and equations in every notebook

The [paper reading guide](PAPER_GUIDE.md) maps the equations to all eleven lessons.
Every notebook includes primary-paper citations and optional math companions beside its examples.
The notation is adapted to the actual course code; it does not purport to specify Jev's internals.

Research-source verification was refreshed **2026-10-02** using primary PDFs, ACL bibliography
records, and publisher DOI metadata through command-line tools. No browser webpages were opened.
The TypeSafe documentation check date above remains separate.

| Paper | Evidence accessed | Equation or method used |
|---|---|---|
| [Guo et al. (2017), On Calibration of Modern Neural Networks](https://proceedings.mlr.press/v70/guo17a.html) | Primary PDF, sections 2 and 4.2 | Temperature scaling and NLL; course losses are means, and lesson 03 bins binary yes-probabilities rather than top-label confidence |
| [Vaswani et al. (2017), Attention Is All You Need](https://arxiv.org/abs/1706.03762) | Primary PDF, sections 3.2–3.5 | Scaled attention, equation 1; our masks, learned positions, and classifier are educational adaptations |
| [Devlin et al. (2019), BERT](https://aclanthology.org/N19-1423/) | Primary PDF, sections 3 and 4.1; ACL bibliography | Contextual representations and classification background; not executed or downloaded as a model |
| [Kim (2014), Convolutional Neural Networks for Sentence Classification](https://aclanthology.org/D14-1181/) | Primary PDF, section 2; ACL bibliography | Local filters and max-over-time pooling; different toy settings |
| [Cho et al. (2014), Learning Phrase Representations using RNN Encoder–Decoder for Statistical Machine Translation](https://aclanthology.org/D14-1179/) | Primary PDF, section 2.3, equations 5–8; ACL bibliography | Historical GRU; PyTorch's reset-after variant is explicitly distinguished |
| [Kingma and Ba (2015), Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980) | Primary PDF, Algorithm 1 | Bias-corrected moment updates; conference year 2015, first preprint 2014 |
| [Gneiting and Raftery (2007), Strictly Proper Scoring Rules, Prediction, and Estimation](https://doi.org/10.1198/016214506000001437) | Author-hosted primary PDF, sections 2 and 3.1 | Propriety; quadratic and log scores in Examples 1 and 3, converted from rewards to losses |
| [Rumelhart, Hinton, and Williams (1986), Learning representations by back-propagating errors](https://doi.org/10.1038/323533a0) | Author-hosted scanned primary paper, pages 1–2 | Backpropagation background; our linear softmax gradient is a separate classroom derivation |
| [Brier (1950), Verification of Forecasts Expressed in Terms of Probability](https://doi.org/10.1175/1520-0493(1950)078%3C0001:VOFEIT%3E2.0.CO;2) | Publisher bibliographic metadata; original full text unavailable | Historical source; checked categorical formula is available in Gneiting and Raftery, Example 1 |
| [Chow (1970), On Optimum Recognition Error and Reject Tradeoff](https://doi.org/10.1109/TIT.1970.1054406) | Publisher bibliographic metadata; original full text unavailable | Historical recognition/rejection setting; our cost equations are derived from stated assumptions |
| [Salton and Buckley (1988), Term-weighting approaches in automatic text retrieval](https://doi.org/10.1016/0306-4573(88)90021-0) | Publisher bibliographic metadata; original full text unavailable | Historical term weighting; exact smoothed IDF follows the implementation convention linked above |
| [Efron (1979), Bootstrap Methods: Another Look at the Jackknife](https://doi.org/10.1214/aos/1176344552) | Publisher bibliographic metadata; original full text unavailable | Historical resampling framework; lesson 03 defines its percentile-interval calculation explicitly |

No unchecked paper equation numbers are supplied for unavailable full texts. The derivative,
cost bounds, case accounting, and pair-accuracy ceiling are course derivations. Binary
one-probability Brier and full-category Brier have different scales, stated beside their formulas.
None of the cited papers independently reproduces Jev or validates this course's toy results.

## PyTorch lab references

Lesson 10 was exercised locally with **PyTorch 2.14.1+cpu**, installed from the official CPU
wheel index on **2026-10-02**. Installed API documentation and executable checks support the
implementation. The links below are reference destinations; their webpages were not reopened.

| Primary reference | Used for |
|---|---|
| [CrossEntropyLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html) | Raw class logits and integer targets |
| [Embedding](https://docs.pytorch.org/docs/stable/generated/torch.nn.Embedding.html) | Learned token vectors and padding |
| [Conv1d](https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv1d.html) | Three-token local filters |
| [GRU](https://docs.pytorch.org/docs/stable/generated/torch.nn.GRU.html) | Recurrent sequence encoder |
| [Packed sequences](https://docs.pytorch.org/docs/stable/generated/torch.nn.utils.rnn.pack_padded_sequence.html) | Ignore padded suffixes in the GRU |
| [TransformerEncoder](https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoder.html) | Masked attention with supplied position vectors |

The 864 sentences, fixed experiment, and six model classes are authored course material.
Neither the installed library nor these references establish anything about Jev's internals.
