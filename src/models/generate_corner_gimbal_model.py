#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""Generate the film-plane CORNER / WHOLE-MECHANISM SketchUp model (film-plane-redesign branch).

One full VERTICAL EDGE of the film plane so the top/bottom rail story is visible:

    floor rail (Y, focus) → BOTTOM corner (bears — COMPRESSION) → ghost film plane
    → TOP corner (hangs — TENSION) → ceiling rail (Y, focus)

Each corner is the same manual, off-the-shelf motion stack (mirrored top↔bottom):

  • FOCUS (Y): HGR20 rail + HGH20CA carriage, driven by a ¾"-6 Acme screw + handwheel.
  • VERTICAL (Z): ¾"-6 Acme (self-locking) mounted OUTBOARD of the film edge (out of the light
    cone), driven via a right-angle BEVEL gearbox + extension shaft to a handwheel at ~1.2 m.
  • HORIZONTAL (X): floating HGR15 slide (gravity-neutral; absorbs the swing arc).
  • JOINT: single U-JOINT (Ruland US12-6-6-SS; through-axis Y → tilt pin = X, swing pin = Z;
    twist locked) → stub mount → film-frame corner.

Nominal stack ≈ 150 mm/corner → FP_H ≈ 2388 − 300 ≈ 2088 mm (image area ~101 sq ft). ±40° tilt.

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
C_SCREW = "#9098A0"; C_CROSS = "#8A8A92"; C_FRAME = "#2A6B2A"; C_PANEL = "#1F3B66"
C_CAR = "#C04010"; C_HW = "#3A3A40"

CH = 2388          # container interior height (mm) — local
STACK = 150        # nominal mechanism stack per corner (mm)
FP_H = CH - 2 * STACK   # ≈ 2088
HW_Z = 1200        # handwheel standing height (mm)


