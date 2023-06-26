# -*- coding: utf-8 -*-
"""Identification and transliteration functions for Chinese characters."""

from __future__ import unicode_literals
import re

import hanzidentifier
import zhon.hanzi
import zhon.pinyin

import dragonmapper.data
from dragonmapper.transcriptions import (
    accented_to_numbered,
    pinyin_to_ipa,
    pinyin_to_zhuyin
)

UNKNOWN = hanzidentifier.UNKNOWN
BOTH = hanzidentifier.BOTH
MIXED = hanzidentifier.MIXED
TRAD = TRADITIONAL = hanzidentifier.TRADITIONAL
SIMP = SIMPLIFIED = hanzidentifier.SIMPLIFIED
identify = hanzidentifier.identify
is_simplified = hanzidentifier.is_simplified
is_traditional = hanzidentifier.is_traditional
has_chinese = hanzidentifier.has_chinese

try:
    str = unicode
except NameError:
    pass

_READING_SEPARATOR = '/'


def _load_data():
    """Load the word and character mapping data into a dictionary.

    In the data files, each line is formatted like this:
        HANZI   PINYIN_READING/PINYIN_READING

    So, lines need to be split by '\t' and then the Pinyin readings need to be
    split by '/'.

    """
    data = {}
    for name, file_name in (('words', 'hanzi_pinyin_words.tsv'),
                            ('characters', 'hanzi_pinyin_characters.tsv')):
        # Split the lines by tabs: [[hanzi, pinyin]...].
        lines = [line.split('\t') for line in
                 dragonmapper.data.load_data_file(file_name)]
        # Make a dictionary: {hanzi: [pinyin, pinyin]...}.
        data[name] = {hanzi: pinyin.split('/') for hanzi, pinyin in lines}
    return data

_HANZI_PINYIN_MAP = _load_data()
_CHARACTERS = _HANZI_PINYIN_MAP['characters']
_WORDS = _HANZI_PINYIN_MAP['words']


def _hanzi_to_pinyin(hanzi):
    """Return the Pinyin reading for a Chinese word.

    If the given string *hanzi* matches a CC-CEDICT word, the return value is
    formatted like this: [WORD_READING1, WORD_READING2, ...]

    If the given string *hanzi* doesn't match a CC-CEDICT word, the return
    value is formatted like this: [[CHAR_READING1, CHAR_READING2 ...], ...]

    When returning character readings, if a character wasn't recognized, the
    original character is returned, e.g. [[CHAR_READING1, ...], CHAR, ...]

    """
    try:
        return _HANZI_PINYIN_MAP['words'][hanzi]
    except KeyError:
        return [_CHARACTERS.get(character, character) for character in hanzi]


def _enclose_readings(container, readings):
    """Enclose a reading within a container, e.g. '[]'."""
    container_start, container_end = tuple(container)
    enclosed_readings = '%(container_start)s%(readings)s%(container_end)s' % {
        'container_start': container_start, 'container_end': container_end,
        'readings': readings}
    return enclosed_readings


def to_pinyin(s, delimiter=' ', all_readings=False, container='[]',
              accented=True):
    """Convert a string's Chinese characters to Pinyin readings.

    *s* is a string containing Chinese characters. *accented* is a
    boolean value indicating whether to return accented or numbered Pinyin
    readings.

    *delimiter* is the character used to indicate word boundaries in *s*.
    This is used to differentiate between words and characters so that a more
    accurate reading can be returned.

    *all_readings* is a boolean value indicating whether or not to return all
    possible readings in the case of words/characters that have multiple
    readings. *container* is a two character string that is used to
    enclose words/characters if *all_readings* is ``True``. The default
    ``'[]'`` is used like this: ``'[READING1/READING2]'``.

    Characters not recognized as Chinese are left untouched.

    """
    hanzi = s
    pinyin = ''

    # Process the given string.
    while hanzi:

        # Get the next match in the given string.
        match = re.search('[^%s%s]+' % (delimiter, zhon.hanzi.punctuation),
                          hanzi)

        # There are no more matches, but the string isn't finished yet.
        if match is None and hanzi:
            pinyin += hanzi
            break

        match_start, match_end = match.span()

        # Process the punctuation marks that occur before the match.
        if match_start > 0:
            pinyin += hanzi[0:match_start]

        # Get the Chinese word/character readings.
        readings = _hanzi_to_pinyin(match.group())

        # Process the returned word readings.
        if match.group() in _WORDS:
            if all_readings:
                reading = _enclose_readings(container,
                                            _READING_SEPARATOR.join(readings))
            else:
                reading = readings[0]
            pinyin += reading

        # Process the returned character readings.
        else:
            # Process each character individually.
            for character in readings:
                # Don't touch unrecognized characters.
                if isinstance(character, str):
                    pinyin += character
                # Format multiple readings.
                elif isinstance(character, list) and all_readings:
                    pinyin += _enclose_readings(
                        container, _READING_SEPARATOR.join(character))
                # Select and format the most common reading.
                elif isinstance(character, list) and not all_readings:
                    # Add an apostrophe to separate syllables.
                    if (pinyin and character[0][0] in zhon.pinyin.vowels and
                            pinyin[-1] in zhon.pinyin.lowercase):
                        pinyin += "'"
                    pinyin += character[0]

        # Move ahead in the given string.
        hanzi = hanzi[match_end:]

    if accented:
        return pinyin
    else:
        return accented_to_numbered(pinyin)


def to_zhuyin(s, delimiter=' ', all_readings=False, container='[]'):
    """Convert a string's Chinese characters to Zhuyin readings.

    *s* is a string containing Chinese characters.

    *delimiter* is the character used to indicate word boundaries in *s*.
    This is used to differentiate between words and characters so that a more
    accurate reading can be returned.

    *all_readings* is a boolean value indicating whether or not to return all
    possible readings in the case of words/characters that have multiple
    readings. *container* is a two character string that is used to
    enclose words/characters if *all_readings* is ``True``. The default
    ``'[]'`` is used like this: ``'[READING1/READING2]'``.

    Characters not recognized as Chinese are left untouched.

    """
    numbered_pinyin = to_pinyin(s, delimiter, all_readings, container, False)
    zhuyin = pinyin_to_zhuyin(numbered_pinyin)
    return zhuyin


def to_ipa(s, delimiter=' ', all_readings=False, container='[]'):
    """Convert a string's Chinese characters to IPA.

    *s* is a string containing Chinese characters.

    *delimiter* is the character used to indicate word boundaries in *s*.
    This is used to differentiate between words and characters so that a more
    accurate reading can be returned.

    *all_readings* is a boolean value indicating whether or not to return all
    possible readings in the case of words/characters that have multiple
    readings. *container* is a two character string that is used to
    enclose words/characters if *all_readings* is ``True``. The default
    ``'[]'`` is used like this: ``'[READING1/READING2]'``.

    Characters not recognized as Chinese are left untouched.

    """
    numbered_pinyin = to_pinyin(s, delimiter, all_readings, container, False)
    ipa = pinyin_to_ipa(numbered_pinyin)
    return ipa
