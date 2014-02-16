# -*- coding: utf-8 -*-
"""Provides mapping functions between various Chinese transcription systems."""

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
                    set(_UNACCENTED_VOWELS + 'v'))))

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
_IPA_SYL = '[%(characters)s]+[%(marks)s]*' % {'characters': _IPA_CHARACTERS,
                                              'marks': _IPA_MARKS}


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
    """Check if the given string contains accented Pinyin vowels."""
    return bool(re.search('[%s]' % _ACCENTED_VOWELS, s))


def _npinyin_vowel_to_apinyin(vowel, tone):
    """Convert a numbered Pinyin vowel to an accented Pinyin vowel."""
    try:
        return _PINYIN_TONES[vowel + str(tone)]
    except IndexError:
        raise ValueError("Vowel must be one of '%s' and tone must be an int "
                         "or str 1-5." % _UNACCENTED_VOWELS)


def _apinyin_vowel_to_npinyin(vowel):
    """Convert an accented Pinyin vowel to a numbered Pinyin vowel."""
    for numbered, accented in _PINYIN_TONES.items():
        if vowel == accented:
            return numbered[0], numbered[1]


def _parse_npinyin_syl(unparsed_syl):
    """Return the syllable and tone of a numbered Pinyin syllable."""
    tone = unparsed_syl[-1]
    if not tone.isdigit():
        syl, tone = unparsed_syl, '5'
    elif tone == '0':
        syl, tone = unparsed_syl[:-1], '5'
    elif tone in '12345':
        syl = unparsed_syl[:-1]
    else:
        raise ValueError("Invalid syllable: %s" % unparsed_syl)
    return syl, tone


def _parse_apinyin_syl(unparsed_syl):
    """Return the syllable and tone of an accented Pinyin syllable.

    Any accented vowels are returned without their accents.

    Implements the following algorithm:

    1. If the syllable has an accent mark, convert that vowel to a
        regular vowel and add the tone to the end of the syllable.
    2. Otherwise, assume the syllable is tone 5 (no accent marks).

    """
    if unparsed_syl[0] == '\u00B7':
        return unparsed_syl[1:], '5'  # Special case for middle dot tone mark.
    for c in unparsed_syl:
        if c in _ACCENTED_VOWELS:
            vowel, tone = _apinyin_vowel_to_npinyin(c)
            return unparsed_syl.replace(c, vowel), tone
    return unparsed_syl, '5'


def _parse_pinyin_syl(unparsed_syl):
    """Return the syllable and tone of a Pinyin syllable.

    Accented vowels are returned with the accents removed.

    """

    if _has_accented_vowels(unparsed_syl):
        return _parse_apinyin_syl(unparsed_syl)
    else:
        return _parse_npinyin_syl(unparsed_syl)


def _parse_zhuyin_syl(unparsed_syl):
    """Return the syllable and tone of a Zhuyin syllable."""
    tone = unparsed_syl[-1]
    if tone in zhon.zhuyin.characters:
        syl, tone = unparsed_syl, '1'
    elif tone in zhon.zhuyin.marks:
        for num, mark in _ZHUYIN_TONES.items():
            if tone == mark:
                syl, tone = unparsed_syl[:-1], num
    else:
        raise ValueError("Invalid syllable: %s" % unparsed_syl)

    return syl, tone


def _parse_ipa_syl(unparsed_syl):
    """Return the syllable and tone of an IPA syllable."""
    _tone = re.search('[%(marks)s]+' % {'marks': _IPA_MARKS}, unparsed_syl)
    if not _tone:
        syl, tone = unparsed_syl, '5'
    else:
        for tone, mark in _IPA_TONES.items():
            if _tone.group() == mark:
                break
        syl = unparsed_syl[0:_tone.start()]
    return syl, tone


def _mem_lower_case(s):
    """Convert a string to lowercase and remember its original case."""
    return s.lower(), [c.islower() for c in s]


def _mem_restore_case(s, mem):
    """Restore a lowercase string's characters to their original case."""
    return ''.join([c if mem[i] else c.upper() for i, c in enumerate(s)])


def npinyin_syl_to_apinyin(syl):
    """Convert a numbered Pinyin syllable to an accented Pinyin syllable.

    It implements the following algorithm to determine where to place tone
    marks:

    1. If the syllable has an 'a', 'e', or 'o' (in that order), put the
        tone mark over that vowel.
    2. Otherwise, put the tone mark on the last vowel.

    """
    lsyl, case_mem = _mem_lower_case(syl)
    if syl == 'r5':
        return 'r'  # Special case for 'r' suffix.
    if re.search('[%s]' % _UNACCENTED_VOWELS, lsyl) is None:
        return syl
    _syl, tone = _parse_npinyin_syl(lsyl)
    _syl = re.sub('u:|v', '\u00fc', _syl)
    if 'a' in _syl:
        psyl = _syl.replace('a', _npinyin_vowel_to_apinyin('a', tone))
    elif 'e' in _syl:
        psyl = _syl.replace('e', _npinyin_vowel_to_apinyin('e', tone))
    elif 'o' in _syl:
        psyl = _syl.replace('o', _npinyin_vowel_to_apinyin('o', tone))
    else:
        vowel = _syl[max(map(_syl.rfind, _UNACCENTED_VOWELS))]
        psyl = _syl.replace(vowel, _npinyin_vowel_to_apinyin(vowel, tone))
    return _mem_restore_case(psyl, case_mem)


