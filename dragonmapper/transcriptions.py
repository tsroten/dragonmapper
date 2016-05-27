# -*- coding: utf-8 -*-
"""Identification and conversion functions for Chinese transcriptions."""

from __future__ import unicode_literals
import re

import zhon.pinyin
import zhon.zhuyin

import dragonmapper.data


UNKNOWN = 0
PINYIN = 1
ZHUYIN = 2
IPA = 3

_UNACCENTED_VOWELS = 'aeiou\u00FC'
_ACCENTED_VOWELS = (''.join(set(zhon.pinyin.vowels.lower()).difference(
                    set(_UNACCENTED_VOWELS + 'v'))) + '\u00B7')

_PINYIN_TONES = {
    'a1': '\u0101', 'a2': '\xe1', 'a3': '\u01ce', 'a4': '\xe0', 'a5': 'a',
    'e1': '\u0113', 'e2': '\xe9', 'e3': '\u011b', 'e4': '\xe8', 'e5': 'e',
    'i1': '\u012b', 'i2': '\xed', 'i3': '\u01d0', 'i4': '\xec', 'i5': 'i',
    'o1': '\u014d', 'o2': '\xf3', 'o3': '\u01d2', 'o4': '\xf2', 'o5': 'o',
    'u1': '\u016b', 'u2': '\xfa', 'u3': '\u01d4', 'u4': '\xf9', 'u5': 'u',
    '\u00fc1': '\u01d6', '\u00fc2': '\u01d8', '\u00fc3': '\u01da',
    '\u00fc4': '\u01dc', '\u00fc5': '\u00fc'
}

_ZHUYIN_TONES = {
    '1': '', '2': 'ˊ', '3': 'ˇ', '4': 'ˋ', '5': '˙'
}

_IPA_TONES = {
    '1': '˥', '2': '˧˥', '3': '˧˩˧', '4': '˥˩', '5': ''
}

_IPA_CHARACTERS = 'AIŋmPɑœɔɕəɛaɤefɨiɪklɯnopstuwxyɻʂʈʊʐɥʰj'
_IPA_MARKS = '˩˧˥'
_IPA_SYLLABLE = ('[%(characters)s]+[%(marks)s]*' %
                 {'characters': _IPA_CHARACTERS, 'marks': _IPA_MARKS})


def _load_data():
    """Load the transcription mapping data into a dictionary."""
    lines = dragonmapper.data.load_data_file('transcriptions.csv')
    pinyin_map, zhuyin_map, ipa_map = {}, {}, {}
    for line in lines:
        p, z, i = line.split(',')
        pinyin_map[p] = {'Zhuyin': z, 'IPA': i}
        zhuyin_map[z] = {'Pinyin': p, 'IPA': i}
        ipa_map[i] = {'Pinyin': p, 'Zhuyin': z}
    return pinyin_map, zhuyin_map, ipa_map

_PINYIN_MAP, _ZHUYIN_MAP, _IPA_MAP = _load_data()


def _has_accented_vowels(s):
    """Check if the given string contains accented Pinyin vowels.

    This includes the prepended middle dot.

    """
    return bool(re.search('[%s]' % _ACCENTED_VOWELS, s))


def _numbered_vowel_to_accented(vowel, tone):
    """Convert a numbered Pinyin vowel to an accented Pinyin vowel."""
    if isinstance(tone, int):
        tone = str(tone)
    return _PINYIN_TONES[vowel + tone]


def _accented_vowel_to_numbered(vowel):
    """Convert an accented Pinyin vowel to a numbered Pinyin vowel."""
    for numbered_vowel, accented_vowel in _PINYIN_TONES.items():
        if vowel == accented_vowel:
            return tuple(numbered_vowel)


def _parse_numbered_syllable(unparsed_syllable):
    """Return the syllable and tone of a numbered Pinyin syllable."""
    tone_number = unparsed_syllable[-1]
    if not tone_number.isdigit():
        syllable, tone = unparsed_syllable, '5'
    elif tone_number == '0':
        syllable, tone = unparsed_syllable[:-1], '5'
    elif tone_number in '12345':
        syllable, tone = unparsed_syllable[:-1], tone_number
    else:
        raise ValueError("Invalid syllable: %s" % unparsed_syllable)
    return syllable, tone


