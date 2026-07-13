#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""Generate the film-plane CORNER GIMBAL SketchUp model (film-plane-redesign branch).

Study A / design-A corner joint, shown in its larger context so the 2D can be checked in 3D:

    depth rail (HGR20) → carriage → FLOATING X-Z cross-slide → cross-slide yoke →
    TILT pin (Ø24, horizontal) → gimbal block → SWING pin (Ø24, vertical, offset) →
    frame yoke → film-frame corner (2x2 angle) → a ghost quarter of the rigid film plane.

Two perpendicular Ø24 shoulder-bolt pins = a universal joint (tilt + swing, no twist), each
in double shear on acetal bushings. REUSES the ruby helpers from generate_sketchup_model.py.

Local axes (mm): X = horizontal along the wall (= TILT axis), Y = depth toward pinhole
(= rail travel), Z = up (SWING axis is vertical). Built in a local frame centered on the joint.

Usage (open a NEW blank SketchUp doc first):
    /usr/bin/python3 src/models/generate_corner_gimbal_model.py --save
    /usr/bin/python3 src/models/generate_corner_gimbal_model.py --save --send
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import generate_sketchup_model as ov          # ruby helpers + component()

TAGS = ["Rail & Carriage", "Cross-Slide", "Gimbal", "Frame", "Film Plane", "Labels"]

C_STEEL = "#B0B0B8"    # rail, carriage, frame angle
C_ALUM  = "#C8D8E8"    # cross-slide, yokes, gimbal block
C_PIN   = "#B07010"    # Ø24 shoulder-bolt pins (amber)
C_BUSH  = "#5A3E00"    # acetal/PTFE bushings
C_FRAME = "#2A6B2A"    # film-frame angle (green)
C_PANEL = "#1F3B66"    # film-plane panel (ghost)
C_NUT   = "#80808A"

# ── key geometry (mm), local frame; joint centered near (0,0,~90) ──
PIN_R = 12             # Ø24 pins
BUSH_R = 15            # Ø30 bushings
TILT_Z = 74           # tilt-pin height (horizontal, along X)
SWING_Z0, SWING_Z1 = 90, 130   # swing pin (vertical, along Z), offset above the tilt pin
BLK = dict(x=-18, y=-18, z=60, w=36, d=36, h=54)   # gimbal block


def rail_and_carriage():
    p = []
    # depth rail (HGR20) running in Y (rail travel = depth)
    p.append(ov.ruby_box("Depth Rail HGR20", -12, -190, 0, 24, 380, 18, color=C_STEEL))
    # carriage (HGH20CA) riding the rail
    p.append(ov.ruby_box("Carriage HGH20CA", -22, -34, 18, 44, 68, 24, color="#C04010"))
    return "\n".join(p)


def cross_slide():
    p = []
    # the X-Z floating stage (represented as one plate here) — it absorbs the arc travel
    p.append(ov.ruby_box("X Cross-Slide (float)", -34, -16, 42, 68, 32, 8, color=C_ALUM))
    p.append(ov.ruby_box("Z Cross-Slide (float)", -30, -14, 50, 60, 28, 8, color="#B8C8D8"))
    # cross-slide yoke: two lugs (spaced in X) that carry the TILT pin in double shear
    p.append(ov.ruby_box("Slide Yoke Lug L", -34, -11, 58, 12, 22, 30, color=C_ALUM))
    p.append(ov.ruby_box("Slide Yoke Lug R", 22, -11, 58, 12, 22, 30, color=C_ALUM))
    return "\n".join(p)


