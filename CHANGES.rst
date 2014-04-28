.. :changelog:

Change Log
----------

0.2.2 (2014-04-28)
++++++++++++++++++

* Fixes a capitalization bug related to #5.

0.2.1 (2014-04-28)
++++++++++++++++++

* Reformats ``README.rst``.
* Renames change log file to ``*.rst``.
* Adds authors and contributing files.
* Sets up Travis CI.
* Adds version to ``__init__.py``.
* Fixes #5. Make ``accented_to_numbered()`` add apostrophes when needed.
* Fixes #4. Fixes ``numbered_to_accented()`` handling of ``'v'`` vowel.
* Fixes #3. Changes ``IndexError`` exception handlers to ``KeyError``.
* Fixes #2. Fixes ``accented_to_numbered()`` with uppercase accented vowel.

0.2.0 (2014-04-14)
++++++++++++++++++

* Fixes typo in is_pinyin.
* Adds is_pinyin_compatible() and is_zhuyin_compatible() functions.
* Removes code for identifying Hanzi and incorporates Hanzi Identifier library.
* Removes Sphinx viewcode extension.
* Adds Python 3.4 environment to tox configuration.
* Fixes typo in setup.py. Fixes #1.

0.1.0 (2014-02-17)
++++++++++++++++++

* Initial release.
