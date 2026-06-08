#!/usr/bin/env python3
"""TBS-001 — TRANSPORT-CLEARANCE STUDY (scratch model, like the cantilever study).

Validates the split-panel transport scheme BEFORE any cascade:
  - the hinge panel is split into a FIXED top header + FIXED bottom sill (both at
    the door plane, X0) and a SLIDING leaf that threads the clear Z-window between
    the two film-plane rails,
  - the light-trap DRUM is TRIMMED to the same window (top 2248, bottom 190) so it
    clears the rails as it retracts to transport,
  - the two front brace verts are shown GHOSTED (demount for transport),
  - the left walkway floor-leg cantilever supports are present (grate ghosted /
    lifted out for transport).

Posed STATICALLY at the transport rest (slide = PANEL_SLIDE): drum at X480 — its
Ø900 body straddles the X150 rail line, so the drum↔rail clearance reads directly.
A side-elevation scene (camera along −Y) shows the Z-bands stacked so the threading
is unambiguous.

    python3 src/models/generate_transport_study_model.py --send          # push to SketchUp
    python3 src/models/generate_transport_study_model.py --send --skp     # + save .skp
"""
import argparse
import os
import sys

import generate_sketchup_model as ov
import generate_walkway_model as wm
import generate_lighttrap_model as lt

ruby_box, ruby_cylinder = ov.ruby_box, ov.ruby_cylinder
component, mm = ov.component, ov.mm

# ── geometry (all from tbs_constants via ov) ─────────────────────────────────
C_WID, C_HGT, WALL_T = ov.C_WID, ov.C_HGT, ov.WALL_T          # 2362, 2388, 40
RAIL_X = ov.RAIL_X_L                                          # 150 — left rail X
RAIL = 40                                                     # 40×40 rail tube
BL_Z0, BL_Z1 = ov.RAIL_OFF_BOT, ov.RAIL_OFF_BOT + RAIL        # 150 .. 190
TL_Z0, TL_Z1 = ov.C_HGT - ov.RAIL_OFF - RAIL, ov.C_HGT - ov.RAIL_OFF  # 2248 .. 2288
RAIL_Y0, RAIL_Y1 = ov.FP_Y_MIN, ov.FP_Y                       # 100 .. 2262 (portals)
BR = ov.BRACE_RHS                                            # 50 — brace RHS
BZ0, BZ1 = ov.BRACE_Z_BOT, ov.BRACE_Z_TOP                    # 150 .. 2288

# the clear threading window between the two rails
WIN_Z0, WIN_Z1 = BL_Z1, TL_Z0                                # 190 .. 2248

PANEL_SLIDE = ov.PANEL_SLIDE                                 # 880
FLOOR_GAP = ov.PANEL_FLOOR_GAP                               # 130
YD_L, YD_R = ov.PANEL_CORNER_YD_L, ov.PANEL_CORNER_YD_R      # 653, 1709
T_CORNER, T_CENTER = 40, ov.PANEL_CENTER_T                   # 40, 120
DRUM_CY, DRUM_R = ov.DRUM_CY, ov.DRUM_R                      # 1181, 450
APER_R = DRUM_R + 18                                         # 468
APER_L_Y, APER_R_Y = DRUM_CY - APER_R, DRUM_CY + APER_R      # 713, 1649
DRUM_TX = ov.DRUM_CX + PANEL_SLIDE                           # -400+880 = 480 (transport center X)

# trimmed drum band (threads the window)
DRUM_Z0, DRUM_Z1 = WIN_Z0, WIN_Z1                            # 190 .. 2248

# drum STEEL FRAME (top + bottom bearings) — must also fit inside the window so it
# threads the rails as it slides with the leaf. The bearings/beams eat the top and
# bottom of the window, so the drum BODY shrinks to suit.
BEAR_H = 28                                                 # bearing + beam band
DRUM_BODY_Z0, DRUM_BODY_Z1 = WIN_Z0 + BEAR_H, WIN_Z1 - BEAR_H   # 218 .. 2220 (interior ~2002)
FRAME_POST_YD = ((YD_L, APER_L_Y), (APER_R_Y, YD_R))        # (653,713) & (1649,1709) — flank drum

