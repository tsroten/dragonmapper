Tutorial
========

This tutorial will walk you through common tasks involving Dragon Mapper and
its two supported data formats: Chinese characters and Chinese transcriptions.
Not all of Dragon Mapper's functions or their options are explained here. Be
sure to read the :doc:`api` for further information.

.. note::

   Python 2 strings are not Unicode by default. Prefix the strings in these
   code samples with 'u' to make them work correctly. For example,
   ``u'这个字怎么念？'`` instead of ``'这个字怎么念？'``. See `Unicode Literals
   in Python Source Code`_ for more information.

.. _Unicode Literals in Python Source Code: https://docs.python.org/2/howto/unicode.html#unicode-literals-in-python-source-code

Working with Chinese Characters
-------------------------------

When using Dragon Mapper to work with Chinese characters, you will first want
to import Dragon Mapper's :mod:`dragonmapper.hanzi` module:

.. code:: python

    >>> from dragonmapper import hanzi

It will take a second or two for Dragon Mapper to load the CC-CEDICT and
Unihan data into memory.

Convert Characters to Readings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's take a look at a common task: converting a string of Chinese characters
to Pinyin. We'll be using the function :func:`dragonmapper.hanzi.to_pinyin`.

.. code:: python

    >>> s = '这个字怎么念？'
    >>> hanzi.to_pinyin(s)
    'zhègèzìzěnmeniàn？'

As you can see, Dragon Mapper simply replaced each Chinese character with it's
most common reading. Dragon Mapper will automatically add apostrophes to
separate syllables if needed. That is all you need for simple cases. However,
you may want to include all possible readings just in case the most common
reading is incorrect.

.. code:: python

    >>> hanzi.to_pinyin(s, all_readings=True)
    '[zhè][gè/ge/gě/gàn][zì/zi][zěn][me/yāo/mó/ma][niàn]？'

In the previous examples, Dragon Mapper converted each character separately.
Most of the time, you will want to segment your text into words and convert
whole words instead of just characters. Just separate the words by spaces or
Chinese punctuation marks and Dragon Mapper will recognize the word boundaries.

.. code:: python

    >>> # Sentence without word boundaries marked.
    ... s = '这个很便宜。'
    >>> hanzi.to_pinyin(s)
    'zhègèhěnbiànyi。'

    >>> # Sentence with word boundaries marked.
    ... s_spaced = '这个 很 便宜。'
    >>> hanzi.to_pinyin(s_spaced)
    'zhège hěn piànyi。'

    >>> hanzi.to_pinyin(s_spaced, all_readings=True)
    '[zhège] [hěn] [piànyi/biànyí]。'

Dragon Mapper's :func:`dragonmapper.hanzi.to_zhuyin` and
:func:`dragonmapper.hanzi.to_ipa` work just like the above examples.

Identifying Chinese Characters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Identifying a string of Chinese as containing Traditional versus Simplified
characters is a difficult task that involves a lot more than merely looking at
each character on its own. That task is best left up to humans. However, it can
also be helpful to get a general idea of what character system a string is
compatible with. Dragon Mapper can assist with that.

:func:`dragonmapper.hanzi.identify` and its related functions can identify
Chinese characters as Traditional or Simplified based on the CC-CEDICT
dictionary. Again, don't see this as a fool proof way to determine a string's
identity. Instead, look at it as a way to determine what character system a
string is compatible with. Let's take a look:

.. code:: python

    >>> s = '那辆车是我的。'
    >>> hanzi.identify(s) is hanzi.SIMPLIFIED
    True

    >>> # Shortcut functions are provided:
    ... hanzi.is_simplified(s)
    True
    >>> hanzi.is_traditional(s)
    False

The Traditional and Simplified Chinese character systems share some
characters. Sometimes a string can be compatible with both character systems:

.. code:: python

    >>> s = '你好！'
    >>> hanzi.identify(s) is hanzi.BOTH
    True

    >>> # Using the shortcut functions:
    ... hanzi.is_traditional(s)
    True
    >>> hanzi.is_simplified(s)
    True

Sometimes, a string might contain characters that exist exclusively in
Traditional Chinese and characters that exist exclusively in Simplified:

