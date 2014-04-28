# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import warnings
import contextlib
import tempfile
import shutil
import pytest

from pycrfsuite import Trainer, Tagger


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


def test_trainer(tmpdir):
    trainer = Trainer('lbfgs')
    trainer.append_dicts(XSEQ, YSEQ)

    model_filename = str(tmpdir.join('model.crfsuite'))
    assert not os.path.isfile(model_filename)
    trainer.train(model_filename)
    assert os.path.isfile(model_filename)


def test_trainer_noselect(tmpdir):
    # This shouldn't segfault; see https://github.com/chokkan/crfsuite/pull/21
    trainer = Trainer()
    trainer.append_dicts(XSEQ, YSEQ)
    model_filename = str(tmpdir.join('model.crfsuite'))
    trainer.train(model_filename)


def test_trainer_noappend(tmpdir):
    # This shouldn't segfault; see https://github.com/chokkan/crfsuite/pull/21
    trainer = Trainer()
    trainer.select('lbfgs')
    model_filename = str(tmpdir.join('model.crfsuite'))
    trainer.train(model_filename)


def test_trainer_noselect_noappend(tmpdir):
    # This shouldn't segfault; see https://github.com/chokkan/crfsuite/pull/21
    trainer = Trainer()
    model_filename = str(tmpdir.join('model.crfsuite'))
    trainer.train(model_filename)


def test_training_messages(tmpdir):

    class CapturingTrainer(Trainer):
        def __init__(self):
            self.messages = []

        def message(self, message):
            self.messages.append(message)

    trainer = CapturingTrainer()
    trainer.select('lbfgs')
    trainer.append_dicts(XSEQ, YSEQ)
    assert not trainer.messages

    model_filename = str(tmpdir.join('model.crfsuite'))
    trainer.train(model_filename)
    assert trainer.messages
    assert 'type: CRF1d\n' in trainer.messages
    # print("".join(trainer.messages))


def test_training_messages_exception(tmpdir):
    class BadTrainer(Trainer):
        def message(self, message):
            raise Exception("error")

    trainer = BadTrainer()
    trainer.select('lbfgs')
    trainer.append_dicts(XSEQ, YSEQ)

    with warnings.catch_warnings(record=True) as w:
        model_filename = str(tmpdir.join('model.crfsuite'))
        trainer.train(model_filename)
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
    from pycrfsuite import CRFSUITE_VERSION
    assert bool(CRFSUITE_VERSION), CRFSUITE_VERSION


def test_tagger_open_close_labels(tmpdir):
    trainer = Trainer('lbfgs')
    trainer.append_dicts(XSEQ, YSEQ)
    model_filename = str(tmpdir.join('model.crfsuite'))

    trainer.train(model_filename)

    tagger = Tagger()

    with pytest.raises(ValueError):
        # tagger should be closed, so labels() method should fail here
        labels = tagger.labels()

    with tagger.open(model_filename):
        labels = tagger.labels()
    assert set(labels) == set(YSEQ)

    with pytest.raises(ValueError):
        # tagger should be closed, so labels() method should fail here
        labels = tagger.labels()


def test_tagger_open_non_existing():
    tagger = Tagger()
    with pytest.raises(IOError):
        tagger.open('foo')


def test_tagger_open_invalid():
    tagger = Tagger()
    with pytest.raises(ValueError):
        tagger.open(__file__)


def test_tagger_open_invalid_small(tmpdir):
    tmp = tmpdir.join('tmp.txt')
    tmp.write(b'foo')
    tagger = Tagger()
    with pytest.raises(ValueError):
        tagger.open(str(tmp))


def test_tagger_open_invalid_small_with_correct_signature(tmpdir):
    tmp = tmpdir.join('tmp.txt')
    tmp.write(b"lCRFfoo")
    tagger = Tagger()
    with pytest.raises(ValueError):
        tagger.open(str(tmp))


@pytest.mark.skipif(True, reason="this test segfaults, see https://github.com/chokkan/crfsuite/pull/24")
def test_tagger_open_invalid_with_correct_signature(tmpdir):
    tmp = tmpdir.join('tmp.txt')
    tmp.write(b"lCRFfoo"*100)
    tagger = Tagger()
    with pytest.raises(ValueError):
        tagger.open(str(tmp))
