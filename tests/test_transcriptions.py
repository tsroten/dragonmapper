# -*- coding: utf-8 -*-
"""Unit tests for dragonmapper.transcriptions."""

import unittest

from dragonmapper import transcriptions as trans


class TestIdentifyFunctions(unittest.TestCase):
    numbered_pinyin = "fa1zhan3 ni3hao3"
    accented_pinyin = "fāzhǎnnǐhǎo"
    zhuyin = "ㄝ ㄦ ㄒㄧㄣ"
    ipa = "fa˥ ʈʂan˧˩˧ ni˧˩˧ xɑʊ˧˩˧"
    unknown = "blahblah"

    def test_identify(self):
        self.assertEqual(trans.identify(self.numbered_pinyin), trans.PINYIN)
        self.assertEqual(trans.identify(self.accented_pinyin), trans.PINYIN)
        self.assertEqual(trans.identify(self.zhuyin), trans.ZHUYIN)
        self.assertEqual(trans.identify(self.ipa), trans.IPA)
        self.assertEqual(trans.identify(self.unknown), trans.UNKNOWN)

    def test_is_pinyin(self):
        self.assertTrue(trans.is_pinyin(self.numbered_pinyin))
        self.assertTrue(trans.is_pinyin(self.accented_pinyin))
        self.assertFalse(trans.is_pinyin(self.zhuyin))
        self.assertFalse(trans.is_pinyin(self.ipa))
        self.assertFalse(trans.is_pinyin(self.unknown))

    def test_is_zhuyin(self):
        self.assertTrue(trans.is_zhuyin(self.zhuyin))
        self.assertFalse(trans.is_zhuyin(self.numbered_pinyin))
        self.assertFalse(trans.is_zhuyin(self.accented_pinyin))
        self.assertFalse(trans.is_zhuyin(self.ipa))
        self.assertFalse(trans.is_zhuyin(self.unknown))

    def test_is_ipa(self):
        self.assertTrue(trans.is_ipa(self.ipa))
        self.assertFalse(trans.is_ipa(self.numbered_pinyin))
        self.assertFalse(trans.is_ipa(self.accented_pinyin))
        self.assertFalse(trans.is_ipa(self.zhuyin))
        self.assertFalse(trans.is_ipa(self.unknown))

    def test_is_pinyin_compatible(self):
        self.assertFalse(trans.is_pinyin_compatible(self.ipa))
        self.assertTrue(trans.is_pinyin_compatible(self.numbered_pinyin))
        self.assertTrue(trans.is_pinyin_compatible(self.accented_pinyin))
        self.assertFalse(trans.is_pinyin_compatible(self.zhuyin))
        self.assertTrue(trans.is_pinyin_compatible(self.unknown))

    def test_is_zhuyin_compatible(self):
        self.assertFalse(trans.is_zhuyin_compatible(self.ipa))
        self.assertFalse(trans.is_zhuyin_compatible(self.numbered_pinyin))
        self.assertFalse(trans.is_zhuyin_compatible(self.accented_pinyin))
        self.assertTrue(trans.is_zhuyin_compatible(self.zhuyin))
        self.assertFalse(trans.is_zhuyin_compatible(self.unknown))