# split-panel bands
HDR_Z0, HDR_Z1 = TL_Z0 - 10, 2300                           # fixed header 2238..2300
SILL_Z0, SILL_Z1 = FLOOR_GAP, BL_Z1 + 15                    # fixed sill 130..205
LEAF_Z0, LEAF_Z1 = SILL_Z1, HDR_Z0 - 5                      # sliding leaf 205..2233
SKIN_T = 60                                                  # representative skin thickness (X)
LEAF_X = PANEL_SLIDE                                         # 880 — leaf at transport rest

# colors
C_SHELL = ov.C_SHELL
C_STEEL = ov.C_STEEL
C_ALUM = ov.C_ALUM
C_FIXED = "#9AA0A6"      # fixed header / sill (gray)
C_LEAF = "#C79A5B"       # sliding leaf (amber)
C_WALK = "#8A8E99"       # walkway grate (ghost)

CTX_X = 2700             # how far down-length to draw the ghost shell

# brace verts (uprights) at X150, Yd 100..150 (near) and 2262..2312 (far). The
# leaf is NARROWED in Yd to thread BETWEEN them; fixed jambs seal the side gaps.
VERT_W = BR                                                 # 50
VERT_NEAR_Y0, VERT_NEAR_Y1 = ov.FP_Y_MIN, ov.FP_Y_MIN + VERT_W       # 100..150
VERT_FAR_Y0, VERT_FAR_Y1 = ov.FP_Y, ov.FP_Y + VERT_W                 # 2262..2312
LEAF_Y0 = VERT_NEAR_Y1 + 8                                  # 158 — clear of near vert inner face
LEAF_Y1 = VERT_FAR_Y0 - 8                                   # 2254 — clear of far vert inner face

# ── bearing / carriage (the hinge-panel suspension) ──────────────────────────
BEAR_YD = (YD_L, YD_R)                    # 653, 1709 — carriage depths (NEW_YD_L/R)
RAIL_BZ0 = C_HGT - 30                      # 2358 — HGR20 ceiling-rail underside
RAIL_BZ1 = C_HGT                           # 2388
CARR_Z0, CARR_Z1 = RAIL_BZ0 - 28, RAIL_BZ0  # 2330 .. 2358 — HGH20CA block
BRK_W = 60                                 # suspension bracket footprint (X)
RAIL_BX0, RAIL_BLEN = -30, PANEL_SLIDE + 220   # ceiling rail span (X-30 .. 1070)

TAGS = ["Context", "Film Rails", "Brace verts", "Fixed Frame", "Bearing Rail",
        "Walkway Supports", "Walkway Grate",
        "Floor Guide",
        "Drum (transport)", "Leaf (transport)", "Slide hanger (transport)",
        "Drum (camera)", "Leaf (camera)", "Slide hanger (camera)",
        "Drum (camera ghost)", "Crossing ghost", "Labels"]


def context():
    a = 0.10
    return '\n'.join([
        ruby_box("Floor (ghost)", 0, 0, -WALL_T, CTX_X, C_WID, WALL_T, color=C_SHELL, alpha=a),
        ruby_box("Ceiling (ghost)", 0, 0, C_HGT, CTX_X, C_WID, WALL_T, color=C_SHELL, alpha=a),
        ruby_box("Wall near (ghost)", 0, -WALL_T, 0, CTX_X, WALL_T, C_HGT, color=C_SHELL, alpha=a),
        ruby_box("Wall far (ghost)", 0, C_WID, 0, CTX_X, WALL_T, C_HGT, color=C_SHELL, alpha=a),
    ])


