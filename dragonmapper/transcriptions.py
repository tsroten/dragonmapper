# -*- coding: utf-8 -*-
"""Provides mapping functions between various Chinese transcription systems."""

from __future__ import unicode_literals
import re

import zhon.pinyin
import zhon.zhuyin

import dragonmapper.data


UNKNOWN = 0
APINYIN = ACCENTED_PINYIN = 1
NPINYIN = NUMBERED_PINYIN = 2
ZHUYIN = 3
IPA = 4

_NPINYIN_VOWELS = 'aeiou\u00FC'

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


def _load_data():
    """Load the transcription mapping data into a dictionary."""
    lines = dragonmapper.data.load_data_file('transcriptions.csv')
    mapping = {}
    for line in lines:
        p, z, i = line.split(',')
        mapping[p] = {'Zhuyin': z, 'IPA': i}
        mapping[z] = {'Pinyin': p, 'IPA': i}
    return mapping

_TRANSCRIPTION_MAP = _load_data()


def _npinyin_vowel_to_apinyin(vowel, tone):
    """Convert a numbered Pinyin vowel to an accented Pinyin vowel."""
    try:
        return _PINYIN_TONES[vowel + str(tone)]
    except IndexError:
        raise ValueError("Vowel must be one of '%s' and tone must be an int "
                         "or str 1-5." % _NPINYIN_VOWELS)


def _apinyin_vowel_to_npinyin(vowel):
    """Convert an accented Pinyin vowel to a numbered Pinyin vowel."""
    for numbered, accented in _PINYIN_TONES.items():
        if vowel == accented:
            return numbered[0], numbered[1]


def _parse_npinyin_syl(syllable):
    """Return the syllable and tone of a numbered Pinyin syllable."""
    tone = syllable[-1]
    if not tone.isdigit():
        syl, tone = syllable, '5'
    elif tone == '0':
        syl, tone = syllable[:-1], '5'
    elif tone in '12345':
        syl = syllable[:-1]
    else:
        raise ValueError("Invalid syllable: %s" % syllable)
    return syl, tone


def _parse_zhuyin_syl(syllable):
    """Return the syllable and tone of a Zhuyin syllable."""
    tone = syllable[-1]
    if tone in zhon.zhuyin.characters:
        syl, tone = syllable, '1'
    elif tone in zhon.zhuyin.marks:
        for num, mark in _ZHUYIN_TONES.items():
            if tone == mark:
                syl, tone = syllable[:-1], num
    else:
        raise ValueError("Invalid syllable: %s" % syllable)

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
    if re.search('[%s]' % _NPINYIN_VOWELS, lsyl) is None:
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
        vowel = _syl[max(map(_syl.rfind, _NPINYIN_VOWELS))]
        psyl = _syl.replace(vowel, _npinyin_vowel_to_apinyin(vowel, tone))
    return _mem_restore_case(psyl, case_mem)


def npinyin_syl_to_zhuyin(syl):
    """Convert a numbered Pinyin syllable to a Zhuyin syllable."""
    _syl, tone = _parse_npinyin_syl(syl)
    try:
        zsyl = _TRANSCRIPTION_MAP[_syl.lower()]['Zhuyin']
    except IndexError:
        raise ValueError('Not a valid syllable: %s' % syl)
    return zsyl + _ZHUYIN_TONES[tone]


def npinyin_syl_to_ipa(syl):
    """Convert a numbered Pinyin syllable to an IPA syllable."""
    _syl, tone = _parse_npinyin_syl(syl)
    try:
        isyl = _TRANSCRIPTION_MAP[_syl.lower()]['IPA']
    except IndexError:
        raise ValueError('Not a valid syllable: %s' % syl)
    return isyl + _IPA_TONES[tone]


