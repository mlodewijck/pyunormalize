# This script generates the `pyunormalize._unicode_data` module.
#
# Input files:
#     https://www.unicode.org/Public/17.0.0/ucd/CompositionExclusions.txt
#     https://www.unicode.org/Public/17.0.0/ucd/DerivedNormalizationProps.txt
#     https://www.unicode.org/Public/17.0.0/ucd/UnicodeData.txt
#
# Output file:
#     tools/_unicode_data.py
#
# The resulting output file must be copied into the `pyunormalize`
# package directory.

import os
import urllib.request

UNICODE_VERSION = "17.0.0"

# Define working path
ROOT = os.path.dirname(os.path.abspath(__file__))

# Useful script context info
SCRIPT_PATH = "/".join(os.path.normpath(__file__).split(os.sep)[-3:])

# Files from the Unicode character database (UCD)
COMPOSITION_EXCLUSIONS_TXT = "CompositionExclusions.txt"
DERIVED_NORMALIZATION_PROPS_TXT = "DerivedNormalizationProps.txt"
UNICODE_DATA_TXT = "UnicodeData.txt"


def read_remote(filename):
    url = f"https://www.unicode.org/Public/{UNICODE_VERSION}/ucd/{filename}"

    print(f".. Fetching {url}")
    with urllib.request.urlopen(url) as response:
        print(f".. Extracting data from {filename}")
        return response.read().decode("utf-8").splitlines()


def main():
    #
    # Unicode file: UnicodeData.txt
    #

    try:
        path = os.path.join(ROOT, UNICODE_DATA_TXT)
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        print(
            f"\n.. {UNICODE_DATA_TXT} not found locally. "
            f"Fetching from Unicode.org..."
        )
        lines = read_remote(UNICODE_DATA_TXT)
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
                dec_dcp.append(f'"{c}"' if c.startswith("<") else f"0x{c:0>5}")

            dcp_list.append(f"    0x{code:0>5}: [{', '.join(dec_dcp)}],")

    #
    # Unicode file: CompositionExclusions.txt
    #

    try:
        path = os.path.join(ROOT, COMPOSITION_EXCLUSIONS_TXT)
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        print(
            f"\n.. {COMPOSITION_EXCLUSIONS_TXT} not found locally. "
            f"Fetching from Unicode.org..."
        )
        lines = read_remote(COMPOSITION_EXCLUSIONS_TXT)
        print(".. Done.")

    assert UNICODE_VERSION in lines[0], "Unicode version mismatch"

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
        path = os.path.join(ROOT, DERIVED_NORMALIZATION_PROPS_TXT)
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        print(
            f"\n.. {DERIVED_NORMALIZATION_PROPS_TXT} not found locally. "
            f"Fetching from Unicode.org..."
        )
        lines = read_remote(DERIVED_NORMALIZATION_PROPS_TXT)
        print(".. Done.")

    assert UNICODE_VERSION in lines[0], "Unicode version mismatch"

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


    decomp_by_character = "\n".join(dcp_list)
    non_zero_ccc_table = "\n".join(ccc_list)
    composition_exclusions = "\n".join(exclusions_list)
    NFD__QC_NO = "\n".join(NFD_QC_NO_list)
    NFC__QC_NO = "\n".join(NFC_QC_NO_list)
    NFC__QC_MAYBE = "\n".join(NFC_QC_MAYBE_list)
    NFKD_QC_NO = "\n".join(NFKD_QC_NO_list)
    NFKC_QC_NO = "\n".join(NFKC_QC_NO_list)
    NFKC_QC_MAYBE = "\n".join(NFKC_QC_MAYBE_list)

    output_path = os.path.join(ROOT, "_unicode_data.py")
    with open(output_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(f'''\
"""Data derived from the Unicode character database (UCD).

Assembled using {SCRIPT_PATH}
"""

_UNICODE_VERSION = "{UNICODE_VERSION}"

# --- DECOMPOSITION ---
# Dictionary mapping code points to their canonical decomposition sequence,
# excluding Hangul syllables
_DECOMP_BY_CHARACTER = {{
{decomp_by_character}
}}

# --- CANONICAL ORDERING ---
# Dictionary mapping code points to their canonical combining class value,
# excluding entries where ccc = 0
_NON_ZERO_CCC_TABLE = {{
{non_zero_ccc_table}
}}

# --- COMPOSITION ---
# Set of code points excluded from composition
_COMPOSITION_EXCLUSIONS = {{
{composition_exclusions}
}}

# --- NFC QUICK CHECK ---
# Set of code points where NFC_Quick_Check=No,
# i.e., characters that cannot ever occur in the normalization form C
_NFC__QC_NO = {{
{NFC__QC_NO}
}}

# Set of code points where NFC_Quick_Check=Maybe,
# i.e., characters that may or may not occur in the normalization form C,
# depending on the context
_NFC__QC_MAYBE = {{
{NFC__QC_MAYBE}
}}

# Set of code points listed for NFC_Quick_Check=No or NFC_Quick_Check=Maybe
_NFC__QC_NO_OR_MAYBE = _NFC__QC_NO | _NFC__QC_MAYBE

# --- NFD QUICK CHECK ---
# Set of code points where NFD_Quick_Check=No,
# i.e., characters that cannot ever occur in the normalization form D
_NFD__QC_NO = {{
{NFD__QC_NO}
}}

# --- NFKC QUICK CHECK ---
# Set of code points where NFKC_Quick_Check=No,
# i.e., characters that cannot ever occur in the normalization form KC
_NFKC_QC_NO = {{
{NFKC_QC_NO}
}}

# Set of code points where NFKC_Quick_Check=Maybe,
# i.e., characters that may or may not occur in the normalization form KC,
# depending on the context
_NFKC_QC_MAYBE = {{
{NFKC_QC_MAYBE}
}}

# Set of code points listed for NFKC_Quick_Check=No or NFKC_Quick_Check=Maybe
_NFKC_QC_NO_OR_MAYBE = _NFKC_QC_NO | _NFKC_QC_MAYBE

# --- NFKD QUICK CHECK ---
# Set of code points where NFKD_Quick_Check=No,
# i.e., characters that cannot ever occur in the normalization form KD
_NFKD_QC_NO = {{
{NFKD_QC_NO}
}}

# Cleanup intermediate variables
del _NFC__QC_NO, _NFC__QC_MAYBE, _NFKC_QC_NO, _NFKC_QC_MAYBE
''')


if __name__ == "__main__":
    main()
