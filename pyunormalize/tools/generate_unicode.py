# This script generates the pyunormalize.unicode module.
#
# Input files:
#     https://www.unicode.org/Public/16.0.0/ucd/CompositionExclusions.txt
#     https://www.unicode.org/Public/16.0.0/ucd/DerivedNormalizationProps.txt
#     https://www.unicode.org/Public/16.0.0/ucd/UnicodeData.txt
#
# Output file:
#     tools/generate_unicode/unicode.py
#
# The output file must be copied to the `pyunormalize` directory.

import pathlib
import urllib.error
import urllib.request

UNICODE_VERSION = "16.0.0"
SCRIPT_PATH = "/".join(pathlib.Path(__file__).parts[-3:])

# Files from the Unicode character database (UCD)
EXCLUSIONS = "CompositionExclusions.txt"
PROPS = "DerivedNormalizationProps.txt"
UNICODE_DATA = "UnicodeData.txt"


def read_remote(filename):
    url = f"https://www.unicode.org/Public/{UNICODE_VERSION}/ucd/"

    try:
        print("\n.. Fetching URL...")
        response = urllib.request.urlopen(f"{url}{filename}")
        # print(response.__dict__)
    except urllib.error.HTTPError as e:
        raise Exception(
            f"The server could not fulfill the request. Error code: {e.code}"
        )
    except urllib.error.URLError as e:
        raise Exception(
            f"We failed to reach a server.\nReason:\n{e.reason}"
        )

    print(f".. Extracting data from {filename}")
    return response.read().decode("utf-8").splitlines()


def check_version(line):
    assert UNICODE_VERSION in line, "Wrong Unicode version number."


