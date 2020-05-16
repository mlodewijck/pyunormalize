"""pyunormalize.data"""

__all__ = [
    "cdecomp",
    "kdecomp",
    "comp_excl",
    "full_comp_excl",
    "precomp_chars",
    "comp_with_prev",
    "ccc"
]

from pyunormalize import unicode

# Character decomposition mappings [dict]
decomp = unicode.decomposition_mappings

# Non-zero canonical combining class values [dict]
ccc = unicode.combining_class_values

# Characters excluded from composition [set]
comp_excl = unicode.composition_exclusions

# Hangul constants
_VFIRST, _VLAST = 0x1161, 0x1175  # vowels (syllable nucleuses)
_TFIRST, _TLAST = 0x11A8, 0x11C2  # trailing consonants (syllable codas)


cdecomp = {}  # canonical decompositions
kdecomp = {}  # compatibility decompositions
precomp_chars = {}  # precomposed characters (canonical composites)
COMP_EXCL_ADD = []  # non-starter and singleton decompositions

comp_with_prev = set([  # may compose with a previous character
    *range(_VFIRST, _VLAST + 1),
    *range(_TFIRST, _TLAST + 1)
])

for key in decomp:
    val = decomp[key]
    if isinstance(val[0], int):
        #assert len(val) in (1, 2)  # checked
        cdecomp[key] = kdecomp[key] = val
        if len(val) == 1 or val[0] in ccc:  # singleton or non-starter
            COMP_EXCL_ADD.append(key)
        else:
            precomp_chars[tuple(val)] = key
            if key not in comp_excl:
                comp_with_prev.add(val[1])
    else:
        kdecomp[key] = val[1:]

# Full composition exclusions
full_comp_excl = comp_excl | set(COMP_EXCL_ADD)


def _full_decomposition(decomp_dict):
    # A full decomposition of a character sequence results from decomposing
    # each of the characters in the sequence until no characters can be further
    # decomposed.

    for key in decomp_dict:
        tmp = []
        decomposition = [key]
        while True:
            for x in decomposition:
                if x in decomp_dict:
                    tmp.extend(decomp_dict[x])
                else:
                    tmp.append(x)

            if tmp == decomposition:
                decomp_dict[key] = decomposition  # done
                break

            decomposition, tmp = tmp, []


# Full canonical decomposition
_full_decomposition(cdecomp)

# Full compatibility decomposition
_full_decomposition(kdecomp)
