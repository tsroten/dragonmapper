API
===

.. module:: dragonmapper.hanzi

dragonmapper.hanzi
------------------

Identification and transcription functions for Chinese characters.

Importing this module takes a moment because it loads
`CC-CEDICT <http://cc-cedict.org/wiki/>`_ and
`Unihan <http://www.unicode.org/charts/unihan.html>`_ data into memory.

Identifying Chinese Characters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Identifying a string of text
as Traditional or Simplified Chinese is a complicated task. This module
takes a simple approach that only looks at individual characters and not word
choice. When these functions identify a string of text as Simplified, they
aren't saying, "This string of Chinese *is* Simplified Chinese and *not*
Traditional Chinese." Instead, see it as identifying the string as *compatible*
with the Simplified Chinese character system.

.. NOTE::

    These identification functions and constants are imported from the
    `Hanzi Identifier <https://github.com/tsroten/hanzidentifier>`_ library.

The following constants are used as return values for :func:`identify`.

.. data:: UNKNOWN

    Indicates that a string doesn't contain any Chinese characters.

.. data:: TRAD
        TRADITIONAL

    Indicates that a string contains Chinese characters that are only used in
    Traditional Chinese.

.. data:: SIMP
        SIMPLIFIED

    Indicates that a string contains Chinese characters that are only used in
    Simplified Chinese.

.. data:: BOTH

    Indicates that a string contains Chinese characters that are compatible
    with both Traditional and Simplified Chinese.

.. data:: MIXED

    Indicates that a string contains Chinese characters that are found
    exclusively in Traditional and Simplified Chinese.

.. function:: identify

    Identify what kind of Chinese characters a string contains.

    *s* is a string to examine. The string's Chinese characters are tested to
    see if they are compatible with the Traditional or Simplified characters
    systems, compatible with both, or contain a mixture of Traditional and
    Simplified characters. The :data:`TRADITIONAL`, :data:`SIMPLIFIED`,
    :data:`BOTH`, or :data:`MIXED` constants are returned to indicate the
    string's identity. If *s* contains no Chinese characters, then
    :data:`UNKNOWN` is returned.

    All characters in a string that aren't found in the CC-CEDICT dictionary
    are ignored.

    Because the Traditional and Simplified Chinese character systems overlap, a
    string containing Simplified characters could identify as
    :data:`SIMPLIFIED` or :data:`BOTH` depending on if the characters are also
    Traditional characters. To make testing the identity of a string easier,
    the functions :func:`is_traditional`, :func:`is_simplified`, and
    :func:`has_chinese` are provided.

.. function:: has_chinese

    Check if a string has Chinese characters in it.

    This is a faster version of:
        >>> identify('foo') is not UNKNOWN

.. function:: is_traditional

    Check if a string's Chinese characters are Traditional.

    This is equivalent to:
        >>> identify('foo') in (TRADITIONAL, BOTH)

.. function:: is_simplified

    Check if a string's Chinese characters are Simplified.

    This is equivalent to:
        >>> identify('foo') in (SIMPLIFIED, BOTH)


Transcribing Chinese Characters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following functions transliterate Chinese characters into various transcription
systems.

.. autofunction:: to_pinyin

.. autofunction:: to_zhuyin

.. autofunction:: to_ipa

.. module:: dragonmapper.transcriptions

dragonmapper.transcriptions
---------------------------

Identification and conversion functions for Chinese transcription systems.

Identifying Chinese Transcriptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following constants are used as return values for :func:`identify`.

.. data:: UNKNOWN

    Indicates that a string isn't a recognized Chinese transcription.

.. data:: PINYIN

    Indicates that a string's content consists of Pinyin.

.. data:: ZHUYIN

    Indicates that a string's content consists of Zhuyin (Bopomofo).

.. data:: IPA

    Indicates that a string's content consists of the International Phonetic
    Alphabet (IPA).

.. autofunction:: identify

The following functions use :func:`identify`, but don't require typing the
names of the module-level constants.

.. autofunction:: is_pinyin

.. autofunction:: is_zhuyin

.. autofunction:: is_ipa

The above functions :func:`is_pinyin` and :func:`is_zhuyin` check for valid
syllables. This takes more time than checking on the character-level, but is more
accurate. If you want to simply know if a string is compatible with Pinyin or Zhuyin,
but don't need to know if each syllable is actually valid, then use these functions:

.. autofunction:: is_pinyin_compatible

.. autofunction:: is_zhuyin_compatible

Converting Chinese Transcriptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Converting between the various transcription systems is fairly simple. A few
things to note:

* When converting from Pinyin to Zhuyin or IPA, spaces are added between each
  syllable because Zhuyin and IPA are not meant to be read in sentence format.
  They don't have the equivalent of Pinyin's apostrophe to separate certain
  syllables.
* When converting from Pinyin to Zhuyin or IPA, all syllable-separating
  apostrophes are removed. Those that don't separate syllables (like quotation
  marks) are left untouched.
* In Pinyin, ``'v'`` is considered another way to write ``'ü'``. The
  ``*_to_pinyin`` functions all output that vowel as ``'ü'``.

These conversion functions come in two flavors: functions that convert
individual syllabes and functions that convert sentence-style text. If you
only have individual syllables to convert, it's quicker to use the
``*_syllable_to_*`` functions that assume the input is a single valid syllable.

Syllable Conversion
```````````````````

.. autofunction:: numbered_syllable_to_accented

.. autofunction:: accented_syllable_to_numbered

.. autofunction:: pinyin_syllable_to_zhuyin

.. autofunction:: pinyin_syllable_to_ipa

.. autofunction:: zhuyin_syllable_to_pinyin

.. autofunction:: zhuyin_syllable_to_ipa

.. autofunction:: ipa_syllable_to_pinyin

.. autofunction:: ipa_syllable_to_zhuyin


Sentence-Style Conversion
`````````````````````````

.. autofunction:: numbered_to_accented

.. autofunction:: accented_to_numbered

.. autofunction:: pinyin_to_zhuyin

.. autofunction:: pinyin_to_ipa

.. autofunction:: zhuyin_to_pinyin

.. autofunction:: zhuyin_to_ipa

.. autofunction:: ipa_to_pinyin

.. autofunction:: ipa_to_zhuyin

Combined: Identification and Conversion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These functions take an unidentified transcription string and identify it,
then convert it into the target transcription system. If you know you'll be
identifying your strings before you convert them, these can save you a few
lines of code.

.. autofunction:: to_pinyin

.. autofunction:: to_zhuyin

.. autofunction:: to_ipa
