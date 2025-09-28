"""Unicode normalization conformance tests.

Test cases are derived from the official Unicode conformance data:
    https://www.unicode.org/Public/17.0.0/ucd/NormalizationTest.txt
"""

import os
import unittest

from pyunormalize import NFC, NFD, NFKC, NFKD, normalize, UNICODE_VERSION

# Conformance test file from the UCD
NORMALIZATION_TEST_TXT = "NormalizationTest.txt"

# File from the UCD used to determine assigned code points
DERIVED_NAME_TXT = "DerivedName.txt"


def _parse_assigned_codepoints():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "data",
        DERIVED_NAME_TXT,
    )

    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()

    if UNICODE_VERSION not in lines[0]:
        raise RuntimeError(
            f"Unicode version mismatch in {DERIVED_NAME_TXT!r} "
            f"(expected {UNICODE_VERSION!r} in line {lines[0]!r})"
        )

    assigned = set()

    for line in lines:
        if not line or line.startswith("#"):
            continue

        key, _, _ = line.partition("; ")
        key = key.rstrip()

        if line.endswith("*"):
            if ".." in key:
                start, _, end = key.partition("..")
                assigned.update(range(int(start, 16), int(end, 16) + 1))
            else:
                assigned.add(int(key, 16))
        else:
            assigned.add(int(key, 16))

    return assigned


def _parse_test_data():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "data",
        NORMALIZATION_TEST_TXT,
    )

    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()

    if UNICODE_VERSION not in lines[0]:
        raise RuntimeError(
            f"Unicode version mismatch in {NORMALIZATION_TEST_TXT!r} "
            f"(expected {UNICODE_VERSION!r} in line {lines[0]!r})"
        )

    normalization_cases = []
    part1_points = set()
    in_part1 = False

    for lineno, line in enumerate(lines, 1):
        if not line or line.startswith("#"):
            continue

        if line.startswith("@Part1"):
            in_part1 = True
            continue
        elif line.startswith("@Part"):
            in_part1 = False
            continue

        fields = line.split(";", 5)[:5]

        case = [
            "".join([chr(int(cp, 16)) for cp in field.split()])
            for field in fields
        ]

        normalization_cases.append((lineno, case))

        # Collect only the c1 code points from @Part1, which should be excluded
        # from the identity tests for assigned code points
        if in_part1:
            first_field = fields[0].split()
            if len(first_field) == 1:
                part1_points.add(int(first_field[0], 16))

    assigned = _parse_assigned_codepoints()
    character_tests = [chr(cp) for cp in assigned - part1_points]

    return normalization_cases, character_tests


class TestUnicodeNormalization(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data, cls.char_tests = _parse_test_data()

    def _check_partial_field_consistency(self, func, indices):
        for lineno, case in self.data:
            results = [case[indices[0]]]
            results.extend(func(case[i]) for i in indices[1:])

            self.assertEqual(
                results.count(results[0]),
                len(results),
                f"normalization mismatch at line {lineno} (case: {case})",
            )

    def _check_full_field_consistency(self, func, raw):
        for lineno, case in self.data:
            results = []
            for i, c in enumerate(case):
                if i == raw:
                    results.append(c)
                results.append(func(c))

            self.assertEqual(
                results.count(results[0]),
                len(results),
                f"normalization mismatch at line {lineno} (case: {case})",
            )

    def test_NFC_partial_field_consistency(self):
        # c2 == toNFC(c1) == toNFC(c2) == toNFC(c3)
        # c4 == toNFC(c4) == toNFC(c5)
        self._check_partial_field_consistency(NFC, indices=[1, 0, 1, 2])
        self._check_partial_field_consistency(NFC, indices=[3, 3, 4])

    def test_NFD_partial_field_consistency(self):
        # c3 == toNFD(c1) == toNFD(c2) == toNFD(c3)
        # c5 == toNFD(c4) == toNFD(c5)
        self._check_partial_field_consistency(NFD, indices=[2, 0, 1, 2])
        self._check_partial_field_consistency(NFD, indices=[4, 3, 4])

    def test_NFKC_full_field_consistency(self):
        # c4 == toNFKC(c1) == ... == toNFKC(c5)
        self._check_full_field_consistency(NFKC, raw=3)

    def test_NFKD_full_field_consistency(self):
        # c5 == toNFKD(c1) == ... == toNFKD(c5)
        self._check_full_field_consistency(NFKD, raw=4)

    def test_identity_assigned_codepoints(self):
        # X == toNFC(X) == toNFD(X) == toNFKC(X) == toNFKD(X)
        forms = ["NFC", "NFD", "NFKC", "NFKD"]
        for char in self.char_tests:
          # results = [char, *[normalize(f, char) for f in forms]]
            results = [normalize(f, char) for f in forms]
            self.assertEqual(
                results.count(char),
                len(results),
                f"not all forms preserved identity for {char!r} ({results})",
            )


if __name__ == "__main__":
    unittest.main()
