# -*- coding: utf-8 -*-
"""Formatting Chinese into HTML with dragonmapper's functions"""


from __future__ import unicode_literals
from dragonmapper import hanzi
from dragonmapper import transcriptions as trans
import zhon
from zhon import pinyin
from zhon import zhuyin


"""See recomended CSS style: DRAGONMAPPER_DIR/style.css"""

TOP_LEFT = 0
TOP_MID = 1
TOP_RIGHT = 2
MID_LEFT = 3
MID_MID = 4
MID_RIGHT = 5
LOW_LEFT = 6
LOW_MID = 7
LOW_RIGHT = 8

TOP = TOP_MID
LEFT = MID_LEFT
CENTER = MID_MID
RIGHT = MID_RIGHT
BOTTOM = LOW_MID

PUT_TEXT_PLACES = (TOP, LEFT, CENTER, RIGHT, BOTTOM)

TOP_PLACES = (TOP_LEFT, TOP_MID, TOP_RIGHT)
LEFT_PLACES = (TOP_LEFT, MID_LEFT, LOW_LEFT)
RIGHT_PLACES = (TOP_RIGHT, MID_RIGHT, LOW_RIGHT)
BOTTOM_PLACES = (LOW_LEFT, LOW_MID, LOW_RIGHT)

STACKED_PLACES = (LEFT, RIGHT)


_indentation = 0
_line_html = ''
_puctuation = tuple(zhon.hanzi.punctuation + zhon.pinyin.punctuation)
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
    elif s in _puctuation:
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


def _is_phonetic_script(s):

    """
    Returns bool if s is any phonetic script.

    *s* string to preform test on
    """

    i_s = _identify(s)
    if i_s == "pinyin" or i_s == "zhuyin" or i_s == "ipa":
        return True
    return False


def _stackify(s):

    """
    Stack string for HTML formatting on the left and right of characters.

    *s* is the string to "stackify".
    """

    return "<br />".join(list(s))


def _html_add(s, tabs=0):

    """
    Wrapper for _line_html+="..."

    *s* is what to add to the html string.
    *tabs* specifies the identation intensity (in tabs).
    """

    global _line_html
    _line_html += (("\n")+("\t"*(tabs+_indentation)))+s


def _split_punct(s):

    """
    Internal function for spliting by punctuation only for HTML formatting.

    *s* specifies the list to preform this action on.
    """

    temp = []

    s = s.split(' ')

    for c in s:
        full_char_temp = ""
        for pc in c:
            if (pc in zhuyin.characters or
                    pc in pinyin.vowels or
                    pc in pinyin.consonants or
                    pc in _tones_marks):
                full_char_temp += pc
            elif pc in _puctuation:
                if full_char_temp != "":
                    temp.append(full_char_temp)
                    full_char_temp = ""
                temp.append("")
        if full_char_temp != "":
            temp.append(full_char_temp)
    return temp


def _return_correct_side(x, y, t, l, c, r, b):

    """
    Returns what side is being referenced by the coordinates, and the ...
    ... coresponding list.

    *x, y* are the coordinates
    *t, l, c, r, b* are top, left, center, right, and bottom, respectively.
    """

    if x == 0 and y == 0:
        return ([], TOP_LEFT)
    elif x == 1 and y == 0:
        return (t, TOP)
    elif x == 2 and y == 0:
        return ([], TOP_RIGHT)
    elif x == 0 and y == 1:
        return (l, LEFT)
    elif x == 1 and y == 1:
        return (c, CENTER)
    elif x == 2 and y == 1:
        return (r, RIGHT)
    elif x == 0 and y == 2:
        return ([], LOW_LEFT)
    elif x == 1 and y == 2:
        return (b, BOTTOM)
    elif x == 2 and y == 2:
        return ([], LOW_RIGHT)


def _fix_empty_arrays(a, length):

    """
    Returns array of length 'length' if it does not contain anything ...
    ... otherwise returns _split_punct(a)

    *a* is the array to proform the action on
    *length* is the length
    """

    if a is None:
        a = [""] * length
    elif len(a) > length:
        a = _split_punct(a)
    return a


def to_html(characters,
            bottom=None,
            right=None,
            left=None,
            top=None,
            minified=False,
            indentation=0):

    """
    Returns valid HTML for the Chinese characters, and (assumed) phonetic ...
     ... notations provided, on any given side.

    *characters* will be displayed in the middle of each output table.
    *bottom/right/left/bottom* will be displayed on their respective sides ...
     ... of the character. Strings from dragonmapper.transcriptions, ...
     ... dragonmapper.hanzi.to_xxxyin, or an array/tuple are acceptable.
    *indentation* specifies how many extra tab spaces there should be.
    """

    global _indentation
    global _line_html
    _indentation = indentation
    _line_html = ""
    proper_length = len(characters)

    _html_add("<table class=\"chinese-line\">")
    _html_add("<tbody>", 1)

    top = _fix_empty_arrays(top, proper_length)
    left = _fix_empty_arrays(left, proper_length)
    right = _fix_empty_arrays(right, proper_length)
    bottom = _fix_empty_arrays(bottom, proper_length)

    for y in range(0, 3):
        _html_add("<tr>", 2)
        char_num = 0
        for i in range(0, (len(characters)*3)):
            x = i % 3
            text = ""
            text_type = "unknown"

            current_side, side = _return_correct_side(
                x, y, top, left, characters, right, bottom)

            if side in PUT_TEXT_PLACES:
                text_type = _identify(current_side[char_num])
                if side in STACKED_PLACES:
                    text = _stackify(current_side[char_num])
                else:
                    text = current_side[char_num]

            if text is not "":
                if _is_phonetic_script(text):
                    _html_add(
                        "<td class=\"{0} {1} {2}\">".format(
                            text_type,
                            characters[char_num],
                            'phonetic-script'),
                        3)
                else:
                    _html_add(
                        "<td class=\"{0} {1}\">".format(
                            text_type, characters[char_num]),
                        3)
            # If the text is blank
            else:
                _html_add(
                    "<td class=\"{0}\">".format(
                        text_type),
                    3)

            if side in RIGHT_PLACES:
                char_num += 1

            _html_add("<span>{0}</span>".format(text), 4)
            _html_add("</td>", 3)

        _html_add("</tr>", 2)
    _html_add("</tbody>", 1)
    _html_add("</table>")

    if minified:
        return _line_html.replace('\t', '').replace('\n', '')
    return _line_html

if __name__ == '__main__':
    zi = '你好，我叫顏毅。我是加拿大人！'
    zh = hanzi.to_zhuyin(zi)
    pi = trans.zhuyin_to_pinyin(hanzi.to_zhuyin(zi))
    print(to_html(zi, bottom=pi, right=zh))
