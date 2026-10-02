"""Fast, independent integrity checks for the small CPU PyTorch teaching lab.

Run from any folder: python path/to/scripts/check_torch_lab.py
The short training fixtures validate implementation; they are not model benchmarks.
"""
from collections import Counter, defaultdict
import math
from pathlib import Path
import sys

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from lab_core import LABELS, tokenise
import torch_lab as lab


def subset(batch, count):
    return {key: value[:count].clone() if isinstance(value, torch.Tensor) else value[:count]
            for key, value in batch.items()}


def independent_metrics(logits, labels, rows):
    """Scalar arithmetic, independent of the lab's metric and softmax helpers."""
    probabilities, nll, brier, predictions = [], 0.0, 0.0, []
    for scores, label in zip(logits.tolist(), labels.tolist()):
        maximum = max(scores)
        exponentials = [math.exp(score - maximum) for score in scores]
        denominator = sum(exponentials)
        probability = [value / denominator for value in exponentials]
        probabilities.append(probability)
        predictions.append(max(range(len(scores)), key=lambda index: scores[index]))
        nll += maximum + math.log(denominator) - scores[label]
        brier += sum((value - (index == label)) ** 2
                     for index, value in enumerate(probability))
    correct = [predicted == label for predicted, label in zip(predictions, labels.tolist())]
    groups = defaultdict(list)
    for index, row in enumerate(rows):
        groups[row['pair_id']].append(index)
    assert all(len(indices) == 2 for indices in groups.values()), 'Incomplete evaluation pair'
    both_correct = sum(all(correct[index] for index in indices) for indices in groups.values())
    return {'probabilities': probabilities, 'correct': sum(correct), 'total': len(rows),
            'both_correct': both_correct, 'pairs': len(groups),
            'nll': nll / len(rows), 'brier': brier / len(rows)}


def check_data():
    rows = lab.load_toy_rows()
    assert rows == lab.make_toy_rows(), 'Saved data differ from the documented generator'
    assert len({row['id'] for row in rows}) == len(rows), 'Duplicate example ID'
    assert len({tuple(tokenise(row['text'])) for row in rows}) == len(rows), 'Duplicate text'
    groups = defaultdict(list)
    for row in rows:
        groups[row['pair_id']].append(row)
    for pair in groups.values():
        assert len(pair) == 2 and pair[0]['label'] != pair[1]['label']
        assert pair[0]['split'] == pair[1]['split'], 'Pair crosses split boundary'
        assert Counter(tokenise(pair[0]['text'])) == Counter(tokenise(pair[1]['text']))
    vocab, splits = lab.prepare_data(rows)
    expected_words = {word for row in rows if row['split'] == 'train'
                      for word in tokenise(row['text'])}
    assert set(vocab) - {'<pad>', '<unk>'} == expected_words
    # Existing splits share their vocabulary; a held-out-only sentinel detects leakage.
    sentinel = dict(rows[0], split='validation', text='heldoutonlysentinel')
    assert lab.fit_vocabulary(rows + [sentinel]) == vocab, 'Held-out text changes vocabulary'
    for batch in splits.values():
        assert batch['rows'] and batch['tokens'].dtype == batch['labels'].dtype == torch.long
        assert torch.equal(batch['lengths'], batch['tokens'].ne(lab.PAD).sum(dim=1))
        assert int(batch['lengths'].max()) <= lab.MAX_TOKENS
    return vocab, splits


