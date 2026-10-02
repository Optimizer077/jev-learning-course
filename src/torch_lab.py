"""Six small PyTorch teaching models. This module does not implement Jev."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import random

import numpy as np
import torch
from torch import nn
from torch.nn.utils.rnn import pack_padded_sequence

from lab_core import LABELS, tokenise

ROOT = Path(__file__).resolve().parents[1]
PAD, UNKNOWN = 0, 1
MAX_TOKENS = 24  # Fixed before looking at test; no silent truncation.
MODEL_NAMES = ('BoW linear', 'BoW MLP', 'Mean embedding', 'CNN', 'GRU', 'Transformer')
SEEDS = (7, 19, 41)


def make_toy_rows():
    """Author reversed sentence pairs, then assign whole pairs to fixed splits."""
    topics = {
        'billing': ('payment', 'invoice', 'charge'),
        'technical': ('export', 'upload', 'download'),
        'account': ('login', 'password', 'signin'),
    }
    templates = (
        'The {first} failed, not the {second}.',
        'My {first} is broken; my {second} is not.',
        'It is {first} that fails, not {second}.',
        '{second} works fine, but {first} does not.',
    )
    prefixes = ('', 'Customer says: ', 'Today: ', 'Please help: ')
    pairs = []
    labels = list(topics)
    for left_index, left_label in enumerate(labels):
        for right_label in labels[left_index+1:]:
            for left in topics[left_label]:
                for right in topics[right_label]:
                    for template_index, template in enumerate(templates):
                        for prefix in prefixes:
                            pair_id = f'pair-{len(pairs):03d}'
                            pairs.append([
                                {'id': pair_id+'-a', 'pair_id': pair_id,
                                 'text': prefix+template.format(first=left, second=right),
                                 'label': left_label, 'template': template_index},
                                {'id': pair_id+'-b', 'pair_id': pair_id,
                                 'text': prefix+template.format(first=right, second=left),
                                 'label': right_label, 'template': template_index},
                            ])
    order = list(range(len(pairs)))
    random.Random(314).shuffle(order)
    split_for = {index: 'train' if rank < 260 else 'validation' if rank < 346 else 'test'
                 for rank, index in enumerate(order)}
    return [dict(row, split=split_for[index]) for index, pair in enumerate(pairs) for row in pair]


def load_toy_rows():
    return json.loads((ROOT/'data'/'torch_toy.json').read_text(encoding='utf-8'))


def validate_toy_rows(rows):
    normalized = [' '.join(tokenise(row['text'])) for row in rows]
    assert len(normalized) == len(set(normalized)), 'Repeated normalized text'
    groups = {}
    for row in rows:
        groups.setdefault(row['pair_id'], []).append(row)
        assert row['label'] in LABELS
    for pair in groups.values():
        assert len(pair) == 2
        assert len({row['split'] for row in pair}) == 1, 'Pair leaked across splits'
        assert pair[0]['label'] != pair[1]['label']
        assert Counter(tokenise(pair[0]['text'])) == Counter(tokenise(pair[1]['text']))
    return Counter(row['split'] for row in rows)


def fit_vocabulary(rows):
    words = sorted({word for row in rows if row['split'] == 'train' for word in tokenise(row['text'])})
    return {'<pad>': PAD, '<unk>': UNKNOWN, **{word: index+2 for index, word in enumerate(words)}}


def encode_rows(rows, vocab):
    tokens = torch.zeros((len(rows), MAX_TOKENS), dtype=torch.long)
    lengths = torch.zeros(len(rows), dtype=torch.long)
    bow = torch.zeros((len(rows), len(vocab)), dtype=torch.float32)
    for index, row in enumerate(rows):
        words = tokenise(row['text'])
        if not words or len(words) > MAX_TOKENS:
            raise ValueError(f'Expected 1..{MAX_TOKENS} tokens; got {len(words)}')
        ids = [vocab.get(word, UNKNOWN) for word in words]
        lengths[index] = len(ids)
        tokens[index, :len(ids)] = torch.tensor(ids)
        bow[index, list(set(ids))] = 1
    return {'tokens': tokens, 'lengths': lengths, 'bow': bow,
            'labels': torch.tensor([LABELS.index(row['label']) for row in rows], dtype=torch.long),
            'rows': rows}


def prepare_data(rows):
    validate_toy_rows(rows)
    vocab = fit_vocabulary(rows)
    splits = {split: encode_rows([row for row in rows if row['split'] == split], vocab)
              for split in ('train', 'validation', 'test')}
    return vocab, splits


class BagClassifier(nn.Module):
    def __init__(self, vocabulary_size, nonlinear=False):
        super().__init__()
        self.network = (nn.Sequential(nn.Linear(vocabulary_size, 24), nn.Tanh(), nn.Linear(24, 3))
                        if nonlinear else nn.Linear(vocabulary_size, 3))

    def forward(self, batch):
        return self.network(batch['bow'])


class MeanEmbedding(nn.Module):
    def __init__(self, vocabulary_size):
        super().__init__()
        self.embedding = nn.Embedding(vocabulary_size, 16, padding_idx=PAD)
        self.head = nn.Linear(16, 3)

    def forward(self, batch):
        # Averaging discards order. Padding contributes neither a vector nor a denominator.
        mask = batch['tokens'].ne(PAD).unsqueeze(-1)
        total = (self.embedding(batch['tokens'])*mask).sum(dim=1)
        mean = total/batch['lengths'].unsqueeze(1)
        return self.head(mean)


class TinyCNN(nn.Module):
    def __init__(self, vocabulary_size):
        super().__init__()
        self.embedding = nn.Embedding(vocabulary_size, 16, padding_idx=PAD)
        self.convolution = nn.Conv1d(16, 24, kernel_size=3, padding=1)
        self.head = nn.Linear(24, 3)

    def forward(self, batch):
        embedded = self.embedding(batch['tokens']).transpose(1, 2)
        features = torch.relu(self.convolution(embedded))
        mask = batch['tokens'].ne(PAD).unsqueeze(1)
        pooled = features.masked_fill(~mask, -torch.inf).amax(dim=2)
        return self.head(pooled)


class TinyGRU(nn.Module):
    def __init__(self, vocabulary_size):
        super().__init__()
        self.embedding = nn.Embedding(vocabulary_size, 16, padding_idx=PAD)
        self.recurrent = nn.GRU(16, 24, batch_first=True)
        self.head = nn.Linear(24, 3)

    def forward(self, batch):
        packed = pack_padded_sequence(self.embedding(batch['tokens']), batch['lengths'].cpu(),
                                      batch_first=True, enforce_sorted=False)
        _, hidden = self.recurrent(packed)
        return self.head(hidden[-1])


class TinyTransformer(nn.Module):
    def __init__(self, vocabulary_size):
        super().__init__()
        self.embedding = nn.Embedding(vocabulary_size, 16, padding_idx=PAD)
        self.position = nn.Embedding(MAX_TOKENS, 16)
        layer = nn.TransformerEncoderLayer(d_model=16, nhead=2, dim_feedforward=32,
                                            dropout=0.0, batch_first=True, activation='gelu')
        self.encoder = nn.TransformerEncoder(layer, num_layers=1, enable_nested_tensor=False)
        self.head = nn.Linear(16, 3)
        self.use_positions = True

    def forward(self, batch):
        valid = batch['tokens'].ne(PAD)
        embedded = self.embedding(batch['tokens'])
        if self.use_positions:
            positions = torch.arange(batch['tokens'].shape[1], device=embedded.device)
            embedded = embedded+self.position(positions).unsqueeze(0)
        context = self.encoder(embedded, src_key_padding_mask=~valid)
        pooled = (context*valid.unsqueeze(-1)).sum(dim=1)/batch['lengths'].unsqueeze(1)
        return self.head(pooled)


def make_model(name, vocabulary_size):
    constructors = {'BoW linear': lambda: BagClassifier(vocabulary_size),
                    'BoW MLP': lambda: BagClassifier(vocabulary_size, nonlinear=True),
                    'Mean embedding': lambda: MeanEmbedding(vocabulary_size),
                    'CNN': lambda: TinyCNN(vocabulary_size), 'GRU': lambda: TinyGRU(vocabulary_size),
                    'Transformer': lambda: TinyTransformer(vocabulary_size)}
    return constructors[name]()


@torch.no_grad()
def predict(model, batch):
    model.eval()
    logits = model(batch)
    probabilities = logits.softmax(dim=1)
    return logits, probabilities


def train_one(name, vocabulary_size, train, validation, seed, epochs=80, learning_rate=0.01):
    """Full-batch CPU updates; choose checkpoint by validation loss, never by test."""
    torch.manual_seed(seed)
    model = make_model(name, vocabulary_size).cpu()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    loss_function = nn.CrossEntropyLoss()
    best_loss, best_epoch, best_state = float('inf'), 0, None
    history = []
    for epoch in range(1, epochs+1):
        model.train()
        optimizer.zero_grad(set_to_none=True)
        logits = model(train)
        loss = loss_function(logits, train['labels'])  # Raw logits; no preceding softmax.
        loss.backward()
        optimizer.step()
        training_logits, _ = predict(model, train)
        training_loss = float(loss_function(training_logits, train['labels']))
        validation_logits, _ = predict(model, validation)
        validation_loss = float(loss_function(validation_logits, validation['labels']))
        history.append((training_loss, validation_loss))
        if validation_loss < best_loss:
            best_loss, best_epoch = validation_loss, epoch
            best_state = deepcopy(model.state_dict())
    model.load_state_dict(best_state)
    model.eval()
    return {'name': name, 'seed': seed, 'model': model, 'history': np.asarray(history),
            'best_epoch': best_epoch, 'validation_loss': best_loss,
            'parameters': sum(parameter.numel() for parameter in model.parameters())}


def evaluate(model, batch):
    logits, probabilities = predict(model, batch)
    predicted = logits.argmax(dim=1)
    correct = predicted.eq(batch['labels'])
    groups = {}
    for index, row in enumerate(batch['rows']):
        groups.setdefault(row['pair_id'], []).append(index)
    both_correct = sum(bool(correct[indices].all()) for indices in groups.values())
    one_hot = torch.nn.functional.one_hot(batch['labels'], 3)
    return {'correct': int(correct.sum()), 'total': len(correct),
            'accuracy': float(correct.float().mean()),
            'both_correct': both_correct, 'pairs': len(groups),
            'pair_accuracy': both_correct/len(groups),
            'nll': float(nn.functional.cross_entropy(logits, batch['labels'])),
            'brier': float((probabilities-one_hot).square().sum(dim=1).mean()),
            'predicted': predicted.numpy(), 'probabilities': probabilities.numpy()}
