# -*- coding: utf-8 -*-
"""Unit tests for dragonmapper.hanzi."""

import unittest

from dragonmapper import hanzi


class TestConversionFunctions(unittest.TestCase):
    chinese = "愛喜歡愛。"
    chinese_segmented = "愛 喜歡 愛。"
    apinyin = "àixǐhuan'ài。"
    apinyin_readings = "[ài][xǐ/xī/chì][huan/huān][ài]。"
    apinyin_segmented = "ài xǐhuan ài。"
    apinyin_segmented_readings = "[ài] [xǐhuan] [ài]。"
    npinyin = "ai4xi3huan5'ai4。"
    npinyin_readings = "[ai4][xi3/xi1/chi4][huan5/huan1][ai4]。"
    npinyin_segmented = "ai4 xi3huan5 ai4。"
    npinyin_segmented_readings = "[ai4] [xi3huan5] [ai4]。"
    ipa = "aɪ˥˩ ɕi˧˩˧ xwan aɪ˥˩。"
    zhuyin = "ㄞˋ ㄒㄧˇ ㄏㄨㄢ˙ ㄞˋ。"

    def test_accented_pinyin(self):
        self.assertEqual(hanzi.to_pinyin(self.chinese), self.apinyin)
        self.assertEqual(
            hanzi.to_pinyin(self.chinese, all_readings=True), self.apinyin_readings
        )
        self.assertEqual(
            hanzi.to_pinyin(self.chinese_segmented), self.apinyin_segmented
        )
        self.assertEqual(
            hanzi.to_pinyin(self.chinese_segmented, all_readings=True),
            self.apinyin_segmented_readings,
        )

    def test_numbered_pinyin(self):
        self.assertEqual(hanzi.to_pinyin(self.chinese, accented=False), self.npinyin)
        self.assertEqual(
            hanzi.to_pinyin(self.chinese, all_readings=True, accented=False),
            self.npinyin_readings,
        )
        self.assertEqual(
            hanzi.to_pinyin(self.chinese_segmented, accented=False),
            self.npinyin_segmented,
        )
        self.assertEqual(
            hanzi.to_pinyin(self.chinese_segmented, all_readings=True, accented=False),
            self.npinyin_segmented_readings,
        )

    def test_word_readings(self):
        self.assertEqual(hanzi.to_pinyin("便宜"), "piànyi")
        self.assertEqual(hanzi.to_pinyin("便宜", all_readings=True), "[piànyi/biànyí]")

    def test_custom_container(self):
        apinyin = self.apinyin_readings.replace("[", "(").replace("]", ")")
        self.assertEqual(
            hanzi.to_pinyin(self.chinese, all_readings=True, container="()"), apinyin
        )

    def test_issue_7(self):
        reading = hanzi.to_pinyin("手")
        self.assertEqual("shǒu", reading)
        reading = hanzi.to_pinyin("收")
        self.assertEqual("shōu", reading)

    def test_issue_10(self):
        """Incorrect readings for 女."""
        reading = hanzi.to_pinyin("女")
        self.assertEqual("nǚ", reading)
