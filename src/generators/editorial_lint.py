# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""editorial_lint.py — TBS-001 report narrative validator (manual step).

Mechanical enforcement of the house style in `skills/skill_report_writing.md`.
Scans the *published* report `.md` files (publish.sh MD_FILES + project-summary.md).

Two tiers (mirrors lint.py):
  GATES    — unambiguous, near-zero-false-positive. Exit 1 on failure (for future CI).
  ADVISORY — judgment-y drift candidates. Printed, never blocks.

This is a MANUAL step — it is NOT wired into the pre-commit hook. Run it by hand:

    python3 src/generators/editorial_lint.py          # all checks
    python3 src/generators/editorial_lint.py --gates   # gates only

Gates here are intentionally conservative; advisory checks are allowed to be noisy
(you review them). See the skill's "Future enforcement" section for the rationale.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, cwd=HERE).stdout.strip() or os.path.join(HERE, "..", "..")


# ── published report docs (same set lint.py's editorial-list check uses) ──────
def _published_docs() -> list[str]:
    pub = open(os.path.join(ROOT, "publish.sh"), encoding="utf-8").read()
    m = re.search(r"MD_FILES=\((.*?)\)", pub, re.DOTALL)
    docs = [os.path.basename(f) for f in re.findall(r'"([^"]+\.md)"', m.group(1))] if m else []
    docs.append("project-summary.md")                       # the home page (synced separately)
    return sorted({d for d in docs if os.path.exists(os.path.join(ROOT, d))})


def _blank(m: re.Match) -> str:
    """Replace a span with spaces but keep its newlines, so line numbers stay correct."""
    return re.sub(r"[^\n]", " ", m.group(0))


def _strip(text: str, *, placeholders: bool = False) -> str:
    """Blank out fenced/inline code, HTML comments, and link targets/URLs so prose
    checks don't fire inside them. `placeholders=True` also blanks filled fact/costing
    blocks (so we can find the RAW restatements that *should* be placeholders)."""
    text = re.sub(r"```.*?```", _blank, text, flags=re.DOTALL)      # fenced code
    text = re.sub(r"`[^`]*`", _blank, text)                          # inline code
    if placeholders:
        text = re.sub(r"<!-- BEGIN (?:fact|costing):.*?<!-- END (?:fact|costing):[^>]*-->",
                      _blank, text, flags=re.DOTALL)
    text = re.sub(r"<!--.*?-->", _blank, text, flags=re.DOTALL)      # HTML comments (SPDX, markers)
    text = re.sub(r"\]\([^)]*\)", lambda m: "]" + " " * (len(m.group(0)) - 1), text)  # link targets
    text = re.sub(r"https?://\S+", _blank, text)                     # bare URLs
    return text