def main():
    # Current working directory
    cwd = pathlib.Path.cwd()

    #
    # Unicode file: UnicodeData.txt
    #

    try:
        lines = (cwd / UNICODE_DATA).read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        lines = read_remote(UNICODE_DATA)
        print(".. Done.")

    # File version is not specified in UnicodeData.txt
    # and therefore cannot be checked.

    ccc_list = []
    dcp_list = []

    for line in lines:
        code, _, _, ccc, _, dcp, *_ = line.split(";", 6)

        if ccc != "0":
            ccc_list.append(f"    0x{code:0>5}: {ccc:>3},")

        if dcp:
            dec_dcp = []

            for c in dcp.split(" "):
                dec_dcp.append(f'"{c}"' if c.startswith("<") else f"0x{c}")

            dcp_list.append(f"    0x{code:0>5}: [{', '.join(dec_dcp)}],")

    #
    # Unicode file: CompositionExclusions.txt
    #

    try:
        lines = (cwd / EXCLUSIONS).read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        lines = read_remote(EXCLUSIONS)
        print(".. Done.")

    # Check file version
    check_version(lines[0])

    exclusions_list = []

    for line in lines:
        line = line.rstrip()
        if line and not line.startswith("#"):
            code = line.split("#")[0].rstrip()
            exclusions_list.append(f"    0x{code:0>5},")

    #
    # Unicode file: DerivedNormalizationProps.txt
    #

    try:
        lines = (cwd / PROPS).read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        lines = read_remote(PROPS)
        print(".. Done.")

    # Check file version
    check_version(lines[0])

    tmp = []

    start = lines.index(
        "# Property:	NFD_Quick_Check"
    )
    stop  = lines.index(
        "# Derived Property: Expands_On_NFD (DEPRECATED as of Unicode 6.0.0)"
    )

    for line in lines[start:stop]:
        if not line or line.startswith("#"):
            continue
        tmp.append(line)

    NFD_QC_NO_list = []
    NFKD_QC_NO_list = []
    NFC_QC_NO_list = []
    NFC_QC_MAYBE_list = []
    NFKC_QC_NO_list = []
    NFKC_QC_MAYBE_list = []

    prop_values = {
        "NFD_QC"  :  NFD_QC_NO_list,
        "NFKD_QC" :  NFKD_QC_NO_list,
        "NFC_QC"  : (NFC_QC_NO_list, NFC_QC_MAYBE_list),
        "NFKC_QC" : (NFKC_QC_NO_list, NFKC_QC_MAYBE_list),
    }

    for line in tmp:
        data = line.split(" # ")[0].split(";")
        data = [d.strip() for d in data]

        code, prop, prov_val = data

        if ".." in code:
            start, end = code.split("..")

            if prop == "NFC_QC" and prov_val == "N":
                tmp_list = prop_values[prop][0]
            elif prop == "NFC_QC":  # and prov_val == "MAYBE"
                tmp_list = prop_values[prop][1]
            elif prop == "NFKC_QC" and prov_val == "N":
                tmp_list = prop_values[prop][0]
            elif prop == "NFKC_QC":  # and prov_val == "MAYBE"
                tmp_list = prop_values[prop][1]
            else:
                tmp_list = prop_values[prop]

            tmp_list.append(
                f"    *range(0x{start:0>5}, 0x{end:0>5} + 1),"
            )

        else:
            if prop == "NFC_QC" and prov_val == "N":
                tmp_list = prop_values[prop][0]
            elif prop == "NFC_QC":  # and prov_val == "MAYBE"
                tmp_list = prop_values[prop][1]
            elif prop == "NFKC_QC" and prov_val == "N":
                tmp_list = prop_values[prop][0]
            elif prop == "NFKC_QC":  # and prov_val == "MAYBE":
                tmp_list = prop_values[prop][1]
            else:
                tmp_list = prop_values[prop]

            tmp_list.append(f"           0x{code:0>5},")


    dcp = "\n".join(dcp_list)
    ccc = "\n".join(ccc_list)
    exclusions = "\n".join(exclusions_list)
    NFD_QC_N   = "\n".join(NFD_QC_NO_list)
    NFKD_QC_N  = "\n".join(NFKD_QC_NO_list)
    NFC_QC_N   = "\n".join(NFC_QC_NO_list)
    NFC_QC_M   = "\n".join(NFC_QC_MAYBE_list)
    NFKC_QC_N  = "\n".join(NFKC_QC_NO_list)
    NFKC_QC_M  = "\n".join(NFKC_QC_MAYBE_list)

    with open(cwd / "_unicode.py", "w", encoding="utf-8", newline="\n") as f:
        f.write(f'''\
"""Data derived from the Unicode character database (UCD).

This file was generated from {SCRIPT_PATH}
"""

_UNICODE_VERSION = "{UNICODE_VERSION}"

# Dictionary mapping characters to their canonical decompositions,
# not including Hangul syllables
_DECOMP_BY_CHARACTER = {{
{dcp}
}}

# Dictionary mapping characters with non-zero canonical combining class values
# to their corresponding values
_NON_ZERO_CCC_TABLE = {{
{ccc}
}}

# Characters which are excluded from composition
_COMPOSITION_EXCLUSIONS = {{
{exclusions}
}}

# NFC_Quick_Check=No
# Characters that cannot ever occur in the normalization form C
_NFC__QC_NO = set([
{NFC_QC_N}
])

# NFC_Quick_Check=Maybe
# Characters that may or may not occur in the normalization form C,
# depending on the context
_NFC__QC_MAYBE = set([
{NFC_QC_M}
])

# Code points listed for NFC_Quick_Check=No or NFC_Quick_Check=Maybe
_NFC__QC_NO_OR_MAYBE = _NFC__QC_NO | _NFC__QC_MAYBE

# NFD_Quick_Check=No
# Characters that cannot ever occur in the normalization form D
_NFD__QC_NO = set([
{NFD_QC_N}
])

# NFKC_Quick_Check=No
# Characters that cannot ever occur in the normalization form KC
_NFKC_QC_NO = set([
{NFKC_QC_N}
])

# NFKC_Quick_Check=Maybe
# Characters that may or may not occur in the normalization form KC,
# depending on the context
_NFKC_QC_MAYBE = set([
{NFKC_QC_M}
])

# Code points listed for NFKC_Quick_Check=No or NFKC_Quick_Check=Maybe
_NFKC_QC_NO_OR_MAYBE = _NFKC_QC_NO | _NFKC_QC_MAYBE

# NFKD_Quick_Check=No
# Characters that cannot ever occur in the normalization form KD
_NFKD_QC_NO = set([
{NFKD_QC_N}
])

del _NFC__QC_NO, _NFC__QC_MAYBE, _NFKC_QC_NO, _NFKC_QC_MAYBE
''')


if __name__ == "__main__":
    main()
