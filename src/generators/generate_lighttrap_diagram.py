#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_lighttrap_diagram.py
TBS-001  Ventilation System — two drawing sheets.

Sheet 1: Ventilation system — container longitudinal section
Sheet 2: Fan & baffle duct — assembly section
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
from tbs_constants import (
    C_OUT, C_CL, C_DIM, C_ALUM, C_STEEL,
    FAN_DIAM, DUCT_DEPTH, DUCT_HEIGHT,
    EVAP_DUCT_Z, EVAP_DUCT_X, C_HGT, C_LEN,
    DIAGRAMS_DIR,
    SWUNG_DOOR_CLEARANCE_MM,
)
from tbs_drawing import draw_dim_h, draw_dim_v, draw_rect, leader, draw_notes
from tbs_title_block import title_block
from tbs_constants import DIAGRAM_DPI

# ── Local palette (not in tbs_constants — specific to this diagram) ──────────
C_SOLAR = "#D4EDDA"   # evap cooler fill
C_GND   = "#2C5F2E"
C_PIPE  = "#6C757D"
C_VEST  = "#EEF5EE"   # vestibule interior
TITLE_COL = "#0F2D5E"


def ann(ax, text, xy, xytext, size=7.5):
    """Leader-line annotation — thin wrapper around shared leader()."""
    leader(ax, xy[0], xy[1], xytext[0], xytext[1], text,
           fs=size, color=C_OUT, ha="center", va="center",
           arrow_style="->", lw=0.9, zorder=10)




# ─────────────────────────────────────────────────────────────────────────────
# SHEET 1 — Ventilation System
# Longitudinal container section (schematic, not to scale)
# Fan positions, cross-ventilation path, evap cooler, cable trunking
# ─────────────────────────────────────────────────────────────────────────────

