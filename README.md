# pyunormalize
A pure Python implementation of the **Unicode normalization algorithm** independent of Python’s core Unicode database. This package conforms to version&nbsp;16.0 of the Unicode standard, released in September&nbsp;2024, and has been rigorously tested for accuracy using the official [Unicode test file](https://www.unicode.org/Public/16.0.0/ucd/NormalizationTest.txt).

### Installation and updates
To install the package, run:
```shell
pip install pyunormalize
```

To upgrade to the latest version, run:
```shell
pip install pyunormalize --upgrade
```

### Unicode character database (UCD) version
To retrieve the version of the Unicode character database in use:
```python
>>> from pyunormalize import UCD_VERSION
>>> UCD_VERSION
'16.0.0'
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
- [Section 3.11, “Normalization Forms,” in the Unicode core specification, version&nbsp;16.0.0](https://www.unicode.org/versions/Unicode16.0.0/core-spec/chapter-3/#G49537)
- [Unicode Standard Annex #15: Unicode Normalization Forms, revision&nbsp;56](https://www.unicode.org/reports/tr15/tr15-56.html)

### Licenses
The code is licensed under the [MIT license](https://github.com/mlodewijck/pyunormalize/blob/master/LICENSE).

Usage of Unicode data files is subject to the [UNICODE TERMS OF USE](https://www.unicode.org/copyright.html). Additional rights and restrictions regarding Unicode data files and software are outlined in the [Unicode Data Files and Software License](https://www.unicode.org/license.txt), a copy of which is included as [UNICODE-LICENSE](https://github.com/mlodewijck/pyunormalize/blob/master/UNICODE-LICENSE).