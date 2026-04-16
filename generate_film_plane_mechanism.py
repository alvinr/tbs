#!/usr/bin/env python3
"""
generate_film_plane_mechanism.py
Moveable film plane mechanism — engineering drawings (4 sheets)

Sheet 1 — Plan view (top-down): rail layout, beam travel, tilt configs
Sheet 2 — Side elevation (cross-section): tilt angles, Scheimpflug lines
Sheet 3 — Frame & hardware detail: beam, carriage, pivot, ACM panel
Sheet 4 — Movement specification table
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, FancyArrowPatch, Polygon
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe

# ── Palette (blueprint dark style) ───────────────────────────────────────────
BG      = "#08152A"
GRID    = "#122040"
STRUCT  = "#1D4E89"
STRUCT2 = "#2A72BA"
DIM     = "#6BBCD4"
ANNO    = "#A8D8EA"
WHITE   = "#E8F4FD"
C_FLAT  = "#90C8E0"   # config 0 — flat
C_T1    = "#72CC72"   # mild tilt
C_T2    = "#E8B840"   # strong tilt
C_T3    = "#E85050"   # max tilt
RAIL    = "#C8A040"   # hardware / rail
MECH    = "#A0D0A0"   # moving parts
PINHOLE = "#F0E060"   # pinhole marker

# ── Container dimensions (mm) ─────────────────────────────────────────────────
L = 5893   # interior length (film plane spans this direction)
W = 2362   # interior width = optical axis = focal length
H = 2388   # interior height
WALL_T = 40

# Carriage travel limits (100 mm clearance each end)
D_NEAR = 100
D_FAR  = W - 100   # = 2262

# Tilt configurations (top_depth, bottom_depth) from pinhole wall
CONFIGS = [
    ("Flat  0°",     D_FAR,  D_FAR,  C_FLAT, "-"),
    ("Mild  5.6°",   1800,   D_FAR,  C_T1,   "--"),
    ("Strong 17.5°", 800,    D_FAR,  C_T2,   "-."),
    ("Max  41.6°",   D_NEAR, D_FAR,  C_T3,   ":"),
]

FONT = {"fontfamily": "monospace"}

def title_block(ax, sheet_no, title, scale_note=""):
    """Standard title block at bottom of sheet."""
    ax.text(0.01, 0.012, f"GIANT PINHOLE CAMERA  ·  GPC-001",
            transform=ax.transAxes, color=DIM, fontsize=7, **FONT)
    ax.text(0.01, 0.004, f"MOVEABLE FILM PLANE — SHEET {sheet_no}: {title}",
            transform=ax.transAxes, color=WHITE, fontsize=7.5, fontweight="bold", **FONT)
    if scale_note:
        ax.text(0.99, 0.012, scale_note,
                transform=ax.transAxes, color=DIM, fontsize=6.5,
                ha="right", **FONT)
    ax.text(0.99, 0.004, "ALL DIMS IN mm UNLESS NOTED",
            transform=ax.transAxes, color=DIM, fontsize=6.5, ha="right", **FONT)

def dim_line_h(ax, x0, x1, y, text, offset=30, col=DIM, fs=7):
    """Horizontal dimension line with arrows and label."""
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="<->", color=col, lw=0.9,
                                mutation_scale=6))
    ax.text((x0+x1)/2, y+offset, text, color=col, fontsize=fs,
            ha="center", va="bottom", **FONT)

def dim_line_v(ax, x, y0, y1, text, offset=30, col=DIM, fs=7):
    """Vertical dimension line."""
    ax.annotate("", xy=(x, y1), xytext=(x, y0),
                arrowprops=dict(arrowstyle="<->", color=col, lw=0.9,
                                mutation_scale=6))
    ax.text(x+offset, (y0+y1)/2, text, color=col, fontsize=fs,
            ha="left", va="center", rotation=0, **FONT)

def leader(ax, xy, xytext, text, col=ANNO, fs=6.5):
    ax.annotate(text, xy=xy, xytext=xytext, color=col, fontsize=fs,
                **FONT, ha="center",
                arrowprops=dict(arrowstyle="-|>", color=col, lw=0.7,
                                mutation_scale=5))

# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1 — PLAN VIEW (overhead, Z looking down)
# X = container length (0→L), Y = optical axis depth (0=pinhole wall → W=image wall)
# ═══════════════════════════════════════════════════════════════════════════════
def sheet1():
    fig, ax = plt.subplots(figsize=(16, 8))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    PAD = 500
    ax.set_xlim(-PAD, L + PAD)
    ax.set_ylim(-PAD, W + 700)
    ax.set_aspect("equal")
    ax.axis("off")

    # Container outline
    ax.add_patch(Rectangle((0, 0), L, W, fc=STRUCT, ec=WHITE, lw=1.8, zorder=2))
    ax.add_patch(Rectangle((0, 0), L, W, fc=GRID, ec=WHITE, lw=1.8, zorder=2))

    # Container wall hatching (structural steel)
    for x in np.arange(80, L, 457):
        ax.plot([x, x], [0, W], color=STRUCT2, lw=0.4, alpha=0.35, zorder=3)

    # Pinhole wall (y=0) — highlighted
    ax.add_patch(Rectangle((0, -WALL_T), L, WALL_T, fc=STRUCT2, ec=WHITE, lw=1.5, zorder=4))
    ax.text(L/2, -WALL_T/2, "PINHOLE WALL  (20ft LONG SIDE)",
            color=WHITE, fontsize=7.5, ha="center", va="center", **FONT, zorder=5)

    # Far wall (y=W)
    ax.add_patch(Rectangle((0, W), L, WALL_T, fc=STRUCT, ec=WHITE, lw=1.0, zorder=4))
    ax.text(L/2, W + WALL_T/2, "FAR WALL  (20ft LONG SIDE)",
            color=DIM, fontsize=7, ha="center", va="center", **FONT, zorder=5)

    # End walls
    for xw in [(-WALL_T, -WALL_T, 0, W+WALL_T), (L, 0, WALL_T, W+2*WALL_T)]:
        ax.add_patch(Rectangle((xw[0], xw[1]), xw[2], xw[3],
                               fc=STRUCT, ec=WHITE, lw=1.0, zorder=4))

    # Pinhole symbol
    ph_x = L / 2
    ax.add_patch(Circle((ph_x, 0), 60, fc=PINHOLE, ec=WHITE, lw=1.5, zorder=6))
    ax.add_patch(Circle((ph_x, 0), 20, fc=BG, ec=WHITE, lw=1.0, zorder=7))
    ax.text(ph_x + 180, -250, "PINHOLE  Ø2.17mm", color=PINHOLE,
            fontsize=7, **FONT, zorder=7)

    # ── RAILS (4 total: 2 near left wall, 2 near right wall) ─────────────────
    RAIL_W = 60      # rail width in plan view
    RAIL_X_L = 200   # distance from container left end
    RAIL_X_R = L - 200 - RAIL_W  # near right end
    rail_y0 = D_NEAR
    rail_y1 = D_FAR

    for rx in [RAIL_X_L, RAIL_X_R]:
        ax.add_patch(Rectangle((rx, rail_y0), RAIL_W, rail_y1-rail_y0,
                               fc=RAIL, ec=WHITE, lw=1.0, zorder=5, alpha=0.9))
        # Rail end stops
        for ry in [rail_y0, rail_y1]:
            ax.add_patch(Rectangle((rx-20, ry-15), RAIL_W+40, 30,
                                   fc=WHITE, ec=WHITE, lw=0.5, zorder=6))

    ax.text(RAIL_X_L + 30, D_NEAR + (D_FAR-D_NEAR)/2, "HGR20\nRAIL",
            color=BG, fontsize=6, ha="center", va="center", **FONT,
            rotation=90, zorder=7)

    # Travel arrow
    ax.annotate("", xy=(RAIL_X_L+30, D_FAR-20), xytext=(RAIL_X_L+30, D_NEAR+20),
                arrowprops=dict(arrowstyle="<->", color=WHITE, lw=0.8,
                                mutation_scale=5), zorder=8)
    ax.text(RAIL_X_L-120, (D_NEAR+D_FAR)/2, f"{D_FAR-D_NEAR}\nmm\ntravel",
            color=WHITE, fontsize=6.5, ha="center", va="center", **FONT)

    # ── TILT CONFIGURATIONS — top beam (solid) + bottom beam (dashed) ─────────
    BEAM_W_PLAN = 80   # beam height in plan view

    for i, (name, d_top, d_bot, col, ls) in enumerate(CONFIGS):
        alpha = 0.95 if i == 0 else 0.82
        lw = 2.0 if i == 0 else 1.6

        # Top beam (near left rail — at x=RAIL_X_L, near right at x=RAIL_X_R)
        # In plan view the top beam appears as a wide horizontal band at y=d_top
        ax.add_patch(Rectangle((RAIL_X_L+RAIL_W, d_top - BEAM_W_PLAN//2),
                               RAIL_X_R - (RAIL_X_L+RAIL_W),
                               BEAM_W_PLAN,
                               fc=col, ec=col, lw=0, zorder=4+i,
                               alpha=0.18 if i > 0 else 0.25))
        ax.plot([RAIL_X_L+RAIL_W, RAIL_X_R],
                [d_top, d_top],
                color=col, lw=lw, ls=ls, alpha=alpha, zorder=6+i,
                label=f"TOP BEAM — {name}")

        # Bottom beam (dashed if different from top)
        if d_bot != d_top:
            ax.plot([RAIL_X_L+RAIL_W, RAIL_X_R],
                    [d_bot, d_bot],
                    color=col, lw=lw*0.8, ls=":", alpha=0.75, zorder=6+i)
            # Connector lines at ends
            for bx in [RAIL_X_L+RAIL_W, RAIL_X_R]:
                ax.plot([bx, bx], [d_top, d_bot],
                        color=col, lw=0.7, ls="-", alpha=0.5, zorder=5+i)

        # Label at right
        label_y = (d_top + d_bot) / 2
        ax.text(RAIL_X_R + 150, label_y, f"{name}\nT={d_top}  B={d_bot}",
                color=col, fontsize=6.5, va="center", **FONT, zorder=8)

    # Carriage markers
    for i, (_, d_top, d_bot, col, _) in enumerate(CONFIGS):
        for rx in [RAIL_X_L, RAIL_X_R]:
            ax.add_patch(Rectangle((rx-15, d_top-50), RAIL_W+30, 100,
                                   fc=col, ec=WHITE, lw=0.7,
                                   alpha=0.6, zorder=7+i))

    # ── Dimension annotations ─────────────────────────────────────────────────
    dim_line_h(ax, 0, L, W+350, f"INTERIOR LENGTH  {L} mm  (19 ft 4 in)",
               offset=0, col=DIM, fs=7.5)
    dim_line_v(ax, L+250, 0, W, f"OPTICAL AXIS  {W} mm  (7 ft 9 in)",
               offset=20, col=DIM)
    dim_line_v(ax, -350, D_NEAR, D_FAR, f"TRAVEL  {D_FAR-D_NEAR} mm",
               offset=-260, col=RAIL)
    dim_line_h(ax, 0, RAIL_X_L, -250, f"{RAIL_X_L}", col=DIM, fs=6.5)

    # Optical axis arrow
    ax.annotate("", xy=(ph_x, W-150), xytext=(ph_x, 150),
                arrowprops=dict(arrowstyle="-|>", color=PINHOLE,
                                lw=1.2, mutation_scale=8), zorder=8)
    ax.text(ph_x+200, W/2, "OPTICAL AXIS", color=PINHOLE,
            fontsize=7, rotation=90, va="center", **FONT)

    # Legend
    legend_x = L + 200
    legend_y = W + 500
    ax.text(legend_x - 200, legend_y, "LEGEND", color=WHITE,
            fontsize=8, fontweight="bold", **FONT)
    for i, (name, d_top, d_bot, col, ls) in enumerate(CONFIGS):
        ly = legend_y - 120 - i*110
        ax.plot([legend_x-200, legend_x+100], [ly, ly],
                color=col, lw=2.0, ls=ls)
        ax.text(legend_x+150, ly, f"TOP BEAM  {name}\n(top={d_top}, bot={d_bot})",
                color=col, fontsize=6.5, va="center", **FONT)

    ax.text(L/2, W + 580, "SHEET 1 — PLAN VIEW  (TOP DOWN, LOOKING AT CONTAINER FLOOR)",
            color=WHITE, fontsize=9, ha="center", fontweight="bold", **FONT)
    ax.text(L/2, W + 480,
            "SHOWS TOP BEAM (solid) AND BOTTOM BEAM (dotted) POSITIONS FOR EACH TILT CONFIG",
            color=DIM, fontsize=7, ha="center", **FONT)

    title_block(ax, "1 / 4", "PLAN VIEW — RAIL LAYOUT & BEAM POSITIONS",
                "SCALE: PROPORTIONAL (mm)")
    fig.tight_layout(pad=0.3)
    fig.savefig("film-plane-sheet1.png", dpi=130, bbox_inches="tight",
                facecolor=BG)
    plt.close(fig)
    print("  → film-plane-sheet1.png")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2 — SIDE ELEVATION (cross-section looking along container length)
# X = optical axis depth (0=pinhole → W=image wall), Y = height (0=floor → H=ceiling)
# ═══════════════════════════════════════════════════════════════════════════════
def sheet2():
    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    PADX, PADY = 350, 350
    ax.set_xlim(-PADX, W + PADX)
    ax.set_ylim(-PADY, H + PADY + 100)
    ax.set_aspect("equal")
    ax.axis("off")

    # Container walls
    # Pinhole wall (left)
    ax.add_patch(Rectangle((-WALL_T, -WALL_T), WALL_T, H+2*WALL_T,
                           fc=STRUCT2, ec=WHITE, lw=2.0, zorder=4))
    # Far wall (right)
    ax.add_patch(Rectangle((W, -WALL_T), WALL_T, H+2*WALL_T,
                           fc=STRUCT, ec=WHITE, lw=1.5, zorder=4))
    # Floor
    ax.add_patch(Rectangle((-WALL_T, -WALL_T), W+2*WALL_T, WALL_T,
                           fc=STRUCT, ec=WHITE, lw=1.5, zorder=4))
    # Ceiling
    ax.add_patch(Rectangle((-WALL_T, H), W+2*WALL_T, WALL_T,
                           fc=STRUCT, ec=WHITE, lw=1.5, zorder=4))

    # Interior fill
    ax.add_patch(Rectangle((0, 0), W, H, fc=GRID, ec="none", zorder=2))

    # Wall labels
    ax.text(-WALL_T/2, H/2, "PINHOLE\nWALL",
            color=WHITE, fontsize=6.5, ha="center", va="center",
            rotation=90, **FONT, zorder=5)
    ax.text(W + WALL_T/2, H/2, "FAR\nWALL",
            color=DIM, fontsize=6.5, ha="center", va="center",
            rotation=90, **FONT, zorder=5)

    # ── Rails on ceiling and floor ────────────────────────────────────────────
    RAIL_H_ELEV = 30   # rail height in elevation view
    RAIL_W_ELEV = D_FAR - D_NEAR

    # Floor rails (bottom carriage)
    ax.add_patch(Rectangle((D_NEAR, 0), RAIL_W_ELEV, RAIL_H_ELEV,
                           fc=RAIL, ec=WHITE, lw=0.8, zorder=5, alpha=0.9))
    ax.text(W/2, RAIL_H_ELEV/2, "FLOOR RAIL  HGR20  ×2",
            color=BG, fontsize=6, ha="center", va="center", **FONT, zorder=6)

    # Ceiling rails (top carriage)
    ax.add_patch(Rectangle((D_NEAR, H-RAIL_H_ELEV), RAIL_W_ELEV, RAIL_H_ELEV,
                           fc=RAIL, ec=WHITE, lw=0.8, zorder=5, alpha=0.9))
    ax.text(W/2, H - RAIL_H_ELEV/2, "CEILING RAIL  HGR20  ×2",
            color=BG, fontsize=6, ha="center", va="center", **FONT, zorder=6)

    # ── Tilt configurations — film plane lines ────────────────────────────────
    CARRIAGE_W = 80    # carriage block width (depth direction)
    CARRIAGE_H = 60    # carriage block height
    BEAM_D = 80        # beam depth (front-back)
    BEAM_H = 80        # beam height (cross-section = 80×80 box)

    for i, (name, d_top, d_bot, col, ls) in enumerate(CONFIGS):
        lw = 2.8 if i == 0 else 2.2
        alpha = 1.0 if i == 0 else 0.90
        zord = 10 + i

        # Top carriage block (on ceiling rail)
        tc_x = d_top - CARRIAGE_W/2
        tc_y = H - RAIL_H_ELEV - CARRIAGE_H
        ax.add_patch(Rectangle((tc_x, tc_y), CARRIAGE_W, CARRIAGE_H,
                               fc=col, ec=WHITE, lw=0.8, alpha=0.5, zorder=zord))

        # Bottom carriage block (on floor rail)
        bc_x = d_bot - CARRIAGE_W/2
        bc_y = RAIL_H_ELEV
        ax.add_patch(Rectangle((bc_x, bc_y), CARRIAGE_W, CARRIAGE_H,
                               fc=col, ec=WHITE, lw=0.8, alpha=0.5, zorder=zord))

        # Film plane line: from (d_top, H-RAIL_H_ELEV-CARRIAGE_H) to (d_bot, RAIL_H_ELEV+CARRIAGE_H)
        fp_top_y = tc_y   # film plane top y
        fp_bot_y = bc_y + CARRIAGE_H

        ax.plot([d_top, d_bot], [fp_top_y, fp_bot_y],
                color=col, lw=lw, ls=ls, alpha=alpha, zorder=zord+1,
                solid_capstyle="round")

        # Tilt angle arc (at bottom pivot)
        if d_top != d_bot:
            theta = np.degrees(np.arctan2(d_top - d_bot, fp_top_y - fp_bot_y))
            arc_r = 120
            from matplotlib.patches import Arc
            ax.add_patch(Arc((d_bot, fp_bot_y), arc_r*2, arc_r*2,
                             angle=0, theta1=90-abs(theta), theta2=90,
                             color=col, lw=1.0, alpha=0.8, zorder=zord))
            mid_ang = np.radians(90 - abs(theta)/2)
            ax.text(d_bot + arc_r*1.4*np.sin(np.radians(abs(theta)/2)),
                    fp_bot_y + arc_r*1.3*np.cos(np.radians(abs(theta)/2)),
                    f"{abs(theta):.1f}°",
                    color=col, fontsize=6.5, ha="center", **FONT, zorder=zord+2)

        # Label
        mid_x = (d_top + d_bot) / 2
        mid_y = (fp_top_y + fp_bot_y) / 2
        offset_x = 120 + i * 80
        ax.text(mid_x + offset_x, mid_y, name,
                color=col, fontsize=7, va="center", **FONT, zorder=zord+2)

    # ── Scheimpflug lines (for non-flat configs) ──────────────────────────────
    # The Scheimpflug line passes through: film plane intersection with lens plane extended
    # For pinhole: the "hinge line" — where tilted film plane meets the subject plane
    # Simplified: draw a line from the pinhole through the midpoint of each film plane
    PH_Y = H / 2   # pinhole height (centre of pinhole wall)

    for i, (name, d_top, d_bot, col, ls) in enumerate(CONFIGS):
        if d_top == d_bot:
            continue
        fp_top_y = H - RAIL_H_ELEV - 60
        fp_bot_y = RAIL_H_ELEV + 60
        # Line from pinhole (0, PH_Y) through film plane midpoint, extended
        mid_d = (d_top + d_bot) / 2
        mid_y = (fp_top_y + fp_bot_y) / 2
        # Extend line to scene space (x < 0 = outside container)
        if mid_d != 0:
            t = -200 / mid_d
            ext_y = PH_Y + (mid_y - PH_Y) * (1 - t)
            ax.plot([0, -200], [PH_Y, ext_y],
                    color=col, lw=0.8, ls=":", alpha=0.5, zorder=8)

    # ── Pinhole ───────────────────────────────────────────────────────────────
    ax.add_patch(Circle((0, PH_Y), 40, fc=PINHOLE, ec=WHITE, lw=1.5, zorder=12))
    ax.add_patch(Circle((0, PH_Y), 15, fc=BG, ec=WHITE, lw=0.8, zorder=13))
    ax.text(-180, PH_Y, "PINHOLE\nØ2.17mm", color=PINHOLE,
            fontsize=7, ha="center", va="center", **FONT)

    # Focal-length arrow (flat config)
    fl_y = 60
    ax.annotate("", xy=(D_FAR, fl_y), xytext=(0, fl_y),
                arrowprops=dict(arrowstyle="<->", color=C_FLAT,
                                lw=1.0, mutation_scale=7), zorder=9)
    ax.text(D_FAR/2, fl_y + 40, f"FOCAL LENGTH  {W} mm  (FLAT CONFIG)",
            color=C_FLAT, fontsize=7, ha="center", **FONT)

    # ── Dimension annotations ─────────────────────────────────────────────────
    dim_line_h(ax, 0, W, H + 180, f"INTERIOR WIDTH (OPTICAL AXIS)  {W} mm",
               offset=0, col=DIM)
    dim_line_v(ax, W + 200, 0, H, f"INTERIOR HEIGHT  {H} mm",
               offset=20, col=DIM)
    dim_line_h(ax, D_NEAR, D_FAR, -220, f"RAIL TRAVEL  {D_FAR-D_NEAR} mm",
               offset=0, col=RAIL)

    # Clearance dim
    dim_line_h(ax, 0, D_NEAR, -120, f"{D_NEAR}", offset=0, col=DIM, fs=6.5)
    dim_line_h(ax, D_FAR, W, -120, f"{W-D_FAR}", offset=0, col=DIM, fs=6.5)

    # Legend
    ax.text(W + PADX - 20, H + 200, "TILT CONFIGS", color=WHITE,
            fontsize=8, fontweight="bold", ha="right", **FONT)
    for i, (name, d_top, d_bot, col, ls) in enumerate(CONFIGS):
        ly = H + 100 - i*100
        ang = np.degrees(np.arctan2(d_top-d_bot, H-120)) if d_top != d_bot else 0
        ax.plot([W+180, W+320], [ly, ly], color=col, lw=2.5, ls=ls)
        ax.text(W+360, ly, f"{name}  (T={d_top}, B={d_bot})",
                color=col, fontsize=6.5, va="center", **FONT)

    ax.text(W/2, H + 260,
            "SHEET 2 — SIDE ELEVATION  (CROSS-SECTION THROUGH CONTAINER CENTRELINE)",
            color=WHITE, fontsize=9, ha="center", fontweight="bold", **FONT)

    title_block(ax, "2 / 4", "SIDE ELEVATION — TILT CONFIGURATIONS", "SCALE: PROPORTIONAL (mm)")
    fig.tight_layout(pad=0.3)
    fig.savefig("film-plane-sheet2.png", dpi=130, bbox_inches="tight",
                facecolor=BG)
    plt.close(fig)
    print("  → film-plane-sheet2.png")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3 — FRAME & HARDWARE DETAIL
# ═══════════════════════════════════════════════════════════════════════════════
def sheet3():
    fig = plt.figure(figsize=(16, 12))
    fig.patch.set_facecolor(BG)

    # 2×2 sub-panels
    axes = []
    positions = [(0.04, 0.52, 0.44, 0.42),   # TL — beam cross-section
                 (0.52, 0.52, 0.44, 0.42),   # TR — carriage + rail detail
                 (0.04, 0.08, 0.44, 0.38),   # BL — pivot joint
                 (0.52, 0.08, 0.44, 0.38)]   # BR — ACM panel arrangement
    for p in positions:
        a = fig.add_axes(p)
        a.set_facecolor(BG)
        a.axis("off")
        axes.append(a)

    ax_beam, ax_rail, ax_pivot, ax_acm = axes

    # ── TL: 80×80 Aluminium box section / 80/20 T-slot cross-section ──────────
    ax = ax_beam
    ax.set_xlim(-150, 350); ax.set_ylim(-150, 350); ax.set_aspect("equal")

    S = 80   # 80mm section
    T = 8    # wall thickness
    ax.add_patch(Rectangle((0, 0), S, S, fc=STRUCT2, ec=WHITE, lw=2.0, zorder=3))
    ax.add_patch(Rectangle((T, T), S-2*T, S-2*T, fc=BG, ec="none", zorder=4))
    # T-slot grooves (80/20 style)
    G = 14; GD = 8
    for gx in [S*0.25-G/2, S*0.75-G/2]:
        ax.add_patch(Rectangle((gx, -GD), G, GD+T, fc=STRUCT, ec=WHITE, lw=0.7, zorder=5))
        ax.add_patch(Rectangle((gx, S), G, GD, fc=STRUCT, ec=WHITE, lw=0.7, zorder=5))
    for gy in [S*0.25-G/2, S*0.75-G/2]:
        ax.add_patch(Rectangle((-GD, gy), GD+T, G, fc=STRUCT, ec=WHITE, lw=0.7, zorder=5))
        ax.add_patch(Rectangle((S, gy), GD, G, fc=STRUCT, ec=WHITE, lw=0.7, zorder=5))
    # Centre bore
    ax.add_patch(Circle((S/2, S/2), 9, fc=BG, ec=WHITE, lw=0.8, zorder=5))

    dim_line_h(ax, 0, S, -80, "80 mm", offset=0, col=DIM)
    dim_line_v(ax, S+80, 0, S, "80 mm", offset=15, col=DIM)
    ax.text(S/2, S + 120, "HORIZONTAL BEAM SECTION\n80×80 ALUMINIUM T-SLOT EXTRUSION\n(80/20 10-4080  or  equiv.)",
            color=WHITE, fontsize=7.5, ha="center", va="bottom", **FONT)
    ax.text(S/2, -130, "MATERIAL: 6105-T5 aluminium  ·  SPAN: 5,893 mm  ×2",
            color=DIM, fontsize=6.5, ha="center", **FONT)

    # ── TR: HGR20 rail + HGH20CA carriage cross-section ─────────────────────
    ax = ax_rail
    ax.set_xlim(-200, 400); ax.set_ylim(-100, 350); ax.set_aspect("equal")

    # Rail profile (simplified HGR20)
    rl_w = 44; rl_h = 30   # HGR20: 44mm wide, 30mm tall
    ax.add_patch(FancyBboxPatch((-rl_w/2, 0), rl_w, rl_h,
                               boxstyle="round,pad=2",
                               fc=RAIL, ec=WHITE, lw=1.5, zorder=3))
    # Mounting holes
    for hx in [-16, 16]:
        ax.add_patch(Circle((hx, rl_h/2), 4.5, fc=BG, ec=WHITE, lw=0.8, zorder=4))
    # Rail groove (ball channel)
    for rx in [-12, 12]:
        ax.add_patch(Circle((rx, rl_h), 5, fc=BG, ec=WHITE, lw=0.7, zorder=4))

    # Carriage block (HGH20CA)
    cb_w = 63; cb_h = 55
    ax.add_patch(Rectangle((-cb_w/2, rl_h-5), cb_w, cb_h,
                           fc=MECH, ec=WHITE, lw=1.5, zorder=5))
    # Carriage mounting holes
    for cx_, cy_ in [(-22, rl_h+15), (22, rl_h+15), (-22, rl_h+38), (22, rl_h+38)]:
        ax.add_patch(Circle((cx_, cy_), 4, fc=BG, ec=WHITE, lw=0.7, zorder=6))

    dim_line_h(ax, -rl_w/2, rl_w/2, -50, f"{rl_w} mm", offset=0, col=DIM)
    dim_line_h(ax, -cb_w/2, cb_w/2, rl_h + cb_h + 40, f"{cb_w} mm", offset=0, col=DIM)
    dim_line_v(ax, cb_w/2+60, rl_h, rl_h+cb_h, f"{cb_h} mm", offset=15, col=MECH)

    ax.text(0, rl_h + cb_h + 120, "RAIL + CARRIAGE CROSS-SECTION\nHIWIN HGR20 RAIL  +  HGH20CA CARRIAGE",
            color=WHITE, fontsize=7.5, ha="center", va="bottom", **FONT)
    ax.text(0, -90, "LOAD RATING: 9.7 kN dynamic  ·  USE: 4× rail, 8× carriage",
            color=DIM, fontsize=6.5, ha="center", **FONT)
    ax.text(-80, rl_h/2, "HGR20\nRAIL", color=BG, fontsize=6.5,
            ha="center", va="center", rotation=90, **FONT)
    ax.text(0, rl_h + cb_h/2, "HGH20CA\nCARRIAGE", color=BG, fontsize=6.5,
            ha="center", va="center", **FONT)

    # ── BL: Pivot joint detail ────────────────────────────────────────────────
    ax = ax_pivot
    ax.set_xlim(-200, 500); ax.set_ylim(-150, 280); ax.set_aspect("equal")

    # Beam end
    bm_w = 100; bm_h = 80
    ax.add_patch(Rectangle((0, 0), bm_w, bm_h, fc=STRUCT2, ec=WHITE, lw=1.5, zorder=3))
    ax.add_patch(Rectangle((10, 10), bm_w-20, bm_h-20, fc=BG, ec="none", zorder=4))
    ax.text(bm_w/2, bm_h/2, "BEAM", color=DIM, fontsize=6, ha="center", **FONT)

    # Pivot flange
    fl_w = 30; fl_h = 120
    ax.add_patch(Rectangle((bm_w, -20), fl_w, fl_h,
                           fc=RAIL, ec=WHITE, lw=1.5, zorder=5))
    # Pin hole
    pin_y = bm_h / 2
    ax.add_patch(Circle((bm_w + fl_w/2, pin_y), 14, fc=BG, ec=WHITE, lw=1.0, zorder=6))
    ax.add_patch(Circle((bm_w + fl_w/2, pin_y), 12.7, fc=MECH, ec=WHITE, lw=0.8, zorder=7))

    # Film frame connecting bar
    ff_w = 120
    ax.add_patch(Rectangle((bm_w + fl_w, pin_y - 20), ff_w, 40,
                           fc=ANNO, ec=WHITE, lw=1.0, zorder=5, alpha=0.8))
    ax.add_patch(Circle((bm_w + fl_w + 25, pin_y), 14, fc=BG, ec=WHITE, lw=1.0, zorder=6))
    ax.add_patch(Circle((bm_w + fl_w + 25, pin_y), 12.7, fc=MECH, ec=WHITE, lw=0.8, zorder=7))

    # Igus bearing annotation
    leader(ax, (bm_w + fl_w/2, pin_y), (bm_w + fl_w/2, pin_y + 120),
           "IGUS DRYLIN\nJFM-01-25\nBEARING", col=MECH)

    # Dimensions
    dim_line_h(ax, bm_w, bm_w+fl_w, -80, f"{fl_w}", offset=0, col=DIM)
    dim_line_v(ax, bm_w + fl_w + ff_w + 60, pin_y-20, pin_y+20, "40", offset=15, col=ANNO)

    ax.text(100, 230, "PIVOT JOINT DETAIL — BEAM TO FILM FRAME\n25mm STEEL PIN  +  IGUS DRYLIN BEARING  ×8",
            color=WHITE, fontsize=7.5, ha="center", va="bottom", **FONT)
    ax.text(100, -130, "ALLOWS ±45° ROTATION  ·  LOCKS WITH COLLAR NUT  ·  SS316 PIN",
            color=DIM, fontsize=6.5, ha="center", **FONT)

    # ── BR: ACM panel arrangement (flat vs tilted) ────────────────────────────
    ax = ax_acm
    ax.set_xlim(-100, 650); ax.set_ylim(-80, 350); ax.set_aspect("equal")

    # Flat panel
    panel_h = 200; panel_w = 250
    ax.add_patch(Rectangle((20, 50), panel_w, panel_h, fc=ANNO, ec=WHITE,
                           lw=1.5, zorder=3, alpha=0.7))
    ax.add_patch(Rectangle((20, 50), panel_w, panel_h/2, fc=DIM, ec=WHITE,
                           lw=1.0, zorder=4, alpha=0.5))
    # Hinge at centre
    ax.add_patch(Rectangle((20-5, 50+panel_h/2-6), panel_w+10, 12,
                           fc=RAIL, ec=WHITE, lw=1.0, zorder=5))
    ax.text(20+panel_w/2, 50+panel_h/2, "HINGE", color=BG,
            fontsize=6, ha="center", va="center", **FONT)
    ax.text(20+panel_w/2, 50+panel_h+20, "FLAT  (0°)", color=C_FLAT,
            fontsize=7.5, ha="center", **FONT)
    ax.text(20+panel_w/2, 50-20, "2× Dibond ACM  4mm\n1,500×3,000mm sheets",
            color=DIM, fontsize=6.5, ha="center", **FONT)
    dim_line_v(ax, 20-60, 50, 50+panel_h, f"{H} mm\n(schematic)", offset=-70, col=DIM)

    # Tilted panel (folded)
    t_ang = np.radians(30)
    tx0, ty0 = 420, 50
    # Lower half flat
    ax.add_patch(Rectangle((tx0, ty0), panel_w*0.7, panel_h/2,
                           fc=DIM, ec=WHITE, lw=1.5, alpha=0.5, zorder=3))
    # Upper half folded back
    fold_len = panel_h/2
    fold_dx = fold_len * np.sin(t_ang)
    fold_dy = fold_len * np.cos(t_ang)
    pts = np.array([[tx0, ty0+panel_h/2],
                    [tx0 + panel_w*0.7, ty0+panel_h/2],
                    [tx0 + panel_w*0.7 + fold_dx, ty0+panel_h/2+fold_dy],
                    [tx0 + fold_dx, ty0+panel_h/2+fold_dy]])
    ax.add_patch(Polygon(pts, fc=ANNO, ec=WHITE, lw=1.5, alpha=0.7, zorder=4))
    # Hinge
    ax.add_patch(Rectangle((tx0-5, ty0+panel_h/2-6), panel_w*0.7+10, 12,
                           fc=RAIL, ec=WHITE, lw=1.0, zorder=5))
    ax.text(tx0+panel_w*0.35 + fold_dx/2, ty0+panel_h/2+fold_dy/2+20,
            f"30° fold", color=C_T2, fontsize=6.5, ha="center", **FONT)
    ax.text(tx0 + panel_w*0.35, ty0+panel_h+fold_dy+25, "TILTED  (upper panel folds back)",
            color=C_T2, fontsize=7.5, ha="center", **FONT)

    ax.text(260, 310, "ACM BACKING PANEL ARRANGEMENT\nHINGED AT MIDPOINT — FOLDS TO ACCOMMODATE TILT",
            color=WHITE, fontsize=7.5, ha="center", va="bottom", **FONT)
    ax.text(260, -60, "PANEL: DIBOND 4mm  ·  HINGE: 2\" ALUMINIUM PIANO HINGE FULL WIDTH",
            color=DIM, fontsize=6.5, ha="center", **FONT)

    # Main title
    fig.text(0.5, 0.97, "SHEET 3 — FRAME & HARDWARE DETAILS",
             color=WHITE, fontsize=11, ha="center", fontweight="bold", **FONT)

    for a in axes:
        title_block(a, "3 / 4", "HARDWARE DETAILS")

    fig.savefig("film-plane-sheet3.png", dpi=130, bbox_inches="tight",
                facecolor=BG)
    plt.close(fig)
    print("  → film-plane-sheet3.png")


# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 4 — MOVEMENT SPECIFICATION TABLE
# ═══════════════════════════════════════════════════════════════════════════════
def sheet4():
    fig, ax = plt.subplots(figsize=(16, 10))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis("off")

    ax.text(0.5, 0.96, "SHEET 4 — MOVEMENT SPECIFICATION  &  TILT CONFIGURATION TABLE",
            transform=ax.transAxes, color=WHITE, fontsize=13, ha="center",
            fontweight="bold", **FONT)
    ax.text(0.5, 0.92, "GPC-001  ·  MOVEABLE FILM PLANE  ·  CONTAINER INTERIOR: 5,893 × 2,362 × 2,388 mm",
            transform=ax.transAxes, color=DIM, fontsize=8.5, ha="center", **FONT)

    # ── Table 1: Axis movement summary ───────────────────────────────────────
    def draw_table(ax, x0, y0, headers, rows, col_widths, row_h=0.048,
                   hdr_col=STRUCT2, row_cols=(GRID, BG)):
        total_w = sum(col_widths)
        # Header
        xc = x0
        ax.add_patch(Rectangle((x0, y0), total_w, row_h*1.2,
                               transform=ax.transAxes,
                               fc=hdr_col, ec=WHITE, lw=0.8, zorder=3,
                               clip_on=False))
        for h, cw in zip(headers, col_widths):
            ax.text(xc + cw/2, y0 + row_h*0.6, h,
                    transform=ax.transAxes, color=WHITE, fontsize=7.5,
                    ha="center", va="center", fontweight="bold", **FONT)
            xc += cw

        # Rows
        for ri, row in enumerate(rows):
            ry = y0 - (ri+1)*row_h
            fc = row_cols[ri % 2]
            ax.add_patch(Rectangle((x0, ry), total_w, row_h,
                                   transform=ax.transAxes,
                                   fc=fc, ec=GRID, lw=0.5, zorder=2,
                                   clip_on=False))
            xc = x0
            for cell, cw in zip(row, col_widths):
                col_text = WHITE if ri == 0 else ANNO
                ax.text(xc + cw/2, ry + row_h*0.5, str(cell),
                        transform=ax.transAxes, color=col_text, fontsize=7,
                        ha="center", va="center", **FONT)
                xc += cw

    ax.text(0.05, 0.88, "TABLE 1 — MOVEMENT AXES",
            transform=ax.transAxes, color=DIM, fontsize=8, fontweight="bold", **FONT)

    axes_headers = ["AXIS", "DESCRIPTION", "MAX TRAVEL", "RESOLUTION", "ACTUATOR", "LOCK"]
    axes_rows = [
        ["TILT (top)",    "Top edge along optical axis",   "0–2,262 mm", "~5 mm",  "3/4\"-6 leadscrew + handwheel", "Locking collar"],
        ["TILT (bottom)", "Bottom edge along optical axis","0–2,262 mm", "~5 mm",  "3/4\"-6 leadscrew + handwheel", "Locking collar"],
        ["MAX TILT",      "Top=100mm, Bot=2262mm (or rev.)","42°",        "0.12°/turn","same",                     "Both locks"],
        ["BACK FOCUS",    "Entire plane along optical axis","100–2,262mm","~5 mm",  "Both leadscrews together",     "Both locks"],
        ["RISE / FALL",   "Plane translates vertically",   "±200 mm",    "—",      "Manual slide + T-slot lock",   "T-nut"],
        ["SHIFT",         "Plane translates horizontally", "±300 mm",    "—",      "Manual slide + T-slot lock",   "T-nut"],
    ]
    draw_table(ax, 0.05, 0.78, axes_headers, axes_rows,
               [0.10, 0.22, 0.14, 0.10, 0.24, 0.15])

    ax.text(0.05, 0.57, "TABLE 2 — TILT CONFIGURATION SPECS",
            transform=ax.transAxes, color=DIM, fontsize=8, fontweight="bold", **FONT)

    def tilt_angle(d_top, d_bot):
        dz = d_top - d_bot
        dy = H - 120   # effective film height between carriage attachment points
        return np.degrees(np.arctan2(abs(dz), dy))

    def film_plane_length(d_top, d_bot):
        dz = abs(d_top - d_bot)
        dy = H - 120
        return round(np.sqrt(dz**2 + dy**2))

    def area_change(d_top, d_bot):
        fl = film_plane_length(d_top, d_bot)
        nominal = H - 120
        return f"+{round((fl/nominal - 1)*100)}%"

    config_headers = ["CONFIG", "NAME", "TOP EDGE\n(mm from PH)", "BOT EDGE\n(mm from PH)",
                      "TILT ANGLE", "FILM PLANE\nLENGTH (mm)", "AREA\nCHANGE",
                      "PRINCIPAL EFFECT"]
    config_rows = []
    config_names_full = [
        ("0", "Flat",            D_FAR,  D_FAR,  "No distortion — reference baseline"),
        ("1", "Mild tilt up",    1800,   D_FAR,  "Subtle keystone — top compressed"),
        ("2", "Strong tilt up",  800,    D_FAR,  "Strong keystone — top severely compressed"),
        ("3", "Max tilt up",     D_NEAR, D_FAR,  "Extreme — top hugely stretched laterally"),
        ("4", "Max tilt down",   D_FAR,  D_NEAR, "Extreme reverse — ground rushes forward"),
        ("5", "Both near",       D_NEAR, D_NEAR, "Entire plane close — uniform magnification boost"),
        ("6", "Compound",        D_NEAR, D_FAR,  "+ 20° swing = diagonal perspective break"),
    ]
    for cfg_id, name, d_top, d_bot, effect in config_names_full:
        ang = tilt_angle(d_top, d_bot)
        fl = film_plane_length(d_top, d_bot)
        ac = area_change(d_top, d_bot)
        config_rows.append([cfg_id, name, d_top, d_bot,
                            f"{ang:.1f}°", f"{fl:,}", ac, effect])

    draw_table(ax, 0.05, 0.48, config_headers, config_rows,
               [0.04, 0.12, 0.10, 0.10, 0.08, 0.11, 0.07, 0.33],
               hdr_col=STRUCT)

    ax.text(0.05, 0.27, "TABLE 3 — COMPONENT BILL OF MATERIALS",
            transform=ax.transAxes, color=DIM, fontsize=8, fontweight="bold", **FONT)

    bom_headers = ["ITEM", "DESCRIPTION", "SPEC", "QTY", "SOURCE A (SoCal/US)", "EST. UNIT $"]
    bom_rows = [
        ["1", "Linear guide rail",     "HGR20, 2,200mm",          "4",  "Automation Overstock, Gardena CA",  "$45"],
        ["2", "Rail carriage",         "HGH20CA flanged",          "8",  "Automation Overstock / Amazon",     "$18"],
        ["3", "Horiz. beam (T-slot)",  "80/20 10-4080, 8ft",      "4",  "8020.net / MiSUMi USA",             "$52"],
        ["4", "Acme leadscrew",        "3/4\"-6, 8ft length",     "2",  "Roton Products (LA area)",          "$95"],
        ["5", "Acme nut (bronze)",     "3/4\"-6",                 "4",  "Roton Products / McMaster-Carr",    "$12"],
        ["6", "Handwheel 8\"",         "3/4\" bore, cast alum.",  "4",  "Grainger (Anaheim/LA/SD)",          "$35"],
        ["7", "Pivot pin SS316",       "1\" dia × 8\" long",      "8",  "McMaster-Carr #98173A150",          "$8"],
        ["8", "Igus bearing block",    "drylin RJUM-01-25",       "8",  "igus.com (ships overnight)",        "$14"],
        ["9", "Alum. angle 2\"×2\"",   "3/16\" wall, 8ft",       "10", "Metal Supermarkets SoCal",          "$22"],
        ["10","Dibond ACM 4mm",        "4ft×8ft sheets",          "6",  "Grimco, City of Industry CA",       "$85"],
        ["11","EPDM foam tape",        "1\"×1/2\", 50ft roll",    "3",  "McMaster-Carr #8614K84",            "$28"],
        ["12","Duvetyne (light seal)", "60\" wide, 10yd",         "1",  "B&H Photo / Rosco direct",          "$95"],
        ["13","Piano hinge alum.",     "2\" wide, 72\" length",   "2",  "McMaster-Carr #1580A51",            "$28"],
        ["14","6-mil black poly",      "10ft×100ft roll",         "1",  "Home Depot (local SoCal)",          "$65"],
    ]
    draw_table(ax, 0.05, 0.18, bom_headers, bom_rows,
               [0.04, 0.18, 0.16, 0.04, 0.33, 0.08],
               hdr_col="#1A5C3A")

    # Total estimate
    costs = [45, 18, 52, 95, 12, 35, 8, 14, 22, 85, 28, 95, 28, 65]
    qtys  = [4,  8,  4,  2,  4,  4,  8,  8,  10, 6,  3,  1,  2,  1]
    total = sum(c*q for c,q in zip(costs, qtys))
    ax.text(0.95, 0.032, f"MATERIALS TOTAL (EST.):  ${total:,}",
            transform=ax.transAxes, color=C_T1, fontsize=8.5,
            ha="right", fontweight="bold", **FONT)
    ax.text(0.95, 0.018, "Excl. fabrication, fasteners, electrical actuation option",
            transform=ax.transAxes, color=DIM, fontsize=7, ha="right", **FONT)

    title_block(ax, "4 / 4", "MOVEMENT SPECS & BILL OF MATERIALS")
    fig.savefig("film-plane-sheet4.png", dpi=130, bbox_inches="tight",
                facecolor=BG)
    plt.close(fig)
    print("  → film-plane-sheet4.png")


# ── Run all sheets ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Generating film plane mechanism drawings...")
    sheet1()
    sheet2()
    sheet3()
    sheet4()
    print("Done.")
