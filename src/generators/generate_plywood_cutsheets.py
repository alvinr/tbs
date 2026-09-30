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

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.path.insert(0, os.path.dirname(__file__))
from tbs_constants import (                                    # noqa: E402
    DIAGRAMS_DIR,
    PANEL_CORNER_YD_L, PANEL_CORNER_YD_R, APRON_FIX_W, C_WID,
    PANEL_FLOOR_GAP, PANEL_FLOOR_GAP_SIDE,
    PWP_PANEL_X0, PWP_PANEL_X1, SHELF_W, SHELF_DEPTH,
)
from tbs_drawing import draw_notes                            # noqa: E402
from tbs_title_block import title_block                        # noqa: E402

TOTAL_SHEETS = 2
C_BG = "#FAFAFA"
FONT = {"fontfamily": "monospace"}
C_OUT = "#1A1A1A"
C_DIM = "#404040"
C_WOOD = "#D8C39A"       # plywood face
C_STOCK = "#F0E9D8"      # stock-sheet ground
C_STUB = "#C7B48A"       # fixed (non-fold) piece, distinguished from a fold-down apron

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
            ("Shirt standoff cleat", 40, 120, 6, "shirt-to-rear-panel standoff blocks"),
        ]),
        dict(key="pinhole-panel-ply-18", stock=STOCK_8x4, npieced=2, pieces=[
            ("Pinhole backing half", PINHOLE_HALF, 1440, 2, f"3× Big Blue filters + P-04/SV-02/DV-02 skid row; 2 halves butt-jointed → the full {PINHOLE_W}×1440 face (>1219 stock width)"),
        ]),
    ]),
    dict(gid="B", thick=18, grade="18mm SANDEPLY Sande hardwood plywood",
         sku="Home Depot 203414066", stock=STOCK_HD, parts=[
        dict(key="ep-backing-panel", stock=STOCK_HD, pieces=[
            ("EP electrical backboard", 700, 2000, 1, "interior wall electrical backboard — MPPT / battery / inverter / disconnects / IP65 box"),
        ]),
    ]),
    dict(gid="C", thick=18, grade='¾" CC pressure-treated pine',
         sku="Home Depot 206343229", stock=STOCK_8x4, parts=[
        dict(key="panel-fanb-ply", stock=STOCK_8x4, pieces=[
            ("Fan-B mount band", 610, 1220, 1, "hinged-panel near-corner rigid fan/duct mount band"),
            ("Cooler stowage base", 600, 350, 1, "evap-cooler stowage base (cargo-door end)"),
        ]),
    ]),
    dict(gid="D", thick=18, grade="18mm UV-coated white hardwood (Swaner)",
         sku="Home Depot 302874373", stock=STOCK_HD, parts=[
        dict(key="shelf-phenolic-ply", stock=STOCK_HD, pieces=[
            ("Chem-prep shelf board", SHELF_W, SHELF_DEPTH, 1, "fold-down chemistry-prep work surface (pinhole wall)"),
        ]),
    ]),
    dict(gid="E", thick=12, grade="12mm exterior BC plywood (flat-black interior face)",
         sku="standard exterior", stock=STOCK_8x4, parts=[
        dict(key="panel-bottom-apron", stock=STOCK_8x4, pieces=[
            ("Near fold-down light apron", APR_NEAR_W, APR_CORNER_H, 1, "seals under-leaf light gap, near corner"),
            ("Far fold-down light apron", APR_FAR_W, APR_CORNER_H, 1, "seals under-leaf light gap, far corner"),
            ("Fixed pivot stub", APRON_FIX_W, APR_CORNER_H, 1, "fixed strip clearing the Ø220 pivot mount plate"),
            ("Fixed center baffle", BAFFLE_W, APR_CENTER_H, 1, "fixed light baffle under the drum bay"),
        ]),
    ]),
]

# dims that DERIVE from a tbs_constants value (shown with a ᴰ marker in the schedule)
_DERIVED = {PINHOLE_W, PINHOLE_HALF, APR_NEAR_W, APR_FAR_W, APRON_FIX_W, BAFFLE_W,
            APR_CORNER_H, APR_CENTER_H, SHELF_W, SHELF_DEPTH}


def _save(fig, fname):
    os.makedirs(DIAGRAMS_DIR, exist_ok=True)
    png = os.path.join(DIAGRAMS_DIR, fname)
    fig.savefig(png, dpi=150, bbox_inches="tight", facecolor=C_BG)
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
    ax.text(CX["grp"], HDR_Y, "GRP", fontsize=8, fontweight="bold", color=C_OUT, **FONT)
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
        ax.text(CX["grp"], y, g["gid"], fontsize=9, fontweight="bold", color=C_OUT, **FONT)
        nsheets = sum(p.get("npieced", 1) for p in g["parts"])
        ax.text(CX["piece"], y, f"{g['grade']}  ·  {g['sku']}  ·  "
                f"{nsheets}× {g['stock'][0]}×{g['stock'][1]} stock sheet(s)",
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
        "• Buy one stock sheet per row in the group band (Group A's three parts share SKU 303564747 and may nest — carried separate for cut margin).",
        "• ᴰ dims derive from tbs_constants and update with the geometry; plain dims are spec/report literals. Cost, supplier and SKU live in parts.py (the key on each part's └ line).",
        "• The cut LAYOUT (how the pieces nest on each 4×8) is Sheet 2. Fabrication detail for a piece (hole positions, edge seal, hinge line) stays on its owning subsystem sheet.",
    ], 2, 14.5, spacing=2.6, fs=7.2, title_fs=8.0, width=96, wrap=150,
       color=C_OUT, title_color=C_OUT, border_color=C_DIM, font=FONT)

    ax_tb = fig.add_axes([0.03, 0.008, 0.94, 0.045])
    ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis("off")
    title_block(ax_tb, f"SHEET 1 OF {TOTAL_SHEETS}", drawing_title="PLYWOOD CUT SHEETS",
                subtitle="PLYWOOD SCHEDULE — ALL SUBSYSTEMS",
                scale_note="SCHEDULE · ALL DIMS IN mm", doc_id="TBS-001 · Plywood Cut Sheets")
    _save(fig, "plywood-cutsheets-sheet1.png")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — NESTING LAYOUT (each stock sheet with its pieces shelf-packed)
