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
    LT_EDGE_CHAN_W, LT_EDGE_CHAN_LEG, LT_EDGE_CHAN_T, LT_EDGE_CHAN_N,
    LT_EDGE_CHAN_RIVET_PITCH, LT_EDGE_CHAN_END_BOLT,
    LT_HOUSING_ARC, LT_HOUSING_RIVET_N,
    LT_WIPER_N, LT_WIPER_TRIM, LT_WIPER_SPACING, LT_WIPER_BACKING, LT_WIPER_HOLDER_W,
    DIAGRAM_DPI, DIAGRAMS_DIR,
)
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


def hollow_beam_long(ax, x, z, w, h, wall, near, *, fc=C_STEEL, lw=1.4, zorder=4, breaks=True):
    """RHS/SHS shown in LONGITUDINAL section (cut along its length) — the two walls the cut passes
    through read as solid bands, the bore between is void (BG). x,z = outer corner; w,h = drawn size;
    `wall` = wall thickness; `near` in {'bottom','top','left','right'} = which wall faces the viewer/joint
    (kept solid across its full length); the opposite wall is the far band. `breaks` adds end break-marks."""
    draw_rect(ax, x, z, w, h, fc=fc, lw=lw, zorder=zorder)                                   # outer (both walls)
    draw_rect(ax, x + wall, z + wall, w - 2 * wall, h - 2 * wall, fc=BG, lw=lw * 0.7, zorder=zorder + 1)  # hollow bore (void)
    if breaks:                                                                              # beam continues past the crop
        if near in ("bottom", "top"):
            for bx in (x, x + w):
                ax.plot([bx - 4, bx + 4, bx - 4], [z + wall, z + h / 2, z + h - wall],
                        color=C_OUT, lw=0.8, zorder=zorder + 3, solid_capstyle="round")
        else:
            for bz in (z, z + h):
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
    rect(-g, g, -d / 2, d / 2, fc=SHK, ec=C_OUT, lw=0.8, zorder=zb)                        # shank
    hu = -g if head < 0 else g                                                             # head end (outer face)
    if csk:                                               # flush countersunk flat head — tapers INTO the material
        into = 1 if head < 0 else -1                      # +axis into the joint for a head-below bolt
        cw = hw * 0.85
        pts = [pmap(hu, -cw / 2), pmap(hu, cw / 2),
               pmap(hu + into * hh * 1.4, d / 2), pmap(hu + into * hh * 1.4, -d / 2)]
        ax.add_patch(mpatches.Polygon(pts, closed=True, fc=HN, ec=C_OUT, lw=0.9, zorder=zb + 1))
    else:
        rect(hu - (hh if head < 0 else 0), hu + (0 if head < 0 else hh), -hw / 2, hw / 2,
             fc=HN, ec=C_OUT, lw=0.9, zorder=zb + 1)                                       # protruding hex head
    fu = g if head < 0 else -g                                                             # far (thread) end
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

    # ── End caps — metal hub discs (both 8mm 6061-T6 Al, identical) ──────────
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
           HO_R + 40, Z_TOP + 220,
           f"UPPER: {LT_CAP_TOP_T:.0f}mm 6061-T6 Al cap + BOLTED stub shaft →\n"
           f"SKF 6215-2RS1 (Ø{SKF6215_ID} bore) · isolated Al top ring, 6×M10",
           fs=6.5, color=C_OUT, ha="center", arrow_style="->", font=FONT)
    leader(ax, X_AX - SKF6215_OD / 2, Z_BOT + SKF6215_W / 2,
           X_LO + 250, Z_BOT - 20,
           f"LOWER: {LT_CAP_BOT_T:.0f}mm 6061-T6 Al cap + BOLTED stub shaft →\n"
           f"SKF 6215-2RS1 · welded steel floor collar, 8×M10",
           fs=6.5, color=C_OUT, ha="center", arrow_style="->", font=FONT)

    # ── Grab rail on a STEEL STILE spanning the two caps — the pull load goes into the
    # structural Al caps, NOT the thin HDPE drum wall. (interior side of the bore) ───
    STILE_W = 40
    stile_x = DI_R - STILE_W                                     # stile just off the interior wall
    draw_rect(ax, stile_x, Z_CAP_B, STILE_W, Z_CAP_T - Z_CAP_B, fc=C_STEEL, lw=1.2, zorder=6)   # handle stile (cap→cap)
    for zc, hd_ in ((Z_CAP_T, -1), (Z_CAP_B, 1)):                                               # stile-end plug + M12 → each cap
        draw_rect(ax, stile_x + 8, min(zc, zc + hd_ * 70), STILE_W - 16, 70, fc="#9AA0A8", lw=0.8, zorder=7)  # solid plug in tube end
        draw_bolt(ax, stile_x + STILE_W / 2, zc + hd_ * 22, 40, d=11, head=hd_, end="tapped", zb=8)           # M12 tapped into cap
    leader(ax, stile_x + STILE_W / 2, Z_CAP_T - 20, stile_x + 620, Z_CAP_T + 140,
           "STILE → CAP: M12 tapped into each Al cap via a\nsolid plug in the RHS end (1 top + 1 bottom) — see Sheet 11", fs=6.0, color=C_DIM,
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
        draw_bolt(ax, stile_x - 3, gz, 26, d=6.35, vertical=False, head=-1, end="tapped")        # foot → stile: 1/4" tapped
    leader(ax, GX - hd / 2, GRAB_Z + GRAB_L / 4, -110, GRAB_Z + 520,
           f"PULL HANDLE — off-the-shelf 12\" round pull handle (McMaster 1871A65, Ø0.5\" bar),\n1/4\" through-holes BOLTED (tapped) at both feet to a steel STILE ({STILE_W}×{STILE_W}×5 SS RHS)\nthat spans + bolts to the two Al caps — pull load into the caps · see MOUNT DETAIL",
           fs=6.5, color=C_OUT, ha="center", arrow_style="->", font=FONT)
    draw_dim_v(ax, GX - hd / 2 - 55, GZ0, GZ1, f"{GRAB_L}mm handle", offset=45, fs=6.5, font=FONT)
    draw_dim_h(ax, GX, stile_x, GZ1 + 75, f"{GRAB_SO}mm standoff", offset=45, fs=6.5, font=FONT)
    draw_dim_v(ax, GX - hd / 2 - 150, Z_CAP_B, GRAB_Z, f"{GRAB_Z - Z_CAP_B:.0f}mm\n(cap inner edge → grip CL)",
               offset=45, fs=6.5, font=FONT)

    # (The pull-handle mount detail — handle → stile → cap plug joint — is drawn to scale on its
    #  own Sheet 11; the GA above shows only the assembled arrangement + a reference.)
    ax.text(HO_R + 470, 900, "PULL-HANDLE MOUNT — see SHEET 11\n(handle → stile → cap · plug joint, to scale)",
            ha="center", va="center", fontsize=7.5, color=TITLE_COL, fontweight="bold", **FONT, zorder=15)

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

    title_block(ax, "SHEET 1 OF 11", drawing_title="REVOLVING LIGHT-TRAP",
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
    draw_notes(ax, notes, 40, -240, 34, fs=7, font=FONT, width=1650,
               title_color=TITLE_COL)

    title_block(ax, "SHEET 2 OF 11", drawing_title="REVOLVING LIGHT-TRAP",
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

    title_block(ax, "SHEET 3 OF 11", drawing_title="REVOLVING LIGHT-TRAP",
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
    draw_rect(ax, odx + HW, br_bot, CHAN, br_top - br_bot, fc="#8A8F98", lw=1.0, zorder=8)   # #4 channel backing
    for zz in range(int(br_bot) + 8, int(br_top), 8):                                        # bristles lay over into the gap
        ax.plot([odx + HW + CHAN, odx + HW + CHAN + S * 15], [zz, zz + 11], color="#333", lw=0.5, zorder=8)
    for zz in (-134, -126):                                                                  # break (shell + brush continue down)
        ax.plot([DPT - 3, odx + HW + CHAN + 3], [zz - 3, zz + 3], color=C_OUT, lw=0.6, zorder=9)
    leader(ax, odx + HW + CHAN + S * 6, br_top - 22, 250, -CAPT - 150,
           f"RUNNING-GAP BRUSH — #4 strip brush in an Al flange holder\n({LT_WIPER_N} strips on the drum OD, Sheet 7): starts clear BELOW\nthe cap lap so its flange rivets stagger past the shell→cap rivets",
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
    # flange → shell blind rivet (radial = UP; factory head on the flange/outside, bulb inside the drum)
    blind_rivet(ax, ix(-17), iz((HWmm - LT_DRUM_T) / 2), 90, IS * (LT_DRUM_T + HWmm), d=IS * LT_RIVET_D)
    draw_dim_v(ax, ix(-36), iz(0), iz(GAPmm), f"{GAPmm}mm GAP", offset=30, fs=6.2, font=FONT)
    leader(ax, ix(-17), iz(HWmm), ix(-20), iz(-LT_DRUM_T) - 44,
           "Al STRAIGHT-FLANGE HOLDER (anodized, 0.050\" wall)\nBLIND-RIVETED to the shell — rivet in the flange,\noffset from the brush (head out, bulb inside the drum)",
           fs=6.0, color=C_OUT, ha="center", arrow_style="->", font=FONT)
    leader(ax, ix(HWmm + CHmm / 2), iz(GAPmm), ix(30), iz(GAPmm) + 60,
           f"#4 STRIP BRUSH — 3/16\" channel,\n0.008\" BLACK nylon, {LT_WIPER_TRIM:.1f}mm trim", fs=6.0, color=C_OUT,
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

    title_block(ax, "SHEET 4 OF 11", drawing_title="REVOLVING LIGHT-TRAP",
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
        # stub shaft Ø75 — SHORT stub: it engages ONLY the bearing bore + is fixed axially by the two
        # circlips (bearing captive between them). It terminates just above the upper circlip, with a
        # designed 5mm AXIAL GAP to the beam — the rotating shaft never touches the fixed beam; the
        # circlips maintain that clearance. The bearing carries + locates the drum; load → ring bolts.
        z_stub = 15 * SC * s                           # shaft top: just above the upper circlip (13.5*SC)
        z_fl = -40 * SC * s
        draw_rect(ax, cx - rs, min(z_stub, z_fl), 2 * rs, abs(z_stub - z_fl),
                  fc=C_STEEL, lw=1.4, zorder=6)
        # bearing mount: isolated Al top ring (upper) / welded steel floor collar (lower). The ring
        # extends 5mm PAST the shaft top toward the beam (its beam-side face is the bolting datum), so
        # the shaft top is recessed inside the ring bore with a clear gap up to the beam.
        HRr = (100 if up else 105) * SC
        band(cx, ro, HRr, min(-18 * SC * s, 20 * SC * s), max(-18 * SC * s, 20 * SC * s),
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
        # axle beam — HOLLOW 100×50×3 RHS shown in LONGITUDINAL section: solid near + far 3mm
        # walls with the hollow bore VOID between them (white). It sits on the ring's beam-side face,
        # 5mm clear above the shaft top — the shaft never touches it (see the GAP dimension).
        zr0, zr1 = 20 * SC * s, 68 * SC * s
        _bz0, _bz1 = min(zr0, zr1), max(zr0, zr1)
        _bw = LT_FRAME_T * SC                                                # drawn wall thickness
        _bx0, _bwd = cx - 140 * SC, 280 * SC
        draw_rect(ax, _bx0, _bz0, _bwd, _bz1 - _bz0, fc=C_STEEL, lw=1.4, zorder=4)               # outer (walls)
        draw_rect(ax, _bx0, _bz0 + _bw, _bwd, (_bz1 - _bz0) - 2 * _bw, fc=BG, lw=1.0, zorder=5)  # HOLLOW bore (void)
        for _bx in (_bx0, _bx0 + _bwd):                                      # break marks — beam continues past crop
            ax.plot([_bx - 4, _bx + 4, _bx - 4], [_bz0 + _bw, (_bz0 + _bz1) / 2, _bz1 - _bw],
                    color=C_OUT, lw=0.8, zorder=7, solid_capstyle="round")
        # Al drum cap + bolted steel stub-shaft flange
        draw_rect(ax, cx - 110 * SC, min(zc0, zc1), 220 * SC, abs(zc1 - zc0),
                  fc=C_ALUM, lw=1.4, zorder=6)
        zf0, zf1 = -40 * SC * s, -55 * SC * s
        draw_rect(ax, cx - 80 * SC, min(zf0, zf1), 160 * SC, abs(zf1 - zf0),
                  fc=C_STEEL, lw=1.4, zorder=6)
        for g in (-1, 1):                          # cap → flange bolts (M10 countersunk, tapped, Ø120 PCD)
            fb0, fb1 = -40 * SC * s, zc1
            draw_bolt(ax, cx + g * 60 * SC, (fb0 + fb1) / 2, abs(fb1 - fb0),
                      d=8 * SC, head=int(-s), end="tapped", csk=True, zb=9)
        # ring/collar → beam bolts: HEAD on the ring's outer face (accessible), up through the
        # ring + the beam's near 3mm wall, into a RIVET-NUT (blind threaded insert) in that wall (the ring↔beam contact
        # face carries no fastener — the bolt clamps it, the thread is in the beam wall).
        for g in (-1, 1):
            ring_far = -18 * SC * s                    # ring face away from the beam (head bears here)
            wnz = 20 * SC * s                          # beam near wall face; the rivet-nut barrel spans the 3mm wall, head on the inner edge
            draw_bolt(ax, cx + g * 85 * SC, (ring_far + wnz) / 2, abs(wnz - ring_far),
                      d=8 * SC, head=int(-s), end="rivnut", wall=LT_FRAME_T * SC, csk=True, zb=9)
            for zc in (13.5 * SC, -13.5 * SC):     # circlip grooves — snug each side of the bearing (below the beam)
                ax.plot([cx + g * rs, cx + g * (rs - 5 * SC)], [zc, zc],
                        color=C_OUT, lw=1.6, zorder=9)
        # (Lower collar is BOLTED to the floor plate — 8× M10 into rivet-nuts, same as the upper
        #  ring; no weld. The ring→beam bolts above are the collar→plate connection.)
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
        (55 * SC,  (-100 * SC, 40 * SC),  "AXLE BEAM — 6×M10\ninto RIVET-NUTS (blind inserts, 3mm RHS)"),
        (18 * SC,  (-(ro + 20 * SC), 0),  "ALUMINUM TOP RING (bearing seat Ø130 H7) — LOCATED:\nouter race on a SHOULDER (drum side, Ø122) + a DIN 472\nRETAINING RING (beam side); nylon-isolated"),
        (-52 * SC, (-70 * SC, -47 * SC),  "STEEL FLANGE — bolt from cap\ninto TAPPED 4×M10"),
        (-90 * SC, (-90 * SC, -62 * SC),  f"TOP CAP {LT_CAP_TOP_T:.0f}mm 6061-T6 Al, Ø{LT_CAP_OD}\n(single-part blueprint — Sheet 6)"),
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
    draw_dim_v(ax, UX + 330, -18 * SC, 20 * SC, "38mm RING H", offset=44, fs=6.0,
               right=True, font=FONT)
    draw_dim_v(ax, UX + 405, 20 * SC, 68 * SC, "48mm RAIL H", offset=44, fs=6.0,
               right=True, font=FONT)
    draw_dim_v(ax, UX + 480, -55 * SC, -40 * SC, "15mm FLANGE T", offset=44,
               fs=6.0, right=True, font=FONT)
    draw_dim_v(ax, UX + 555, -55 * SC - CAPd, -55 * SC, f"{LT_CAP_TOP_T:.0f}mm Al CAP T",
               offset=44, fs=6.0, right=True, font=FONT)
    draw_dim_v(ax, UX - 255, -40 * SC, 15 * SC, "55mm SHAFT L", offset=44,
               fs=6.0, font=FONT)
    leader(ax, UX + rs, 13.5 * SC, UX + 150, 102 * SC,
           "CIRCLIPS (DIN 471) each side —\nfix the bearing axially on the shaft,\nso the shaft→beam GAP is held",
           fs=6.2, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    # designed 5mm axial gap: shaft top → beam underside (the shaft never touches the fixed beam)
    draw_dim_v(ax, UX + 120, 15 * SC, 20 * SC, "5mm GAP\n(shaft→beam)", offset=14, fs=5.5, right=True, font=FONT)

    # ── Lower-hub callouts (right column) ────────────────────────────────────
    RxL = LX + HALF + 60
    lo_labels = [
        (58 * SC,  (0, 115 * SC),         f"BOTTOM CAP {LT_CAP_BOT_T:.0f}mm 6061-T6 Al\nbolt into TAPPED 4×M10 flange"),
        (-48 * SC, (100 * SC, -40 * SC),  "AXLE BEAM — 8×M10\ninto RIVET-NUTS"),
        (12 * SC,  (ro + 20 * SC, 0),     "STEEL FLOOR COLLAR (BOLTED, not welded) —\nFLOATING bearing: plain Ø130 H7 bore, outer race free\nto slide axially (the upper bearing is the located one)"),
        (-18 * SC, (ro - 6 * SC, -18 * SC), "COLLAR → FLOOR PLATE:\n8×M10 BOLTED (rivet-nuts, no weld)"),
    ]
    for zt, (tx, tz), txt in lo_labels:
        leader(ax, LX + tx, tz, RxL, zt, txt, fs=6.5, color=C_OUT, ha="left",
               arrow_style="->", font=FONT)
    # Lower-hub dimension lines — collar + floor plate (h + v) ────────────────
    draw_dim_h(ax, LX - 105 * SC, LX + 105 * SC, -310, "Ø210 COLLAR OD",
               offset=46, fs=6.2, above=False, font=FONT)
    draw_dim_h(ax, LX - 140 * SC, LX + 140 * SC, -372, "280mm FLOOR PLATE W",
               offset=46, fs=6.2, above=False, font=FONT)
    draw_dim_v(ax, LX - HALF - 40, -20 * SC, 18 * SC, "38mm COLLAR H", offset=44,
               fs=6.0, font=FONT)
    draw_dim_v(ax, LX - HALF - 120, -68 * SC, -20 * SC, "48mm PLATE H", offset=44,
               fs=6.0, font=FONT)
    ax.text(LX, -235, "bearing · shaft · cap · flange  AS UPPER HUB", ha="center",
            va="top", fontsize=6.2, color=C_DIM, **FONT, zorder=15)

    # ── RIVET-NUT DETAIL — how the ring/collar secures to the CLOSED axle beam (no inside nut) ──
    IS = 7
    ox, oz = 1830, -560
    def rx(mm): return ox + IS * mm
    def rz(mm): return oz + IS * mm
    T = LT_FRAME_T                                            # 3mm RHS wall
    BH = 2 * T + 40                                           # beam box height shown (mm)
    ax.text(ox, rz(BH + 10), "RIVET-NUT DETAIL — ring → CLOSED axle beam  (7:1)",
            ha="center", va="bottom", fontsize=7.5, color=TITLE_COL, fontweight="bold", **FONT, zorder=15)
    draw_rect(ax, rx(-30), rz(-15), IS * 60, IS * 15, fc=C_ALUM, lw=1.2, zorder=6)                 # Al top ring (below the beam)
    draw_rect(ax, rx(-38), rz(0), IS * 76, IS * BH, fc=C_STEEL, lw=1.4, zorder=5)                  # closed RHS beam — outer
    draw_rect(ax, rx(-38) + IS * T, rz(T), IS * (76 - 2 * T), IS * (BH - 2 * T), fc=BG, lw=0.8, zorder=5)  # hollow bore (empty)
    cz = (rz(-15) + rz(0)) / 2                                # ring → beam bolt: head under the ring, up through the ring;
    draw_bolt(ax, ox, cz, rz(0) - rz(-15), d=58, head=-1, end="rivnut", wall=IS * T, csk=True)  # countersunk head + barrel spans the wall
    leader(ax, ox - 20, rz(-15), rx(-42), rz(-15) - 34, "COUNTERSUNK bolt head — flush in the\nring underside (driven from below)",
           fs=6.0, color=C_OUT, ha="right", arrow_style="->", font=FONT)
    leader(ax, ox + 24, rz(T + 6), rx(48), rz(T + 30), "RIVET-NUT (blind threaded insert) set in the beam's\nBOTTOM wall from below — its barrel provides the\ncaptive thread; the bolt clamps the ring up to the wall",
           fs=6.0, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, rx(-16), rz(BH * 0.62), rx(-48), rz(BH + 4), "BORE — EMPTY:\nNO nut inside the closed tube",
           fs=6.0, color=C_DIM, ha="right", arrow_style="->", font=FONT)

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
        "Bearing mounts: upper in isolated aluminum top ring (6×M10 into rivet-nuts / blind threaded inserts set in the beam wall, nylon-isolated); lower in welded steel floor collar (8×M10). Cap→flange: bolt from the cap into the TAPPED steel flange. Full fastening on Sheet 6.",
        "Axial retention — INNER race: circlip on the stub shaft each side of each bearing (DIN 471). OUTER race: the UPPER bearing is LOCATED — the outer race seats on a machined shoulder (bore steps Ø130→Ø122, drum side) that carries the hanging load, captured by a DIN 472 retaining ring on the beam side; the LOWER bearing FLOATS (plain Ø130 H7 bore, outer race free to slide) so it can't fight thermal growth.",
        "Shaft seat: the stub shaft seats ONLY in the Ø75 h6 bearing bore — the SKF 6215 IS the 'socket' (off-the-shelf; shaft blueprint on Sheet 6). It TERMINATES just below the beam underside — it does NOT penetrate the beam and needs NO clearance bore; the bearing (in the ring below the beam) carries + locates the drum, and the load goes to the beam through the ring bolts.",
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

    title_block(ax, "SHEET 5 OF 11", drawing_title="REVOLVING LIGHT-TRAP",
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
        ax.text(cx, pz - rod - 14, f"{n}×M10 on Ø{pcd} PCD · Ø11 clearance → rivet-nut in the beam wall",
                ha="center", va="top", fontsize=7.5, color=C_OUT, **FONT, zorder=9)
        tz = thk * s2                                                         # SECTION (annular)
        for xr0, xr1 in ((cx - rod, cx - rbore), (cx + rbore, cx + rod)):
            draw_rect(ax, xr0, sz, xr1 - xr0, tz, fc=fc, lw=1.4, zorder=5)
        if located:
            # LOCATED bearing seat: bore steps Ø{bore}→Ø{bore-8} to form a SHOULDER (drum-side end)
            # the outer race seats on; a DIN 472 retaining-ring groove at the beam-side end captures it.
            rsh = (bore - 8) / 2 * s2
            for g in (-1, 1):
                draw_rect(ax, min(cx + g * rsh, cx + g * rbore), sz, rbore - rsh, tz * 0.42, fc=fc, lw=1.0, zorder=6)      # shoulder lip
                draw_rect(ax, min(cx + g * (rbore - 4), cx + g * (rbore + 5)), sz + tz * 0.74, 9, tz * 0.22, fc="#606068", lw=0.8, zorder=7)  # DIN 472 ring in groove
            leader(ax, cx + (rsh + rbore) / 2, sz + tz * 0.2, cx + rod + 54, sz - 26,
                   f"Ø{bore - 8} SHOULDER (drum end) —\nouter race seats here", fs=6.2, color=C_OUT, ha="left", arrow_style="->", font=FONT)
            leader(ax, cx + rbore, sz + tz * 0.85, cx + rod + 54, sz + tz + 30,
                   "DIN 472 retaining-ring\ngroove (beam end)", fs=6.2, color=C_OUT, ha="left", arrow_style="->", font=FONT)
        draw_cl_v(ax, cx, sz - 16, sz + tz + 16)
        draw_dim_v(ax, cx + rod + 36, sz, sz + tz, f"{thk}mm THK", offset=34, fs=7, right=True, font=FONT)
        draw_dim_h(ax, cx - rbore, cx + rbore, sz - 20, f"Ø{bore} BORE", offset=30, fs=6.6, above=False, font=FONT)
        if weldnote:
            # CAGE FLOOR / BOTTOM PLATE under the collar + bolts down to it (was a fillet weld)
            plate_tz = LT_FRAME_PLATE_T * s2
            plate_hw = rod + 100
            draw_rect(ax, cx - plate_hw, sz - plate_tz, 2 * plate_hw, plate_tz, fc=C_STEEL, lw=1.4, zorder=4)
            for g in (-1, 1):                        # collar BOLTED down to the plate (was a fillet weld)
                draw_bolt(ax, cx + g * (rod - 24), (sz + tz + sz - plate_tz) / 2, (tz + plate_tz),
                          d=10 * s2, head=1, end="tapped", zb=8)
            draw_dim_v(ax, cx + plate_hw + 34, sz - plate_tz, sz, f"{LT_FRAME_PLATE_T}mm PLATE",
                       offset=30, fs=6.4, right=True, font=FONT)
            leader(ax, cx - plate_hw + 50, sz - plate_tz / 2, cx - plate_hw - 20, sz - plate_tz - 46,
                   "CAGE FLOOR / BOTTOM PLATE\n(collar BOLTED down — 8× M10, no weld)", fs=6.4, color=C_OUT,
                   ha="right", arrow_style="->", font=FONT)
            mat_z = sz - plate_tz - 100
        else:
            mat_z = sz - 54
        ax.text(cx, mat_z, mat + ("" if not weldnote else f"\n{weldnote}"),
                ha="center", va="top", fontsize=7.5, color=C_OUT, **FONT, zorder=9)

    ring(R_RING, LT_TOPRING_OD, SKF6215_OD, 165, LT_FRAME_MOUNT_BOLT_TOP, 38, C_ALUM,
         "UPPER BEARING RING  (2.2:1)", "6061-T6 Al · Ø130 H7 seat + Ø122 shoulder + DIN 472 groove — LOCATED · nylon-isolated", located=True)
    ring(R_COLLAR, LT_COLLAR_OD, SKF6215_OD, 175, LT_FRAME_MOUNT_BOLT_BOT, 38, C_STEEL,
         "LOWER FLOOR COLLAR  (2.2:1)", "A36 steel · plain Ø130 H7 bore — FLOATING (outer race slides)", weldnote="BOLTED to floor plate (8× M10) — no weld")

    # ── Stub-shaft + flange: flange plan (top) + elevation (below) ───────────
    cx = CX
    sh_r, fl_r, fl_t = SKF6215_ID / 2 * s2, 160 / 2 * s2, 12 * s2
    shaft_L = 150 * s2
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
    ax.text(cx, fpz - fl_r - 14, "4×M10 TAPPED on Ø120 PCD (cap bolts in)", ha="center", va="top",
            fontsize=7.5, color=C_OUT, **FONT, zorder=9)
    draw_rect(ax, cx - fl_r, ez - fl_t, 2 * fl_r, fl_t, fc=C_STEEL, lw=1.6, zorder=5)     # flange
    draw_rect(ax, cx - sh_r, ez, 2 * sh_r, shaft_L, fc=C_STEEL, lw=1.6, zorder=5)         # shaft
    for g in (-1, 1):
        ax.add_patch(mpatches.Polygon([(cx + g * sh_r, ez), (cx + g * (sh_r + 14), ez),
                                       (cx + g * sh_r, ez + 14)], closed=True, fc="#CC4422", ec="#CC4422", zorder=7))
    for zc in (ez + shaft_L - 12, ez + shaft_L - 26):
        ax.plot([cx - sh_r, cx - sh_r + 8], [zc, zc], color=C_OUT, lw=1.2, zorder=8)
        ax.plot([cx + sh_r - 8, cx + sh_r], [zc, zc], color=C_OUT, lw=1.2, zorder=8)
    draw_cl_v(ax, cx, ez - fl_t - 16, ez + shaft_L + 16)
    draw_dim_v(ax, cx - fl_r - 34, ez, ez + shaft_L, f"150 LG (Ø{SKF6215_ID})", offset=34, fs=7, font=FONT)
    draw_dim_v(ax, cx + fl_r + 34, ez - fl_t, ez, "12mm THK", offset=32, fs=6.6, right=True, font=FONT)
    ax.text(cx, ez + shaft_L + 16, "Ø75 h6 stub · circlip groove each end", ha="center", va="bottom",
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

    notes = [
        "MACHINED COMPONENTS  (end cap + bearing seats + stub-shaft — assembled on Sheet 5)",
        f"Bearing seat bores Ø{SKF6215_OD} H7 for the SKF 6215 OD; the stub shaft Ø{SKF6215_ID} h6 for the bearing bore, with DIN 471 circlip grooves each side (INNER-race retention). OUTER race: the UPPER ring is LOCATED — Ø122 shoulder (drum end) + DIN 472 retaining-ring groove (beam end); the LOWER collar is a plain Ø130 H7 bore (FLOATING).",
        "FASTENING — cap bolts into the TAPPED stub-shaft flange (cap Ø11 clearance). Ring + collar → axle beam: M10 into RIVET-NUTS / blind threaded inserts (McMaster 95105A199 — M10 twist-resistant, chromate-plated steel; 100×50×3 RHS — 3mm wall too thin to tap, and no internal access to weld a nut). Al ring nylon-isolated; collar BOLTED to the floor plate (8× M10, same as the ring — no weld).",
        "RINGS + STUB 2.2:1 · CAP 1:2 (isotropic) · bolt holes shown enlarged · ALL DIMS IN mm",
    ]
    draw_notes(ax, notes, X_LO + 40, R_CAP - cr - 100, 36, fs=6.5, font=FONT, width=1560, wrap=112, title_color=TITLE_COL)

    title_block(ax, "SHEET 6 OF 11", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="MACHINED COMPONENTS — END CAP + BEARING SEATS + STUB-SHAFT",
                scale_note="RINGS + STUB 2.2:1 · CAP 1:2 · ALL DIMS IN mm",
                doc_id="TBS-001 · Revolving Light-Trap", height=0.02, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet6.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet6.png saved")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 7 — Seals & light-path verification
# Three drum rotations proving no straight-through EXT↔INT light path (the drum's
# single 280° wall always blocks one side) + the running-gap / wiper seal details.
# ═════════════════════════════════════════════════════════════════════════════
def draw_sheet7():
    HR, DR = LT_HOUSING_R, LT_DRUM_OR
    oh = LT_OPENING_DEG / 2
    C6_HOUSE = "#2E5E8C"          # FIXED housing (outer skin) — steel blue
    C6_DRUM = "#B5732E"           # ROTATING drum (inner wall) — warm amber
    dx = 2 * HR + 640
    plans = [(0, 180, "A · DRUM OPEN TO EXTERIOR"),
             (dx, 0, "B · DRUM OPEN TO INTERIOR"),
             (2 * dx, 90, "C · DRUM MID-ROTATION")]
    X_LO, X_HI = -HR - 320, 2 * dx + HR + 640       # extra right room for the top-end light-path section
    Z_LO, Z_HI = -HR - 1720, HR + 360               # extra bottom room: wrapped seal notes clear the title block
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
        # fixed housing walls (OUTER) — TWO 100° material arcs (two 80° openings at 0° & 180°)
        for a_lo, a_hi in ((oh, 180 - oh), (180 + oh, 360 - oh)):
            ts = [math.radians(a_lo + (a_hi - a_lo) * k / 30) for k in range(31)]
            ax.plot([cx + HR * math.cos(t) for t in ts], [HR * math.sin(t) for t in ts],
                    color=C6_HOUSE, lw=5.0, zorder=6)
        for gc in (0, 180):                                       # housing opening-edge ticks
            for e in (gc - oh, gc + oh):
                a = math.radians(e)
                ax.plot([cx + (HR - 22) * math.cos(a), cx + (HR + 22) * math.cos(a)],
                        [(HR - 22) * math.sin(a), (HR + 22) * math.sin(a)],
                        color=C6_HOUSE, lw=1.2, zorder=7)
        # rotating drum wall (INNER) — single 80° opening at dth (warm amber)
        arc(cx, 0, DR, dth, LT_OPENING_DEG, C6_DRUM, 7.0)
        for t in (dth - oh, dth + oh):                            # drum opening jamb ticks
            a = math.radians(t)
            ax.plot([cx + (DR - 24) * math.cos(a), cx + (DR + 24) * math.cos(a)],
                    [(DR - 24) * math.sin(a), (DR + 24) * math.sin(a)],
                    color="#B08020", lw=1.4, zorder=7)
        # WIPER STRIPS on the drum wall (rotate WITH the drum) — bristles span the gap to
        # the housing bore. N strips @ spacing° ≤ 100° keep ≥1 in each material arc always.
        brz = HR - LT_HOUSING_T
        for k in range(LT_WIPER_N):
            sa = math.radians(dth + oh + k * LT_WIPER_SPACING)
            cw, sw = math.cos(sa), math.sin(sa)
            ax.plot([cx + DR * cw, cx + brz * cw], [DR * sw, brz * sw],
                    color="#4A4A4A", lw=3.4, zorder=8)                          # strip + bristles across the gap
            draw_circle(ax, cx + DR * cw, DR * sw, 7, lw=0.6, color="#222",
                        fill=True, fc="#222", zorder=9)                          # holder on the drum OD
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
            ("#4A4A4A", f"WIPER STRIP ×{LT_WIPER_N} (on drum)", 3.4),
            ("#E8A800", "LIGHT PATH (ray)", 2.0)]
    lx = dx - 930
    for col, lab, w in keys:
        ax.plot([lx, lx + 70], [lz, lz], color=col, lw=w, zorder=9)
        ax.text(lx + 85, lz, lab, ha="left", va="center", fontsize=7, color=C_OUT,
                **FONT, zorder=9)
        lx += 640

    # ── Seal detail (radial section at the running gap) ──────────────────────
    # Brush strip RIVETED to the ROTATING drum OD; bristles wipe the FIXED housing bore.
    sx, sz = dx, -HR - 620
    draw_rect(ax, sx - 200, sz - 90, 60, 180, fc="#DDE4EC", lw=1.4, zorder=5)   # FIXED housing wall (bore face at sx-140)
    draw_rect(ax, sx + 140, sz - 90, 46, 180, fc=C_LT_DRUM, lw=1.4, zorder=5)   # ROTATING drum wall (OD face at sx+140)
    # Al straight-flange holder — ONE continuous extrusion: vertical mounting flange against the
    # drum OD (riveted) integral with a U-track (opening inboard) that grips the #4 brush channel.
    ax.add_patch(mpatches.Polygon([
        (sx + 112, sz + 22), (sx + 132, sz + 22), (sx + 132, sz + 42), (sx + 140, sz + 42),
        (sx + 140, sz - 42), (sx + 132, sz - 42), (sx + 132, sz - 22), (sx + 112, sz - 22),
        (sx + 112, sz - 16), (sx + 132, sz - 16), (sx + 132, sz + 16), (sx + 112, sz + 16)],
        closed=True, fc=C_ALUM, ec=C_OUT, lw=1.0, zorder=6))                    # flanged-U holder (one piece)
    draw_rect(ax, sx + 112, sz - 16, 20, 32, fc="#8A8F98", lw=1.0, zorder=7)    # #4 (3/16") channel seated in the U-track
    for zz in range(-14, 16, 6):                                               # black-nylon bristles lay over onto the bore
        ax.plot([sx + 112, sx - 138], [sz + zz, sz + zz + 10], color="#222", lw=0.6, zorder=6)
    for zc in (sz - 38, sz + 38):                                              # flange blind rivets (offset from the channel)
        ax.plot([sx + 132, sx + 182], [zc, zc], color=C_OUT, lw=1.8, zorder=8)
    draw_dim_h(ax, sx - 140, sx + 140, sz - 120, f"≈{RUN_GAP}mm RUNNING GAP", offset=40,
               fs=6.5, above=False, font=FONT)
    leader(ax, sx + 100, sz + 30, sx + 250, sz + 120,
           f"BRUSH STRIP ×{LT_WIPER_N} — #4 (3/16\") strip brush, 0.008\" BLACK nylon, {LT_WIPER_TRIM:.1f}mm trim,\n"
           f"snapped into an Al straight-flange holder FLANGE-RIVETED to the ROTATING drum OD\n"
           f"(rivets in the flange, offset from the brush — see Sheet 4); bristles wipe the FIXED\n"
           f"housing bore across the {RUN_GAP}mm gap · one 96\" piece per line (no joint)",
           fs=6.3, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, sx - 170, sz - 40, sx - 300, sz - 80, f"HOUSING {LT_HOUSING_T}mm (bore)", fs=6,
           color=C_DIM, ha="right", arrow_style="->", font=FONT)
    leader(ax, sx + 163, sz - 60, sx + 300, sz - 90, f"DRUM {LT_DRUM_T:.2f}mm", fs=6,
           color=C_DIM, ha="left", arrow_style="->", font=FONT)
    ax.text(sx, sz + 190, "SEAL DETAIL — RUNNING GAP (enlarged)", ha="center", va="bottom",
            fontsize=7.5, color=TITLE_COL, fontweight="bold", **FONT, zorder=9)

    # ── TOP-END LIGHT PATH — the running gap is CAPPED at its axial top by the cap↔frame neoprene
    # wiper, so a ray up the gap can't circumnavigate OVER the brushes. Bottom end is identical. ──
    tex, tez = 2 * dx + 320, -HR - 640
    gx0, gw = tex - 10, 46                                                         # gap: drum OD (left) → housing bore (right)
    gx1 = gx0 + gw
    ax.text(tex, tez + 210, "TOP-END LIGHT PATH — gap CAPPED at top\n(cap ↔ frame neoprene seal · bottom identical)",
            ha="center", va="bottom", fontsize=7.5, color=TITLE_COL, fontweight="bold", **FONT, zorder=9)
    draw_rect(ax, gx0 - 12, tez - 175, 12, 205, fc=C_LT_DRUM, lw=1.2, zorder=5)    # drum shell (rotating)
    draw_rect(ax, gx1, tez - 175, 14, 235, fc="#DDE4EC", lw=1.2, zorder=5)         # housing wall (fixed)
    draw_rect(ax, gx0 - 110, tez + 6, 110, 22, fc=C_ALUM, lw=1.2, zorder=6)        # drum cap (rotating)
    draw_rect(ax, gx0 - 110, tez + 48, gw + 150, 18, fc=C_STEEL, lw=1.4, zorder=6) # frame top plate (fixed)
    draw_rect(ax, gx0 - 78, tez + 28, gw + 76, 18, fc=C_GASKT, lw=1.0, zorder=7)   # neoprene wiper — caps the gap
    for zz in range(-120, -66, 8):                                                # brush (running-gap seal), lower
        ax.plot([gx0, gx1 - 4], [tez + zz, tez + zz + 5], color="#222", lw=0.6, zorder=6)
    draw_rect(ax, gx0 - 6, tez - 132, 6, 70, fc="#A8763A", lw=0.5, zorder=6)       # brush holder (bronze)
    ax.annotate("", xy=(gx0 + gw / 2, tez + 24), xytext=(gx0 + gw / 2, tez - 165),  # daylight ray UP the gap …
                arrowprops=dict(arrowstyle="-|>", color="#E8A800", lw=1.8), zorder=8)
    for s1, s2 in (((-11, 26), (11, 40)), ((-11, 40), (11, 26))):                  # … killed at the seal (red ✗)
        ax.plot([gx0 + gw / 2 + s1[0], gx0 + gw / 2 + s2[0]], [tez + s1[1], tez + s2[1]], color="#D33", lw=2.2, zorder=9)
    leader(ax, gx0 + 20, tez + 40, gx1 + 40, tez + 120, "NEOPRENE WIPER (cap↔frame)\ncaps the gap — light STOPS here",
           fs=6, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    ax.text(gx1 + 46, tez + 57, "FRAME TOP PLATE (fixed)", ha="left", va="center", fontsize=6, color=C_DIM, **FONT, zorder=9)
    leader(ax, gx0 - 60, tez + 17, gx0 - 118, tez + 40, "DRUM CAP (rotating)", fs=6, color=C_DIM, ha="right", arrow_style="->", font=FONT)
    leader(ax, gx1 + 7, tez - 90, gx1 + 120, tez - 70, "HOUSING (fixed)", fs=6, color=C_DIM, ha="left", arrow_style="->", font=FONT)
    leader(ax, gx0 + 3, tez - 95, gx0 - 118, tez - 150, f"BRUSH + {RUN_GAP}mm gap\n(circumferential seal)", fs=6, color=C_DIM, ha="right", arrow_style="->", font=FONT)
    ax.text(gx0 + gw / 2, tez - 195, "daylight ↑ the gap →\nBLOCKED at the top seal", ha="center", va="top",
            fontsize=6, color=C_OUT, **FONT, zorder=9)

    notes = [
        "SEALS & LIGHT-PATH",
        "Plans A–C: yellow rays = the light path — daylight enters an aligned opening and is stopped by the drum's opaque wall before it can reach the far opening; at mid-rotation both openings are blocked at entry.",
        f"Running-gap wiper: {LT_WIPER_N}× vertical #4 (3/16\") strip brushes (0.008\" BLACK nylon, {LT_WIPER_TRIM:.1f}mm trim) snapped into anodized-Al straight-flange holders FLANGE-RIVETED to the rotating drum OD at {LT_WIPER_SPACING:.0f}° spacing (Ø{LT_RIVET_D} blind rivets, McMaster 97447A015) — the rivets land in the aluminum flange, clear of the brush (a 3/16\" channel is too small to rivet through); bristles lay over onto the fixed housing bore across the {RUN_GAP}mm gap. 96\" stock → each line is ONE continuous piece over the full drum height (no joint).",
        f"Strip count (this study): {LT_WIPER_SPACING:.0f}° spacing ≤ the 100° housing material arc, so ≥1 strip always sits in each arc between the openings at every rotation → the annular gap can never carry light EXT↔INT (dark-gray marks in plans A–C).",
        "Top + bottom axial ends: 12mm closed-cell neoprene wiper strips (rotating drum cap ↔ fixed frame plate) + silicone bead CAP the running gap so a ray can't bypass the brushes over the top/bottom — see the TOP-END LIGHT PATH detail. The brushes seal the gap circumferentially; the neoprene seals it axially.",
        f"Light-tight by geometry: each opening {LT_OPENING_DEG}° (<90°); the drum's {LT_SHELL_ARC}° wall bridges the two 180°-apart housing openings at every rotation. Interior flat-black; residual scatter killed at the matte wall. ALL DIMS IN mm.",
    ]
    draw_notes(ax, notes, X_LO + 60, -HR - 880, 34, fs=7, font=FONT, width=3600, wrap=190,
               title_color=TITLE_COL)

    title_block(ax, "SHEET 7 OF 11", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="SEALS & LIGHT-PATH VERIFICATION",
                scale_note="ALL DIMS IN mm", doc_id="TBS-001 · Revolving Light-Trap",
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
    # FILLET WELDS (typ.) at every post↔beam joint — red triangles in the re-entrant corners
    ws = 16
    for yd, s in ((cyl + RHS, 1), (cyr - RHS, -1)):
        for zb, zdir in ((Z_TOP - BH, -1), (Z_BOT + BH, 1)):
            px, pz = fe(yd, zb)
            ax.add_patch(mpatches.Polygon([(px, pz), (px + s * ws, pz), (px, pz + zdir * ws)],
                                          closed=True, fc="#CC4422", ec="#CC4422", zorder=10))
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
           *fe(CY + 150, Z_BOT + 320), "SKF 6215 ×2\n(seated in the beams)", fs=6.5,
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
           fp(cx1, cyr)[0] + 70, fp(cx1, cyr)[1] + 55,
           f"Al EDGE CHANNEL {LT_EDGE_CHAN_W}×{LT_EDGE_CHAN_LEG}×{LT_EDGE_CHAN_T} U — bonded over each\nfree HDPE edge ({LT_EDGE_CHAN_N} total); ends bolt to top/bottom beams — see Sheet 9",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)

    # ── RHS tube-section inset — the frame members are HOLLOW tube, not solid bar ──
    sxi, szi, SCi = PX + 70, 470, 1.8
    ax.text(sxi + 210, szi + LT_AXLE_BEAM_H * SCi + 66,
            "FRAME MEMBERS = RHS TUBE (HOLLOW) — cut sections:", ha="center", va="bottom",
            fontsize=8, color=TITLE_COL, fontweight="bold", **FONT, zorder=15)
    tube_rect(ax, sxi, szi, RHS * SCi, RHS * SCi, LT_FRAME_T * SCi, fc="#9BA0A8", lw=1.4, zorder=6)
    draw_dim_h(ax, sxi, sxi + RHS * SCi, szi - 26, f"{RHS}mm", offset=26, fs=6.2, above=False, font=FONT)
    draw_dim_v(ax, sxi - 26, szi, szi + RHS * SCi, f"{RHS}mm", offset=26, fs=6.2, font=FONT)
    ax.text(sxi + RHS * SCi / 2, szi + RHS * SCi + 18, f"{RHS}×{RHS}×{LT_FRAME_T} RHS\nposts + rails",
            ha="center", va="bottom", fontsize=6.5, color=C_OUT, **FONT, zorder=9)
    bxi = sxi + 360
    tube_rect(ax, bxi, szi, LT_AXLE_BEAM_W * SCi, LT_AXLE_BEAM_H * SCi, LT_AXLE_BEAM_T * SCi,
              fc="#9BA0A8", lw=1.4, zorder=6)
    draw_dim_h(ax, bxi, bxi + LT_AXLE_BEAM_W * SCi, szi - 26, f"{LT_AXLE_BEAM_W}mm", offset=26, fs=6.2, above=False, font=FONT)
    draw_dim_v(ax, bxi - 26, szi, szi + LT_AXLE_BEAM_H * SCi, f"{LT_AXLE_BEAM_H}mm", offset=26, fs=6.2, font=FONT)
    ax.text(bxi + LT_AXLE_BEAM_W * SCi / 2, szi + LT_AXLE_BEAM_H * SCi + 18,
            f"{LT_AXLE_BEAM_H}×{LT_AXLE_BEAM_W}×{LT_AXLE_BEAM_T} RHS\naxle beams", ha="center",
            va="bottom", fontsize=6.5, color=C_OUT, **FONT, zorder=9)
    ax.text(bxi + LT_AXLE_BEAM_W * SCi + 50, szi + LT_AXLE_BEAM_H * SCi / 2,
            f"wall {LT_FRAME_T}mm (typ.)", ha="left", va="center", fontsize=6.2, color=C_DIM, **FONT, zorder=9)

    # ── Notes ────────────────────────────────────────────────────────────────
    notes = [
        "SUPPORT FRAME — INTEGRATED STEEL WELDED BOX CAGE (part of the swing-panel weldment)",
        f"Box: {RHS}×{RHS}×{LT_FRAME_T} steel RHS — 4 corner posts + perimeter rails (welded). No jamb posts: the free HDPE opening edges are stiffened by Al edge channels (below).",
        f"Axle beams: {LT_AXLE_BEAM_H}×{LT_AXLE_BEAM_W}×{LT_AXLE_BEAM_T} steel RHS, span Yd ({LT_AXLE_BEAM_SPAN}mm) at the drum axis; carry the SKF 6215 at midspan (drum hangs from the top beam).",
        f"Bearing seats: upper isolated 6061-T6 Al ring (Ø{LT_TOPRING_OD}, {LT_FRAME_MOUNT_BOLT_TOP}×M10); lower welded steel collar (Ø{LT_COLLAR_OD}, {LT_FRAME_MOUNT_BOLT_BOT}×M10).",
        f"Fixed housing (outer skin) laps + rivets to rim-angle on the top/bottom beams; free opening edges capped by {LT_EDGE_CHAN_N}× Al U-channel (ends bolt to the beams) — see Sheet 9. Drum rotates free inside.",
        "The cage is welded into the panel top/bottom rails → one structure, swings together. Panel frame owned by the hinged-panel report.",
        "WELDS (red triangles): 6mm fillet weld all-round at every member junction — each corner post to the top/bottom axle beams + perimeter rails, and the axle beam ends to the rails (typ., both views).",
        "ALL DIMS IN mm · plate thickness exaggerated for clarity",
    ]
    draw_notes(ax, notes, X_LO + 60, -300, 58, fs=7, font=FONT, width=2500, wrap=138,
               title_color=TITLE_COL)

    title_block(ax, "SHEET 8 OF 11", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="SUPPORT FRAME — GENERAL ARRANGEMENT (INTEGRATED STEEL CAGE)",
                scale_note="ALL DIMS IN mm", doc_id="TBS-001 · Revolving Light-Trap",
                height=0.045, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet8.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet8.png saved")


# ═════════════════════════════════════════════════════════════════════════════
# SHEET 9 — Housing → frame attachment (outer-skin fixing)
# The fixed housing (5mm) laps a rolled rim-angle TEK-screwed to the frame; SS rivets +
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
    # horizontal leg is TEK-SCREWED up under the beam; the standing lip hangs down for the housing to lap.
    l_angle(ax, 0, 0, -RIML, -LIP, LEGT, fc=C_ALUM, lw=1.4, zorder=5)             # rim-angle (L)
    draw_bolt(ax, -RIML * 0.5, (-LEGT + _fw) / 2, LEGT + _fw, d=8, head=-1, end="tapped", zb=7)  # TEK screw: flat leg → beam bottom wall
    draw_rect(ax, 0, -LIP, DPT, LIP, fc=C_GASKT, lw=0.8, zorder=5)                # DP8010 bead
    draw_rect(ax, DPT, -LIP - 90, HOUT, LIP + 90, fc="#DDE4EC", lw=1.6, zorder=6)  # housing laps down, butts beam underside (broken below)
    for zz in (-LIP - 55, -LIP - 67, -LIP - 79):                                 # break line (housing continues down)
        ax.plot([DPT - 3, DPT + HOUT + 3], [zz - 4, zz + 4], color=C_OUT, lw=0.6, zorder=7)
    blind_rivet(ax, (DPT + HOUT - LEGT) / 2, -LIP / 2, 0, S * (LT_HOUSING_T + 1 + LT_RIM_T), d=RVD)  # radial housing → lip rivet
    draw_dim_v(ax, DPT + HOUT + 40, -LIP, 0, f"{LT_LAP_H}mm LAP", offset=40, fs=6.5, right=True, font=FONT)
    draw_dim_h(ax, DPT, DPT + HOUT, -LIP - 40, f"{LT_HOUSING_T}mm HOUSING", offset=48, fs=6.2,
               above=True, font=FONT)
    leader(ax, -RIML * 0.5, -LEGT, -150, -LIP + 90, "RIM ANGLE 25×25×3 6061-T6 Al — flat leg\nTEK-SCREWED up into the beam bottom wall\n(#14 self-drilling, Al→3mm steel, @ ~150mm)",
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
    leader(ax, dx - LEG2 * 0.35, dz - HT2 / 2 - CT2, dx + 70, dz - HT2 / 2 - CT2 - 64,
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
        "1. Rolled 25×25×3 6061-T6 Al rim-angle, radius R450, TEK-SCREWED to the frame top + bottom beams (#14 self-drilling, Al flat leg → 3mm steel wall, ~150mm pitch; two 100° arcs — the openings have no rim). No welds — avoids welding Al to the steel frame.",
        f"2. Housing laps {LT_LAP_H}mm over the standing lip; DP8010 bead in the lap (bond + light seal).",
        f"3. Drill Ø{LT_RIVET_HOLE:.1f} (#30), {LT_HOUSING_RIVET_N}× Ø{LT_RIVET_D} SS blind rivets per edge (McMaster 97525A435, low-profile head, ~{LT_RIVET_PITCH}mm pitch), wet in DP8010.",
        f"4. Free opening edges (no jamb posts): each of the {LT_EDGE_CHAN_N} vertical HDPE edges is capped by a bonded Al U-channel (DETAIL B) — Ø{LT_RIVET_D} SS blind rivets thru both legs + HDPE @ ~{LT_EDGE_CHAN_RIVET_PITCH}mm (grip ~{2 * LT_EDGE_CHAN_T + LT_HOUSING_T}mm), + DP8010; channel ends bolt to the top + bottom beams (1× M{LT_EDGE_CHAN_END_BOLT}/end via L-clip).",
        "SECTION A–A 7:1 (isotropic) · DETAIL B 7:1 · HOUSING PLAN 1:2 · fastener symbols schematic · ALL DIMS IN mm",
    ]
    draw_notes(ax, notes, X_LO + 60, -360, 24, fs=7, font=FONT, width=1450,
               title_color=TITLE_COL, wrap=180)

    title_block(ax, "SHEET 9 OF 11", drawing_title="REVOLVING LIGHT-TRAP",
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

    # ── FIXED: axle beam — HOLLOW RHS in longitudinal section (both walls solid, bore void) ─
    hollow_beam_long(ax, 0, Z_BEAM0, LT_AXLE_BEAM_SPAN / 2, LT_AXLE_BEAM_H,
                     LT_AXLE_BEAM_T, "bottom", fc=C_STEEL, lw=1.4, zorder=4, breaks=False)
    # ── FIXED: cage corner post — HOLLOW vertical RHS framing the beam end ────
    POST_R0 = LT_AXLE_BEAM_SPAN / 2                                          # 481 — beam outer end / cage corner
    hollow_beam_long(ax, POST_R0, Z_BRK, LT_FRAME_RHS, Z_BEAM0 + LT_AXLE_BEAM_H - Z_BRK,
                     LT_FRAME_T, "left", fc=C_STEEL, lw=1.4, zorder=3, breaks=False)  # continues down (break below)
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
    Z_STUB_TOP = Z_BEAM0 - 3                                                        # stub ends 3mm below the beam — no penetration
    draw_rect(ax, 0, -LT_CAP_TOP_T, bID, Z_STUB_TOP + LT_CAP_TOP_T, fc=C_STEEL, lw=1.0, zorder=5)  # 75Ø stub shaft (ends below beam)
    ax.plot([bID, bID + 8], [Z_BRG0 + bW + 4, Z_BRG0 + bW + 4], color=C_OUT, lw=0.9, zorder=8)  # circlip
    draw_rect(ax, 0, -LT_CAP_TOP_T, CAPR, LT_CAP_TOP_T, fc=C_ALUM, lw=1.2, zorder=5)  # 8mm Al cap disc
    draw_rect(ax, 0, 0, 80, 15, fc=C_STEEL, lw=1.0, zorder=6)                         # Ø160 steel stub-shaft flange (4×M10 tapped, Ø120 PCD)
    # ── Securing bolts (project convention) — each butts the faces it joins ─────
    # Ring → beam: head on the RING BOTTOM, up through the ring + the beam's 3mm bottom
    # wall, into a RIVET-NUT (blind threaded insert) set in that wall from outside (does NOT float into the void).
    rbx = bOD + 15
    wnz = Z_BEAM0                                                                     # beam bottom (near) wall face; the rivet-nut barrel spans the 3mm wall, head on the inner edge
    draw_bolt(ax, rbx, (Z_BRG0 + wnz) / 2, wnz - Z_BRG0, d=10, head=-1, end="rivnut", wall=LT_AXLE_BEAM_T, csk=True)
    # Cap → flange: countersunk flush in the CAP UNDERSIDE, up through the cap into the TAPPED flange.
    cbx = 60                                                                          # Ø120 PCD — clear of the Ø75 shaft and the Ø160 flange edge
    cb0, cb1 = -LT_CAP_TOP_T, 10
    draw_bolt(ax, cbx, (cb0 + cb1) / 2, cb1 - cb0, d=10, head=-1, end="tapped", csk=True)
    leader(ax, rbx, wnz + 6, POST_R0 - 250, Z_BEAM0 + LT_AXLE_BEAM_H + 30,
           f"Al RING → BEAM\n{LT_FRAME_MOUNT_BOLT_TOP}×M10 COUNTERSUNK into RIVET-NUTS\n(blind inserts, beam bottom wall — 3mm RHS)", fs=6.0, color=C_OUT,
           ha="right", arrow_style="->", font=FONT)
    leader(ax, cbx, -LT_CAP_TOP_T, -120, -LT_CAP_TOP_T - 45,
           "CAP → FLANGE\n4×M10 COUNTERSUNK (tapped)", fs=6.0, color=C_OUT, ha="left", arrow_style="->", font=FONT)

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
    draw_dim_v(ax, -95, -LT_CAP_TOP_T, -LT_CAP_TOP_T + SHAFT_L, f"{SHAFT_L} STUB (Ø{SKF6215_ID})",
               offset=48, fs=6.5, font=FONT)
    draw_dim_h(ax, 0, CAPR, -LT_CAP_TOP_T - 60, f"Ø{LT_CAP_OD} CAP (radius)", offset=14,
               fs=6.5, above=False, font=FONT)
    # ── A/B rail positions — radial (dim_h) + vertical joint rise (dim_v) ────
    draw_dim_h(ax, 0, DOR_, -LT_CAP_TOP_T - 95, f"R{DOR_:.0f} — A: rotating drum rail (Ø{2 * LT_DRUM_OR})",
               offset=14, fs=6.0, above=False, font=FONT)
    draw_dim_h(ax, 0, HOR_, -LT_CAP_TOP_T - 135, f"R{HOR_:.0f} — B: fixed housing rail (Ø{DRUM_D})",
               offset=14, fs=6.0, above=False, font=FONT)
    draw_dim_v(ax, HOR_ + 55, LT_LAP_H / 2, Z_BEAM0 - LT_LAP_H / 2,
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
           f"RUNNING GAP {RUN_GAP}mm — {LT_WIPER_N}× #4 strip brushes in Al flange holders\nFLANGE-RIVETED to the ROTATING drum OD, bristles wiping the fixed bore (Sheets 4/7)",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, LT_AXLE_BEAM_SPAN / 2 - 60, Z_BEAM0 + LT_AXLE_BEAM_H / 2, 575, Z_BEAM0 + 120,
           f"AXLE BEAM {LT_AXLE_BEAM_H}×{LT_AXLE_BEAM_W} steel RHS — carries the central\nbearing + the fixed housing; swing-panel weldment (Sheet 8)",
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
        "OUTER joint (fixed), DETAIL B: housing laps a rim-angle TEK-screwed to the axle beam — SS blind rivets + DP8010; full detail on Sheet 9.",
        "The two joints sit at different heights (drum joint at the cap, housing joint at the beam) and on opposite walls of the running gap, so the rotating rivets always clear the fixed ones.",
        "Drum + housing continue the full 2,200mm below the break lines. Bottom end mirrors this, with the lower bearing in a welded steel floor collar (Sheet 5). ALL DIMS IN mm.",
    ]
    draw_notes(ax, notes, X_LO + 40, Z_BRK - 170, 14, fs=7, font=FONT, width=1000,
               title_color=TITLE_COL, wrap=200)

    title_block(ax, "SHEET 10 OF 11", drawing_title="REVOLVING LIGHT-TRAP",
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
    draw_rect(ax, AX(-15), AZ(-40), A * 30, A * 40, fc="#9AA0A8", lw=1.4, zorder=8)             # solid steel plug
    ax.add_patch(mpatches.Rectangle((AX(-6.5), AZ(-40)), A * 13, A * 40, fc=BG, ec="none", zorder=8))  # M12 clearance thru plug
    draw_bolt(ax, ax0, (AZ(-40) + AZ(8)) / 2, AZ(8) - AZ(-40), d=A * 12, head=-1, end="tapped", zb=10)  # M12 → tapped cap
    for zc in (-14, -30):                           # 2× M8 cross-bolts → plug (retention)
        draw_bolt(ax, AX(-11), AZ(zc), A * 21, d=A * 8, vertical=False, head=-1, end="tapped", zb=11)
    for zz in (sbot + 6, sbot + 12):                # break marks (stile continues down)
        ax.plot([AX(-STW / 2) + 5, AX(STW / 2) - 5], [AZ(zz) - 5, AZ(zz) + 5], color=C_OUT, lw=0.8, zorder=9)
    draw_dim_v(ax, AX(-43) - 34, AZ(0), AZ(LT_CAP_TOP_T), f"{LT_CAP_TOP_T:.0f}", offset=24, fs=6.0, font=FONT)
    draw_dim_h(ax, AX(-STW / 2), AX(STW / 2), AZ(sbot) - 38, f"{STW}", offset=28, fs=6.5, above=False, font=FONT)
    draw_dim_v(ax, AX(STW / 2) + 38, AZ(-40), AZ(0), "40", offset=24, fs=6.0, right=True, font=FONT)
    draw_dim_h(ax, AX(-15), AX(15), AZ(-40) - 34, "30", offset=26, fs=6.0, above=False, font=FONT)
    leader(ax, AX(30), AZ(4), AX(66) + 46, AZ(4) + 60, "TOP CAP — 8mm 6061-T6 Al", fs=6.5, color=C_DIM, ha="left", arrow_style="->", font=FONT)
    leader(ax, ax0 + A * 6, AZ(-18), AX(43) + 46, AZ(-8),
           "M12 TAPPED into the cap (blind, ~8mm engagement —\nno pierce / no light leak); clamps the plug up to the cap",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, AX(-11), AZ(-30), AX(43) + 46, AZ(-56),
           f"SOLID STEEL PLUG (~30×30×40) fills the\nopen {STW}×{STW}×5 RHS end + 2× M8 cross-bolts\nthrough the 5mm wall, tapped into the plug —\ngives the open tube a bolting face (pull\nload → handle → tube → plug → cap)",
           fs=6.5, color=C_OUT, ha="left", arrow_style="->", font=FONT)
    leader(ax, AX(-STW / 2), AZ(sbot + 34), AX(-43) - 34, AZ(sbot + 78),
           f"STILE — {STW}×{STW}×5 SS RHS\n(spans cap → cap, ~2.1 m)", fs=6.5, color=C_OUT, ha="right", arrow_style="->", font=FONT)

    # ══ VIEW B — HANDLE ARRANGEMENT (interior elevation · SCALE 1:2) ══════════
    B = 0.55
    bx, bz = 780, -40                               # stile axis; grip midpoint
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
    for gz in (-GRAB_L / 2, GRAB_L / 2):                          # 2 feet, bolted to the stile
        draw_rect(ax, BX(-STW / 2 - 6), BZ(gz - 16), B * 6, B * 32, fc=C_STEEL, lw=0.9, zorder=7)
        draw_bolt(ax, BX(-STW / 2 - 3), BZ(gz), B * 26, d=B * 6.35, vertical=False, head=-1, end="tapped", zb=9)
    draw_dim_v(ax, BX(gxo) - B * hd - 46, BZ(-GRAB_L / 2), BZ(GRAB_L / 2), f"{GRAB_L} HANDLE", offset=28, fs=6.5, font=FONT)
    draw_dim_h(ax, BX(gxo), BX(-STW / 2), BZ(-GRAB_L / 2) - 40, f"{GRAB_SO} STANDOFF", offset=26, fs=6.5, above=False, font=FONT)
    leader(ax, BX(gxo), BZ(GRAB_L / 4), BX(STW / 2) + 70, BZ(GRAB_L / 4 + 40),
           f"McMaster 1871A65 — Ø{GRAB_D:.1f} (0.5\") round pull handle;\nbolted at both feet (2× 1/4\" tapped into the RHS wall) · NO welds",
           fs=6.2, color=C_OUT, ha="left", arrow_style="->", font=FONT)

    # ══ Notes ═════════════════════════════════════════════════════════════════
    notes = [
        "PULL-HANDLE MOUNT  (interior face only — no fastener pierces the drum wall / no light leak)",
        f"1. Stile: {STW}×{STW}×5 SS RHS, spans + fastens between the two 8mm 6061-T6 Al caps (top + bottom ends identical).",
        "2. Each open RHS end takes a SOLID STEEL PLUG (~30×30×40) cross-bolted 2× M8 through the tube walls (tapped into the plug) — this gives the open section a bolting face.",
        "3. A single M12 TAPPED into the cap clamps each plug up to it (blind, ~8mm engagement — no pierce). Pull load path: handle → tube → plug → cap, landing in the structural cap (not the thin HDPE wall).",
        "4. Off-the-shelf pull handle McMaster 1871A65 (Ø0.5\" bar, 308mm long, 52mm standoff) bolts at its two feet with 1/4\" screws tapped into the RHS wall. No welds anywhere.",
        "VIEW A 3:1 · VIEW B 1:2 · ALL DIMS IN mm",
    ]
    draw_notes(ax, notes, X_LO + 40, -320, 20, fs=7, font=FONT, width=1360, wrap=120, title_color=TITLE_COL)

    title_block(ax, "SHEET 11 OF 11", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="PULL-HANDLE MOUNT — STILE → CAP PLUG JOINT + HANDLE ARRANGEMENT",
                scale_note="VIEW A 3:1 · VIEW B 1:2 · ALL DIMS IN mm",
                doc_id="TBS-001 · Revolving Light-Trap", height=0.045, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet11.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  → diagrams/lighttrap-sheet11.png saved")


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
    print("Done.")


if __name__ == "__main__":
    main()
