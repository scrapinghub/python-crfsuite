# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pytest
from pycrfsuite import Trainer, Tagger


XSEQ = [
    {'walk': 1, 'shop': 0.5},
    {'walk': 1},
    {'walk': 1, 'clean': 0.5},
    {u'shop': 0.5, u'clean': 0.5},
    {'walk': 0.5, 'clean': 1},
    {'clean': 1, u'shop': 0.1},
    {'walk': 1, 'shop': 0.5},
    {},
    {'clean': 1},
]
YSEQ = ['sunny', 'sunny', u'sunny', 'rainy', 'rainy', 'rainy',
        'sunny', 'sunny', 'rainy']


def default_model(tmpdir):
    trainer = Trainer('lbfgs')
    trainer.append_dicts(XSEQ, YSEQ)
    model_filename = str(tmpdir.join('model.crfsuite'))
    trainer.train(model_filename)
    return model_filename


def test_open_close_labels(tmpdir):
    model_filename = default_model(tmpdir)
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


def test_open_non_existing():
    tagger = Tagger()
    with pytest.raises(IOError):
        tagger.open('foo')


def test_open_invalid():
    tagger = Tagger()
    with pytest.raises(ValueError):
        tagger.open(__file__)


def test_open_invalid_small(tmpdir):
    tmp = tmpdir.join('tmp.txt')
    tmp.write(b'foo')
    tagger = Tagger()
    with pytest.raises(ValueError):
        tagger.open(str(tmp))


def test_open_invalid_small_with_correct_signature(tmpdir):
    tmp = tmpdir.join('tmp.txt')
    tmp.write(b"lCRFfoo")
    tagger = Tagger()
    with pytest.raises(ValueError):
        tagger.open(str(tmp))


@pytest.mark.skipif(True, reason="this test segfaults, see https://github.com/chokkan/crfsuite/pull/24")
def test_open_invalid_with_correct_signature(tmpdir):
    tmp = tmpdir.join('tmp.txt')
    tmp.write(b"lCRFfoo"*100)
    tagger = Tagger()
    with pytest.raises(ValueError):
        tagger.open(str(tmp))


def test_invalid_feature_format(tmpdir):
    Tagger()
    Tagger(feature_format='stringlist')
    Tagger(feature_format='dict')

    with pytest.raises(ValueError):
        Tagger(feature_format='dicts')

    with pytest.raises(ValueError):
        Tagger(feature_format='foo')


def test_tag(tmpdir):
    model_filename = default_model(tmpdir)
    with Tagger().open(model_filename) as tagger:
        yseq = tagger.tag(XSEQ, feature_format='dict')
        assert yseq == YSEQ

    with Tagger().open(model_filename) as tagger:
        yseq = tagger.tag([x.keys() for x in XSEQ], feature_format='stringlist')
        assert yseq == YSEQ


def test_tag_invalid_feature_format(tmpdir):
    model_filename = default_model(tmpdir)
    with Tagger().open(model_filename) as tagger:
        with pytest.raises(ValueError):
            tagger.tag(XSEQ, feature_format='dicts')
