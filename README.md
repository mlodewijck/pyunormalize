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
    >>> unistr = "\u017F\u0307\u0323"
    >>> 
    >>> nfc = NFC(unistr)
    >>> f'{nfc}  ->  {list(nfc)}'
    "ẛ̣  ->  ['ẛ', '̣']"
    >>> nfd = NFD(unistr)
    >>> f'{nfd}  ->  {list(nfd)}'
    "ẛ̣  ->  ['ſ', '̣', '̇']"
    >>> nfkc = NFKC(unistr)
    >>> f'{nfkc}  ->  {list(nfkc)}'
    "ṩ  ->  ['ṩ']"
    >>> nfkd = NFKD(unistr)
    >>> f'{nfkd}  ->  {list(nfkd)}'
    "ṩ  ->  ['s', '̣', '̇']"

    >>> from pyunormalize import normalize
    >>> unistr = "\u017F\u0307\u0323"
    >>> forms = ["NFC", "NFD", "NFKC", "NFKD"]
    >>> [normalize(f, unistr) for f in forms]
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
