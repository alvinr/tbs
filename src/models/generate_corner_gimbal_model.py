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

TAGS = ["Corners", "Film Plane", "Pinhole", "Labels"]

C_STEEL = "#B0B0B8"; C_CROSS = "#8A8A92"; C_PANEL = "#1F3B66"; C_CAR = "#C04010"
C_TILT = "#2E8B57"   # vertical (Z) slide — TILT accommodation (green)
C_SWING = "#7B5EA7"  # horizontal (X) slide — SWING accommodation (purple)

# real container/film layout (mm) — sourced from tbs_constants via ov (no hardcoded copies)
CH = ov.C_HGT                        # interior height
X_L, X_R = ov.FP_X_L, ov.FP_X_R      # film left / right edges (X, the long axis)
FP_Y = ov.FP_Y                       # film depth from the pinhole wall (Y)
PH_X, PH_Z = ov.PH_X, ov.C_HGT // 2  # pinhole X (film-width centre) and Z (mid-height)
CZ_F, CZ_C = 15, ov.C_HGT - 15       # floor / ceiling rail-mount Z
BUILD = 140                          # rail-mount → panel-corner stack height (mm)
PZ0, PZ1 = CZ_F + BUILD, CZ_C - BUILD   # panel bottom / top edge Z (≈ 155 / 2233)


def corner(tag, cx, cz, sv, cin):
    """One corner's slide-and-clamp stack. cx = corner X; cz = rail-mount Z; sv = +1 builds up
    (floor) / -1 down (ceiling); cin = +1 if panel centre is at +X (left corners) / -1 (right)."""
    P = []

    def band(name, x, w, y, d, a, b, col, al=None):     # box; z from build-heights a..b (a<b)
        zmin = cz + a if sv > 0 else cz - b
        P.append(ov.ruby_box(f"{name} {tag}", x, y, zmin, w, d, b - a, color=col, alpha=al))

    xo = cx - cin * 30                                  # vertical slide, just outboard of the corner
    xr0 = cx if cin > 0 else cx - 260                   # horizontal rail extends toward centre (~260mm swing travel)
    # DEPTH RAIL — 1.5" (1.9" OD) 304 pipe (both beam & rail). Spans the FULL container width
    # (wall-to-wall in Y), flanged + through-bolted at each end; a 4-wheel Speed-Rail trolley rides it.
    zc = cz + sv * 24                                   # pipe centre Z (48mm OD → r24)
    P.append(ov.ruby_cylinder(f"Depth pipe rail Y (1.5in 304, grey) {tag}", cx, 0, zc,
                              24, ov.C_WID, color=C_STEEL, axis="y"))
    for fy in (0, ov.C_WID - 12):                       # interior flange plate at each wall (8 total)
        P.append(ov.ruby_box(f"Pipe flange {tag} {int(fy)}", cx - 45, fy, zc - 45, 90, 12, 90, color=C_CROSS))
    for ey, w2 in ((-ov.WALL_T - 8, "PH"), (ov.C_WID + ov.WALL_T, "far")):  # exterior backing plate (8)
        P.append(ov.ruby_box(f"Pipe wall plate {tag} {w2}", cx - 50, ey, zc - 50, 100, 8, 100, color=C_STEEL, alpha=0.5))
    band("Depth trolley cradle (red)", cx - 26, 52, FP_Y - 26, 48, 0, 48, C_CAR, al=0.35)
    # 4 wheels = a fore pair + an aft pair, each a 90° V (2 wheels) on the interior side of the pipe
    for wy in (FP_Y - 24, FP_Y - 6):
        for wsx in (-18, 18):
            P.append(ov.ruby_cylinder(f"Trolley wheel {tag} {int(wy)}_{wsx}", cx + wsx - 4, wy,
                                      zc + sv * 22, 8, 8, color=C_CROSS, axis="x"))
    # vertical slide rail sized to the ~280mm TILT travel it must take up (not the nominal stack height)
    band("Vertical Z slide rail (TILT ~280mm, green)", xo - 7, 16, FP_Y - 9, 18, 18, 300, C_TILT)
    band("Vertical Z carriage", xo - 17, 34, FP_Y - 15, 30, 95, 145, C_TILT)
    # horizontal slide rail sized to the ~260mm SWING travel
    band("Horizontal X slide rail (SWING ~260mm, purple)", xr0, 260, FP_Y - 7, 14, 108, 122, C_SWING)
    band("Horizontal X carriage", cx - 24, 48, FP_Y - 12, 24, 114, 136, C_SWING)
    band("U-joint", cx - 12, 24, FP_Y - 12, 24, 130, 150, C_CROSS)
    return "\n".join(P)


