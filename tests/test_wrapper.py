# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import warnings
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
    trainer = Trainer('lbfgs')
    trainer.append_dicts(XSEQ, YSEQ)

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


def test_training_messages_exception():
    class BadTrainer(Trainer):
        def on_message(self, message):
            raise Exception("error")

    trainer = BadTrainer()
    trainer.select('lbfgs')
    trainer.append_dicts(XSEQ, YSEQ)

    with warnings.catch_warnings(record=True) as w:
        trainer.train('model.crfsuite')
    assert len(w) > 0


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
    assert 'L1' in trainer.help('c1')

    trainer.select('l2sgd')
    assert 'c2' in trainer.params()
    assert 'c1' not in trainer.params()
    assert 'L2' in trainer.help('c2')


def test_help_invalid_parameter():
    trainer = Trainer()
    trainer.select('l2sgd')

    # This segfaults without a workaround;
    # see https://github.com/chokkan/crfsuite/pull/21
    with pytest.raises(ValueError):
        trainer.help('foo')

    with pytest.raises(ValueError):
        trainer.help('c1')


def test_get_parameter():
    trainer = Trainer()
    trainer.select('l2sgd')
    assert abs(trainer.get('c2') - 0.1) > 1e-6
    trainer.set('c2', 0.1)
    assert abs(trainer.get('c2') - 0.1) < 1e-6


def test_set_parameters_in_constructor():
    trainer = Trainer(c2=100)
    assert abs(trainer.get('c2') - 100) < 1e-6


def test_version():
    from pycrfsuite.pycrfsuite import __version__
    assert bool(__version__), __version__
