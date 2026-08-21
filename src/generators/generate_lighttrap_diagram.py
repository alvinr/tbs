#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_lighttrap_diagram.py
TBS-001  Revolving Light-Trap — fabrication blueprint set (7 sheets).

Sheet 1: General Arrangement — vertical section on the drum axis
Sheet 2: Housing cylinder — cut sheet (flat pattern)
Sheet 3: Rotating drum — cut sheet (flat pattern) + caps
Sheet 4: Bearing hub & stub-shaft detail
Sheet 5: Shell → cap lap-and-fasten joint (rivets + DP8010)
Sheet 6: Seals & light-path verification
Sheet 7: Drum cage / support frame

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
    LT_HOUSING_R, LT_HOUSING_T, LT_DRUM_OR, LT_DRUM_T, LT_OPENING_DEG,
    LT_CAP_TOP_T, LT_CAP_BOT_T, LT_CAP_OD, LT_LAP_H, LT_RIVET_D, LT_RIVET_PITCH,
    LT_RIVET_N,
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

    # ── End caps — metal hub discs (top 6061-T6 Al, bottom A36 steel) ────────
    cap_x0 = X_AX - LT_CAP_OD / 2
    draw_rect(ax, cap_x0, Z_CAP_T, LT_CAP_OD, LT_CAP_TOP_T, fc=C_ALUM, lw=1.2, zorder=7)
    draw_rect(ax, cap_x0, Z_CAP_B - LT_CAP_BOT_T, LT_CAP_OD, LT_CAP_BOT_T,
              fc=C_STEEL, lw=1.2, zorder=7)

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
              (Z_CAP_B - LT_CAP_BOT_T) - (Z_BOT + SKF6215_W), fc=C_STEEL, lw=1.0, zorder=8)
    leader(ax, X_AX + SKF6215_OD / 2, Z_TOP - SKF6215_W / 2,
           HO_R + 340, Z_TOP + 240,
           f"UPPER: {LT_CAP_TOP_T:.0f}mm 6061-T6 Al cap + BOLTED stub shaft →\n"
           f"SKF 6215-2RS1 (Ø{SKF6215_ID} bore) · isolated Al top ring, 6×M10",
           fs=6.5, color=C_OUT, ha="center", arrow_style="->", font=FONT)
    leader(ax, X_AX - SKF6215_OD / 2, Z_BOT + SKF6215_W / 2,
           X_LO + 250, Z_BOT - 20,
           f"LOWER: {LT_CAP_BOT_T:.0f}mm A36 steel cap + WELDED stub shaft →\n"
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
    draw_dim_v(ax, GX - GRAB_D / 2 - 55, GZ0, GZ1, f"{GRAB_L}mm", offset=45,
               fs=6.5, font=FONT)
    draw_dim_h(ax, GX - GRAB_D / 2, GX + GRAB_D / 2, GZ1 + 75, f"Ø{GRAB_D}mm",
               offset=45, fs=6.5, font=FONT)
    draw_dim_v(ax, GX - GRAB_D / 2 - 150, 0, GRAB_Z, f"{GRAB_Z}mm AFF\n(floor → rail CL)",
               offset=45, fs=6.5, font=FONT)

    # ── Dimensions ───────────────────────────────────────────────────────────
    draw_dim_h(ax, HO_L, HO_R, Z_TOP + 300, f"Ø{DRUM_D} HOUSING OD",
               offset=90, fs=7, font=FONT)
    draw_dim_v(ax, HO_L - 300, Z_BOT, Z_TOP,
               f"{DRUM_H_LT - PANEL_FLOOR_GAP}mm CLEAR", offset=95, fs=7, font=FONT)
    draw_dim_v(ax, X_HI - 160, 0, Z_TOP, f"{DRUM_H_LT}mm TOP AFF",
               offset=95, fs=7, right=True, font=FONT)
    leader(ax, HI_R - 2, 1320,
           HO_R + 330, 1720,
           f"≈{RUN_GAP}mm radial running gap\n(drum OD → housing bore; sealed — Sheet 6)",
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
            f"PLAN (schematic) — two {LT_OPENING_DEG}° openings\n180° apart · detail Sheets 2 & 6",
            ha="center", va="top", fontsize=6.5, color=C_DIM, **FONT, zorder=15)

    # ── Bill of materials ────────────────────────────────────────────────────
    bom = [
        "BILL OF MATERIALS",
        f"1 HOUSING SKIN  1   {LT_HOUSING_T}mm UV-HDPE, Ø{DRUM_D}",
        f"2 DRUM SHELL    1   {LT_DRUM_T:.2f}mm (1/8in) HDPE, Ø{2 * LT_DRUM_OR}",
        f"3 TOP CAP       1   {LT_CAP_TOP_T:.0f}mm 6061-T6 Al, Ø{LT_CAP_OD}",
        f"4 BOTTOM CAP    1   {LT_CAP_BOT_T:.0f}mm A36 steel, Ø{LT_CAP_OD}",
        f"5 BEARING       2   SKF 6215-2RS1 (Ø{SKF6215_ID} bore)",
        f"6 SHELL RIVETS  {2 * LT_RIVET_N}  Ø{LT_RIVET_D} SS blind (~{LT_RIVET_PITCH}mm pitch)",
        "7 JOINT BOND    -   3M DP8010 (shell→cap lap seal)",
        "8 SEALS         -   12/20mm neoprene + silicone",
        f"9 GRAB RAIL     1   Ø{GRAB_D}×{GRAB_L} SS round",
    ]
    draw_notes(ax, bom, HO_R + 720, 1600, 118, fs=6.8, font=FONT,
               width=1000, title_color=TITLE_COL)

    title_block(ax, "SHEET 1 OF 7", drawing_title="REVOLVING LIGHT-TRAP",
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

    title_block(ax, "SHEET 2 OF 7", drawing_title="REVOLVING LIGHT-TRAP",
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

    cap_r  = LT_CAP_OD / 2
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

    # ── Top + bottom caps (Ø855 metal discs; top Al bolted, bottom steel welded) ──
    # Top cap — 6061-T6 aluminum, bolted stub-shaft flange (4×M10)
    draw_circle(ax, cap_cx, cz_top, cap_r, lw=2.0, color=C_OUT, fill=True,
                fc=C_ALUM, zorder=4)
    draw_circle(ax, cap_cx, cz_top, 78, lw=1.2, color=C_OUT, zorder=6)       # hub boss
    draw_circle(ax, cap_cx, cz_top, SKF6215_ID / 2, lw=1.4, color="#CC4422", zorder=7)
    bolt_holes(ax, cap_cx, cz_top, 55, 4, 6, color=C_OUT, zorder=7)          # 4× M10 flange
    ax.text(cap_cx, cz_top - cap_r - 55, f"TOP CAP\n{LT_CAP_TOP_T:.0f}mm 6061-T6 Al",
            ha="center", va="top", fontsize=8, color=C_OUT, fontweight="bold",
            **FONT, zorder=15)
    # Bottom cap — A36 steel, stub shaft welded (no flange bolts); weld ticks on boss
    draw_circle(ax, cap_cx, cz_bot, cap_r, lw=2.0, color=C_OUT, fill=True,
                fc=C_STEEL, zorder=4)
    draw_circle(ax, cap_cx, cz_bot, 78, lw=1.2, color="#CC4422", zorder=6)   # welded boss
    draw_circle(ax, cap_cx, cz_bot, SKF6215_ID / 2, lw=1.4, color="#CC4422", zorder=7)
    ax.text(cap_cx, cz_bot - cap_r - 55, f"BOTTOM CAP\n{LT_CAP_BOT_T:.0f}mm A36 steel",
            ha="center", va="top", fontsize=8, color=C_OUT, fontweight="bold",
            **FONT, zorder=15)
    draw_dim_h(ax, cap_cx - cap_r, cap_cx + cap_r, cz_top + cap_r + 90,
               f"Ø{LT_CAP_OD}", offset=70, fs=7.5, font=FONT)
    leader(ax, cap_cx + 60, cz_top, cap_cx + cap_r + 70, cz_top + cap_r * 0.7,
           f"TOP: stub-shaft hub BOLTED 4×M10 (Al cap)\nBOTTOM: stub shaft WELDED (steel cap)\n"
           f"Ø{SKF6215_ID} → SKF 6215 (Sheet 4)",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)

    # ── Fabrication notes ────────────────────────────────────────────────────
    notes = [
        "ROTATING DRUM — FABRICATION",
        f"Shell: {LT_DRUM_T:.2f}mm (1/8in) HDPE, blank {W_SHELL:.0f} × {SHELL_H}mm.",
        f"Caps (Ø{LT_CAP_OD}): TOP {LT_CAP_TOP_T:.0f}mm 6061-T6 Al · BOTTOM {LT_CAP_BOT_T:.0f}mm A36 steel.",
        f"1. Roll shell to R{LT_DRUM_OR}; the two free edges are the opening jambs.",
        f"2. Shell laps {LT_LAP_H}mm over each cap rim → {LT_RIVET_N}× Ø{LT_RIVET_D} SS blind rivets/cap + DP8010 bead (see Sheet 5).",
        "3. TOP hub bolted 4×M10 to Al cap; BOTTOM stub shaft welded to steel cap; Ø75 → SKF 6215.",
        f"Running clearance to housing bore ≈ {RUN_GAP_L}mm (radial) — see Sheet 6.",
        "FLAT PATTERN · TRUE DEVELOPED SCALE · ALL DIMS IN mm",
    ]
    draw_notes(ax, notes, 40, -560, 92, fs=7, font=FONT, width=1850,
               title_color=TITLE_COL)

    title_block(ax, "SHEET 3 OF 7", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="ROTATING DRUM — CUT SHEET (FLAT PATTERN) + CAPS",
                scale_note="FLAT PATTERN · ALL DIMS IN mm",
                doc_id="TBS-001 · Revolving Light-Trap", height=0.045, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet3.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet3.png saved")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 4 — Bearing hub & stub-shaft detail
# Two enlarged sections (drum axis vertical): UPPER hub (isolated Al top ring,
# 6×M10) and LOWER hub (welded steel floor collar, 8×M10). SKF 6215-2RS1.
# ═════════════════════════════════════════════════════════════════════════════
def draw_sheet4():
    SC = 2.2                                       # enlargement factor
    rs, ro, bw = SKF6215_ID / 2 * SC, SKF6215_OD / 2 * SC, SKF6215_W / 2 * SC
    CAPd = LT_CAP_TOP_T * SC * 2.4                  # top-cap draw thickness (exaggerated; layout ref)
    UX, LX = 0.0, 1150.0                           # the two hub axes
    HALF = 150 * SC

    # ── Data window → figure size ────────────────────────────────────────────
    PAD_L, PAD_R, PAD_B, PAD_T = 720, 780, 1450, 380
    X_LO, X_HI = UX - HALF - PAD_L, LX + HALF + PAD_R
    Z_LO, Z_HI = -135 * SC - PAD_B, 70 * SC + PAD_T
    FIG_W = 20.0
    FIG_H = FIG_W * (Z_HI - Z_LO) / (X_HI - X_LO)
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DIAGRAM_DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Z_LO, Z_HI)
    ax.set_aspect("equal")
    ax.axis("off")

    def band(cx, r0, r1, z0, z1, **kw):            # symmetric radial band (section)
        draw_rect(ax, cx + r0, z0, r1 - r0, z1 - z0, **kw)
        draw_rect(ax, cx - r1, z0, r1 - r0, z1 - z0, **kw)

    def hub(cx, up):
        s = 1 if up else -1
        # SKF 6215 bearing races + balls + 2RS seals
        band(cx, rs, rs + 9 * SC, -bw, bw, fc=C_STEEL, lw=1.0, zorder=7)
        band(cx, ro - 9 * SC, ro, -bw, bw, fc=C_STEEL, lw=1.0, zorder=7)
        for g in (-1, 1):
            draw_circle(ax, cx + g * (rs + ro) / 2, 0, 6.5 * SC, lw=1.0,
                        color=C_OUT, fill=True, fc="white", zorder=8)
            for zf in (-bw, bw):
                ax.plot([cx + g * (rs + 3 * SC), cx + g * (ro - 3 * SC)], [zf, zf],
                        color="#CC4422", lw=1.2, zorder=8)
        # per-hub cap: 6061-T6 Al (top) / A36 steel (bottom)
        capd = (LT_CAP_TOP_T if up else LT_CAP_BOT_T) * SC * 2.4
        cap_fc = C_ALUM if up else C_STEEL
        zc0, zc1 = -115 * SC * s, -115 * SC * s - capd * s
        # stub shaft Ø75 — reaches the flange face (top) or the cap face (bottom, welded)
        z_stub = 40 * SC * s
        z_fl = (-100 if up else -115) * SC * s
        draw_rect(ax, cx - rs, min(z_stub, z_fl), 2 * rs, abs(z_stub - z_fl),
                  fc=C_STEEL, lw=1.4, zorder=6)
        # housing ring (Al, upper) / floor collar (steel, lower)
        HRr = (100 if up else 105) * SC
        band(cx, ro, HRr, -15 * SC, 15 * SC,
             fc=(C_ALUM if up else C_STEEL), lw=1.4, zorder=5)
        # panel rail / floor plate
        zr0, zr1 = 15 * SC * s, 63 * SC * s
        draw_rect(ax, cx - 140 * SC, min(zr0, zr1), 280 * SC, abs(zr1 - zr0),
                  fc=C_STEEL, lw=1.4, zorder=4)
        # drum cap
        draw_rect(ax, cx - 110 * SC, min(zc0, zc1), 220 * SC, abs(zc1 - zc0),
                  fc=cap_fc, lw=1.4, zorder=6)
        if up:                                     # Al cap → bolted steel stub-shaft flange
            zf0, zf1 = -100 * SC * s, -115 * SC * s
            draw_rect(ax, cx - 80 * SC, min(zf0, zf1), 160 * SC, abs(zf1 - zf0),
                      fc=C_STEEL, lw=1.4, zorder=6)
            for g in (-1, 1):
                ax.plot([cx + g * 55 * SC] * 2, [-100 * SC * s, zc1],
                        color=C_OUT, lw=1.8, zorder=9)       # flange bolts
        else:                                      # steel cap → stub shaft welded (fillets)
            for g in (-1, 1):
                ax.add_patch(mpatches.Polygon(
                    [(cx + g * rs, zc0), (cx + g * rs, zc0 + 22 * SC * s),
                     (cx + g * (rs + 22 * SC), zc0)],
                    closed=True, fc="#CC4422", ec="#CC4422", zorder=9))
        # bearing mount bolts (ring/collar → rail) + circlip grooves
        for g in (-1, 1):
            ax.plot([cx + g * 85 * SC] * 2, [15 * SC * s, 60 * SC * s],
                    color=C_OUT, lw=2.4, zorder=9)
            for zc in (18 * SC, -18 * SC):         # circlip grooves each side
                ax.plot([cx + g * rs, cx + g * (rs - 5 * SC)], [zc, zc],
                        color=C_OUT, lw=1.6, zorder=9)
        if not up:                                 # collar-to-plate weld
            for g in (-1, 1):
                ax.add_patch(mpatches.Polygon(
                    [(cx + g * ro, -15 * SC), (cx + g * ro, -15 * SC - 15 * SC),
                     (cx + g * (ro - 15 * SC), -15 * SC)],
                    closed=True, fc="#CC4422", ec="#CC4422", zorder=9))
        draw_cl_v(ax, cx, -135 * SC, 135 * SC)
        ax.text(cx, 115 * SC + CAPd + 60, "UPPER HUB — DRUM TOP" if up else
                "LOWER HUB — DRUM BOTTOM", ha="center", va="bottom", fontsize=8.5,
                color=TITLE_COL, fontweight="bold", **FONT, zorder=15)

    hub(UX, True)
    hub(LX, False)

    # ── Upper-hub callouts (left column) ─────────────────────────────────────
    LxT = UX - HALF - 60
    up_labels = [
        (55 * SC,  (-100 * SC, 40 * SC),  "PANEL TOP RAIL\n6×M10 (isolated mount)"),
        (12 * SC,  (-(ro + 20 * SC), 0),  "ALUMINUM TOP RING\n(seats bearing OD, H7)"),
        (-110 * SC,(-70 * SC, -107 * SC), "STEEL FLANGE\n4×M10 to Al cap"),
        (-134 * SC,(-90 * SC, -122 * SC), f"TOP CAP {LT_CAP_TOP_T:.0f}mm 6061-T6 Al"),
    ]
    for zt, (tx, tz), txt in up_labels:
        leader(ax, UX + tx, tz, LxT, zt, txt, fs=6.5, color=C_OUT, ha="right",
               arrow_style="->", font=FONT)
    # ── Upper-hub dimension lines — every part, horizontal (Ø/width) below ────
    draw_dim_h(ax, UX - rs, UX + rs, -310, f"Ø{SKF6215_ID} SHAFT (h6)",
               offset=46, fs=6.2, above=False, font=FONT)
    draw_dim_h(ax, UX - ro, UX + ro, -372, f"Ø{SKF6215_OD} BEARING OD",
               offset=46, fs=6.2, above=False, font=FONT)
    draw_dim_h(ax, UX - 80 * SC, UX + 80 * SC, -434, "Ø160 STEEL FLANGE",
               offset=46, fs=6.2, above=False, font=FONT)
    draw_dim_h(ax, UX - 100 * SC, UX + 100 * SC, -500, "Ø200 Al TOP RING OD",
               offset=46, fs=6.2, above=False, font=FONT)
    draw_dim_h(ax, UX - 140 * SC, UX + 140 * SC, -570, "280mm PANEL RAIL W",
               offset=46, fs=6.2, above=False, font=FONT)
    # Vertical (height / thickness), stacked in the centre gap:
    draw_dim_v(ax, UX + 255, -bw, bw, f"{SKF6215_W}mm BRG W", offset=44, fs=6.0,
               right=True, font=FONT)
    draw_dim_v(ax, UX + 350, -15 * SC, 15 * SC, "30mm RING H", offset=44, fs=6.0,
               right=True, font=FONT)
    draw_dim_v(ax, UX + 445, 15 * SC, 63 * SC, "48mm RAIL H", offset=44, fs=6.0,
               right=True, font=FONT)
    draw_dim_v(ax, UX + 540, -115 * SC, -100 * SC, "15mm FLANGE T", offset=44,
               fs=6.0, right=True, font=FONT)
    draw_dim_v(ax, UX + 635, -115 * SC - CAPd, -115 * SC, f"{LT_CAP_TOP_T:.0f}mm Al CAP T",
               offset=44, fs=6.0, right=True, font=FONT)
    draw_dim_v(ax, UX - 245, -100 * SC, 40 * SC, "140mm SHAFT L", offset=44,
               fs=6.0, font=FONT)
    leader(ax, UX - 100 * SC, -115 * SC - CAPd / 2, UX - HALF - 60, -150 * SC,
           f"Al CAP Ø{LT_CAP_OD}\n(width — see Sheet 3)", fs=6.2, color=C_DIM,
           ha="right", arrow_style="->", font=FONT)
    leader(ax, UX + rs, 18 * SC, UX + 150, 102 * SC,
           "CIRCLIP each side\n(DIN 471)", fs=6.2, color=C_OUT, ha="left",
           arrow_style="->", font=FONT)

    # ── Lower-hub callouts (right column) ────────────────────────────────────
    RxL = LX + HALF + 60
    lo_labels = [
        (58 * SC,  (0, 115 * SC),         f"BOTTOM CAP {LT_CAP_BOT_T:.0f}mm A36 steel\nstub shaft WELDED (no flange)"),
        (-48 * SC, (100 * SC, -40 * SC),  "PANEL BOTTOM RAIL /\nFLOOR PLATE — 8×M10"),
        (12 * SC,  (ro + 20 * SC, 0),     "WELDED STEEL\nFLOOR COLLAR"),
        (-16 * SC, (ro - 6 * SC, -16 * SC), "COLLAR → PLATE WELD"),
    ]
    for zt, (tx, tz), txt in lo_labels:
        leader(ax, LX + tx, tz, RxL, zt, txt, fs=6.5, color=C_OUT, ha="left",
               arrow_style="->", font=FONT)
    # Lower-hub dimension lines — collar + floor plate (h + v) ────────────────
    draw_dim_h(ax, LX - 105 * SC, LX + 105 * SC, -310, "Ø210 COLLAR OD",
               offset=46, fs=6.2, above=False, font=FONT)
    draw_dim_h(ax, LX - 140 * SC, LX + 140 * SC, -372, "280mm FLOOR PLATE W",
               offset=46, fs=6.2, above=False, font=FONT)
    draw_dim_v(ax, LX - HALF - 40, -15 * SC, 15 * SC, "30mm COLLAR H", offset=44,
               fs=6.0, font=FONT)
    draw_dim_v(ax, LX - HALF - 120, -63 * SC, -15 * SC, "48mm PLATE H", offset=44,
               fs=6.0, font=FONT)
    ax.text(LX, -235, "bearing · shaft · bearing-mount  AS UPPER HUB", ha="center",
            va="top", fontsize=6.2, color=C_DIM, **FONT, zorder=15)

    # ── Fabrication / spec notes ─────────────────────────────────────────────
    notes = [
        "BEARING HUB — SPECIFICATION",
        f"Bearing ×2: SKF 6215-2RS1 — Ø{SKF6215_ID}×Ø{SKF6215_OD}×{SKF6215_W}mm, sealed 2RS, C3, 0–120°C, 52.7 kN dyn.",
        f"TOP: drum → {LT_CAP_TOP_T:.0f}mm 6061-T6 Al cap → 4×M10 steel flange → Ø75 stub shaft → bearing.",
        f"BOTTOM: drum → {LT_CAP_BOT_T:.0f}mm A36 steel cap → stub shaft WELDED to cap → Ø75 → bearing.",
        "Bearing mounts: upper in isolated aluminum top ring (6×M10); lower in welded steel floor collar (8×M10).",
        "Axial retention: circlip on the stub shaft each side of each bearing (DIN 471).",
        "Ring / rail / flange / collar / plate sizes PROVISIONAL — confirm vs panel-frame design.",
        "ENLARGED ~2:1 · CAP THICKNESS EXAGGERATED · ALL DIMS IN mm",
    ]
    draw_notes(ax, notes, X_LO + 60, -740, 92, fs=7, font=FONT,
               width=2350, title_color=TITLE_COL)

    title_block(ax, "SHEET 4 OF 7", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="BEARING HUB & STUB-SHAFT DETAIL",
                scale_note="ENLARGED ~2:1 · ALL DIMS IN mm",
                doc_id="TBS-001 · Revolving Light-Trap", height=0.045, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet4.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet4.png saved")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 5 — Shell → cap lap-and-fasten joint
# The HDPE shell edge laps over a rolled rim-angle lip on each metal cap and is
# radially riveted (SS blind) + DP8010-bonded. Enlarged section + rivet pattern.
# ═════════════════════════════════════════════════════════════════════════════
def draw_sheet5():
    # ── Data window ──────────────────────────────────────────────────────────
    X_LO, X_HI, Z_LO, Z_HI = -470, 1090, -650, 540
    FIG_W = 18.0
    FIG_H = FIG_W * (Z_HI - Z_LO) / (X_HI - X_LO)
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DIAGRAM_DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Z_LO, Z_HI)
    ax.set_aspect("equal")
    ax.axis("off")

    # ── SECTION A-A — radial section through the rim (enlarged, NTS) ──────────
    CAPT = 60          # cap disc draw thickness (rep 6–8mm)
    LEGT = 20          # rim-angle leg draw thickness (rep 3mm)
    LIP  = 180         # standing-leg draw height (rep 25mm lap)
    ax.text(-160, Z_HI - 40, "SECTION A–A  (rim, enlarged — NOT TO SCALE)",
            ha="center", va="top", fontsize=8.5, color=TITLE_COL, fontweight="bold",
            **FONT, zorder=15)
    # metal cap disc
    draw_rect(ax, -340, -CAPT, 340, CAPT, fc=C_ALUM, lw=1.6, zorder=4)
    # rim angle (flat leg on cap + standing lip), rolled 25×25×3
    draw_rect(ax, -180, 0, 180, LEGT, fc=C_ALUM, lw=1.4, zorder=5)      # flat leg
    draw_rect(ax, -20, 0, 20, LIP, fc=C_ALUM, lw=1.4, zorder=5)         # standing lip
    # DP8010 bead in the lap
    draw_rect(ax, 0, -10, 10, LIP + 10, fc=C_GASKT, lw=0.8, zorder=5)
    # HDPE shell lapping over the lip
    draw_rect(ax, 10, -40, 20, LIP + 100, fc=C_LT_DRUM, lw=1.6, zorder=6)
    # break line at shell top
    for zz in (LIP + 70, LIP + 82, LIP + 94):
        ax.plot([8, 32], [zz - 4, zz + 4], color=C_OUT, lw=0.6, zorder=7)
    # radial SS blind rivet through shell + DP + lip
    rz = LIP * 0.5
    draw_rect(ax, -20, rz - 5, 50, 10, fc=C_STEEL, lw=1.0, zorder=8)    # shank
    draw_rect(ax, -34, rz - 12, 14, 24, fc=C_STEEL, lw=1.0, zorder=8)   # head (inside)
    ax.add_patch(mpatches.Polygon([(30, rz - 5), (42, rz), (30, rz + 5)],
                                  closed=True, fc=C_STEEL, ec=C_OUT, lw=0.8, zorder=8))
    # flat-leg → cap fasteners (Al: rivet / steel: weld)
    for xr in (-140, -75):
        draw_rect(ax, xr - 4, -CAPT, 8, LEGT + CAPT, fc=C_STEEL, lw=0.8, zorder=7)

    # ── Section dimensions + callouts ────────────────────────────────────────
    draw_dim_v(ax, 60, 0, LIP, f"{LT_LAP_H}mm LAP", offset=42, fs=6.5, right=True, font=FONT)
    draw_dim_h(ax, 10, 30, -60, f"{LT_DRUM_T:.2f}mm SHELL", offset=40, fs=6.2,
               above=False, font=FONT)
    draw_dim_v(ax, -360, -CAPT, 0, f"{LT_CAP_BOT_T:.0f}–{LT_CAP_TOP_T:.0f}mm CAP",
               offset=44, fs=6.2, font=FONT)
    leader(ax, 5, rz, 250, rz + 70,
           f"SS Ø{LT_RIVET_D} CLOSED-END BLIND RIVET (radial)\nthrough shell + lip · ~{LT_RIVET_PITCH}mm pitch",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, -10, LIP - 20, -300, LIP + 60,
           "RIM ANGLE 25×25×3, rolled to R427\nTOP: 6061-T6 Al (riveted to cap)\nBOTTOM: A36 steel (welded to cap)",
           fs=6.5, color=C_OUT, ha="right", arrow_style="->", font=FONT)
    leader(ax, 20, LIP + 40, 250, LIP + 30,
           f"HDPE SHELL {LT_DRUM_T:.2f}mm\nlaps {LT_LAP_H}mm over the lip",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, 5, 40, 250, -30,
           "3M DP8010 bead\n(bond + light seal)", fs=6.5, color="#5A3020",
           ha="left", arrow_style="->", font=FONT)
    leader(ax, -75, -CAPT + 20, -300, -CAPT - 55,
           "FLAT LEG → CAP\nAl: rivet · steel: weld", fs=6.2, color=C_DIM,
           ha="right", arrow_style="->", font=FONT)

    # ── Rivet pattern — cap plan + pitch detail ──────────────────────────────
    pcx, pcz, pr = 760, 300, 190
    draw_circle(ax, pcx, pcz, pr, lw=1.6, color=C_OUT, zorder=5)
    for i in range(LT_RIVET_N):
        aa = 2 * math.pi * i / LT_RIVET_N
        draw_circle(ax, pcx + pr * math.cos(aa), pcz + pr * math.sin(aa), 5,
                    lw=0.8, color="#CC4422", fill=True, fc="#CC4422", zorder=6)
    ax.text(pcx, pcz, f"Ø{LT_CAP_OD}\ncap rim", ha="center", va="center",
            fontsize=7, color=C_DIM, **FONT, zorder=7)
    ax.text(pcx, pcz - pr - 45,
            f"RIVET PATTERN — {LT_RIVET_N}× Ø{LT_RIVET_D} per cap @ ~{LT_RIVET_PITCH}mm pitch\n"
            f"(BOTH caps · {2 * LT_RIVET_N} rivets total)", ha="center", va="top",
            fontsize=6.8, color=C_OUT, **FONT, zorder=7)
    # pitch detail strip
    sx0, sz = 470, -40
    ax.plot([sx0, sx0 + 300], [sz, sz], color=C_OUT, lw=1.4, zorder=5)
    for i in range(6):
        draw_circle(ax, sx0 + 30 + i * 48, sz, 6, lw=0.8, color="#CC4422",
                    fill=True, fc="#CC4422", zorder=6)
    draw_dim_h(ax, sx0 + 30, sx0 + 78, sz + 55, f"{LT_RIVET_PITCH}mm", offset=34,
               fs=6.2, font=FONT)
    ax.text(sx0 + 150, sz - 40, "developed rim — rivet pitch", ha="center",
            va="top", fontsize=6.2, color=C_DIM, **FONT, zorder=7)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes = [
        "SHELL → CAP LAP-AND-FASTEN JOINT  (both caps)",
        "1. Rim: 25×25×3 angle ring rolled to R427 — TOP 6061-T6 Al (riveted to Al cap); BOTTOM A36 steel (welded to steel cap).",
        f"2. Shell sleeves {LT_LAP_H}mm over the standing lip.",
        "3. Apply 3M DP8010 bead to the lap (structural LSE bond + light seal); clamp.",
        f"4. Drill Ø5, set {LT_RIVET_N}× Ø{LT_RIVET_D} SS closed-end blind rivets per cap (~{LT_RIVET_PITCH}mm pitch), wet in DP8010.",
        "5. Closed-end rivets + DP8010 keep the joint light-tight; supersedes the extrusion weld.",
        "ENLARGED — NOT TO SCALE · ALL DIMS IN mm",
    ]
    draw_notes(ax, notes, X_LO + 60, -150, 52, fs=7, font=FONT, width=1980,
               title_color=TITLE_COL)

    title_block(ax, "SHEET 5 OF 7", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="SHELL → CAP LAP-AND-FASTEN JOINT (RIVETS + DP8010)",
                scale_note="ENLARGED · NTS · ALL DIMS IN mm",
                doc_id="TBS-001 · Revolving Light-Trap", height=0.045, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet5.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet5.png saved")


def main():
    print("Generating TBS-001 Revolving Light-Trap blueprint sheets...")
    draw_sheet1()
    draw_sheet2()
    draw_sheet3()
    draw_sheet4()
    draw_sheet5()
    print("Done.")


if __name__ == "__main__":
    main()
