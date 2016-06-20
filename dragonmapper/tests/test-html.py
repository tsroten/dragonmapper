# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import codecs
import unittest
from dragonmapper import html


"""Unit tests for dragonmapper.html."""


class TestHtmlFuctions(unittest.TestCase):

    maxDiff = None

    f = codecs.open("dragonmapper/data/test-html-data.txt", 'r', 'utf8')

    s = '我叫顏毅'
    zh = 'ㄨㄛˇ ㄐㄧㄠˋ ㄧㄢˊ ㄧˋ'
    pi = 'wǒ jiào yán yì'

    s2 = '你好，我媽媽對我叫“顏毅”。'
    zh2 = 'ㄋㄧˇ ㄏㄠˇ，ㄨㄛˇ ㄇㄚ ㄇㄚ ㄉㄨㄟˋ ㄨㄛˇ ㄐㄧㄠˋ：“ㄧㄢˊ ㄧˋ”'
    pi2 = 'nǐ hǎo，wǒ mā mā duì wǒ jiào：“yán yì”'
    zh2_man = ['', '', '', '', '', '', '', '', '', '', 'yan2', 'yi4', '', '']

    zh3 = "ㄨㄛˇ ㄉㄨㄟˋ ㄊㄚ ㄕㄨㄛ：“ㄋㄧˇ ㄇㄚ ㄇㄚ ㄉㄨㄟˋ ㄋㄧˇ ㄕㄨㄛ：“ㄋㄧˇ " +\
        "ㄅㄚˋ ㄅㄚˋ ㄉㄨㄟˋ ㄋㄧˇ ㄕㄨㄛ：“ㄋㄧˇ ㄏㄠˇ ㄋㄩˇ ㄦ˙”””"

    indented_5 = f.readline()\
        .replace("\\n", "\n").replace("\\t", "\t").rstrip('\n')
    indented_0 = f.readline()\
        .replace("\\n", "\n").replace("\\t", "\t").rstrip('\n')
    indented_3 = f.readline()\
        .replace("\\n", "\n").replace("\\t", "\t").rstrip('\n')
    zhuyin_both_pinyin_both = f.readline()\
        .replace("\\n", "\n").replace("\\t", "\t").rstrip('\n')
    pinyin_top = f.readline()\
        .replace("\\n", "\n").replace("\\t", "\t").rstrip('\n')
    zhuyin_top = f.readline()\
        .replace("\\n", "\n").replace("\\t", "\t").rstrip('\n')
    pinyin_bottom = f.readline()\
        .replace("\\n", "\n").replace("\\t", "\t").rstrip('\n')
    manual_pinyin = f.readline()\
        .replace("\\n", "\n").replace("\\t", "\t").rstrip('\n')

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

    def test_is_phonetic_script(self):
        self.assertEqual(html._is_phonetic_script("ni3"), True)
        self.assertEqual(html._is_phonetic_script("老f22x9-\\"), False)
        self.assertEqual(html._is_phonetic_script("ni˧˩˧ xɑʊ˧˩˧"), True)
        self.assertEqual(html._is_phonetic_script("ㄨㄛˇ"), True)
