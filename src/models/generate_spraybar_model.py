#!/usr/bin/env python3
"""Generate the TBS-001 Spray-Bar Gantry SketchUp model (logical model: spraybar).

A focused model of the spray-bar gantry: the 40×40×3mm aluminum SHS beam (its
34mm bore carries the wash water — no separate pipe), the two wheel carriages
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

from tbs_constants import (
    PROC_OPEN_X_L, PROC_OPEN_X_R, SPRAY_BAR_BEAM, SPRAY_BAR_BEAM_T,
    SPRAY_BAR_BORE, SPRAY_BAR_POLY_OD, SPRAY_BAR_POLY_ID,
    SPRAY_BAR_Z_BOT, SPRAY_BAR_Z_TOP, SPRAY_BAR_WHEEL_DIA, SPRAY_BAR_WHEEL_W,
    SPRAY_BAR_WHEEL_SP, SPRAY_BAR_AXLE_Z, SPRAY_BAR_N_NOZZLES,
    SPRAY_BAR_FEED_Z, PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR,
    PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_RIM, SPRAY_BAR_TRAY_FLOOR,
    PROC_TRAY_DRAIN_X, PROC_TRAY_DRAIN_YD,
    PROC_TRAY_SUMP_W, PROC_TRAY_SUMP_D, PROC_TRAY_SUMP_Z,
)

TAGS = ["Beam", "Carriages", "Feed & Pole", "Tray"]

# Representative gantry Yd position (it travels in Yd; park it mid-tray).
GY = (PROC_TRAY_YD_NEAR + PROC_TRAY_YD_FAR) // 2        # 1180

# Colours
C_ALUM   = "#C8D8E8"   # aluminum SHS beam + pole
C_STEEL  = "#B0B0B8"   # carriage plate / clamps
C_NYLON  = "#33343A"   # nylon wheels
C_WATER  = "#2060C0"   # feed hose / water in pipe
C_TRAY   = "#9FB8C8"   # tray-floor reference patch
C_POLY   = "#2A2A2A"   # LDPE irrigation poly pipe (inside the bore)
C_NOZZLE = "#3B7A3B"   # flat-fan spray nozzles
C_CLAMP  = "#C0C0C8"   # saddle / U-clamps
C_BOLT   = "#80808A"   # axle + bolts

XL, XR = PROC_OPEN_X_L, PROC_OPEN_X_R
S = SPRAY_BAR_BEAM                                       # 40
ZB, ZT = SPRAY_BAR_Z_BOT, SPRAY_BAR_Z_TOP               # 20 .. 60


def ruby_saddle(name, xc, sw, cy, cz, ri, t, a0_deg, a1_deg, color, n=24):
    """Curved saddle / conduit-style clamp: an annular band (inner radius `ri`,
    thickness `t`) wrapping from `a0_deg` to `a1_deg` around a Yd-Z circle centred
    at (cy, cz), extruded along X by `sw` (centred on `xc`). Cradles under the
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
    bore_cz = ZB + S / 2                   # bore / poly-pipe centre Z (= 40)
    # 40x40 SHS beam — translucent so the internal irrigation pipe reads
    parts.append(ov.ruby_box("Spray Beam 40x40x3 Al SHS",
                             XL, GY - S / 2, ZB, XR - XL, S, S,
                             color=C_ALUM, alpha=0.45))
    # end caps (left = feed end)
    parts.append(ov.ruby_box("Beam End Cap (feed)",
                             XL - 4, GY - S / 2, ZB, 4, S, S, color=C_ALUM))
    parts.append(ov.ruby_box("Beam End Cap",
                             XR, GY - S / 2, ZB, 4, S, S, color=C_ALUM))
    # 3/4" LDPE irrigation poly pipe inside the bore (+ translucent water core)
    parts.append(ov.ruby_cylinder("Irrigation Poly Pipe (3/4 LDPE)",
                                  XL, GY, bore_cz, SPRAY_BAR_POLY_OD / 2, XR - XL,
                                  color=C_POLY, axis="x"))
    parts.append(ov.ruby_cylinder("Water in Pipe",
                                  XL, GY, bore_cz, SPRAY_BAR_POLY_ID / 2, XR - XL,
                                  color=C_WATER, axis="x", alpha=0.55))
    # flat-fan nozzles barbed into the poly pipe, spraying down through the beam
    # (true 150mm pitch, centred on the span)
    sp = 150
    margin = ((XR - XL) - (SPRAY_BAR_N_NOZZLES - 1) * sp) / 2
    for i in range(SPRAY_BAR_N_NOZZLES):
        nx = XL + margin + i * sp
        # threaded body: barbs UP from the beam bottom through the poly pipe BOTTOM
        # wall, tip ending inside the bore (one wall only — not through the top wall)
        parts.append(ov.ruby_cylinder("Nozzle Body", nx, GY, ZB, 4,
                                      bore_cz - ZB, color=C_NOZZLE, axis="z"))
        # flat-fan nozzle below the beam, seated FLUSH against the beam bottom
        parts.append(ov.ruby_cylinder("Nozzle Tip", nx, GY, ZB - 6, 6.5, 6,
                                      color=C_NOZZLE, axis="z"))
    return '\n'.join(parts)


