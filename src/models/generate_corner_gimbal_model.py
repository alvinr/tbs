#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""Generate the film-plane CORNER GIMBAL SketchUp model (film-plane-redesign branch).

A TRUE gimbal: an open middle RING held in TWO perpendicular U-forks so each member is free
to rotate about its pin (a solid block can't articulate — it must sit in a U-fork).

    depth rail (HGR20) → carriage → FLOATING X-Z cross-slide → CROSS-SLIDE U-FORK →
    TILT pin (Ø24, horizontal, X) → GIMBAL RING → SWING pin (Ø24, vertical, Z; offset in
    depth so it clears the tilt pin) → FRAME U-FORK → film-frame corner (2x2 angle) →
    ghost quarter of the rigid ACM film plane.

Both pins are Ø24 shoulder bolts in DOUBLE shear on acetal bushings; the two axes are offset
in Y (depth) so the two through-pins don't intersect. REUSES generate_sketchup_model.py helpers.

Local axes (mm): X = horizontal along the wall (TILT axis), Y = depth toward pinhole (rail
travel), Z = up (SWING axis). Joint centered near (0,0,96).

Usage (open a NEW blank SketchUp doc first):
    /usr/bin/python3 src/models/generate_corner_gimbal_model.py --save [--send]
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import generate_sketchup_model as ov          # ruby helpers + component()

TAGS = ["Rail & Carriage", "Cross-Slide", "Gimbal", "Frame", "Film Plane", "Labels"]

C_STEEL = "#B0B0B8"; C_ALUM = "#C8D8E8"; C_PIN = "#B07010"
C_BUSH = "#5A3E00"; C_FRAME = "#2A6B2A"; C_PANEL = "#1F3B66"; C_NUT = "#80808A"

# ── gimbal geometry (mm), local frame ──
PIN_R, BUSH_R = 12, 15
RCZ = 96                              # ring centre Z
ROX, ROZ = 30, 30                     # ring outer half-width (X) and half-height (Z)
RHX, RHZ = 16, 16                     # ring hole half-width / half-height  (walls ~14 thick)
RY0, RYD = -12, 24                    # ring depth (Y): from RY0, 24 deep
TILT_Y = -6                           # tilt-pin depth offset  (horizontal pin, along X)
SWING_X = 0; SWING_Y = 6              # swing-pin depth offset (vertical pin, along Z)
SWING_Z0, SWING_Z1 = 52, 144          # swing-pin extent (Z)
FTOP = SWING_Z1 + 4                   # frame sits just above the top fork lug


def rail_and_carriage():
    return "\n".join([
        ov.ruby_box("Depth Rail HGR20", -12, -190, 0, 24, 380, 18, color=C_STEEL),
        ov.ruby_box("Carriage HGH20CA", -22, -34, 18, 44, 68, 24, color="#C04010"),
    ])


def cross_slide():
    p = [
        ov.ruby_box("X Cross-Slide (float)", -40, -16, 42, 80, 32, 8, color=C_ALUM),
        ov.ruby_box("Z Cross-Slide (float)", -34, -14, 50, 68, 28, 8, color="#B8C8D8"),
        # CROSS-SLIDE U-FORK: two lugs (outboard in X) carrying the TILT pin — the ring
        # sits BETWEEN them and rotates about the tilt axis
        ov.ruby_box("Slide Fork Lug L", -44, TILT_Y - 9, 58, 14, 22, 50, color=C_ALUM),
        ov.ruby_box("Slide Fork Lug R", 30, TILT_Y - 9, 58, 14, 22, 50, color=C_ALUM),
    ]
    return "\n".join(p)


def gimbal():
    p = []
    # OPEN gimbal ring — four walls (so both members can rotate; not a solid block)
    p.append(ov.ruby_box("Gimbal Ring wall L", -ROX, RY0, RCZ - ROZ, ROX - RHX, RYD, 2 * ROZ, color=C_ALUM))
    p.append(ov.ruby_box("Gimbal Ring wall R", RHX, RY0, RCZ - ROZ, ROX - RHX, RYD, 2 * ROZ, color=C_ALUM))
    p.append(ov.ruby_box("Gimbal Ring wall Bot", -RHX, RY0, RCZ - ROZ, 2 * RHX, RYD, ROZ - RHZ, color=C_ALUM))
    p.append(ov.ruby_box("Gimbal Ring wall Top", -RHX, RY0, RCZ + RHZ, 2 * RHX, RYD, ROZ - RHZ, color=C_ALUM))
    # TILT pin (Ø24, horizontal X, offset -Y) — fork-L → ring-L → ring-R → fork-R (double shear)
    p.append(ov.ruby_cylinder("Tilt Pin O24 (shoulder bolt)", -44, TILT_Y, RCZ, PIN_R, 88, color=C_PIN, axis="x"))
    p.append(ov.ruby_box("Tilt Pin Head", -50, TILT_Y - 14, RCZ - 14, 6, 28, 28, color=C_PIN))
    p.append(ov.ruby_box("Tilt Pin Nut", 44, TILT_Y - 13, RCZ - 13, 8, 26, 26, color=C_NUT))
    p.append(ov.ruby_cylinder("Tilt Bushing L", -ROX, TILT_Y, RCZ, BUSH_R, ROX - RHX, color=C_BUSH, axis="x"))
    p.append(ov.ruby_cylinder("Tilt Bushing R", RHX, TILT_Y, RCZ, BUSH_R, ROX - RHX, color=C_BUSH, axis="x"))
    # SWING pin (Ø24, vertical Z, offset +Y) — fork-bot → ring-bot → ring-top → fork-top (double shear)
    p.append(ov.ruby_cylinder("Swing Pin O24 (shoulder bolt)", SWING_X, SWING_Y, SWING_Z0, PIN_R, SWING_Z1 - SWING_Z0, color=C_PIN, axis="z"))
    p.append(ov.ruby_box("Swing Pin Head", -14, SWING_Y - 14, SWING_Z1, 28, 28, 6, color=C_PIN))
    p.append(ov.ruby_box("Swing Pin Nut", -13, SWING_Y - 13, SWING_Z0 - 8, 26, 26, 8, color=C_NUT))
    p.append(ov.ruby_cylinder("Swing Bushing Bot", SWING_X, SWING_Y, RCZ - ROZ, BUSH_R, ROZ - RHZ, color=C_BUSH, axis="z"))
    p.append(ov.ruby_cylinder("Swing Bushing Top", SWING_X, SWING_Y, RCZ + RHZ, BUSH_R, ROZ - RHZ, color=C_BUSH, axis="z"))
    return "\n".join(p)


def frame_corner():
    p = [
        # FRAME U-FORK: two lugs (outboard top/bottom in Z) carrying the SWING pin — the ring
        # sits BETWEEN them and the frame rotates about the swing axis
        ov.ruby_box("Frame Fork Lug Top", -RHX, SWING_Y - 9, RCZ + ROZ, 2 * RHX, 22, SWING_Z1 - (RCZ + ROZ) + 2, color=C_ALUM),
        ov.ruby_box("Frame Fork Lug Bot", -RHX, SWING_Y - 9, SWING_Z0 - 2, 2 * RHX, 22, (RCZ - ROZ) - (SWING_Z0 - 2), color=C_ALUM),
    ]
    # film-frame corner — 2x2x3/16 aluminum angle (L): vertical leg + horizontal leg
    p.append(ov.ruby_box("Frame Angle vert web", -5, 24, FTOP, 50, 5, 300, color=C_FRAME))
    p.append(ov.ruby_box("Frame Angle vert flange", -5, 24, FTOP, 5, 50, 300, color=C_FRAME))
    p.append(ov.ruby_box("Frame Angle horiz web", -5, 24, FTOP, 320, 5, 50, color=C_FRAME))
    p.append(ov.ruby_box("Frame Angle horiz flange", -5, 24, FTOP, 320, 50, 5, color=C_FRAME))
    return "\n".join(p)


def film_plane():
    return ov.ruby_box("Film Plane (ACM, ghost quarter)", 0, 29, FTOP, 900, 4, 750, color=C_PANEL, alpha=0.22)


def labels():
    L = []
    def txt(s, x, y, z, vx, vy, vz):
        L.append(f'''
tt = entities.add_text("{s}", Geom::Point3d.new({ov.mm(x)}, {ov.mm(y)}, {ov.mm(z)}), Geom::Vector3d.new({ov.mm(vx)}, {ov.mm(vy)}, {ov.mm(vz)}))
tt.layer = model.layers["Labels"] rescue nil''')
    txt("TILT pin O24 (ring rotates in slide U-fork)", 44, TILT_Y, RCZ, 60, -45, -25)
    txt("SWING pin O24 (frame rotates in frame U-fork)", 0, SWING_Y, SWING_Z1, 55, 45, 35)
    txt("OPEN gimbal ring (free to rotate both axes)", ROX, 0, RCZ, 60, -55, 5)
    txt("Cross-slide U-fork", -44, TILT_Y, 70, -60, -40, -8)
    txt("Frame U-fork", RHX, SWING_Y, RCZ + ROZ + 8, 55, 40, 20)
    txt("Floating X-Z cross-slide", -34, -14, 50, -55, -40, -10)
    txt("Film frame (2x2 angle) + ACM", 20, 29, FTOP + 130, 60, 40, 40)
    return "\n".join(L)


def generate_ruby():
    comps = [
        ov.component("Rail & Carriage", "Rail & Carriage", rail_and_carriage()),
        ov.component("Cross-Slide", "Cross-Slide", cross_slide()),
        ov.component("Gimbal Joint", "Gimbal", gimbal()),
        ov.component("Frame Corner", "Frame", frame_corner()),
        ov.component("Film Plane", "Film Plane", film_plane()),
    ]
    body = "\n".join(comps)
    tags_ruby = "\n".join(f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep = "[" + ", ".join(f'"{t}"' for t in TAGS) + "]"
    full = ["Rail & Carriage", "Cross-Slide", "Gimbal", "Frame", "Film Plane"]
    scenes = [
        ("Overview", full, None),
        ("Joint Detail", ["Cross-Slide", "Gimbal", "Frame"], (0, 0, RCZ, 300)),
        ("Labeled", full + ["Labels"], None),
    ]

    def scene_lit(n, tags, tgt):
        tg = "[" + ", ".join(f'"{t}"' for t in tags) + "]"
        cam = "nil" if tgt is None else f"[{ov.mm(tgt[0])}, {ov.mm(tgt[1])}, {ov.mm(tgt[2])}, {ov.mm(tgt[3])}]"
        return f'["{n}", {tg}, {cam}]'
    scenes_ruby = "[" + ", ".join(scene_lit(*s) for s in scenes) + "]"

    return f'''# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/generate_corner_gimbal_model.py — do not edit this .rb directly.
model = Sketchup.active_model
model.start_operation("Film-Plane Corner Gimbal", true)
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

# ── "Labeled" scene callouts (Labels tag) ──
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

dir = Geom::Vector3d.new(0.55, -0.72, 0.42); dir.normalize!
{scenes_ruby}.each {{ |name, tags, tgt|
  model.layers.each {{ |l| l.visible = (l == default_layer || tags.include?(l.name)) }}
  if tgt
    t = Geom::Point3d.new(tgt[0], tgt[1], tgt[2])
    cdir = Geom::Vector3d.new(0.55, -0.72, 0.42); cdir.normalize!
    model.active_view.camera = Sketchup::Camera.new(t.offset(cdir, tgt[3]), t, Z_AXIS)
  else
    ctr = model.bounds.center
    eye = ctr.offset(dir, model.bounds.diagonal * 1.5)
    model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
    model.active_view.zoom_extents
  end
  page = model.pages.add(name)
  page.use_camera = true
}}
model.layers.each {{ |l| l.visible = true }}

model.commit_operation
{{ success: true, model: "Film-Plane Corner Gimbal",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }}.to_json
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate the film-plane corner gimbal SketchUp model")
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
