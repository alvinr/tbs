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
#
# ORIENTATION (corrected):
#   Container long axis (5,898mm) = HORIZONTAL (left–right)
#   Optical depth (2,362mm)       = VERTICAL (bottom–top)
#   Pinhole: on BOTTOM long wall at X=2,946mm (mid-point)
#   Image plane: on TOP long wall
#   Cargo door / vestibule: RIGHT short-end wall
#   All equipment in colonnade strip Yd ≤ 1,220mm (near bottom/pinhole wall)
# ─────────────────────────────────────────────────────────────────────────────

def draw_sheet2():
    from matplotlib.patches import Polygon as MplPolygon

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
            "·  Pinhole on long wall — optical axis crosses container width (2,362mm)",
            ha="center", va="center", fontsize=8.0, color=C_DIM)

    # ── Scale constants ───────────────────────────────────────────────────────
    S      = 1.0 / 500.0   # 1 drawing unit = 500mm
    OX     = 1.2           # container left edge (far end from cargo door)
    OY     = 3.6           # container bottom edge = PINHOLE WALL (Yd=0)

    C_LEN  = 5898          # mm interior length (horizontal in plan)
    C_WID  = 2362          # mm interior width  = optical depth (vertical in plan)
    WT_MM  = 120           # schematic wall thickness

    PH_X_MM    = 2946      # pinhole X along long axis (midpoint)
    FP_Y_MM    = 2262      # film-plane depth from pinhole wall
    COLN_MM    = 1220      # colonnade boundary depth
    DRUM_CY_MM = 1600      # drum centre — offset toward far wall for IBC clearance

    clen    = C_LEN  * S   # 11.796
    cwid    = C_WID  * S   # 4.724
    wt      = WT_MM  * S   # 0.24
    ph_x    = OX + PH_X_MM  * S   # 7.092
    fp_y    = OY + FP_Y_MM  * S
    coln_y  = OY + COLN_MM  * S   # colonnade boundary in drawing
    drum_cy = OY + DRUM_CY_MM * S

    VD_MM   = 1200
    vd      = VD_MM * S    # 2.4 units — vestibule depth
    VX      = OX + clen    # cargo-door short wall X position

    # ── Container shell ───────────────────────────────────────────────────────
    ax.add_patch(mpatches.Rectangle((OX, OY), clen, cwid,
                 fc="#F8F8F4", ec=C_OUT, lw=2.5, zorder=2))
    for rx, ry, rw, rh in [
        (OX,          OY,         clen, wt),         # BOTTOM long wall — PINHOLE WALL
        (OX,          OY+cwid-wt, clen, wt),         # TOP long wall — IMAGE PLANE WALL
        (OX,          OY+wt,      wt,   cwid-2*wt),  # LEFT short wall (far end)
        (OX+clen-wt,  OY+wt,      wt,   cwid-2*wt),  # RIGHT short wall — CARGO DOOR
    ]:
        ax.add_patch(mpatches.Rectangle((rx, ry), rw, rh,
                     fc=C_STEEL, ec=C_OUT, lw=0.5, zorder=3))
    ax.text(OX + clen/2, OY + cwid - wt - 0.22,
            "20FT ISO CONTAINER  —  INTERIOR  (top-down plan)",
            fontsize=8.0, ha="center", va="top", color=C_DIM, style="italic")

    # ── Optical cone (pinhole → image plane, in plan view) ────────────────────
    # Cone expands from the pinhole point on the bottom wall to the full
    # image-plane width on the top wall.
    cone_verts = [
        (ph_x,        OY + wt),         # pinhole (bottom long wall)
        (OX + wt,     OY + cwid - wt),  # top-left interior corner
        (OX+clen-wt,  OY + cwid - wt),  # top-right interior corner
    ]
    ax.add_patch(MplPolygon(cone_verts, closed=True,
                fc="#FFE8C0", ec="none", alpha=0.28, zorder=4))
    ax.text(ph_x, OY + cwid * 0.64,
            "OPTICAL CONE\n(shadow zone — keep entirely clear)",
            ha="center", va="center", fontsize=8.0,
            color="#8B5A00", style="italic", alpha=0.75, zorder=5)

    # ── Colonnade safe zone (near pinhole wall) ───────────────────────────────
    ax.add_patch(mpatches.Rectangle((OX+wt, OY+wt), clen-2*wt, COLN_MM*S - wt,
                 fc="#E0F0E0", ec="none", alpha=0.40, zorder=4))
    ax.plot([OX+wt, OX+clen-wt], [coln_y, coln_y],
            color="#1A7A1A", lw=1.5, ls="--", zorder=7)
    ax.text(OX+clen-wt + 0.10, coln_y,
            "Colonnade limit  Yd=1,220mm ▲",
            fontsize=7.0, color="#1A7A1A", va="center", ha="left")

    # ── Image plane — TOP long wall ───────────────────────────────────────────
    ax.add_patch(mpatches.Rectangle((OX+wt, OY+cwid-wt-0.14), clen-2*wt, 0.14,
                 fc="#A8C8E8", ec=C_CL, lw=1.5, zorder=5))
    ax.text(OX + clen/2, OY + cwid - wt - 0.07,
            "IMAGE PLANE  —  5,893 × 2,388 mm",
            ha="center", va="center", fontsize=7.5, color=TITLE_COL,
            fontweight="bold", zorder=6)

    # ── Pinhole — BOTTOM long wall at X=2,946mm ───────────────────────────────
    ax.add_patch(plt.Circle((ph_x, OY + wt/2), 0.12,
                 fc="black", ec=C_OUT, lw=1.0, zorder=8))
    ax.annotate("PINHOLE  Ø2.17mm\nX=2,946mm  f/1088",
                xy=(ph_x, OY + wt/2),
                xytext=(ph_x, OY - 0.52),
                fontsize=7.5, color=C_OUT, ha="center", va="top",
                arrowprops=dict(arrowstyle="-", color=C_DIM, lw=0.9),
                bbox=dict(fc="white", ec="none", pad=1.5))

    # ── Vestibule — right of container (cargo-door end) ───────────────────────
    ax.add_patch(mpatches.Rectangle((VX, OY), vd, cwid,
                 fc="#F0F5F0", ec=C_OUT, lw=1.5, ls="--", zorder=2))
    ax.text(VX + vd/2, OY + cwid * 0.30,
            "LIGHT TRAP\nVESTIBULE",
            ha="center", va="center", fontsize=8.5,
            fontweight="bold", color="#2D6A2D", rotation=90, zorder=5)

    # Revolving drum — Ø750mm vertical axis (plan footprint = circle)
    DRUM_R_MM = 375
    drum_r  = DRUM_R_MM * S      # 0.75 drawing units
    drum_cx = VX + drum_r + 0.08
    ax.add_patch(plt.Circle((drum_cx, drum_cy), drum_r,
                 fc="#E8E8D8", ec=C_OUT, lw=1.5, alpha=0.9, zorder=6))
    # Entry gap — dashed line where drum meets container wall
    ax.plot([VX, VX], [drum_cy - drum_r, drum_cy + drum_r],
            color=C_CL, lw=1.8, ls=(0, (4, 2)), zorder=7)
    ax.text(drum_cx, drum_cy,
            "DRUM\nØ750mm\nVERT.AXIS",
            ha="center", va="center", fontsize=6.0, color=C_OUT, zorder=7)
    ax.annotate(f"Centre Yd={DRUM_CY_MM}mm",
                xy=(VX, drum_cy),
                xytext=(VX + vd + 0.30, drum_cy + 0.40),
                fontsize=6.5, color=C_DIM, ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color=C_DIM, lw=0.7))

    # Cargo-door symbol
    ax.add_patch(mpatches.Rectangle((VX+vd-wt*0.5, OY+cwid*0.20),
                 wt*0.5, cwid*0.60,
                 fc="white", ec=C_OUT, lw=1.2, zorder=5))
    ax.text(VX+vd+0.10, OY+cwid*0.12,
            "CARGO DOOR\n(entrance)", fontsize=7.0, color=C_DIM,
            ha="left", va="center")

    # Safelight strip in vestibule
    ax.add_patch(mpatches.Rectangle((VX+0.15, OY+cwid-wt-0.12), vd-0.30, 0.10,
                 fc="#FFD700", ec=C_OUT, lw=0.8, zorder=5))
    ax.text(VX+vd/2, OY+cwid-wt-0.06, "D",
            ha="center", va="center", fontsize=7.0, fontweight="bold",
            color=C_OUT)

    # NEMA inlet — exterior right of vestibule
    NM_X = VX + vd + 0.10
    NM_Y = OY + cwid * 0.68
    ax.add_patch(mpatches.Rectangle((NM_X, NM_Y), 0.45, 0.45,
                 fc="#FFF0CC", ec=C_OUT, lw=1.2, zorder=5))
    ax.text(NM_X+0.225, NM_Y+0.225, "AC\nIN",
            ha="center", va="center", fontsize=7.0,
            fontweight="bold", color=C_OUT, zorder=6)

    # ── Helper: colonnade equipment rectangle ─────────────────────────────────
    def equip(x_mm, yd_mm, w_mm, d_mm, label, col, sublabel=""):
        """
        x_mm  — TBS X from left end of container (long axis), mm
        yd_mm — depth from pinhole wall, mm
        w_mm  — width along long axis, mm
        d_mm  — depth (into container from pinhole wall), mm
        """
        ex = OX + wt + x_mm * S
        ey = OY + wt + yd_mm * S
        ew = w_mm * S
        ed = d_mm * S
        ax.add_patch(mpatches.Rectangle((ex, ey), ew, ed,
                     fc=col, ec=C_OUT, lw=1.0, zorder=5, alpha=0.88))
        cy_e = ey + ed / 2
        ax.text(ex + ew/2, cy_e + (0.10 if sublabel else 0), label,
                ha="center", va="center", fontsize=6.5, fontweight="bold",
                color=C_OUT, zorder=6)
        if sublabel:
            ax.text(ex + ew/2, cy_e - 0.12, sublabel,
                    ha="center", va="center", fontsize=5.5, color=C_DIM, zorder=6)

    # ── LEFT WING — X=0–2,380mm ───────────────────────────────────────────────
    equip(100,  100, 1219, 1016, "BLUE IBC ×2",  "#C8E8FF", "2×600L stacked")
    equip(1380, 100,  600,  350, "EVAP\nCOOLER", C_SOLAR,   "80W 12V  (E)")
    equip(1980, 100,  400,  300, "PUMP\nMFD",    C_BATT,    "100W 12V  (C)")

    # ── RIGHT WING — X=3,374–5,893mm ─────────────────────────────────────────
    equip(3374, 100, 1160,  580, "DRUMS ×2",  C_STEEL,   "2×55 gal")
    equip(4674, 100, 1219, 1016, "BROWN IBC", "#D7CCC8", "1×600L")

    # ── Electrical panel + battery — on pinhole wall face (Yd=0) ─────────────
    EP_X_MM, EP_W_MM = 2050, 300
    EP_DX = OX + wt + EP_X_MM * S
    EP_DW = EP_W_MM * S
    ax.add_patch(mpatches.Rectangle((EP_DX, OY + wt*0.18), EP_DW, wt*0.64,
                 fc=C_ELEC, ec=C_OUT, lw=1.0, zorder=7))
    ax.text(EP_DX + EP_DW/2, OY + wt/2, "EP",
            ha="center", va="center", fontsize=6.5, fontweight="bold", color=C_OUT)

    BA_X_MM, BA_W_MM = 100, 500
    BA_DX = OX + wt + BA_X_MM * S
    BA_DW = BA_W_MM * S
    ax.add_patch(mpatches.Rectangle((BA_DX, OY + wt*0.18), BA_DW, wt*0.64,
                 fc=C_BATT, ec=C_OUT, lw=1.0, zorder=7))
    ax.text(BA_DX + BA_DW/2, OY + wt/2, "BAT",
            ha="center", va="center", fontsize=6.5, fontweight="bold", color=C_OUT)

    # ── Fans ──────────────────────────────────────────────────────────────────
    # Fan A — intake, left short wall (far end from cargo door)
    FA_X = OX + wt/2
    FA_Y = OY + cwid * 0.50
    ax.add_patch(plt.Circle((FA_X, FA_Y), 0.22,
                 fc=C_ALUM, ec=C_OUT, lw=1.2, zorder=5))
    ax.text(FA_X, FA_Y, "A",
            ha="center", va="center", fontsize=9, fontweight="bold",
            color=C_OUT, zorder=6)

    # Fan B — exhaust, right short wall (cargo-door end)
    FB_X = OX + clen - wt/2
    FB_Y = OY + cwid * 0.70
    ax.add_patch(plt.Circle((FB_X, FB_Y), 0.22,
                 fc=C_ALUM, ec=C_OUT, lw=1.2, zorder=5))
    ax.text(FB_X, FB_Y, "B",
            ha="center", va="center", fontsize=9, fontweight="bold",
            color=C_OUT, zorder=6)

    # ── Cable trunking — pinhole wall face (Yd=0, outside optical cone) ───────
    TK_Y  = OY + wt - 0.07
    TK_X1 = OX + wt + 0.05
    TK_X2 = OX + clen - wt - 0.05
    ax.plot([TK_X1, TK_X2], [TK_Y, TK_Y],
            color=C_PIPE, lw=4.5, solid_capstyle="round", zorder=6)
    ax.text((TK_X1+TK_X2)/2, TK_Y - 0.24,
            "40×25mm PVC cable trunking — pinhole wall face (Yd=0) — outside optical cone",
            ha="center", va="top", fontsize=7.0, color=C_PIPE, fontweight="bold")

    # Short drop conduits from trunking to each device
    for ddx, ddy in [
        (EP_DX + EP_DW/2,             OY + wt),
        (BA_DX + BA_DW/2,             OY + wt),
        (OX + wt + 1680*S,            OY + wt + 350*S),   # evap cooler
        (OX + wt + 2180*S,            OY + wt + 300*S),   # pump
        (OX + wt + 3954*S,            OY + wt + 580*S),   # drums centre
        (OX + wt + 5283*S,            OY + wt + 1016*S),  # brown IBC centre
        (FA_X,                         FA_Y - 0.22),
        (FB_X,                         FB_Y - 0.22),
    ]:
        ax.plot([ddx, ddx], [TK_Y, ddy],
                color=C_PIPE, lw=1.0, ls=":", zorder=4)

    # ── Solar panels — exterior (below container in plan) ─────────────────────
    SP_X2 = OX + clen * 0.25
    SP_Y2 = OY - 1.80
    SP_W2 = clen * 0.50
    SP_H2 = 0.65
    ax.add_patch(FancyBboxPatch((SP_X2, SP_Y2), SP_W2, SP_H2,
                 boxstyle="round,pad=0.04", fc=C_SOLAR, ec=C_OUT, lw=1.8, zorder=3))
    ax.text(SP_X2+SP_W2/2, SP_Y2+SP_H2/2,
            "SOLAR PANELS  (3 × 200W)  —  EXTERIOR GROUND MOUNT, SOUTH-FACING",
            ha="center", va="center", fontsize=8.5, fontweight="bold",
            color=C_OUT, zorder=4)
    ax.annotate("", xy=(EP_DX + EP_DW/2, OY),
                xytext=(SP_X2 + SP_W2*0.72, SP_Y2 + SP_H2),
                arrowprops=dict(arrowstyle="-|>", color="#2D7A2D", lw=1.8,
                                connectionstyle="arc3,rad=0.25"), zorder=4)
    ax.text(SP_X2+SP_W2*0.80, SP_Y2+SP_H2*0.5 + 0.40,
            "PV cable  10 AWG\nMC4 / sealed penetration",
            fontsize=7.0, color="#2D7A2D", ha="center", va="center")

    # ── Dimension lines ───────────────────────────────────────────────────────
    DIM_Y = OY - 0.92
    DIM_X = OX - 0.52

    def dim_h(x1, x2, dy, text):
        ax.annotate("", xy=(x2, dy), xytext=(x1, dy),
                    arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=1.0))
        ax.plot([x1, x1], [OY, dy], color=C_DIM, lw=0.5, ls=":")
        ax.plot([x2, x2], [OY, dy], color=C_DIM, lw=0.5, ls=":")
        ax.text((x1+x2)/2, dy - 0.18, text,
                ha="center", va="top", fontsize=7.5, color=C_DIM)

    def dim_v(dx, y1, y2, text):
        ax.annotate("", xy=(dx, y2), xytext=(dx, y1),
                    arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=1.0))
        ax.plot([OX, dx], [y1, y1], color=C_DIM, lw=0.5, ls=":")
        ax.plot([OX, dx], [y2, y2], color=C_DIM, lw=0.5, ls=":")
        ax.text(dx - 0.18, (y1+y2)/2, text,
                ha="right", va="center", fontsize=7.5,
                color=C_DIM, rotation=90)

    dim_h(OX,  OX+clen, DIM_Y, "5,898 mm  (container interior length)")
    dim_h(VX,  VX+vd,   DIM_Y, "1,200 mm  (vestibule)")
    dim_v(DIM_X, OY, OY+cwid,  "2,362 mm  (optical depth / interior width)")
    dim_v(DIM_X, OY, coln_y,   "1,220 mm\n(colonnade)")

    # ── Component key ─────────────────────────────────────────────────────────
    KX = VX + vd + 0.80
    KY = OY + cwid - 0.05
    ax.text(KX, KY + 0.28, "COMPONENT KEY",
            ha="left", va="center", fontsize=9.5,
            fontweight="bold", color=C_OUT)
    ax.plot([KX, KX + 5.8], [KY + 0.05, KY + 0.05], color=C_OUT, lw=1.0)

    key_rows = [
        ("EP",    C_ELEC,    "ELECTRICAL PANEL (EP)",
         "IP65 enclosure  |  MPPT + fuse block  |  Pinhole wall face, X=2,050mm"),
        ("BAT",   C_BATT,    "BATTERY BANK (BAT)",
         "2×100Ah LiFePO4 12V  |  2,400Wh  |  Pinhole wall face, X=100mm"),
        ("A",     C_ALUM,    "INTAKE FAN — Cct A",
         "6\" inline DC  |  5A / 16 AWG / 60W  |  Far end wall"),
        ("B",     C_ALUM,    "EXHAUST FAN — Cct B",
         "6\" inline DC  |  5A / 16 AWG / 60W  |  Cargo door wall"),
        ("C",     C_BATT,    "WATER PUMP — Cct C",
         "12V DC pump  |  15A / 14 AWG / 100W  |  Colonnade left wing"),
        ("D",     "#FFD700", "SAFELIGHT — Cct D",
         "Red LED strip  |  5A / 18 AWG / 15W  |  Vestibule ceiling"),
        ("E",     C_SOLAR,   "EVAP COOLER — Cct E",
         "12V DC 80W  |  10A / 14 AWG  |  Colonnade left wing"),
        ("AC\nIN","#FFF0CC", "NEMA 5-15R INLET (exterior)",
         "Shore power backup  |  → shore charger inside EP"),
    ]
    for j, (badge, bc, title_k, spec) in enumerate(key_rows):
        ky = KY - 0.28 - j * 0.60
        ax.add_patch(mpatches.Rectangle((KX, ky - 0.20), 0.50, 0.44,
                     fc=bc, ec=C_OUT, lw=0.9, zorder=4))
        ax.text(KX+0.25, ky + 0.01, badge,
                ha="center", va="center", fontsize=8.0,
                fontweight="bold", color=C_OUT, zorder=5)
        ax.text(KX+0.65, ky + 0.04, title_k,
                ha="left", va="center", fontsize=8.5,
                fontweight="bold", color=C_OUT)
        ax.text(KX+0.65, ky - 0.12, spec,
                ha="left", va="center", fontsize=7.5, color=C_DIM)

    # ── Drawing notes ─────────────────────────────────────────────────────────
    NX, NY = OX, 1.35
    ax.add_patch(FancyBboxPatch((NX-0.10, NY-0.15), 14.0, 1.30,
                 boxstyle="round,pad=0.04", fc="#F8F9FA", ec=C_DIM, lw=0.8, zorder=2))
    ax.text(NX+0.10, NY+0.95, "DRAWING NOTES:",
            ha="left", va="center", fontsize=8.5,
            fontweight="bold", color=C_OUT)
    notes = [
        "1.  Pinhole on bottom long wall (front face) at X=2,946mm. Image plane on opposite long wall. "
        "Optical axis perpendicular to container length.",
        "2.  All equipment in colonnade zone (Yd≤1,220mm from pinhole wall). "
        "Amber shaded area = optical shadow cone — keep entirely clear.",
        "3.  Cable trunking (40×25mm PVC) runs along pinhole wall face at Yd=0 — outside optical cone. "
        "Drop conduits (10mm corrugated) connect to each device.",
        "4.  Solar panels mounted externally (south-facing, 30° tilt). "
        "PV cable enters through sealed IP67 penetration on pinhole wall face.",
    ]
    for ni, note in enumerate(notes):
        ax.text(NX+0.10 + (ni >= 2)*7.0, NY + 0.70 - (ni % 2)*0.33,
                note, ha="left", va="center", fontsize=7.5, color=C_DIM,
                wrap=True)

    # ── Title block ──────────────────────────────────────────────────────────
    title_block(ax, FW, 2, 2,
                "CONTAINER FLOOR PLAN & WIRING LAYOUT",
                "Top-down plan  ·  Colonnade layout  ·  Optical cone clear  ·  Scale 1:500",
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
