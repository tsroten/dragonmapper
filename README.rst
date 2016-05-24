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
* Output HTML based on the above.

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

.. code:: python

    >>> s = "我是加拿大人"
    >>> zh = hanzi.to_zhuyin(s).split(' ')
    >>> zh
    ['ㄨㄛˇ', 'ㄕˋ', 'ㄐㄧㄚ', 'ㄋㄚˊ', 'ㄉㄚˋ', 'ㄖㄣˊ']
    >>> h = dragonmapper.html.to_html(s, right=zh)
    >>> print(h)

.. image:: http://s33.postimg.org/nzsw0y4qn/Screenshot_from_2016_05_24_01_17_00.png
        :target: http://postimg.org/image/6z9zs9rp7/


Getting Started
---------------
* `Install Dragon Mapper <http://dragonmapper.readthedocs.org/en/latest/installation.html>`_
* Read `Dragon Mapper's tutorial <http://dragonmapper.readthedocs.org/en/latest/tutorial.html>`_
* Report bugs and ask questions via `GitHub Issues <https://github.com/tsroten/dragonmapper>`_
* Refer to the `API documentation <http://dragonmapper.readthedocs.org/en/latest/api.html>`_ when you need more technical information
* `Contribute <http://dragonmapper.readthedocs.org/en/latest/contributing.html>`_ documentation, code, or feedback
