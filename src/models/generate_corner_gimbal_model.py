#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""Generate the film-plane CORNER MECHANISM SketchUp model — COMBINED four-corner view.

Shows the WHOLE film plane with all FOUR corners + the pinhole, so tilt and swing read together:

    pinhole (far wall, Y=0) ← throw → film plane (4499 × ~2088, at depth Y=2262)
    four corners TL / TR / BL / BR, each a slide-and-clamp stack:
        DEPTH slide (Y)      — the drive: a top↔bottom depth diff = TILT, a left↔right diff = SWING
        VERTICAL slide (Z)   — absorbs the TILT foreshortening
        HORIZONTAL slide (X) — absorbs the SWING foreshortening
        U-JOINT (Ruland US12-6-6-SS) — tilt + swing, twist locked
    A light cone from the pinhole to the four corners shows the plane faces the pinhole.

No screws/handwheels — a pinhole's infinite DoF makes this scene control, not focus: push each
slide, cam-clamp to lock. Scenes: Overview (iso) · Tilt (side) · Swing (top) · Corner detail · Labeled.

REUSES generate_sketchup_model.py helpers. Open a NEW blank SketchUp doc before --send.

Usage:
    /usr/bin/python3 src/models/generate_corner_gimbal_model.py --save [--send]
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import generate_sketchup_model as ov          # ruby helpers + component()
import generate_corridor_water_panel as cp    # IBC corridor deep-box frame + tote restraint (beams) — reused verbatim

TAGS = ["Corners", "Film Plane", "Pinhole", "Context", "Labels"]

C_STEEL = "#B0B0B8"; C_CROSS = "#8A8A92"; C_PANEL = "#1F3B66"; C_CAR = "#C04010"
C_FRAME = "#8FB0C8"   # film-plane 2x2 6061 Al angle perimeter frame (the ACM backing is captured in it)
C_TILT = "#2E8B57"   # vertical (Z) slide — TILT accommodation (green)
C_SWING = "#7B5EA7"  # horizontal (X) slide — SWING accommodation (purple)

# real container/film layout (mm) — sourced from tbs_constants via ov (no hardcoded copies)
CH = ov.C_HGT                        # interior height
X_L, X_R = ov.FP_X_L, ov.FP_X_R - 25   # right edge trimmed 25mm (+ a 35mm end-plate trim) to clear the IBC frame → FP_W 4499→4474
FP_Y = ov.FP_Y                       # film depth from the pinhole wall (Y)
PH_X, PH_Z = ov.PH_X, ov.C_HGT // 2  # pinhole X (film-width centre) and Z (mid-height)
# ── 304 U-CHANNEL rails, BOTH 3"×1.5" (McMaster 1262T21, $352/6ft, 0.188" wall) — the deflection is
# ~25× overkill even at 3×1.5, so the 4×2 is unnecessary weight/cost. Wheels ride the OPEN channel;
# the CLOSED web-back is the splice face (one section does the H-bar's two-U job). ──
# BOTTOM = web-VERTICAL: deep dim resists bending; the walkway pins the film bottom so depth is FREE.
#          Wheels on the bottom flange (weight, gravity-seated).
# TOP    = laid FLAT (inverted-U): guide only → minimise the Z footprint → max ceiling / film height.
#          Guide wheels under the web (depth guidance, no weight).
CD_BOT, CW_BOT = 76, 38              # bottom 3×1.5 web-vertical: web depth (Z) × flange (X)
CD_TOP, CW_TOP = 76, 38              # top 3×1.5 laid flat: web width (X) × flange height (Z)
HB_T = 5                             # web/flange wall = 0.188" (4.78mm)
SPLICE_YD = 260                      # removable = 6ft (1830) + 260mm; the length-splice sits at the PINHOLE end
                                     # (Yd~260, shortest-throw = least-travelled) → least chance the trolley rolls it