.. code:: python

    >>> s = 'Traditional: 車. Simplified: 车.'
    >>> hanzi.identify(s) is hanzi.MIXED
    True

    >>> hanzi.has_chinese(s)
    True
    >>> # It's not compatible with Traditional or Simplified Chinese:
    ... hanzi.is_traditional(s)
    False
    >>> hanzi.is_simplified(s)
    False

The last scenario is a string that doesn't contain any Chinese characters:

.. code:: python

    >>> s = 'Hello. My name is Thomas.'
    >>> hanzi.identify(s) is hanzi.UNKNOWN
    True

    >>> hanzi.has_chinese(s)
    False

Working with Transcriptions
---------------------------

When using Dragon Mapper to work with Chinese transcriptions, you will first
want to import Dragon Mapper's :mod:`dragonmapper.transcriptions` module:

.. code:: python

    >>> from dragonmapper import transcriptions

Identifying Transcription Systems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dragon Mapper supports three transcription systems: Pinyin (accented and
numbered), Zhuyin (Bopomofo), and the International Phonetic Alphabet (IPA).

Let's try to identify which transcription system a string is:

.. code:: python

    >>> s = 'Wǒ shì yīgè měiguórén.'
    >>> transcriptions.identify(s) is transcriptions.PINYIN
    True
    
    >>> # Shortcut functions:
    ... transcriptions.is_pinyin(s)
    True
    >>> transcriptions.is_zhuyin(s)
    False
    >>> transcriptions.is_ipa(s)
    False

.. code:: python

    >>> s = 'ㄋㄧˇ ㄏㄠˇ'
    >>> transcriptions.identify(s) is transcriptions.ZHUYIN
    True

    >>> # Shortcut functions:
    ... transcriptions.is_zhuyin(s)
    True
    >>> transcriptions.is_pinyin(s)
    False
    >>> transcriptions.is_ipa(s)
    False

The functions above operate on a syllable-level to check whether or not a Pinyin or Zhuyin
string is valid. However, this can take awhile, so if you don't need to validate a string
on the syllable-level, consider validating it on a character-level with
:func:`~dragonmapper.transcriptions.is_pinyin_compatible` or :func:`~dragonmapper.transcriptions.is_zhuyin_compatible`

.. code:: python

    >>> s = 'Wǒ shì yīgè měiguórén.'
    >>> transcriptions.is_pinyin_compatible(s)
    True


Converting Transcription Systems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Converting between Pinyin, Zhuyin, and IPA is simple. The syllables
have a one-to-one correspondence. Let's see how Dragon Mapper handles it:

.. code:: python

    >>> zhuyin = 'ㄋㄧˇ ㄏㄠˇ'
    >>> pinyin = transcriptions.zhuyin_to_pinyin(zhuyin)
    >>> ipa = transcriptions.zhuyin_to_ipa(zhuyin)

    >>> print(pinyin)
    nǐ hǎo
    >>> print(ipa)
    ni˧˩˧ xɑʊ˧˩˧

Pinyin apostrophes are handled automatically when converting to/from Pinyin.
If you're into using middle dots for tone markers, those are supported as
well.

If you have a string and you don't know what transcription system it's using,
but you know what system you want to convert it to, Dragon Mapper has some
handy functions to help you:


.. code:: python

    >>> unknown = 'nǐhǎo'
    >>> transcriptions.to_zhuyin(unknown)
    'ㄋㄧˇ ㄏㄠˇ'

    >>> # If it's already in the target transcription, no conversion is done.
    ... transcriptions.to_pinyin(unknown)
    'nǐhǎo'

:func:`dragonmapper.transcriptions.to_pinyin`,
:func:`dragonmapper.transcriptions.to_zhuyin`, and
:func:`dragonmapper.transcriptions.to_ipa` all work like that.

Conclusion
----------

You've seen that Dragon Mapper understands two data formats: Chinese
characters and Chinese transcriptions. Dragon Mapper has both identification
and conversion capabilities.

Not all of Dragon Mapper's functions or their options were explained above. Be
sure to read the :doc:`api` for further information.
