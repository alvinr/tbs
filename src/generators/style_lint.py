# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""style_lint.py — TBS-001 voice & terseness checker (manual, advisory).

The §F "Voice" pass from skills/skill_report_writing.md, made checkable. It flags the
robotic tells (hedging, filler, stock-marketing phrasing) and reports prose word count /
bloat so a terseness pass has a worklist. It NEVER rewrites an engineering value — it points.

Two tracks (the split is read from docs/editorial-review-todo.md, the single source):
  Track 2 — personal/engaging (project-summary.md + funding-proposal.md).
  Track 1 — terse engineering (everything else reader-facing).

Advisory only — NOT in the commit hook. Run by hand:

    python3 src/generators/style_lint.py                 # all tracked docs, ranked by tells
    python3 src/generators/style_lint.py water-system-report.md   # one doc, with line numbers
    python3 src/generators/style_lint.py --track2        # just Home + Proposal
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, cwd=HERE).stdout.strip() or os.path.join(HERE, "..", "..")
DOCS = os.path.join(ROOT, "docs")
TRACKER = os.path.join(DOCS, "editorial-review-todo.md")

# ── robotic tells (advisory, both tracks) ────────────────────────────────────
# (label, regex) — case-insensitive, word-bounded. Kept conservative; false positives
# are cheap because the human reviews every hit.
TELLS = [
    ("hedge: aim to",            r"\baim(?:s|ed)? to\b"),
    ("hedge: look forward to",   r"\blook(?:ing)? forward to\b"),
    ("filler: it is important",  r"\bit is important to note\b|\bit should be noted\b|\bit's worth noting\b"),
    ("wordy: in order to",       r"\bin order to\b"),
    ("wordy: due to the fact",   r"\bdue to the fact that\b"),
    ("wordy: a number of",       r"\ba number of\b"),
    ("wordy: in terms of",       r"\bin terms of\b"),
    ("wordy: serves to",         r"\bserves? to\b"),
    ("wordy: for the purpose of", r"\bfor the purpose(s)? of\b"),
    ("wordy: utilize",           r"\butiliz(e|es|ed|ing)\b"),
    ("wordy: facilitate",        r"\bfacilitat(e|es|ed|ing)\b"),
    ("vague: a variety/range of", r"\ba (?:variety|range|number|host|plethora) of\b"),
    ("vague: various/numerous",  r"\b(?:various|numerous|myriad)\b"),
    ("market: step forward",     r"\bsignificant step forward\b|\bgreat leap\b"),
    ("market: lays foundation",  r"\blay(?:s|ing)? (?:the|a) (?:ground|found)work\b|\blays? the foundation\b"),
    ("market: seamless",         r"\bseamless(ly)?\b"),
    ("market: robust",           r"\brobust\b"),
    ("market: best-in-class",    r"\b(?:best-in-class|world-class|state-of-the-art|cutting-edge)\b"),
    ("market: game-changer",     r"\bgame[- ]chang(?:er|ing)\b|\brevolutioniz\w*\b"),
    ("market: empower/supercharge", r"\b(?:empower|supercharge)\w*\b"),
    ("market: leverage (verb)",  r"\bleverag(e|es|ed|ing)\b"),
]
TELLS = [(label, re.compile(pat, re.IGNORECASE)) for label, pat in TELLS]
CONTRACTION = re.compile(r"\b\w+'(?:s|t|re|ve|ll|d|m)\b", re.IGNORECASE)
FIRST_PERSON = re.compile(r"\b(?:I|I'm|I've|I'd|my|we|we're|we've|our)\b")

# ── terseness candidates (learned from editorial corrections) ────────────────
# A sentence longer than this reads as a windup to tighten; and a parenthetical that
# dumps ≥3 measurement tokens is usually detail the diagram-of-record already carries
# (the kind of "(each 4,049mm … 3,048mm)" / "(WF5, 610mm centers)" aside cut by hand).
LONG_SENTENCE_WORDS = 40
MEASURE = re.compile(r"\b\d[\d,]*(?:\.\d+)?\s?mm\b|\b[ZX]\d{2,}\b|Ø\d|\b\d+(?:\.\d+)?\s?(?:kN|N·m)\b|\b\d+°")
PAREN = re.compile(r"\(([^()]{1,400}?)\)")
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
_WORD = re.compile(r"\b[A-Za-z][A-Za-z'-]*\b")


def tracked_docs() -> dict[str, int]:
    """Map doc path (relative to docs/) → track (1 or 2), parsed from the tracker."""
    out: dict[str, int] = {}
    if not os.path.exists(TRACKER):
        return out
    track = 0
    for line in open(TRACKER, encoding="utf-8"):
        s = line.strip()
        if s.startswith("## Track 2"):
            track = 2
        elif s.startswith("## Track 1"):
            track = 1
        elif s.startswith("## "):          # N/A / internal sections end the tracked set
            track = 0
        elif track and re.match(r"- \[[ x~]\] ", s):
            m = re.match(r"- \[[ x~]\] ([A-Za-z0-9_./-]+\.md)", s)
            if m:
                out[m.group(1)] = track
    return out