# ── FILM-PLANE WIDTH INSET — the ghost panel edges land on the CARRIAGE line (inb), NOT the rail line.
# At the rail line (X_L/X_R) the full-height panel skewers the bottom weight beam (which straddles cx by
# ±CW_BOT/2). Pulling each edge inboard to the carriage seats the corner IN its carrier (the frame bracket
# already reaches here) and clears the bottom-beam inboard flange tip by HB_T+... ──
FILM_INSET = CW_BOT / 2 + 14         # 33 — carriage line, inboard of the bottom (weight) beam by 14mm
FCX_L = X_L + FILM_INSET             # 183 — film LEFT edge, seated in the left carrier (clear of the beam)
FCX_R = X_R - FILM_INSET             # 4591 — film RIGHT edge, seated in the right carrier
FP_W_CORNER = FCX_R - FCX_L          # 4408 — active image width once the panel sits in the carriers

# ── vertical layout (mm) — bottom pinned by the walkway; top pinned by the ceiling (flat-guide fit) ──
PZ0 = ov.RAIL_OFF_BOT                # 160 — film BOTTOM edge, ABOVE the Z140 walkway (hard floor, +20mm)
BUILD_BOT = 110                      # bottom channel centre → film-corner stack (weight-bearing carriage)
GUIDE_GAP = 10                       # top guide-follower gap (film top just below the flat guide channel)
PZ_HB_BOT = PZ0 + BUILD_BOT          # 270 — bottom channel WEB-centre (bottom flange @220 clears the deck; film hangs below)
PZ_HB_TOP = ov.C_HGT - CW_TOP // 2 - 6   # top flat-channel centre (just under the ceiling)
PZ1 = PZ_HB_TOP - CW_TOP // 2 - GUIDE_GAP # film TOP edge — held just under the flat guide channel
BUILD = BUILD_BOT                    # (label back-compat)
CZ_F, CZ_C = 15, ov.C_HGT - 15       # (retained only for the faint floor/ceiling context boxes)

# ── LEFT-rail transport split (drop-in). The hinge panel swings about the pivot post (= film far-left post,
# Yd2287) and sweeps the X150 rail line, so the LEFT rail (top + bottom) is a fixed PARKING STUB near the
# pivot + a REMOVABLE section over the swing zone that LIFTS OUT (its welded bridge bears on the stub, held
# by a retaining screw; no floor post at the cut). RIGHT (BR/TR) = flanged wall-to-wall (shares the IBC
# combined corner plate). LEFT_CUT_YD ≈ the panel-swing-envelope edge. ──
LEFT_CUT_YD = 2090                   # cut Yd = the panel-swing envelope edge on the X150 rail (computed); stub = C_WID-2090 = 272mm.
                                     # NB: removable = 0..2090 = 6.86 ft EXCEEDS the 6 ft stock — needs a longer length or a splice.


def channel_v(name, cx, zc, y0, ylen, tag, cin, alpha=None):
    """BOTTOM rail — 304 U-channel stood WEB-VERTICAL (4×2). Web is the OUTBOARD back (splice face);
    the two flanges project INBOARD, forming the wheel channel that opens toward the film. Deep web
    (CD_BOT) resists bending. zc = web-centre Z."""
    P = []
    outx = cx - cin * CW_BOT / 2                    # outboard face
    web_x = min(outx, outx + cin * HB_T)
    fl_x = min(outx, outx + cin * CW_BOT)
    P.append(ov.ruby_box(f"{name} web {tag}", web_x, y0, zc - CD_BOT / 2, HB_T, ylen, CD_BOT, color=C_STEEL, alpha=alpha))
    for fz in (zc + CD_BOT / 2 - HB_T, zc - CD_BOT / 2):
        P.append(ov.ruby_box(f"{name} flange {tag} {int(fz)}", fl_x, y0, fz, CW_BOT, ylen, HB_T, color=C_STEEL, alpha=alpha))
    # inboard LIP on the bottom flange — lateral keeper: stops the load roller walking off in X on swing
    in_edge = cx + cin * CW_BOT / 2
    P.append(ov.ruby_box(f"{name} bottom-flange lip {tag}", min(in_edge, in_edge - cin * 5), y0, zc - CD_BOT / 2 + HB_T, 5, ylen, 9, color=C_STEEL, alpha=alpha))
    return P