def film_rails():
    """The two left rails (the obstacles) + the brace beams. Verts are separate."""
    L = RAIL_Y1 - RAIL_Y0
    return '\n'.join([
        ruby_box("FP Rail BL (lower-left)", RAIL_X, RAIL_Y0, BL_Z0, RAIL, L, RAIL, color=C_STEEL),
        ruby_box("FP Rail TL (upper-left)", RAIL_X, RAIL_Y0, TL_Z0, RAIL, L, RAIL, color=C_STEEL),
        # brace cross-beams (front portion only) at each portal depth
        ruby_box("FP Brace beam bottom (pinhole)", RAIL_X, RAIL_Y0, BZ0, 1450, BR, BR, color=C_STEEL),
        ruby_box("FP Brace beam bottom (film)", RAIL_X, RAIL_Y1, BZ0, 1450, BR, BR, color=C_STEEL),
        ruby_box("FP Brace beam top (pinhole)", RAIL_X, RAIL_Y0, BZ1 - BR, 1450, BR, BR, color=C_STEEL),
        ruby_box("FP Brace beam top (film)", RAIL_X, RAIL_Y1, BZ1 - BR, 1450, BR, BR, color=C_STEEL),
    ])


def brace_verts():
    """The two front brace verts — now PERMANENT: the narrowed leaf threads between
    them, so they no longer need to be demountable."""
    h = BZ1 - BZ0
    return '\n'.join([
        ruby_box("Brace vert L (near) — PERMANENT", RAIL_X, VERT_NEAR_Y0, BZ0, BR, BR, h, color=C_STEEL),
        ruby_box("Brace vert L (far) — PERMANENT", RAIL_X, VERT_FAR_Y0, BZ0, BR, BR, h, color=C_STEEL),
    ])


def fixed_header_sill():
    """Header above the top rail + sill below the bottom rail — both fixed at the
    door plane (X0), so they never reach the X150 rails."""
    lh = LEAF_Z1 - LEAF_Z0
    return '\n'.join([
        ruby_box("Fixed header (above TL rail)", 0, 0, HDR_Z0, SKIN_T, C_WID, HDR_Z1 - HDR_Z0,
                 color=C_FIXED),
        ruby_box("Fixed sill (below BL rail)", 0, 0, SILL_Z0, SKIN_T, C_WID, SILL_Z1 - SILL_Z0,
                 color=C_FIXED),
        # NEW fixed jambs — seal the side gaps left by the narrowed leaf (cover the verts)
        ruby_box("Fixed jamb near (new)", 0, 0, LEAF_Z0, SKIN_T, LEAF_Y0, lh, color=C_FIXED),
        ruby_box("Fixed jamb far (new)", 0, LEAF_Y1, LEAF_Z0, SKIN_T, C_WID - LEAF_Y1, lh, color=C_FIXED),
    ])


def sliding_leaf(x, alpha=1.0, suffix=""):
    """The leaf band (Z205..2233) — stepped zones with the center drum aperture."""
    h = LEAF_Z1 - LEAF_Z0
    p = []
    # near/far corners NARROWED to LEAF_Y0..LEAF_Y1 so they thread between the verts
    p.append(ruby_box(f"Leaf near corner (narrowed){suffix}", x, LEAF_Y0, LEAF_Z0, T_CORNER, YD_L - LEAF_Y0, h, color=C_LEAF, alpha=alpha))
    p.append(ruby_box(f"Leaf center strip near{suffix}", x, YD_L, LEAF_Z0, T_CENTER, APER_L_Y - YD_L, h, color=C_LEAF, alpha=alpha))
    p.append(ruby_box(f"Leaf center strip far{suffix}", x, APER_R_Y, LEAF_Z0, T_CENTER, YD_R - APER_R_Y, h, color=C_LEAF, alpha=alpha))
    p.append(ruby_box(f"Leaf far corner (narrowed){suffix}", x, YD_R, LEAF_Z0, T_CORNER, LEAF_Y1 - YD_R, h, color=C_LEAF, alpha=alpha))
    return '\n'.join(p)


