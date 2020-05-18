# -*- coding: utf-8 -*-
"""pyunormalize.core"""

from pyunormalize import data

# Full canonical decomposition mappings [dict]
cdecomp = data.cdecomp

# Full compatibility decomposition mappings [dict]
kdecomp = data.kdecomp

# Precomposed characters (canonical composites) [dict]
precomp_chars = data.precomp_chars

# Non-zero canonical combining class values [dict]
ccc = data.ccc

# Characters excluded from composition [set]
comp_excl = data.comp_excl

# Characters excluded from full composition [set]
full_comp_excl = data.full_comp_excl

# Code points that may compose with a previous character [set]
comp_with_prev = data.comp_with_prev

# Hangul constants
_SFIRST, _SLAST = 0xAC00, 0xD7A3  # Hangul syllables for modern Korean
_LFIRST, _LLAST = 0x1100, 0x1112  # leading consonants (syllable onsets)
_VFIRST, _VLAST = 0x1161, 0x1175  # vowels (syllable nucleuses)
_TFIRST, _TLAST = 0x11A8, 0x11C2  # trailing consonants (syllable codas)
_TSTART = 0x11A7                  # one less than _TFIRST
_VCOUNT = 0x1175 - 0x1161 + 1     # 21
_TCOUNT = 0x11C2 - 0x11A7 + 1     # 28


#
# Quick verification check
#

def check_NFC(unistr):
    """Quick check for Normalization Form C. Quickly determine whether
    the Unicode string `unistr` is in NFC. The result is either True,
    False, or None. For True or False, the answer is definite; in the
    None case, the check was inconclusive (maybe yes, maybe no).

    Examples:

    >>> from pyunormalize import check_NFC
    >>> check_NFC("한국")
    True
    >>> s = "e\u0340"
    >>> check_NFC(s)
    False
    >>> s = "e\u0300"
    >>> check_NFC(s)
    >>> print(check_NFC(s))
    None
    """
    maybe = False
    curr_ccc, prev_ccc = 0, 0
    for u in unistr:
        u = ord(u)
        if u in ccc:
            curr_ccc = ccc[u]
            if curr_ccc < prev_ccc:
                return False
        if u in comp_with_prev:
            maybe = True
        if u in full_comp_excl:
            return False
        prev_ccc, curr_ccc = curr_ccc, 0

    return None if maybe else True


def check_NFD(unistr):
    """Quick check for Normalization Form D. Quickly determine whether
    the Unicode string `unistr` is in NFD. The result is either True or
    False.

    Examples:

    >>> from pyunormalize import check_NFD
    >>> check_NFD("한국")
    False
    >>> s = "".join(["ᄒ", "ᅡ", "ᆫ", "ᄀ", "ᅮ", "ᆨ"])
    >>> check_NFD(s)
    True
    """
    curr_ccc, prev_ccc = 0, 0
    for u in unistr:
        u = ord(u)
        if u in cdecomp or _SFIRST <= u <= _SLAST:
            return False
        if u in ccc:
            curr_ccc = ccc[u]
            if curr_ccc < prev_ccc:
                return False
        prev_ccc, curr_ccc = curr_ccc, 0

    return True


def _nfkc_no(cp):
    if cp in full_comp_excl:
        return True
    if cp not in kdecomp or _SFIRST <= cp <= _SLAST:
        return False
    if cp not in cdecomp:
        return True

    return cdecomp[cp] != kdecomp[cp]


def check_NFKC(unistr):
    """Quick check for Normalization Form KC. Quickly determine whether
    the Unicode string `unistr` is in NFKC. The result is either True,
    False, or None. For True or False, the answer is definite; in the
    None case, the check was inconclusive (maybe yes, maybe no).
    """
    maybe = False
    curr_ccc, prev_ccc = 0, 0
    for u in unistr:
        u = ord(u)
        if u in ccc:
            curr_ccc = ccc[u]
            if curr_ccc < prev_ccc:
                return False
        if u in comp_with_prev:
            maybe = True
        if _nfkc_no(u):
            return False
        prev_ccc, curr_ccc = curr_ccc, 0

    return None if maybe else True


def check_NFKD(unistr):
    """Quick check for Normalization Form KD. Quickly determine whether
    the Unicode string `unistr` is in NFKD. The result is either True
    or False.
    """
    curr_ccc, prev_ccc = 0, 0
    for u in unistr:
        u = ord(u)
        if u in kdecomp or _SFIRST <= u <= _SLAST:
            return False
        if u in ccc:
            curr_ccc = ccc[u]
            if curr_ccc < prev_ccc:
                return False
        prev_ccc, curr_ccc = curr_ccc, 0

    return True


