# pyunormalize
[![PyPI Version](https://img.shields.io/pypi/v/pyunormalize.svg)](https://pypi.python.org/pypi/pyunormalize) [![PyPI License](https://img.shields.io/pypi/l/pyunormalize.svg)](https://pypi.python.org/pypi/pyunormalize)

A pure Python implementation of the **Unicode Normalization Algorithm** independent from the Python core Unicode database. This package supports version 14.0 of the Unicode Standard (released September 14, 2021). It has been successfully tested against the [Unicode test file](https://www.unicode.org/Public/14.0.0/ucd/NormalizationTest.txt).

To get the version of the Unicode character database currently used:

```python
>>> from pyunormalize import UCD_VERSION
>>> UCD_VERSION
'14.0.0'
```

For the formal specification of the Unicode Normalization Algorithm, see [Section 3.11, Normalization Forms](https://www.unicode.org/versions/Unicode14.0.0/ch03.pdf#G49537), in the Unicode core specification.

### Installation
```shell
pip install pyunormalize
```

### Example usage
```python
>>> from pyunormalize import NFC, NFD, NFKC, NFKD
>>> s = "élève"  # "\u00E9\u006C\u00E8\u0076\u0065"
>>> nfc = NFC(s)
>>> nfd = NFD(s)
>>> nfc == s
True
>>> nfd == nfc
False
>>> " ".join([f"{ord(x):04X}" for x in nfc])
'00E9 006C 00E8 0076 0065'
>>> " ".join([f"{ord(x):04X}" for x in nfd])
'0065 0301 006C 0065 0300 0076 0065'
>>> 
>>> s = "⑴ ﬃ ²"
>>> NFC(s), NFKC(s), NFD(s), NFKD(s)
('⑴ ﬃ ²', '(1) ffi 2', '⑴ ﬃ ²', '(1) ffi 2')

>>> from pyunormalize import normalize
>>> forms = ["NFC", "NFD", "NFKC", "NFKD"]
>>> [normalize(f, "\u017F\u0307\u0323") for f in forms]
['ẛ̣', 'ẛ̣', 'ṩ', 'ṩ']
```

### References
* https://www.unicode.org/versions/Unicode14.0.0/ch03.pdf#G49537
* https://unicode.org/reports/tr15/
* https://www.unicode.org/Public/14.0.0/ucd/CompositionExclusions.txt
* https://www.unicode.org/Public/14.0.0/ucd/DerivedNormalizationProps.txt
* https://www.unicode.org/Public/14.0.0/ucd/UnicodeData.txt
* https://www.unicode.org/Public/14.0.0/ucd/NormalizationTest.txt

### License
The pyunormalize library is released under an [MIT license](https://github.com/mlodewijck/pyunormalize/blob/master/LICENSE).

The Unicode Standard files this library makes use of are licensed under the Unicode License Agreement for Data Files and Software. Please consult the [UNICODE, INC. LICENSE AGREEMENT](https://www.unicode.org/license.html) prior to use.

### Changes
[CHANGELOG](https://github.com/mlodewijck/pyunormalize/blob/master/CHANGELOG.md)
