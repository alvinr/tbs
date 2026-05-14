#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_electrical_diagram.py
TBS-001 Electrical & Systems — two engineering drawing sheets.

Sheet 1: System one-line diagram (power flow, components, fuse ratings)
Sheet 2: Container floor plan with wiring layout  (scale 1:500)
"""

import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Arc
import os
from tbs_constants import (
    svg_path, SVG_DIR,
    C_WASTE_IBC, C_BLUE_IBC, C_BROWN_IBC,
    C_EVAP, C_ELEC, C_BATT, C_PUMP,
)
from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v, leader

# ── Palette ───────────────────────────────────────────────────────────────────
C_OUT   = "#1A1A1A"
C_CL    = "#2060A0"
C_DIM   = "#505050"
C_ALUM  = "#C8D8E8"
C_STEEL = "#B0B0B8"
# C_ELEC, C_BATT imported from tbs_constants (unified equipment colors)
C_SOLAR = "#D4EDDA"       # solar array schematic fill (not an equipment constant)
C_WARN  = "#F8D7DA"
C_GND   = "#2C5F2E"
C_PIPE  = "#6C757D"
TITLE_COL = "#0F2D5E"

# Light tints of unified equipment colors for Sheet 1 schematic blocks
# where bold fills would overpower wiring labels and text
C_ELEC_TINT  = "#FFF3CC"   # pale yellow tint for electrical panel schematic boxes
C_BATT_TINT  = "#CCE5FF"   # pale blue tint for battery schematic boxes
C_EVAP_TINT  = "#D4EDDA"   # pale green tint for evap cooler schematic boxes
C_PUMP_TINT  = "#FFDEC8"   # pale orange tint for pump schematic boxes


# ── Shared helpers ────────────────────────────────────────────────────────────

def rbox(ax, x, y, w, h, title, subtitle="", fc=C_ELEC_TINT, ec=C_OUT, lw=1.4,
         ts=9.0, ss=7.5, bold=True):
    """Rounded rectangle with title + optional subtitle."""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04",
                                fc=fc, ec=ec, lw=lw, zorder=3))
    ty = y + h / 2 + (0.11 if subtitle else 0)
    ax.text(x + w / 2, ty, title, ha="center", va="center",
            fontsize=ts, fontweight="bold" if bold else "normal",
            color=C_OUT, zorder=4)
    if subtitle:
        ax.text(x + w / 2, y + h / 2 - 0.13, subtitle,
                ha="center", va="center", fontsize=ss, color=C_DIM, zorder=4)


def varrow(ax, x, y1, y2, col=C_CL, lw=2.0):
    ax.annotate("", xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=lw), zorder=5)


def wlabel(ax, x, y, text, ha="left", size=7.5):
    """Wire label with white background."""
    ax.text(x, y, text, ha=ha, va="center", fontsize=size, color=C_DIM,
            bbox=dict(fc="white", ec="none", pad=1.5), zorder=6)






# ─────────────────────────────────────────────────────────────────────────────
# SHEET 1 — System One-Line Diagram
# Layout:
#   Left column  (x=0.7–7.0):  power chain top-to-bottom
#   Centre-right (x=7.5–13.0): shore charger branch + ground + legend + summary
#   Right column (x=8.5–20.0): 6 circuits fanning off vertical spine
# ─────────────────────────────────────────────────────────────────────────────

def draw_sheet1():
    FW, FH = 22.0, 15.0
    fig, ax = plt.subplots(figsize=(FW, FH), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(0, FW)
    ax.set_ylim(0, FH)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # Page title
    ax.text(FW / 2, FH - 0.38, "SYSTEM ONE-LINE DIAGRAM — 12V DC OFF-GRID",
            ha="center", va="center", fontsize=15, fontweight="bold", color=TITLE_COL)
    ax.text(FW / 2, FH - 0.72,
            "TBS-001  ·  The Big Shoebox Project  ·  "
            "All loads 12V DC  ·  Negative-grounded system",
            ha="center", va="center", fontsize=8.5, color=C_DIM)

    # ── LEFT COLUMN: power chain ──────────────────────────────────────────────
    LX, LW = 0.7, 6.2
    CX = LX + LW / 2   # centreline

    # 1. Solar array  y=12.0–13.1
    rbox(ax, LX, 12.0, LW, 1.1,
         "SOLAR ARRAY",
         "3 × 200W monocrystalline  |  12V nominal  |  Isc = 30A combined",
         fc=C_SOLAR, ts=9.5, ss=8.0)

    # 2. MPPT  y=10.3–11.2
    rbox(ax, LX, 10.3, LW, 0.9,
         "MPPT CHARGE CONTROLLER",
         "Victron SmartSolar MPPT 100/50  |  Max PV: 100V OC / 50A charge",
         fc=C_ELEC_TINT, ts=9.5, ss=8.0)
    varrow(ax, CX, 12.0, 11.2, col=C_SOLAR)
    wlabel(ax, CX + 0.18, 11.6, "10 AWG PV cable  |  Via flush-mount power panel")

    # 3. Battery bank  y=8.4–9.5
    rbox(ax, LX, 8.4, LW, 1.1,
         "BATTERY BANK — 200Ah / 2,400Wh",
         "2 × 100Ah 12V LiFePO4 in parallel  |  100% DoD usable  |  Safe to 60 °C",
         fc=C_BATT_TINT, ts=9.5, ss=8.0)
    varrow(ax, CX, 10.3, 9.5, col=C_CL)
    wlabel(ax, CX + 0.18, 9.9, "2 AWG  |  Charge positive")

    # Negative busbar (dashed, right side of column)
    nb_x = LX + LW - 0.35
    ax.plot([nb_x, nb_x], [8.4, 5.6],
            color=C_STEEL, lw=1.5, linestyle="--", zorder=3)
    wlabel(ax, nb_x + 0.12, 7.0, "NEG busbar  2/0 AWG", size=7.0)

    # 4. 200A ANL main fuse  y=6.95–7.65
    rbox(ax, LX + 1.2, 6.95, LW - 2.4, 0.70,
         "200A ANL MAIN FUSE",
         "Battery (+) → busbar  |  2/0 AWG",
         fc=C_WARN, ts=9.0, ss=7.5)
    varrow(ax, CX, 8.4, 7.65, col=C_OUT)
    wlabel(ax, CX + 0.18, 8.05, "2/0 AWG  |  Battery positive")

    # 5. Fuse block  y=5.4–6.55
    rbox(ax, LX, 5.4, LW, 1.15,
         "BLUE SEA 5026 FUSE BLOCK",
         "12-circuit ST-blade  |  Positive + negative busbars  |  In IP65 enclosure",
         fc=C_WARN, ts=10.0, ss=8.0)
    varrow(ax, CX, 6.95, 6.55, col=C_OUT)
    wlabel(ax, CX + 0.18, 6.75, "2/0 AWG  |  Fuse → busbar")

    # Ground symbol below fuse block
    gx = LX + 0.7
    gy0 = 5.1
    ax.plot([gx, gx], [5.4, gy0], color=C_GND, lw=1.5, zorder=4)
    for i, hw in enumerate([0.40, 0.28, 0.16]):
        yg = gy0 - i * 0.14
        ax.plot([gx - hw, gx + hw], [yg, yg],
                color=C_GND, lw=1.6 - i * 0.3, zorder=4)
    ax.text(gx + 0.55, gy0 - 0.25,
            "CHASSIS EARTH\n8ft copper ground stake\n+ container body bond",
            ha="left", va="center", fontsize=7.5, color=C_GND, zorder=5)

    # ── SHORE CHARGER BRANCH (centre-top, same row as battery) ───────────────
    SC_X = LX + LW + 1.0
    SC_W = 5.8
    SC_Y = 8.4

    rbox(ax, SC_X, SC_Y, SC_W, 1.1,
         "SHORE CHARGER  (optional backup)",
         "Victron Blue Smart IP65 12/15  |  100–240V AC in  |  15A DC / 12V out",
         fc="#F5EDD0", ts=9.0, ss=8.0, bold=False)

    # Horizontal arrow: battery right → shore charger left
    mid_y = SC_Y + 0.55
    ax.annotate("", xy=(SC_X, mid_y), xytext=(LX + LW, mid_y),
                arrowprops=dict(arrowstyle="-|>", color="#A07820", lw=2.0), zorder=5)
    wlabel(ax, LX + LW + 0.15, mid_y + 0.20, "4 AWG  |  Charge return")

    # NEMA 5-15R inlet below shore charger
    rbox(ax, SC_X, SC_Y - 1.35, SC_W, 0.80,
         "NEMA 5-15R INLET  (flush-mount power panel — pinhole wall)",
         "Weatherproof  |  Shore power input when mains available",
         fc="white", ec=C_OUT, lw=1.0, ts=8.5, ss=7.5, bold=False)
    varrow(ax, SC_X + SC_W / 2, SC_Y - 0.55, SC_Y, col="#A07820")
    wlabel(ax, SC_X + SC_W / 2 + 0.15, SC_Y - 0.28, "Shore AC →", size=7.0)

    # ── LEGEND ────────────────────────────────────────────────────────────────
    lx, ly = SC_X, 1.4
    LEG_H = 3.78
    ax.add_patch(FancyBboxPatch((lx - 0.1, ly - 0.15), SC_W + 0.2, LEG_H,
                 boxstyle="round,pad=0.05", fc="#F8F9FA", ec=C_DIM, lw=0.8, zorder=2))
    ax.text(lx + SC_W / 2, ly + LEG_H - 0.32, "LEGEND",
            ha="center", va="center", fontsize=9.5,
            fontweight="bold", color=C_OUT)
    ax.plot([lx + 0.1, lx + SC_W - 0.1], [ly + LEG_H - 0.55, ly + LEG_H - 0.55],
            color=C_DIM, lw=0.7)
    legend_items = [
        (C_SOLAR,      "Solar / generation"),
        (C_BATT_TINT,  "Battery / storage"),
        (C_ELEC_TINT,  "Controller / charger"),
        (C_WARN,       "Fuse / protection device"),
        (C_ALUM,       "Ventilation loads"),
        (C_EVAP_TINT,  "Cooling loads"),
        ("#FFFFF0",    "Lighting loads"),
        ("#F5EDD0",    "Shore power (backup only)"),
        (C_GND,        "Earth / chassis ground"),
    ]
    for j, (col, txt) in enumerate(legend_items):
        yl = ly + LEG_H - 0.88 - j * 0.36
        ax.add_patch(mpatches.Rectangle((lx + 0.15, yl - 0.11), 0.45, 0.28,
                     fc=col, ec=C_OUT, lw=0.7, zorder=4))
        ax.text(lx + 0.75, yl + 0.03, txt,
                ha="left", va="center", fontsize=8.0, color=C_DIM)

    # ── ENERGY SUMMARY ────────────────────────────────────────────────────────
    ex = lx + SC_W + 0.8
    ey, ew, eh = 1.4, 6.8, 3.78
    ax.add_patch(FancyBboxPatch((ex - 0.1, ey - 0.15), ew + 0.2, eh,
                 boxstyle="round,pad=0.05", fc="#F8F9FA", ec=C_DIM, lw=0.8, zorder=2))
    ax.text(ex + ew / 2, ey + eh - 0.28, "ENERGY SUMMARY",
            ha="center", va="center", fontsize=9.5,
            fontweight="bold", color=TITLE_COL)
    ax.plot([ex + 0.1, ex + ew - 0.1], [ey + eh - 0.55, ey + eh - 0.55],
            color=C_DIM, lw=0.7)
    summary = [
        ("Battery capacity",    "200Ah × 12V = 2,400Wh  (LiFePO4, 100% DoD)"),
        ("Energy per session",  "~1.5–1.8 kWh  (one print, ~3–4h active)"),
        ("Prints per charge",   "1.3–1.6 full prints from a full charge"),
        ("Solar yield",         "600W × 5.5h = 3,300 Wh/day  (Palm Springs)"),
        ("Solar recharge",      "~1 day from flat with 600W array"),
        ("Shore recharge",      "~14h from flat  (15A charger)"),
        ("Peak load",           "~475W simultaneous  (all circuits on)"),
    ]
    for k, (param, val) in enumerate(summary):
        yk = ey + eh - 0.80 - k * 0.37
        ax.text(ex + 0.20, yk, param + ":",
                ha="left", va="center", fontsize=7.8,
                fontweight="bold", color=C_OUT)
        ax.text(ex + ew - 0.20, yk, val,
                ha="right", va="center", fontsize=7.8, color=C_DIM)

    # ── CIRCUITS — right column ───────────────────────────────────────────────
    circuits = [
        # letter, name, fuse, wire, load, note, colour
        ("A", "VENTILATION FAN\nINTAKE  (6\")",   "5A",  "16 AWG", "60W",
         "Far end wall (X=5,893mm)  |  low position  |  Yd=75mm corner", C_ALUM),
        ("B", "VENTILATION FAN\nEXHAUST  (6\")",  "5A",  "16 AWG", "60W",
         "Cargo door end wall (X=0)  |  high position  |  Yd=2,287mm corner", C_ALUM),
        ("C", "WATER PUMP  (12V DC)",              "15A", "14 AWG", "100W",
         "Adjacent water totes", C_PUMP_TINT),
        ("D", "SAFELIGHT\ninterior + vestibule",  "5A",  "18 AWG", "15W",
         "3× red LED strips (ceiling, N–S)  |  pull-cord switch", "#FFEEDD"),
        ("E", "EVAPORATIVE\nCOOLER  (12V DC)",      "10A", "14 AWG", "80W",
         "Far short wall  |  light-safe baffled intake", C_EVAP_TINT),
        ("F", "FILM PLANE\nACTUATORS  (optional)",  "20A", "12 AWG", "≤100W pk",
         "Future provision  |  leave fused spare", "#E8E8E8"),
        ("G", "WHITE LED PANELS\n(general lighting)",  "10A", "16 AWG", "60W",
         "3×20W ceiling panels  |  pull-cord switch  |  non-operational only", "#FFFFF0"),
    ]

    SP_X  = ex - 0.5      # spine x
    CB_X  = SP_X + 0.65   # circuit boxes left edge
    CB_W  = FW - CB_X - 0.4
    CB_H  = 0.78
    CB_GAP = 1.05
    CB_Y_TOP = 13.1       # top circuit box y

    # Vertical distribution spine
    spine_bot = 5.4 + 1.15 / 2   # mid-height of fuse block
    spine_top = CB_Y_TOP + CB_H + 0.10
    ax.plot([SP_X, SP_X], [spine_bot, spine_top],
            color=C_CL, lw=3.0, solid_capstyle="butt", zorder=3)

    # Horizontal bus: fuse block right edge → spine
    bus_y = spine_bot
    ax.annotate("", xy=(SP_X, bus_y), xytext=(LX + LW, bus_y),
                arrowprops=dict(arrowstyle="-|>", color=C_CL, lw=3.0), zorder=5)
    wlabel(ax, (LX + LW + SP_X) / 2, bus_y + 0.22,
           "Distribution bus  |  2 AWG", ha="center")

    # Column offsets — spec columns shrunk to give more room to LOCATION / NOTE
    NOTE_OFF = 4.95   # note column starts at CB_X + NOTE_OFF
    col_defs = [
        # (x_start, width, header_text)
        (CB_X,        2.2,             "CIRCUIT / DEVICE"),
        (CB_X + 2.25, 0.70,            "FUSE"),
        (CB_X + 3.05, 0.90,            "WIRE\nGAUGE"),
        (CB_X + 4.05, 0.80,            "MAX\nLOAD"),
        (CB_X + NOTE_OFF, CB_W - NOTE_OFF, "LOCATION / NOTE"),
    ]
    hdr_y = CB_Y_TOP + CB_H + 0.48
    for cx0, cw, htxt in col_defs:
        ax.text(cx0 + cw / 2, hdr_y, htxt,
                ha="center", va="center", fontsize=8.5,
                fontweight="bold", color=C_OUT)
    ax.plot([CB_X, CB_X + CB_W], [hdr_y - 0.24, hdr_y - 0.24],
            color=C_OUT, lw=1.0)

    for i, (letter, name, fuse, wire, load, note, fc_c) in enumerate(circuits):
        cy = CB_Y_TOP - i * CB_GAP
        tap_y = cy + CB_H / 2

        # Tap line from spine to circuit
        ax.plot([SP_X, CB_X - 0.05], [tap_y, tap_y],
                color=C_CL, lw=1.8, zorder=3)

        # Fuse symbol on tap line
        fc_cx = SP_X + 0.33
        ax.add_patch(mpatches.Rectangle(
            (fc_cx - 0.12, tap_y - 0.12), 0.24, 0.24,
            fc=C_WARN, ec=C_OUT, lw=1.0, zorder=5))
        ax.text(fc_cx, tap_y, fuse,
                ha="center", va="center", fontsize=7.0,
                fontweight="bold", color=C_OUT, zorder=6)

        # Circuit letter badge
        ax.add_patch(mpatches.Rectangle((CB_X, cy), 0.60, CB_H,
                     fc=fc_c, ec=C_OUT, lw=1.2, zorder=3))
        ax.text(CB_X + 0.30, tap_y, letter,
                ha="center", va="center", fontsize=13,
                fontweight="bold", color=C_OUT, zorder=4)

        # Device name cell
        ax.add_patch(FancyBboxPatch((CB_X + 0.60, cy), 1.60, CB_H,
                     boxstyle="round,pad=0.02",
                     fc=fc_c, ec=C_OUT, lw=1.0, zorder=3))
        ax.text(CB_X + 0.60 + 0.80, tap_y, name,
                ha="center", va="center", fontsize=8.0,
                fontweight="bold", color=C_OUT, zorder=4)

        # Spec cells: fuse, wire, load
        for xi, cw, txt in [
            (CB_X + 2.25, 0.70, fuse),
            (CB_X + 3.05, 0.90, wire),
            (CB_X + 4.05, 0.80, load),
        ]:
            ax.add_patch(mpatches.Rectangle((xi, cy), cw, CB_H,
                         fc="white", ec=C_OUT, lw=0.8, zorder=3))
            ax.text(xi + cw / 2, tap_y, txt,
                    ha="center", va="center", fontsize=8.0,
                    color=C_OUT, zorder=4)

        # Note cell
        nx = CB_X + NOTE_OFF
        nw = CB_W - NOTE_OFF
        ax.add_patch(mpatches.Rectangle((nx, cy), nw, CB_H,
                     fc="white", ec=C_OUT, lw=0.8, zorder=3))
        wrapped = textwrap.fill(note, width=40)
        ax.text(nx + nw / 2, tap_y, wrapped,
                ha="center", va="center", fontsize=7.2, color=C_DIM,
                linespacing=1.25, zorder=4)

    # ── Title block ──────────────────────────────────────────────────────────
    title_block(ax, "SHEET 1 OF 3",
                drawing_title="SYSTEM ONE-LINE DIAGRAM",
                subtitle="Power flow  ·  Component specifications  ·  Circuit fuse ratings  ·  Wire gauges",
                scale_note="Not to scale",
                doc_id="TBS-ELEC · Electrical & Systems")

    plt.savefig("diagrams/electrical-sheet1.png", dpi=150, bbox_inches="tight",
                pad_inches=0.10, facecolor="white")
    plt.savefig(svg_path("diagrams/electrical-sheet1.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  → electrical-sheet1.png  Done.")


# ─────────────────────────────────────────────────────────────────────────────
# SHEET 2 — Container Floor Plan + Wiring Layout  (scale 1:500)
#
# ORIENTATION:
#   Container long axis (5,898mm) = HORIZONTAL (left–right in plan)
#   Optical depth (2,362mm)       = VERTICAL (bottom–top in plan)
#   LEFT short wall  = X=0   = CARGO DOOR end (hinged panel / light trap)
#   RIGHT short wall = X=5898= FAR END
#   BOTTOM long wall = Y=0   = PINHOLE WALL  (Yd=0)
#   TOP long wall    = Y=2362= IMAGE PLANE WALL
#   Pinhole: on BOTTOM long wall at X=2,946mm (midpoint)
#   Image plane: on TOP long wall
#   NO vestibule shown — light trap is part of hinged-panel drawing
#   All equipment in colonnade strip Yd ≤ 1,220mm (near bottom/pinhole wall)
# ─────────────────────────────────────────────────────────────────────────────

def draw_sheet2():
    from matplotlib.patches import Polygon as MplPolygon
    from tbs_constants import (
        C_LEN as TBS_C_LEN, C_WID as TBS_C_WID, FP_H,
        PH_X as TBS_PH_X, PH_D, PH_FNO,
        FP_X_L, FP_X_R,
        ZONE_L_END, ZONE_R_START,
        EVAP_X, EVAP_W, EVAP_Y, EVAP_D,
        EP_X, EP_W, BA_X, BA_W, PUMP_X, PUMP_W,
        IBC_COL_X, IBC_W, IBC_D,
        BLUE_IBC_Y, BROWN_IBC_Y, IBC_FAR_Y,
        DRUM_CX, DRUM_D, DRUM_R,
        FAN_A_YD, FAN_B_YD,
        DIAGRAMS_DIR, svg_path,
    )

    FW, FH = 24.0, 14.0
    fig, ax = plt.subplots(figsize=(FW, FH), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(0, FW)
    ax.set_ylim(0, FH)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # ── Page title ────────────────────────────────────────────────────────────
    ax.text(FW / 2, FH - 0.38,
            "CONTAINER FLOOR PLAN & WIRING LAYOUT — TBS-001",
            ha="center", va="center", fontsize=13, fontweight="bold",
            color=TITLE_COL)
    ax.text(FW / 2, FH - 0.72,
            "Top-down plan view  ·  Scale 1:500  ·  All dimensions in mm  "
            "·  Pinhole on bottom long wall — optical axis crosses container width (2,362mm)",
            ha="center", va="center", fontsize=8.0, color=C_DIM)

    # ── Scale / geometry constants ────────────────────────────────────────────
    # 1 drawing unit = 500 mm
    S     = 1.0 / 500.0

    # Container placement in figure space
    # LEFT  short wall = X=0    = CARGO DOOR end  (hinged panel, light trap)
    # RIGHT short wall = X=5898 = far end
    # BOTTOM long wall = Y=0    = PINHOLE WALL  (Yd=0, optical origin)
    # TOP   long wall  = Y=2362 = IMAGE PLANE WALL
    OX = 2.5   # drawing x of container left edge (cargo door side)
    OY = 4.5   # drawing y of container bottom edge (pinhole wall)

    C_LEN   = TBS_C_LEN    # 5893 mm container interior length
    C_WID   = TBS_C_WID    # 2362 mm container interior width = optical depth
    WT_MM   = 120           # mm schematic wall thickness

    PH_X_MM = TBS_PH_X     # 2637 mm — centred on active film plane (was 2560, was 2946)

    # Zone boundaries
    ZONE_L  = ZONE_L_END   # 625 mm — left end zone right boundary
    ZONE_R  = ZONE_R_START  # 4,649 mm — right end zone left boundary

    clen   = C_LEN * S     # drawing units (full container length incl. walls)
    cwid   = C_WID * S     # drawing units (full container width incl. walls)
    wt     = WT_MM * S     # drawing units (schematic wall thickness)
    S_yd   = (cwid - 2*wt) / C_WID  # Yd scale: maps yd=0→OY+wt, yd=C_WID→OY+cwid-wt

    # Interior X scale: TBS X (0–C_LEN mm) maps to drawing interior (OX+wt … OX+clen-wt)
    S_xi   = (clen - 2*wt) / C_LEN
    def ix(x_mm):
        """Map TBS interior X (mm) to drawing X coordinate."""
        return OX + wt + x_mm * S_xi

    ph_x     = ix(PH_X_MM)     # pinhole x in drawing coords
    zone_l_x = ix(ZONE_L)      # left zone boundary x
    zone_r_x = ix(ZONE_R)      # right zone boundary x
    fp_l_x   = ix(FP_X_L)      # film plane left edge x
    fp_r_x   = ix(FP_X_R)      # film plane right edge x

    # ── Container shell ───────────────────────────────────────────────────────
    ax.add_patch(mpatches.Rectangle((OX, OY), clen, cwid,
                 fc="#F8F8F4", ec=C_OUT, lw=2.5, zorder=2))
    for rx, ry, rw, rh in [
        (OX,          OY,          clen, wt),          # BOTTOM  — PINHOLE WALL
        (OX,          OY+cwid-wt,  clen, wt),          # TOP     — IMAGE PLANE WALL
        (OX,          OY+wt,       wt,   cwid-2*wt),   # LEFT    — CARGO DOOR end
        (OX+clen-wt,  OY+wt,       wt,   cwid-2*wt),   # RIGHT   — far end
    ]:
        ax.add_patch(mpatches.Rectangle((rx, ry), rw, rh,
                     fc=C_STEEL, ec=C_OUT, lw=0.5, zorder=3))

    # Wall labels on exterior faces
    ax.text(OX - 0.12, OY + cwid/2,
            "CARGO DOOR\n(X=0)",
            fontsize=7.0, color=C_OUT, ha="right", va="center",
            fontweight="bold")
    ax.text(OX + clen + 0.12, OY + cwid/2,
            "FAR END\n(X=5,898mm)",
            fontsize=7.0, color=C_DIM, ha="left", va="center")
    ax.text(OX + clen/2, OY + cwid - wt + 0.82,
            "20FT ISO CONTAINER  —  INTERIOR  (top-down plan)",
            fontsize=8.0, ha="center", va="top", color=C_DIM, style="italic")

    # ── Zone fills (shadow-free end zones + optical zone) ────────────────────
    int_left  = OX + wt   # drawing x of interior left face
    int_right = OX + clen - wt   # drawing x of interior right face
    int_w     = int_right - int_left   # interior drawing width
    ax.add_patch(mpatches.Rectangle(
                 (int_left, OY+wt), zone_l_x - int_left, cwid-2*wt,
                 fc="#FFF0E0", ec="none", alpha=0.55, zorder=4))   # left end zone
    ax.add_patch(mpatches.Rectangle(
                 (zone_l_x, OY+wt), zone_r_x - zone_l_x, cwid-2*wt,
                 fc="#F0FFF0", ec="none", alpha=0.45, zorder=4))   # optical zone
    ax.add_patch(mpatches.Rectangle(
                 (zone_r_x, OY+wt), int_right - zone_r_x, cwid-2*wt,
                 fc="#E8F0FF", ec="none", alpha=0.55, zorder=4))   # right end zone

    # Zone boundary lines
    for zx, zlabel in [(zone_l_x, f"X={ZONE_L}mm"), (zone_r_x, f"X={ZONE_R}mm")]:
        ax.plot([zx, zx], [OY+wt, OY+cwid-wt], color=C_DIM, lw=1.2, ls="--",
                zorder=7)
        ax.text(zx, OY+cwid-wt+0.08, zlabel, ha="center", va="bottom",
                fontsize=6.5, color=C_DIM)

    ax.text((int_left + zone_l_x)/2, OY + cwid - wt + 0.52,
            "LEFT\nEND ZONE", ha="center", va="top", fontsize=7.0,
            color="#805000", fontweight="bold", zorder=5)
    ax.text((zone_l_x + zone_r_x)/2, OY + cwid - wt + 0.52,
            "OPTICAL ZONE\n(film plane only)", ha="center", va="top", fontsize=7.0,
            color="#006000", fontweight="bold", zorder=5)
    ax.text((zone_r_x + int_right)/2, OY + cwid - wt + 0.52,
            "RIGHT\nEND ZONE", ha="center", va="top", fontsize=7.0,
            color="#004080", fontweight="bold", zorder=5)

    # ── Optical cone — pinhole to new film plane edges ────────────────────────
    cone_verts = [
        (ph_x,    OY + wt),          # pinhole on bottom long wall
        (fp_l_x,  OY + cwid - wt),   # film plane left edge
        (fp_r_x,  OY + cwid - wt),   # film plane right edge
    ]
    ax.add_patch(MplPolygon(cone_verts, closed=True,
                fc="#FFE8C0", ec="none", alpha=0.40, zorder=5))
    ax.text(ph_x, OY + cwid * 0.60,
            "OPTICAL CONE — keep clear",
            ha="center", va="center", fontsize=8.0,
            color="#8B5A00", style="italic", alpha=0.85, zorder=6)

    # ── Image plane strip — new width X=1100–4649mm ───────────────────────────
    ax.add_patch(mpatches.Rectangle(
                 (fp_l_x, OY+cwid-wt-0.15), fp_r_x - fp_l_x, 0.15,
                 fc="#A8C8E8", ec=C_CL, lw=1.5, zorder=6))
    ax.text((fp_l_x+fp_r_x)/2, OY + cwid - wt - 0.075,
            f"FILM PLANE  X={FP_X_L}–{FP_X_R}mm  ({FP_X_R-FP_X_L}mm wide × {FP_H}mm H)",
            ha="center", va="center", fontsize=7.5, color=TITLE_COL,
            fontweight="bold", zorder=7)

    # ── Pinhole — bottom long wall at X=2,874mm (recentred on new film plane) ─
    ax.add_patch(plt.Circle((ph_x, OY + wt/2), 0.12,
                 fc="black", ec=C_OUT, lw=1.0, zorder=8))
    leader(ax, ph_x, OY + wt/2, ph_x * 1.1, OY - 0.50,
           f"PINHOLE  Ø{PH_D}mm\nX={TBS_PH_X}mm  f/{PH_FNO}",
           fs=7.5, ha="center")

    # ── NEMA inlet — positioned after EP is drawn (see below) ───────────────

    # ── Colonnade equipment ───────────────────────────────────────────────────
    # x_mm  = TBS X along long axis (0 = cargo door end = LEFT in plan)
    #          TBS coords run 0–5,893mm interior-to-interior.
    #          Map to drawing interior: ex = OX + wt + x_mm * S_x.
    # yd_mm = depth from pinhole wall (0 = pinhole wall = BOTTOM in plan)
    def equip(x_mm, yd_mm, w_mm, d_mm, label, col, sublabel=""):
        ex = ix(x_mm)                  # TBS X=0 maps to interior face of left wall
        ey = OY + wt + yd_mm * S_yd   # depth from interior face of pinhole wall
        ew = w_mm * S_xi
        ed = d_mm * S_yd
        ax.add_patch(mpatches.Rectangle((ex, ey), ew, ed,
                     fc=col, ec=C_OUT, lw=1.0, zorder=5, alpha=0.88))
        cy_e = ey + ed / 2
        ax.text(ex+ew/2, cy_e + (0.10 if sublabel else 0), label,
                ha="center", va="center", fontsize=6.5, fontweight="bold",
                color=C_OUT, zorder=6)
        if sublabel:
            ax.text(ex+ew/2, cy_e - 0.12, sublabel,
                    ha="center", va="center", fontsize=5.5, color=C_DIM, zorder=6)

    # LEFT END ZONE (X=0–625mm) — light trap drum only (waste drums eliminated rev 5)
    # Drum centred at X=0 (spans cargo door wall); only draw interior half X=0–DRUM_R
    from tbs_constants import C_LT_DRUM
    equip(0, C_WID//2 - DRUM_R, DRUM_R, DRUM_D, "LT DRUM\n(partial)", C_LT_DRUM,
          f"Ø{DRUM_D}mm vertical axis  Yd={C_WID//2 - DRUM_R}–{C_WID//2 + DRUM_R}mm")

    # ── Ghost: hinged panel + drum in TRANSPORT position ────────────────────
    # Panel retracted 300mm inward (X=300–380 corner / 300–420 center)
    # Drum center at X=300, Yd centered at C_WID/2
    from tbs_constants import (
        PANEL_SLIDE, PANEL_CORNER_T, PANEL_CENTER_T,
        PANEL_CORNER_YD_L, PANEL_CORNER_YD_R,
    )
    GHOST_ALPHA = 0.18
    GHOST_EC = "#808080"
    GHOST_LS = (0, (4, 3))   # dashed

    # Panel — stepped profile: corners thinner, center thicker
    # Near corner: Yd=0 to PANEL_CORNER_YD_L, thickness=PANEL_CORNER_T
    for (yd_lo, yd_hi, thick) in [
        (0, PANEL_CORNER_YD_L, PANEL_CORNER_T),
        (PANEL_CORNER_YD_L, PANEL_CORNER_YD_R, PANEL_CENTER_T),
        (PANEL_CORNER_YD_R, C_WID, PANEL_CORNER_T),
    ]:
        gp_x = ix(PANEL_SLIDE)
        gp_w = thick * S_xi
        gp_y = OY + wt + yd_lo * S_yd
        gp_h = (yd_hi - yd_lo) * S_yd
        ax.add_patch(mpatches.Rectangle((gp_x, gp_y), gp_w, gp_h,
                     fc="#B0A090", ec=GHOST_EC, lw=1.0, ls=GHOST_LS,
                     alpha=GHOST_ALPHA, zorder=4))

    # Drum — circle at X=PANEL_SLIDE (center moves with panel)
    gd_cx = ix(PANEL_SLIDE)   # drum center X in transport
    gd_cy = OY + wt + (C_WID / 2) * S_yd
    gd_r = DRUM_R * S_xi
    ax.add_patch(plt.Circle((gd_cx, gd_cy), gd_r,
                 fc=C_LT_DRUM, ec=GHOST_EC, lw=1.0, ls=GHOST_LS,
                 alpha=GHOST_ALPHA, zorder=4))

    # Label
    ax.text(ix(PANEL_SLIDE + PANEL_CENTER_T + 30),
            OY + wt + C_WID * 0.08 * S_yd,
            "Panel + drum\n(transport position)",
            ha="left", va="bottom", fontsize=6.0, color="#808080",
            style="italic", zorder=5)

    # PINHOLE WALL FACE (Yd=0) — evap cooler (rev 3) + pump manifold
    equip(EVAP_X, EVAP_Y, EVAP_W, EVAP_D, "EVAP\nCOOLER", C_EVAP, "80W 12V  (E)")
    equip(PUMP_X, 0, PUMP_W, 80, "", C_PUMP, "")

    # RIGHT END ZONE — 4× IBC in 2×2 stack
    # Near column (Yd=100–1116): Blue #1 on top, Brown on bottom
    equip(IBC_COL_X, BLUE_IBC_Y, IBC_W, IBC_D, "IBC-1 BLUE\n+ IBC-3 BROWN",
          C_BLUE_IBC, "Near column  Yd=100–1116")
    # Far column (Yd=1141–2157): Blue #2 on top, Waste on bottom
    equip(IBC_COL_X, IBC_FAR_Y, IBC_W, IBC_D, "IBC-2 BLUE\n+ IBC-4 WASTE",
          C_WASTE_IBC, "Far column  Yd=1141–2157")

    # ── EP + BAT wall-mounted on interior face of pinhole wall (Yd=0) ────────
    WALL_MOUNT_H = wt * 0.55   # shallow depth for wall-mounted box
    EP_DX = ix(EP_X)
    EP_DW = EP_W * S_xi
    ax.add_patch(mpatches.Rectangle((EP_DX, OY + wt), EP_DW, WALL_MOUNT_H,
                 fc=C_ELEC, ec=C_OUT, lw=1.0, zorder=7))
    ax.text(EP_DX+EP_DW/2, OY + wt + WALL_MOUNT_H/2, "EP",
            ha="center", va="center", fontsize=6.5, fontweight="bold", color=C_OUT)

    BA_DX = ix(BA_X)
    BA_DW = BA_W * S_xi
    ax.add_patch(mpatches.Rectangle((BA_DX, OY + wt), BA_DW, WALL_MOUNT_H,
                 fc=C_BATT, ec=C_OUT, lw=1.0, zorder=7))
    ax.text(BA_DX+BA_DW/2, OY + wt + WALL_MOUNT_H/2, "BAT",
            ha="center", va="center", fontsize=6.5, fontweight="bold", color=C_OUT)

    # ── External power panel — flush-mount in pinhole wall ──────────────────
    from tbs_constants import PWR_PANEL_X, PWR_PANEL_W
    PP_DX = ix(PWR_PANEL_X)
    PP_DW = PWR_PANEL_W * S_xi
    PP_DH = wt                             # flush in the wall thickness
    PP_DY = OY                             # sits in the wall itself
    ax.add_patch(mpatches.Rectangle((PP_DX, PP_DY), PP_DW, PP_DH,
                 fc=C_ALUM, ec=C_OUT, lw=1.2, zorder=7))
    ax.text(PP_DX + PP_DW / 2, PP_DY + PP_DH / 2, "EXT\nPWR",
            ha="center", va="center", fontsize=6.5,
            fontweight="bold", color=C_OUT, zorder=8)
    # Cable routing from panel to EP (interior)
    ax.plot([PP_DX + PP_DW / 2, PP_DX + PP_DW / 2],
            [PP_DY + PP_DH, OY + wt + WALL_MOUNT_H],
            color="#808080", lw=1.2, ls=":", zorder=4)

    # ── Fans ──────────────────────────────────────────────────────────────────
    # Fan A — INTAKE: RIGHT short wall = far end (X=C_LEN), Yd=75mm near-wall corner
    FA_X = OX + clen - wt/2
    FA_Y = OY + wt + FAN_A_YD * S_yd
    ax.add_patch(plt.Circle((FA_X, FA_Y), 0.22,
                 fc=C_ALUM, ec=C_OUT, lw=1.2, zorder=5))
    ax.text(FA_X, FA_Y, "A",
            ha="center", va="center", fontsize=9, fontweight="bold",
            color=C_OUT, zorder=6)

    # Fan B — EXHAUST: LEFT short wall = cargo door end (X=0), Yd=2287mm far-wall corner
    FB_X = OX + wt/2
    FB_Y = OY + wt + FAN_B_YD * S_yd
    ax.add_patch(plt.Circle((FB_X, FB_Y), 0.22,
                 fc=C_ALUM, ec=C_OUT, lw=1.2, zorder=5))
    ax.text(FB_X, FB_Y, "B",
            ha="center", va="center", fontsize=9, fontweight="bold",
            color=C_OUT, zorder=6)

    # Safelight D — three ceiling-mounted N–S strips
    # Positioned in gaps between white LED panels to avoid visual overlap
    # Each shortened to stay clear of optical cone at its X position
    SL_STRIPS = [
        (600,  1800),   # near cargo door — cone limit at Yd≈1,889, stop at 1,800
        (1800, 2100),   # between white panels 1 & 2 — cone limit at Yd≈2,174, stop at 2,100
        (4100, 2100),   # between white panels 2 & 3 — cone limit at Yd≈2,730, stop at 2,100
    ]
    SL_STRIP_W = 20    # strip width along X (mm)
    SL_POSITIONS = [s[0] for s in SL_STRIPS]   # for component key reference
    for sl_x_mm, sl_yd_max in SL_STRIPS:
        sl_dx = ix(sl_x_mm)
        sl_dw = max(SL_STRIP_W * S_xi, 0.08)
        sl_dy1 = OY + wt + 0.05
        sl_dy2 = OY + wt + sl_yd_max * S_yd
        ax.add_patch(mpatches.Rectangle((sl_dx, sl_dy1), sl_dw, sl_dy2 - sl_dy1,
                     fc="#FFD700", ec=C_OUT, lw=0.8, zorder=5))
        ax.text(sl_dx + sl_dw + 0.06, (sl_dy1 + sl_dy2) / 2, "D",
                ha="left", va="center", fontsize=6.5, fontweight="bold", color=C_OUT)

    # ── White LED panels (Circuit G) — 3× ceiling-mounted ───────────────────
    LED_W_MM = 600    # panel width along X
    LED_D_MM = 300    # panel depth along Yd
    LED_YD   = C_WID / 2 - LED_D_MM / 2   # centered across width
    LED_POSITIONS = [1000, 2900, 4800]     # X positions (mm)
    C_LED = "#FFFFF0"
    for lp_x in LED_POSITIONS:
        lx = ix(lp_x)
        ly = OY + wt + LED_YD * S_yd
        lw = LED_W_MM * S_xi
        ld = LED_D_MM * S_yd
        ax.add_patch(mpatches.Rectangle((lx, ly), lw, ld,
                     fc=C_LED, ec=C_OUT, lw=0.8, zorder=5, alpha=0.85))
        ax.text(lx + lw / 2, ly + ld / 2, "G",
                ha="center", va="center", fontsize=7.0, fontweight="bold",
                color=C_OUT, zorder=6)

    # ── Pull-cord switches — pinhole wall side, near EP ─────────────────────
    PS_X_MM = 1800   # X position (mm) — near electrical panel
    PS_YD   = 50     # just off pinhole wall
    PS_SZ   = 0.16   # symbol size in drawing units
    C_SWITCH = "#E0E0FF"
    for si, (sw_label, sw_x_off) in enumerate([("D", -40), ("G", 40)]):
        sx = ix(PS_X_MM + sw_x_off)
        sy = OY + wt + PS_YD * S_yd
        ax.add_patch(mpatches.Circle((sx, sy), PS_SZ,
                     fc=C_SWITCH, ec=C_OUT, lw=1.0, zorder=7))
        ax.text(sx, sy, sw_label,
                ha="center", va="center", fontsize=6.0, fontweight="bold",
                color=C_OUT, zorder=8)
    # Pull switch leader
    ps_mid_x = ix(PS_X_MM)
    leader(ax, ps_mid_x, OY + wt + PS_YD * S_yd,
           ps_mid_x - 0.6, OY + cwid * 0.18,
           "Pull-cord switches\nD=safelight  G=white",
           fs=6.5, color="#606080")

    # ── Cable trunking — pinhole wall face, full interior length ──────────────
    # Runs at Yd=0 on pinhole wall — physically on the wall, outside optical cone
    TK_Y  = OY + wt + 0.07
    TK_X1 = OX + wt + 0.05
    TK_X2 = OX + clen - wt - 0.05
    ax.plot([TK_X1, TK_X2], [TK_Y, TK_Y],
            color=C_PIPE, lw=4.5, solid_capstyle="round", zorder=6)
    ax.text((TK_X1+TK_X2)/2 + 1.65, TK_Y + 0.24,
            "40×25mm PVC cable trunking — pinhole wall face (Yd=0)\noutside optical cone",
            ha="center", va="top", fontsize=7.0, color=C_PIPE, fontweight="bold")

    # Drop conduits from trunking to devices
    EVAP_CX = ix(EVAP_X + EVAP_W/2)
    PUMP_CX = ix(PUMP_X + PUMP_W/2)
    IBC_CX  = ix(IBC_COL_X + IBC_W/2)
    for ddx, ddy in [
        (BA_DX + BA_DW/2,    OY + wt),
        (EP_DX + EP_DW/2,    OY + wt),
        (EVAP_CX,            OY+wt + EVAP_Y*S_yd),           # evap cooler (Yd=0, pinhole wall)
        (PUMP_CX,            OY+wt + 80*S_yd),               # pump manifold
        (IBC_CX,             OY+wt + BLUE_IBC_Y*S_yd),      # IBC column centre
        (FA_X,               FA_Y - 0.22),
        (FB_X,               FB_Y - 0.22),
    ] + [(ix(sl_x + SL_STRIP_W / 2), OY + wt + 0.05) for sl_x in SL_POSITIONS] + [
        (ix(PS_X_MM),        OY + wt + PS_YD * S_yd),   # pull switches
    ] + [(ix(lp + LED_W_MM/2), OY + wt + LED_YD * S_yd) for lp in LED_POSITIONS]:
        ax.plot([ddx, ddx], [TK_Y, ddy],
                color=C_PIPE, lw=1.0, ls=":", zorder=4)

    # ── Component leaders — label every key item on the diagram ────────────────
    # EP — Electrical panel
    leader(ax, EP_DX + EP_DW/2, OY + wt + WALL_MOUNT_H,
           EP_DX + EP_DW/2, OY + cwid * 0.42,
           "Electrical panel (EP)\nMPPT + fuse block\nPinhole wall face",
           fs=6.5, color=C_ELEC)
    # BAT — Battery bank
    leader(ax, BA_DX + BA_DW/2, OY + wt + WALL_MOUNT_H,
           BA_DX + BA_DW/2, OY + cwid * 0.3,
           "Battery bank (BAT)\n2×100Ah LiFePO4",
           fs=6.5, color=C_BATT)
    # Fan A — Intake (far end wall)
    leader(ax, FA_X + 0.1, FA_Y + 0.1,
           FA_X + 1.2, FA_Y + 0.5,
           "Intake fan (A)\n6\" DC  60W",
           fs=6.5, ha="right")
    # Fan B — Exhaust (cargo door wall)
    leader(ax, FB_X - 0.1 , FB_Y + 0.1,
           FB_X - 1.2, FB_Y + 0.7,
           "Exhaust fan (B)\n6\" DC  60W",
           fs=6.5)
    # Pump — Cct C
    leader(ax, PUMP_CX, OY + wt + 80 * S_yd,
           PUMP_CX + 0.8, OY + cwid * 0.3,
           "Water pump (C)\n12V DC  100W",
           fs=6.5, color=C_PUMP)
    # Safelight — Cct D (label middle strip)
    sl_ldr_x = ix(SL_POSITIONS[1] + SL_STRIP_W / 2)
    sl_ldr_y = OY + cwid * 0.5
    leader(ax, sl_ldr_x, sl_ldr_y,
           sl_ldr_x - 0.8, OY + cwid * 0.22,
           "Safelight (D)\n3× red LED strips\nceiling, N–S",
           fs=6.5, color="#B8960A")
    # Evap cooler — Cct E
    leader(ax, EVAP_CX, OY + wt + (EVAP_Y + EVAP_D) * S_yd,
           EVAP_CX, OY + cwid * 0.3,
           "Evap cooler (E)\n12V DC  80W",
           fs=6.5, color=C_EVAP)
    # LED panels — Cct G (label middle panel only)
    led_mid_cx = ix(LED_POSITIONS[1] + LED_W_MM / 2)
    led_mid_cy = OY + wt + (LED_YD + LED_D_MM) * S_yd
    leader(ax, led_mid_cx, led_mid_cy,
           led_mid_cx + 0.8, OY + cwid * 0.62,
           "LED panels (G)\n3×20W  4000K white",
           fs=6.5, color="#808000")
    # External power panel
    leader(ax, PP_DX + PP_DW * 4/5, PP_DY + (PP_DH * 0.5),
           PP_DX + PP_DW * 2, PP_DY - 0.5,
           "External power panel\n3×MC4 + NEMA 5-15R\nSingle sealed penetration",
           fs=6.5, color="#806030", ha="center")

    # ── Solar panels — exterior (below container in plan) ─────────────────────
    SP_X2 = OX + clen * 0.25
    SP_Y2 = OY - 1.45
    SP_W2 = clen * 0.50
    SP_H2 = 0.60
    ax.add_patch(FancyBboxPatch((SP_X2, SP_Y2), SP_W2, SP_H2,
                 boxstyle="round,pad=0.04", fc=C_SOLAR, ec=C_OUT, lw=1.8, zorder=3))
    ax.text(SP_X2+SP_W2/2, SP_Y2+SP_H2/2,
            "SOLAR PANELS  (3×200W)  —  EXTERIOR, SOUTH-FACING",
            ha="center", va="center", fontsize=8.5, fontweight="bold",
            color=C_OUT, zorder=4)
    ax.annotate("", xy=(PP_DX + PP_DW / 2, PP_DY + PP_DH),
                xytext=(SP_X2, SP_Y2+SP_H2),
                arrowprops=dict(arrowstyle="-|>", color="#2D7A2D", lw=1.8,
                                connectionstyle="arc3,rad=-0.15"), zorder=4)
    ax.text(SP_X2 - 0.2, (SP_Y2+SP_H2 + PP_DY)/2,
            "PV cable  10 AWG / MC4\nvia ext. power panel",
            fontsize=7.0, color="#2D7A2D", ha="right", va="center")

    # ── Dimension lines ───────────────────────────────────────────────────────
    DIM_Y = OY - 0.82
    DIM_X = OX - 0.42

    draw_dim_h(ax, OX, OX+clen, DIM_Y-1.5, f"{C_LEN} mm  (container interior length)",
               above=False, offset=0.08, fs=7.5)
    draw_dim_h(ax, fp_l_x, fp_r_x, DIM_Y - 1.10,
               f"Film plane  {FP_X_R-FP_X_L}mm",
               above=False, offset=0.08, fs=7.5)
    draw_dim_v(ax, DIM_X-0.5, OY, OY+cwid,  f"{C_WID} mm  (optical depth / interior width)",
               offset=0.08, fs=7.5)

    # ── Component key (right of container) ───────────────────────────────────
    KX = OX + clen + 0.70 + FW * 0.10
    KY = OY + cwid - 0.05
    ax.text(KX, KY + 0.28, "COMPONENT KEY",
            ha="left", va="center", fontsize=9.5, fontweight="bold", color=C_OUT)
    ax.plot([KX, KX + 5.8], [KY + 0.05, KY + 0.05], color=C_OUT, lw=1.0)

    key_rows = [
        ("EP",    C_ELEC,    "ELECTRICAL PANEL (EP)",
         "IP65 enclosure  |  MPPT + fuse block  |  Pinhole wall face, X=2,050mm"),
        ("BAT",   C_BATT,    "BATTERY BANK (BAT)",
         "2×100Ah LiFePO4 12V  |  2,400Wh  |  Pinhole wall face, X=100mm"),
        ("A",     C_ALUM,    "INTAKE FAN — Cct A",
         "6\" inline DC  |  5A / 16 AWG / 60W  |  Far end wall (X=5,893mm)  |  Yd=75mm"),
        ("B",     C_ALUM,    "EXHAUST FAN — Cct B",
         "6\" inline DC  |  5A / 16 AWG / 60W  |  Cargo door end wall (X=0)  |  Yd=2,287mm"),
        ("C",     C_PUMP,    "WATER PUMP — Cct C",
         "12V DC  |  15A / 14 AWG / 100W  |  Pinhole wall face, X=2,600mm"),
        ("D",     "#FFD700", "SAFELIGHT — Cct D",
         f"3× red LED strips  |  5A / 18 AWG / 15W  |  Ceiling N–S at X≈{', '.join(str(x) for x in SL_POSITIONS)}"),
        ("E",     C_EVAP,    "EVAP COOLER — Cct E",
         f"12V DC 80W  |  10A / 14 AWG  |  Pinhole wall face (Yd=0), X={EVAP_X}–{EVAP_X+EVAP_W}mm"),
        ("G",     C_LED,     "WHITE LED PANELS — Cct G",
         "3×20W ceiling panels  |  10A / 16 AWG / 60W  |  Pull-cord switch, non-operational only"),
        ("D/G",   C_SWITCH,  "PULL-CORD SWITCHES",
         "SPST 6A ceiling switches  |  D=safelight, G=white light  |  Pinhole wall, X≈1,800mm"),
        ("EXT\nPWR",C_ALUM,"EXTERNAL POWER PANEL",
         "3×MC4 solar + NEMA 5-15R AC  |  Flush-mount in wall cutout  |  Pinhole wall"),
    ]
    for j, (badge, bc, title_k, spec) in enumerate(key_rows):
        ky = KY - 0.28 - j * 0.60
        ax.add_patch(mpatches.Rectangle((KX, ky-0.20), 0.50, 0.44,
                     fc=bc, ec=C_OUT, lw=0.9, zorder=4))
        ax.text(KX+0.25, ky+0.01, badge,
                ha="center", va="center", fontsize=8.0,
                fontweight="bold", color=C_OUT, zorder=5)
        ax.text(KX+0.65, ky+0.04, title_k,
                ha="left", va="center", fontsize=8.5,
                fontweight="bold", color=C_OUT)
        ax.text(KX+0.65, ky-0.12, spec,
                ha="left", va="center", fontsize=7.5, color=C_DIM)

    # ── Drawing notes — stacked vertically, right-aligned under component key ─
    import textwrap
    NOTE_W = 6.2     # box width (drawing units)
    NX = KX          # align left edge with component key
    NY = 0.30
    notes = [
        f"1. Pinhole at X={TBS_PH_X}mm on bottom long wall (recentred on new film plane). "
        f"Film plane X={FP_X_L}\u2013{FP_X_R}mm ({FP_X_R-FP_X_L}mm wide) at Yd=2,262mm. f/1088.",
        f"2. Shadow-free end zones: Left X=0\u2013{FP_X_L}mm (light trap + 55-gal drums \u00d72), "
        f"Right X={FP_X_R}\u20135,893mm (IBCs only). Evap cooler on pinhole wall (Yd=0, "
        f"X={EVAP_X}\u2013{EVAP_X+EVAP_W}mm). Amber cone \u2014 keep entirely clear.",
        "3. Cable trunking (40\u00d725mm PVC) on pinhole wall face (Yd=0) \u2014 outside "
        "optical cone. Drop conduits (10mm corrugated) to each device.",
        "4. Light trap (revolving drum, \u00d8750mm vertical axis) in left end zone \u2014 "
        "integral to cargo-door hinged panel. See Hinged Panel drawings (\u00a712).",
        "5. Circuit G (white LED panels) and Circuit D (safelight) are independently switched "
        "via pull-cord ceiling switches on the pinhole wall. White light must be off during operation.",
    ]
    # Wrap each note and measure total height
    WRAP_CHARS = 120
    NOTE_FS = 6.5
    LINE_SP = 0.20
    NOTE_PAD = 0.12
    wrapped_lines = []
    for note in notes:
        lines = textwrap.wrap(note, width=WRAP_CHARS)
        wrapped_lines.append(lines)
    total_lines = sum(len(ls) for ls in wrapped_lines) + len(notes) - 1  # +gaps between notes
    box_h = 0.35 + total_lines * LINE_SP + 2 * NOTE_PAD

    ax.add_patch(FancyBboxPatch((NX - 0.10, NY - NOTE_PAD), NOTE_W, box_h,
                 boxstyle="round,pad=0.04", fc="#F8F9FA", ec=C_DIM, lw=0.8, zorder=2))
    ax.text(NX + 0.05, NY + box_h - NOTE_PAD - 0.15, "DRAWING NOTES:",
            ha="left", va="center", fontsize=7.5,
            fontweight="bold", color=C_OUT)
    cy = NY + box_h - NOTE_PAD - 0.40
    for ni, lines in enumerate(wrapped_lines):
        for line in lines:
            ax.text(NX + 0.05, cy, line,
                    ha="left", va="center", fontsize=NOTE_FS, color=C_DIM)
            cy -= LINE_SP
        if ni < len(wrapped_lines) - 1:
            cy -= LINE_SP * 0.4  # small gap between notes

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 2 OF 3",
                drawing_title="CONTAINER FLOOR PLAN & WIRING LAYOUT",
                subtitle="Top-down plan  ·  End-zone layout  ·  Optical cone clear",
                scale_note="1:500  (1 drawing unit = 500 mm)",
                doc_id="TBS-ELEC · Electrical & Systems")

    plt.savefig(f"{DIAGRAMS_DIR}/electrical-sheet2.png", dpi=150, bbox_inches="tight",
                pad_inches=0.10, facecolor="white")
    plt.savefig(svg_path(f"{DIAGRAMS_DIR}/electrical-sheet2.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  → electrical-sheet2.png  Done.")



# ─────────────────────────────────────────────────────────────────────────────
# SHEET 3 — Pinhole Wall Interior Elevation
#
# ORIENTATION:
#   Viewer stands inside container looking toward the pinhole wall (Yd=0).
#   Horizontal axis = container X mirrored (0=cargo door RIGHT, 5893=far end LEFT).
#   Vertical axis = Z (0=floor, 2388=ceiling).
#   Equipment mounted on the wall face is drawn at actual X and Z positions.
# ─────────────────────────────────────────────────────────────────────────────

def draw_sheet3():
    from tbs_constants import (
        C_LEN as TBS_C_LEN, C_HGT as TBS_C_HGT,
        PH_X as TBS_PH_X, PH_H, PH_D,
        EP_X, EP_W, EP_H_LO, EP_H_HI,
        BA_X, BA_W, BA_H_LO, BA_H_HI,
        PUMP_X, PUMP_W, PUMP_H_LO, PUMP_H_HI,
        EVAP_X, EVAP_W, EVAP_H,
        PWR_PANEL_X, PWR_PANEL_W, PWR_PANEL_H,
        DIAGRAMS_DIR, svg_path, C_LT_DRUM,
    )

    FW, FH = 24.0, 9.9
    fig, ax = plt.subplots(figsize=(FW, FH), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(0, FW)
    ax.set_ylim(0, FH)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # ── Scale ─────────────────────────────────────────────────────────────────
    S = 1.0 / 400.0   # 1 drawing unit = 400mm (approx 1:40 at 150dpi)

    # Wall placement in figure space
    OX = 2.0    # drawing x of wall left edge
    OY = 1.5    # drawing y of wall bottom edge (Z=0, floor)

    C_LEN = TBS_C_LEN   # 5893mm
    C_HGT = TBS_C_HGT   # 2388mm

    wlen = C_LEN * S     # wall width in drawing units
    whgt = C_HGT * S     # wall height in drawing units

    def wx(x_mm):
        """Map TBS X (mm) to drawing X coordinate (mirrored: interior view)."""
        return OX + (C_LEN - x_mm) * S

    def wz(z_mm):
        """Map TBS Z (mm) to drawing Y coordinate."""
        return OY + z_mm * S

    # ── Page title (positioned above top dimension lines) ───────────────────
    TITLE_Y = OY + whgt + 1.30
    ax.text(FW / 2, TITLE_Y,
            "PINHOLE WALL INTERIOR ELEVATION — TBS-001",
            ha="center", va="center", fontsize=13, fontweight="bold",
            color=TITLE_COL)
    ax.text(FW / 2, TITLE_Y - 0.34,
            "View looking toward pinhole wall (Yd=0) from inside  ·  Scale 1:40  "
            "·  All dimensions in mm",
            ha="center", va="center", fontsize=8.0, color=C_DIM)

    # ── Wall rectangle ────────────────────────────────────────────────────────
    ax.add_patch(mpatches.Rectangle((OX, OY), wlen, whgt,
                 fc="#F8F8F4", ec=C_OUT, lw=2.5, zorder=2))

    # Floor line
    ax.plot([OX - 0.3, OX + wlen + 0.3], [OY, OY],
            color=C_OUT, lw=3.0, zorder=3)
    ax.text(OX + wlen / 2, OY - 0.20, "FLOOR (Z=0)",
            ha="center", va="top", fontsize=7.5, color=C_DIM)

    # Ceiling line
    ax.plot([OX - 0.3, OX + wlen + 0.3], [OY + whgt, OY + whgt],
            color=C_OUT, lw=3.0, zorder=3)
    ax.text(OX + wlen / 2, OY + whgt + 0.12, "CEILING (Z=2,388mm)",
            ha="center", va="bottom", fontsize=7.5, color=C_DIM)

    # Wall labels
    ax.text(OX - 0.15, OY + whgt / 2, "FAR\nEND\n(X=5,893)",
            ha="right", va="center", fontsize=7.0, color=C_DIM)
    ax.text(OX + wlen + 0.15, OY + whgt / 2, "CARGO\nDOOR\nEND\n(X=0)",
            ha="left", va="center", fontsize=7.0, color=C_OUT,
            fontweight="bold")

    # ── Cable trunking — horizontal at ceiling corner ─────────────────────────
    TK_H_MM = 25    # trunking height (mm)
    TK_W_MM = 40    # trunking depth (mm) — shown as height on elevation
    TK_Z = C_HGT - TK_H_MM   # bottom of trunking (Z=2363mm)
    tk_y = wz(TK_Z)
    tk_h = TK_H_MM * S
    ax.add_patch(mpatches.Rectangle((OX + 0.02, tk_y), wlen - 0.04, tk_h,
                 fc=C_PIPE, ec=C_OUT, lw=1.2, zorder=6, alpha=0.85))
    ax.text(OX + wlen / 2, tk_y + tk_h / 2,
            "40×25mm PVC CABLE TRUNKING — FULL LENGTH",
            ha="center", va="center", fontsize=7.0, fontweight="bold",
            color="white", zorder=7)

    # ── Helper: wall-mount equipment box ──────────────────────────────────────
    def wall_equip(x_mm, z_lo, z_hi, w_mm, label, sublabel, fc, badge=""):
        ex = wx(x_mm + w_mm)   # mirrored: right edge of component maps to left in drawing
        ey = wz(z_lo)
        ew = w_mm * S
        eh = (z_hi - z_lo) * S
        ax.add_patch(mpatches.Rectangle((ex, ey), ew, eh,
                     fc=fc, ec=C_OUT, lw=1.2, zorder=5, alpha=0.88))
        cx = ex + ew / 2
        cy = ey + eh / 2
        ax.text(cx, cy + 0.08, label,
                ha="center", va="center", fontsize=7.5, fontweight="bold",
                color=C_OUT, zorder=6)
        if sublabel:
            ax.text(cx, cy - 0.10, sublabel,
                    ha="center", va="center", fontsize=6.0, color=C_DIM, zorder=6)
        # Drop conduit from trunking
        ax.plot([cx, cx], [tk_y, ey + eh],
                color=C_PIPE, lw=1.2, ls=":", zorder=4)
        return ex, ey, ew, eh

    # ── External power panel (flush in wall) ──────────────────────────────────
    # Centered vertically at ~EP mounting height
    PP_Z_LO = EP_H_LO   # align with bottom of EP
    PP_Z_HI = PP_Z_LO + PWR_PANEL_H
    pp_x = wx(PWR_PANEL_X + PWR_PANEL_W)   # mirrored
    pp_y = wz(PP_Z_LO)
    pp_w = PWR_PANEL_W * S
    pp_h = PWR_PANEL_H * S
    ax.add_patch(mpatches.Rectangle((pp_x, pp_y), pp_w, pp_h,
                 fc=C_ALUM, ec=C_OUT, lw=1.5, zorder=5))
    ax.text(pp_x + pp_w / 2, pp_y + pp_h / 2 + 0.06,
            "EXT POWER\nPANEL", ha="center", va="center",
            fontsize=6.5, fontweight="bold", color=C_OUT, zorder=6)
    ax.text(pp_x + pp_w / 2, pp_y + pp_h / 2 - 0.14,
            "3×MC4 + NEMA", ha="center", va="center",
            fontsize=5.5, color=C_DIM, zorder=6)
    # Cable route from panel up to trunking
    ax.plot([pp_x + pp_w / 2, pp_x + pp_w / 2], [pp_y + pp_h, tk_y],
            color=C_PIPE, lw=1.2, ls=":", zorder=4)

    # ── Evaporative cooler (floor-standing) ───────────────────────────────────
    wall_equip(EVAP_X, 0, EVAP_H, EVAP_W,
               "EVAPORATIVE\nCOOLER", "Circuit E  80W", C_EVAP)

    # ── Electrical panel (wall-mounted) ───────────────────────────────────────
    wall_equip(EP_X, EP_H_LO, EP_H_HI, EP_W,
               "ELECTRICAL\nPANEL (EP)", "MPPT + fuse block", C_ELEC)

    # ── Battery bank (wall-mounted) ───────────────────────────────────────────
    wall_equip(BA_X, BA_H_LO, BA_H_HI, BA_W,
               "BATTERY BANK", "2×100Ah LiFePO4", C_BATT)

    # ── Pump manifold (wall-mounted) ──────────────────────────────────────────
    wall_equip(PUMP_X, PUMP_H_LO, PUMP_H_HI, PUMP_W,
               "PUMP\nMANIFOLD", "Circuit C  100W", "#F5C8A0")

    # ── Pinhole ───────────────────────────────────────────────────────────────
    ph_x = wx(TBS_PH_X)
    ph_z = wz(PH_H)
    ax.add_patch(plt.Circle((ph_x, ph_z), 0.12,
                 fc="black", ec=C_OUT, lw=1.0, zorder=8))
    leader(ax, ph_x, ph_z, ph_x, ph_z - 0.8,
           f"PINHOLE  Ø{PH_D}mm\nX={TBS_PH_X}  Z={PH_H}mm",
           fs=7.0, ha="center")

    # ── Pull-cord switches ────────────────────────────────────────────────────
    PS_X_MM = 1800     # X position (near EP)
    PS_Z_MM = C_HGT - 60   # just below trunking
    CORD_HANG_Z = 900  # cord bottom hangs to ~900mm above floor (~1500mm above walkway deck at 100mm)

    C_SWITCH = "#E0E0FF"
    for si, (sw_label, sw_color, sw_x_off) in enumerate([
        ("D", "#FFD700", -60), ("G", "#FFFFF0", 60)
    ]):
        sx = wx(PS_X_MM + sw_x_off)
        sz = wz(PS_Z_MM)
        # Switch body
        sw_sz = 0.20
        ax.add_patch(mpatches.Rectangle((sx - sw_sz/2, sz - sw_sz/2), sw_sz, sw_sz,
                     fc=sw_color, ec=C_OUT, lw=1.2, zorder=7))
        ax.text(sx, sz, sw_label,
                ha="center", va="center", fontsize=7.0, fontweight="bold",
                color=C_OUT, zorder=8)
        # Pull cord hanging down
        cord_bot = wz(CORD_HANG_Z)
        ax.plot([sx, sx], [sz - sw_sz/2, cord_bot],
                color=C_OUT, lw=0.8, ls="-", zorder=5)
        # Small circle at cord end (pull handle)
        ax.add_patch(plt.Circle((sx, cord_bot), 0.06,
                     fc="white", ec=C_OUT, lw=0.8, zorder=6))
        # Conduit from switch to trunking
        ax.plot([sx, sx], [sz + sw_sz/2, tk_y],
                color=C_PIPE, lw=1.0, ls=":", zorder=4)

    # Pull switch label
    leader(ax, wx(PS_X_MM), wz(CORD_HANG_Z) - 0.1,
           wx(PS_X_MM) - 1.2, wz(CORD_HANG_Z) - 0.6,
           "Pull-cord switches\nD = safelight (red)\nG = white light\nCords hang to ~1,500mm\nabove walkway deck",
           fs=6.5, color="#606080")

    # ── LED panels (ceiling-mounted, shown as rectangles at top) ──────────────
    LED_W_MM = 600
    LED_H_MM = 30    # panel thickness shown in elevation
    LED_Z = C_HGT - TK_H_MM - LED_H_MM - 10   # just below trunking
    LED_POSITIONS = [1000, 2900, 4800]
    C_LED = "#FFFFF0"
    for lp_x in LED_POSITIONS:
        lx = wx(lp_x + LED_W_MM)   # mirrored
        lz = wz(LED_Z)
        lw = LED_W_MM * S
        lh = LED_H_MM * S
        ax.add_patch(mpatches.Rectangle((lx, lz), lw, lh,
                     fc=C_LED, ec=C_OUT, lw=1.0, zorder=5))
        ax.text(lx + lw / 2, lz + lh / 2, "G",
                ha="center", va="center", fontsize=6.5, fontweight="bold",
                color=C_OUT, zorder=6)
        # Conduit stub up to trunking
        ax.plot([lx + lw / 2, lx + lw / 2], [lz + lh, tk_y],
                color=C_PIPE, lw=1.0, ls=":", zorder=4)

    # LED panel leader (label middle panel)
    mid_led_cx = wx(LED_POSITIONS[1] + LED_W_MM / 2)
    mid_led_cz = wz(LED_Z + LED_H_MM)
    leader(ax, mid_led_cx, mid_led_cz,
           mid_led_cx - 1.5, mid_led_cz + 0.5,
           "LED panels (G)\n3×20W  4000K  ceiling-mount\n300×600mm each",
           fs=6.5, color="#808000")

    # ── Safelight strips — two ceiling-mounted N–S strips flanking pinhole ───
    # Circuit D: 2× red LED strips at X≈1399 and X≈3399 (offset ±1000mm from pinhole)
    # Shown in elevation as short rectangles at ceiling height (they run N–S, perpendicular to this view)
    SL3_POSITIONS = [600, 1800, 4100]   # match sheet 2 positions
    SL3_W_MM = 20     # strip width along X
    SL3_H_MM = 20     # strip thickness in elevation
    SL3_Z = C_HGT - TK_H_MM - LED_H_MM - 10 - SL3_H_MM - 10  # below LED panels
    for sl3_x in SL3_POSITIONS:
        s3x = wx(sl3_x + SL3_W_MM)   # mirrored
        s3z = wz(SL3_Z)
        s3w = max(SL3_W_MM * S, 0.08)
        s3h = SL3_H_MM * S
        ax.add_patch(mpatches.Rectangle((s3x, s3z), s3w, s3h,
                     fc="#FFD700", ec=C_OUT, lw=0.8, zorder=5))
        ax.text(s3x + s3w / 2, s3z + s3h / 2, "D",
                ha="center", va="center", fontsize=5.0, fontweight="bold",
                color=C_OUT, zorder=6)
        # Conduit up to trunking
        ax.plot([s3x + s3w / 2, s3x + s3w / 2], [s3z + s3h, tk_y],
                color=C_PIPE, lw=1.0, ls=":", zorder=4)
    # Leader on near-pinhole strip
    s3_ldr_x = wx(SL3_POSITIONS[0] + SL3_W_MM / 2)
    s3_ldr_z = wz(SL3_Z)
    leader(ax, s3_ldr_x, s3_ldr_z,
           s3_ldr_x + 0.8, s3_ldr_z - 0.5,
           f"Safelight (D)\n3× red LED strips\nceiling N–S\nX≈{', '.join(str(x) for x in SL3_POSITIONS)}",
           fs=6.5, color="#B8960A")

    # ── Dimension lines ───────────────────────────────────────────────────────
    # Overall wall width
    draw_dim_h(ax, OX, OX + wlen, OY - 0.70,
               f"{C_LEN} mm  (interior length)",
               above=False, offset=0.08, fs=7.5)
    # Overall wall height
    draw_dim_v(ax, OX - 0.60, OY, OY + whgt,
               f"{TBS_C_HGT} mm",
               offset=0.08, fs=7.5)

    # EP height dimensions — dim line to the left of EP (mirrored)
    ep_x_l = wx(EP_X)  # right edge in drawing (mirrored)
    draw_dim_v(ax, ep_x_l + 0.15, OY, wz(EP_H_LO),
               f"{EP_H_LO}", offset=0.05, fs=6.5)
    draw_dim_v(ax, ep_x_l + 0.15, wz(EP_H_LO), wz(EP_H_HI),
               f"{EP_H_HI - EP_H_LO}", offset=0.05, fs=6.5)

    # Battery height dimensions — dim line to the left of BAT (mirrored)
    ba_x_l = wx(BA_X)  # right edge in drawing (mirrored)
    draw_dim_v(ax, ba_x_l + 0.15, OY, wz(BA_H_LO),
               f"{BA_H_LO}", offset=0.05, fs=6.5)
    draw_dim_v(ax, ba_x_l + 0.15, wz(BA_H_LO), wz(BA_H_HI),
               f"{BA_H_HI - BA_H_LO}", offset=0.05, fs=6.5)

    # Pinhole height
    draw_dim_v(ax, ph_x - 0.25, OY, wz(PH_H),
               f"PH  Z={PH_H}", offset=0.05, fs=6.5)

    # Trunking height callout
    draw_dim_v(ax, OX - 0.40, wz(TK_Z), OY + whgt,
               f"Trunking\n{TK_H_MM}mm", offset=0.05, fs=6.0)

    # Pull switch cord length
    ps_dim_x = wx(PS_X_MM - 120)  # mirrored offset
    draw_dim_v(ax, ps_dim_x, wz(CORD_HANG_Z), wz(PS_Z_MM),
               f"Cord\n{PS_Z_MM - CORD_HANG_Z}mm", offset=0.05, fs=6.0)

    # ── Horizontal X dimensions for key equipment ─────────────────────────────
    DIM_Z_TOP = OY + whgt + 0.40
    draw_dim_h(ax, wx(EVAP_X + EVAP_W), wx(EVAP_X), DIM_Z_TOP,
               f"Evap  X={EVAP_X}–{EVAP_X+EVAP_W}",
               above=True, offset=0.05, fs=6.0)
    draw_dim_h(ax, wx(EP_X + EP_W), wx(EP_X), DIM_Z_TOP + 0.35,
               f"EP  X={EP_X}–{EP_X+EP_W}",
               above=True, offset=0.05, fs=6.0)
    draw_dim_h(ax, wx(BA_X + BA_W), wx(BA_X), DIM_Z_TOP,
               f"BAT  X={BA_X}–{BA_X+BA_W}",
               above=True, offset=0.05, fs=6.0)
    draw_dim_h(ax, wx(PUMP_X + PUMP_W), wx(PUMP_X), DIM_Z_TOP,
               f"Pump  X={PUMP_X}–{PUMP_X+PUMP_W}",
               above=True, offset=0.05, fs=6.0)

    # ── Component key (right of elevation) ────────────────────────────────────
    KX = OX + wlen + 1.2
    KY = OY + whgt + 1.2
    ax.text(KX, KY + 0.25, "COMPONENT KEY",
            ha="left", va="center", fontsize=9.0, fontweight="bold", color=C_OUT)
    ax.plot([KX, KX + 6.0], [KY + 0.05, KY + 0.05], color=C_OUT, lw=1.0)

    key_items = [
        (C_PIPE,    "CABLE TRUNKING",    "40×25mm PVC  |  Ceiling corner rail  |  Full length"),
        (C_ELEC,    "ELECTRICAL PANEL",  f"EP  |  X={EP_X}–{EP_X+EP_W}  |  Z={EP_H_LO}–{EP_H_HI}mm"),
        (C_BATT,    "BATTERY BANK",      f"BAT  |  X={BA_X}–{BA_X+BA_W}  |  Z={BA_H_LO}–{BA_H_HI}mm"),
        ("#F5C8A0", "PUMP MANIFOLD",     f"Cct C  |  X={PUMP_X}–{PUMP_X+PUMP_W}  |  Z={PUMP_H_LO}–{PUMP_H_HI}mm"),
        (C_EVAP,    "EVAP COOLER",       f"Cct E  |  X={EVAP_X}–{EVAP_X+EVAP_W}  |  Floor to Z={EVAP_H}mm"),
        (C_ALUM,    "EXT POWER PANEL",   f"Flush-mount  |  X={PWR_PANEL_X}–{PWR_PANEL_X+PWR_PANEL_W}  |  3×MC4 + NEMA"),
        ("#FFFFF0", "LED PANELS (G)",    "3×20W  4000K  |  Ceiling-mount  |  X≈1000, 2900, 4800"),
        ("#E0E0FF", "PULL SWITCHES",     "Ccts D & G  |  SPST 6A  |  X≈1,800mm  |  Cord to ~1,500mm AFF"),
        ("#FFD700", "SAFELIGHT (D)",     f"3× red LED strips  |  Ceiling N–S  |  X≈{', '.join(str(x) for x in SL3_POSITIONS)}"),
    ]
    for j, (fc, title_k, spec) in enumerate(key_items):
        ky = KY - 0.25 - j * 0.55
        ax.add_patch(mpatches.Rectangle((KX, ky - 0.16), 0.45, 0.38,
                     fc=fc, ec=C_OUT, lw=0.8, zorder=4))
        ax.text(KX + 0.60, ky + 0.04, title_k,
                ha="left", va="center", fontsize=7.5,
                fontweight="bold", color=C_OUT)
        ax.text(KX + 0.60, ky - 0.12, spec,
                ha="left", va="center", fontsize=6.5, color=C_DIM)

    # ── Drawing notes ─────────────────────────────────────────────────────────
    import textwrap
    NX = KX
    NOTE_W = 6.0
    notes = [
        "1. Elevation looking toward pinhole wall (Yd=0) from inside the container. "
        "All equipment is wall-mounted or floor-standing on the pinhole wall face.",
        "2. Cable trunking runs horizontally at the ceiling corner rail (Z≈2,363mm). "
        "Drop conduits (10mm corrugated, shown dashed) descend to each device.",
        "3. Pull-cord switches at ceiling height, cords hang to ~1,500mm above "
        "walkway deck (~900mm AFF). D=safelight (red), G=white light.",
        "4. LED panels are ceiling-mounted, centered across container width. "
        "Connected to Circuit G via trunking. Non-operational only.",
    ]
    WRAP_CHARS = 100
    NOTE_FS = 6.5
    LINE_SP = 0.20
    NOTE_PAD = 0.12
    wrapped_lines = []
    for note in notes:
        lines = textwrap.wrap(note, width=WRAP_CHARS)
        wrapped_lines.append(lines)
    total_lines = sum(len(ls) for ls in wrapped_lines) + len(notes) - 1
    box_h = 0.35 + total_lines * LINE_SP + 2 * NOTE_PAD

    # Position notes box directly below component key
    key_bottom = KY - 0.25 - (len(key_items) - 1) * 0.55 - 0.30
    NY = key_bottom - box_h

    ax.add_patch(FancyBboxPatch((NX - 0.10, NY - NOTE_PAD), NOTE_W, box_h,
                 boxstyle="round,pad=0.04", fc="#F8F9FA", ec=C_DIM, lw=0.8, zorder=2))
    ax.text(NX + 0.05, NY + box_h - NOTE_PAD - 0.15, "DRAWING NOTES:",
            ha="left", va="center", fontsize=7.5,
            fontweight="bold", color=C_OUT)
    cy = NY + box_h - NOTE_PAD - 0.40
    for ni, lines in enumerate(wrapped_lines):
        for line in lines:
            ax.text(NX + 0.05, cy, line,
                    ha="left", va="center", fontsize=NOTE_FS, color=C_DIM)
            cy -= LINE_SP
        if ni < len(wrapped_lines) - 1:
            cy -= LINE_SP * 0.4

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 3 OF 3",
                drawing_title="PINHOLE WALL INTERIOR ELEVATION",
                subtitle="Equipment mounting  ·  Cable trunking & drop conduits  ·  Pull-cord switches  ·  LED panels",
                scale_note="1:40  (1 drawing unit = 400 mm)",
                doc_id="TBS-ELEC · Electrical & Systems")

    plt.savefig(f"{DIAGRAMS_DIR}/electrical-sheet3.png", dpi=150, bbox_inches="tight",
                pad_inches=0.10, facecolor="white")
    plt.savefig(svg_path(f"{DIAGRAMS_DIR}/electrical-sheet3.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  → electrical-sheet3.png  Done.")


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs(SVG_DIR, exist_ok=True)
    print("Generating TBS-001 Electrical & Systems diagrams...")
    draw_sheet1()
    draw_sheet2()
    draw_sheet3()
    print("Done.")