def channel_flat(name, cx, zc, y0, ylen, tag, alpha=None):
    """TOP guide rail — 304 U-channel laid FLAT (inverted-U, 3×1.5). Web is the closed TOP (splice face);
    two flanges hang DOWN forming a down-opening channel; the guide wheels run under the web. Short in Z
    (CW_TOP) → minimum ceiling cost. zc = section-centre Z."""
    P = []
    P.append(ov.ruby_box(f"{name} web {tag}", cx - CD_TOP / 2, y0, zc + CW_TOP / 2 - HB_T, CD_TOP, ylen, HB_T, color=C_STEEL, alpha=alpha))
    for fx in (cx - CD_TOP / 2, cx + CD_TOP / 2 - HB_T):
        P.append(ov.ruby_box(f"{name} flange {tag} {int(fx)}", fx, y0, zc - CW_TOP / 2, HB_T, ylen, CW_TOP, color=C_STEEL, alpha=alpha))
    return P


def corner(tag, cx, fz, zc, cin, side):
    """One corner on a 304 U-channel depth rail. BOTTOM = web-vertical 4×2 (weight); TOP = flat 3×1.5 (guide).
      cx = corner X   fz = film-corner Z   zc = rail web-centre Z   cin = +1 (left) / -1 (right)
      side = 'L' drop-in (stub + welded bridge + removable + support + pinhole gusset) / 'R' flanged."""
    P = []
    ty = FP_Y
    xr0 = cx if cin > 0 else cx - 260
    is_bot = fz < ov.C_HGT / 2
    if is_bot:
        rail = lambda nm, y0, yl, al=None: channel_v(nm, cx, zc, y0, yl, tag, cin, al)
        sec_h, chan_w = CD_BOT, CW_BOT
    else:
        rail = lambda nm, y0, yl, al=None: channel_flat(nm, cx, zc, y0, yl, tag, al)
        sec_h, chan_w = CW_TOP, CD_TOP
    botf = zc - sec_h / 2                                # section bottom Z
    splice_z = botf - 12 if is_bot else zc + CW_TOP / 2  # splice on the web-back: bottom under / top over

    # ── U-CHANNEL DEPTH RAIL ──
    if side == "R":                                     # RIGHT: continuous, flanged wall-to-wall (IBC combined plate)
        P += rail("U-rail (FLANGED)", 0, ov.C_WID)
        for fy in (0, ov.C_WID - 12):                    # end plate trimmed 35mm on the OUTBOARD (+X) side to clear the IBC frame
            P.append(ov.ruby_box(f"Rail end flange (outboard-trimmed) {tag} {int(fy)}", cx - 55, fy, botf - 5, 75, 12, sec_h + 10, color=C_CROSS))
    else:                                              # LEFT: parking stub + removable + welded bridge + support + gusset
        P += rail("U-rail STUB (fixed, parks corner)", LEFT_CUT_YD, ov.C_WID - LEFT_CUT_YD)
        P += rail("U-rail REMOVABLE (out for transport)", 0, LEFT_CUT_YD, 0.30)
        # the bridge is WELDED to the REMOVABLE beam and LAPS + BEARS on the stub (weight rides the bridge,
        # not the screw); a retaining SCREW into the STUB just holds it — drops straight in, then lock
        if is_bot:   # bottom: fishplate on the OUTBOARD web face — clear of the inboard carriage
            P.append(ov.ruby_box(f"Welded bridge (welded to REMOVABLE, bears on stub, outboard web) {tag}", cx - cin * (CW_BOT / 2 + 12), LEFT_CUT_YD - 60, botf, 12, 150, CD_BOT, color=C_CROSS))
            P.append(ov.ruby_cylinder(f"Retaining screw (bridge→STUB) {tag}", cx - cin * (CW_BOT / 2 + 22), LEFT_CUT_YD + 45, botf + CD_BOT / 2, 5, 26, color=C_STEEL, axis="x"))
        else:        # top: splice plate over the web (above the mechanism — already clear), flush to the web width
            P.append(ov.ruby_box(f"Welded bridge (welded to REMOVABLE, bears on stub, over web) {tag}", cx - CD_TOP / 2, LEFT_CUT_YD - 60, splice_z, CD_TOP, 150, 12, color=C_CROSS))
            P.append(ov.ruby_cylinder(f"Retaining screw (bridge→STUB) {tag}", cx, LEFT_CUT_YD + 45, splice_z + 4, 5, 26, color=C_STEEL, axis="z"))
        # No floor post at the cut: the stub (Yd LEFT_CUT_YD→C_WID) is anchored at the pivot post (= film
        # far-left post) + the far wall, and the cut is only ~197mm cantilevered from it — the removable's
        # welded bridge BEARS on the stub, whose pivot-post anchor carries the reaction, so a floor post
        # (which would foul the sliding carriage) is unnecessary.
        P.append(ov.ruby_box(f"Rail far flange (pivot post) {tag}", cx - 55, ov.C_WID - 12, botf - 5, 110, 12, sec_h + 10, color=C_CROSS))
        P.append(ov.ruby_box(f"Pinhole-wall gusset/seat {tag}", cx - 56, 0, botf - 30, 112, 45, sec_h + 55, color=C_CROSS))
        # length splice (removable = 6ft + 260mm) at the PINHOLE end — shortest-throw, least-travelled;
        # same outboard-web placement so it's clear of the carriage
        if is_bot:
            P.append(ov.ruby_box(f"Length splice (pinhole end, outboard web) {tag}", cx - cin * (CW_BOT / 2 + 12), SPLICE_YD - 55, botf, 12, 110, CD_BOT, color=C_CROSS))
        else:
            P.append(ov.ruby_box(f"Length splice (pinhole end, over web) {tag}", cx - CD_TOP / 2, SPLICE_YD - 55, splice_z, CD_TOP, 110, 12, color=C_CROSS))

    # ── SKATE (spray-bar carriage pattern): Ø32 acetal wheels IN the channel; the Ø10 axle is
    # cantilevered from the CARRIAGE (inboard) — the axle and its retainer bolts pass through the
    # CARRIAGE PLATE, never the beam. ──
    rz = botf + HB_T + 16 if is_bot else zc + CW_TOP / 2 - HB_T - 16   # wheel-centre Z
    inb = cx + cin * (chan_w / 2 + 14)                   # carriage line — inboard of the channel opening (film side)
    # BOTTOM = Ø32x16 load rollers (weight). TOP = a WIDE Ø32 guide DRUM that nearly spans the flat-channel
    # throat, so BOTH flanges locate it laterally (tight X) — the flat rail's answer to the bottom rail's lip.
    if is_bot:
        rlabel, r_x0, r_len = "Acetal wheel Ø32 (weight)", cx - 8, 16
    else:
        rlabel, r_x0, r_len = "Acetal guide wheel Ø32 (10mm narrower than the yoke; ~5mm clearance each side)", cx - 26, 52
    kx, kz = cx - 6, zc + CD_BOT / 2 - HB_T - 10   # bottom keeper (anti-lift, under the top flange); Ø20 on a stub axle
    for ry in (ty - 30, ty + 14):
        P.append(ov.ruby_cylinder(f"{rlabel} {tag} {int(ry)}", r_x0, ry, rz, 16, r_len, color=C_CAR, axis="x"))
        if is_bot:
            # BOTTOM: the channel opens INBOARD, so the Ø10 axle exits the OPENING to the inboard carriage (correct).
            wax0 = min(r_x0, inb - 6)
            P.append(ov.ruby_cylinder(f"Wheel axle Ø10 {tag} {int(ry)}", wax0, ry, rz, 5, max(r_x0 + r_len, inb + 6) - wax0, color=C_CROSS, axis="x"))
            # keeper roller (anti-lift, under the top flange) + its stub axle to the carriage
            P.append(ov.ruby_cylinder(f"Keeper roller Ø20 (anti-lift) {tag} {int(ry)}", kx, ry, kz, 10, 12, color=C_CAR, axis="x"))
            P.append(ov.ruby_cylinder(f"Keeper axle Ø8 {tag} {int(ry)}", min(kx, inb), ry, kz, 4, abs(inb - kx) + 10, color=C_CROSS, axis="x"))
        else:
            # TOP: the channel opens DOWN, so the axle stays WITHIN the throat (Ø10, spanning the drum);
            # the yoke below grabs its ends — it never crosses a flange.
            P.append(ov.ruby_cylinder(f"Guide axle Ø10 (in throat) {tag} {int(ry)}", cx - 33, ry, rz, 5, 66, color=C_CROSS, axis="x"))
    if not is_bot:
        # TOP YOKE — the carriage extends UP through the channel OPENING (past the lips): two arms grab the
        # guide-axle ends (free space between the narrow wheel and each arm) + bear the flanges (lateral X)
        # + hook the lips (anti-drop). A cross-piece JOINS the two arms into ONE part below the opening;
        # a rail then runs inboard to the carriage plate. The axle never pierces a flange.
        yb = zc - CW_TOP / 2                                   # channel opening (flange-lip Z)
        for ax_x in (cx - 33, cx + 33):
            P.append(ov.ruby_box(f"Yoke arm + lip hook (thru opening) {tag} {int(ax_x)}", ax_x - 2, ty - 34, yb - 14, 4, 68, rz - (yb - 14), color=C_CAR))
        P.append(ov.ruby_box(f"Yoke cross-piece (joins the two arms) {tag}", cx - 35, ty - 34, yb - 22, 70, 68, 8, color=C_CAR))
        P.append(ov.ruby_box(f"Yoke rail (→ inboard carriage) {tag}", min(cx + 33, inb), ty - 34, yb - 20, abs(inb - (cx + 33)) + 6, 68, 6, color=C_CAR))
    # carriage plate on the axle ends + axle-retainer bolts DOWN THROUGH THE PLATE (saddle-clamp, not the beam).
    # Spans the FULL Z of film-corner / load-roller / KEEPER-roller so every axle lands on it (keeper included).
    zlo, zhi = min(fz, rz, kz), max(fz, rz, kz)
    P.append(ov.ruby_box(f"Carriage plate (bolted to skate axles) {tag}", inb - 6, ty - 40, zlo - 6, 14, 80, (zhi - zlo) + 24, color=C_CAR))
    for ry in (ty - 30, ty + 14):
        P.append(ov.ruby_cylinder(f"Axle retainer bolt (thru plate) {tag} {int(ry)}", inb, ry, rz - 22, 2.5, 44, color=C_CROSS, axis="z"))

    # ── mechanism, inboard: Z slide (tilt) → X slide (swing) → U-joint → the FILM-PLANE CORNER ──
    P.append(ov.ruby_box(f"Vertical Z slide rail (TILT, green) {tag}", inb - 3, ty - 9, min(fz, rz) - 4, 16, 18, abs(rz - fz) + 20, color=C_TILT))
    P.append(ov.ruby_box(f"Horizontal X slide rail (SWING, purple) {tag}", xr0, ty - 7, fz - 4, 260, 14, 14, color=C_SWING))
    P.append(ov.ruby_box(f"U-joint {tag}", cx - 12, ty - 12, fz - 14, 24, 24, 24, color=C_CROSS))
    # FILM-PLANE FRAME CORNER — bolts onto the U-joint, so the ghost panel is carried by this corner.
    # Kept INBOARD of the web (outboard edge at the web inboard face) so the beam-flush cut support clears it.
    ybk = min(ty - 8, FP_Y - 4)
    fbx = cx - cin * (CW_BOT / 2 - HB_T)                 # web inboard face = the moving assembly's outboard limit
    P.append(ov.ruby_box(f"Frame corner L-bracket (6061 Al anodized, expendable — angle frame → U-joint) {tag}", min(fbx, fbx + cin * 48), ybk, fz - 26, 48, (FP_Y + 8) - ybk, 52, color=C_STEEL))
    # the film-frame angle CORNER bolts onto this bracket → the ACM is carried ACM → angle frame → bracket → U-joint
    fcx = cx + cin * FILM_INSET                          # film-plane corner (frame heel)
    P.append(ov.ruby_cylinder(f"Frame-corner bolt (angle frame → bracket) {tag}", fcx, FP_Y - 6, fz, 3, 18, color=C_STEEL, axis="y"))
    return "\n".join(P)


