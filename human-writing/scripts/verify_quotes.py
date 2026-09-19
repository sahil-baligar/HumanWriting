#!/usr/bin/env python3
"""
verify_quotes.py - check every quotation in an essay against the source text.

A quotation passes only if it appears in the source word for word and letter
for letter. Line breaks and runs of spaces are the one thing forgiven, because
PDF extraction and hard wrapping put them in places the author never did.
Everything else counts: spelling, capitals, punctuation, and the difference
between a straight and a curly apostrophe.

Each quotation must also be followed by a citation in the form (Author, page).

Usage
    python verify_quotes.py essay.md source.txt
    python verify_quotes.py essay.md book.txt --pages      # check page numbers
    python verify_quotes.py essay.md book.txt --pages --page-offset 12
    python verify_quotes.py essay.md a.txt b.txt --json

The source must be plain text. For a PDF, extract it first, keeping page
breaks as form feeds:
    pdftotext -layout book.pdf book.txt
With --pages, page N is the text after the (N-1)th form feed, plus the offset
for front matter printed with its own numbering.

Exit status is 1 if any quotation fails, so it can gate a pipeline.
Stdlib only. Python 3.8+.
"""

import argparse
import difflib
import json
import re
import sys

VERSION = "2.1.0"

QUOTE_RE = re.compile(r'"([^"\n]+)"|“([^”\n]+)”')
CITE_RE = re.compile(
    r'^\s*\(\s*([^(),]+?)\s*,\s*(?:pp?\.\s*)?([0-9ivxlcdm]+(?:\s*[-–]\s*[0-9ivxlcdm]+)?)\s*\)',
    re.I)
TYPO = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"',
                      "–": "-", "—": "-", " ": " "})
MIN_WORDS = 3


def squash(s):
    return re.sub(r"\s+", " ", s).strip()


def find_whole(hay, needle):
    """Offset of needle in hay, refusing matches that cut a word in half."""
    if not needle:
        return -1
    pat = re.escape(needle)
    if needle[0].isalnum():
        pat = r"(?<!\w)" + pat
    if needle[-1].isalnum():
        pat += r"(?!\w)"
    m = re.search(pat, hay)
    return m.start() if m else -1


def page_of(pages, idx):
    """1-based page index of a character offset in the squashed source."""
    for n, (start, end) in enumerate(pages, 1):
        if start <= idx < end:
            return n
    return None


def load_sources(paths):
    text, pages = "", []
    for p in paths:
        raw = open(p, encoding="utf-8").read()
        for chunk in raw.split("\f"):
            s = squash(chunk)
            start = len(text)
            text += s + " "
            pages.append((start, len(text)))
    return text, pages


def closest(needle, hay):
    """Best-matching window of the source, for showing what the quote got wrong."""
    words = hay.split(" ")
    n = len(needle.split(" "))
    best, best_r = "", 0.0
    first = needle.split(" ")[0].lower()
    for i, w in enumerate(words):
        if w.lower() != first and i % 8:
            continue
        cand = " ".join(words[i:i + n])
        r = difflib.SequenceMatcher(None, needle, cand).ratio()
        if r > best_r:
            best, best_r = cand, r
    return best, round(best_r, 2)


def page_matches(cited, found, offset):
    if found is None:
        return None
    nums = [int(x) for x in re.findall(r"\d+", cited)]
    if not nums:
        return None  # roman numerals: front matter, not checked
    lo, hi = nums[0], nums[-1]
    return lo <= found - offset <= hi


def check(essay, src, pages, use_pages, offset):
    results = []
    for m in QUOTE_RE.finditer(essay):
        q = m.group(1) or m.group(2)
        body = squash(q)
        r = {"quote": body, "line": essay.count("\n", 0, m.start()) + 1}
        cite = CITE_RE.match(essay[m.end():m.end() + 120])
        r["citation"] = f"({cite.group(1)}, {cite.group(2)})" if cite else None

        # Strip trailing punctuation that belongs to the essay's sentence, not
        # the quotation, when the source does not have it there.
        idx = find_whole(src, body)
        if idx < 0 and body[-1:] in ",.":
            idx = find_whole(src, body[:-1])
        if idx >= 0:
            r["status"] = "exact"
        elif find_whole(src.translate(TYPO), body.translate(TYPO)) >= 0:
            r["status"] = "typography"
            r["note"] = "Matches only if quote marks, apostrophes or dashes are normalised. Copy them from the source exactly."
        else:
            r["status"] = "not found"
            r["closest"], r["similarity"] = closest(body, src)

        short = len(body.split()) < MIN_WORDS
        if short and r["status"] != "exact":
            r["status"] = "short"
            r["note"] = "Under three words. Scare quotes and titles are not checked, but a real quotation must still match."

        if r["status"] == "exact" and not cite and not short:
            r["status"] = "no citation"
            r["note"] = "Follow the closing quotation mark with (Author, page)."

        if use_pages and cite and idx >= 0:
            found = page_of(pages, idx)
            ok = page_matches(cite.group(2), found, offset)
            r["found_page"] = None if found is None else found - offset
            if ok is False:
                r["status"] = "wrong page"
                r["note"] = f"Cited {cite.group(2)}, found on page {found - offset}."
        results.append(r)
    return results


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("essay")
    ap.add_argument("sources", nargs="+", help="plain-text source files")
    ap.add_argument("--pages", action="store_true",
                    help="check cited pages against form-feed page breaks")
    ap.add_argument("--page-offset", type=int, default=0,
                    help="physical page minus printed page number")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    essay = open(a.essay, encoding="utf-8").read()
    src, pages = load_sources(a.sources)
    res = check(essay, src, pages, a.pages, a.page_offset)
    failed = [r for r in res if r["status"] not in ("exact", "short")]

    if a.json:
        out = json.dumps({"version": VERSION, "quotes": res, "failed": len(failed)},
                         indent=2, ensure_ascii=False)
    else:
        L = [f"verify_quotes {VERSION}: {len(res)} quotations, {len(failed)} failed", ""]
        for r in res:
            mark = "ok  " if r["status"] in ("exact", "short") else "FAIL"
            L.append(f"{mark} line {r['line']:<4} [{r['status']}] \"{r['quote'][:70]}\" "
                     f"{r['citation'] or '(no citation)'}")
            if r.get("note"):
                L.append(f"          {r['note']}")
            if r.get("closest"):
                L.append(f"          source has: \"{r['closest'][:90]}\" "
                         f"(similarity {r['similarity']})")
        out = "\n".join(L)
    try:
        print(out)
    except UnicodeEncodeError:
        sys.stdout.buffer.write(out.encode("utf-8", "replace") + b"\n")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
