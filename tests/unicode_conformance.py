"""Unicode conformance testing.

Information about conformance testing for Unicode normalization forms:
- www.unicode.org/Public/13.0.0/ucd/NormalizationTest.txt
- unicode.org/reports/tr15/
"""

import time
import os.path
import re
import sys
import urllib.error
import urllib.request

from pyunormalize import (
    NFC, NFD, NFKC, NFKD,
    check_NFC, check_NFD, check_NFKC, check_NFKD,
    UCD_VERSION as _UCD_VERSION
)

# The Unicode Standard used to process the data
UNICODE_VERSION = "13.0.0"

# The Unicode Character Database
UCD_VERSION = UNICODE_VERSION

assert UCD_VERSION == _UCD_VERSION

here = "https://www.unicode.org/Public/" + UCD_VERSION + "/ucd/"
URL = here + "NormalizationTest.txt"

DIR_PATH = os.path.dirname(__file__)
UNICODE_FILE = URL.rsplit("/", 1)[-1]

COUNTER = 0


def hex_to_chr(seq):
    return "".join(chr(int(x, 16)) for x in seq.split())


def parse(lines):
    assert re.match(
        "^#.*{}-(.+).txt.*$".format(UNICODE_FILE[:-4]), lines[0]
    ).group(1) == UCD_VERSION

    data = []  # list of lists
    for num, line in enumerate(lines, 1):
        if line and not line.startswith(("#", "@")):
            *c, _ = line.split(";", 5)
            rec = [hex_to_chr(seq) for seq in c]
            # rec: [source, nfc, nfd, nfkc, nfkd]
            data.append([num, *rec])

    return data