def draw_sheet1():
    FW, FH = 24.0, 13.0
    fig, ax = plt.subplots(figsize=(FW, FH), dpi=DIAGRAM_DPI)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(0, FW)
    ax.set_ylim(0, FH)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    ax.text(FW/2, FH - 0.38,
            "VENTILATION SYSTEM — CONTAINER LONGITUDINAL SECTION",
            ha="center", va="center", fontsize=13, fontweight="bold",
            color=TITLE_COL)
    ax.text(FW/2, FH - 0.70,
            "TBS-001  ·  Longitudinal section (schematic, not to scale)  ·  "
            "Fan positions, cross-ventilation path, evap cooler  ·  "
            "Baffle duct assembly detail — see Sheet 2",
            ha="center", va="center", fontsize=8.0, color=C_DIM)

    # ── LEFT HALF: Container longitudinal section ────────────────────────────
    # Schematic box representing the container interior
    CX, CY = 1.8, 4.0      # container interior bottom-left
    CW, CH = 20.0, 7.0     # container interior drawing dimensions (schematic)
    WT = 0.35               # wall thickness (schematic)

    # Container shell
    draw_rect(ax, CX, CY, CW, CH, fc="#F2F2EE", lw=2.5, zorder=2)
    # Hatched walls
    for rx, ry, rw, rh in [
        (CX,       CY,      CW, WT),            # floor
        (CX,       CY+CH-WT, CW, WT),           # ceiling
        (CX,       CY+WT,   WT, CH-2*WT),       # left wall (image plane end)
        (CX+CW-WT, CY+WT,   WT, CH-2*WT),      # right wall (door/vestibule end)
    ]:
        draw_rect(ax, rx, ry, rw, rh, fc=C_STEEL, lw=0.5, zorder=3)

    # Interior label
    ax.text(CX + CW/2, CY + CH/2,
            "CONTAINER INTERIOR\n5898mm long × 2352mm wide",
            ha="center", va="center", fontsize=9.0, color=C_DIM,
            style="italic", zorder=3)

    # ── EXHAUST FAN A (left end wall — far / IBC end, compact axial panel fan, high position) ──
    # Both fans are identical: 150mm compact axial panel fan, ~50mm body depth.
    # Same part, same mounting flange, same baffle duct — simplified procurement.
    PF_T  = 0.16   # panel fan body thickness in drawing units (~50mm, schematic)
    R_PF  = 0.38   # panel fan impeller radius (150mm dia, schematic)
    BD_W  = 0.80   # baffle duct schematic depth
    FA_Y  = CY + CH - WT - CH * 0.18    # high position (sealed-end corridor, below X1)

    # Baffle duct box — between interior face of left wall and panel fan
    bd_a_x0 = CX + WT                      # right edge of left wall = duct left face
    draw_rect(ax, bd_a_x0, FA_Y - 0.40, BD_W, 0.80, fc="#D8E8D8", lw=0.9, zorder=5)
    ax.text(bd_a_x0 + BD_W / 2, FA_Y, "BAFFLE\nDUCT",
            ha="center", va="center", fontsize=5.5, color=C_DIM, zorder=6)

    # Grille indicator — tinted strip in left wall exterior face
    draw_rect(ax, CX, FA_Y - 0.40, WT, 0.80, fc="#A8D8B0", lw=0.7, zorder=5)
    ax.text(CX + WT / 2, FA_Y, "G", ha="center", va="center",
            fontsize=6.0, color=C_GND, fontweight="bold", zorder=6)

    # Panel fan body — thin rectangle immediately right of baffle duct
    FA_X   = bd_a_x0 + BD_W + PF_T / 2    # fan center (impeller plane)
    pf_a_x0 = bd_a_x0 + BD_W              # left face of panel fan
    draw_rect(ax, pf_a_x0, FA_Y - R_PF - 0.08, PF_T, (R_PF + 0.08) * 2,
              fc=C_ALUM, lw=1.5, zorder=5)
    # fan EDGE-ON (axis horizontal, along the airflow): centerline + motor hub +
    # pitched impeller blades + ID. (Was a face-on circle, which read vertical-axis.)
    ax.plot([pf_a_x0 - 0.08, pf_a_x0 + PF_T + 0.08], [FA_Y, FA_Y],
            color=C_CL, lw=0.7, ls=(0, (4, 3)), zorder=6)
    draw_rect(ax, FA_X - PF_T * 0.32, FA_Y - R_PF * 0.26, PF_T * 0.64, R_PF * 0.52,
              fc=C_STEEL, lw=0.8, zorder=7)
    for sgn in (-1, 1):
        ax.plot([pf_a_x0 + PF_T * 0.30, pf_a_x0 + PF_T * 0.70],
                [FA_Y + sgn * R_PF * 0.30, FA_Y + sgn * R_PF * 0.80],
                color=C_DIM, lw=1.0, alpha=0.5, zorder=6)
    ax.text(FA_X, FA_Y + R_PF + 0.05, "A", ha="center", va="bottom",
            fontsize=8.5, fontweight="bold", color=C_OUT, zorder=7)

    # Airflow: container → fan → baffle → grille → exterior left (leftward, out)
    ax.annotate("", xy=(CX - 1.6, FA_Y),
                xytext=(CX, FA_Y),
                arrowprops=dict(arrowstyle="-|>", color="#D32F2F", lw=2.5), zorder=7)
    ax.text(CX - 1.8, FA_Y, "HOT AIR\nOUT",
            ha="left", va="center", fontsize=8.0, color="#D32F2F", fontweight="bold")
    # Short interior collection arrow from container into fan
    ax.annotate("", xy=(pf_a_x0 + PF_T + 0.05, FA_Y),
                xytext=(pf_a_x0 + PF_T + 0.65, FA_Y),
                arrowprops=dict(arrowstyle="-|>", color="#D32F2F", lw=1.2, alpha=0.6), zorder=6)

    ann(ax, f"Cct A  |  {FAN_DIAM}mm compact axial panel fan\n5A / 16AWG / 60W / 150+ CFM\n~50mm body depth",
        (FA_X, FA_Y - R_PF), (FA_X + 1.4, FA_Y - 2.2), size=7.5)
    ann(ax, "HIGH POSITION\n~2000mm AFF",
        (FA_X, FA_Y - R_PF), (FA_X + 1.2, FA_Y - 1.0), size=7.5)

    # ── INTAKE FAN B (right end wall — cargo door panel, identical compact axial panel fan, low position)
    # Same fan, duct, and mounting as Fan A.
    FB_Y  = CY + WT + CH * 0.18   # low position

    # Baffle duct box — between interior face of right wall and panel fan
    bd_b_x0 = CX + CW - WT - BD_W     # left edge of baffle duct box
    draw_rect(ax, bd_b_x0, FB_Y - 0.40, BD_W, 0.80, fc="#D8E8D8", lw=0.9, zorder=5)
    ax.text(bd_b_x0 + BD_W / 2, FB_Y, "BAFFLE\nDUCT",
            ha="center", va="center", fontsize=5.5, color=C_DIM, zorder=6)

    # Grille indicator — tinted strip in right wall exterior face
    draw_rect(ax, CX + CW - WT, FB_Y - 0.40, WT, 0.80, fc="#A8D8B0", lw=0.7, zorder=5)
    ax.text(CX + CW - WT / 2, FB_Y, "G", ha="center", va="center",
            fontsize=6.0, color=C_GND, fontweight="bold", zorder=6)

    # Panel fan body — thin rectangle immediately left of baffle duct
    FB_X  = bd_b_x0 - PF_T / 2           # fan center (impeller plane)
    pf_x0 = bd_b_x0 - PF_T               # left face of panel fan
    draw_rect(ax, pf_x0, FB_Y - R_PF - 0.08, PF_T, (R_PF + 0.08) * 2,
              fc=C_ALUM, lw=1.5, zorder=5)
    # Impeller circle on face
    # fan EDGE-ON (axis horizontal) — matches Fan A, Sheet 2, and the 3D model
    ax.plot([pf_x0 - 0.08, pf_x0 + PF_T + 0.08], [FB_Y, FB_Y],
            color=C_CL, lw=0.7, ls=(0, (4, 3)), zorder=6)
    draw_rect(ax, FB_X - PF_T * 0.32, FB_Y - R_PF * 0.26, PF_T * 0.64, R_PF * 0.52,
              fc=C_STEEL, lw=0.8, zorder=7)
    for sgn in (-1, 1):
        ax.plot([pf_x0 + PF_T * 0.30, pf_x0 + PF_T * 0.70],
                [FB_Y + sgn * R_PF * 0.30, FB_Y + sgn * R_PF * 0.80],
                color=C_DIM, lw=1.0, alpha=0.5, zorder=6)
    ax.text(FB_X, FB_Y + R_PF + 0.05, "B", ha="center", va="bottom",
            fontsize=8.5, fontweight="bold", color=C_OUT, zorder=7)

    # Airflow: exterior right → grille → baffle → fan (leftward into container)
    ax.annotate("", xy=(CX + CW, FB_Y),
                xytext=(CX + CW + 1.6, FB_Y),
                arrowprops=dict(arrowstyle="-|>", color=C_CL, lw=2.5), zorder=7)
    ax.text(CX + CW + 1.8, FB_Y, "OUTSIDE\nAIR IN",
            ha="right", va="center", fontsize=8.0, color=C_CL, fontweight="bold")
    # Short interior distribution arrow from fan into container
    ax.annotate("", xy=(pf_x0 - 0.65, FB_Y),
                xytext=(pf_x0 - 0.05, FB_Y),
                arrowprops=dict(arrowstyle="-|>", color=C_CL, lw=1.2, alpha=0.6), zorder=6)

    ann(ax, f"Cct B  |  {FAN_DIAM}mm compact axial panel fan\n5A / 16AWG / 60W / 150+ CFM\n~50mm body depth  ·  275mm cone margin",
        (FB_X, FB_Y + R_PF), (FB_X - 2.0, FB_Y + 2.2), size=7.5)
    ann(ax, "LOW POSITION\n~600mm AFF",
        (FB_X, FB_Y + R_PF), (FB_X - 1.2, FB_Y + 1.0), size=7.5)

    # ── EVAP COOLER (ground-placed outside, pinhole wall at X=EVAP_DUCT_X=1000mm) ──
    # Left wall = far end (X=5893), right wall = door end (X=0).
    # X=EVAP_DUCT_X(1000) → fraction from left = (C_LEN-1000)/C_LEN ≈ 0.83
    # Cooler sits on ground outside; flex duct connects to baffled wall stub.
    EC_WALL_X = CX + CW * ((C_LEN - EVAP_DUCT_X) / C_LEN)
    # Duct penetrates HIGH on the wall face at Z=EVAP_DUCT_Z (not the floor).
    ec_z = CY + WT + (CH - 2 * WT) * (EVAP_DUCT_Z / C_HGT)   # high penetration Z
    # Baffled duct stub on the wall face, high up — Ø200 duct seen end-on (round).
    ax.add_patch(mpatches.Circle((EC_WALL_X, ec_z), 0.20,
                                 fc="#A8D8B0", ec=C_OUT, lw=1.2, zorder=6))
    ax.add_patch(mpatches.Circle((EC_WALL_X, ec_z), 0.12,
                                 fc="none", ec=C_OUT, lw=0.7, zorder=7))   # bore
    # Cooler box — outside, on the ground (below the container floor).
    EC_W, EC_H = 1.3, 0.65
    EC_X = EC_WALL_X - EC_W / 2
    EC_Y = CY - 0.55 - EC_H
    ax.add_patch(mpatches.FancyBboxPatch((EC_X, EC_Y), EC_W, EC_H,
                 boxstyle="round,pad=0.04", fc=C_SOLAR, ec=C_OUT, lw=1.5, zorder=5))
    ax.text(EC_X + EC_W / 2, EC_Y + EC_H / 2, "EVAP COOLER\n(Cct E)",
            ha="center", va="center", fontsize=7.0, fontweight="bold",
            color=C_OUT, zorder=6)
    ax.text(EC_X + EC_W / 2, EC_Y - 0.12, "OUTSIDE — on ground",
            ha="center", va="top", fontsize=6.5, color=C_DIM, fontweight="bold", zorder=10)
    # Flex duct — rises up the EXTERIOR wall from the cooler to the high penetration.
    dx = EC_X - 0.30   # routed just outside the container, clear of the interior
    ax.plot([EC_X, dx, dx, EC_WALL_X],
            [EC_Y + EC_H / 2, EC_Y + EC_H / 2, ec_z, ec_z],
            color=C_PIPE, lw=3.0, ls="--", zorder=4)
    ax.text(dx - 0.1, (EC_Y + ec_z) / 2, "flex duct\n(up exterior wall)", ha="right",
            va="center", fontsize=6.0, color=C_PIPE, style="italic", zorder=10)
    # Airflow arrow: duct → into the container at the high penetration.
    ax.annotate("", xy=(EC_WALL_X - 0.6, ec_z), xytext=(EC_WALL_X, ec_z),
                arrowprops=dict(arrowstyle="-|>", color=C_CL, lw=2.0), zorder=7)
    ann(ax, f"Light-safe baffled intake\n(Ø200mm, HIGH — Z={EVAP_DUCT_Z}mm)",
        (EC_WALL_X, ec_z), (EC_WALL_X - 2.0, ec_z + 0.9))

    # ── Cross-ventilation airflow path ────────────────────────────────────────
    # Curved arrow from intake Fan B (right wall, low) diagonally to exhaust Fan A (left wall, high)
    ax.annotate("", xy=(FA_X + R_PF + 0.3, FA_Y),
                xytext=(FB_X - R_PF - 0.3, FB_Y),
                arrowprops=dict(arrowstyle="-|>", color=C_CL,
                                lw=5, mutation_scale=20,
                                connectionstyle="arc3,rad=0.35",
                                alpha=0.6), zorder=4)
    ax.text(CX + CW/2, CY + CH/2 - 0.8,
            "cross-ventilation\npath (low → high)",
            ha="center", va="center", fontsize=7.5, color=C_CL,
            style="italic", alpha=0.7)

    # ── Cable trunking (top corner rail) ──────────────────────────────────────
    TK_Y = CY + CH - WT - 0.12
    ax.plot([CX + WT, CX + CW - WT], [TK_Y, TK_Y],
            color=C_PIPE, lw=4.0, solid_capstyle="round", zorder=4)
    ax.text((CX + WT + CX + CW - WT)/2, TK_Y + 0.22,
            "40 × 25mm PVC cable trunking  (Circuits A, B, D, E)",
            ha="center", va="bottom", fontsize=7.5, color=C_PIPE, fontweight="bold")
    # Drop conduits
    for dx, dy in [(FA_X, FA_Y + R_PF), (FB_X, FB_Y + R_PF),
                   (EC_WALL_X, CY + WT)]:
        ax.plot([dx, dx], [TK_Y, dy], color=C_PIPE, lw=0.9, linestyle=":", zorder=3)

    # Revolving drum light trap label on right (replaces old vestibule)
    ax.add_patch(mpatches.Rectangle((CX + CW, CY), 1.5, CH,
                 fc=C_VEST, ec=C_OUT, lw=1.5, linestyle="--", zorder=2))
    ax.text(CX + CW + 0.75, CY + CH/2, "DRUM\nLIGHT\nTRAP",
            ha="center", va="center", fontsize=7.0, color="#2D6A2D",
            fontweight="bold", rotation=90)

    # ── Film left-rail removal — swing-out clearance note ─────────────────────
    # The film-plane LEFT RAIL (X=150mm in container coords) passes through the
    # drum volume (Yd 731–1631mm). That rail (TL+BL) lifts out of its saddles so the
    # cargo panel + drum can SWING ~56° about the pivot post for transport.
    # In this schematic longitudinal section the left rail is not drawn (it runs
    # perpendicular to this view), but we add a callout note above the drum box
    # so the relationship is documented on this sheet.
    DRUM_BOX_X = CX + CW        # 21.8 — drum box left edge in drawing coords
    DRUM_BOX_MID_Y = CY + CH / 2  # vertical center of drum box (~7.5)
    DRUM_BOX_TOP_Y = CY + CH      # 11.0 — top of drum box
    # Note box — placed above the drum box, within canvas (xlim 0–24, ylim 0–13).
    # Right-aligned to X=23.9 so it stays inside the axis xlim=24.
    NOTE_RX = 23.90               # right edge of note box
    NOTE_W  = 3.70                # note box width
    NOTE_H  = 1.10                # note box height
    NOTE_LX = NOTE_RX - NOTE_W    # left edge = 20.20
    NOTE_CX = NOTE_LX + NOTE_W / 2  # 22.05 — center
    NOTE_CY = DRUM_BOX_TOP_Y + 0.90  # 11.90 — above drum box
    ax.add_patch(mpatches.FancyBboxPatch(
        (NOTE_LX, NOTE_CY - NOTE_H / 2), NOTE_W, NOTE_H,
        boxstyle="round,pad=0.06", fc="#FFFBE6", ec="#C07030", lw=1.0,
        zorder=11))
    ax.text(NOTE_CX, NOTE_CY,
            "SWING-OUT (rev10): CARGO PANEL + DRUM REVOLVE\n"
            "~56° ABOUT THE PIVOT POST FOR TRANSPORT\n"
            "LEFT film rail (TL+BL) lifts out to clear the X=150 plane",
            ha="center", va="center", fontsize=6.5, color="#7A3A00",
            fontweight="bold", zorder=12)
    # Leader arrow from note bottom to drum box top-center
    DRUM_BOX_CX = DRUM_BOX_X + 0.75   # 22.55 — drum box horizontal center
    ax.annotate("", xy=(DRUM_BOX_CX, DRUM_BOX_TOP_Y),
                xytext=(NOTE_CX, NOTE_CY - NOTE_H / 2),
                arrowprops=dict(arrowstyle="->", color="#C07030", lw=1.0),
                zorder=12)

    # ── Transport / walkway note — the swing needs the left rails + left walkway out ─
    # (rev10) The cargo panel + drum SWING ~56° about the pivot post for transport (no
    # slide). The LEFT film rails (TL+BL) lift out of their saddles + the LEFT WALKWAY
    # (X 170–470mm) lifts out so the swinging cage can transition the X=150 rail plane.
    # The walkway is LOWERED (deck Z=130) and stays in place during camera operation.
    TN_W  = 3.70
    TN_H  = 0.95
    TN_RX = 23.90
    TN_LX = TN_RX - TN_W          # 20.20
    TN_CX = TN_LX + TN_W / 2      # 22.05
    TN_CY = CY - 0.55              # 3.45 — just below drum box bottom (CY=4.0)
    ax.add_patch(mpatches.FancyBboxPatch(
        (TN_LX, TN_CY - TN_H / 2), TN_W, TN_H,
        boxstyle="round,pad=0.06", fc="#E8F4FD", ec="#1565C0", lw=1.0,
        zorder=11))
    ax.text(TN_CX, TN_CY,
            "TRANSPORT (rev10): strike the LEFT film rails + lift out\n"
            "the left walkway → cargo panel + drum SWING ~56° about\n"
            f"the pivot post, clearing the door (true min X +{SWUNG_DOOR_CLEARANCE_MM}mm)",
            ha="center", va="center", fontsize=6.2, color="#0D47A1",
            fontweight="bold", zorder=12)
    # Leader arrow from note top to drum box bottom-center
    ax.annotate("", xy=(DRUM_BOX_CX, CY),
                xytext=(TN_CX, TN_CY + TN_H / 2),
                arrowprops=dict(arrowstyle="->", color="#1565C0", lw=1.0),
                zorder=12)

    # Operating modes table (shifted down to clear cooler outside container)
    MX, MY = CX, CY - 1.6
    ax.add_patch(mpatches.FancyBboxPatch((MX - 0.1, MY - 1.45), CW + 0.2, 1.55,
                 boxstyle="round,pad=0.04", fc="#F8F9FA", ec=C_DIM, lw=0.8, zorder=2))
    ax.text(MX + CW/2, MY - 0.05, "FAN OPERATING MODES",
            ha="center", va="top", fontsize=9.0, fontweight="bold", color=C_OUT)
    modes = [
        ("EXPOSURE",               "OFF",        "OFF",        "OFF"),
        ("LOADING / DEVELOPMENT",  "Low speed",  "Low speed",  "ON"),
        ("POST-SESSION PURGE",     "Full speed", "Full speed", "OFF"),
        ("PRE-COOL (before entry)", "Full speed", "Full speed", "ON"),
    ]
    hdrs = ["MODE", "FAN A — end wall (exhaust)", "FAN B — panel (intake)", "EVAP COOLER"]
    for ci, hdr in enumerate(hdrs):
        hx = MX + ci * (CW / 4)
        ax.text(hx + CW/8, MY - 0.30, hdr,
                ha="center", va="center", fontsize=7.8, fontweight="bold", color=C_OUT)
    ax.plot([MX, MX + CW], [MY - 0.46, MY - 0.46], color=C_OUT, lw=0.7)
    for ri, (mode, fa, fb, ec_m) in enumerate(modes):
        ry = MY - 0.60 - ri * 0.22
        vals = [mode, fa, fb, ec_m]
        for ci, val in enumerate(vals):
            vx = MX + ci * (CW / 4)
            ax.text(vx + CW/8, ry, val,
                    ha="center", va="center", fontsize=7.5,
                    color=C_OUT if ci == 0 else ("#D32F2F" if "OFF" in val else "#2E7D32"))

    # Mirror so drum/door end is on the left (consistent with other elevations)
    ax.invert_xaxis()

    title_block(ax, "SHEET 1 OF 2",
                drawing_title="VENTILATION SYSTEM",
                subtitle="Cross-ventilation layout  ·  Fan positions  ·  Evap cooler  ·  Cable trunking",
                scale_note="Schematic — not to scale",
                doc_id="TBS-LT · Light Trap & Ventilation")

    plt.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet1.png"), dpi=DIAGRAM_DPI, bbox_inches="tight",
                pad_inches=0.10, facecolor="white")
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet1.png  Done.")


