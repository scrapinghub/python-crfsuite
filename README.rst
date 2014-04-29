===============
python-crfsuite
===============

.. image:: https://travis-ci.org/tpeng/python-crfsuite.svg?branch=master
    :target: https://travis-ci.org/tpeng/python-crfsuite

PyCRFsuite is a python binding to CRFsuite_.

Installation
============

::

    pip install python-crfuite

Usage
=====

See docs_ and examples_.

.. _docs: http://python-crfsuite.rtfd.org/
.. _examples: http://nbviewer.ipython.org/github/tpeng/python-crfsuite/tree/master/examples/

Contributing
============

* Source code: https://github.com/tpeng/python-crfsuite
* Issue tracker: https://github.com/tpeng/python-crfsuite/issues

Feel free to submit ideas, bugs reports, pull requests or regular patches.

In order to run tests, install Cython_  and tox_, then type

::

    ./update_cython.sh
    tox

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

CRFsuite_ C/C++ library is licensed under BSD license.

.. _CRFsuite: https://github.com/chokkan/crfsuite

Alternatives
============

* https://github.com/jakevdp/pyCRFsuite - uses C API instead of C++ API;
* https://github.com/chokkan/crfsuite/tree/master/swig/python - official
  Python wrapper, exposes C++ API using SWIG.