_cfunc = {
    "NFC": check_NFC, "NFD": check_NFD, "NFKC": check_NFKC, "NFKD": check_NFKD
}


def check(form, unistr):
    """Quickly determine whether the Unicode string `unistr` is in the
    Unicode normalization form `form`. Valid values for `form` are
    "NFC", "NFD", "NFKC", and "NFKD". The result is either True, False,
    or None. For True or False, the answer is definite; in the None
    case, the check was inconclusive (maybe yes, maybe no). The check
    function will always produce a definite result for the
    normalization forms D and KD.

    Examples:

    >>> from pyunormalize import check
    >>> s = "한국"
    >>> check("NFC", s)
    True
    >>> check("NFD", s)
    False
    >>> 
    >>> forms = ["NFC", "NFD", "NFKC", "NFKD"]
    >>> s = "\u1E9B\u0323"
    >>> [check(f, s) for f in forms]
    [None, False, False, False]
    """
    return _cfunc[form](unistr)

#
# Normalization
#

def NFC(unistr):
    """Return the canonical equivalent "composed" form of the original
    Unicode string `unistr`. That is, transform the Unicode string into
    the Unicode "Normalization Form C": character sequences are
    replaced by canonically equivalent composites, where possible;
    compatibility characters are unaffected.

    Examples:

    >>> from pyunormalize import NFC
    >>> s = "".join(["ᄒ", "ᅡ", "ᆫ", "ᄀ", "ᅮ", "ᆨ"])
    >>> nfc = NFC(s)
    >>> nfc
    '한국'
    >>> len(nfc)
    2
    >>> [*nfc]
    ['한', '국']
    >>> 
    >>> NFC("ﬃ")
    'ﬃ'
    """
    res = _compose(_reorder(_decompose(unistr)))
    return "".join(map(chr, res))


def NFD(unistr):
    """Return the canonical equivalent "decomposed" form of the
    original Unicode string `unistr`. That is, transform the Unicode
    string into the Unicode "Normalization Form D": composite
    characters are replaced by canonically equivalent character
    sequences, in canonical order; compatibility characters are
    unaffected.

    Examples:

    >>> from pyunormalize import NFD
    >>> s = "한국"
    >>> nfd = NFD(s)
    >>> nfd
    '한국'
    >>> len(nfd)
    6
    >>> [*nfd]
    ['ᄒ', 'ᅡ', 'ᆫ', 'ᄀ', 'ᅮ', 'ᆨ']
    >>>
    >>> NFD("ⓕ")
    'ⓕ'
    """
    res = _reorder(_decompose(unistr))
    return "".join(map(chr, res))


def NFKC(unistr):
    """Return the compatibility equivalent "composed" form of the
    original Unicode string `unistr`. That is, transform the Unicode
    string into the Unicode "Normalization Form KC": character
    sequences are replaced by canonically equivalent composites, where
    possible; compatibility characters are replaced by their nominal
    counterparts.

    Examples:

    >>> from pyunormalize import NFKC
    >>> NFKC("ﬃ")
    'ffi'
    >>> s = "".join(["ハ", "゚", "ヒ", "゚", "フ", "゚", "ヘ", "゚", "ホ", "゚"])
    >>> s
    'パピプペポ'
    >>> len(s)
    10
    >>> nfkc = NFKC(s)
    >>> len(nfkc)
    5
    >>> [*nfkc]
    ['パ', 'ピ', 'プ', 'ペ', 'ポ']
    """
    res = _compose(_reorder(_decompose(unistr, compat=True)))
    return "".join(map(chr, res))


def NFKD(unistr):
    """Return the compatibility equivalent "decomposed" form of the
    original Unicode string `unistr`. That is, transform the Unicode
    string into the Unicode "Normalization Form KD": composite
    characters are replaced by canonically equivalent character
    sequences, in canonical order; compatibility characters are
    replaced by their nominal counterparts.

    Examples:

    >>> from pyunormalize import NFKD
    >>> NFKD("ⓕ")
    'f'
    >>> s = "パピプペポ"
    >>> len(s)
    5
    >>> nfkd = NFKD(s)
    >>> len(nfkd)
    10
    >>> [*nfkd]
    ['ハ', '゚', 'ヒ', '゚', 'フ', '゚', 'ヘ', '゚', 'ホ', '゚']
    """
    res = _reorder(_decompose(unistr, compat=True))
    return "".join(map(chr, res))


_nfunc = {"NFC": NFC, "NFD": NFD, "NFKC": NFKC, "NFKD": NFKD}


