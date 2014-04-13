"""
demostrates how to use pycrfsuite for conll tasks.

python example.py train modelname

"""
from datasets.conll import load_conll, features
from pycrfsuite import CRFSuite
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report

import sys
from itertools import chain

def avg_bio_f1_score(y_true, y_pred):
    """
    Macro-averaged F1 score of lists of BIO-encoded sequences
    ``y_true`` and ``y_pred``.

    A named entity in a sequence from ``y_pred`` is considered
    correct only if it is an exact match of the corresponding entity
    in the ``y_true``.

    It requires https://github.com/larsmans/seqlearn to work.
    """
    from seqlearn.evaluation import bio_f_score
    return sum(map(bio_f_score, y_true, y_pred)) / len(y_true)


def bio_classification_report(y_true, y_pred):
    """
    Classification report for a list of BIO-encoded sequences.
    It computes token-level metrics and discards "O" labels.
    """
    y_true_combined = list(chain.from_iterable(y_true))
    y_pred_combined = list(chain.from_iterable(y_pred))
    tagset = (set(y_true_combined) | set(y_pred_combined)) - {'O'}
    return classification_report(
        y_true_combined,
        y_pred_combined,
        labels = sorted(tagset, key=lambda tag: tag.split('-', 1)[::-1])
    )

if __name__ == '__main__':

    print __doc__

    if len(sys.argv) < 3:
        print "Usage: {0} training_file modelname".format(sys.argv[0])
        sys.exit(1)

    clf = CRFSuite(sys.argv[2])

    X = []
    y = []

    for xseq, yseq in load_conll(sys.argv[1], features):
        X.append(xseq)
        y.append(yseq)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print bio_classification_report(y_test, y_pred)