"""A pure Python implementation of the Unicode Normalization Algorithm
independent from the Python core Unicode database. This package supports
version 14.0 of the Unicode Standard (released September 14, 2021).
It has been successfully tested against the Unicode test file found at
www.unicode.org/Public/14.0.0/ucd/NormalizationTest.txt

To get the version of the Unicode character database currently used:

    >>> from pyunormalize import UCD_VERSION
    >>> UCD_VERSION
    '14.0.0'

For the formal specification of the Unicode Normalization Algorithm,
see Section 3.11, Normalization Forms, in the Unicode core
specification.
"""

from sys import version_info as _version_info

if _version_info < (3, 6):
    raise SystemExit(f"\n{__package__} requires Python >= 3.6 to run.")

__all__ = [
    "NFC",
    "NFD",
    "NFKC",
    "NFKD",
    "normalize",
    "UCD_VERSION",
    "UNICODE_VERSION",
    "__version__",
]

# The Unicode Standard used to process the data
UNICODE_VERSION = "14.0.0"

# The Unicode Character Database
UCD_VERSION = UNICODE_VERSION

__author__  = "Marc Lodewijck"
__version__ = "14.0.0.post3"


from pyunormalize.unicode import UCD_VERSION as _UCD

if _UCD != UCD_VERSION:
    raise SystemExit(f"\nWrong UCD version number in {unicode.__name__}")

from pyunormalize.normalization import *
