.. Dragon Mapper documentation master file, created by
   sphinx-quickstart on Tue Jan 28 08:53:40 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Dragon Mapper's documentation!
=========================================

Dragon Mapper is a Python library that provides identification and conversion
functions for Chinese text processing:

* Identify a string as Traditional or Simplified Chinese, Pinyin, or Zhuyin.
* Convert between Chinese characters, Pinyin, Zhuyin, and the International
  Phonetic Alphabet.

.. code:: python

    >>> s = '我是一个美国人。'
    >>> dragonmapper.hanzi.is_simplified(s)
    True
    >>> dragonmapper.hanzi.to_pinyin(s)
    'wǒshìyīgèměiguórén。'
    >>> dragonmapper.hanzi.to_pinyin(s, all_readings=True)
    '[wǒ][shì/shi/tí][yī][gè/ge/gě/gàn][měi][guó][rén/ren]。'

.. code:: python

    >>> s = 'Wǒ shì yīgè měiguórén.'
    >>> dragonmapper.transcriptions.is_pinyin(s)
    True
    >>> dragonmapper.transcriptions.pinyin_to_zhuyin(s)
    'ㄨㄛˇ ㄕˋ ㄧ ㄍㄜˋ ㄇㄟˇ ㄍㄨㄛˊ ㄖㄣˊ.'
    >>> dragonmapper.transcriptions.pinyin_to_ipa(s)
    'wɔ˧˩˧ ʂɨ˥˩ i˥ kɤ˥˩ meɪ˧˩˧ kwɔ˧˥ ʐən˧˥.'

If this is your first time using Dragon Mapper, check out the :doc:`installation`.
Then, read the :doc:`tutorial`.

If you want a more in-depth view of Dragon Mapper, check out the :doc:`api`.

If you're looking to help out, read :doc:`contributing`.

Support
-------

If you encounter a bug, have a feature request, or need help using Dragon Mapper, then use
`Dragon Mapper's GitHub Issues page <https://github.com/tsroten/dragonmapper/issues>`_ to send
feedback.

Documentation Contents
----------------------

.. toctree::
    :maxdepth: 2

    readme
    installation
    tutorial
    api
    contributing
    authors
    history
