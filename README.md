This implementation supports the most recent version of the Unicode
Standard, currently Unicode 13.0 (released March 2020). It has been
successfully tested against the Unicode test file found at
www.unicode.org/Public/13.0.0/ucd/NormalizationTest.txt

To get the version of the Unicode Character Database currently used:

>>> import pyunormalize
>>> print(pyunormalize.UCD_VERSION)
13.0.0

>>> from pyunormalize import UCD_VERSION
>>> print(UCD_VERSION)
13.0.0
