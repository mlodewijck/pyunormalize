# -*- coding: utf-8 -*-
"""Unit tests for pyunormalize."""

import unittest

from pyunormalize.core import _decompose, _reorder, _compose
from pyunormalize import (
    check, check_NFC, check_NFD, check_NFKC, check_NFKD,
    normalize, NFC, NFD, NFKC, NFKD,
    UCD_VERSION as _UCD_VERSION, UNICODE_VERSION as _UNICODE_VERSION
)

# The Unicode Standard used to process the data
UNICODE_VERSION = "13.0.0"

# The Unicode Character Database version used
UCD_VERSION = UNICODE_VERSION


class TestSuite(unittest.TestCase):

    def test_UCD_VERSION(self):
        self.assertTrue(_UCD_VERSION == UCD_VERSION)

    def test_UNICODE_VERSION(self):
        self.assertTrue(_UNICODE_VERSION == UNICODE_VERSION)

    def test_check_NFC(self):

        s = "\u1E9B\u0323"
        self.assertIsNone(check_NFC(s))  # MAYBE -> None

        s = "\u017F\u0307\u0323"
        self.assertFalse(check_NFC(s))  # NO -> False
 
    def test_check_NFKC(self):

        s = "\u1E9B\u0323"
        self.assertFalse(check_NFKC(s))  # NO -> False

        s = "\u017F\u0307\u0323"
        self.assertFalse(check_NFKC(s))  # NO -> False

    def test_check(self):

        s = "\u00E9"  # é
        self.assertTrue(check("NFC", s) == check_NFC(s))  # YES
        self.assertTrue(check("NFD", s) == check_NFD(s))  # NO
        self.assertTrue(check("NFKC", s) == check_NFKC(s))  # YES
        self.assertTrue(check("NFKD", s) == check_NFKD(s))  # NO

        s = "\u0065\u0301"  # é
        self.assertTrue(check("NFC", s) == check_NFC(s))  # NO
        self.assertTrue(check("NFD", s) == check_NFD(s))  # YES
        self.assertTrue(check("NFKC", s) == check_NFKC(s))  # NO
        self.assertTrue(check("NFKD", s) == check_NFKD(s))  # YES

        s = "\u0300"
        self.assertTrue(check("NFC", s) == check_NFC(s))  # MAYBE
        self.assertTrue(check("NFKC", s) == check_NFKC(s))  # MAYBE

    def test_normalize(self):

        # Characters whose normalization forms
        # under NFC, NFD, NFKC, and NFKD are all different:
        #   ϓ   U+03D3 GREEK UPSILON WITH ACUTE AND HOOK SYMBOL
        #   ϔ   U+03D4 GREEK UPSILON WITH DIAERESIS AND HOOK SYMBOL
        #   ẛ   U+1E9B LATIN SMALL LETTER LONG S WITH DOT ABOVE

        for s in ["\u03D3", "\u03D4", "\u1E9B"]:
            self.assertTrue(normalize("NFC", s) ==  NFC(s))
            self.assertTrue(normalize("NFD", s) ==  NFD(s))
            self.assertTrue(normalize("NFKC", s) == NFKC(s))
            self.assertTrue(normalize("NFKD", s) == NFKD(s))

    def test_internals(self):

        self.assertEqual(_decompose("\u00C0"),
            [0x0041, 0x0300])
        self.assertEqual(_decompose("\u00BE", compat=True),
            [0x0033, 0x2044, 0x0034])
        self.assertEqual(_decompose("힡"),
            [0x1112, 0x1175, 0x11C0])

        items = [0x017F, 0x0307, 0x0323]
        self.assertEqual(_reorder(items), [0x017F, 0x0323, 0x0307])

        s = "a\u0328\u0302\u0301"  # a + ogonek + circumflex + acute
        self.assertEqual(_decompose(s),
            [0x0061, 0x0328, 0x0302, 0x0301])
        self.assertEqual(_reorder([0x0061, 0x0328, 0x0302, 0x0301]),
            [0x0061, 0x0328, 0x0302, 0x0301])
        self.assertEqual(_compose([0x0061, 0x0328, 0x0302, 0x0301]),
            [0x0105, 0x0302, 0x0301])

        s = "\u0105\u0302\u0301"  # a-ogonek + circumflex + acute
        self.assertEqual(_compose(_decompose(_reorder(s))),
            [0x0105, 0x0302, 0x0301])

        s = "\u0105\u0301\u0302"  # a-ogonek + acute + circumflex
        self.assertEqual(_decompose(s),
            [0x0061, 0x0328, 0x0301, 0x0302])
        self.assertEqual(_reorder([0x0061, 0x0328, 0x0301, 0x0302]),
            [0x0061, 0x0328, 0x0301, 0x0302])
        self.assertEqual(_compose([0x0061, 0x0328, 0x0301, 0x0302]),
            [0x0105, 0x0301, 0x0302])

        self.assertEqual(_compose(_decompose(_reorder(s))),
            [0x0105, 0x0301, 0x0302])


if __name__ == "__main__":
    unittest.main()
