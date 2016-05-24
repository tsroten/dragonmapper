# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import codecs
import unittest
from dragonmapper import html


"""Unit tests for dragonmapper.html."""


class TestHtmlFuctions(unittest.TestCase):

    f = codecs.open("dragonmapper/data/test-html-data.txt", 'r', 'utf8')

    s = '我叫顏毅'
    zh = ['ㄨㄛˇ', 'ㄐㄧㄠˋ', 'ㄧㄢˊ', 'ㄧˋ']
    pi = ['wǒ', 'jiào', 'yán', 'yì']

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
