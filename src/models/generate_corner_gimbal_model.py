#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""Generate the film-plane CORNER-JOINT SketchUp model (film-plane-redesign branch).

The corner joint is an OFF-THE-SHELF single universal joint (Ruland US12-6-6-SS: 303 SS,
self-lubricating sintered-bronze plain bearing, 45° max, grease-free) — NOT a custom gimbal.
A U-joint is the catalog embodiment of the two-crossed-pins, twist-locked kinematics: it gives
tilt + swing and locks twist, factory-aligned and in stock.

Per-corner motion stack (local axes: X = horizontal along wall = TILT, Y = depth toward pinhole
= focus, Z = up = SWING / stack direction):

    depth rail (Y, focus) → carriage → DRIVEN vertical Z leadscrew (holds the ~280 mm tilt
    foreshortening; self-locking) → FLOATING X slide (absorbs the horizontal arc, gravity-neutral)
    → single U-JOINT (tilt pin X + swing pin Z, twist locked) → stub mount → film-frame corner
    → ghost quarter of the rigid film plane.

REUSES generate_sketchup_model.py helpers. Open a NEW blank SketchUp doc before --send.

Usage:
    /usr/bin/python3 src/models/generate_corner_gimbal_model.py --save [--send]
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import generate_sketchup_model as ov          # ruby helpers + component()

TAGS = ["Rail & Carriage", "Z + X Stage", "U-Joint", "Frame", "Film Plane", "Labels"]

C_STEEL = "#B0B0B8"; C_ALUM = "#C8D8E8"; C_PIN = "#B07010"; C_SCREW = "#9098A0"
C_CROSS = "#8A8A92"; C_FRAME = "#2A6B2A"; C_PANEL = "#1F3B66"

JC = 130          # U-joint centre Z (mm), local frame


def rail_and_carriage():
    return "\n".join([
        ov.ruby_box("Depth Rail HGR20 (Y focus)", -12, -190, 0, 24, 380, 18, color=C_STEEL),
        ov.ruby_box("Carriage HGH20CA", -22, -34, 18, 44, 68, 24, color="#C04010"),
    ])


def z_x_stage():
    """Driven vertical Z leadscrew + floating X slide."""
    return "\n".join([
        # DRIVEN vertical leadscrew — self-locking, holds the tilt foreshortening
        ov.ruby_box("Z screw base bearing", -14, -14, 38, 28, 28, 8, color=C_STEEL),
        ov.ruby_cylinder("Vertical Z leadscrew (driven)", 0, 0, 42, 6, 116, color=C_SCREW, axis="z"),
        ov.ruby_box("Z drive nut (rides screw)", -18, -18, 86, 36, 36, 18, color=C_ALUM),
        # FLOATING X slide — gravity-neutral, absorbs the horizontal arc
        ov.ruby_box("Floating X slide", -26, -12, 104, 52, 24, 7, color="#B8C8D8"),
    ])


def ujoint():
    """Single universal joint (Ruland US12-6-6-SS): cross + two perpendicular yokes."""
    p = []
    # cross / spider block at the joint centre
    p.append(ov.ruby_box("U-joint cross block", -11, -11, JC - 11, 22, 22, 22, color=C_CROSS))
    # TILT pin (X, horizontal) — gripped by the OUTPUT (panel-side) yoke; offset -Y so it clears swing
    p.append(ov.ruby_cylinder("Tilt pin (X)", -30, -4, JC, 5, 60, color=C_PIN, axis="x"))
    # SWING pin (Z, vertical) — gripped by the INPUT (carrier-side) yoke; offset +Y so it clears tilt
    p.append(ov.ruby_cylinder("Swing pin (Z)", 0, 4, JC - 26, 5, 52, color=C_PIN, axis="z"))
    # OUTPUT yoke (panel side): two ears left/right on the tilt pin + web + stub toward panel (+Y)
    p.append(ov.ruby_box("Out yoke ear L", -30, -10, JC - 10, 10, 20, 20, color=C_ALUM))
    p.append(ov.ruby_box("Out yoke ear R", 20, -10, JC - 10, 10, 20, 20, color=C_ALUM))
    p.append(ov.ruby_box("Out yoke web", -30, 10, JC - 8, 60, 8, 16, color=C_ALUM))
    p.append(ov.ruby_box("Out yoke stub", -6, 17, JC - 6, 12, 26, 12, color=C_ALUM))
    # INPUT yoke (carrier side): two ears top/bottom on the swing pin + web + foot to the X slide (-Y)
    p.append(ov.ruby_box("In yoke ear Bot", -9, -9, JC - 26, 18, 18, 10, color="#B8C8D8"))
    p.append(ov.ruby_box("In yoke ear Top", -9, -9, JC + 16, 18, 18, 10, color="#B8C8D8"))
    p.append(ov.ruby_box("In yoke web", -8, -17, JC - 26, 16, 8, 52, color="#B8C8D8"))
    p.append(ov.ruby_box("In yoke foot", -12, -16, 100, 24, 28, 8, color="#B8C8D8"))
    return "\n".join(p)


