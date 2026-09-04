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
Sheet 11: Pull-handle mount detail — stile → cap plug joint + handle arrangement (to scale)

All geometry reads from tbs_constants.py (single source of truth). Bearing /
seal / hardware specs trace to light-trap-selection.md §4.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
import os

from tbs_constants import C_OUT, C_CL, C_DIM, C_ALUM, C_STEEL, C_GASKT, C_LT_DRUM, DRUM_CX, DRUM_CY, DRUM_D, DRUM_H_LT, PANEL_FLOOR_GAP, LT_HOUSING_R, LT_HOUSING_T, LT_DRUM_OR, LT_DRUM_T, LT_OPENING_DEG, LT_CAP_TOP_T, LT_CAP_BOT_T, LT_CAP_OD, LT_LAP_H, LT_RIVET_D, LT_RIVET_HOLE, LT_RIVET_PITCH, LT_RIVET_N, LT_RIM_LEG, LT_RIM_T, LT_RIM_RIVET_PITCH, LT_SHELL_ARC, DRUM_CAGE_X0, DRUM_CAGE_X1, DRUM_CAGE_YD_L, DRUM_CAGE_YD_R, LT_FRAME_RHS, LT_FRAME_T, LT_FRAME_PLATE_T, LT_TOPRING_OD, LT_COLLAR_OD, LT_RING_BOLT_PCD, LT_FRAME_MOUNT_BOLT_TOP, LT_FRAME_MOUNT_BOLT_BOT, LT_AXLE_BEAM_H, LT_AXLE_BEAM_W, LT_AXLE_BEAM_T, LT_AXLE_BEAM_SPAN, LT_STUB_SHAFT_L, LT_BRG_STANDOFF, LT_CAGE_TOP, LT_CAGE_BOT, LT_HOUSING_Z_BOT, LT_HOUSING_Z_TOP, LT_BRG_PLATE_OD, LT_BRG_PLATE_T, LT_TBEAM_Z0, LT_BBEAM_Z1, LT_EDGE_CHAN_W, LT_EDGE_CHAN_LEG, LT_EDGE_CHAN_T, LT_EDGE_CHAN_N, LT_EDGE_CHAN_RIVET_PITCH, LT_EDGE_CHAN_END_BOLT, LT_HOUSING_ARC, LT_HOUSING_RIVET_N, LT_WIPER_N, LT_WIPER_TRIM, LT_WIPER_SPACING, LT_WIPER_BACKING, LT_WIPER_HOLDER_W, DIAGRAM_DPI, DIAGRAMS_DIR
from tbs_drawing import (
    draw_dim_h, draw_dim_v, draw_rect, draw_circle, draw_cl_v, draw_cl_h,
    leader, draw_notes,
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

# ── Off-the-shelf round pull handle — McMaster 1871A65 (light-trap-selection.md §4.4) ──
GRAB_D  = 12.7  # handle bar Ø (mm) — 0.50" round bar (1871A65)
GRAB_L  = 308   # overall handle length (mm) — 12.13" (feet at the ends)
GRAB_SO = 52    # grip standoff / arch height off the stile face (mm) — 2.06"
GRAB_Z  = 900   # mounting height above floor (mm)

# ── Derived running clearance (drum OD → housing bore), single-sourced ───────
RUN_GAP = LT_HOUSING_R - LT_HOUSING_T - LT_DRUM_OR   # radial gap, mm


def blind_rivet(ax, cx, cz, ang, grip, d=12):
    """Installed SS blind rivet in section — LOW-PROFILE head at +axis (McMaster
    97525A425 standard head: Ø ≈ 2× body, only ~0.32× body tall — NOT a tall dome),
    upset (set) blind head at −axis; `ang` = axis direction (deg), `grip` = joint stack."""
    RSC = "#C9CCD2"
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))

    def T(u, v):
        return (cx + u * ca - v * sa, cz + u * sa + v * ca)
    g = grip / 2
    ax.add_patch(mpatches.Polygon([T(-g, -d / 2), T(g, -d / 2), T(g, d / 2), T(-g, d / 2)],
                                  closed=True, fc=RSC, ec=C_OUT, lw=1.0, zorder=8))
    # Factory head — low, wide, shallow-domed (head Ø≈2d, height≈0.35d per datasheet)
    HW, HH = d * 1.0, d * 0.35
    head = [T(g, HW)]
    for kk in range(13):
        a = math.pi * (0.5 - kk / 12.0)
        head.append(T(g + HH * math.cos(a), HW * math.sin(a)))
    head.append(T(g, -HW))
    ax.add_patch(mpatches.Polygon(head, closed=True, fc=RSC, ec=C_OUT, lw=1.2, zorder=9))
    # snapped-off mandrel stub at the head center (open-end rivet — DP8010 seals the bore)
    ax.plot(*zip(T(g, 0), T(g + HH + d * 0.12, 0)), color=C_OUT, lw=0.7, zorder=10)
    bb, br = -g - d * 0.22, d * 0.55
    blind = [T(-g, d * 0.6)]
    for kk in range(13):
        a = math.pi * (0.5 - kk / 12.0)
        blind.append(T(bb - br * math.cos(a), d * 0.9 * math.sin(a)))
    blind.append(T(-g, -d * 0.6))
    ax.add_patch(mpatches.Polygon(blind, closed=True, fc=RSC, ec=C_OUT, lw=1.2, zorder=9))


def tube_rect(ax, x, y, w, h, wall, *, fc=C_STEEL, lw=1.4, zorder=6):
    """RHS/SHS tube shown in CUT cross-section — wall material filled, bore void (BG).
    x,y = outer corner; w,h = outer size; wall = wall thickness."""
    draw_rect(ax, x, y, w, h, fc=fc, lw=lw, zorder=zorder)                                  # outer (wall)
    draw_rect(ax, x + wall, y + wall, w - 2 * wall, h - 2 * wall, fc=BG, lw=lw * 0.7, zorder=zorder)  # bore (hollow)


def l_angle(ax, cx, cz, leg_x, leg_z, t, *, fc=C_ALUM, lw=1.4, zorder=5):
    """L-angle (equal/unequal) in section as ONE continuous polygon — a single extrusion, NOT two
    overlapping plates. (cx,cz) = the OUTER corner where the two outer faces meet; `leg_x`/`leg_z` =
    signed leg lengths (sign = direction the leg runs); `t` = leg wall thickness."""
    sx = 1 if leg_x >= 0 else -1
    sz = 1 if leg_z >= 0 else -1
    ax.add_patch(mpatches.Polygon([
        (cx, cz), (cx + leg_x, cz), (cx + leg_x, cz + sz * t),
        (cx + sx * t, cz + sz * t), (cx + sx * t, cz + leg_z), (cx, cz + leg_z)],
        closed=True, fc=fc, ec=C_OUT, lw=lw, zorder=zorder))


def hollow_beam_long(ax, x, z, w, h, wall, near, *, fc=C_STEEL, lw=1.4, zorder=4, breaks=True, open_ends=()):
    """RHS/SHS shown in LONGITUDINAL section (cut along its length) — the two walls the cut passes
    through read as solid bands, the bore between is void (BG). x,z = outer corner; w,h = drawn size;
    `wall` = wall thickness; `near` in {'bottom','top','left','right'} = which wall faces the viewer/joint.
    `open_ends` = a set of sides ('left','right','top','bottom') drawn WITHOUT an end cap — so the hollow
    reads as an open / cut tube end (not a closed box). `breaks` adds end break-marks on the capped ends."""
    horiz = near in ("bottom", "top")
    draw_rect(ax, x + wall, z + wall, w - 2 * wall, h - 2 * wall, fc=BG, lw=0, zorder=zorder)  # hollow bore (void)
    if horiz:                                                                                # near = top/bottom → horizontal wall bands
        draw_rect(ax, x, z, w, wall, fc=fc, lw=lw, zorder=zorder + 1)                         # bottom wall (full length)
        draw_rect(ax, x, z + h - wall, w, wall, fc=fc, lw=lw, zorder=zorder + 1)              # top wall
        if "left" not in open_ends:  draw_rect(ax, x, z, wall, h, fc=fc, lw=lw, zorder=zorder + 1)          # left end cap
        if "right" not in open_ends: draw_rect(ax, x + w - wall, z, wall, h, fc=fc, lw=lw, zorder=zorder + 1)  # right end cap
    else:                                                                                    # near = left/right → vertical wall bands
        draw_rect(ax, x, z, wall, h, fc=fc, lw=lw, zorder=zorder + 1)                         # left wall
        draw_rect(ax, x + w - wall, z, wall, h, fc=fc, lw=lw, zorder=zorder + 1)              # right wall
        if "bottom" not in open_ends: draw_rect(ax, x, z, w, wall, fc=fc, lw=lw, zorder=zorder + 1)          # bottom end cap
        if "top" not in open_ends:    draw_rect(ax, x, z + h - wall, w, wall, fc=fc, lw=lw, zorder=zorder + 1)  # top end cap
    if breaks:                                                                              # capped ends that continue past the crop
        if horiz:
            for bx in (x, x + w):
                if ("left" if bx == x else "right") in open_ends:
                    continue
                ax.plot([bx - 4, bx + 4, bx - 4], [z + wall, z + h / 2, z + h - wall],
                        color=C_OUT, lw=0.8, zorder=zorder + 3, solid_capstyle="round")
        else:
            for bz in (z, z + h):
                if ("bottom" if bz == z else "top") in open_ends:
                    continue
                ax.plot([x + wall, x + w / 2, x + w - wall], [bz - 4, bz + 4, bz - 4],
                        color=C_OUT, lw=0.8, zorder=zorder + 3, solid_capstyle="round")


