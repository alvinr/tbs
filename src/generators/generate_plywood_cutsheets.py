#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_plywood_cutsheets.py — the ONE plywood cut-sheet / nesting drawing for TBS-001.

Plywood is used in many subsystems (IBC-corridor plumbing panel, pump-mount shirt, pinhole-wall
filter-skid backing, the EP electrical backboard, the hinged panel's Fan-B mount band + fold-down
light-trap aprons, and the chem-prep shelf). Each consumer sheet used to cut its own ad-hoc rectangle;
this generator is the SINGLE cut-sheet the buyer/fabricator works from — every plywood part in one
schedule + nesting layout, grouped by grade + thickness so same-stock parts nest on one sheet.

SINGLE SOURCE: the cut dimensions come from `tbs_constants` wherever the piece is geometry-driven
(pinhole panel width, apron widths/heights from the floor gap, chem-shelf) and are literals only where
the spec fixes them (EP backboard, pump-mount shirt, side boards, Fan-B band, cooler base). Cost /
supplier / SKU stay single-sourced in `parts.py` (cross-referenced by the `key` column). So the cut
figures can't drift from the geometry, and the money can't drift from the registry.

    python3 src/generators/generate_plywood_cutsheets.py     # → diagrams/plywood-cutsheets-sheet1/2.png
