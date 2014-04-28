=============
Dragon Mapper
=============

.. image:: https://badge.fury.io/py/dragonmapper.png
    :target: http://badge.fury.io/py/dragonmapper
    
.. image:: https://travis-ci.org/tsroten/dragonmapper.png?branch=develop
        :target: https://travis-ci.org/tsroten/dragonmapper

Dragon Mapper is a Python library that provides identification and conversion
functions for Chinese text processing.

* Documentation: http://dragonmapper.rtfd.org
* GitHub: https://github.com/tsroten/dragonmapper
* Free software: MIT license

Features
--------

* Convert between Chinese characters, Pinyin, Zhuyin, and the International
  Phonetic Alphabet.
* Identify a string as Traditional or Simplified Chinese, Pinyin, Zhuyin, or
  the International Phonetic Alphabet.

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

Getting Started
---------------
* `Install Dragon Mapper <http://dragonmapper.readthedocs.org/en/latest/installation.html>`_
* Read `Dragon Mapper's tutorial <http://dragonmapper.readthedocs.org/en/latest/tutorial.html>`_
* Report bugs and ask questions via `GitHub Issues <https://github.com/tsroten/dragonmapper>`_
* Refer to the `API documentation <http://dragonmapper.readthedocs.org/en/latest/api.html>`_ when you need more technical information
* `Contribute <http://dragonmapper.readthedocs.org/en/latest/contributing.html>`_ documentation, code, or feedback