def apinyin_syl_to_npinyin(syl):
    """Convert an accented Pinyin syllable to a numbered Pinyin syllable.

    This function assumes the syllable is valid Pinyin.

    Implements the following algorithm:

    1. If the syllable has an accent mark, convert that vowel to a
        regular vowel and add the tone to the end of the syllable.
    2. Otherwise, assume the syllable is tone 5 (no accent marks).

    """
    return ''.join(_parse_apinyin_syl(syl))


def pinyin_syl_to_zhuyin(syl):
    """Convert a Pinyin syllable to a Zhuyin syllable."""
    _syl, tone = _parse_pinyin_syl(syl)
    try:
        zsyl = _PINYIN_MAP[_syl.lower()]['Zhuyin']
    except IndexError:
        raise ValueError('Not a valid syllable: %s' % syl)
    return zsyl + _ZHUYIN_TONES[tone]


def pinyin_syl_to_ipa(syl):
    """Convert a Pinyin syllable to an IPA syllable."""
    _syl, tone = _parse_pinyin_syl(syl)
    try:
        isyl = _PINYIN_MAP[_syl.lower()]['IPA']
    except IndexError:
        raise ValueError('Not a valid syllable: %s' % syl)
    return isyl + _IPA_TONES[tone]


def _zhuyin_syl_to_npinyin(syl):
    """Convert a Zhuyin syllable to a numbered Pinyin syllable."""
    _syl, tone = _parse_zhuyin_syl(syl)
    try:
        psyl = _ZHUYIN_MAP[_syl]['Pinyin']
    except IndexError:
        raise ValueError('Not a valid syllable: %s' % syl)
    return psyl + tone


def _zhuyin_syl_to_apinyin(syl):
    """Convert a Zhuyin syllable to an accented Pinyin syllable."""
    return npinyin_syl_to_apinyin(_zhuyin_syl_to_npinyin(syl))


def zhuyin_syl_to_pinyin(syl, accented=True):
    """Convert a Zhuyin syllable to a Pinyin syllable."""
    if accented:
        return _zhuyin_syl_to_apinyin(syl)
    else:
        return _zhuyin_syl_to_npinyin(syl)


def zhuyin_syl_to_ipa(syl):
    """Convert a Zhuyin syllable to an IPA syllable."""
    return pinyin_syl_to_ipa(_zhuyin_syl_to_npinyin(syl))


def _ipa_syl_to_npinyin(syl):
    """Convert an IPA syllable to a numbered Pinyin syllable."""
    _syl, tone = _parse_ipa_syl(syl)
    try:
        psyl = _IPA_MAP[_syl]['Pinyin']
    except IndexError:
        raise ValueError('Not a valid syllable: %s' % syl)
    return psyl + tone


def _ipa_syl_to_apinyin(syl):
    """Convert an IPA syllable to an accented Pinyin syllable."""
    return npinyin_syl_to_apinyin(_ipa_syl_to_npinyin(syl))


def ipa_syl_to_pinyin(syl, accented=True):
    """Convert an IPA syllable to a Pinyin syllable."""
    return _ipa_syl_to_apinyin(syl) if accented else _ipa_syl_to_npinyin(syl)


def ipa_syl_to_zhuyin(syl):
    """Convert an IPA syllable to a Zhuyin syllable."""
    return pinyin_syl_to_zhuyin(_ipa_syl_to_npinyin(syl))


def _convert(s, re_pattern, syl_func, remove_apostrophes=False,
             separate_syllables=False):
    """Convert a string's syllables to a different transcription system."""
    _s = s
    n = ''
    while _s:
        m = re.search(re_pattern, _s, re.I)
        if m is None and _s:
            # There are no more matches, but the given string isn't fully
            # processed yet.
            n += _s
            break
        start, end = m.span()
        if start > 0:  # Handle extra characters before matched syllable.
            if n and remove_apostrophes and start == 1 and _s[0] == "'":
                pass  # Remove the apostrophe between Pinyin syllables.
                if separate_syllables:  # Separate syllables by a space.
                    n += ' '
            else:
                n += _s[0:start]
        else:  # Matched syllable starts immediately.
            if n and separate_syllables:  # Separate syllables by a space.
                n += ' '
        n += syl_func(m.group())  # Convert the matched syllable.
        _s = _s[end:]
    return n