def gimbal():
    p = []
    # gimbal block (2 offset perpendicular bores)
    p.append(ov.ruby_box("Gimbal Block", BLK["x"], BLK["y"], BLK["z"], BLK["w"], BLK["d"], BLK["h"], color=C_ALUM))
    # TILT pin (Ø24, horizontal along X) — through slide yoke lugs + block, double shear
    p.append(ov.ruby_cylinder("Tilt Pin O24 (shoulder bolt)", -36, 0, TILT_Z, PIN_R, 72, color=C_PIN, axis="x"))
    p.append(ov.ruby_box("Tilt Pin Head", -42, -14, TILT_Z - 14, 6, 28, 28, color=C_PIN))
    p.append(ov.ruby_box("Tilt Pin Nut", 36, -13, TILT_Z - 13, 8, 26, 26, color=C_NUT))
    # tilt-pin acetal bushings (in each lug)
    p.append(ov.ruby_cylinder("Tilt Bushing L", -24, 0, TILT_Z, BUSH_R, 6, color=C_BUSH, axis="x"))
    p.append(ov.ruby_cylinder("Tilt Bushing R", 18, 0, TILT_Z, BUSH_R, 6, color=C_BUSH, axis="x"))
    # SWING pin (Ø24, vertical along Z) — through block + frame yoke, double shear
    p.append(ov.ruby_cylinder("Swing Pin O24 (shoulder bolt)", 0, 0, SWING_Z0, PIN_R, SWING_Z1 - SWING_Z0, color=C_PIN, axis="z"))
    p.append(ov.ruby_box("Swing Pin Head", -14, -14, SWING_Z1, 28, 28, 6, color=C_PIN))
    p.append(ov.ruby_box("Swing Pin Nut", -13, -13, SWING_Z0 - 8, 26, 26, 8, color=C_NUT))
    p.append(ov.ruby_cylinder("Swing Bushing", 0, 0, SWING_Z1 - 12, BUSH_R, 8, color=C_BUSH, axis="z"))
    return "\n".join(p)


def frame_corner():
    p = []
    # frame yoke: a C-fork (rotated 90 deg from the slide yoke) carrying the SWING pin;
    # two lugs spaced along Z with a back plate on +Y, block boss between them
    p.append(ov.ruby_box("Frame Yoke Back", -16, 18, SWING_Z0 - 6, 32, 8, (SWING_Z1 + 6) - (SWING_Z0 - 6), color=C_ALUM))
    p.append(ov.ruby_box("Frame Yoke Lug Lower", -16, -6, SWING_Z0 - 6, 32, 24, 8, color=C_ALUM))
    p.append(ov.ruby_box("Frame Yoke Lug Upper", -16, -6, SWING_Z1, 32, 24, 8, color=C_ALUM))
    # film-frame corner — 2x2x3/16 aluminum angle (L): a vertical leg + a horizontal leg
    fz = SWING_Z1 + 14                       # frame corner sits above the yoke
    p.append(ov.ruby_box("Frame Angle vert leg", -5, 22, fz, 50, 5, 300, color=C_FRAME))         # up the side
    p.append(ov.ruby_box("Frame Angle vert flange", -5, 22, fz, 5, 50, 300, color=C_FRAME))
    p.append(ov.ruby_box("Frame Angle horiz leg", -5, 22, fz, 320, 5, 50, color=C_FRAME))        # along the edge
    p.append(ov.ruby_box("Frame Angle horiz flange", -5, 22, fz, 320, 50, 5, color=C_FRAME))
    return "\n".join(p)


def film_plane():
    # a ghost quarter of the rigid film plane (ACM), bonded to the angle frame
    fz = SWING_Z1 + 14
    return ov.ruby_box("Film Plane (ACM, ghost quarter)", 0, 27, fz, 900, 4, 750, color=C_PANEL, alpha=0.22)


def labels():
    L = []
    def txt(s, x, y, z, vx, vy, vz):
        L.append(f'''
tt = entities.add_text("{s}", Geom::Point3d.new({ov.mm(x)}, {ov.mm(y)}, {ov.mm(z)}), Geom::Vector3d.new({ov.mm(vx)}, {ov.mm(vy)}, {ov.mm(vz)}))
tt.layer = model.layers["Labels"] rescue nil''')
    txt("TILT pin O24 (horizontal)", 36, 0, TILT_Z, 70, -40, -30)
    txt("SWING pin O24 (vertical)", 0, 0, SWING_Z1, 60, 40, 40)
    txt("Gimbal block (2 offset bores)", 18, -18, 90, 60, -50, 0)
    txt("Floating X-Z cross-slide", -30, -16, 50, -60, -40, -10)
    txt("Depth rail (travel = depth)", 0, 180, 9, 20, 60, 20)
    txt("Film frame (2x2 angle) + ACM", 20, 27, SWING_Z1 + 120, 60, 40, 40)
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
        ("Joint Detail", ["Cross-Slide", "Gimbal", "Frame"], (0, 0, 95, 320)),
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
