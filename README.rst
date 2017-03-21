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
* [HTML] You can even mix-and-match the different phonetic systems:
* [HTML] right=, and top= are also available.
* [HTML] See data/default-style.css

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
    >>> zh = hanzi.to_zhuyin(s)
    >>> zh
    'ㄨㄛˇ ㄕˋ ㄐㄧㄚ ㄋㄚˊ ㄉㄚˋ ㄖㄣˊ'
    >>> h = dragonmapper.html.to_html(s, right=zh)
    >>> print(h)

.. image:: http://s25.postimg.org/82l3nbfrz/Screenshot_from_2016_06_03_11_16_14.png
        :target: http://postimg.org/image/m90uijqmz/

.. code:: python

    >>> s = "我是加拿大人"
    >>> zh = hanzi.to_zhuyin(s)
    >>> pi = trans.zhuyin_to_pinyin(zh)
    >>> pi
    'wǒ shì jiā ná dà rén'
    >>> h = dragonmapper.html.to_html(s, bottom=pi)
    >>> print(h)

* The intermediate switch to Zhuyin, is because of spacing. You can space out the characters instead.
.. image:: http://s25.postimg.org/9vo0bn0yn/Screenshot_from_2016_06_03_11_16_39.png
        :target: http://postimg.org/image/j3g8sc80r/

.. code:: python

    >>> s = "我是加拿大人"
    >>> zh = hanzi.to_zhuyin(s)
    >>> pi = trans.zhuyin_to_pinyin(zh)
    >>> h = dragonmapper.html.to_html(s, bottom=pi, right=zh)
    >>> print(h)

.. image:: http://s25.postimg.org/9g854vpnj/Screenshot_from_2016_06_03_11_16_57.png
        :target: http://postimg.org/image/m90uijqmz/

Getting Started
---------------
* `Install Dragon Mapper <http://dragonmapper.readthedocs.org/en/latest/installation.html>`_
* Read `Dragon Mapper's tutorial <http://dragonmapper.readthedocs.org/en/latest/tutorial.html>`_
* Report bugs and ask questions via `GitHub Issues <https://github.com/tsroten/dragonmapper>`_
* Refer to the `API documentation <http://dragonmapper.readthedocs.org/en/latest/api.html>`_ when you need more technical information
* `Contribute <http://dragonmapper.readthedocs.org/en/latest/contributing.html>`_ documentation, code, or feedback
