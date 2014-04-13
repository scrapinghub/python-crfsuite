from datasets.conll import load_conll
from nose.tools import assert_equal
from cStringIO import StringIO

TEST_FILE = """

The     Det
cat     N

really  Adv
.       Punc

"""

def features(words, i):
    word = words[i]
    yield 'lower:{}'.format(word.lower())
    if word[0].isupper():
        yield "CAP"

def test_conll():
    xseqs = []
    yseqs = []

    for xseq, yseq in load_conll(StringIO(TEST_FILE), features):
        xseqs.append(xseq)
        yseqs.append(yseq)

    assert_equal(xseqs[0], [{'lower:the': 1, 'CAP': 1}, {'lower:cat': 1}])
    assert_equal(xseqs[1], [{'lower:really': 1}, {'lower:.': 1}])
    assert_equal(yseqs, [['Det', 'N'], ['Adv', 'Punc']])
