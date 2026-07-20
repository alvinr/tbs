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
        U-JOINT (Ruland USKC12-6-6-SS) — tilt + swing, twist locked
    A light cone from the pinhole to the four corners shows the plane faces the pinhole.

No screws/handwheels — a pinhole's infinite DoF makes this scene control, not focus: push each
slide, cam-clamp to lock. Scenes: Overview (iso) · Tilt (side) · Swing (top) · Corner detail · Labeled.

REUSES generate_sketchup_model.py helpers. Open a NEW blank SketchUp doc before --send.

Usage:
    /usr/bin/python3 src/models/generate_film_plane_mechanism_model.py --save [--send]
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import generate_sketchup_model as ov          # ruby helpers + component()
import generate_corridor_water_panel as cp    # IBC corridor deep-box frame + tote restraint (beams) — reused verbatim

TAGS = ["Corners", "Film Plane", "Pinhole", "Context", "Movement", "Labels"]

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
PZ_HB_TOP = ov.C_HGT - CW_TOP // 2 - 50  # top flat-channel centre — lowered so the on-top rail fittings
                                         # (bridge/splice/pinhole-wall gusset) clear the ceiling by 25mm
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
        if is_bot:   # bottom: cut BRIDGE ON TOP (gravity-held) + a locating PIN (flush to rail underside) + a short bottom support bridge
            P.append(ov.ruby_box(f"Welded bridge (welded to REMOVABLE, bears on stub, ON TOP) {tag}", cx - CW_BOT / 2, LEFT_CUT_YD - 60, zc + CD_BOT / 2, CW_BOT, 150, 12, color=C_CROSS))
            # locating pin — drops through the bridge + top flange; BOTTOM flush to the TOP OF THE INNER RAIL
            # (underside of the top flange = zc + CD_BOT/2 - HB_T), head shown on top
            P.append(ov.ruby_cylinder(f"Locating pin (bridge↔STUB, flush to inner-rail top) {tag}", cx, LEFT_CUT_YD + 45, zc + CD_BOT / 2 - HB_T, 5, HB_T + 12, color=C_STEEL, axis="z"))
            # short bottom support bridge welded to the STUB, laps under + carries the removable beam (~64mm)
            P.append(ov.ruby_box(f"Bottom support bridge (STUB → beam underside) {tag}", cx - CW_BOT / 2, LEFT_CUT_YD - 32, botf - 12, CW_BOT, 64, 12, color=C_CROSS))
        else:        # top: splice plate over the web; locating pin FLUSH with the bridge top (not proud)
            P.append(ov.ruby_box(f"Welded bridge (welded to REMOVABLE, bears on stub, over web) {tag}", cx - CD_TOP / 2, LEFT_CUT_YD - 60, splice_z, CD_TOP, 150, 12, color=C_CROSS))
            P.append(ov.ruby_cylinder(f"Locating pin (bridge↔STUB, flush) {tag}", cx, LEFT_CUT_YD + 45, splice_z - HB_T, 5, HB_T + 12, color=C_STEEL, axis="z"))
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
    for ry in (ty + 8, ty + 48):
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
    # Spans the film-corner / load-roller (/ keeper on the bottom) so every axle lands on it. kz is the
    # BOTTOM keeper only — exclude it at the top. TOP corners: cap the plate top 25mm below the ceiling.
    zvals = (fz, rz, kz) if is_bot else (fz, rz)
    zlo, zhi = min(zvals), max(zvals)
    plate_top = min(zhi + 18, ov.C_HGT - 25)
    P.append(ov.ruby_box(f"Carriage plate (bolted to skate axles) {tag}", inb - 6, ty + 1, zlo - 6, 14, 86, plate_top - (zlo - 6), color=C_CAR))
    for ry in (ty + 8, ty + 48):
        blen = min(44, plate_top - (rz - 22))                 # keep the retainer bolt within the (capped) plate
        P.append(ov.ruby_cylinder(f"Axle retainer bolt (thru plate) {tag} {int(ry)}", inb, ry, rz - 22, 2.5, blen, color=C_CROSS, axis="z"))

    # ── mechanism, inboard: Z slide (tilt) → X slide (swing) → U-joint → the FILM-PLANE CORNER ──
    # The cross-slides sit on the BACKING side of the film plane (Yd > FP_Y) so the frame SITS ON them — the
    # muslin-clamp perp leg projects the other way (toward the pinhole), so nothing is drawn through the slides.
    P.append(ov.ruby_box(f"Vertical Z slide rail (TILT, green) {tag}", inb - 3, ty + 1, min(fz, rz) - 4, 16, 18, abs(rz - fz) + 20, color=C_TILT))
    P.append(ov.ruby_box(f"Horizontal X slide rail (SWING, purple) {tag}", xr0, ty + 1, fz - 4, 260, 14, 14, color=C_SWING))
    P.append(ov.ruby_box(f"U-joint (Ruland USKC12-6-6-SS, keyway+clamp) {tag}", cx - 12, ty - 4, fz - 14, 24, 24, 24, color=C_CROSS))
    # input stub Ø9.5 (3/8") from the X-carriage into the U-joint bore, and the 4040N12 304 shaft
    # support (two-piece clamp) that fixes that stub to the X (swing) slide — Sheet 9 View B.
    stub_x0 = cx + 5 if cin > 0 else cx - 51
    sup_x0  = cx + 26 if cin > 0 else cx - 49
    P.append(ov.ruby_cylinder(f"Input stub 3/8 (X slide → U-joint) {tag}", stub_x0, ty + 8, fz, 4.75, 46, color=C_STEEL, axis="x"))
    P.append(ov.ruby_box(f"4040N12 304 shaft support (clamps input stub → X slide) {tag}", sup_x0, ty - 1, fz - 11, 23, 18, 22, color=C_STEEL))
    # output stub Ø9.5 (U-joint 2nd bore → 304 SS corner plate), secured by a countersunk cap screw (Sheet 9 B, J4)
    P.append(ov.ruby_cylinder(f"Output stub 3/8 (U-joint → corner plate) {tag}", cx, ty - 14, fz, 4.75, 20, color=C_STEEL, axis="y"))
    # FILM-PLANE FRAME CORNER — bolts onto the U-joint, so the ghost panel is carried by this corner.
    # Kept INBOARD of the web (outboard edge at the web inboard face) so the beam-flush cut support clears it.
    ybk = min(ty - 8, FP_Y - 4)
    fbx = cx - cin * (CW_BOT / 2 - HB_T)                 # web inboard face = the moving assembly's outboard limit
    # Corner plate reduced (was 48×52); on the BOTTOM corners its floor is held 25mm above the walkway top
    _walk_top = ov.RAIL_OFF_BOT - 20                       # walkway (hard-floor) top = Z140
    plate_z0 = (_walk_top + 25) if is_bot else (fz - 14)   # bottom: 25mm clearance to the walkway
    P.append(ov.ruby_box(f"Corner plate 304 SS (U-joint mount — angle frame → U-joint) {tag}", min(fbx, fbx + cin * 34), ybk, plate_z0, 34, (FP_Y + 8) - ybk, 40, color=C_STEEL))
    # the film-frame angle CORNER bolts onto this 304 SS plate → the ACM is carried ACM → angle frame → 304 SS corner plate → U-joint
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
    # the ACM seats against the frame's in-plane leg; the muslin is clamped onto the ACM by spring clips on the upstand (Sheet 6); and
    # the frame's four CORNERS bolt onto the frame
    # 304 SS corner plates — which carry it through the U-joint to the cross-slides. So the load path is
    # ACM → angle frame → 304 SS corner plate → U-joint, never a butt joint. The corner plate is STEEL
    # (not the expendable 6061 angle): the U-joint funnels the corner load into a few bolts, too concentrated
    # for aluminum — 304 SS for strength + a galvanic/wet-zone match to the 303 SS U-joint.
    AL, AT = 50, 5                                # 2x2 angle leg / wall
    yperp = FP_Y - AL                             # perp leg projects toward the pinhole (muslin side)
    yin = FP_Y - AT                               # in-plane leg lies against the ACM front face
    P = [
        # ACM rigid backing (ghost), seated against the frame in-plane leg
        ov.ruby_box("Film-plane ACM backing (ghost)", FCX_L, FP_Y, PZ0, FP_W_CORNER, 4, PZ1 - PZ0,
                    color=C_PANEL, alpha=0.14),
        # 2x2 6061 Al angle perimeter frame — top / bottom (perp leg + in-plane leg = an L)
        ov.ruby_box("Film frame 2x2 6061 Al angle — top (upstand / muslin spring clip)", FCX_L, yperp, PZ1 - AT, FP_W_CORNER, AL, AT, color=C_FRAME),
        ov.ruby_box("Film frame 2x2 6061 Al angle — top (in-plane leg / ACM seat)", FCX_L, yin, PZ1 - AL, FP_W_CORNER, AT, AL, color=C_FRAME),
        ov.ruby_box("Film frame 2x2 6061 Al angle — bottom (upstand / muslin spring clip)", FCX_L, yperp, PZ0, FP_W_CORNER, AL, AT, color=C_FRAME),
        ov.ruby_box("Film frame 2x2 6061 Al angle — bottom (in-plane leg / ACM seat)", FCX_L, yin, PZ0, FP_W_CORNER, AT, AL, color=C_FRAME),
        # left / right
        ov.ruby_box("Film frame 2x2 6061 Al angle — left (upstand / muslin spring clip)", FCX_L, yperp, PZ0, AT, AL, PZ1 - PZ0, color=C_FRAME),
        ov.ruby_box("Film frame 2x2 6061 Al angle — left (in-plane leg / ACM seat)", FCX_L, yin, PZ0, AL, AT, PZ1 - PZ0, color=C_FRAME),
        ov.ruby_box("Film frame 2x2 6061 Al angle — right (upstand / muslin spring clip)", FCX_R - AT, yperp, PZ0, AT, AL, PZ1 - PZ0, color=C_FRAME),
        ov.ruby_box("Film frame 2x2 6061 Al angle — right (in-plane leg / ACM seat)", FCX_R - AL, yin, PZ0, AL, AT, PZ1 - PZ0, color=C_FRAME),
    ]
    return "\n".join(P)