def _carriage(xend, side, din):
    """One wheel carriage (2D Detail C/D). The carriage is the full beam width in
    X with its OUTER edge flush with the beam end (`din` = +1 left end, -1 right).
    Notched 5mm Al plate (two wings) + two Ø50 nylon wheels on Ø10 through-axles
    (saddle clamps + M5 bolts); the beam is sandwiched by TWO flat C-clamps (one
    per face) that hook over the beam top and bolt down through the plate."""
    parts = []
    ww, wd, az = SPRAY_BAR_WHEEL_W, SPRAY_BAR_WHEEL_DIA, SPRAY_BAR_AXLE_Z  # 20, 50, 27
    half = SPRAY_BAR_WHEEL_SP / 2          # 100 — wheel offset in Yd
    plate_z = az + 2                        # 29 — plate bottom (2mm above axle)
    plate_t = 5                             # 5mm Al plate
    plate_top = plate_z + plate_t           # 34
    CW = S                                  # carriage width in X (= beam width, 40)
    cx0 = xend if din > 0 else xend - CW    # outer X edge flush with the beam end
    cxc = cx0 + CW / 2                       # carriage / wheel centre X
    notch = S / 2                            # 20 — wings extend in to meet the beam faces

    # ── notched 5mm Al carriage plate — two wings either side of the beam ──
    parts.append(ov.ruby_box(f"Carriage Plate L {side}",
                             cx0, GY - half - 18, plate_z,
                             CW, (GY - notch) - (GY - half - 18), plate_t, color=C_ALUM))
    parts.append(ov.ruby_box(f"Carriage Plate R {side}",
                             cx0, GY + notch, plate_z,
                             CW, (GY + half + 18) - (GY + notch), plate_t, color=C_ALUM))

    # ── each wheel: Ø50 nylon on a Ø10 through-axle (centred on the wing). The
    # axle is retained by a curved saddle clamp on EACH side of the wheel (like a
    # conduit/pipe saddle), each bolted down through the plate with two bolts
    # straddling the axle — two bolts either side of the wheel. ──
    sw = 6                                    # saddle width along the axle
    sgap = ww / 2 + 6                         # saddle offset from wheel centre (flanks the wheel)
    for dy in (-half, half):
        cy = GY + dy
        parts.append(ov.ruby_cylinder(f"Wheel {side}",
                                      cxc - ww / 2, cy, az, wd / 2, ww,
                                      color=C_NYLON, axis="x"))
        parts.append(ov.ruby_cylinder(f"Axle Pin 10mm {side}",
                                      cxc - ww / 2 - 14, cy, az, 5, ww + 28,
                                      color=C_BOLT, axis="x"))
        for sx_ in (cxc - sgap, cxc + sgap):  # a saddle clamp either side of the wheel
            # curved hump cradling under the axle
            parts.append(ruby_saddle(f"Axle Saddle {side}",
                                     sx_, sw, cy, az, 6, 2, 180, 360, C_CLAMP))
            for sgn in (-1, 1):               # a flat foot each side + bolt through it
                foot_y0 = cy + 6 if sgn > 0 else cy - 16
                parts.append(ov.ruby_box(f"Axle Saddle Foot {side}",
                                         sx_ - sw / 2, foot_y0, plate_z - 2, sw, 10, 2,
                                         color=C_CLAMP))
                parts.append(ov.ruby_cylinder(f"Axle Bolt {side}",
                                              sx_, cy + sgn * 11, plate_z - 4, 2.5,
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
            # bolt through bottom plate + spacer + top plate (nut head proud each end)
            parts.append(ov.ruby_cylinder(f"Clamp Bolt {side}",
                                          bx_, by_, ZB - ct - 4, 2.5,
                                          (ZT + ct + 4) - (ZB - ct - 4), color=C_BOLT, axis="z"))
    return parts


def build_carriages():
    parts = []
    parts += _carriage(XL, "L", 1)
    parts += _carriage(XR, "R", -1)
    # tray-floor reference patch (the wheels roll on this 2mm SS tray floor)
    parts.append(ov.ruby_box("Tray Floor (ref)",
                             XL - 60, GY - half_band(), 0,
                             (XR - XL) + 120, 2 * half_band(), 2,
                             color=C_TRAY, alpha=0.25))
    return '\n'.join(parts)


def half_band():
    return SPRAY_BAR_WHEEL_SP / 2 + 60                    # 160 — patch half-width in Yd


def build_feed_pole():
    parts = []
    cx = (XL + XR) / 2          # pole/joint X — beam centre (POLE_X)
    by = GY                      # gantry Yd
    c_joint = "#C8B070"          # zinc/brass ball-joint socket
    c_bolt = "#50505A"           # bolts / U-bolt
    c_ss = "#D8D0BC"             # SS ball + M12 stud

    # ── pole connection: 20mm ball joint clamped to the beam TOP face ──
    # flange (Ø44/50mm) on the beam top
    parts.append(ov.ruby_box("Pole Mount Flange",
                             cx - 22, by - 22, ZT, 44, 44, 5, color=C_STEEL))
    # U-bolt (M8) clamping the socket housing down to the beam top
    parts.append(ov.ruby_pipe_run("Pole U-bolt",
                                  [(cx, by - 22, ZT - 6), (cx, by - 22, ZT + 36),
                                   (cx, by + 22, ZT + 36), (cx, by + 22, ZT - 6)],
                                  2.5, color=c_bolt))
    # socket housing — the ball-joint body, Ø36 × 28
    parts.append(ov.ruby_cylinder("Ball-Joint Socket (20mm)",
                                  cx, by, ZT + 5, 18, 28, color=c_joint, axis="z"))

    # ── articulated stud + arm tube + telescoping pole to the operator ──
    op_y, op_z = 180, 80 + 890         # operator hand: near walkway, ~890 above grate
    ball_z = ZT + 5 + 14 + 2           # ≈ 71 — ball centre inside the socket
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

    # ── water feed: the blue hose runs down the pole and terminates at a manifold
    #    by the ball joint; a series of irrigation tubes branch from it along the
    #    beam top to feed points, each barbed through the beam wall into the
    #    internal poly pipe (per Sheet 7 connection detail) ──
    parts.append(ov.ruby_pipe("Feed Hose (upper)",
                              (cx + 22, op_y, op_z), (cx + 22, mid_y, mid_z), 8, color=C_WATER))
    parts.append(ov.ruby_pipe("Feed Hose (lower)",
                              (cx + 22, mid_y, mid_z), (cx + 22, by, ball_z + 12), 8, color=C_WATER))
    # distribution manifold on the beam top, beside the ball joint
    man_cx, man_z = cx + 38, ZT + 4
    parts.append(ov.ruby_box("Feed Manifold",
                             man_cx - 18, by - 14, man_z, 36, 28, 18, color=C_WATER))
    parts.append(ov.ruby_pipe("Feed Hose to Manifold",
                              (cx + 22, by, ball_z + 12), (man_cx, by, man_z + 18), 8,
                              color=C_WATER))
    # irrigation tubes + barbed fittings into the poly pipe
    nfeed = 7
    bore_cz = ZB + S / 2
    for i in range(nfeed):
        fx = XL + (i + 0.5) / nfeed * (XR - XL)
        ty = by + (i - (nfeed - 1) / 2) * 3          # slight Yd spread to separate tubes
        parts.append(ov.ruby_pipe("Feed Tube",
                                  (man_cx, ty, man_z + 9), (fx, ty, ZT + 6), 3.5,
                                  color=C_WATER))
        parts.append(ov.ruby_cylinder("Feed Barb Fitting",
                                      fx, ty, bore_cz - 2, 4, (ZT + 6) - (bore_cz - 2),
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
    parts.append(ov.ruby_box("Tray Floor", xl, yn, 0, w, d, ft, color=C_TRAY, alpha=0.55))
    parts.append(ov.ruby_box("Tray Rim Near", xl, yn, 0, w, wt, rim, color=C_TRAY, alpha=0.3))
    parts.append(ov.ruby_box("Tray Rim Far", xl, yf - wt, 0, w, wt, rim, color=C_TRAY, alpha=0.3))
    parts.append(ov.ruby_box("Tray Rim Left", xl, yn, 0, wt, d, rim, color=C_TRAY, alpha=0.3))
    parts.append(ov.ruby_box("Tray Rim Right", xr - wt, yn, 0, wt, d, rim, color=C_TRAY, alpha=0.3))
    # drain sump well, recessed below the floor at the near-rim low corner
    parts.append(ov.ruby_box("Tray Sump",
                             PROC_TRAY_DRAIN_X - PROC_TRAY_SUMP_W / 2, PROC_TRAY_DRAIN_YD,
                             -PROC_TRAY_SUMP_Z, PROC_TRAY_SUMP_W, PROC_TRAY_SUMP_D,
                             PROC_TRAY_SUMP_Z, color=C_TRAY, alpha=0.55))
    return '\n'.join(parts)


def generate_ruby():
    comps = [
        ov.component("Spray Beam", "Beam", build_beam()),
        ov.component("Wheel Carriages", "Carriages", build_carriages()),
        ov.component("Feed & Push Pole", "Feed & Pole", build_feed_pole()),
        ov.component("Processing Tray", "Tray", build_tray()),
    ]
    body = '\n'.join(comps)
    tags_ruby = '\n'.join(
        f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep_tags_ruby = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'
    scenes = [
        ("Beam", ["Beam"]),
        ("Carriage Assembly", ["Beam", "Carriages"]),
        ("Pole & Ball Joint", ["Beam", "Feed & Pole"]),
        ("Processing Tray", ["Tray", "Beam", "Carriages"]),
        ("Combined", TAGS),
    ]
    scenes_ruby = '[' + ', '.join(
        '["%s", [%s]]' % (n, ', '.join(f'"{t}"' for t in tags))
        for n, tags in scenes) + ']'

    return f'''model = Sketchup.active_model
model.start_operation("TBS-001 Spray-Bar Gantry", true)
entities = model.active_entities

opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# Idempotent rebuild: erase all prior groups/instances.
to_erase = entities.to_a.select {{ |e|
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance)
}}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each {{ |p| model.pages.erase(p) }}

{tags_ruby}

{body}

model.definitions.purge_unused
model.materials.purge_unused

keep_tags = {keep_tags_ruby}
default_layer = model.layers[0]
model.layers.to_a.each {{ |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}}

dir = Geom::Vector3d.new(0.5, -0.78, 0.38); dir.normalize!

{scenes_ruby}.each {{ |name, tags|
  model.layers.each {{ |l| l.visible = (l == default_layer || tags.include?(l.name)) }}
  # frame just this scene's visible geometry (the tray is much larger than the bar)
  ctr = model.bounds.center
  eye = ctr.offset(dir, model.bounds.diagonal * 1.4)
  model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
  model.active_view.zoom_extents
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
