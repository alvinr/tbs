#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_lighttrap_diagram.py
TBS-001  Revolving Light-Trap — fabrication blueprint set (6 sheets).

Sheet 1: General Arrangement — vertical section on the drum axis
Sheet 2: Housing cylinder — cut sheet (flat pattern)
Sheet 3: Rotating drum — cut sheet (flat pattern) + caps
Sheet 4: Bearing hub & stub-shaft detail
Sheet 5: Seals & light-path verification
Sheet 6: Drum cage / support frame

All geometry reads from tbs_constants.py (single source of truth). Bearing /
seal / hardware specs trace to light-trap-selection.md §4.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
import os

from tbs_constants import (
    C_OUT, C_CL, C_DIM, C_ALUM, C_STEEL, C_GASKT, C_LT_DRUM,
    DRUM_CX, DRUM_CY, DRUM_D, DRUM_R, DRUM_H_LT, PANEL_FLOOR_GAP,
    LT_HOUSING_R, LT_HOUSING_T, LT_DRUM_OR, LT_DRUM_T, LT_CAP_T, LT_OPENING_DEG,
    DRUM_CAGE_X0, DRUM_CAGE_X1, DRUM_CAGE_YD_L, DRUM_CAGE_YD_R,
    DIAGRAM_DPI, DIAGRAMS_DIR,
)
from tbs_drawing import (
    draw_dim_h, draw_dim_v, draw_rect, draw_circle, draw_cl_v,
    leader, draw_notes, bolt_holes,
)
from tbs_title_block import title_block

BG = "white"
FONT = {"fontfamily": "monospace"}
TITLE_COL = "#0F2D5E"

# ── SKF 6215-2RS1 sealed deep-groove bearing (light-trap-selection.md §4.2) ──
#    Not in tbs_constants — bearing catalog dims, local to these drawings.
SKF6215_ID = 75    # bore Ø (mm)
SKF6215_OD = 130   # outer Ø (mm)
SKF6215_W  = 25    # width (mm)

# ── SS grab rail (light-trap-selection.md §4.4) ─────────────────────────────
GRAB_D = 100   # rail Ø (mm)
GRAB_L = 400   # rail length (mm)
GRAB_Z = 900   # mounting height above floor (mm)

