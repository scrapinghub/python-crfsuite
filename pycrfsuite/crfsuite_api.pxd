from libcpp.string cimport string
from libcpp.vector cimport vector

cdef extern from "../crfsuite/include/crfsuite_api.hpp" namespace "CRFSuite":
    cdef cppclass Attribute:
        string attr
        double value

        Attribute()
        Attribute(string)
        Attribute(string, double)

    ctypedef vector[Attribute] Item
    ctypedef vector[Item] ItemSequence
    ctypedef vector[string] StringList

    cdef cppclass Trainer:
        Trainer() except +
        void clear()
        void append(ItemSequence, vector[string], int)
        int select(string, string)
        int train(string, int)
        vector[string] params()
        void set(string, string)
        string get(string)
        string help(string)
        # message(String) ?

    cdef cppclass Tagger:
        Tagger() except +
        int open(string)
        void close()
        vector[string] labels()
        vector[string] tag(ItemSequence)
        void set(ItemSequence)
        vector[string] viterbi()
        double probability(vector[string])
        double marginal(string, int)
