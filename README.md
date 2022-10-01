# pyunormalize
A pure Python implementation of the **Unicode normalization algorithm** independent from the Python core Unicode database. This package supports version&nbsp;15.0 of the Unicode standard (released on September&nbsp;13, 2022). It has been thoroughly tested against the [Unicode test file](https://www.unicode.org/Public/15.0.0/ucd/NormalizationTest.txt).

For the formal specification of the Unicode normalization algorithm, see [Section 3.11, Normalization Forms](https://www.unicode.org/versions/Unicode15.0.0/ch03.pdf#G49537), in the Unicode core specification.

### Installation
The easiest method to install is using pip:
```shell
pip install pyunormalize
```

### UCD version
To get the version of the Unicode character database currently used:
```python
>>> from pyunormalize import UCD_VERSION
>>> UCD_VERSION
'15.0.0'
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
>>> normalize("NFKD", "⑴ ﬃ ²")
'(1) ffi 2'
>>> forms = ["NFC", "NFD", "NFKC", "NFKD"]
>>> [normalize(f, "\u017F\u0307\u0323") for f in forms]
['ẛ̣', 'ẛ̣', 'ṩ', 'ṩ']
```

### Related resources
This implementation is based on the following resources:
- [Section 3.11, Normalization Forms, in the Unicode core specification, version&nbsp;15.0.0](https://www.unicode.org/versions/Unicode15.0.0/ch03.pdf#G49537)
- [Unicode Standard Annex #15: Unicode Normalization Forms, version&nbsp;53](https://www.unicode.org/reports/tr15/tr15-53.html)

### Licenses
The code is available under the [MIT license](https://github.com/mlodewijck/pyunormalize/blob/master/LICENSE).

Usage of Unicode data files is governed by the [UNICODE TERMS OF USE](https://www.unicode.org/copyright.html), a copy of which is included as [UNICODE-LICENSE](https://github.com/mlodewijck/pyunormalize/blob/master/UNICODE-LICENSE).
