Changes
=======

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
