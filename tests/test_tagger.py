# -*- coding: utf-8 -*-
from __future__ import absolute_import
import pytest
from pycrfsuite import Tagger, Trainer


def test_open_close_labels(model_filename, yseq):
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


def test_invalid_feature_format():
    Tagger()
    Tagger(feature_format='stringlist')
    Tagger(feature_format='dict')

    with pytest.raises(ValueError):
        Tagger(feature_format='dicts')

    with pytest.raises(ValueError):
        Tagger(feature_format='foo')


def test_tag(model_filename, xseq, yseq):
    with Tagger().open(model_filename) as tagger:
        assert tagger.tag(xseq, feature_format='dict') == yseq

    with Tagger().open(model_filename) as tagger:
        # if we discard weights the results become different
        data = [x.keys() for x in xseq]
        assert tagger.tag(data, feature_format='stringlist') != yseq


def test_tag_formats(tmpdir, xseq, yseq):
    # make all coefficients 1 and check that results are the same
    model_filename = str(tmpdir.join('model.crfsuite'))
    xseq = [dict((key, 1) for key in x) for x in xseq]

    trainer = Trainer()
    trainer.set('c2', 1e-6)  # make sure model overfits
    trainer.append_dicts(xseq, yseq)
    trainer.train(model_filename)

    with Tagger().open(model_filename) as tagger:
        assert tagger.tag(xseq, feature_format='dict') == yseq

    with Tagger().open(model_filename) as tagger:
        data = [x.keys() for x in xseq]
        assert tagger.tag(data, feature_format='stringlist') == yseq


def test_tag_invalid_feature_format(model_filename, xseq):
    with Tagger().open(model_filename) as tagger:
        with pytest.raises(ValueError):
            tagger.tag(xseq, feature_format='dicts')


def test_tag_probability(model_filename, xseq, yseq):
    with Tagger().open(model_filename) as tagger:
        res = tagger.tag(xseq, feature_format='dict')
        prob = tagger.probability(res)
        prob2 = tagger.probability([yseq[0]]*len(yseq))
        assert prob > prob2
        assert 0 < prob < 1
        assert 0 < prob2 < 1


def test_dump(tmpdir, model_filename):
    with Tagger().open(model_filename) as tagger:
        dump_filename = str(tmpdir.join("dump.txt"))
        tagger.dump(dump_filename)

        with open(dump_filename, 'rb') as f:
            res = f.read().decode('utf8')
            assert 'LABELS = {' in res
            assert u'проверка --> rainy:' in res

    # it shouldn't segfault on a closed tagger
    with pytest.raises(RuntimeError):
        tagger.dump(dump_filename)


def test_info(model_filename):
    with Tagger().open(model_filename) as tagger:
        res = tagger.info()

        assert res.transitions[('sunny', 'sunny')] > res.transitions[('sunny', 'rainy')]
        assert res.state_features[('walk', 'sunny')] > res.state_features[('walk', 'rainy')]
        assert (u'проверка', u'rainy') in res.state_features
        assert res.header['num_labels'] == '2'
        assert set(res.labels.keys()) == set(['sunny', 'rainy'])
        assert set(res.attributes.keys()) == set(['shop', 'walk', 'clean', u'проверка'])

    # it shouldn't segfault on a closed tagger
    with pytest.raises(RuntimeError):
        tagger.info()
