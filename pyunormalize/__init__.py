# -*- coding: utf-8 -*-
"""Unicode normalization forms. A library independent from the Python
core Unicode database.

For the formal specification of the Unicode Normalization Algorithm,
see Section 3.11, Normalization Forms, in the Unicode core
specification. Unicode Standard Annex #15, "Unicode Normalization
Forms", contains more detailed explanations, examples, and
implementation strategies.


Quick verification check:

    # Quick check for Normalization Form ...

    # Quickly determine whether the Unicode string `unistr` is in the
    # Unicode normalization form `form`. Valid values for `form` are
    # "NFC", "NFD", "NFKC", and "NFKD". The result is either True, False,
    # or None. For True or False, the answer is definite; in the None
    # case, the check was inconclusive (maybe yes, maybe no). The check
    # function will always produce a definite result for the
    # normalization forms D and KD.

    from pyunormalize import (
        check_NFC, check_NFD, check_NFKC, check_NFKD
    )

    unistr = ą̂́  # \u0061\u0302\u0301\u0328
    print(check_NFC(unistr))  # None
    print(check_NFD(unistr))  # False

    unistr = "\u017F\u0307\u0323"
    print(check_NFC(unistr))   # None
    print(check_NFD(unistr))   # False
    print(check_NFKC(unistr))  # False
    print(check_NFKD(unistr))  # False



    # Quickly determine whether the Unicode string `unistr` is in the
    # Unicode normalization form `form`. Valid values for `form` are
    # "NFC", "NFD", "NFKC", and "NFKD". 

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

    from pyunormalize import NFC, NFD, NFKC, NFKD

    unistr = "a\u0302\u0301\u0328"  # ą̂́
    print(NFC(unistr))  # \u0105\u0302\u0301
    print(NFD(unistr))  # \u0061\u0328\u0302\u0301

    unistr = "한국"  # "\u1112\u1161\u11AB\u1100\u116E\u11A8"
    print(NFC(unistr))  # 한국

    unistr = "한국"  # "\uD55C\uAD6D"
    print(NFD(unistr))  # 한국

    unistr = "\u017F\u0307\u0323"
    nfc = NFC(unistr)    # ẛ̣  (\u1E9B\u0323)
    nfd = NFD(unistr)    # ẛ̣ (\u017F\u0323\u0307)
    nfkc = NFKC(unistr)  # ṩ  (\u1E69)
    nfkd = NFKD(unistr)  # ṩ  (\u0073\u0323\u0307)


    Transform the Unicode string `unistr` into the Unicode
    normalization form `form`. Valid values for `form` are "NFC",
    "NFD", "NFKC", and "NFKD":

    from pyunormalize import normalize

    unistr = "\u017F\u0307\u0323"
    forms = ["NFC", "NFD", "NFKC", "NFKD"]
    print([normalize(f, unistr) for f in forms])
    # ['ẛ̣', 'ẛ̣', 'ṩ', 'ṩ']


The version of the Unicode Character Database used in this package:

    import pyunormalize
    print(pyunormalize.UCD_VERSION)

    Or:

    from pyunormalize import UCD_VERSION
    print(UCD_VERSION)

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