def drum_body(cx, alpha=1.0, sfx=""):
    """Revolving drum (Ø900 housing arcs + Ø864 rotor C-shell + caps), body within
    the bearings (Z218..2220) so the steel frame fits the rail window."""
    z0, z1 = DRUM_BODY_Z0, DRUM_BODY_Z1
    h = z1 - z0
    od = lt.OPENING_DEG
    aw = ov.ruby_arc_wall
    return '\n'.join([
        aw(f"Drum housing arc near{sfx}", cx, DRUM_CY, lt.HOUSING_R, lt.HOUSING_T, h,
           gap_center_deg=270, gap_deg=180 + od, color=C_ALUM, alpha=0.40 * alpha, z0=z0),
        aw(f"Drum housing arc far{sfx}", cx, DRUM_CY, lt.HOUSING_R, lt.HOUSING_T, h,
           gap_center_deg=90, gap_deg=180 + od, color=C_ALUM, alpha=0.40 * alpha, z0=z0),
        aw(f"Drum rotor C-shell{sfx}", cx, DRUM_CY, lt.DRUM_OR, lt.DRUM_T, h,
           gap_center_deg=180, gap_deg=od, color=C_ALUM, alpha=0.82 * alpha, z0=z0),
        ruby_cylinder(f"Drum top cap{sfx}", cx, DRUM_CY, z1 - 5, lt.DRUM_OR, 5, color=C_ALUM, alpha=alpha, axis="z"),
        ruby_cylinder(f"Drum bottom cap{sfx}", cx, DRUM_CY, z0, lt.DRUM_OR, 5, color=C_ALUM, alpha=alpha, axis="z"),
    ])


def drum_frame(cx, x_leaf, alpha=1.0, sfx=""):
    """STEEL frame carrying the drum: 2 posts flanking it (which double as the leaf
    center jambs) + top & bottom cross-beams carrying the drum bearings, tied back
    to the leaf. Whole frame fits the rail window (190..2248) so it threads the
    rails as it slides with the leaf."""
    fz0, fz1 = WIN_Z0, WIN_Z1
    C_BEAR = "#5A5AA0"
    p = []
    for (y0, y1) in FRAME_POST_YD:                            # posts flank the drum
        p.append(ruby_box(f"Drum frame post (steel){sfx}", cx - 30, y0, fz0, 60, y1 - y0, fz1 - fz0,
                          color=C_STEEL, alpha=alpha))
    # top + bottom cross-beams (carry the bearings)
    p.append(ruby_box(f"Drum frame top beam{sfx}", cx - 30, YD_L, fz1 - BEAR_H, 60, YD_R - YD_L, BEAR_H, color=C_STEEL, alpha=alpha))
    p.append(ruby_box(f"Drum frame bottom beam{sfx}", cx - 30, YD_L, fz0, 60, YD_R - YD_L, BEAR_H, color=C_STEEL, alpha=alpha))
    # top + bottom bearings on the drum axis
    p.append(ruby_cylinder(f"Drum TOP bearing{sfx}", cx, DRUM_CY, fz1 - BEAR_H, 65, BEAR_H, color=C_BEAR, alpha=alpha, axis="z"))
    p.append(ruby_cylinder(f"Drum BOTTOM bearing{sfx}", cx, DRUM_CY, fz0, 65, BEAR_H, color=C_BEAR, alpha=alpha, axis="z"))
    # ties from the drum frame back to the leaf (top + bottom, each side)
    lo, hi = min(cx + 30, x_leaf), max(cx + 30, x_leaf)
    for (y0, y1) in FRAME_POST_YD:
        yc = (y0 + y1) / 2 - 20
        p.append(ruby_box(f"Frame-to-leaf tie top{sfx}", lo, yc, fz1 - BEAR_H, hi - lo, 40, BEAR_H, color=C_STEEL, alpha=alpha))
        p.append(ruby_box(f"Frame-to-leaf tie bottom{sfx}", lo, yc, fz0, hi - lo, 40, BEAR_H, color=C_STEEL, alpha=alpha))
    return '\n'.join(p)


def drum_assembly(cx, x_leaf, alpha=1.0, sfx=""):
    return drum_body(cx, alpha, sfx) + "\n" + drum_frame(cx, x_leaf, alpha, sfx)