def check_models(vocab, splits):
    batch = splits['test']
    pairs = defaultdict(list)
    for index, row in enumerate(batch['rows']):
        pairs[row['pair_id']].append(index)
    for name in lab.MODEL_NAMES:
        torch.manual_seed(123)
        model = lab.make_model(name, len(vocab))
        logits, probabilities = lab.predict(model, batch)
        assert logits.shape == (len(batch['rows']), len(LABELS))
        assert torch.isfinite(logits).all() and torch.isfinite(probabilities).all()
        assert torch.allclose(probabilities.sum(dim=1), torch.ones(len(batch['rows'])), atol=1e-6)
        altered = dict(batch, labels=(batch['labels'] + 1) % len(LABELS),
                       rows=[dict(row, label=LABELS[(LABELS.index(row['label']) + 1) % len(LABELS)])
                             for row in batch['rows']])
        assert torch.equal(logits, lab.predict(model, altered)[0]), 'Reference labels affect prediction'
        expected = independent_metrics(logits, batch['labels'], batch['rows'])
        actual = lab.evaluate(model, batch)
        assert np.allclose(probabilities.numpy(), expected['probabilities'], atol=1e-6)
        for key in ('correct', 'total', 'both_correct', 'pairs'):
            assert actual[key] == expected[key], (name, key)
        for key in ('nll', 'brier'):
            assert math.isclose(actual[key], expected[key], rel_tol=1e-6), (name, key)
        assert math.isclose(actual['pair_accuracy'], expected['both_correct'] / expected['pairs'])
        assert math.isclose(actual['accuracy'], expected['correct'] / expected['total'], abs_tol=1e-7)
        if name in ('BoW linear', 'BoW MLP', 'Mean embedding'):
            assert all(torch.allclose(logits[a], logits[b], atol=1e-6) for a, b in pairs.values())
            assert actual['both_correct'] == 0 and actual['correct'] <= len(batch['rows']) // 2
        single = subset(batch, 1)
        trimmed = dict(single, tokens=single['tokens'][:, :int(single['lengths'][0])])
        with torch.no_grad():
            assert torch.allclose(model(single), model(trimmed), atol=2e-6), (name, 'padding')
        if name == 'Transformer':
            assert any(not torch.allclose(logits[a], logits[b], atol=2e-6)
                       for a, b in pairs.values()), 'Positioned model cannot distinguish order'
            model.use_positions = False
            unordered, _ = lab.predict(model, batch)
            assert all(torch.allclose(unordered[a], unordered[b], atol=2e-6)
                       for a, b in pairs.values()), 'Position-free attention should lose order'
            model.use_positions = True
        model.train()
        model.zero_grad(set_to_none=True)
        torch.nn.functional.cross_entropy(model(splits['train']), splits['train']['labels']).backward()
        assert all(parameter.grad is not None and torch.isfinite(parameter.grad).all()
                   for parameter in model.parameters()), (name, 'gradient')
        if hasattr(model, 'embedding'):
            gradient = model.embedding.weight.grad[lab.PAD]
            assert torch.equal(gradient, torch.zeros_like(gradient)), (name, 'padding gradient')


def check_checkpoints(vocab, splits):
    # Small runs check all optimizers; the separate adverse fixture forces rollback.
    for name in lab.MODEL_NAMES:
        run = lab.train_one(name, len(vocab), splits['train'], splits['validation'], seed=7, epochs=3)
        assert np.isfinite(run['history']).all() and run['history'].shape == (3, 2)
        assert run['best_epoch'] == int(run['history'][:, 1].argmin()) + 1
        assert math.isclose(run['validation_loss'], float(run['history'][:, 1].min()), rel_tol=1e-6)
        logits, _ = lab.predict(run['model'], splits['validation'])
        expected = independent_metrics(logits, splits['validation']['labels'], splits['validation']['rows'])
        assert math.isclose(expected['nll'], run['validation_loss'], rel_tol=1e-6)
        assert not run['model'].training
    fixture = subset(splits['train'], 2)
    missing_label = next(index for index in range(len(LABELS)) if index not in fixture['labels'].tolist())
    adverse = dict(fixture, labels=torch.full((2,), missing_label, dtype=torch.long))
    continued = lab.train_one('BoW linear', len(vocab), fixture, adverse, seed=7, epochs=12)
    first_epoch = lab.train_one('BoW linear', len(vocab), fixture, adverse, seed=7, epochs=1)
    assert continued['best_epoch'] == 1 and continued['history'][-1, 1] > continued['history'][0, 1]
    assert all(torch.equal(value, first_epoch['model'].state_dict()[key])
               for key, value in continued['model'].state_dict().items()), 'Best checkpoint not restored'


def main():
    torch.set_num_threads(1)
    vocab, splits = check_data()
    check_models(vocab, splits)
    check_checkpoints(vocab, splits)
    print('PyTorch checks passed: generated data, splits, vocabulary, six model gradients/masks, '
          'label independence, independent metrics, order invariants, and checkpoint restoration.')


if __name__ == '__main__':
    main()