def npinyin_to_apinyin(s):
    """Convert all numbered Pinyin syllables in a string to accented Pinyin."""
    return _convert(s, zhon.pinyin.syl, npinyin_syl_to_apinyin)


def apinyin_to_npinyin(s):
    """Convert all accented Pinyin syllables in a string to numbered Pinyin."""
    return _convert(s, zhon.pinyin.syl, apinyin_syl_to_npinyin)


def pinyin_to_zhuyin(s):
    """Convert all Pinyin syllables in a string to Zhuyin."""
    return _convert(s, zhon.pinyin.syl, pinyin_syl_to_zhuyin, True, True)


def pinyin_to_ipa(s):
    """Convert all Pinyin syllables in a string to IPA."""
    return _convert(s, zhon.pinyin.syl, pinyin_syl_to_ipa, True, True)


def zhuyin_to_pinyin(s, accented=True):
    """Convert all Zhuyin syllables in a string to Pinyin."""
    return _convert(s, zhon.zhuyin.syl, _zhuyin_syl_to_apinyin if accented else
                    _zhuyin_syl_to_npinyin)


def zhuyin_to_ipa(s):
    """Convert all Zhuyin syllables in a string to IPA."""
    return _convert(s, zhon.zhuyin.syl, zhuyin_syl_to_ipa)


def ipa_to_pinyin(s, accented=True):
    """Convert all IPA syllables in a string to Pinyin."""
    return _convert(s, _IPA_SYL, _ipa_syl_to_apinyin if accented else
                    _ipa_syl_to_npinyin)


def ipa_to_zhuyin(s):
    """Convert all IPA syllables in a string to Zhuyin."""
    return _convert(s, _IPA_SYL, ipa_syl_to_zhuyin)


def to_pinyin(s, accented=True):
    """Convert a string to Pinyin."""
    i = identify(s)
    if i == PINYIN:
        if _has_accented_vowels(s):
            return s if accented else apinyin_to_npinyin(s)
        else:
            return npinyin_to_apinyin(s) if accented else s
    elif i == ZHUYIN:
        return zhuyin_to_pinyin(s, accented=accented)
    elif i == IPA:
        return ipa_to_pinyin(s, accented=accented)
    else:
        raise ValueError("String is not a valid Chinese transcription.")


def to_zhuyin(s):
    """Convert a string to Zhuyin."""
    i = identify(s)
    if i == ZHUYIN:
        return s
    elif i == PINYIN:
        return pinyin_to_zhuyin(s)
    elif i == IPA:
        return ipa_to_zhuyin(s)
    else:
        raise ValueError("String is not a valid Chinese transcription.")


def to_ipa(s):
    """Convert a string to IPA."""
    i = identify(s)
    if i == IPA:
        return s
    elif i == PINYIN:
        return pinyin_to_ipa(s)
    elif i == ZHUYIN:
        return zhuyin_to_ipa(s)
    else:
        raise ValueError("String is not a valid Chinese transcription.")


def _is_pattern_match(ptn, s):
    """Check if a re pattern expression matches an entire string."""
    m = re.match(ptn, s, re.I)
    return m.group() == s if m else False


def is_pinyin(p):
    """Check if a given string consists of valid Pinyin."""
    ptn = ('(?:%(word)s|[ \t%(punctuation)s])+' %
           {'word': zhon.pinyin.word, 'punctuation': zhon.pinyin.punctuation,
            })
    return _is_pattern_match(ptn, p)


def is_zhuyin(s):
    """Check if a given string consists of valid Zhuyin."""
    ptn = '(?:%(syl)s|\s)+' % {'syl': zhon.zhuyin.syl}
    return _is_pattern_match(ptn, s)


def is_ipa(s):
    """Check if a given string consists of valid Chinese IPA."""
    ptn = ('(?:%(syl)s|[ \t%(punctuation)s])+' %
           {'syl': _IPA_SYL, 'punctuation': zhon.pinyin.punctuation})
    return _is_pattern_match(ptn, s)


def identify(s):
    """Identify a given string's transcription system.

    *s* is the string to identify. The string is checked to see if its
    contents are valid Pinyin, Zhuyin, or IPA. The :data:`PINYIN`,
    :data:`ZHUYIN`, and :data:`IPA` constants are returned to indicate the
    string's identity.
    If *s* is not a valid transcription system, then :data:`UNKNOWN` is
    returned.

    """
    if is_pinyin(s):
        return PINYIN
    elif is_zhuyin(s):
        return ZHUYIN
    elif is_ipa(s):
        return IPA
    else:
        return UNKNOWN