def _parse_accented_syllable(unparsed_syllable):
    """Return the syllable and tone of an accented Pinyin syllable.

    Any accented vowels are returned without their accents.

    Implements the following algorithm:

    1. If the syllable has an accent mark, convert that vowel to a
        regular vowel and add the tone to the end of the syllable.
    2. Otherwise, assume the syllable is tone 5 (no accent marks).

    """
    if unparsed_syllable[0] == '\u00B7':
        # Special case for middle dot tone mark.
        return unparsed_syllable[1:], '5'
    for character in unparsed_syllable:
        if character in _ACCENTED_VOWELS:
            vowel, tone = _accented_vowel_to_numbered(character)
            return unparsed_syllable.replace(character, vowel), tone
    return unparsed_syllable, '5'


def _parse_pinyin_syllable(unparsed_syllable):
    """Return the syllable and tone of a Pinyin syllable.

    Accented vowels are returned with the accents removed.

    """

    if _has_accented_vowels(unparsed_syllable):
        return _parse_accented_syllable(unparsed_syllable)
    else:
        return _parse_numbered_syllable(unparsed_syllable)


def _parse_zhuyin_syllable(unparsed_syllable):
    """Return the syllable and tone of a Zhuyin syllable."""
    zhuyin_tone = unparsed_syllable[-1]
    if zhuyin_tone in zhon.zhuyin.characters:
        syllable, tone = unparsed_syllable, '1'
    elif zhuyin_tone in zhon.zhuyin.marks:
        for tone_number, tone_mark in _ZHUYIN_TONES.items():
            if zhuyin_tone == tone_mark:
                syllable, tone = unparsed_syllable[:-1], tone_number
    else:
        raise ValueError("Invalid syllable: %s" % unparsed_syllable)

    return syllable, tone


def _parse_ipa_syllable(unparsed_syllable):
    """Return the syllable and tone of an IPA syllable."""
    ipa_tone = re.search('[%(marks)s]+' % {'marks': _IPA_MARKS},
                         unparsed_syllable)
    if not ipa_tone:
        syllable, tone = unparsed_syllable, '5'
    else:
        for tone_number, tone_mark in _IPA_TONES.items():
            if ipa_tone.group() == tone_mark:
                tone = tone_number
                break
        syllable = unparsed_syllable[0:ipa_tone.start()]
    return syllable, tone


def _lower_case(s):
    """Convert a string to lowercase and remember its original case."""
    return s.lower(), [c.islower() for c in s]


def _restore_case(s, memory):
    """Restore a lowercase string's characters to their original case."""
    cased_s = []
    for i, c in enumerate(s):
        if i + 1 > len(memory):
            break
        cased_s.append(c if memory[i] else c.upper())
    return ''.join(cased_s)


def numbered_syllable_to_accented(s):
    """Convert numbered Pinyin syllable *s* to an accented Pinyin syllable.

    It implements the following algorithm to determine where to place tone
    marks:

    1. If the syllable has an 'a', 'e', or 'o' (in that order), put the
        tone mark over that vowel.
    2. Otherwise, put the tone mark on the last vowel.

    """
    if s == 'r5':
        return 'r'  # Special case for 'r' suffix.

    lowercase_syllable, case_memory = _lower_case(s)
    syllable, tone = _parse_numbered_syllable(lowercase_syllable)
    syllable = syllable.replace('v', '\u00fc')
    if re.search('[%s]' % _UNACCENTED_VOWELS, syllable) is None:
        return s
    if 'a' in syllable:
        accented_a = _numbered_vowel_to_accented('a', tone)
        accented_syllable = syllable.replace('a', accented_a)
    elif 'e' in syllable:
        accented_e = _numbered_vowel_to_accented('e', tone)
        accented_syllable = syllable.replace('e', accented_e)
    elif 'o' in syllable:
        accented_o = _numbered_vowel_to_accented('o', tone)
        accented_syllable = syllable.replace('o', accented_o)
    else:
        vowel = syllable[max(map(syllable.rfind, _UNACCENTED_VOWELS))]
        accented_vowel = _numbered_vowel_to_accented(vowel, tone)
        accented_syllable = syllable.replace(vowel, accented_vowel)
    return _restore_case(accented_syllable, case_memory)