# ─────────────────────────────────────────────────────────────────────────────
# SHEET 2 — Fan + Baffle Duct + Wall Assembly
# Longitudinal cross-section through the fan axis showing how the fan,
# baffle duct housing, and container wall connect.
# ─────────────────────────────────────────────────────────────────────────────

def draw_sheet2():

    # ── Physical dimensions (mm) ─────────────────────────────────────────────
    WALL_T  = 25                     # container wall (exaggerated — real ~2-3mm)
    DD      = DUCT_DEPTH             # 300
    DH      = DUCT_HEIGHT            # 200
    SK      = 10                     # duct housing wall thickness
    BF_T    = 6                      # baffle plate (exaggerated — real ~2mm)
    PF_BD   = 50                     # panel fan body depth
    PF_R    = FAN_DIAM / 2           # 75
    FL_OH   = 30                     # flange overhang above/below duct
    FL_T    = 5                      # flange plate thickness
    GL_W    = 40                     # louvre grille depth
    GL_H    = int(DH * 0.65)         # 130

    # ── Reference coordinates (mm) ───────────────────────────────────────────
    # X = 0 at exterior face of container wall.  Z increases upward.
    WALL_X  = 0
    DX      = WALL_X + WALL_T        # 25  — interior wall face / duct left
    FX      = DX + DD                 # 325 — duct right face / fan inlet
    DZ      = 150                     # duct bottom
    FCZ     = DZ + DH / 2            # 250 — fan / duct center
    int_h   = DH - 2 * SK           # 180 clear interior
    int_d   = DD - SK                # 290 clear interior depth
    wz0     = DZ - FL_OH             # 120 — wall / flange bottom
    wz1     = DZ + DH + FL_OH        # 380 — wall / flange top

    # ── Canvas ────────────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(24, 14), dpi=DIAGRAM_DPI)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(-250, 850)
    ax.set_ylim(-100, 500)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # ── Title ─────────────────────────────────────────────────────────────────
    cx = 300
    ax.text(cx, 488,
            "FAN & BAFFLE DUCT — PLAN (LOOKING DOWN)",
            ha="center", va="center", fontsize=13, fontweight="bold",
            color=TITLE_COL)
    ax.text(cx, 475,
            "TBS-001  ·  Horizontal section through fan axis, looking down  ·  Exterior left → Interior right  ·  "
            "Baffles full-height (welded top+bottom), air gap on alternating sides  ·  Dimensions in mm",
            ha="center", va="center", fontsize=8.0, color=C_DIM)

    # ── Container wall ────────────────────────────────────────────────────────
    draw_rect(ax, WALL_X, wz0, WALL_T, wz1 - wz0, fc=C_STEEL, lw=2.0, zorder=4)
    for zi in range(wz0, wz1, 8):
        ax.plot([WALL_X, WALL_X + WALL_T], [zi, zi + 10],
                color=C_OUT, lw=0.4, alpha=0.4, zorder=5)
    draw_rect(ax, WALL_X, DZ + SK, WALL_T, int_h, fc="#F2F2EE", color="none", lw=0, zorder=5)
    ann(ax, "CONTAINER WALL\ncorrugated steel\n(wall thickness exaggerated)",
        (WALL_X + WALL_T / 2, wz1 - 5), (WALL_X - 40, wz1 + 25))

    # ── Weatherproof louvre grille ─────────────────────────────────────────────
    GL_Z = DZ + DH / 2 - GL_H / 2
    draw_rect(ax, WALL_X - GL_W, GL_Z, GL_W, GL_H, fc="#D0D8C8", lw=1.2, zorder=6)
    slat_h  = 4
    slat_gap = GL_H / 6
    for i in range(5):
        slat_z = GL_Z + slat_gap * (i + 0.5)
        ax.add_patch(mpatches.FancyBboxPatch(
            (WALL_X - GL_W + 3, slat_z - slat_h / 2), GL_W - 6, slat_h,
            boxstyle="round,pad=0.3", fc=C_DIM, ec="none", zorder=7, alpha=0.75))
    ann(ax, "Weatherproof louvre grille\n(no fan — passive inlet/outlet)\n150mm dia. round → rect adapter",
        (WALL_X - GL_W / 2, GL_Z - 5), (WALL_X - GL_W / 2 - 50, GL_Z - 50))

    # ── Baffle duct housing ───────────────────────────────────────────────────
    draw_rect(ax, DX, DZ, DD, DH, fc="#F5F5F5", lw=2.0, zorder=3)
    for rx, ry, rw, rh in [
        (DX, DZ,        DD, SK),
        (DX, DZ+DH-SK,  DD, SK),
    ]:
        draw_rect(ax, rx, ry, rw, rh, fc=C_STEEL, lw=0.8, zorder=4)
    ax.add_patch(mpatches.Rectangle((DX, DZ + SK), DD, int_h,
                 fc="#2A2A2A", ec="none", zorder=2, alpha=0.12))

    # ── Wall mounting flange ──────────────────────────────────────────────────
    draw_rect(ax, DX, wz0, FL_T, wz1 - wz0, fc=C_ALUM, lw=1.2, zorder=6)
    for bz in [wz0 + FL_OH * 0.45, wz1 - FL_OH * 0.45]:
        ax.plot(DX + FL_T / 2, bz, "o", color=C_OUT, ms=4, zorder=7)
    ann(ax, "Wall mounting flange\n5mm plate · 4×M10 bolts\n(interior face of wall)",
        (DX + FL_T / 2, wz0 - 5), (DX + 20, wz0 - 45))

    # ── Baffles ───────────────────────────────────────────────────────────────
    AIR_GAP = 75                            # airflow gap left by each baffle (S-path)
    B1_X = DX + int_d * 0.30
    B1_H = int_h - AIR_GAP
    B1_Z = DZ + SK + int_h - B1_H
    draw_rect(ax, B1_X, B1_Z, BF_T, B1_H, fc=C_OUT, lw=0.5, zorder=5)

    B2_X = DX + int_d * 0.70
    B2_H = int_h - AIR_GAP
    B2_Z = DZ + SK
    draw_rect(ax, B2_X, B2_Z, BF_T, B2_H, fc=C_OUT, lw=0.5, zorder=5)

    ann(ax, "Baffle 1 (full height,\nwelded top+bottom)\n75mm AIRFLOW gap\nnear side",
        (B1_X + BF_T / 2, B1_Z + B1_H * 0.6),
        (B1_X - 50, B1_Z + B1_H * 0.6 + 20))
    ann(ax, "Baffle 2 (full height,\nwelded top+bottom)\n75mm AIRFLOW gap\nfar side",
        (B2_X + BF_T / 2, B2_Z + B2_H * 0.4),
        (B2_X + 50, B2_Z + B2_H * 0.4 - 30))
    ax.text(DX + DD / 2, DZ + SK + int_h * 0.5,
            "FLAT BLACK\nPOWDER COAT\nALL INTERIOR FACES",
            ha="center", va="center", fontsize=7.0, color="#808080",
            style="italic", alpha=0.85, zorder=9)
    ax.text(300, -50,
            "LIGHT-TIGHT: each baffle is FULL height, welded to the duct top & bottom (no edge gap); the two "
            "plates take opposite sides (75mm air gap each) — air winds left↔right (horizontal S-path) while the line of sight stays blocked.",
            ha="center", va="center", fontsize=8.5, color=TITLE_COL, fontweight="bold", zorder=9)

    # ── Fan mounting flange (duct right face) ─────────────────────────────────
    draw_rect(ax, FX - FL_T, wz0, FL_T, wz1 - wz0, fc=C_ALUM, lw=1.2, zorder=6)
    for bz in [wz0 + FL_OH * 0.45, wz1 - FL_OH * 0.45]:
        ax.plot(FX - FL_T / 2, bz, "o", color=C_OUT, ms=4, zorder=7)
    ann(ax, "Fan mounting flange\n5mm plate · 4×M10 bolts\n(same both fans)",
        (FX - FL_T / 2, wz1 + 5), (FX - FL_T / 2, wz1 + 45))

    # ── Panel fan body ────────────────────────────────────────────────────────
    draw_rect(ax, FX, FCZ - PF_R - 5, PF_BD, (PF_R + 5) * 2,
              fc=C_ALUM, lw=1.8, zorder=5)
    # Fan shown IN PROFILE (axis horizontal, air flows L→R along X) — consistent
    # with this section and the 3D model. (Was a face-on circle, which read as a
    # vertical axis.)
    draw_rect(ax, FX, FCZ - PF_R, PF_BD, 2 * PF_R, fc="#E8EEF4", lw=0.8, zorder=5.5)  # bore
    ax.plot([FX - 10, FX + PF_BD + 10], [FCZ, FCZ],
            color=C_CL, lw=0.9, ls=(0, (6, 3)), zorder=7)                              # axis CL
    hub_d, hub_l = PF_R * 0.40, PF_BD * 0.58                                           # motor hub
    draw_rect(ax, FX + (PF_BD - hub_l) / 2, FCZ - hub_d / 2, hub_l, hub_d,
              fc=C_STEEL, lw=1.0, zorder=8)
    for sgn in (-1, 1):                                                                # impeller blades
        for bxo in (0.32, 0.50, 0.68):                                                 # (pitched, in profile)
            xb = FX + PF_BD * bxo
            ax.plot([xb - 5, xb + 5], [FCZ + sgn * hub_d / 2, FCZ + sgn * (PF_R - 6)],
                    color=C_DIM, lw=1.3, alpha=0.55, zorder=7)
    ax.text(FX, FCZ + PF_R + 10, "INLET\n(air enters)",
            ha="center", va="bottom", fontsize=7.0, color=C_CL, fontweight="bold", zorder=10)
    ax.text(FX + PF_BD, FCZ + PF_R + 10, "OUTLET\n(air exits)",
            ha="center", va="bottom", fontsize=7.0, color="#D32F2F", fontweight="bold", zorder=10)
    ax.text(FX + PF_BD / 2, FCZ - PF_R - 10,
            "← FAN AXIS HORIZONTAL →\nair flows along this axis",
            ha="center", va="top", fontsize=7.0, color=C_DIM, style="italic", zorder=10)

    # ── Wiring run ────────────────────────────────────────────────────────────
    wr_x = FX + PF_BD + 5
    wr_z = FCZ - PF_R * 0.35
    ax.plot([wr_x, wr_x + 80], [wr_z, wr_z],
            color=C_PIPE, lw=2.5, solid_capstyle="round", zorder=5)
    ax.text(wr_x + 85, wr_z,
            "16 AWG wiring → Cct A/B\n→ electrical panel\n(all inside container)",
            ha="left", va="center", fontsize=7.5, color=C_PIPE, zorder=10)

    ax.text(520, FCZ + PF_R - 20,
            f"{FAN_DIAM}mm COMPACT AXIAL PANEL FAN  ·  Fan A (exhaust) and Fan B (intake) — identical\n"
            "Cct A/B  ·  60W  ·  150+ CFM  ·  ~50mm body depth  ·  Interior-mounted",
            ha="center", va="top", fontsize=8.0, fontweight="bold", color=C_OUT, zorder=10)

    # ── Airflow arrows ────────────────────────────────────────────────────────
    mid_z = FCZ
    gap1_z = DZ + SK
    gap2_z = DZ + SK + int_h - int_h * 0.35
    z_gap1 = gap1_z + int_h * 0.35 / 2
    z_gap2 = gap2_z + int_h * 0.35 / 2
    pc, plw = C_CL, 1.6

    ax.annotate("", xy=(WALL_X - GL_W, mid_z), xytext=(WALL_X - GL_W - 60, mid_z),
                arrowprops=dict(arrowstyle="-|>", color=pc, lw=2.5), zorder=8)
    ax.text(WALL_X - GL_W - 65, mid_z, "OUTSIDE\nAIR IN",
            ha="right", va="center", fontsize=9.0, color=pc, fontweight="bold", zorder=10)
    ax.annotate("", xy=(DX + 10, mid_z), xytext=(WALL_X + WALL_T - 3, mid_z),
                arrowprops=dict(arrowstyle="-|>", color=pc, lw=plw), zorder=7)
    # S-path through baffles
    ax.annotate("", xy=(B1_X - 12, z_gap1), xytext=(B1_X - 12, mid_z),
                arrowprops=dict(arrowstyle="-|>", color=pc, lw=plw), zorder=7)
    ax.annotate("", xy=(B1_X + BF_T + 12, z_gap1), xytext=(B1_X - 3, z_gap1),
                arrowprops=dict(arrowstyle="-|>", color=pc, lw=plw), zorder=7)
    ax.annotate("", xy=(B2_X - 12, z_gap2), xytext=(B2_X - 12, z_gap1),
                arrowprops=dict(arrowstyle="-|>", color=pc, lw=plw), zorder=7)
    ax.annotate("", xy=(B2_X + BF_T + 12, z_gap2), xytext=(B2_X - 3, z_gap2),
                arrowprops=dict(arrowstyle="-|>", color=pc, lw=plw), zorder=7)
    ax.annotate("", xy=(FX - 3, mid_z), xytext=(B2_X + BF_T + 18, mid_z),
                arrowprops=dict(arrowstyle="-|>", color=pc, lw=plw), zorder=7)
    ax.annotate("", xy=(FX + PF_BD + 60, mid_z),
                xytext=(FX + PF_BD + 8, mid_z),
                arrowprops=dict(arrowstyle="-|>", color=pc, lw=2.5), zorder=8)
    ax.text(FX + PF_BD + 65, mid_z, "INTO\nCONTAINER",
            ha="left", va="center", fontsize=9.0, color=pc, fontweight="bold", zorder=10)
    ax.text(FX + PF_BD + 65, mid_z - PF_R - 10,
            "(exhaust: flow reversed — same assembly)",
            ha="left", va="top", fontsize=7.0, color=C_DIM, style="italic", zorder=10)

    # ── Zone labels ───────────────────────────────────────────────────────────
    ax.text(-70, wz0 - 10, "EXTERIOR",
            ha="center", va="top", fontsize=9.0, color=C_DIM, fontweight="bold", zorder=10)
    ax.text(DX + (FX + PF_BD - DX) / 2, wz0 + 15,
            "INTERIOR (container)",
            ha="center", va="top", fontsize=9.0, color=C_DIM, fontweight="bold", zorder=10)
    ax.plot([WALL_X + WALL_T / 2, WALL_X + WALL_T / 2], [wz0 - 20, wz0 - 5],
            color=C_DIM, lw=1.0, ls=":")

    # ── Dimension lines ───────────────────────────────────────────────────────
    draw_dim_h(ax, DX, DX + DD, DZ - 35, f"{DUCT_DEPTH}mm  (duct depth)",
               offset=10, fs=7.5, zorder=10, color=C_DIM)
    draw_dim_v(ax, DX - 55, DZ, DZ + DH, f"{DUCT_HEIGHT}mm",
               offset=10, fs=7.5, zorder=10, color=C_DIM)
    draw_dim_h(ax, WALL_X, WALL_X + WALL_T, DZ + DH + 25, "wall",
               offset=10, fs=7.5, zorder=10, color=C_DIM)
    ax.plot([WALL_X, WALL_X], [DZ + DH, DZ + DH + 30],
            color=C_DIM, lw=0.5, ls=":")
    ax.plot([WALL_X + WALL_T, WALL_X + WALL_T], [DZ + DH, DZ + DH + 30],
            color=C_DIM, lw=0.5, ls=":")
    draw_dim_h(ax, FX, FX + PF_BD, DZ - 30, "~50mm\n(panel fan body)",
               offset=10, fs=7.5, zorder=10, color=C_DIM)

    # ── Notes ─────────────────────────────────────────────────────────────────
    draw_notes(ax, [
        "BOTH FANS — 150mm COMPACT AXIAL PANEL FAN  ·  ONE PART NUMBER",
        "Fan A (exhaust, far end wall) and Fan B (intake, cargo door panel) are identical.",
        "Same fan body, same mounting flange, same baffle duct — simplified fabrication and procurement.",
        f"Total depth from wall (each):  {DUCT_DEPTH}mm baffle duct + {PF_BD}mm fan = {DUCT_DEPTH + PF_BD}mm",
        "Shadow margins:  Fan A → +894mm clear of cone right edge  ·  Fan B → +275mm clear of cone left edge  ✓",
    ], x=350, y_top=80, spacing=15,
       fs=7.5, title_fs=8.5, title_color=C_CL, width=300,
       border_color=C_CL, border_lw=1.0)

    title_block(ax, "SHEET 2 OF 2",
                drawing_title="FAN & BAFFLE DUCT — ASSEMBLY SECTION",
                subtitle="Interior-mounted fan  ·  Passive louvre grille (exterior only)  ·  "
                "Baffle duct interior-mounted  ·  All wiring inside container",
                scale_note="Dimensions in mm — wall thickness exaggerated",
                doc_id="TBS-LT · Light Trap & Ventilation")

    plt.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet2.png"), dpi=DIAGRAM_DPI, bbox_inches="tight",
                pad_inches=0.10, facecolor="white")
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet2.png  Done.")


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Generating TBS-001 Light Trap & Ventilation diagrams...")
    draw_sheet1()
    draw_sheet2()
    print("Done.")
