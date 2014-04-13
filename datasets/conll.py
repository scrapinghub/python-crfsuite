"""
Load ConLL dataset and generate features
"""
from itertools import imap, groupby
from contextlib import closing

def _open(f):
    return closing(open(f) if isinstance(f, basestring) else f)

def load_conll(fname, features):
    """Load ConLL file and extract features"""

    with _open(fname) as f:
        lines = imap(str.strip, f)
        groups = (grp for nonempty, grp in groupby(lines, bool) if nonempty)

        xseq = []
        yseq = []

        for group in groups:
            group = list(group)
            obs, lbl = zip(*(ln.rsplit(None, 1) for ln in group))

            for i in xrange(len(obs)):
                xseq.append(dict.fromkeys(features(obs, i), 1))
                yseq.append(lbl[i])

            if xseq and yseq:
                yield xseq, yseq
                xseq = []
                yseq = []

def features(words, i):
    word = words[i]

    yield "word:{}".format(word.lower())

    if word[0].isupper():
        yield "CAP"

    if i > 0:
        yield "word-1:{}".format(words[i - 1].lower())
    if i + 1 < len(words):
        yield "word+1:{}".format(words[i + 1].lower())
