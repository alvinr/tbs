#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""Generate the TBS-001 Spray-Bar Gantry SketchUp model (logical model: spraybar).

A focused model of the spray-bar gantry: the 40×25×3mm 304-SS RHS beam (its
side-mounted 3/4" LDPE manifold carries the wash water), the two wheel carriages
that roll on the tray floor, the spray jets, the feed hose, and the telescoping
push pole. REUSES the ruby helpers from the Overview generator
(generate_sketchup_model.py). Three scenes:
    1. Beam               (the SHS beam + spray jets + end caps)
    2. Carriage Assembly  (beam + the two wheel carriages, on a tray-floor patch)
    3. Combined           (everything + feed hose + push pole)

Usage (build into a SketchUp document — open a NEW blank doc first):
    python3 src/models/generate_spraybar_model.py --save        # write spraybar.rb
    python3 src/models/generate_spraybar_model.py --save --send # + send to the ACTIVE doc
"""
import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import generate_sketchup_model as ov          # ruby helpers + component()

from tbs_constants import PROC_OPEN_X_L, PROC_OPEN_X_R, SPRAY_BAR_BEAM, SPRAY_BAR_BEAM_H, SPRAY_BAR_POLY_OD, SPRAY_BAR_POLY_ID, SPRAY_BAR_Z_BOT, SPRAY_BAR_Z_TOP, SPRAY_BAR_WHEEL_DIA, SPRAY_BAR_WHEEL_W, SPRAY_BAR_WHEEL_SP, SPRAY_BAR_AXLE_Z, SPRAY_BAR_N_NOZZLES, PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR, PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_RIM, SPRAY_BAR_TRAY_FLOOR, PROC_TRAY_DRAIN_X, PROC_TRAY_DRAIN_YD, PROC_TRAY_SUMP_W, PROC_TRAY_SUMP_D, PROC_TRAY_SUMP_Z

TAGS = ["Beam", "Carriage L", "Carriage R", "Tray Ref", "Feed & Pole", "Tray", "Labels"]

# Representative gantry Yd position (it travels in Yd; park it mid-tray).
GY = (PROC_TRAY_YD_NEAR + PROC_TRAY_YD_FAR) // 2        # 1180

# Colors
C_ALUM   = "#C8D8E8"   # aluminum SHS beam + pole
C_STEEL  = "#B0B0B8"   # carriage plate / clamps
C_NYLON  = "#33343A"   # acetal (Delrin) wheels
C_WATER  = "#2060C0"   # feed hose / water in pipe
C_TRAY   = "#9FB8C8"   # tray-floor reference patch
C_POLY   = "#2A2A2A"   # LDPE irrigation poly pipe (side-mounted manifold)
C_NOZZLE = "#3B7A3B"   # flat-fan spray nozzles
C_SS     = "#B8BCC4"   # 304 stainless RHS beam
C_CLAMP  = "#C0C0C8"   # saddle / U-clamps
C_BOLT   = "#80808A"   # axle + bolts

# Beam / carriages / poly-pipe span the FULL TRAY width (matching the 2D diagram,
# generate_spray_bar_diagram.py — PROC_TRAY_X±30), so the wheels reach the tray
# edges. The NOZZLES stay in the print OPEN zone (PROC_OPEN_X). (Bugfix 2026-06-06:
# the 3D beam previously used PROC_OPEN_X and fell 300mm short of the tray each side.)
XL, XR = PROC_TRAY_X_L + 30, PROC_TRAY_X_R - 30          # beam span = tray width (200..4599)
NXL, NXR = PROC_OPEN_X_L, PROC_OPEN_X_R                  # nozzle span = print open zone
S = SPRAY_BAR_BEAM                                       # 40 (Yd width)
ZB, ZT = SPRAY_BAR_Z_BOT, SPRAY_BAR_Z_TOP               # 29 .. 54 (@ low corner)


def ruby_saddle(name, xc, sw, cy, cz, ri, t, a0_deg, a1_deg, color, n=24):
    """Curved saddle / conduit-style clamp: an annular band (inner radius `ri`,
    thickness `t`) wrapping from `a0_deg` to `a1_deg` around a Yd-Z circle centerd
    at (cy, cz), extruded along X by `sw` (centerd on `xc`). Cradles under the
    axle and rises up both sides toward the plate where the bolts pass through."""
    ro = ri + t
    x0 = xc - sw / 2.0
    a0, a1 = math.radians(a0_deg), math.radians(a1_deg)
    pts = []
    for i in range(n + 1):                       # outer arc forward
        a = a0 + (a1 - a0) * i / n
        pts.append((cy + ro * math.cos(a), cz + ro * math.sin(a)))
    for i in range(n, -1, -1):                   # inner arc back
        a = a0 + (a1 - a0) * i / n
        pts.append((cy + ri * math.cos(a), cz + ri * math.sin(a)))
    pts_ruby = ', '.join(
        f'[{ov.mm(round(x0, 2))},{ov.mm(round(y, 2))},{ov.mm(round(z, 2))}]'
        for y, z in pts)
    r_, g_, b_ = ov.hex_to_rgb(color)
    mat_nm = ov.shared_mat_name(name, color, None)
    return '\n'.join([
        f'  # {name}',
        f'  grp = ents.add_group',
        f'  grp.name = "{name}"',
        f'  ge = grp.entities',
        f'  face = ge.add_face([{pts_ruby}])',
        f'  face.reverse! if face.normal.x < 0',
        f'  face.pushpull({ov.mm(sw)})',
        f'  mat = model.materials["{mat_nm}"] || model.materials.add("{mat_nm}")',
        f'  mat.color = Sketchup::Color.new({r_}, {g_}, {b_})',
        f'  mat.alpha = 1.0',
        f'  grp.material = mat',
        '',
    ])


def build_beam():
    parts = []
    BH = SPRAY_BAR_BEAM_H                       # 25 — beam height in Z (laid flat)
    poly_cy = GY + S / 2 + SPRAY_BAR_POLY_OD / 2   # poly on the beam's inboard (+Yd) side face
    poly_cz = ZB + BH / 2                          # poly center at beam mid-height
    # 40×25×3 304-SS RHS beam (laid flat — low profile for grate clearance)
    parts.append(ov.ruby_box("Spray Beam 40x25x3 304-SS RHS",
                             XL, GY - S / 2, ZB, XR - XL, S, BH, color=C_SS))
    # end caps (left = feed end)
    parts.append(ov.ruby_box("Beam End Cap (feed)",
                             XL - 4, GY - S / 2, ZB, 4, S, BH, color=C_SS))
    parts.append(ov.ruby_box("Beam End Cap",
                             XR, GY - S / 2, ZB, 4, S, BH, color=C_SS))
    # 3/4" LDPE poly manifold — SIDE-mounted on the beam's inboard face (+ water core)
    parts.append(ov.ruby_cylinder("Side Poly Manifold (3/4 LDPE)",
                                  XL, poly_cy, poly_cz, SPRAY_BAR_POLY_OD / 2, XR - XL,
                                  color=C_POLY, axis="x"))
    parts.append(ov.ruby_cylinder("Water in Manifold",
                                  XL, poly_cy, poly_cz, SPRAY_BAR_POLY_ID / 2, XR - XL,
                                  color=C_WATER, axis="x", alpha=0.55))
    # flat-fan nozzles — side-tapped (saddle-tee) into the poly manifold, spray down-and-in
    # (true 150mm pitch, centered on the span)
    sp = 150
    margin = ((NXR - NXL) - (SPRAY_BAR_N_NOZZLES - 1) * sp) / 2
    for i in range(SPRAY_BAR_N_NOZZLES):
        nx = NXL + margin + i * sp
        # saddle-tee barb into the poly + nozzle body hanging below it
        parts.append(ov.ruby_cylinder("Nozzle Body", nx, poly_cy, poly_cz - 12, 4, 12,
                                      color=C_NOZZLE, axis="z"))
        parts.append(ov.ruby_cylinder("Nozzle Tip", nx, poly_cy, poly_cz - 18, 6.5, 6,
                                      color=C_NOZZLE, axis="z"))
    return '\n'.join(parts)


def _csk_head(name, cx, cy, z0, z1, r0, r1, color, n=12):
    """A countersunk flat-head frustum: wide flush face (r0) at z0 tapering to the shank (r1) at z1 —
    the 3D analogue of the 2D chamfered CSK head that sits flush in the clamp underside."""
    ring = lambda z, r: [(cx + r * math.cos(2 * math.pi * i / n),
                          cy + r * math.sin(2 * math.pi * i / n), z) for i in range(n)]
    bot, top = ring(z0, r0), ring(z1, r1)
    P = lambda p: f'[{ov.mm(p[0])},{ov.mm(p[1])},{ov.mm(p[2])}]'
    L = [f'  # {name}', '  grp = ents.add_group', f'  grp.name = "{name}"', '  ge = grp.entities']
    for i in range(n):                                   # tapered skirt (quads)
        j = (i + 1) % n
        L.append(f'  ge.add_face({P(bot[i])}, {P(bot[j])}, {P(top[j])}, {P(top[i])})')
    L.append('  ge.add_face(' + ', '.join(P(p) for p in bot) + ')')   # flush bottom cap
    r, g, b = ov.hex_to_rgb(color)
    L += [f'  mat = model.materials["{name}"] || model.materials.add("{name}")',
          f'  mat.color = Sketchup::Color.new({r}, {g}, {b})',
          '  grp.material = mat', '']
    return '\n'.join(L)


def _carriage(xend, side, din):
    """One wheel carriage (2D Detail C/D). The carriage is the full beam width in
    X with its OUTER edge flush with the beam end (`din` = +1 left end, -1 right).
    Notched 5mm Al plate (two wings) + two Ø32 acetal wheels on Ø10 through-axles
    (saddle clamps + M5 bolts); the beam is sandwiched by TWO flat C-clamps (one
    per face) that hook over the beam top and bolt down through the plate."""
    parts = []
    ww, wd, az = SPRAY_BAR_WHEEL_W, SPRAY_BAR_WHEEL_DIA, SPRAY_BAR_AXLE_Z  # 20, 32, 36
    half = SPRAY_BAR_WHEEL_SP / 2          # 100 — wheel offset in Yd
    plate_z = az + 2                        # 29 — plate bottom (2mm above axle)
    plate_t = 5                             # 5mm Al plate
    plate_top = plate_z + plate_t           # 34
    CW = S                                  # carriage width in X (= beam width, 40)
    cx0 = xend if din > 0 else xend - CW    # outer X edge flush with the beam end
    cxc = cx0 + CW / 2                       # carriage / wheel center X
    notch = S / 2                            # 20 — wings extend in to meet the beam faces

    # ── notched 5mm Al carriage plate — two wings either side of the beam ──
    parts.append(ov.ruby_box(f"Carriage Plate L {side}",
                             cx0, GY - half - 18, plate_z,
                             CW, (GY - notch) - (GY - half - 18), plate_t, color=C_ALUM))
    parts.append(ov.ruby_box(f"Carriage Plate R {side}",
                             cx0, GY + notch, plate_z,
                             CW, (GY + half + 18) - (GY + notch), plate_t, color=C_ALUM))

    # ── each wheel: Ø32 acetal on a Ø10 through-axle (centerd on the wing). The
    # axle is retained by a curved saddle clamp on EACH side of the wheel (like a
    # conduit/pipe saddle), each bolted down through the plate with two bolts
    # straddling the axle — two bolts either side of the wheel. ──
    sw = 19                                   # saddle width along the axle — 3/4" (19mm) flat bar
    sgap = ww / 2 + 11.5                      # saddle offset from wheel center — 3/4" strap
    #                                           moved out to clear the wheel by 2mm
    for dy in (-half, half):
        cy = GY + dy
        parts.append(ov.ruby_cylinder(f"Wheel {side}",
                                      cxc - ww / 2, cy, az, wd / 2, ww,
                                      color=C_NYLON, axis="x"))
        parts.append(ov.ruby_cylinder(f"Axle Pin 10mm {side}",
                                      cxc - ww / 2 - 23, cy, az, 5, ww + 46,
                                      color=C_BOLT, axis="x"))
        for sx_ in (cxc - sgap, cxc + sgap):  # a saddle clamp either side of the wheel
            # curved hump cradling under the axle — 1/8" (3.18mm) 304 SS flat bar
            parts.append(ruby_saddle(f"Axle Saddle {side}",
                                     sx_, sw, cy, az, 6, 3.18, 180, 360, C_CLAMP))
            for sgn in (-1, 1):               # a flat 12mm foot each side + M5 bolt through it
                foot_y0 = cy + 6 if sgn > 0 else cy - 18
                parts.append(ov.ruby_box(f"Axle Saddle Foot {side}",
                                         sx_ - sw / 2, foot_y0, plate_z - 3.18, sw, 12, 3.18,
                                         color=C_CLAMP))
                parts.append(ov.ruby_cylinder(f"Axle Bolt {side}",
                                              sx_, cy + sgn * 12, plate_z - 4, 2.5,
                                              (plate_top + 3) - (plate_z - 4), color=C_BOLT, axis="z"))

    # ── beam clamped vertically: a BOTTOM clamp under the beam + a TOP clamp over
    # it, drawn together by bolts at the two sides — sandwiches the beam. Both are
    # the full carriage width with the outer edge flush with the beam end. ──
    ct = 3                                   # clamp flat-bar thickness
    cl_y0, cl_yw = GY - 32, 64               # extended so the Ø5 bolt holes are fully enclosed
    parts.append(ov.ruby_box(f"Bottom Clamp {side}",
                             cx0, cl_y0, ZB - ct, CW, cl_yw, ct, color=C_CLAMP))
    parts.append(ov.ruby_box(f"Top Clamp {side}",
                             cx0, cl_y0, ZT, CW, cl_yw, ct, color=C_CLAMP))
    # two bolts per side (4 total) — spaced along the carriage width, just outside
    # each beam face; one solid spacer block per side fills the gap between the
    # plates, setting the clamp height to the beam so tightening grips the beam.
    for by_ in (GY - (S / 2 + 4), GY + (S / 2 + 4)):     # near + far beam faces
        parts.append(ov.ruby_box(f"Clamp Spacer {side}",
                                 cx0 + 4, by_ - 4, ZB, CW - 8, 8, ZT - ZB, color=C_ALUM))
        for bx_ in (cx0 + 9, cx0 + CW - 9):             # fore + aft along the width
            # COUNTERSUNK on the TRAY-FACING underside (matches the 2D "M6 CSK flush underside —
            # clearance"): the shaft is flush at the bottom-clamp underside (no proud head toward the
            # tray) with a CSK frustum head seated in the clamp; only the TOP nut stays proud.
            parts.append(ov.ruby_cylinder(f"Clamp Bolt {side}",
                                          bx_, by_, ZB - ct, 2.5,
                                          (ZT + ct + 4) - (ZB - ct), color=C_BOLT, axis="z"))
            parts.append(_csk_head(f"Clamp Bolt CSK Head {side}", bx_, by_,
                                   ZB - ct, ZB, 4.5, 2.5, C_BOLT))
    return parts


def build_carriages(include_floor=True):
    parts = []
    parts += _carriage(XL, "L", 1)
    parts += _carriage(XR, "R", -1)
    if include_floor:
        # tray-floor reference patch (the wheels roll on this 2mm SS tray floor).
        # Omitted when embedded in the overview, which has its own processing tray.
        parts.append(ov.ruby_box("Tray Floor (ref)",
                                 XL - 60, GY - half_band(), 0,
                                 (XR - XL) + 120, 2 * half_band(), 2,
                                 color=C_TRAY, alpha=0.25))
    return '\n'.join(parts)


def half_band():
    return SPRAY_BAR_WHEEL_SP / 2 + 60                    # 160 — patch half-width in Yd


def build_carriage_one(xend, side, din):
    """One wheel carriage on its own tag (so a scene can show just one)."""
    return '\n'.join(_carriage(xend, side, din))


def tray_ref_patch():
    """The small tray-floor reference patch the wheels roll on — its OWN tag, shown
    only in the carriage-only scenes (the Combined / Processing Tray scenes have the
    REAL tray, so the ref patch would double up under the beam)."""
    return ov.ruby_box("Tray Floor (ref)",
                       XL - 60, GY - half_band(), ov.PROC_TRAY_FLOOR_Z_LOW - 2,
                       (XR - XL) + 120, 2 * half_band(), 2,
                       color=C_TRAY, alpha=0.25)


# ── "Labeled" scene callouts (project rule: every .skp gets a Labeled scene) ──
SPRAYBAR_LABELS = [   # (instance name, text, leader Δx,Δy,Δz mm)
    ("Processing Tray", "PROCESSING TRAY", 500, -700, 700),
]
SPRAYBAR_POINT_LABELS = [   # (x,y,z,text,Δx,Δy,Δz)
    (1400, 1180,  60, "SPRAY BEAM\n(40 RHS + 3/4-in LDPE bore)", 0, -900,  650),
    (  XL, 1180,  60, "WHEEL CARRIAGE\n(saddle clamp + 2 wheels)", -750, -350, 600),
    (  XR, 1180,  60, "WHEEL CARRIAGE",                          700, -350,  600),  # 2nd (right) carriage
    ( 950, 1180,  18, "SPRAY NOZZLES\n(39 90-deg down-jets @ 100mm)", 250, -950,  380),
    (2399, 1180,  90, "FEED POLE + BALL JOINT",                 700, -250,  800),  # anchor on the ball-joint socket
    (2399, 1200,  70, "CENTER FEED\n(single inlet tee)",       -600, -700,  650),  # anchor on the center feed tee
    (4550,   80,   0, "DRAIN SUMP",                             200, -600,  450),  # tray drain sump (near-right corner)
]


def spraybar_labels():
    """Ruby that adds in-model text callouts (with leaders) on the major parts, on
    the 'Labels' tag — instance-anchored at bounds top-centre + point-anchored."""
    rows = []
    for name, text, dx, dy, dz in SPRAYBAR_LABELS:
        rows.append(
            f'inst = entities.grep(Sketchup::ComponentInstance).find {{ |i| i.name == "{name}" }}\n'
            f'if inst\n'
            f'  bb = inst.bounds\n'
            f'  anc = Geom::Point3d.new(bb.center.x, bb.center.y, bb.max.z)\n'
            f'  txt = entities.add_text("{text}", anc, Geom::Vector3d.new({ov.mm(dx)}, {ov.mm(dy)}, {ov.mm(dz)}))\n'
            f'  txt.layer = model.layers["Labels"] rescue nil\n'
            f'end')
    for x, y, z, text, dx, dy, dz in SPRAYBAR_POINT_LABELS:
        rows.append(
            f'anc = Geom::Point3d.new({ov.mm(x)}, {ov.mm(y)}, {ov.mm(z)})\n'
            f'txt = entities.add_text("{text}", anc, Geom::Vector3d.new({ov.mm(dx)}, {ov.mm(dy)}, {ov.mm(dz)}))\n'
            f'txt.layer = model.layers["Labels"] rescue nil')
    return '\n'.join(rows)


def build_feed_pole():
    parts = []
    cx = (XL + XR) / 2          # pole/joint X — beam center (POLE_X)
    by = GY                      # gantry Yd
    c_joint = "#C8B070"          # zinc/brass ball-joint socket
    c_bolt = "#50505A"           # bolts / U-bolt
    c_ss = "#D8D0BC"             # SS ball + M12 stud

    # ── pole connection: flange-base ball joint fastened to the beam TOP face ──
    # flange (44×44×5) on the beam top, held by 4 self-tapping screws (no internal
    # beam access for nuts) — nothing overhangs the ball, so the arm articulates free
    parts.append(ov.ruby_box("Pole Mount Flange",
                             cx - 22, by - 22, ZT, 44, 44, 5, color=C_STEEL))
    for sxx in (cx - 16, cx + 16):
        for syy in (by - 16, by + 16):
            parts.append(ov.ruby_cylinder("Flange Self-Tapping Screw",
                                          sxx, syy, ZT - 4, 1.8, 9, color=c_bolt, axis="z"))
            parts.append(ov.ruby_cylinder("Flange Screw Head",
                                          sxx, syy, ZT + 5, 3, 2.5, color=c_bolt, axis="z"))
    # socket housing — the ball-joint body, Ø36 × 28
    parts.append(ov.ruby_cylinder("Ball-Joint Socket (20mm)",
                                  cx, by, ZT + 5, 18, 28, color=c_joint, axis="z"))

    # ── articulated stud + arm tube + telescoping pole to the operator ──
    op_y, op_z = 640, 1300             # operator hand — pole raised ~25° steeper (toward vertical) for coil separation
    ball_z = ZT + 5 + 14 + 2           # ≈ 71 — ball center inside the socket
    mid_y, mid_z = (by + op_y) / 2, (ball_z + op_z) / 2
    # M12 stud emerging from the socket, angled toward the operator (articulated)
    parts.append(ov.ruby_pipe("Ball-Joint Stud (M12)",
                              (cx, by, ball_z), (cx, by - 28, ball_z + 24), 6, color=c_ss))
    # Ø25 aluminum arm tube clamped onto the stud
    parts.append(ov.ruby_pipe("Arm Tube (25 OD Al)",
                              (cx, by - 24, ball_z + 20), (cx, mid_y, mid_z), 12.5, color=C_ALUM))
    # pinch bolt clamping the arm onto the stud
    parts.append(ov.ruby_cylinder("Pinch Bolt",
                                  cx - 18, by - 26, ball_z + 26, 3, 36, color=c_bolt, axis="x"))
    # telescoping pole (thinner) continuing to the operator's hand
    parts.append(ov.ruby_pipe("Telescoping Pole",
                              (cx, mid_y, mid_z), (cx, op_y, op_z), 11, color=C_ALUM))
    # T-handle at the operator end
    parts.append(ov.ruby_cylinder("Pole Handle",
                                  cx - 90, op_y, op_z, 9, 180, color=C_STEEL, axis="x"))

    # ── water feed: the blue hose runs down the pole and makes a SINGLE center feed
    #    into the side poly manifold at the beam center (Option 1 — the ¾" manifold is
    #    over-bored for the 3.5 GPM flow, so pressure holds uniform end-to-end from one
    #    feed; no distribution manifold or feed-tube fan needed). ──
    BH = SPRAY_BAR_BEAM_H
    poly_cy = GY + S / 2 + SPRAY_BAR_POLY_OD / 2     # side manifold Yd (inboard face)
    poly_cz = ZB + BH / 2                            # side manifold Z (beam mid-height)
    # hose down the pole, then a CORRUGATED FLEX CONNECTOR (right-angle) dropping onto
    # the single center inlet tee on the side manifold. The flex absorbs the handle's
    # articulation; zip-tie loops bind the hose to the pole.
    O = (cx, op_y, op_z)
    M = (cx, mid_y, mid_z)
    A = (cx, by - 24, ball_z + 20)          # arm base, near the ball joint
    hoff = 20                                # pole radius + hose radius — tangent
    parts.append(ov.ruby_pipe("Feed Hose (upper)",
                              (cx + hoff, O[1], O[2]), (cx + hoff, M[1], M[2]), 8, color=C_WATER))
    parts.append(ov.ruby_pipe("Feed Hose (lower)",
                              (cx + hoff, M[1], M[2]), (cx + hoff, A[1], A[2]), 8, color=C_WATER))
    parts.append(ov.ruby_flex_run("Feed Flex Connector",
                                  [(cx + hoff, A[1], A[2]), (cx + hoff, poly_cy, A[2]),
                                   (cx + hoff, poly_cy, poly_cz + 18),
                                   (cx, poly_cy, poly_cz + 18)],
                                  7, color=C_WATER, elbow_r=10))
    # grey zip-tie loops binding the hose to the pole at ~200mm intervals (report §3.12)
    for q1, q2 in ((O, M), (M, A)):
        dd = (0.0, q2[1] - q1[1], q2[2] - q1[2])
        seg_l = math.sqrt(dd[1] ** 2 + dd[2] ** 2)
        vl = math.sqrt(dd[2] ** 2 + dd[1] ** 2)
        vh = (0.0, dd[2] / vl, -dd[1] / vl)          # in-plane axis ⟂ to pole and to X
        nt = max(1, int(round(seg_l / 200)))
        for s in range(nt):
            t = (s + 0.5) / nt
            # loop centerd on the combined bundle (shifted toward the larger pole),
            # with enough perpendicular radius to clear the Ø25 arm tube
            cyz = (cx + 8, q1[1] + t * dd[1], q1[2] + t * dd[2])
            loop = []
            for k in range(10):
                th = 2 * math.pi * k / 10
                ca, sb = 23 * math.cos(th), 16.5 * math.sin(th)
                loop.append((cyz[0] + ca, cyz[1] + sb * vh[1], cyz[2] + sb * vh[2]))
            for k in range(10):
                parts.append(ov.ruby_pipe("Zip Tie", loop[k], loop[(k + 1) % 10], 1.2,
                                          color="#888888", n=6))
    # single center-feed barbed inlet tee into the SIDE poly manifold at the beam center
    parts.append(ov.ruby_cylinder("Center Feed Barb Tee", cx, poly_cy, poly_cz - 2, 5, 18,
                 color=C_NOZZLE, axis="z"))
    return '\n'.join(parts)


def build_tray():
    """The 304 SS processing tray the gantry rolls in: floor + 50mm rim walls +
    drain sump. Drawn translucent so the spray bar reads inside it."""
    parts = []
    xl, xr = PROC_TRAY_X_L, PROC_TRAY_X_R
    yn, yf = PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR
    w, d = xr - xl, yf - yn
    rim, ft, wt = PROC_TRAY_RIM, SPRAY_BAR_TRAY_FLOOR, 3   # rim height, floor + wall thickness
    zc = ov.PROC_TRAY_FLOOR_Z_LOW                         # 20 — pan RAISED so the sump bottom rests on Z0
    parts.append(ov.ruby_box("Tray Shim Base", xl, yn, 0, w, d, zc - ft, color="#D8CFBC", alpha=0.4))
    parts.append(ov.ruby_box("Tray Floor", xl, yn, zc - ft, w, d, ft, color=C_TRAY, alpha=0.55))
    parts.append(ov.ruby_box("Tray Rim Near", xl, yn, zc - ft, w, wt, rim, color=C_TRAY, alpha=0.3))
    parts.append(ov.ruby_box("Tray Rim Far", xl, yf - wt, zc - ft, w, wt, rim, color=C_TRAY, alpha=0.3))
    parts.append(ov.ruby_box("Tray Rim Left", xl, yn, zc - ft, wt, d, rim, color=C_TRAY, alpha=0.3))
    parts.append(ov.ruby_box("Tray Rim Right", xr - wt, yn, zc - ft, wt, d, rim, color=C_TRAY, alpha=0.3))
    # drain sump well — bottom rests on the container floor (Z0), up to the raised pan floor
    parts.append(ov.ruby_box("Tray Sump",
                             PROC_TRAY_DRAIN_X - PROC_TRAY_SUMP_W / 2, PROC_TRAY_DRAIN_YD,
                             0, PROC_TRAY_SUMP_W, PROC_TRAY_SUMP_D,
                             PROC_TRAY_SUMP_Z, color=C_TRAY, alpha=0.55))
    return '\n'.join(parts)


def generate_ruby():
    comps = [
        ov.component("Spray Beam", "Beam", build_beam()),
        ov.component("Wheel Carriage L", "Carriage L", build_carriage_one(XL, "L", 1)),
        ov.component("Wheel Carriage R", "Carriage R", build_carriage_one(XR, "R", -1)),
        ov.component("Tray Floor Ref", "Tray Ref", tray_ref_patch()),
        ov.component("Feed & Push Pole", "Feed & Pole", build_feed_pole()),
        ov.component("Processing Tray", "Tray", build_tray()),
    ]
    body = '\n'.join(comps)
    tags_ruby = '\n'.join(
        f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep_tags_ruby = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'
    full = ["Beam", "Carriage L", "Carriage R", "Feed & Pole", "Tray"]  # no Tray Ref
    # (name, visible tags, optional close-up target [x,y,z,standoff] mm or None)
    scenes = [
        ("Overview", full, None),   # full assembly — listed first (was "Combined")
        ("Beam", ["Beam"], None),
        ("Carriage Assembly", ["Beam", "Carriage L", "Carriage R", "Tray Ref"], None),
        ("One Carriage", ["Carriage L"], (XL, GY, 55, 480)),
        ("Pole & Ball Joint", ["Beam", "Feed & Pole"], None),
        ("Processing Tray", ["Tray", "Beam", "Carriage L", "Carriage R"], None),
        ("Labeled", full + ["Labels"], None),
    ]

    def scene_lit(n, tags, tgt):
        tg = '[' + ', '.join(f'"{t}"' for t in tags) + ']'
        cam = 'nil' if tgt is None else \
            f'[{ov.mm(tgt[0])}, {ov.mm(tgt[1])}, {ov.mm(tgt[2])}, {ov.mm(tgt[3])}]'
        return f'["{n}", {tg}, {cam}]'
    scenes_ruby = '[' + ', '.join(scene_lit(*s) for s in scenes) + ']'

    sf_meta = ov.sketchfab_meta_ruby(
        "TBS-001 Spraybar Model",
        "The processing tray provides the containment surface and the spray bar delivers even "
        "water distribution across the full print width.",
        "18fb381fbf48459cac25dcaa23958387", "sketchup")

    return f'''# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/ — do not edit this .rb directly.
model = Sketchup.active_model
model.start_operation("TBS-001 Spray-Bar Gantry", true)
entities = model.active_entities

opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# Idempotent rebuild: erase all prior groups/instances.
to_erase = entities.to_a.select {{ |e|
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text)
}}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each {{ |p| model.pages.erase(p) }}

{sf_meta}
{tags_ruby}

{body}

# ── "Labeled" scene callouts (Labels tag — shown only in the "Labeled" scene) ──
{spraybar_labels()}

{ov.license_note()}

model.definitions.purge_unused
model.materials.purge_unused

keep_tags = {keep_tags_ruby}
default_layer = model.layers[0]
model.layers.to_a.each {{ |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}}

dir = Geom::Vector3d.new(0.5, -0.78, 0.38); dir.normalize!

{scenes_ruby}.each {{ |name, tags, tgt|
  model.layers.each {{ |l| l.visible = (l == default_layer || tags.include?(l.name)) }}
  if tgt
    # close-up: aim at the target with a tight standoff (no zoom_extents); use a
    # direction nearly PERPENDICULAR to the beam (mostly −Y) so the carriage reads
    # rather than the beam vanishing down the line of sight.
    t = Geom::Point3d.new(tgt[0], tgt[1], tgt[2])
    cdir = Geom::Vector3d.new(0.18, -0.88, 0.44); cdir.normalize!
    model.active_view.camera = Sketchup::Camera.new(t.offset(cdir, tgt[3]), t, Z_AXIS)
  else
    # frame just this scene's visible geometry (the tray is much larger than the bar)
    ctr = model.bounds.center
    eye = ctr.offset(dir, model.bounds.diagonal * 1.4)
    model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
    model.active_view.zoom_extents
  end
  page = model.pages.add(name)
  page.use_camera = true
}}
model.layers.each {{ |l| l.visible = true }}

model.commit_operation
{{ success: true, model: "Spray-Bar Gantry",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }}.to_json
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate the TBS-001 Spray-Bar Gantry SketchUp model")
    parser.add_argument("--save", action="store_true",
                        help="Write Ruby to src/models/spraybar.rb")
    parser.add_argument("--send", action="store_true",
                        help="Send the Ruby to the ACTIVE SketchUp document "
                             "(clears it first - open a NEW doc before sending)")
    args = parser.parse_args()

    ruby = generate_ruby()
    if args.save:
        out = os.path.join(os.path.dirname(__file__), "spraybar.rb")
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