def draw_bolt(ax, cx, cz, length, *, d=10, vertical=True, head=-1, end="nut", csk=False, wall=None, zb=10):
    """Bolt in section — the project convention (cf. corner-gimbal bolt()): a filled shank
    with a wider HEAD at the `head` end and, at the far end, a hex NUT / rivet-nut / tapped
    thread. cx,cz = shank mid; `length` = grip along the axis; d = nominal Ø (drawn).
    head = -1 → head at the −axis end (below/left); +1 → +axis end.
    csk = True → flush COUNTERSUNK head (tapered flat head recessed into the joined face),
    e.g. an Al cap into a steel flange; else a protruding hex head.
    end: 'nut' plain hex nut · 'rivnut' rivet-nut / blind threaded insert (flanged sleeve set in the
    wall from outside) · 'tapped' into a tapped hole (no nut)."""
    SHK, HN = "#8A8F98", C_STEEL
    hh, hw = d * 0.6, d * 1.9                              # head/nut along-axis / across
    g = length / 2

    def rect(u0, u1, v0, v1, **kw):                       # (along-axis u, across v) → x/z
        if vertical:
            ax.add_patch(mpatches.Rectangle((cx + v0, cz + u0), v1 - v0, u1 - u0, **kw))
        else:
            ax.add_patch(mpatches.Rectangle((cx + u0, cz + v0), u1 - u0, v1 - v0, **kw))

    def pmap(u, v):                                        # (along-axis u, across v) → point
        return (cx + v, cz + u) if vertical else (cx + u, cz + v)
    hu = -g if head < 0 else g                                                             # head end (outer face)
    fu = g if head < 0 else -g                                                             # far (thread) end
    if csk:                                               # flush countersunk bolt — ONE continuous shape + color
        into = 1 if head < 0 else -1                      # +axis into the joint for a head-below bolt
        cw = hw * 0.85
        tu = hu + into * hh * 1.4                          # where the flared head meets the shank
        pts = [pmap(hu, -cw / 2), pmap(hu, cw / 2), pmap(tu, d / 2),   # flared flat head → taper …
               pmap(fu, d / 2), pmap(fu, -d / 2), pmap(tu, -d / 2)]    # … → shank to the far end
        ax.add_patch(mpatches.Polygon(pts, closed=True, fc=SHK, ec=C_OUT, lw=0.9, zorder=zb))
    else:
        rect(-g, g, -d / 2, d / 2, fc=SHK, ec=C_OUT, lw=0.8, zorder=zb)                    # shank
        rect(hu - (hh if head < 0 else 0), hu + (0 if head < 0 else hh), -hw / 2, hw / 2,
             fc=HN, ec=C_OUT, lw=0.9, zorder=zb + 1)                                       # protruding hex head
    if end == "nut":
        rect(fu - (0 if head < 0 else hh), fu + (hh if head < 0 else 0), -hw / 2, hw / 2,
             fc=HN, ec=C_OUT, lw=0.9, zorder=zb + 1)                                       # hex nut
    elif end == "rivnut":                              # rivet-nut / blind threaded insert. The BARREL is
        # aligned with (spans) the wall thickness `wall`; a low PANCAKE head (same profile as the blind-rivet
        # factory head) seats on the INNER (bore-side) edge; the bolt threads up into it. Distinct BRONZE so
        # it reads apart from the silver blind rivets. `wall` = the drawn metal thickness the barrel occupies.
        RN = "#A8763A"
        into = 1 if head < 0 else -1                   # +axis = through the wall, away from the bolt head
        wt = wall if wall is not None else hh          # wall thickness the barrel spans
        hp = fu + into * wt                            # inner (bore-side) edge = the dotted metal-thickness line
        rect(fu, hp, -hw * 0.44, hw * 0.44, fc=RN, ec=C_OUT, lw=0.8, zorder=zb + 1)   # barrel — aligned with the wall thickness
        rect(fu, hp, -d * 0.48, d * 0.48, fc=SHK, ec="none", zorder=zb + 2)           # bolt threaded up inside the barrel
        HWr, HHr = d * 0.95, d * 0.42                                                 # low pancake head on the inner edge (bore side)
        dome = [pmap(hp, HWr)]
        for kk in range(13):
            a = math.pi * (0.5 - kk / 12.0)
            dome.append(pmap(hp + into * HHr * math.cos(a), HWr * math.sin(a)))
        dome.append(pmap(hp, -HWr))
        ax.add_patch(mpatches.Polygon(dome, closed=True, fc=RN, ec=C_OUT, lw=0.9, zorder=zb + 3))


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 1 — General Arrangement
# Vertical section on the drum axis (view looks along +Yd):
#   horizontal axis = X depth (exterior → interior), vertical axis = Z height.
# ═════════════════════════════════════════════════════════════════════════════
def draw_sheet1():
    # ── Key positions in mm (all from constants) ─────────────────────────────
    X_AX = DRUM_CX                       # drum axis X (= -420)
    HO_L = X_AX - LT_HOUSING_R           # housing outer, exterior side
    HO_R = X_AX + LT_HOUSING_R           # housing outer, interior side
    HI_L = HO_L + LT_HOUSING_T           # housing inner (bore) faces
    HI_R = HO_R - LT_HOUSING_T
    DO_L = X_AX - LT_DRUM_OR             # drum shell outer faces
    DO_R = X_AX + LT_DRUM_OR
    DI_L = DO_L + LT_DRUM_T              # drum shell inner faces
    DI_R = DO_R - LT_DRUM_T

    # Z scheme reconciled with Sheet 8: the drum HANGS from a bearing ABOVE its
    # top cap (below the top axle beam); the fixed housing spans beam-to-beam; the
    # lower bearing floats above the bottom beam.
    Z_DBOT, Z_DTOP = PANEL_FLOOR_GAP, DRUM_H_LT   # drum caps: 130 (bottom) · 2100 (top)
    Z_BOT, Z_TOP = Z_DBOT, Z_DTOP                 # aliases used by the dimensions below
    Z_HBOT, Z_HTOP = LT_HOUSING_Z_BOT, LT_HOUSING_Z_TOP   # fixed housing skin: 93 → 2167
    Z_TBM0, Z_TBM1 = LT_TBEAM_Z0, LT_CAGE_TOP     # top axle beam: 2167 → 2217
    Z_BBM0, Z_BBM1 = LT_CAGE_BOT, LT_BBEAM_Z1     # bottom axle beam (50×40 RHS)
    Z_CAP_B = Z_DBOT + LT_CAP_BOT_T               # bottom cap inner face (138)
    Z_CAP_T = Z_DTOP - LT_CAP_TOP_T               # top cap inner face (2092)
    z_ubrg = Z_DTOP + LT_BRG_STANDOFF             # upper bearing bottom — above the top cap (2130)
    z_lbrg = Z_DBOT - SKF6215_W                   # lower bearing bottom — below the bottom cap (105)

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
    ax.text(X_LO + 30, -430, "FLOOR LEVEL", ha="left", va="center",
            fontsize=7.5, color=C_DIM, **FONT, zorder=15)

    # ── Fixed housing walls (Ø800, 5mm UV-HDPE) — spans beam-to-beam ─────────
    for x0 in (HO_L, HI_R):
        draw_rect(ax, x0, Z_HBOT, LT_HOUSING_T, Z_HTOP - Z_HBOT,
                  fc="#DDE4EC", lw=1.4, zorder=5)
    leader(ax, HO_L + LT_HOUSING_T / 2, 1780,
           HO_L - 350, 1780,
           f"FIXED HOUSING\nØ{DRUM_D} · {LT_HOUSING_T}mm UV-HDPE",
           fs=7, color=C_OUT, ha="center", arrow_style="->", font=FONT)

    # ── Rotating drum shell (Ø864, 1/8in HDPE) ───────────────────────────────
    for x0 in (DO_L, DI_R):
        draw_rect(ax, x0, Z_CAP_B, LT_DRUM_T, Z_CAP_T - Z_CAP_B,
                  fc=C_LT_DRUM, lw=1.4, zorder=6)
    leader(ax, DO_L + LT_DRUM_T / 2, 1330,
           HO_L - 325, 1330,
           f"ROTATING DRUM\nØ{2 * LT_DRUM_OR} · {LT_DRUM_T:.2f}mm (1/8in) HDPE\nsingle {LT_OPENING_DEG}° opening",
           fs=7, color=C_OUT, ha="center", arrow_style="->", font=FONT)

    # ── End caps — metal hub discs (both 8mm 6061-T6 Al, identical) ──────────
    cap_x0 = X_AX - LT_CAP_OD / 2
    draw_rect(ax, cap_x0, Z_DTOP - LT_CAP_TOP_T, LT_CAP_OD, LT_CAP_TOP_T, fc=C_ALUM, lw=1.2, zorder=7)  # top cap 2092..2100
    draw_rect(ax, cap_x0, Z_DBOT, LT_CAP_OD, LT_CAP_BOT_T, fc=C_ALUM, lw=1.2, zorder=7)                 # bottom cap 130..138

    # ── Rotation axis ─────────────────────────────────────────────────────────
    draw_cl_v(ax, X_AX, Z_LO + 120, Z_HI - 120)          # drum rotation axis

    # ── Axle beams (top + bottom) + Ø240 mount plates + bearing ring/collar ──
    #    (the drum HANGS from the upper bearing seated below the top beam — Sheet 8)
    # This section looks ALONG the beam axis (Yd), so each 50×50 RHS beam reads END-ON: a small
    # hollow square on the far-wider Ø240 mount plate (Sheet 8 shows the full 962mm Yd span).
    _BW, _BT = LT_AXLE_BEAM_W, LT_AXLE_BEAM_T
    for zb0, zb1 in ((Z_TBM0, Z_TBM1), (Z_BBM0, Z_BBM1)):
        draw_rect(ax, X_AX - _BW / 2, zb0, _BW, zb1 - zb0, fc=C_STEEL, lw=1.2, zorder=4)                       # RHS outer (cut end-on)
        draw_rect(ax, X_AX - _BW / 2 + _BT, zb0 + _BT, _BW - 2 * _BT, (zb1 - zb0) - 2 * _BT, fc=BG, lw=0.8, zorder=4)  # hollow bore
    draw_rect(ax, X_AX - LT_BRG_PLATE_OD / 2, z_ubrg + SKF6215_W, LT_BRG_PLATE_OD, LT_BRG_PLATE_T, fc=C_STEEL, lw=1.0, zorder=5)  # top mount plate 2155..2167
    draw_rect(ax, X_AX - LT_BRG_PLATE_OD / 2, LT_BBEAM_Z1, LT_BRG_PLATE_OD, LT_BRG_PLATE_T, fc=C_STEEL, lw=1.0, zorder=5)          # bottom mount plate 93..105
    draw_rect(ax, X_AX - LT_TOPRING_OD / 2, z_ubrg, LT_TOPRING_OD, SKF6215_W, fc=C_ALUM, lw=1.0, zorder=6)   # upper Al ring 2130..2155
    draw_rect(ax, X_AX - LT_COLLAR_OD / 2, z_lbrg, LT_COLLAR_OD, SKF6215_W, fc=C_STEEL, lw=1.0, zorder=6)     # lower steel collar 105..130

    # ── SKF 6215 bearings (upper ABOVE the cap · lower BELOW the cap) ──────────
    for z_brg in (z_ubrg, z_lbrg):
        draw_rect(ax, X_AX - SKF6215_OD / 2, z_brg, SKF6215_OD, SKF6215_W, fc="#9BA0A8", lw=1.0, zorder=7)
        draw_rect(ax, X_AX - SKF6215_ID / 2, z_brg, SKF6215_ID, SKF6215_W, fc="white", lw=0.8, zorder=8)
    # Ø160 steel stub-shaft FLANGE on each cap (bolted 4×M10) → the Ø75 shaft rises FROM the flange
    # through the bearing (matches the Sheet 5/6 hub — cap → flange → shaft, NOT cap → shaft).
    _FL = 15
    draw_rect(ax, X_AX - 80, Z_DTOP, 160, _FL, fc=C_STEEL, lw=1.1, zorder=9)                    # top flange 2100..2115
    draw_rect(ax, X_AX - 80, Z_DBOT - _FL, 160, _FL, fc=C_STEEL, lw=1.1, zorder=9)              # bottom flange 115..130
    draw_rect(ax, X_AX - SKF6215_ID / 2, Z_DTOP + _FL, SKF6215_ID,
              (z_ubrg + SKF6215_W) - (Z_DTOP + _FL), fc=C_STEEL, lw=1.0, zorder=10)             # upper Ø75 shaft (flange → bearing top)
    draw_rect(ax, X_AX - SKF6215_ID / 2, z_lbrg, SKF6215_ID,
              (Z_DBOT - _FL) - z_lbrg, fc=C_STEEL, lw=1.0, zorder=10)                            # lower Ø75 shaft (bearing → flange)
    leader(ax, X_AX - SKF6215_OD / 2, z_ubrg + SKF6215_W / 2,
           HO_L - 350, Z_DTOP + 150,
           f"UPPER: {LT_CAP_TOP_T:.0f}mm Al cap → Ø160 steel flange →\nØ{SKF6215_ID} stub shaft →"
           f"SKF 6215-2RS1 (Ø{SKF6215_ID} bore)\nHANGS below the top beam · isolated\nAl ring, 6×M10",
           fs=6, color=C_OUT, ha="center", arrow_style="->", font=FONT)
    leader(ax, X_AX - SKF6215_OD / 2, z_lbrg + SKF6215_W / 2,
           X_LO + 475, -135,
           f"LOWER: {LT_CAP_BOT_T:.0f}mm Al cap → Ø160 steel flange → Ø{SKF6215_ID} stub shaft →\n"
           f"SKF 6215-2RS1 FLOATS above the bottom beam · steel collar, 8×M10",
           fs=6, color=C_OUT, ha="center", arrow_style="->", font=FONT)
    leader(ax, X_AX, z_ubrg + SKF6215_W + LT_BRG_PLATE_T / 2 + 30,
           HO_L - 275, Z_TBM1 + 135,
           "TOP AXLE BEAM 50×50 (end-on) on the Ø240 mount plate\n(beam spans Yd — full span on Sheet 8)",
           fs=6, color=C_DIM, ha="center", arrow_style="->", font=FONT)

    # ── Grab rail on a STEEL STILE spanning the two caps — the pull load goes into the
    # structural Al caps, NOT the thin HDPE drum wall. (interior side of the bore) ───
    STILE_W = 40
    stile_x = DI_R - STILE_W                                     # stile just off the interior wall
    draw_rect(ax, stile_x, Z_CAP_B, STILE_W, Z_CAP_T - Z_CAP_B, fc=C_STEEL, lw=1.2, zorder=6)   # handle stile (cap→cap)
    for zc, hd_ in ((Z_CAP_T, -1), (Z_CAP_B, 1)):                                               # stile-end tapped plug + CSK cap bolt
        draw_rect(ax, stile_x + 8, min(zc, zc + hd_ * 70), STILE_W - 16, 70, fc="#9AA0A8", lw=0.8, zorder=7)  # solid tapped plug in tube end
        draw_bolt(ax, stile_x + STILE_W / 2, zc + hd_ * 18, 44, d=11, head=int(-hd_), end="tapped", csk=True, zb=8)  # CSK bolt through cap → plug
    leader(ax, stile_x + STILE_W / 2, Z_CAP_T + 4, stile_x + 640, Z_CAP_T + 160,
           "STILE → CAP: M10 countersunk bolt through\neach cap into a tapped plug in the RHS end (+ grub\nscrews, 1 top + 1 bottom) — see Sheet 11", fs=6.0, color=C_DIM,
           ha="right", arrow_style="->", font=FONT)
    GX = stile_x - GRAB_SO                                       # grip standoff, inboard of the stile
    GZ0, GZ1 = GRAB_Z - GRAB_L / 2, GRAB_Z + GRAB_L / 2
    hd = GRAB_D
    hbar = "#C9CCD2"
    # rounded round-bar pull handle (1871A65): grip parallel to the stile + two arms to the feet, drawn
    # as a capsule silhouette so the corners read ROUNDED, like a bent pipe (not a squared bracket).
    def capsule(x0, z0, x1, z1):
        ang = math.atan2(z1 - z0, x1 - x0)
        nx, nz = -math.sin(ang) * hd / 2, math.cos(ang) * hd / 2
        ax.add_patch(mpatches.Polygon([(x0 + nx, z0 + nz), (x1 + nx, z1 + nz),
                                       (x1 - nx, z1 - nz), (x0 - nx, z0 - nz)], closed=True, fc=hbar, ec="none", zorder=9))
        for cx0, cz0 in ((x0, z0), (x1, z1)):
            ax.add_patch(mpatches.Circle((cx0, cz0), hd / 2, fc=hbar, ec="none", zorder=9))
    capsule(GX, GZ0 + hd, GX, GZ1 - hd)                          # grip (vertical)
    capsule(GX, GZ0 + hd, stile_x - 4, GZ0)                      # bottom arm (rounded corner)
    capsule(GX, GZ1 - hd, stile_x - 4, GZ1)                      # top arm (rounded corner)
    for gz in (GZ0, GZ1):                                        # two flat feet, BOLTED to the stile (no welds)
        draw_rect(ax, stile_x - 6, gz - 16, 6, 32, fc=C_STEEL, lw=1.0, zorder=8)                 # flat foot pad (0.27")
        draw_bolt(ax, stile_x - 3, gz, 26, d=6.35, vertical=False, head=-1, end="rivnut", wall=5, csk=True)   # foot → stile: 1/4" CSK (flush) into rivet-nut
    leader(ax, GX - hd / 2, GRAB_Z + GRAB_L * 0.1, 780, GRAB_Z - 320,
           f"PULL HANDLE — off-the-shelf 12\" round pull handle (McMaster 1871A65,\nØ0.5\" bar),1/4\" through-holes BOLTED (tapped) at both feet to a \nsteel STILE ({STILE_W}×{STILE_W}×5 SS RHS) that spans + bolts to the two Al \ncaps — pull load into the caps · see MOUNT DETAIL",
           fs=6.5, color=C_OUT, ha="center", arrow_style="->", font=FONT)
    draw_dim_v(ax, GX - hd / 2 - 55, GZ0, GZ1, f"{GRAB_L}mm handle", offset=45, fs=6.5, font=FONT)
    draw_dim_h(ax, GX, stile_x, GZ1 + 75, f"{GRAB_SO}mm standoff", offset=45, fs=6.5, font=FONT)
    draw_dim_v(ax, GX - hd / 2 - 150, Z_CAP_B, GRAB_Z, f"{GRAB_Z - Z_CAP_B:.0f}mm\n(cap inner edge → grip CL)",
               offset=45, fs=6.5, font=FONT)

    # (The pull-handle mount detail — handle → stile → cap plug joint — is drawn to scale on its
    #  own Sheet 11; the GA above shows only the assembled arrangement + a reference.)
    ax.text(HO_R + 500, 950, "PULL-HANDLE MOUNT — see SHEET 11\n(handle → stile → cap · plug joint, to scale)",
            ha="center", va="center", fontsize=7.5, color=TITLE_COL, fontweight="bold", **FONT, zorder=15)

    # ── Dimensions ───────────────────────────────────────────────────────────
    draw_dim_h(ax, HO_L, HO_R, Z_TOP + 300, f"Ø{DRUM_D} HOUSING OD",
               offset=90, fs=7, font=FONT)
    draw_dim_v(ax, HO_L - 600, Z_BOT, Z_TOP,
               f"{DRUM_H_LT - PANEL_FLOOR_GAP}mm CLEAR", offset=95, fs=7, font=FONT)
    draw_dim_v(ax, X_HI - 160, 0, Z_TOP, f"{DRUM_H_LT}mm TOP AFF",
               offset=95, fs=7, right=True, font=FONT)
    leader(ax, HI_R - 2, 1300,
           HO_R + 250, 1180,
           f"≈{RUN_GAP}mm radial running gap\n(drum OD → housing bore; sealed — Sheet 7)",
           fs=6.5, color=C_DIM, ha="left", arrow_style="->", font=FONT)

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

    title_block(ax, "SHEET 1 OF 12", drawing_title="REVOLVING LIGHT-TRAP",
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
    HOUSING_H = LT_HOUSING_Z_TOP - LT_HOUSING_Z_BOT   # blank height = 2062 (housing spans beam-to-beam)
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
    draw_notes(ax, notes, 40, -240, 34, fs=7, font=FONT, width=1650,
               title_color=TITLE_COL)

    title_block(ax, "SHEET 2 OF 12", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="HOUSING CYLINDER — CUT SHEET (FLAT PATTERN)",
                scale_note="FLAT PATTERN · ALL DIMS IN mm",
                doc_id="TBS-001 · Revolving Light-Trap", height=0.045, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet2.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet2.png saved")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 3 — Rotating drum shell cut sheet (flat pattern; caps → Sheet 6)
# The 1/8in HDPE C-shell developed flat (single 80° opening → 280° of material),
# plus the two 8mm 6061-T6 Al top/bottom caps with bolted steel stub-shaft hubs.
# ═════════════════════════════════════════════════════════════════════════════
def draw_sheet3():
    DRUM_OD   = 2 * LT_DRUM_OR                          # Ø864
    L_FULL    = math.pi * DRUM_OD                       # full circumference
    W_SHELL   = (360 - LT_OPENING_DEG) / 360.0 * L_FULL # 280° of material
    OW        = (LT_OPENING_DEG / 360.0) * L_FULL       # removed opening arc
    SHELL_H   = DRUM_H_LT - PANEL_FLOOR_GAP - 80        # drum body height (= 2040)
    RUN_GAP_L = LT_HOUSING_R - LT_HOUSING_T - LT_DRUM_OR

    # ── Data window → figure size (shell flat pattern only; caps → Sheet 6) ──
    PAD_L, PAD_R, PAD_B, PAD_T = 380, 430, 1520, 430
    X_LO, X_HI = -PAD_L, W_SHELL + PAD_R
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

    # ── Fabrication notes ────────────────────────────────────────────────────
    notes = [
        "ROTATING DRUM SHELL — CUT SHEET (flat pattern)",
        f"Shell: {LT_DRUM_T:.2f}mm (1/8in) HDPE, blank {W_SHELL:.0f} × {SHELL_H}mm — this developed blank is the shop's cutting/rolling template.",
        f"1. Cut the blank, roll to R{LT_DRUM_OR}; the two free edges are the {LT_OPENING_DEG}° opening jambs.",
        f"2. Shell laps {LT_LAP_H}mm over each cap rim → {LT_RIVET_N}× Ø{LT_RIVET_D} SS blind rivets/cap + DP8010 bead (see Sheet 4).",
        "The end caps (Ø855 6061-T6 Al, hub bore + 4×M10 flange + rim-rivet holes) are drawn on Sheet 6 with the other machined metal parts.",
        f"Running clearance to housing bore ≈ {RUN_GAP_L}mm (radial) — see Sheet 7.",
        "FLAT PATTERN · TRUE DEVELOPED SCALE · ALL DIMS IN mm",
    ]
    draw_notes(ax, notes, 40, -560, 92, fs=7, font=FONT, width=1850,
               title_color=TITLE_COL)

    title_block(ax, "SHEET 3 OF 12", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="ROTATING DRUM SHELL — CUT SHEET (FLAT PATTERN)",
                scale_note="FLAT PATTERN · TRUE DEVELOPED SCALE · ALL DIMS IN mm",
                doc_id="TBS-001 · Revolving Light-Trap", height=0.045, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet3.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet3.png saved")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 4 — Shell → cap lap-and-fasten joint
# The HDPE shell edge laps over a rolled rim-angle lip on each metal cap and is
# radially riveted (SS blind) + DP8010-bonded. Enlarged section + rivet pattern.
# ═════════════════════════════════════════════════════════════════════════════
def draw_sheet4():                           # Sheet 4 — drum secure (shell→cap joint)
    # ── Data window ──────────────────────────────────────────────────────────
    X_LO, X_HI, Z_LO, Z_HI = -470, 1540, -650, 540
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
    l_angle(ax, 0, 0, -RIML, LIP, LEGT, fc=C_ALUM, lw=1.4, zorder=5)           # rim-angle (L) — flat leg on cap + lip up
    draw_rect(ax, 0, -DPT, DPT, LIP + DPT, fc=C_GASKT, lw=0.8, zorder=5)       # DP8010 bead
    draw_rect(ax, DPT, -125, SHT, LIP + 175, fc=C_LT_DRUM, lw=1.6, zorder=6)   # shell laps the lip + hangs down (drum body)
    rz = LIP * 0.5
    blind_rivet(ax, (DPT + SHT - LEGT) / 2, rz, 0, S * (LT_DRUM_T + 1 + LT_RIM_T), d=RVD)  # shell → lip rivet (radial)
    blind_rivet(ax, -RIML / 2, (LEGT - CAPT) / 2, 90, CAPT + LEGT, d=RVD * 0.8)             # one leg → cap rivet (vertical)
    # ── Running-gap brush wiper on the drum OD — a #4 (3/16") strip brush snapped into a Tanis
    # anodized-aluminum STRAIGHT-FLANGE holder. This is a LONGITUDINAL cut along the brush, so the
    # holder flange + its blind rivets run PARALLEL to the brush, circumferentially offset (behind
    # the cut plane) — the true mount + the rivet-clear-of-brush is the HOLDER PROFILE inset below.
    # The run starts BELOW the cap lap so its flange rivets stagger clear of the shell→cap rivets.
    odx  = DPT + SHT                              # drum OD (shell outer face)
    HW   = S * LT_WIPER_HOLDER_W                   # holder flange wall (0.050")
    CHAN = S * LT_WIPER_BACKING                    # #4 channel backing (3/16")
    br_bot, br_top = -128, -18                     # brush run on the shell body (below the lap)
    draw_rect(ax, odx, br_bot, HW, br_top - br_bot, fc=C_ALUM, lw=1.0, zorder=7)             # Al holder (on the OD)
    ax.plot([odx, odx], [br_bot, br_top], color=C_GASKT, lw=2.6, zorder=8)                   # DP8010 bond: holder flange → HDPE shell
    draw_rect(ax, odx + HW, br_bot, CHAN, br_top - br_bot, fc="#8A8F98", lw=1.0, zorder=8)   # #4 channel backing
    for zz in range(int(br_bot) + 8, int(br_top), 8):                                        # bristles lay over into the gap
        ax.plot([odx + HW + CHAN, odx + HW + CHAN + S * 15], [zz, zz + 11], color="#333", lw=0.5, zorder=8)
    for zc in (-90,):                                                                        # holder → shell blind rivet — SINGLE (a 2nd upper rivet would foul the rim-angle L)
        blind_rivet(ax, odx - S * 1.5, zc, 0, S * (LT_DRUM_T + LT_WIPER_HOLDER_W), d=S * LT_RIVET_D)
    for zz in (-134, -126):                                                                  # break (shell + brush continue down)
        ax.plot([DPT - 3, odx + HW + CHAN + 3], [zz - 3, zz + 3], color=C_OUT, lw=0.6, zorder=9)
    leader(ax, odx + HW + CHAN + S * 6, br_top - 22, 250, -CAPT - 150,
           f"RUNNING-GAP BRUSH — #4 strip brush in an Al flange holder ({LT_WIPER_N} strips,\nSheet 7): the holder is DP8010-BONDED to the HDPE shell (brown, PRIMARY) + a SINGLE\nbackup blind rivet (washer inside) — a 2nd/upper rivet would foul the rim-angle L; see\nHOLDER PROFILE inset →; runs clear BELOW the cap lap",
           fs=6.0, color=C_OUT, ha="left", arrow_style="->", font=FONT)

    # ── Section dimensions + callouts (all to the 7:1 geometry) ──────────────
    draw_dim_v(ax, DPT + SHT + 40, 0, LIP, f"{LT_LAP_H}mm LAP", offset=42, fs=6.5, right=True, font=FONT)
    draw_dim_h(ax, DPT, DPT + SHT, -55, f"{LT_DRUM_T:.2f}mm SHELL", offset=40, fs=6.2,
               above=False, font=FONT)
    draw_dim_v(ax, -360, -CAPT, 0, f"{LT_CAP_TOP_T:.0f}mm CAP", offset=44, fs=6.2, font=FONT)
    # rivet positions (dim_v: shell-rivet CL height on the lap; dim_h: leg-rivet in from the lip)
    draw_dim_v(ax, DPT + SHT + 130, 0, rz, f"{LT_LAP_H / 2:.0f}mm shell-rivet CL", offset=40, fs=6.0, right=True, font=FONT)
    draw_dim_h(ax, -RIML / 2, 0, -CAPT - 22, f"{LT_RIM_LEG / 2:.0f}mm leg-rivet from lip", offset=34, fs=6.0, above=False, font=FONT)
    draw_dim_v(ax, -RIML / 2 - 30, -CAPT, LEGT, f"{LT_CAP_TOP_T + LT_RIM_T:.0f}mm leg-rivet grip\n(flat leg → cap)", offset=40, fs=6.0, font=FONT)
    leader(ax, (DPT + SHT - LEGT) / 2, rz, 200, rz + 70,
           f"SS Ø{LT_RIVET_D} BLIND RIVET (radial, low-profile head)\nthrough shell + lip · ~{LT_RIVET_PITCH}mm circumferential pitch",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, -LEGT, LIP - 20, -200, LIP + 55,
           f"RIM ANGLE {LT_RIM_LEG}×{LT_RIM_LEG}×{LT_RIM_T}, rolled to R{LT_CAP_OD // 2}\n6061-T6 Al — riveted to both caps",
           fs=6.5, color=C_OUT, ha="right", arrow_style="->", font=FONT)
    leader(ax, DPT + SHT, LIP + 30, 250, LIP + 30,
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

    # ── HOLDER PROFILE inset — TRUE cross-section ⊥ to the brush length (scale 7:1) ─
    # Dedicated right column. Radial = UP, circumferential = across. Shows the flange riveted to
    # the shell CLEAR of the brush, the #4 channel in the track, bristles laying over the fixed bore.
    IS = 7                                                   # inset scale (real mm × 7)
    ox, oz = 1300, 150                                       # drum OD baseline (circumferential center)
    def ix(mm): return ox + IS * mm
    def iz(mm): return oz + IS * mm
    HWmm, CHmm, GAPmm, HTmm = LT_WIPER_HOLDER_W, LT_WIPER_BACKING, RUN_GAP, LT_HOUSING_T
    ax.text(ox, iz(GAPmm + HTmm) + 44, "HOLDER PROFILE — section ⊥ brush  (7:1)",
            ha="center", va="bottom", fontsize=8, color=TITLE_COL, fontweight="bold", **FONT, zorder=15)
    draw_rect(ax, ix(-32), iz(-LT_DRUM_T), IS * 64, IS * LT_DRUM_T, fc=C_LT_DRUM, lw=1.2, zorder=5)   # rotating drum shell
    draw_rect(ax, ix(-32), iz(GAPmm), IS * 64, IS * HTmm, fc="#DDE4EC", lw=1.2, zorder=5)             # fixed housing wall (bore face)
    # Al straight-flange holder — ONE continuous extrusion (single piece): a flat mounting flange
    # (left, riveted to the shell) integral with the U-track (right) that grips the #4 brush channel.
    w, cav, wH, fL = HWmm, CHmm, CHmm, -28              # wall · channel cavity · wall-height · flange-left (mm)
    ax.add_patch(mpatches.Polygon([
        (ix(fL), iz(0)), (ix(2 * w + cav), iz(0)),                      # flange + track base (bottom, on the OD)
        (ix(2 * w + cav), iz(w + wH)), (ix(w + cav), iz(w + wH)),       # right (outer) track wall
        (ix(w + cav), iz(w)), (ix(w), iz(w)),                           # cavity floor (U bottom)
        (ix(w), iz(w + wH)), (ix(0), iz(w + wH)),                       # left (inner) track wall
        (ix(0), iz(w)), (ix(fL), iz(w))],                              # flange top
        closed=True, fc=C_ALUM, ec=C_OUT, lw=1.0, zorder=6))            # flanged-U holder (one piece)
    draw_rect(ax, ix(w), iz(w), IS * cav, IS * wH, fc="#8A8F98", lw=0.9, zorder=7)   # #4 channel seated in the U-track
    # bristles project radially up from the channel (seated on the U-track base), lay over the bore
    for k in range(9):
        bx = ix(w + 0.4 + k * (cav - 0.8) / 8)
        ax.plot([bx, bx], [iz(w + wH), iz(GAPmm)], color="#222", lw=0.6, zorder=7)
        ax.plot([bx, bx + IS * 6], [iz(GAPmm), iz(GAPmm)], color="#222", lw=0.6, zorder=7)            # lay-over on the bore
    # flange → shell securing: the flange is BONDED to the soft HDPE shell with DP8010 (spreads the load
    # over the whole flange so nothing point-loads / pulls through the 3mm plastic) — this is the PRIMARY
    # attachment; the blind rivet clamps during cure + is the mechanical backup, with a backup washer on
    # the blind (inside) face so its bulb can't pull through the HDPE.
    ax.plot([ix(fL), ix(2 * w + cav)], [iz(0), iz(0)], color=C_GASKT, lw=3.2, zorder=6)                    # DP8010 bond line (flange → shell)
    blind_rivet(ax, ix(-17), iz((HWmm - LT_DRUM_T) / 2), 90, IS * (LT_DRUM_T + HWmm), d=IS * LT_RIVET_D)
    draw_rect(ax, ix(-17) - IS * 7, iz(-LT_DRUM_T) - IS * 1.4, IS * 14, IS * 1.4, fc=C_STEEL, lw=0.6, zorder=6)  # backup washer (blind side, spreads the bulb load in the HDPE)
    draw_dim_v(ax, ix(-36), iz(0), iz(GAPmm), f"{GAPmm}mm GAP", offset=30, fs=6.2, font=FONT)
    leader(ax, ix(-17), iz(HWmm), ix(-20), iz(-LT_DRUM_T) - 44,
           "Al STRAIGHT-FLANGE HOLDER (anodized, 0.050\" wall — Tanis/Gordon AH400436):\nflange DP8010-BONDED to the HDPE shell (brown — spreads the load, no pull-through)\n+ Ø3.18 blind rivet w/ a backup washer (inside face); rivet clear of the brush",
           fs=6.0, color=C_OUT, ha="center", arrow_style="->", font=FONT)
    leader(ax, ix(HWmm + CHmm / 2), iz(GAPmm), ix(22), iz(GAPmm) + 60,
           f"#4 (3/16\") STRIP BRUSH\n0.008\" black nylon, {LT_WIPER_TRIM:.1f}mm trim", fs=6.0, color=C_OUT,
           ha="left", arrow_style="->", font=FONT)
    ax.text(ox, iz(GAPmm + HTmm) + 8, "FIXED HOUSING (bore)", ha="center", va="bottom",
            fontsize=6.2, color=C_DIM, **FONT, zorder=8)
    ax.text(ox, iz(-LT_DRUM_T) - 70, "ROTATING DRUM OD", ha="center", va="top",
            fontsize=6.2, color=C_DIM, **FONT, zorder=8)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes = [
        "SHELL → CAP LAP-AND-FASTEN JOINT  (both caps)",
        f"1. Rim: {LT_RIM_LEG}×{LT_RIM_LEG}×{LT_RIM_T} angle ring rolled to R{LT_CAP_OD // 2} — 6061-T6 Al, riveted to both Al caps.",
        f"2. Shell sleeves {LT_LAP_H}mm over the standing lip.",
        "3. Apply 3M DP8010 bead to the lap (structural LSE bond + light seal); clamp.",
        f"4. Drill Ø{LT_RIVET_HOLE:.1f} (#30), set {LT_RIVET_N}× Ø{LT_RIVET_D} SS blind rivets per cap (McMaster 97525A425, low-profile head, ~{LT_RIVET_PITCH}mm pitch), wet in DP8010.",
        "5. DP8010 (wet in the lap + the open mandrel bore) keeps the joint light-tight; supersedes the extrusion weld.",
        "SECTION A–A 7:1 (isotropic) · CAP PLAN 1:2 · fastener symbols schematic · ALL DIMS IN mm",
    ]
    draw_notes(ax, notes, X_LO + 60, -450, 15, fs=7, font=FONT, width=1780,
               title_color=TITLE_COL)

    title_block(ax, "SHEET 4 OF 12", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="ROTATING DRUM — SECURE (SHELL → CAP LAP-AND-FASTEN JOINT)",
                scale_note="SECTION 7:1 · CAP PLAN 1:2 · ALL DIMS IN mm",
                doc_id="TBS-001 · Revolving Light-Trap", height=0.045, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet4.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet4.png saved")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 5 — Bearing hub & stub-shaft detail
# Two enlarged sections (drum axis vertical): UPPER hub (isolated Al top ring,
# 6×M10) and LOWER hub (welded steel floor collar, 8×M10). SKF 6215-2RS1.
# ═════════════════════════════════════════════════════════════════════════════
def draw_sheet5():                              # Sheet 5 — bearing hub
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
        # stub shaft Ø75 — SHORT stub engaging ONLY the bearing bore. LOWER hub: fixed axially by two
        # circlips (terminates just above the upper circlip). UPPER hub (located, carries the hang): the
        # beam-side circlip is REPLACED by a bolted END-RETAINER PLATE, so the shaft is faced FLUSH with
        # the inner-race top face and the drum's hanging load runs through a POSITIVE bolted member, not a
        # single circlip. Either way a designed AXIAL GAP keeps the rotating parts clear of the fixed beam.
        z_stub = bw if up else 15 * SC * s             # upper: flush with the inner-race face; lower: just above the upper circlip
        z_fl = -40 * SC * s
        draw_rect(ax, cx - rs, min(z_stub, z_fl), 2 * rs, abs(z_stub - z_fl),
                  fc=C_STEEL, lw=1.4, zorder=6)
        if up:
            # END-RETAINER PLATE — Ø90×4 steel disc bolted to the shaft end by a central M10 CSK cap
            # screw; its rim clamps the SKF 6215 inner-race top face against the drum-side circlip, so the
            # drum's hanging load is carried by a bolted member (transport-shock robust). Sits in the
            # ring-bore pocket, ~3.5mm clear of the beam. Replaces the beam-side circlip.
            rp_h = 4 * SC
            draw_rect(ax, cx - 45 * SC, z_stub, 90 * SC, rp_h, fc="#9AA0A8", lw=1.4, zorder=10)   # Ø90 plate
            _rt, _rb = z_stub + rp_h, z_stub - 12 * SC                                            # central M10 CSK into the shaft end
            draw_bolt(ax, cx, (_rt + _rb) / 2, _rt - _rb, d=7 * SC, head=1, end="tapped", csk=True, zb=11)
        # bearing mount: isolated Al top ring (upper) / welded steel floor collar (lower). The ring
        # extends 5mm PAST the shaft top toward the beam (its beam-side face is the bolting datum), so
        # the shaft top is recessed inside the ring bore with a clear gap up to the beam.
        HRr = (LT_TOPRING_OD / 2 if up else LT_COLLAR_OD / 2) * SC
        # ring beam-side face: UPPER raised so the ring stands 45mm tall (was 38) — this lifts the beam
        # ~7mm so the end-retainer plate clears the fixed beam by ≈10mm (welding-tolerance margin);
        # LOWER collar stays 38mm (no retainer plate there).
        rtop = (27 if up else 20) * SC
        band(cx, ro, HRr, min(-18 * SC * s, rtop * s), max(-18 * SC * s, rtop * s),
             fc=(C_ALUM if up else C_STEEL), lw=1.4, zorder=5)
        if up:
            # UPPER = LOCATED bearing: the outer race is fixed BOTH ways. A machined SHOULDER on the
            # drum side (bore steps Ø130→Ø122) carries the hanging load (the drum weight seats the
            # outer race onto the ledge); a DIN 472 retaining ring in a groove on the beam side
            # captures it for handling/transport. (LOWER bearing FLOATS — plain Ø130 H7 bore.)
            for g in (-1, 1):
                lx = min(cx + g * (ro - 8 * SC), cx + g * ro)
                draw_rect(ax, lx, -18 * SC, 8 * SC, 18 * SC - bw, fc=C_ALUM, lw=1.0, zorder=6)   # shoulder lip
                rx0 = min(cx + g * (ro - 2 * SC), cx + g * (ro + 3 * SC))
                draw_rect(ax, rx0, bw, 5 * SC, 3.5 * SC, fc="#606068", lw=0.8, zorder=8)          # DIN 472 retaining ring
        # Ø240×12 SOLID steel MOUNT PLATE — the ring/collar bolts to THIS (its Ø200 bolt circle is far
        # wider than the 50mm beam) and it is fillet-welded to the beam, so the stack is ring/collar →
        # PLATE → beam: the ring/collar (and its bearing) sit SURFACE-mounted ON the plate, NOT sunk into
        # it. The plate fills the gap between the ring's beam-side face and the beam. 12mm ≈ 4× the wall.
        _bw = LT_FRAME_T * SC                                                # drawn wall thickness
        _pt = 4 * _bw                                                        # plate thickness (Ø240×12)
        _rface = rtop * s                                                    # ring/collar beam-side face (bolting datum)
        _bx0, _bwd = cx - 140 * SC, 280 * SC
        draw_rect(ax, _bx0 - 24 * SC, min(_rface, _rface + _pt * s), _bwd + 48 * SC, _pt,
                  fc=C_STEEL, lw=1.4, zorder=5)                                                  # mount plate, ON the ring face
        # axle beam — HOLLOW 50×50×3 RHS in LONGITUDINAL section (solid near+far walls + hollow void),
        # placed BEYOND the plate so the plate separates it from the ring/collar (shaft never touches it).
        zr0, zr1 = _rface + _pt * s, _rface + (_pt + 48 * SC) * s
        _bz0, _bz1 = min(zr0, zr1), max(zr0, zr1)
        draw_rect(ax, _bx0, _bz0, _bwd, _bz1 - _bz0, fc=C_STEEL, lw=1.4, zorder=4)               # outer (walls)
        draw_rect(ax, _bx0, _bz0 + _bw, _bwd, (_bz1 - _bz0) - 2 * _bw, fc=BG, lw=1.0, zorder=5)  # HOLLOW bore (void)
        for _bx in (_bx0, _bx0 + _bwd):                                      # break marks — beam continues past crop
            ax.plot([_bx - 4, _bx + 4, _bx - 4], [_bz0 + _bw, (_bz0 + _bz1) / 2, _bz1 - _bw],
                    color=C_OUT, lw=0.8, zorder=7, solid_capstyle="round")
        _wj = _rface + _pt * s                                               # plate↔beam junction (weld)
        for _wx in (_bx0, _bx0 + _bwd):                                      # fillet welds plate↔beam (both edges)
            _wd = -1 if _wx == _bx0 else 1
            ax.add_patch(mpatches.Polygon([(_wx, _wj), (_wx + _wd * 7 * SC, _wj), (_wx, _wj + 7 * SC * s)],
                                          closed=True, fc="#CC4422", ec="#CC4422", zorder=8))
        # Al drum cap (full Ø755 — shown BROKEN; it spans well past the ring bolts) + stub-shaft flange
        CAPW = 155 * SC
        draw_rect(ax, cx - CAPW, min(zc0, zc1), 2 * CAPW, abs(zc1 - zc0),
                  fc=C_ALUM, lw=1.4, zorder=6)
        for g in (-1, 1):                          # break line — the cap continues out to Ø755
            bxk, zt, zb = cx + g * CAPW, max(zc0, zc1), min(zc0, zc1)
            ax.plot([bxk, bxk + g * 8 * SC, bxk - g * 4 * SC, bxk],
                    [zt + 3, (zt + zb) / 2, (zt + zb) / 2, zb - 3], color=C_OUT, lw=1.0, zorder=8)
        zf0, zf1 = -40 * SC * s, -55 * SC * s
        draw_rect(ax, cx - 80 * SC, min(zf0, zf1), 160 * SC, abs(zf1 - zf0),
                  fc=C_STEEL, lw=1.4, zorder=6)
        for g in (-1, 1):                          # cap → flange bolts (M10 countersunk in the cap, threading into the TAPPED steel flange — no nut, Ø120 PCD)
            fb0, fb1 = -40 * SC * s, zc1
            draw_bolt(ax, cx + g * 60 * SC, (fb0 + fb1) / 2, abs(fb1 - fb0),
                      d=8 * SC, head=int(-s), end="tapped", csk=True, zb=9)
        # ring/collar → mount-plate bolts: CSK HEAD on the ring's outer face (accessible), up through
        # the ring, TAPPED into the solid 12mm steel mount plate (no rivet-nut — the plate is thick
        # enough to tap directly, and it, not the thin beam wall, carries the Ø200 bolt circle).
        for g in (-1, 1):
            ring_far = -18 * SC * s                    # ring face away from the plate (head bears here)
            wnz = rtop * s + _pt * s                    # through the ring, TAPPED into the Ø240×12 mount plate
            draw_bolt(ax, cx + g * LT_RING_BOLT_PCD / 2 * SC, (ring_far + wnz) / 2, abs(wnz - ring_far),
                      d=8 * SC, head=int(-s), end="tapped", csk=True, zb=9)
            # DIN 471 EXTERNAL circlip(s) — seated in the Ø72 shaft groove, projecting OUTWARD past the
            # shaft OD to butt the bearing inner-race face. UPPER hub: drum-side circlip only (the beam-side
            # one is replaced by the end-retainer plate). LOWER hub: both sides.
            for zc in ((-13.5 * SC,) if up else (13.5 * SC, -13.5 * SC)):
                draw_rect(ax, min(cx + g * (rs - 1.5 * SC), cx + g * (rs + 3 * SC)), zc - 1.3 * SC,
                          4.5 * SC, 2.6 * SC, fc="#707078", lw=0.8, zorder=9)
        # (Lower collar taps into its own Ø240×12 mount plate on the bottom beam — 8× M10, same
        #  scheme as the upper ring; the plate is welded to the beam, the collar bolts to the plate.)
        draw_cl_v(ax, cx, -135 * SC, 135 * SC)
        ax.text(cx, 115 * SC + CAPd + 60, "UPPER HUB — DRUM TOP" if up else
                "LOWER HUB — DRUM BOTTOM", ha="center", va="bottom", fontsize=8.5,
                color=TITLE_COL, fontweight="bold", **FONT, zorder=15)

    hub(UX, True)
    hub(LX, False)

    # (Shaft now terminates below the beam — visually obvious + covered in the note; no callout needed.)

    # ── Upper-hub callouts (left column) ─────────────────────────────────────
    LxT = UX - HALF - 60
    up_labels = [
        (55 * SC,  (-100 * SC, 40 * SC),  "MOUNT PLATE — 6×M10 tapped\n(Ø240×12 steel, welded to the beam)"),
        (18 * SC,  (-(ro + 20 * SC), 0),  "ALUMINUM TOP RING (bearing seat Ø130 H7) — LOCATED:\nouter race on a SHOULDER (drum side, Ø122) + a DIN 472\nRETAINING RING (beam side); nylon-isolated"),
        (-52 * SC, (-70 * SC, -47 * SC),  "STEEL FLANGE — bolt from cap\ninto TAPPED 4×M10"),
        (-90 * SC, (-90 * SC, -62 * SC),  f"TOP CAP {LT_CAP_TOP_T:.0f}mm 6061-T6 Al, Ø{LT_CAP_OD}\n(shown BROKEN — spans well past the ring; blueprint Sheet 6)"),
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
    draw_dim_h(ax, UX - LT_TOPRING_OD / 2 * SC, UX + LT_TOPRING_OD / 2 * SC, -385, f"Ø{LT_TOPRING_OD} Al TOP RING OD",
               offset=46, fs=6.2, above=False, font=FONT)
    draw_dim_h(ax, UX - 140 * SC, UX + 140 * SC, -455, "280mm PANEL RAIL W",
               offset=46, fs=6.2, above=False, font=FONT)
    # Vertical (height / thickness), stacked in the centre gap:
    draw_dim_v(ax, UX + 255, -bw, bw, f"{SKF6215_W}mm BRG W", offset=44, fs=6.0,
               right=True, font=FONT)
    draw_dim_v(ax, UX + 330, -18 * SC, 27 * SC, "45mm RING H", offset=44, fs=6.0,
               right=True, font=FONT)
    draw_dim_v(ax, UX + 405, 39 * SC, 87 * SC, "48mm RAIL H", offset=44, fs=6.0,
               right=True, font=FONT)
    draw_dim_v(ax, UX + 480, -55 * SC, -40 * SC, "15mm FLANGE T", offset=44,
               fs=6.0, right=True, font=FONT)
    draw_dim_v(ax, UX + 555, -55 * SC - CAPd, -55 * SC, f"{LT_CAP_TOP_T:.0f}mm Al CAP T",
               offset=44, fs=6.0, right=True, font=FONT)
    draw_dim_v(ax, UX - 255, -40 * SC, bw, "52mm SHAFT L", offset=44,
               fs=6.0, font=FONT)
    leader(ax, UX + rs, -13.5 * SC, UX + 150, 102 * SC,
           "DRUM-SIDE CIRCLIP (DIN 471) +\nBEAM-SIDE END-RETAINER PLATE —\ntogether fix the bearing on the shaft",
           fs=6.2, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, UX + 40 * SC, bw + 2 * SC, UX - 150, 118 * SC,
           "END-RETAINER PLATE — Ø90×4 steel, bolted to the shaft end (M10 CSK); its rim\n"
           "clamps the inner-race face, so the hanging load runs through a BOLTED member,\n"
           "not a lone circlip. Sits in the ring-bore pocket, ≈10mm clear of the fixed beam",
           fs=6.2, color=C_OUT, ha="right", arrow_style="->", font=FONT)

    # ── Lower-hub callouts (right column) ────────────────────────────────────
    RxL = LX + HALF + 60
    lo_labels = [
        (58 * SC,  (0, 115 * SC),         f"BOTTOM CAP {LT_CAP_BOT_T:.0f}mm 6061-T6 Al\nbolt into TAPPED 4×M10 flange"),
        (-48 * SC, (100 * SC, -40 * SC),  "MOUNT PLATE — 8×M10 tapped\n(Ø240×12 steel, welded to the beam)"),
        (12 * SC,  (ro + 20 * SC, 0),     "STEEL FLOOR COLLAR (BOLTED, not welded) — FLOATING bearing:\nthe outer race is deliberately NOT axially retained. The plain Ø130 H7\nbore locates it radially + it slides freely for thermal growth; the bearing\nis a captive unit held on the shaft by the circlips (upper bearing = located)"),
        (-18 * SC, (ro - 6 * SC, -18 * SC), "COLLAR → MOUNT PLATE:\n8×M10 tapped (plate welded to beam)"),
    ]
    for zt, (tx, tz), txt in lo_labels:
        leader(ax, LX + tx, tz, RxL, zt, txt, fs=6.5, color=C_OUT, ha="left",
               arrow_style="->", font=FONT)
    # Lower-hub dimension lines — collar + floor plate (h + v) ────────────────
    draw_dim_h(ax, LX - LT_COLLAR_OD / 2 * SC, LX + LT_COLLAR_OD / 2 * SC, -310, f"Ø{LT_COLLAR_OD} COLLAR OD",
               offset=46, fs=6.2, above=False, font=FONT)
    draw_dim_h(ax, LX - 140 * SC, LX + 140 * SC, -372, "280mm FLOOR PLATE W",
               offset=46, fs=6.2, above=False, font=FONT)
    draw_dim_v(ax, LX - HALF - 40, -20 * SC, 18 * SC, "38mm COLLAR H", offset=44,
               fs=6.0, font=FONT)
    draw_dim_v(ax, LX - HALF - 120, -80 * SC, -32 * SC, "48mm BEAM H", offset=44,
               fs=6.0, font=FONT)
    ax.text(LX, -235, "bearing · shaft · cap · flange  AS UPPER HUB", ha="center",
            va="top", fontsize=6.2, color=C_DIM, **FONT, zorder=15)

    # ── MOUNT-PLATE DETAIL — ring bolts UP into a tapped steel plate that is WELDED to the beam ──
    IS = 7
    ox, oz = 1830, -740
    def rx(mm): return ox + IS * mm
    def rz(mm): return oz + IS * mm
    T = LT_FRAME_T                                            # 3mm RHS wall
    PT = LT_BRG_PLATE_T                                       # 12mm SOLID steel mount plate
    RB = 50                                                   # 50×50 beam box shown (mm)
    ax.text(ox, rz(PT + RB + 12), "MOUNT-PLATE DETAIL  (7:1)",
            ha="center", va="bottom", fontsize=7.0, color=TITLE_COL, fontweight="bold", **FONT, zorder=15)
    ax.text(ox, rz(PT + RB + 2), "ring → tapped plate → welded beam", ha="center", va="bottom",
            fontsize=6.0, color=C_DIM, **FONT, zorder=15)
    draw_rect(ax, rx(-30), rz(-15), IS * 60, IS * 15, fc=C_ALUM, lw=1.2, zorder=6)                 # Al ring (below the plate)
    draw_rect(ax, rx(-58), rz(0), IS * 116, IS * PT, fc=C_STEEL, lw=1.4, zorder=5)                 # SOLID mount plate (Ø240, overhangs the beam)
    draw_rect(ax, rx(-25), rz(PT), IS * 50, IS * RB, fc=C_STEEL, lw=1.4, zorder=5)                 # 50×50 RHS beam — outer
    draw_rect(ax, rx(-25) + IS * T, rz(PT + T), IS * (50 - 2 * T), IS * (RB - 2 * T), fc=BG, lw=0.8, zorder=5)  # beam hollow bore
    for g in (-1, 1):                                         # fillet-weld triangles at the plate↔beam junction
        ax.add_patch(mpatches.Polygon([(rx(g * 25), rz(PT)), (rx(g * 25) + g * IS * 7, rz(PT)),
                                       (rx(g * 25), rz(PT) + IS * 7)], closed=True, fc="#CC4422", ec="#CC4422", zorder=8))
    # ring → plate bolt: CSK head FLUSH in the ring underside, shank spanning the full
    # 15mm ring + tapped into the 12mm plate (no nut) — i.e. the depth of BOTH plates
    _bz0, _bz1 = rz(-15), rz(PT - 1)
    draw_bolt(ax, ox, (_bz0 + _bz1) / 2, _bz1 - _bz0, d=58, head=-1, csk=True, end="tapped")
    leader(ax, ox - 20, rz(-8), rx(-52), rz(-8) + 20, "CSK bolt head — flush in the\nring underside (driven from below)",
           fs=6.0, color=C_OUT, ha="right", arrow_style="->", font=FONT)
    leader(ax, ox + 24, rz(PT / 2), rx(64), rz(PT / 2 + 12), "M10 TAPPED into the Ø240×12 SOLID\nsteel plate (thick — taps directly)",
           fs=6.0, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, rx(28), rz(PT + 2), rx(60), rz(PT + 26), "PLATE fillet-WELDED to the beam\n(steel↔steel — cage weldment)",
           fs=6.0, color=C_DIM, ha="left", arrow_style="->", font=FONT)

    # ── Component blueprints are on Sheet 6 (single-part drawings) ───────────
    ax.text((UX + LX) / 2, -640,
            "MACHINED COMPONENTS (Al top ring · steel floor collar · stub-shaft + flange) —\n"
            "fully dimensioned single-part blueprints incl. bolt patterns on SHEET 6.\n"
            "End cap (Ø855 6061-T6 Al, 4×M10 hub flange) — SHEET 6.",
            ha="center", va="center", fontsize=8, color=TITLE_COL, fontweight="bold",
            **FONT, zorder=9)

    # ── Fabrication / spec notes ─────────────────────────────────────────────
    notes = [
        "BEARING HUB — SPECIFICATION",
        f"Bearing ×2: SKF 6215-2RS1 — Ø{SKF6215_ID}×Ø{SKF6215_OD}×{SKF6215_W}mm, sealed 2RS, C3, 0–120°C, 52.7 kN dyn.",
        f"Caps ×2 (identical): {LT_CAP_TOP_T:.0f}mm 6061-T6 Al — drum → cap → 4×M10 steel flange → Ø75 stub shaft → bearing.",
        "Bearing mounts: each SKF 6215 seats in an isolated ring/collar that bolts (M10 tapped) into a Ø240×12 steel MOUNT PLATE fillet-welded across the 50×50 beam — the ring's Ø200 bolt circle is far wider than the beam, and the 12mm plate taps directly (no rivet-nuts). Upper ring nylon-isolated; lower collar floats. Cap→flange: countersunk bolt in the cap, THROUGH the steel flange + a nut (drilled through — not tapped). Full fastening on Sheet 6.",
        "Axial retention — INNER race: circlip on the stub shaft each side of each bearing (DIN 471). OUTER race: the UPPER bearing is LOCATED — the outer race seats on a machined shoulder (bore steps Ø130→Ø122, drum side) that carries the hanging load, captured by a DIN 472 retaining ring on the beam side; the LOWER bearing FLOATS (plain Ø130 H7 bore, outer race free to slide) so it can't fight thermal growth.",
        "Shaft seat: the stub shaft seats ONLY in the Ø75 h6 bearing bore — the SKF 6215 IS the 'socket' (off-the-shelf; shaft blueprint on Sheet 6). It TERMINATES just below the beam underside — it does NOT penetrate the beam and needs NO clearance bore; the bearing (in the ring below the beam) carries + locates the drum, and the load goes to the beam through the ring bolts.",
        "ASSEMBLY SEQUENCE: the ring/collar → mount-plate CSK bolt circle (Ø200) sits CLEAR of the Ø160 welded stub-shaft flange, so the drum flange passes the bolt heads on assembly. Bolt the ring to the plate FIRST (mount plate + ring + bearing on the beam), THEN insert the drum stub up into the bearing. The Ø755 cap (shown broken — it spans well past the bolt circle) then covers the bolts, so servicing them means un-hanging the drum.",
        "This sheet is the hub ASSEMBLY (how the parts stack). Single-part blueprints + bolt patterns: bearing seats + stub-shaft + end cap on SHEET 6; frame members on SHEET 8.",
        "SECTIONS 2.2:1 (isotropic) · ALL DIMS IN mm",
    ]
    draw_notes(ax, notes, X_LO + 60, -830, 46, fs=7, font=FONT,
               width=2350, wrap=140, title_color=TITLE_COL)

    # ── Section scale bar (50 mm, to the 2.2:1 section geometry) ─────────────
    sbx, sbz = UX - HALF - 40, -560
    ax.plot([sbx, sbx + 50 * SC], [sbz, sbz], color=C_OUT, lw=1.4, zorder=8)
    for xt in (sbx, sbx + 25 * SC, sbx + 50 * SC):
        ax.plot([xt, xt], [sbz - 10, sbz + 10], color=C_OUT, lw=1.0, zorder=8)
    ax.text(sbx + 25 * SC, sbz - 22, "50 mm  (SECTIONS 2.2:1)", ha="center", va="top",
            fontsize=6.5, color=C_OUT, **FONT, zorder=8)

    title_block(ax, "SHEET 5 OF 12", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="BEARING HUB & STUB-SHAFT — ASSEMBLY",
                scale_note="SECTIONS 2.2:1 · ALL DIMS IN mm",
                doc_id="TBS-001 · Revolving Light-Trap", height=0.045, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet5.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet5.png saved")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 6 — Machined components (single-part blueprints, 1:2)
# The turned/machined metal parts that Sheet 5 assembles: upper Al bearing ring,
# lower steel floor collar, and the stub-shaft + flange. Each: PLAN (end view with
# OD / bore / PCD / bolt holes) + SECTION (thickness) + full dims + material.
# ═════════════════════════════════════════════════════════════════════════════
def draw_sheet6():
    # PORTRAIT single column — four machined parts stacked, drawn large (page width).
    s2 = 2.2                                                                  # 2.2:1 (rings / collar / stub)
    scc = 0.5                                                                 # 1:2 (the big Ø855 end cap)
    CX = 560                                                                  # single-column center
    SEC_DZ = 400                                                             # plan → section drop (rings)
    R_RING, R_COLLAR, R_STUB, R_CAP = -150, -1060, -1990, -3110              # plan-z of each row
    X_LO, X_HI = -260, 1380
    Z_LO, Z_HI = R_CAP - 860, 360                                            # extra bottom margin: wrapped notes clear the title block
    FIG_H = 26.0
    FIG_W = FIG_H * (X_HI - X_LO) / (Z_HI - Z_LO)
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DIAGRAM_DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Z_LO, Z_HI)
    ax.set_aspect("equal")                                                   # ISOTROPIC
    ax.axis("off")
    ax.text(CX, Z_HI - 8, "MACHINED COMPONENTS\nEND CAP + BEARING SEATS + STUB-SHAFT",
            ha="center", va="top", fontsize=11, color=TITLE_COL, fontweight="bold", **FONT, zorder=15)

    def holes(cx, cz, rpcd, n):
        for i in range(n):
            a = math.radians(90 + i * 360.0 / n)
            hx, hy = cx + rpcd * math.cos(a), cz + rpcd * math.sin(a)
            draw_circle(ax, hx, hy, 7, lw=1.0, color=C_OUT, fill=True, fc="white", zorder=8)
            ax.plot([hx - 12, hx + 12], [hy, hy], color=C_OUT, lw=0.5, zorder=9)
            ax.plot([hx, hx], [hy - 12, hy + 12], color=C_OUT, lw=0.5, zorder=9)

    def ring(pz, od, bore, pcd, n, thk, fc, title, mat, weldnote=None, located=False):
        cx = CX
        rod, rbore, rpcd = od / 2 * s2, bore / 2 * s2, pcd / 2 * s2
        sz = pz - SEC_DZ
        ax.text(cx, pz + rod + 82, title, ha="center", va="bottom", fontsize=9.5,
                color=TITLE_COL, fontweight="bold", **FONT, zorder=10)
        draw_circle(ax, cx, pz, rod, lw=1.8, color=C_OUT, fill=True, fc=fc, zorder=5)
        draw_circle(ax, cx, pz, rbore, lw=1.4, color=C_OUT, fill=True, fc="white", zorder=6)
        draw_circle(ax, cx, pz, rpcd, lw=0.9, color=C_CL, ls="--", zorder=6)
        holes(cx, pz, rpcd, n)
        draw_cl_h(ax, cx - rod - 20, cx + rod + 20, pz)
        draw_cl_v(ax, cx, pz - rod - 20, pz + rod + 20)
        draw_dim_h(ax, cx - rod, cx + rod, pz + rod + 6, f"Ø{od} OD", offset=34, fs=7, font=FONT)
        ax.text(cx, pz, f"Ø{bore}\nH7", ha="center", va="center", fontsize=7, color=C_DIM, **FONT, zorder=9)
        ax.text(cx, pz - rod - 14, f"{n}×M10 COUNTERSUNK on Ø{pcd} PCD (flush in the ring face) · Ø11 c'bore → tapped M10 in the Ø240×12 mount plate",
                ha="center", va="top", fontsize=7.5, color=C_OUT, **FONT, zorder=9)
        tz = thk * s2                                                         # SECTION (annular)
        for xr0, xr1 in ((cx - rod, cx - rbore), (cx + rbore, cx + rod)):
            draw_rect(ax, xr0, sz, xr1 - xr0, tz, fc=fc, lw=1.4, zorder=5)
        if located:
            # LOCATED bearing seat: bore steps Ø{bore}→Ø{bore-8} to form a SHOULDER (drum-side end)
            # the outer race seats on; a DIN 472 retaining-ring groove at the beam-side end captures it.
            rsh = (bore - 8) / 2 * s2
            for g in (-1, 1):
                draw_rect(ax, min(cx + g * rsh, cx + g * rbore), sz, rbore - rsh, tz * 0.42, fc=fc, lw=1.0, zorder=6)      # shoulder lip (drum end, outer-race abutment)
                gw = 4.15 * s2                                                                                             # DIN 472 for Ø130: NARROW 4.15mm axial groove/ring (McMaster 98455A170)
                gz = sz + tz * 0.60 - gw / 2                                                                               # beam-side, set well IN from the edge
                draw_rect(ax, min(cx + g * rbore, cx + g * (rbore + 2 * s2)), gz, 2 * s2, gw, fc=BG, lw=0.8, zorder=6)      # groove Ø134×4.15 (2mm deep) cut OUTWARD into the bore wall
                draw_rect(ax, min(cx + g * (rbore - 2 * s2), cx + g * (rbore + 2 * s2)), gz + 0.3 * s2, 4 * s2, gw - 0.6 * s2, fc="#606068", lw=0.8, zorder=7)  # DIN 472 internal ring — narrow, projecting INWARD past the bore to retain the outer race
            ax.text(cx + rod + 100, sz + tz / 2, "LOCATED seat:\nshoulder (drum end)\n+ ring groove (beam end)\n— spec in notes", ha="left",
                    va="center", fontsize=6.2, color=C_OUT, **FONT, zorder=9)
        draw_cl_v(ax, cx, sz - 16, sz + tz + 16)
        draw_dim_v(ax, cx + rod + 36, sz, sz + tz, f"{thk}mm THK", offset=34, fs=7, right=True, font=FONT)
        draw_dim_h(ax, cx - rbore, cx + rbore, sz - 20, f"Ø{bore} BORE", offset=30, fs=6.6, above=False, font=FONT)
        if weldnote:
            # Ø240×12 steel MOUNT PLATE (fillet-welded to the bottom beam) — the collar taps into it
            plate_tz = LT_BRG_PLATE_T * s2
            plate_hw = LT_BRG_PLATE_OD / 2 * s2
            draw_rect(ax, cx - plate_hw, sz - plate_tz, 2 * plate_hw, plate_tz, fc=C_STEEL, lw=1.4, zorder=4)
            for g in (-1, 1):                        # collar bolts (M10 CSK tapped) down into the plate; CSK flush in the collar face
                draw_bolt(ax, cx + g * rpcd, (sz + tz + sz - plate_tz) / 2, (tz + plate_tz),
                          d=10 * s2, head=1, end="tapped", csk=True, zb=8)
            draw_dim_h(ax, cx - plate_hw, cx + plate_hw, sz - plate_tz - 22, f"Ø{LT_BRG_PLATE_OD} MOUNT PLATE",
                       offset=28, fs=6.4, above=False, font=FONT)
            draw_dim_v(ax, cx + plate_hw + 34, sz - plate_tz, sz, f"{LT_BRG_PLATE_T}mm PLATE",
                       offset=30, fs=6.4, right=True, font=FONT)
            leader(ax, cx - plate_hw + 50, sz - plate_tz / 2, cx - plate_hw - 20, sz - plate_tz - 70,
                   f"Ø{LT_BRG_PLATE_OD}×{LT_BRG_PLATE_T} STEEL MOUNT PLATE\n(fillet-welded to the bottom beam; collar taps in — 8× M10)", fs=6.4, color=C_OUT,
                   ha="right", arrow_style="->", font=FONT)
            mat_z = sz - plate_tz - 128
        else:
            mat_z = sz - 54
        ax.text(cx, mat_z, mat + ("" if not weldnote else f"\n{weldnote}"),
                ha="center", va="top", fontsize=7.5, color=C_OUT, **FONT, zorder=9)

    ring(R_RING, LT_TOPRING_OD, SKF6215_OD, LT_RING_BOLT_PCD, LT_FRAME_MOUNT_BOLT_TOP, 45, C_ALUM,
         "UPPER BEARING RING  (2.2:1)", "6061-T6 Al · Ø130 H7 seat + Ø122 shoulder + DIN 472 groove — LOCATED · nylon-isolated · 45mm tall", located=True)
    ring(R_COLLAR, LT_COLLAR_OD, SKF6215_OD, LT_RING_BOLT_PCD, LT_FRAME_MOUNT_BOLT_BOT, 38, C_STEEL,
         "LOWER BEARING COLLAR  (2.2:1)", "A36 steel · plain Ø130 H7 bore — FLOATING (outer race slides)", weldnote="8× M10 TAPPED into the Ø240×12 mount plate (welded to beam)")

    # ── Stub-shaft + flange: flange plan (top) + elevation (below) ───────────
    cx = CX
    sh_r, fl_r, fl_t = SKF6215_ID / 2 * s2, 160 / 2 * s2, 12 * s2
    shaft_L = LT_STUB_SHAFT_L * s2
    fpz = R_STUB
    ez = R_STUB - 690                                                        # elevation base (flange), shaft up
    ax.text(cx, fpz + fl_r + 82, "STUB-SHAFT + FLANGE  (2.2:1)", ha="center", va="bottom", fontsize=9.5,
            color=TITLE_COL, fontweight="bold", **FONT, zorder=10)
    draw_circle(ax, cx, fpz, fl_r, lw=1.8, color=C_OUT, fill=True, fc=C_STEEL, zorder=5)
    draw_circle(ax, cx, fpz, sh_r, lw=1.4, color=C_OUT, fill=True, fc="#9BA0A8", zorder=6)
    draw_circle(ax, cx, fpz, 120 / 2 * s2, lw=0.9, color=C_CL, ls="--", zorder=6)
    holes(cx, fpz, 120 / 2 * s2, 4)
    draw_cl_h(ax, cx - fl_r - 20, cx + fl_r + 20, fpz)
    draw_dim_h(ax, cx - fl_r, cx + fl_r, fpz + fl_r + 6, "Ø160 FLANGE", offset=32, fs=7, font=FONT)
    ax.text(cx, fpz - fl_r - 14, "4×M10 TAPPED on Ø120 PCD (cap bolt threads in — no nut)", ha="center", va="top",
            fontsize=7.5, color=C_OUT, **FONT, zorder=9)
    draw_rect(ax, cx - fl_r, ez - fl_t, 2 * fl_r, fl_t, fc=C_STEEL, lw=1.6, zorder=5)     # flange
    draw_rect(ax, cx - sh_r, ez, 2 * sh_r, shaft_L, fc=C_STEEL, lw=1.6, zorder=5)         # shaft
    for g in (-1, 1):
        ax.add_patch(mpatches.Polygon([(cx + g * sh_r, ez), (cx + g * (sh_r + 14), ez),
                                       (cx + g * sh_r, ez + 14)], closed=True, fc="#CC4422", ec="#CC4422", zorder=7))
    for zc in (ez + shaft_L - 12, ez + shaft_L - 26):
        ax.plot([cx - sh_r, cx - sh_r + 8], [zc, zc], color=C_OUT, lw=1.2, zorder=8)
        ax.plot([cx + sh_r - 8, cx + sh_r], [zc, zc], color=C_OUT, lw=1.2, zorder=8)
    # M10 tapped hole in the BEAM-SIDE end — UPPER shaft only (end-retainer-plate screw)
    _thd = 5.25 * s2                                                                     # Ø10.5 tap drill (shown)
    draw_rect(ax, cx - _thd, ez + shaft_L - 34, 2 * _thd, 34, fc="white", lw=1.0, zorder=8)
    for _k in (6, 14, 22, 30):
        _tz = ez + shaft_L - _k
        ax.plot([cx - _thd, cx - _thd + 5], [_tz, _tz + 4], color=C_OUT, lw=0.6, zorder=9)
        ax.plot([cx + _thd - 5, cx + _thd], [_tz + 4, _tz], color=C_OUT, lw=0.6, zorder=9)
    leader(ax, cx + _thd, ez + shaft_L - 18, cx + fl_r + 40, ez + shaft_L - 66,
           "M10 ×16 TAPPED (beam end,\nUPPER shaft) — retainer-plate screw", fs=6.4,
           color=C_OUT, ha="left", arrow_style="->", font=FONT)
    draw_cl_v(ax, cx, ez - fl_t - 16, ez + shaft_L + 16)
    draw_dim_v(ax, cx - fl_r - 34, ez, ez + shaft_L, f"{LT_STUB_SHAFT_L} LG (Ø{SKF6215_ID})", offset=34, fs=7, font=FONT)
    draw_dim_v(ax, cx + fl_r + 34, ez - fl_t, ez, "12mm THK", offset=32, fs=6.6, right=True, font=FONT)
    ax.text(cx, ez + shaft_L + 16, "Ø75 h6 stub · circlip groove Ø72.0 × 2.65 (90154A895) — LOWER shaft: each end (2 clips) · UPPER shaft: drum end only + M10 tapped beam end", ha="center", va="bottom",
            fontsize=7, color=C_DIM, **FONT, zorder=9)
    ax.text(cx, ez - fl_t - 34, "1045 steel shaft + steel flange · weld + stress-relieve", ha="center",
            va="top", fontsize=7.5, color=C_OUT, **FONT, zorder=9)

    # ── End cap (Ø855) — plan + thickness note (1:2) ─────────────────────────
    ccx, ccz = CX, R_CAP
    cr = LT_CAP_OD / 2 * scc
    ax.text(ccx, ccz + cr + 82, "END CAP ×2 identical  (1:2)", ha="center", va="bottom",
            fontsize=9.5, color=TITLE_COL, fontweight="bold", **FONT, zorder=10)
    draw_circle(ax, ccx, ccz, cr, lw=1.8, color=C_OUT, fill=True, fc=C_ALUM, zorder=5)
    draw_circle(ax, ccx, ccz, 78 * scc, lw=1.0, color=C_OUT, zorder=6)                   # hub boss
    draw_circle(ax, ccx, ccz, SKF6215_ID / 2 * scc, lw=1.2, color="#CC4422", zorder=7)   # Ø75 bore
    holes(ccx, ccz, 60 * scc, 4)                                                         # 4× flange clearance holes
    oh2 = LT_OPENING_DEG / 2
    n_rim = round((LT_SHELL_ARC / 360.0) * math.pi * LT_CAP_OD / LT_RIM_RIVET_PITCH)
    rrc = (LT_CAP_OD / 2 - 14) * scc
    for i in range(n_rim):
        a = math.radians(oh2 + (i + 0.5) / n_rim * LT_SHELL_ARC)
        draw_circle(ax, ccx + rrc * math.cos(a), ccz + rrc * math.sin(a), 4,
                    lw=0.7, color="#CC4422", fill=True, fc="#CC4422", zorder=7)
    draw_circle(ax, ccx, ccz, rrc, lw=0.7, color=C_CL, ls="--", zorder=6)
    draw_cl_h(ax, ccx - cr - 20, ccx + cr + 20, ccz)
    draw_cl_v(ax, ccx, ccz - cr - 20, ccz + cr + 20)
    draw_dim_h(ax, ccx - cr, ccx + cr, ccz + cr + 6, f"Ø{LT_CAP_OD} OD", offset=34, fs=7, font=FONT)
    ax.text(ccx, ccz - cr - 14,
            f"4× Ø11 clearance on Ø120 PCD (bolt → tapped flange) · Ø{SKF6215_ID} h6 bore · {LT_CAP_TOP_T:.0f}mm 6061-T6 Al plate\n"
            f"{n_rim}× Ø{LT_RIVET_HOLE} rim-rivet holes @ {LT_RIM_RIVET_PITCH}mm on the 280° arc",
            ha="center", va="top", fontsize=7.5, color=C_OUT, **FONT, zorder=9)

    # ── CIRCLIP DETAIL — DIN 471 external ring seated in the Ø75 shaft groove (close-up · 5:1) ──
    CD = 5.0
    ccx2, ccz2 = 980, -2150
    def CDX(mm): return ccx2 + CD * mm
    def CDZ(mm): return ccz2 + CD * mm
    ax.text(ccx2, CDZ(28), "CIRCLIP DETAIL (5:1)\nDIN 471 IN SHAFT GROOVE",
            ha="center", va="bottom", fontsize=8.5, color=TITLE_COL, fontweight="bold", **FONT, zorder=15)
    draw_rect(ax, CDX(-16), CDZ(-22), CD * 16, CD * 44, fc="#9BA0A8", lw=1.6, zorder=5)         # Ø75 shaft body (OD at local x=0)
    draw_rect(ax, CDX(-1.5), CDZ(-1.325), CD * 1.5, CD * 2.65, fc=BG, lw=0.8, zorder=6)         # groove notch — Ø72.0 × 2.65 cut into the OD
    draw_rect(ax, CDX(-1.5), CDZ(-1.25), CD * 3.3, CD * 2.5, fc="#565660", lw=1.1, zorder=8)    # DIN 471 ring — seated in the groove, MAJORITY projecting OUT past the OD
    draw_rect(ax, CDX(0), CDZ(1.25), CD * 12, CD * 16, fc=C_STEEL, lw=1.2, zorder=6)            # bearing inner race — bore on the shaft, end face butts the circlip
    ax.plot([CDX(0), CDX(0)], [CDZ(-22), CDZ(22)], color=C_CL, ls="--", lw=0.7, zorder=7)       # Ø75 OD reference line
    draw_dim_v(ax, CDX(-20), CDZ(-1.325), CDZ(1.325), "2.65", offset=CD * 2.4, fs=6.0, font=FONT)   # groove width
    leader(ax, CDX(1.8), CDZ(0.2), CDX(15), CDZ(-13),
           "DIN 471 EXTERNAL CIRCLIP\n(McMaster 90154A895) — seated in\nthe Ø72.0 × 2.65 shaft groove,\nprojecting ~1.8mm past the Ø75 OD\nto retain the bearing inner race",
           fs=6.2, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, CDX(7), CDZ(9), CDX(15), CDZ(15), "BEARING INNER RACE\n(end face butts the circlip)", fs=6.0, color=C_DIM, ha="left", arrow_style="->", font=FONT)
    leader(ax, CDX(-11), CDZ(-15), CDX(-20), CDZ(-19), "SHAFT Ø75 h6\n(groove Ø72.0)", fs=6.0, color=C_DIM, ha="right", arrow_style="->", font=FONT)

    notes = [
        "MACHINED COMPONENTS  (end cap + bearing seats + stub-shaft — assembled on Sheet 5)",
        f"Bearing seat bores Ø{SKF6215_OD} H7 for the SKF 6215 OD. Stub shaft Ø{SKF6215_ID} h6, circlip groove Ø72.0 × 2.65 (INNER-race retention; McMaster 90154A895, ext, Ø75). LOWER shaft: a groove each side of the bearing (2 clips). UPPER shaft (carries the hang): drum-side groove only — the beam-side clip is REPLACED by a bolted END-RETAINER PLATE (Ø90 × 4 mild steel, central Ø10.5 c'bore for an M10×25 flat-head CSK screw) into an M10 ×16 tapped hole in the beam-side shaft end; its rim clamps the inner-race face, so the hang is on a bolted member, not one circlip. OUTER race — UPPER ring LOCATED: the bore steps Ø130→Ø122 to form a ~4mm-high shoulder (drum end, outer-race abutment) + a retaining-ring groove Ø134.0 × 4.15 (beam end; McMaster 98455A170, int, Ø130). LOWER collar: plain Ø130 H7 bore, FLOATING (outer race free to slide — the upper bearing is the located one).",
        "FASTENING — cap → flange: countersunk bolt in the cap (Ø11 clearance) threading into the TAPPED stub-shaft flange on the Ø120 PCD — the flange is a machined steel part, so it is tapped directly (no nut; bolt ends flush in the flange). Ring + collar → MOUNT PLATE: M10 CSK tapped into the Ø240×12 steel plate that is fillet-welded across the 50×50 beam (steel↔steel — part of the cage weldment); the 12mm plate is thick enough to tap directly, so no rivet-nuts, and the wide plate catches the Ø200 bolt circle the 50mm beam cannot. Al ring nylon-isolated.",
        "RINGS + STUB 2.2:1 · CAP 1:2 (isotropic) · bolt holes shown enlarged · ALL DIMS IN mm",
    ]
    draw_notes(ax, notes, X_LO + 40, R_CAP - cr - 100, 34, fs=6, font=FONT, width=1560, wrap=138, title_color=TITLE_COL)

    title_block(ax, "SHEET 6 OF 12", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="MACHINED COMPONENTS — END CAP + BEARING SEATS + STUB-SHAFT",
                scale_note="RINGS + STUB 2.2:1 · CAP 1:2 · ALL DIMS IN mm",
                doc_id="TBS-001 · Revolving Light-Trap", height=0.02, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet6.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet6.png saved")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 7 — Light-lock verification (access + light-path + seals)
# Panel A: an operator fits the open drum bore. Panel B: three drum rotations prove
# no straight-through EXT↔INT light path (the drum's opaque wall always blocks one
# side). Panel C: the running-gap brush + axial-end neoprene seal details.
# ═════════════════════════════════════════════════════════════════════════════
def draw_sheet7():
    HR, DR = LT_HOUSING_R, LT_DRUM_OR
    OD = LT_OPENING_DEG
    SHO, DEP = 520, 330                     # operator plan footprint (mm)
    GREEN, AMBER = "#2E8B57", "#D08000"
    HOUS, DRUMC = "#2E5E8C", "#B5732E"      # fixed housing / rotating drum

    fig, ax = plt.subplots(figsize=(20, 21.5))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    ax.set_xlim(-130, 2130); ax.set_ylim(-1260, 1460)
    ax.set_aspect("equal"); ax.axis("off")

    def arc(cx, cy, r, gaps, lw, color, z=5):
        step = 0.4
        n = int(360 / step) + 1
        xs, ys = [], []
        for i in range(n):
            deg = i * step
            openm = any(abs((deg - gc + 180) % 360 - 180) <= gw / 2 for gc, gw in gaps)
            if openm:
                xs.append(float("nan")); ys.append(float("nan"))
            else:
                t = math.radians(deg)
                xs.append(cx + r * math.cos(t)); ys.append(cy + r * math.sin(t))
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="butt", zorder=z)

    def zones(cx, cy, w):
        ax.add_patch(mpatches.Rectangle((cx - w, cy - w), 2 * w, w, fc="#EEF2F8", ec="none", zorder=1))
        ax.add_patch(mpatches.Rectangle((cx - w, cy), 2 * w, w, fc="#EEF6EE", ec="none", zorder=1))
        ax.plot([cx - w, cx + w], [cy, cy], color=C_DIM, lw=0.8, ls=(0, (5, 3)), zorder=2)

    def sun(x, y, s=28):
        ax.add_patch(mpatches.Circle((x, y), s, fc="#FFD24D", ec=AMBER, lw=1.2, zorder=8))
        for a in range(0, 360, 45):
            r = math.radians(a)
            ax.plot([x + s * 1.2 * math.cos(r), x + s * 1.7 * math.cos(r)],
                    [y + s * 1.2 * math.sin(r), y + s * 1.7 * math.sin(r)], color=AMBER, lw=1.3, zorder=8)

    ax.text(1000, 1415, "REVOLVING LIGHT-TRAP — PASSES BOTH TESTS",
            ha="center", fontsize=15, fontweight="bold", color=C_OUT, **FONT)
    ax.text(1000, 1378, f"Fixed Ø{int(round(2 * HR))} housing (two {OD}° openings, 180° apart) + single-opening C-shell drum",
            ha="center", fontsize=9, color=GREEN, **FONT)
    ax.plot([-130, 2130], [660, 660], color=C_DIM, lw=1.0, ls=(0, (6, 4)), zorder=3)

    # ── PANEL A — person fit ──
    ax.text(-110, 1352, "A.  PERSON FIT  —  open drum bore, no fins", ha="left",
            fontsize=12, fontweight="bold", color=C_OUT, **FONT)
    Acx, Acy, s = 470, 940, 0.78
    Rd, ORd = HR * s, DR * s
    zones(Acx, Acy, Rd + 64)
    arc(Acx, Acy, Rd, [(90, OD), (270, OD)], 6, HOUS, 5)
    arc(Acx, Acy, ORd, [(270, OD)], 4, DRUMC, 6)
    ax.add_patch(mpatches.Ellipse((Acx, Acy), SHO * s, DEP * s, fc=GREEN, ec="#16613a",
                                  lw=1.3, alpha=0.40, zorder=7))
    ax.text(Acx, Acy, f"operator\n~{SHO}×{DEP}\nfits the bore", fontsize=6.8, color="#16613a",
            **FONT, ha="center", va="center", zorder=8)
    ax.text(Acx, Acy + Rd + 22, "INTERIOR / walkway (exit)", fontsize=7.5, color=GREEN,
            **FONT, fontweight="bold", ha="center")

    # ── VERDICT box (top-right) ──
    v_x, v_y, v_w, v_h = 900, 900, 1200, 300
    ax.add_patch(mpatches.FancyBboxPatch((v_x, v_y), v_w, v_h,
                                         boxstyle="round,pad=6,rounding_size=12",
                                         fc="#EAF6EE", ec=GREEN, lw=1.6, zorder=2))
    ax.text(v_x + 20, v_y + v_h - 22, "VERDICT  ✓  PASS — no daylight path at any rotation", ha="left",
            va="center", fontsize=12.5, fontweight="bold", color=GREEN, **FONT)
    for i, line in enumerate([
        "The two housing openings are 80° wide and 180° apart, so the 80° drum opening can",
        "never reach both at once. The housing's solid wall always covers the opening the drum",
        "isn't aligned with — light enters the bore but never exits to the interior. A fixed",
        "housing (the seal is the housing geometry, not the panel aperture) does the work.",
    ]):
        ax.text(v_x + 20, v_y + v_h - 72 - i * 44, line, ha="left", va="center", fontsize=8, color="#16361f", **FONT)

    # ── PANEL B — light-tight at every rotation ──
    ax.text(-110, 588, "B.  LIGHT-TIGHT AT EVERY ROTATION", ha="left", fontsize=12,
            fontweight="bold", color=C_OUT, **FONT)
    Bcy, bs = 340, 0.52
    Rd, ORd = HR * bs, DR * bs
    for bx, (da, ttl, desc) in zip(
            [370, 1090, 1810],
            [(270, "1 · ENTER", "exterior open; interior\ncovered by drum →\nlight enters bore, no exit"),
             (0,   "2 · TRANSIT", "drum opening at the side;\nboth openings covered →\nfully sealed"),
             (90,  "3 · EXIT", "interior open to walkway;\nexterior covered by drum →\nno daylight enters")]):
        zones(bx, Bcy, Rd + 58)
        arc(bx, Bcy, Rd, [(90, OD), (270, OD)], 5, HOUS, 5)
        arc(bx, Bcy, ORd, [(da, OD)], 4, DRUMC, 6)
        sun(bx - Rd - 30, Bcy - Rd * 0.5)
        ax.text(bx, Bcy + Rd + 60, ttl, ha="center", fontsize=9.5, fontweight="bold", color=GREEN, **FONT)
        ax.text(bx, Bcy - Rd - 48, desc, ha="center", va="top", fontsize=7, color=C_DIM, **FONT)
        if da == 270:
            ax.annotate("", xy=(bx, Bcy + ORd * 0.92), xytext=(bx, Bcy - Rd - 24),
                        arrowprops=dict(arrowstyle="-|>", color=AMBER, lw=2.0), zorder=9)
            ax.plot([bx], [Bcy + ORd], marker="x", ms=9, mew=2.4, color=GREEN, zorder=10)
        else:
            ax.annotate("", xy=(bx, Bcy - ORd * 0.92), xytext=(bx, Bcy - Rd - 24),
                        arrowprops=dict(arrowstyle="-|>", color=AMBER, lw=2.0), zorder=9)
            ax.plot([bx], [Bcy - ORd], marker="x", ms=9, mew=2.4, color=GREEN, zorder=10)

    # ── PANEL C — running-gap + axial-end seals (detail carried from the seal study) ──
    ax.plot([-130, 2130], [-30, -30], color=C_DIM, lw=1.0, ls=(0, (6, 4)), zorder=3)
    ax.text(-110, -100, "C.  RUNNING-GAP + AXIAL-END SEALS", ha="left", fontsize=12,
            fontweight="bold", color=C_OUT, **FONT)

    lz = -180
    keys = [(HOUS, "FIXED HOUSING (outer)", 6.0),
            (DRUMC, "ROTATING DRUM (inner)", 5.0),
            ("#4A4A4A", f"WIPER STRIP ×{LT_WIPER_N} (on drum)", 3.4),
            (AMBER, "LIGHT PATH (ray)", 2.0)]
    lx = -80
    for col, lab, w in keys:
        ax.plot([lx, lx + 70], [lz, lz], color=col, lw=w, zorder=9)
        ax.text(lx + 85, lz, lab, ha="left", va="center", fontsize=7.5, color=C_OUT, **FONT, zorder=9)
        lx += 560

    ax.text(1815, -640,
            "SEAL CROSS-SECTIONS\n\nrunning-gap brush (radial)\n→ SHEET 4 HOLDER PROFILE\n\ntop-end neoprene (axial)\n→ SHEET 12 (drawn 1.5:1)",
            ha="center", va="center", fontsize=9, color=TITLE_COL, fontweight="bold",
            **FONT, zorder=9,
            bbox=dict(boxstyle="round,pad=0.9", fc="#EEF3F8", ec=C_OUT, lw=1.4))

    notes = [
        "SEALS & LIGHT-PATH",
        "Amber rays = the light path — daylight enters an aligned opening and is stopped by the drum's opaque wall before it can reach the far opening; at mid-rotation both openings are blocked at entry.",
        f"Running-gap wiper: {LT_WIPER_N}× vertical #4 (3/16\") strip brushes (0.008\" BLACK nylon, {LT_WIPER_TRIM:.1f}mm trim) snapped into anodized-Al straight-flange holders FLANGE-RIVETED to the rotating drum OD at {LT_WIPER_SPACING:.0f}° spacing (Ø{LT_RIVET_D} blind rivets, McMaster 97447A015) — the rivets land in the aluminum flange, clear of the brush; bristles lay over onto the fixed housing bore across the {RUN_GAP:.0f}mm gap. 96\" stock → each line is ONE continuous piece over the full drum height (no joint).",
        f"Strip count: {LT_WIPER_SPACING:.0f}° spacing ≤ the {int(round(180 - LT_OPENING_DEG))}° housing material arc, so ≥1 strip always sits in each arc between the openings at every rotation → the annular gap can never carry light EXT↔INT.",
        "Top + bottom axial ends: 12mm closed-cell neoprene wiper strips (rotating drum cap ↔ fixed frame plate) + silicone bead CAP the running gap so a ray can't bypass the brushes over the top/bottom — SEE SHEET 12 for the enlarged top-end seal cross-section. The brushes seal the gap circumferentially; the neoprene seals it axially.",
        f"Light-tight by geometry: each opening {LT_OPENING_DEG}° (<90°); the drum's {LT_SHELL_ARC}° wall bridges the two 180°-apart housing openings at every rotation. Interior flat-black; residual scatter killed at the matte wall. ALL DIMS IN mm.",
    ]
    draw_notes(ax, notes, -80, -280, 34, fs=7, font=FONT, width=1470, wrap=80,
               title_color=TITLE_COL)

    title_block(ax, "SHEET 7 OF 12", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="LIGHT-LOCK VERIFICATION — ACCESS · LIGHT-PATH · SEALS",
                scale_note="PLAN VIEWS · NOT TO SCALE · ALL DIMS IN mm",
                doc_id="TBS-001 · Revolving Light-Trap",
                height=0.045, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet7.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet7.png saved")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 8 — Support frame, general arrangement
# The integrated steel welded box cage (part of the swing-panel frame) that carries
# both SKF 6215 bearings + the fixed housing. ELEVATION (left) + PLAN (top-right).
# ═════════════════════════════════════════════════════════════════════════════
def draw_sheet8():
    CX, CY, HR = DRUM_CX, DRUM_CY, LT_HOUSING_R
    Z_DBOT, Z_DTOP = PANEL_FLOOR_GAP, DRUM_H_LT            # drum extent (shell + caps)
    Z_CBOT, Z_CTOP = LT_CAGE_BOT, LT_CAGE_TOP              # cage: posts + top/bottom axle beams
    Z_HBOT, Z_HTOP = LT_HOUSING_Z_BOT, LT_HOUSING_Z_TOP    # fixed housing skin (spans beam-to-beam)
    RHS = LT_FRAME_RHS
    cx0, cx1, cyl, cyr = DRUM_CAGE_X0, DRUM_CAGE_X1, DRUM_CAGE_YD_L, DRUM_CAGE_YD_R
    cW_x, cW_y, cH = cx1 - cx0, cyr - cyl, Z_CTOP - Z_CBOT
    PLd = LT_FRAME_PLATE_T * 3          # plate draw thickness (exaggerated)

    # View placements (generic fig units, mm-scaled)
    EX, EZ = 0, 0                        # ELEVATION origin (Yd→x, Z→z)
    PX, PZ = cW_y + 780, cH - cW_y       # PLAN origin (X→x, Yd→z), top-right

    def fe(yd, z):   # elevation map
        return (EX + (yd - cyl), EZ + (z - Z_CBOT))

    def fp(x, yd):   # plan map
        return (PX + (x - cx0), PZ + (yd - cyl))

    X_LO, X_HI = -560, PX + cW_x + 360
    Z_LO, Z_HI = -1180, cH + 300                    # extra bottom room: wrapped notes clear the title block
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
    ax.text(*fe(cyl + cW_y / 2, Z_CTOP + 170), s="ELEVATION — LOOKING ALONG DRUM AXIS DEPTH",
            ha="center", va="bottom", fontsize=8.5, color=TITLE_COL, fontweight="bold",
            **FONT, zorder=15)
    BH = LT_AXLE_BEAM_H
    # housing skin (outer light-seal) — spans BEAM-to-BEAM, past the drum caps
    for yd in (CY - HR, CY + HR - LT_HOUSING_T):
        rrect(fe(yd, Z_HBOT), LT_HOUSING_T, Z_HTOP - Z_HBOT, fc="#DDE4EC", lw=1.2, zorder=5)
    # drum shell inside — spans the FULL drum height so its inner face laps to both caps (no gap)
    for yd in (CY - LT_DRUM_OR, CY + LT_DRUM_OR - LT_DRUM_T):
        rrect(fe(yd, Z_DBOT), LT_DRUM_T, Z_DTOP - Z_DBOT, fc=C_LT_DRUM, lw=1.0, zorder=5)
    # drum caps (Al) — top + bottom. Drawn to the shell INNER face (the cap nests inside the shell
    # + rim-angle lap) so the cap edge sits flush with the drum inner wall — no phantom gap in the GA.
    cap_w = 2 * (LT_DRUM_OR - LT_DRUM_T)
    for zc in (Z_DTOP - LT_CAP_TOP_T, Z_DBOT):
        rrect(fe(CY - cap_w / 2, zc), cap_w, LT_CAP_TOP_T, fc=C_ALUM, lw=1.0, zorder=6)
    # top + bottom AXLE-SUPPORT BEAMS (50×50 RHS, span Yd) — CLEAR of the drum caps
    rrect(fe(cyl, Z_CTOP - BH), cW_y, BH, fc=C_STEEL, lw=1.4, zorder=7)
    rrect(fe(cyl, Z_CBOT), cW_y, BH, fc=C_STEEL, lw=1.4, zorder=7)
    # bearing MOUNT PLATES (Ø240 steel) — the Ø240 ring/collar bolt to THESE, welded across
    # the 50mm beam (the Ø200 bolt circle is far wider than the beam → only 2/6 would hit it).
    for zp in (LT_TBEAM_Z0 - LT_BRG_PLATE_T, LT_BBEAM_Z1):
        rrect(fe(CY - LT_BRG_PLATE_OD / 2, zp), LT_BRG_PLATE_OD, LT_BRG_PLATE_T, fc="#9AA0A8", lw=1.3, zorder=8)
    # 4 corner posts → in elevation the front/back pairs overlap: 2 vertical RHS
    for yd in (cyl, cyr - RHS):
        rrect(fe(yd, Z_CBOT), RHS, cH, fc=C_STEEL, lw=1.4, zorder=4)
    # FILLET WELDS (typ.) at every post↔beam joint — red triangles in the re-entrant corners
    ws = 16
    for yd, s in ((cyl + RHS, 1), (cyr - RHS, -1)):
        for zbw, zdir in ((Z_CTOP - BH, -1), (Z_CBOT + BH, 1)):
            px, pz = fe(yd, zbw)
            ax.add_patch(mpatches.Polygon([(px, pz), (px + s * ws, pz), (px, pz + zdir * ws)],
                                          closed=True, fc="#CC4422", ec="#CC4422", zorder=10))
    # fillet welds — each Ø240 mount plate to its beam (steel↔steel, at both Yd edges of the plate)
    for yw, sw in ((CY - LT_BRG_PLATE_OD / 2, -1), (CY + LT_BRG_PLATE_OD / 2, 1)):
        for zj, zdir in ((LT_TBEAM_Z0, -1), (LT_BBEAM_Z1, 1)):
            px, pz = fe(yw, zj)
            ax.add_patch(mpatches.Polygon([(px, pz), (px + sw * ws, pz), (px, pz + zdir * ws)],
                                          closed=True, fc="#CC4422", ec="#CC4422", zorder=10))
    # bearings on the axis: UPPER hangs BELOW the top beam (drum suspended), LOWER sits ABOVE
    # the bottom beam (floating). Each is offset from its cap by the stub-shaft standoff.
    z_ubrg = Z_DTOP + LT_BRG_STANDOFF        # upper bearing bottom — above the top cap, below the top beam
    z_lbrg = Z_DBOT - SKF6215_W              # lower bearing bottom — below the bottom cap, above the bottom beam
    # bearing-seat RING (upper, isolated Al) / COLLAR (lower, steel) — Ø240, seats the SKF 6215 and
    # bolts up/down to the mount plate (matches the Sheet 1/5 hub); drawn BEHIND the bearing.
    rrect(fe(CY - LT_TOPRING_OD / 2, z_ubrg), LT_TOPRING_OD, SKF6215_W, fc=C_ALUM, lw=1.0, zorder=6)
    rrect(fe(CY - LT_COLLAR_OD / 2, z_lbrg), LT_COLLAR_OD, SKF6215_W, fc=C_STEEL, lw=1.0, zorder=6)
    for z_brg in (z_ubrg, z_lbrg):
        rrect(fe(CY - SKF6215_OD / 2, z_brg), SKF6215_OD, SKF6215_W, fc="#B0B0B8", lw=1.2, zorder=8)
        rrect(fe(CY - SKF6215_ID / 2, z_brg), SKF6215_ID, SKF6215_W, fc="white", lw=0.8, zorder=9)
    # Ø160 steel stub-shaft FLANGE on each cap (bolted 4×M10) → the Ø75 shaft rises FROM the flange
    # (matches the Sheet 5/6 hub — cap → flange → shaft, NOT cap → shaft).
    _FL = 15
    rrect(fe(CY - 80, Z_DTOP), 160, _FL, fc="#9AA0A8", lw=1.0, zorder=7)                   # top flange 2100..2115
    rrect(fe(CY - 80, Z_DBOT - _FL), 160, _FL, fc="#9AA0A8", lw=1.0, zorder=7)             # bottom flange 115..130
    # stub shafts on the axis (flange → bearing; the bearing decouples them from the fixed beam)
    rrect(fe(CY - SKF6215_ID / 2, Z_DTOP + _FL), SKF6215_ID, (z_ubrg + SKF6215_W) - (Z_DTOP + _FL), fc="#9BA0A8", lw=0.8, zorder=7)
    rrect(fe(CY - SKF6215_ID / 2, z_lbrg), SKF6215_ID, (Z_DBOT - _FL) - z_lbrg, fc="#9BA0A8", lw=0.8, zorder=7)
    draw_cl_v(ax, fe(CY, 0)[0], fe(CY, Z_CBOT)[1] - 80, fe(CY, Z_CTOP)[1] + 80)
    # panel-rail tie context (ghost above/below the cage)
    for z0 in (Z_CTOP + 6, Z_CBOT - 55):
        rrect(fe(cyl - 90, z0), cW_y + 180, 50, fc="#EDEDED", lw=0.8, zorder=2)
    # elevation dims + labels
    draw_dim_v(ax, fe(cyl, 0)[0] - 90, fe(cyl, Z_CBOT)[1], fe(cyl, Z_CTOP)[1],
               f"{cH}mm POST H", offset=70, fs=7, font=FONT)
    draw_dim_v(ax, fe(cyr, 0)[0] + 70, fe(cyr, Z_DBOT)[1], fe(cyr, Z_DTOP)[1],
               f"{Z_DTOP - Z_DBOT}mm DRUM", offset=44, fs=6.6, right=True, font=FONT)
    draw_dim_h(ax, fe(cyl, 0)[0], fe(cyr, 0)[0], fe(0, Z_CTOP)[1] + 90,
               f"{LT_AXLE_BEAM_SPAN}mm BEAM SPAN (Yd)", offset=60, fs=7, font=FONT)
    leader(ax, *fe(cyr - RHS / 2, Z_CTOP * 0.62), *fe(cyr + 130, Z_CTOP * 0.66),
           f"CORNER POST\n{RHS}×{RHS}×{LT_FRAME_T} RHS (×4)\nwelded into panel rails",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, *fe(cyl + 150, Z_CTOP - BH / 2), *fe(cyl - 80, Z_CTOP + 110),
           f"TOP AXLE BEAM {LT_AXLE_BEAM_H}×{LT_AXLE_BEAM_W}×{LT_AXLE_BEAM_T} RHS\nCLEAR above the cap — bearing hangs below (drum hangs from it)",
           fs=6.5, color=C_OUT, ha="right", arrow_style="->", font=FONT)
    leader(ax, *fe(cyl + 150, Z_CBOT + BH / 2), *fe(cyl - 80, Z_CBOT - 130),
           f"BOTTOM AXLE BEAM {LT_AXLE_BEAM_H}×{LT_AXLE_BEAM_W} RHS\n+ floor anchor (lower bearing sits above it)",
           fs=6.5, color=C_OUT, ha="right", arrow_style="->", font=FONT)
    leader(ax, *fe(CY + SKF6215_OD / 2, z_ubrg + SKF6215_W / 2),
           *fe(CY + 370, z_ubrg + 220), "SKF 6215 ×2\n(upper hangs below top beam;\nlower floats above bottom beam)", fs=6.5,
           color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, *fe(CY - LT_BRG_PLATE_OD / 2, LT_TBEAM_Z0 - LT_BRG_PLATE_T / 2),
           *fe(cyl - 80, Z_CTOP * 0.80), f"BEARING MOUNT PLATE Ø{LT_BRG_PLATE_OD}×{LT_BRG_PLATE_T}\nwelded across the beam — ring bolts to THIS\n(Ø200 bolt circle » 50mm beam)", fs=6.3,
           color=C_OUT, ha="right", arrow_style="->", font=FONT)
    leader(ax, *fe(CY - HR + LT_HOUSING_T, Z_DTOP * 0.4), *fe(cyl - 80, Z_DTOP * 0.34),
           f"FIXED HOUSING Ø{DRUM_D}\n(outer skin, beam-to-beam — Sheet 9)", fs=6.5, color=C_OUT,
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
    # 4 corner posts — CUT cross-section (looking down the vertical RHS) → drawn HOLLOW
    for xx in (cx0, cx1 - RHS):
        for yy in (cyl, cyr - RHS):
            px, pz = fp(xx, yy)
            tube_rect(ax, px, pz, RHS, RHS, LT_FRAME_T, fc="#9BA0A8", lw=1.2, zorder=6)
    # AXLE BEAM — spans Yd at the drum axis X, central bearing at midspan
    rrect(fp(CX - LT_AXLE_BEAM_W / 2, cyl), LT_AXLE_BEAM_W, cW_y, fc=C_STEEL, lw=1.4, zorder=7)
    # FILLET WELDS (plan) — small red triangles at each member junction (fp-based, orientation-safe)
    wsp = 16

    def weld_tri(Xc, Ydc, Xd, Ydd):
        ax.add_patch(mpatches.Polygon([fp(Xc, Ydc), fp(Xc + Xd, Ydc), fp(Xc, Ydc + Ydd)],
                                      closed=True, fc="#CC4422", ec="#CC4422", zorder=10))
    for xx in (cx0, cx1 - RHS):                            # 4 corner posts ↔ rails
        sx = wsp if xx < CX else -wsp
        cX = xx + RHS if xx < CX else xx
        for yy in (cyl, cyr - RHS):
            sy = wsp if yy < CY else -wsp
            cY = yy + RHS if yy < CY else yy
            weld_tri(cX, cY, sx, sy)
    weld_tri(CX - LT_AXLE_BEAM_W / 2, cyl + RHS, LT_AXLE_BEAM_W, wsp)      # axle beam ↔ near rail
    weld_tri(CX - LT_AXLE_BEAM_W / 2, cyr - RHS, LT_AXLE_BEAM_W, -wsp)     # axle beam ↔ far rail
    draw_dim_h(ax, fp(CX - LT_AXLE_BEAM_W / 2, cyr)[0], fp(CX + LT_AXLE_BEAM_W / 2, cyr)[0],
               fp(0, cyr)[1] + 40, f"{LT_AXLE_BEAM_W}mm AXLE BEAM W (at drum axis X)",
               offset=45, fs=6.5, font=FONT)
    draw_circle(ax, hc[0], hc[1], SKF6215_OD / 2, lw=1.2, color=C_OUT, fill=True,
                fc="#B0B0B8", zorder=8)
    draw_circle(ax, hc[0], hc[1], SKF6215_ID / 2, lw=1.0, color="#CC4422", zorder=9)
    # aperture edges + opening labels. The 80° housing opening is drawn as a colored arc;
    # each free HDPE edge is capped by a bonded Al U-channel (slot grips the 5mm wall,
    # legs run into the material arc) — the stiffener that replaced the steel jamb posts.
    oh = LT_OPENING_DEG / 2
    AL_CH = "#5B6E8C"
    for oc, tag, col in ((180, "EXT", "#5060A0"), (0, "INT", "#407040")):
        a0, a1 = math.radians(oc - oh), math.radians(oc + oh)
        ts = [a0 + (a1 - a0) * k / 20 for k in range(21)]
        ax.plot([hc[0] + HR * math.cos(t) for t in ts], [hc[1] + HR * math.sin(t) for t in ts],
                color=col, lw=5.0, zorder=7)                        # 80° opening (aperture)
        for e, sgn in ((oc - oh, -1), (oc + oh, +1)):               # -1/+1 = tangent into the material arc
            a = math.radians(e)
            rx, ry, tx, ty = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
            ox, oy = hc[0] + HR * rx, hc[1] + HR * ry                            # outer edge face
            ix, iy = hc[0] + (HR - LT_HOUSING_T) * rx, hc[1] + (HR - LT_HOUSING_T) * ry  # inner face
            L = LT_EDGE_CHAN_LEG
            ax.plot([ox, ix], [oy, iy], color=AL_CH, lw=2.6, zorder=9)           # channel base (caps the cut edge)
            ax.plot([ox, ox + sgn * L * tx], [oy, oy + sgn * L * ty], color=AL_CH, lw=2.6, zorder=9)  # outer leg
            ax.plot([ix, ix + sgn * L * tx], [iy, iy + sgn * L * ty], color=AL_CH, lw=2.6, zorder=9)  # inner leg
            ax.plot([hc[0] + (HR - 46) * rx, hc[0] + (HR + 60) * rx],
                    [hc[1] + (HR - 46) * ry, hc[1] + (HR + 60) * ry],
                    color=col, lw=0.9, ls=":", zorder=7)            # opening edge
        ax.text(hc[0] + (HR + 86) * math.cos(math.radians(oc)),
                hc[1] + (HR + 86) * math.sin(math.radians(oc)), f"{tag}\nOPENING\n({LT_OPENING_DEG}°)",
                ha="center", va="center", fontsize=6.5, color=col, **FONT, zorder=9)
    # plan dims + labels
    draw_dim_h(ax, fp(cx0, cyl)[0], fp(cx1, cyl)[0], fp(0, cyl)[1] - 80,
               f"{cW_x}mm CAGE (X)", offset=55, fs=7, above=False, font=FONT)
    draw_dim_v(ax, fp(cx0, 0)[0] - 80, fp(cx0, cyl)[1], fp(cx0, cyr)[1],
               f"{cW_y}mm (Yd)", offset=55, fs=7, font=FONT)
    leader(ax, hc[0] + LT_AXLE_BEAM_W / 2, hc[1] + 120, fp(cx1, cyr)[0] + 70, fp(cx1, cyr)[1] - 270,
           f"AXLE BEAM {LT_AXLE_BEAM_H}×{LT_AXLE_BEAM_W} RHS\ncarries central SKF 6215 at midspan",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, *fp(cx0 + RHS / 2, cyr - RHS / 2), fp(cx0, cyr)[0] - 40, fp(cx0, cyr)[1] + 50,
           f"CORNER POST + PERIMETER RAILS\n{RHS}×{RHS}×{LT_FRAME_T} RHS welded box",
           fs=6.5, color=C_OUT, ha="right", arrow_style="->", font=FONT)
    leader(ax, hc[0] + HR * math.cos(math.radians(40)), hc[1] + HR * math.sin(math.radians(40)),
           fp(cx1, cyr)[0] + 20, fp(cx1, cyr)[1] + 55,
           f"Al EDGE CHANNEL {LT_EDGE_CHAN_W}×{LT_EDGE_CHAN_LEG}×{LT_EDGE_CHAN_T} U — bonded over each\nfree HDPE edge ({LT_EDGE_CHAN_N} total); ends bolt to\ntop/bottom beams — see Sheet 9",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)

    # ── RHS tube-section inset — the frame members are HOLLOW tube, not solid bar ──
    sxi, szi, SCi = PX + 70, 470, 1.8
    ax.text(sxi + 210, szi + LT_AXLE_BEAM_H * SCi + 66,
            "FRAME MEMBER (RHS) + BEARING MOUNT PLATE — cut sections:", ha="center", va="bottom",
            fontsize=8, color=TITLE_COL, fontweight="bold", **FONT, zorder=15)
    tube_rect(ax, sxi, szi, RHS * SCi, RHS * SCi, LT_FRAME_T * SCi, fc="#9BA0A8", lw=1.4, zorder=6)
    draw_dim_h(ax, sxi, sxi + RHS * SCi, szi - 26, f"{RHS}mm", offset=26, fs=6.2, above=False, font=FONT)
    draw_dim_v(ax, sxi - 26, szi, szi + RHS * SCi, f"{RHS}mm", offset=26, fs=6.2, font=FONT)
    ax.text(sxi + RHS * SCi / 2, szi + RHS * SCi + 18, f"{RHS}×{RHS}×{LT_FRAME_T} RHS\nposts · rails · axle beams",
            ha="center", va="bottom", fontsize=6.5, color=C_OUT, **FONT, zorder=9)
    ax.text(sxi + RHS * SCi + 26, szi + RHS * SCi / 2,
            f"wall {LT_FRAME_T}mm", ha="left", va="center", fontsize=6.2, color=C_DIM, **FONT, zorder=9)
    # BEARING MOUNT PLATE section (solid steel disc — the ring/collar bolt to it, not the beam)
    bxi = sxi + 540
    PSC = 0.9                                              # plate shown at a smaller scale (wide + thin)
    draw_rect(ax, bxi, szi, LT_BRG_PLATE_OD * PSC, LT_BRG_PLATE_T * SCi, fc=C_STEEL, lw=1.4, zorder=6)
    draw_dim_h(ax, bxi, bxi + LT_BRG_PLATE_OD * PSC, szi - 26, f"Ø{LT_BRG_PLATE_OD}", offset=26, fs=6.2, above=False, font=FONT)
    draw_dim_v(ax, bxi - 26, szi, szi + LT_BRG_PLATE_T * SCi, f"{LT_BRG_PLATE_T}mm", offset=26, fs=6.2, font=FONT)
    ax.text(bxi + LT_BRG_PLATE_OD * PSC / 2, szi + LT_BRG_PLATE_T * SCi + 18,
            f"Ø{LT_BRG_PLATE_OD}×{LT_BRG_PLATE_T} STEEL bearing mount plate (×2)\nwelded across the beam · ring/collar bolt to it", ha="center",
            va="bottom", fontsize=6.5, color=C_OUT, **FONT, zorder=9)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes = [
        "SUPPORT FRAME — INTEGRATED STEEL WELDED BOX CAGE (part of the swing-panel weldment)",
        f"Box: {RHS}×{RHS}×{LT_FRAME_T} steel RHS — 4 corner posts + perimeter rails (welded). No jamb posts: the free HDPE opening edges are stiffened by Al edge channels (below).",
        f"Axle beams: {LT_AXLE_BEAM_H}×{LT_AXLE_BEAM_W}×{LT_AXLE_BEAM_T} steel RHS (= the perimeter section — the 962mm span is barely stressed, δ≈0.3mm under the hung drum), span Yd ({LT_AXLE_BEAM_SPAN}mm) at the drum axis; carry the SKF 6215 at midspan (drum hangs from the top beam).",
        f"Bearing mount plate: Ø{LT_BRG_PLATE_OD}×{LT_BRG_PLATE_T} steel disc welded across each beam — the ring/collar bolt to THIS, not the beam wall (their Ø200 bolt circle is far wider than the 50mm beam). Seats: upper isolated 6061-T6 Al ring (Ø{LT_TOPRING_OD}, {LT_FRAME_MOUNT_BOLT_TOP}×M10); lower steel collar (Ø{LT_COLLAR_OD}, {LT_FRAME_MOUNT_BOLT_BOT}×M10).",
        f"Fixed housing (outer skin) laps + rivets to rim-angle on the top/bottom beams; free opening edges capped by {LT_EDGE_CHAN_N}× Al U-channel (ends bolt to the beams) — see Sheet 9. Drum rotates free inside.",
        "The cage is welded into the panel top/bottom rails → one structure, swings together. Panel frame owned by the hinged-panel report.",
        "WELDS (red triangles): 6mm fillet weld all-round at every member junction — each corner post to the top/bottom axle beams + perimeter rails, and the axle beam ends to the rails (typ., both views).",
        "ALL DIMS IN mm · plate thickness exaggerated for clarity",
    ]
    draw_notes(ax, notes, X_LO + 60, -300, 58, fs=7, font=FONT, width=2500, wrap=138,
               title_color=TITLE_COL)

    title_block(ax, "SHEET 8 OF 12", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="SUPPORT FRAME — GENERAL ARRANGEMENT (INTEGRATED STEEL CAGE)",
                scale_note="ALL DIMS IN mm", doc_id="TBS-001 · Revolving Light-Trap",
                height=0.045, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet8.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet8.png saved")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 9 — Housing → frame attachment (outer-skin fixing)
# The fixed housing (5mm) laps a rolled rim-angle blind-riveted to the frame; SS rivets +
# DP8010. Section + Detail B (opening-edge Al U-channel) + plan (200° housing, two 100° arcs).
# ═════════════════════════════════════════════════════════════════════════════
def draw_sheet9():
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
    _fw = S * LT_FRAME_T                                                           # frame-beam wall (3mm RHS)
    draw_rect(ax, -RIML - 40, 0, RIML + 100, BEAMH, fc=C_STEEL, lw=1.6, zorder=4)  # frame beam — bottom wall (rim welds here)
    draw_rect(ax, -RIML - 40, _fw, RIML + 100, BEAMH - _fw, fc=BG, lw=0.9, zorder=5)  # HOLLOW bore (void) above the wall
    for xx in (-RIML - 20, -RIML + 20, -RIML + 60):                              # break line (hollow beam continues up)
        ax.plot([xx - 4, xx + 4], [BEAMH - 8, BEAMH + 8], color=C_OUT, lw=0.6, zorder=7)
    # rim-angle — ONE continuous 25×25×3 L-section (single extrusion, not two plates): the
    # horizontal leg is BLIND-RIVETED up into the beam bottom wall; the standing lip hangs down for the housing to lap.
    l_angle(ax, 0, 0, -RIML, -LIP, LEGT, fc=C_ALUM, lw=1.4, zorder=5)             # rim-angle (L)
    # SS blind rivet (18-8, Ø1/8", McMaster 97525A425 — same family as the lap rivets): set from BELOW
    # through the flat leg + the 3mm beam bottom wall; the set head forms INSIDE the closed RHS bore (no
    # internal access, unlike a weld-nut; bears on the full wall, unlike a self-driller's ~2 threads).
    _tx = -RIML * 0.5
    blind_rivet(ax, _tx, (-LEGT + _fw) / 2, -90, LEGT + _fw, d=RVD)
    draw_rect(ax, 0, -LIP, DPT, LIP, fc=C_GASKT, lw=0.8, zorder=5)                # DP8010 bead
    draw_rect(ax, DPT, -LIP - 90, HOUT, LIP + 90, fc="#DDE4EC", lw=1.6, zorder=6)  # housing laps down, butts beam underside (broken below)
    for zz in (-LIP - 55, -LIP - 67, -LIP - 79):                                 # break line (housing continues down)
        ax.plot([DPT - 3, DPT + HOUT + 3], [zz - 4, zz + 4], color=C_OUT, lw=0.6, zorder=7)
    blind_rivet(ax, (DPT + HOUT - LEGT) / 2, -LIP / 2, 0, S * (LT_HOUSING_T + 1 + LT_RIM_T), d=RVD)  # radial housing → lip rivet
    draw_dim_v(ax, DPT + HOUT + 40, -LIP, 0, f"{LT_LAP_H}mm LAP", offset=40, fs=6.5, right=True, font=FONT)
    draw_dim_h(ax, DPT, DPT + HOUT, -LIP - 40, f"{LT_HOUSING_T}mm HOUSING", offset=48, fs=6.2,
               above=True, font=FONT)
    leader(ax, -RIML * 0.5, -LEGT, -150, -LIP + 90, "RIM ANGLE 25×25×3 6061-T6 Al — flat leg\nBLIND-RIVETED up into the beam bottom wall\n(Ø1/8\" 18-8 SS, 97525A425, Al→3mm steel, @ ~150mm)",
           fs=6.5, color=C_OUT, ha="right", arrow_style="->", font=FONT)
    leader(ax, DPT + HOUT, -LIP + 30, 125, -255, f"FIXED HOUSING {LT_HOUSING_T}mm UV-HDPE\nlaps {LT_LAP_H}mm over the lip",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, (DPT + HOUT - LEGT) / 2, -LIP / 2, 125, -135, f"SS Ø{LT_RIVET_D} BLIND RIVET (radial, low-profile head)\nthrough housing + lip · + DP8010 (light seal)",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, -RIML + 40, BEAMH / 2, -150, BEAMH + 40, "FRAME TOP BEAM / RAIL (steel · Sheet 8)",
           fs=6.5, color=C_OUT, ha="right", arrow_style="->", font=FONT)
    ax.text(150, -LIP - 130, "(bottom edge identical, mirrored, to the bottom beam)",
            ha="center", va="center", fontsize=6.2, color=C_DIM, **FONT, zorder=9)
    sbx, sbz = -300, -LIP - 60                                                   # section scale bar (20mm)
    ax.plot([sbx, sbx + S * 20], [sbz, sbz], color=C_OUT, lw=1.4, zorder=8)
    for xt in (sbx, sbx + S * 10, sbx + S * 20):
        ax.plot([xt, xt], [sbz - 6, sbz + 6], color=C_OUT, lw=1.0, zorder=8)
    ax.text(sbx + S * 10, sbz - 13, "20 mm  (SECTION 7:1)", ha="center", va="top",
            fontsize=6, color=C_OUT, **FONT, zorder=8)

    # ── DETAIL B — free opening EDGE: Al U-channel over the HDPE (plan · 7:1) ──
    # Horizontal cut through a vertical opening edge: the shell runs in from the left
    # and is capped at the cut edge (right) by the bonded Al U-channel that replaced the
    # jamb post. Legs run back along the inner + outer faces; rivet through both + HDPE.
    dx, dz = 400, 55
    HT2 = S * LT_HOUSING_T                 # HDPE wall thickness in section
    LEG2 = S * LT_EDGE_CHAN_LEG            # channel leg length (over the faces)
    CT2 = S * LT_EDGE_CHAN_T               # channel wall
    WL = S * 30                            # length of shell shown (broken on the left)
    ax.text(dx - LEG2 / 2, dz + HT2 / 2 + CT2 + 48, "DETAIL B — OPENING EDGE  (plan · SCALE 7:1)",
            ha="center", va="bottom", fontsize=8.5, color=TITLE_COL, fontweight="bold",
            **FONT, zorder=15)
    draw_rect(ax, dx - WL, dz - HT2 / 2, WL, HT2, fc="#DDE4EC", lw=1.6, zorder=5)   # HDPE shell wall
    for xb in (dx - WL, dx - WL + 12, dx - WL + 24):                                # break (shell continues)
        ax.plot([xb - 4, xb + 4], [dz - HT2 / 2 - 4, dz + HT2 / 2 + 4], color=C_OUT, lw=0.6, zorder=7)
    draw_rect(ax, dx - 6, dz - HT2 / 2, 6, HT2, fc=C_GASKT, lw=0.6, zorder=6)       # DP8010 in the slot
    # U-channel — ONE continuous 20×18×3 U-section (single extrusion, not three plates): the
    # base caps the HDPE edge, the two legs run back over the inner + outer faces.
    ax.add_patch(mpatches.Polygon([
        (dx - LEG2, dz + HT2 / 2 + CT2), (dx + CT2, dz + HT2 / 2 + CT2),
        (dx + CT2, dz - HT2 / 2 - CT2), (dx - LEG2, dz - HT2 / 2 - CT2),
        (dx - LEG2, dz - HT2 / 2), (dx, dz - HT2 / 2),
        (dx, dz + HT2 / 2), (dx - LEG2, dz + HT2 / 2)],
        closed=True, fc=C_ALUM, ec=C_OUT, lw=1.4, zorder=6))                        # U-channel
    blind_rivet(ax, dx - LEG2 * 0.5, dz, 90, S * (2 * LT_EDGE_CHAN_T + LT_HOUSING_T), d=RVD)  # thru legs + HDPE
    draw_dim_h(ax, dx - LEG2, dx, dz - HT2 / 2 - CT2 - 30, f"{LT_EDGE_CHAN_LEG}mm LEG",
               offset=26, fs=6.0, above=False, font=FONT)
    leader(ax, dx - LEG2 * 0.35, dz - HT2 / 2 - CT2, dx - 20, dz - HT2 / 2 - CT2 - 64,
           f"Al U-CHANNEL {LT_EDGE_CHAN_W}×{LT_EDGE_CHAN_LEG}×{LT_EDGE_CHAN_T} 6063-T5 — bonded over the\n{LT_HOUSING_T}mm HDPE edge (DP8010); caps BOTH faces (jamb-post replacement)",
           fs=6.2, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, dx + CT2, dz + HT2 * 0.3, dx + CT2 + 64, dz + 40,
           f"Ø{LT_RIVET_D} SS BLIND RIVET (low-profile head)\nthru both legs + HDPE",
           fs=6.2, color=C_OUT, ha="left", arrow_style="->", font=FONT)

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
        "1. Rolled 25×25×3 6061-T6 Al rim-angle, radius R450, BLIND-RIVETED to the frame top + bottom beams (Ø1/8\" 18-8 SS blind rivets, McMaster 97525A425, Al flat leg → 3mm steel wall, ~150mm pitch; two 100° arcs — the openings have no rim). Set from below; the set head forms inside the closed RHS. No welds, no self-drillers — avoids welding Al to steel and thread-stripping the thin wall.",
        f"2. Housing laps {LT_LAP_H}mm over the standing lip; DP8010 bead in the lap (bond + light seal).",
        f"3. Drill Ø{LT_RIVET_HOLE:.1f} (#30), {LT_HOUSING_RIVET_N}× Ø{LT_RIVET_D} SS blind rivets per edge (McMaster 97525A435, low-profile head, ~{LT_RIVET_PITCH}mm pitch), wet in DP8010.",
        f"4. Free opening edges (no jamb posts): each of the {LT_EDGE_CHAN_N} vertical HDPE edges is capped by a bonded Al U-channel (DETAIL B) — Ø{LT_RIVET_D} SS blind rivets thru both legs + HDPE @ ~{LT_EDGE_CHAN_RIVET_PITCH}mm (grip ~{2 * LT_EDGE_CHAN_T + LT_HOUSING_T}mm), + DP8010; channel ends bolt to the top + bottom beams (1× M{LT_EDGE_CHAN_END_BOLT}/end via L-clip).",
        "SECTION A–A 7:1 (isotropic) · DETAIL B 7:1 · HOUSING PLAN 1:2 · fastener symbols schematic · ALL DIMS IN mm",
    ]
    draw_notes(ax, notes, X_LO + 60, -360, 24, fs=7, font=FONT, width=1450,
               title_color=TITLE_COL, wrap=180)

    title_block(ax, "SHEET 9 OF 12", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="HOUSING → FRAME ATTACHMENT (OUTER-SKIN FIXING)",
                scale_note="SECTION 7:1 · DETAIL B 7:1 · HOUSING PLAN 1:2 · ALL DIMS IN mm",
                doc_id="TBS-001 · Revolving Light-Trap", height=0.045, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet9.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet9.png saved")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 10 — Combined top-end assembly (radial half-section, drawn to scale · 100mm bar)
# One radial half-section at the TOP end showing BOTH joints nested concentrically:
#   inner ROTATING drum shell→cap lap joint (Sheet 4) + outer FIXED housing→frame
#   lap joint (Sheet 9), with the upper SKF 6215 bearing and the running-gap seal
#   between them — so the reader sees how the two combine at the same level.
# Axis on the LEFT (r = 0), radius increases to the right; z = height near the top.
# ═════════════════════════════════════════════════════════════════════════════
def draw_sheet10():
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
    DOR_ = LT_DRUM_OR                        # 382    drum shell outer
    HIR_ = LT_HOUSING_R - LT_HOUSING_T       # 445    housing inner
    HOR_ = LT_HOUSING_R                      # 450    housing outer
    bID, bOD, bW = SKF6215_ID / 2, SKF6215_OD / 2, SKF6215_W   # 37.5 / 65 / 25
    SHAFT_L = LT_STUB_SHAFT_L                 # Ø75 × 75 stub (shortened from 150 for ceiling clearance)
    Z_BRG0 = SHAFT_L - 20 - bW               # bearing bottom (bW wide, 20 below shaft top)
    Z_BEAM0 = SHAFT_L - 8                     # beam underside just below shaft top
    Z_BRK = -150                             # break-line level (drum/housing continue down)

    # ── Rotation axis (left edge, r = 0) ─────────────────────────────────────
    draw_cl_v(ax, 0, Z_BRK - 20, Z_BEAM0 + 130)
    ax.text(-10, Z_BEAM0 + 120, "DRUM\nAXIS", ha="right", va="top", fontsize=6.2,
            color=C_CL, **FONT, zorder=9)

    # ── FIXED: axle beam — HOLLOW RHS in longitudinal section (both walls solid, bore void) ─
    hollow_beam_long(ax, 0, Z_BEAM0, LT_AXLE_BEAM_SPAN / 2, LT_AXLE_BEAM_H,
                     LT_AXLE_BEAM_T, "bottom", fc=C_STEEL, lw=1.4, zorder=4, breaks=False,
                     open_ends=("left",))               # OPEN at the drum axis (tube continues to the other half)
    # ── FIXED: cage corner post — HOLLOW vertical RHS framing the beam end ────
    POST_R0 = LT_AXLE_BEAM_SPAN / 2                                          # 481 — beam outer end / cage corner
    hollow_beam_long(ax, POST_R0, Z_BRK, LT_FRAME_RHS, Z_BEAM0 + LT_AXLE_BEAM_H - Z_BRK,
                     LT_FRAME_T, "left", fc=C_STEEL, lw=1.4, zorder=3, breaks=False,
                     open_ends=("bottom",))             # OPEN at the bottom (post continues down full height)
    # ── Upper SKF 6215 bearing (to scale) + isolated Al ring + steel mount plate ─
    Z_PLATE0 = Z_BEAM0 - LT_BRG_PLATE_T                                             # mount-plate underside (welded under the beam)
    draw_rect(ax, bID, Z_PLATE0, LT_BRG_PLATE_OD / 2 - bID, LT_BRG_PLATE_T, fc=C_STEEL, lw=1.2, zorder=6)  # Ø240×12 steel mount plate (welded to beam)
    for wx in (LT_BRG_PLATE_OD / 2,):                                               # fillet weld plate↔beam (outer edge)
        ax.add_patch(mpatches.Polygon([(wx, Z_BEAM0), (wx - 6, Z_BEAM0), (wx, Z_BEAM0 - 6)], closed=True, fc="#CC4422", ec="#CC4422", zorder=8))
    draw_rect(ax, bOD, Z_BRG0, LT_TOPRING_OD / 2 - bOD, Z_PLATE0 - Z_BRG0, fc=C_ALUM, lw=1.0, zorder=5)  # Ø240 Al ring (bolts up to the plate)
    draw_rect(ax, bOD - 7.5, Z_BRG0, 7.5, bW, fc=C_STEEL, lw=0.8, zorder=6)         # outer race
    draw_rect(ax, bID, Z_BRG0, 7.5, bW, fc=C_STEEL, lw=0.8, zorder=6)               # inner race
    draw_circle(ax, (bID + bOD) / 2, Z_BRG0 + bW / 2, 8, lw=0.7, color=C_OUT,
                fill=True, fc="white", zorder=7)                                     # one ball (section)
    # ── ROTATING: stub shaft + bolted hub + cap ──────────────────────────────
    Z_STUB_TOP = Z_BEAM0 - 3                                                        # stub ends 3mm below the beam — no penetration
    draw_rect(ax, 0, -LT_CAP_TOP_T, bID, Z_STUB_TOP + LT_CAP_TOP_T, fc=C_STEEL, lw=1.0, zorder=5)  # 75Ø stub shaft (ends below beam)
    ax.plot([bID, bID + 8], [Z_BRG0 + bW + 4, Z_BRG0 + bW + 4], color=C_OUT, lw=0.9, zorder=8)  # circlip
    draw_rect(ax, 0, -LT_CAP_TOP_T, CAPR, LT_CAP_TOP_T, fc=C_ALUM, lw=1.2, zorder=5)  # 8mm Al cap disc
    draw_rect(ax, 0, 0, 80, 15, fc=C_STEEL, lw=1.0, zorder=6)                         # Ø160 steel stub-shaft flange (4×M10 tapped, Ø120 PCD)
    # ── Securing bolts (project convention) — each butts the faces it joins ─────
    # Ring → mount plate: CSK head on the RING BOTTOM, up through the ring, TAPPED into the solid
    # 12mm steel mount plate (welded across the beam) — no rivet-nut; the plate taps directly.
    rbx = LT_RING_BOLT_PCD / 2                                                        # Ø200 bolt circle — clear of the Ø160 flange
    wnz = Z_PLATE0 + LT_BRG_PLATE_T * 0.6                                             # tapped into the mount plate
    draw_bolt(ax, rbx, (Z_BRG0 + wnz) / 2, wnz - Z_BRG0, d=10, head=-1, end="tapped", csk=True)
    # Cap → flange: countersunk flush in the cap face, THROUGH the cap and THROUGH the full 15mm
    # flange (tapped all the way through — a through-drilled + tapped hole is simpler to make than a
    # blind partial-depth one; no nut, the flange is the thread). Bolt ends flush at the flange far face.
    cbx = 60                                                                          # Ø120 PCD — clear of the Ø75 shaft and the Ø160 flange edge
    cb0, cb1 = -LT_CAP_TOP_T, 15                                                       # cap top (CSK head) → flange bottom face (z=15)
    draw_bolt(ax, cbx, (cb0 + cb1) / 2, cb1 - cb0, d=10, head=-1, end="tapped", csk=True)
    leader(ax, rbx, wnz + 6, POST_R0 - 250, Z_BEAM0 + LT_AXLE_BEAM_H + 30,
           f"Al RING → MOUNT PLATE\n{LT_FRAME_MOUNT_BOLT_TOP}×M10 CSK TAPPED\n(Ø{LT_BRG_PLATE_OD}×{LT_BRG_PLATE_T} steel, welded to the beam)", fs=6.0, color=C_OUT,
           ha="right", arrow_style="->", font=FONT)
    leader(ax, cbx, -LT_CAP_TOP_T, -120, -LT_CAP_TOP_T - 45,
           "CAP → FLANGE\n4×M10 COUNTERSUNK into\nTAPPED flange (no nut)", fs=6.0, color=C_OUT, ha="left", arrow_style="->", font=FONT)

    # ── INNER joint — drum shell → cap lap (to scale; detail on Sheet 4) ─────
    l_angle(ax, CAPR, 0, -LT_RIM_LEG, LT_LAP_H, LT_RIM_T, fc=C_ALUM, lw=0.8, zorder=6)       # rim-angle (L) — flat leg on cap + lip up
    draw_rect(ax, DIR_, Z_BRK, LT_DRUM_T, LT_LAP_H - Z_BRK, fc=C_LT_DRUM, lw=1.0, zorder=7)  # drum shell (laps up, hangs down)
    blind_rivet(ax, (CAPR - LT_RIM_T + DOR_) / 2, LT_LAP_H / 2, 0,
                DOR_ - (CAPR - LT_RIM_T), d=LT_RIVET_D)                                       # RADIAL blind rivet (in-section, dome outboard)

    # ── Running gap (open here) — the seal is the 4 VERTICAL drum-OD strip brushes, which sit
    # BELOW the cap lap (not at this level); shown + detailed on Sheets 4 & 7, called out by the
    # leader below. (No horizontal seal element here — that was a stale felt-seal artifact.)

    # ── FIXED outer skin — housing + housing → frame lap (detail on Sheet 9) ─
    draw_rect(ax, HIR_, Z_BRK, LT_HOUSING_T, Z_BEAM0 - Z_BRK, fc="#DDE4EC", lw=1.0, zorder=6)  # housing wall
    l_angle(ax, HIR_, Z_BEAM0, -LT_RIM_LEG, -LT_LAP_H, LT_RIM_T, fc=C_ALUM, lw=0.8, zorder=7)  # rim-angle (L) — flat leg under beam + lip down
    blind_rivet(ax, (HIR_ - LT_RIM_T + HOR_) / 2, Z_BEAM0 - LT_LAP_H / 2, 0,
                HOR_ - (HIR_ - LT_RIM_T), d=LT_RIVET_D)                                       # RADIAL blind rivet (in-section, dome outboard)

    # break lines (drum + housing continue down to the floor) ─────────────────
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
    draw_dim_v(ax, -95, -LT_CAP_TOP_T, -LT_CAP_TOP_T + SHAFT_L, f"{SHAFT_L} STUB (Ø{SKF6215_ID})",
               offset=48, fs=6.5, font=FONT)
    draw_dim_h(ax, 0, CAPR, -LT_CAP_TOP_T - 60, f"Ø{LT_CAP_OD} CAP (radius)", offset=14,
               fs=6.5, above=False, font=FONT)
    # ── A/B rail positions — radial (dim_h) + vertical joint rise (dim_v) ────
    draw_dim_h(ax, 0, DOR_, -LT_CAP_TOP_T - 95, f"R{DOR_:.0f} — A: rotating drum rail (Ø{2 * LT_DRUM_OR})",
               offset=14, fs=6.0, above=False, font=FONT)
    draw_dim_h(ax, 0, HOR_, -LT_CAP_TOP_T - 135, f"R{HOR_:.0f} — B: fixed housing rail (Ø{DRUM_D})",
               offset=14, fs=6.0, above=False, font=FONT)
    draw_dim_v(ax, HOR_ + 65, LT_LAP_H / 2, Z_BEAM0 - LT_LAP_H / 2,
               f"{Z_BEAM0 - LT_LAP_H:.0f}mm — A→B joint rise\n(drum joint at cap · housing joint at beam)",
               offset=38, fs=6.0, right=True, font=FONT)
    draw_dim_h(ax, HOR_, POST_R0, -55, f"{POST_R0 - HOR_:.0f}mm — fixed housing outer skin → corner post",
               offset=32, fs=6.0, above=False, font=FONT)

    # ── Zone tags ────────────────────────────────────────────────────────────
    ax.text(210, -40, "◄ ROTATES WITH DRUM", ha="center", va="center", fontsize=7,
            color="#407040", fontweight="bold", **FONT, zorder=9)
    ax.text(300, Z_BEAM0 + LT_AXLE_BEAM_H + 10, "FIXED (FRAME + HOUSING) ►", ha="center", va="center", fontsize=7,
            color="#5060A0", fontweight="bold", **FONT, zorder=9)

    # ── Leaders ──────────────────────────────────────────────────────────────
    leader(ax, (bID + bOD) / 2, Z_BRG0 + bW / 2, 270, Z_BEAM0 + 30,
           "SKF 6215-2RS1 upper bearing\nin isolated Al ring, bolted to the axle beam (Sheet 5)",
           fs=6.5, color=C_OUT, ha="center", arrow_style="->", font=FONT)
    leader(ax, 30, 8, -20, -20, "Al CAP + BOLTED\nSTUB HUB (4×M10)", fs=6.5, color=C_OUT,
           ha="right", arrow_style="->", font=FONT)
    leader(ax, DOR_ + RUN_GAP / 2, LT_LAP_H / 2, 575, 55,
           f"RUNNING GAP {RUN_GAP}mm — {LT_WIPER_N}× #4 strip brushes in Al flange holders\nFLANGE-RIVETED to the ROTATING drum OD, bristles\n wiping the fixed bore (Sheets 4/7)",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, LT_AXLE_BEAM_SPAN / 2 - 60, Z_BEAM0 + LT_AXLE_BEAM_H / 2, 575, Z_BEAM0 + 120,
           f"AXLE BEAM {LT_AXLE_BEAM_H}×{LT_AXLE_BEAM_W} steel RHS — carries the central\nbearing + the fixed housing;\nswing-panel weldment (Sheet 8)",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, POST_R0 + LT_FRAME_RHS / 2, -35, 575, -35,
           f"CAGE CORNER POST {LT_FRAME_RHS}×{LT_FRAME_RHS}×{LT_FRAME_T} RHS\nframes the beam end · welded to the panel rails (Sheet 8)",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, HOR_, -110, 575, -130, f"FIXED HOUSING Ø{DRUM_D} (outer skin)\nrotating drum Ø{2 * LT_DRUM_OR} inside",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)

    notes = [
        "COMBINED TOP-END ASSEMBLY  (drawn to scale — see 100mm bar)",
        "The rotating drum (cap + shell on the stub shaft) hangs from the central bearing and turns inside the fixed housing; the two never touch — a brush-sealed running gap separates them (4× vertical #4 strip brushes on the drum OD, Sheets 4 & 7).",
        "INNER joint (rotating), DETAIL A: drum shell laps the cap rim-angle — SS blind rivets + DP8010; full detail on Sheet 4.",
        "OUTER joint (fixed), DETAIL B: housing laps a rim-angle blind-riveted to the axle beam (SS blind rivets both the rim→beam + the housing→rim laps) + DP8010; full detail on Sheet 9.",
        "The two joints sit at different heights (drum joint at the cap, housing joint at the beam) and on opposite walls of the running gap, so the rotating rivets always clear the fixed ones.",
        "Drum + housing continue below the break lines to the floor (drum interior ~1,970mm; housing skin ~2,060mm, beam-to-beam). Bottom end mirrors this, with the lower bearing in a welded steel floor collar (Sheet 5). ALL DIMS IN mm.",
    ]
    draw_notes(ax, notes, X_LO + 40, Z_BRK - 170, 14, fs=7, font=FONT, width=1000,
               title_color=TITLE_COL, wrap=200)

    title_block(ax, "SHEET 10 OF 12", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="COMBINED TOP-END ASSEMBLY (INNER + OUTER LAP JOINTS)",
                scale_note="HALF-SECTION · TO SCALE (100mm bar) · DETAILS A/B → SHEETS 4 & 9",
                doc_id="TBS-001 · Revolving Light-Trap", height=0.045, scale=0.72)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet10.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet10.png saved")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 11 — Pull-handle mount detail (to scale): stile → cap PLUG joint + handle
# ═════════════════════════════════════════════════════════════════════════════
def draw_sheet11():
    X_LO, X_HI, Z_LO, Z_HI = -120, 1240, -560, 320
    FIG_W = 15.0
    FIG_H = FIG_W * (Z_HI - Z_LO) / (X_HI - X_LO)
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DIAGRAM_DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Z_LO, Z_HI)
    ax.set_aspect("equal")
    ax.axis("off")
    STW = 40                                        # handle stile — 40×40×5 SS RHS

    # ══ VIEW A — STILE → CAP PLUG JOINT (section · SCALE 3:1) ═════════════════
    A = 3.0
    ax0, cz = 150, 120                              # joint x-center; cap-underside plane
    def AX(mm): return ax0 + A * mm
    def AZ(mm): return cz + A * mm
    ax.text(ax0, AZ(LT_CAP_TOP_T) + 52, "VIEW A — STILE → CAP PLUG JOINT  (section · 3:1)",
            ha="center", va="bottom", fontsize=8.5, color=TITLE_COL, fontweight="bold", **FONT, zorder=15)
    draw_rect(ax, AX(-43), AZ(0), A * 86, A * LT_CAP_TOP_T, fc=C_ALUM, lw=1.6, zorder=6)        # 8mm Al top cap
    sbot = -110
    draw_rect(ax, AX(-STW / 2), AZ(sbot), A * STW, A * (0 - sbot), fc=C_STEEL, lw=1.6, zorder=6)  # stile RHS (section)
    draw_rect(ax, AX(-STW / 2 + 5), AZ(sbot + 5), A * (STW - 10), A * (0 - sbot - 5), fc=BG, lw=0.8, zorder=7)  # bore
    draw_rect(ax, AX(-15), AZ(-40), A * 30, A * 40, fc="#9AA0A8", lw=1.4, zorder=8)             # solid steel plug (TAPPED)
    # cap bolt — COUNTERSUNK in the cap OUTSIDE face, DOWN through the cap, threading into the TAPPED
    # plug (driven from outside the cap = wrench-accessible; sealed for light-tightness).
    draw_bolt(ax, ax0, (AZ(LT_CAP_TOP_T) + AZ(-26)) / 2, AZ(LT_CAP_TOP_T) - AZ(-26),
              d=A * 10, head=1, end="tapped", csk=True, zb=10)
    for zc in (-16, -30):                           # 2× GRUB (set) screws through the 5mm wall, seating on the plug
        draw_rect(ax, AX(-STW / 2), AZ(zc) - A * 2.2, A * 8, A * 4.4, fc="#606068", lw=0.7, zorder=9)
        ax.plot([AX(-STW / 2), AX(-STW / 2)], [AZ(zc) - A * 1.6, AZ(zc) + A * 1.6], color=C_OUT, lw=1.4, zorder=10)  # socket end
    for zz in (sbot + 6, sbot + 12):                # break marks (stile continues down)
        ax.plot([AX(-STW / 2) + 5, AX(STW / 2) - 5], [AZ(zz) - 5, AZ(zz) + 5], color=C_OUT, lw=0.8, zorder=9)
    draw_dim_v(ax, AX(-43) - 34, AZ(0), AZ(LT_CAP_TOP_T), f"{LT_CAP_TOP_T:.0f}", offset=24, fs=6.0, font=FONT)
    draw_dim_h(ax, AX(-STW / 2), AX(STW / 2), AZ(sbot) - 38, f"{STW}", offset=28, fs=6.5, above=False, font=FONT)
    draw_dim_v(ax, AX(STW / 2) + 38, AZ(-40), AZ(0), "40", offset=24, fs=6.0, right=True, font=FONT)
    draw_dim_h(ax, AX(-15), AX(15), AZ(-40) - 34, "30", offset=26, fs=6.0, above=False, font=FONT)
    leader(ax, AX(30), AZ(4), AX(66) + 46, AZ(4) - 20, "TOP CAP — 8mm 6061-T6 Al", fs=6.5, color=C_DIM, ha="left", arrow_style="->", font=FONT)
    leader(ax, ax0, AZ(LT_CAP_TOP_T), AX(43) + 46, AZ(18),
           "M10 COUNTERSUNK BOLT — driven from the cap's OUTSIDE\nface (wrench-accessible), THROUGH the cap into the TAPPED\nplug; sealed (DP8010) for light-tightness",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, AX(6), AZ(-18), AX(43) + 46, AZ(-54),
           f"SOLID STEEL PLUG (TAPPED, ~30×30×40) fills the open\n{STW}×{STW}×5 RHS end + carries the cap-bolt thread.\nLoad path: handle → tube → grub screws → plug →\ncap bolt → cap",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, AX(-STW / 2), AZ(-16), AX(-43) - 34, AZ(-8),
           "2× M8 GRUB SCREWS\nthru wall → seat on plug\n(lock + anti-rotation)",
           fs=6.2, color=C_OUT, ha="right", arrow_style="->", font=FONT)
    leader(ax, AX(-STW / 2), AZ(sbot + 34), AX(-43) - 34, AZ(sbot + 78),
           f"STILE — {STW}×{STW}×5 SS RHS\n(spans cap → cap, ~2.1 m)", fs=6.5, color=C_OUT, ha="right", arrow_style="->", font=FONT)

    # ══ VIEW B — HANDLE ARRANGEMENT (interior elevation · SCALE 1:2) ══════════
    B = 0.55
    bx, bz = 980, 40                              # stile axis; grip midpoint
    def BX(mm): return bx + B * mm
    def BZ(mm): return bz + B * mm
    hd = GRAB_D
    ax.text(bx, BZ(GRAB_L / 2) + 74, "VIEW B — HANDLE ARRANGEMENT  (interior elevation · 1:2)",
            ha="center", va="bottom", fontsize=8.5, color=TITLE_COL, fontweight="bold", **FONT, zorder=15)
    draw_rect(ax, BX(-STW / 2), BZ(-GRAB_L / 2 - 70), B * STW, B * (GRAB_L + 140), fc=C_STEEL, lw=1.4, zorder=5)  # stile (elevation)
    for zz in (BZ(GRAB_L / 2 + 55), BZ(GRAB_L / 2 + 62), BZ(-GRAB_L / 2 - 55), BZ(-GRAB_L / 2 - 62)):  # break marks
        ax.plot([BX(-STW / 2) + 3, BX(STW / 2) - 3], [zz - 3, zz + 3], color=C_OUT, lw=0.6, zorder=8)

    def cap_bar(x0, z0, x1, z1):
        ang = math.atan2(z1 - z0, x1 - x0)
        nx, nz = -math.sin(ang) * B * hd / 2, math.cos(ang) * B * hd / 2
        ax.add_patch(mpatches.Polygon([(BX(x0) + nx, BZ(z0) + nz), (BX(x1) + nx, BZ(z1) + nz),
                                       (BX(x1) - nx, BZ(z1) - nz), (BX(x0) - nx, BZ(z0) - nz)],
                                      closed=True, fc="#C9CCD2", ec=C_OUT, lw=1.0, zorder=8))
        for cx0, cz0 in ((x0, z0), (x1, z1)):
            ax.add_patch(mpatches.Circle((BX(cx0), BZ(cz0)), B * hd / 2, fc="#C9CCD2", ec=C_OUT, lw=1.0, zorder=8))
    gxo = -GRAB_SO
    cap_bar(gxo, -GRAB_L / 2 + hd, gxo, GRAB_L / 2 - hd)          # grip (parallel to stile)
    cap_bar(gxo, -GRAB_L / 2 + hd, -STW / 2 - 4, -GRAB_L / 2)     # bottom arm
    cap_bar(gxo, GRAB_L / 2 - hd, -STW / 2 - 4, GRAB_L / 2)       # top arm
    for gz in (-GRAB_L / 2, GRAB_L / 2):                          # 2 feet, bolted to the stile via rivet-nuts in the hollow wall
        draw_rect(ax, BX(-STW / 2 - 6), BZ(gz - 16), B * 6, B * 32, fc=C_STEEL, lw=0.9, zorder=7)
        draw_bolt(ax, BX(-STW / 2 - 3), BZ(gz), B * 28, d=B * 6.35, vertical=False, head=-1, end="rivnut", wall=B * 5, csk=True, zb=9)
    draw_dim_v(ax, BX(gxo) - B * hd - 46, BZ(-GRAB_L / 2), BZ(GRAB_L / 2), f"{GRAB_L} HANDLE", offset=28, fs=6.5, font=FONT)
    draw_dim_h(ax, BX(gxo), BX(-STW / 2), BZ(-GRAB_L / 2) - 40, f"{GRAB_SO} STANDOFF", offset=26, fs=6.5, above=False, font=FONT)
    leader(ax, BX(gxo), BZ(GRAB_L / 4), BX(STW * 0.9), BZ(GRAB_L / 4 + 40),
           f"McMaster 1871A65 — Ø{GRAB_D:.1f} (0.5\") round pull\nhandle; bolted at both feet (2× 1/4\"-20 into\nRIVET-NUTS set in the hollow 5mm RHS wall)",
           fs=6.2, color=C_OUT, ha="left", arrow_style="->", font=FONT)

    # ══ Notes ═════════════════════════════════════════════════════════════════
    notes = [
        "PULL-HANDLE MOUNT  (interior face only — no fastener pierces the drum wall / no light leak)",
        f"1. Stile: {STW}×{STW}×5 SS RHS, spans + fastens between the two 8mm 6061-T6 Al caps (top + bottom ends identical).",
        "2. Each open RHS end takes a SOLID STEEL PLUG (~30×30×40), TAPPED, locked in the tube by 2× GRUB (set) screws through the wall — anti-rotation + retention; the open section gets a solid fastening body.",
        "3. A single M10 COUNTERSUNK bolt is driven from the cap's OUTSIDE face (wrench-accessible), THROUGH the cap into the tapped plug — sealed with DP8010 for light-tightness. Pull load path: handle → tube → grub screws → plug → cap bolt → cap (lands in the structural cap, not the thin HDPE wall).",
        "4. Off-the-shelf pull handle McMaster 1871A65 (Ø0.5\" bar, 308mm long, 52mm standoff) bolts at its two feet with 1/4\" screws tapped into the RHS wall. No welds anywhere.",
    ]
    draw_notes(ax, notes, X_LO + 40, -320, 20, fs=7, font=FONT, width=1160, wrap=120, title_color=TITLE_COL)

    title_block(ax, "SHEET 11 OF 12", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="PULL-HANDLE MOUNT — STILE → CAP PLUG JOINT + HANDLE ARRANGEMENT",
                scale_note="VIEW A 3:1 · VIEW B 1:2 · ALL DIMS IN mm",
                doc_id="TBS-001 · Revolving Light-Trap", height=0.045, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet11.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet11.png saved")


def draw_sheet12():
    # Top-end seal cross-section pulled off Sheet 7 and drawn large + schematic (radial gap
    # exaggerated) so the neoprene/brush seal path is easy to read; not a true single scale.
    X_LO, X_HI, Z_LO, Z_HI = 120, 1500, -360, 1000
    FIG_W = 15.0
    FIG_H = FIG_W * (Z_HI - Z_LO) / (X_HI - X_LO)
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DIAGRAM_DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(X_LO, X_HI)
    ax.set_ylim(Z_LO, Z_HI)
    ax.set_aspect("equal")
    ax.axis("off")
    S = 1.5

    # ══ TOP-END LIGHT PATH (axial section · 1.5:1) ═══════════════════════════
    # (the running-gap brush radial section lives on Sheet 4 — HOLDER PROFILE — so
    #  it is not duplicated here; this sheet is the axial top/bottom seal only.)
    otx, otz = 700, 560
    def TX(mm): return otx + S * mm
    def TZ(mm): return otz + S * mm
    ax.text(TX(0), TZ(230), "TOP-END LIGHT PATH  (axial section · schematic — radial gap exaggerated)\ngap CAPPED at top · cap ↔ frame neoprene seal · bottom identical",
            ha="center", va="bottom", fontsize=8.5, color=TITLE_COL, fontweight="bold", **FONT, zorder=15)
    draw_rect(ax, TX(-22), TZ(-175), S * 12, S * 205, fc=C_LT_DRUM, lw=1.2, zorder=5)   # drum shell (rotating)
    draw_rect(ax, TX(36), TZ(-175), S * 14, S * 235, fc="#DDE4EC", lw=1.2, zorder=5)    # housing wall (fixed)
    draw_rect(ax, TX(-120), TZ(6), S * 110, S * 22, fc=C_ALUM, lw=1.2, zorder=6)        # drum cap (rotating)
    draw_rect(ax, TX(-120), TZ(48), S * 196, S * 18, fc=C_STEEL, lw=1.4, zorder=6)      # frame top plate (fixed)
    draw_rect(ax, TX(-88), TZ(28), S * 122, S * 18, fc=C_GASKT, lw=1.0, zorder=7)       # neoprene wiper — caps the gap
    ax.plot([TX(-88), TX(34)], [TZ(28), TZ(28)], color="#8A5A2B", lw=2.6, zorder=8)     # PSA adhesive bond: neoprene → rotating drum cap
    ax.plot([TX(-40), TX(34)], [TZ(46), TZ(46)], color="#B03030", lw=1.4, ls=(0, (2, 2)), zorder=8)  # wiping contact: free edge sweeps the fixed frame plate
    # running-gap brush: holder BONDED to the drum's OUTER (gap-facing) surface and protruding INTO the
    # gap; bristles lay across the gap onto the fixed housing bore (circumferential seal — see Sheet 4).
    draw_rect(ax, TX(-10), TZ(-132), S * 6, S * 70, fc="#A8763A", lw=0.5, zorder=6)     # brush holder (bronze) on the drum OD
    for zz in range(-120, -66, 8):                                                      # bristles → fixed housing
        ax.plot([TX(-4), TX(32)], [TZ(zz), TZ(zz + 5)], color="#222", lw=0.6, zorder=6)
    ax.annotate("", xy=(TX(13), TZ(24)), xytext=(TX(13), TZ(-165)),                     # daylight ray UP the gap …
                arrowprops=dict(arrowstyle="-|>", color="#E8A800", lw=1.8), zorder=8)
    for s1, s2 in (((-11, 26), (11, 40)), ((-11, 40), (11, 26))):                       # … killed at the seal (red ✗)
        ax.plot([TX(13 + s1[0]), TX(13 + s2[0])], [TZ(s1[1]), TZ(s2[1])], color="#D33", lw=2.2, zorder=9)
    leader(ax, TX(4), TZ(37), TX(44), TZ(150),
           "NEOPRENE WIPER — PSA-backed strip BONDED to the\nrotating drum cap (brown) + silicone bead; its free\nedge sweeps the fixed frame plate — caps the gap",
           fs=6.3, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    ax.text(TX(82), TZ(57), "FRAME TOP PLATE (fixed)", ha="left", va="center", fontsize=6.5, color=C_DIM, **FONT, zorder=9)
    leader(ax, TX(-70), TZ(17), TX(-128), TZ(50), "DRUM CAP (rotating)", fs=6.5, color=C_DIM, ha="right", arrow_style="->", font=FONT)
    leader(ax, TX(43), TZ(-90), TX(120), TZ(-70), "HOUSING (fixed)", fs=6.5, color=C_DIM, ha="left", arrow_style="->", font=FONT)
    leader(ax, TX(-7), TZ(-95), TX(-55), TZ(-160), f"BRUSH + {RUN_GAP}mm gap\n(circumferential seal)", fs=6.5, color=C_DIM, ha="right", arrow_style="->", font=FONT)
    ax.text(TX(13), TZ(-195), "daylight ↑ the gap →\nBLOCKED at the top seal", ha="center", va="top",
            fontsize=6.5, color=C_OUT, **FONT, zorder=9)

    notes = [
        "TOP-END SEAL DETAIL  (enlarged from Sheet 7)",
        "Top + bottom axial ends: 12mm closed-cell neoprene wiper strips secured by their own PSA adhesive back (McMaster 93855K6) BONDED to the rotating drum cap face + a silicone bead along the seam; the strip's free edge sweeps the fixed frame plate. This CAPS the running gap so a ray can't bypass the brushes over the top/bottom. The neoprene seals the gap AXIALLY; together with the brushes (circumferential) there is no straight-through or over-the-top light path.",
        f"The running-gap brush radial section (the {LT_WIPER_N}× #4 strip brushes flange-riveted to the drum OD) is the HOLDER PROFILE inset on Sheet 4 — not duplicated here.",
        "NOT TO SCALE — the radial running gap is exaggerated so the seal path reads clearly (a true 13mm gap would be a hairline here); vertical members ≈ 1.5×. See Sheet 4 for the to-scale (7:1) holder profile and Sheet 7 for the rotation/light-path plans A–C.",
    ]
    draw_notes(ax, notes, X_LO + 40, 150, 20, fs=7, font=FONT, width=1200, wrap=118, title_color=TITLE_COL)

    title_block(ax, "SHEET 12 OF 12", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="SEAL DETAIL — TOP-END NEOPRENE (enlarged)",
                scale_note="SCHEMATIC (gap exaggerated) · ALL DIMS IN mm",
                doc_id="TBS-001 · Revolving Light-Trap", height=0.045, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet12.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet12.png saved")


def main():
    print("Generating TBS-001 Revolving Light-Trap blueprint sheets...")
    draw_sheet1()
    draw_sheet2()
    draw_sheet3()
    draw_sheet4()    # Sheet 4 — drum secure (shell → cap joint)
    draw_sheet5()       # Sheet 5 — bearing hub (assembly)
    draw_sheet6() # Sheet 6 — machined components (bearing seats + stub-shaft)
    draw_sheet7()          # Sheet 7 — seals & light-path
    draw_sheet8()          # Sheet 8 — support frame GA
    draw_sheet9()          # Sheet 9 — housing → frame attachment
    draw_sheet10()          # Sheet 10 — combined top-end assembly (inner + outer joints)
    draw_sheet11()          # Sheet 11 — pull-handle mount detail (to scale)
    draw_sheet12()          # Sheet 12 — seal details (enlarged from Sheet 7)
    print("Done.")


if __name__ == "__main__":
    main()
