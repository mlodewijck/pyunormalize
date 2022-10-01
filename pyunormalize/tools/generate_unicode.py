# This script generates the pyunormalize.unicode module.
#
# Input files:
#     https://www.unicode.org/Public/15.0.0/ucd/CompositionExclusions.txt
#     https://www.unicode.org/Public/15.0.0/ucd/DerivedNormalizationProps.txt
#     https://www.unicode.org/Public/15.0.0/ucd/UnicodeData.txt
#
# Output file:
#     tools/generate_unicode/unicode.py
#
# The output file must be copied to the *pyunormalize* directory.

import pathlib
import urllib.error
import urllib.request

UNICODE_VERSION = "15.0.0"
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

    print(".. Extracting data...")
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
    for item in lines:
        code, name, _, ccc, _, dcp, *_ = item.split(";", 6)
        if ccc != "0":
            ccc_list.append(f"    0x{code:0>5}: {ccc:>3},  # {name}")
        if dcp:
            dec_dcp = []
            for c in dcp.split(" "):
                dec_dcp.append(f'"{c}"' if c.startswith("<") else f"0x{c}")
            dcp_list.append(
                f"    0x{code:0>5}: [{', '.join(dec_dcp)}],  # {name}"
            )

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
    for item in lines:
        item = item.rstrip()
        if item and not item.startswith("#"):
            code, name = item.split("#")
            exclusions_list.append(
                f"    0x{code.rstrip():0>5},  # {name.lstrip()}"
            )

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

    NFD_QC_NO_list  = []
    NFKD_QC_NO_list = []
    NFC_QC_NO_list  = []
    NFC_QC_MAYBE_list  = []
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
        # ['00C0..00C5    ', ' NFD_QC', ' N']
        data = [d.strip() for d in data]
        # ['00C0..00C5', 'NFD_QC', 'N']
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
            tmp_list.append(f"    0x{code:0>5},")


    dcp = "\n".join(dcp_list)
    ccc = "\n".join(ccc_list)
    exclusions = "\n".join(exclusions_list)
    NFD_QC_N   = "\n    ".join(NFD_QC_NO_list)
    NFKD_QC_N  = "\n    ".join(NFKD_QC_NO_list)
    NFC_QC_N   = "\n    ".join(NFC_QC_NO_list)
    NFC_QC_M   = "\n    ".join(NFC_QC_MAYBE_list)
    NFKC_QC_N  = "\n    ".join(NFKC_QC_NO_list)
    NFKC_QC_M  = "\n    ".join(NFKC_QC_MAYBE_list)

    with open(cwd / "unicode.py", "w", encoding="utf-8", newline="\n") as f:
        f.write(f'''\
"""Data derived from the Unicode character database (UCD).

This file was generated from {SCRIPT_PATH}
"""

UNICODE_VERSION = "{UNICODE_VERSION}"

# Character decomposition mappings (not including Hangul syllables)
_DECOMP = {{
{dcp}
}}

# Non-zero canonical combining class values
_CCC = {{
{ccc}
}}

# Composition exclusions
_COMP_EXCL = {{
{exclusions}
}}

# Quick_Check property values
_QC_PROP_VAL = {{

    # NFD_Quick_Check=No
    # Characters that cannot ever occur in the normalization form D
    "NFD_QC=N": set([
    {NFD_QC_N}
    ]),

    # NFKD_Quick_Check=No
    # Characters that cannot ever occur in the normalization form KD
    "NFKD_QC=N": set([
    {NFKD_QC_N}
    ]),

    # NFC_Quick_Check=No
    # Characters that cannot ever occur in the normalization form C
    "NFC_QC=N": set([
    {NFC_QC_N}
    ]),

    # NFC_Quick_Check=Maybe
    # Characters that may or may not occur in the normalization form C,
    # depending on the context
    "NFC_QC=M": set([
    {NFC_QC_M}
    ]),

    # NFKC_Quick_Check=No
    # Characters that cannot ever occur in the normalization form KC
    "NFKC_QC=N": set([
    {NFKC_QC_N}
    ]),

    # NFKC_Quick_Check=Maybe
    # Characters that may or may not occur in the normalization form KC,
    # depending on the context
    "NFKC_QC=M": set([
    {NFKC_QC_M}
    ]),
}}
''')


if __name__ == "__main__":
    main()