def accented_syllable_to_numbered(s):
    """Convert accented Pinyin syllable *s* to a numbered Pinyin syllable."""
    if s[0] == '\u00B7':
        lowercase_syllable, case_memory = _lower_case(s[1:])
        lowercase_syllable = '\u00B7' + lowercase_syllable
    else:
        lowercase_syllable, case_memory = _lower_case(s)
    numbered_syllable, tone = _parse_accented_syllable(lowercase_syllable)
    return _restore_case(numbered_syllable, case_memory) + tone


def pinyin_syllable_to_zhuyin(s):
    """Convert Pinyin syllable *s* to a Zhuyin syllable."""
    pinyin_syllable, tone = _parse_pinyin_syllable(s)
    try:
        zhuyin_syllable = _PINYIN_MAP[pinyin_syllable.lower()]['Zhuyin']
    except KeyError:
        raise ValueError('Not a valid syllable: %s' % s)
    return zhuyin_syllable + _ZHUYIN_TONES[tone]


def pinyin_syllable_to_ipa(s):
    """Convert Pinyin syllable *s* to an IPA syllable."""
    pinyin_syllable, tone = _parse_pinyin_syllable(s)
    try:
        ipa_syllable = _PINYIN_MAP[pinyin_syllable.lower()]['IPA']
    except KeyError:
        raise ValueError('Not a valid syllable: %s' % s)
    return ipa_syllable + _IPA_TONES[tone]


def _zhuyin_syllable_to_numbered(s):
    """Convert Zhuyin syllable *s* to a numbered Pinyin syllable."""
    zhuyin_syllable, tone = _parse_zhuyin_syllable(s)
    try:
        pinyin_syllable = _ZHUYIN_MAP[zhuyin_syllable]['Pinyin']
    except KeyError:
        raise ValueError('Not a valid syllable: %s' % s)
    return pinyin_syllable + tone


def _zhuyin_syllable_to_accented(s):
    """Convert Zhuyin syllable *s* to an accented Pinyin syllable."""
    numbered_pinyin = _zhuyin_syllable_to_numbered(s)
    return numbered_syllable_to_accented(numbered_pinyin)


def zhuyin_syllable_to_pinyin(s, accented=True):
    """Convert Zhuyin syllable *s* to a Pinyin syllable.

    If *accented* is ``True``, diacritics are added to the Pinyin syllable. If
    it's ``False``, numbers are used to indicate the syllable's tone.

    """
    if accented:
        return _zhuyin_syllable_to_accented(s)
    else:
        return _zhuyin_syllable_to_numbered(s)


def zhuyin_syllable_to_ipa(s):
    """Convert Zhuyin syllable *s* to an IPA syllable."""
    numbered_pinyin = _zhuyin_syllable_to_numbered(s)
    return pinyin_syllable_to_ipa(numbered_pinyin)


def _ipa_syllable_to_numbered(s):
    """Convert IPA syllable *s* to a numbered Pinyin syllable."""
    ipa_syllable, tone = _parse_ipa_syllable(s)
    try:
        pinyin_syllable = _IPA_MAP[ipa_syllable]['Pinyin']
    except KeyError:
        raise ValueError('Not a valid syllable: %s' % s)
    return pinyin_syllable + tone


def _ipa_syllable_to_accented(s):
    """Convert IPA syllable *s* to an accented Pinyin syllable."""
    numbered_pinyin = _ipa_syllable_to_numbered(s)
    return numbered_syllable_to_accented(numbered_pinyin)


def ipa_syllable_to_pinyin(s, accented=True):
    """Convert IPA syllable *s* to a Pinyin syllable.

    If *accented* is ``True``, diacritics are added to the Pinyin syllable. If
    it's ``False``, numbers are used to indicate the syllable's tone.

    """
    if accented:
        return _ipa_syllable_to_accented(s)
    else:
        return _ipa_syllable_to_numbered(s)


