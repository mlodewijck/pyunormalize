import os.path
import re
import sys
import urllib.error
import urllib.request

# The Unicode Standard used to process the data
UNICODE_VERSION = "13.0.0"

# The Unicode Character Database
UCD_VERSION = UNICODE_VERSION

# Files from UCD
DATA = "UnicodeData.txt"
CEXL = "CompositionExclusions.txt"


def _url(url):
    try:
        print("\nFetching URL...")
        with urllib.request.urlopen(url) as f:
            print("Extracting data...", end=" ")
            return f.read().decode("utf-8").splitlines()
    except urllib.error.HTTPError as e:
        sys.exit(
            "The server couldn't fulfill the request.\n"
            "Error code: {}\n".format(e.code))
    except urllib.error.URLError as e:
        sys.exit(
            "We failed to reach a server.\n"
            "Reason: {}\n".format(e.reason))


def main():
    dir_path = os.path.dirname(__file__)
    here = "https://www.unicode.org/Public/" + UCD_VERSION + "/ucd/"

    ##
    ## Unicode file: UnicodeData.txt
    ##

    path = os.path.join(dir_path, DATA)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    else:
        url = here + DATA
        lines = _url(url)
        print("Done.")

    # File version is not specified in UnicodeData.txt
    # and therefore cannot be checked.

    ccc = []
    dcp = []
    kfrmt = '"{}"'.format
    cfrmt = "0x{}".format
    ccc_frmt = "    {:<8}: {:>3},  # {}".format
    dcp_frmt = "    {:<8}: [{}],  # {}".format
    for item in lines:
        #00D9;LATIN CAPITAL LETTER U WITH GRAVE;Lu;0;L;0055 0300;;;;N;LATIN CAPITAL LETTER U GRAVE;;;00F9;
        data = item.split(";", 6)
        code = data[0]
        name = data[1]
        ccc_ = data[3]
        dcp_ = data[5]
        if ccc_ != "0":
            ccc.append(ccc_frmt("0x" + code, ccc_, name))
        if dcp_:
            dec_dcp = []
            for c in dcp_.split(" "):
                dec_dcp.append(kfrmt(c)) if c.startswith("<") else dec_dcp.append(cfrmt(c))
            dcp.append(dcp_frmt("0x" + code, ", ".join(dec_dcp), name))

    ##
    ## Unicode file: CompositionExclusions.txt
    ##

    path = os.path.join(dir_path, CEXL)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    else:
        url = here + CEXL
        lines = _url(url)
        print("Done.")

    # Check file version
    assert re.match(
        "^#.*{}-(.+).txt.*$".format(CEXL[:-4]), lines[0]
    ).group(1) == UCD_VERSION

    excl = []
    excl_frmt = "    {:<8}  # {}".format
    for item in lines:
        item = item.rstrip()
        if item and not item.startswith("#"):
            code, name = item.split("#")
            excl.append(excl_frmt("0x" + code.rstrip() + ",", name.lstrip()))


    filename = os.path.basename(__file__).split("_", 1)[1]

    with open(filename, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("""\
\"\"\"Data derived from the Unicode Character Database.

UCD Version: {0}
\"\"\"

# Character decomposition mappings
decomposition_mappings = {{
{1}
}}

# Non-zero canonical combining class values
combining_class_values = {{
{2}
}}

# Composition exclusions
composition_exclusions = {{
{3}
}}
""".format(UCD_VERSION, "\n".join(dcp), "\n".join(ccc), "\n".join(excl)))


if __name__ == "__main__":
    main()
