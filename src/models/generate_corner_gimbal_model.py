#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""Generate the film-plane CORNER / WHOLE-MECHANISM SketchUp model (film-plane-redesign branch).

Shows one full VERTICAL EDGE of the film plane so the top/bottom rail story is visible:

    floor rail (Y, focus) → BOTTOM corner (bears — COMPRESSION) → ghost film plane
    → TOP corner (hangs — TENSION) → ceiling rail (Y, focus)

Each corner is the same off-the-shelf motion stack (mirrored top↔bottom):

    depth rail (Y focus) + HGH20CA carriage
    → DRIVEN vertical Z Acme leadscrew (¾"-6, self-locking; holds the ~280 mm tilt foreshortening)
    → FLOATING X slide (HGR15, gravity-neutral; absorbs the horizontal arc)
    → single U-JOINT (Ruland US12-6-6-SS; through-axis = Y, so tilt pin = X, swing pin = Z; twist locked)
    → stub mount → film-frame corner.

Nominal stack ≈ 150 mm/corner → FP_H ≈ 2388 − 300 ≈ 2088 mm (image area ~101 sq ft).

REUSES generate_sketchup_model.py helpers. Open a NEW blank SketchUp doc before --send.

Usage:
    /usr/bin/python3 src/models/generate_corner_gimbal_model.py --save [--send]
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import generate_sketchup_model as ov          # ruby helpers + component()

TAGS = ["Bottom Corner", "Top Corner", "Film Plane", "Labels"]

C_STEEL = "#B0B0B8"; C_ALUM = "#C8D8E8"; C_XSL = "#B8C8D8"; C_PIN = "#B07010"
C_SCREW = "#9098A0"; C_CROSS = "#8A8A92"; C_FRAME = "#2A6B2A"; C_PANEL = "#1F3B66"; C_CAR = "#C04010"

CH = 2388          # container interior height (mm) — local
STACK = 150        # nominal mechanism stack per corner (mm)
FP_H = CH - 2 * STACK   # ≈ 2088 — film-plane height after the top+bottom bite


def corner(z0, s, tag):
    """One corner's motion stack. z0 = rail-mount Z; s = +1 builds up (bottom), -1 builds down (top).
    Build-heights (a,b) are distances from the rail mount along the build direction."""
    P = []

    def bb(name, hx, y0, dy, a, b, color, alpha=1.0):        # symmetric box centred on X=0
        zmin = z0 + a if s > 0 else z0 - b
        P.append(ov.ruby_box(f"{name} {tag}", -hx, y0, zmin, 2 * hx, dy, b - a, color=color, alpha=alpha))

    def rbx(name, x, w, y0, dy, a, b, color):                # explicit-X box
        zmin = z0 + a if s > 0 else z0 - b
        P.append(ov.ruby_box(f"{name} {tag}", x, y0, zmin, w, dy, b - a, color=color))

    def cz(name, cx, cy, a, b, r, color):                    # cylinder along Z
        base = z0 + a if s > 0 else z0 - b
        P.append(ov.ruby_cylinder(f"{name} {tag}", cx, cy, base, r, b - a, color=color, axis="z"))

    def cx(name, x0, cy, h, length, r, color):               # cylinder along X (at one height)
        z = z0 + h if s > 0 else z0 - h
        P.append(ov.ruby_cylinder(f"{name} {tag}", x0, cy, z, r, length, color=color, axis="x"))

    # depth rail (Y = focus) + carriage
    bb("Depth rail Y focus", 12, -170, 340, 0, 18, C_STEEL)
    bb("Carriage HGH20CA", 22, -30, 60, 18, 30, C_CAR)
    # DRIVEN vertical Z Acme leadscrew (self-locking)
    bb("Z screw bearing", 14, -14, 28, 30, 36, C_STEEL)
    cz("Vertical Z leadscrew driven", 0, 0, 36, 122, 6, C_SCREW)
    bb("Z drive nut", 16, -16, 32, 92, 112, C_ALUM)
    # FLOATING X slide (gravity-neutral)
    bb("Floating X slide", 24, -11, 22, 116, 126, C_XSL)
    # single U-JOINT (through-axis Y): cross + tilt pin (X) + swing pin (Z) + two yokes
    bb("U-joint cross", 10, -10, 20, 130, 150, C_CROSS)
    cx("Tilt pin X", -26, -4, 140, 52, 5, C_PIN)
    cz("Swing pin Z", 0, 4, 126, 156, 5, C_PIN)
    rbx("Out yoke ear L", -30, 8, -10, 20, 130, 150, C_ALUM)
    rbx("Out yoke ear R", 22, 8, -10, 20, 130, 150, C_ALUM)
    rbx("Out yoke web", -30, 60, 10, 8, 132, 148, C_ALUM)
    rbx("Out yoke stub", -6, 12, 17, 30, 134, 146, C_ALUM)
    rbx("In yoke ear Lo", -9, 18, -9, 18, 122, 134, C_XSL)
    rbx("In yoke ear Hi", -9, 18, -9, 18, 146, 158, C_XSL)
    rbx("In yoke web", -8, 16, -17, 8, 122, 158, C_XSL)
    # stub → film-frame corner plate
    rbx("Stub-to-frame plate", -10, 70, 40, 10, 120, 180, C_FRAME)
    return "\n".join(P)


def film_plane():
    zb = STACK          # panel bottom edge
    zt = CH - STACK     # panel top edge
    return "\n".join([
        # 2x2 aluminum angle along this vertical edge
        ov.ruby_box("Frame angle web", -5, 50, zb, 5, 50, zt - zb, color=C_FRAME),
        ov.ruby_box("Frame angle flange", -5, 50, zb, 50, 5, zt - zb, color=C_FRAME),
        # ghost film plane (quarter width shown)
        ov.ruby_box("Film plane (ghost)", 0, 53, zb, 620, 4, zt - zb, color=C_PANEL, alpha=0.16),
    ])


def labels():
    L = []
    def txt(s, x, y, z, vx, vy, vz):
        L.append(f'''
tt = entities.add_text("{s}", Geom::Point3d.new({ov.mm(x)}, {ov.mm(y)}, {ov.mm(z)}), Geom::Vector3d.new({ov.mm(vx)}, {ov.mm(vy)}, {ov.mm(vz)}))
tt.layer = model.layers["Labels"] rescue nil''')
    txt("CEILING rail (Y focus) — TOP corners HANG = TENSION", 0, -170, CH, 40, -60, 30)
    txt("FLOOR rail (Y focus) — BOTTOM corners BEAR = COMPRESSION", 0, -170, 0, 40, -60, -30)
    txt("Single U-joint (Ruland US12-6-6-SS) — tilt X + swing Z, twist locked", -30, -4, STACK + 20, -60, -40, 10)
    txt("DRIVEN vertical Z leadscrew (self-locking)", 16, 0, 100, 55, 45, 0)
    txt("Floating X slide (horizontal arc)", 24, 0, 122, 55, 45, 0)
    txt(f"Film plane 4499 x {FP_H} (mechanism takes ~{STACK} top + bottom)", 300, 53, CH / 2, 60, 45, 0)
    return "\n".join(L)


def generate_ruby():
    comps = [
        ov.component("Bottom Corner", "Bottom Corner", corner(0, +1, "(bot)")),
        ov.component("Top Corner", "Top Corner", corner(CH, -1, "(top)")),
        ov.component("Film Plane", "Film Plane", film_plane()),
    ]
    body = "\n".join(comps)
    tags_ruby = "\n".join(f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep = "[" + ", ".join(f'"{t}"' for t in TAGS) + "]"
    full = ["Bottom Corner", "Top Corner", "Film Plane"]
    scenes = [
        ("Overview", full, None),
        ("Bottom Corner", ["Bottom Corner", "Film Plane"], (0, 0, STACK, 320)),
        ("Top Corner", ["Top Corner", "Film Plane"], (0, 0, CH - STACK, 320)),
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

dir = Geom::Vector3d.new(0.55, -0.72, 0.30); dir.normalize!
{scenes_ruby}.each {{ |name, tags, tgt|
  model.layers.each {{ |l| l.visible = (l == default_layer || tags.include?(l.name)) }}
  if tgt
    t = Geom::Point3d.new(tgt[0], tgt[1], tgt[2])
    cdir = Geom::Vector3d.new(0.55, -0.72, 0.30); cdir.normalize!
    model.active_view.camera = Sketchup::Camera.new(t.offset(cdir, tgt[3]), t, Z_AXIS)
  else
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
{{ success: true, model: "Film-Plane Corner Mechanism",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }}.to_json
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate the film-plane corner / whole-mechanism SketchUp model")
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
