#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_electrical_diagram.py
TBS-001 Electrical & Systems — five engineering drawing sheets.

Sheet 1: System one-line diagram (power flow, components, fuse ratings)
Sheet 2: Container floor plan with wiring layout  (scale 1:500)
Sheet 3: Pinhole-wall interior elevation
Sheet 4: Plumbing-panel pump power (Circuit C)
Sheet 5: Main panel layout + fuse schedule
"""

import textwrap
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import os
from tbs_constants import C_BLUE_IBC, C_EVAP, C_ELEC, C_BATT, C_PUMP, DIAGRAMS_DIR, PWR_PANEL_W, PWR_PANEL_H, PWR_PANEL_D, PWR_PANEL_CUTOUT_W, PWR_PANEL_CUTOUT_H, EVAP_COOLER_W_AC, EVAP_COOLER_W_BUS
from tbs_title_block import title_block
from tbs_drawing import (draw_dim_h, draw_dim_v, leader, draw_notes,
                         draw_rect, draw_circle, hatch_rect, draw_pipe_path)

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
#   Center-right (x=7.5–13.0): shore charger branch + ground + legend + summary
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
    CX = LX + LW / 2   # centerline

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
    # 1b. PV array disconnect — load-break isolator between array and MPPT (NEC 690.13)
    rbox(ax, LX + 1.2, 11.32, LW - 2.4, 0.46,
         "PV ARRAY DISCONNECT  (load-break)",
         "DC 50A / 150VDC  |  array → MPPT, on the EP interior (NEC 690.13)",
         fc=C_WARN, ts=8.3, ss=6.4)
    varrow(ax, CX, 12.0, 11.78, col=C_SOLAR)
    wlabel(ax, CX + 0.18, 11.92, "10 AWG PV  |  via power panel", size=6.8)

    # 3. Battery bank  y=8.4–9.5
    rbox(ax, LX, 8.4, LW, 1.1,
         "BATTERY — 100Ah / 1,200Wh (standard, 1 pack)",
         "1× 100Ah 12V LiFePO4  |  busbar wired for a 2nd pack (plug-in → 200Ah / 2,400Wh)  |  100% DoD",
         fc=C_BATT_TINT, ts=9.5, ss=8.0)
    # 2b. MPPT charge-line fuse — protects the MPPT→battery conductor (6 AWG)
    rbox(ax, LX + 1.2, 9.55, LW - 2.4, 0.42,
         "60A CHARGE-LINE FUSE  (MPPT → battery)",
         "Close to the battery  |  6 AWG charge conductor",
         fc=C_WARN, ts=8.3, ss=6.4)
    varrow(ax, CX, 10.3, 9.97, col=C_CL)
    wlabel(ax, CX + 0.18, 10.12, "6 AWG  |  Charge +", size=6.8)

    # Negative busbar (dashed, right side of column)
    nb_x = LX + LW - 0.35
    ax.plot([nb_x, nb_x], [8.4, 5.6],
            color=C_STEEL, lw=1.5, linestyle="--", zorder=3)
    wlabel(ax, nb_x + 0.12, 7.0, "NEG busbar  2/0 AWG", size=7.0)

    # 4. MRBF terminal fuse — on the battery (+) post, ≤180mm  y=7.82–8.29
    bx = LX + 1.2
    bw = LW - 2.4
    rbox(ax, bx, 7.82, bw, 0.47,
         "200A MRBF TERMINAL FUSE",
         "Terminal-mount on battery (+) post, ≤180mm (ABYC E-11)",
         fc=C_WARN, ts=9.0, ss=6.8)
    varrow(ax, CX, 8.4, 8.29, col=C_OUT)
    wlabel(ax, CX + 0.18, 8.36, "2/0 AWG  |  Battery positive")

    # 4b. Remote battery switch (contactor) — tripped by the external E-stop  y=7.24–7.71
    rbox(ax, bx, 7.24, bw, 0.47,
         "REMOTE BATTERY SWITCH  (contactor)",
         "Blue Sea ML-RBS 500A magnetic-latch  |  trips OFF on either E-stop (in/out)",
         fc=C_WARN, ts=9.0, ss=6.8)
    varrow(ax, CX, 7.82, 7.71, col=C_OUT)

    # 4c. Internal main disconnect switch — maintenance/service  y=6.66–7.13
    rbox(ax, bx, 6.66, bw, 0.47,
         "MAIN DISCONNECT SWITCH  (internal)",
         "Blue Sea m-Series 300A manual isolator  |  maintenance / service",
         fc=C_WARN, ts=9.0, ss=6.8)
    varrow(ax, CX, 7.24, 7.13, col=C_OUT)

    # 5. Fuse block  y=5.4–6.55
    rbox(ax, LX, 5.4, LW, 1.15,
         "BLUE SEA 5026 FUSE BLOCK",
         "12-circuit ST-blade  |  Positive + negative busbars  |  In IP65 enclosure on the plywood",
         fc=C_WARN, ts=10.0, ss=8.0)
    varrow(ax, CX, 6.66, 6.55, col=C_OUT)
    wlabel(ax, CX + 0.18, 6.605, "2/0 AWG", size=6.8)

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

    # ── SHORE CHARGER BRANCH (center-top, same row as battery) ───────────────
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
         "Weatherproof  |  Shore power input when grid power available",
         fc="white", ec=C_OUT, lw=1.0, ts=8.5, ss=7.5, bold=False)
    varrow(ax, SC_X + SC_W / 2, SC_Y - 0.55, SC_Y, col="#A07820")
    wlabel(ax, SC_X + SC_W / 2 + 0.15, SC_Y - 0.28, "Shore AC →", size=7.0)

    # ── EXTERNAL EMERGENCY CUT-OFF (E-stop on the external power panel) ────────
    # Sits above the distribution bus (y≈5.98) and below the NEMA inlet (y=7.05).
    es_y, es_h = 6.32, 0.60
    rbox(ax, SC_X, es_y, SC_W, es_h,
         "EMERGENCY CUT-OFF  (E-STOP) — external panel",
         "Red IP66 mushroom on power-panel face  →  trips contactor OFF (1 of 2)",
         fc=C_WARN, ts=9.0, ss=7.0)
    # low-current control loop: contactor (left chain) → external E-stop
    ax.annotate("", xy=(SC_X, es_y + es_h / 2), xytext=(bx + bw, 7.47),
                arrowprops=dict(arrowstyle="-|>", color="#6A3DA8",
                                lw=1.6, linestyle=(0, (4, 2))), zorder=7)
    wlabel(ax, (bx + bw + SC_X) / 2 - 0.1, 7.18,
           "Control 2× 18 AWG  |  pinhole-wall gland", ha="center", size=7.0)
    # interior E-stop on the EP face — paralleled with the exterior one (kill from inside too).
    # Sits BELOW the distribution bus (y≈5.98) — the external E-stop is above it — so the bus runs
    # cleanly in the gap between the two E-stop boxes instead of straight through this one.
    ies_y = 5.26
    rbox(ax, SC_X, ies_y, SC_W, es_h,
         "EMERGENCY CUT-OFF  (E-STOP) — interior EP",
         "Red IP65 mushroom on the EP face  →  also trips contactor OFF (2 of 2)",
         fc=C_WARN, ts=9.0, ss=7.0)
    ax.annotate("", xy=(SC_X, ies_y + es_h / 2), xytext=(bx + bw, 7.20),
                arrowprops=dict(arrowstyle="-|>", color="#6A3DA8",
                                lw=1.6, linestyle=(0, (4, 2))), zorder=7)
    wlabel(ax, (bx + bw + SC_X) / 2 - 0.1, 6.42,
           "parallel — either E-stop trips it", ha="center", size=6.6)

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
    # NOTE: these values must match calculate_energy_budget.py and
    # electrical-report.md §3.1.  Update all three when specs change.
    summary = [
        ("Battery capacity",    "100Ah × 12V = 1,200Wh  (standard, 1 pack; +2nd → 2,400Wh)"),
        ("Energy per session",  "780 Wh (0.78 kWh)  — 3.0h continuous + pumps"),
        ("Sessions per charge", "1.5 standard  (3.1 with the 2nd pack)"),
        ("Solar yield",         "600W × 5.5h = 3,300 Wh/day  (Palm Springs)"),
        ("Solar sessions/day",  "4.2 prints/day from solar alone"),
        ("Shore recharge",      "~7h standard  (~14h with the 2nd pack)"),
        ("Peak load",           "~492W simultaneous  (all circuits on)"),
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
        # letter, name, fuse, wire, load, note, color
        ("A", "VENTILATION FAN\nEXHAUST  (6\")",  "5A",  "16 AWG", "60W",
         "Sealed end wall (X=5893mm)  |  below X1, in corridor  |  Yd=1181mm", C_ALUM),
        ("B", "VENTILATION FAN\nINTAKE  (6\")",   "5A",  "16 AWG", "60W",
         "Cargo door panel (X=0)  |  low position  |  Yd=365mm", C_ALUM),
        ("C", "WATER PUMPS\n(corridor + P-02)",       "15A", "14 AWG", "100W",
         "Corridor panel (Yd=1046–1316) + P-02 (pinhole wall)", C_PUMP_TINT),
        ("D", "SAFELIGHT\ninterior + vestibule",  "5A",  "18 AWG", "15W",
         "3× red LED strips (ceiling, N–S)  |  pull-cord switch", "#FFEEDD"),
        ("E", "EVAP COOLER\n(120V AC via inverter)",  "40A", "10 AWG", f"{EVAP_COOLER_W_BUS}W",
         "Inverter→AC unit  |  GFCI  |  200mm duct (see §7.6)", C_EVAP_TINT),
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
    title_block(ax, "SHEET 1 OF 7",
                drawing_title="SYSTEM ONE-LINE DIAGRAM",
                subtitle="Power flow  ·  Component specifications  ·  Circuit fuse ratings  ·  Wire gauges",
                scale_note="Not to scale",
                doc_id="TBS-ELEC · Electrical & Systems")

    plt.savefig(os.path.join(DIAGRAMS_DIR, "electrical-sheet1.png"), dpi=150, bbox_inches="tight",
                pad_inches=0.10, facecolor="white")
    plt.close(fig)
    print("  → electrical-sheet1.png  Done.")


# ─────────────────────────────────────────────────────────────────────────────
# SHEET 2 — Container Floor Plan + Wiring Layout  (scale 1:500)
#
# ORIENTATION:
#   Container long axis (5893mm) = HORIZONTAL (left–right in plan)
#   Optical depth (2362mm)       = VERTICAL (bottom–top in plan)
#   LEFT short wall  = X=0   = CARGO DOOR end (hinged panel / light trap)
#   RIGHT short wall = X=5893= FAR END
#   BOTTOM long wall = Y=0   = PINHOLE WALL  (Yd=0)
#   TOP long wall    = Y=2362= IMAGE PLANE WALL
#   Pinhole: on BOTTOM long wall at X=2399mm (centered on film plane)
#   Image plane: on TOP long wall
#   NO vestibule shown — light trap is part of hinged-panel drawing
#   EP + BAT on pinhole wall (Yd=0); pumps on plumbing panel (Yd=1046)
# ─────────────────────────────────────────────────────────────────────────────

def draw_sheet2():
    from matplotlib.patches import Polygon as MplPolygon
    from tbs_constants import C_LEN as TBS_C_LEN, C_WID as TBS_C_WID, FP_H, PH_X as TBS_PH_X, PH_D, PH_FNO, FP_X_L, FP_X_R, ZONE_L_END, ZONE_R_START, EVAP_DUCT_X, EVAP_DUCT_D, EP_X, EP_W, BA_X, BA_W, CORRIDOR_YD_NEAR, CORRIDOR_W, EQPANEL_W, EQPANEL_X, BB_OD, IBC_COL_X, IBC_W, IBC_D, BLUE_IBC_Y, IBC_FAR_Y, DRUM_D, DRUM_R, FAN_A_YD, FAN_B_YD, DIAGRAMS_DIR

    # ── mm-first coordinate system ───────────────────────────────────────────
    # Axes show mm directly.  Interior: X 0→C_LEN, Yd 0→C_WID.
    # Adapter variables let existing expressions (OX+wt, OY+cwid-wt, ix(),
    # x*S_xi, etc.) evaluate to correct mm values without rewriting every line.
    C_LEN   = TBS_C_LEN    # 5893mm
    C_WID   = TBS_C_WID    # 2362mm
    WT_MM   = 120           # mm schematic wall thickness
    PH_X_MM = TBS_PH_X     # 2399mm
    ZONE_L  = ZONE_L_END
    ZONE_R  = ZONE_R_START

    OX   = -WT_MM
    OY   = -WT_MM
    wt   = WT_MM
    clen = C_LEN + 2 * WT_MM
    cwid = C_WID + 2 * WT_MM
    S_yd = (cwid - 2 * wt) / C_WID   # = 1.0
    S_xi = (clen - 2 * wt) / C_LEN   # = 1.0
    def ix(x_mm):
        return OX + wt + x_mm * S_xi  # = x_mm

    PAD_X_L   = 1300
    PAD_X_R   = 4800
    PAD_Y_BOT = 1800
    PAD_Y_TOP = 1350
    X_LO = OX - PAD_X_L
    X_HI = OX + clen + PAD_X_R
    Y_LO = OY - PAD_Y_BOT
    Y_HI = OY + cwid + PAD_Y_TOP
    FIG_CX = (X_LO + X_HI) / 2

    FW, FH = 24.0, 12.0
    fig, ax = plt.subplots(figsize=(FW, FH), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Y_LO, Y_HI)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # ── Page title — positioned above container ─────────────────────────────
    title_y = OY + cwid + 550
    ax.text(FIG_CX, title_y,
            "CONTAINER FLOOR PLAN & WIRING LAYOUT — TBS-001",
            ha="center", va="center", fontsize=13, fontweight="bold",
            color=TITLE_COL)
    ax.text(FIG_CX, title_y - 170,
            "Top-down plan view  ·  All dimensions in mm  "
            "·  Pinhole on bottom long wall — optical axis crosses container width (2362mm)",
            ha="center", va="center", fontsize=8.0, color=C_DIM)

    ph_x     = PH_X_MM
    zone_l_x = ZONE_L
    zone_r_x = ZONE_R
    fp_l_x   = FP_X_L
    fp_r_x   = FP_X_R

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
    ax.text(OX - 60, OY + cwid/2,
            "CARGO DOOR\n(X=0)",
            fontsize=7.0, color=C_OUT, ha="right", va="center",
            fontweight="bold")
    ax.text(OX + clen + 60, OY + cwid/2,
            "FAR END\n(X=5893mm)",
            fontsize=7.0, color=C_DIM, ha="left", va="center")
    ax.text(OX + clen/2, OY + cwid - wt + 410,
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
        ax.text(zx, OY+cwid-wt+40, zlabel, ha="center", va="bottom",
                fontsize=6.5, color=C_DIM)

    ax.text((int_left + zone_l_x)/2, OY + cwid - wt + 260,
            "LEFT\nEND ZONE", ha="center", va="top", fontsize=7.0,
            color="#805000", fontweight="bold", zorder=5)
    ax.text((zone_l_x + zone_r_x)/2, OY + cwid - wt + 260,
            "OPTICAL ZONE\n(film plane only)", ha="center", va="top", fontsize=7.0,
            color="#006000", fontweight="bold", zorder=5)
    ax.text((zone_r_x + int_right)/2, OY + cwid - wt + 260,
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

    # ── Image plane strip — X=150–4649mm ────────────────────────────────────
    ax.add_patch(mpatches.Rectangle(
                 (fp_l_x, OY+cwid-wt-75), fp_r_x - fp_l_x, 75,
                 fc="#A8C8E8", ec=C_CL, lw=1.5, zorder=6))
    ax.text((fp_l_x+fp_r_x)/2, OY + cwid - wt - 38,
            f"FILM PLANE  X={FP_X_L}–{FP_X_R}mm  ({FP_X_R-FP_X_L}mm wide × {FP_H}mm H)",
            ha="center", va="center", fontsize=7.5, color=TITLE_COL,
            fontweight="bold", zorder=7)

    # ── Pinhole — bottom long wall at X=2874mm (recenterd on new film plane) ─
    ax.add_patch(plt.Circle((ph_x, OY + wt/2), 60,
                 fc="black", ec=C_OUT, lw=1.0, zorder=8))
    leader(ax, ph_x, OY + wt/2, ph_x + 350, OY - 175,
           f"PINHOLE  Ø{PH_D}mm\nX={TBS_PH_X}mm  f/{PH_FNO}",
           fs=7.5, ha="center")

    # ── NEMA inlet — positioned after EP is drawn (see below) ───────────────

    # ── Colonnade equipment ───────────────────────────────────────────────────
    # x_mm  = TBS X along long axis (0 = cargo door end = LEFT in plan)
    #          TBS coords run 0–5893mm interior-to-interior.
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
        ax.text(ex+ew/2, cy_e + (50 if sublabel else 0), label,
                ha="center", va="center", fontsize=6.5, fontweight="bold",
                color=C_OUT, zorder=6)
        if sublabel:
            ax.text(ex+ew/2, cy_e - 60, sublabel,
                    ha="center", va="center", fontsize=5.5, color=C_DIM, zorder=6)

    # LEFT END ZONE (X=0–150mm) — light trap drum only (waste drums eliminated rev 5)
    # Drum centerd at X=0 (spans cargo door wall); only draw interior half X=0–DRUM_R
    from tbs_constants import C_LT_DRUM
    equip(0, C_WID//2 - DRUM_R, DRUM_R, DRUM_D, "LT DRUM\n(partial)", C_LT_DRUM,
          f"Ø{DRUM_D}mm vertical axis  Yd={C_WID//2 - DRUM_R}–{C_WID//2 + DRUM_R}mm")

    # ── Ghost: hinged panel + drum in TRANSPORT position (SWUNG ~56°) ────────
    # rev10: the panel + drum REVOLVE ~56° about the Ø89 pivot (PIVOT_X, PIVOT_YD)
    # for transport — they no longer slide. Drawn as a faint swung ghost.
    import numpy as _np
    from tbs_constants import (
        PIVOT_X, PIVOT_YD, SWING_LOCK_DEG, PANEL_CORNER_T, PANEL_CENTER_T,
        PANEL_CORNER_YD_L, PANEL_CORNER_YD_R,
    )
    GHOST_ALPHA = 0.18
    GHOST_EC = "#808080"
    GHOST_LS = (0, (4, 3))   # dashed

    def _sw(X, Yd):
        t = _np.radians(SWING_LOCK_DEG); c, s = _np.cos(t), _np.sin(t)
        return (PIVOT_X + (X - PIVOT_X) * c - (Yd - PIVOT_YD) * s,
                PIVOT_YD + (X - PIVOT_X) * s + (Yd - PIVOT_YD) * c)
    def _pt(X, Yd):                      # physical (X, Yd) -> draw pixel
        Xs, Yds = _sw(X, Yd)
        return (ix(Xs), OY + wt + Yds * S_yd)

    # Panel — stepped profile rotated about the pivot (each zone a swung polygon)
    for (yd_lo, yd_hi, thick) in [
        (0, PANEL_CORNER_YD_L, PANEL_CORNER_T),
        (PANEL_CORNER_YD_L, PANEL_CORNER_YD_R, PANEL_CENTER_T),
        (PANEL_CORNER_YD_R, C_WID, PANEL_CORNER_T),
    ]:
        poly = [_pt(0, yd_lo), _pt(thick, yd_lo), _pt(thick, yd_hi), _pt(0, yd_hi)]
        ax.add_patch(mpatches.Polygon(poly, closed=True,
                     fc="#B0A090", ec=GHOST_EC, lw=1.0, ls=GHOST_LS,
                     alpha=GHOST_ALPHA, zorder=4))

    # Drum — swung center
    gd_cx, gd_cy = _pt(PANEL_CENTER_T / 2, C_WID / 2)
    gd_r = DRUM_R * S_xi
    ax.add_patch(plt.Circle((gd_cx, gd_cy), gd_r,
                 fc=C_LT_DRUM, ec=GHOST_EC, lw=1.0, ls=GHOST_LS,
                 alpha=GHOST_ALPHA, zorder=4))

    # Label
    ax.text(gd_cx, gd_cy, "Panel + drum\n(swung 56°, transport)",
            ha="center", va="center", fontsize=6.0, color="#808080",
            style="italic", zorder=5)

    # PINHOLE WALL — duct penetration (evap cooler now external)
    duct_cx = ix(EVAP_DUCT_X)
    duct_cy = OY + wt / 2
    duct_r = EVAP_DUCT_D / 2
    ax.add_patch(plt.Circle((duct_cx, duct_cy), duct_r,
                 fc=C_EVAP, ec=C_OUT, lw=1.2, zorder=7))
    ax.text(duct_cx, duct_cy, "E",
            ha="center", va="center", fontsize=6.5, fontweight="bold",
            color=C_OUT, zorder=8)

    # CORRIDOR PUMPS (Yd=1046) — P-01/03/04/05 + ACC (P-02 + the filters are on the pinhole wall)
    equip(EQPANEL_X - BB_OD, CORRIDOR_YD_NEAR, EQPANEL_W, CORRIDOR_W,
          "C", C_PUMP, "Corridor pumps")

    # RIGHT END ZONE — 4× IBC in 2×2 stack
    # Near column (Yd=30–1046): Blue #1 on top, Brown on bottom
    equip(IBC_COL_X, BLUE_IBC_Y, IBC_W, IBC_D, "IBC-1 BLUE\n+ IBC-3 BROWN",
          C_BLUE_IBC, "Near column  Yd=30–1046")
    # Far column (Yd=1316–2332): Blue #2 on top, Waste on bottom — 270mm plumbing corridor between columns
    # Plan view sees top tier (Blue #2)
    equip(IBC_COL_X, IBC_FAR_Y, IBC_W, IBC_D, "IBC-2 BLUE\n+ IBC-4 WASTE",
          C_BLUE_IBC, "Far column  Yd=1316–2332")

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
    # Fan A — EXHAUST: RIGHT short wall = sealed end (X=C_LEN), Yd=1181mm (below the X1 fill port, in the plumbing corridor)
    FA_X = OX + clen - wt/2
    FA_Y = OY + wt + FAN_A_YD * S_yd
    ax.add_patch(plt.Circle((FA_X, FA_Y), 110,
                 fc=C_ALUM, ec=C_OUT, lw=1.2, zorder=5))
    ax.text(FA_X, FA_Y, "A",
            ha="center", va="center", fontsize=9, fontweight="bold",
            color=C_OUT, zorder=6)

    # Fan B — INTAKE: LEFT short wall = cargo door panel (X=0), Yd=365mm near pinhole wall (near corner — rev9/B2 swap), LOW
    FB_X = OX + wt/2
    FB_Y = OY + wt + FAN_B_YD * S_yd
    ax.add_patch(plt.Circle((FB_X, FB_Y), 110,
                 fc=C_ALUM, ec=C_OUT, lw=1.2, zorder=5))
    ax.text(FB_X, FB_Y, "B",
            ha="center", va="center", fontsize=9, fontweight="bold",
            color=C_OUT, zorder=6)

    # Safelight D — three ceiling-mounted N–S strips
    # Positioned in gaps between white LED panels to avoid visual overlap
    # Each shortened to stay clear of optical cone at its X position
    SL_STRIPS = [
        (600,  1800),   # near cargo door — cone limit at Yd≈1889, stop at 1800
        (1800, 2100),   # between white panels 1 & 2 — cone limit at Yd≈2174, stop at 2100
        (4100, 2100),   # between white panels 2 & 3 — cone limit at Yd≈2730, stop at 2100
    ]
    SL_STRIP_W = 20    # strip width along X (mm)
    SL_POSITIONS = [s[0] for s in SL_STRIPS]   # for component key reference
    for sl_x_mm, sl_yd_max in SL_STRIPS:
        sl_dx = ix(sl_x_mm)
        sl_dw = max(SL_STRIP_W * S_xi, 40)
        sl_dy1 = OY + wt + 25
        sl_dy2 = OY + wt + sl_yd_max * S_yd
        ax.add_patch(mpatches.Rectangle((sl_dx, sl_dy1), sl_dw, sl_dy2 - sl_dy1,
                     fc="#FFD700", ec=C_OUT, lw=0.8, zorder=5))
        ax.text(sl_dx + sl_dw + 30, (sl_dy1 + sl_dy2) / 2, "D",
                ha="left", va="center", fontsize=6.5, fontweight="bold", color=C_OUT)

    # ── White LED panels (Circuit G) — 3× ceiling-mounted ───────────────────
    LED_W_MM = 600    # panel width along X
    LED_D_MM = 300    # panel depth along Yd
    LED_YD   = C_WID / 2 - LED_D_MM / 2   # centered across width
    LED_POSITIONS = [1000, 2900, 4424]     # X positions (mm) — 3rd rotated 90° at the EP (matches 3D EQPANEL_X)
    C_LED = "#FFFFF0"
    for li, lp_x in enumerate(LED_POSITIONS):
        rot = (li == 2)                    # 3rd panel is rotated 90° (300 across X, 600 along Yd)
        lx = ix(lp_x)
        ly = OY + wt + LED_YD * S_yd
        lw = (LED_D_MM if rot else LED_W_MM) * S_xi
        ld = (LED_W_MM if rot else LED_D_MM) * S_yd
        ax.add_patch(mpatches.Rectangle((lx, ly), lw, ld,
                     fc=C_LED, ec=C_OUT, lw=0.8, zorder=5, alpha=0.85))
        ax.text(lx + lw / 2, ly + ld / 2, "G",
                ha="center", va="center", fontsize=7.0, fontweight="bold",
                color=C_OUT, zorder=6)

    # ── Pull-cord switches — pinhole wall side, near EP ────────────────────
    PS_X_MM = EP_X - 110   # X position — ceiling-mounted, left of EP (cleared)
    PS_YD   = 50     # just off pinhole wall
    PS_SZ   = 80     # symbol radius (mm)
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
           ps_mid_x - 550, OY + cwid * 0.22,
           "Pull-cord switches\nD=safelight\nG=white",
           fs=6.5, color="#606080")

    # ── Cable trunking — pinhole wall face, full interior length ──────────────
    # Runs at Yd=0 on pinhole wall — physically on the wall, outside optical cone
    TK_Y  = OY + wt + 35
    TK_X1 = OX + wt + 25
    TK_X2 = OX + clen - wt - 25
    ax.plot([TK_X1, TK_X2], [TK_Y, TK_Y],
            color=C_PIPE, lw=4.5, solid_capstyle="round", zorder=6)
    ax.text((TK_X1+TK_X2)/2 + 825, TK_Y + 120,
            "40×25mm PVC cable trunking — pinhole wall face (Yd=0)\noutside optical cone",
            ha="center", va="top", fontsize=7.0, color=C_PIPE, fontweight="bold")

    # Drop conduits from trunking to devices
    DUCT_CX = ix(EVAP_DUCT_X)
    PUMP_CX = ix((EQPANEL_X - BB_OD) + EQPANEL_W / 2)
    IBC_CX  = ix(IBC_COL_X + IBC_W/2)
    for ddx, ddy in [
        (BA_DX + BA_DW/2,    OY + wt),
        (EP_DX + EP_DW/2,    OY + wt),
        (DUCT_CX,            OY + wt / 2),                   # duct penetration (in wall)
        (PUMP_CX,            OY+wt + (CORRIDOR_YD_NEAR + CORRIDOR_W/2)*S_yd),  # equip panel
        (IBC_CX,             OY+wt + BLUE_IBC_Y*S_yd),      # IBC column center
        (FA_X,               FA_Y - 110),
        (FB_X,               FB_Y - 110),
    ] + [(ix(sl_x + SL_STRIP_W / 2), OY + wt + 25) for sl_x in SL_POSITIONS] + [
        (ix(PS_X_MM),        OY + wt + PS_YD * S_yd),   # pull switches
    ] + [(ix(lp + LED_W_MM/2 + (150 if lp == 2900 else 0)), OY + wt + LED_YD * S_yd) for lp in LED_POSITIONS]:
        ax.plot([ddx, ddx], [TK_Y, ddy],
                color=C_PIPE, lw=1.0, ls=":", zorder=4)

    # ── Component leaders — label every key item on the diagram ────────────────
    # EP — Electrical panel
    leader(ax, EP_DX + 50, OY + wt + WALL_MOUNT_H,
           EP_DX - EP_DW + 25, OY + cwid * 0.32,
           "Electrical panel (EP)\nMPPT + fuse block\nPinhole wall face",
           fs=6.5, color=C_ELEC)
    # BAT — Battery bank
    leader(ax, BA_DX + BA_DW * 0.9, OY + wt + WALL_MOUNT_H,
           BA_DX + BA_DW * 0.6, OY + cwid * 0.3,
           "Battery bank (BAT)\n2×100Ah LiFePO4",
           fs=6.5, color=C_BATT)
    # Fan A — Exhaust (far end wall)
    leader(ax, FA_X + 50, FA_Y + 50,
           FA_X + 600, FA_Y + 250,
           "Exhaust fan (A)\n6\" DC  60W",
           fs=6.5, ha="right")
    # Fan B — Intake (cargo door panel)
    leader(ax, FB_X - 50, FB_Y + 50,
           FB_X - 480, FB_Y + 350,
           "Intake fan (B)\n6\" DC  60W",
           fs=6.5)
    # Pump — Cct C (on plumbing panel in IBC corridor)
    leader(ax, PUMP_CX, OY + wt + (CORRIDOR_YD_NEAR + CORRIDOR_W/2) * S_yd,
           PUMP_CX + 275, OY + cwid * 0.50,
           "Water pumps (C)\n12V DC  100W\ncorridor + P-02 (wall)",
           fs=6.5, color=C_PUMP)
    # Safelight — Cct D (label middle strip)
    sl_ldr_x = ix(SL_POSITIONS[1] + SL_STRIP_W / 2)
    sl_ldr_y = OY + cwid * 0.5
    leader(ax, sl_ldr_x, sl_ldr_y,
           sl_ldr_x - 450, OY + cwid * 0.72,
           "Safelight (D)\n3× red LED strips\nceiling, N–S",
           fs=6.5, color="#B8960A")
    # Evap cooler — Cct E (external, duct penetration)
    leader(ax, DUCT_CX, OY + wt / 2,
           DUCT_CX - 550, OY - 400,
           f"Evap cooler (E)\n120V AC {EVAP_COOLER_W_AC}W via inverter\nExternal + duct",
           fs=6.5, color=C_EVAP)
    # LED panels — Cct G (label middle panel only)
    led_mid_cx = ix(LED_POSITIONS[1] + LED_W_MM / 2)
    led_mid_cy = OY + wt + (LED_YD + LED_D_MM) * S_yd
    leader(ax, led_mid_cx, led_mid_cy,
           led_mid_cx + 300, OY + cwid * 0.62,
           "LED panels (G)\n3×20W  4000K white",
           fs=6.5, color="#808000")
    # External power panel
    leader(ax, PP_DX + PP_DW * 4/5, PP_DY + (PP_DH * 0.5),
           PP_DX + PP_DW * 2, PP_DY - 175,
           "External power panel\n3×MC4 + NEMA 5-15R\nSingle sealed penetration",
           fs=6.5, color="#806030", ha="center")

    # ── Solar panels — exterior (below container in plan) ─────────────────────
    SP_X2 = OX + clen * 0.25
    SP_Y2 = OY - 575
    SP_W2 = clen * 0.50
    SP_H2 = 250
    ax.add_patch(FancyBboxPatch((SP_X2, SP_Y2), SP_W2, SP_H2,
                 boxstyle="round,pad=20", fc=C_SOLAR, ec=C_OUT, lw=1.8, zorder=3))
    ax.text(SP_X2+SP_W2/2, SP_Y2+SP_H2/2,
            "SOLAR PANELS  (3×200W)  —  EXTERIOR, SOUTH-FACING",
            ha="center", va="center", fontsize=8.5, fontweight="bold",
            color=C_OUT, zorder=4)
    ax.annotate("", xy=(PP_DX + PP_DW / 2, PP_DY + PP_DH),
                xytext=(SP_X2, SP_Y2+SP_H2),
                arrowprops=dict(arrowstyle="-|>", color="#2D7A2D", lw=1.8,
                                connectionstyle="arc3,rad=-0.15"), zorder=4)
    ax.text(SP_X2 - 100, (SP_Y2+SP_H2 + PP_DY)/2,
            "PV cable  10 AWG / MC4\nvia ext. power panel",
            fontsize=7.0, color="#2D7A2D", ha="right", va="center")

    # ── Dimension lines ───────────────────────────────────────────────────────
    DIM_Y = OY - 300
    DIM_X = OX - 210

    draw_dim_h(ax, OX, OX+clen, DIM_Y-600, f"{C_LEN}mm  (container interior length)",
               above=False, offset=40, fs=7.5)
    draw_dim_h(ax, fp_l_x, fp_r_x, DIM_Y - 425,
               f"Film plane  {FP_X_R-FP_X_L}mm",
               above=False, offset=40, fs=7.5)
    draw_dim_v(ax, DIM_X-250, OY, OY+cwid,  f"{C_WID}mm  (optical depth / interior width)",
               offset=40, fs=7.5)

    # ── Component key (right of container) ───────────────────────────────────
    KX = C_LEN + WT_MM + 1550
    KY = OY + cwid + 250
    ax.text(KX, KY + 140, "COMPONENT KEY",
            ha="left", va="center", fontsize=9.5, fontweight="bold", color=C_OUT)
    ax.plot([KX, KX + 2900], [KY + 25, KY + 25], color=C_OUT, lw=1.0)

    key_rows = [
        ("EP",    C_ELEC,    "ELECTRICAL PANEL (EP)",
         f"EP panel  |  MPPT + fuse block  |  Pinhole wall face, X={EP_X}mm"),
        ("BAT",   C_BATT,    "BATTERY BANK (BAT)",
         f"2×100Ah LiFePO4 12V  |  2,400Wh  |  Pinhole wall face, X={BA_X}mm"),
        ("A",     C_ALUM,    "EXHAUST FAN — Cct A",
         "6\" inline DC  |  5A / 16 AWG / 60W  |  Sealed end wall (X=5893mm), below X1  |  Yd=1181mm"),
        ("B",     C_ALUM,    "INTAKE FAN — Cct B",
         "6\" inline DC  |  5A / 16 AWG / 60W  |  Cargo door panel (X=0), low  |  Yd=365mm"),
        ("C",     C_PUMP,    "PLUMBING PANEL — Cct C",
         f"Water pumps P-01/03/04/05 (corridor) + P-02 (pinhole wall)  |  12V DC  |  15A / 14 AWG / 100W"),
        ("D",     "#FFD700", "SAFELIGHT — Cct D",
         f"3× red LED strips  |  5A / 18 AWG / 15W  |  Ceiling N–S at X≈{', '.join(str(x) for x in SL_POSITIONS)}"),
        ("E",     C_EVAP,    "EVAP COOLER — Cct E",
         f"120V AC {EVAP_COOLER_W_AC}W via inverter ({EVAP_COOLER_W_BUS}W on 12V bus)  |  40A / 10 AWG DC + GFCI  |  duct at X={EVAP_DUCT_X}mm"),
        ("G",     C_LED,     "WHITE LED PANELS — Cct G",
         "3×20W ceiling panels  |  10A / 16 AWG / 60W  |  Pull-cord switch, non-operational only"),
        ("D/G",   C_SWITCH,  "PULL-CORD SWITCHES",
         f"SPST 6A ceiling switches  |  D=safelight, G=white light  |  Left of EP (cleared), X≈{PS_X_MM}mm"),
        ("EXT\nPWR",C_ALUM,"EXTERNAL POWER PANEL",
         "3×MC4 solar + NEMA 5-15R AC  |  Flush-mount in wall cutout  |  Pinhole wall"),
    ]
    for j, (badge, bc, title_k, spec) in enumerate(key_rows):
        ky = KY - 140 - j * 250
        ax.add_patch(mpatches.Rectangle((KX, ky-100), 250, 220,
                     fc=bc, ec=C_OUT, lw=0.9, zorder=4))
        ax.text(KX+125, ky+5, badge,
                ha="center", va="center", fontsize=8.0,
                fontweight="bold", color=C_OUT, zorder=5)
        ax.text(KX+325, ky+20, title_k,
                ha="left", va="center", fontsize=8.5,
                fontweight="bold", color=C_OUT)
        ax.text(KX+325, ky-60, spec,
                ha="left", va="center", fontsize=7.5, color=C_DIM)

    # ── Drawing notes ──────────────────────────────────────────────────────────
    notes = [
        "DRAWING NOTES:",
        f"1. Pinhole at X={TBS_PH_X}mm on bottom long wall (recentered on new film plane). "
        f"Film plane X={FP_X_L}\u2013{FP_X_R}mm ({FP_X_R-FP_X_L}mm wide) at Yd=2262mm. f/1088.",
        f"2. Shadow-free end zones: Left X=0\u2013{FP_X_L}mm (light trap), ",
        f"Right X={FP_X_R}\u20135893mm (IBCs only). Evap cooler external via "
        f"\u00d8{EVAP_DUCT_D}mm duct at X={EVAP_DUCT_X}mm. Amber cone \u2014 keep entirely clear.",
        "3. Cable trunking (40\u00d725mm PVC) on pinhole wall face (Yd=0) \u2014 outside "
        "optical cone. Drop conduits (10mm corrugated) to each device.",
        "4. Light trap (housed revolving door, \u00d8900mm vertical axis) in left end zone \u2014 "
        "integral to cargo-door hinged panel. See Hinged Panel drawings (\u00a712).",
        "5. Circuit G (white LED panels) and Circuit D (safelight) are independently switched ",
        "via pull-cord ceiling switches on the pinhole wall. White light must be off during operation.",
    ]
    draw_notes(ax, notes, 6200, Y_LO + 1250, spacing=80,
               fs=7, width=4250, font={"fontfamily": "monospace"})

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 2 OF 7",
                drawing_title="CONTAINER FLOOR PLAN & WIRING LAYOUT",
                subtitle="Top-down plan  ·  End-zone layout  ·  Optical cone clear",
                scale_note="Axes in mm  (approx 1:500)",
                doc_id="TBS-ELEC · Electrical & Systems")

    plt.savefig(f"{DIAGRAMS_DIR}/electrical-sheet2.png", dpi=150, bbox_inches="tight",
                pad_inches=0.10, facecolor="white")
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
        BA_X, BA_W, BA_H_LO, BA_H_HI, BA_STACK_TOP,
        EVAP_DUCT_X, EVAP_DUCT_D, EVAP_DUCT_Z,
        CORRIDOR_YD_NEAR, CORRIDOR_W,
        PWR_PANEL_X, PWR_PANEL_W, PWR_PANEL_H,
        PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_RIM,
        WALKWAY_W, WALKWAY_H, WALKWAY_LEFT_X,
        DIAGRAMS_DIR,  C_LT_DRUM, PULL_CORD_BOTTOM_Z,
    )

    # ── mm-first coordinate system ───────────────────────────────────────────
    # All coordinates are in mm. wx() mirrors X for interior-view convention.
    C_LEN = TBS_C_LEN   # 5893mm
    C_HGT = TBS_C_HGT   # 2388mm
    OX = 0
    OY = 0
    wlen = C_LEN
    whgt = C_HGT

    def wx(x_mm):
        return C_LEN - x_mm

    PAD_X_L = 800
    PAD_X_R = 2900
    PAD_Z_BOT = 600
    PAD_Z_TOP = 950
    X_LO = OX - PAD_X_L
    X_HI = OX + wlen + PAD_X_R
    Z_LO = OY - PAD_Z_BOT
    Z_HI = OY + whgt + PAD_Z_TOP
    FIG_CX = (X_LO + X_HI) / 2

    FW, FH = 24.0, 10.0
    fig, ax = plt.subplots(figsize=(FW, FH), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Z_LO, Z_HI)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # ── Page title (positioned above top dimension lines) ───────────────────
    TITLE_Y = OY + whgt + 520
    ax.text(FIG_CX, TITLE_Y,
            "PINHOLE WALL INTERIOR ELEVATION — TBS-001",
            ha="center", va="center", fontsize=13, fontweight="bold",
            color=TITLE_COL)
    ax.text(FIG_CX, TITLE_Y - 136,
            "View looking toward pinhole wall (Yd=0) from inside  "
            "·  All dimensions in mm",
            ha="center", va="center", fontsize=8.0, color=C_DIM)

    # ── Wall rectangle ────────────────────────────────────────────────────────
    ax.add_patch(mpatches.Rectangle((OX, OY), wlen, whgt,
                 fc="#F8F8F4", ec=C_OUT, lw=2.5, zorder=2))

    # Floor line
    ax.plot([OX - 120, OX + wlen + 120], [OY, OY],
            color=C_OUT, lw=3.0, zorder=3)
    ax.text(OX + wlen / 2, OY - 80, "FLOOR (Z=0)",
            ha="center", va="top", fontsize=7.5, color=C_DIM)

    # Ceiling line
    ax.plot([OX - 120, OX + wlen + 120], [OY + whgt, OY + whgt],
            color=C_OUT, lw=3.0, zorder=3)
    ax.text(OX + wlen / 2, OY + whgt + 48, "CEILING (Z=2388mm)",
            ha="center", va="bottom", fontsize=7.5, color=C_DIM)

    # Wall labels
    ax.text(OX - 60, OY + whgt / 2, "FAR\nEND\n(X=5893)",
            ha="right", va="center", fontsize=7.0, color=C_DIM)
    ax.text(OX + wlen + 60, OY + whgt / 2, "CARGO\nDOOR\nEND\n(X=0)",
            ha="left", va="center", fontsize=7.0, color=C_OUT,
            fontweight="bold")

    # ── Ghost: processing tray rim ──────────────────────────────────────────
    GHOST_ALPHA = 0.22
    GHOST_EC = "#808080"
    GHOST_LS = (0, (4, 3))
    # Tray rim: X=170–4629, Z=0–50mm
    tray_x_l = wx(PROC_TRAY_X_L)    # mirrored: right in drawing
    tray_x_r = wx(PROC_TRAY_X_R)    # mirrored: left in drawing
    tray_w = tray_x_l - tray_x_r    # positive because mirrored
    tray_h = PROC_TRAY_RIM
    ax.add_patch(mpatches.Rectangle((tray_x_r, OY), tray_w, tray_h,
                 fc="#D0E8D0", ec=GHOST_EC, lw=1.0, ls=GHOST_LS,
                 alpha=GHOST_ALPHA, zorder=3))
    ax.text((tray_x_l + tray_x_r) / 3, OY + tray_h / 2,
            f"PROCESSING TRAY RIM  (Z=0–{PROC_TRAY_RIM}mm,  X={PROC_TRAY_X_L}–{PROC_TRAY_X_R}mm)",
            ha="center", va="center", fontsize=5.5, color="#606060",
            style="italic", zorder=4)

    # ── Ghost: near walkway deck ─────────────────────────────────────────────
    # Near walkway runs along pinhole wall, X=470–4629, deck at Z=100mm
    wk_x_l = wx(WALKWAY_LEFT_X + WALKWAY_W)   # walkway starts at X=470 (left butt joint)
    wk_x_r = wx(PROC_TRAY_X_R)                # ends at tray right edge
    wk_w = wk_x_l - wk_x_r
    wk_h = WALKWAY_H
    ax.add_patch(mpatches.Rectangle((wk_x_r, OY), wk_w, wk_h,
                 fc="#E0D8C8", ec=GHOST_EC, lw=1.0, ls=GHOST_LS,
                 alpha=GHOST_ALPHA, zorder=3))
    ax.text((wk_x_l + wk_x_r) / 2.5, OY + wk_h / 1.5,
            f"NEAR WALKWAY DECK  (Z=0–{WALKWAY_H}mm,  X={WALKWAY_LEFT_X + WALKWAY_W}–{PROC_TRAY_X_R}mm)",
            ha="center", va="center", fontsize=5.5, color="#606060",
            style="italic", zorder=4)

    # ── Cable trunking — horizontal at ceiling corner ─────────────────────────
    TK_H_MM = 25    # trunking height (mm)
    TK_W_MM = 40    # trunking depth (mm) — shown as height on elevation
    TK_Z = C_HGT - TK_H_MM   # bottom of trunking (Z=2363mm)
    tk_y = (TK_Z)
    tk_h = TK_H_MM
    ax.add_patch(mpatches.Rectangle((OX + 8, tk_y), wlen - 16, tk_h,
                 fc=C_PIPE, ec=C_OUT, lw=1.2, zorder=6, alpha=0.85))
    ax.text(OX + wlen / 2, tk_y + tk_h / 2,
            "40×25mm PVC CABLE TRUNKING — FULL LENGTH",
            ha="center", va="center", fontsize=7.0, fontweight="bold",
            color="white", zorder=7)

    # ── Helper: wall-mount equipment box ──────────────────────────────────────
    def wall_equip(x_mm, z_lo, z_hi, w_mm, label, sublabel, fc, badge=""):
        ex = wx(x_mm + w_mm)   # mirrored: right edge of component maps to left in drawing
        ey = (z_lo)
        ew = w_mm
        eh = z_hi - z_lo
        ax.add_patch(mpatches.Rectangle((ex, ey), ew, eh,
                     fc=fc, ec=C_OUT, lw=1.2, zorder=5, alpha=0.88))
        cx = ex + ew / 2
        cy = ey + eh / 2
        ax.text(cx, cy + 32, label,
                ha="center", va="center", fontsize=7.5, fontweight="bold",
                color=C_OUT, zorder=6)
        if sublabel:
            ax.text(cx, cy - 40, sublabel,
                    ha="center", va="center", fontsize=6.0, color=C_DIM, zorder=6)
        # Drop conduit from trunking
        ax.plot([cx, cx], [tk_y, ey + eh],
                color=C_PIPE, lw=2.0, solid_capstyle="round", zorder=4)
        return ex, ey, ew, eh

    # ── External power panel (flush in wall) ──────────────────────────────────
    # Centered vertically at ~EP mounting height
    PP_Z_LO = EP_H_LO   # align with bottom of EP
    PP_Z_HI = PP_Z_LO + PWR_PANEL_H
    pp_x = wx(PWR_PANEL_X + PWR_PANEL_W)   # mirrored
    pp_y = (PP_Z_LO)
    pp_w = PWR_PANEL_W
    pp_h = PWR_PANEL_H
    ax.add_patch(mpatches.Rectangle((pp_x, pp_y), pp_w, pp_h,
                 fc=C_ALUM, ec=C_OUT, lw=1.5, zorder=5))
    ax.text(pp_x + pp_w / 2, pp_y + pp_h / 2 + 24,
            "EXT POWER\nPANEL", ha="center", va="center",
            fontsize=6.5, fontweight="bold", color=C_OUT, zorder=6)
    ax.text(pp_x + pp_w / 2, pp_y + pp_h / 2 - 56,
            "3×MC4 + NEMA", ha="center", va="center",
            fontsize=5.5, color=C_DIM, zorder=6)
    # Cable route from panel up to trunking
    ax.plot([pp_x + pp_w / 2, pp_x + pp_w / 2], [pp_y + pp_h, tk_y],
            color=C_PIPE, lw=2.0, solid_capstyle="round", zorder=4)

    # ── Duct penetration (evap cooler now external) ────────────────────────────
    duct_cx = wx(EVAP_DUCT_X)
    duct_cz = (EVAP_DUCT_Z)
    duct_r = EVAP_DUCT_D / 2
    ax.add_patch(plt.Circle((duct_cx, duct_cz), duct_r,
                 fc=C_EVAP, ec=C_OUT, lw=1.5, zorder=6))
    ax.text(duct_cx, duct_cz, "E",
            ha="center", va="center", fontsize=7.0, fontweight="bold",
            color=C_OUT, zorder=7)
    # Conduit from duct to trunking
    ax.plot([duct_cx, duct_cx], [duct_cz + duct_r, tk_y],
            color=C_PIPE, lw=2.0, solid_capstyle="round", zorder=4)
    leader(ax, duct_cx + duct_r, duct_cz,
           duct_cx + 480, duct_cz - 240,
           f"DUCT PENETRATION\nØ{EVAP_DUCT_D}mm  (Cct E)\nEvap cooler external",
           fs=6.5, color=C_EVAP)

    # ── Electrical panel (wall-mounted) ───────────────────────────────────────
    wall_equip(EP_X, EP_H_LO, EP_H_HI, EP_W,
               "ELECTRICAL\nPANEL (EP)", "MPPT + fuse block", C_ELEC)

    # ── Battery bank (wall-mounted) ───────────────────────────────────────────
    wall_equip(BA_X, BA_H_LO, BA_STACK_TOP, BA_W,
               "BATTERY BANK", "2×100Ah LiFePO4 (stacked)", C_BATT)

    # (Pump manifold removed from pinhole wall — now on plumbing panel in IBC corridor)

    # ── Pinhole ───────────────────────────────────────────────────────────────
    ph_x = wx(TBS_PH_X)
    ph_z = (PH_H)
    ax.add_patch(plt.Circle((ph_x, ph_z), 48,
                 fc="black", ec=C_OUT, lw=1.0, zorder=8))
    leader(ax, ph_x, ph_z, ph_x, ph_z + 320,
           f"PINHOLE  Ø{PH_D}mm\nX={TBS_PH_X}  Z={PH_H}mm",
           fs=7.0, ha="center")

    # ── Pull-cord switches ────────────────────────────────────────────────────
    PS_X_MM = EP_X - 110   # X position — ceiling-mounted, left of EP (cleared)
    PS_Z_MM = C_HGT - 60   # just below trunking
    CORD_HANG_Z = PULL_CORD_BOTTOM_Z  # 1180mm AFF — cord bottom clears the deployed chem shelf

    C_SWITCH = "#E0E0FF"
    for si, (sw_label, sw_color, sw_x_off) in enumerate([
        ("D", "#FFD700", -60), ("G", "#FFFFF0", 60)
    ]):
        sx = wx(PS_X_MM + sw_x_off)
        sz = (PS_Z_MM)
        # Switch body
        sw_sz = 80
        ax.add_patch(mpatches.Rectangle((sx - sw_sz/2, sz - sw_sz/2), sw_sz, sw_sz,
                     fc=sw_color, ec=C_OUT, lw=1.2, zorder=7))
        ax.text(sx, sz, sw_label,
                ha="center", va="center", fontsize=7.0, fontweight="bold",
                color=C_OUT, zorder=8)
        # Pull cord hanging down — parallel lines with repeating slash marks
        cord_bot = (CORD_HANG_Z)
        cord_top = sz - sw_sz/2
        cord_w = 11.2  # half-width of cord (mm)
        # Two parallel lines
        ax.plot([sx - cord_w, sx - cord_w], [cord_top, cord_bot],
                color=C_OUT, lw=0.9, zorder=5)
        ax.plot([sx + cord_w, sx + cord_w], [cord_top, cord_bot],
                color=C_OUT, lw=0.9, zorder=5)
        # Repeating diagonal slash marks between the parallel lines
        slash_spacing = 48  # spacing between slashes (mm)
        slash_ext = cord_w * 0.3  # how far slash extends beyond cord edges
        n_slashes = int((cord_top - cord_bot) / slash_spacing)
        for j in range(n_slashes):
            y_mid = cord_top - (j + 0.5) * slash_spacing
            ax.plot([sx - cord_w - slash_ext, sx + cord_w + slash_ext],
                    [y_mid - slash_spacing * 0.3, y_mid + slash_spacing * 0.3],
                    color=C_OUT, lw=0.7, zorder=5)
        # Small circle at cord end (pull handle)
        ax.add_patch(plt.Circle((sx, cord_bot), 24,
                     fc="white", ec=C_OUT, lw=0.8, zorder=6))
        # Conduit from switch to trunking
        ax.plot([sx, sx], [sz + sw_sz/2, tk_y],
                color=C_PIPE, lw=2.0, solid_capstyle="round", zorder=4)

    # Pull switch label
    leader(ax, wx(PS_X_MM + sw_x_off), (CORD_HANG_Z),
           wx(PS_X_MM) + 200, (CORD_HANG_Z) - 240,
           "Pull-cord switches\nD = safelight (red)\nG = white light\nCords end ~1180mm AFF\n(above the deployed shelf)",
           fs=6.5, color="#606080")

    # ── LED panels (ceiling-mounted, shown as rectangles at top) ──────────────
    LED_W_MM = 600
    LED_H_MM = 30    # panel thickness shown in elevation
    LED_Z = C_HGT - TK_H_MM - LED_H_MM - 10   # just below trunking
    LED_POSITIONS = [1000, 2900, 4800]
    C_LED = "#FFFFF0"
    for lp_x in LED_POSITIONS:
        lx = wx(lp_x + LED_W_MM)   # mirrored
        lz = (LED_Z)
        lw = LED_W_MM
        lh = LED_H_MM
        ax.add_patch(mpatches.Rectangle((lx, lz), lw, lh,
                     fc=C_LED, ec=C_OUT, lw=1.0, zorder=5))
        ax.text(lx + lw / 2, lz + lh / 2, "G",
                ha="center", va="center", fontsize=6.5, fontweight="bold",
                color=C_OUT, zorder=6)
        # Conduit stub up to trunking
        ax.plot([lx + lw / 2, lx + lw / 2], [lz + lh, tk_y],
                color=C_PIPE, lw=2.0, solid_capstyle="round", zorder=4)

    # LED panel leader (label middle panel)
    mid_led_cx = wx(LED_POSITIONS[1] + LED_W_MM / 2)
    mid_led_cz = (LED_Z + LED_H_MM)
    leader(ax, mid_led_cx, mid_led_cz - 40,
           mid_led_cx - 600, mid_led_cz - 200,
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
        s3z = (SL3_Z)
        s3w = max(SL3_W_MM, 32)
        s3h = SL3_H_MM
        ax.add_patch(mpatches.Rectangle((s3x, s3z), s3w, s3h,
                     fc="#FFD700", ec=C_OUT, lw=0.8, zorder=5))
        ax.text(s3x + s3w / 2, s3z + s3h / 2, "D",
                ha="center", va="center", fontsize=5.0, fontweight="bold",
                color=C_OUT, zorder=6)
        # Conduit up to trunking
        ax.plot([s3x + s3w / 2, s3x + s3w / 2], [s3z + s3h, tk_y],
                color=C_PIPE, lw=2.0, solid_capstyle="round", zorder=4)
    # Leader on near-pinhole strip
    s3_ldr_x = wx(SL3_POSITIONS[0] + SL3_W_MM / 2)
    s3_ldr_z = (SL3_Z)
    leader(ax, s3_ldr_x, s3_ldr_z,
           s3_ldr_x + 200, s3_ldr_z - 200,
           f"Safelight (D)\n3× red LED strips\nceiling N–S\nX≈{', '.join(str(x) for x in SL3_POSITIONS)}",
           fs=6.5, color="#B8960A")

    # ── Dimension lines ───────────────────────────────────────────────────────
    # Overall wall width
    draw_dim_h(ax, OX, OX + wlen, OY - 280,
               f"{C_LEN}mm  (interior length)",
               above=False, offset=32, fs=7.5)
    # Overall wall height
    draw_dim_v(ax, OX - 360, OY, OY + whgt,
               f"{TBS_C_HGT}mm",
               offset=32, fs=7.5)

    # EP height dimensions — dim line to the left of EP (mirrored)
    ep_x_l = wx(EP_X)  # right edge in drawing (mirrored)
    draw_dim_v(ax, ep_x_l, OY, (EP_H_LO),
               f"{EP_H_LO}mm", offset=20, fs=6.5)
    draw_dim_v(ax, ep_x_l - 340, (EP_H_LO), (EP_H_HI),
               f"{EP_H_HI - EP_H_LO}mm", offset=20, fs=6.5)

    # Battery height dimensions — dim line to the left of BAT (mirrored)
    ba_x_l = wx(BA_X)  # right edge in drawing (mirrored)
    draw_dim_v(ax, ba_x_l + 60, OY, (BA_H_LO),
               f"{BA_H_LO}\nmm", offset=20, fs=6.5)
    draw_dim_v(ax, ba_x_l + 60, (BA_H_LO), (BA_STACK_TOP),
               f"{BA_STACK_TOP - BA_H_LO}mm", offset=20, fs=6.5, right=True)

    # Pinhole height
    draw_dim_v(ax, ph_x - 80, OY, (PH_H),
               f"{PH_H}mm", offset=20, fs=6.5, right=True)

    # Trunking height callout
    draw_dim_v(ax, OX - 200, (TK_Z), OY + whgt,
               f"Trunking\n{TK_H_MM}mm", offset=20, fs=6.0)

    # Pull switch cord length
    ps_dim_x = wx(PS_X_MM)  # mirrored offset
    draw_dim_v(ax, ps_dim_x, (CORD_HANG_Z), (PS_Z_MM),
               f"Cord {PS_Z_MM - CORD_HANG_Z}mm", offset=20, fs=6.0, right=True)

    # ── Horizontal X dimensions for key equipment ─────────────────────────────
    DIM_Z_TOP = OY + whgt + 160
    draw_dim_h(ax, wx(EP_X + EP_W), wx(EP_X), DIM_Z_TOP + 140,
               f"EP  X={EP_X}–{EP_X+EP_W}",
               above=True, offset=20, fs=6.0)
    draw_dim_h(ax, wx(BA_X + BA_W), wx(BA_X), DIM_Z_TOP,
               f"BAT  X={BA_X}–{BA_X+BA_W}",
               above=True, offset=20, fs=6.0)
    # Duct penetration position
    draw_dim_v(ax, duct_cx + duct_r + 60, OY, duct_cz,
               f"Duct Z={EVAP_DUCT_Z}mm", offset=20, fs=6.0, right=True)

    # ── Component key (right of elevation) ────────────────────────────────────
    KX = OX + wlen + 480
    KY = OY + whgt + 480
    ax.text(KX, KY + 100, "COMPONENT KEY",
            ha="left", va="center", fontsize=9.0, fontweight="bold", color=C_OUT)
    ax.plot([KX, KX + 2400], [KY + 20, KY + 20], color=C_OUT, lw=1.0)

    key_items = [
        (C_PIPE,    "CABLE TRUNKING",    "40×25mm PVC  |  Ceiling corner rail  |  Full length"),
        (C_ELEC,    "ELECTRICAL PANEL",  f"EP  |  X={EP_X}–{EP_X+EP_W}  |  Z={EP_H_LO}–{EP_H_HI}mm"),
        (C_BATT,    "BATTERY BANK",      f"BAT  |  X={BA_X}–{BA_X+BA_W}  |  Z={BA_H_LO}–{BA_STACK_TOP}mm (2 stacked)"),
        ("#F5C8A0", "WATER PUMPS",   f"Cct C  |  P-01/03/04/05 corridor (Yd={CORRIDOR_YD_NEAR}–{CORRIDOR_YD_NEAR + CORRIDOR_W}) + P-02 (pinhole wall)"),
        (C_EVAP,    "DUCT PENETRATION",  f"Cct E  |  Ø{EVAP_DUCT_D}mm at X={EVAP_DUCT_X}, Z={EVAP_DUCT_Z}mm  |  Evap cooler external"),
        (C_ALUM,    "EXT POWER PANEL",   f"Flush-mount  |  X={PWR_PANEL_X}–{PWR_PANEL_X+PWR_PANEL_W}  |  3×MC4 + NEMA"),
        ("#FFFFF0", "LED PANELS (G)",    "3×20W  4000K  |  Ceiling-mount  |  X≈1000, 2900, 4800"),
        ("#E0E0FF", "PULL SWITCHES",     f"Ccts D & G  |  SPST 6A  |  X≈{PS_X_MM}mm  |  Cord to ~1500mm AFF"),
        ("#FFD700", "SAFELIGHT (D)",     f"3× red LED strips  |  Ceiling N–S  |  X≈{', '.join(str(x) for x in SL3_POSITIONS)}"),
    ]
    for j, (fc, title_k, spec) in enumerate(key_items):
        ky = KY - 100 - j * 220
        ax.add_patch(mpatches.Rectangle((KX, ky - 64), 180, 152,
                     fc=fc, ec=C_OUT, lw=0.8, zorder=4))
        ax.text(KX + 240, ky + 16, title_k,
                ha="left", va="center", fontsize=7.5,
                fontweight="bold", color=C_OUT)
        ax.text(KX + 240, ky - 48, spec,
                ha="left", va="center", fontsize=6.5, color=C_DIM)

    # ── Drawing notes ─────────────────────────────────────────────────────────
    notes = [
        "DRAWING NOTES:",
        "1. Elevation looking toward pinhole wall (Yd=0) from inside the container. EP and battery wall-mounted; corridor pumps (P-01/03/04/05+ACC)",
        "in the IBC corridor (Yd=1046), P-02 + the 3-stage filters on the pinhole wall; evap cooler external via duct.",
        "2. Cable trunking runs horizontally at the ceiling corner rail (Z\u22482363mm). Drop conduits (10mm corrugated, shown dashed) descend to each device.",
        "3. Pull-cord switches at ceiling height, cords hang to ~1500mm above walkway deck (~900mm AFF). D=safelight (red), G=white light.",
        "4. LED panels are ceiling-mounted, centered across container width. Connected to Circuit G via trunking. Non-operational only.",
    ]
    key_bottom = KY - 100 - (len(key_items) - 1) * 220 - 120
    notes_y_top = key_bottom - 120
    draw_notes(ax, notes, -500, KY + 40, spacing=60,
               fs=7, width=3400, font={"fontfamily": "monospace"})

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, "SHEET 3 OF 7",
                drawing_title="PINHOLE WALL INTERIOR ELEVATION",
                subtitle="Equipment mounting  ·  Cable trunking & drop conduits  ·  Pull-cord switches  ·  LED panels",
                scale_note="Axes in mm  (approx 1:40)",
                doc_id="TBS-ELEC · Electrical & Systems")

    plt.savefig(f"{DIAGRAMS_DIR}/electrical-sheet3.png", dpi=150, bbox_inches="tight",
                pad_inches=0.10, facecolor="white")
    plt.close(fig)
    print("  → electrical-sheet3.png  Done.")


# ─────────────────────────────────────────────────────────────────────────────

def draw_sheet4():
    """SHEET 4 — Corridor Plumbing-Panel Pump Power (Circuit C), scale elevation.

    Engineering elevation of the corridor plumbing panel (matches panel-layout.png):
    the single vertical pump column (ACC-01 + P-01/P-04/P-05/P-03) drawn to scale,
    powered from a 12V distribution block that is fed from the MASTER pump switch on
    the EP (electrical panel) via the ceiling trunk → curved-elbow branches to each
    pump. No per-pump switches — each Shurflo runs on its internal pressure switch;
    the EP master switch is the single manual cutoff. P-02 (Brown recycle) is on
    the pinhole-wall panel, shown as an off-panel branch. Routing follows pipe
    conventions (parallel-wall conduit + curved elbow fittings, never hard corners).
    """
    from tbs_constants import DIAGRAMS_DIR
    import generate_panel_layout as pl
    R = mpatches.Rectangle
    CC, CDK = "#2980B9", "#1B5A82"                       # Circuit-C blue + darker edge

    fig, ax = plt.subplots(figsize=(7.6, 12.4))
    ax.set_aspect("equal")
    ax.axis("off")

    PW, PH = pl.PANEL_W, pl.PANEL_H                       # 270 × 2060 (to scale)
    pcx, pw, ph = pl.PUMP_COL_C, pl.PUMP_W, pl.PUMP_H     # column center 135, body 127 × 218
    p_left = pcx - pw / 2                                 # 71.5 — pump left edge

    # ── Panel (to scale) ──
    ax.add_patch(R((0, 0), PW, PH, fc="#EFE6CC", ec=C_OUT, lw=1.6, zorder=2))
    leader(ax, 0, PH - 55, -95, PH + 15,
           "CORRIDOR PLUMBING\nPANEL — 18mm ply\n270 × 2060mm", fs=6.2, color=C_OUT, ha="right")

    # ── ACC-01 (passive accumulator — unpowered, drawn for context) ──
    ax.add_patch(mpatches.FancyBboxPatch((pl.ACC_YD - pl.ACC_OD / 2, pl.ACC_Z), pl.ACC_OD, pl.ACC_LEN,
                 boxstyle="round,pad=0,rounding_size=16", fc="#AEB6BE", ec=C_OUT, lw=1.1, zorder=6))
    ax.text(pl.ACC_YD, pl.ACC_Z + pl.ACC_LEN / 2, "ACC-01", ha="center", va="center",
            fontsize=6.6, fontweight="bold", zorder=8)

    # ── Pumps (single vertical column, real Z) + electrical terminals ──
    pumps = [("P-01", pl.P01_Z, "Blue supply"), ("P-04", pl.P04_Z, "Tray drain"),
             ("P-05", pl.P05_Z, "Brown drain"), ("P-03", pl.P03_Z, "Waste drain")]
    term = {}
    for nm, zb, sub in pumps:
        ax.add_patch(R((p_left, zb), pw, ph, fc="#B4B4BC", ec=C_OUT, lw=1.3, zorder=6))
        ax.text(pcx, zb + ph / 2 + 14, nm, ha="center", va="center", fontsize=9, fontweight="bold", zorder=8)
        ax.text(pcx, zb + ph / 2 - 20, sub, ha="center", va="center", fontsize=5.4, color="#444", zorder=8)
        tz = zb + ph / 2
        ax.add_patch(R((p_left - 15, tz - 13), 15, 26, fc="#242424", ec=C_OUT, lw=0.8, zorder=7))
        term[nm] = (p_left - 15, tz)                      # terminal left face (branch lands here)

    # ── 12V distribution block: full-width header bar (fed from the EP master switch) ──
    mcx = PW / 2
    ax.add_patch(R((6, 1866), PW - 12, 96, fc="#5A5A64", ec=C_OUT, lw=1.2, zorder=7))
    ax.text(mcx, 1930, "12V DIST. BLOCK", ha="center", va="center", fontsize=6.0,
            color="white", fontweight="bold", zorder=9)
    ax.text(mcx, 1892, "from EP master sw", ha="center", va="center", fontsize=5.0,
            color="#DADADA", zorder=9)

    # ── Circuit-C feed (switched at the EP master switch) into the block ──
    draw_pipe_path(ax, [mcx, mcx], [PH + 300, 1962], 17, 2.5, fc=CC, ec=CDK, zorder=5)
    ax.text(mcx, PH + 330, "CIRCUIT C · 14 AWG · 15A\n(switched at the EP master switch,\nvia ceiling trunk)",
            ha="center", va="bottom", fontsize=6.4, color=CC, fontweight="bold")

    # ── Curved-elbow branch conduits: block → each pump terminal. Own lane each, longest
    #    drop = outermost, so runs never cross (each stops at its pump). ──
    lanes = {"P-01": 16, "P-04": 26, "P-05": 36, "P-03": 46}
    for nm, zb, sub in pumps:
        ln = lanes[nm]
        tx, tz = term[nm]
        draw_pipe_path(ax, [ln, ln, tx], [1866, tz, tz], 12, 1.8, fc=CC, ec=CDK, zorder=4)

    # ── P-02 branch leaving the panel toward the pinhole-wall panel (short tag; detail at right) ──
    draw_pipe_path(ax, [12, -60], [1907, 1907], 12, 1.8, fc=CC, ec=CDK, zorder=4)
    ax.text(-70, 1907, "→ P-02", ha="right", va="center", fontsize=6.4, color=CDK, fontweight="bold")

    # ── Right-side callouts ──
    ax.text(PW + 90, 1500,
            "12V DIST. BLOCK — the switched\nCircuit-C feed lands here. The MASTER\npump switch (one manual cutoff for the\n"
            "whole circuit) is on the EP — see\nSheet 5. No per-pump switches; each\nShurflo 2088 runs on its internal\n"
            "pressure switch when its valves open.\n\n"
            "16 AWG branches — curved elbow\nfittings (pipe convention), one per\npump.\n\n"
            "P-02 (Brown recycle) is fed by a\nCircuit-C branch off this block, on\nthe Pinhole-Wall panel.\n\n"
            "ACC-01 is a passive accumulator —\nunpowered.",
            fontsize=6.2, ha="left", va="top", color="#333")

    # xlim encompasses ALL content — the CORRIDOR leader (left) and the notes block (right) — so the
    # transAxes title block spans the full page width (and its left cell is wide enough for the © line).
    ax.set_xlim(-431, 1433)
    ax.set_ylim(-820, PH + 470)

    # ── Notes + title block (clear band below the panel) ──
    draw_notes(ax, [
        "CIRCUIT C — PUMP POWER:",
        "The 14 AWG / 15A Circuit-C feed is switched at the MASTER pump switch on the EP (Sheet 5),",
        "runs the ceiling trunk to this panel's 12V distribution block, then a 16 AWG branch to each",
        "pump. The four corridor pumps stack in a single column (bottom→top: ACC-01, P-01, P-04, P-05,",
        "P-03); P-02 (Brown recycle) taps the switched feed on the Pinhole-Wall panel. No per-pump",
        "switches — the EP master switch is the single cutoff and each Shurflo 2088 runs on its internal",
        "pressure switch. 15A fuse covers a single pump (7.5A) with margin. Conduit branches use curved",
        "elbow fittings (pipe convention). Wet zone: sealed, above the spill line.",
        "See Plumbing Panel report §3.2 / Electrical §7.3.",
    ], -280, -80, spacing=44, fs=6.6, width=1600)

    title_block(ax, "SHEET 4 OF 7",
                drawing_title="PUMP POWER",
                subtitle="Circuit C · scale elevation",
                scale_note="1:8 · mm",
                doc_id="TBS-ELEC", height=0.075, portrait=True)

    plt.savefig(f"{DIAGRAMS_DIR}/electrical-sheet4.png", dpi=150, bbox_inches="tight",
                pad_inches=0.10, facecolor="white")
    plt.close(fig)
    print("  → electrical-sheet4.png  Done.")


def draw_sheet5():
    """SHEET 5 — Main Panel Layout + Fuse Schedule.

    TRUE-SCALE front elevation (mm, equal aspect) of the EP panel (plywood backboard; DC terminals in an IP65 enclosure) —
    mirrors the 3D model's `power_core` arrangement (MPPT, the A-G blade-fuse stack,
    +/- busbars, rotary main disconnect, Circuit-C master pump switch) — with the
    internal feed one-line and a fuse schedule. BOTH axes are real mm: panel-relative X (0 = panel left = EP_X),
    Z = real height. Component sizes/positions read from tbs_constants (same as the 3D).
    """
    from tbs_constants import (EP_H_LO, EP_H_HI, EP_W, EP_COL_W, EP_X, MPPT_W, MPPT_H,
                               FUSEBLK_W, BUSBAR_L, BUSBAR_H, DISCONNECT_D, C_BATT,
                               BA_H_LO, BA_H_HI, BA_STACK_Z2, BA_STACK_TOP, BA_W,
                               INVERTER_W, INVERTER_H, INVERTER_Z, EP_POST_Z, PV_DISC_X, PV_DISC_Z, EP_DISC_Z,
                               CONTACTOR_W, CONTACTOR_H, MRBF_D, MRBF_H)
    R = mpatches.Rectangle
    # letter, circuit name, fuse, wire, load, color (= 3D model CCT color)
    CIRCUITS5 = [
        ("A", "Vent fan — exhaust",  "5A",  "16 AWG", "60 W",   "#C0392B"),
        ("B", "Vent fan — intake",   "5A",  "16 AWG", "60 W",   "#E67E22"),
        ("C", "Plumbing panel (pumps)", "15A", "14 AWG", "100 W",  "#2980B9"),
        ("D", "Safelight",           "5A",  "18 AWG", "15 W",   "#8E44AD"),
        ("E", "Evap cooler (inv.)",  "40A", "10 AWG", f"{EVAP_COOLER_W_BUS} W",   "#16A085"),
        ("F", "Actuators (spare)",   "20A", "12 AWG", "≤100 W", "#7F8C8D"),
        ("G", "White LED panels",    "10A", "16 AWG", "60 W",   "#F1C40F"),
    ]

    fig, ax = plt.subplots(figsize=(13.5, 8.0))
    ax.set_aspect("equal")        # ← true scale: 1 mm in X == 1 mm in Z
    ax.axis("off")

    eh0, eh1 = EP_H_LO, EP_H_HI                          # 1150, 1560 (reach re-lay)
    # ── Panel outline — plywood backboard, dimensioned ──
    ax.add_patch(FancyBboxPatch((0, BA_H_LO - 12), EP_COL_W, (eh1 + 12) - (BA_H_LO - 12), boxstyle="round,pad=2",
                                fc="#F4F6F8", ec=C_OUT, lw=1.8, zorder=2))
    ax.text(EP_COL_W / 2, eh1 + 95, "EP PANEL — FRONT ELEVATION\n(reach-optimized · plywood backboard)",
            ha="center", va="bottom", fontsize=7.5, fontweight="bold", color=TITLE_COL)
    draw_dim_v(ax, EP_COL_W + 48, BA_H_LO, eh1, f"{eh1 - BA_H_LO}mm")
    draw_dim_h(ax, 0, EP_COL_W, BA_H_LO - 45, f"{EP_COL_W}mm", above=False)
    # no-stool reach ceiling reference
    ax.plot([-60, EP_COL_W + 20], [1750, 1750], color="#B03030", lw=0.7, ls=(0, (5, 3)), zorder=1)
    ax.text(-58, 1758, "no-stool reach 1750", ha="left", va="bottom", fontsize=5.0, color="#B03030")

    # ── Battery stack (bottom, set-and-forget) ──
    for _bz, _lb in [(BA_H_LO, "BAT 1"), (BA_STACK_Z2, "BAT 2")]:
        ax.add_patch(R((0, _bz), BA_W, BA_H_HI - BA_H_LO, fc=C_BATT, ec=C_OUT, lw=1.0, zorder=4))
        ax.text(BA_W / 2, _bz + (BA_H_HI - BA_H_LO) / 2, _lb, ha="center", va="center",
                fontsize=5.2, color="white", fontweight="bold", zorder=5)
    ax.text(BA_W + 8, (BA_H_LO + BA_STACK_TOP) / 2, "2x 100Ah\nstacked", ha="left", va="center", fontsize=5.0, color=C_OUT)
    # ── Contactor + MRBF ──
    ax.add_patch(R((10, EP_POST_Z), CONTACTOR_W, CONTACTOR_H, fc="#C42B1C", ec=C_OUT, lw=0.9, zorder=4))
    ax.text(10 + CONTACTOR_W / 2, EP_POST_Z + CONTACTOR_H / 2, "CONT.", ha="center", va="center", fontsize=4.5, color="white", fontweight="bold", zorder=5)
    ax.add_patch(R((CONTACTOR_W + 30, EP_POST_Z), MRBF_D, MRBF_H, fc="#222222", ec=C_OUT, lw=0.8, zorder=4))
    ax.text(CONTACTOR_W + 30 + MRBF_D / 2, EP_POST_Z + MRBF_H + 8, "MRBF", ha="center", va="bottom", fontsize=4.3, color=C_OUT)
    # ── Inverter ──
    ax.add_patch(R((0, INVERTER_Z), INVERTER_W, INVERTER_H, fc="#404848", ec=C_OUT, lw=1.0, zorder=4))
    ax.text(INVERTER_W / 2, INVERTER_Z + INVERTER_H / 2, "INVERTER\n12->120V", ha="center", va="center", fontsize=5.0, color="white", fontweight="bold", zorder=5)

    # ── Disconnect cluster (EP_DISC_Z) — main · master · PV · interior E-stop, grouped + reachable ──
    dz = EP_DISC_Z
    ax.add_patch(mpatches.Circle((55, dz + 35), DISCONNECT_D / 2, fc="#D43A2F", ec=C_OUT, lw=1.1, zorder=5))
    ax.text(55, dz + 35, "MAIN\nDISC.", ha="center", va="center", fontsize=4.2, fontweight="bold", color="white", zorder=6)
    msw_x, msw_w, msw_h = 105, 50, 84
    ax.add_patch(R((msw_x, dz), msw_w, msw_h, fc="#202020", ec=C_OUT, lw=1.1, zorder=5))
    ax.add_patch(R((msw_x + msw_w / 2 - 8, dz + 40), 16, 34, fc="#C0202A", ec=C_OUT, lw=0.7, zorder=6))
    ax.text(msw_x + msw_w / 2, dz + msw_h - 9, "MSTR", ha="center", va="center", fontsize=4.0, color="white", fontweight="bold", zorder=7)
    _pvx = PV_DISC_X - EP_X
    ax.add_patch(R((_pvx, PV_DISC_Z), 70, 70, fc="#D43A2F", ec=C_OUT, lw=1.0, zorder=5))
    ax.add_patch(R((_pvx + 28, PV_DISC_Z + 20), 14, 40, fc="#C0202A", ec=C_OUT, lw=0.7, zorder=6))
    ax.text(_pvx + 35, PV_DISC_Z + 78, "PV DISC.", ha="center", va="bottom", fontsize=4.4, color="#D43A2F", fontweight="bold", zorder=6)
    ax.add_patch(mpatches.Circle((300, dz + 25), 16, fc="#C42B1C", ec="#F2C200", lw=2.0, zorder=5))
    ax.text(300, dz + 25, "E", ha="center", va="center", fontsize=4.6, color="white", fontweight="bold", zorder=6)
    ax.plot([20, 320], [dz - 8, dz - 8], color=C_OUT, lw=0.6, ls=(0, (3, 2)), zorder=3)
    ax.text(170, dz - 14, "↑ reachable disconnect cluster", ha="center", va="top", fontsize=5.0, color=C_OUT, fontweight="bold", zorder=6)

    # ── IP65 enclosure (fuse block 5026 + busbars + charge fuse) at chest height ──
    ax.add_patch(R((10, eh0), 200, 220, fc="none", ec="#8A9AA8", lw=1.0, ls=(0, (4, 2)), zorder=3))
    ax.text(12, eh0 + 224, "IP65 enclosure", ha="left", va="bottom", fontsize=5.0, color="#8A9AA8")
    fb_x0, base_z = 15, eh0 + 40                          # 1190
    fbase_h, fuse_h = 28, 42
    ax.add_patch(R((fb_x0, base_z), FUSEBLK_W, fbase_h, fc="#2B2B30", ec=C_OUT, lw=0.9, zorder=4))
    pitch = FUSEBLK_W / len(CIRCUITS5)
    bw = pitch * 0.55
    for i, (lt, nm, fz, wr, ld, col) in enumerate(CIRCUITS5):
        cx = fb_x0 + (i + 0.5) * pitch
        ax.add_patch(R((cx - bw / 2, base_z + fbase_h), bw, fuse_h, fc=col, ec=C_OUT, lw=0.7, zorder=5))
        ax.text(cx, base_z + fbase_h + fuse_h / 2, lt, ha="center", va="center", fontsize=5.0, fontweight="bold", color="white", zorder=6)
    ax.text(fb_x0 + FUSEBLK_W / 2, base_z + fbase_h + fuse_h + 6, "↑ A–G → loads", ha="center", va="bottom", fontsize=5.0, color=C_OUT, fontweight="bold")
    ax.text(fb_x0 + FUSEBLK_W / 2, base_z - 8, "Blue Sea 5026 · 12-circ (7 used + 5 spare) · flip cover", ha="center", va="top", fontsize=4.4, color=C_OUT)
    bbp, bbn = eh0 + 170, eh0 + 140
    ax.add_patch(R((15, bbp), BUSBAR_L, BUSBAR_H, fc="#C0392B", ec=C_OUT, lw=0.7, zorder=4))
    ax.add_patch(R((15, bbn), BUSBAR_L, BUSBAR_H, fc="#2C2C2C", ec=C_OUT, lw=0.7, zorder=4))
    ax.text(15 + BUSBAR_L / 2, bbp + BUSBAR_H / 2, "+", ha="center", va="center", fontsize=6, color="white", fontweight="bold", zorder=5)
    ax.text(15 + BUSBAR_L / 2, bbn + BUSBAR_H / 2, "−", ha="center", va="center", fontsize=6, color="white", fontweight="bold", zorder=5)
    ax.text(15 + BUSBAR_L + 6, (bbp + bbn) / 2 + BUSBAR_H / 2, "± busbars", ha="left", va="center", fontsize=5.2, color=C_OUT)
    ax.add_patch(R((150, eh0 + 155), 45, 45, fc="#222222", ec=C_OUT, lw=0.7, zorder=5))
    ax.text(172, eh0 + 155 + 22, "60A\nchg", ha="center", va="center", fontsize=3.8, color="white", zorder=6)

    # ── MPPT (top of the reachable stack — was ~1970) ──
    mz = eh1 - MPPT_H                                     # 1460
    ax.add_patch(R((15, mz), MPPT_W, MPPT_H, fc="#3A5BA0", ec=C_OUT, lw=1.1, zorder=4))
    ax.text(15 + MPPT_W / 2, mz + MPPT_H / 2, "MPPT 100/50\n(display)", ha="center", va="center", fontsize=6.0, fontweight="bold", color="white", zorder=5)
    varrow(ax, 60, eh1 + 30, mz + MPPT_H, col=C_GND)
    ax.text(60, eh1 + 36, "PV IN · 10 AWG", ha="center", va="bottom", fontsize=5.6, color=C_GND, fontweight="bold")

    # ── feed one-line ──
    varrow(ax, 55, BA_STACK_TOP + 8, dz + 35 - DISCONNECT_D / 2, col="#8B1A1A", lw=1.5)   # batt(+) → main disc
    ax.text(80, (BA_STACK_TOP + dz) / 2, "(+) 2/0 · MRBF 200A", ha="left", va="center", fontsize=4.6, color="#8B1A1A", fontweight="bold", rotation=90)
    ax.plot([55, 55, 15], [dz + 35 + DISCONNECT_D / 2, bbp + 70, bbp + BUSBAR_H], color="#8B1A1A", lw=1.3, zorder=3)  # disc → +bus
    ax.text(24, bbp + 80, "→ (+) bus", ha="left", va="bottom", fontsize=4.6, color="#8B1A1A")
    c_cx = fb_x0 + 2.5 * pitch                            # Cct-C blade
    ax.plot([c_cx, c_cx, msw_x + msw_w / 2], [base_z, dz + msw_h, dz + msw_h], color="#2980B9", lw=1.3, zorder=3)  # fuse C → master sw
    varrow(ax, msw_x + msw_w / 2, dz + msw_h, eh1 + 18, col="#2980B9", lw=1.4)
    ax.text(msw_x + msw_w / 2 + 6, eh1 + 14, "→ ceiling → pumps (Sheet 4)", ha="left", va="top", fontsize=5.0, color="#2980B9", fontweight="bold")

    # ── Fuse schedule table (right, same mm coordinate space) ──
    tx = 400
    th = eh1 - 50                                        # header Z
    ax.text(tx, eh1 + 80, "FUSE SCHEDULE — BLUE SEA 5026  (Cct A–G)", ha="left",
            va="bottom", fontsize=8.5, fontweight="bold", color=TITLE_COL)
    cols = [(tx + 55, "POS", "center"), (tx + 100, "CIRCUIT", "left"),
            (tx + 400, "FUSE", "center"), (tx + 540, "WIRE", "center"), (tx + 700, "LOAD", "center")]
    for cxt, label, hh in cols:
        ax.text(cxt, th, label, ha=hh, va="center", fontsize=7.0, fontweight="bold", color=C_OUT)
    ax.plot([tx - 20, tx + 790], [th - 28, th - 28], color=C_OUT, lw=1.0)
    row_h = 72
    for i, (lt, nm, fz, wr, ld, col) in enumerate(CIRCUITS5):
        ry = th - 60 - i * row_h
        ax.add_patch(R((tx - 5, ry - 16), 34, 32, fc=col, ec=C_OUT, lw=0.7))
        ax.text(tx + 55, ry, lt, ha="center", va="center", fontsize=7.0, fontweight="bold")
        ax.text(tx + 100, ry, nm, ha="left", va="center", fontsize=6.6)
        ax.text(tx + 400, ry, fz, ha="center", va="center", fontsize=6.8, fontweight="bold")
        ax.text(tx + 540, ry, wr, ha="center", va="center", fontsize=6.4)
        ax.text(tx + 700, ry, ld, ha="center", va="center", fontsize=6.4)
    botline = th - 60 - len(CIRCUITS5) * row_h + 36
    ax.plot([tx - 20, tx + 790], [botline, botline], color=C_OUT, lw=0.8)
    ax.text(tx, botline - 44,
            "Feed: Battery (+) → 200A MRBF → main disconnect (Blue Sea m-Series) → (+) busbar → fuse block.\n"
            "Circuit C is switched at the on-panel MASTER PUMP SWITCH before it leaves for the pumps (Sheet 4).\n"
            "Charge: PV array → MPPT 100/50 → busbars.  Layout mirrors the 3D model; ratings per Sheet 1.",
            ha="left", va="top", fontsize=6.2, color="#333")

    ax.set_xlim(-70, 1230)
    ax.set_ylim(80, 1720)

    title_block(ax, "SHEET 5 OF 7",
                drawing_title="MAIN PANEL — LAYOUT",
                subtitle="True-scale front elevation · feed one-line · fuse schedule",
                scale_note="True scale · mm (equal aspect)",
                doc_id="TBS-ELEC", height=0.07)

    plt.savefig(f"{DIAGRAMS_DIR}/electrical-sheet5.png", dpi=150, bbox_inches="tight",
                pad_inches=0.10, facecolor="white")
    plt.close(fig)
    print("  → electrical-sheet5.png  Done.")




def draw_sheet6():
    """External Power Panel — folded in from the retired generate_power_panel_diagram.py
    (2026-06). Palette + layout constants are LOCAL here so the drawing is byte-identical
    regardless of this module's module-level palette (e.g. C_DIM differs between the two)."""
    C_OUT   = "#1A1A1A"
    C_DIM   = "#404040"
    C_CL    = "#2060A0"
    C_STEEL = "#B0B0B8"
    C_ALUM  = "#C8D8E8"
    C_BOX   = "#E8E0C8"      # panel face plate fill
    C_NEMA  = "#FFF0CC"       # NEMA inlet fill
    C_MC4   = "#2D7A2D"       # MC4 connector color (solar green)
    C_AC    = "#A07820"       # AC shore power color
    C_WALL  = "#C0C0C8"       # container wall
    C_GASKT = "#5A3020"       # gasket / neoprene
    C_INT   = "#F0FFF0"       # interior zone
    FONT    = {"fontfamily": "monospace"}

    # ── Panel dimensions (mm) ───────────────────────────────────────────────────
    PLATE_W  = PWR_PANEL_W         # 300mm face plate
    PLATE_H  = PWR_PANEL_H         # 200mm face plate
    PLATE_T  = PWR_PANEL_D         # 3mm aluminum plate thickness
    CUT_W    = PWR_PANEL_CUTOUT_W  # 280mm wall cutout
    CUT_H    = PWR_PANEL_CUTOUT_H  # 180mm wall cutout
    WALL_T   = 3                   # container wall thickness (corrugated steel)
    GASKET_T = 3                   # neoprene gasket thickness
    MOUNT_HOLE_D = 6               # mounting bolt hole diameter
    MOUNT_INSET  = 15              # mounting hole inset from plate edge

    # MC4 connector layout
    MC4_R    = 8              # MC4 bulkhead connector radius
    MC4_X    = 70             # MC4 column X from panel left edge
    MC4_GAP  = 25             # gap between + and - in a pair
    MC4_PITCH = 55            # vertical pitch between pairs
    MC4_DEPTH = 40            # MC4 bulkhead protrusion behind plate (mm)

    # NEMA inlet
    NEMA_W   = 55             # NEMA receptacle width
    NEMA_H   = 45             # NEMA receptacle height
    NEMA_X   = 195            # NEMA left edge from panel left edge
    NEMA_Y   = 153            # NEMA bottom edge — center aligns with PV3 (175mm)
    NEMA_DEPTH = 45           # NEMA body protrusion behind plate (mm)

    # Deutsch DT 2-pin bulkhead (Circuit E — evap cooler DC output)
    DT_R     = 10             # connector body radius (mm)
    DT_X     = 230            # center X from panel left edge
    DT_Y     = 65             # center Y — aligns with PV1 (65mm)
    DT_DEPTH = 30             # body protrusion behind plate (mm)
    C_DT     = "#E8884A"      # orange — matches pump/cooler circuit color

    # Emergency cut-off (E-stop) — external battery kill; trips the battery contactor
    ESTOP_X      = 150        # center X from panel left edge (open plate center)
    ESTOP_Y      = 100        # center Y — plate vertical center
    ESTOP_R      = 20         # red mushroom dome radius (≈40mm button)
    ESTOP_RING_R = 26         # safety-yellow collar radius
    ESTOP_DEPTH  = 55         # contact-block protrusion behind plate (mm)
    C_ESTOP      = "#C42B1C"  # emergency red
    C_ESTOP_RING = "#F2C200"  # safety yellow collar

    fig = plt.figure(figsize=(22, 15))
    fig.patch.set_facecolor("white")

    gs = fig.add_gridspec(2, 2, width_ratios=[1, 1], height_ratios=[3, 1.2],
                          hspace=0.25, wspace=0.3,
                          left=0.05, right=0.95, top=0.92, bottom=0.08)

    # ═════════════════════════════════════════════════════════════════════════
    # VIEW A — Front Elevation (panel face, exterior view)
    # ═════════════════════════════════════════════════════════════════════════
    ax_a = fig.add_subplot(gs[0, 0])
    ax_a.set_aspect("equal")
    ax_a.axis("off")


    pad = 80
    ax_a.set_xlim((-pad), (PLATE_W + pad))
    ax_a.set_ylim((-pad), (PLATE_H + pad))

    # Face plate outline (aluminum, flat — no rounded box since it's a plate)
    draw_rect(ax_a, (0), (0), (PLATE_W), (PLATE_H),
              fc=C_ALUM, color=C_OUT, lw=2.0, zorder=3)

    # Wall cutout visible behind plate (dashed, centered)
    cut_off_x = (PLATE_W - CUT_W) / 2
    cut_off_y = (PLATE_H - CUT_H) / 2
    ax_a.add_patch(mpatches.Rectangle(
        ((cut_off_x), (cut_off_y)), (CUT_W), (CUT_H),
        fc="none", ec=C_DIM, lw=1.0, ls="--", zorder=4))
    ax_a.text((PLATE_W - cut_off_x - 5), (cut_off_y + 5),
              "WALL CUTOUT\n(HIDDEN)", ha="right", va="bottom",
              fontsize=5.5, color=C_DIM, style="italic", **FONT, zorder=4)

    # Mounting holes (4 corners)
    for mx, my in [(MOUNT_INSET, MOUNT_INSET),
                   (PLATE_W - MOUNT_INSET, MOUNT_INSET),
                   (MOUNT_INSET, PLATE_H - MOUNT_INSET),
                   (PLATE_W - MOUNT_INSET, PLATE_H - MOUNT_INSET)]:
        draw_circle(ax_a, (mx), (my), (MOUNT_HOLE_D / 2),
                     lw=0.8, color=C_DIM, zorder=5)

    # MC4 bulkhead connectors — 3 pairs on left side
    mc4_y_base = PLATE_H / 2 - MC4_PITCH
    for i in range(3):
        cy = mc4_y_base + i * MC4_PITCH
        cx_pos = MC4_X - MC4_GAP / 2
        draw_circle(ax_a, (cx_pos), (cy), (MC4_R),
                     lw=1.5, color=C_MC4, fill=True, fc="#C0E8C0", zorder=5)
        ax_a.text((cx_pos), (cy), "+", ha="center", va="center",
                  fontsize=8, fontweight="bold", color=C_MC4, zorder=6)
        cx_neg = MC4_X + MC4_GAP / 2
        draw_circle(ax_a, (cx_neg), (cy), (MC4_R),
                     lw=1.5, color=C_MC4, fill=True, fc="#E0E0E0", zorder=5)
        ax_a.text((cx_neg), (cy), "−", ha="center", va="center",
                  fontsize=8, fontweight="bold", color=C_DIM, zorder=6)
        ax_a.text((MC4_X + MC4_GAP / 2 + MC4_R + 8), (cy),
                  f"PV{i + 1}", ha="left", va="center",
                  fontsize=7, color=C_MC4, fontweight="bold", **FONT, zorder=6)

    # NEMA 5-15R inlet — right side
    nema_cx = NEMA_X + NEMA_W / 2
    nema_cy = NEMA_Y + NEMA_H / 2
    ax_a.add_patch(mpatches.FancyBboxPatch(
        ((NEMA_X), (NEMA_Y)), (NEMA_W), (NEMA_H),
        boxstyle="round,pad=3", fc=C_NEMA, ec=C_OUT, lw=1.5, zorder=5))
    slot_w, slot_h = 4, 14
    slot_gap = 18
    for dx in [-slot_gap / 2, slot_gap / 2]:
        ax_a.add_patch(mpatches.Rectangle(
            ((nema_cx + dx - slot_w / 2), (nema_cy + 2)),
            (slot_w), (slot_h),
            fc="white", ec=C_OUT, lw=1.0, zorder=6))
    ground_r = 5
    theta = np.linspace(np.pi, 2 * np.pi, 20)
    gx = (nema_cx) + (ground_r) * np.cos(theta)
    gy = (nema_cy - 6) + (ground_r) * np.sin(theta)
    ax_a.plot(gx, gy, color=C_OUT, lw=1.0, zorder=6)

    # Deutsch DT 2-pin bulkhead — Circuit E (evap cooler DC output)
    draw_circle(ax_a, (DT_X), (DT_Y), (DT_R),
                 lw=1.5, color=C_DT, fill=True, fc="#FFE0C0", zorder=5)
    ax_a.text((DT_X), (DT_Y), "E", ha="center", va="center",
              fontsize=7, fontweight="bold", color=C_DT, zorder=6)

    # Emergency cut-off (E-stop) — red mushroom on safety-yellow collar
    draw_circle(ax_a, (ESTOP_X), (ESTOP_Y), (ESTOP_RING_R),
                 lw=1.5, color=C_OUT, fill=True, fc=C_ESTOP_RING, zorder=5)
    draw_circle(ax_a, (ESTOP_X), (ESTOP_Y), (ESTOP_R),
                 lw=1.5, color="#7A1810", fill=True, fc=C_ESTOP, zorder=6)
    # raised-dome highlight (upper-left)
    draw_circle(ax_a, (ESTOP_X - 5), (ESTOP_Y + 5), (ESTOP_R * 0.45),
                 lw=0, color=C_ESTOP, fill=True, fc="#E05646", zorder=7)
    ax_a.text((ESTOP_X), (ESTOP_Y - ESTOP_RING_R - 5), "STOP",
              ha="center", va="top", fontsize=6.5, fontweight="bold",
              color="#7A1810", zorder=7, **FONT)

    # Title
    ax_a.text((PLATE_W / 2), (PLATE_H + 55),
              "VIEW A — FRONT ELEVATION (EXTERIOR FACE)",
              ha="center", va="bottom", fontsize=9, fontweight="bold",
              color=C_OUT, **FONT)

    # Dimensions
    draw_dim_h(ax_a, (0), (PLATE_W), (-30),
               f"{PLATE_W}mm", offset=(8), fs=7, above=False, font=FONT)
    draw_dim_v(ax_a, (-30), (0), (PLATE_H),
               f"{PLATE_H}mm", offset=(8), fs=7, font=FONT)

    # Leaders
    leader(ax_a, (MC4_X), (mc4_y_base + 2 * MC4_PITCH + MC4_R + 5),
           (MC4_X - 25), (PLATE_H + 35),
           "SOLAR PV INPUTS (×3 PAIRS)\n3×200W array (parallel) → MPPT\nIP67 MC4 bulkheads",
           fs=6.5, color=C_MC4, ha="center", arrow_style="-|>", font=FONT)

    leader(ax_a, (NEMA_X + NEMA_W + 5), (NEMA_Y + NEMA_H / 2),
           (PLATE_W + 25), (NEMA_Y + NEMA_H / 2 + 10),
           "NEMA 5-15R\nWEATHERPROOF INLET\n120V AC SHORE POWER",
           fs=6.5, color=C_AC, ha="left", arrow_style="-|>", font=FONT)

    leader(ax_a, (DT_X + DT_R + 3), (DT_Y),
           (PLATE_W + 25), (DT_Y - 25),
           "GFCI WEATHERPROOF\nAC OUTLET (120V, in-use cover)\nCIRCUIT E — COOLER",
           fs=6, color=C_DT, ha="left", arrow_style="-|>", font=FONT)

    leader(ax_a, (ESTOP_X), (ESTOP_Y + ESTOP_RING_R + 3),
           (ESTOP_X), (PLATE_H + 28),
           "EMERGENCY CUT-OFF (E-STOP)\n40mm IP66 · TRIPS BATTERY CONTACTOR",
           fs=6.5, color=C_ESTOP, ha="center", arrow_style="-|>", font=FONT)

    leader(ax_a, (PLATE_W - MOUNT_INSET + MOUNT_HOLE_D),
           (PLATE_H - MOUNT_INSET),
           (PLATE_W + 25), (PLATE_H + 30),
           f"M{MOUNT_HOLE_D} MOUNTING\nBOLTS (×4)",
           fs=6, color=C_DIM, arrow_style="-|>", font=FONT)

    # ═════════════════════════════════════════════════════════════════════════
    # VIEW B — Cross-Section Through Wall (flush-mount detail)
    # ═════════════════════════════════════════════════════════════════════════
    ax_b = fig.add_subplot(gs[0, 1])
    ax_b.set_aspect("equal")
    ax_b.axis("off")

    # Depth axis values are intentionally exaggerated for readability

    # All vertical dimensions use a consistent mm_unit so that the plate
    # (3mm thick on depth axis), bolts (M6 = 6mm shaft), cutout (180mm),
    # and plate height (200mm) are all proportionally correct.
    #
    # Depth axis (horizontal) is exaggerated for readability:
    #   plate_t_draw and wall_thick are NOT to the same scale as height.

    wall_x = 100          # wall exterior face X position
    wall_thick = 40       # exaggerated wall thickness (depth axis)
    plate_t_draw = 12     # exaggerated plate thickness (depth axis)
    gasket_t_draw = 6     # exaggerated gasket thickness (depth axis)
    conn_depth = 50       # connector body protrusion (depth axis)

    # Vertical scale: 1mm_v = real mm in the height direction
    mm_v = 0.7            # drawing units per real mm (height axis)

    # Derived vertical positions from real dimensions
    plate_h_draw = PLATE_H * mm_v         # 200mm plate height
    cut_h_draw = CUT_H * mm_v             # 180mm cutout height
    plate_bot = 0                          # plate bottom edge
    plate_top = plate_h_draw               # plate top edge
    cut_bot = (plate_h_draw - cut_h_draw) / 2   # cutout centered in plate
    cut_top = cut_bot + cut_h_draw
    mount_inset_draw = MOUNT_INSET * mm_v  # 15mm bolt inset from plate edge

    # Bolt positions (15mm from plate edge = well within plate)
    bolt_positions = [plate_bot + mount_inset_draw,
                      plate_top - mount_inset_draw]

    # Bolt dimensions (proportional to plate via mm_v)
    bolt_shaft_h = 6 * mm_v      # M6 = 6mm diameter
    bolt_head_w = 4 * mm_v * (plate_t_draw / (3 * mm_v))  # depth-axis exaggerated
    bolt_head_h = 10 * mm_v      # 10mm across-flats
    nut_w = 5 * mm_v * (plate_t_draw / (3 * mm_v))        # depth-axis exaggerated
    nut_h = 10 * mm_v            # 10mm across-flats

    sec_h = plate_h_draw
    ext_pad = 80
    int_pad = 180
    ax_b.set_xlim((-ext_pad), (wall_x + wall_thick + int_pad))
    ax_b.set_ylim((-40), (sec_h + 80))

    # Interior zone fill
    ax_b.add_patch(mpatches.Rectangle(
        ((wall_x + wall_thick), (-20)), (int_pad), (sec_h + 80),
        fc=C_INT, ec="none", alpha=0.3, zorder=1))

    # Container wall — top section (above cutout)
    hatch_rect(ax_b, (wall_x), (cut_top), (wall_thick),
               (sec_h - cut_top + 20),
               color=C_WALL, edgecolor=C_OUT, lw=1.5, alpha=1.0, zorder=3)
    # Container wall — bottom section (below cutout)
    hatch_rect(ax_b, (wall_x), (-20), (wall_thick),
               (cut_bot + 20),
               color=C_WALL, edgecolor=C_OUT, lw=1.5, alpha=1.0, zorder=3)

    # Cutout opening (clear)
    draw_rect(ax_b, (wall_x), (cut_bot), (wall_thick),
              (cut_h_draw),
              fc="white", color=C_OUT, lw=1.0, zorder=2)

    # Gasket (between plate and wall exterior face, around cutout perimeter)
    gasket_x = wall_x - gasket_t_draw
    gasket_strip_h = (plate_h_draw - cut_h_draw) / 2 + 3 * mm_v  # overlap cutout edge
    # Top gasket strip
    draw_rect(ax_b, (gasket_x), (cut_top - 3 * mm_v),
              (gasket_t_draw), (gasket_strip_h),
              fc=C_GASKT, color=C_GASKT, lw=0.8, zorder=5)
    # Bottom gasket strip
    draw_rect(ax_b, (gasket_x), (cut_bot - (gasket_strip_h - 3 * mm_v)),
              (gasket_t_draw), (gasket_strip_h),
              fc=C_GASKT, color=C_GASKT, lw=0.8, zorder=5)

    # Face plate (flush with exterior wall face)
    plate_x = gasket_x - plate_t_draw
    draw_rect(ax_b, (plate_x), (plate_bot), (plate_t_draw),
              (plate_h_draw),
              fc=C_ALUM, color=C_OUT, lw=1.5, zorder=6)

    # Connector bodies protruding through cutout into interior
    mc4_spacing = cut_h_draw / 4
    for i in range(3):
        cy = cut_bot + mc4_spacing * (i + 0.5)
        draw_rect(ax_b, (wall_x - 5), (cy - 4 * mm_v),
                  (wall_thick + conn_depth + 5), (8 * mm_v),
                  fc="#C0E8C0", color=C_MC4, lw=1.0, zorder=4)
        ax_b.plot([(wall_x + wall_thick + conn_depth),
                   (wall_x + wall_thick + int_pad - 30)],
                  [(cy), (cy)],
                  color=C_MC4, lw=1.5, zorder=5)

    # NEMA body through cutout — aligned with PV3
    nema_cy = cut_bot + mc4_spacing * 2.5
    draw_rect(ax_b, (wall_x - 5), (nema_cy - 5 * mm_v),
              (wall_thick + conn_depth + 5), (10 * mm_v),
              fc=C_NEMA, color=C_AC, lw=1.0, zorder=4)
    ax_b.plot([(wall_x + wall_thick + conn_depth),
               (wall_x + wall_thick + int_pad - 30)],
              [(nema_cy), (nema_cy)],
              color=C_AC, lw=1.5, ls="--", zorder=5)

    # Deutsch DT body through cutout (Circuit E — cooler DC output) — aligned with PV1
    dt_cy = cut_bot + mc4_spacing * 0.5
    draw_rect(ax_b, (wall_x - 5), (dt_cy - 3 * mm_v),
              (wall_thick + DT_DEPTH + 5), (6 * mm_v),
              fc="#FFE0C0", color=C_DT, lw=1.0, zorder=4)
    ax_b.plot([(wall_x + wall_thick + DT_DEPTH),
               (wall_x + wall_thick + int_pad - 30)],
              [(dt_cy), (dt_cy)],
              color=C_DT, lw=1.5, zorder=5)
    ax_b.plot([(wall_x - 5), (-ext_pad + 10)],
              [(dt_cy), (dt_cy)],
              color=C_DT, lw=1.5, ls="--", zorder=5)

    # Mounting bolts (through plate + gasket + wall, nut clamped against wall)
    washer_w = 1.5 * mm_v * (plate_t_draw / (3 * mm_v))  # washer thickness
    washer_h = 12 * mm_v     # washer OD ~12mm
    for by_pos in bolt_positions:
        # Bolt shaft — from bolt head through plate, gasket, wall to nut
        shaft_start = plate_x - bolt_head_w
        shaft_end = wall_x + wall_thick + washer_w + nut_w
        draw_rect(ax_b, (shaft_start),
                  (by_pos - bolt_shaft_h / 2),
                  (shaft_end - shaft_start),
                  (bolt_shaft_h),
                  fc=C_STEEL, color=C_OUT, lw=0.6, zorder=7)
        # Bolt head (exterior side of plate)
        draw_rect(ax_b, (plate_x - bolt_head_w),
                  (by_pos - bolt_head_h / 2),
                  (bolt_head_w), (bolt_head_h),
                  fc=C_STEEL, color=C_OUT, lw=0.8, zorder=8)
        # Washer (against interior face of wall)
        draw_rect(ax_b, (wall_x + wall_thick),
                  (by_pos - washer_h / 2),
                  (washer_w), (washer_h),
                  fc="#E0E0E0", color=C_OUT, lw=0.6, zorder=8)
        # Nut (clamped against washer, flush with interior wall face)
        draw_rect(ax_b, (wall_x + wall_thick + washer_w),
                  (by_pos - nut_h / 2),
                  (nut_w), (nut_h),
                  fc=C_STEEL, color=C_OUT, lw=0.8, zorder=8)

    # Interior destination labels
    int_label_x = wall_x + wall_thick + int_pad - 25
    ax_b.text((int_label_x), (cut_bot + mc4_spacing + 16),
              "→ MPPT", ha="left", va="center", fontsize=7,
              color=C_MC4, fontweight="bold", **FONT, zorder=7)
    ax_b.text((int_label_x), (nema_cy),
              "→ CHARGER", ha="left", va="center", fontsize=7,
              color=C_AC, fontweight="bold", **FONT, zorder=7)
    ax_b.text((int_label_x), (dt_cy),
              "← CCT E", ha="left", va="center", fontsize=7,
              color=C_DT, fontweight="bold", **FONT, zorder=7)
    ax_b.text((-ext_pad + 8), (dt_cy + 5),
              "→ COOLER", ha="left", va="bottom", fontsize=7,
              color=C_DT, fontweight="bold", **FONT, zorder=7)

    # Zone labels
    ax_b.text((plate_x - 30), (sec_h + 55),
              "EXTERIOR", ha="center", va="bottom", fontsize=9,
              fontweight="bold", color=C_DIM, **FONT)
    ax_b.text((wall_x + wall_thick + int_pad / 2), (sec_h + 55),
              "INTERIOR", ha="center", va="bottom", fontsize=9,
              fontweight="bold", color=C_DIM, **FONT)

    # Title
    ax_b.text(((wall_x + wall_thick + int_pad) / 2), (sec_h + 70),
              "VIEW B — CROSS-SECTION (FLUSH-MOUNT DETAIL)",
              ha="center", va="bottom", fontsize=9, fontweight="bold",
              color=C_OUT, **FONT)

    # Dimensions
    draw_dim_h(ax_b, (plate_x), (plate_x + plate_t_draw), (-25),
               f"{PLATE_T}mm\nPLATE", offset=(5), fs=6, above=False, font=FONT)
    draw_dim_h(ax_b, (wall_x), (wall_x + wall_thick), (-25),
               "WALL", offset=(5), fs=6, above=False, font=FONT)
    draw_dim_v(ax_b, (wall_x + wall_thick + 8), (cut_bot), (cut_top),
               f"{CUT_H}mm\nCUTOUT", offset=(5), fs=6, right=True, font=FONT)

    # Leader labels
    leader(ax_b, (gasket_x - gasket_t_draw / 2 + 3),
           (cut_top + 5),
           (gasket_x - 60), (cut_top - 5),
           "NEOPRENE GASKET\n3mm — WEATHERSEAL",
           fs=6, color=C_GASKT, ha="center", arrow_style="-|>", font=FONT)

    leader(ax_b, (plate_x + PLATE_T / 2), (cut_top + 23),
           (plate_x - 25), (sec_h + 40),
           f"ALUMINUM FACE PLATE\n{PLATE_W}×{PLATE_H}×{PLATE_T}mm\nFLUSH WITH WALL",
           fs=6, color=C_OUT, ha="center", arrow_style="-|>", font=FONT)

    leader(ax_b, (wall_x + wall_thick / 2), (-15),
           (wall_x + wall_thick / 2), (-35),
           "CONTAINER WALL\n(CORRUGATED STEEL)",
           fs=6, color=C_WALL, ha="center", va="top", arrow_style="-|>", font=FONT)

    leader(ax_b, (wall_x + wall_thick + 5), (bolt_positions[1]),
           (wall_x + wall_thick + 25), (bolt_positions[1] + 25),
           "M6 BOLT + NUT\nW/ WASHER (×4)",
           fs=6, color=C_DIM, ha="left", arrow_style="-|>", font=FONT)

    # ═════════════════════════════════════════════════════════════════════════
    # VIEW C — Simplified Wiring Schematic
    # ═════════════════════════════════════════════════════════════════════════
    ax_c = fig.add_subplot(gs[1, :])
    ax_c.set_aspect("equal")
    ax_c.axis("off")
    ax_c.set_xlim(0, 22)
    ax_c.set_ylim(-2.7, 4.5)

    ax_c.text(8.75, 4.6, "VIEW C — WIRING SCHEMATIC",
              ha="center", va="bottom", fontsize=9, fontweight="bold",
              color=C_OUT, **FONT)

    def sbox(ax, x, y, w, h, label, sublabel="", fc="white", tc=C_OUT):
        ax.add_patch(FancyBboxPatch((x, y), w, h,
                     boxstyle="round,pad=0.06", fc=fc, ec=C_OUT, lw=1.2, zorder=3))
        ax.text(x + w / 2, y + h / 2 + (0.12 if sublabel else 0), label,
                ha="center", va="center", fontsize=7.5, fontweight="bold",
                color=tc, **FONT, zorder=4)
        if sublabel:
            ax.text(x + w / 2, y + h / 2 - 0.15, sublabel,
                    ha="center", va="center", fontsize=6, color=C_DIM,
                    **FONT, zorder=4)

    def sarrow(ax, x1, y, x2, col=C_OUT, lw=1.8):
        ax.annotate("", xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=lw), zorder=3)

    row_bot = 0.8
    row_top = 2.8

    # Solar path (top row)
    sbox(ax_c, 0.5, row_top, 2.8, 0.9,
         "SOLAR PANELS", "3×200W  12V", fc="#E8F5E8", tc=C_MC4)
    sarrow(ax_c, 3.3, row_top + 0.45, 4.5, col=C_MC4)
    ax_c.text(3.9, row_top + 0.65, "MC4", fontsize=6, color=C_MC4,
              ha="center", **FONT)
    ax_c.text(3.9, row_top + 1.02, "30A fuse + 3-way\ncombiner / string", fontsize=5.0,
              color=C_MC4, ha="center", va="bottom", **FONT)

    sbox(ax_c, 4.5, row_top, 3.0, 0.9,
         "FLUSH-MOUNT PANEL", "MC4 bulkhead ×3", fc=C_ALUM)
    sarrow(ax_c, 7.5, row_top + 0.45, 10.0, col=C_MC4)
    ax_c.text(8.75, row_top + 0.65, "10 AWG PV", fontsize=6, color=C_MC4,
              ha="center", **FONT)

    sbox(ax_c, 10.0, row_top, 3.2, 0.9,
         "MPPT CONTROLLER", "Victron 100/50", fc="#FFF3CC")
    sarrow(ax_c, 13.2, row_top + 0.45, 14.5, col=C_CL)
    sbox(ax_c, 14.5, row_top - 0.3, 3.0, 1.5,
         "BATTERY 1×100Ah", "std · 2nd pack: plug-in", fc="#E0E8F8")

    # Shore power path (bottom row)
    sbox(ax_c, 0.5, row_bot, 2.8, 0.9,
         "SHORE POWER", "120V AC grid", fc=C_NEMA, tc=C_AC)
    sarrow(ax_c, 3.3, row_bot + 0.45, 4.5, col=C_AC)
    ax_c.text(3.9, row_bot + 0.65, "AC cord", fontsize=6, color=C_AC,
              ha="center", **FONT)

    sbox(ax_c, 4.5, row_bot, 3.0, 0.9,
         "FLUSH-MOUNT PANEL", "NEMA 5-15R inlet", fc=C_ALUM)
    sarrow(ax_c, 7.5, row_bot + 0.45, 10.0, col=C_AC)

    sbox(ax_c, 10.0, row_bot, 3.2, 0.9,
         "SHORE CHARGER", "Victron IP65 12/15", fc="#F5EDD0", tc=C_AC)
    # Continuous line from shore charger to battery bank
    bat_cx = 16.0
    ax_c.plot([13.2, bat_cx], [row_bot + 0.45, row_bot + 0.45],
              color=C_AC, lw=1.8, zorder=3)
    ax_c.annotate("", xy=(bat_cx, row_top - 0.3), xytext=(bat_cx, row_bot + 0.45),
                  arrowprops=dict(arrowstyle="-|>", color=C_AC, lw=1.8,
                                  connectionstyle="arc3,rad=0"), zorder=3)
    ax_c.text(bat_cx + 0.15, (row_top + row_bot) / 2 + 0.3, "12V DC\ncharge",
              fontsize=6, color=C_AC, ha="left", va="center", **FONT)

    # Cooler AC output path (bottom row — reverse direction: interior → exterior)
    row_cool = -0.4
    sbox(ax_c, 0.5, row_cool, 2.8, 0.9,
         "EVAP COOLER", f"120V AC  {EVAP_COOLER_W_AC}W", fc="#FFE0C0", tc=C_DT)
    sarrow(ax_c, 4.5, row_cool + 0.45, 3.3, col=C_DT)
    ax_c.text(3.9, row_cool + 0.65, "AC cord", fontsize=6, color=C_DT,
              ha="center", **FONT)

    sbox(ax_c, 4.5, row_cool, 3.0, 0.9,
         "PANEL GFCI OUTLET", "120V AC, in-use cover", fc=C_ALUM)
    sarrow(ax_c, 10.0, row_cool + 0.45, 7.5, col=C_DT)
    ax_c.text(8.75, row_cool + 0.65, "from inverter", fontsize=6, color=C_DT,
              ha="center", **FONT)

    sbox(ax_c, 10.0, row_cool, 3.2, 0.9,
         "INVERTER + FUSE", "12→120V · Cct E 40A DC", fc="#FFF3CC", tc=C_DT)
    sarrow(ax_c, 14.5, row_cool + 0.45, 13.2, col=C_DT)
    ax_c.plot([14.5, bat_cx], [row_cool + 0.45, row_cool + 0.45],
              color=C_DT, lw=1.8, zorder=3)
    ax_c.annotate("", xy=(bat_cx, row_top - 0.3), xytext=(bat_cx, row_cool + 0.45),
                  arrowprops=dict(arrowstyle="-|>", color=C_DT, lw=1.0,
                                  connectionstyle="arc3,rad=0"), zorder=2)

    # Emergency cut-off control path (E-stop → contactor at the battery)
    row_es = -1.7
    C_CTRL = "#6A3DA8"

    def carrow(ax, x1, y, x2, col=C_CTRL, lw=1.5):
        ax.annotate("", xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=lw,
                                    linestyle=(0, (4, 2))), zorder=3)

    sbox(ax_c, 0.5, row_es, 2.8, 0.9,
         "EMERGENCY E-STOP", "red mushroom · IP66", fc="#F6D6D2", tc=C_ESTOP)
    carrow(ax_c, 3.3, row_es + 0.45, 4.5)
    sbox(ax_c, 4.5, row_es, 3.0, 0.9,
         "FLUSH-MOUNT PANEL", "E-stop button", fc=C_ALUM)
    carrow(ax_c, 7.5, row_es + 0.45, 10.0)
    ax_c.text(8.75, row_es + 0.65, "control 2×18 AWG", fontsize=6, color=C_CTRL,
              ha="center", **FONT)
    sbox(ax_c, 10.0, row_es, 3.2, 0.9,
         "BATTERY CONTACTOR", "ML-RBS · in battery + feed", fc="#F6D6D2", tc=C_ESTOP)
    # contactor is in the main battery (+) feed — solid power link up to the bank
    ax_c.plot([13.2, bat_cx + 0.3], [row_es + 0.45, row_es + 0.45],
              color=C_OUT, lw=1.8, zorder=3)
    ax_c.annotate("", xy=(bat_cx + 0.3, row_top - 0.3), xytext=(bat_cx + 0.3, row_es + 0.45),
                  arrowprops=dict(arrowstyle="-|>", color=C_OUT, lw=1.4), zorder=2)
    ax_c.text(bat_cx + 0.45, row_es + 0.9, "main +", fontsize=5.5, color=C_OUT,
              ha="left", va="center", **FONT)

    # Container wall indicator — single line (flush mount, no gland)
    wall_x_sch = 7.45
    ax_c.plot([wall_x_sch, wall_x_sch],
              [row_es - 0.5, row_top + 1.0],
              color=C_WALL, lw=4, zorder=1)
    ax_c.text(wall_x_sch, row_es - 0.7, "CONTAINER\nWALL",
              ha="center", va="top", fontsize=6, color=C_WALL,
              fontweight="bold", **FONT)
    ax_c.text(wall_x_sch + 0.15, row_es - 0.45, "(flush-mount\n panel)",
              ha="left", va="top", fontsize=5, color=C_DIM, **FONT)

    # Zone labels
    ax_c.text(wall_x_sch / 2, row_top + 1.35, "EXTERIOR",
              ha="center", va="bottom", fontsize=8, fontweight="bold",
              color=C_DIM, **FONT)
    ax_c.text((wall_x_sch + 22) / 2, row_top + 1.35, "CONTAINER INTERIOR",
              ha="center", va="bottom", fontsize=8, fontweight="bold",
              color=C_DIM, **FONT)

    # ═════════════════════════════════════════════════════════════════════════
    # Title block
    # ═════════════════════════════════════════════════════════════════════════
    ax_tb = fig.add_axes([0.05, 0.0, 0.9, 0.08])
    ax_tb.set_xlim(0, 1)
    ax_tb.set_ylim(0, 1)
    ax_tb.axis("off")
    title_block(ax_tb, "SHEET 6 OF 7",
                drawing_title="EXTERNAL POWER PANEL — FLUSH MOUNT",
                subtitle="SOLAR + SHORE INPUT · COOLER DC OUTPUT · WIRING SCHEMATIC",
                scale_note="AXES IN mm",
                height=0.85)

    fig.savefig(f"{DIAGRAMS_DIR}/electrical-sheet6.png",
                dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  → electrical-sheet6.png  Done.")


def draw_sheet7():
    """SHEET 7 — Symbol-based system schematic (traditional EE wiring diagram).

    Complements the Sheet-1 block one-line with a standard-symbol schematic of the
    whole 12V DC system: PV → disconnect → MPPT → 60A fuse → battery → 200A MRBF →
    contactor → main disconnect → fuse block → the seven load circuits (A–G, each a
    fuse + load symbol) → negative bus → battery. The contactor coil (K1) is held in
    by the two E-stops (NC) in series; a shore charger feeds the battery; the negative
    bus is bonded to chassis earth. Not to scale — a connection schematic.
    """
    from tbs_constants import DIAGRAMS_DIR
    FT = {"fontfamily": "monospace"}
    LN, RED, BLU, GRN = "#1A1A1A", "#C0392B", "#2471A3", "#2E7D32"
    fig, ax = plt.subplots(figsize=(18, 11))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(0, 2060); ax.set_ylim(-60, 1340)
    R = mpatches.Rectangle

    def wire(pts, c=LN, lw=1.7, z=3):
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=c, lw=lw, zorder=z,
                solid_capstyle="round", solid_joinstyle="round")
    def dot(x, y, c=LN):
        ax.add_patch(mpatches.Circle((x, y), 6.5, fc=c, ec=c, zorder=6))
    def txt(x, y, t, fs=7, ha="center", va="center", c=LN, w="normal"):
        ax.text(x, y, t, ha=ha, va=va, fontsize=fs, color=c, zorder=8, fontweight=w, **FT)
    def box(x, y, w, h, label, sub="", fc="white", fs=7.5):
        ax.add_patch(mpatches.FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                     boxstyle="round,pad=0,rounding_size=7", fc=fc, ec=LN, lw=1.6, zorder=4))
        txt(x, y + (11 if sub else 0), label, fs=fs, w="bold")
        if sub:
            txt(x, y - 13, sub, fs=5.5, c="#444")

    # ── symbols ──────────────────────────────────────────────────────────────
    def fuse(x, y, rating, vert=True, lab_side="right"):
        if vert:
            ax.add_patch(R((x - 13, y - 26), 26, 52, fc="white", ec=LN, lw=1.6, zorder=5))
            ax.plot([x, x], [y - 26, y + 26], color=LN, lw=1.1, zorder=6)
            dx = 20 if lab_side == "right" else -20
            txt(x + dx, y, rating, fs=6.4, ha=("left" if lab_side == "right" else "right"), w="bold", c=RED)
        else:
            ax.add_patch(R((x - 26, y - 13), 52, 26, fc="white", ec=LN, lw=1.6, zorder=5))
            ax.plot([x - 26, x + 26], [y, y], color=LN, lw=1.1, zorder=6)
            txt(x, y + 22, rating, fs=6.4, w="bold", c=RED)
    def disconnect(x, y, label=""):                       # open-able isolator (vertical)
        dot(x, y - 22); ax.plot([x, x - 18], [y - 22, y + 20], color=LN, lw=2.0, zorder=5); dot(x, y + 22)
        if label:
            txt(x - 28, y, label, fs=6, ha="right")
    def contactor(x, y):                                  # NO power contact of K1 (vertical)
        dot(x, y - 22); ax.plot([x, x - 18], [y - 22, y + 20], color=LN, lw=2.0, zorder=5); dot(x, y + 22)
        ax.plot([x - 9, x - 9], [y - 4, y + 8], color=LN, lw=0.9, ls=(0, (2, 2)), zorder=5)  # actuation tie
        txt(x - 30, y + 26, "K1", fs=6.3, ha="right", w="bold")
    def battery(x, y):
        yy = y + 34
        for w, lw in [(38, 1.2), (18, 3.2), (38, 1.2), (18, 3.2)]:
            ax.plot([x - w / 2, x + w / 2], [yy, yy], color=LN, lw=lw, zorder=5); yy -= 19
        wire([(x, y + 34), (x, y + 60)]); wire([(x, y - 40), (x, y - 62)])
        txt(x + 34, y + 50, "+", fs=11, w="bold"); txt(x + 34, y - 52, "−", fs=11, w="bold")
        txt(x, y - 96, "BATTERY", fs=7, w="bold"); txt(x, y - 114, "100Ah 12V LiFePO₄", fs=5.6, c="#444")
    def estop(x, y):                                      # NC pushbutton (horizontal contact)
        dot(x - 22, y); dot(x + 22, y)
        ax.plot([x - 22, x + 14], [y, y + 12], color=LN, lw=2.0, zorder=5)   # NC blade (opens on push)
        ax.plot([x, x], [y + 8, y + 30], color=RED, lw=1.7, zorder=5)        # actuator stem
        ax.add_patch(mpatches.FancyBboxPatch((x - 17, y + 30), 34, 11, boxstyle="round,pad=0,rounding_size=5",
                     fc=RED, ec=LN, lw=1.0, zorder=6))
    def coil(x, y, label="K1"):
        ax.add_patch(R((x - 17, y - 22), 34, 44, fc="white", ec=LN, lw=1.6, zorder=5))
        txt(x, y, label, fs=7, w="bold")
    def motor(x, y, letter="M", fc="white"):
        ax.add_patch(mpatches.Circle((x, y), 27, fc=fc, ec=LN, lw=1.6, zorder=5)); txt(x, y, letter, fs=9.5, w="bold")
    def lamp(x, y):
        ax.add_patch(mpatches.Circle((x, y), 27, fc="#FFF6C8", ec=LN, lw=1.6, zorder=5))
        ax.plot([x - 19, x + 19], [y - 19, y + 19], color=LN, lw=1.2, zorder=6)
        ax.plot([x - 19, x + 19], [y + 19, y - 19], color=LN, lw=1.2, zorder=6)
    def ground(x, y):
        wire([(x, y), (x, y - 20)])
        for i, w in enumerate([30, 19, 9]):
            ax.plot([x - w / 2, x + w / 2], [y - 20 - i * 7, y - 20 - i * 7], color=LN, lw=2.0, zorder=5)

    # ── title ──────────────────────────────────────────────────────────────
    txt(1030, 1305, "SYSTEM SCHEMATIC — 12V DC OFF-GRID (SYMBOL DIAGRAM)", fs=13, w="bold", c=BLU)
    txt(1030, 1275, "TBS-001 · negative-grounded · one battery bank shown · all loads 12V DC (Circuit E via inverter)", fs=7, c="#444")

    # ═══ GENERATION + CHARGE CHAIN (left, vertical) ═══
    GX = 210
    box(GX, 1150, 150, 74, "PV ARRAY", "3×200W · Isc 30A", fc="#DFF0D8")
    wire([(GX, 1113), (GX, 1076)]); disconnect(GX, 1054, "PV\nDISC")
    txt(GX + 26, 1054, "50A", fs=6, ha="left", c=RED)
    wire([(GX, 1032), (GX, 992)]); box(GX, 950, 150, 66, "MPPT", "Victron 100/50", fc="#FCF3CF")
    wire([(GX, 917), (GX, 852)]); fuse(GX, 826, "60A")
    wire([(GX, 800), (GX, 726)]); txt(GX - 90, 763, "6 AWG", fs=5.6, ha="right", c="#666")

    # ═══ BATTERY + PROTECTION (center) ═══
    BX, BY = 470, 640
    battery(BX, BY)
    # charge line: 60A fuse → battery +
    wire([(GX, 726), (GX, 700), (BX, 700)]); dot(BX, 700); wire([(BX, 700), (BX, BY + 60)])
    # discharge / protection chain along the top of the battery + (horizontal)
    PY = 700
    wire([(BX, PY), (610, PY)]); fuse(636, PY, "200A", vert=False)
    txt(636, PY + 40, "MRBF", fs=5.6, c="#666")
    wire([(662, PY), (742, PY)]); contactor(768, PY)
    wire([(794, PY), (874, PY)]); disconnect(900, PY, "MAIN")
    wire([(926, PY), (1000, PY)]); dot(1000, PY)
    wire([(1000, PY), (1000, 1150)])                        # rise to the positive bus
    # negative return
    wire([(BX, BY - 62), (BX, 250)]); dot(BX, 250)
    ground(BX + 130, 250); wire([(BX, 250), (BX + 130, 250)]); dot(BX + 130, 250)
    txt(BX + 150, 232, "CHASSIS EARTH\n8ft stake + body bond", fs=5.6, ha="left", va="top")

    # ═══ E-STOP CONTROL LOOP (holds K1 coil in) ═══
    CLY = 470
    wire([(768, PY), (768, CLY + 22)])                     # tap control power near the contactor
    wire([(768, CLY + 22), (768, CLY)]); dot(768, CLY - 0)
    estop(720, CLY); estop(632, CLY)
    wire([(768, CLY), (742, CLY)]); wire([(698, CLY), (654, CLY)]); wire([(610, CLY), (556, CLY)])
    coil(556, CLY, "K1"); wire([(556, CLY - 22), (556, 250), (BX, 250)])
    txt(540, 402, "E-STOP LOOP — 2× NC in series;\neither press drops K1 (opens the contactor)",
        fs=5.6, c=RED, w="bold", ha="left", va="top")

    # ═══ SHORE CHARGER (optional AC backup) ═══
    box(230, 470, 190, 66, "SHORE CHARGER", "Victron IP65 12/15", fc="#F5E9C8")
    txt(120, 470, "AC~", fs=8, w="bold"); wire([(135, 470), (135, 470)]); dot(135, 470); wire([(135, 470), (135, 470)])
    ax.plot([128, 142], [470, 470], color=LN, lw=1.6, zorder=3)
    wire([(325, 470), (360, 470), (360, 700)]); dot(360, 700)   # DC out → charge node

    # ═══ POSITIVE BUS + FUSE BLOCK + 7 LOAD CIRCUITS (right) ═══
    BUS_Y, NEG_Y = 1150, 250
    BUS_X0, BUS_X1 = 1000, 1980
    wire([(BUS_X0, BUS_Y), (BUS_X1, BUS_Y)], lw=2.4)        # positive bus
    wire([(BX + 130, NEG_Y), (BUS_X1, NEG_Y)], lw=2.4)      # negative bus
    txt(BUS_X0 + 6, BUS_Y + 20, "BLUE SEA 5026 FUSE BLOCK  (+ bus)", fs=6.4, ha="left", w="bold")
    txt(BUS_X1, NEG_Y - 20, "NEGATIVE BUS  (− return)", fs=6.4, ha="right")
    circuits = [
        ("A", "5A", "16", "EXHAUST FAN", "M"), ("B", "5A", "16", "INTAKE FAN", "M"),
        ("C", "15A", "14", "PUMPS (panel)", "M"), ("D", "5A", "18", "SAFELIGHT", "L"),
        ("E", "40A", "10", "EVAP COOLER", "INV"), ("F", "20A", "12", "FP ACTUATORS", "M"),
        ("G", "10A", "16", "WHITE LED", "L"),
    ]
    xs = [1110, 1235, 1360, 1485, 1610, 1735, 1860]
    for (c, fu, awg, name, kind), x in zip(circuits, xs):
        dot(x, BUS_Y)
        wire([(x, BUS_Y), (x, 1090)]); fuse(x, 1064, fu)
        txt(x, 1112, c, fs=9, w="bold", c=BLU)
        wire([(x, 1038), (x, 690)])
        txt(x + 16, 950, f"{awg} AWG", fs=5.2, ha="left", c="#666")
        if kind == "M":
            motor(x, 640); nb = 613
        elif kind == "L":
            lamp(x, 640); nb = 613
        else:                                               # inverter → AC load
            box(x, 700, 96, 44, "INV", "12→120V", fc="#EBF5FB", fs=6); motor(x, 590, "M", fc="#EBF5FB"); nb = 563
            wire([(x, 678), (x, 617)])
        wire([(x, 640 if kind != "INV" else 590), (x, 640 if kind != "INV" else 590)])
        wire([(x, nb), (x, NEG_Y)]); dot(x, NEG_Y)
        txt(x, 686 if kind != "INV" else 740, name, fs=5.4, va="bottom")

    # ── legend of symbols ──
    lx, ly = 70, 150
    ax.add_patch(R((lx - 20, ly - 130), 470, 150, fc="#FBFBFB", ec="#BBB", lw=1.0, zorder=2))
    txt(lx - 10, ly + 2, "SYMBOLS:", fs=6.6, ha="left", w="bold")
    fuse(lx + 20, ly - 34, "", vert=True); txt(lx + 44, ly - 34, "fuse", fs=6, ha="left")
    disconnect(lx + 150, ly - 34); txt(lx + 172, ly - 34, "isolator", fs=6, ha="left")
    contactor(lx + 300, ly - 34); txt(lx + 322, ly - 34, "contactor K1", fs=6, ha="left")
    motor(lx + 30, ly - 96, "M"); txt(lx + 66, ly - 96, "motor (fan/pump)", fs=6, ha="left")
    lamp(lx + 260, ly - 96); txt(lx + 296, ly - 96, "lamp (LED/safelight)", fs=6, ha="left")

    # title block
    ax_tb = fig.add_axes([0.05, -0.02, 0.9, 0.06])
    ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis("off")
    title_block(ax_tb, "SHEET 7 OF 7", drawing_title="SYSTEM SCHEMATIC (SYMBOL DIAGRAM)",
                subtitle="Full-system EE schematic · protection · E-stop loop · 7 load circuits",
                scale_note="Not to scale", height=0.85)
    fig.savefig(f"{DIAGRAMS_DIR}/electrical-sheet7.png", dpi=150, bbox_inches="tight",
                pad_inches=0.12, facecolor="white")
    plt.close(fig)
    print("  → electrical-sheet7.png  Done.")


if __name__ == "__main__":
    print("Generating TBS-001 Electrical & Systems diagrams...")
    draw_sheet1()
    draw_sheet2()
    draw_sheet3()
    draw_sheet4()
    draw_sheet5()
    draw_sheet6()
    draw_sheet7()
    print("Done.")
