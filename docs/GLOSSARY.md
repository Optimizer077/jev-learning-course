# Working glossary

## Start with these five words

| Word | Plain-language meaning | First example |
|---|---|---|
| Evidence | What happened, or what the input contains. | The customer message says the export crashes. |
| Question | The judgment you ask the model to make. | Which support queue fits this message? |
| Probability | A number expressing the model's estimate of an outcome. | 0.90 means 90%; it is not a guarantee. |
| Policy | Your program's rule for choosing what to do. | Route above a threshold; otherwise review. |
| Evaluation | Checking behavior on examples with reference answers. | Count correct routes on held-out messages. |

[Lesson 01](../notebooks/01_jev_basics.ipynb) puts these ideas together. The remaining terms are references;
you do not need to memorize them before starting.

## Interface and machine-learning terms

| Term | Meaning in this course |
|---|---|
| State | Evidence supplied for a decision; it is not the answer label. |
| Choice | One selected option plus a distribution over the supplied alternatives. |
| Score | Expected position over ordered rubric levels; not an exact physical measurement. |
| Noul | A probability for the positive answer to a yes/no question. |
| Logit | A real-valued score before probability normalization. |
| Feature | An input number used by a model; text models need a representation that produces such numbers. |
| Weight | A learned parameter that determines an input's contribution to a score. |
| Bias | An added offset in a scoring calculation. |
| Matrix | A rectangular table of numbers; rows and columns keep calculations organized. |
| Representation | The numbers used to describe an input; what it omits can limit the model. |
| Prototype | A representative feature vector, such as an average of examples within a class. |
| Cosine similarity | Alignment between vector directions; a similarity score, not inherently a probability. |
| TF–IDF | Term-frequency and inverse-document-frequency weighting; the lab uses binary term presence with smoothed IDF. |
| Abstention | Choosing review instead of making an automatic prediction. |
| Softmax | Normalizes scores; normalization does not establish calibration. |
| Temperature | A positive divisor of logits that changes concentration while preserving ranking. |
| Calibration | Agreement between probabilities and outcome frequencies across cases. |
| Confidence | In Jev, a summary derived from a Choice/Score distribution; its precise formula is not supplied in the reviewed page. |
| Discrimination | Ability to distinguish cases with different outcomes. |
| Cross-entropy / log loss | Penalizes low probability assigned to the observed class. |
| Brier score | Squared probability error; binary and multiclass conventions differ. |
| Proper scoring rule | An expected scoring objective optimized by reporting the true distribution. |
| Gradient | Local rate of change of a loss with respect to parameters. |
| Calibration split | Data used to fit probability adjustments after training. |
| Test split | Data reserved for assessing the frozen model and policy. |
| Leakage | Information enters fitting/evaluation that would not be available at prediction time. |
| Coverage | Fraction of cases handled automatically under a selective policy. |
| Selective error | Error rate among automatic cases only; state the denominator. |
| Distribution shift | A change in inputs or their relationship to outcomes. |
| Attention mask | Specifies which positions can read which other positions. |
| Parallel evaluation | Scheduling computations together; not statistical independence. |
| RLCD | Reinforcement Learning for Calibrated Decisions; we illustrate its motivation, not the proprietary algorithm. |
| Closed set | Answers must belong to supplied options, even when all options are poor. |
| Out of domain | Outside the population or task evaluated during development. |
