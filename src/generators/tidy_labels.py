#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
tidy_labels.py — the STATIC half of the label-tidy tool.

Scans a diagram generator for the SOURCE-detectable label anti-patterns codified in
skills/skill_label_placement.md and reports them; ``--fix`` auto-applies the safe,
unambiguous ones (preserving formatting via exact source-span splicing).

    python3 src/generators/tidy_labels.py --check src/generators/generate_walkway_diagram.py
    python3 src/generators/tidy_labels.py --fix   src/generators/generate_walkway_diagram.py
    python3 src/generators/tidy_labels.py --check src/generators/*.py      # sweep

Auto-fixed (high confidence, scale-independent):
  * DIM range-suffix   — strip a redundant ``(X=a–b)`` / ``(Yd=…)`` / ``(Z=n)`` from a
                         draw_dim_* label; the extension lines already show the span (P7).
  * DIM unit-less      — a draw_dim_* label whose FIRST token is a measured value (a bare
                         number or a single ``{expr}``) but carries no unit → insert ``mm``
                         after it (P7).  Skips Ø-diameters, ``×`` specs, X=/Yd=/Z= station
                         labels, and named/text-leading dims — those conventionally omit mm.

Deliberately NOT auto-fixed / not flagged:
  * dimension ``offset`` — scale-dependent (3–8 data-units in detail views vs 25–80 mm-first);
    a static bump is unsafe, so it's a visual call.
  * multi-line leaders — on this project the 2D set is manufacturing blueprints where detailed
    callouts (part no., material, DN) are WANTED, so a line-count "spec-sheet" flag is noise.

Reported only (need judgement or a rendered look — the /tidy-labels skill, P1/P8/P9):
  * LEADER range-suffix — a ``(X=…)`` on a leader may be a legit part id; a human/vision decides.
  * NOTES hand-wrapped  — a notes list with leading-space continuation items → use ``wrap=``.

The VISUAL rules (notes over geometry, leader in the nearest clear pocket, bbox on hatch,
collisions, title-block overlap) are NOT detectable here — render + crop-zoom in the skill.
"""
import argparse
import ast
import glob
import re
import sys

# label = which positional arg carries the display string
LABEL_IDX = {"draw_dim_h": 4, "draw_dim_v": 4, "leader": 5}
UNIT_RE = re.compile(r"(mm|cm|°|deg|m²|mm²|²|kg)")
# a trailing " (X=…)" / " (Yd=…)" / " (Z=…)" coordinate range, just before the closing quote
RANGE_RE = re.compile(r"\s*\((?:X|Yd|Z)=[^)]*\)(?=[\"'])")
# a dim label we should NOT flag as unit-less — conventional diameter (Ø), a multi-dim/thread
# spec (×), or a coordinate/station reference (X= / Yd= / Z=). Those legitimately omit "mm".
NOUNIT_SKIP_RE = re.compile(r"Ø|×|\bX=|\bYd=|\bZ=")
# a label whose FIRST token is a measured value — a bare number (opt. ~ / decimals) or a single
# f-expr — captured so we can insert "mm" right after it: f?  quote  value  rest…quote
LEADING_VAL_RE = re.compile(r"""^(f?)(["'])(~?\d[\d.]*|\{[^{}]*\})(.*)\2$""", re.S)


class Finding:
    # Fixes are applied by exact source-SEGMENT replacement (old → new) on the finding's line —
    # NOT char/byte spans, because ast col_offset is byte-based and the source is full of
    # non-ASCII (– × ° Ø), which desyncs any char-offset splice.
    def __init__(self, rule, line, msg, fixable=False, old=None, new=None):
        self.rule, self.line, self.msg = rule, line, msg
        self.fixable, self.old, self.new = fixable, old, new


def _fname(call):
    f = call.func
    return f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else "")


def analyze(src, path):
    tree = ast.parse(src)
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = _fname(node)
        if fn not in LABEL_IDX:
            continue
        idx = LABEL_IDX[fn]
        label = node.args[idx] if len(node.args) > idx else None
        is_dim = fn.startswith("draw_dim")
        # NOTE: no static `offset<8` rule — the right offset is scale-dependent (3–8 data-units
        # in detail views, 25–80 in mm-first sheets, P1/P7). Judging it needs the rendered scale,
        # so it belongs to the visual /tidy-labels pass, not a blanket static bump.

        if not isinstance(label, (ast.Constant, ast.JoinedStr)):
            continue
        seg = ast.get_source_segment(src, label)
        if seg is None or "\n" in seg:   # only single-line label segments are auto-fixable
            continue

        # ── coordinate-range suffix ────────────────────────────────────────────
        m = RANGE_RE.search(seg)
        if m:
            if is_dim:
                out.append(Finding("DIM range-suffix", label.lineno,
                                   f"strip {m.group().strip()!r} (span shown by extension lines)",
                                   True, seg, RANGE_RE.sub("", seg)))
            else:
                out.append(Finding("LEADER range-suffix", label.lineno,
                                   f"has {m.group().strip()!r} — keep only if it's a real part id (else strip)"))

        # ── unit-less dimension ────────────────────────────────────────────────
        # Only a dim whose FIRST token is a measured value gets mm; skip Ø / × / station
        # labels (conventional) and named/text-leading dims (deck Z140, "WALL" — intentional).
        if is_dim and not UNIT_RE.search(seg) and not NOUNIT_SKIP_RE.search(seg):
            m = LEADING_VAL_RE.match(seg)
            if m:
                fpref, q, val, rest = m.groups()
                new = f"{fpref}{q}{val}mm{rest}{q}"     # insert mm right after the leading value
                out.append(Finding("DIM unit-less", label.lineno,
                                   f"add 'mm' after leading value ({val})", True, seg, new))
            # non-numeric-leading dims are named/station labels — deliberately not flagged.

    # NOTE: no LEADER "spec-sheet" (≥3-line) rule. On this project the 2D set is a set of
    # manufacturing blueprints where completeness is the point, so detailed multi-line callouts
    # (bearing part no., plate spec, valve DN) are usually WANTED. Whether a secondary line is
    # genuinely redundant vs buildable detail is a judgement — the visual /tidy-labels pass, not a
    # blanket line-count flag (it fired ~30× here, almost all legitimate).

    # ── hand-wrapped notes lists (draw_notes(..., [ ... ], ...)) ────────────────
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _fname(node) == "draw_notes":
            for a in node.args:
                if isinstance(a, ast.List):
                    cont = [e for e in a.elts
                            if isinstance(e, ast.Constant) and isinstance(e.value, str)
                            and e.value[:3] == "   "]
                    if cont:
                        out.append(Finding("NOTES hand-wrapped", a.lineno,
                                           f"{len(cont)} hand-wrapped continuation line(s) → pass logical "
                                           f"one-string notes + wrap= (P8)"))
    return out


def apply_fixes(src, findings):
    """Replace each fixed label's exact source segment on its own line (offset-free)."""
    lines = src.split("\n")
    n = 0
    for f in findings:
        if not f.fixable:
            continue
        i = f.line - 1
        if f.old in lines[i]:
            lines[i] = lines[i].replace(f.old, f.new, 1)
            n += 1
    return "\n".join(lines), n


def main():
    ap = argparse.ArgumentParser(description="Static label-tidy: report/auto-fix source-detectable label issues.")
    ap.add_argument("paths", nargs="+", help="generator .py file(s) or globs")
    ap.add_argument("--check", action="store_true", help="report only (default)")
    ap.add_argument("--fix", action="store_true", help="auto-apply the safe fixes in place")
    args = ap.parse_args()

    files = []
    for p in args.paths:
        files += glob.glob(p)
    total_fix = total_flag = 0
    RANK = {"DIM range-suffix": 0, "DIM unit-less": 1,
            "LEADER range-suffix": 2, "NOTES hand-wrapped": 3}
    for path in sorted(set(files)):
        try:
            src = open(path).read()
            findings = analyze(src, path)
        except SyntaxError as ex:
            print(f"  {path}: SKIP (syntax: {ex})")
            continue
        if not findings:
            continue
        findings.sort(key=lambda f: (RANK.get(f.rule, 9), f.line))
        rel = path.replace("src/generators/", "")
        print(f"\n\033[1m{rel}\033[0m")
        for f in findings:
            tag = "\033[32mFIX \033[0m" if f.fixable else "\033[33mflag\033[0m"
            print(f"  {tag} L{f.line:<5} {f.rule:<20} {f.msg}")
            total_fix += f.fixable
            total_flag += (not f.fixable)
        if args.fix:
            new_src, n = apply_fixes(src, findings)
            if n:
                ast.parse(new_src)                     # guard: never write unparseable source
                open(path, "w").write(new_src)
                print(f"  \033[32m→ applied {n} fix(es)\033[0m")

    verb = "applied" if args.fix else "auto-fixable"
    print(f"\n{total_fix} {verb}, {total_flag} flagged for the visual pass (/tidy-labels).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
