===============
python-crfsuite
===============

.. image:: https://travis-ci.org/tpeng/python-crfsuite.svg?branch=master
    :target: https://travis-ci.org/tpeng/python-crfsuite

python-crfsuite is a python binding to CRFsuite_.

Installation
============

::

    pip install python-crfsuite

Usage
=====

See docs_ and an example_.

.. _docs: http://python-crfsuite.rtfd.org/
.. _example: http://nbviewer.ipython.org/github/tpeng/python-crfsuite/blob/master/examples/CoNLL%202002.ipynb

Contributing
============

* Source code: https://github.com/tpeng/python-crfsuite
* Issue tracker: https://github.com/tpeng/python-crfsuite/issues

Feel free to submit ideas, bugs reports, pull requests or regular patches.

In order to run tests, install Cython_ (> 0.20.1)  and tox_, then type

::

    ./update_cpp.sh; tox

from the source checkout.

Please don't commit generated cpp files in the same commit as other files.

.. _Cython: http://cython.org/
.. _tox: http://tox.testrun.org

Authors
=======

* Terry Peng <pengtaoo@gmail.com>
* Mikhail Korobov <kmike84@gmail.com>

Bundled CRFSuite_ C/C++ library is by Naoaki Okazaki & contributors.

License
=======

python-crfsuite is licensed under MIT license.
CRFsuite_ library is licensed under BSD license.

.. _CRFsuite: https://github.com/chokkan/crfsuite

Alternatives
============

* https://github.com/jakevdp/pyCRFsuite - uses C API instead of C++ API;
  allows to use scipy sparse matrices as an input.
* https://github.com/chokkan/crfsuite/tree/master/swig/python - official
  Python wrapper, exposes C++ API using SWIG.

This package (python-crfsuite) wraps CRFsuite C++ API using Cython.
It is faster than official SWIG wrapper and has a simpler codebase than
a more advanced pyCRFsuite. python-crfsuite works in Python 2 and Python 3,
doesn't have external dependencies (CRFsuite is bundled, numpy/scipy stack
is not needed) and workarounds some of the issues with C++ CRFsuite library.
