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
        U-JOINT (Belden UJ-SS750x375) — tilt + swing, twist locked
    A light cone from the pinhole to the four corners shows the plane faces the pinhole.

No screws/handwheels — a pinhole's infinite DoF makes this scene control, not focus: push each
slide, cam-clamp to lock. Scenes: Overview (iso) · Tilt (side) · Swing (top) · Corner detail · Labeled.

REUSES generate_sketchup_model.py helpers. Open a NEW blank SketchUp doc before --send.

Usage:
    /usr/bin/python3 src/models/generate_film_plane_mechanism_model.py --save [--send]
"""
import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import generate_sketchup_model as ov          # ruby helpers + component()
import generate_corridor_water_panel as cp    # IBC corridor deep-box frame + tote restraint (beams) — reused verbatim

TAGS = ["Corners", "Film Plane", "Pinhole", "Context", "Movement", "Shell", "Plane Tilt", "Plane Swing", "Labels"]

# Sketchfab identity — stamped on every --send (force_name) so the model never re-uploads blank.
# Values are the ones already carried in the live .skp's `sketchfab` attribute dict (stable UID).
SF_TITLE = "TBS-001 Articulated Film Plane Model"
SF_ID    = "572b4aaa2d394de1b8852160d7cdcfc3"   # stable Sketchfab UID — re-uploads REPLACE this model
SF_TAGS  = "sketchup"
SF_DESC  = ("The configuration the photosensitive film plane is flush against one of the 20ft "
            "long-side walls of the container. This has a view-camera-style moveable film plane — "
            "a mechanism with four independently actuated corners.")

C_STEEL = "#B0B0B8"; C_CROSS = "#8A8A92"; C_PANEL = "#1F3B66"; C_CAR = "#C04010"
C_FRAME = "#8FB0C8"   # film-plane 2x2 6061 Al angle perimeter frame (the ACM backing is captured in it)
C_TILT = "#2E8B57"   # vertical (Z) slide — TILT accommodation (green)
C_SWING = "#7B5EA7"  # horizontal (X) slide — SWING accommodation (purple)
C_CLAMP = "#3A3A40"  # cam rail-brake (fp-cam-clamp, McMaster 5128A63)
C_POLY = "#D8D4C8"   # UHMW pad (cam-brake pinch face)

# real container/film layout (mm) — sourced from tbs_constants via ov (no hardcoded copies)
CH = ov.C_HGT                        # interior height
X_L, X_R = ov.FP_X_L, ov.FP_X_R - 25   # right edge trimmed 25mm (+ a 35mm end-plate trim) to clear the IBC frame → FP_W 4499→4474
FP_Y = ov.FP_Y                       # film depth from the pinhole wall (Y)
PH_X, PH_Z = ov.PH_X, ov.C_HGT // 2  # pinhole X (film-width centre) and Z (mid-height)
# ── 6061 Al U-CHANNEL rails, BOTH 3"×1.5" (McMaster 1262T21, $352/6ft, 0.188" wall) — the deflection is
# ~25× overkill even at 3×1.5, so the 4×2 is unnecessary weight/cost. Wheels ride the OPEN channel;
# the CLOSED web-back is the splice face (one section does the H-bar's two-U job). ──
# BOTH rails WEB-VERTICAL (2026-08-10 reconciliation): the deep web resists bending, and a CAPTURED
# skate (rollers grip both flanges) holds each corner regardless of load direction.
# BOTTOM: load rollers gravity-seated on the bottom flange (weight).
# TOP:    the SAME captured skate — the keeper/capture rollers react the plane's tip-force, not gravity.
#         (The old flat/inverted-U top let the model draw ~38mm more film height than FP_H=2094 claimed;
#          web-vertical reconciles the model DOWN to FP_H. Transport swing unaffected — left rail is a
#          removable drop-in.)
CD_BOT, CW_BOT = 76, 38              # 3×1.5 web-vertical: web depth (Z) × flange (X) — BOTH rails
CD_TOP, CW_TOP = CD_BOT, CW_BOT      # top = the SAME web-vertical section as the bottom
HB_T = 5                             # web/flange wall = 0.188" (4.78mm)
SPLICE_YD = 260                      # removable = 6ft (1830) + 260mm; the length-splice sits at the PINHOLE end
                                     # (Yd~260, shortest-throw = least-travelled) → least chance the skate rolls it

# ── FILM-PLANE WIDTH INSET — the ghost panel edges land on the CARRIAGE line (inb), NOT the rail line.
# At the rail line (X_L/X_R) the full-height panel skewers the bottom weight beam (which straddles cx by
# ±CW_BOT/2). Pulling each edge inboard to the carriage seats the corner IN its carrier (the frame bracket
# already reaches here) and clears the bottom-beam inboard flange tip by HB_T+... ──
FILM_INSET = CW_BOT / 2 + 14         # 33 — carriage line, inboard of the bottom (weight) beam by 14mm
FCX_L = X_L + FILM_INSET             # 183 — film LEFT edge, seated in the left carrier (clear of the beam)
FCX_R = X_R - FILM_INSET             # 4591 — film RIGHT edge, seated in the right carrier
FP_W_CORNER = FCX_R - FCX_L          # 4408 — active image width once the panel sits in the carriers

# ── vertical layout (mm) — bottom pinned by the walkway; top pinned by the ceiling (web-vertical fit) ──
PZ0 = ov.RAIL_OFF_BOT                # 160 — film BOTTOM edge, ABOVE the Z140 walkway (hard floor, +20mm)
BUILD_BOT = 110                      # bottom channel centre → film-corner stack (weight-bearing carriage)
GUIDE_GAP = 10                       # top guide-follower gap (film top just below the web-vertical guide channel)
PZ_HB_BOT = PZ0 + BUILD_BOT          # 270 — bottom channel WEB-centre (bottom flange @220 clears the deck; film hangs below)
PZ_HB_TOP = ov.C_HGT - CD_TOP // 2 - 50  # 2300 — top rail WEB-centre, web-vertical, 50mm below the ceiling
PZ1 = PZ_HB_TOP - CD_TOP // 2 - GUIDE_GAP # 2252 — film TOP edge, just under the web-vertical guide channel
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
    """BOTTOM rail — 6061 Al U-channel stood WEB-VERTICAL. Web is the OUTBOARD back (splice face);
    the two flanges project INBOARD, forming the wheel channel that opens toward the film. Deep web
    (CD_BOT) resists bending. zc = web-centre Z."""
    P = []
    outx = cx - cin * CW_BOT / 2                    # outboard face
    web_x = min(outx, outx + cin * HB_T)
    fl_x = min(outx, outx + cin * CW_BOT)
    P.append(ov.ruby_box(f"{name} web {tag}", web_x, y0, zc - CD_BOT / 2, HB_T, ylen, CD_BOT, color=ov.C_ALUM, alpha=alpha))
    for fz in (zc + CD_BOT / 2 - HB_T, zc - CD_BOT / 2):
        P.append(ov.ruby_box(f"{name} flange {tag} {int(fz)}", fl_x, y0, fz, CW_BOT, ylen, HB_T, color=ov.C_ALUM, alpha=alpha))
    # inboard LIP on the bottom flange — lateral keeper: stops the load roller walking off in X on swing
    in_edge = cx + cin * CW_BOT / 2
    P.append(ov.ruby_box(f"{name} bottom-flange lip {tag}", min(in_edge, in_edge - cin * 5), y0, zc - CD_BOT / 2 + HB_T, 5, ylen, 9, color=ov.C_ALUM, alpha=alpha))
    return P


def corner_slide_parts(cx, fcx, fz, cin, is_bot, ty):
    """SINGLE source for the drift-prone corner assembly — the green Z / purple X cross-slide ways, the U-joint
    + its input/output stubs + 4040N12 shaft support, the frame-corner bolt, and the 304 corner plate. Returns
    absolute-coordinate part-specs keyed by name; the CALLER supplies its own label (emit_slide) and any
    coordinate OFFSET (0 = absolute; -centre for the whole-plane frame; -pivot for the Movement panel). ty is
    the corner's backing-side Y (FP_Y, or MID_Y for the whole plane). Positions/dims match the Movement +
    whole-plane scenes (Sheet-3 slide-clearance fixes); corner() re-syncs to these.
      spec = (kind, x, y, z, a, b, c, color, axis)   kind ∈ {box (a×b×c), cyl (Ø a, len b, axis)}."""
    Lz, Lx = 250, 260
    gx0 = (cx + cin * 26 - 5) if is_bot else ((fcx - 20) if cin > 0 else (fcx + 4))  # green outboard of the frame leg
    gz0 = (fz - 20) if is_bot else (fz - 4 - Lz)        # green Z (bottom up / top down, below the rail)
    px0 = (cx - 20) if cin > 0 else (cx + 20 - Lx)
    pz_purple = (fz - 18) if is_bot else (fz + 4)        # purple clear of the film face
    stub_x0 = (cx + 5) if cin > 0 else (cx - 51)
    sup_x0 = (cx + 26) if cin > 0 else (cx - 49)
    cpx0 = (cx - 14) if cin > 0 else (cx - 20)
    cpz0 = (fz + 5) if is_bot else (fz - 45)
    return {
        "green":         ("box", gx0, ty + 1, gz0, 10, 18, Lz, C_TILT, None),
        "purple":        ("box", px0, ty + 1, pz_purple, Lx, 14, 14, C_SWING, None),
        "ujoint":        ("box", cx - 12, ty - 4, fz - 14, 24, 24, 24, C_CROSS, None),
        "input_stub":    ("cyl", stub_x0, ty + 8, fz, 4.75, 46, None, C_STEEL, "x"),
        "shaft_support": ("box", sup_x0, ty - 1, fz - 11, 23, 18, 22, C_STEEL, None),
        "output_stub":   ("cyl", cx, ty - 14, fz, 4.75, 20, None, C_STEEL, "y"),
        "frame_bolt":    ("cyl", fcx, ty - 6, fz, 3, 18, None, C_STEEL, "y"),
        "corner_plate":  ("box", cpx0, ty - 8, cpz0, 34, 16, 40, C_STEEL, None),
    }


def emit_slide(label, spec, ox=0, oy=0, oz=0):
    """Emit one corner_slide_parts spec as ruby, applying an (ox,oy,oz) coordinate offset."""
    kind, x, y, z, a, b, c, color, axis = spec
    if kind == "box":
        return ov.ruby_box(label, x + ox, y + oy, z + oz, a, b, c, color=color)
    return ov.ruby_cylinder(label, x + ox, y + oy, z + oz, a, b, color=color, axis=axis)


def corner(tag, cx, fz, zc, cin, side):
    """One corner on a 6061 Al U-channel depth rail. BOTH web-vertical: BOTTOM weight, TOP guide (captured skate).
      cx = corner X   fz = film-corner Z   zc = rail web-centre Z   cin = +1 (left) / -1 (right)
      side = 'L' drop-in (stub + welded bridge + removable + support + pinhole gusset) / 'R' flanged."""
    P = []
    ty = FP_Y
    is_bot = fz < ov.C_HGT / 2
    # BOTH corners web-vertical now — same rail + captured skate; only the Z position + stack direction differ.
    rail = lambda nm, y0, yl, al=None: channel_v(nm, cx, zc, y0, yl, tag, cin, al)
    sec_h, chan_w = CD_BOT, CW_BOT
    botf = zc - sec_h / 2                                # section bottom Z
    splice_z = botf - 12                                 # length splice on the outboard web-back (both)

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
        # BRIDGE welded to the REMOVABLE bears ON TOP of the stub (gravity-held) + a locating PIN (flush to the
        # inner-rail top) + a short bottom support bridge (~64mm) — web-vertical, SAME both corners.
        P.append(ov.ruby_box(f"Welded bridge (welded to REMOVABLE, bears on stub, ON TOP) {tag}", cx - CW_BOT / 2, LEFT_CUT_YD - 60, zc + CD_BOT / 2, CW_BOT, 150, 12, color=C_CROSS))
        P.append(ov.ruby_cylinder(f"Locating pin (bridge↔STUB, flush to inner-rail top) {tag}", cx, LEFT_CUT_YD + 45, zc + CD_BOT / 2 - HB_T, 5, HB_T + 12, color=C_STEEL, axis="z"))
        P.append(ov.ruby_box(f"Bottom support bridge (STUB → beam underside) {tag}", cx - CW_BOT / 2, LEFT_CUT_YD - 32, botf - 12, CW_BOT, 64, 12, color=C_CROSS))
        # No floor post at the cut: the stub (Yd LEFT_CUT_YD→C_WID) is anchored at the pivot post (= film
        # far-left post) + the far wall, and the cut is only ~197mm cantilevered from it — the removable's
        # welded bridge BEARS on the stub, whose pivot-post anchor carries the reaction, so a floor post
        # (which would foul the sliding carriage) is unnecessary.
        P.append(ov.ruby_box(f"Rail far flange (pivot post) {tag}", cx - 55, ov.C_WID - 12, botf - 5, 110, 12, sec_h + 10, color=C_CROSS))
        P.append(ov.ruby_box(f"Pinhole-wall gusset/seat {tag}", cx - 56, 0, botf - 30, 112, 45, sec_h + 55, color=C_CROSS))
        # length splice (removable = 6ft + 260mm) at the PINHOLE end — shortest-throw, least-travelled;
        # same outboard-web placement so it's clear of the carriage
        P.append(ov.ruby_box(f"Length splice (pinhole end, outboard web) {tag}", cx - cin * (CW_BOT / 2 + 12), SPLICE_YD - 55, botf, 12, 110, CD_BOT, color=C_CROSS))

    # ── SKATE (spray-bar carriage pattern): Ø32 acetal wheels IN the channel; the Ø10 axle is
    # cantilevered from the CARRIAGE (inboard) — the axle and its retainer bolts pass through the
    # CARRIAGE PLATE, never the beam. ──
    rz = botf + HB_T + 16                                 # roller-centre Z — on the bottom flange (both corners)
    inb = cx + cin * (chan_w / 2 + 14)                   # carriage line — inboard of the channel opening (film side)
    # CAPTURED skate (both corners): Ø32 acetal roller (WIDE face) on the bottom flange + a Ø20 KEEPER roller
    # under the top flange. At the BOTTOM the roller carries gravity; at the TOP the SAME pair reacts the plane's
    # tip-force in either direction (a captured guide, not gravity-seated). The Ø10 axle is cantilevered from the
    # inboard CARRIAGE and exits the channel opening — it never crosses a flange.
    rlabel, r_x0, r_len = "Acetal roller Ø32 (wide face)", cx - 10, 20
    kx, kz = cx - 6, zc + CD_BOT / 2 - HB_T - 10          # keeper (under the top flange); Ø20 on a stub axle
    for ry in (ty + 8, ty + 48):
        P.append(ov.ruby_cylinder(f"{rlabel} {tag} {int(ry)}", r_x0, ry, rz, 16, r_len, color=C_CAR, axis="x"))
        wax0 = min(r_x0, inb - 6)
        P.append(ov.ruby_cylinder(f"Wheel axle Ø10 {tag} {int(ry)}", wax0, ry, rz, 5, max(r_x0 + r_len, inb + 6) - wax0, color=C_CROSS, axis="x"))
        P.append(ov.ruby_cylinder(f"Keeper roller Ø20 (anti-lift / anti-tip) {tag} {int(ry)}", kx, ry, kz, 10, 12, color=C_CAR, axis="x"))
        P.append(ov.ruby_cylinder(f"Keeper axle Ø8 {tag} {int(ry)}", min(kx, inb), ry, kz, 4, abs(inb - kx) + 10, color=C_CROSS, axis="x"))
    # carriage plate on the axle ends + axle-retainer bolts DOWN THROUGH THE PLATE (saddle-clamp, not the beam).
    # Spans the film-corner + load roller + keeper so every axle lands on it. TOP corners: cap the plate top
    # 25mm below the ceiling.
    zvals = (fz, rz, kz)
    zlo, zhi = min(zvals), max(zvals)
    plate_top = min(zhi + 18, ov.C_HGT - 25)
    P.append(ov.ruby_box(f"Carriage plate (bolted to skate axles) {tag}", inb - 6, ty + 1, zlo - 6, 14, 86, plate_top - (zlo - 6), color=C_CAR))
    for ry in (ty + 8, ty + 48):
        blen = min(44, plate_top - (rz - 22))                 # keep the retainer bolt within the (capped) plate
        P.append(ov.ruby_cylinder(f"Axle retainer bolt (thru plate) {tag} {int(ry)}", inb, ry, rz - 22, 2.5, blen, color=C_CROSS, axis="z"))

    # ── CAM RAIL-BRAKE (fp-cam-clamp, McMaster 5128A63) — BOTH corners now (web-vertical). Base on the carriage-
    # plate top; the hold-down arm reaches OUTBOARD over the channel TOP FLANGE and a UHMW pad presses DOWN on it.
    # Self-reacting: the Ø32 roller on the BOTTOM flange reacts the pinch, so it never unloads the skate. Thrown
    # to lock depth for the shot + transport. One representative shown (BOM: 3 per corner). ──
    tfz = zc + CD_BOT / 2                                  # top-flange top surface
    basex = inb - cin * 3                                  # base near the plate's outboard edge
    padx = cx + cin * 8                                    # pad over the (inboard part of the) top flange
    cby = ty + 33
    P.append(ov.ruby_box(f"Cam-brake base (5128A63) {tag}", basex - 5, cby, plate_top, 10, 22, 8, color=C_CLAMP))
    P.append(ov.ruby_box(f"Cam-brake hold-down arm {tag}", min(basex, padx), cby + 7, tfz + 4, abs(basex - padx), 8, 4, color=C_CLAMP))
    P.append(ov.ruby_box(f"Cam-brake UHMW pad {tag}", padx - 6, cby + 6, tfz, 12, 10, 4, color=C_POLY))
    P.append(ov.ruby_cylinder(f"Cam-brake lever {tag}", padx, cby + 11, tfz + 4, 2, 20, color=C_CLAMP, axis="z"))  # lever OVER the pad

    # ── mechanism, inboard: Z slide (tilt) → X slide (swing) → U-joint → the FILM-PLANE CORNER ──
    # The cross-slides sit on the BACKING side of the film plane (Yd > FP_Y) so the frame SITS ON them — the
    # muslin-clamp perp leg projects the other way (toward the pinhole), so nothing is drawn through the slides.
    # muslin-clamp perp leg projects the other way (toward the pinhole). Green Z / purple X ways, U-joint +
    # stubs + 4040N12 shaft support, 304 corner plate, and the frame-corner bolt are the SHARED assembly
    # (corner_slide_parts) — the single source these + the Movement + whole-plane scenes all draw from.
    fcx = cx + cin * FILM_INSET                          # film-plane corner (frame heel)
    sp = corner_slide_parts(cx, fcx, fz, cin, is_bot, FP_Y)
    P.append(emit_slide(f"Vertical Z slide rail (TILT, green) {tag}", sp["green"]))
    P.append(emit_slide(f"Horizontal X slide rail (SWING, purple) {tag}", sp["purple"]))
    P.append(emit_slide(f"U-joint (Belden UJ-SS750x375, setscrew) {tag}", sp["ujoint"]))
    P.append(emit_slide(f"Input stub 3/8 (X slide → U-joint) {tag}", sp["input_stub"]))
    P.append(emit_slide(f"4040N12 304 shaft support (clamps input stub → X slide) {tag}", sp["shaft_support"]))
    P.append(emit_slide(f"Output stub 3/8 (U-joint → corner plate) {tag}", sp["output_stub"]))
    P.append(emit_slide(f"Corner plate 304 SS (U-joint mount — angle frame → U-joint) {tag}", sp["corner_plate"]))
    P.append(emit_slide(f"Frame-corner bolt (angle frame → bracket) {tag}", sp["frame_bolt"]))
    return "\n".join(P)


def corners():
    P = [
        corner("BL", X_L, PZ0, PZ_HB_BOT, +1, "L"),   # bottom-left  — web-vertical (weight), drop-in
        corner("BR", X_R, PZ0, PZ_HB_BOT, -1, "R"),   # bottom-right — web-vertical (weight), flanged (IBC plate)
        corner("TL", X_L, PZ1, PZ_HB_TOP, +1, "L"),   # top-left     — web-vertical guide, drop-in
        corner("TR", X_R, PZ1, PZ_HB_TOP, -1, "R"),   # top-right    — web-vertical guide, flanged
    ]
    # faint floor + ceiling so the UPPER (ceiling) and LOWER (floor) rails read as mounted structure
    P.append(ov.ruby_box("Floor", X_L - 250, 0, -12, (X_R - X_L) + 500, FP_Y + 250, 12, color=C_STEEL, alpha=0.05))
    P.append(ov.ruby_box("Ceiling", X_L - 250, 0, CH, (X_R - X_L) + 500, FP_Y + 250, 12, color=C_STEEL, alpha=0.05))
    return "\n".join(P)


def film_plane():
    # The film plane is NOT a bare sheet butted to the corner brackets. It is a rigid ACM BACKING captured in a
    # 2x2 6061 Al angle PERIMETER FRAME (plain 6061-T6, 2"×2"×1/8" — an EXPENDABLE part; plain Al in the
    # splash-not-immersed cyanotype zone, replaced on pitting, chosen over 304 SS for weight + cost):
    # the ACM seats against the frame's in-plane leg; the muslin is clamped onto the ACM by spring clips on the upstand (Sheet 6); and
    # the frame's four CORNERS bolt onto the frame
    # 304 SS corner plates — which carry it through the U-joint to the cross-slides. So the load path is
    # ACM → angle frame → 304 SS corner plate → U-joint, never a butt joint. The corner plate is STEEL
    # (not the expendable 6061 angle): the U-joint funnels the corner load into a few bolts, too concentrated
    # for aluminum — 304 SS for strength + a galvanic/wet-zone match to the 303 SS U-joint.
    AL, AT = 50, 3                                # 2x2 angle leg / wall
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
MOVEMENT_TWO_WAY = {"BL", "TL", "BR", "TR"}  # all cycle 0 -> +1 -> -1 (toward pinhole, then toward the far wall)
# Movement is a SCHEMATIC demo scene — the real corners are 4.5 m apart, so the right-side corners are
# DISPLAY-SHIFTED left to sit beside the left ones (reduce the L↔R gap). Edit the target X to taste.
MV_TARGET_X = {"BR": 2200, "TR": 2200}


def movement(corner="BL", two_way=False):
    """One 'Movement' scene corner — the cross-slide OPERATING on a CLICK.
    PHASE 1 (drive 0->0.5): the carriage rolls FORWARD in Y + the panel TILTS about the U-joint (far edge
    toward the pinhole). PHASE 2 (0.5->1): the U-joint + panel DEPLOY by sliding along the GREEN (Z) slide
    (bottom corners slide UP, top corners slide DOWN). On the Movement tag. Bottom = web-vertical weight
    channel + load rollers; top = same captured skate (guide). Panel/tilt mirror by corner.
    Returns (static, carriage, float, panel, pivot, dy_fwd, deploy, tilt, anchor)."""
    ty = FP_Y
    AL, AT = 50, 3                                     # 2x2 angle leg / wall (match film_plane())
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
    # PER SHEET 3: tilt/swing is DRIVEN by the depth (Y) ROLL; the green Z / purple X cross-slides only take
    # up a SMALL foreshortening. So the roll is the star and the cross-slide floats just FORESHORTEN mm
    # (TILT → GREEN Z; SWING → PURPLE X, inboard so the ACM clears the corner beam).
    FORESHORTEN = 50
    deploy = (cin * FORESHORTEN) if swing_corner else (sz * FORESHORTEN)
    # tilt about the U-JOINT CENTRE (not the film corner) so the frame + corner plate stay JOINED through the
    # tilt. U-joint box = (cx-12, ty-4, fz-14, 24³) → centre = (cx, ty+8, fz-2).
    pivot = (cx, ty + 8, fz - 2)
    px, py, pz = pivot
    chan_w = CW_BOT
    inb = cx + cin * (chan_w / 2 + 14)                 # carriage line — inboard of the channel opening
    rz = zc - CD_BOT / 2 + HB_T + 16                    # wheel-centre Z (web-vertical, both corners)
    cpx0c = (inb - 6) if cin > 0 else (inb - 8)        # carriage-plate min-x
    # Per Sheet 3 EACH corner carries BOTH cross-slides (green Z + purple X). The ACTIVE one (green for tilt,
    # purple for swing) is the base WAY the stack floats along; the OTHER rides the stack. Both come from the
    # SHARED corner_slide_parts (single source with corner() + the whole-plane scenes).
    sp = corner_slide_parts(cx, fcx, fz, cin, is_bot, FP_Y)
    green_way = emit_slide(f"Vertical Z cross-slide (TILT, green ~250) (Movement {corner})", sp["green"])
    purple_way = emit_slide(f"Horizontal X cross-slide (SWING, purple ~260) (Movement {corner})", sp["purple"])
    if swing_corner:   # purple X is the ACTIVE way; green Z rides the stack
        deploy_rail, perp_slide = purple_way, green_way
    else:              # green Z is the ACTIVE way; purple X rides the stack
        deploy_rail, perp_slide = green_way, purple_way
    # ── STATIC rail + CARRIAGE (skate + plate + the GREEN Z deploy rail) ──
    # two_way rolls the carriage -Y as well as +Y, so extend the rail toward the PINHOLE to keep it on-track.
    rail_y0, rail_len = ty - 160, 960
    if two_way:
        rail_y0 -= dy_fwd + 40
        rail_len += dy_fwd + 40
    carr = []
    static_ruby = "\n".join(channel_v(f"U-channel rail (Movement {corner})", cx, zc, rail_y0, rail_len, f"Move{corner}", cin))
    for ry in (ty + 8, ty + 48):
        carr.append(ov.ruby_cylinder(f"Acetal skate wheel Ø32 (Movement {corner}) {int(ry)}", cx - 10, ry, rz, 16, 20, color=C_CAR, axis="x"))
    carr.append(ov.ruby_box(f"Carriage plate (Movement {corner})", cpx0c, ty + 1, fz - 6, 14, 86, (rz + 46) - (fz - 6), color=C_CAR))
    # the ACTIVE cross-slide way (fixed to the carriage); the stack floats a SMALL foreshortening along it
    carr.append(deploy_rail)
    # FLOAT (the OTHER cross-slide + U-joint + its mounting hardware) — floats FORESHORTEN mm along the way
    floatp = [
        perp_slide,
        emit_slide(f"U-joint (Belden UJ-SS750x375) (Movement {corner})", sp["ujoint"]),
        emit_slide(f"Input stub 3/8 (X slide → U-joint) (Movement {corner})", sp["input_stub"]),
        emit_slide(f"4040N12 304 shaft support (clamps stub → carrier) (Movement {corner})", sp["shaft_support"]),
        emit_slide(f"Output stub 3/8 (U-joint → corner plate) (Movement {corner})", sp["output_stub"]),
    ]
    # PANEL (corner plate + frame + ACM) — relative to the U-joint-centre pivot so it TILTS about the U-joint;
    # the 304 corner plate + frame bolt (shared parts, offset -pivot) live HERE so they stay bolted through the tilt.
    ax0 = fcx if cin > 0 else fcx - plen              # panel-body X min (grows inboard from the corner)
    az0 = fz if is_bot else fz - plen                 # panel-body Z min (grows into the film from the corner)
    hz_up = fz if is_bot else fz - AT                 # horizontal-leg (upstand / in-plane) Z, at the corner edge
    hz_in = fz if is_bot else fz - AL
    vx_up = fcx if cin > 0 else fcx - AT              # vertical-leg (upstand / in-plane) X, at the corner edge
    vx_in = fcx if cin > 0 else fcx - AL
    hlbl = "bottom" if is_bot else "top"
    vlbl = "left" if cin > 0 else "right"
    panel = [
        emit_slide(f"304 SS corner plate (Movement {corner})", sp["corner_plate"], -px, -py, -pz),
        ov.ruby_box(f"ACM film-panel corner — partial ghost (Movement {corner})", ax0 - px, FP_Y - py, az0 - pz, plen, 4, plen, color=C_PANEL, alpha=0.30),
        ov.ruby_box(f"Film frame 2x2 6061 — {hlbl} upstand (Movement {corner})", ax0 - px, yperp - py, hz_up - pz, plen, AL, AT, color=C_FRAME),
        ov.ruby_box(f"Film frame 2x2 6061 — {hlbl} in-plane leg (Movement {corner})", ax0 - px, yin - py, hz_in - pz, plen, AT, AL, color=C_FRAME),
        ov.ruby_box(f"Film frame 2x2 6061 — {vlbl} upstand (Movement {corner})", vx_up - px, yperp - py, az0 - pz, AT, AL, plen, color=C_FRAME),
        ov.ruby_box(f"Film frame 2x2 6061 — {vlbl} in-plane leg (Movement {corner})", vx_in - px, yin - py, az0 - pz, AL, AT, plen, color=C_FRAME),
        emit_slide(f"Frame-corner bolt (angle frame → corner plate) (Movement {corner})", sp["frame_bolt"], -px, -py, -pz),
    ]
    anchor = (cx + cin * 420, ty + 500, fz + sz * 520)
    return static_ruby, "\n".join(carr), "\n".join(floatp), "\n".join(panel), pivot, dy_fwd, deploy, rot_attr, rot_val, anchor


def movement_dc(sfx, carr, floatp, panel, pivot, dy_fwd, deploy, rot_attr, rot_val, anchor, two_way=False):
    """Emit the click DC for a Movement corner (sfx = 'BL'/'TL'/'BR'/'TR'). One parent DC (Movement<sfx>)
    carries the lone onclick; the driver is RELAYED one level at a time (DC ancestor-refs resolve only ONE
    level up). Nesting: Movement<sfx> > Carriage<sfx> (roll Y) > Float<sfx> (cross-slide foreshorten) >
    PanelTilt<sfx> (rot_attr = rotx TILT / rotz SWING).
    two_way=True → move cycles 0 → +1 → -1 (toward pinhole, then toward the far wall); the roll + rotation
    flip sign each way, while the cross-slide foreshortening rides ABS(move) (symmetric — same both ways)."""
    px, py, pz = pivot
    rot_label = "swing" if rot_attr == "rotz" else "tilt"
    dep_axis = "x" if rot_attr == "rotz" else "z"      # SWING deploys along PURPLE X; TILT along GREEN Z
    dep_color = "purple X" if dep_axis == "x" else "green Z"
    onclick_vals = "0, 1, -1" if two_way else "0, 1"    # two_way: center -> pinhole -> far wall -> center
    dep_expr = f"ABS(drive) * {deploy}" if two_way else f"drive * {deploy}"   # foreshorten is symmetric
    click_text = (f"CLICK {sfx}: 1st click {rot_label}s toward the PINHOLE, 2nd toward the FAR WALL — the {dep_color} slider foreshortens the SAME both ways"
                  if two_way else
                  f"CLICK {sfx}: depth-roll DRIVES the {rot_label}; the {dep_color} cross-slide takes up the foreshortening")
    ldx = 300 if sfx[1] == "L" else -300               # L=left → +X, R=right → -X
    ldz = 300 if sfx[0] == "B" else -300               # B=bottom → +Z, T=top → -Z
    return f'''
# ═══ Movement — {sfx} corner (Sheet 3 model): ONE click — the depth-rail ROLL drives the {rot_label};
# the {dep_color} cross-slide takes up the small foreshortening. One coordinated motion. ═══
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
mvp_{sfx}_inst.set_attribute(da, "_move_label", "{sfx}: depth-roll drives the {rot_label} ({dep_color} cross-slide absorbs foreshortening)")
mvp_{sfx}_inst.set_attribute(da, "onclick", 'ANIMATE("move", {onclick_vals})')
mvp_{sfx}_inst.set_attribute(da, "_onclick_access", "NONE")
# carriage ROLLS along the depth rail (Y) — the DRIVER of {rot_label} (Sheet 3); one coordinated motion
[mvo_{sfx}, mvo_{sfx}_inst].each do |e|
  e.set_attribute(da, "_name", "Carriage{sfx}"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "drive", 0.0); e.set_attribute(da, "y", 0.0)
end
mvo_{sfx}_inst.set_attribute(da, "_drive_formula", "Movement{sfx}!move")
mvo_{sfx}_inst.set_attribute(da, "_y_formula", "drive * {dy_fwd}")
# float (U-joint + panel) — the cross-slide takes up a SMALL foreshortening along the {dep_color} way
[mvfl_{sfx}, mvfl_{sfx}_inst].each do |e|
  e.set_attribute(da, "_name", "Float{sfx}"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "drive", 0.0); e.set_attribute(da, "{dep_axis}", 0.0)
end
mvfl_{sfx}_inst.set_attribute(da, "_drive_formula", "Carriage{sfx}!drive")
mvfl_{sfx}_inst.set_attribute(da, "_{dep_axis}_formula", "{dep_expr}")
# panel {rot_label}S about the U-joint (rotx=tilt / rotz=swing) — the DOF the depth-roll produces
[mvpan_{sfx}, mvpan_{sfx}_inst].each do |e|
  e.set_attribute(da, "_name", "PanelTilt{sfx}"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "drive", 0.0); e.set_attribute(da, "{rot_attr}", 0.0)
end
mvpan_{sfx}_inst.set_attribute(da, "_drive_formula", "Float{sfx}!drive")
mvpan_{sfx}_inst.set_attribute(da, "_{rot_attr}_formula", "drive * {rot_val}")
mvtxt_{sfx} = entities.add_text("{click_text}", Geom::Point3d.new({ov.mm(anchor[0])}, {ov.mm(anchor[1])}, {ov.mm(anchor[2])}), Geom::Vector3d.new({ov.mm(ldx)}, {ov.mm(-400)}, {ov.mm(ldz)}))
mvtxt_{sfx}.layer = model.layers["Movement"] rescue nil
'''


MID_Y = ov.C_WID / 2.0   # middle of the container depth — where the whole-plane demo sits (room to tilt/swing)


def shell():
    """Context for the whole-plane scenes — a faint floor + the FOUR full-depth rails the corners roll on
    (all 4 web-vertical). NO container walls or ceiling (open, so the plane + rails read
    clearly from any angle)."""
    x0, xw = -300, (X_R - X_L) + 800
    Wd = ov.C_WID
    P = [
        ov.ruby_box("Floor (reference)", x0, 0, -12, xw, Wd, 12, color=C_STEEL, alpha=0.08),
    ]
    # the FOUR depth rails (run in Y the full container depth): ALL web-vertical (BL/BR floor, TL/TR ceiling)
    P += channel_v("Depth rail BL", X_L, PZ_HB_BOT, 0, Wd, "rBL", +1)
    P += channel_v("Depth rail BR", X_R, PZ_HB_BOT, 0, Wd, "rBR", -1)
    P += channel_v("Depth rail TL", X_L, PZ_HB_TOP, 0, Wd, "rTL", +1)
    P += channel_v("Depth rail TR", X_R, PZ_HB_TOP, 0, Wd, "rTR", -1)
    return "\n".join(P)


PLANE_CORNERS = [(X_L, FCX_L, PZ0, PZ_HB_BOT, +1, True), (X_R, FCX_R, PZ0, PZ_HB_BOT, -1, True),
                 (X_L, FCX_L, PZ1, PZ_HB_TOP, +1, False), (X_R, FCX_R, PZ1, PZ_HB_TOP, -1, False)]


def plane_frame(px, pz, yc):
    """The ROTATING body of the whole plane — 6061 frame + near-invisible clickable fill + per-corner U-joint,
    stubs, 4040N12 shaft support, 304 corner plate. Relative to the centre pivot (px, yc, pz) so a DC rotates
    it (tilt = rotx / swing = rotz). The CARRIAGES are NOT here — they stay on the rails (see plane_carriage)."""
    AL, AT = 50, 3
    yperp, yin = yc - AL, yc - AT
    W = FP_W_CORNER
    ty = yc
    def bx(name, x, y, z, w, d, h, color, alpha=None):
        return ov.ruby_box(name, x - px, y - yc, z - pz, w, d, h, color=color, alpha=alpha)
    def bcyl(name, x, y, z, dia, ln, color, axis):
        return ov.ruby_cylinder(name, x - px, y - yc, z - pz, dia, ln, color=color, axis=axis)
    P = [
        bx("Film panel (near-invisible, clickable fill) — whole plane", FCX_L, yc, PZ0, W, 4, PZ1 - PZ0, C_PANEL, 0.04),
        bx("Film frame — top upstand", FCX_L, yperp, PZ1 - AT, W, AL, AT, C_FRAME),
        bx("Film frame — top in-plane", FCX_L, yin, PZ1 - AL, W, AT, AL, C_FRAME),
        bx("Film frame — bottom upstand", FCX_L, yperp, PZ0, W, AL, AT, C_FRAME),
        bx("Film frame — bottom in-plane", FCX_L, yin, PZ0, W, AT, AL, C_FRAME),
        bx("Film frame — left upstand", FCX_L, yperp, PZ0, AT, AL, PZ1 - PZ0, C_FRAME),
        bx("Film frame — left in-plane", FCX_L, yin, PZ0, AL, AT, PZ1 - PZ0, C_FRAME),
        bx("Film frame — right upstand", FCX_R - AT, yperp, PZ0, AT, AL, PZ1 - PZ0, C_FRAME),
        bx("Film frame — right in-plane", FCX_R - AL, yin, PZ0, AL, AT, PZ1 - PZ0, C_FRAME),
    ]
    # NOTE: the cross-slide ways are NOT here — they're fixed to the CARRIAGE (rail-aligned) in plane_carriage,
    # and the U-joint (here, in the frame) SLIDES along them as the frame rotates. So the ways keep their
    # positions and the frame moves relative to them (correct); they do not follow the frame's rotation.
    for (cx, fcx, fz, zc, cin, isb) in PLANE_CORNERS:
        t = f"({int(fcx)},{int(fz)})"
        # U-joint + stubs + shaft support + frame bolt + corner plate — SHARED (corner_slide_parts), offset -centre
        sp = corner_slide_parts(cx, fcx, fz, cin, isb, yc)
        for key, lbl in (("ujoint", "U-joint (Belden UJ-SS750x375)"), ("input_stub", "Input stub 3/8"),
                         ("shaft_support", "4040N12 304 shaft support"), ("output_stub", "Output stub 3/8"),
                         ("frame_bolt", "Frame-corner bolt"), ("corner_plate", "304 SS corner plate")):
            P.append(emit_slide(f"{lbl} {t}", sp[key], -px, -yc, -pz))
    return "\n".join(P)


def plane_carriage(cx, fz, zc, cin, isb, yc):
    """The RAIL-BOUND body for ONE corner — the captured skate (load + keeper rollers, both corners) +
    carriage plate + the TWO cross-slide ways (green Z, purple X). Built at ABSOLUTE coords (placed at
    identity); the DC translates it in Y ONLY (= the roll along the depth rail). It never rotates, so the
    ways stay RAIL-ALIGNED and the frame's U-joint SLIDES along them (the ways keep their positions and the
    frame moves relative to them — same rules as the Movement scene)."""
    ty = yc
    chan_w = CW_BOT
    inb = cx + cin * (chan_w / 2 + 14)
    fcx = cx + cin * FILM_INSET
    rz = zc - CD_BOT / 2 + HB_T + 16
    cpx0c = (inb - 6) if cin > 0 else (inb - 8)
    t = f"({int(cx)},{int(fz)})"
    P = []
    for ry in (ty + 8, ty + 48):
        P.append(ov.ruby_cylinder(f"Acetal skate wheel Ø32 {t} {int(ry)}", cx - 8, ry, rz, 16, 16, color=C_CAR, axis="x"))
    P.append(ov.ruby_box(f"Carriage plate {t}", cpx0c, ty + 1, fz - 6, 14, 86, (rz + 46) - (fz - 6), color=C_CAR))
    # the two cross-slide ways, RAIL-ALIGNED (fixed to the carriage) — SHARED (corner_slide_parts); the
    # U-joint (in the frame) rides them, so they keep their positions and the frame moves relative to them.
    sp = corner_slide_parts(cx, fcx, fz, cin, isb, yc)
    P.append(emit_slide(f"Vertical Z cross-slide way (green) {t}", sp["green"]))
    P.append(emit_slide(f"Horizontal X cross-slide way (purple) {t}", sp["purple"]))
    return "\n".join(P)


def whole_plane_dc(mode):
    """One-click DC (mode = 'Tilt'/'Swing'). The FRAME rotates (rotx/rotz) about the plane centre, while each
    CARRIAGE stays on its rail and only ROLLS in Y — so the carriage is never dragged off the track; the
    cross-slide takes up the perpendicular offset. Same rules as the Movement scene. Structure:
    WholePlane<mode> (move, onclick) → PlaneFrame<mode> (rot) + 4× PlaneCar<mode><i> (y-roll)."""
    rot_attr = "rotx" if mode == "Tilt" else "rotz"
    rot_val = 15
    cxr = (FCX_L + FCX_R) / 2.0
    czr = (PZ0 + PZ1) / 2.0
    yc = MID_Y
    tag = f"Plane {mode}"
    s = math.sin(math.radians(rot_val))
    car_ruby = ""
    for i, (cx, fcx, fz, zc, cin, isb) in enumerate(PLANE_CORNERS):
        # the carriage rolls in Y to track its U-joint's Y as the frame rotates (swing: dx·sinθ; tilt: -dz·sinθ)
        dyi = (fcx - cxr) * s if mode == "Swing" else -(fz - czr) * s
        car_ruby += f'''
car{mode}{i} = model.definitions.add("Plane carriage {mode} {i}")
ents = car{mode}{i}.entities
{plane_carriage(cx, fz, zc, cin, isb, yc)}
car{mode}{i}_inst = plw{mode}.entities.add_instance(car{mode}{i}, Geom::Transformation.new)
car{mode}{i}_inst.name = "Plane carriage {mode} {i}"; car{mode}{i}_inst.layer = model.layers["{tag}"]
[car{mode}{i}, car{mode}{i}_inst].each {{ |e| e.set_attribute(da, "_name", "PlaneCar{mode}{i}"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "y", 0.0) }}
car{mode}{i}_inst.set_attribute(da, "_y_formula", "WholePlane{mode}!move * {dyi:.2f}")
'''
    return f'''
# ═══ Whole plane — {mode}: FRAME rotates {rot_attr} about the centre; each CARRIAGE stays on its rail and
# only ROLLS in Y (the cross-slide absorbs the perpendicular offset) — same rules as the Movement scene. ═══
plw{mode} = model.definitions.add("Whole plane {mode}")
da = "dynamic_attributes"
frm{mode} = model.definitions.add("Plane frame {mode}")
ents = frm{mode}.entities
{plane_frame(cxr, czr, yc)}
frm{mode}_inst = plw{mode}.entities.add_instance(frm{mode}, Geom::Transformation.translation([{ov.mm(cxr)}, {ov.mm(yc)}, {ov.mm(czr)}]))
frm{mode}_inst.name = "Plane frame {mode}"; frm{mode}_inst.layer = model.layers["{tag}"]
[frm{mode}, frm{mode}_inst].each {{ |e| e.set_attribute(da, "_name", "PlaneFrame{mode}"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "{rot_attr}", 0.0) }}
frm{mode}_inst.set_attribute(da, "_{rot_attr}_formula", "WholePlane{mode}!move * {rot_val}")
{car_ruby}
plw{mode}_inst = entities.add_instance(plw{mode}, Geom::Transformation.new)
plw{mode}_inst.name = "Whole plane {mode}"; plw{mode}_inst.layer = model.layers["{tag}"]
[plw{mode}, plw{mode}_inst].each do |e|
  e.set_attribute(da, "_name", "WholePlane{mode}"); e.set_attribute(da, "_lengthunits", "MILLIMETERS"); e.set_attribute(da, "move", 0.0)
end
plw{mode}_inst.set_attribute(da, "_move_access", "VIEW")
plw{mode}_inst.set_attribute(da, "_move_label", "{mode}: click — frame {rot_attr}s, carriages roll on the rails")
plw{mode}_inst.set_attribute(da, "onclick", 'ANIMATE("move", 0, 1)')
plw{mode}_inst.set_attribute(da, "_onclick_access", "NONE")
pltxt{mode} = entities.add_text("CLICK: {mode} — the frame {rot_attr}s; each carriage stays on its rail and rolls in Y", Geom::Point3d.new({ov.mm(cxr)}, {ov.mm(yc + 300)}, {ov.mm(PZ1 + 150)}), Geom::Vector3d.new({ov.mm(300)}, {ov.mm(-300)}, {ov.mm(300)}))
pltxt{mode}.layer = model.layers["{tag}"] rescue nil
'''


def generate_ruby():
    mv_corners = ["BL", "TL", "BR", "TR"]
    mv = {c: movement(c, two_way=(c in MOVEMENT_TWO_WAY)) for c in mv_corners}
    comps = [
        ov.component("Corners", "Corners", corners()),
        ov.component("Film Plane", "Film Plane", film_plane()),
        ov.component("Pinhole", "Pinhole", pinhole()),
        ov.component("Context (walkway + IBC cantilever/beams)", "Context", context()),
    ] + [ov.component(f"Movement base ({c} corner)", "Movement", mv[c][0]) for c in mv_corners] + [
        ov.component("Container shell (no ceiling)", "Shell", shell()),
    ]
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
        # Whole-plane tilt / swing — the clickable rigid plane (with all 4 corner mechanisms) at the
        # container-depth MIDDLE, inside a ceiling-less shell.
        ("Whole plane — tilt", ["Shell", "Plane Tilt"], (2400, MID_Y, CH / 2, 6800)),
        ("Whole plane — swing", ["Shell", "Plane Swing"], (2400, MID_Y, CH / 2, 6800)),
    ]
    mv_dc = "".join(movement_dc(c, *mv[c][1:], two_way=(c in MOVEMENT_TWO_WAY)) for c in mv_corners)
    mv_dc += whole_plane_dc("Tilt") + whole_plane_dc("Swing")

    def scene_lit(n, tags, tgt):
        tg = "[" + ", ".join(f'"{t}"' for t in tags) + "]"
        cam = f"[{ov.mm(tgt[0])}, {ov.mm(tgt[1])}, {ov.mm(tgt[2])}, {ov.mm(tgt[3])}]"
        return f'["{n}", {tg}, {cam}]'
    # Overview + Corner detail come first; Movement + the two Whole-plane scenes are created AFTER Swing (top)
    iso_first_ruby = "[" + ", ".join(scene_lit(*s) for s in iso[:2]) + "]"
    iso_last_ruby = "[" + ", ".join(scene_lit(*s) for s in iso[2:]) + "]"
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

{ov.sketchfab_meta_ruby(SF_TITLE, SF_DESC, SF_ID, SF_TAGS)}
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
{iso_first_ruby}.each {{ |name, tags, tgt|
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

# ── Movement + the two Whole-plane scenes (iso), AFTER Swing (top) ──
{iso_last_ruby}.each {{ |name, tags, tgt|
  model.layers.each {{ |l| l.visible = (l == default_layer || tags.include?(l.name)) }}
  t = Geom::Point3d.new(tgt[0], tgt[1], tgt[2])
  cdir = Geom::Vector3d.new(0.5, -0.7, 0.4); cdir.normalize!
  model.active_view.camera = Sketchup::Camera.new(t.offset(cdir, tgt[3]), t, Z_AXIS)
  page = model.pages.add(name)
  page.use_camera = true
}}

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
