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


def _return_correct_side(x, y, t, l, c, r, b, bl, br, tl, tr):

    """
    Returns what side is being referenced by the coordinates, and the ...
    ... coresponding list.

    *x, y* are the coordinates
    *t, l, c, r, b* are top, left, center, right, and bottom, respectively.
    *bl, br, tl, and tr* are bottomleft, bottomright, topleft, and topright.
    """

    if x == 0 and y == 0:
        return (tl, TOP_LEFT)
    elif x == 1 and y == 0:
        return (t, TOP)
    elif x == 2 and y == 0:
        return (tr, TOP_RIGHT)
    elif x == 0 and y == 1:
        return (l, LEFT)
    elif x == 1 and y == 1:
        return (c, CENTER)
    elif x == 2 and y == 1:
        return (r, RIGHT)
    elif x == 0 and y == 2:
        return (bl, LOW_LEFT)
    elif x == 1 and y == 2:
        return (b, BOTTOM)
    elif x == 2 and y == 2:
        return (br, LOW_RIGHT)


def _get_side_string(s):
    """
    Returns side as string (for html-css referencing)

    s is int constant
    """

    result = ""
    if s == TOP_LEFT:
        result = "top-left"
    elif s == TOP_MID:
        result = "top-mid top"
    elif s == TOP_RIGHT:
        result = "top-right"
    elif s == MID_LEFT:
        result = "mid-left left"
    elif s == MID_MID:
        result = "mid-mid center"
    elif s == MID_RIGHT:
        result = "mid-right right"
    elif s == LOW_LEFT:
        result = "low-left"
    elif s == LOW_MID:
        result = "low-mid bottom"
    elif s == LOW_RIGHT:
        result = "low-right"
    return result


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
            bottom_left=None,
            bottom=None,
            bottom_right=None,
            right=None,
            left=None,
            top_left=None,
            top=None,
            top_right=None,
            minified=False,
            indentation=0):

    """
    Returns valid HTML for the Chinese characters, and (assumed) phonetic ...
     ... notations provided, on any given side.

    *characters* will be displayed in the middle of each output table.
    *bottom/right/left/bottom ...* will be displayed on their respective ...
     ... sides of the character. Strings from dragonmapper.transcriptions, ...
     ... dragonmapper.hanzi.to_xxxyin, or an array/tuple are acceptable.
    *indentation* specifies how many extra tab spaces there should be.
    """

    global _indentation
    global _line_html
    _indentation = indentation
    _line_html = ""
    proper_length = len(characters)

    char_type = 'unknown'
    if hanzi.is_traditional(characters) and hanzi.is_simplified(characters):
        char_type = 'traditional-simplified-same'
    elif hanzi.is_traditional(characters):
        char_type = 'traditional'
    elif hanzi.is_simplified(characters):
        char_type = 'simplified'

    _html_add(
        "<table class=\"chinese-word {0} {1}\">".format(
            "".join(characters), char_type)
    )
    _html_add("<tbody>", 1)

    top_left = _fix_empty_arrays(top_left, proper_length)
    top = _fix_empty_arrays(top, proper_length)
    top_right = _fix_empty_arrays(top_right, proper_length)
    left = _fix_empty_arrays(left, proper_length)
    right = _fix_empty_arrays(right, proper_length)
    bottom_left = _fix_empty_arrays(bottom_left, proper_length)
    bottom = _fix_empty_arrays(bottom, proper_length)
    bottom_right = _fix_empty_arrays(bottom_right, proper_length)

    for y in range(0, 3):
        _html_add("<tr>", 2)
        char_num = 0
        for i in range(0, (len(characters)*3)):
            x = i % 3
            text = ""
            text_type = "unknown"
            phonetic_script_string = ""

            current_side, side = _return_correct_side(
                x, y, top, left, characters, right, bottom,
                bottom_left, bottom_right, top_left, top_right
            )

            text_type = _identify(current_side[char_num])
            if side in STACKED_PLACES:
                text = _stackify(current_side[char_num])
            else:
                text = current_side[char_num]

            if _is_phonetic_script(text):
                phonetic_script_string = " phonetic-script"

            if text is "":
                _html_add(
                    "<td><span class=\"{0} empty\"></span></td>".format(
                        characters),
                    3)
            else:
                _html_add("<td>", 3)
                _html_add(
                    "<span class=\"{0}{1} {2} {3}\">{4}</span>".format(
                        characters,
                        phonetic_script_string,
                        text_type,
                        _get_side_string(side),
                        text),
                    4)
                _html_add("</td>", 3)

            if side in RIGHT_PLACES:
                char_num += 1
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
