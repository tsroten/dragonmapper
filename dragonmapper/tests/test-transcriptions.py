# -*- coding: utf-8 -*-
"""Unit tests for dragonmapper.transcriptions."""

from __future__ import unicode_literals
import unittest

from dragonmapper import transcriptions as trans


class TestIdentifyFunctions(unittest.TestCase):

    npinyin = 'fa1zhan3 ni3hao3'
    apinyin = 'fāzhǎnnǐhǎo'
    zhuyin = 'ㄝ ㄦ ㄒㄧㄣ'
    unknown = 'blahblah'

    def test_identify(self):
        self.assertEqual(trans.identify(self.npinyin), trans.NPINYIN)
        self.assertEqual(trans.identify(self.apinyin), trans.APINYIN)
        self.assertEqual(trans.identify(self.zhuyin), trans.ZHUYIN)
        self.assertEqual(trans.identify(self.unknown), trans.UNKNOWN)

    def test_is_pinyin(self):
        self.assertTrue(trans.is_pinyin(self.npinyin))
        self.assertTrue(trans.is_pinyin(self.apinyin))
        self.assertFalse(trans.is_pinyin(self.zhuyin))
        self.assertFalse(trans.is_pinyin(self.unknown))

    def test_is_npinyin(self):
        self.assertTrue(trans.is_npinyin(self.npinyin))
        self.assertFalse(trans.is_npinyin(self.apinyin))
        self.assertFalse(trans.is_npinyin(self.zhuyin))
        self.assertFalse(trans.is_npinyin(self.unknown))

    def test_is_apinyin(self):
        self.assertTrue(trans.is_apinyin(self.apinyin))
        self.assertFalse(trans.is_apinyin(self.npinyin))
        self.assertFalse(trans.is_apinyin(self.zhuyin))
        self.assertFalse(trans.is_apinyin(self.unknown))

    def test_is_zhuyin(self):
        self.assertTrue(trans.is_zhuyin(self.zhuyin))
        self.assertFalse(trans.is_zhuyin(self.npinyin))
        self.assertFalse(trans.is_zhuyin(self.apinyin))
        self.assertFalse(trans.is_zhuyin(self.unknown))


class TestConvertFunctions(unittest.TestCase):

    npinyin = 'Wo3 shi4 yi1ge4 mei3guo2ren2.'
    apinyin = 'Wǒ shì yīgè měiguórén.'
    npinyin_spaced = 'Wo3 shi4 yi1 ge4 mei3 guo2 ren2.'
    apinyin_spaced = 'Wǒ shì yī gè měi guó rén.'
    zhuyin = 'ㄨㄛˇ ㄕˋ ㄧ ㄍㄜˋ ㄇㄟˇ ㄍㄨㄛˊ ㄖㄣˊ.'
    ipa = 'wɔ˧˩˧ ʂɨ˥˩ i˥ kɤ˥˩ meɪ˧˩˧ kwɔ˧˥ ʐən˧˥.'

    def test_numbered_to_pinyin(self):
        self.assertEqual(trans.npinyin_to_apinyin(self.npinyin), self.apinyin)

    def test_numbered_to_zhuyin(self):
        self.assertEqual(trans.npinyin_to_zhuyin(self.npinyin), self.zhuyin)

    def test_numbered_to_ipa(self):
        self.assertEqual(trans.npinyin_to_ipa(self.npinyin), self.ipa)

    def test_zhuyin_to_numbered(self):
        self.assertEqual(trans.zhuyin_to_npinyin(self.zhuyin),
                         self.npinyin_spaced.lower())

    def test_zhuyin_to_pinyin(self):
        self.assertEqual(trans.zhuyin_to_apinyin(self.zhuyin),
                         self.apinyin_spaced.lower())

    def test_zhuyin_to_ipa(self):
        self.assertEqual(trans.zhuyin_to_ipa(self.zhuyin), self.ipa)

    def test_pinyin_to_zhuyin(self):
        self.assertEqual(trans.apinyin_to_zhuyin(self.apinyin), self.zhuyin)

    def test_pinyin_to_numbered(self):
        self.assertEqual(trans.apinyin_to_npinyin(self.apinyin), self.npinyin)

    def test_pinyin_to_ipa(self):
        self.assertEqual(trans.apinyin_to_ipa(self.apinyin), self.ipa)

    def test_pinyin_middle_dot(self):
        self.assertEqual(trans.apinyin_to_npinyin('\u00B7zi'), 'zi5')

    def test_pinyin_r_suffix(self):
        self.assertEqual(trans.npinyin_to_apinyin('hua1r5'), 'hu\u0101r')
        self.assertEqual(trans.apinyin_to_npinyin('hu\u0101r'), 'hua1r5')

    def test_drop_apostrophe(self):
        self.assertEqual(trans.npinyin_to_zhuyin("xi1'an1"), 'ㄒㄧ ㄢ')
        self.assertEqual(trans.npinyin_to_ipa("xi1'an1"), 'ɕi˥ an˥')
        self.assertEqual(trans.npinyin_to_apinyin("xi1'an1"), "xī'ān")
        self.assertEqual(trans.apinyin_to_zhuyin("xī'ān"), 'ㄒㄧ ㄢ')
        self.assertEqual(trans.apinyin_to_ipa("xī'ān"), 'ɕi˥ an˥')
        self.assertEqual(trans.apinyin_to_npinyin("xī'ān"), "xi1'an1")

    def test_handle_middle_dot(self):
        self.assertEqual(trans.apinyin_to_npinyin('ān\u00B7jing'), 'an1jing5')
