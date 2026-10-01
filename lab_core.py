"""Transparent NumPy teaching baselines. None of these functions implements Jev."""
from pathlib import Path
import json
import re
import numpy as np

ROOT = Path(__file__).resolve().parent
LABELS = ('billing', 'technical', 'account')

def softmax(logits, temperature=1.0):
    if not np.isfinite(temperature) or temperature <= 0:
        raise ValueError('Temperature must be finite and positive')
    z = np.asarray(logits, dtype=float) / temperature
    z -= z.max(axis=-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)

def nll(probabilities, labels):
    p = np.asarray(probabilities)
    y = np.asarray(labels, dtype=int)
    return float(-np.log(p[np.arange(len(y)), y].clip(1e-12, 1)).mean())

def multiclass_brier(probabilities, labels):
    """Sum squared error across classes, then mean across examples (range 0..2)."""
    p = np.asarray(probabilities)
    return float(np.square(p - np.eye(p.shape[1])[labels]).sum(axis=1).mean())

def tokenise(text):
    return re.findall(r"[a-z]+", text.lower())

def vocabulary(texts):
    return {word: i for i, word in enumerate(sorted({w for t in texts for w in tokenise(t)}))}

def vectorise(texts, vocab):
    """Binary bag of words. Vocabulary must be fitted on training text only."""
    matrix = np.zeros((len(texts), len(vocab)))
    for row, text in enumerate(texts):
        for word in set(tokenise(text)):
            if word in vocab:
                matrix[row, vocab[word]] = 1.0
    return matrix

def fit_linear(X, y, steps=800, learning_rate=0.4, regularisation=0.02):
    weights = np.zeros((X.shape[1], len(LABELS)))
    bias = np.zeros(len(LABELS))
    targets = np.eye(len(LABELS))[y]
    losses = []
    for _ in range(steps):
        p = softmax(X @ weights + bias)
        losses.append(nll(p, y) + regularisation * np.square(weights).sum() / 2)
        gradient = (p - targets) / len(y)
        weights -= learning_rate * (X.T @ gradient + regularisation * weights)
        bias -= learning_rate * gradient.sum(axis=0)
    return weights, bias, np.array(losses)

def load_tickets():
    return json.loads((ROOT / 'data' / 'tickets.json').read_text(encoding='utf-8'))

def train_text_baseline():
    rows = load_tickets()
    training = [r for r in rows if r['split'] == 'train']
    vocab = vocabulary([r['text'] for r in training])
    X = vectorise([r['text'] for r in training], vocab)
    y = np.array([LABELS.index(r['label']) for r in training])
    weights, bias, losses = fit_linear(X, y)
    return rows, vocab, weights, bias, losses

def split_arrays(rows, split, vocab):
    selected = [r for r in rows if r['split'] == split]
    X = vectorise([r['text'] for r in selected], vocab)
    y = np.array([LABELS.index(r['label']) for r in selected])
    return selected, X, y

def choose_temperature(logits, y):
    grid = np.geomspace(0.25, 5, 121)
    losses = np.array([nll(softmax(logits, t), y) for t in grid])
    return float(grid[losses.argmin()]), grid, losses

def selective_metrics(p, y, cutoff, review_cost=0.2, error_cost=1.0):
    automatic = p.max(axis=1) >= cutoff
    wrong = p.argmax(axis=1) != y
    return {
        'cutoff': float(cutoff),
        'automatic': int(automatic.sum()), 'total': len(y),
        'coverage': float(automatic.mean()),
        'error': float(wrong[automatic].mean()) if automatic.any() else None,
        'cost': float(np.mean(error_cost * (automatic & wrong) + review_cost * ~automatic)),
    }

def confusion_counts(y, predicted, classes=3):
    result = np.zeros((classes, classes), dtype=int)
    np.add.at(result, (y, predicted), 1)
    return result
