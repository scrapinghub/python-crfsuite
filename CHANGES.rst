Changes
=======

0.8.1 (2014-10-10)
------------------

* fix packaging issues with 0.8 release.

0.8 (2014-10-10)
----------------

* :class:`~ItemSequence` wrapper is added;
* tox tests are fixed.

0.7 (2014-08-11)
----------------

* More data formats for ``xseq``: ``{"prefix": {feature_dict}}`` and
  ``{"key": set(["key1",...])}`` feature dicts are now accepted by
  :class:`pycrfsuite.Trainer` and :class:`pycrfsuite.Tagger`;
* feature separator changed from "=" to ":" (it looks better in case of
  multi-level features);
* small doc and README fixes.


0.6.1 (2014-06-06)
------------------

* Switch to setuptools;
* wheels are uploaded to pypi for faster installation.

0.6 (2014-05-29)
----------------

* More data formats for ``xseq``: ``{"key": "value"}`` and
  ``{"key": bool_value}`` feature dicts are now accepted by
  :class:`pycrfsuite.Trainer` and :class:`pycrfsuite.Tagger`.

0.5 (2014-05-27)
----------------

* Exceptions in logging message handlers are now propogated and raised. This
  allows, for example, to stop training earlier by pressing Ctrl-C.

* It is now possible to customize :class:`pycrfsuite.Trainer` logging
  more easily by overriding the following methods:
  :meth:`pycrfsuite.Trainer.on_start`,
  :meth:`pycrfsuite.Trainer.on_featgen_progress`,
  :meth:`pycrfsuite.Trainer.on_featgen_end`,
  :meth:`pycrfsuite.Trainer.on_prepared`,
  :meth:`pycrfsuite.Trainer.on_prepare_error`,
  :meth:`pycrfsuite.Trainer.on_iteration`,
  :meth:`pycrfsuite.Trainer.on_optimization_end`
  :meth:`pycrfsuite.Trainer.on_end`. The feature is implemented by parsing
  CRFsuite log. There is :class:`pycrfsuite.BaseTrainer` that is not
  doing this.

0.4.1 (2014-05-18)
------------------

* :meth:`pycrfsuite.Tagger.info()` is fixed.

0.4 (2014-05-16)
----------------

* (backwards-incompatible) training parameters are now passed
  using ``params`` argument of  :class:`pycrfsuite.Trainer` constructor
  instead of ``**kwargs``;
* (backwards-incompatible) logging support is dropped;
* `verbose` argument for :class:`pycrfsuite.Trainer` constructor;
* :meth:`pycrfsuite.Trainer.get_params` and
  :meth:`pycrfsuite.Trainer.set_params` for getting/setting multiple training
  parameters at once;
* string handling in Python 3.x is fixed by rebuilding the wrapper with
  Cython 0.21dev;
* algorithm names are normalized to support names used
  by crfsuite console utility and documented in crfsuite manual;
* type conversion for training parameters is fixed: ``feature.minfreq``
  now works, and boolean arguments become boolean.

0.3 (2014-05-14)
----------------

python-crfsuite now detects the featue format (dict vs list of strings)
automatically - it turns out the performance overhead is negligible.

* ``Trainer.append_stringslists`` and ``Trainer.append_dicts`` methods
  are replaced with a single :meth:`pycrfsuite.Trainer.append` method;
* ``Tagger.set_stringlists`` and ``Tagger.set_dicts`` methods are
  removed in favor of :meth:`pycrfsuite.Tagger.set` method;
* ``feature_format`` arguments in :class:`pycrfsuite.Tagger` methods
  and constructor are dropped.

0.2 (2014-05-14)
----------------

* :meth:`pycrfsuite.Tagger.dump()` and :meth:`pycrfsuite.Tagger.info()`
  methods for model debugging;
* a memory leak in Trainer is fixed (trainer instances were never
  garbage collected);
* documentation and testing improvements.

0.1 (2014-04-30)
----------------

Many changes; python-crfsuite is almost rewritten.

0.0.1 (2014-04-24)
------------------

Initial release.