def _loc(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


# ═════════════════════════ GATES (block; exit 1) ═════════════════════════════

# British spellings that are never correct in American technical prose. Word-bounded
# and chosen to avoid false positives (e.g. \bcentre\w* misses "central"; the analyse
# verb forms exclude the noun "analyses"; \bmetre\b misses "diameter/parameter").
_BRITISH = [
    (r"\bcolour\w*", "color"),
    (r"\bcentre\w*", "center"),
    (r"\baluminium\b", "aluminum"),
    (r"\banalys(?:e|ed|ing)\b", "analyze"),
    (r"\bfibres?\b", "fiber"),
    (r"\b(?:milli|centi|kilo)?metres?\b", "meter"),
    (r"\b(?:milli|centi)?litres?\b", "liter"),
    (r"\bbehaviour\w*", "behavior"),
    (r"\b(?:favou|neighbou|harbou|labou|vapou|odou|honou|humou)rs?\b", "-or (drop the u)"),
    (r"\bcatalogue\w*", "catalog"),
    (r"\blicenc\w*", "license"),
    (r"\bdefence\w*", "defense"),
    (r"\bmould\w*", "mold"),
    (r"\bsulph\w*", "sulf-"),
    (r"\btyres?\b", "tire"),
    (r"\bdraught\w*", "draft"),
    (r"\bgrey\b", "gray"),
]


def gate_american_spelling() -> list[str]:
    issues = []
    for fn in _published_docs():
        text = _strip(open(os.path.join(ROOT, fn), encoding="utf-8").read())
        for pat, hint in _BRITISH:
            for m in re.finditer(pat, text, re.IGNORECASE):
                issues.append(f"{fn}:{_loc(text, m.start())}  '{m.group(0)}' → use American '{hint}'")
    return issues


def gate_source_links() -> list[str]:
    """Every list item in a Source References / References / Sources section must carry
    a markdown link `[...](...)` — no bare titles, catalog names, or standard numbers."""
    issues = []
    hdr = re.compile(r"^#{2,3}\s.*\b(?:source references|references|sources)\b", re.IGNORECASE)
    item = re.compile(r"^\s*(?:[-*]|\d+\.)\s+(.*\S)")
    for fn in _published_docs():
        lines = open(os.path.join(ROOT, fn), encoding="utf-8").read().splitlines()
        in_sec = False
        for i, ln in enumerate(lines, 1):
            if ln.startswith("#"):
                in_sec = bool(hdr.match(ln))
                continue
            if in_sec:
                mi = item.match(ln)
                if mi and "](" not in mi.group(1):     # a reference item with no hyperlink
                    issues.append(f"{fn}:{i}  reference has no hyperlink → '{mi.group(1)[:70]}'")
    return issues


# ═════════════════════════ ADVISORY (print only) ════════════════════════════

# Stale design terms from superseded revisions. Extend as designs retire elements.
_BANNED = [
    (r"55[- ]?gal\w*", "waste is IBC-4; the 55-gal waste-drum design was eliminated in rev 5"),
    (r"\bcolonnade\b", "the colonnade layout is superseded by the end-zone design"),
    (r"Portacool\s+Jetstream", "the cooler is the Hessaire MC18M (Portacool Jetstream was fictional)"),
    (r"\bdolly track\w*", "dolly tracks were removed in rev 5"),
]


def warn_banned_terms() -> list[str]:
    issues = []
    for fn in _published_docs():
        text = _strip(open(os.path.join(ROOT, fn), encoding="utf-8").read())
        for pat, why in _BANNED:
            for m in re.finditer(pat, text, re.IGNORECASE):
                issues.append(f"{fn}:{_loc(text, m.start())}  stale term '{m.group(0)}' — {why}")
    return issues


def warn_should_be_placeholder() -> list[str]:
    """A value the facts registry recognizes, restated RAW (outside a placeholder block)
    and AGREEING with canonical — convert it to a fact placeholder so it auto-cascades.
    (Disagreements are caught separately by lint.py's facts-registry gate/warning.)"""
    sys.path.insert(0, HERE)
    import facts  # noqa: E402
    issues = []
    for fn in _published_docs():
        raw = open(os.path.join(ROOT, fn), encoding="utf-8").read()
        text = _strip(raw, placeholders=True)               # drop already-placeheld blocks
        for key, fact in facts.FACTS.items():
            canon = float(fact["value"])
            for pat in fact["aliases"]:
                for m in re.finditer(pat, text):
                    try:
                        got = float(m.group(1).replace(",", ""))
                    except (ValueError, IndexError):
                        continue
                    if abs(got - canon) <= 1e-6:            # agrees → just not single-sourced yet
                        issues.append(f"{fn}:{_loc(text, m.start())}  '{m.group(0).strip()}' "
                                      f"→ wrap in <!-- fact:{key} --> (auto-cascades)")
    return issues


def warn_thousands_sep() -> list[str]:
    """Convention: 4+ digit QUANTITIES carry a comma thousands separator. Flags a 4+ digit
    number with a `$` prefix or a unit suffix that has no comma (e.g. '4499mm' → '4,499mm',
    '$1455' → '$1,455'). A unit/`$` is required, so bare product/model numbers (Shurflo 2088,
    years, f-numbers — no unit) are not flagged. `_MODEL_NUMS` exempts model designations
    that collide with a unit ('Ecobulk MX 1000 L' — the 1000 is the model, not a volume)."""
    num = re.compile(r"(?<![#\d.,$])(\$?)(\d{4,})( ?)(mm|cm|kg|gal|Wh|W|V|A|L|g|°|sq ft|m²|km|hrs?|km/h|CFM)?(?![\w])")
    _MODEL_NUMS = re.compile(r"MX $")          # Schütz Ecobulk MX 1000 — model name, not a quantity
    issues = []
    for fn in _published_docs():
        text = _strip(open(os.path.join(ROOT, fn), encoding="utf-8").read())
        for m in num.finditer(text):
            pre, digits, sp, unit = m.group(1), m.group(2), m.group(3), m.group(4)
            if not (pre or unit):            # bare number (product/model/year) — not a quantity
                continue
            if _MODEL_NUMS.search(text[:m.start()]):
                continue
            sep = f"{int(digits):,}"
            issues.append(f"{fn}:{_loc(text, m.start())}  "
                          f"'{pre}{digits}{sp}{unit or ''}' → '{pre}{sep}{sp}{unit or ''}'")
    return issues


def warn_source_refs_section() -> list[str]:
    """A published report with no References / Sources / See Also section."""
    hdr = re.compile(r"^#{1,3}\s.*\b(?:source references|references|sources|see also)\b", re.IGNORECASE)
    issues = []
    for fn in _published_docs():
        lines = open(os.path.join(ROOT, fn), encoding="utf-8").read().splitlines()
        if not any(hdr.match(ln) for ln in lines):
            issues.append(f"{fn}  no Source References / See Also section")
    return issues


# ═════════════════════════════════ runner ═══════════════════════════════════
GATES = [
    ("American spelling", gate_american_spelling),
    ("source references are hyperlinked", gate_source_links),
]
ADVISORY = [
    ("banned stale design terms", warn_banned_terms),
    ("restated value should be a fact placeholder", warn_should_be_placeholder),
    ("thousands-separator consistency", warn_thousands_sep),
    ("report has a Source References section", warn_source_refs_section),
]


def _run(checks) -> int:
    failed = 0
    for name, fn in checks:
        issues = fn()
        print(f"  [{'FAIL' if issues else 'OK  '}] {name}")
        for msg in issues:
            print("         " + msg)
        failed += bool(issues)
    return failed


def main() -> int:
    gates_only = "--gates" in sys.argv[1:]
    print("TBS-001 editorial validator — GATES (block on failure):")
    gate_fail = _run(GATES)
    if not gates_only:
        print("\nTBS-001 editorial validator — ADVISORY (review; never blocks):")
        _run(ADVISORY)
    if gate_fail:
        print(f"\n✗ {gate_fail} gate(s) failed. Fix before relying on this in CI.")
        return 1
    print("\n✓ editorial gates passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
