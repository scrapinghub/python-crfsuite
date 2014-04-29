# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pytest
from pycrfsuite import Tagger


def test_open_close_labels(tmpdir, model_filename, yseq):
    tagger = Tagger()

    with pytest.raises(ValueError):
        # tagger should be closed, so labels() method should fail here
        labels = tagger.labels()

    with tagger.open(model_filename):
        labels = tagger.labels()
    assert set(labels) == set(yseq)

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


def test_tag(tmpdir, model_filename, xseq, yseq):
    with Tagger().open(model_filename) as tagger:
        yseq = tagger.tag(xseq, feature_format='dict')
        assert yseq == yseq

    with Tagger().open(model_filename) as tagger:
        yseq = tagger.tag([x.keys() for x in xseq], feature_format='stringlist')
        assert yseq == yseq


def test_tag_invalid_feature_format(tmpdir, model_filename, xseq):
    with Tagger().open(model_filename) as tagger:
        with pytest.raises(ValueError):
            tagger.tag(xseq, feature_format='dicts')
