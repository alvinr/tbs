#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
tidy_labels.py — the STATIC half of the label-tidy tool.

Scans a diagram generator for the SOURCE-detectable label anti-patterns codified in
skills/skill_label_placement.md and reports them; ``--fix`` auto-applies the safe,
unambiguous ones (preserving formatting via exact source-span splicing).

    python3 src/generators/tidy_labels.py --check    src/generators/generate_walkway_diagram.py
    python3 src/generators/tidy_labels.py --fix      src/generators/generate_walkway_diagram.py
    python3 src/generators/tidy_labels.py --check    src/generators/*.py      # sweep (static)
    python3 src/generators/tidy_labels.py --overflow src/generators/*.py      # render-based (needs matplotlib)

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
title-block overlap) are NOT detectable from source — render + crop-zoom in the skill. But
the ONE mechanical visual failure — a label off the frame edge or overlapping another —
IS caught by the render-based ``--overflow`` pass:
  * ``--overflow``   — RENDER every sheet the generator's __main__ draws (via monkeypatched
                       Figure.savefig, no files written) and measure each text artist's bbox
                       against the axes data limits (the intended frame — the sheets use
                       axis("off") + bbox_inches="tight") and against its neighbours. Reports
                       OVERFLOW (off LEFT/RIGHT/TOP/BOTTOM by >``--tol``%, default 4 — skipped on
                       small INSET axes <12%% of the figure, whose tiny frame isn't the visual
                       boundary and balloons the %%) + CROWDED (two DIFFERENT labels overlapping
                       ≥60%% of the smaller; ``--no-collisions`` to skip — bbox-based, so multi-line
                       whitespace makes it advisory). Report
                       only; repositioning is a judgement (P1/P8). Needs matplotlib; the static
                       ``--check``/``--fix`` path stays dependency-free (mpl imported lazily).
"""
import argparse
import ast
import glob
import os
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


# ─────────────────────────────────────────────────────────────────────────────
# RENDER-BASED overflow/collision pass (--overflow). The STATIC checks above can't
# see where a label lands; this one RENDERS each sheet the generator draws and
# measures every text artist's bbox against the axes data limits (the intended
# frame, since the sheets use axis("off") + bbox_inches="tight") and against its
# neighbours. Catches the one visual failure mode that IS mechanical: a leader/dim/
# notes label sprawling past the frame edge (P8/P1) or overlapping another label.
# Heavy deps (matplotlib) are imported lazily so the static path stays dep-free.
# ─────────────────────────────────────────────────────────────────────────────
def _scan_axes(ax, renderer, sheet, findings, tol_frac, collide):
    """Measure every non-empty Text artist in `ax`; record frame-overflow + label collisions."""
    import matplotlib.text as mtext
    # A small INSET axes (section detail, legend) isn't the sheet's visual frame — a label leaving
    # its tiny box into the surrounding sheet is cosmetic, and % overflow vs a tiny range balloons
    # (a label 2× an inset's width reads "+192%"). Skip OVERFLOW on insets; still check collisions.
    pos = ax.get_position()
    is_inset = (pos.width * pos.height) < 0.12
    xl, yl = ax.get_xlim(), ax.get_ylim()
    x_lo, x_hi = min(xl), max(xl)
    y_lo, y_hi = min(yl), max(yl)
    xr, yr = x_hi - x_lo, y_hi - y_lo
    if xr <= 0 or yr <= 0:
        return
    tol_x, tol_y = tol_frac * xr, tol_frac * yr
    inv = ax.transData.inverted()

    def _clip(s):
        s = " / ".join(p.strip() for p in s.splitlines() if p.strip())
        return (s[:44] + "…") if len(s) > 45 else s

    boxes = []
    for t in ax.get_children():
        if not isinstance(t, mtext.Text):
            continue
        s = t.get_text()
        if not s or not s.strip():
            continue                                   # empty (e.g. the arrow-only annotate of a dim)
        try:
            bb = t.get_window_extent(renderer)
        except Exception:
            continue
        if bb.width <= 0 or bb.height <= 0:
            continue
        (ax0, ay0) = inv.transform((bb.x0, bb.y0))
        (ax1, ay1) = inv.transform((bb.x1, bb.y1))
        bx_lo, bx_hi = min(ax0, ax1), max(ax0, ax1)
        by_lo, by_hi = min(ay0, ay1), max(ay0, ay1)
        boxes.append((_clip(s), bx_lo, bx_hi, by_lo, by_hi))
        sides = []
        if x_lo - bx_lo > tol_x:
            sides.append(("off LEFT", (x_lo - bx_lo) / xr))
        if bx_hi - x_hi > tol_x:
            sides.append(("off RIGHT", (bx_hi - x_hi) / xr))
        if y_lo - by_lo > tol_y:
            sides.append(("off BOTTOM", (y_lo - by_lo) / yr))
        if by_hi - y_hi > tol_y:
            sides.append(("off TOP", (by_hi - y_hi) / yr))
        if sides and not is_inset:
            desc = ", ".join(f"{d} +{f * 100:.0f}%" for d, f in sides)
            findings.append((sheet, "OVERFLOW", _clip(s), desc))

    if not collide:
        return
    for i in range(len(boxes)):
        si, ix0, ix1, iy0, iy1 = boxes[i]
        ai = (ix1 - ix0) * (iy1 - iy0)
        for j in range(i + 1, len(boxes)):
            sj, jx0, jx1, jy0, jy1 = boxes[j]
            ox = min(ix1, jx1) - max(ix0, jx0)
            oy = min(iy1, jy1) - max(iy0, jy0)
            if ox <= 0 or oy <= 0:
                continue
            aj = (jx1 - jx0) * (jy1 - jy0)
            frac = (ox * oy) / max(1e-9, min(ai, aj))
            if frac >= 0.6 and si != sj:               # substantial overlap of two DIFFERENT labels
                findings.append((sheet, "CROWDED", si, f"overlaps “{sj}” ({frac * 100:.0f}%)"))


def overflow_pass(path, tol_frac=0.02, collide=True):
    """Render every sheet `path`'s main() draws and return (sheet, kind, text, detail) findings."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure

    findings = []
    orig_savefig = Figure.savefig

    def patched_savefig(self, fname, *a, **k):
        sheet = os.path.basename(fname) if isinstance(fname, (str, bytes, os.PathLike)) else "<figure>"
        try:
            self.canvas.draw()
            renderer = self.canvas.get_renderer()
            for ax in self.axes:
                _scan_axes(ax, renderer, str(sheet), findings, tol_frac, collide)
        except Exception as ex:                        # never let the check crash the render sweep
            findings.append((str(sheet), "ERROR", "", f"scan failed: {ex}"))
        return                                          # skip the real write — read-only check

    import contextlib
    import runpy
    d = os.path.dirname(os.path.abspath(path))
    added = d not in sys.path
    if added:
        sys.path.insert(0, d)                           # sibling imports (tbs_drawing, …)
    saved_argv = sys.argv[:]
    sys.argv = [path]                                   # a generator's __main__ may read sys.argv
    Figure.savefig = patched_savefig
    try:
        # run the file AS __main__ so it renders however it's wired (main() or a module-level block)
        with open(os.devnull, "w") as dn, contextlib.redirect_stdout(dn):
            runpy.run_path(path, run_name="__main__")
    except Exception as ex:
        findings.append(("<module>", "ERROR", "", f"render failed: {ex}"))
    finally:
        Figure.savefig = orig_savefig
        sys.argv = saved_argv
        if added and d in sys.path:
            sys.path.remove(d)
        plt.close("all")
    return findings


def run_overflow(files, tol_frac, collide):
    total = 0
    for path in sorted(set(files)):
        rel = path.replace("src/generators/", "")
        try:
            findings = overflow_pass(path, tol_frac=tol_frac, collide=collide)
        except SyntaxError as ex:
            print(f"  {rel}: SKIP (syntax: {ex})")
            continue
        if not findings:
            continue
        # group by sheet, OVERFLOW first
        order = {"OVERFLOW": 0, "CROWDED": 1, "ERROR": 2}
        findings.sort(key=lambda f: (f[0], order.get(f[1], 9)))
        print(f"\n\033[1m{rel}\033[0m")
        cur = None
        for sheet, kind, text, detail in findings:
            if sheet != cur:
                print(f"  \033[1m{sheet}\033[0m")
                cur = sheet
            col = {"OVERFLOW": "\033[31m", "CROWDED": "\033[33m", "ERROR": "\033[35m"}.get(kind, "")
            label = f"“{text}” " if text else ""
            print(f"    {col}{kind:<9}\033[0m {label}— {detail}")
            total += (kind in ("OVERFLOW", "CROWDED"))
    print(f"\n{total} label(s) off-frame / overlapping — reposition per skill_label_placement.md (P1/P8).")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Static label-tidy: report/auto-fix source-detectable label issues.")
    ap.add_argument("paths", nargs="+", help="generator .py file(s) or globs")
    ap.add_argument("--check", action="store_true", help="report only (default)")
    ap.add_argument("--fix", action="store_true", help="auto-apply the safe fixes in place")
    ap.add_argument("--overflow", action="store_true",
                    help="RENDER each sheet and report labels off the frame edge / overlapping (render-based, needs matplotlib)")
    ap.add_argument("--no-collisions", action="store_true", help="with --overflow: report frame-overflow only, skip label collisions")
    ap.add_argument("--tol", type=float, default=4.0, help="with --overflow: overflow tolerance, %% of axis range (default 4; bbox_inches=tight absorbs a few %%)")
    args = ap.parse_args()

    files = []
    for p in args.paths:
        files += glob.glob(p)

    if args.overflow:
        return run_overflow(files, tol_frac=args.tol / 100.0, collide=not args.no_collisions)
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
