Dragon Mapper
=============

Dragon Mapper is a Python library that provides identification and conversion
functions for Chinese text processing.

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


Install
-------

Dragon Mapper supports Python 2.7 and 3. The only additional requirement is
`Zhon <https://github.com/tsroten/zhon>`_.

Just use pip:

.. code:: bash

    $ pip install dragonmapper


Documentation
-------------

Dragon Mapper includes complete and easy-to-read `documentation <https://dragonmapper.readthedocs.org/>`_. Check it out for a gentle introduction or the full API details.

Bugs/Feature Requests
---------------------

Dragon Mapper uses its `GitHub Issues page
<https://github.com/tsroten/dragonmapper/issues>`_ to track bugs, feature
requests, and support questions.

License
-------

Dragon Mapper is released under the OSI-approved `MIT License <http://opensource.org/licenses/MIT>`_. See the file LICENSE.txt for more information.