def _txt():
    path_ = os.path.join(DIR_PATH, UNICODE_FILE)
    if os.path.exists(path_):
        print("\n.. Extracting data from text file found in local directory...")
        with open(path_, "r", encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        return parse(lines)

    return None


def _url():
    def _excepthook(type, value, traceback):
        print(value)

    try:
        print("\n.. Fetching URL...")
        response = urllib.request.urlopen(URL)
        #print(response.__dict__)

    except urllib.error.HTTPError as e:
        sys.excepthook = _excepthook
        raise Exception(
            "{0} The server couldn't fulfill the request.\n"
            "{0} Error code:\n\n{1}\n"
            .format("..", e.code))

    except urllib.error.URLError as e:
        sys.excepthook = _excepthook
        raise Exception(
            "{0} We failed to reach a server.\n"
            "{0} Reason:\n\n{1}\n"
            .format("..", e.reason))

    print(".. Extracting data...")

    lines = response.read().decode("utf-8").splitlines()
    return parse(lines)


def main():
    data = _txt() or _url()

    start_time = time.perf_counter()
    global COUNTER

    print(".. Test can start.\n")

    chars = []  # needed for character by character test (below)

    # NFC
    # c2 ==  toNFC(c1) ==  toNFC(c2) ==  toNFC(c3)
    # c4 ==  toNFC(c4) ==  toNFC(c5)
    print("""
Normalization Form C
----------------------------------------------------------------------
""".rstrip())

    s, f = 0, 0
    for record in data:
        num, source, nfc, nfd, nfkc, nfkd = record
        if len(source) == 1:
            chars.append(ord(source[0]))

        lst_1 = []
        if check_NFC(source):
            lst_1.append(source)
        else:
            lst_1.append(NFC(source))

        if check_NFC(nfc):
            lst_1.append(nfc)
        else:
            lst_1.append(NFC(nfc))

        if check_NFC(nfd):
            lst_1.append(nfd)
        else:
            lst_1.append(NFC(nfd))

        lst_2 = []
        if check_NFC(nfkc):
            lst_2.append(nfkc)
        else:
            lst_2.append(NFC(nfkc))

        if check_NFC(nfkd):
            lst_2.append(nfkd)
        else:
            lst_2.append(NFC(nfkd))

#        lst_1 = [nfc, NFC(source), NFC(nfc), NFC(nfd)]
#        lst_2 = [nfkc, NFC(nfkc), NFC(nfkd)]
#        if (all(x == lst_1[0] for x in lst_1)
#                and all(x == lst_2[0] for x in lst_2)):
#            s += 1
        if (all(x == nfc for x in lst_1)
                and all(x == nfkc for x in lst_2)):
            s += 1
        else:
            f += 1
            print("Failed on line {}.".format(num))

    r = s + f
    if f:
        res = "{} ({} tests, {} failures)".format("FAIL", r, f)
    else:
        res = "{} ({} tests)".format("OK", r)
        COUNTER += 1

    print("{}".format(res))


    # NFD
    # c3 ==  toNFD(c1) ==  toNFD(c2) ==  toNFD(c3)
    # c5 ==  toNFD(c4) ==  toNFD(c5)
    print("""
Normalization Form D
----------------------------------------------------------------------
""".rstrip())

    s, f = 0, 0
    for record in data:
        num, source, nfc, nfd, nfkc, nfkd = record

        lst_1 = []
        if check_NFD(source):
            lst_1.append(source)
        else:
            lst_1.append(NFD(source))

        if check_NFD(nfc):
            lst_1.append(nfc)
        else:
            lst_1.append(NFD(nfc))

        if check_NFD(nfd):
            lst_1.append(nfd)
        else:
            lst_1.append(NFD(nfd))

        lst_2 = []
        if check_NFD(nfkc):
            lst_2.append(nfkc)
        else:
            lst_2.append(NFD(nfkc))

        if check_NFD(nfkd):
            lst_2.append(nfkd)
        else:
            lst_2.append(NFD(nfkd))

#        lst_1 = [nfd, NFD(source), NFD(nfc), NFD(nfd)]
#        lst_2 = [nfkd, NFD(nfkc), NFD(nfkd)]
#        if (all(x == lst_1[0] for x in lst_1)
#                and all(x == lst_2[0] for x in lst_2)):
#            s += 1
        if (all(x == nfd for x in lst_1)
                and all(x == nfkd for x in lst_2)):
            s += 1
        else:
            f += 1
            print("Failed on line {}.".format(num))

    r = s + f
    if f:
        res = "{} ({} tests, {} failures)".format("FAIL", r, f)
    else:
        res = "{} ({} tests)".format("OK", r)
        COUNTER += 1

    print("{}".format(res))


    # NFKC
    # c4 == toNFKC(c1) == toNFKC(c2) == toNFKC(c3) == toNFKC(c4) == toNFKC(c5)
    print("""
Normalization Form KC
----------------------------------------------------------------------
""".rstrip())

    s, f = 0, 0
    for record in data:
        num, source, nfc, nfd, nfkc, nfkd = record

        lst = []
        if check_NFKC(source):
            lst.append(source)
        else:
            lst.append(NFKC(source))

        if check_NFKC(nfc):
            lst.append(nfc)
        else:
            lst.append(NFKC(nfc))

        if check_NFKC(nfd):
            lst.append(nfd)
        else:
            lst.append(NFKC(nfd))

        if check_NFKC(nfkc):
            lst.append(nfkc)
        else:
            lst.append(NFKC(nfkc))

        if check_NFKC(nfkd):
            lst.append(nfkd)
        else:
            lst.append(NFKC(nfkd))

        #if (NFKC(source) == NFKC(nfc) == NFKC(nfd) == NFKC(nfkc) == NFKC(nfkd)
        #        == nfkc):
        #    s += 1
        if all(item == nfkc for item in lst):
            s += 1
        else:
            f += 1
            print("Failed on line {}.".format(num))

    r = s + f
    if f:
        res = "{} ({} tests, {} failures)".format("FAIL", r, f)
    else:
        res = "{} ({} tests)".format("OK", r)
        COUNTER += 1

    print("{}".format(res))


    # NFKD
    # c5 == toNFKD(c1) == toNFKD(c2) == toNFKD(c3) == toNFKD(c4) == toNFKD(c5)
    print("""
Normalization Form KD
----------------------------------------------------------------------
""".rstrip())

    s, f = 0, 0
    for record in data:
        num, source, nfc, nfd, nfkc, nfkd = record

        lst = []
        if check_NFKD(source):
            lst.append(source)
        else:
            lst.append(NFKD(source))

        if check_NFKD(nfc):
            lst.append(nfc)
        else:
            lst.append(NFKD(nfc))

        if check_NFKD(nfd):
            lst.append(nfd)
        else:
            lst.append(NFKD(nfd))

        if check_NFKD(nfkc):
            lst.append(nfkc)
        else:
            lst.append(NFKD(nfkc))

        if check_NFKD(nfkd):
            lst.append(nfkd)
        else:
            lst.append(NFKD(nfkd))
 
        #if (NFKD(source) == NFKD(nfc) == NFKD(nfd) == NFKD(nfkc) == NFKD(nfkd)
        #        == nfkd):
        #    s += 1
        if all(item == nfkd for item in lst):
            s += 1
        else:
            f += 1
            print("Failed on line {}.".format(num))

    r = s + f
    if f:
        res = "{} ({} tests, {} failures)".format("FAIL", r, f)
    else:
        res = "{} ({} tests)".format("OK", r)
        COUNTER += 1

    print("{}".format(res))


    #
    # Character by character test
    #

    # X == toNFC(X) == toNFD(X) == toNFKC(X) == toNFKD(X)
    print("""
Character by character test, all normalization forms
----------------------------------------------------------------------
""".rstrip())

    # The characters included in the chars list
    # have already been processed (above)
    items = set(range(0x0, 0x110000)) - set(chars)

    s, f = 0, 0
    for x in items:
        c = chr(x)

        lst = []
        if not check_NFC(c):
            lst.append(NFC(c))

        if not check_NFD(c):
            lst.append(NFD(c))

        if not check_NFKC(c):
            lst.append(NFKC(c))

        if not check_NFKD(c):
            lst.append(NFKD(c))

        #if c == NFC(c) == NFD(c) == NFKC(c) == NFKD(c):
        #    s += 1
        if all(item == c for item in lst):
            s += 1
        else:
            f += 1
            print("Failed for U+{}".format(format(x, "04X")))

    r = s + f
    if f:
        res = "{} ({} tests, {} failures)".format("FAIL", r, f)
    else:
        res = "{} ({} tests)".format("OK", r)
        COUNTER += 1

    print("{}".format(res))


    if COUNTER == 5:
        print("\n.. Implementation conforms to UAX #15 version {}."
              .format(UNICODE_VERSION))
    else:
        print("\n.. Implementation does not conform to UAX #15 version {}."
              .format(UNICODE_VERSION))

    print(".. {:.3f} seconds\n".format(time.perf_counter() - start_time))

#    from pyunormalize.core import _cache_info
#    _cache_info()

# maxsize=128
#    C: CacheInfo(hits=27886, misses=32586, maxsize=128, currsize=128)
#    K: CacheInfo(hits=55371, misses=39971, maxsize=128, currsize=128)

# maxsize=None:
#    C: CacheInfo(hits=43826, misses=29416, maxsize=None, currsize=29416)
#    K: CacheInfo(hits=62251, misses=33091, maxsize=None, currsize=33091)


if __name__ == "__main__":
    main()
