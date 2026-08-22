#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_lighttrap_diagram.py
TBS-001  Revolving Light-Trap — fabrication blueprint set (10 sheets).

Sheet 1: General Arrangement — vertical section on the drum axis
Sheet 2: Housing cylinder — cut sheet (flat pattern)
Sheet 3: Rotating drum — cut (shell flat pattern + full end-cap blueprint)
Sheet 4: Rotating drum — secure (shell → cap lap-and-fasten joint)
Sheet 5: Bearing hub & stub-shaft detail (assembly)
Sheet 6: Machined components — bearing seats & stub-shaft (single-part blueprints)
Sheet 7: Seals & light-path verification
Sheet 8: Support frame — general arrangement (integrated steel cage)
Sheet 9: Housing → frame attachment (outer-skin fixing)
Sheet 10: Combined top-end assembly (inner + outer lap joints, half-section)

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
    DRUM_CX, DRUM_CY, DRUM_D, DRUM_H_LT, PANEL_FLOOR_GAP,
    LT_HOUSING_R, LT_HOUSING_T, LT_DRUM_OR, LT_DRUM_T, LT_OPENING_DEG,
    LT_CAP_TOP_T, LT_CAP_BOT_T, LT_CAP_OD, LT_LAP_H, LT_RIVET_D, LT_RIVET_HOLE, LT_RIVET_PITCH,
    LT_RIVET_N, LT_RIM_LEG, LT_RIM_T, LT_RIM_RIVET_PITCH, LT_SHELL_ARC,
    DRUM_CAGE_X0, DRUM_CAGE_X1, DRUM_CAGE_YD_L, DRUM_CAGE_YD_R,
    LT_FRAME_RHS, LT_FRAME_T, LT_FRAME_PLATE_T, LT_TOPRING_OD, LT_COLLAR_OD,
    LT_FRAME_MOUNT_BOLT_TOP, LT_FRAME_MOUNT_BOLT_BOT,
    LT_AXLE_BEAM_H, LT_AXLE_BEAM_W, LT_AXLE_BEAM_T, LT_AXLE_BEAM_SPAN,
    LT_HOUSING_ARC, LT_HOUSING_RIVET_N,
    DIAGRAM_DPI, DIAGRAMS_DIR,
)
from tbs_drawing import (
    draw_dim_h, draw_dim_v, draw_rect, draw_circle, draw_cl_v, draw_cl_h,
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


def blind_rivet(ax, cx, cz, ang, grip, d=12):
    """Installed SS closed-end blind rivet in section — dome factory head at +axis,
    upset (set) blind head at −axis; `ang` = axis direction (deg), `grip` = joint stack."""
    RSC = "#C9CCD2"
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))

    def T(u, v):
        return (cx + u * ca - v * sa, cz + u * sa + v * ca)
    g = grip / 2
    ax.add_patch(mpatches.Polygon([T(-g, -d / 2), T(g, -d / 2), T(g, d / 2), T(-g, d / 2)],
                                  closed=True, fc=RSC, ec=C_OUT, lw=1.0, zorder=8))
    fb, hr = g + d * 0.35, d * 0.9
    dome = [T(g, d * 0.95)]
    for kk in range(13):
        a = math.pi * (0.5 - kk / 12.0)
        dome.append(T(fb + hr * math.cos(a), d * 0.95 * math.sin(a)))
    dome.append(T(g, -d * 0.95))
    ax.add_patch(mpatches.Polygon(dome, closed=True, fc=RSC, ec=C_OUT, lw=1.2, zorder=9))
    ax.plot(*zip(T(fb + hr * 0.5, 0), T(fb + hr, 0)), color=C_OUT, lw=0.7, zorder=10)
    bb, br = -g - d * 0.25, d * 0.7
    blind = [T(-g, d * 0.7)]
    for kk in range(13):
        a = math.pi * (0.5 - kk / 12.0)
        blind.append(T(bb - br * math.cos(a), d * 1.25 * math.sin(a)))
    blind.append(T(-g, -d * 0.7))
    ax.add_patch(mpatches.Polygon(blind, closed=True, fc=RSC, ec=C_OUT, lw=1.2, zorder=9))


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
              fc=C_ALUM, lw=1.2, zorder=7)

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
           f"LOWER: {LT_CAP_BOT_T:.0f}mm 6061-T6 Al cap + BOLTED stub shaft →\n"
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
    leader(ax, HI_R - 2, 1300,
           HO_R + 250, 1880,
           f"≈{RUN_GAP}mm radial running gap\n(drum OD → housing bore; sealed — Sheet 7)",
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
        f"3 END CAPS      2   {LT_CAP_TOP_T:.0f}mm 6061-T6 Al, Ø{LT_CAP_OD}",
        f"4 RIM ANGLE     2   {LT_RIM_LEG}×{LT_RIM_LEG}×{LT_RIM_T} rolled R{LT_CAP_OD // 2} (6061-T6 Al)",
        f"5 BEARING       2   SKF 6215-2RS1 (Ø{SKF6215_ID} bore)",
        f"6 SHELL RIVETS  {2 * LT_RIVET_N}  Ø{LT_RIVET_D} SS blind (~{LT_RIVET_PITCH}mm pitch)",
        "7 JOINT BOND    -   3M DP8010 (shell→cap lap seal)",
        "8 SEALS         -   12/20mm neoprene + silicone",
        f"9 GRAB RAIL     1   Ø{GRAB_D}×{GRAB_L} SS round",
    ]
    draw_notes(ax, bom, HO_R + 720, 1610, 112, fs=6.8, font=FONT,
               width=1000, title_color=TITLE_COL)

    title_block(ax, "SHEET 1 OF 10", drawing_title="REVOLVING LIGHT-TRAP",
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

    title_block(ax, "SHEET 2 OF 10", drawing_title="REVOLVING LIGHT-TRAP",
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
    # Bottom cap — 6061-T6 Al, bolted stub-shaft flange (identical to top)
    draw_circle(ax, cap_cx, cz_bot, cap_r, lw=2.0, color=C_OUT, fill=True,
                fc=C_ALUM, zorder=4)
    draw_circle(ax, cap_cx, cz_bot, 78, lw=1.2, color=C_OUT, zorder=6)       # hub boss
    draw_circle(ax, cap_cx, cz_bot, SKF6215_ID / 2, lw=1.4, color="#CC4422", zorder=7)
    bolt_holes(ax, cap_cx, cz_bot, 55, 4, 6, color=C_OUT, zorder=7)          # 4× M10 flange
    ax.text(cap_cx, cz_bot - cap_r - 55, f"BOTTOM CAP\n{LT_CAP_BOT_T:.0f}mm 6061-T6 Al",
            ha="center", va="top", fontsize=8, color=C_OUT, fontweight="bold",
            **FONT, zorder=15)
    draw_dim_h(ax, cap_cx - cap_r, cap_cx + cap_r, cz_top + cap_r + 90,
               f"Ø{LT_CAP_OD}", offset=70, fs=7.5, font=FONT)
    leader(ax, cap_cx + 60, cz_top, cap_cx + cap_r + 70, cz_top + cap_r * 0.7,
           f"Both caps: stub-shaft hub BOLTED 4×M10 (6061-T6 Al)\n"
           f"Ø{SKF6215_ID} → SKF 6215 (Sheet 5)",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)

    # ── Fabrication notes ────────────────────────────────────────────────────
    notes = [
        "ROTATING DRUM — FABRICATION",
        f"Shell: {LT_DRUM_T:.2f}mm (1/8in) HDPE, blank {W_SHELL:.0f} × {SHELL_H}mm.",
        f"Caps (Ø{LT_CAP_OD}): both {LT_CAP_TOP_T:.0f}mm 6061-T6 Al (identical).",
        f"1. Roll shell to R{LT_DRUM_OR}; the two free edges are the opening jambs.",
        f"2. Shell laps {LT_LAP_H}mm over each cap rim → {LT_RIVET_N}× Ø{LT_RIVET_D} SS blind rivets/cap + DP8010 bead (see Sheet 4).",
        "3. Both stub-shaft hubs bolted 4×M10 to the Al caps; Ø75 → SKF 6215.",
        f"Running clearance to housing bore ≈ {RUN_GAP_L}mm (radial) — see Sheet 7.",
        "FLAT PATTERN · TRUE DEVELOPED SCALE · ALL DIMS IN mm",
    ]
    draw_notes(ax, notes, 40, -560, 92, fs=7, font=FONT, width=1850,
               title_color=TITLE_COL)

    title_block(ax, "SHEET 3 OF 10", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="ROTATING DRUM — CUT (FLAT PATTERN + CAPS)",
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
def draw_sheet_hub():                              # Sheet 5 — bearing hub
    SC = 2.2                                       # enlargement factor
    rs, ro, bw = SKF6215_ID / 2 * SC, SKF6215_OD / 2 * SC, SKF6215_W / 2 * SC
    CAPd = LT_CAP_TOP_T * SC                        # top-cap draw thickness (to scale; layout ref)
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
        # both caps: 6061-T6 Al, bolted steel stub-shaft flange (4×M10)
        capd = LT_CAP_TOP_T * SC
        zc0, zc1 = -55 * SC * s, -55 * SC * s - capd * s
        # stub shaft Ø75 — short stub: flange face → past the bearing (only what the
        # bearing seat + circlips + flange need; no reason for a long shaft)
        z_stub = 30 * SC * s
        z_fl = -40 * SC * s
        draw_rect(ax, cx - rs, min(z_stub, z_fl), 2 * rs, abs(z_stub - z_fl),
                  fc=C_STEEL, lw=1.4, zorder=6)
        # bearing mount: isolated Al top ring (upper) / welded steel floor collar (lower)
        HRr = (100 if up else 105) * SC
        band(cx, ro, HRr, -15 * SC, 15 * SC,
             fc=(C_ALUM if up else C_STEEL), lw=1.4, zorder=5)
        # panel rail / floor plate
        zr0, zr1 = 15 * SC * s, 63 * SC * s
        draw_rect(ax, cx - 140 * SC, min(zr0, zr1), 280 * SC, abs(zr1 - zr0),
                  fc=C_STEEL, lw=1.4, zorder=4)
        # Al drum cap + bolted steel stub-shaft flange
        draw_rect(ax, cx - 110 * SC, min(zc0, zc1), 220 * SC, abs(zc1 - zc0),
                  fc=C_ALUM, lw=1.4, zorder=6)
        zf0, zf1 = -40 * SC * s, -55 * SC * s
        draw_rect(ax, cx - 80 * SC, min(zf0, zf1), 160 * SC, abs(zf1 - zf0),
                  fc=C_STEEL, lw=1.4, zorder=6)
        for g in (-1, 1):
            ax.plot([cx + g * 55 * SC] * 2, [-40 * SC * s, zc1],
                    color=C_OUT, lw=1.8, zorder=9)       # flange bolts
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
        (-52 * SC, (-70 * SC, -47 * SC),  "STEEL FLANGE\n4×M10 to Al cap"),
        (-90 * SC, (-90 * SC, -62 * SC),  f"TOP CAP {LT_CAP_TOP_T:.0f}mm 6061-T6 Al, Ø{LT_CAP_OD}\n(width — see Sheet 3)"),
    ]
    for zt, (tx, tz), txt in up_labels:
        leader(ax, UX + tx, tz, LxT, zt, txt, fs=6.5, color=C_OUT, ha="right",
               arrow_style="->", font=FONT)
    # ── Upper-hub dimension lines — every part, horizontal (Ø/width) below ────
    draw_dim_h(ax, UX - rs, UX + rs, -195, f"Ø{SKF6215_ID} SHAFT (h6)",
               offset=46, fs=6.2, above=False, font=FONT)
    draw_dim_h(ax, UX - ro, UX + ro, -257, f"Ø{SKF6215_OD} BEARING OD",
               offset=46, fs=6.2, above=False, font=FONT)
    draw_dim_h(ax, UX - 80 * SC, UX + 80 * SC, -319, "Ø160 STEEL FLANGE",
               offset=46, fs=6.2, above=False, font=FONT)
    draw_dim_h(ax, UX - 100 * SC, UX + 100 * SC, -385, "Ø200 Al TOP RING OD",
               offset=46, fs=6.2, above=False, font=FONT)
    draw_dim_h(ax, UX - 140 * SC, UX + 140 * SC, -455, "280mm PANEL RAIL W",
               offset=46, fs=6.2, above=False, font=FONT)
    # Vertical (height / thickness), stacked in the centre gap:
    draw_dim_v(ax, UX + 255, -bw, bw, f"{SKF6215_W}mm BRG W", offset=44, fs=6.0,
               right=True, font=FONT)
    draw_dim_v(ax, UX + 330, -15 * SC, 15 * SC, "30mm RING H", offset=44, fs=6.0,
               right=True, font=FONT)
    draw_dim_v(ax, UX + 405, 15 * SC, 63 * SC, "48mm RAIL H", offset=44, fs=6.0,
               right=True, font=FONT)
    draw_dim_v(ax, UX + 480, -55 * SC, -40 * SC, "15mm FLANGE T", offset=44,
               fs=6.0, right=True, font=FONT)
    draw_dim_v(ax, UX + 555, -55 * SC - CAPd, -55 * SC, f"{LT_CAP_TOP_T:.0f}mm Al CAP T",
               offset=44, fs=6.0, right=True, font=FONT)
    draw_dim_v(ax, UX - 255, -40 * SC, 30 * SC, "70mm SHAFT L", offset=44,
               fs=6.0, font=FONT)
    leader(ax, UX + rs, 18 * SC, UX + 150, 102 * SC,
           "CIRCLIP each side\n(DIN 471)", fs=6.2, color=C_OUT, ha="left",
           arrow_style="->", font=FONT)

    # ── Lower-hub callouts (right column) ────────────────────────────────────
    RxL = LX + HALF + 60
    lo_labels = [
        (58 * SC,  (0, 115 * SC),         f"BOTTOM CAP {LT_CAP_BOT_T:.0f}mm 6061-T6 Al\nstub shaft BOLTED 4×M10"),
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
    ax.text(LX, -235, "bearing · shaft · cap · flange  AS UPPER HUB", ha="center",
            va="top", fontsize=6.2, color=C_DIM, **FONT, zorder=15)

    # ── Component blueprints are on Sheet 6 (single-part drawings) ───────────
    ax.text((UX + LX) / 2, -640,
            "MACHINED COMPONENTS (Al top ring · steel floor collar · stub-shaft + flange) —\n"
            "fully dimensioned single-part blueprints incl. bolt patterns on SHEET 6.\n"
            "End cap (Ø855 6061-T6 Al, 4×M10 hub flange) — SHEET 3.",
            ha="center", va="center", fontsize=8, color=TITLE_COL, fontweight="bold",
            **FONT, zorder=9)

    # ── Fabrication / spec notes ─────────────────────────────────────────────
    notes = [
        "BEARING HUB — SPECIFICATION",
        f"Bearing ×2: SKF 6215-2RS1 — Ø{SKF6215_ID}×Ø{SKF6215_OD}×{SKF6215_W}mm, sealed 2RS, C3, 0–120°C, 52.7 kN dyn.",
        f"Caps ×2 (identical): {LT_CAP_TOP_T:.0f}mm 6061-T6 Al — drum → cap → 4×M10 steel flange → Ø75 stub shaft → bearing.",
        "Bearing mounts: upper in isolated aluminum top ring (6×M10); lower in welded steel floor collar (8×M10).",
        "Axial retention: circlip on the stub shaft each side of each bearing (DIN 471).",
        "This sheet is the hub ASSEMBLY (how the parts stack). Single-part blueprints + bolt patterns: bearing seats + stub-shaft on SHEET 6; end cap on SHEET 3; frame members on SHEET 8.",
        "SECTIONS 2.2:1 (isotropic) · ALL DIMS IN mm",
    ]
    draw_notes(ax, notes, X_LO + 60, -830, 92, fs=7, font=FONT,
               width=2350, title_color=TITLE_COL)

    # ── Section scale bar (50 mm, to the 2.2:1 section geometry) ─────────────
    sbx, sbz = UX - HALF - 40, -560
    ax.plot([sbx, sbx + 50 * SC], [sbz, sbz], color=C_OUT, lw=1.4, zorder=8)
    for xt in (sbx, sbx + 25 * SC, sbx + 50 * SC):
        ax.plot([xt, xt], [sbz - 10, sbz + 10], color=C_OUT, lw=1.0, zorder=8)
    ax.text(sbx + 25 * SC, sbz - 22, "50 mm  (SECTIONS 2.2:1)", ha="center", va="top",
            fontsize=6.5, color=C_OUT, **FONT, zorder=8)

    title_block(ax, "SHEET 5 OF 10", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="BEARING HUB & STUB-SHAFT — ASSEMBLY",
                scale_note="SECTIONS 2.2:1 · ALL DIMS IN mm",
                doc_id="TBS-001 · Revolving Light-Trap", height=0.045, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet5.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet5.png saved")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 5 — Shell → cap lap-and-fasten joint
# The HDPE shell edge laps over a rolled rim-angle lip on each metal cap and is
# radially riveted (SS blind) + DP8010-bonded. Enlarged section + rivet pattern.
# ═════════════════════════════════════════════════════════════════════════════
def draw_sheet_secure():                           # Sheet 4 — drum secure (shell→cap joint)
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

    # ── SECTION A-A — radial section through the rim (SCALE 7:1, isotropic) ───
    S = 7                                    # drawn = real mm × 7 (both axes)
    CAPT = S * LT_CAP_TOP_T                   # cap thickness (8mm)
    LEGT = S * LT_RIM_T                        # rim-angle leg thickness (3mm)
    LIP  = S * LT_LAP_H                        # lap / standing-lip height (25mm)
    SHT  = S * LT_DRUM_T                       # shell thickness (3.18mm)
    DPT  = S * 1.0                             # DP8010 bead (~1mm)
    RIML = S * LT_RIM_LEG                      # rim flat-leg length (25mm)
    RVD  = S * LT_RIVET_D                      # rivet Ø (3.18mm, 1/8")
    ax.text(-150, Z_HI - 40, "SECTION A–A  (shell → cap rim · SCALE 7:1)",
            ha="center", va="top", fontsize=8.5, color=TITLE_COL, fontweight="bold",
            **FONT, zorder=15)
    draw_rect(ax, -340, -CAPT, 340, CAPT, fc=C_ALUM, lw=1.6, zorder=4)         # cap disc (Al)
    draw_rect(ax, -RIML, 0, RIML, LEGT, fc=C_ALUM, lw=1.4, zorder=5)           # rim flat leg on cap
    draw_rect(ax, -LEGT, 0, LEGT, LIP, fc=C_ALUM, lw=1.4, zorder=5)            # standing lip
    draw_rect(ax, 0, -DPT, DPT, LIP + DPT, fc=C_GASKT, lw=0.8, zorder=5)       # DP8010 bead
    draw_rect(ax, DPT, -40, SHT, LIP + 90, fc=C_LT_DRUM, lw=1.6, zorder=6)     # shell laps over lip
    for zz in (LIP + 55, LIP + 67, LIP + 79):                                 # break line (shell continues down)
        ax.plot([DPT - 3, DPT + SHT + 3], [zz - 4, zz + 4], color=C_OUT, lw=0.6, zorder=7)
    rz = LIP * 0.5
    blind_rivet(ax, (DPT + SHT - LEGT) / 2, rz, 0, S * (LT_DRUM_T + 1 + LT_RIM_T), d=RVD)  # shell → lip rivet (radial)
    blind_rivet(ax, -RIML / 2, (LEGT - CAPT) / 2, 90, CAPT + LEGT, d=RVD * 0.8)             # one leg → cap rivet (vertical)

    # ── Section dimensions + callouts (all to the 7:1 geometry) ──────────────
    draw_dim_v(ax, DPT + SHT + 40, 0, LIP, f"{LT_LAP_H}mm LAP", offset=42, fs=6.5, right=True, font=FONT)
    draw_dim_h(ax, DPT, DPT + SHT, -55, f"{LT_DRUM_T:.2f}mm SHELL", offset=40, fs=6.2,
               above=False, font=FONT)
    draw_dim_v(ax, -360, -CAPT, 0, f"{LT_CAP_TOP_T:.0f}mm CAP", offset=44, fs=6.2, font=FONT)
    leader(ax, (DPT + SHT - LEGT) / 2, rz, 250, rz + 70,
           f"SS Ø{LT_RIVET_D} DOMED-HEAD BLIND RIVET (radial)\nthrough shell + lip · ~{LT_RIVET_PITCH}mm circumferential pitch",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, -LEGT, LIP - 20, -300, LIP + 55,
           f"RIM ANGLE {LT_RIM_LEG}×{LT_RIM_LEG}×{LT_RIM_T}, rolled to R{LT_CAP_OD // 2}\n6061-T6 Al — riveted to both caps",
           fs=6.5, color=C_OUT, ha="right", arrow_style="->", font=FONT)
    leader(ax, DPT + SHT, LIP + 30, 250, LIP + 20,
           f"HDPE SHELL {LT_DRUM_T:.2f}mm\nlaps {LT_LAP_H}mm over the lip",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, DPT / 2, 40, 250, -30,
           "3M DP8010 bead\n(bond + light seal)", fs=6.5, color="#5A3020",
           ha="left", arrow_style="->", font=FONT)
    leader(ax, -RIML / 2, LEGT / 2, -300, -CAPT - 55,
           f"FLAT LEG → CAP rivet\n(SS blind, @ {LT_RIM_RIVET_PITCH}mm circumferential)", fs=6.2, color=C_DIM,
           ha="right", arrow_style="->", font=FONT)

    # ── Section scale bar (20 mm, to the 7:1 geometry) ───────────────────────
    sbx, sbz = 60, -CAPT - 60
    ax.plot([sbx, sbx + S * 20], [sbz, sbz], color=C_OUT, lw=1.4, zorder=8)
    for xt in (sbx, sbx + S * 10, sbx + S * 20):
        ax.plot([xt, xt], [sbz - 6, sbz + 6], color=C_OUT, lw=1.0, zorder=8)
    ax.text(sbx + S * 10, sbz - 13, "20 mm  (SECTION 7:1)", ha="center", va="top",
            fontsize=6, color=C_OUT, **FONT, zorder=8)

    # ── Rivet pattern — cap plan (280° C-shell arc; the 80° opening has no rim) ─
    pcx, pcz, pr = 790, 300, LT_CAP_OD / 4                                  # cap outline at 1:2
    draw_circle(ax, pcx, pcz, pr, lw=1.0, color=C_DIM, ls="--", zorder=5)   # cap disc (full Ø855)
    oh = LT_OPENING_DEG / 2
    aarc = [math.radians(oh + t) for t in range(0, LT_SHELL_ARC + 1, 4)]    # 280° rim-angle arc
    ax.plot([pcx + pr * math.cos(a) for a in aarc], [pcz + pr * math.sin(a) for a in aarc],
            color=C_OUT, lw=2.6, zorder=6)
    for i in range(LT_RIVET_N):                                            # rivets over the 280° arc
        a = math.radians(oh + (i + 0.5) / LT_RIVET_N * LT_SHELL_ARC)
        draw_circle(ax, pcx + pr * math.cos(a), pcz + pr * math.sin(a), 5,
                    lw=0.8, color="#CC4422", fill=True, fc="#CC4422", zorder=7)
    for t in (-oh, oh):                                                    # opening jambs
        a = math.radians(t)
        ax.plot([pcx, pcx + pr * math.cos(a)], [pcz, pcz + pr * math.sin(a)],
                color="#B08020", lw=1.4, zorder=6)
    ax.text(pcx + pr + 18, pcz, f"{LT_OPENING_DEG}° OPENING\n(no rim / shell)", ha="left",
            va="center", fontsize=6.2, color="#B08020", **FONT, zorder=7)
    ax.text(pcx, pcz, f"Ø{LT_CAP_OD}\ncap rim ({LT_SHELL_ARC}° arc)\nCAP PLAN — 1:2", ha="center",
            va="center", fontsize=7, color=C_DIM, **FONT, zorder=7)
    ax.text(pcx, pcz - pr - 40,
            f"RIVET PATTERN — {LT_RIVET_N}× Ø{LT_RIVET_D} per cap @ ~{LT_RIVET_PITCH}mm pitch\n"
            f"(BOTH caps · {2 * LT_RIVET_N} rivets total · rivet symbols schematic)", ha="center", va="top",
            fontsize=6.8, color=C_OUT, **FONT, zorder=7)
    # pitch detail strip
    sx0, sz = 470, -40
    ax.plot([sx0, sx0 + 300], [sz, sz], color=C_OUT, lw=1.4, zorder=5)
    for i in range(6):
        draw_circle(ax, sx0 + 30 + i * 48, sz, 6, lw=0.8, color="#CC4422",
                    fill=True, fc="#CC4422", zorder=6)
    draw_dim_h(ax, sx0 + 30, sx0 + 78, sz + 55, f"{LT_RIVET_PITCH}mm", offset=34,
               fs=6.2, font=FONT)
    ax.text(sx0 + 150, sz - 40, "developed rim — rivet pitch (schematic)", ha="center",
            va="top", fontsize=6.2, color=C_DIM, **FONT, zorder=7)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes = [
        "SHELL → CAP LAP-AND-FASTEN JOINT  (both caps)",
        f"1. Rim: {LT_RIM_LEG}×{LT_RIM_LEG}×{LT_RIM_T} angle ring rolled to R{LT_CAP_OD // 2} — 6061-T6 Al, riveted to both Al caps.",
        f"2. Shell sleeves {LT_LAP_H}mm over the standing lip.",
        "3. Apply 3M DP8010 bead to the lap (structural LSE bond + light seal); clamp.",
        f"4. Drill Ø{LT_RIVET_HOLE:.1f} (#30), set {LT_RIVET_N}× Ø{LT_RIVET_D} SS domed-head blind rivets per cap (McMaster 97525A425, ~{LT_RIVET_PITCH}mm pitch), wet in DP8010.",
        "5. Closed-end rivets + DP8010 keep the joint light-tight; supersedes the extrusion weld.",
        "SECTION A–A 7:1 (isotropic) · CAP PLAN 1:2 · fastener symbols schematic · ALL DIMS IN mm",
    ]
    draw_notes(ax, notes, X_LO + 60, -150, 15, fs=7, font=FONT, width=1980,
               title_color=TITLE_COL)

    title_block(ax, "SHEET 4 OF 10", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="ROTATING DRUM — SECURE (SHELL → CAP LAP-AND-FASTEN JOINT)",
                scale_note="SECTION 7:1 · CAP PLAN 1:2 · ALL DIMS IN mm",
                doc_id="TBS-001 · Revolving Light-Trap", height=0.045, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet4.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet4.png saved")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 7 — Support frame, general arrangement
# The integrated steel welded box cage (part of the swing-panel frame) that carries
# both SKF 6215 bearings + the fixed housing. ELEVATION (left) + PLAN (top-right).
# ═════════════════════════════════════════════════════════════════════════════
def draw_sheet7():
    CX, CY, HR = DRUM_CX, DRUM_CY, LT_HOUSING_R
    Z_BOT, Z_TOP = PANEL_FLOOR_GAP, DRUM_H_LT
    RHS = LT_FRAME_RHS
    cx0, cx1, cyl, cyr = DRUM_CAGE_X0, DRUM_CAGE_X1, DRUM_CAGE_YD_L, DRUM_CAGE_YD_R
    cW_x, cW_y, cH = cx1 - cx0, cyr - cyl, Z_TOP - Z_BOT
    PLd = LT_FRAME_PLATE_T * 3          # plate draw thickness (exaggerated)

    # View placements (generic fig units, mm-scaled)
    EX, EZ = 0, 0                        # ELEVATION origin (Yd→x, Z→z)
    PX, PZ = cW_y + 780, cH - cW_y       # PLAN origin (X→x, Yd→z), top-right

    def fe(yd, z):   # elevation map
        return (EX + (yd - cyl), EZ + (z - Z_BOT))

    def fp(x, yd):   # plan map
        return (PX + (x - cx0), PZ + (yd - cyl))

    X_LO, X_HI = -560, PX + cW_x + 360
    Z_LO, Z_HI = -900, cH + 300
    FIG_W = 20.0
    FIG_H = FIG_W * (Z_HI - Z_LO) / (X_HI - X_LO)
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DIAGRAM_DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Z_LO, Z_HI)
    ax.set_aspect("equal")
    ax.axis("off")

    def rrect(p0, w, h, **kw):
        draw_rect(ax, p0[0], p0[1], w, h, **kw)

    # ══ ELEVATION (looking along −X: Yd horizontal, Z vertical) ═══════════════
    ax.text(*fe(cyl + cW_y / 2, Z_TOP + 170), s="ELEVATION — LOOKING ALONG DRUM AXIS DEPTH",
            ha="center", va="bottom", fontsize=8.5, color=TITLE_COL, fontweight="bold",
            **FONT, zorder=15)
    # housing cylinder (outer skin) — walls at CY±HR
    for yd in (CY - HR, CY + HR - LT_HOUSING_T):
        rrect(fe(yd, Z_BOT), LT_HOUSING_T, cH, fc="#DDE4EC", lw=1.2, zorder=5)
    # drum shell inside
    for yd in (CY - LT_DRUM_OR, CY + LT_DRUM_OR - LT_DRUM_T):
        rrect(fe(yd, Z_BOT + 40), LT_DRUM_T, cH - 80, fc=C_LT_DRUM, lw=1.0, zorder=5)
    # top + bottom AXLE-SUPPORT BEAMS (100×50 RHS, span Yd, carry the central bearing)
    BH = LT_AXLE_BEAM_H
    rrect(fe(cyl, Z_TOP - BH), cW_y, BH, fc=C_STEEL, lw=1.4, zorder=6)
    rrect(fe(cyl, Z_BOT), cW_y, BH, fc=C_STEEL, lw=1.4, zorder=6)
    # 4 corner posts → in elevation the front/back pairs overlap: 2 vertical RHS
    for yd in (cyl, cyr - RHS):
        rrect(fe(yd, Z_BOT), RHS, cH, fc=C_STEEL, lw=1.4, zorder=4)
    # bearings on the axis, seated in the beams (drum HANGS from the top beam)
    for z_brg in (Z_TOP - BH - SKF6215_W, Z_BOT + BH):
        rrect(fe(CY - SKF6215_OD / 2, z_brg), SKF6215_OD, SKF6215_W, fc="#B0B0B8", lw=1.2, zorder=8)
        rrect(fe(CY - SKF6215_ID / 2, z_brg), SKF6215_ID, SKF6215_W, fc="white", lw=0.8, zorder=9)
    draw_cl_v(ax, fe(CY, 0)[0], fe(CY, Z_BOT)[1] - 80, fe(CY, Z_TOP)[1] + 80)
    # panel-rail tie context (ghost above/below the beams)
    for z0 in (Z_TOP + 6, Z_BOT - 55):
        rrect(fe(cyl - 90, z0), cW_y + 180, 50, fc="#EDEDED", lw=0.8, zorder=2)
    # elevation dims + labels
    draw_dim_v(ax, fe(cyl, 0)[0] - 90, fe(cyl, Z_BOT)[1], fe(cyl, Z_TOP)[1],
               f"{cH}mm POST H", offset=70, fs=7, font=FONT)
    draw_dim_h(ax, fe(cyl, 0)[0], fe(cyr, 0)[0], fe(0, Z_TOP)[1] + 90,
               f"{LT_AXLE_BEAM_SPAN}mm BEAM SPAN (Yd)", offset=60, fs=7, font=FONT)
    leader(ax, *fe(cyr - RHS / 2, Z_TOP * 0.62), *fe(cyr + 130, Z_TOP * 0.66),
           f"CORNER POST\n{RHS}×{RHS}×{LT_FRAME_T} RHS (×4)\nwelded into panel rails",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, *fe(cyl + 150, Z_TOP - BH / 2), *fe(cyl - 80, Z_TOP + 110),
           f"TOP AXLE BEAM {LT_AXLE_BEAM_H}×{LT_AXLE_BEAM_W}×{LT_AXLE_BEAM_T} RHS\n(carries upper bearing — drum hangs from it)",
           fs=6.5, color=C_OUT, ha="right", arrow_style="->", font=FONT)
    leader(ax, *fe(cyl + 150, Z_BOT + BH / 2), *fe(cyl - 80, Z_BOT - 130),
           f"BOTTOM AXLE BEAM {LT_AXLE_BEAM_H}×{LT_AXLE_BEAM_W} RHS\n+ floor anchor (locates lower bearing)",
           fs=6.5, color=C_OUT, ha="right", arrow_style="->", font=FONT)
    leader(ax, *fe(CY + SKF6215_OD / 2, Z_BOT + BH + SKF6215_W / 2),
           *fe(CY + 300, Z_BOT + 320), "SKF 6215 ×2\n(seated in the beams)", fs=6.5,
           color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, *fe(CY - HR + LT_HOUSING_T, Z_TOP * 0.4), *fe(cyl - 80, Z_TOP * 0.34),
           f"FIXED HOUSING Ø{DRUM_D}\n(outer skin — Sheet 9)", fs=6.5, color=C_OUT,
           ha="right", arrow_style="->", font=FONT)

    # ══ PLAN (top-down: X horizontal, Yd vertical) ════════════════════════════
    ax.text(*fp(cx0 + cW_x / 2, cyl - 150), s="PLAN — LOOKING DOWN",
            ha="center", va="top", fontsize=8.5, color=TITLE_COL, fontweight="bold",
            **FONT, zorder=15)
    hc = fp(CX, CY)
    # housing + drum circles (background)
    draw_circle(ax, hc[0], hc[1], LT_DRUM_OR, lw=1.0, color=C_LT_DRUM, fill=True,
                fc="#F1ECE0", zorder=3)
    draw_circle(ax, hc[0], hc[1], HR, lw=1.6, color=C_OUT, zorder=4)
    draw_circle(ax, hc[0], hc[1], HR - LT_HOUSING_T, lw=0.8, color=C_DIM, zorder=4)
    # perimeter box frame — 4 rails between the corner posts
    rrect(fp(cx0, cyl), cW_x, RHS, fc=C_STEEL, lw=1.2, zorder=5)
    rrect(fp(cx0, cyr - RHS), cW_x, RHS, fc=C_STEEL, lw=1.2, zorder=5)
    rrect(fp(cx0, cyl), RHS, cW_y, fc=C_STEEL, lw=1.2, zorder=5)
    rrect(fp(cx1 - RHS, cyl), RHS, cW_y, fc=C_STEEL, lw=1.2, zorder=5)
    # 4 corner posts
    for xx in (cx0, cx1 - RHS):
        for yy in (cyl, cyr - RHS):
            rrect(fp(xx, yy), RHS, RHS, fc="#9BA0A8", lw=1.2, zorder=6)
    # AXLE BEAM — spans Yd at the drum axis X, central bearing at midspan
    rrect(fp(CX - LT_AXLE_BEAM_W / 2, cyl), LT_AXLE_BEAM_W, cW_y, fc=C_STEEL, lw=1.4, zorder=7)
    draw_circle(ax, hc[0], hc[1], SKF6215_OD / 2, lw=1.2, color=C_OUT, fill=True,
                fc="#B0B0B8", zorder=8)
    draw_circle(ax, hc[0], hc[1], SKF6215_ID / 2, lw=1.0, color="#CC4422", zorder=9)
    # jamb frames at the aperture edges + opening labels
    oh = LT_OPENING_DEG / 2
    for oc, tag, col in ((180, "EXT", "#5060A0"), (0, "INT", "#407040")):
        for e in (oc - oh, oc + oh):
            a = math.radians(e)
            jx, jy = hc[0] + HR * math.cos(a), hc[1] + HR * math.sin(a)
            rrect((jx - RHS / 2, jy - RHS / 2), RHS, RHS, fc="#9BA0A8", lw=1.0, zorder=8)
        ax.text(hc[0] + (HR + 78) * math.cos(math.radians(oc)),
                hc[1] + (HR + 78) * math.sin(math.radians(oc)), f"{tag}\nOPENING",
                ha="center", va="center", fontsize=6.5, color=col, **FONT, zorder=9)
    # plan dims + labels
    draw_dim_h(ax, fp(cx0, cyl)[0], fp(cx1, cyl)[0], fp(0, cyl)[1] - 80,
               f"{cW_x}mm CAGE (X)", offset=55, fs=7, above=False, font=FONT)
    draw_dim_v(ax, fp(cx0, 0)[0] - 80, fp(cx0, cyl)[1], fp(cx0, cyr)[1],
               f"{cW_y}mm (Yd)", offset=55, fs=7, font=FONT)
    leader(ax, hc[0] + LT_AXLE_BEAM_W / 2, hc[1] + 120, fp(cx1, cyr)[0] + 70, fp(cx1, cyr)[1] - 20,
           f"AXLE BEAM {LT_AXLE_BEAM_H}×{LT_AXLE_BEAM_W} RHS\ncarries central SKF 6215 at midspan",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, *fp(cx0 + RHS / 2, cyr - RHS / 2), fp(cx0, cyr)[0] - 40, fp(cx0, cyr)[1] + 50,
           f"CORNER POST + PERIMETER RAILS\n{RHS}×{RHS}×{LT_FRAME_T} RHS welded box",
           fs=6.5, color=C_OUT, ha="right", arrow_style="->", font=FONT)
    leader(ax, hc[0] + HR * math.cos(math.radians(40)), hc[1] + HR * math.sin(math.radians(40)),
           fp(cx1, cyr)[0] + 70, fp(cx1, cyr)[1] + 55,
           f"JAMB FRAME {RHS}×{RHS} RHS (×2/opening)", fs=6.5, color=C_OUT,
           ha="left", arrow_style="->", font=FONT)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes = [
        "SUPPORT FRAME — INTEGRATED STEEL WELDED BOX CAGE (part of the swing-panel weldment)",
        f"Box: {RHS}×{RHS}×{LT_FRAME_T} steel RHS — 4 corner posts + perimeter rails + 2 jamb frames per opening (welded).",
        f"Axle beams: {LT_AXLE_BEAM_H}×{LT_AXLE_BEAM_W}×{LT_AXLE_BEAM_T} steel RHS, span Yd ({LT_AXLE_BEAM_SPAN}mm) at the drum axis; carry the SKF 6215 at midspan (drum hangs from the top beam).",
        f"Bearing seats: upper isolated 6061-T6 Al ring (Ø{LT_TOPRING_OD}, {LT_FRAME_MOUNT_BOLT_TOP}×M10); lower welded steel collar (Ø{LT_COLLAR_OD}, {LT_FRAME_MOUNT_BOLT_BOT}×M10).",
        "Fixed housing (outer skin) laps + rivets to rim-angle on the beams + jamb frames — see Sheet 9. Drum rotates free inside.",
        "The cage is welded into the panel top/bottom rails → one structure, swings together. Panel frame owned by the hinged-panel report.",
        "ALL DIMS IN mm · plate thickness exaggerated for clarity",
    ]
    draw_notes(ax, notes, X_LO + 60, -300, 92, fs=7, font=FONT, width=2500,
               title_color=TITLE_COL)

    title_block(ax, "SHEET 8 OF 10", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="SUPPORT FRAME — GENERAL ARRANGEMENT (INTEGRATED STEEL CAGE)",
                scale_note="ALL DIMS IN mm", doc_id="TBS-001 · Revolving Light-Trap",
                height=0.045, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet8.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet8.png saved")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 6 — Seals & light-path verification
# Three drum rotations proving no straight-through EXT↔INT light path (the drum's
# single 280° wall always blocks one side) + the running-gap / wiper seal details.
# ═════════════════════════════════════════════════════════════════════════════
def draw_sheet6():
    HR, DR = LT_HOUSING_R, LT_DRUM_OR
    oh = LT_OPENING_DEG / 2
    C6_HOUSE = "#2E5E8C"          # FIXED housing (outer skin) — steel blue
    C6_DRUM = "#B5732E"           # ROTATING drum (inner wall) — warm amber
    dx = 2 * HR + 640
    plans = [(0, 180, "A · DRUM OPEN TO EXTERIOR"),
             (dx, 0, "B · DRUM OPEN TO INTERIOR"),
             (2 * dx, 90, "C · DRUM MID-ROTATION")]
    X_LO, X_HI = -HR - 320, 2 * dx + HR + 320
    Z_LO, Z_HI = -HR - 1420, HR + 360
    FIG_W = 20.0
    FIG_H = FIG_W * (Z_HI - Z_LO) / (X_HI - X_LO)
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DIAGRAM_DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Z_LO, Z_HI)
    ax.set_aspect("equal")
    ax.axis("off")

    def arc(cx, cz, r, gapc, gapd, color, lw):
        a0, a1 = gapc + gapd / 2, gapc + 360 - gapd / 2
        ts = [math.radians(a0 + (a1 - a0) * k / 72) for k in range(73)]
        ax.plot([cx + r * math.cos(t) for t in ts], [cz + r * math.sin(t) for t in ts],
                color=color, lw=lw, zorder=6)

    def angdiff(a, b):
        return abs((a - b + 180) % 360 - 180)

    def ray(cx, x0, x1, yy):                                     # one light-path ray (arrow)
        ax.annotate("", xy=(x1, yy), xytext=(x0, yy),
                    arrowprops=dict(arrowstyle="-|>", color="#E8A800", lw=1.7), zorder=5)

    for cx, dth, title in plans:
        # running-gap ring (drum OD → housing bore) — thin, so the annulus reads
        draw_circle(ax, cx, 0, HR - LT_HOUSING_T, lw=0.8, color="#B8BDC6", fill=False, zorder=2)
        # fixed housing walls (OUTER) — two 80° openings, 180° apart (steel blue)
        for gc in (0, 180):
            arc(cx, 0, HR, gc, LT_OPENING_DEG, C6_HOUSE, 5.0)
        # rotating drum wall (INNER) — single 80° opening at dth (warm amber)
        arc(cx, 0, DR, dth, LT_OPENING_DEG, C6_DRUM, 7.0)
        for t in (dth - oh, dth + oh):                            # drum opening jamb ticks
            a = math.radians(t)
            ax.plot([cx + (DR - 24) * math.cos(a), cx + (DR + 24) * math.cos(a)],
                    [(DR - 24) * math.sin(a), (DR + 24) * math.sin(a)],
                    color="#B08020", lw=1.4, zorder=7)
        # LIGHT-PATH RAYS — daylight enters an aligned opening, stopped by the drum wall
        any_aligned = any(angdiff(dth, o) < oh for o in (0, 180))
        for oc in (0, 180):
            es = -1 if oc == 180 else 1                           # side light comes from (EXT=left)
            if angdiff(dth, oc) < oh:                             # aligned → ray crosses to far wall
                for yy in (-150, -55, 55, 150):
                    xh = cx - es * math.sqrt(max(DR * DR - yy * yy, 0.0))
                    ray(cx, cx + es * (HR + 105), xh, yy)
            elif not any_aligned:                                # mid-rotation → blocked at entry
                for yy in (-45, 45):
                    xh = cx + es * math.sqrt(max(DR * DR - yy * yy, 0.0))
                    ray(cx, cx + es * (HR + 105), xh, yy)
        ax.text(cx, HR + 60, title, ha="center", va="bottom", fontsize=7.5,
                color=TITLE_COL, fontweight="bold", **FONT, zorder=9)
        for oc, tag, col in ((180, "EXT", "#5060A0"), (0, "INT", "#407040")):
            aligned = angdiff(dth, oc) < oh
            dirx = -1 if oc == 180 else 1
            ax.text(cx + dirx * (HR + 125), 0, f"{tag}\n{'OPEN (entry)' if aligned else 'SEALED'}",
                    ha=("right" if oc == 180 else "left"), va="center", fontsize=6.5,
                    color=(col if aligned else "#D33"), **FONT, zorder=9)

    ax.text(dx, -HR - 120,
            f"NO STRAIGHT-THROUGH LIGHT PATH: the drum's {LT_SHELL_ARC}° opaque wall always seals at least\n"
            f"one side (openings {LT_OPENING_DEG}° < 90°, housing openings 180° apart, drum has one). Interior stays dark.",
            ha="center", va="top", fontsize=8, color=C_OUT, fontweight="bold", **FONT, zorder=9)

    # ── Legend — inner vs outer panel + light path ───────────────────────────
    lz = -HR - 250
    keys = [(C6_HOUSE, "FIXED HOUSING (outer)", 6.0),
            (C6_DRUM, "ROTATING DRUM (inner)", 7.0),
            ("#E8A800", "LIGHT PATH (ray)", 2.0)]
    lx = dx - 930
    for col, lab, w in keys:
        ax.plot([lx, lx + 70], [lz, lz], color=col, lw=w, zorder=9)
        ax.text(lx + 85, lz, lab, ha="left", va="center", fontsize=7, color=C_OUT,
                **FONT, zorder=9)
        lx += 640

    # ── Seal detail (radial section at the running gap) ──────────────────────
    sx, sz = dx, -HR - 620
    draw_rect(ax, sx - 200, sz - 90, 60, 180, fc="#DDE4EC", lw=1.4, zorder=5)   # housing wall
    draw_rect(ax, sx + 140, sz - 90, 46, 180, fc=C_LT_DRUM, lw=1.4, zorder=5)   # drum wall
    for zz in (sz - 60, sz + 60):                                              # brush/felt seal bristles
        for xx in range(-135, 140, 10):
            ax.plot([sx + xx, sx + xx + 8], [zz - 3, zz + 3], color="#7E7E76", lw=0.5, zorder=6)
    draw_rect(ax, sx - 140, sz - 12, 280, 24, fc="#7E7E76", lw=0.8, zorder=4)   # felt gap seal band
    draw_dim_h(ax, sx - 140, sx + 140, sz - 120, f"≈{RUN_GAP}mm RUNNING GAP", offset=40,
               fs=6.5, above=False, font=FONT)
    leader(ax, sx, sz + 20, sx - 320, sz + 80,
           "FELT / BRUSH GAP SEAL\n(drum ↔ housing running gap)", fs=6.5, color=C_OUT,
           ha="right", arrow_style="->", font=FONT)
    leader(ax, sx - 170, sz, sx - 300, sz - 60, f"HOUSING {LT_HOUSING_T}mm", fs=6,
           color=C_DIM, ha="right", arrow_style="->", font=FONT)
    leader(ax, sx + 163, sz, sx + 300, sz - 60, f"DRUM {LT_DRUM_T:.2f}mm", fs=6,
           color=C_DIM, ha="left", arrow_style="->", font=FONT)
    ax.text(sx, sz + 190, "SEAL DETAIL — RUNNING GAP (enlarged)", ha="center", va="bottom",
            fontsize=7.5, color=TITLE_COL, fontweight="bold", **FONT, zorder=9)

    notes = [
        "SEALS & LIGHT-PATH",
        "Plans A–C: yellow rays = the light path — daylight enters an aligned opening and is stopped by the drum's opaque wall before it can reach the far opening; at mid-rotation both openings are blocked at entry.",
        f"Running gap {RUN_GAP}mm (drum OD → housing bore): closed by a felt/brush wiper — drum rotates against it.",
        "Top + bottom: 12mm closed-cell neoprene wiper strips (cap ↔ frame) + silicone bead to the frame plates.",
        f"Light-tight by geometry: each opening {LT_OPENING_DEG}° (<90°); the drum's {LT_SHELL_ARC}° wall bridges the two 180°-apart housing openings at every rotation.",
        "Interior faces flat-black; residual scatter is killed at the matte wall. ALL DIMS IN mm.",
    ]
    draw_notes(ax, notes, X_LO + 60, -HR - 880, 60, fs=7, font=FONT, width=2400,
               title_color=TITLE_COL)

    title_block(ax, "SHEET 7 OF 10", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="SEALS & LIGHT-PATH VERIFICATION",
                scale_note="ALL DIMS IN mm", doc_id="TBS-001 · Revolving Light-Trap",
                height=0.045, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet7.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet7.png saved")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 8 — Housing → frame attachment (outer-skin fixing)
# The fixed housing (5mm) laps a rolled rim-angle welded to the frame; SS rivets +
# DP8010. Section + jamb detail + plan (200° housing material, two 100° arcs).
# ═════════════════════════════════════════════════════════════════════════════
def draw_sheet8():
    X_LO, X_HI, Z_LO, Z_HI = -470, 1140, -680, 300
    FIG_W = 18.0
    FIG_H = FIG_W * (Z_HI - Z_LO) / (X_HI - X_LO)
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DIAGRAM_DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Z_LO, Z_HI)
    ax.set_aspect("equal")
    ax.axis("off")

    # ── SECTION A-A — housing edge → frame (SCALE 7:1, isotropic) ─────────────
    S = 7                                    # drawn = real mm × 7 (both axes)
    LEGT = S * LT_RIM_T                        # rim-angle leg thickness (3mm)
    LIP  = S * LT_LAP_H                        # lap / lip height (25mm)
    DPT  = S * 1.0                             # DP8010 bead (~1mm)
    HOUT = S * LT_HOUSING_T                    # housing thickness (5mm)
    RIML = S * LT_RIM_LEG                      # rim flat-leg length (25mm)
    RVD  = S * LT_RIVET_D                      # rivet Ø (3.18mm, 1/8")
    BEAMH = S * 16                             # 16mm of the frame beam shown (broken)
    ax.text(-150, Z_HI - 40, "SECTION A–A  (housing → frame rim · SCALE 7:1)",
            ha="center", va="top", fontsize=8.5, color=TITLE_COL, fontweight="bold",
            **FONT, zorder=15)
    draw_rect(ax, -RIML - 40, 0, RIML + 100, BEAMH, fc=C_STEEL, lw=1.6, zorder=4)  # frame beam (broken)
    for xx in (-RIML - 20, -RIML + 20, -RIML + 60):                              # break line (beam continues up)
        ax.plot([xx - 4, xx + 4], [BEAMH - 8, BEAMH + 8], color=C_OUT, lw=0.6, zorder=7)
    draw_rect(ax, -RIML, -LEGT, RIML, LEGT, fc=C_ALUM, lw=1.4, zorder=5)          # rim flat leg (welded under beam)
    draw_rect(ax, -LEGT, -LIP, LEGT, LIP, fc=C_ALUM, lw=1.4, zorder=5)            # standing lip (down)
    ax.add_patch(mpatches.Polygon([(-RIML, 0), (-RIML + 16, 0), (-RIML, -16)], closed=True,
                                  fc="#CC4422", ec="#CC4422", zorder=6))          # weld to beam
    draw_rect(ax, 0, -LIP, DPT, LIP, fc=C_GASKT, lw=0.8, zorder=5)                # DP8010 bead
    draw_rect(ax, DPT, -LIP - 90, HOUT, LIP + 100, fc="#DDE4EC", lw=1.6, zorder=6)  # housing laps down (broken)
    for zz in (-LIP - 55, -LIP - 67, -LIP - 79):                                 # break line (housing continues down)
        ax.plot([DPT - 3, DPT + HOUT + 3], [zz - 4, zz + 4], color=C_OUT, lw=0.6, zorder=7)
    blind_rivet(ax, (DPT + HOUT - LEGT) / 2, -LIP / 2, 0, S * (LT_HOUSING_T + 1 + LT_RIM_T), d=RVD)  # radial housing → lip rivet
    draw_dim_v(ax, DPT + HOUT + 40, -LIP, 0, f"{LT_LAP_H}mm LAP", offset=40, fs=6.5, right=True, font=FONT)
    draw_dim_h(ax, DPT, DPT + HOUT, -LIP - 50, f"{LT_HOUSING_T}mm HOUSING", offset=38, fs=6.2,
               above=False, font=FONT)
    leader(ax, -LEGT, -LIP + 30, -300, -LIP + 90, "RIM ANGLE 25×25×3 6061-T6 Al\nWELDED to the frame beam",
           fs=6.5, color=C_OUT, ha="right", arrow_style="->", font=FONT)
    leader(ax, DPT + HOUT, -LIP + 30, 250, -55, f"FIXED HOUSING {LT_HOUSING_T}mm UV-HDPE\nlaps {LT_LAP_H}mm over the lip",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, (DPT + HOUT - LEGT) / 2, -LIP / 2, 250, -215, f"SS Ø{LT_RIVET_D} DOMED-HEAD BLIND RIVET (radial)\nthrough housing + lip · + DP8010 (light seal)",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, -RIML + 40, BEAMH / 2, -300, BEAMH + 40, "FRAME TOP BEAM / RAIL (steel · Sheet 8)",
           fs=6.5, color=C_OUT, ha="right", arrow_style="->", font=FONT)
    ax.text(150, -LIP - 130, "(bottom edge identical, mirrored, to the bottom beam)",
            ha="center", va="center", fontsize=6.2, color=C_DIM, **FONT, zorder=9)
    sbx, sbz = -300, -LIP - 60                                                   # section scale bar (20mm)
    ax.plot([sbx, sbx + S * 20], [sbz, sbz], color=C_OUT, lw=1.4, zorder=8)
    for xt in (sbx, sbx + S * 10, sbx + S * 20):
        ax.plot([xt, xt], [sbz - 6, sbz + 6], color=C_OUT, lw=1.0, zorder=8)
    ax.text(sbx + S * 10, sbz - 13, "20 mm  (SECTION 7:1)", ha="center", va="top",
            fontsize=6, color=C_OUT, **FONT, zorder=8)

    # ── PLAN — housing footprint (200° material, two 100° arcs) + rivets ──────
    pcx, pcz, pr = 820, 10, LT_HOUSING_R / 2
    oh = LT_OPENING_DEG / 2

    def arc(cx, cz, r, gapc, gapd, color, lw, z=6):
        a0, a1 = gapc + gapd / 2, gapc + 360 - gapd / 2
        # draw both material arcs separately (two openings) — caller loops gaps
        ts = [math.radians(a0 + (a1 - a0) * k / 40) for k in range(41)]
        ax.plot([cx + r * math.cos(t) for t in ts], [cz + r * math.sin(t) for t in ts],
                color=color, lw=lw, zorder=z)
    # two 100° housing arcs (material between the two 80° openings at 0° and 180°)
    for a_lo, a_hi in ((oh, 180 - oh), (180 + oh, 360 - oh)):
        ts = [math.radians(a_lo + (a_hi - a_lo) * k / 40) for k in range(41)]
        ax.plot([pcx + pr * math.cos(t) for t in ts], [pcz + pr * math.sin(t) for t in ts],
                color=C_OUT, lw=2.6, zorder=6)
        # rivets along each arc
        n = max(2, round(LT_HOUSING_RIVET_N / 2))
        for k in range(n):
            t = math.radians(a_lo + (a_hi - a_lo) * (k + 0.5) / n)
            draw_circle(ax, pcx + pr * math.cos(t), pcz + pr * math.sin(t), 5,
                        lw=0.8, color="#CC4422", fill=True, fc="#CC4422", zorder=7)
    for oc, tag, col in ((180, "EXT", "#5060A0"), (0, "INT", "#407040")):
        ax.text(pcx + (pr + 70) * math.cos(math.radians(oc)),
                pcz + (pr + 70) * math.sin(math.radians(oc)), f"{tag}\nOPENING\n(no rim)",
                ha="center", va="center", fontsize=6.2, color=col, **FONT, zorder=8)
    ax.text(pcx, pcz, f"Ø{DRUM_D}\nHOUSING\n({LT_HOUSING_ARC}° rim, 2 arcs)\nHOUSING PLAN — 1:2", ha="center",
            va="center", fontsize=6.8, color=C_DIM, **FONT, zorder=8)
    ax.text(pcx, pcz - pr - 55,
            f"RIVET PATTERN — {LT_HOUSING_RIVET_N}× Ø{LT_RIVET_D} per edge @ ~{LT_RIVET_PITCH}mm\n"
            f"(top + bottom · {2 * LT_HOUSING_RIVET_N} rivets total · rivet symbols schematic)", ha="center", va="top",
            fontsize=6.8, color=C_OUT, **FONT, zorder=8)

    notes = [
        "HOUSING → FRAME ATTACHMENT  (fixed outer skin — does NOT rotate)",
        "1. Rolled 25×25×3 6061-T6 Al rim-angle, radius R450, WELDED to the frame top + bottom beams (two 100° arcs — the openings have no rim).",
        f"2. Housing laps {LT_LAP_H}mm over the standing lip; DP8010 bead in the lap (bond + light seal).",
        f"3. Drill Ø{LT_RIVET_HOLE:.1f} (#30), {LT_HOUSING_RIVET_N}× Ø{LT_RIVET_D} SS domed-head blind rivets per edge (McMaster 97525A435, ~{LT_RIVET_PITCH}mm pitch), wet in DP8010.",
        "4. Housing vertical edges (at the openings) rivet to the jamb frames the same way (see Sheet 8).",
        "SECTION A–A 7:1 (isotropic) · HOUSING PLAN 1:2 · fastener symbols schematic · ALL DIMS IN mm",
    ]
    draw_notes(ax, notes, X_LO + 60, -340, 60, fs=7, font=FONT, width=2050,
               title_color=TITLE_COL)

    title_block(ax, "SHEET 9 OF 10", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="HOUSING → FRAME ATTACHMENT (OUTER-SKIN FIXING)",
                scale_note="SECTION 7:1 · HOUSING PLAN 1:2 · ALL DIMS IN mm",
                doc_id="TBS-001 · Revolving Light-Trap", height=0.045, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet9.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet9.png saved")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 9 — Combined top-end assembly (half-section, NTS)
# One radial half-section at the TOP end showing BOTH joints nested concentrically:
#   inner ROTATING drum shell→cap lap joint (Sheet 4) + outer FIXED housing→frame
#   lap joint (Sheet 9), with the upper SKF 6215 bearing and the running-gap seal
#   between them — so the reader sees how the two combine at the same level.
# Axis on the LEFT (r = 0), radius increases to the right; z = height near the top.
# ═════════════════════════════════════════════════════════════════════════════
def draw_sheet9():
    X_LO, X_HI, Z_LO, Z_HI = -200, 820, -560, 320
    FIG_W = 15.5
    FIG_H = FIG_W * (Z_HI - Z_LO) / (X_HI - X_LO)
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DIAGRAM_DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Z_LO, Z_HI)
    ax.set_aspect("equal")                                                   # ISOTROPIC — drawn to scale
    ax.axis("off")

    ax.text(300, Z_HI - 6, "TOP-END ASSEMBLY  (radial half-section on the drum axis — DRAWN TO SCALE)",
            ha="center", va="top", fontsize=8.5, color=TITLE_COL, fontweight="bold",
            **FONT, zorder=15)

    # ── Real dimensions (mm) from constants; z datum = cap top plane ─────────
    CAPR = LT_CAP_OD / 2                     # 427.5  cap radius
    DIR_ = LT_DRUM_OR - LT_DRUM_T            # 428.82 drum shell inner
    DOR_ = LT_DRUM_OR                        # 432    drum shell outer
    HIR_ = LT_HOUSING_R - LT_HOUSING_T       # 445    housing inner
    HOR_ = LT_HOUSING_R                      # 450    housing outer
    bID, bOD, bW = SKF6215_ID / 2, SKF6215_OD / 2, SKF6215_W   # 37.5 / 65 / 25
    SHAFT_L = 150                            # 75Ø × 150 stub
    Z_BRG0 = SHAFT_L - 20 - bW               # bearing bottom (bW wide, 20 below shaft top)
    Z_BEAM0 = SHAFT_L - 8                     # beam underside just below shaft top
    Z_BRK = -150                             # break-line level (drum/housing continue down)

    # ── Rotation axis (left edge, r = 0) ─────────────────────────────────────
    draw_cl_v(ax, 0, Z_BRK - 20, Z_BEAM0 + 130)
    ax.text(-10, Z_BEAM0 + 120, "DRUM\nAXIS", ha="right", va="top", fontsize=6.2,
            color=C_CL, **FONT, zorder=9)

    # ── FIXED: axle beam (steel RHS) — carries central bearing AND housing ───
    draw_rect(ax, 0, Z_BEAM0, LT_AXLE_BEAM_SPAN / 2, LT_AXLE_BEAM_H, fc=C_STEEL, lw=1.4, zorder=4)
    # ── FIXED: cage corner post (vertical RHS) framing the beam end ──────────
    POST_R0 = LT_AXLE_BEAM_SPAN / 2                                          # 481 — beam outer end / cage corner
    draw_rect(ax, POST_R0, Z_BRK, LT_FRAME_RHS, Z_BEAM0 + LT_AXLE_BEAM_H - Z_BRK,
              fc=C_STEEL, lw=1.4, zorder=3)                                  # corner post (continues down full height)
    for dz in (0, 8, 16):                                                    # break line (post continues down)
        ax.plot([POST_R0 + 4, POST_R0 + LT_FRAME_RHS - 4], [Z_BRK + 6 + dz, Z_BRK + 14 + dz],
                color=C_OUT, lw=0.6, zorder=9)
    # ── Upper SKF 6215 bearing (to scale) + isolated Al ring ─────────────────
    draw_rect(ax, bOD, Z_BRG0, 30, Z_BEAM0 - Z_BRG0, fc=C_ALUM, lw=1.0, zorder=5)   # Al ring bolts up to beam
    draw_rect(ax, bOD - 7.5, Z_BRG0, 7.5, bW, fc=C_STEEL, lw=0.8, zorder=6)         # outer race
    draw_rect(ax, bID, Z_BRG0, 7.5, bW, fc=C_STEEL, lw=0.8, zorder=6)               # inner race
    draw_circle(ax, (bID + bOD) / 2, Z_BRG0 + bW / 2, 8, lw=0.7, color=C_OUT,
                fill=True, fc="white", zorder=7)                                     # one ball (section)
    # ── ROTATING: stub shaft + bolted hub + cap ──────────────────────────────
    draw_rect(ax, 0, -LT_CAP_TOP_T, bID, SHAFT_L, fc=C_STEEL, lw=1.0, zorder=5)     # 75Ø×150 stub shaft
    ax.plot([bID, bID + 8], [Z_BRG0 + bW + 4, Z_BRG0 + bW + 4], color=C_OUT, lw=0.9, zorder=8)  # circlip
    draw_rect(ax, 0, -LT_CAP_TOP_T, CAPR, LT_CAP_TOP_T, fc=C_ALUM, lw=1.2, zorder=5)  # 8mm Al cap disc
    draw_rect(ax, 0, 0, 55, 16, fc=C_ALUM, lw=1.0, zorder=6)                         # bolted hub boss (4×M10)

    # ── INNER joint — drum shell → cap lap (to scale; detail on Sheet 4) ─────
    draw_rect(ax, CAPR - LT_RIM_LEG, 0, LT_RIM_LEG, LT_RIM_T, fc=C_ALUM, lw=0.8, zorder=6)   # rim flat leg
    draw_rect(ax, CAPR - LT_RIM_T, 0, LT_RIM_T, LT_LAP_H, fc=C_ALUM, lw=0.8, zorder=6)       # standing lip (up)
    draw_rect(ax, DIR_, Z_BRK, LT_DRUM_T, LT_LAP_H - Z_BRK, fc=C_LT_DRUM, lw=1.0, zorder=7)  # drum shell (laps up, hangs down)
    draw_circle(ax, (CAPR - LT_RIM_T + DOR_) / 2, LT_LAP_H / 2, LT_RIVET_D / 2,
                lw=0.6, color=C_OUT, fill=True, fc="#C9CCD2", zorder=8)                       # blind rivet (Ø4.8, to scale)

    # ── Running gap + felt seal (to scale; detail on Sheet 7) ────────────────
    draw_rect(ax, DOR_, LT_LAP_H / 2 - 4, RUN_GAP, 8, fc="#7E7E76", lw=0.5, zorder=6)

    # ── FIXED outer skin — housing + housing → frame lap (detail on Sheet 9) ─
    draw_rect(ax, HIR_, Z_BRK, LT_HOUSING_T, Z_BEAM0 - Z_BRK, fc="#DDE4EC", lw=1.0, zorder=6)  # housing wall
    draw_rect(ax, HIR_ - LT_RIM_T, Z_BEAM0 - LT_LAP_H, LT_RIM_T, LT_LAP_H, fc=C_ALUM, lw=0.8, zorder=7)  # lip (down)
    draw_rect(ax, HIR_ - LT_RIM_LEG, Z_BEAM0 - LT_RIM_T, LT_RIM_LEG, LT_RIM_T, fc=C_ALUM, lw=0.8, zorder=7)  # flat leg → beam
    draw_circle(ax, (HIR_ - LT_RIM_T + HOR_) / 2, Z_BEAM0 - LT_LAP_H / 2, LT_RIVET_D / 2,
                lw=0.6, color=C_OUT, fill=True, fc="#C9CCD2", zorder=8)                       # blind rivet (Ø4.8, to scale)

    # break lines (drum + housing continue down the full 2,200mm) ─────────────
    for r0, r1 in ((DIR_ - 4, DOR_ + 4), (HIR_ - 4, HOR_ + 4)):
        for dz in (0, 8, 16):
            ax.plot([r0, r1], [Z_BRK + 6 + dz, Z_BRK + 14 + dz], color=C_OUT, lw=0.6, zorder=9)

    # ── Detail bubbles → the enlarged joint sheets (A→4, B→8; see notes) ─────
    for (rc, zc, tag) in ((CAPR, LT_LAP_H / 2, "A"), (HIR_, Z_BEAM0 - LT_LAP_H / 2, "B")):
        draw_circle(ax, rc, zc, 40, lw=1.0, color=C_DIM, ls="--", zorder=8)
        ax.annotate(tag, xy=(rc - 34, zc), xytext=(rc - 95, zc),
                    ha="center", va="center", fontsize=11, fontweight="bold", color=C_DIM,
                    arrowprops=dict(arrowstyle="->", color=C_DIM, lw=0.9), zorder=9, **FONT)

    # ── Scale bar (100 mm, to scale) ─────────────────────────────────────────
    sb_z = Z_BRK - 70
    ax.plot([0, 100], [sb_z, sb_z], color=C_OUT, lw=1.6, zorder=9)
    for xt in (0, 50, 100):
        ax.plot([xt, xt], [sb_z - 7, sb_z + 7], color=C_OUT, lw=1.2, zorder=9)
    ax.text(50, sb_z - 16, "100 mm  (scale bar)", ha="center", va="top", fontsize=6.5,
            color=C_OUT, **FONT, zorder=9)

    # ── Key dimensions (to scale) ────────────────────────────────────────────
    draw_dim_v(ax, -95, -LT_CAP_TOP_T, Z_BEAM0 - 8, f"{SHAFT_L} STUB (Ø{SKF6215_ID})",
               offset=48, fs=6.5, font=FONT)
    draw_dim_h(ax, 0, CAPR, -LT_CAP_TOP_T - 60, f"Ø{LT_CAP_OD} CAP (radius)", offset=44,
               fs=6.5, above=False, font=FONT)

    # ── Zone tags ────────────────────────────────────────────────────────────
    ax.text(210, -70, "◄ ROTATES WITH DRUM", ha="center", va="center", fontsize=7,
            color="#407040", fontweight="bold", **FONT, zorder=9)
    ax.text(300, Z_BEAM0 + 70, "FIXED (FRAME + HOUSING) ►", ha="center", va="center", fontsize=7,
            color="#5060A0", fontweight="bold", **FONT, zorder=9)

    # ── Leaders ──────────────────────────────────────────────────────────────
    leader(ax, (bID + bOD) / 2, Z_BRG0 + bW / 2, 210, Z_BEAM0 + 30,
           "SKF 6215-2RS1 upper bearing\nin isolated Al ring, bolted to the axle beam (Sheet 5)",
           fs=6.5, color=C_OUT, ha="center", arrow_style="->", font=FONT)
    leader(ax, 30, 8, -150, -35, "Al CAP + BOLTED\nSTUB HUB (4×M10)", fs=6.5, color=C_OUT,
           ha="right", arrow_style="->", font=FONT)
    leader(ax, DOR_ + RUN_GAP / 2, LT_LAP_H / 2, 700, 55,
           f"RUNNING GAP {RUN_GAP}mm + felt/brush seal (Sheet 7)",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, LT_AXLE_BEAM_SPAN / 2 - 60, Z_BEAM0 + LT_AXLE_BEAM_H / 2, 700, Z_BEAM0 + 120,
           f"AXLE BEAM {LT_AXLE_BEAM_H}×{LT_AXLE_BEAM_W} steel RHS — carries the central\nbearing + the fixed housing; swing-panel weldment (Sheet 8)",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, POST_R0 + LT_FRAME_RHS / 2, -35, 700, -35,
           f"CAGE CORNER POST {LT_FRAME_RHS}×{LT_FRAME_RHS}×{LT_FRAME_T} RHS\nframes the beam end · welded to the panel rails (Sheet 8)",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, HOR_, -110, 700, -130, f"FIXED HOUSING Ø{DRUM_D} (outer skin)\nrotating drum Ø{2 * LT_DRUM_OR} inside",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)

    notes = [
        "COMBINED TOP-END ASSEMBLY  (drawn to scale — see 100mm bar)",
        "The rotating drum (cap + shell on the stub shaft) hangs from the central bearing and turns inside the fixed housing; the two never touch — a felt-sealed running gap separates them.",
        "INNER joint (rotating), DETAIL A: drum shell laps the cap rim-angle — SS blind rivets + DP8010; full detail on Sheet 4.",
        "OUTER joint (fixed), DETAIL B: housing laps a rim-angle welded to the axle beam — SS blind rivets + DP8010; full detail on Sheet 9.",
        "The two joints sit at different heights (drum joint at the cap, housing joint at the beam) and on opposite walls of the running gap, so the rotating rivets always clear the fixed ones.",
        "Drum + housing continue the full 2,200mm below the break lines. Bottom end mirrors this, with the lower bearing in a welded steel floor collar (Sheet 5). ALL DIMS IN mm.",
    ]
    draw_notes(ax, notes, X_LO + 40, Z_BRK - 170, 34, fs=7, font=FONT, width=1240,
               title_color=TITLE_COL)

    title_block(ax, "SHEET 10 OF 10", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="COMBINED TOP-END ASSEMBLY (INNER + OUTER LAP JOINTS)",
                scale_note="HALF-SECTION · TO SCALE (100mm bar) · DETAILS A/B → SHEETS 4 & 9",
                doc_id="TBS-001 · Revolving Light-Trap", height=0.045, scale=0.72)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet10.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet10.png saved")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 6 — Machined components (single-part blueprints, 1:2)
# The turned/machined metal parts that Sheet 5 assembles: upper Al bearing ring,
# lower steel floor collar, and the stub-shaft + flange. Each: PLAN (end view with
# OD / bore / PCD / bolt holes) + SECTION (thickness) + full dims + material.
# ═════════════════════════════════════════════════════════════════════════════
def draw_sheet_components():
    X_LO, X_HI, Z_LO, Z_HI = -300, 2260, -520, 360
    FIG_W = 20.0
    FIG_H = FIG_W * (Z_HI - Z_LO) / (X_HI - X_LO)
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DIAGRAM_DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Z_LO, Z_HI)
    ax.set_aspect("equal")                                                   # ISOTROPIC 1:2
    ax.axis("off")
    s2 = 0.5                                                                  # 1:2
    ax.text(980, Z_HI - 8, "MACHINED COMPONENTS — BEARING SEATS & STUB-SHAFT  (single-part blueprints · 1:2)",
            ha="center", va="top", fontsize=9, color=TITLE_COL, fontweight="bold", **FONT, zorder=15)

    def holes(cx, cz, rpcd, n):
        for i in range(n):
            a = math.radians(90 + i * 360.0 / n)
            hx, hy = cx + rpcd * math.cos(a), cz + rpcd * math.sin(a)
            draw_circle(ax, hx, hy, 5, lw=1.0, color=C_OUT, fill=True, fc="white", zorder=8)
            ax.plot([hx - 9, hx + 9], [hy, hy], color=C_OUT, lw=0.5, zorder=9)
            ax.plot([hx, hx], [hy - 9, hy + 9], color=C_OUT, lw=0.5, zorder=9)

    def ring(cx, od, bore, pcd, n, thk, fc, title, mat, weldnote=None):
        rod, rbore, rpcd = od / 2 * s2, bore / 2 * s2, pcd / 2 * s2
        pz, sz = 120, -170                                                   # plan / section z-centers
        # ── PLAN (end view) ──
        ax.text(cx, pz + rod + 40, title, ha="center", va="bottom", fontsize=8,
                color=TITLE_COL, fontweight="bold", **FONT, zorder=10)
        draw_circle(ax, cx, pz, rod, lw=1.8, color=C_OUT, fill=True, fc=fc, zorder=5)
        draw_circle(ax, cx, pz, rbore, lw=1.4, color=C_OUT, fill=True, fc="white", zorder=6)
        draw_circle(ax, cx, pz, rpcd, lw=0.8, color=C_CL, ls="--", zorder=6)
        holes(cx, pz, rpcd, n)
        draw_cl_h(ax, cx - rod - 16, cx + rod + 16, pz)
        draw_cl_v(ax, cx, pz - rod - 16, pz + rod + 16)
        draw_dim_h(ax, cx - rod, cx + rod, pz + rod + 8, f"Ø{od} OD", offset=30, fs=6.4, font=FONT)
        ax.text(cx, pz, f"Ø{bore}\nH7", ha="center", va="center", fontsize=6.2, color=C_DIM, **FONT, zorder=9)
        ax.text(cx, pz - rod - 16, f"{n}×M10 on Ø{pcd} PCD · drill Ø11", ha="center", va="top",
                fontsize=6.6, color=C_OUT, **FONT, zorder=9)
        # ── SECTION (annular, thickness) ──
        tz = thk * s2
        for xr0, xr1 in ((cx - rod, cx - rbore), (cx + rbore, cx + rod)):
            draw_rect(ax, xr0, sz, xr1 - xr0, tz, fc=fc, lw=1.4, zorder=5)
        draw_cl_v(ax, cx, sz - 14, sz + tz + 14)
        draw_dim_v(ax, cx + rod + 30, sz, sz + tz, f"{thk} THK", offset=30, fs=6.4, right=True, font=FONT)
        draw_dim_h(ax, cx - rbore, cx + rbore, sz - 18, f"Ø{bore} BORE", offset=26, fs=6.0,
                   above=False, font=FONT)
        if weldnote:
            ax.add_patch(mpatches.Polygon([(cx - rod, sz), (cx - rod - 14, sz), (cx - rod, sz + 14)],
                                          closed=True, fc="#CC4422", ec="#CC4422", zorder=7))
            ax.add_patch(mpatches.Polygon([(cx + rod, sz), (cx + rod + 14, sz), (cx + rod, sz + 14)],
                                          closed=True, fc="#CC4422", ec="#CC4422", zorder=7))
        ax.text(cx, sz - 48, mat + ("" if not weldnote else f"\n{weldnote}"),
                ha="center", va="top", fontsize=6.6, color=C_OUT, **FONT, zorder=9)

    # ── 1 · Upper Al bearing ring ────────────────────────────────────────────
    ring(80, LT_TOPRING_OD, SKF6215_OD, 165, LT_FRAME_MOUNT_BOLT_TOP, 30, C_ALUM,
         "UPPER BEARING RING", "6061-T6 Al · bore Ø130 H7 (bearing seat) · isolate w/ nylon shoulder")
    # ── 2 · Lower steel floor collar ─────────────────────────────────────────
    ring(880, LT_COLLAR_OD, SKF6215_OD, 175, LT_FRAME_MOUNT_BOLT_BOT, 30, C_STEEL,
         "LOWER FLOOR COLLAR", "A36 steel · bore Ø130 (bearing seat)", weldnote="6mm fillet weld to floor plate")

    # ── 3 · Stub-shaft + flange (elevation + flange plan) ────────────────────
    cx = 1720
    sh_r, fl_r, fl_t = SKF6215_ID / 2 * s2, 160 / 2 * s2, 12 * s2
    shaft_L = 150 * s2
    ez = -125                                                                # elevation base (flange top)
    ax.text(cx, 120 + fl_r + 40, "STUB-SHAFT + FLANGE", ha="center", va="bottom", fontsize=8,
            color=TITLE_COL, fontweight="bold", **FONT, zorder=10)
    # ELEVATION: flange (bottom) + shaft (up)
    draw_rect(ax, cx - fl_r, ez - fl_t, 2 * fl_r, fl_t, fc=C_STEEL, lw=1.6, zorder=5)     # flange
    draw_rect(ax, cx - sh_r, ez, 2 * sh_r, shaft_L, fc=C_STEEL, lw=1.6, zorder=5)         # shaft
    for g in (-1, 1):                                                                     # fillet weld shaft→flange
        ax.add_patch(mpatches.Polygon([(cx + g * sh_r, ez), (cx + g * (sh_r + 12), ez),
                                       (cx + g * sh_r, ez + 12)], closed=True, fc="#CC4422", ec="#CC4422", zorder=7))
    for zc in (ez + shaft_L - 10, ez + shaft_L - 22):                                     # circlip grooves
        ax.plot([cx - sh_r, cx - sh_r + 6], [zc, zc], color=C_OUT, lw=1.2, zorder=8)
        ax.plot([cx + sh_r - 6, cx + sh_r], [zc, zc], color=C_OUT, lw=1.2, zorder=8)
    draw_cl_v(ax, cx, ez - fl_t - 14, ez + shaft_L + 14)
    draw_dim_v(ax, cx - fl_r - 30, ez, ez + shaft_L, f"{150} LG (Ø{SKF6215_ID})", offset=30, fs=6.4, font=FONT)
    draw_dim_v(ax, cx + fl_r + 30, ez - fl_t, ez, "12 THK", offset=28, fs=6.0, right=True, font=FONT)
    ax.text(cx, ez + shaft_L + 16, "Ø75 h6 stub · circlip groove each end", ha="center", va="bottom",
            fontsize=6.2, color=C_DIM, **FONT, zorder=9)
    # FLANGE PLAN (above the elevation)
    fpz = 120
    draw_circle(ax, cx, fpz, fl_r, lw=1.8, color=C_OUT, fill=True, fc=C_STEEL, zorder=5)
    draw_circle(ax, cx, fpz, sh_r, lw=1.4, color=C_OUT, fill=True, fc="#9BA0A8", zorder=6)  # shaft (solid)
    draw_circle(ax, cx, fpz, 120 / 2 * s2, lw=0.8, color=C_CL, ls="--", zorder=6)
    holes(cx, fpz, 120 / 2 * s2, 4)
    draw_cl_h(ax, cx - fl_r - 16, cx + fl_r + 16, fpz)
    draw_dim_h(ax, cx - fl_r, cx + fl_r, fpz + fl_r + 8, "Ø160 FLANGE", offset=28, fs=6.2, font=FONT)
    ax.text(cx, fpz - fl_r - 14, "4×M10 on Ø120 PCD · drill Ø11", ha="center", va="top",
            fontsize=6.6, color=C_OUT, **FONT, zorder=9)
    ax.text(cx, ez - fl_t - 30, "1045 steel shaft + steel flange · weld + stress-relieve", ha="center",
            va="top", fontsize=6.6, color=C_OUT, **FONT, zorder=9)

    notes = [
        "MACHINED COMPONENTS  (bearing seats + stub-shaft — assembled on Sheet 5)",
        f"Bearing seat bores Ø{SKF6215_OD} H7 for the SKF 6215 OD; the stub shaft Ø{SKF6215_ID} h6 for the bearing bore. Circlip grooves (DIN 471) each side.",
        "Upper ring 6061-T6 Al (electrically isolated from the steel frame by a nylon shoulder + isolating washers); lower collar A36 steel, fillet-welded to the floor plate.",
        "Stub-shaft flange bolts to the cap (4×M10, Sheet 3); ring/collar bolt to the axle beam (Sheet 8). Bolt holes shown enlarged; drill Ø11 clearance for M10.",
        "PLANS + SECTIONS 1:2 (isotropic) · ALL DIMS IN mm",
    ]
    draw_notes(ax, notes, X_LO + 60, -300, 40, fs=7, font=FONT, width=2450, title_color=TITLE_COL)

    title_block(ax, "SHEET 6 OF 10", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="MACHINED COMPONENTS — BEARING SEATS & STUB-SHAFT",
                scale_note="PLANS + SECTIONS 1:2 · ALL DIMS IN mm",
                doc_id="TBS-001 · Revolving Light-Trap", height=0.045, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet6.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet6.png saved")


def main():
    print("Generating TBS-001 Revolving Light-Trap blueprint sheets...")
    draw_sheet1()
    draw_sheet2()
    draw_sheet3()
    draw_sheet_secure()    # Sheet 4 — drum secure (shell → cap joint)
    draw_sheet_hub()       # Sheet 5 — bearing hub (assembly)
    draw_sheet_components() # Sheet 6 — machined components (bearing seats + stub-shaft)
    draw_sheet6()          # Sheet 7 — seals & light-path
    draw_sheet7()          # Sheet 8 — support frame GA
    draw_sheet8()          # Sheet 9 — housing → frame attachment
    draw_sheet9()          # Sheet 10 — combined top-end assembly (inner + outer joints)
    print("Done.")


if __name__ == "__main__":
    main()
