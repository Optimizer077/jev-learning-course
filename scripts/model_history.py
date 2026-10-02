"""Source-backed historical context and unexecuted model comparisons."""

HISTORY_TRACKS = [
    ('Evaluate probabilities', '#0d766f', '#e5f6f2', [
        ('1950', 'Probability forecasts', 'Brier: score estimates\nagainst observed outcomes.'),
        ('1970', 'Recognition or review', 'Chow: balance recognition\nerrors and rejection.'),
        ('2017', 'Modern calibration', 'Guo: check confidence\nand fit temperature.'),
    ]),
    ('Represent the input', '#6245b7', '#eee9fc', [
        ('1986 / 1988', 'Gradients and word weights', 'Backpropagation milestone;\nterm-weighting study.'),
        ('2014', 'CNNs and gated recurrence', 'Kim: local word windows.\nCho: recurrent gates.'),
        ('2017', 'Transformer attention', 'Vaswani: attention plus\nposition information.'),
    ]),
    ('Adapt to a task', '#b7432b', '#fceee9', [
        ('2019', 'BERT and RoBERTa', 'Pretrained contextual encoders\nwith downstream adaptation.'),
        ('2019', 'Sentence vectors / hypotheses', 'Sentence-BERT matching;\nYin: labels as hypotheses.'),
        ('2022 preprint', 'SetFit', 'Adapt sentence embeddings,\nthen fit a task classifier.'),
    ]),
]

NEW_ROWS = '''| Contextual encoder plus classifier | Build context-sensitive representations, then predict a task label | A learned task output | No; BERT and RoBERTa are background reading |
| Sentence-BERT matching | Compare pretrained contextual sentence vectors | Similarity, not automatically a probability | No; paper-based comparison |
| Entailment-based classification | Treat the text as evidence and candidate descriptions as hypotheses | Entailment-based judgments | No; paper-based comparison |
| SetFit | Adapt a pretrained sentence encoder and fit a classifier with labeled examples | Outputs for the learned task classes | No; paper-based comparison |'''

BACKGROUND = {
    '06': ('### 1. Fixed class heads', r'''
**Paper connection · three ways to use candidate descriptions**

Our overlap scores below use word-presence vectors. The research offers richer choices:
[Sentence-BERT](https://aclanthology.org/D19-1410/) compares trained contextual sentence vectors;
an [entailment approach](https://aclanthology.org/D19-1404/) reads a text together with a label
hypothesis; [SetFit](https://arxiv.org/abs/2209.11055) learns a classifier from a small labeled task set.
These differ in what must be encoded together, how labels enter, and what training is required.
None is executed in this cell or disclosed as Jev's implementation.

The [history and comparison guide](MODEL_HISTORY.md) explains the papers and their scope.
'''),
    '10': ('### 4. Choose six ways', r'''
**Paper connection · small random models versus pretrained encoders**

The CNN, GRU, and attention ideas have published antecedents in the 2014 and 2017 papers
linked below. Our small classifiers start from random weights and learn the authored toy task.
[BERT](https://aclanthology.org/N19-1423/) and [RoBERTa](https://arxiv.org/abs/1907.11692)
instead pretrain contextual language representations before task adaptation.

Mean pooling alone does not make our toy a [Sentence-BERT model](https://aclanthology.org/D19-1410/).
Our token vector depends only on the word, so rearranging the same tokens leaves its mean unchanged.
A contextual encoder's token vectors depend on the sequence and positions **before** pooling;
their mean need not have that invariance. Whether an unexecuted model answers the reversed pair
correctly remains a question for an actual evaluation.

Read the optional [method history](MODEL_HISTORY.md) after inspecting one trained model.
'''),
}

RELATED_READING = r'''
## Paper reading · history and nearby methods

The experiment above measures three local methods. The following are **reading comparisons**;
no BERT, RoBERTa, Sentence-BERT, entailment model, or SetFit weights are loaded here.

### Follow three ways of supplying a label

For the message “The payment failed, not the export,” compare these possible workflows:

1. **Sentence-BERT matching:** encode the message and descriptions such as “billing issue” and
   compare their sentence vectors. The paper trains a shared contextual encoder for meaningful
   sentence embeddings. Cosine similarity does not become an 80% probability merely because it is 0.8.
2. **Entailment-based classification:** treat the message as a premise and a candidate description
   as a hypothesis, such as “This text describes a billing problem.” This task is natural language
   inference (NLI). Yin, Hay, and Roth's paper
   trains binary entailment/non-entailment models on source inference datasets. This is not a claim
   that their exact method is a modern three-class zero-shot pipeline. “Zero-shot” describes the
   target-label setting; the source model was trained previously. Its fully-unseen setup uses
   source training, while its partially-unseen setup also fits provided seen-label task examples.
3. **SetFit:** provide labeled task examples, adapt a pretrained Sentence Transformer through
   contrastive sentence pairs, then train a logistic-regression head on the original examples.
   The encoder learns higher similarity for same-label pairs and lower similarity for different-label pairs.
   Generated pairs reuse those examples; they do not create new independent labeled evidence.

**Check your understanding:** add a fourth queue called “account access.” Which workflow accepts
a new description at prediction time, and which needs new labeled examples and task fitting?
What would you measure before trusting the new queue's predictions?
The purpose is to compare mechanisms, not to invent results for models we did not run.

### A short history of the methods

The graphic below groups selected publication milestones. It is a map of ideas relevant to this
course, not a claim about Jev's private ancestry. The dates identify the linked papers, rather
than the first invention of every idea. The [full guide](MODEL_HISTORY.md) supplies the links,
similarities, differences, and a suggested reading order.
'''


def enrich_history(name, cells, md, code):
    number = name[:2]
    result = [cell for cell in cells if not cell.get('metadata', {}).get('course_history')]
    if number in BACKGROUND:
        anchor, source = BACKGROUND[number]
        matches = [i for i, cell in enumerate(result) if cell.cell_type == 'markdown' and anchor in cell.source]
        if len(matches) != 1:
            raise ValueError(f'{name}: history anchor {anchor!r} missing or repeated')
        cell = md(source)
        cell.id = f'history-{number}-reading'
        cell.metadata['course_history'] = 'reading'
        result.insert(matches[0]+1, cell)
    if number == '09':
        original = ('| Contextual encoder plus classifier | Build context-sensitive representations, '
                    'then predict a task label | A learned task output | No; see the linked BERT paper |')
        matches = [cell for cell in result if cell.cell_type == 'markdown' and original in cell.source]
        if len(matches) == 1:
            matches[0].source = matches[0].source.replace(original, NEW_ROWS)
        elif not any(NEW_ROWS in cell.source for cell in result if cell.cell_type == 'markdown'):
            raise ValueError(f'{name}: related-method table missing or changed')
        matches = [i for i, cell in enumerate(result) if cell.cell_type == 'markdown' and '## Next Steps' in cell.source]
        if len(matches) != 1:
            raise ValueError(f'{name}: next-step anchor missing or repeated')
        reading = md(RELATED_READING)
        reading.id = 'history-09-reading'
        reading.metadata['course_history'] = 'reading'
        diagram = code("""from tutorial_utils import show_diagram
show_diagram('model-history-mobile', 'Selected paper milestones grouped by probability evaluation, input representation, and task adaptation. Dates refer to publications, not a claimed Jev lineage. See the adjacent history guide for source links.')""")
        diagram.id = 'history-09-diagram'
        diagram.metadata['course_history'] = 'diagram'
        result[matches[0]:matches[0]] = [reading, diagram]
    return result
