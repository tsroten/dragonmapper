# -*- coding: utf-8 -*-
"""Unit tests for dragonmapper.transcriptions."""

from __future__ import unicode_literals
import unittest

from dragonmapper import transcriptions as trans


class TestIdentifyFunctions(unittest.TestCase):

    npinyin = 'fa1zhan3 ni3hao3'
    apinyin = 'fāzhǎnnǐhǎo'
    zhuyin = 'ㄝ ㄦ ㄒㄧㄣ'
    ipa = 'fa˥ ʈʂan˧˩˧ ni˧˩˧ xɑʊ˧˩˧'
    unknown = 'blahblah'

    def test_identify(self):
        self.assertEqual(trans.identify(self.npinyin), trans.PINYIN)
        self.assertEqual(trans.identify(self.apinyin), trans.PINYIN)
        self.assertEqual(trans.identify(self.zhuyin), trans.ZHUYIN)
        self.assertEqual(trans.identify(self.ipa), trans.IPA)
        self.assertEqual(trans.identify(self.unknown), trans.UNKNOWN)

    def test_is_pinyin(self):
        self.assertTrue(trans.is_pinyin(self.npinyin))
        self.assertTrue(trans.is_pinyin(self.apinyin))
        self.assertFalse(trans.is_pinyin(self.zhuyin))
        self.assertFalse(trans.is_pinyin(self.ipa))
        self.assertFalse(trans.is_pinyin(self.unknown))

    def test_is_zhuyin(self):
        self.assertTrue(trans.is_zhuyin(self.zhuyin))
        self.assertFalse(trans.is_zhuyin(self.npinyin))
        self.assertFalse(trans.is_zhuyin(self.apinyin))
        self.assertFalse(trans.is_zhuyin(self.ipa))
        self.assertFalse(trans.is_zhuyin(self.unknown))

    def test_is_ipa(self):
        self.assertTrue(trans.is_ipa(self.ipa))
        self.assertFalse(trans.is_ipa(self.npinyin))
        self.assertFalse(trans.is_ipa(self.apinyin))
        self.assertFalse(trans.is_ipa(self.zhuyin))
        self.assertFalse(trans.is_ipa(self.unknown))


class TestConvertFunctions(unittest.TestCase):

    npinyin = 'Wo3 shi4 yi1ge4 mei3guo2ren2.'
    apinyin = 'Wǒ shì yīgè měiguórén.'
    npinyin_spaced = 'Wo3 shi4 yi1 ge4 mei3 guo2 ren2.'
    apinyin_spaced = 'Wǒ shì yī gè měi guó rén.'
    zhuyin = 'ㄨㄛˇ ㄕˋ ㄧ ㄍㄜˋ ㄇㄟˇ ㄍㄨㄛˊ ㄖㄣˊ.'
    ipa = 'wɔ˧˩˧ ʂɨ˥˩ i˥ kɤ˥˩ meɪ˧˩˧ kwɔ˧˥ ʐən˧˥.'

    def test_numbered_to_accented(self):
        self.assertEqual(trans.npinyin_to_apinyin(self.npinyin), self.apinyin)

    def test_accented_to_numbered(self):
        self.assertEqual(trans.apinyin_to_npinyin(self.apinyin), self.npinyin)

    def test_pinyin_to_zhuyin(self):
        self.assertEqual(trans.pinyin_to_zhuyin(self.apinyin), self.zhuyin)
        self.assertEqual(trans.pinyin_to_zhuyin(self.npinyin), self.zhuyin)

    def test_pinyin_to_ipa(self):
        self.assertEqual(trans.pinyin_to_ipa(self.apinyin), self.ipa)
        self.assertEqual(trans.pinyin_to_ipa(self.npinyin), self.ipa)

    def test_zhuyin_to_pinyin(self):
        self.assertEqual(trans.zhuyin_to_pinyin(self.zhuyin),
                         self.apinyin_spaced.lower())
        self.assertEqual(trans.zhuyin_to_pinyin(self.zhuyin, accented=False),
                         self.npinyin_spaced.lower())

    def test_zhuyin_to_ipa(self):
        self.assertEqual(trans.zhuyin_to_ipa(self.zhuyin), self.ipa)

    def test_ipa_to_pinyin(self):
        self.assertEqual(trans.ipa_to_pinyin(self.ipa),
                         self.apinyin_spaced.lower())
        self.assertEqual(trans.ipa_to_pinyin(self.ipa, accented=False),
                         self.npinyin_spaced.lower())

    def test_ipa_to_zhuyin(self):
        self.assertEqual(trans.ipa_to_zhuyin(self.ipa), self.zhuyin)

    def test_pinyin_middle_dot(self):
        self.assertEqual(trans.apinyin_to_npinyin('\u00B7zi'), 'zi5')

    def test_pinyin_r_suffix(self):
        self.assertEqual(trans.npinyin_to_apinyin('hua1r5'), 'hu\u0101r')
        self.assertEqual(trans.apinyin_to_npinyin('hu\u0101r'), 'hua1r5')

    def test_drop_apostrophe(self):
        self.assertEqual(trans.pinyin_to_zhuyin("xi1'an1"), 'ㄒㄧ ㄢ')
        self.assertEqual(trans.pinyin_to_ipa("xi1'an1"), 'ɕi˥ an˥')
        self.assertEqual(trans.npinyin_to_apinyin("xi1'an1"), "xī'ān")
        self.assertEqual(trans.pinyin_to_zhuyin("xī'ān"), 'ㄒㄧ ㄢ')
        self.assertEqual(trans.pinyin_to_ipa("xī'ān"), 'ɕi˥ an˥')
        self.assertEqual(trans.apinyin_to_npinyin("xī'ān"), "xi1'an1")

    def test_handle_middle_dot(self):
        self.assertEqual(trans.apinyin_to_npinyin('ān\u00B7jing'), 'an1jing5')