def pinhole():
    # Pinhole WALL removed (2026-07-17) — the full-width ghost plane made orbiting awkward;
    # the aperture marker + light cone still fix the pinhole in space.
    P = [
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
    txt("4040N12 304 shaft support — clamps the input stub to the X (swing) slide", X_L + 40, FP_Y + 8, PZ0 - 8, 55, 45, -14)
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


CORNER_SPEC = {  # cx, zc(rail web Z), fz(film-corner Z), cin(+left/-right), fcx(film corner X), is_bot
    "BL": (X_L, PZ_HB_BOT, PZ0, +1, FCX_L, True),
    "BR": (X_R, PZ_HB_BOT, PZ0, -1, FCX_R, True),
    "TL": (X_L, PZ_HB_TOP, PZ1, +1, FCX_L, False),
    "TR": (X_R, PZ_HB_TOP, PZ1, -1, FCX_R, False),
}
SWING_CORNERS = {"BR", "TR"}  # these demo a SWING (rotz, yaw about the vertical axis) instead of a TILT (rotx)
# Movement is a SCHEMATIC demo scene — the real corners are 4.5 m apart, so the right-side corners are
# DISPLAY-SHIFTED left to sit beside the left ones (reduce the L↔R gap). Edit the target X to taste.
MV_TARGET_X = {"BR": 2200, "TR": 2200}


def movement(corner="BL"):
    """One 'Movement' scene corner — the cross-slide OPERATING on a CLICK.
    PHASE 1 (drive 0->0.5): the carriage rolls FORWARD in Y + the panel TILTS about the U-joint (far edge
    toward the pinhole). PHASE 2 (0.5->1): the U-joint + panel DEPLOY by sliding along the GREEN (Z) slide
    (bottom corners slide UP, top corners slide DOWN). On the Movement tag. Bottom = web-vertical weight
    channel + load rollers; top = flat guide channel + guide drum & yoke. Panel/tilt mirror by corner.
    Returns (static, carriage, float, panel, pivot, dy_fwd, deploy, tilt, anchor)."""
    ty = FP_Y
    AL, AT = 50, 5                                     # 2x2 angle leg / wall (match film_plane())
    yperp, yin = FP_Y - AL, FP_Y - AT                  # perp leg (muslin side) / in-plane leg (ACM seat)
    plen = 720
    dy_fwd = 320
    cx, zc, fz, cin, fcx, is_bot = CORNER_SPEC[corner]
    xdisp = (MV_TARGET_X[corner] - cx) if corner in MV_TARGET_X else 0   # schematic display shift (reduce L↔R gap)
    cx += xdisp
    fcx += xdisp
    sz = 1 if is_bot else -1
    swing_corner = corner in SWING_CORNERS             # SWING (rotz yaw) vs TILT (rotx) demo
    rot_attr = "rotz" if swing_corner else "rotx"
    rot_val = 30 if swing_corner else sz * 30          # PHASE 1 far edge toward the pinhole (-Y)
    # DEPLOY (phase 2) rides the slide MATCHING the rotation: TILT → GREEN Z (bottom up / top down);
    # SWING → PURPLE X, INBOARD (toward centre, AWAY from the corner beam) so the ACM never drives THROUGH
    # the beam (the bottom weight beam overlaps the ACM in Z; only an inboard shift keeps it clear).
    deploy = (cin * 300) if swing_corner else (sz * 300)
    # tilt about the U-JOINT CENTRE (not the film corner) so the frame + corner plate stay JOINED through the
    # tilt. U-joint box = (cx-12, ty-4, fz-14, 24³) → centre = (cx, ty+8, fz-2).
    pivot = (cx, ty + 8, fz - 2)
    px, py, pz = pivot
    chan_w = CW_BOT if is_bot else CD_TOP
    inb = cx + cin * (chan_w / 2 + 14)                 # carriage line — inboard of the channel opening
    rz = (zc - CD_BOT / 2 + HB_T + 16) if is_bot else (zc + CW_TOP / 2 - HB_T - 16)   # wheel-centre Z
    gx0 = (inb - 3) if cin > 0 else (inb - 13)         # green Z-slide min-x (≈centred on inb)
    cpx0c = (inb - 6) if cin > 0 else (inb - 8)        # carriage-plate min-x
    # DEPLOY rail (long, in the CARRIAGE) + the PERPENDICULAR slide stub (short, in the FLOAT — rides along)
    if swing_corner:   # PURPLE X = deploy rail (LOCAL slide-and-clamp, per Sheet 2 — NOT beam-spanning);
        # GREEN Z = short stub. Per Sheet 2 View B the X cross-slide is a foreshortening absorber at the
        # corner, so it stays inboard of / at the corner and does NOT cross the beam. Deploy INBOARD keeps
        # the ACM clear of the corner beam.
        Lx = abs(deploy) + 60                          # local purple rail, longer than the stroke
        px0 = (cx - 20) if cin > 0 else (cx + 20 - Lx)
        deploy_rail = ov.ruby_box(f"Horizontal X slide rail (SWING/deploy, purple) (Movement {corner})", px0, ty + 1, fz - 4, Lx, 14, 14, color=C_SWING)
        perp_stub = ov.ruby_box(f"Vertical Z slide stub (TILT, green) (Movement {corner})", gx0, ty + 1, min(fz, rz) - 4, 16, 18, abs(rz - fz) + 20, color=C_TILT)
    else:              # GREEN Z = deploy rail; PURPLE X = short stub
        Ldep = abs(deploy) + 60                        # green rail longer than the Z stroke (U-joint stays ON it)
        gz0 = (fz - 20) if deploy > 0 else (fz + 20 - Ldep)
        deploy_rail = ov.ruby_box(f"Vertical Z slide rail (TILT/deploy, green) (Movement {corner})", gx0, ty + 1, gz0, 16, 18, Ldep, color=C_TILT)
        perp_stub = ov.ruby_box(f"Horizontal X slide stub (SWING, purple) (Movement {corner})", cx - 70, ty + 1, fz - 4, 140, 14, 14, color=C_SWING)
    # ── STATIC rail + CARRIAGE (skate + plate + the GREEN Z deploy rail) ──
    carr = []
    if is_bot:
        static_ruby = "\n".join(channel_v(f"U-channel rail (Movement {corner})", cx, zc, ty - 160, 960, f"Move{corner}", cin))
        for ry in (ty + 8, ty + 48):
            carr.append(ov.ruby_cylinder(f"Acetal skate wheel Ø32 (Movement {corner}) {int(ry)}", cx - 8, ry, rz, 16, 16, color=C_CAR, axis="x"))
        carr.append(ov.ruby_box(f"Carriage plate (Movement {corner})", cpx0c, ty + 1, fz - 6, 14, 86, (rz + 46) - (fz - 6), color=C_CAR))
    else:
        yb = zc - CW_TOP / 2                            # channel opening (flange-lip Z)
        zlo, zhi = min(fz, rz), max(fz, rz)
        static_ruby = "\n".join(channel_flat(f"U-channel rail (Movement {corner})", cx, zc, ty - 160, 960, f"Move{corner}"))
        for ry in (ty + 8, ty + 48):
            carr.append(ov.ruby_cylinder(f"Acetal guide wheel Ø32 (Movement {corner}) {int(ry)}", cx - 26, ry, rz, 16, 52, color=C_CAR, axis="x"))
        for ax_x in (cx - 33, cx + 33):                # yoke arms reach DOWN through the opening to the carriage
            carr.append(ov.ruby_box(f"Yoke arm (Movement {corner}) {int(ax_x)}", ax_x - 2, ty - 34, yb - 14, 4, 68, rz - (yb - 14), color=C_CAR))
        carr.append(ov.ruby_box(f"Yoke cross-piece (Movement {corner})", cx - 35, ty - 34, yb - 22, 70, 68, 8, color=C_CAR))
        carr.append(ov.ruby_box(f"Yoke rail → carriage (Movement {corner})", min(cx + 33, inb), ty - 34, yb - 20, abs(inb - (cx + 33)) + 6, 68, 6, color=C_CAR))
        carr.append(ov.ruby_box(f"Carriage plate (Movement {corner})", cpx0c, ty + 1, zlo - 6, 14, 86, (zhi + 18) - (zlo - 6), color=C_CAR))
    # the DEPLOY rail (long) is fixed to the carriage; the U-joint rides it in phase 2
    carr.append(deploy_rail)
    # FLOAT (perpendicular slide stub + U-joint) — DEPLOYS along the deploy rail, carrying the panel
    floatp = [
        perp_stub,
        ov.ruby_box(f"U-joint (Ruland USKC12-6-6-SS) (Movement {corner})", cx - 12, ty - 4, fz - 14, 24, 24, 24, color=C_CROSS),
    ]
    # PANEL (corner plate + frame + ACM) — relative to the U-joint-centre pivot so it TILTS about the U-joint;
    # the 304 corner plate lives HERE (not the float) so it stays bolted to the frame through the tilt.
    ax0 = fcx if cin > 0 else fcx - plen              # panel-body X min (grows inboard from the corner)
    az0 = fz if is_bot else fz - plen                 # panel-body Z min (grows into the film from the corner)
    hz_up = fz if is_bot else fz - AT                 # horizontal-leg (upstand / in-plane) Z, at the corner edge
    hz_in = fz if is_bot else fz - AL
    vx_up = fcx if cin > 0 else fcx - AT              # vertical-leg (upstand / in-plane) X, at the corner edge
    vx_in = fcx if cin > 0 else fcx - AL
    cpx0 = (cx - 14) if cin > 0 else (cx - 20)        # corner-plate X min (mirrors across cx)
    cpz0 = (fz + 5) if is_bot else (fz - 45)          # corner-plate Z min (above the U-joint / below for TR)
    hlbl = "bottom" if is_bot else "top"
    vlbl = "left" if cin > 0 else "right"
    panel = [
        ov.ruby_box(f"304 SS corner plate (Movement {corner})", cpx0 - px, (FP_Y - 8) - py, cpz0 - pz, 34, 16, 40, color=C_STEEL),
        ov.ruby_box(f"ACM film-panel corner — partial ghost (Movement {corner})", ax0 - px, FP_Y - py, az0 - pz, plen, 4, plen, color=C_PANEL, alpha=0.30),
        ov.ruby_box(f"Film frame 2x2 6061 — {hlbl} upstand (Movement {corner})", ax0 - px, yperp - py, hz_up - pz, plen, AL, AT, color=C_FRAME),
        ov.ruby_box(f"Film frame 2x2 6061 — {hlbl} in-plane leg (Movement {corner})", ax0 - px, yin - py, hz_in - pz, plen, AT, AL, color=C_FRAME),
        ov.ruby_box(f"Film frame 2x2 6061 — {vlbl} upstand (Movement {corner})", vx_up - px, yperp - py, az0 - pz, AT, AL, plen, color=C_FRAME),
        ov.ruby_box(f"Film frame 2x2 6061 — {vlbl} in-plane leg (Movement {corner})", vx_in - px, yin - py, az0 - pz, AL, AT, plen, color=C_FRAME),
    ]
    anchor = (cx + cin * 420, ty + 500, fz + sz * 520)
    return static_ruby, "\n".join(carr), "\n".join(floatp), "\n".join(panel), pivot, dy_fwd, deploy, rot_attr, rot_val, anchor


def movement_dc(sfx, carr, floatp, panel, pivot, dy_fwd, deploy, rot_attr, rot_val, anchor):
    """Emit the ONE-click flip DC for a Movement corner (sfx = 'BL'/'TL'/'BR'). One parent DC (Movement<sfx>)
    carries the lone onclick; the driver is RELAYED one level at a time (DC ancestor-refs resolve only ONE
    level up), and the phase gating uses ABS ramps (MIN/MAX are unsupported by the DC formula engine).
    Nesting: Movement<sfx> > Carriage<sfx> (roll Y) > Float<sfx> (DEPLOY along green Z) > PanelTilt<sfx>
    (rot_attr = rotx TILT / rotz SWING)."""
    px, py, pz = pivot
    rot_label = "swing" if rot_attr == "rotz" else "tilt"
    dep_axis = "x" if rot_attr == "rotz" else "z"      # SWING deploys along PURPLE X; TILT along GREEN Z
    dep_color = "purple X" if dep_axis == "x" else "green Z"
    ldx = 300 if sfx[1] == "L" else -300               # L=left → +X, R=right → -X
    ldz = 300 if sfx[0] == "B" else -300               # B=bottom → +Z, T=top → -Z
    return f'''
# ═══ Movement — {sfx} corner: ONE click FLIPS home <-> deployed (roll forward + tilt, then deploy along green Z). ═══
mvpan_{sfx} = model.definitions.add("Panel tilt {sfx}")
ents = mvpan_{sfx}.entities
{panel}
mvfl_{sfx} = model.definitions.add("Float {sfx}")
ents = mvfl_{sfx}.entities
{floatp}
mvpan_{sfx}_inst = mvfl_{sfx}.entities.add_instance(mvpan_{sfx}, Geom::Transformation.translation([{ov.mm(px)}, {ov.mm(py)}, {ov.mm(pz)}]))
mvpan_{sfx}_inst.name = "Panel tilt {sfx}"; mvpan_{sfx}_inst.layer = model.layers["Movement"]
mvo_{sfx} = model.definitions.add("Carriage {sfx}")
ents = mvo_{sfx}.entities
{carr}
mvfl_{sfx}_inst = mvo_{sfx}.entities.add_instance(mvfl_{sfx}, Geom::Transformation.new)
mvfl_{sfx}_inst.name = "Float {sfx}"; mvfl_{sfx}_inst.layer = model.layers["Movement"]
mvp_{sfx} = model.definitions.add("Movement {sfx}")
mvo_{sfx}_inst = mvp_{sfx}.entities.add_instance(mvo_{sfx}, Geom::Transformation.new)
mvo_{sfx}_inst.name = "Carriage {sfx}"; mvo_{sfx}_inst.layer = model.layers["Movement"]
mvp_{sfx}_inst = entities.add_instance(mvp_{sfx}, Geom::Transformation.new)
mvp_{sfx}_inst.name = "Movement {sfx}"; mvp_{sfx}_inst.layer = model.layers["Movement"]
da = "dynamic_attributes"
[mvp_{sfx}, mvp_{sfx}_inst].each do |e|
  e.set_attribute(da, "_name", "Movement{sfx}"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "move", 0.0)
end
mvp_{sfx}_inst.set_attribute(da, "_move_access", "VIEW")
mvp_{sfx}_inst.set_attribute(da, "_move_label", "Flip {sfx}: home <-> deployed (roll + {rot_label}, then deploy along {dep_color})")
mvp_{sfx}_inst.set_attribute(da, "onclick", 'ANIMATE("move", 0, 1)')
mvp_{sfx}_inst.set_attribute(da, "_onclick_access", "NONE")
# carriage rolls FORWARD in Y — PHASE 1 (drive 0->0.5)
[mvo_{sfx}, mvo_{sfx}_inst].each do |e|
  e.set_attribute(da, "_name", "Carriage{sfx}"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "drive", 0.0); e.set_attribute(da, "y", 0.0)
end
mvo_{sfx}_inst.set_attribute(da, "_drive_formula", "Movement{sfx}!move")
mvo_{sfx}_inst.set_attribute(da, "_y_formula", "(drive + 0.5 - ABS(drive - 0.5)) * {dy_fwd}")
# float (U-joint + panel) DEPLOYS by sliding along the {dep_color} slide — PHASE 2 (drive 0.5->1)
[mvfl_{sfx}, mvfl_{sfx}_inst].each do |e|
  e.set_attribute(da, "_name", "Float{sfx}"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "drive", 0.0); e.set_attribute(da, "{dep_axis}", 0.0)
end
mvfl_{sfx}_inst.set_attribute(da, "_drive_formula", "Carriage{sfx}!drive")
mvfl_{sfx}_inst.set_attribute(da, "_{dep_axis}_formula", "(drive - 0.5 + ABS(drive - 0.5)) * {deploy}")
# panel {rot_label}S about the U-joint (rotx=tilt / rotz=swing) — PHASE 1 (drive 0->0.5)
[mvpan_{sfx}, mvpan_{sfx}_inst].each do |e|
  e.set_attribute(da, "_name", "PanelTilt{sfx}"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "drive", 0.0); e.set_attribute(da, "{rot_attr}", 0.0)
end
mvpan_{sfx}_inst.set_attribute(da, "_drive_formula", "Float{sfx}!drive")
mvpan_{sfx}_inst.set_attribute(da, "_{rot_attr}_formula", "(drive + 0.5 - ABS(drive - 0.5)) * {rot_val}")
mvtxt_{sfx} = entities.add_text("CLICK {sfx}: 1) {rot_label} toward pinhole  2) deploy along the {dep_color} slide", Geom::Point3d.new({ov.mm(anchor[0])}, {ov.mm(anchor[1])}, {ov.mm(anchor[2])}), Geom::Vector3d.new({ov.mm(ldx)}, {ov.mm(-400)}, {ov.mm(ldz)}))
mvtxt_{sfx}.layer = model.layers["Movement"] rescue nil
'''


def generate_ruby():
    mv_corners = ["BL", "TL", "BR", "TR"]
    mv = {c: movement(c) for c in mv_corners}
    comps = [
        ov.component("Corners", "Corners", corners()),
        ov.component("Film Plane", "Film Plane", film_plane()),
        ov.component("Pinhole", "Pinhole", pinhole()),
        ov.component("Context (walkway + IBC cantilever/beams)", "Context", context()),
    ] + [ov.component(f"Movement base ({c} corner)", "Movement", mv[c][0]) for c in mv_corners]
    body = "\n".join(comps)
    tags_ruby = "\n".join(f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep = "[" + ", ".join(f'"{t}"' for t in TAGS) + "]"
    show = ["Corners", "Film Plane", "Pinhole"]
    show_ctx = show + ["Context"]
    # ONE Movement scene framing all four corner demos (2×2 grid: left column @X_L, right column display-
    # shifted to MV_TARGET_X). Centre on the grid mid-point, wide enough to hold all four + their motion.
    mv_cx = (X_L + MV_TARGET_X["BR"]) / 2
    # Overview (with context) FIRST, then the zoomed corner detail; side/top + Labeled added after.
    iso = [
        ("Overview", show_ctx, (2400, FP_Y - 700, CH / 2, 9500)),
        ("Corner detail", show, (X_L, FP_Y, PZ0 + 30, 620)),
        ("Movement", ["Movement"], (mv_cx, FP_Y + 250, CH / 2, 4400)),
    ]
    mv_dc = "".join(movement_dc(c, *mv[c][1:]) for c in mv_corners)

    def scene_lit(n, tags, tgt):
        tg = "[" + ", ".join(f'"{t}"' for t in tags) + "]"
        cam = f"[{ov.mm(tgt[0])}, {ov.mm(tgt[1])}, {ov.mm(tgt[2])}, {ov.mm(tgt[3])}]"
        return f'["{n}", {tg}, {cam}]'
    iso_ruby = "[" + ", ".join(scene_lit(*s) for s in iso) + "]"
    show_ruby = "[" + ", ".join(f'"{t}"' for t in show) + "]"
    lbl_show_ruby = "[" + ", ".join(f'"{t}"' for t in show + ["Labels"]) + "]"

    return f'''# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/generate_film_plane_mechanism_model.py — do not edit this .rb directly.
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
{mv_dc}

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

# Land on the Overview scene (which hides Movement/Context) so the post-regen view matches a real
# scene rather than an ad-hoc all-visible state (else the 4 Movement demos appear to "leak" into
# whatever scene tab is selected until it is re-clicked).
model.pages.selected_page = model.pages[0] if model.pages.count > 0

model.commit_operation
{{ success: true, model: "Film-Plane Corner Mechanism",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }}.to_json
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate the film-plane combined corner mechanism model")
    parser.add_argument("--save", action="store_true", help="Write Ruby to src/models/film-plane-mechanism.rb")
    parser.add_argument("--send", action="store_true", help="Send to the ACTIVE SketchUp doc (open a NEW doc first)")
    args = parser.parse_args()

    ruby = generate_ruby()
    if args.save:
        out = os.path.join(os.path.dirname(__file__), "film-plane-mechanism.rb")
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