def ipa_syllable_to_zhuyin(s):
    """Convert IPA syllable *s* to a Zhuyin syllable."""
    numbered_pinyin = _ipa_syllable_to_numbered(s)
    return pinyin_syllable_to_zhuyin(numbered_pinyin)


def _convert(s, re_pattern, syllable_function, add_apostrophes=False,
             remove_apostrophes=False, separate_syllables=False):
    """Convert a string's syllables to a different transcription system."""
    original = s
    new = ''
    while original:
        match = re.search(re_pattern, original, re.IGNORECASE | re.UNICODE)
        if match is None and original:
            # There are no more matches, but the given string isn't fully
            # processed yet.
            new += original
            break
        match_start, match_end = match.span()
        if match_start > 0:  # Handle extra characters before matched syllable.
            if (new and remove_apostrophes and match_start == 1 and
                    original[0] == "'"):
                pass  # Remove the apostrophe between Pinyin syllables.
                if separate_syllables:  # Separate syllables by a space.
                    new += ' '
            else:
                new += original[0:match_start]
        else:  # Matched syllable starts immediately.
            if new and separate_syllables:  # Separate syllables by a space.
                new += ' '
            elif (new and add_apostrophes and
                    match.group()[0].lower() in _UNACCENTED_VOWELS):
                new += "'"
        # Convert the matched syllable.
        new += syllable_function(match.group())
        original = original[match_end:]
    return new


def numbered_to_accented(s):
    """Convert all numbered Pinyin syllables in *s* to accented Pinyin."""
    return _convert(s, zhon.pinyin.syllable, numbered_syllable_to_accented,
                    add_apostrophes=True)


def accented_to_numbered(s):
    """Convert all accented Pinyin syllables in *s* to numbered Pinyin."""
    return _convert(s, zhon.pinyin.syllable, accented_syllable_to_numbered)


def pinyin_to_zhuyin(s):
    """Convert all Pinyin syllables in *s* to Zhuyin.

    Spaces are added between connected syllables and syllable-separating
    apostrophes are removed.

    """
    return _convert(s, zhon.pinyin.syllable, pinyin_syllable_to_zhuyin,
                    remove_apostrophes=True, separate_syllables=True)


def pinyin_to_ipa(s):
    """Convert all Pinyin syllables in *s* to IPA.

    Spaces are added between connected syllables and syllable-separating
    apostrophes are removed.

    """
    return _convert(s, zhon.pinyin.syllable, pinyin_syllable_to_ipa,
                    remove_apostrophes=True, separate_syllables=True)


def zhuyin_to_pinyin(s, accented=True):
    """Convert all Zhuyin syllables in *s* to Pinyin.

    If *accented* is ``True``, diacritics are added to the Pinyin syllables. If
    it's ``False``, numbers are used to indicate tone.

    """
    if accented:
        function = _zhuyin_syllable_to_accented
    else:
        function = _zhuyin_syllable_to_numbered
    return _convert(s, zhon.zhuyin.syllable, function)


def zhuyin_to_ipa(s):
    """Convert all Zhuyin syllables in *s* to IPA."""
    return _convert(s, zhon.zhuyin.syllable, zhuyin_syllable_to_ipa)


def ipa_to_pinyin(s, accented=True):
    """Convert all IPA syllables in *s* to Pinyin.

    If *accented* is ``True``, diacritics are added to the Pinyin syllables. If
    it's ``False``, numbers are used to indicate tone.

    """
    if accented:
        function = _ipa_syllable_to_accented
    else:
        function = _ipa_syllable_to_numbered
    return _convert(s, _IPA_SYLLABLE, function)


def ipa_to_zhuyin(s):
    """Convert all IPA syllables in *s* to Zhuyin."""
    return _convert(s, _IPA_SYLLABLE, ipa_syllable_to_zhuyin)


def to_pinyin(s, accented=True):
    """Convert *s* to Pinyin.

    If *accented* is ``True``, diacritics are added to the Pinyin syllables. If
    it's ``False``, numbers are used to indicate tone.

    """
    identity = identify(s)
    if identity == PINYIN:
        if _has_accented_vowels(s):
            return s if accented else accented_to_numbered(s)
        else:
            return numbered_to_accented(s) if accented else s
    elif identity == ZHUYIN:
        return zhuyin_to_pinyin(s, accented=accented)
    elif identity == IPA:
        return ipa_to_pinyin(s, accented=accented)
    else:
        raise ValueError("String is not a valid Chinese transcription.")