# ── Derived running clearance (drum OD → housing bore), single-sourced ───────
RUN_GAP = LT_HOUSING_R - LT_HOUSING_T - LT_DRUM_OR   # radial gap, mm


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 1 — General Arrangement
# Vertical section on the drum axis (view looks along +Yd):
#   horizontal axis = X depth (exterior → interior), vertical axis = Z height.
# ═════════════════════════════════════════════════════════════════════════════
def draw_sheet1():
    # ── Key positions in mm (all from constants) ─────────────────────────────
    X_AX = DRUM_CX                       # drum axis X (= -400)
    HO_L = X_AX - LT_HOUSING_R           # housing outer, exterior side
    HO_R = X_AX + LT_HOUSING_R           # housing outer, interior side
    HI_L = HO_L + LT_HOUSING_T           # housing inner (bore) faces
    HI_R = HO_R - LT_HOUSING_T
    DO_L = X_AX - LT_DRUM_OR             # drum shell outer faces
    DO_R = X_AX + LT_DRUM_OR
    DI_L = DO_L + LT_DRUM_T              # drum shell inner faces
    DI_R = DO_R - LT_DRUM_T

    Z_BOT = PANEL_FLOOR_GAP              # assembly bottom (= 130)
    Z_TOP = DRUM_H_LT                    # assembly top (= 2250)
    Z_CAP_B = Z_BOT + 40                 # bottom cap plane (bearing zone below)
    Z_CAP_T = Z_TOP - 40                 # top cap plane (bearing zone above)

    # ── Data window → figure size (aspect equal, mm units) ───────────────────
    PAD_L, PAD_R = 720, 1560
    PAD_B, PAD_T = 560, 540
    X_LO, X_HI = HO_L - PAD_L, HO_R + PAD_R
    Z_LO, Z_HI = 0 - PAD_B, Z_TOP + PAD_T

    FIG_H = 13.0
    FIG_W = FIG_H * (X_HI - X_LO) / (Z_HI - Z_LO)
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DIAGRAM_DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Z_LO, Z_HI)
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Environment zones + floor ────────────────────────────────────────────
    ax.add_patch(plt.Rectangle((X_LO, Z_LO), HO_L - X_LO, Z_HI - Z_LO,
                               fc="#EEF2F8", ec="none", zorder=1))
    ax.text((X_LO + HO_L) / 2, Z_TOP, "EXTERIOR", color="#5060A0", fontsize=10,
            ha="center", va="center", fontweight="bold", alpha=0.55, **FONT, zorder=15)
    ax.add_patch(plt.Rectangle((HO_R, Z_LO), X_HI - HO_R, Z_HI - Z_LO,
                               fc="#EEF6EE", ec="none", zorder=1))
    ax.text(X_HI - 340, 300, "INTERIOR\n(DARKROOM / WALKWAY)", color="#407040",
            fontsize=9, ha="center", va="center", fontweight="bold", alpha=0.55,
            **FONT, zorder=15)
    ax.add_patch(plt.Rectangle((X_LO, -PAD_B), X_HI - X_LO, PAD_B,
                               fc="#D8D0C0", ec="none", zorder=1))
    ax.plot([X_LO, X_HI], [0, 0], color=C_OUT, lw=1.6, zorder=4)
    ax.text(X_LO + 30, -150, "FLOOR LEVEL", ha="left", va="center",
            fontsize=7.5, color=C_DIM, **FONT, zorder=15)

    # ── Fixed housing walls (Ø900, 5mm UV-HDPE) ──────────────────────────────
    for x0 in (HO_L, HI_R):
        draw_rect(ax, x0, Z_BOT, LT_HOUSING_T, Z_TOP - Z_BOT,
                  fc="#DDE4EC", lw=1.4, zorder=5)
    leader(ax, HO_L + LT_HOUSING_T / 2, 1780,
           HO_L - 250, 1780,
           f"FIXED HOUSING\nØ{DRUM_D} · {LT_HOUSING_T}mm UV-HDPE",
           fs=7, color=C_OUT, ha="center", arrow_style="->", font=FONT)

    # ── Rotating drum shell (Ø864, 1/8in HDPE) ───────────────────────────────
    for x0 in (DO_L, DI_R):
        draw_rect(ax, x0, Z_CAP_B, LT_DRUM_T, Z_CAP_T - Z_CAP_B,
                  fc=C_LT_DRUM, lw=1.4, zorder=6)
    leader(ax, DO_L + LT_DRUM_T / 2, 1330,
           HO_L - 250, 1330,
           f"ROTATING DRUM\nØ{2 * LT_DRUM_OR} · {LT_DRUM_T:.2f}mm (1/8in) HDPE\nsingle {LT_OPENING_DEG}° opening",
           fs=7, color=C_OUT, ha="center", arrow_style="->", font=FONT)

    # ── Top + bottom caps (3/16in HDPE, carry the stub shafts) ───────────────
    for z in (Z_CAP_T, Z_CAP_B - LT_CAP_T):
        draw_rect(ax, DI_L, z, DI_R - DI_L, LT_CAP_T, fc="#D9CFB8", lw=1.2, zorder=7)

    # ── Rotation axis + stub shafts + SKF 6215 bearings ──────────────────────
    draw_cl_v(ax, X_AX, Z_LO + 120, Z_HI - 120)          # drum rotation axis
    for z_brg in (Z_TOP - SKF6215_W, Z_BOT):
        draw_rect(ax, X_AX - SKF6215_OD / 2, z_brg, SKF6215_OD, SKF6215_W,
                  fc=C_STEEL, lw=1.2, zorder=8)
        draw_rect(ax, X_AX - SKF6215_ID / 2, z_brg, SKF6215_ID, SKF6215_W,
                  fc="white", lw=0.8, zorder=9)
    draw_rect(ax, X_AX - 18, Z_CAP_T, 36, (Z_TOP - SKF6215_W) - Z_CAP_T,
              fc=C_STEEL, lw=1.0, zorder=8)
    draw_rect(ax, X_AX - 18, Z_BOT + SKF6215_W, 36,
              (Z_CAP_B - LT_CAP_T) - (Z_BOT + SKF6215_W), fc=C_STEEL, lw=1.0, zorder=8)
    leader(ax, X_AX + SKF6215_OD / 2, Z_TOP - SKF6215_W / 2,
           HO_R + 340, Z_TOP + 240,
           f"UPPER: {LT_CAP_T:.2f}mm (3/16in) cap + stub shaft →\n"
           f"SKF 6215-2RS1 (Ø{SKF6215_ID} bore) · isolated Al top ring, 6×M10",
           fs=6.5, color=C_OUT, ha="center", arrow_style="->", font=FONT)
    leader(ax, X_AX - SKF6215_OD / 2, Z_BOT + SKF6215_W / 2,
           X_LO + 250, Z_BOT - 20,
           f"LOWER: {LT_CAP_T:.2f}mm (3/16in) cap + stub shaft →\n"
           f"SKF 6215-2RS1 · welded steel floor collar, 8×M10",
           fs=6.5, color=C_OUT, ha="center", arrow_style="->", font=FONT)

    # ── Grab rail — VERTICAL bar inside the bore, interior-side wall ──────────
    GX = DI_R - GRAB_D / 2 - 15          # rail center X, inside the bore
    GZ0, GZ1 = GRAB_Z - GRAB_L / 2, GRAB_Z + GRAB_L / 2
    draw_rect(ax, GX - GRAB_D / 2, GZ0, GRAB_D, GRAB_L, lw=1.4,
              fc="#C9CCD2", zorder=9)
    for zb in (GZ0 + 40, GZ1 - 40):      # welded bracket stubs to the drum wall
        draw_rect(ax, GX + GRAB_D / 2, zb - 12, DI_R - (GX + GRAB_D / 2), 24,
                  lw=1.0, fc=C_STEEL, zorder=8)
    leader(ax, GX, GRAB_Z,
           HO_R + 330, GRAB_Z - 380,
           f"GRAB RAIL Ø{GRAB_D}×{GRAB_L} SS (vertical)\ninside bore, interior side · {GRAB_Z}mm AFF",
           fs=6.5, color=C_OUT, ha="center", arrow_style="->", font=FONT)

    # ── Dimensions ───────────────────────────────────────────────────────────
    draw_dim_h(ax, HO_L, HO_R, Z_TOP + 300, f"Ø{DRUM_D} HOUSING OD",
               offset=90, fs=7, font=FONT)
    draw_dim_v(ax, HO_L - 300, Z_BOT, Z_TOP,
               f"{DRUM_H_LT - PANEL_FLOOR_GAP}mm CLEAR", offset=95, fs=7, font=FONT)
    draw_dim_v(ax, X_HI - 160, 0, Z_TOP, f"{DRUM_H_LT}mm TOP AFF",
               offset=95, fs=7, right=True, font=FONT)
    leader(ax, HI_R - 2, 1320,
           HO_R + 330, 1720,
           f"≈{RUN_GAP}mm radial running gap\n(drum OD → housing bore; sealed — Sheet 5)",
           fs=6.5, color=C_DIM, ha="center", arrow_style="->", font=FONT)

    # ── Inset plan (schematic): opening orientation ──────────────────────────
    px, pz, pr = X_HI - 520, Z_TOP + 180, 300
    draw_circle(ax, px, pz, pr, lw=1.4, color=C_OUT, zorder=6)
    draw_circle(ax, px, pz, pr * (LT_DRUM_OR / LT_HOUSING_R), lw=1.0,
                color=C_DIM, ls="--", zorder=6)
    for t0, col in ((180 - LT_OPENING_DEG / 2, "#5060A0"),
                    (-LT_OPENING_DEG / 2, "#407040")):
        ax.add_patch(mpatches.Wedge((px, pz), pr, t0, t0 + LT_OPENING_DEG,
                                    width=pr * 0.16, fc=col, ec=C_OUT, lw=0.6,
                                    alpha=0.75, zorder=7))
    ax.text(px - pr - 30, pz, "EXT", ha="right", va="center", fontsize=6.5,
            color="#5060A0", **FONT, zorder=15)
    ax.text(px + pr + 30, pz, "INT", ha="left", va="center", fontsize=6.5,
            color="#407040", **FONT, zorder=15)
    ax.text(px, pz - pr - 60,
            f"PLAN (schematic) — two {LT_OPENING_DEG}° openings\n180° apart · detail Sheets 2 & 5",
            ha="center", va="top", fontsize=6.5, color=C_DIM, **FONT, zorder=15)

    # ── Bill of materials ────────────────────────────────────────────────────
    bom = [
        "BILL OF MATERIALS",
        f"1 HOUSING SKIN  1  {LT_HOUSING_T}mm UV-HDPE, Ø{DRUM_D}",
        f"2 DRUM SHELL    1  {LT_DRUM_T:.2f}mm (1/8in) HDPE, Ø{2 * LT_DRUM_OR}",
        f"3 DRUM CAPS     2  {LT_CAP_T:.2f}mm (3/16in) HDPE",
        f"4 BEARING       2  SKF 6215-2RS1 (Ø{SKF6215_ID} bore)",
        "5 SEALS         -  12/20mm neoprene + silicone",
        f"6 GRAB RAIL     1  Ø{GRAB_D}×{GRAB_L} SS round",
    ]
    draw_notes(ax, bom, HO_R + 720, 1600, 135, fs=6.8, font=FONT,
               width=980, title_color=TITLE_COL)

    title_block(ax, "SHEET 1 OF 6", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="GENERAL ARRANGEMENT — VERTICAL SECTION ON DRUM AXIS",
                scale_note="ALL DIMS IN mm", doc_id="TBS-001 · Revolving Light-Trap",
                height=0.045, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet1.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet1.png saved")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 2 — Housing cylinder cut sheet (flat pattern)
# The 5mm UV-HDPE skin developed flat: roll to Ø900 and extrusion-weld the seam,
# then cut the two 80° openings. Developed length = π·Ø900.
# ═════════════════════════════════════════════════════════════════════════════
def draw_sheet2():
    L        = math.pi * DRUM_D                       # developed length
    HOUSING_H = DRUM_H_LT - PANEL_FLOOR_GAP           # blank height = 2120
    OW       = (LT_OPENING_DEG / 360.0) * L           # opening arc width
    SEAM_DEG = 90                                     # seam falls mid-solid-arc (near-Yd)

    def dev(theta):                                   # angle → developed x from seam
        return ((theta - SEAM_DEG) % 360) / 360.0 * L

    # Opening cut positions along the developed width (EXT @180°, INT @0°) ──────
    ext_x0, ext_x1 = dev(180 - LT_OPENING_DEG / 2), dev(180 + LT_OPENING_DEG / 2)
    int_x0, int_x1 = dev(360 - LT_OPENING_DEG / 2), dev(360 + LT_OPENING_DEG / 2)
    # Sill + header bands keep the welded cylinder continuous (chosen cut heights).
    SILL_H, HEADER_H = 80, 150
    op_z0, op_z1 = SILL_H, HOUSING_H - HEADER_H

    # ── Data window → figure size ────────────────────────────────────────────
    PAD_L, PAD_R, PAD_B, PAD_T = 520, 520, 1180, 470
    X_LO, X_HI = -PAD_L, L + PAD_R
    Z_LO, Z_HI = -PAD_B, HOUSING_H + PAD_T
    FIG_W = 18.0
    FIG_H = FIG_W * (Z_HI - Z_LO) / (X_HI - X_LO)
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DIAGRAM_DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Z_LO, Z_HI)
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Developed blank ──────────────────────────────────────────────────────
    draw_rect(ax, 0, 0, L, HOUSING_H, fc="#DDE4EC", lw=2.0, zorder=3)
    # ── Two 80° opening cutouts ──────────────────────────────────────────────
    for x0, x1, tag, col in ((ext_x0, ext_x1, "EXTERIOR OPENING", "#5060A0"),
                             (int_x0, int_x1, "INTERIOR OPENING\n(onto walkway)", "#407040")):
        draw_rect(ax, x0, op_z0, x1 - x0, op_z1 - op_z0, fc="white", lw=1.6, zorder=5)
        ax.plot([x0, x1], [op_z0, op_z1], color=C_DIM, lw=0.5, ls=":", zorder=5)
        ax.plot([x0, x1], [op_z1, op_z0], color=C_DIM, lw=0.5, ls=":", zorder=5)
        ax.text((x0 + x1) / 2, (op_z0 + op_z1) / 2, f"{tag}\n{LT_OPENING_DEG}° · CUT OUT",
                ha="center", va="center", fontsize=8, color=col, fontweight="bold",
                **FONT, zorder=15)

    # ── Weld seam (blank edges join here; mid-solid-arc at θ=90°) ─────────────
    for xs in (0, L):
        ax.plot([xs, xs], [0, HOUSING_H], color="#CC4422", lw=2.4, zorder=6)
    leader(ax, 0, HOUSING_H * 0.62, -300, HOUSING_H * 0.62,
           "ROLL + EXTRUSION\nWELD SEAM\n(edges joined; seam\nmid-arc at 90°)",
           fs=6.5, color="#CC4422", ha="center", arrow_style="->", font=FONT)

    # ── Angular registration ticks along the top edge ────────────────────────
    for theta, lab in ((90, "90° SEAM"), (180, "180° EXT"), (270, "270°"),
                       (360, "0/360° INT")):
        xd = dev(theta) if theta != 90 else 0
        ax.plot([xd, xd], [HOUSING_H, HOUSING_H + 55], color=C_CL, lw=0.7, zorder=6)
        ax.text(xd, HOUSING_H + 70, lab, ha="center", va="bottom", fontsize=6,
                color=C_CL, **FONT, zorder=15)

    # ── Dimensions ───────────────────────────────────────────────────────────
    draw_dim_h(ax, 0, L, HOUSING_H + 230,
               f"DEVELOPED LENGTH = π·Ø{DRUM_D} = {L:.0f}mm", offset=80, fs=8, font=FONT)
    draw_dim_v(ax, -150, 0, HOUSING_H, f"{HOUSING_H}mm BLANK HEIGHT",
               offset=90, fs=7.5, font=FONT)
    draw_dim_h(ax, ext_x0, ext_x1, op_z1 + 90,
               f"{OW:.0f}mm ({LT_OPENING_DEG}° arc)", offset=55, fs=6.5, font=FONT)
    draw_dim_h(ax, int_x0, int_x1, op_z1 + 90,
               f"{OW:.0f}mm ({LT_OPENING_DEG}° arc)", offset=55, fs=6.5, font=FONT)
    draw_dim_h(ax, 0, ext_x0, op_z0 - 120, f"{ext_x0:.0f}mm", offset=50, fs=6.5,
               above=False, font=FONT)
    draw_dim_v(ax, int_x1 + 130, op_z0, op_z1, f"{op_z1 - op_z0:.0f}mm\nOPENING",
               offset=80, fs=6.5, right=True, font=FONT)
    draw_dim_v(ax, L + 130, 0, SILL_H, f"{SILL_H}mm\nSILL", offset=70, fs=6, right=True, font=FONT)
    draw_dim_v(ax, L + 130, HOUSING_H - HEADER_H, HOUSING_H, f"{HEADER_H}mm\nHEADER",
               offset=70, fs=6, right=True, font=FONT)

    # ── Fabrication notes ────────────────────────────────────────────────────
    notes = [
        "HOUSING SKIN — FABRICATION",
        f"Material: {LT_HOUSING_T}mm UV-stabilized HDPE sheet (~7 m²).",
        f"1. Cut blank {L:.0f} × {HOUSING_H}mm; cut the two {LT_OPENING_DEG}° openings.",
        "2. Roll to Ø900 (R450); extrusion-weld the seam (mid-arc, 90°).",
        "3. Interior face black-pigmented + flat-black touch-in at welds.",
        "   Exterior face UV-stabilized — no primer.",
        "FLAT PATTERN · TRUE DEVELOPED SCALE · ALL DIMS IN mm",
    ]
    draw_notes(ax, notes, 40, -240, 100, fs=7, font=FONT, width=1650,
               title_color=TITLE_COL)

    title_block(ax, "SHEET 2 OF 6", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="HOUSING CYLINDER — CUT SHEET (FLAT PATTERN)",
                scale_note="FLAT PATTERN · ALL DIMS IN mm",
                doc_id="TBS-001 · Revolving Light-Trap", height=0.045, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet2.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet2.png saved")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 3 — Rotating drum cut sheet (flat pattern) + caps
# The 1/8in HDPE C-shell developed flat (single 80° opening → 280° of material),
# plus the two 3/16in top/bottom caps with bolted steel stub-shaft hubs.
# ═════════════════════════════════════════════════════════════════════════════
def draw_sheet3():
    DRUM_OD   = 2 * LT_DRUM_OR                          # Ø864
    L_FULL    = math.pi * DRUM_OD                       # full circumference
    W_SHELL   = (360 - LT_OPENING_DEG) / 360.0 * L_FULL # 280° of material
    OW        = (LT_OPENING_DEG / 360.0) * L_FULL       # removed opening arc
    SHELL_H   = DRUM_H_LT - PANEL_FLOOR_GAP - 80        # drum body height (= 2040)
    RUN_GAP_L = LT_HOUSING_R - LT_HOUSING_T - LT_DRUM_OR

    cap_r  = LT_DRUM_OR
    cap_cx = W_SHELL + 360 + cap_r
    cz_top = SHELL_H - cap_r
    cz_bot = cap_r

    # ── Data window → figure size ────────────────────────────────────────────
    PAD_L, PAD_R, PAD_B, PAD_T = 380, 430, 1520, 430
    X_LO, X_HI = -PAD_L, cap_cx + cap_r + PAD_R
    Z_LO, Z_HI = -PAD_B, SHELL_H + PAD_T
    FIG_W = 20.0
    FIG_H = FIG_W * (Z_HI - Z_LO) / (X_HI - X_LO)
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DIAGRAM_DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Z_LO, Z_HI)
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Drum C-shell developed blank ─────────────────────────────────────────
    draw_rect(ax, 0, 0, W_SHELL, SHELL_H, fc=C_LT_DRUM, lw=2.0, zorder=3)
    for xe in (0, W_SHELL):                    # the two opening jambs (free edges)
        ax.plot([xe, xe], [0, SHELL_H], color="#B08020", lw=3.0, zorder=6)
    ax.text(W_SHELL / 2, SHELL_H / 2,
            f"ROTATING DRUM C-SHELL\n{LT_DRUM_T:.2f}mm (1/8in) HDPE\n"
            f"280° of Ø{DRUM_OD} — roll to R{LT_DRUM_OR}",
            ha="center", va="center", fontsize=9, color=C_OUT, fontweight="bold",
            **FONT, zorder=15)
    leader(ax, 0, SHELL_H * 0.28, -300, SHELL_H * 0.28,
           f"OPENING JAMB\n(free edge)", fs=6.5, color="#B08020", ha="center",
           arrow_style="->", font=FONT)
    leader(ax, W_SHELL, SHELL_H * 0.72, W_SHELL + 250, SHELL_H * 0.80,
           f"OPENING JAMB\n(free edge)", fs=6.5, color="#B08020", ha="center",
           arrow_style="->", font=FONT)

    # ── Dimensions (shell) ───────────────────────────────────────────────────
    draw_dim_h(ax, 0, W_SHELL, SHELL_H + 210,
               f"DEVELOPED WIDTH = 280°·π·Ø{DRUM_OD} = {W_SHELL:.0f}mm",
               offset=80, fs=8, font=FONT)
    draw_dim_v(ax, -160, 0, SHELL_H, f"{SHELL_H}mm SHELL HEIGHT",
               offset=90, fs=7.5, font=FONT)
    ax.text(W_SHELL / 2, SHELL_H + 340,
            f"single {LT_OPENING_DEG}° opening removed  ·  arc = {OW:.0f}mm",
            ha="center", va="bottom", fontsize=7, color=C_DIM, **FONT, zorder=15)

    # ── Top + bottom caps (Ø864, 3/16in HDPE, bolted stub-shaft hub) ─────────
    for cz, tag in ((cz_top, "TOP CAP"), (cz_bot, "BOTTOM CAP")):
        draw_circle(ax, cap_cx, cz, cap_r, lw=2.0, color=C_OUT,
                    fill=True, fc="#D9CFB8", zorder=4)
        draw_circle(ax, cap_cx, cz, 78, lw=1.2, color=C_OUT, zorder=6)   # steel hub boss
        draw_circle(ax, cap_cx, cz, SKF6215_ID / 2, lw=1.4, color="#CC4422",
                    zorder=7)                                             # Ø75 stub-shaft bore
        bolt_holes(ax, cap_cx, cz, 55, 4, 6, color=C_OUT, zorder=7)      # 4× M10 flange bolts
        ax.text(cap_cx, cz - cap_r - 55, tag, ha="center", va="top", fontsize=8,
                color=C_OUT, fontweight="bold", **FONT, zorder=15)
    draw_dim_h(ax, cap_cx - cap_r, cap_cx + cap_r, cz_top + cap_r + 90,
               f"Ø{DRUM_OD}", offset=70, fs=7.5, font=FONT)
    leader(ax, cap_cx, cz_top, cap_cx + cap_r + 60, cz_top + 150,
           f"steel stub-shaft hub, 4×M10 to cap\nØ{SKF6215_ID} shaft → SKF 6215 (Sheet 4)",
           fs=6.5, color=C_OUT, ha="center", arrow_style="->", font=FONT)

    # ── Shell → cap weld detail (enlarged, NTS) ──────────────────────────────
    wx, wz = W_SHELL / 2 - 200, -470
    draw_rect(ax, wx, wz, 420, 70, fc="#D9CFB8", lw=1.4, zorder=5)          # cap edge
    draw_rect(ax, wx + 180, wz + 70, 44, 260, fc=C_LT_DRUM, lw=1.4, zorder=5)  # shell wall
    ax.add_patch(mpatches.Polygon([(wx + 180, wz + 70), (wx + 150, wz + 70),
                                   (wx + 180, wz + 130)], closed=True,
                                  fc="#CC4422", ec="#CC4422", zorder=6))
    ax.add_patch(mpatches.Polygon([(wx + 224, wz + 70), (wx + 254, wz + 70),
                                   (wx + 224, wz + 130)], closed=True,
                                  fc="#CC4422", ec="#CC4422", zorder=6))
    leader(ax, wx + 202, wz + 90, wx + 470, wz + 30,
           f"SHELL → CAP\nEXTRUSION FILLET WELD\n(both faces) · DETAIL NTS",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)

    # ── Fabrication notes ────────────────────────────────────────────────────
    notes = [
        "ROTATING DRUM — FABRICATION",
        f"Shell: {LT_DRUM_T:.2f}mm (1/8in) HDPE, blank {W_SHELL:.0f} × {SHELL_H}mm.",
        f"Caps: {LT_CAP_T:.2f}mm (3/16in) HDPE, Ø{DRUM_OD} — cut from housing offcut.",
        f"1. Roll shell to R{LT_DRUM_OR}; the two free edges are the opening jambs.",
        "2. Extrusion-fillet-weld shell to both caps (both faces).",
        "3. Bolt steel stub-shaft hub (4×M10) to each cap; Ø75 shaft to SKF 6215.",
        f"Running clearance to housing bore ≈ {RUN_GAP_L}mm (radial) — see Sheet 5.",
        "FLAT PATTERN · TRUE DEVELOPED SCALE · ALL DIMS IN mm",
    ]
    draw_notes(ax, notes, 40, -560, 92, fs=7, font=FONT, width=1850,
               title_color=TITLE_COL)

    title_block(ax, "SHEET 3 OF 6", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="ROTATING DRUM — CUT SHEET (FLAT PATTERN) + CAPS",
                scale_note="FLAT PATTERN · ALL DIMS IN mm",
                doc_id="TBS-001 · Revolving Light-Trap", height=0.045, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet3.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet3.png saved")


def main():
    print("Generating TBS-001 Revolving Light-Trap blueprint sheets...")
    draw_sheet1()
    draw_sheet2()
    draw_sheet3()
    print("Done.")


if __name__ == "__main__":
    main()
