#!/usr/bin/env python3
"""
generate_electrical_diagram.py
TBS-001 Electrical & Systems — two engineering drawing sheets.

Sheet 1: System one-line diagram (power flow, components, fuse ratings)
Sheet 2: Container floor plan with wiring layout
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ── Palette (white-background engineering style) ──────────────────────────────
C_OUT   = "#1A1A1A"   # outlines / text
C_CL    = "#2060A0"   # centre lines / flow arrows
C_DIM   = "#404040"   # dimensions / labels
C_ALUM  = "#C8D8E8"   # aluminium / neutral component fill
C_STEEL = "#B0B0B8"   # steel fill
C_ELEC  = "#FFF3CC"   # electrical component fill (warm yellow)
C_SOLAR = "#D4EDDA"   # solar / green highlight
C_BATT  = "#CCE5FF"   # battery fill (blue)
C_WARN  = "#F8D7DA"   # warning / fuse
C_GND   = "#2C5F2E"   # ground green
C_PIPE  = "#6C757D"   # conduit / pipe

TITLE_COL = "#0F2D5E"  # TBS dark blue


# ── Helpers ───────────────────────────────────────────────────────────────────

def box(ax, x, y, w, h, label, sublabel="", fc=C_ELEC, ec=C_OUT, lw=1.2,
        fontsize=7.5, subfontsize=6.0, bold=False):
    rect = FancyBboxPatch((x, y), w, h,
                          boxstyle="round,pad=0.02",
                          fc=fc, ec=ec, lw=lw, zorder=3)
    ax.add_patch(rect)
    fw = "bold" if bold else "normal"
    ax.text(x + w/2, y + h/2 + (0.08 if sublabel else 0),
            label, ha="center", va="center",
            fontsize=fontsize, fontweight=fw, color=C_OUT, zorder=4)
    if sublabel:
        ax.text(x + w/2, y + h/2 - 0.10,
                sublabel, ha="center", va="center",
                fontsize=subfontsize, color=C_DIM, zorder=4)


def arrow(ax, x1, y1, x2, y2, col=C_CL, lw=1.5):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=lw),
                zorder=5)


def hline(ax, x1, x2, y, col=C_CL, lw=1.2):
    ax.plot([x1, x2], [y, y], color=col, lw=lw, zorder=3)


def vline(ax, x, y1, y2, col=C_CL, lw=1.2):
    ax.plot([x, x], [y1, y2], color=col, lw=lw, zorder=3)


def label(ax, x, y, text, ha="center", va="center", size=6.5, col=C_DIM):
    ax.text(x, y, text, ha=ha, va=va, fontsize=size, color=col, zorder=5)


def title_block(ax, fig_w, sheet_n, sheet_total, title1, title2, scale_str,
                project="THE BIG SHOEBOX PROJECT", series="TBS-ELEC"):
    tb_h = 0.55
    tb_y = 0.02
    # outer border
    ax.add_patch(mpatches.Rectangle((0.1, tb_y), fig_w - 0.2, tb_h,
                                    fc="white", ec=C_OUT, lw=1.5, zorder=6,
                                    transform=ax.transData))
    # dividers
    for xd in [fig_w * 0.35, fig_w * 0.65]:
        ax.plot([xd, xd], [tb_y, tb_y + tb_h], color=C_OUT, lw=0.8, zorder=7)
    # content
    ax.text(fig_w * 0.175, tb_y + 0.38, project,
            ha="center", va="center", fontsize=7.0,
            fontweight="bold", color=TITLE_COL, zorder=7)
    ax.text(fig_w * 0.175, tb_y + 0.22, series,
            ha="center", va="center", fontsize=6.0, color=C_DIM, zorder=7)
    ax.text(fig_w * 0.175, tb_y + 0.10, "ELECTRICAL & SYSTEMS REPORT",
            ha="center", va="center", fontsize=5.5, color=C_DIM, zorder=7)

    ax.text(fig_w * 0.50, tb_y + 0.36, title1,
            ha="center", va="center", fontsize=8.5,
            fontweight="bold", color=C_OUT, zorder=7)
    ax.text(fig_w * 0.50, tb_y + 0.20, title2,
            ha="center", va="center", fontsize=6.5, color=C_DIM, zorder=7)
    ax.text(fig_w * 0.50, tb_y + 0.09, f"Scale: {scale_str}",
            ha="center", va="center", fontsize=5.5, color=C_DIM, zorder=7)

    ax.text(fig_w * 0.825, tb_y + 0.36,
            f"Sheet {sheet_n} of {sheet_total}",
            ha="center", va="center", fontsize=7.0,
            fontweight="bold", color=C_OUT, zorder=7)
    ax.text(fig_w * 0.825, tb_y + 0.20, "TBS-001  ·  20FT ISO CAMERA",
            ha="center", va="center", fontsize=6.0, color=C_DIM, zorder=7)
    ax.text(fig_w * 0.825, tb_y + 0.09, "2026",
            ha="center", va="center", fontsize=5.5, color=C_DIM, zorder=7)


# ─────────────────────────────────────────────────────────────────────────────
# SHEET 1 — System One-Line Diagram
# ─────────────────────────────────────────────────────────────────────────────

def draw_sheet1():
    FW, FH = 14.0, 10.0
    fig, ax = plt.subplots(figsize=(FW, FH), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(0, FW)
    ax.set_ylim(0, FH)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # ── Title ─────────────────────────────────────────────────────────────────
    ax.text(FW/2, FH - 0.35, "SYSTEM ONE-LINE DIAGRAM — 12V DC OFF-GRID",
            ha="center", va="center", fontsize=12, fontweight="bold",
            color=TITLE_COL)
    ax.text(FW/2, FH - 0.65, "TBS-001 · The Big Shoebox Project",
            ha="center", va="center", fontsize=8, color=C_DIM)

    # ── Solar array (top left) ────────────────────────────────────────────────
    sx, sy, sw, sh = 0.8, 7.8, 3.2, 0.9
    box(ax, sx, sy, sw, sh,
        "SOLAR ARRAY", "3 × 200W monocrystalline  |  12V nominal  |  30A Isc combined",
        fc=C_SOLAR, bold=True)
    # panel cells hint
    for i in range(6):
        x0 = sx + 0.15 + i * 0.45
        ax.add_patch(mpatches.Rectangle((x0, sy + 0.1), 0.35, 0.7,
                     fc="#A8D8B0", ec=C_OUT, lw=0.5, zorder=4))

    # ── MPPT controller ───────────────────────────────────────────────────────
    mx, my, mw, mh = 0.8, 6.0, 3.2, 0.85
    box(ax, mx, my, mw, mh,
        "MPPT CHARGE CONTROLLER",
        "Victron SmartSolar MPPT 100/50  |  100V PV input  |  50A charge",
        fc=C_ELEC, bold=True)

    # Arrow: solar → MPPT
    arrow(ax, sx + sw/2, sy, mx + mw/2, my + mh, col=C_SOLAR)
    label(ax, sx + sw/2 + 0.25, (sy + my + mh)/2 + 0.05, "10 AWG PV cable\nMC4 connectors",
          size=5.5)

    # ── Battery bank (centre) ─────────────────────────────────────────────────
    bx, by, bw, bh = 0.8, 4.1, 3.2, 0.95
    box(ax, bx, by, bw, bh,
        "BATTERY BANK",
        "2 × 100Ah 12V LiFePO4 in parallel  =  200Ah / 2,400Wh usable",
        fc=C_BATT, bold=True, fontsize=8)
    # battery symbol — two cells
    for i in range(2):
        bsx = bx + 0.3 + i * 1.4
        ax.add_patch(mpatches.Rectangle((bsx, by + 0.1), 1.1, 0.75,
                     fc="#A0C4FF", ec=C_OUT, lw=0.8, zorder=4))
        ax.text(bsx + 0.55, by + 0.47, "100Ah\nLiFePO4",
                ha="center", va="center", fontsize=5.5, color=C_OUT, zorder=5)

    # Arrow: MPPT → Battery
    arrow(ax, mx + mw/2, my, bx + bw/2, by + bh, col=C_CL)
    label(ax, mx + mw/2 + 0.25, (my + by + bh)/2, "2 AWG\n(charge)",
          size=5.5)

    # ── Shore charger (branch into battery) ───────────────────────────────────
    chx, chy, chw, chh = 5.0, 4.1, 2.8, 0.95
    box(ax, chx, chy, chw, chh,
        "SHORE CHARGER (optional)",
        "Victron Blue Smart IP65 12/15  |  100–240V AC in  |  15A DC out",
        fc="#F0E8D0", bold=False, fontsize=7)
    # arrow shore → battery
    arrow(ax, chx, chy + chh/2, bx + bw, by + bh/2, col="#B08020")
    label(ax, (chx + bx + bw)/2, by + bh/2 + 0.15,
          "4 AWG", size=5.5, col="#B08020")
    # NEMA inlet
    box(ax, chx, chy - 0.9, chw, 0.7, "NEMA 5-15R INLET",
        "Weatherproof  |  Exterior short wall",
        fc="white", fontsize=7)
    arrow(ax, chx + chw/2, chy - 0.2, chx + chw/2, chy, col="#B08020")

    # ── Main fuse ─────────────────────────────────────────────────────────────
    fx, fy, fw2, fh = 0.8, 2.8, 1.5, 0.65
    box(ax, fx, fy, fw2, fh, "200A MAIN FUSE",
        "ANL fuse  |  2/0 AWG  |  Batt+ → busbar",
        fc=C_WARN, bold=False, fontsize=7)
    arrow(ax, bx + bw * 0.3, by, fx + fw2/2, fy + fh, col=C_OUT)

    # ── Fuse block ────────────────────────────────────────────────────────────
    fbx, fby, fbw, fbh = 0.8, 1.3, 3.2, 1.0
    box(ax, fbx, fby, fbw, fbh,
        "BLUE SEA 5026 FUSE BLOCK",
        "12-circuit  |  Positive busbar + negative busbar",
        fc=C_WARN, bold=True, fontsize=8)
    # arrow: main fuse → fuse block
    arrow(ax, fx + fw2/2, fy, fbx + fbw * 0.3, fby + fbh, col=C_OUT)
    # arrow: battery neg → fuse block neg
    ax.plot([bx + bw * 0.7, bx + bw * 0.7, fbx + fbw * 0.7],
            [by, fby + 0.35, fby + 0.35],
            color=C_STEEL, lw=1.2, linestyle="--", zorder=3)
    label(ax, bx + bw * 0.7 + 0.15, (by + fby + 0.35)/2 + 0.1,
          "NEG\n2/0 AWG", size=5.5, col=C_DIM)

    # ── Ground symbol ─────────────────────────────────────────────────────────
    gx, gy = fbx + fbw * 0.7 - 0.3, fby - 0.55
    for i, (lw_g, len_g) in enumerate([(1.2, 0.5), (1.0, 0.35), (0.7, 0.2)]):
        y_g = gy - i * 0.12
        ax.plot([gx + 0.25 - len_g/2, gx + 0.25 + len_g/2],
                [y_g, y_g], color=C_GND, lw=lw_g, zorder=4)
    ax.plot([gx + 0.25, gx + 0.25], [fby + 0.35, gy], color=C_GND, lw=1.2)
    ax.text(gx + 0.55, gy - 0.18, "EARTH\nGround stake + container body",
            ha="left", va="center", fontsize=5.5, color=C_GND)

    # ── Individual circuits ───────────────────────────────────────────────────
    circuits = [
        ("A", "INTAKE FAN (6\")",  "5A  |  16 AWG  |  60W", C_ALUM),
        ("B", "EXHAUST FAN (6\")", "5A  |  16 AWG  |  60W", C_ALUM),
        ("C", "WATER PUMP",        "15A  |  14 AWG  |  100W", C_BATT),
        ("D", "SAFELIGHT",         "5A  |  18 AWG  |  15W", "#FFEEDD"),
        ("E", "EVAP COOLER (12V)", "10A  |  14 AWG  |  80W", C_SOLAR),
        ("F", "ACTUATORS (opt.)",  "20A  |  12 AWG  |  100W peak", "#E8E8E8"),
    ]

    # Fan out from fuse block top-right area across the page
    circ_x_start = 5.5
    circ_y_top   = FH - 1.2
    circ_w, circ_h = 2.8, 0.72
    circ_gap = 0.95

    # Horizontal bus line from fuse block
    bus_x = fbx + fbw
    bus_y = fby + fbh * 0.6
    ax.plot([bus_x, circ_x_start - 0.15], [bus_y, bus_y],
            color=C_CL, lw=2.0, zorder=3)

    # Vertical spine
    vspine_x = circ_x_start - 0.15
    y_bottom_circuit = circ_y_top - (len(circuits) - 1) * circ_gap - circ_h
    ax.plot([vspine_x, vspine_x], [bus_y, circ_y_top + circ_h/2 + 0.1],
            color=C_CL, lw=2.0, zorder=3)

    for i, (letter, name, spec, fc_c) in enumerate(circuits):
        cy = circ_y_top - i * circ_gap
        # tap off spine
        ax.plot([vspine_x, circ_x_start], [cy + circ_h/2, cy + circ_h/2],
                color=C_CL, lw=1.2, zorder=3)
        # fuse symbol
        fuse_x = circ_x_start - 0.05
        ax.add_patch(mpatches.Rectangle((fuse_x, cy + circ_h/2 - 0.08), 0.12, 0.16,
                     fc=C_WARN, ec=C_OUT, lw=0.8, zorder=4))
        # circuit box
        box(ax, circ_x_start + 0.1, cy, circ_w, circ_h,
            f"Cct {letter}  —  {name}", spec,
            fc=fc_c, fontsize=7.5, subfontsize=6.0)

    # ── Legend ────────────────────────────────────────────────────────────────
    lx, ly = 8.6, 4.0
    ax.text(lx, ly + 1.25, "LEGEND", ha="left", va="center",
            fontsize=7.5, fontweight="bold", color=C_OUT)
    legend_items = [
        (C_SOLAR, "Solar / generation"),
        (C_BATT,  "Battery / storage"),
        (C_ELEC,  "Controller / charger"),
        (C_WARN,  "Fuse / protection"),
        (C_ALUM,  "Ventilation loads"),
        (C_GND,   "Earth / ground"),
    ]
    for j, (col, txt) in enumerate(legend_items):
        yl = ly + 0.95 - j * 0.32
        ax.add_patch(mpatches.Rectangle((lx, yl - 0.10), 0.28, 0.22,
                     fc=col, ec=C_OUT, lw=0.7, zorder=4))
        ax.text(lx + 0.38, yl + 0.01, txt, ha="left", va="center",
                fontsize=6.5, color=C_DIM)

    # ── Energy summary box ────────────────────────────────────────────────────
    ex, ey, ew, eh = 8.6, 1.0, 4.8, 2.7
    ax.add_patch(FancyBboxPatch((ex, ey), ew, eh,
                 boxstyle="round,pad=0.05",
                 fc="#F8F9FA", ec=C_DIM, lw=1.0, zorder=3))
    ax.text(ex + ew/2, ey + eh - 0.25, "ENERGY SUMMARY",
            ha="center", va="center", fontsize=7.5,
            fontweight="bold", color=TITLE_COL)
    summary_lines = [
        ("Battery capacity",   "200Ah × 12V = 2,400 Wh usable"),
        ("Session energy",     "~1.5–1.8 kWh per print"),
        ("Sessions per charge","1.3–1.6 prints from full"),
        ("Solar generation",   "600W × 5.5h = 3,300 Wh/day (Palm Springs)"),
        ("Recharge time",      "~14h from flat via shore charger"),
        ("Peak draw",          "~415W (all loads on)"),
    ]
    for k, (param, val) in enumerate(summary_lines):
        yk = ey + eh - 0.60 - k * 0.33
        ax.text(ex + 0.2, yk, param + ":", ha="left", va="center",
                fontsize=6.0, fontweight="bold", color=C_OUT)
        ax.text(ex + ew - 0.15, yk, val, ha="right", va="center",
                fontsize=6.0, color=C_DIM)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, FW, 1, 2,
                "SYSTEM ONE-LINE DIAGRAM",
                "Power flow  ·  Component specs  ·  Circuit fuse ratings",
                "Not to scale")

    plt.savefig("electrical-sheet1.png", dpi=150, bbox_inches="tight",
                pad_inches=0.05, facecolor="white")
    plt.close(fig)
    print("  → electrical-sheet1.png  Done.")


# ─────────────────────────────────────────────────────────────────────────────
# SHEET 2 — Container Floor Plan + Wiring Layout
# ─────────────────────────────────────────────────────────────────────────────

def draw_sheet2():
    FW, FH = 16.0, 10.0
    fig, ax = plt.subplots(figsize=(FW, FH), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(0, FW)
    ax.set_ylim(0, FH)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    ax.text(FW/2, FH - 0.35,
            "CONTAINER FLOOR PLAN & WIRING LAYOUT — TBS-001",
            ha="center", va="center", fontsize=12,
            fontweight="bold", color=TITLE_COL)
    ax.text(FW/2, FH - 0.65,
            "Top-down plan view  ·  Scale 1:60  ·  All dimensions in mm",
            ha="center", va="center", fontsize=7.5, color=C_DIM)

    # ── Scale: 1:60, 1mm drawing = 60mm real
    # Container interior: 5,898 × 2,352mm → 98.3 × 39.2 drawing units
    # Use 1 unit = 60mm → scale factor
    S = 1/60.0  # drawing mm per real mm

    # Origin: bottom-left of container interior at (1.0, 1.5) drawing coords
    OX, OY = 1.0, 1.5

    # Real dimensions (mm)
    C_LEN  = 5898    # container interior length (long axis, horizontal)
    C_WID  = 2352    # container interior width (short axis, vertical on plan)
    VEST_D = 1200    # vestibule depth
    VEST_W = 2352    # vestibule width (same as container)
    WALL_T = 50      # wall thickness (schematic)

    # Drawing dimensions
    clen = C_LEN * S   # ~98.3
    cwid = C_WID * S   # ~39.2
    vd   = VEST_D * S  # 20.0
    vw   = VEST_W * S

    # ── Container outline ─────────────────────────────────────────────────────
    # Long axis horizontal, cargo doors at RIGHT end
    ax.add_patch(mpatches.Rectangle((OX, OY), clen, cwid,
                 fc="#F5F5F0", ec=C_OUT, lw=2.0, zorder=2))
    # Wall hatch (thin lines at corners to suggest thickness)
    wall_t_d = WALL_T * S
    for seg in [(OX, OY, clen, wall_t_d),          # bottom wall
                (OX, OY+cwid-wall_t_d, clen, wall_t_d),  # top wall
                (OX, OY, wall_t_d, cwid),            # left (pinhole) wall
                (OX+clen-wall_t_d, OY, wall_t_d, cwid)]:  # right (door) wall
        ax.add_patch(mpatches.Rectangle(seg[:2], seg[2], seg[3],
                     fc=C_STEEL, ec=C_OUT, lw=0.5, zorder=3))

    # ── Vestibule (right of container) ────────────────────────────────────────
    vx = OX + clen
    vy = OY
    ax.add_patch(mpatches.Rectangle((vx, vy), vd, vw,
                 fc="#EEF4EE", ec=C_OUT, lw=1.5, zorder=2,
                 linestyle="--"))
    # S-path baffles inside vestibule
    b_proj = 0.3 * vw  # baffle projection
    # baffle 1 — from bottom
    ax.add_patch(mpatches.Rectangle((vx + vd*0.3, vy), 0.04*vd, b_proj,
                 fc=C_STEEL, ec=C_OUT, lw=0.8, zorder=4))
    # baffle 2 — from top
    ax.add_patch(mpatches.Rectangle((vx + vd*0.65, vy + vw - b_proj), 0.04*vd, b_proj,
                 fc=C_STEEL, ec=C_OUT, lw=0.8, zorder=4))
    # exterior door
    ax.add_patch(mpatches.Rectangle((vx + vd - 0.12, vy + vw*0.2),
                 0.12, vw * 0.6, fc="white", ec=C_OUT, lw=1.0, zorder=4))
    ax.text(vx + vd/2, vy + vw/2, "LIGHT\nTRAP\nVESTIBULE",
            ha="center", va="center", fontsize=5.5, color="#2D6A2D",
            fontweight="bold", zorder=5)

    # ── Film plane (left short wall — image plane) ────────────────────────────
    fp_y = OY + cwid * 0.05
    fp_h = cwid * 0.90
    ax.add_patch(mpatches.Rectangle((OX + wall_t_d, fp_y), 0.5, fp_h,
                 fc="#A8C8E8", ec=C_CL, lw=1.2, zorder=4))
    ax.text(OX + wall_t_d + 0.25, fp_y + fp_h/2,
            "IMAGE\nPLANE\n(film plane\nmechanism)",
            ha="center", va="center", fontsize=5.0, color=TITLE_COL,
            rotation=90, zorder=5)

    # ── Pinhole (centre of left long wall — top wall in plan) ────────────────
    # Actually: pinhole is on one LONG wall (top or bottom). Let's say it's
    # centred on the top long wall.
    ph_x = OX + clen * 0.5
    ph_y_wall = OY + cwid - wall_t_d
    ax.add_patch(plt.Circle((ph_x, ph_y_wall + wall_t_d/2),
                 0.25, fc="black", ec=C_OUT, lw=1.0, zorder=5))
    ax.annotate("PINHOLE\n(Ø2.17mm)", xy=(ph_x, ph_y_wall + wall_t_d/2),
                xytext=(ph_x - 1.0, ph_y_wall + wall_t_d + 0.8),
                fontsize=5.5, color=C_OUT, ha="center",
                arrowprops=dict(arrowstyle="-", color=C_DIM, lw=0.8))

    # ── Electrical enclosure ──────────────────────────────────────────────────
    enc_x = OX + clen - wall_t_d - 1.8
    enc_y = OY + cwid * 0.55
    enc_w, enc_h = 1.5, 0.9
    box(ax, enc_x, enc_y, enc_w, enc_h,
        "ELEC\nPANEL", "IP65 enclosure\nFuse block + MPPT",
        fc=C_ELEC, fontsize=5.5, subfontsize=4.5)

    # ── Battery bank ──────────────────────────────────────────────────────────
    bat_x = OX + clen - wall_t_d - 1.8
    bat_y = OY + cwid * 0.15
    bat_w, bat_h = 1.5, 0.75
    box(ax, bat_x, bat_y, bat_w, bat_h,
        "BATTERY\nBANK", "2×100Ah LiFePO4",
        fc=C_BATT, fontsize=5.5, subfontsize=4.5)

    # ── Ventilation fans ──────────────────────────────────────────────────────
    # Intake fan: right (door) end short wall, low position
    fan_in_x = OX + clen - wall_t_d - 0.4
    fan_in_y = OY + cwid * 0.12
    ax.add_patch(plt.Circle((fan_in_x, fan_in_y), 0.28,
                 fc=C_ALUM, ec=C_OUT, lw=0.8, zorder=4))
    ax.text(fan_in_x, fan_in_y, "FAN\nIN", ha="center", va="center",
            fontsize=4.5, color=C_OUT, zorder=5)
    ax.annotate("Cct A\n6\" intake", xy=(fan_in_x, fan_in_y),
                xytext=(fan_in_x + 0.7, fan_in_y - 0.5),
                fontsize=5.0, color=C_DIM, ha="left",
                arrowprops=dict(arrowstyle="-", color=C_DIM, lw=0.7))

    # Exhaust fan: left (pinhole) end short wall, high position
    fan_ex_x = OX + wall_t_d + 0.4
    fan_ex_y = OY + cwid * 0.85
    ax.add_patch(plt.Circle((fan_ex_x, fan_ex_y), 0.28,
                 fc=C_ALUM, ec=C_OUT, lw=0.8, zorder=4))
    ax.text(fan_ex_x, fan_ex_y, "FAN\nOUT", ha="center", va="center",
            fontsize=4.5, color=C_OUT, zorder=5)
    ax.annotate("Cct B\n6\" exhaust", xy=(fan_ex_x, fan_ex_y),
                xytext=(fan_ex_x + 0.5, fan_ex_y + 0.7),
                fontsize=5.0, color=C_DIM, ha="left",
                arrowprops=dict(arrowstyle="-", color=C_DIM, lw=0.7))

    # ── Evaporative cooler ────────────────────────────────────────────────────
    cool_x = OX + clen * 0.55
    cool_y = OY + cwid * 0.1
    cool_w, cool_h = 1.4, 0.65
    box(ax, cool_x, cool_y, cool_w, cool_h,
        "EVAP\nCOOLER", "Cct E  |  80W 12V",
        fc=C_SOLAR, fontsize=5.5, subfontsize=4.5)
    # cooler intake duct on bottom long wall
    ax.add_patch(mpatches.Rectangle((cool_x + cool_w/2 - 0.15, OY),
                 0.30, wall_t_d, fc="#A8D8B0", ec=C_OUT, lw=0.7, zorder=4))
    ax.annotate("Light-safe\nbaffled intake", xy=(cool_x + cool_w/2, OY),
                xytext=(cool_x + cool_w/2 + 1.0, OY - 0.5),
                fontsize=5.0, color=C_DIM,
                arrowprops=dict(arrowstyle="-", color=C_DIM, lw=0.7))

    # ── Water system IBC totes ────────────────────────────────────────────────
    for i, (label_t, col_t) in enumerate([("IBC\nBLUE\n(wash)", "#C8E8FF"),
                                           ("IBC\nGREY\n(waste)", "#D8D8D8")]):
        tx = OX + wall_t_d + 1.0 + i * 2.2
        ty = OY + cwid * 0.35
        tw, thh = 1.8, 1.6
        ax.add_patch(mpatches.Rectangle((tx, ty), tw, thh,
                     fc=col_t, ec=C_OUT, lw=0.8, zorder=3))
        ax.text(tx + tw/2, ty + thh/2, label_t,
                ha="center", va="center", fontsize=5.0, color=C_OUT, zorder=4)

    # Water pump
    wp_x = OX + wall_t_d + 5.2
    wp_y = OY + cwid * 0.48
    ax.add_patch(plt.Circle((wp_x, wp_y), 0.30,
                 fc=C_BATT, ec=C_OUT, lw=0.8, zorder=4))
    ax.text(wp_x, wp_y, "PUMP\nCct C", ha="center", va="center",
            fontsize=4.5, color=C_OUT, zorder=5)

    # ── NEMA inlet on exterior ─────────────────────────────────────────────────
    nm_x = OX + clen + vd + 0.05
    nm_y = OY + cwid * 0.6
    ax.add_patch(mpatches.Rectangle((nm_x, nm_y), 0.5, 0.5,
                 fc="#FFF0CC", ec=C_OUT, lw=0.8, zorder=4))
    ax.text(nm_x + 0.25, nm_y + 0.25, "NEMA\nINLET",
            ha="center", va="center", fontsize=4.5, color=C_OUT, zorder=5)
    ax.annotate("Shore\npower\n(backup)", xy=(nm_x + 0.25, nm_y),
                xytext=(nm_x + 0.25, nm_y - 0.8),
                fontsize=5.0, color="#B08020", ha="center",
                arrowprops=dict(arrowstyle="-", color="#B08020", lw=0.8))

    # ── Conduit routes (dashed) ────────────────────────────────────────────────
    trunk_y = OY + cwid - wall_t_d - 0.3   # top rail trunking
    trunk_x1 = OX + wall_t_d
    trunk_x2 = OX + clen - wall_t_d
    ax.plot([trunk_x1, trunk_x2], [trunk_y, trunk_y],
            color=C_PIPE, lw=2.0, linestyle="-", zorder=3,
            label="Cable trunking (top corner rail)")
    ax.text((trunk_x1 + trunk_x2)/2, trunk_y + 0.25,
            "40×25mm PVC cable trunking — all circuits routed here",
            ha="center", va="bottom", fontsize=5.0, color=C_PIPE)

    # Drop lines from trunking to devices
    for dx, dy in [(enc_x + enc_w/2, enc_y + enc_h),
                   (bat_x + bat_w/2, bat_y + bat_h),
                   (fan_in_x, fan_in_y + 0.28),
                   (cool_x + cool_w/2, cool_y + cool_h)]:
        ax.plot([dx, dx], [trunk_y, dy], color=C_PIPE,
                lw=0.8, linestyle=":", zorder=2)

    # ── Dimensions ────────────────────────────────────────────────────────────
    dim_col = C_DIM

    def dim_h(x1, x2, y_d, text, above=True):
        off = 0.25 if above else -0.25
        yt = y_d + off
        ax.annotate("", xy=(x2, y_d), xytext=(x1, y_d),
                    arrowprops=dict(arrowstyle="<->", color=dim_col, lw=0.7))
        ax.text((x1+x2)/2, yt, text, ha="center", va="center",
                fontsize=5.0, color=dim_col)

    def dim_v(x_d, y1, y2, text, right=True):
        off = 0.25 if right else -0.25
        xt = x_d + off
        ax.annotate("", xy=(x_d, y2), xytext=(x_d, y1),
                    arrowprops=dict(arrowstyle="<->", color=dim_col, lw=0.7))
        ax.text(xt, (y1+y2)/2, text, ha="left" if right else "right",
                va="center", fontsize=5.0, color=dim_col, rotation=90)

    # Container length
    dim_h(OX, OX + clen, OY - 0.5, "5,898mm (interior length)")
    # Container width
    dim_v(OX - 0.5, OY, OY + cwid, "2,352mm (interior width)")
    # Vestibule depth
    dim_h(vx, vx + vd, OY - 0.5, "1,200mm (vestibule)")

    # ── Legend ────────────────────────────────────────────────────────────────
    lx2, ly2 = OX + clen + vd + 0.8, OY + cwid - 0.3
    ax.text(lx2, ly2, "LEGEND", ha="left", va="top",
            fontsize=7.0, fontweight="bold", color=C_OUT)
    leg2 = [
        (C_BATT,  "Battery / water loads"),
        (C_ALUM,  "Ventilation"),
        (C_SOLAR, "Cooling"),
        (C_ELEC,  "Electrical panel"),
        (C_PIPE,  "Cable trunking route"),
        ("#A8C8E8", "Film plane"),
        ("#EEF4EE", "Light trap vestibule"),
    ]
    for j2, (col2, txt2) in enumerate(leg2):
        yl2 = ly2 - 0.45 - j2 * 0.38
        ax.add_patch(mpatches.Rectangle((lx2, yl2 - 0.12), 0.30, 0.25,
                     fc=col2, ec=C_OUT, lw=0.7, zorder=5))
        ax.text(lx2 + 0.42, yl2, txt2, ha="left", va="center",
                fontsize=5.5, color=C_DIM)

    # ── North arrow / orientation ─────────────────────────────────────────────
    nx, ny = OX + clen + vd + 0.9, OY + 1.2
    ax.annotate("", xy=(nx, ny + 0.6), xytext=(nx, ny),
                arrowprops=dict(arrowstyle="-|>", color=C_CL, lw=1.5))
    ax.text(nx, ny + 0.75, "N", ha="center", va="bottom",
            fontsize=7, fontweight="bold", color=C_CL)
    ax.text(nx, ny - 0.2, "(schematic\norientation)", ha="center",
            va="top", fontsize=4.5, color=C_DIM)

    # ── Title block ───────────────────────────────────────────────────────────
    title_block(ax, FW, 2, 2,
                "CONTAINER FLOOR PLAN & WIRING LAYOUT",
                "Top-down plan  ·  Component positions  ·  Conduit routes",
                "1:60  (1 unit = 60mm)")

    plt.savefig("electrical-sheet2.png", dpi=150, bbox_inches="tight",
                pad_inches=0.05, facecolor="white")
    plt.close(fig)
    print("  → electrical-sheet2.png  Done.")


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Generating TBS-001 Electrical & Systems diagrams...")
    draw_sheet1()
    draw_sheet2()
    print("Done.")