def zhuyin_syl_to_npinyin(syl):
    """Convert a Zhuyin syllable to a numbered Pinyin syllable."""
    _syl, tone = _parse_zhuyin_syl(syl)
    try:
        psyl = _TRANSCRIPTION_MAP[_syl]['Pinyin']
    except IndexError:
        raise ValueError('Not a valid syllable: %s' % syl)
    return psyl + tone


def zhuyin_syl_to_apinyin(syl):
    """Convert a Zhuyin syllable to an accented Pinyin syllable."""
    return npinyin_syl_to_apinyin(zhuyin_syl_to_npinyin(syl))


def zhuyin_syl_to_ipa(syl):
    """Convert a Zhuyin syllable to an IPA syllable."""
    return npinyin_syl_to_ipa(zhuyin_syl_to_npinyin(syl))


def apinyin_syl_to_npinyin(syl):
    """Convert an accented Pinyin syllable to a numbered Pinyin syllable.

    This function assumes the syllable is valid Pinyin.

    Implements the following algorithm:
        1. If the syllable has an accent mark, convert that vowel to a
            regular vowel and add the tone to the end of the syllable.
        2. Otherwise, assume the syllable is tone 5 (no accent marks).

    """
    if syl[0] == '\u00B7':
        return syl[1:] + '5'  # Special case for middle dot tone mark.
    for c in syl:
        if c not in _NPINYIN_VOWELS and c in _PINYIN_TONES.values():
            vowel, tone = _apinyin_vowel_to_npinyin(c)
            return syl.replace(c, vowel) + tone
    return syl + '5'


def apinyin_syl_to_zhuyin(syl):
    """Convert a Zhuyin syllable to an accented Pinyin syllable."""
    return npinyin_syl_to_zhuyin(apinyin_syl_to_npinyin(syl))


def apinyin_syl_to_ipa(syl):
    """Convert an accented Pinyin syllable to an IPA syllable."""
    return npinyin_syl_to_ipa(apinyin_syl_to_npinyin(syl))


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


def npinyin_to_apinyin(n):
    """Convert all numbered Pinyin syllables in a string to accented Pinyin."""
    return _convert(n, zhon.pinyin.syl, npinyin_syl_to_apinyin)


def npinyin_to_zhuyin(n):
    """Convert all numbered Pinyin syllables in a string to Zhuyin."""
    return _convert(n, zhon.pinyin.syl, npinyin_syl_to_zhuyin, True, True)


def npinyin_to_ipa(n):
    """Convert all numbered Pinyin syllables in a string to IPA."""
    return _convert(n, zhon.pinyin.syl, npinyin_syl_to_ipa, True, True)


def zhuyin_to_npinyin(z):
    """Convert all Zhuyin syllables in a string to numbered Pinyin."""
    return _convert(z, zhon.zhuyin.syl, zhuyin_syl_to_npinyin)


def zhuyin_to_apinyin(z):
    """Convert all Zhuyin syllables in a string to accented Pinyin."""
    return _convert(z, zhon.zhuyin.syl, zhuyin_syl_to_apinyin)


def zhuyin_to_ipa(z):
    """Convert all Zhuyin syllables in a string to IPA."""
    return _convert(z, zhon.zhuyin.syl, zhuyin_syl_to_ipa)


def apinyin_to_zhuyin(p):
    """Convert all accented Pinyin syllables in a string to Zhuyin."""
    return _convert(p, zhon.pinyin.syl, apinyin_syl_to_zhuyin, True, True)


def apinyin_to_npinyin(p):
    """Convert all accented Pinyin syllables in a string to numbered Pinyin."""
    return _convert(p, zhon.pinyin.syl, apinyin_syl_to_npinyin)


def apinyin_to_ipa(p):
    """Convert all accented Pinyin syllables in a string to IPA."""
    return _convert(p, zhon.pinyin.syl, apinyin_syl_to_ipa, True, True)


def to_pinyin(s, accented=True):
    """Convert a string to Pinyin."""
    return to_apinyin(s) if accented else to_npinyin(s)