def corners():
    P = [
        corner("BL", X_L, PZ0, PZ_HB_BOT, +1, "L"),   # bottom-left  — 4×2 web-vertical (weight), drop-in
        corner("BR", X_R, PZ0, PZ_HB_BOT, -1, "R"),   # bottom-right — 4×2 web-vertical (weight), flanged (IBC plate)
        corner("TL", X_L, PZ1, PZ_HB_TOP, +1, "L"),   # top-left     — 3×1.5 flat guide, drop-in
        corner("TR", X_R, PZ1, PZ_HB_TOP, -1, "R"),   # top-right    — 3×1.5 flat guide, flanged
    ]
    # faint floor + ceiling so the UPPER (ceiling) and LOWER (floor) rails read as mounted structure
    P.append(ov.ruby_box("Floor", X_L - 250, 0, -12, (X_R - X_L) + 500, FP_Y + 250, 12, color=C_STEEL, alpha=0.05))
    P.append(ov.ruby_box("Ceiling", X_L - 250, 0, CH, (X_R - X_L) + 500, FP_Y + 250, 12, color=C_STEEL, alpha=0.05))
    return "\n".join(P)


def film_plane():
    # The film plane is NOT a bare sheet butted to the corner brackets. It is a rigid ACM BACKING captured in a
    # 2x2 6061 Al angle PERIMETER FRAME (anodized 6061-T6, 2"×2"×3/16" — an EXPENDABLE part; anodized Al in the
    # splash-not-immersed cyanotype zone, replaced on pitting, chosen over 304 SS for weight + cost):
    # the ACM seats against the frame's in-plane leg; the muslin wraps + clamps to the perp leg (Sheet 6); and
    # the frame's four CORNERS bolt onto the frame
    # corner brackets — which carry it through the U-joint to the cross-slides. So the load path is
    # ACM → angle frame → corner bracket → U-joint, never a butt joint.
    AL, AT = 50, 5                                # 2x2 angle leg / wall
    yperp = FP_Y - AL                             # perp leg projects toward the pinhole (muslin side)
    yin = FP_Y - AT                               # in-plane leg lies against the ACM front face
    P = [
        # ACM rigid backing (ghost), seated against the frame in-plane leg
        ov.ruby_box("Film-plane ACM backing (ghost)", FCX_L, FP_Y, PZ0, FP_W_CORNER, 4, PZ1 - PZ0,
                    color=C_PANEL, alpha=0.14),
        # 2x2 6061 Al angle perimeter frame — top / bottom (perp leg + in-plane leg = an L)
        ov.ruby_box("Film frame 2x2 6061 Al angle — top (perp leg / muslin clamp)", FCX_L, yperp, PZ1 - AT, FP_W_CORNER, AL, AT, color=C_FRAME),
        ov.ruby_box("Film frame 2x2 6061 Al angle — top (in-plane leg / ACM seat)", FCX_L, yin, PZ1 - AL, FP_W_CORNER, AT, AL, color=C_FRAME),
        ov.ruby_box("Film frame 2x2 6061 Al angle — bottom (perp leg / muslin clamp)", FCX_L, yperp, PZ0, FP_W_CORNER, AL, AT, color=C_FRAME),
        ov.ruby_box("Film frame 2x2 6061 Al angle — bottom (in-plane leg / ACM seat)", FCX_L, yin, PZ0, FP_W_CORNER, AT, AL, color=C_FRAME),
        # left / right
        ov.ruby_box("Film frame 2x2 6061 Al angle — left (perp leg / muslin clamp)", FCX_L, yperp, PZ0, AT, AL, PZ1 - PZ0, color=C_FRAME),
        ov.ruby_box("Film frame 2x2 6061 Al angle — left (in-plane leg / ACM seat)", FCX_L, yin, PZ0, AL, AT, PZ1 - PZ0, color=C_FRAME),
        ov.ruby_box("Film frame 2x2 6061 Al angle — right (perp leg / muslin clamp)", FCX_R - AT, yperp, PZ0, AT, AL, PZ1 - PZ0, color=C_FRAME),
        ov.ruby_box("Film frame 2x2 6061 Al angle — right (in-plane leg / ACM seat)", FCX_R - AL, yin, PZ0, AL, AT, PZ1 - PZ0, color=C_FRAME),
    ]
    return "\n".join(P)


