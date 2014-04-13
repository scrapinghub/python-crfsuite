cimport crfsuite_api

from libcpp.vector cimport vector
from collections import namedtuple

PyAttribute = namedtuple('PyAttribute', ['name', 'value'])

cdef vector[crfsuite_api.Item] _alloc_citem_seq(xseq):
    cdef vector[crfsuite_api.Item] cxseq = vector[crfsuite_api.Item]()
    cdef vector[crfsuite_api.Attribute] citem

    for item in xseq:
        citem = vector[crfsuite_api.Attribute]()
        for attr in item:
            citem.push_back(crfsuite_api.Attribute(attr.name, attr.value))
        cxseq.push_back(citem)
    return cxseq

cdef _free_citem_seq(vector[crfsuite_api.Item] cxseq):
    # XXX: no remove?
    for citem in cxseq:
        citem.swap(vector[crfsuite_api.Attribute]())
    cxseq.swap(vector[crfsuite_api.Item]())

cdef class PyTrainer:
    cdef crfsuite_api.Trainer* p_this

    def __cinit__(self):
        self.p_this = new crfsuite_api.Trainer()

    def __dealloc__(self):
        del self.p_this

    def clear(self):
        self.p_this.clear()

    def append(self, xseq, yseq, group):
        cxseq = _alloc_citem_seq(xseq)
        self._append(cxseq, yseq, group)
        _free_citem_seq(cxseq)

    cdef _append(self, crfsuite_api.ItemSequence xseq, crfsuite_api.StringList yseq, int group):
        self.p_this.append(xseq, yseq, group)

    def select(self, algorithm, type):
        return self.p_this.select(algorithm, type)

    def train(self, model, holdout):
        return self.p_this.train(model, holdout)

    def params(self):
        return self.p_this.params()

    def set(self, name, value):
        self.p_this.set(name, value)

    def get(self, name):
        return self.p_this.get(name)

    def help(self, name):
        return self.p_this.help(name)

cdef class PyTagger:
    cdef crfsuite_api.Tagger* p_this

    def __cinit__(self):
        self.p_this = new crfsuite_api.Tagger()

    def __dealloc__(self):
        del self.p_this

    def open(self, name):
        return self.p_this.open(name)

    def close(self):
        self.p_this.close()

    def labels(self):
        return self.p_this.labels()

    def tag(self, xseq):
        cxseq = _alloc_citem_seq(xseq)
        labels = self._tag(cxseq)
        _free_citem_seq(cxseq)
        return labels

    cdef _tag(self, crfsuite_api.ItemSequence xseq):
        return self.p_this.tag(xseq)

    def set(self, xseq):
        cxseq = _alloc_citem_seq(xseq)
        self._set(cxseq)
        _free_citem_seq(cxseq)

    cdef _set(self, crfsuite_api.ItemSequence xseq):
        self.p_this.set(xseq)

    def viterbi(self):
        return self.p_this.viterbi()

    def probability(self, yseq):
        return self.p_this.probability(yseq)

    def marginal(self, y, pos):
        return self.p_this.marginal(y, pos)
