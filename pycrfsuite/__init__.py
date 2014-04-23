"""
CRFsuite scikit-learn API.
"""
import itertools
from sklearn.base import BaseEstimator
from .pycrfsuite import PyTrainer, PyTagger, PyAttribute

class CRFSuite(BaseEstimator):
    """Class for training and applying CRFsuite models.

    Parameters
    ----------
    algorithm : string,
        'lbfgs' for Gradient descent using the L-BFGS method,
        'l2sgd' for Stochastic Gradient Descent with L2 regularization term
        'ap' for Averaged Perceptron
        'pa' for Passive Aggressive
        'arow' for Adaptive Regularization Of Weight Vector

    c1: float
        the coefficient for L1 regularization.

    c2: float
        The coefficient for L2 regularization.
    """

    def __init__(self, model_filename, algorithm='l2sgd', c1=0.0, c2=1.0):
        self.model_filename = model_filename
        self.algorithm = algorithm
        self.c1 = c1
        self.c2 = c2

    def fit(self, X, y):

        trainer = PyTrainer()
        trainer.select(self.algorithm, 'crf1d')

        for items, labels in itertools.izip(X, y):
            xseq = self._to_xseq(items)
            yseq = self._to_yseq(labels)
            trainer.append(xseq, yseq, 0)

        if self.algorithm == 'lbfgs':
            trainer.set('c1', str(self.c1))

        trainer.set('c2', str(self.c2))
        trainer.train(self.model_filename, -1)

    def predict(self, X):
        tagger = PyTagger()
        tagger.open(self.model_filename)

        xseqs = [self._to_xseq(x) for x in X]
        yseqs = []

        for xseq in xseqs:
            tagger.set(xseq)
            yseqs.append(tagger.viterbi())

        return yseqs

    def _to_attribute(self, feature):

        if isinstance(feature, tuple):
            return PyAttribute(feature[0], feature[1])

        if isinstance(feature, basestring):
            return PyAttribute(feature, 1)

        if isinstance(feature, dict):
            feature = "%s:%s" %(feature.keys()[0].encode('utf8'), \
                unicode(feature.values()[0]).encode('utf8'))
            return PyAttribute(feature, 1)

        raise ValueError('unexpected feature type: %s' %feature)

    def _to_xseq(self, x):
        xseq = []
        for feats in x:
            # XXX: drop big combined dict features?
            if isinstance(feats, dict):
                feats = [{k:v} for k, v in feats.iteritems()]
            xseq.append([self._to_attribute(feat) for feat in feats])
        return xseq

    def _to_yseq(self, labels):
        return [label.encode('utf8') for label in labels]