def _prose(text: str) -> str:
    """Strip the parts that aren't re-voiceable prose: code fences, tables, HTML
    comments, headings, images, link-reference/source lines, and fact/costing blocks."""
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)         # code fences
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)         # HTML comments
    kept = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s or s.startswith(("|", "#", "![", "<")):   # tables, headings, images, HTML blocks
            continue
        if s.startswith("|---") or re.match(r"^\|?[-: |]+\|", s):   # table rule
            continue
        kept.append(ln)
    return "\n".join(kept)


def _words(prose: str) -> int:
    return len(re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", prose))


def scan(path: str, track: int):
    """Return (word_count, hits, stiff, long_sentences, dim_parens)."""
    full = open(path, encoding="utf-8").read()
    prose = _prose(full)
    hits, dim_parens = [], []
    for i, ln in enumerate(full.splitlines(), 1):
        if ln.strip().startswith(("|", "#", "<!--")):
            continue
        for label, rx in TELLS:
            for m in rx.finditer(ln):
                hits.append((i, label, m.group(0)))
        for m in PAREN.finditer(ln):                      # dim-dump parentheticals
            inner = m.group(1)
            if "http" in inner or "](" in inner:          # skip markdown links / URLs
                continue
            if len(MEASURE.findall(inner)) >= 3:
                snip = inner if len(inner) <= 48 else inner[:46] + "…"
                dim_parens.append((i, f"({snip})"))
    long_sents = []                                       # sentences can span lines → scan the prose
    for block in re.split(r"\n\s*\n", prose):
        lines = block.split("\n")
        is_list = sum(bool(re.match(r"\s*[-*]|\s*\d+\.", l)) for l in lines) > len(lines) / 2
        units = lines if is_list else SENT_SPLIT.split(" ".join(lines))
        for u in units:
            if "](" in u or "http" in u:                  # skip link-heavy lines
                continue
            wc = len(_WORD.findall(u))
            if wc > LONG_SENTENCE_WORDS:
                long_sents.append((wc, u.strip().lstrip("-*0123456789. ")[:58] + "…"))
    stiff = 0
    if track == 2:                              # Track-2 stiffness: prose that reads corporate
        for para in re.split(r"\n\s*\n", prose):
            sents = [s for s in re.split(r"(?<=[.!?])\s+", para.strip()) if len(s.split()) > 3]
            if len(sents) >= 4 and not CONTRACTION.search(para) and not FIRST_PERSON.search(para):
                stiff += 1
    return _words(prose), hits, stiff, long_sents, dim_parens


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    flags = {a for a in sys.argv[1:] if a.startswith("-")}
    docs = tracked_docs()
    if not docs:
        print("No tracked docs found (is docs/editorial-review-todo.md present with Track 1/2 sections?)")
        return 0

    if "--track1" in flags:
        docs = {d: t for d, t in docs.items() if t == 1}
    if "--track2" in flags:
        docs = {d: t for d, t in docs.items() if t == 2}

    single = args[0] if args else None
    rows = []
    for rel, track in sorted(docs.items()):
        path = os.path.join(DOCS, rel)
        if not os.path.exists(path):
            continue
        if single and os.path.basename(rel) != os.path.basename(single) and rel != single:
            continue
        words, hits, stiff, longs, dims = scan(path, track)
        rows.append((rel, track, words, hits, stiff, longs, dims))

    if single and rows:
        rel, track, words, hits, stiff, longs, dims = rows[0]
        print(f"\n{rel}  (Track {track})  ·  {words} prose words  ·  {len(hits)} tells"
              + (f"  ·  {stiff} stiff para(s)" if track == 2 else "")
              + f"  ·  {len(longs)} long sent · {len(dims)} dim-dump paren")
        for ln, label, txt in hits:
            print(f"  L{ln:<4} {label:<26} “{txt}”")
        for ln, snip in dims:
            print(f"  L{ln:<4} {'dim-dump paren':<26} {snip}")
        for wc, snip in sorted(longs, reverse=True):
            print(f"  {'':<6}{'long sentence (' + str(wc) + 'w)':<26} “{snip}”")
        if not (hits or stiff or longs or dims):
            print("  clean — no tells, long sentences, or dim-dump parens.")
        return 0

    # roster view, ranked by tell count
    print("TBS-001 style_lint — voice & terseness (advisory; never blocks)\n")
    print(f"  {'doc':<42} {'trk':>3} {'words':>6} {'tells':>5} {'long':>5} {'dims':>5} {'stiff':>5}")
    print(f"  {'-'*42} {'-'*3} {'-'*6} {'-'*5} {'-'*5} {'-'*5} {'-'*5}")
    for rel, track, words, hits, stiff, longs, dims in sorted(
            rows, key=lambda r: (-(len(r[3]) + len(r[5]) + len(r[6])), -r[2])):
        flag = "  ⚠" if (len(hits) >= 5 or len(longs) >= 8 or len(dims) >= 4) else ""
        print(f"  {rel:<42} {track:>3} {words:>6} {len(hits):>5} {len(longs):>5} {len(dims):>5} {stiff:>5}{flag}")
    tot_w = sum(r[2] for r in rows)
    tot_t = sum(len(r[3]) for r in rows)
    tot_l = sum(len(r[5]) for r in rows)
    tot_d = sum(len(r[6]) for r in rows)
    print(f"\n  {len(rows)} docs · {tot_w:,} prose words · {tot_t} tells · {tot_l} long sentences"
          f" · {tot_d} dim-dump parens. Run `style_lint.py <doc>` for line-level. ⚠ = dense.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