def corners():
    P = [
        corner("BL", X_L, CZ_F, +1, +1),
        corner("BR", X_R, CZ_F, +1, -1),
        corner("TL", X_L, CZ_C, -1, +1),
        corner("TR", X_R, CZ_C, -1, -1),
    ]
    # faint floor + ceiling so the UPPER (ceiling) and LOWER (floor) rails read as mounted structure
    P.append(ov.ruby_box("Floor", X_L - 250, 0, -12, (X_R - X_L) + 500, FP_Y + 250, 12, color=C_STEEL, alpha=0.05))
    P.append(ov.ruby_box("Ceiling", X_L - 250, 0, CH, (X_R - X_L) + 500, FP_Y + 250, 12, color=C_STEEL, alpha=0.05))
    return "\n".join(P)


def film_plane():
    return ov.ruby_box("Film plane (ghost)", X_L, FP_Y, PZ0, X_R - X_L, 4, PZ1 - PZ0,
                       color=C_PANEL, alpha=0.14)


def pinhole():
    P = [
        ov.ruby_box("Pinhole wall (far)", 0, -14, 0, 5893, 14, CH, color=C_STEEL, alpha=0.06),
        ov.ruby_box("Pinhole aperture", PH_X - 11, -18, PH_Z - 11, 22, 22, 22, color="#101014"),
    ]
    corners_xyz = [(X_L, PZ1), (X_R, PZ1), (X_L, PZ0), (X_R, PZ0)]
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
    txt(f"Film plane 4499 x {PZ1 - PZ0} (mechanism ~{BUILD} top + bottom)", 2400, FP_Y, PH_Z, 60, 45, 20)
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


def generate_ruby():
    comps = [
        ov.component("Corners", "Corners", corners()),
        ov.component("Film Plane", "Film Plane", film_plane()),
        ov.component("Pinhole", "Pinhole", pinhole()),
    ]
    body = "\n".join(comps)
    tags_ruby = "\n".join(f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep = "[" + ", ".join(f'"{t}"' for t in TAGS) + "]"
    show = ["Corners", "Film Plane", "Pinhole"]
    # iso scenes handled by the loop (target x,y,z,dist); side/top handled explicitly after
    iso = [
        ("Overview", show, (2400, FP_Y - 400, CH / 2, 6500)),
        ("Corner detail", show, (X_L, FP_Y, PZ0 + 30, 620)),
        ("Labeled", show + ["Labels"], (2400, FP_Y - 400, CH / 2, 7200)),
    ]

    def scene_lit(n, tags, tgt):
        tg = "[" + ", ".join(f'"{t}"' for t in tags) + "]"
        cam = f"[{ov.mm(tgt[0])}, {ov.mm(tgt[1])}, {ov.mm(tgt[2])}, {ov.mm(tgt[3])}]"
        return f'["{n}", {tg}, {cam}]'
    iso_ruby = "[" + ", ".join(scene_lit(*s) for s in iso) + "]"
    show_ruby = "[" + ", ".join(f'"{t}"' for t in show) + "]"

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

# ── iso scenes (Overview / Corner detail / Labeled) ──
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
