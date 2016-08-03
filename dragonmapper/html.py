# -*- coding: utf-8 -*-
"""Formatting Chinese into HTML with dragonmapper's functions"""


from __future__ import unicode_literals
from dragonmapper import hanzi
from dragonmapper import transcriptions as trans
import zhon

"""See recomended CSS style: DRAGONMAPPER_DIR/style.css"""

CHINESE_TYPE_UNKNOWN = 0
CHINESE_TYPE_SIMPLIFIED = 1
CHINESE_TYPE_TRADITIONAL = 2
CHINESE_TYPE_SAME = 3

TYPE_TO_CSS_CLASS = {0: 'unknown',
                        1: 'simplified',
                        2: 'traditional',
                        3: 'traditional-simplified-same'}

_indentation = 0
_line_html = ''
punctuation = tuple(zhon.hanzi.punctuation + zhon.pinyin.punctuation)
_tones_marks = ['¯', 'ˊ', 'ˇ', 'ˋ', '˙', '1', '2', '3', '4', '5']


def _identify(s):

    """
    Returns string of text type for HTML/CSS.

    *s* is the string to identify.
    """

    if hanzi.has_chinese(s):
        return "hanzi"
    elif s == "":
        return "unknown"
    elif s in punctuation:
        return "punct"
    elif s in _tones_marks:
        return "tone-mark"
    else:
        c = trans.identify(s)
        if c == trans.ZHUYIN:
            return "zhuyin"
        elif c == trans.PINYIN:
            return "pinyin"
        elif c == trans.IPA:
            return "ipa"
        elif c == trans.UNKNOWN:
            return "unknown"


def _html_add(s, tabs=0):

    """
    Wrapper for _line_html+="..."

    *s* is what to add to the html string.
    *tabs* specifies the identation intensity (in tabs).
    """

    global _line_html
    _line_html += (("\n")+("\t"*(tabs+_indentation)))+s


def is_what_type_of_chinese(s):

    """
    Returns values for diffent kinds of Chinese, see CHINESE_TYPE_...

    *s* character string
    """

    if hanzi.is_traditional(s) and hanzi.is_simplified(s):
        return CHINESE_TYPE_SAME
    elif hanzi.is_traditional(s):
        return CHINESE_TYPE_TRADITIONAL
    elif hanzi.is_simplified(s):
        return CHINESE_TYPE_SIMPLIFIED
    return CHINESE_TYPE_UNKNOWN


def to_html(characters,
            top=None,
            minified=False,
            indentation=0):

    """
    Returns (probably) valid HTML(5) for the Chinese characters,
        and phonetic notations provided.

    *characters* is an string of the Chinese characters.
    *top* an array that will be displayed on top of the respective characters.
    TODO: Add support for more sides... Waiting on browser support.
    *indentation* specifies how many extra tabs there should be.
    """

    global _indentation
    global _line_html
    _indentation = indentation
    _line_html = ""

    phonetic_script_type = _identify("".join(top))

    char_type = TYPE_TO_CSS_CLASS[is_what_type_of_chinese(characters)]

    _html_add(
        "<ruby class=\"{0} chinese-word {1}\">".format(
            "".join(characters), char_type)
    )
    for i in range(len(characters)):
        _html_add("<rb class=\"{0} hanzi\">{1}</rb>\
<rt class=\"{0} phonetic-script {2}\">{3}</rt>".format(
            characters,
            characters[i],
            phonetic_script_type,
            top[i]
        ), 1)
    _html_add("</ruby>")

    if minified:
        return _line_html.replace('\t', '').replace('\n', '')
    return _line_html
