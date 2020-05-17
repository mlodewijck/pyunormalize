# -*- coding: utf-8 -*-
"""Unicode normalization forms. A library independent from the Python
core Unicode database.

For the formal specification of the Unicode Normalization Algorithm,
see Section 3.11, Normalization Forms, in the Unicode core
specification. Unicode Standard Annex #15, "Unicode Normalization
Forms", contains more detailed explanations, examples, and
implementation strategies.

To get the version of the Unicode Character Database currently used:

    import pyunormalize
    print(pyunormalize.UCD_VERSION)

    Or:

    from pyunormalize import UCD_VERSION
    print(UCD_VERSION)


Quick verification check:

    from pyunormalize import (
        check_NFC, check_NFD, check_NFKC, check_NFKD
    )

    print(check_NFC("élève"))  # True
    print(check_NFD("élève"))  # False

    unistr = "\u017F\u0307\u0323"
    print(check_NFC(unistr))   # None
    print(check_NFD(unistr))   # False
    print(check_NFKC(unistr))  # False
    print(check_NFKD(unistr))  # False


    from pyunormalize import check

    unistr = "\u017F\u0307\u0323"
    forms = ["NFC", "NFD", "NFKC", "NFKD"]
    print([check(f, unistr) for f in forms])
    # [None, False, False, False]

    unistr = "한국"  # "\u1112\u1161\u11AB\u1100\u116E\u11A8"
    print(check("NFC", unistr))  # None
    print(check("NFD", unistr))  # True

    unistr = "한국"  # "\uD55C\uAD6D"
    print(check("NFC", unistr))  # True
    print(check("NFD", unistr))  # False


Normalization:

    from pyunormalize import NFC, NFD

    unistr = "한국"  # "\u1112\u1161\u11AB\u1100\u116E\u11A8"
    print(NFC(unistr))  # 한국

    unistr = "한국"  # "\uD55C\uAD6D"
    print(NFD(unistr))  # 한국


    from pyunormalize import NFC, NFD, NFKC, NFKD
    unistr = "\u017F\u0307\u0323"
    nfc = NFC(unistr)    # ẛ̣
    nfd = NFD(unistr)    # ẛ̣
    nfkc = NFKC(unistr)  # ṩ
    nfkd = NFKD(unistr)  # ṩ


    from pyunormalize import normalize
    unistr = "\u017F\u0307\u0323"
    forms = ["NFC", "NFD", "NFKC", "NFKD"]
    print([normalize(f, unistr) for f in forms])
    # ['ẛ̣', 'ẛ̣', 'ṩ', 'ṩ']

"""

__all__ = [
    "NFC",
    "NFD",
    "NFKC",
    "NFKD",
    "normalize",
    "check_NFC",
    "check_NFD",
    "check_NFKC",
    "check_NFKD",
    "check",
    "UCD_VERSION",
    "UNICODE_VERSION",
    "__version__"
]

# The Unicode Standard used to process the data
UNICODE_VERSION = "13.0.0"

# The Unicode Character Database
UCD_VERSION = UNICODE_VERSION

__author__  = "Marc Lodewijck"
__version__ = "0.1.0"


from .core import *