def pinhole():
    P = [
        ov.ruby_box("Pinhole wall (far)", 0, -14, 0, 5893, 14, CH, color=C_STEEL, alpha=0.06),
        ov.ruby_box("Pinhole aperture", PH_X - 11, -18, PH_Z - 11, 22, 22, 22, color="#101014"),
    ]
    corners_xyz = [(FCX_L, PZ1), (FCX_R, PZ1), (FCX_L, PZ0), (FCX_R, PZ0)]
    rays = "\n".join(
        f'  ents.add_edges(Geom::Point3d.new({ov.mm(PH_X)}, {ov.mm(0)}, {ov.mm(PH_Z)}), '
        f'Geom::Point3d.new({ov.mm(x)}, {ov.mm(FP_Y)}, {ov.mm(z)}))'
        for x, z in corners_xyz)
    P.append("  # light cone — pinhole → 4 panel corners\n" + rays + "\n")
    return "\n".join(P)


def labels():
    L = []
    def txt(s, x, y, z, vx, vy, vz):
        L.append(f'''
tt = entities.add_text("{s}", Geom::Point3d.new({ov.mm(x)}, {ov.mm(y)}, {ov.mm(z)}), Geom::Vector3d.new({ov.mm(vx)}, {ov.mm(vy)}, {ov.mm(vz)}))
tt.layer = model.layers["Labels"] rescue nil''')
    txt("PINHOLE (far wall) — the film plane faces it across the throw", PH_X, 0, PH_Z, 60, -50, 30)
    txt(f"Film plane {FP_W_CORNER} x {PZ1 - PZ0} (edges seated in the carriers; bottom @Z{PZ0} above walkway, weight on the bottom rail; top = light guide only)", 2400, FP_Y, PH_Z, 60, 45, 20)
    txt("TOP pair vs BOTTOM pair depth = TILT", X_L, FP_Y, CH, -60, -40, 30)
    txt("LEFT pair vs RIGHT pair depth = SWING", X_R, FP_Y, PZ0, 60, 40, -20)
    txt("UPPER rails (ceiling) — TOP corners hang (tension)", 2400, FP_Y - 350, CH, 45, -40, 12)
    txt("LOWER rails (floor) — BOTTOM corners bear (compression)", 2400, FP_Y - 350, 0, 45, -40, -12)
    # one corner (BL) annotated with the three slides + joint
    txt("DEPTH slide (Y, GREY) — drives tilt + swing", X_L, FP_Y - 300, PZ0 - 40, -55, -40, -10)
    txt("VERTICAL slide (Z, GREEN) — absorbs TILT", X_L - 30, FP_Y, PZ0 + 20, -60, -40, 10)
    txt("HORIZONTAL slide (X, PURPLE) — absorbs SWING", X_L + 120, FP_Y, PZ0 + 10, 55, -40, 5)
    txt("U-joint (tilt + swing, twist locked)", X_L, FP_Y - 12, PZ0, -55, -45, 15)
    return "\n".join(L)


