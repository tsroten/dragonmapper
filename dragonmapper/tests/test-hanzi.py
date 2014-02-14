# -*- coding: utf-8 -*-
"""Unit tests for dragonmapper.hanzi."""

from __future__ import unicode_literals
import unittest

from dragonmapper import hanzi


class TestIdentifyFunctions(unittest.TestCase):

    traditional = '神稱旱地為地，稱水的聚處為海。神看著是好的。'
    simplified = '神称旱地为地，称水的聚处为海。神看着是好的。'
    both = '你好！'
    mixed = '車车'
    none = 'Hello. There are no Chinese characters in this string.'

    def test_identify(self):
        self.assertEqual(hanzi.identify(self.traditional), hanzi.TRADITIONAL)
        self.assertEqual(hanzi.identify(self.simplified), hanzi.SIMPLIFIED)
        self.assertEqual(hanzi.identify(self.both), hanzi.BOTH)
        self.assertEqual(hanzi.identify(self.mixed), hanzi.MIXED)
        self.assertEqual(hanzi.identify(self.none), hanzi.NONE)

    def test_is_chinese(self):
        self.assertTrue(hanzi.is_chinese(self.traditional))
        self.assertTrue(hanzi.is_chinese(self.both))
        self.assertTrue(hanzi.is_chinese(self.simplified))
        self.assertTrue(hanzi.is_chinese(self.mixed))
        self.assertFalse(hanzi.is_chinese(self.none))

    def test_is_traditional(self):
        self.assertTrue(hanzi.is_traditional(self.traditional))
        self.assertTrue(hanzi.is_traditional(self.both))
        self.assertFalse(hanzi.is_traditional(self.simplified))
        self.assertFalse(hanzi.is_traditional(self.mixed))
        self.assertFalse(hanzi.is_traditional(self.none))

    def test_is_simplified(self):
        self.assertTrue(hanzi.is_simplified(self.simplified))
        self.assertTrue(hanzi.is_simplified(self.both))
        self.assertFalse(hanzi.is_simplified(self.traditional))
        self.assertFalse(hanzi.is_simplified(self.mixed))
        self.assertFalse(hanzi.is_simplified(self.none))


class TestConversionFunctions(unittest.TestCase):

    chinese = '愛喜歡愛。'
    chinese_segmented = '愛 喜歡 愛。'
    apinyin = "àixǐhuan'ài。"
    apinyin_readings = '[ài][xǐ/xī/chì][huan/huān][ài]。'
    apinyin_segmented = 'ài xǐhuan ài。'
    apinyin_segmented_readings = '[ài] xǐhuan [ài]。'
    npinyin = "ai4xi3huan5'ai4。"
    npinyin_readings = '[ai4][xi3/xi1/chi4][huan5/huan1][ai4]。'
    npinyin_segmented = 'ai4 xi3huan5 ai4。'
    npinyin_segmented_readings = '[ai4] xi3huan5 [ai4]。'
    ipa = 'aɪ˥˩ ɕi˧˩˧ xwan aɪ˥˩。'
    zhuyin = 'ㄞˋ ㄒㄧˇ ㄏㄨㄢ˙ ㄞˋ。'

    def test_accented_pinyin(self):
        self.assertEqual(hanzi.to_pinyin(self.chinese), self.apinyin)
        self.assertEqual(hanzi.to_pinyin(self.chinese, all_readings=True),
                         self.apinyin_readings)
        self.assertEqual(hanzi.to_pinyin(self.chinese_segmented),
                         self.apinyin_segmented)
        self.assertEqual(hanzi.to_pinyin(self.chinese_segmented,
                                         all_readings=True),
                         self.apinyin_segmented_readings)

    def test_numbered_pinyin(self):
        self.assertEqual(hanzi.to_pinyin(self.chinese, False), self.npinyin)
        self.assertEqual(hanzi.to_pinyin(self.chinese, False,
                                         all_readings=True),
                         self.npinyin_readings)
        self.assertEqual(hanzi.to_pinyin(self.chinese_segmented, False),
                         self.npinyin_segmented)
        self.assertEqual(hanzi.to_pinyin(self.chinese_segmented, False,
                                         all_readings=True),
                         self.npinyin_segmented_readings)

    def test_word_readings(self):
        self.assertEqual(hanzi.to_pinyin('便宜'), 'biànyí')
        self.assertEqual(hanzi.to_pinyin('便宜', all_readings=True),
                         'biànyí/piànyi')
