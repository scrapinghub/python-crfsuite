# cython: embedsignature=True
cimport crfsuite_api

from libcpp.vector cimport vector
from libcpp.string cimport string


class CRFSuiteTrainError(Exception):

    _messages = {
        crfsuite_api.CRFSUITEERR_UNKNOWN: "Unknown error occurred",
        crfsuite_api.CRFSUITEERR_OUTOFMEMORY: "Insufficient memory",
        crfsuite_api.CRFSUITEERR_NOTSUPPORTED: "Unsupported operation",
        crfsuite_api.CRFSUITEERR_INCOMPATIBLE: "Incompatible data",
        crfsuite_api.CRFSUITEERR_INTERNAL_LOGIC: "Internal error",
        crfsuite_api.CRFSUITEERR_OVERFLOW: "Overflow",
        crfsuite_api.CRFSUITEERR_NOTIMPLEMENTED: "Not implemented",
    }

    def __init__(self, code):
        self.code = code
        Exception.__init__(self._messages.get(self.code, "Unexpected error"))


cdef crfsuite_api.ItemSequence dicts_to_seq(seq) except+:
    """
    Convert an iterable of dicts {unicode_key: float_value}
    to an ItemSequence.
    """
    cdef dict x
    cdef crfsuite_api.ItemSequence c_seq
    cdef crfsuite_api.Item c_item
    cdef string c_key
    cdef double c_value

    for x in seq:
        c_item = crfsuite_api.Item()
        c_item.reserve(len(x))
        for key in x:
            if isinstance(key, unicode):
                c_key = (<unicode>key).encode('utf8')
            else:
                c_key = key
            c_value = x[key]
            c_item.push_back(crfsuite_api.Attribute(c_key, c_value))
        c_seq.push_back(c_item)

    return c_seq


cdef crfsuite_api.ItemSequence stringlists_to_seq(seq) except+:
    """
    Convert an iterable of lists ``[key1, key2, ...]``
    to an ItemSequence.
    """
    cdef crfsuite_api.ItemSequence c_seq
    cdef crfsuite_api.Item c_item
    cdef string c_key

    for x in seq:
        c_item = crfsuite_api.Item()
        c_item.reserve(len(x))
        for key in x:
            if isinstance(key, unicode):
                c_key = (<unicode>key).encode('utf8')
            else:
                c_key = key
            c_item.push_back(crfsuite_api.Attribute(c_key))
        c_seq.push_back(c_item)

    return c_seq


cdef class Trainer:
    cdef crfsuite_api.Trainer c_trainer

    def append_dicts(self, xseq, yseq, group=0):
        """
        Append an instance to the data set.
        ``xseq`` should be a sequence of {'key': weight} dicts.
        """
        self.c_trainer.append(dicts_to_seq(xseq), yseq, group)

    def append_stringlists(self, xseq, yseq, group=0):
        """
        Append an instance to the data set.
        ``xseq`` should be a sequence of ``[key1, key2, ...]`` lists.
        """
        self.c_trainer.append(stringlists_to_seq(xseq), yseq, group)

    def select(self, algorithm, type='crf1d'):
        """
        Initialize the training algorithm.

        Parameters
        ----------
        algorithm : {'lbfgs', 'l2sgd', 'ap', 'pa', 'arow'}
            The name of the training algorithm.

            * 'lbfgs' for Gradient descent using the L-BFGS method,
            * 'l2sgd' for Stochastic Gradient Descent with L2 regularization term
            * 'ap' for Averaged Perceptron
            * 'pa' for Passive Aggressive
            * 'arow' for Adaptive Regularization Of Weight Vector

        type : string, optional
            The name of the graphical model.
        """
        if not self.c_trainer.select(algorithm, type):
            raise ValueError(
                "Bad arguments: algorithm=%r, type=%r" % (algorithm, type)
            )

    def train(self, model, holdout=-1):
        """
        Run the training algorithm.
        This function starts the training algorithm with the data set given
        by append_... methods.

        Parameters
        ----------
        model : string
            The filename to which the trained model is stored.
            If this value is empty, this function does not
            write out a model file.

        holdout : int, optional
            The group number of holdout evaluation. The
            instances with this group number will not be used
            for training, but for holdout evaluation.
            Default value is -1, meaning "use all instances for training".
        """
        status_code = self.c_trainer.train(model, holdout)
        if status_code != crfsuite_api.CRFSUITE_SUCCESS:
            raise CRFSuiteTrainError(status_code)

    def params(self):
        """
        Obtain the list of parameters.

        This function returns the list of parameter names available for the
        graphical model and training algorithm specified by select() function.

        Returns
        -------
        list of strings
            The list of parameters available for the current
            graphical model and training algorithm.

        """
        return self.c_trainer.params()

    def set(self, name, value):
        """
        Set a training parameter.
        This function sets a parameter value for the graphical model and
        training algorithm specified by select() function.

        Parameters
        ----------
        name : string
            The parameter name.
        value : string
            The value of the parameter.

        """
        self.c_trainer.set(name, value)

    def get(self, name):
        """
        Get the value of a training parameter.
        This function gets a parameter value for the graphical model and
        training algorithm specified by select() function.

        Parameters
        ----------
        name : string
            The parameter name.

        """
        return self.c_trainer.get(name)

    def help(self, name):
        """
        Get the description of a training parameter.
        This function obtains the help message for the parameter specified
        by the name. The graphical model and training algorithm must be
        selected by select() function before calling this function.

        Parameters
        ----------
        name : string
            The parameter name.

        Returns
        -------
        string
            The description (help message) of the parameter.

        """
        return self.c_trainer.help(name)

    def clear(self):
        """ Remove all instances in the data set. """
        self.c_trainer.clear()




# cdef class PyTagger:
#     cdef crfsuite_api.Tagger* p_this
#
#     def __cinit__(self):
#         self.p_this = new crfsuite_api.Tagger()
#
#     def __dealloc__(self):
#         del self.p_this
#
#     def open(self, name):
#         return self.p_this.open(name)
#
#     def close(self):
#         self.p_this.close()
#
#     def labels(self):
#         return self.p_this.labels()
#
#     def tag(self, xseq):
#         cxseq = _alloc_citem_seq(xseq)
#         labels = self._tag(cxseq)
#         _free_citem_seq(cxseq)
#         return labels
#
#     cdef _tag(self, crfsuite_api.ItemSequence xseq):
#         return self.p_this.tag(xseq)
#
#     def set(self, xseq):
#         cxseq = _alloc_citem_seq(xseq)
#         self._set(cxseq)
#         _free_citem_seq(cxseq)
#
#     cdef _set(self, crfsuite_api.ItemSequence xseq):
#         self.p_this.set(xseq)
#
#     def viterbi(self):
#         return self.p_this.viterbi()
#
#     def probability(self, yseq):
#         return self.p_this.probability(yseq)
#
#     def marginal(self, y, pos):
#         return self.p_this.marginal(y, pos)
