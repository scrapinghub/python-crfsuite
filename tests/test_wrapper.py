# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import pytest

from pycrfsuite.pycrfsuite import Trainer


XSEQ = [
    {'walk': 1, 'shop': 0.5},
    {'walk': 1},
    {'walk': 1, 'clean': 0.5},
    {'shop': 0.5, 'clean': 0.5},
    {'walk': 0.5, 'clean': 1},
    {'clean': 1, 'shop': 0.1},
    {'walk': 1, 'shop': 0.5},
    {},
    {'clean': 1},
]
YSEQ = ['sunny', 'sunny', 'sunny', 'rainy', 'rainy', 'rainy', 'sunny', 'sunny', 'rainy']


def test_trainer():
    trainer = Trainer()
    trainer.append_dicts(XSEQ, YSEQ)
    trainer.select('lbfgs')

    assert not os.path.isfile('model.crfsuite')
    trainer.train('model.crfsuite')
    assert os.path.isfile('model.crfsuite')


def test_trainer_noselect():
    # This shouldn't segfault; see https://github.com/chokkan/crfsuite/pull/21
    trainer = Trainer()
    trainer.append_dicts(XSEQ, YSEQ)
    trainer.train('model.crfsuite')


def test_trainer_noappend():
    # This shouldn't segfault; see https://github.com/chokkan/crfsuite/pull/21
    trainer = Trainer()
    trainer.select('lbfgs')
    trainer.train('model.crfsuite')


def test_trainer_noselect_noappend():
    # This shouldn't segfault; see https://github.com/chokkan/crfsuite/pull/21
    trainer = Trainer()
    trainer.train('model.crfsuite')


def test_training_messages():

    class CapturingTrainer(Trainer):
        def __init__(self):
            self.messages = []

        def on_message(self, message):
            self.messages.append(message)

    trainer = CapturingTrainer()
    trainer.select('lbfgs')
    trainer.append_dicts(XSEQ, YSEQ)
    assert not trainer.messages
    trainer.train('model.crfsuite')
    assert trainer.messages
    assert 'type: CRF1d\n' in trainer.messages
    # print("".join(trainer.messages))


def test_trainer_select_raises_error():
    trainer = Trainer()
    with pytest.raises(ValueError):
        trainer.select('foo')


def test_params_and_help():
    trainer = Trainer()

    trainer.select('lbfgs')
    assert 'c1' in trainer.params()
    assert 'c2' in trainer.params()
    assert 'num_memories' in trainer.params()

    trainer.select('l2sgd')
    assert 'c2' in trainer.params()
    assert 'c1' not in trainer.params()

    assert 'L2' in trainer.help('c2')

    # This segfaults; see https://github.com/chokkan/crfsuite/pull/21
    # with pytest.raises(ValueError):
    #     trainer.help('c1')


def test_version():
    from pycrfsuite.pycrfsuite import __version__
    assert bool(__version__), __version__
