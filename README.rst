==========
PyCRFsuite
==========

PyCRFsuite is a python binding of CRFsuite_ and mimic scikit-learn_ to provide a similar API.

Why
===
Why make another python binding for CRFsuite_ even crfsuite has its own SWIG python package_? Some of the reasons are:

* crfsuite SWIG package is not easy to build . There are some openning issues reported on crfsuite e.g. issue6_, issue19_
* can't dump the model (with `crfsuite dump`) trained by the crfsuite's SWIG python package_.
* wrapping a library with cython is fun and easy to extend.

Installation
============

Prepare `crfsuite` and `liblbfgs`::

    git submodule init && git submodule update

and then::

    python setup.py install

if you modify the `pycrfsuite.pyx`, make sure run::

    update_cpp.sh

Usage
=====

The easiest way to start is to fetch a dataset in CoNLL 2000 format, define a feature extraction function, e.g.::

    def features(words, i):
        word = words[i]

        yield "word:{}".format(word.lower())

        if word[0].isupper():
            yield "CAP"

        if i > 0:
            yield "word-1:{}".format(words[i - 1].lower())
        if i + 1 < len(words):
            yield "word+1:{}".format(words[i + 1].lower())

Load the training file, say train.txt::

    X = []
    y = []

    for xseq, yseq in load_conll('train.txt', features):
        X.append(xseq)
        y.append(yseq)

Train a model::

    from pycrfsuite import CRFsuite

    clf = CRFSuite('model_name')
    clf.fit(X, y)

Authors
======
Terry Peng <pengtaoo@gmail.com>

License
=======
Licensed under MIT license.

.. _CRFsuite: https://github.com/chokkan/crfsuite
.. _package: https://github.com/chokkan/crfsuite/swig/python
.. _scikit-learn: http://scikit-learn.org/
.. _issue6: https://github.com/chokkan/crfsuite/issues/6
.. _issue19: https://github.com/chokkan/crfsuite/issues/19