def drum_side_seals(x_leaf, alpha=1.0, sfx=""):
    """The two MISSING light-tight closures — one each side of the drum. The drum
    leads the panel by 400mm, so each closure runs perpendicular to the panel (90°)
    from the panel plane forward to butt the drum housing's near/far tangent,
    closing the gap between the flat aperture and the round drum."""
    cx = x_leaf + ov.DRUM_CX                 # drum center X (drum leads the panel by 400)
    xlo, dx = min(cx, x_leaf), abs(x_leaf - cx)
    t, z0, z1 = 8, LEAF_Z0, LEAF_Z1
    near_y = DRUM_CY - lt.HOUSING_R - t       # butts the near tangent (Yd731) from outside
    far_y = DRUM_CY + lt.HOUSING_R            # butts the far tangent (Yd1631) from outside
    return '\n'.join([
        ruby_box(f"Drum side light-seal (near){sfx}", xlo, near_y, z0, dx, t, z1 - z0, color=C_LEAF, alpha=alpha),
        ruby_box(f"Drum side light-seal (far){sfx}", xlo, far_y, z0, dx, t, z1 - z0, color=C_LEAF, alpha=alpha),
    ])


def drum_ghost(cx):
    """Faint Ø900 cylinder marking the drum's camera (operating) position so the
    transport view shows the slide travel."""
    return ruby_cylinder("Drum camera-position ghost (Ø900)", cx, DRUM_CY, DRUM_Z0,
                         DRUM_R, DRUM_Z1 - DRUM_Z0, color=C_ALUM, alpha=0.15, axis="z")


def walkway_supports():
    """Floor-leg cantilever supports (permanent — present in both states)."""
    return '\n'.join(wm.left_floor_cantilevers())


def walkway_grate():
    """The removable left grate — INSTALLED for camera/operating, lifted out for
    transport (its own tag, hidden in the transport scene)."""
    grate_z = ov.WALKWAY_H - ov.WALKWAY_GRATE_T
    return ruby_box("Left walkway grate (installed)", ov.WALKWAY_LEFT_X, 0, grate_z,
                    ov.WALKWAY_W, C_WID, ov.WALKWAY_GRATE_T, color=C_WALK)


def _post_centers():
    return [(y0 + y1) / 2.0 for (y0, y1) in FRAME_POST_YD]   # 683, 1679


# Forward offset of the hang point from the drum frame so it NEVER reaches the
# X150 rail during the slide: at camera the drum frame is at X-400, so the hang
# point at -400+640 = 240 stays inboard of the rail (150-190). No crossing → nothing
# demountable.
HANGER_OFFSET = 640
HX_CAM = ov.DRUM_CX + HANGER_OFFSET          # 240
HX_TRN = None                                # set below once DRUM_TX known
ARM_Z0, ARM_Z1 = WIN_Z1 - 36, WIN_Z1 - 8     # 2212..2240 — top arm, 8mm UNDER the TL rail


def ceiling_rails():
    """Fixed HGR20 ceiling rails — span the (forward-offset) hang-point travel, at
    the drum-frame post depths."""
    x0 = HX_CAM - 60
    span = (DRUM_TX + HANGER_OFFSET + 90) - x0
    p = []
    for yc in _post_centers():
        p.append(ruby_box(f"HGR20 ceiling rail (Yd{int(yc)})", x0, yc - 10, RAIL_BZ0,
                          span, 20, RAIL_BZ1 - RAIL_BZ0, color=C_STEEL))
    return '\n'.join(p)


def ceiling_hanger(cx, alpha=1.0, sfx=""):
    """FORWARD-OFFSET ceiling hang. A top arm runs inboard from the drum frame at
    Z2212-2240 (8mm UNDER the TL rail — it threads the window), to a hang point
    offset +HANGER_OFFSET, where a vertical riser rises to the carriage. The hang
    point stays inboard of the X150 rail throughout the slide, so NOTHING crosses
    the rail and nothing is demountable."""
    hx = cx + HANGER_OFFSET
    p = []
    for yc in _post_centers():
        p.append(ruby_box(f"Top arm — UNDER TL rail{sfx}", cx, yc - 25, ARM_Z0,
                          HANGER_OFFSET, 50, ARM_Z1 - ARM_Z0, color=C_STEEL, alpha=alpha))
        p.append(ruby_box(f"Vertical riser (inboard of rail){sfx}", hx - 25, yc - 25, ARM_Z1,
                          50, 50, CARR_Z0 - ARM_Z1, color="#B03030", alpha=alpha))
        p.append(ruby_box(f"Slide carriage (HGH20CA){sfx}", hx - 22, yc - 22, CARR_Z0,
                          44, 44, CARR_Z1 - CARR_Z0, color="#B03030", alpha=alpha))
    return '\n'.join(p)


