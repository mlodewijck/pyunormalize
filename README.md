# pyunormalize
[![PyPI Version](https://img.shields.io/pypi/v/pyunormalize.svg)](https://pypi.python.org/pypi/pyunormalize) [![PyPI License](https://img.shields.io/pypi/l/pyunormalize.svg)](https://pypi.python.org/pypi/pyunormalize)

Blah blah...

Blah blah...

Blah blah...

### Installation
```shell
pip install pyunormalize
```

### Features
The library provides:

* Blah blah...
* Blah blah...

### Example usage
```python
To get the version of the Unicode character database currently used:

    >>> from pyunormalize import UCD_VERSION
    >>> UCD_VERSION
    '14.0.0'

Normalization:

    >>> from pyunormalize import NFC, NFD, NFKC, NFKD
    >>> s = "\u017F\u0307\u0323"
    >>> nfc = NFC(s)
    >>> f"{nfc}  ->  {list(nfc)}"
    "ẛ̣  ->  ['ẛ', '̣']"
    >>> nfd = NFD(s)
    >>> f"{nfd}  ->  {list(nfd)}"
    "ẛ̣  ->  ['ſ', '̣', '̇']"
    >>> nfkc = NFKC(s)
    >>> f"{nfkc}  ->  {list(nfkc)}"
    "ṩ  ->  ['ṩ']"
    >>> nfkd = NFKD(s)
    >>> f"{nfkd}  ->  {list(nfkd)}"
    "ṩ  ->  ['s', '̣', '̇']"
    >>> 
    >>> 
    >>> s = "élève"  # "\u00E9\u006C\u00E8\u0076\u0065"
    >>> nfc = NFC(s)
    >>> nfd = NFD(s)
    >>> nfc == s
    True
    >>> nfc == nfd
    False
    >>> " ".join([f"{ord(x):04X}" for x in nfc])
    '00E9 006C 00E8 0076 0065'
    >>> " ".join([f"{ord(x):04X}" for x in nfd])
    '0065 0301 006C 0065 0300 0076 0065'

    >>> from pyunormalize import normalize
    >>> s = "\u017F\u0307\u0323"
    >>> forms = ["NFC", "NFD", "NFKC", "NFKD"]
    >>> [normalize(form, s) for form in forms]
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
pyunormalize is released under an MIT license. The full text of the license is available [here](https://github.com/mlodewijck/pyunormalize/blob/master/LICENSE).

The Unicode Standard files this library makes use of are licensed under the Unicode License Agreement for Data Files and Software. Please consult the [UNICODE, INC. LICENSE AGREEMENT](https://www.unicode.org/license.html) prior to use.

### Changes
* [CHANGELOG](https://github.com/mlodewijck/pyunormalize/blob/master/CHANGELOG.md)