"""
import os
import sys
import textwrap

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Circle, Rectangle

sys.path.insert(0, os.path.dirname(__file__))
from tbs_constants import (                                    # noqa: E402
    DIAGRAMS_DIR,
    PANEL_CORNER_YD_L, PANEL_CORNER_YD_R, APRON_FIX_W, C_WID,
    PANEL_FLOOR_GAP, PANEL_FLOOR_GAP_SIDE,
    PWP_PANEL_X0, PWP_PANEL_X1, SHELF_W, SHELF_DEPTH,
)
from tbs_drawing import draw_notes, leader                     # noqa: E402
from tbs_title_block import title_block                        # noqa: E402

TOTAL_SHEETS = 2
C_BG = "#FAFAFA"
FONT = {"fontfamily": "monospace"}
C_OUT = "#1A1A1A"
C_DIM = "#404040"
C_WOOD = "#D8C39A"       # plywood face
C_STOCK = "#F0E9D8"      # stock-sheet ground
C_STUB = "#C7B48A"       # fixed (non-fold) piece, distinguished from a fold-down apron
C_CUT = "#B0202A"        # guillotine saw-cut line (dashed red)

# ── derived cut dimensions (geometry-driven → from tbs_constants; cannot drift) ─────────────
PINHOLE_W = PWP_PANEL_X1 - PWP_PANEL_X0                  # 1795 — pinhole-wall panel width (X span)
PINHOLE_HALF = round(PINHOLE_W / 2)                      # 898  — cut as 2 butt-jointed halves (1795 > 1219 stock width)
APR_NEAR_W = PANEL_CORNER_YD_L                           # 653  — near fold-down apron (Yd0→653)
APR_FAR_W = (C_WID - APRON_FIX_W) - PANEL_CORNER_YD_R    # 453  — far apron (Yd1709→2162)
BAFFLE_W = PANEL_CORNER_YD_R - PANEL_CORNER_YD_L         # 1056 — fixed center baffle (drum-bay width)
APR_CORNER_H = PANEL_FLOOR_GAP_SIDE                      # 282  — corner floor gap the aprons/stub close
APR_CENTER_H = PANEL_FLOOR_GAP                           # 217  — center floor gap the baffle closes

STOCK_8x4 = (1219, 2438)     # nominal 4'×8' sheet
STOCK_HD = (1220, 2440)      # Home-Depot-stated 4'×8' for the SANDEPLY / UV-white lines

# ── the plywood registry ────────────────────────────────────────────────────────────────────
# Each GROUP shares one (grade, thickness) → its parts nest on the same stock. Each part lists its
# CUT PIECES: (label, W_mm, H_mm, qty, where-used). "D" flags a constant-derived dim in the schedule.
GROUPS = [
    dict(gid="A", thick=18, grade='23/32" RTD Southern Yellow Pine exterior sheathing',
         sku="Home Depot 303564747", stock=STOCK_8x4, parts=[
        dict(key="corridor-panel-ply-18", stock=STOCK_8x4, pieces=[
            ("Corridor rear backing board", 168, 1849, 1, "IBC-corridor plumbing panel rear face"),
            ("Drain-riser spine", 456, 1966, 1, "waste-riser / X-port P-clip spine"),
            ("Pump-run side board (far)", 399, 420, 1, "#29 pump-run pipe support"),
            ("Pump-run side board (near-lo)", 399, 420, 1, "#29 pump-run pipe support"),
            ("Pump-run side board (near-hi)", 399, 690, 1, "#29 pump-run pipe support"),
        ]),
        dict(key="corridor-panel-ply-25", stock=STOCK_8x4, pieces=[
            ("Pump-mount shirt", 610, 1650, 1, "backs pumps P-01..P-05 on the corridor panel"),
            ("Shirt standoff cleat strip", 40, 720, 1, "one 40×720 strip, cut to 6× 120mm shirt-to-rear-panel standoff blocks"),
        ]),
        dict(key="pinhole-panel-ply-18", stock=STOCK_8x4, npieced=2, pieces=[
            ("Pinhole backing half", PINHOLE_HALF, 1440, 2, f"3× Big Blue filters + P-04/SV-02/DV-02 skid row; 2 halves butt-jointed → the full {PINHOLE_W}×1440 face (>1219 stock width)"),
        ]),
        dict(key="panel-bottom-apron", stock=STOCK_8x4, pieces=[
            ("Near fold-down light apron", APR_NEAR_W, APR_CORNER_H, 1, "seals under-leaf light gap, near corner (18mm, flat-black interior face)"),
            ("Far fold-down light apron", APR_FAR_W, APR_CORNER_H, 1, "seals under-leaf light gap, far corner"),
            ("Fixed pivot stub", APRON_FIX_W, APR_CORNER_H, 1, "fixed strip clearing the Ø220 pivot mount plate"),
            ("Fixed center baffle", BAFFLE_W, APR_CENTER_H, 1, "fixed light baffle under the drum bay"),
        ]),
        dict(key="panel-fanb-ply", stock=STOCK_8x4, pieces=[
            ("Fan-B mount band", 610, 1220, 1, "hinged-panel near-corner rigid fan/duct mount band (rotated 90°, nests on a pinhole-backing sheet)"),
            ("Cooler stowage base", 600, 350, 1, "evap-cooler stowage base (cargo-door end)"),
        ]),
    ]),
    dict(gid="B", thick=18, grade="18mm UV-coated white hardwood (Swaner)",
         sku="Home Depot 302874373", stock=STOCK_HD, parts=[
        dict(key="shelf-phenolic-ply", stock=STOCK_HD, pieces=[
            ("Chem-prep shelf board", SHELF_W, SHELF_DEPTH, 1, "fold-down chemistry-prep work surface (pinhole wall)"),
        ]),
        dict(key="ep-backing-panel", stock=STOCK_HD, pieces=[
            ("EP electrical backboard", 700, 2000, 1, "interior wall electrical backboard — MPPT / battery / inverter / disconnects / IP65 box (backboard is finish-agnostic → shares the chem-shelf UV-white sheet)"),
        ]),
    ]),
]

# dims that DERIVE from a tbs_constants value (shown with a ᴰ marker in the schedule)
_DERIVED = {PINHOLE_W, PINHOLE_HALF, APR_NEAR_W, APR_FAR_W, APRON_FIX_W, BAFFLE_W,
            APR_CORNER_H, APR_CENTER_H, SHELF_W, SHELF_DEPTH}

CUT_MARGIN = 6       # saw kerf reserved between adjacent pieces (mm)
FIT_TOL = 5          # plywood cut tolerance — a piece up to 5mm over a free rect still fits (a full-width
#                      1220mm piece cuts from a 1219mm sheet; the 1mm is inside the tolerance)


def _group_pieces(g):
    """Flatten a group's parts into a piece pool (label, w, h), expanding qty — nesting mixes pieces
    across the group's subsystems (same grade+thickness stock)."""
    out = []
    for p in g["parts"]:
        for (label, w, h, q, _where) in p["pieces"]:
            for _ in range(q):
                out.append((label, float(w), float(h)))
    return out


