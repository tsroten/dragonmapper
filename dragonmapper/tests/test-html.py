# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import codecs
import unittest
from dragonmapper import html


"""Unit tests for dragonmapper.html."""


class TestHtmlFuctions(unittest.TestCase):

    def fix_line(s):
        """
        Returns string without useless characters

        *s* is line from file
        """
        return s.replace("\\n", "\n").replace("\\t", "\t").rstrip('\n')


    maxDiff = None

    f = codecs.open("dragonmapper/data/test-html-data.txt", 'r', 'utf8')

    s = '我叫顏毅'
    zh = 'ㄨㄛˇ ㄐㄧㄠˋ ㄧㄢˊ ㄧˋ'
    pi = 'wǒ jiào yán yì'
    jp = 'ngo5 giu3 ngaan4 ngai6'

    s2 = '你好，我媽媽對我叫：“顏毅”。'
    zh2 = 'ㄋㄧˇ ㄏㄠˇ，ㄨㄛˇ ㄇㄚ ㄇㄚ ㄉㄨㄟˋ ㄨㄛˇ ㄐㄧㄠˋ：“ㄧㄢˊ ㄧˋ”'
    pi2 = 'nǐ hǎo，wǒ mā mā duì wǒ jiào：“yán yì”'
    jp2 = 'nei5 hou2，ngo5 ma1 ma1 deoi3 ngo5 giu3：“ngaan4 ngai6”。'
    zh2_man = ['', '', '', '', '', '', '', '', '', '', '', 'yan2', 'yi4', '', '']

    zh3 = "ㄨㄛˇ ㄉㄨㄟˋ ㄊㄚ ㄕㄨㄛ：“ㄋㄧˇ ㄇㄚ ㄇㄚ ㄉㄨㄟˋ ㄋㄧˇ ㄕㄨㄛ：“ㄋㄧˇ " +\
        "ㄅㄚˋ ㄅㄚˋ ㄉㄨㄟˋ ㄋㄧˇ ㄕㄨㄛ：“ㄋㄧˇ ㄏㄠˇ ㄋㄩˇ ㄦ˙”””"

    indented_5 = fix_line(f.readline())
    indented_0 = fix_line(f.readline())
    indented_3 = fix_line(f.readline())
    zhuyin_both_pinyin_both = fix_line(f.readline())
    pinyin_top = fix_line(f.readline())
    zhuyin_top = fix_line(f.readline())
    pinyin_bottom = fix_line(f.readline())
    manual_pinyin = fix_line(f.readline())
    jyutping_html = fix_line(f.readline())

    def test_indented_5(self):
        self.assertEqual(
            html.to_html(
                self.s, bottom=self.pi,
                left=self.zh, indentation=5),
            self.indented_5)

    def test_indented_0(self):
        self.assertEqual(
            html.to_html(
                self.s, bottom=self.pi,
                right=self.zh, indentation=0),
            self.indented_0)

    def test_indented_3(self):
        self.assertEqual(
            html.to_html(
                self.s, bottom=self.pi,
                top=self.zh, indentation=3),
            self.indented_3)

    def test_zhuyin_both_pinyin_both(self):
        self.assertEqual(
            html.to_html(
                self.s, bottom=self.pi,
                top=self.pi, left=self.zh,
                right=self.zh),
            self.zhuyin_both_pinyin_both)

    def test_pinyin_top(self):
        self.assertEqual(html.to_html(self.s, top=self.pi), self.pinyin_top)

    def test_zhuyin_top(self):
        self.assertEqual(html.to_html(self.s, top=self.zh), self.zhuyin_top)

    def test_pinyin_bottom(self):
        self.assertEqual(
            html.to_html(
                self.s, bottom=self.pi),
            self.pinyin_bottom)

    def test_identify(self):
        self.assertEqual(html._identify("，"), 'punct')
        self.assertEqual(html._identify("你好嗎？"), 'hanzi')
        self.assertEqual(html._identify("wǒ mā mā"), 'pinyin')
        self.assertEqual(html._identify("ㄨㄛˇ ㄐㄧㄠˋ ㄧㄢˊ ㄧˋ"), 'zhuyin')
        self.assertEqual(html._identify("1"), 'tone-mark')
        self.assertEqual(html._identify("ˋ"), 'tone-mark')
        self.assertEqual(html._identify("："), 'punct')

    def test_stackify(self):
        self.assertEqual(html._stackify("ni3"), "n<br />i<br />3")
        self.assertEqual(html._stackify("ㄨㄛˇ"), "ㄨ<br />ㄛ<br />ˇ")
        self.assertEqual(html._stackify("小狗"), "小<br />狗")
        self.assertEqual(
            html._stackify("phantom"),
            "p<br />h<br />a<br />n<br />t<br />o<br />m")
        self.assertEqual(
            html._stackify("gxF52f"),
            "g<br />x<br />F<br />5<br />2<br />f")

    def test_split_punct(self):
        self.assertEqual(
            html._split_punct("ni3 hao3 ma5？"),
            ['ni3', 'hao3', 'ma5', ''])
        self.assertEqual(
            html._split_punct("ㄨㄛˇ：ㄇㄚ ㄇㄚ"),
            ['ㄨㄛˇ', '', 'ㄇㄚ', 'ㄇㄚ'])
        self.assertEqual(
            html._split_punct("wo3 jiao4：“yan2 yi4”"),
            ['wo3', 'jiao4', '', '', 'yan2', 'yi4', ''])
        self.assertEqual(
            html._split_punct("ni3 shi4：wo3 de5 peng2 you5 ma5？"),
            ['ni3', 'shi4', '', 'wo3', 'de5', 'peng2', 'you5', 'ma5', ''])
        self.assertEqual(
            html._split_punct(
                self.zh3),
            ['ㄨㄛˇ', 'ㄉㄨㄟˋ', 'ㄊㄚ', 'ㄕㄨㄛ', '', '', 'ㄋㄧˇ', 'ㄇㄚ', 'ㄇㄚ',
                'ㄉㄨㄟˋ', 'ㄋㄧˇ', 'ㄕㄨㄛ', '', '', 'ㄋㄧˇ', 'ㄅㄚˋ', 'ㄅㄚˋ',
                'ㄉㄨㄟˋ', 'ㄋㄧˇ', 'ㄕㄨㄛ', '', '', 'ㄋㄧˇ', 'ㄏㄠˇ', 'ㄋㄩˇ',
                'ㄦ˙', '', '', ''])

    def test_manual_phonetics_input(self):
        self.assertEqual(
            html.to_html(
                self.s2, bottom=self.zh2_man),
            self.manual_pinyin)

    def test_return_correct_sid(self):
        self.assertEqual(
            html._return_correct_side(
                2, 0, [], [], [], [], []
            ),
            ([], html.TOP_RIGHT)
        )
        self.assertEqual(
            html._return_correct_side(
                2, 2, [], [], [], [], []
            ),
            ([], html.LOW_RIGHT)
        )
        self.assertEqual(
            html._return_correct_side(
                1, 2, [], [], [], [], []
            ),
            ([], html.BOTTOM)
        )

    def test_fix_empty_arrays(self):
        self.assertEqual(
            html._fix_empty_arrays(
                None, 6
            ),
            [""] * 6
        )

    def test_jyutping_in_html(self):
        self.assertEqual(
            html.to_html(
                self.s2, top=self.jp2),
            self.jyutping_html)
