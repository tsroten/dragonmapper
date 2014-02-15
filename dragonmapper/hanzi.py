# -*- coding: utf-8 -*-
"""Identification and transliteration functions for Chinese characters."""

from __future__ import unicode_literals
import re

import zhon.cedict
import zhon.hanzi
import zhon.pinyin

import dragonmapper.data
import dragonmapper.transcriptions

try:
    str = unicode
except NameError:
    pass


UNKNOWN = 0
TRAD = TRADITIONAL = 1
SIMP = SIMPLIFIED = 2
BOTH = 3
MIXED = 4


_TRAD_CHARS = set(list(zhon.cedict.traditional))
_SIMP_CHARS = set(list(zhon.cedict.simplified))
_SHARED_CHARS = _TRAD_CHARS.intersection(_SIMP_CHARS)
_ALL_CHARS = zhon.cedict.all

_SEPARATOR = '/'


def _load_data():
    """Load the word and character mapping data into a dictionary.

    In the data files, each line is formatted like this:
        HANZI   PINYIN_READING/PINYIN_READING

    So, lines need to be split by '\t' and then the Pinyin readings need to be
    split by '/'.

    """
    _data = {}
    for d, f in (('words', 'hanzi_pinyin_words.tsv'),
                 ('characters', 'hanzi_pinyin_characters.tsv')):
        # Split the lines by tabs: [[hanzi, pinyin]...].
        lines = [l.split('\t') for l in dragonmapper.data.load_data_file(f)]
        # Make a dictionary: {hanzi: [pinyin, pinyin]...}.
        _data[d] = {h: p.split('/') for h, p in lines}
    return _data

print("Loading word/character data files.")
_HANZI_PINYIN_MAP = _load_data()
_CHARACTERS = _HANZI_PINYIN_MAP['characters']
_WORDS = _HANZI_PINYIN_MAP['words']


def identify(s):
    """Identify what kind of Chinese characters a string contains.

    *s* is a string to examine. The string's Chinese characters are tested to
    see if they are compatible with the Traditional or Simplified characters
    systems, compatible with both, or contain a mixture of Traditional and
    Simplified characters. The :data:`TRADITIONAL`, :data:`SIMPLIFIED`,
    :data:`BOTH`, or :data:`MIXED` constants are returned to indicate the
    string's identity. If *s* contains no Chinese characters, then :data:`NONE`
    is returned.

    All characters in a string that aren't found in the CC-CEDICT dictionary
    are ignored.

    Because the Traditional and Simplified Chinese character systems overlap, a
    string containing Simplified characters could identify as
    :data:`SIMPLIFIED` or :data:`BOTH` depending on if the characters are also
    Traditional characters. To make testing the identity of a string easier,
    the functions :func:`is_traditional` and :func:`is_simplified` are
    provided.

    """
    ctext = set(re.sub('[^%s]' % _ALL_CHARS, '', s))
    if not ctext:
        return UNKNOWN
    if ctext.issubset(_SHARED_CHARS):
        return BOTH
    if ctext.issubset(_TRAD_CHARS):
        return TRAD
    if ctext.issubset(_SIMP_CHARS):
        return SIMP
    return MIXED


def is_chinese(s):
    """Check if a string has Chinese characters in it.

    This is equivalent to:
        >>> identify('foo') in (TRADITIONAL, SIMPLIFIED, BOTH, MIXED)

    """
    return identify(s) in (TRADITIONAL, SIMPLIFIED, BOTH, MIXED)


def is_traditional(s):
    """Check if a string's Chinese characters are Traditional.

    This is equivalent to:
        >>> identify('foo') in (TRADITIONAL, BOTH)

    """
    return identify(s) in (TRADITIONAL, BOTH)


def is_simplified(s):
    """Check if a string's Chinese characters are Simplified.

    This is equivalent to:
        >>> identify('foo') in (SIMPLIFIED, BOTH)

    """
    return identify(s) in (SIMPLIFIED, BOTH)


def _hanzi_to_pinyin(w):
    """Return the Pinyin reading for a Chinese word.

    If the given string *w* matches a CC-CEDICT word, the return value is
    formatted like this: [WORD_READING1, WORD_READING2, ...]

    If the given string *w* doesn't match a CC-CEDICT word, the return value
    is formatted like this: [[CHAR_READING1, CHAR_READING2 ...], ...]

    When returning character readings, if a character wasn't recognized, the
    original character is returned, e.g. [[CHAR_READING1, ...], CHAR, ...]

    """
    try:
        return _HANZI_PINYIN_MAP['words'][w]
    except KeyError:
        return [_CHARACTERS.get(c, c) for c in w]


def to_pinyin(hanzi, accented=True, delimiter=' ', all_readings=False):
    """Convert a string's Chinese characters to Pinyin readings.

    *hanzi* is a string containing Chinese characters. *accented* is a
    :data:`bool` indicating whether to return accented or numbered Pinyin
    readings.

    *delimiter* is the character used to indicate word boundaries in *hanzi*.
    This is used to differentiate between words and characters so that a more
    accurate Pinyin reading can be returned.

    *all_readings* is a :data:`bool` indicating whether or not to return all
    possible readings in the case of words/characters that have multiple
    readings.

    Characters not recognized as Chinese are left untouched.

    """
    _hanzi = hanzi
    pinyin = ''

    # Process the given string.
    while _hanzi:

        # Get the next match in the given string.
        m = re.search('[^%s%s]+' % (delimiter, zhon.hanzi.punctuation), _hanzi)

        # There are no more matches, but the string isn't finished yet.
        if m is None and _hanzi:
            pinyin += _hanzi
            break

        start, end = m.span()

        # Process the punctuation marks that occur before the match.
        if start > 0:
            pinyin += _hanzi[0:start]

        # Get the Chinese word/character readings.
        _p = _hanzi_to_pinyin(m.group())

        # Process the returned word readings.
        if m.group() in _WORDS:
            pinyin += '[%s]' % _SEPARATOR.join(_p) if all_readings else _p[0]

        # Process the returned character readings.
        else:
            # Process each character individually.
            for c in _p:
                # Don't touch unrecognized characters.
                if isinstance(c, str):
                    pinyin += c
                # Format multiple readings.
                elif isinstance(c, list) and all_readings:
                        pinyin += '[%s]' % _SEPARATOR.join(c)
                # Select and format the most common reading.
                elif isinstance(c, list) and not all_readings:
                    # Add an apostrophe to separate syllables.
                    if (pinyin and c[0][0] in zhon.pinyin.vowels and
                            pinyin[-1] in zhon.pinyin.lowercase):
                        pinyin += "'"
                    pinyin += c[0]

        # Move ahead in the given string.
        _hanzi = _hanzi[end:]

    if accented:
        return pinyin
    else:
        return dragonmapper.transcriptions.apinyin_to_npinyin(pinyin)


def to_zhuyin(hanzi, delimiter=' ', all_readings=False):
    """Convert a string's Chinese characters to Zhuyin readings."""
    npinyin = to_pinyin(hanzi, False, delimiter, all_readings)
    zhuyin = dragonmapper.transcriptions.npinyin_to_zhuyin(npinyin)
    return zhuyin


def to_ipa(hanzi, delimiter=' ', all_readings=False):
    """Convert a string's Chinese characters to IPA."""
    npinyin = to_pinyin(hanzi, False, delimiter, all_readings)
    ipa = dragonmapper.transcriptions.npinyin_to_ipa(npinyin)
    return ipa