def _overlap(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return not (bx >= ax + aw - 1e-6 or bx + bw <= ax + 1e-6
               or by >= ay + ah - 1e-6 or by + bh <= ay + 1e-6)


def _contains(a, b):     # free-rect a fully contains b
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax <= bx + 1e-6 and ay <= by + 1e-6 and ax + aw >= bx + bw - 1e-6 and ay + ah >= by + bh - 1e-6


def _split_free(f, used):
    """MAXRECTS split — a free rect f minus the placed rect `used` → up to 4 maximal sub-rects."""
    if not _overlap(f, used):
        return [f]
    fx, fy, fw, fh = f
    ux, uy, uw, uh = used
    out = []
    if ux > fx:                              out.append((fx, fy, ux - fx, fh))                 # left
    if ux + uw < fx + fw:                    out.append((ux + uw, fy, fx + fw - ux - uw, fh))  # right
    if uy > fy:                              out.append((fx, fy, fw, uy - fy))                 # below
    if uy + uh < fy + fh:                    out.append((fx, uy + uh, fw, fy + fh - uy - uh))  # above
    return out


def _prune(rects):
    out = []
    for i, r in enumerate(rects):
        if r[2] <= 1e-6 or r[3] <= 1e-6:
            continue
        if any(j != i and _contains(q, r) and (q != r or j < i) for j, q in enumerate(rects)):
            continue
        out.append(r)
    return out


def _pack_maxrects(pieces, bin_w, bin_h, tol, kerf):
    """MAXRECTS (Best-Short-Side-Fit, 90° rotation) — tightest free-placement nesting, minimizing the
    number of stock sheets. The result is NOT guaranteed guillotine-cuttable; the caller verifies that
    (via cut_plan) and falls back to _pack_once if a sheet can't be cut edge-to-edge."""
    items = sorted(pieces, key=lambda p: -(p[1] * p[2]))
    bins = []

    def _try(free, w, h):
        best = None
        for ri, (fx, fy, fw, fh) in enumerate(free):
            for (pw, ph, rot) in ([(w, h, False)] if abs(w - h) < 1e-6 else [(w, h, False), (h, w, True)]):
                if pw <= fw + tol and ph <= fh + tol:
                    score = max(0.0, min(fw - pw, fh - ph))
                    if best is None or score < best[0]:
                        best = (score, ri, fx, fy, pw, ph, rot)
        return best

    for (label, w0, h0) in items:
        pick = None
        for bi, b in enumerate(bins):
            cand = _try(b["free"], w0, h0)
            if cand and (pick is None or cand[0] < pick[1][0]):
                pick = (bi, cand)
        if pick is None:
            bins.append({"free": [(0, 0, bin_w, bin_h)], "placed": []})
            bi = len(bins) - 1
            cand = _try(bins[bi]["free"], w0, h0)
            if cand is None:
                bins[bi]["placed"].append((0, 0, min(w0, bin_w), min(h0, bin_h), label + " ⚠OVERSIZE", False))
                bins[bi]["free"] = []
                continue
            pick = (bi, cand)
        bi, (_score, _ri, x, y, pw, ph, rot) = pick
        b = bins[bi]
        b["placed"].append((x, y, pw, ph, label, rot))
        used = (x, y, pw + kerf, ph + kerf)
        nf = []
        for f in b["free"]:
            nf.extend(_split_free(f, used))
        b["free"] = _prune(nf)
    return [b["placed"] for b in bins]


def _pack_once(pieces, bin_w, bin_h, order, split, fit, tol, kerf):
    """One GUILLOTINE packing pass (90° cuts only, so every sheet is panel-saw cuttable). `order` keys
    the piece sort, `split` picks the guillotine axis rule, `fit` the free-rect score. A piece may
    overhang a free rect by up to `tol` (5mm cut tolerance → full-width pieces cut to the edge); each
    placed piece reserves `kerf` before its free rect is split by ONE cut into a right strip + top strip."""
    key = {"area": lambda p: -(p[1] * p[2]), "maxside": lambda p: -max(p[1], p[2]),
           "height": lambda p: -p[2], "width": lambda p: -p[1]}[order]
    items = sorted(pieces, key=key)
    bins = []

    def _try(free, w, h):
        best = None
        for ri, (fx, fy, fw, fh) in enumerate(free):
            for (pw, ph, rot) in ([(w, h, False)] if abs(w - h) < 1e-6 else [(w, h, False), (h, w, True)]):
                if pw <= fw + tol and ph <= fh + tol:
                    sss = max(0.0, min(fw - pw, fh - ph))                   # short-side leftover
                    score = sss if fit == "sss" else max(0.0, fw * fh - pw * ph)  # or best-area
                    if best is None or score < best[0]:
                        best = (score, ri, fw, fh, pw, ph, rot)
        return best

    def _guillotine(fx, fy, fw, fh, pw, ph):
        horiz = (fw - pw) <= (fh - ph) if split == "shorter" else (fw - pw) > (fh - ph)
        if horiz:                        # TOP strip kept full-width, right strip piece-high
            parts = ((fx + pw + kerf, fy, fw - pw - kerf, ph), (fx, fy + ph + kerf, fw, fh - ph - kerf))
        else:                            # RIGHT strip kept full-height, top strip piece-wide
            parts = ((fx + pw + kerf, fy, fw - pw - kerf, fh), (fx, fy + ph + kerf, pw, fh - ph - kerf))
        return [r for r in parts if r[2] > 1 and r[3] > 1]

    for (label, w0, h0) in items:
        pick = None
        for bi, b in enumerate(bins):
            cand = _try(b["free"], w0, h0)
            if cand and (pick is None or cand[0] < pick[1][0]):
                pick = (bi, cand)
        if pick is None:
            bins.append({"free": [(0, 0, bin_w, bin_h)], "placed": []})
            bi = len(bins) - 1
            cand = _try(bins[bi]["free"], w0, h0)
            if cand is None:
                bins[bi]["placed"].append((0, 0, min(w0, bin_w), min(h0, bin_h), label + " ⚠OVERSIZE", False))
                bins[bi]["free"] = []
                continue
            pick = (bi, cand)
        bi, (_score, ri, fw, fh, pw, ph, rot) = pick
        b = bins[bi]
        fx, fy, _fw, _fh = b["free"].pop(ri)
        b["placed"].append((fx, fy, pw, ph, label, rot))
        b["free"].extend(_guillotine(fx, fy, fw, fh, pw, ph))
    return [b["placed"] for b in bins]


def _total_cuts(bin_w, bin_h, bins):
    return sum(cut_plan(bin_w, bin_h, pl)[0] for pl in bins)


def pack_group(pieces, bin_w, bin_h, tol=FIT_TOL, kerf=CUT_MARGIN):
    """Pack a group onto the fewest stock sheets, keeping every sheet panel-saw cuttable (edge-to-edge
    90° cuts). The tight MAXRECTS nest is used when every one of its sheets is guillotine-cuttable (it is
    for the current pieces, and it packs one sheet fewer than a pure guillotine greedy); otherwise the
    packer falls back to the guillotine strategy that gives the fewest sheets, then fewest cuts. Among
    equally-good options the fewest total cuts wins. Returns bins of (x, y, w, h, label, rotated)."""
    mr = _pack_maxrects(pieces, bin_w, bin_h, tol, kerf)
    mr_cuts = _total_cuts(bin_w, bin_h, mr)
    best = (len(mr), mr_cuts, mr) if mr_cuts < INF else None
    for order in ("area", "maxside", "height", "width"):
        for split in ("shorter", "longer"):
            for fit in ("sss", "area"):
                bins = _pack_once(pieces, bin_w, bin_h, order, split, fit, tol, kerf)
                cand = (len(bins), _total_cuts(bin_w, bin_h, bins), bins)
                if best is None or cand[:2] < best[:2]:
                    best = cand
    return best[2]


_E = 0.5                                                          # mm epsilon for cut-plan edge tests
INF = float("inf")                                                # a sheet that is not guillotine-cuttable


def cut_plan(bin_w, bin_h, placed):
    """Minimum guillotine (edge-to-edge 90°) cuts to free every piece on a sheet, + the cut segments.
    Recurse: a region holding >1 piece (or 1 piece not filling it) is split by a full-span cut on a
    piece edge that crosses no piece; take the fewest-cut choice. Memoized — a few pieces per sheet."""
    R = [(x, y, x + w, y + h) for (x, y, w, h, _l, _r) in placed]
    memo = {}

    def rec(x0, y0, x1, y1, idxs):
        if not idxs:
            return 0, []
        if len(idxs) == 1:
            a = R[idxs[0]]
            if abs(a[0] - x0) < _E and abs(a[1] - y0) < _E and abs(a[2] - x1) < _E and abs(a[3] - y1) < _E:
                return 0, []
        key = (round(x0), round(y0), round(x1), round(y1), idxs)
        if key in memo:
            return memo[key]
        best = None
        xs = {round(e, 2) for i in idxs for e in (R[i][0], R[i][2]) if x0 + _E < e < x1 - _E}
        for xc in xs:
            if any(R[i][0] < xc - _E and R[i][2] > xc + _E for i in idxs):
                continue
            left = tuple(i for i in idxs if R[i][2] <= xc + _E)
            right = tuple(i for i in idxs if R[i][0] >= xc - _E)
            if len(left) + len(right) != len(idxs):
                continue
            cl, sl = rec(x0, y0, xc, y1, left)
            cr, sr = rec(xc, y0, x1, y1, right)
            if best is None or 1 + cl + cr < best[0]:
                best = (1 + cl + cr, [(xc, y0, xc, y1)] + sl + sr)
        ys = {round(e, 2) for i in idxs for e in (R[i][1], R[i][3]) if y0 + _E < e < y1 - _E}
        for yc in ys:
            if any(R[i][1] < yc - _E and R[i][3] > yc + _E for i in idxs):
                continue
            bot = tuple(i for i in idxs if R[i][3] <= yc + _E)
            top = tuple(i for i in idxs if R[i][1] >= yc - _E)
            if len(bot) + len(top) != len(idxs):
                continue
            cb, sb = rec(x0, y0, x1, yc, bot)
            ct, st = rec(x0, yc, x1, y1, top)
            if best is None or 1 + cb + ct < best[0]:
                best = (1 + cb + ct, [(x0, yc, x1, yc)] + sb + st)
        if best is None:
            best = (0, []) if len(idxs) <= 1 else (INF, [])     # >1 piece, no cut → not guillotine-cuttable
        memo[key] = best
        return best

    return rec(0, 0, bin_w, bin_h, tuple(range(len(R))))


# pack every group once (module-level, so Sheet 1's count and Sheet 2's layout agree)
PACKED = [(g, pack_group(_group_pieces(g), g["stock"][0], g["stock"][1])) for g in GROUPS]
_BINS = {g["gid"]: bins for g, bins in PACKED}
NAIVE_TOTAL = sum(sum(p.get("npieced", 1) for p in g["parts"]) for g in GROUPS)
OPT_TOTAL = sum(len(bins) for _g, bins in PACKED)

# every physical stock sheet gets ONE sequential letter A, B, C… across all groups (the buyer's
# sheet list), so the schedule and the nesting layout name the same sheet. A grade group maps to a
# contiguous run of letters (SYP → A–C, UV-white → D, PT → E).
_SHEET_LETTERS = {}          # gid -> [letters, one per bin]
_gi = 0
for _g, _bins in PACKED:
    _SHEET_LETTERS[_g["gid"]] = [chr(ord("A") + _gi + _i) for _i in range(len(_bins))]
    _gi += len(_bins)


def _letter_span(gid):
    ls = _SHEET_LETTERS[gid]
    return ls[0] if len(ls) == 1 else f"{ls[0]}–{ls[-1]}"


def _is_fixed(label):
    return any(k in label for k in ("Fixed", "stub", "baffle"))


def _save(fig, fname, tight=True):
    os.makedirs(DIAGRAMS_DIR, exist_ok=True)
    png = os.path.join(DIAGRAMS_DIR, fname)
    fig.savefig(png, dpi=150, bbox_inches="tight" if tight else None, facecolor=C_BG)
    plt.close(fig)
    print(f"  {png} saved")


def _d(v):
    """format a mm value, tagging ᴰ if it derives from a constant."""
    return f"{v:g}ᴰ" if v in _DERIVED else f"{v:g}"


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — PLYWOOD SCHEDULE (one row per cut piece; grouped by stock)
# ═══════════════════════════════════════════════════════════════════════════════
def draw_sheet1():
    fig = plt.figure(figsize=(20, 14))
    fig.patch.set_facecolor(C_BG)
    ax = fig.add_axes([0.03, 0.06, 0.94, 0.88])
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    ax.text(50, 98, "PLYWOOD SCHEDULE — ALL SUBSYSTEMS", ha="center", fontsize=14,
            fontweight="bold", color=C_OUT, **FONT)
    ax.text(50, 95.3, "one cut list, grouped by grade + thickness · ᴰ = dimension derived from a "
            "tbs_constants value (cannot drift) · cost/SKU per parts.py key",
            ha="center", fontsize=8, color=C_DIM, **FONT)

    # columns
    CX = {"grp": 2, "piece": 8, "wh": 41, "qty": 55, "where": 60}
    HDR_Y = 91
    ax.text(CX["grp"], HDR_Y, "SHEET", fontsize=8, fontweight="bold", color=C_OUT, **FONT)
    ax.text(CX["piece"], HDR_Y, "CUT PIECE", fontsize=8, fontweight="bold", color=C_OUT, **FONT)
    ax.text(CX["wh"], HDR_Y, "W × H (mm)", fontsize=8, fontweight="bold", color=C_OUT, **FONT)
    ax.text(CX["qty"], HDR_Y, "QTY", fontsize=8, fontweight="bold", color=C_OUT, **FONT)
    ax.text(CX["where"], HDR_Y, "WHERE USED", fontsize=8, fontweight="bold", color=C_OUT, **FONT)
    ax.plot([1, 99], [HDR_Y - 0.9, HDR_Y - 0.9], color=C_OUT, lw=1.1)

    y = HDR_Y - 2.6
    ROW = 1.95
    for g in GROUPS:
        # group band
        ax.plot([1, 99], [y + 1.1, y + 1.1], color=C_DIM, lw=0.5)
        span = _letter_span(g["gid"])
        ax.text(CX["grp"], y, span, fontsize=9, fontweight="bold", color=C_OUT, **FONT)
        opt = len(_BINS[g["gid"]])
        naive = sum(p.get("npieced", 1) for p in g["parts"])
        npieces = len(_group_pieces(g))
        saved = f"  (was {naive})" if opt < naive else ""
        ax.text(CX["piece"], y, f"{g['grade']}  ·  {g['sku']}  ·  "
                f"{npieces} pieces → sheet{'s' if opt != 1 else ''} {span} "
                f"({opt}× {g['stock'][0]}×{g['stock'][1]}){saved}",
                fontsize=7.4, fontweight="bold", color=C_DIM, **FONT)
        y -= ROW
        for p in g["parts"]:
            for (label, w, h, q, where) in p["pieces"]:
                ax.text(CX["piece"], y, label, fontsize=7.2, color=C_OUT, **FONT)
                ax.text(CX["wh"], y, f"{_d(w)} × {_d(h)}", fontsize=7.2, color=C_OUT, **FONT)
                ax.text(CX["qty"], y, f"{q}", fontsize=7.2, color=C_OUT, **FONT)
                ax.text(CX["where"], y, (where[:52] + "…") if len(where) > 53 else where,
                        fontsize=6.8, color=C_DIM, **FONT)
                ax.text(CX["piece"] - 3.4, y, f"({p['key']})" if False else "", fontsize=5, color=C_DIM, **FONT)
                y -= ROW
            # parts.py key line (cost/supplier source)
            ax.text(CX["piece"], y + ROW * 0.02, f"        └ parts.py: {p['key']}",
                    fontsize=6.0, color="#7A7A7A", **FONT)
            y -= ROW * 0.85

    draw_notes(ax, [
        "READ THIS SHEET:",
        f"• Buy the sheet count in each group band — {OPT_TOTAL} stock sheets total (bin-packed from {NAIVE_TOTAL} if each part were cut on its own sheet). Pieces from different subsystems share a sheet within one grade+thickness; you can't cut across grades.",
        "• ᴰ dims derive from tbs_constants and update with the geometry; plain dims are spec/report literals. Cost, supplier and SKU live in parts.py (the key on each part's └ line).",
        "• The optimized cut LAYOUT (which pieces nest on each sheet) is Sheet 2. Fabrication detail for a piece (hole positions, edge seal, hinge line) stays on its owning subsystem sheet.",
    ], 2, 14.5, spacing=2.6, fs=7.2, title_fs=8.0, width=96, wrap=150,
       color=C_OUT, title_color=C_OUT, border_color=C_DIM, font=FONT)

    ax_tb = fig.add_axes([0.03, 0.012, 0.94, 0.055])
    ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis("off")
    title_block(ax_tb, f"SHEET 1 OF {TOTAL_SHEETS}", drawing_title="PLYWOOD CUT SHEETS",
                subtitle="PLYWOOD SCHEDULE — ALL SUBSYSTEMS",
                scale_note="SCHEDULE · ALL DIMS IN mm", doc_id="TBS-001 · Plywood Cut Sheets",
                height=0.92)
    _save(fig, "plywood-cutsheets-sheet1.png", tight=False)


# ── Sheet-2 label helpers (measure real text extents so a label wraps to fit its box, else leads out) ──
_LBL_FS = 5.4
_PX_PAD = 12               # px breathing room inside a box before a label is deemed not to fit


def _txt_wh(renderer, s, fs):
    w, h, _dsc = renderer.get_text_width_height_descent(s, FontProperties(family="monospace", size=fs), False)
    return w, h


def _data_per_px(ax):
    inv = ax.transData.inverted()
    o = inv.transform((0, 0))
    return abs(inv.transform((1, 0))[0] - o[0]), abs(inv.transform((0, 1))[1] - o[1])


def _box_px(ax, x0, y0, w, h):
    p0 = ax.transData.transform((x0, y0))
    p1 = ax.transData.transform((x0 + w, y0 + h))
    return abs(p1[0] - p0[0]), abs(p1[1] - p0[1])


def _wrap_fit(renderer, label, fs, avail_line_px, avail_stack_px, extra_lines=1):
    """Fewest-line wrap of `label` whose widest line fits `avail_line_px` and whose stack
    (lines + extra_lines for the dims) fits `avail_stack_px`. None if it can't fit at all."""
    aw, ah = avail_line_px - _PX_PAD, avail_stack_px - _PX_PAD
    if aw < 14 or ah < 14:
        return None
    lh = _txt_wh(renderer, "Ag", fs)[1] * 1.35
    chosen = None
    for ncols in range(4, len(label) + 1):
        lines = textwrap.wrap(label, ncols) or [label]
        if max(_txt_wh(renderer, ln, fs)[0] for ln in lines) <= aw:
            chosen = lines                                     # keep the widest (fewest-line) fit
    if chosen is None or (len(chosen) + extra_lines) * lh > ah:
        return None
    return chosen


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — OPTIMIZED NESTING (bin-packed stock sheets, pieces mixed across subsystems)
# ═══════════════════════════════════════════════════════════════════════════════
def draw_sheet2():
    fig = plt.figure(figsize=(22, 9))              # wide, to match the row-of-sheets content aspect
    fig.patch.set_facecolor(C_BG)
    ax = fig.add_axes([0.035, 0.11, 0.93, 0.80])
    ax.set_facecolor(C_BG)
    ax.set_aspect("equal", adjustable="datalim")   # keep the axes box put (don't shrink onto the title block)
    ax.axis("off")

    # every physical sheet, in group order, with its sequential buyer letter (A, B, C…)
    sheets = []
    for g, bins in PACKED:
        letters = _SHEET_LETTERS[g["gid"]]
        for i, pl in enumerate(bins):
            sheets.append((letters[i], g["thick"], g["stock"], pl))

    COLS = 4
    GAPX, GAPY = 720, 1050
    CELLW, CELLH = 1220, 2440
    origins = []
    for idx in range(len(sheets)):
        origins.append((idx % COLS * (CELLW + GAPX), -(idx // COLS) * (CELLH + GAPY)))

    # 1) grounds + piece rectangles + guillotine cut lines + sheet headers
    total_cuts = 0
    for (letter, thick, stock, pl), (ox, oy) in zip(sheets, origins):
        w0, h0 = stock
        used = sum(w * h for (_x, _y, w, h, _l, _r) in pl)
        util = 100 * used / (w0 * h0)
        ncuts, segs = cut_plan(w0, h0, pl)
        total_cuts += ncuts
        ax.add_patch(Rectangle((ox, oy), w0, h0, fc=C_STOCK, ec=C_OUT, lw=1.6, zorder=2))
        for (x, yb, w, h, label, rot) in pl:
            fc = C_STUB if _is_fixed(label) else C_WOOD
            ax.add_patch(Rectangle((ox + x, oy + yb), w, h, fc=fc, ec=C_OUT, lw=1.0, zorder=3))
        placed_badges = []                                      # nudge a badge off any already placed on this sheet
        for n, (sx0, sy0, sx1, sy1) in enumerate(segs, 1):      # guillotine saw cuts, in cut order
            ax.plot([ox + sx0, ox + sx1], [oy + sy0, oy + sy1], color=C_CUT, lw=0.9,
                    ls=(0, (5, 2)), zorder=6)
            vert = abs(sx1 - sx0) < 1                            # slide the badge ALONG its own cut (stays on-sheet)
            lo, hi = (min(sy0, sy1), max(sy0, sy1)) if vert else (min(sx0, sx1), max(sx0, sx1))
            cands = [lo + f * (hi - lo) for f in (0.5, 0.35, 0.65, 0.22, 0.78)]
            spots = [(ox + sx0, oy + c) if vert else (ox + c, oy + sy0) for c in cands]
            bx, by = next((s for s in spots
                           if all((s[0] - px) ** 2 + (s[1] - py) ** 2 > (2 * 56) ** 2 for px, py in placed_badges)),
                          spots[0])
            placed_badges.append((bx, by))
            ax.add_patch(Circle((bx, by), 56, fc="white", ec=C_CUT, lw=0.9, zorder=7))
            ax.text(bx, by, str(n), ha="center", va="center", fontsize=5.0,
                    fontweight="bold", color=C_CUT, zorder=8, **FONT)
        ax.text(ox + w0 / 2, oy + h0 + 120, f"SHEET {letter}", ha="center", fontsize=9.0,
                fontweight="bold", color=C_OUT, **FONT)
        ax.text(ox + w0 / 2, oy + h0 + 34, f"{thick}mm · {w0}×{h0} · {util:.0f}% used · {ncuts} cuts",
                ha="center", fontsize=6.4, color=C_DIM, **FONT)

    # 2) fix the view so transData/renderer are valid for text measurement
    maxx = max(ox + s[2][0] for s, (ox, oy) in zip(sheets, origins))
    minx = min(ox for ox, oy in origins)
    maxy = max(oy + s[2][1] for s, (ox, oy) in zip(sheets, origins))
    miny = min(oy for ox, oy in origins)
    ax.set_xlim(minx - 80, maxx + 780)                         # right pad holds the leader-label column
    ax.set_ylim(miny - 100, maxy + 330)                        # top pad holds the per-sheet header labels
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    dpp_x, dpp_y = _data_per_px(ax)

    # 3) piece labels — wrap inside the box; if it still won't fit, defer to a leader (one per piece)
    for (letter, thick, stock, pl), (ox, oy) in zip(sheets, origins):
        w0, h0 = stock
        leads = []
        for (x, yb, w, h, label, rot) in pl:
            short = ("↻ " if rot else "") + label.split(" (")[0]
            dims = f"{w:g}×{h:g}"
            cx, cy = ox + x + w / 2, oy + yb + h / 2
            bw, bh = _box_px(ax, ox + x, oy + yb, w, h)
            rotate = h > w * 1.5
            lines = _wrap_fit(r, short, _LBL_FS, bh if rotate else bw, bw if rotate else bh)
            if lines is None:
                leads.append((ox + x + w, cy, f"{short}\n{dims}"))
                continue
            # center the (label block + dims line) as one stack; label above, dims one line below
            lh = _txt_wh(r, "Ag", _LBL_FS)[1] * 1.3 * (dpp_x if rotate else dpp_y)
            n = len(lines)
            body = "\n".join(lines)
            lbl_off, dim_off = lh / 2, n * lh / 2               # label center up ½ line; dims center down n/2 lines
            if rotate:
                ax.text(cx + lbl_off, cy, body, rotation=90, ha="center", va="center",
                        linespacing=1.3, fontsize=_LBL_FS, color=C_OUT, **FONT)
                ax.text(cx - dim_off, cy, dims, rotation=90, ha="center", va="center",
                        fontsize=_LBL_FS - 0.6, color=C_DIM, **FONT)
            else:
                ax.text(cx, cy + lbl_off, body, ha="center", va="center",
                        linespacing=1.3, fontsize=_LBL_FS, color=C_OUT, **FONT)
                ax.text(cx, cy - dim_off, dims, ha="center", va="center",
                        fontsize=_LBL_FS - 0.6, color=C_DIM, **FONT)
        # leader column down the sheet's right gap
        lx = ox + w0 + 80
        for i, (tipx, tipy, txt) in enumerate(leads):
            ly = oy + h0 - 60 - (i + 0.5) * ((h0 - 120) / max(len(leads), 1))
            leader(ax, tipx, tipy, lx, ly, txt, fs=5.0, color=C_OUT, ha="left",
                   va="center", arrow_style="-", lw=0.6, font=FONT)

    fig.text(0.5, 0.975, "PLYWOOD NESTING — OPTIMIZED CUT LAYOUT",
             ha="center", fontsize=14, fontweight="bold", color=C_OUT, **FONT)
    fig.text(0.5, 0.952, f"guillotine nest (every cut is a 90° edge-to-edge panel-saw cut) · "
             f"{OPT_TOTAL} stock sheets (from {NAIVE_TOTAL} part-by-part) · {total_cuts} cuts total · "
             f"↻ = rotated · ‑ ‑ ⓝ = saw cuts numbered in cutting order · shaded = FIXED piece",
             ha="center", fontsize=8.5, color=C_DIM, **FONT)

    ax_tb = fig.add_axes([0.035, 0.02, 0.93, 0.08])
    ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis("off")
    title_block(ax_tb, f"SHEET 2 OF {TOTAL_SHEETS}", drawing_title="PLYWOOD CUT SHEETS",
                subtitle=f"GUILLOTINE NESTING — {OPT_TOTAL} SHEETS · {total_cuts} CUTS",
                scale_note="PIECES TO SCALE ON 4×8 STOCK · ALL DIMS IN mm",
                doc_id="TBS-001 · Plywood Cut Sheets", height=0.92)
    _save(fig, "plywood-cutsheets-sheet2.png", tight=False)


if __name__ == "__main__":
    print("Generating plywood cut sheets...")
    draw_sheet1()
    draw_sheet2()
    print("Done.")
