# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import codecs
import unittest
from dragonmapper import html


"""Unit tests for dragonmapper.html."""


class TestHtmlFuctions(unittest.TestCase):

    maxDiff = None

    zi = '你好'
    pinyin = ['ni3', 'hao3']
    ruby = '<ruby class="你好 chinese-word traditional-simplified-same">\
<rb class="你好 hanzi">你</rb>\
<rt class="你好 phonetic-script pinyin">ni3</rt>\
<rb class="你好 hanzi">好</rb>\
<rt class="你好 phonetic-script pinyin">hao3</rt></ruby>'


    def test_to_html(self):
        self.assertEqual(html.to_html(self.zi, top=self.pinyin, minified=True),
        self.ruby)
