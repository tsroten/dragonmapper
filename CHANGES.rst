.. :changelog:

Change Log
----------

0.2.6 (2016-05-23)
++++++++++++++++++

* Fixes reading for 女. Fixes #10.
* Add a note about Unicode string for Python 2 users.
* Bumps required hanzidentifier version.
* Fix umlaut on "l" consonant. Fixes #14.

0.2.5 (2015-08-06)
++++++++++++++++++

* Fixes #9. Uses io.open() in setup.py with UTF-8 encoding.

0.2.4 (2015-04-08)
++++++++++++++++++

* Fixes #8. Adds re.UNICODE to transcription conversion.
* Fixes misformatted readings for certain characters.
* Fixes #7. Fixes incorrect Unihan Database readings for the 'ou' vowel combinations.

0.2.3 (2014-04-28)
++++++++++++++++++

* Fixes #6. Adds -r suffix syllable to transcription mapping data.

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