def context():
    """The real supports the corner mechanism lands on — reused verbatim from the overview
    (same global coords): the perimeter walkway (its Z140 deck is the hard floor under the
    bottom edge), the right-walkway cantilever + IBC-corridor cantilever arms, the IBC deep-box
    restraint frame (beams). Lets the corner be judged against its real clearances (esp. the
    walkway hard floor at the bottom) instead of in isolation. Totes omitted — frame/beams only."""
    def s(x):
        return x if isinstance(x, str) else "\n".join(x)
    return "\n".join([
        s(ov.walkways(include_right=True, include_right_hangers=False)),  # decks + right cantilever + IBC arms
        s(ov.fp_combined_corner_plates()),                               # BR rail + right-beam combined plates
        s(cp.frame()),                                                   # IBC corridor deep-box frame (beams)
        s(cp.tote_restraint()),                                          # IBC tote restraint (beams)
    ])


def generate_ruby():
    comps = [
        ov.component("Corners", "Corners", corners()),
        ov.component("Film Plane", "Film Plane", film_plane()),
        ov.component("Pinhole", "Pinhole", pinhole()),
        ov.component("Context (walkway + IBC cantilever/beams)", "Context", context()),
    ]
    body = "\n".join(comps)
    tags_ruby = "\n".join(f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep = "[" + ", ".join(f'"{t}"' for t in TAGS) + "]"
    show = ["Corners", "Film Plane", "Pinhole"]
    show_ctx = show + ["Context"]
    # Overview (with context) FIRST, then the zoomed corner detail; side/top + Labeled added after.
    iso = [
        ("Overview", show_ctx, (2400, FP_Y - 700, CH / 2, 9500)),
        ("Corner detail", show, (X_L, FP_Y, PZ0 + 30, 620)),
    ]

    def scene_lit(n, tags, tgt):
        tg = "[" + ", ".join(f'"{t}"' for t in tags) + "]"
        cam = f"[{ov.mm(tgt[0])}, {ov.mm(tgt[1])}, {ov.mm(tgt[2])}, {ov.mm(tgt[3])}]"
        return f'["{n}", {tg}, {cam}]'
    iso_ruby = "[" + ", ".join(scene_lit(*s) for s in iso) + "]"
    show_ruby = "[" + ", ".join(f'"{t}"' for t in show) + "]"
    lbl_show_ruby = "[" + ", ".join(f'"{t}"' for t in show + ["Labels"]) + "]"

    return f'''# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/generate_corner_gimbal_model.py — do not edit this .rb directly.
model = Sketchup.active_model
model.start_operation("Film-Plane Corner Mechanism", true)
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

{body}

# ── "Labeled" callouts (Labels tag) ──
{labels()}

{ov.license_note()}

model.definitions.purge_unused
model.materials.purge_unused

keep_tags = {keep}
default_layer = model.layers[0]
model.layers.to_a.each {{ |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}}

# ── iso scenes (Overview [with context] / Corner detail) ──
{iso_ruby}.each {{ |name, tags, tgt|
  model.layers.each {{ |l| l.visible = (l == default_layer || tags.include?(l.name)) }}
  t = Geom::Point3d.new(tgt[0], tgt[1], tgt[2])
  cdir = Geom::Vector3d.new(0.5, -0.7, 0.4); cdir.normalize!
  model.active_view.camera = Sketchup::Camera.new(t.offset(cdir, tgt[3]), t, Z_AXIS)
  page = model.pages.add(name)
  page.use_camera = true
}}

# ── Tilt (side) — look along +X at the left edge: depth (Y) horizontal, height (Z) vertical ──
model.layers.each {{ |l| l.visible = (l == default_layer || {show_ruby}.include?(l.name)) }}
tc = Geom::Point3d.new({ov.mm(X_L)}, {ov.mm(FP_Y)}, {ov.mm(CH/2)})
te = Geom::Point3d.new({ov.mm(X_L - 4200)}, {ov.mm(FP_Y)}, {ov.mm(CH/2)})
model.active_view.camera = Sketchup::Camera.new(te, tc, Z_AXIS)
ps = model.pages.add("Tilt (side)"); ps.use_camera = true

# ── Swing (top) — top-down over the pinhole→panel span: width (X) and depth (Y) ──
sc = Geom::Point3d.new({ov.mm(PH_X)}, {ov.mm(FP_Y/2)}, 0)
se = Geom::Point3d.new({ov.mm(PH_X)}, {ov.mm(FP_Y/2)}, {ov.mm(9500)})
model.active_view.camera = Sketchup::Camera.new(se, sc, Y_AXIS)
ps2 = model.pages.add("Swing (top)"); ps2.use_camera = true

# ── Labeled (Labels tag) — LAST scene ──
model.layers.each {{ |l| l.visible = (l == default_layer || {lbl_show_ruby}.include?(l.name)) }}
lc = Geom::Point3d.new({ov.mm(2400)}, {ov.mm(FP_Y - 400)}, {ov.mm(CH/2)})
ldir = Geom::Vector3d.new(0.5, -0.7, 0.4); ldir.normalize!
model.active_view.camera = Sketchup::Camera.new(lc.offset(ldir, {ov.mm(7200)}), lc, Z_AXIS)
pl = model.pages.add("Labeled"); pl.use_camera = true

model.layers.each {{ |l| l.visible = true }}

model.commit_operation
{{ success: true, model: "Film-Plane Corner Mechanism",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }}.to_json
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate the film-plane combined corner mechanism model")
    parser.add_argument("--save", action="store_true", help="Write Ruby to src/models/corner-gimbal.rb")
    parser.add_argument("--send", action="store_true", help="Send to the ACTIVE SketchUp doc (open a NEW doc first)")
    args = parser.parse_args()

    ruby = generate_ruby()
    if args.save:
        out = os.path.join(os.path.dirname(__file__), "corner-gimbal.rb")
        with open(out, "w") as f:
            f.write(ruby)
        print(f"  {out} saved ({len(ruby)} bytes)")
    if args.send:
        from sketchup_client import send_ruby, SketchupError
        try:
            print(f"  SketchUp: {send_ruby(ruby)}")
        except SketchupError as e:
            print(f"  error: {e}", file=sys.stderr)
            sys.exit(1)
    if not args.save and not args.send:
        print(ruby)