def corner(z0, s, tag):
    """One corner's manual motion stack. z0 = rail-mount Z; s = +1 builds up (bottom), -1 down (top).
    Build-heights (a,b) are distances from the rail mount along the build direction; absolute-Z
    elements (the extension shaft + bevel + handwheel at 1.2 m) are placed directly."""
    P = []
    rail_z = z0 + (9 if s > 0 else -9)

    def bb(name, hx, y0, dy, a, b, color, alpha=1.0):        # symmetric box on X=0
        zmin = z0 + a if s > 0 else z0 - b
        P.append(ov.ruby_box(f"{name} {tag}", -hx, y0, zmin, 2 * hx, dy, b - a, color=color, alpha=alpha))

    def rbx(name, x, w, y0, dy, a, b, color):                # explicit-X box
        zmin = z0 + a if s > 0 else z0 - b
        P.append(ov.ruby_box(f"{name} {tag}", x, y0, zmin, w, dy, b - a, color=color))

    def cz(name, cx, cy, a, b, r, color):                    # cylinder along Z
        base = z0 + a if s > 0 else z0 - b
        P.append(ov.ruby_cylinder(f"{name} {tag}", cx, cy, base, r, b - a, color=color, axis="z"))

    def cxx(name, x0, cy, h, length, r, color):              # cylinder along X at build-height h
        z = z0 + h if s > 0 else z0 - h
        P.append(ov.ruby_cylinder(f"{name} {tag}", x0, cy, z, r, length, color=color, axis="x"))

    def cyY(name, cx, y0, dy, h, r, color):                  # cylinder along Y at build-height h
        z = z0 + h if s > 0 else z0 - h
        P.append(ov.ruby_cylinder(f"{name} {tag}", cx, y0, z, r, dy, color=color, axis="y"))

    def diskY(name, cx, y0, z, r, thick, color):             # handwheel disk (abs Z), faces −Y
        P.append(ov.ruby_cylinder(f"{name} {tag}", cx, y0, z, r, thick, color=color, axis="y"))

    def abscylZ(name, cx, cy, za, zb, r, color):             # abs-Z cylinder between za,zb
        P.append(ov.ruby_cylinder(f"{name} {tag}", cx, cy, min(za, zb), r, abs(zb - za), color=color, axis="z"))

    def absbox(name, x, y0, z, w, dy, h, color):
        P.append(ov.ruby_box(f"{name} {tag}", x, y0, z, w, dy, h, color=color))

    # ── FOCUS drive (Y): rail + carriage + Acme screw + handwheel ──
    bb("Depth rail Y focus", 12, -170, 340, 0, 18, C_STEEL)
    bb("Focus carriage HGH20CA", 22, -30, 60, 18, 30, C_CAR)
    cyY("Focus Acme screw Y", 34, -185, 365, 9, 5, C_SCREW)
    diskY("Focus handwheel", 34, -210, rail_z, 55, 12, C_HW)

    # ── VERTICAL drive (Z): OUTBOARD self-locking Acme + nut + brackets ──
    rbx("Outboard carriage bracket", -66, 44, -12, 24, 18, 34, C_ALUM)      # carriage → outboard screw
    cz("Vertical Z Acme (outboard)", -52, 0, 30, 350, 5, C_SCREW)           # long self-locking screw
    rbx("Vert drive nut", -64, 24, -12, 24, 142, 166, C_ALUM)
    rbx("Nut bracket to X-slide", -52, 50, -8, 16, 150, 162, C_ALUM)        # reaches inboard to X-slide

    # ── FLOATING X slide (gravity-neutral) at the corner ──
    bb("Floating X slide", 24, -11, 22, 152, 160, C_XSL)

    # ── single U-JOINT (through-axis Y): cross + tilt pin (X) + swing pin (Z) + two yokes ──
    bb("U-joint cross", 10, -10, 20, 164, 184, C_CROSS)
    cxx("Tilt pin X", -26, -4, 174, 52, 5, C_PIN)
    cz("Swing pin Z", 0, 4, 160, 190, 5, C_PIN)
    rbx("Out yoke ear L", -30, 8, -10, 20, 164, 184, C_ALUM)
    rbx("Out yoke ear R", 22, 8, -10, 20, 164, 184, C_ALUM)
    rbx("Out yoke web", -30, 60, 10, 8, 166, 182, C_ALUM)
    rbx("Out yoke stub", -6, 12, 17, 30, 168, 180, C_ALUM)
    rbx("In yoke ear Lo", -9, 18, -9, 18, 156, 168, C_XSL)
    rbx("In yoke ear Hi", -9, 18, -9, 18, 180, 192, C_XSL)
    rbx("In yoke web", -8, 16, -17, 8, 156, 192, C_XSL)
    rbx("Stub-to-frame plate", -10, 70, 40, 10, 150, 212, C_FRAME)

    # ── VERTICAL drive reach: extension shaft + bevel gearbox + handwheel at 1.2 m (abs Z) ──
    ext_far = z0 + (350 if s > 0 else -350)          # screw far end
    abscylZ("Vert drive extension", -52, 0, ext_far, HW_Z, 4, C_SCREW)
    absbox("Bevel gearbox", -66, -16, HW_Z - 16, 28, 32, 32, C_STEEL)
    diskY("Vert handwheel (1.2m)", -52, -50, HW_Z, 60, 12, C_HW)
    return "\n".join(P)


def film_plane():
    zb = STACK
    zt = CH - STACK
    return "\n".join([
        ov.ruby_box("Frame angle web", -5, 50, zb, 5, 50, zt - zb, color=C_FRAME),
        ov.ruby_box("Frame angle flange", -5, 50, zb, 50, 5, zt - zb, color=C_FRAME),
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
    txt("Single U-joint (Ruland US12-6-6-SS) — tilt X + swing Z", -30, -4, STACK + 40, -60, -40, 10)
    txt("OUTBOARD vertical Z Acme (self-locking, clear of light cone)", -52, 0, 500, -60, -40, 0)
    txt("Bevel gearbox + handwheel at 1.2 m (reachable)", -52, -50, HW_Z, -60, -45, 0)
    txt("Floating X slide (horizontal arc)", 24, 0, STACK + 6, 55, 45, 0)
    txt("Focus Acme screw + handwheel (Y)", 34, -210, CH / 2, 55, -50, 0)
    txt(f"Film plane 4499 x {FP_H} (mechanism ~{STACK} top + bottom)", 300, 53, CH / 2, 60, 45, 0)
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
        ("Bottom Corner", ["Bottom Corner", "Film Plane"], (0, 0, STACK, 360)),
        ("Top Corner", ["Top Corner", "Film Plane"], (0, 0, CH - STACK, 360)),
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