class TestConvertFunctions(unittest.TestCase):
    numbered_pinyin = "Wo3 shi4 yi1ge4 mei3guo2ren2."
    accented_pinyin = "Wǒ shì yīgè měiguórén."
    numbered_pinyin_spaced = "Wo3 shi4 yi1 ge4 mei3 guo2 ren2."
    accented_pinyin_spaced = "Wǒ shì yī gè měi guó rén."
    zhuyin = "ㄨㄛˇ ㄕˋ ㄧ ㄍㄜˋ ㄇㄟˇ ㄍㄨㄛˊ ㄖㄣˊ."
    ipa = "wɔ˧˩˧ ʂɨ˥˩ i˥ kɤ˥˩ meɪ˧˩˧ kwɔ˧˥ ʐən˧˥."

    def test_numbered_to_accented(self):
        accented_pinyin = trans.to_pinyin(self.numbered_pinyin)
        self.assertEqual(accented_pinyin, self.accented_pinyin)

    def test_accented_to_numbered(self):
        numbered_pinyin = trans.to_pinyin(self.accented_pinyin, accented=False)
        self.assertEqual(numbered_pinyin, self.numbered_pinyin)

    def test_pinyin_to_zhuyin(self):
        self.assertEqual(trans.pinyin_to_zhuyin(self.accented_pinyin), self.zhuyin)
        self.assertEqual(trans.pinyin_to_zhuyin(self.numbered_pinyin), self.zhuyin)

    def test_pinyin_to_ipa(self):
        self.assertEqual(trans.pinyin_to_ipa(self.accented_pinyin), self.ipa)
        self.assertEqual(trans.pinyin_to_ipa(self.numbered_pinyin), self.ipa)

    def test_zhuyin_to_pinyin(self):
        self.assertEqual(
            trans.zhuyin_to_pinyin(self.zhuyin), self.accented_pinyin_spaced.lower()
        )
        self.assertEqual(
            trans.zhuyin_to_pinyin(self.zhuyin, accented=False),
            self.numbered_pinyin_spaced.lower(),
        )

    def test_zhuyin_to_ipa(self):
        self.assertEqual(trans.zhuyin_to_ipa(self.zhuyin), self.ipa)

    def test_ipa_to_pinyin(self):
        self.assertEqual(
            trans.ipa_to_pinyin(self.ipa), self.accented_pinyin_spaced.lower()
        )
        self.assertEqual(
            trans.ipa_to_pinyin(self.ipa, accented=False),
            self.numbered_pinyin_spaced.lower(),
        )

    def test_ipa_to_zhuyin(self):
        self.assertEqual(trans.ipa_to_zhuyin(self.ipa), self.zhuyin)

    def test_pinyin_middle_dot(self):
        self.assertEqual(trans.to_pinyin("\u00B7zi", accented=False), "zi5")

    def test_pinyin_r_suffix(self):
        self.assertEqual(trans.to_pinyin("hua1r5"), "hu\u0101r")
        self.assertEqual(trans.to_pinyin("hu\u0101r", accented=False), "hua1r5")

    def test_drop_apostrophe(self):
        self.assertEqual(trans.pinyin_to_zhuyin("xi1'an1"), "ㄒㄧ ㄢ")
        self.assertEqual(trans.pinyin_to_ipa("xi1'an1"), "ɕi˥ an˥")
        self.assertEqual(trans.to_pinyin("xi1'an1"), "xī'ān")
        self.assertEqual(trans.pinyin_to_zhuyin("xī'ān"), "ㄒㄧ ㄢ")
        self.assertEqual(trans.pinyin_to_ipa("xī'ān"), "ɕi˥ an˥")
        self.assertEqual(trans.to_pinyin("xī'ān", accented=False), "xi1'an1")

    def test_handle_middle_dot(self):
        self.assertEqual(trans.to_pinyin("ān\u00B7jing", accented=False), "an1jing5")

    def test_issue_2(self):
        accented = "Ān"
        numbered = "An1"
        self.assertEqual(numbered, trans.accented_syllable_to_numbered(accented))

    def test_issue_3(self):
        invalid_syllable = "zef"
        self.assertRaises(ValueError, trans.pinyin_syllable_to_zhuyin, invalid_syllable)
        self.assertRaises(ValueError, trans.pinyin_syllable_to_ipa, invalid_syllable)
        self.assertRaises(
            ValueError, trans._zhuyin_syllable_to_numbered, invalid_syllable
        )
        self.assertRaises(ValueError, trans._ipa_syllable_to_numbered, invalid_syllable)

    def test_issue_4(self):
        numbered = "lv4"
        accented = "lǜ"
        self.assertEqual(accented, trans.numbered_to_accented(numbered))

    def test_issue_5(self):
        numbered = "guang3er2"
        accented = "guǎng'ér"
        self.assertEqual(accented, trans.numbered_to_accented(numbered))

        # Make sure that extra apostrophes aren't added.
        numbered1 = "xi1'an1"
        accented1 = "xī'ān"
        self.assertEqual(accented1, trans.numbered_to_accented(numbered1))

        # Make sure that uppercase is handled correctly.
        numbered1 = "Yong3Er2"
        accented1 = "Yǒng'Ér"
        self.assertEqual(accented1, trans.numbered_to_accented(numbered1))

    def test_issue_6(self):
        pinyin = "zhuójìnr"
        zhuyin = "ㄓㄨㄛˊ ㄐㄧㄣˋ ㄦ˙"
        ipa = "ʈʂwɔ˧˥ tɕin˥˩ ɻ"

        self.assertEqual(zhuyin, trans.pinyin_to_zhuyin(pinyin))
        self.assertEqual(ipa, trans.pinyin_to_ipa(pinyin))

    def test_issue_8(self):
        accented = "Àodìlì"
        numbered = "Ao4di4li4"

        self.assertEqual(numbered, trans.accented_to_numbered(accented))

    def test_issue_23(self):
        pinyin = "ó"
        zhuyin = "ㄛˊ"

        self.assertEqual(zhuyin, trans.pinyin_to_zhuyin(pinyin))