def bottom_guide(cx, alpha=1.0, sfx=""):
    """Bottom guide rollers on the assembly — run in the fixed floor channel and
    react the forward-offset tipping/lateral load (so the load path is still sound
    without a vertical hanger over the CG)."""
    p = []
    for yc in _post_centers():
        p.append(ruby_cylinder(f"Bottom guide roller{sfx}", cx, yc, WIN_Z0, 28, ARM_Z1 - ARM_Z0,
                               color="#B03030", alpha=alpha, axis="z"))
    return '\n'.join(p)


def floor_guide():
    """FIXED floor guide channel at sill level (Z190..218) spanning the assembly
    travel — the bottom rollers run in it. Threads OVER the BL rail (150-190)."""
    x0 = ov.DRUM_CX - 60
    span = (DRUM_TX + 120) - x0
    p = []
    for yc in _post_centers():
        p.append(ruby_box(f"Floor guide channel (Yd{int(yc)})", x0, yc - 38, WIN_Z0,
                          span, 76, 28, color=C_STEEL))
    return '\n'.join(p)


def leaf_backbone(x, alpha=1.0, suffix=""):
    """60×60 SHS hinge-side backbone of the leaf (the frame member the carriage
    beam transfers load through)."""
    return ruby_box(f"Leaf backbone 60x60 SHS{suffix}", x, 0, LEAF_Z0, 60, 60,
                    LEAF_Z1 - LEAF_Z0, color=C_STEEL, alpha=alpha)