def frame_corner():
    p = [
        ov.ruby_box("Stub-to-frame plate", -10, 40, JC - 30, 70, 10, 60, color=C_FRAME),
        # film-frame corner — 2x2x3/16 aluminum angle (L)
        ov.ruby_box("Frame Angle vert web", -5, 50, JC - 6, 50, 5, 300, color=C_FRAME),
        ov.ruby_box("Frame Angle vert flange", -5, 50, JC - 6, 5, 50, 300, color=C_FRAME),
        ov.ruby_box("Frame Angle horiz web", -5, 50, JC - 6, 320, 5, 50, color=C_FRAME),
        ov.ruby_box("Frame Angle horiz flange", -5, 50, JC - 6, 320, 50, 5, color=C_FRAME),
    ]
    return "\n".join(p)


def film_plane():
    return ov.ruby_box("Film Plane (ACM, ghost quarter)", 0, 55, JC - 6, 880, 4, 740, color=C_PANEL, alpha=0.22)


def labels():
    L = []
    def txt(s, x, y, z, vx, vy, vz):
        L.append(f'''
tt = entities.add_text("{s}", Geom::Point3d.new({ov.mm(x)}, {ov.mm(y)}, {ov.mm(z)}), Geom::Vector3d.new({ov.mm(vx)}, {ov.mm(vy)}, {ov.mm(vz)}))
tt.layer = model.layers["Labels"] rescue nil''')
    txt("Single U-joint (Ruland US12-6-6-SS, 45deg, off-the-shelf)", 0, 4, JC + 26, 55, 45, 30)
    txt("TILT pin (X, horizontal)", 30, -4, JC, 55, -40, 10)
    txt("SWING pin (Z, vertical)", 0, 4, JC - 26, -55, 40, -20)
    txt("DRIVEN vertical Z leadscrew (holds tilt travel)", 0, 0, 60, -60, -40, -8)
    txt("Floating X slide (horizontal arc)", -26, 0, 108, -55, -45, 0)
    txt("Depth rail (Y) — focus", 0, 180, 9, 40, 55, 10)
    txt("Film frame (2x2 angle) + film plane", 40, 55, JC + 120, 60, 45, 40)
    return "\n".join(L)


def generate_ruby():
    comps = [
        ov.component("Rail & Carriage", "Rail & Carriage", rail_and_carriage()),
        ov.component("Z + X Stage", "Z + X Stage", z_x_stage()),
        ov.component("U-Joint", "U-Joint", ujoint()),
        ov.component("Frame Corner", "Frame", frame_corner()),
        ov.component("Film Plane", "Film Plane", film_plane()),
    ]
    body = "\n".join(comps)
    tags_ruby = "\n".join(f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep = "[" + ", ".join(f'"{t}"' for t in TAGS) + "]"
    full = ["Rail & Carriage", "Z + X Stage", "U-Joint", "Frame", "Film Plane"]
    scenes = [
        ("Overview", full, None),
        ("Joint Detail", ["Z + X Stage", "U-Joint", "Frame"], (0, 0, JC, 300)),
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
model.start_operation("Film-Plane Corner U-Joint", true)
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
{{ success: true, model: "Film-Plane Corner U-Joint",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }}.to_json
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate the film-plane corner U-joint SketchUp model")
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