def normalize(form, unistr):
    """Transform the Unicode string `unistr` into the Unicode
    normalization form `form`. Valid values for `form` are "NFC",
    "NFD", "NFKC", and "NFKD".

    Examples:

    >>> from pyunormalize import normalize
    >>> normalize("NFKC", "ﬃ")
    'ffi'
    >>> s = "\u1E9B\u0323"
    >>> forms = ["NFC", "NFD", "NFKC", "NFKD"]
    >>> frmt = "{:04X}".format
    >>> for f in forms:
    ...     normalized = normalize(f, s)
    ...     tmp = " ".join([frmt(ord(x)) for x in normalized])
    ...     "{:<4} : {}".format(f, tmp)
    ...
    'NFC  : 1E9B 0323'
    'NFD  : 017F 0323 0307'
    'NFKC : 1E69'
    'NFKD : 0073 0323 0307'
    """
    return _nfunc[form](unistr)

#
# Internals
#

def _decompose(unistr, compat=None):
    # Computes the full decomposition of the Unicode string. The type of full
    # decomposition chosen depends on which Unicode normalization form is
    # involved. For NFC or NFD, one does a full canonical decomposition. For
    # NFKC or NFKD, one does a full compatibility decomposition.

    decomp = kdecomp if compat else cdecomp
    res = []
    for u in unistr:
        u = ord(u)
        if u in decomp:
            res.extend(decomp[u])
        elif _SFIRST <= u <= _SLAST:
            res.extend(_decompose_hangul_syllable(u))
        else:
            res.append(u)

    return res


def _decompose_hangul_syllable(cp):
    # Hangul Syllable Decomposition Algorithm. Arithmetically derives the full
    # canonical decomposition of a precomposed Hangul syllable.

    s_index = cp - _SFIRST
    t_index = s_index % _TCOUNT
    _ = (s_index - t_index) // _TCOUNT
    V = _VFIRST + (_  % _VCOUNT)
    L = _LFIRST + (_ // _VCOUNT)

    if t_index:  # LVT syllable
        return (L, V, _TSTART + t_index)

    # LV syllable
    return (L, V)


def _reorder(items):
    # Canonical Ordering Algorithm. Once a string has been fully decomposed,
    # any sequences of combining marks that it contains are put into a
    # well-defined order. Only the subset of combining marks which have
    # non-zero Canonical_Combining_Class property values are subject to
    # potential reordering by the Canonical Ordering Algorithm. Both the
    # composed and decomposed normalization forms impose a canonical ordering
    # on the code point sequence, which is necessary for the normal forms to be
    # unique.

    for i, j in enumerate(items):
        if j not in ccc:  # character is a starter
            continue
        idx = i
        while i < len(items) and items[i] in ccc:
            i += 1
        if i == idx + 1:
            continue
        ind = [*range(idx, i)]
        tmp = sorted(ind, key=lambda x: ccc[items[x]])
        if ind != tmp:
            items[idx:i] = [items[x] for x in tmp]

    return items


def _compose(items):
    # Canonical Composition Algorithm. That process transforms the fully
    # decomposed and canonically ordered string into its most fully composed
    # but still canonically equivalent sequence.

    for i, x in enumerate(items):
        if x is None or x in ccc:
            continue

        j = i + 1
        blocked = uncomp = False
        while j < len(items) and not blocked:
            y = items[j]
            if y in ccc:
                uncomp = True
            else:
                blocked = True

            if blocked and uncomp:
                j += 1
                continue

            z = items[j - 1]
            if z is not None and z in ccc and ccc[z] >= ccc[y]:
                j += 1
                continue

            pair = (x, y)
            if pair in precomp_chars:
                precomp = precomp_chars[pair]
            else:
                precomp = _compose_jamo_characters(pair)  # may be None

            if precomp is None or precomp in comp_excl:
                j += 1
                continue

            items[i] = x = precomp  # precomp is a primary composite
            items[j] = None
            if blocked:
                blocked = False
            else:
                uncomp = False
            j += 1

    if None in items:
        return [e for e in items if e is not None]

    return items


def _compose_jamo_characters(pair):
    # Hangul Syllable Composition Algorithm. Arithmetically derives the
    # mapping of a canonically decomposed sequence of Hangul jamo characters
    # to an equivalent precomposed Hangul syllable.

    x, y = pair

    if (_LFIRST <= x <= _LLAST and
        _VFIRST <= y <= _VLAST):
        # Compose a leading consonant and a vowel together into an LV syllable
        l_idx = x - _LFIRST
        v_idx = y - _VFIRST
        return _SFIRST + ((l_idx * _VCOUNT) + v_idx) * _TCOUNT

    if (_SFIRST <= x <= _SLAST and
        _TFIRST <= y <= _TLAST and not (x - _SFIRST) % _TCOUNT):
        # Compose an LV syllable and a trailing consonant into an LVT syllable
        return x + y - _TSTART

    return None


if __name__ == "__main__":
    import doctest
    doctest.testmod()