POINT_LABELS = [
    (RAIL_X, 1181, TL_Z1, "FILM RAILS (left)\nthe obstacle", 1500, 0, 120),
    (DRUM_TX, DRUM_CY, DRUM_Z1, "DRUM in STEEL FRAME\ntop+bottom bearings\nframe threads window\n(body 218-2220)",
     -650, -300, 260),
    (RAIL_X, VERT_NEAR_Y0, 1600, "BRACE VERT (upright)\nPERMANENT — leaf\nthreads between", -900, -500, 250),
    (0, LEAF_Y0 // 2, 1300, "FIXED JAMB (new)\nseals side gap\nover the vert", 650, -550, 300),
    (0, 200, HDR_Z0, "FIXED HEADER + SILL\n(stay at door plane)", 700, -400, 180),
    (LEAF_X, 360, 1400, "SIDE LEAVES\nmounted to drum frame —\nONE rigid assembly,\nthread Yd158-2254 x Z205-2233", 600, -520, 250),
    (DRUM_TX + 200, DRUM_CY - DRUM_R, 1000, "DRUM SIDE LIGHT-SEALS\n90° to panel, butt the\ndrum housing (close the\nflat-panel-to-round-drum gap)", -200, -650, 400),
    (ov.WALKWAY_LEFT_X - 30, 800, 200, "WALKWAY SUPPORTS\n(floor-leg cantilevers)", -500, -650, 700),
    (DRUM_TX + HANGER_OFFSET, 683, RAIL_BZ1, "FORWARD-OFFSET HANGER\nhang point inboard of rail —\ntop arm threads UNDER TL rail,\nNOTHING demountable", 200, -380, 170),
    (DRUM_TX, 683, 800, "BOTTOM GUIDE ROLLER\nin fixed floor channel —\nreacts the offset tipping\n(threads over BL rail)", 350, -550, 250),
]


def labels():
    rows = []
    for x, y, z, text, dx, dy, dz in POINT_LABELS:
        rows.append(
            f'anc = Geom::Point3d.new({mm(x)}, {mm(y)}, {mm(z)})\n'
            f'txt = entities.add_text("{text}", anc, Geom::Vector3d.new({mm(dx)}, {mm(dy)}, {mm(dz)}))\n'
            f'txt.layer = model.layers["Labels"] rescue nil')
    return '\n'.join(rows)


def generate_ruby():
    comps = '\n'.join([
        # ── fixed (present in every scene) ──
        component("Context", "Context", context()),
        component("Film Rails (left)", "Film Rails", film_rails()),
        component("Brace verts (permanent)", "Brace verts", brace_verts()),
        component("Fixed Frame (header/sill/jambs)", "Fixed Frame", fixed_header_sill()),
        component("HGR20 Ceiling Rails (fixed)", "Bearing Rail", ceiling_rails()),
        component("Floor Guide Channel (fixed)", "Floor Guide", floor_guide()),
        component("Walkway Supports", "Walkway Supports", walkway_supports()),
        component("Walkway Grate (installed)", "Walkway Grate", walkway_grate()),
        # ── ONE rigid moving assembly @ TRANSPORT: drum frame + side leaves slide
        #    together +880 (the leaves are mounted to the drum frame, not independent) ──
        component("Side leaves — transport", "Leaf (transport)",
                  sliding_leaf(LEAF_X) + "\n" + leaf_backbone(LEAF_X)
                  + "\n" + drum_side_seals(LEAF_X)),
        component("Drum + frame — transport", "Drum (transport)", drum_assembly(DRUM_TX, LEAF_X)),
        component("Slide hanger — transport", "Slide hanger (transport)",
                  ceiling_hanger(DRUM_TX) + "\n" + bottom_guide(DRUM_TX)),
        # ── same rigid assembly @ CAMERA / operating (leaf X0, drum X-400) ──
        component("Side leaves — camera", "Leaf (camera)",
                  sliding_leaf(0) + "\n" + leaf_backbone(0)
                  + "\n" + drum_side_seals(0)),
        component("Drum + frame — camera", "Drum (camera)", drum_assembly(ov.DRUM_CX, 0)),
        component("Slide hanger — camera", "Slide hanger (camera)",
                  ceiling_hanger(ov.DRUM_CX) + "\n" + bottom_guide(ov.DRUM_CX)),
        # ── ghosts ──
        component("Drum camera-position ghost", "Drum (camera ghost)", drum_ghost(ov.DRUM_CX)),
        # ghost of the assembly with the DRUM FRAME at the rail plane (X150): the
        # frame threads the rectangle, the hang point is offset to X790 (well inboard
        # of the rail), and the top arm passes UNDER it — nothing crosses the rail
        component("Assembly rail-crossing ghost", "Crossing ghost",
                  drum_assembly(RAIL_X, RAIL_X + 400, alpha=0.20, sfx=" (x)") + "\n"
                  + sliding_leaf(RAIL_X + 400, alpha=0.18, suffix=" (x)") + "\n"
                  + ceiling_hanger(RAIL_X, alpha=0.30, sfx=" (x)") + "\n"
                  + bottom_guide(RAIL_X, alpha=0.30, sfx=" (x)")),
    ])
    tags_ruby = '\n'.join(
        f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)

    return f'''model = Sketchup.active_model
model.start_operation("TBS-001 Transport Study", true)
entities = model.active_entities

opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

to_erase = entities.to_a.select {{ |e|
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text)
}}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each {{ |p| model.pages.erase(p) }}

{tags_ruby}

{comps}

{labels()}

model.definitions.purge_unused
model.materials.purge_unused

# ── Camera + scenes ──
# show everything except the named tags
show_only = lambda {{ |hide|
  model.layers.each {{ |l| l.visible = true }}
  hide.each {{ |n| model.layers[n].visible = false if model.layers[n] }}
}}
CAM = ["Drum (camera)", "Leaf (camera)", "Slide hanger (camera)"]
TRN = ["Drum (transport)", "Leaf (transport)", "Slide hanger (transport)"]
GHOSTS = ["Drum (camera ghost)", "Crossing ghost"]

iso_dir = Geom::Vector3d.new(-0.62, -0.70, 0.45); iso_dir.normalize!
def isocam(model, dir, cx, cy, cz, zoom)
  ctr = Geom::Point3d.new(cx.mm, cy.mm, cz.mm)
  eye = ctr.offset(dir, 9500.mm)
  model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
  model.active_view.camera.perspective = true
  model.active_view.zoom_extents
  model.active_view.zoom(zoom)
end

# 1) clearance iso — transport solids + crossing/camera ghosts, hide camera solids + grate
show_only.call(CAM + ["Walkway Grate"])
isocam(model, iso_dir, 760, 1181, 1200, 0.80)
p1 = model.pages.add("Transport — iso (labeled)"); p1.use_camera = true

# 2) side elevation along −Y (Z-bands stack) — same vis, labels off
show_only.call(CAM + ["Walkway Grate"])
model.layers["Labels"].visible = false if model.layers["Labels"]
eye2 = Geom::Point3d.new(900.mm, -5500.mm, 1240.mm)
ctr2 = Geom::Point3d.new(900.mm, 1181.mm, 1240.mm)
model.active_view.camera = Sketchup::Camera.new(eye2, ctr2, Z_AXIS)
model.active_view.camera.perspective = false
model.active_view.zoom_extents
model.active_view.zoom(0.85)
p2 = model.pages.add("Transport — side elevation (Z clearances)"); p2.use_camera = true

# 3) panel assembly only (transport) — just panel frame + leaf + drum + bearing
show_only.call(CAM + GHOSTS + ["Walkway Grate", "Context", "Film Rails", "Brace verts", "Walkway Supports"])
isocam(model, iso_dir, 470, 1181, 1220, 0.90)
p3 = model.pages.add("Panel assembly only"); p3.use_camera = true

# 4) FULL SYSTEM — camera/operating position (leaf X0, drum X-400, grate installed)
show_only.call(TRN + GHOSTS)
isocam(model, iso_dir, 50, 1181, 1200, 0.74)
p4 = model.pages.add("System — camera position"); p4.use_camera = true

# 5) FULL SYSTEM — transport position (leaf X880, drum X480, grate removed, camera ghost)
show_only.call(CAM + ["Walkway Grate", "Crossing ghost"])
isocam(model, iso_dir, 470, 1181, 1200, 0.78)
p5 = model.pages.add("System — transport position"); p5.use_camera = true

model.layers.each {{ |l| l.visible = true }}
model.commit_operation

{{ success: true, model: "Transport Study",
   drum_band: "#{{{DRUM_Z0}}}..#{{{DRUM_Z1}}}",
   rail_window: "#{{{WIN_Z0}}}..#{{{WIN_Z1}}}",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }}.to_json
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TBS-001 transport-clearance study model")
    parser.add_argument("--save", action="store_true", help="Write Ruby to transport-study.rb")
    parser.add_argument("--send", action="store_true", help="Send to running SketchUp")
    parser.add_argument("--skp", action="store_true", help="After --send, save models/transport-study.skp")
    args = parser.parse_args()

    ruby = generate_ruby()

    if args.save:
        out = os.path.join(os.path.dirname(__file__), "transport-study.rb")
        with open(out, "w") as f:
            f.write(ruby)
        print(f"  {out} saved ({len(ruby)} bytes)")

    if args.send:
        from sketchup_client import send_ruby, SketchupError
        try:
            print(f"  SketchUp: {send_ruby(ruby, timeout=180.0)}")
        except SketchupError as e:
            print(f"  error: {e}", file=sys.stderr)
            sys.exit(1)

    if args.skp:
        if not args.send:
            print("  --skp requires --send", file=sys.stderr)
            sys.exit(1)
        from sketchup_client import send_ruby
        skp = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "models", "transport-study.skp"))
        print(f"  saving {skp} ...")
        print("  " + send_ruby('m=Sketchup.active_model; "saved=#{m.save(' + repr(skp) + ')}"'))
