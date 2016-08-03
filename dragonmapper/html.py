# -*- coding: utf-8 -*-
"""Formatting Chinese into HTML with dragonmapper's functions"""


from __future__ import unicode_literals
from dragonmapper import hanzi
from dragonmapper import transcriptions as trans
import zhon
from zhon import pinyin
from zhon import zhuyin


"""See recomended CSS style: DRAGONMAPPER_DIR/style.css"""

_indentation = 0
_line_html = ''

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

def to_html(characters,
            top=None,
            minified=False,
            indentation=0):

    """
    Returns valid HTML(5) for the Chinese characters,
        and phonetic notations provided.

    *characters* is an array of the Chinese characters.
    *top* is an array that will be displayed on top of the characters.
    TODO: Add support for more sides... Waiting on browser support.
    *indentation* specifies how many extra tabs there should be.
    """

    global _indentation
    global _line_html
    _indentation = indentation
    _line_html = ""
    proper_length = len(characters)

    phonetic_script_type = _identify(top)

    char_type = 'unknown'
    if hanzi.is_traditional(characters) and hanzi.is_simplified(characters):
        char_type = 'traditional-simplified-same'
    elif hanzi.is_traditional(characters):
        char_type = 'traditional'
    elif hanzi.is_simplified(characters):
        char_type = 'simplified'

    _html_add(
        "<ruby class=\"{0} chinese-word {1}\">".format(
            "".join(characters), char_type)
    )
    for i in range(len(characters)):
        _html_add("<rb class=\"{0} hanzi\">{1}</rb>\
                    <rt class=\"{0} phonetic-script {2}\">{3}</rt>".format(
                    characters, characters[i], top[i]), 1)
    _html_add("</ruby>")

    if minified:
        return _line_html.replace('\t', '').replace('\n', '')
    return _line_html