def to_zhuyin(s):
    """Convert *s* to Zhuyin."""
    identity = identify(s)
    if identity == ZHUYIN:
        return s
    elif identity == PINYIN:
        return pinyin_to_zhuyin(s)
    elif identity == IPA:
        return ipa_to_zhuyin(s)
    else:
        raise ValueError("String is not a valid Chinese transcription.")


def to_ipa(s):
    """Convert *s* to IPA."""
    identity = identify(s)
    if identity == IPA:
        return s
    elif identity == PINYIN:
        return pinyin_to_ipa(s)
    elif identity == ZHUYIN:
        return zhuyin_to_ipa(s)
    else:
        raise ValueError("String is not a valid Chinese transcription.")


def _is_pattern_match(re_pattern, s):
    """Check if a re pattern expression matches an entire string."""
    match = re.match(re_pattern, s, re.I)
    return match.group() == s if match else False


def is_pinyin(s):
    """Check if *s* consists of valid Pinyin."""
    re_pattern = ('(?:%(word)s|[ \t%(punctuation)s])+' %
                  {'word': zhon.pinyin.word,
                   'punctuation': zhon.pinyin.punctuation})
    return _is_pattern_match(re_pattern, s)


def is_pinyin_compatible(s):
    """Checks if *s* is consists of Pinyin-compatible characters.

    This does not check if *s* contains valid Pinyin syllables; for that
    see :func:`is_pinyin`.

    This function checks that all characters in *s* exist in
    :data:`zhon.pinyin.printable`.

    """
    return _is_pattern_match('[%s]+' % zhon.pinyin.printable, s)


def is_zhuyin(s):
    """Check if *s* consists of valid Zhuyin."""
    re_pattern = '(?:%(syllable)s|\s)+' % {'syllable': zhon.zhuyin.syl}
    return _is_pattern_match(re_pattern, s)


def is_zhuyin_compatible(s):
    """Checks if *s* is consists of Zhuyin-compatible characters.

    This does not check if *s* contains valid Zhuyin syllables; for that
    see :func:`is_zhuyin`.

    Besides Zhuyin characters and tone marks, spaces are also accepted.
    This function checks that all characters in *s* exist in
    :data:`zhon.zhuyin.characters`, :data:`zhon.zhuyin.marks`, or ``' '``.

    """
    printable_zhuyin = zhon.zhuyin.characters + zhon.zhuyin.marks + ' '
    return _is_pattern_match('[%s]+' % printable_zhuyin, s)


def is_ipa(s):
    """Check if *s* consists of valid Chinese IPA."""
    re_pattern = ('(?:%(syllable)s|[ \t%(punctuation)s])+' %
                  {'syllable': _IPA_SYLLABLE,
                   'punctuation': zhon.pinyin.punctuation})
    return _is_pattern_match(re_pattern, s)


def identify(s):
    """Identify a given string's transcription system.

    *s* is the string to identify. The string is checked to see if its
    contents are valid Pinyin, Zhuyin, or IPA. The :data:`PINYIN`,
    :data:`ZHUYIN`, and :data:`IPA` constants are returned to indicate the
    string's identity.
    If *s* is not a valid transcription system, then :data:`UNKNOWN` is
    returned.

    When checking for valid Pinyin or Zhuyin, testing is done on a syllable
    level, not a character level. For example, just because a string is
    composed of characters used in Pinyin, doesn't mean that it will identify
    as Pinyin; it must actually consist of valid Pinyin syllables. The same
    applies for Zhuyin.

    When checking for IPA, testing is only done on a character level. In other
    words, a string just needs to consist of Chinese IPA characters in order
    to identify as IPA.

    """
    if is_pinyin(s):
        return PINYIN
    elif is_zhuyin(s):
        return ZHUYIN
    elif is_ipa(s):
        return IPA
    else:
        return UNKNOWN
