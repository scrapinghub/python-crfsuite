"""
CRFsuite scikit-learn API.
"""
import itertools
from sklearn.base import BaseEstimator
from ._crfsuite import PyTrainer, PyTagger, PyAttribute

class CRFSuite(BaseEstimator):

    def __init__(self, model_filename):
        self.trainer = PyTrainer()
        self.model_filename = model_filename

    def fit(self, X, y):
        for items, labels in itertools.izip(X, y):
            xseq = self._to_xseq(items)
            yseq = self._to_yseq(labels)
            self.trainer.append(xseq, yseq, 0)

        self.trainer.select('l2sgd', 'crf1d')
        self.trainer.set('c2', '0.1')

        self.trainer.train(self.model_filename, -1)

    def predict(self, X):
        tagger = PyTagger()
        tagger.open(self.model_filename)

        xseqs = [self._to_xseq(items) for items in X]
        yseqs = []

        for xseq in xseqs:
            tagger.set(xseq)
            yseqs.append(tagger.viterbi())

        return yseqs

    def _to_xseq(self, items):
        return [[PyAttribute(k, v) for k, v in item.iteritems()] for item in items]

    def _to_yseq(self, labels):
        return [label.encode('utf8') for label in labels]