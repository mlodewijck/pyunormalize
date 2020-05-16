"""Functions testing."""

import time
import os.path
import re
import sys
import urllib.error
import urllib.request

from pyunormalize import (
    check_NFC, check_NFD, check_NFKC, check_NFKD, UCD_VERSION as _UCD_VERSION
)

# The Unicode Standard used to process the data
UNICODE_VERSION = "13.0.0"

# The Unicode Character Database
UCD_VERSION = UNICODE_VERSION

assert UCD_VERSION == _UCD_VERSION

here = "https://www.unicode.org/Public/" + UCD_VERSION + "/ucd/"
URL = here + "DerivedNormalizationProps.txt"

DIR_PATH = os.path.dirname(__file__)
UNICODE_FILE = URL.rsplit("/", 1)[-1]

COUNTER = 0


nfc_qc_no = []
nfc_qc_maybe = []
nfd_qc_no = []
nfkc_qc_no = []
nfkc_qc_maybe = []
nfkd_qc_no = []

props = {
    "NFCN"  : nfc_qc_no,
    "NFCM"  : nfc_qc_maybe,
    "NFDN"  : nfd_qc_no,
    "NFKCN" : nfkc_qc_no,
    "NFKCM" : nfkc_qc_maybe,
    "NFKDN" : nfkd_qc_no,
}

_dict = {}


def parse(lines):
    assert re.match(
        "^#.*{}-(.+).txt.*$".format(UNICODE_FILE[:-4]), lines[0]
    ).group(1) == UCD_VERSION

    prop = None
    for line in lines:
        line = line.rstrip()
        if line.startswith("# Property:"):
            prop = line.split()[-1].split("_")[0]
        elif prop and line and not line.startswith("#"):
            try:
                fields = line.partition("#")[0].split(";")
                cp = [int(c, 16) for c in fields[0].split("..")]
                name = fields[2].strip()
                if len(cp) > 1:
                    props[prop + name].extend(range(cp[0], cp[1] + 1))
                else:
                    props[prop + name].append(cp[0])
            except IndexError:
                break

    for k, v in props.items():
        _dict[k] = set(v)


def main():
    path_ = os.path.join(DIR_PATH, UNICODE_FILE)
    if os.path.exists(path_):
        print("\n.. Extracting data from text file found in local directory...")
        with open(path_, "r", encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    else:
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

    parse(lines)

    start_time = time.perf_counter()
    global COUNTER

    print(".. Test can start.\n")

    ##
    ## NFC_Quick_Check
    ##

    print("""
NFC_QC
----------------------------------------------------------------------
""".rstrip())

    s, f = 0, 0
    for x in range(0x0, 0x110000):
        c = chr(x)
        observed = check_NFC(c)
        if x in _dict["NFCN"]:
            expected = False
        elif x in _dict["NFCM"]:
            expected = None
        else:
            expected = True

        if observed != expected:
            f += 1
            print("Failed for U+{}".format(format(x, "04X")))
        else:
            s += 1

    r = s + f
    if f:
        res = "{} ({} tests, {} failures)".format("FAIL", r, f)
    else:
        res = "{} ({} tests)".format("OK", r)
        COUNTER += 1

    print("{}".format(res))

    ##
    ## NFD_Quick_Check
    ##

    print("""
NFD_QC
----------------------------------------------------------------------
""".rstrip())

    s, f = 0, 0
    for x in range(0x0, 0x110000):
        c = chr(x)
        observed = check_NFD(c)
        if x in _dict["NFDN"]:
            expected = False
        else:
            expected = True

        if observed != expected:
            f += 1
            print("Failed for U+{}".format(format(x, "04X")))
        else:
            s += 1

    r = s + f
    if f:
        res = "{} ({} tests, {} failures)".format("FAIL", r, f)
    else:
        res = "{} ({} tests)".format("OK", r)
        COUNTER += 1

    print("{}".format(res))

    ##
    ## NFKC_Quick_Check
    ##

    print("""
NFKC_QC
----------------------------------------------------------------------
""".rstrip())

    s, f = 0, 0
    for x in range(0x0, 0x110000):
        c = chr(x)
        observed = check_NFKC(c)
        if x in _dict["NFKCN"]:
            expected = False
        elif x in _dict["NFKCM"]:
            expected = None
        else:
            expected = True

        if observed != expected:
            f += 1
            print("Failed for U+{}".format(format(x, "04X")))
        else:
            s += 1

    r = s + f
    if f:
        res = "{} ({} tests, {} failures)".format("FAIL", r, f)
    else:
        res = "{} ({} tests)".format("OK", r)
        COUNTER += 1

    print("{}".format(res))

    ##
    ## NFKD_Quick_Check
    ##

    print("""
NFKD_QC
----------------------------------------------------------------------
""".rstrip())

    s, f = 0, 0
    for x in range(0x0, 0x110000):
        c = chr(x)
        observed = check_NFKD(c)
        if x in _dict["NFKDN"]:
            expected = False
        else:
            expected = True

        if observed != expected:
            f += 1
            print("Failed for U+{}".format(format(x, "04X")))
        else:
            s += 1

    r = s + f
    if f:
        res = "{} ({} tests, {} failures)".format("FAIL", r, f)
    else:
        res = "{} ({} tests)".format("OK", r)
        COUNTER += 1

    print("{}".format(res))


    if COUNTER == 4:
        print("\n.. Quick check tests (Unicode {}) are successfull."
              .format(UNICODE_VERSION))
    else:
        print("\n.. Quick check tests (Unicode {}) have failed."
              .format(UNICODE_VERSION))

    print(".. {:.3f} seconds\n".format(time.perf_counter() - start_time))


if __name__ == "__main__":
    main()
