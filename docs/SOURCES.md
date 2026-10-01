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