def to_apinyin(s):
    """Convert a string to accented Pinyin."""
    i = identify(s)
    if i == ACCENTED_PINYIN:
        return s
    elif i == NUMBERED_PINYIN:
        return npinyin_to_apinyin(s)
    elif i == ZHUYIN:
        return zhuyin_to_apinyin(s)
    else:
        raise ValueError("String is not a valid Chinese transcription.")


def to_npinyin(s):
    """Convert a string to numbered Pinyin."""
    i = identify(s)
    if i == NUMBERED_PINYIN:
        return s
    elif i == ACCENTED_PINYIN:
        return apinyin_to_npinyin(s)
    elif i == ZHUYIN:
        return zhuyin_to_npinyin(s)
    else:
        raise ValueError("String is not a valid Chinese transcription.")


def to_zhuyin(s):
    """Convert a string to Zhuyin."""
    i = identify(s)
    if i == ZHUYIN:
        return s
    elif i == ACCENTED_PINYIN:
        return apinyin_to_zhuyin(s)
    elif i == NUMBERED_PINYIN:
        return npinyin_to_zhuyin(s)
    else:
        raise ValueError("String is not a valid Chinese transcription.")


def to_ipa(s):
    """Convert a string to IPA."""
    i = identify(s)
    if i == IPA:
        return s
    elif i == ACCENTED_PINYIN:
        return apinyin_to_ipa(s)
    elif i == NUMBERED_PINYIN:
        return npinyin_to_ipa(s)
    elif i == ZHUYIN:
        return zhuyin_to_ipa(s)
    else:
        raise ValueError("String is not a valid Chinese transcription.")


def _is_pattern_match(ptn, s):
    """Check if a re pattern expression matches an entire string."""
    m = re.match(ptn, s, re.I)
    return m.group() == s if m else False


def _is_pinyin(p, word_ptn):
    """Check if a string is valid Pinyin according to the given pattern."""
    ptn = ('(?:%(word)s|[ \t%(punctuation)s])+' %
           {'word': word_ptn, 'punctuation': zhon.pinyin.punctuation,
            })
    return _is_pattern_match(ptn, p)


def is_pinyin(p):
    """Check if a given string consists of valid Pinyin."""
    return _is_pinyin(p, zhon.pinyin.word)


def is_apinyin(p):
    """Check if a given string consists of valid accented Pinyin."""
    return _is_pinyin(p, zhon.pinyin.accented_word)


def is_npinyin(n):
    """Check if a given string consists of valid numbered Pinyin."""
    return _is_pinyin(n, zhon.pinyin.numbered_word)


def is_zhuyin(z):
    """Check if a given string consists of valid Zhuyin."""
    ptn = '(?:%(syl)s|\s)+' % {'syl': zhon.zhuyin.syl}
    return _is_pattern_match(ptn, z)


def is_ipa(i):
    """Check if a given string consists of valid Chinese IPA."""
    ptn = ('(?:[%(characters)s]+[%(marks)s]*|[ \t%(punctuation)s])+' %
           {'characters': _IPA_CHARACTERS, 'marks': _IPA_MARKS,
            'punctuation': zhon.pinyin.punctuation})
    return _is_pattern_match(ptn, i)


def identify(s):
    """Identify a given string's transcription system.

    *s* is the string to identify. The string is checked to see if its
    contents are valid accented Pinyin, numbered Pinyin, or Zhuyin. The
    :data:`ACCENTED_PINYIN`, :data:`NUMBERED_PINYIN`, :data:`ZHUYIN`, and
    :data:`IPA` constants are returned to indicate the string's identity.
    If *s* is not a valid transcription system, then :data:`UNKNOWN` is
    returned.

    """
    if is_apinyin(s):
        return ACCENTED_PINYIN
    elif is_npinyin(s):
        return NUMBERED_PINYIN
    elif is_zhuyin(s):
        return ZHUYIN
    elif is_ipa(s):
        return IPA
    else:
        return UNKNOWN