# ═══════════════════════════════════════════════════════════════════════════════
def _pack(pieces, stock_w, margin=25):
    """Shelf-pack (row-major, tallest first) → [(x, y, w, h, label)] in mm on the stock sheet."""
    items = []
    for (label, w, h, q, _where) in pieces:
        for i in range(q):
            items.append((f"{label}" + (f" #{i+1}" if q > 1 else ""), w, h))
    items.sort(key=lambda it: -it[2])
    out = []
    x = margin
    y = margin
    rowh = 0
    for (label, w, h) in items:
        if x + w > stock_w - margin and x > margin:
            x = margin
            y += rowh + margin
            rowh = 0
        out.append((x, y, w, h, label))
        x += w + margin
        rowh = max(rowh, h)
    return out


def draw_sheet2():
    fig = plt.figure(figsize=(20, 14))
    fig.patch.set_facecolor(C_BG)
    ax = fig.add_axes([0.04, 0.06, 0.92, 0.88])
    ax.set_facecolor(C_BG)
    ax.set_aspect("equal")
    ax.axis("off")

    # flatten to individual stock sheets (a part with npieced=N draws N stock sheets)
    sheets = []
    for g in GROUPS:
        for p in g["parts"]:
            n = p.get("npieced", 1)
            for i in range(n):
                # when pieced, each stock sheet carries a half of each qty-N piece
                pcs = []
                for (label, w, h, q, where) in p["pieces"]:
                    if n > 1:
                        pcs.append((label, w, h, max(1, q // n), where))
                    else:
                        pcs.append((label, w, h, q, where))
                sheets.append((g["gid"], p["key"] + (f"  ({i+1}/{n})" if n > 1 else ""),
                               p["stock"], pcs))

    # tile the stock sheets in a grid, drawn at 1:1 mm with gaps
    COLS = 4
    GAPX, GAPY = 620, 900
    sw, sh = STOCK_8x4
    for idx, (gid, key, stock, pcs) in enumerate(sheets):
        col = idx % COLS
        row = idx // COLS
        ox = col * (sw + GAPX)
        oy = -row * (sh + GAPY)
        w0, h0 = stock
        # stock sheet
        ax.add_patch(Rectangle((ox, oy), w0, h0, fc=C_STOCK, ec=C_OUT, lw=1.6, zorder=2))
        ax.text(ox + w0 / 2, oy + h0 + 90, f"[{gid}] {key}", ha="center", fontsize=7.6,
                fontweight="bold", color=C_OUT, **FONT)
        ax.text(ox + w0 / 2, oy + h0 + 18, f"{w0}×{h0} stock", ha="center", fontsize=6.2,
                color=C_DIM, **FONT)
        # packed pieces
        for (x, yb, w, h, label) in _pack(pcs, w0):
            fc = C_STUB if ("Fixed" in label or "stub" in label or "baffle" in label) else C_WOOD
            ax.add_patch(Rectangle((ox + x, oy + yb), w, h, fc=fc, ec=C_OUT, lw=1.0, zorder=3))
            short = label.split(" (")[0]
            cx, cy = ox + x + w / 2, oy + yb + h / 2
            if h > w * 1.6:                                 # rotate; separate label/dim ACROSS the width
                ax.text(cx - 26, cy, short[:24], ha="center", va="center", fontsize=5.4,
                        color=C_OUT, rotation=90, **FONT)
                ax.text(cx + 26, cy, f"{w:g}×{h:g}", ha="center", va="center", fontsize=5.0,
                        color=C_DIM, rotation=90, **FONT)
            else:
                ax.text(cx, cy + 34, short[:24], ha="center", va="center", fontsize=5.4,
                        color=C_OUT, **FONT)
                ax.text(cx, cy - 44, f"{w:g}×{h:g}", ha="center", va="center", fontsize=5.0,
                        color=C_DIM, **FONT)

    ax.autoscale_view()
    ax.text(0.5, 1.005, "PLYWOOD NESTING — CUT LAYOUT PER STOCK SHEET", transform=ax.transAxes,
            ha="center", fontsize=13, fontweight="bold", color=C_OUT, **FONT)
    ax.text(0.5, 0.985, "illustrative shelf-pack (not optimized) · pieces to scale on the 4×8 stock · "
            "shaded = FIXED (non-fold) piece",
            transform=ax.transAxes, ha="center", fontsize=8, color=C_DIM, **FONT)

    ax_tb = fig.add_axes([0.04, 0.008, 0.92, 0.045])
    ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis("off")
    title_block(ax_tb, f"SHEET 2 OF {TOTAL_SHEETS}", drawing_title="PLYWOOD CUT SHEETS",
                subtitle="NESTING LAYOUT — CUT PER STOCK SHEET",
                scale_note="PIECES TO SCALE ON 4×8 STOCK · ALL DIMS IN mm",
                doc_id="TBS-001 · Plywood Cut Sheets")
    _save(fig, "plywood-cutsheets-sheet2.png")


if __name__ == "__main__":
    print("Generating plywood cut sheets...")
    draw_sheet1()
    draw_sheet2()
    print("Done.")
