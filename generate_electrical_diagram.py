#!/usr/bin/env python3
"""
generate_electrical_diagram.py
TBS-001 Electrical & Systems — two engineering drawing sheets.

Sheet 1: System one-line diagram (power flow, components, fuse ratings)
Sheet 2: Container floor plan with wiring layout  (scale 1:500)
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Arc

# ── Palette ───────────────────────────────────────────────────────────────────
C_OUT   = "#1A1A1A"
C_CL    = "#2060A0"
C_DIM   = "#505050"
C_ALUM  = "#C8D8E8"
C_STEEL = "#B0B0B8"
C_ELEC  = "#FFF3CC"
C_SOLAR = "#D4EDDA"
C_BATT  = "#CCE5FF"
C_WARN  = "#F8D7DA"
C_GND   = "#2C5F2E"
C_PIPE  = "#6C757D"
TITLE_COL = "#0F2D5E"


# ── Shared helpers ────────────────────────────────────────────────────────────

def rbox(ax, x, y, w, h, title, subtitle="", fc=C_ELEC, ec=C_OUT, lw=1.4,
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


def title_block(ax, FW, sheet_n, sheet_total, title1, title2, scale_str):
    tb_y, tb_h = 0.05, 0.65
    ax.add_patch(mpatches.Rectangle((0.25, tb_y), FW - 0.5, tb_h,
                                    fc="white", ec=C_OUT, lw=1.5, zorder=6))
    for xd in [FW * 0.30, FW * 0.70]:
        ax.plot([xd, xd], [tb_y, tb_y + tb_h], color=C_OUT, lw=0.8, zorder=7)

    ax.text(FW * 0.15, tb_y + 0.44, "THE BIG SHOEBOX PROJECT",
            ha="center", va="center", fontsize=8.0, fontweight="bold",
            color=TITLE_COL, zorder=7)
    ax.text(FW * 0.15, tb_y + 0.28, "TBS-ELEC  ·  Electrical & Systems",
            ha="center", va="center", fontsize=7.0, color=C_DIM, zorder=7)
    ax.text(FW * 0.15, tb_y + 0.14, "TBS-001  ·  20FT ISO CAMERA  ·  12V DC",
            ha="center", va="center", fontsize=6.5, color=C_DIM, zorder=7)

    ax.text(FW * 0.50, tb_y + 0.45, title1,
            ha="center", va="center", fontsize=11.0, fontweight="bold",
            color=C_OUT, zorder=7)
    ax.text(FW * 0.50, tb_y + 0.27, title2,
            ha="center", va="center", fontsize=7.5, color=C_DIM, zorder=7)
    ax.text(FW * 0.50, tb_y + 0.13, f"Scale: {scale_str}",
            ha="center", va="center", fontsize=7.0, color=C_DIM, zorder=7)

    ax.text(FW * 0.85, tb_y + 0.44, f"Sheet {sheet_n} of {sheet_total}",
            ha="center", va="center", fontsize=9.5, fontweight="bold",
            color=C_OUT, zorder=7)
    ax.text(FW * 0.85, tb_y + 0.27, "2026",
            ha="center", va="center", fontsize=8.0, color=C_DIM, zorder=7)


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
         fc=C_ELEC, ts=9.5, ss=8.0)
    varrow(ax, CX, 12.0, 11.2, col=C_SOLAR)
    wlabel(ax, CX + 0.18, 11.6, "10 AWG PV cable  |  MC4 connectors")

    # 3. Battery bank  y=8.4–9.5
    rbox(ax, LX, 8.4, LW, 1.1,
         "BATTERY BANK — 200Ah / 2,400Wh",
         "2 × 100Ah 12V LiFePO4 in parallel  |  100% DoD usable  |  Safe to 60 °C",
         fc=C_BATT, ts=9.5, ss=8.0)
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
         "NEMA 5-15R INLET  (exterior short wall — vestibule end)",
         "Weatherproof  |  Shore power input when mains available",
         fc="white", ec=C_OUT, lw=1.0, ts=8.5, ss=7.5, bold=False)
    varrow(ax, SC_X + SC_W / 2, SC_Y - 0.55, SC_Y, col="#A07820")
    wlabel(ax, SC_X + SC_W / 2 + 0.15, SC_Y - 0.28, "Shore AC →", size=7.0)

    # ── LEGEND ────────────────────────────────────────────────────────────────
    lx, ly = SC_X, 1.1
    ax.add_patch(FancyBboxPatch((lx - 0.1, ly - 0.15), SC_W + 0.2, 3.6,
                 boxstyle="round,pad=0.05", fc="#F8F9FA", ec=C_DIM, lw=0.8, zorder=2))
    ax.text(lx + SC_W / 2, ly + 3.28, "LEGEND",
            ha="center", va="center", fontsize=9.5,
            fontweight="bold", color=C_OUT)
    ax.plot([lx + 0.1, lx + SC_W - 0.1], [ly + 3.05, ly + 3.05],
            color=C_DIM, lw=0.7)
    legend_items = [
        (C_SOLAR,   "Solar / generation"),
        (C_BATT,    "Battery / storage"),
        (C_ELEC,    "Controller / charger"),
        (C_WARN,    "Fuse / protection device"),
        (C_ALUM,    "Ventilation loads"),
        (C_SOLAR,   "Cooling loads"),
        ("#F5EDD0",  "Shore power (backup only)"),
        (C_GND,     "Earth / chassis ground"),
    ]
    for j, (col, txt) in enumerate(legend_items):
        yl = ly + 2.72 - j * 0.36
        ax.add_patch(mpatches.Rectangle((lx + 0.15, yl - 0.11), 0.45, 0.28,
                     fc=col, ec=C_OUT, lw=0.7, zorder=4))
        ax.text(lx + 0.75, yl + 0.03, txt,
                ha="left", va="center", fontsize=8.0, color=C_DIM)

    # ── ENERGY SUMMARY ────────────────────────────────────────────────────────
    ex = lx + SC_W + 0.8
    ey, ew, eh = 1.1, 6.8, 3.6
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
        ("Peak load",           "~415W simultaneous  (all circuits on)"),
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
        ("A", "VENTILATION FAN — INTAKE  (6\")",   "5A",  "16 AWG", "60W",
         "Near vestibule short wall  |  low position", C_ALUM),
        ("B", "VENTILATION FAN — EXHAUST  (6\")",  "5A",  "16 AWG", "60W",
         "Far short wall  |  high position", C_ALUM),
        ("C", "WATER PUMP  (12V DC)",              "15A", "14 AWG", "100W",
         "Adjacent water totes", C_BATT),
        ("D", "SAFELIGHT — interior + vestibule",  "5A",  "18 AWG", "15W",
         "Red LED strip  |  switched from inside", "#FFEEDD"),
        ("E", "EVAPORATIVE COOLER  (12V DC)",      "10A", "14 AWG", "80W",
         "Far short wall  |  light-safe baffled intake", C_SOLAR),
        ("F", "FILM PLANE ACTUATORS  (optional)",  "20A", "12 AWG", "≤100W pk",
         "Future provision  |  leave fused spare", "#E8E8E8"),
    ]

    SP_X  = ex - 0.5      # spine x
    CB_X  = SP_X + 0.65   # circuit boxes left edge
    CB_W  = FW - CB_X - 0.4
    CB_H  = 0.88
    CB_GAP = 1.22
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

    # Column header row
    col_defs = [
        # (x_start, width, header_text)
        (CB_X,        2.2,          "CIRCUIT / DEVICE"),
        (CB_X + 2.25, 1.55,         "FUSE"),
        (CB_X + 3.85, 1.55,         "WIRE GAUGE"),
        (CB_X + 5.45, 1.55,         "MAX LOAD"),
        (CB_X + 7.05, CB_W - 7.05,  "LOCATION / NOTE"),
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
            (CB_X + 2.25, 1.50, fuse),
            (CB_X + 3.85, 1.50, wire),
            (CB_X + 5.45, 1.50, load),
        ]:
            ax.add_patch(mpatches.Rectangle((xi, cy), cw, CB_H,
                         fc="white", ec=C_OUT, lw=0.8, zorder=3))
            ax.text(xi + cw / 2, tap_y, txt,
                    ha="center", va="center", fontsize=8.5,
                    color=C_OUT, zorder=4)

        # Note cell
        nx = CB_X + 7.05
        nw = CB_W - 7.05
        ax.add_patch(mpatches.Rectangle((nx, cy), nw, CB_H,
                     fc="white", ec=C_OUT, lw=0.8, zorder=3))
        ax.text(nx + nw / 2, tap_y, note,
                ha="center", va="center", fontsize=7.8, color=C_DIM, zorder=4)

    # ── Title block ──────────────────────────────────────────────────────────
    title_block(ax, FW, 1, 2,
                "SYSTEM ONE-LINE DIAGRAM",
                "Power flow  ·  Component specifications  ·  Circuit fuse ratings  ·  Wire gauges",
                "Not to scale")

    plt.savefig("electrical-sheet1.png", dpi=150, bbox_inches="tight",
                pad_inches=0.10, facecolor="white")
    plt.close(fig)
    print("  → electrical-sheet1.png  Done.")


# ─────────────────────────────────────────────────────────────────────────────
# SHEET 2 — Container Floor Plan + Wiring Layout  (scale 1:500)
# Container interior: 5,898 × 2,352 mm → 11.80 × 4.70 drawing units
# ─────────────────────────────────────────────────────────────────────────────

def draw_sheet2():
    FW, FH = 22.0, 13.5
    fig, ax = plt.subplots(figsize=(FW, FH), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(0, FW)
    ax.set_ylim(0, FH)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    ax.text(FW / 2, FH - 0.38,
            "CONTAINER FLOOR PLAN & WIRING LAYOUT — TBS-001",
            ha="center", va="center", fontsize=13, fontweight="bold",
            color=TITLE_COL)
    ax.text(FW / 2, FH - 0.70,
            "Top-down plan view  ·  Scale 1:500  ·  All dimensions in mm  "
            "·  Positions schematic — verify clearances on site",
            ha="center", va="center", fontsize=8.0, color=C_DIM)

    # Scale: 1 drawing unit = 500 mm real
    S   = 1.0 / 500.0
    OX  = 1.3    # container bottom-left x
    OY  = 3.2    # container bottom-left y

    C_LEN  = 5898   # mm interior length
    C_WID  = 2352   # mm interior width
    V_DEP  = 1200   # mm vestibule depth
    WT_MM  = 150    # schematic wall thickness mm (exaggerated for visibility)

    clen = C_LEN * S    # 11.796 units
    cwid = C_WID * S    # 4.704 units
    vd   = V_DEP * S    # 2.4 units
    wt   = WT_MM * S    # 0.30 units

    # ── Container shell ───────────────────────────────────────────────────────
    ax.add_patch(mpatches.Rectangle((OX, OY), clen, cwid,
                 fc="#F2F2EE", ec=C_OUT, lw=2.5, zorder=2))
    # Wall steel fill
    for rx, ry, rw, rh in [
        (OX,              OY,           clen, wt),           # bottom wall
        (OX,              OY+cwid-wt,   clen, wt),           # top wall
        (OX,              OY+wt,        wt,   cwid-2*wt),    # left (image) wall
        (OX+clen-wt,      OY+wt,        wt,   cwid-2*wt),    # right (door) wall
    ]:
        ax.add_patch(mpatches.Rectangle((rx, ry), rw, rh,
                     fc=C_STEEL, ec=C_OUT, lw=0.5, zorder=3))

    ax.text(OX + wt + 0.20, OY + cwid - wt - 0.18,
            "20FT ISO CONTAINER  —  INTERIOR  (top-down plan)",
            fontsize=8.0, ha="left", va="top", color=C_DIM, style="italic")

    # ── Vestibule (right of container, cargo door end) ────────────────────────
    VX = OX + clen
    ax.add_patch(mpatches.Rectangle((VX, OY), vd, cwid,
                 fc="#EEF5EE", ec=C_OUT, lw=2.0, linestyle="--", zorder=2))

    # S-path baffles (floor plan shows them as thick bars)
    b_proj = cwid * 0.58
    ax.add_patch(mpatches.Rectangle((VX + vd*0.28, OY),          wt*0.8, b_proj,
                 fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=5))
    ax.add_patch(mpatches.Rectangle((VX + vd*0.62, OY+cwid-b_proj), wt*0.8, b_proj,
                 fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=5))

    # Exterior door right edge
    ax.add_patch(mpatches.Rectangle((VX+vd-wt*0.5, OY+cwid*0.18), wt*0.5, cwid*0.64,
                 fc="white", ec=C_OUT, lw=1.2, zorder=4))
    # Door swing arc
    ax.add_patch(Arc((VX+vd-wt*0.5, OY+cwid*0.18),
                     2*cwid*0.64, 2*cwid*0.64,
                     angle=0, theta1=0, theta2=90,
                     color=C_DIM, lw=0.8, linestyle=":", zorder=3))

    ax.text(VX + vd/2, OY + cwid/2, "LIGHT TRAP\nVESTIBULE",
            ha="center", va="center", fontsize=9.0,
            fontweight="bold", color="#2D6A2D", rotation=90, zorder=5)

    # ── Film / image plane (left short wall interior) ─────────────────────────
    ax.add_patch(mpatches.Rectangle((OX+wt, OY+wt+0.10), 0.45, cwid-2*wt-0.20,
                 fc="#A8C8E8", ec=C_CL, lw=1.5, zorder=4))
    ax.text(OX+wt+0.225, OY+cwid/2, "IMAGE\nPLANE",
            ha="center", va="center", fontsize=7.5, color=TITLE_COL,
            fontweight="bold", rotation=90, zorder=5)

    # ── Pinhole (centred on right short wall interior — opposite image plane) ─
    ph_x = OX + clen - wt/2
    ph_y = OY + cwid/2
    ax.add_patch(plt.Circle((ph_x, ph_y), 0.13, fc="black", ec=C_OUT, lw=1.0, zorder=6))
    ax.annotate("PINHOLE  Ø2.17mm", xy=(ph_x, ph_y),
                xytext=(ph_x + 1.3, ph_y + 0.6),
                fontsize=8.0, color=C_OUT, ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color=C_DIM, lw=0.9),
                bbox=dict(fc="white", ec="none", pad=1.5))

    # ── Electrical panel IP65 box — upper right interior ─────────────────────
    EP_X = OX + clen - wt - 0.80
    EP_Y = OY + cwid - wt - 0.68
    EP_W, EP_H = 0.72, 0.55
    ax.add_patch(FancyBboxPatch((EP_X, EP_Y), EP_W, EP_H,
                 boxstyle="round,pad=0.03", fc=C_ELEC, ec=C_OUT, lw=1.5, zorder=5))
    ax.text(EP_X+EP_W/2, EP_Y+EP_H/2, "EP",
            ha="center", va="center", fontsize=9.5,
            fontweight="bold", color=C_OUT, zorder=6)

    # ── Battery bank — lower right interior ───────────────────────────────────
    BA_X = OX + clen - wt - 0.95
    BA_Y = OY + wt + 0.10
    BA_W, BA_H = 0.88, 0.65
    ax.add_patch(FancyBboxPatch((BA_X, BA_Y), BA_W, BA_H,
                 boxstyle="round,pad=0.03", fc=C_BATT, ec=C_OUT, lw=1.5, zorder=5))
    ax.text(BA_X+BA_W/2, BA_Y+BA_H/2, "BAT",
            ha="center", va="center", fontsize=9.5,
            fontweight="bold", color=C_OUT, zorder=6)

    # ── IBC totes (water system) ──────────────────────────────────────────────
    for t_off, t_label, t_col in [
        (1.6, "IBC\nBLUE\n(wash)",  "#C8E8FF"),
        (2.7, "IBC\nGREY\n(waste)", "#D8D8D8"),
    ]:
        tx = OX + wt + t_off
        ty = OY + cwid * 0.28
        tw, th = 0.75, 1.05
        ax.add_patch(mpatches.Rectangle((tx, ty), tw, th,
                     fc=t_col, ec=C_OUT, lw=0.9, zorder=4))
        ax.text(tx+tw/2, ty+th/2, t_label,
                ha="center", va="center", fontsize=7.0, color=C_OUT, zorder=5)

    # ── Water pump ────────────────────────────────────────────────────────────
    WP_X = OX + wt + 4.1
    WP_Y = OY + cwid * 0.48
    ax.add_patch(plt.Circle((WP_X, WP_Y), 0.26,
                 fc=C_BATT, ec=C_OUT, lw=1.2, zorder=5))
    ax.text(WP_X, WP_Y, "C", ha="center", va="center",
            fontsize=10, fontweight="bold", color=C_OUT, zorder=6)

    # ── Evaporative cooler — lower wall, centre area ──────────────────────────
    EC_X = OX + wt + 5.8
    EC_Y = OY + wt + 0.10
    EC_W, EC_H = 0.90, 0.58
    ax.add_patch(FancyBboxPatch((EC_X, EC_Y), EC_W, EC_H,
                 boxstyle="round,pad=0.03", fc=C_SOLAR, ec=C_OUT, lw=1.5, zorder=5))
    ax.text(EC_X+EC_W/2, EC_Y+EC_H/2, "E",
            ha="center", va="center", fontsize=9.5,
            fontweight="bold", color=C_OUT, zorder=6)
    # Baffled intake duct on bottom wall
    ax.add_patch(mpatches.Rectangle((EC_X+EC_W/2-0.12, OY), 0.24, wt,
                 fc="#A8D8B0", ec=C_OUT, lw=0.8, zorder=5))
    ax.text(EC_X+EC_W/2, OY - 0.12,
            "baffled\nintake ↑", ha="center", va="top", fontsize=6.5, color=C_DIM)

    # ── Fans ──────────────────────────────────────────────────────────────────
    # Intake fan A — right short wall (vestibule end), low
    FA_X = OX + clen - wt/2
    FA_Y = OY + cwid * 0.20
    ax.add_patch(plt.Circle((FA_X, FA_Y), 0.26, fc=C_ALUM, ec=C_OUT, lw=1.2, zorder=5))
    ax.text(FA_X, FA_Y, "A", ha="center", va="center",
            fontsize=10, fontweight="bold", color=C_OUT, zorder=6)

    # Exhaust fan B — left short wall (image plane end), high
    FB_X = OX + wt/2
    FB_Y = OY + cwid * 0.80
    ax.add_patch(plt.Circle((FB_X, FB_Y), 0.26, fc=C_ALUM, ec=C_OUT, lw=1.2, zorder=5))
    ax.text(FB_X, FB_Y, "B", ha="center", va="center",
            fontsize=10, fontweight="bold", color=C_OUT, zorder=6)

    # Safelight D — vestibule + interior; show as strip on vestibule ceiling
    ax.add_patch(mpatches.Rectangle((VX + 0.15, OY+cwid-wt-0.12), vd-0.30, 0.10,
                 fc="#FFD700", ec=C_OUT, lw=0.8, zorder=5))
    ax.text(VX + vd/2, OY+cwid-wt-0.06, "D", ha="center", va="center",
            fontsize=7.0, fontweight="bold", color=C_OUT, zorder=6)

    # NEMA inlet — exterior, right face of vestibule
    NM_X = VX + vd + 0.10
    NM_Y = OY + cwid * 0.60
    ax.add_patch(mpatches.Rectangle((NM_X, NM_Y), 0.45, 0.45,
                 fc="#FFF0CC", ec=C_OUT, lw=1.2, zorder=5))
    ax.text(NM_X+0.225, NM_Y+0.225, "AC\nIN",
            ha="center", va="center", fontsize=7.0,
            fontweight="bold", color=C_OUT, zorder=6)

    # Solar panels — exterior schematic (above container on plan)
    SP_X2 = OX + clen * 0.25
    SP_Y2 = OY + cwid + 1.0
    SP_W2 = clen * 0.50
    SP_H2 = 0.70
    ax.add_patch(FancyBboxPatch((SP_X2, SP_Y2), SP_W2, SP_H2,
                 boxstyle="round,pad=0.04", fc=C_SOLAR, ec=C_OUT, lw=1.8, zorder=3))
    ax.text(SP_X2+SP_W2/2, SP_Y2+SP_H2/2,
            "SOLAR PANELS  (3 × 200W)  —  EXTERIOR GROUND MOUNT, SOUTH-FACING",
            ha="center", va="center", fontsize=8.5, fontweight="bold",
            color=C_OUT, zorder=4)
    # PV cable arrow solar → EP
    ax.annotate("", xy=(EP_X+EP_W/2, EP_Y+EP_H),
                xytext=(SP_X2+SP_W2*0.75, SP_Y2),
                arrowprops=dict(arrowstyle="-|>", color="#2D7A2D", lw=1.8,
                                connectionstyle="arc3,rad=0.25"), zorder=4)
    ax.text(SP_X2+SP_W2*0.88, SP_Y2+0.45,
            "PV cable  10 AWG\nMC4 connectors\nsealed penetration",
            fontsize=7.0, color="#2D7A2D", ha="left", va="center")

    # ── Cable trunking — top interior corner rail ─────────────────────────────
    TK_Y = OY + cwid - wt - 0.10
    TK_X1 = OX + wt + 0.05
    TK_X2 = OX + clen - wt - 0.05
    ax.plot([TK_X1, TK_X2], [TK_Y, TK_Y],
            color=C_PIPE, lw=4.0, solid_capstyle="round", zorder=3)
    ax.text((TK_X1+TK_X2)/2, TK_Y + 0.22,
            "40 × 25mm PVC cable trunking  — all 12V DC circuits run here",
            ha="center", va="bottom", fontsize=7.5,
            color=C_PIPE, fontweight="bold")

    # Drop conduit lines from trunking to each device
    for dx, dy in [
        (EP_X+EP_W/2,  EP_Y+EP_H),
        (FA_X,         FA_Y+0.26),
        (EC_X+EC_W/2,  EC_Y+EC_H),
        (WP_X,         WP_Y+0.26),
        (BA_X+BA_W/2,  BA_Y+BA_H),
        (FB_X,         FB_Y+0.26),
    ]:
        ax.plot([dx, dx], [TK_Y, dy], color=C_PIPE,
                lw=1.0, linestyle=":", zorder=2)

    # ── Dimension lines ───────────────────────────────────────────────────────
    DIM_Y = OY - 0.65
    DIM_X = OX - 0.65

    def dim_h(x1, x2, dy, text):
        ax.annotate("", xy=(x2, dy), xytext=(x1, dy),
                    arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=1.0))
        ax.plot([x1, x1], [OY, dy], color=C_DIM, lw=0.6, linestyle=":")
        ax.plot([x2, x2], [OY, dy], color=C_DIM, lw=0.6, linestyle=":")
        ax.text((x1+x2)/2, dy - 0.22, text,
                ha="center", va="top", fontsize=8.0, color=C_DIM)

    def dim_v(dx, y1, y2, text):
        ax.annotate("", xy=(dx, y2), xytext=(dx, y1),
                    arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=1.0))
        ax.plot([OX, dx], [y1, y1], color=C_DIM, lw=0.6, linestyle=":")
        ax.plot([OX, dx], [y2, y2], color=C_DIM, lw=0.6, linestyle=":")
        ax.text(dx - 0.22, (y1+y2)/2, text,
                ha="right", va="center", fontsize=8.0,
                color=C_DIM, rotation=90)

    dim_h(OX,  OX+clen, DIM_Y,       "5,898 mm  (container interior length)")
    dim_h(VX,  VX+vd,   DIM_Y,       "1,200 mm\n(vestibule)")
    dim_v(DIM_X, OY, OY+cwid,        "2,352 mm  (interior width)")

    # ── Component key (right of drawing) ─────────────────────────────────────
    KX = VX + vd + 0.80
    KY = OY + cwid - 0.05
    ax.text(KX, KY + 0.28, "COMPONENT KEY",
            ha="left", va="center", fontsize=9.5,
            fontweight="bold", color=C_OUT)
    ax.plot([KX, KX + 5.8], [KY + 0.05, KY + 0.05], color=C_OUT, lw=1.0)

    key_rows = [
        ("EP",  C_ELEC,   "ELECTRICAL PANEL (EP)",
         "IP65 enclosure  |  Fuse block + MPPT controller"),
        ("BAT", C_BATT,   "BATTERY BANK (BAT)",
         "2 × 100Ah LiFePO4 12V parallel  |  2,400Wh"),
        ("A",   C_ALUM,   "INTAKE FAN — Cct A",
         "6\" inline DC fan  |  5A / 16 AWG / 60W"),
        ("B",   C_ALUM,   "EXHAUST FAN — Cct B",
         "6\" inline DC fan  |  5A / 16 AWG / 60W"),
        ("C",   C_BATT,   "WATER PUMP — Cct C",
         "12V DC pump  |  15A / 14 AWG / 100W"),
        ("D",   "#FFD700", "SAFELIGHT — Cct D",
         "Red LED strip  |  5A / 18 AWG / 15W"),
        ("E",   C_SOLAR,  "EVAP COOLER — Cct E",
         "12V DC 80W  |  10A / 14 AWG  |  baffled intake"),
        ("AC\nIN", "#FFF0CC", "NEMA 5-15R INLET (exterior)",
         "Shore power backup  |  → shore charger inside EP"),
    ]
    for j, (badge, bc, title, spec) in enumerate(key_rows):
        ky = KY - 0.28 - j * 0.60
        ax.add_patch(mpatches.Rectangle((KX, ky - 0.20), 0.50, 0.44,
                     fc=bc, ec=C_OUT, lw=0.9, zorder=4))
        ax.text(KX+0.25, ky + 0.01, badge,
                ha="center", va="center", fontsize=8.0,
                fontweight="bold", color=C_OUT, zorder=5)
        ax.text(KX+0.65, ky + 0.04, title,
                ha="left", va="center", fontsize=8.5,
                fontweight="bold", color=C_OUT)
        ax.text(KX+0.65, ky - 0.12, spec,
                ha="left", va="center", fontsize=7.5, color=C_DIM)

    # ── Drawing notes ─────────────────────────────────────────────────────────
    NX, NY = OX, 1.2
    ax.add_patch(FancyBboxPatch((NX-0.10, NY-0.15), 13.5, 1.25,
                 boxstyle="round,pad=0.04", fc="#F8F9FA", ec=C_DIM, lw=0.8, zorder=2))
    ax.text(NX+0.10, NY+0.90, "DRAWING NOTES:",
            ha="left", va="center", fontsize=8.5,
            fontweight="bold", color=C_OUT)
    notes = [
        "1.  All component positions are schematic. Verify clearances on site before installation.",
        "2.  Vestibule bolts to ISO corner castings via M10 × 50mm bolts — no welding required. Remove for transport.",
        "3.  Cable trunking (40×25mm PVC) runs along top interior corner rail. Drop conduits (10mm corrugated grey) to each device.",
        "4.  Solar panels mounted externally (south-facing, 30° tilt). PV cable enters through sealed IP67 wall penetration.",
    ]
    for ni, note in enumerate(notes):
        ax.text(NX+0.10 + (ni >= 2) * 6.8, NY + 0.62 - (ni % 2) * 0.30,
                note, ha="left", va="center", fontsize=7.5, color=C_DIM)

    # ── Title block ──────────────────────────────────────────────────────────
    title_block(ax, FW, 2, 2,
                "CONTAINER FLOOR PLAN & WIRING LAYOUT",
                "Top-down plan  ·  Component positions  ·  Conduit routes  ·  Scale 1:500",
                "1:500  (1 drawing unit = 500 mm)")

    plt.savefig("electrical-sheet2.png", dpi=150, bbox_inches="tight",
                pad_inches=0.10, facecolor="white")
    plt.close(fig)
    print("  → electrical-sheet2.png  Done.")


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Generating TBS-001 Electrical & Systems diagrams...")
    draw_sheet1()
    draw_sheet2()
    print("Done.")
