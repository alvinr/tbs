#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""generate_pinhole_disc_holder_model.py — Pinhole Disc Holder 3D model (logical model: pinhole-disc-holder).

The former tilt-swing mechanism was retired (tilting a pinhole board is optically inert; perspective
is the film-plane's job). This is the simple quick-change holder: a compact Ø180 front plate + a
neoprene light-seal washer + an interchangeable disc (pinhole or lens cell) + a circular retaining
ring clamped by 4 thumb screws. No tilt/swing, no dynamic component.

Geometry is single-sourced from tbs_constants.py (PDH_* — shared with generate_pinhole_disc_holder.py).
Helpers/materials come from generate_sketchup_model (`ov`).

NOTE: --send builds into the ACTIVE SketchUp document (it clears it first). Open a NEW blank
document before sending, then save the result as models/pinhole-disc-holder.skp.
"""
import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import generate_sketchup_model as ov

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "generators"))
from tbs_constants import (
    PDH_PLATE_OD, PDH_PLATE_T, PDH_APERTURE, PDH_TAPER_BORE, PDH_DISC_OD,
    PDH_DISC_SEAT_D, PDH_DISC_SEAT_DEP, PDH_WASHER_OD, PDH_WASHER_ID, PDH_WASHER_T,
    PDH_RING_OD, PDH_RING_ID, PDH_RING_T, PDH_TS_N, PDH_TS_PCD, PDH_TS_D, PDH_PINHOLE_D,
    PDH_MOUNT_BC, PDH_MOUNT_N, PDH_MOUNT_D, PDH_DWL_OFF, PDH_DWL_D,
)

mm = ov.mm
TAGS = ["Plate", "Washer", "Disc", "Ring", "Thumb screws", "Labels"]

# ── Convention: the plate lies in the X-Z plane; the optical axis is +Y. Scene (exterior) at Y=0,
#    camera/interior toward +Y. ────────────────────────────────────────────────────────────────
PLATE_Y0 = 0.0                          # scene face
PLATE_Y1 = float(PDH_PLATE_T)           # camera face (18)
SEAT_Y   = PLATE_Y1 - PDH_DISC_SEAT_DEP  # disc-seat counterbore floor (15)

C_PLATE  = ov.C_ALUM
C_WASHER = "#5A3020"     # neoprene
C_DISC   = "#2A2A2A"     # SS-302 disc
C_PIN    = "#101010"     # pinhole
C_RING   = "#BFC6D0"     # retaining ring (slightly cooler alu)
C_TS     = "#3B3B42"     # knurled thumb screw
C_STEEL  = ov.C_STEEL


def _mat(name, color, alpha=None):
    r, g, b = ov.hex_to_rgb(color)
    nm = ov.shared_mat_name(name, color, alpha)
    a = alpha if alpha is not None else 1.0
    return [f'  mat = model.materials["{nm}"] || model.materials.add("{nm}")',
            f'  mat.color = Sketchup::Color.new({r}, {g}, {b})', f'  mat.alpha = {a}', '  grp.material = mat']


def ruby_annulus(name, cx, cy, cz, r_out, r_in, height, axis="y", color=None, alpha=None, n=64):
    """A ring/tube (outer Ø with a concentric through-bore), extruded `height` along `axis`.
    Solid outer disc → drop the inner circle → erase the inner disc (smallest BOUNDS, so a thin ring
    is handled) → extrude the ring."""
    normal = {"z": "[0,0,1]", "y": "[0,1,0]", "x": "[1,0,0]"}[axis]
    comp = axis
    ctr = f'[{mm(cx)},{mm(cy)},{mm(cz)}]'
    lines = [
        f'  # {name}', '  grp = ents.add_group', f'  grp.name = "{name}"', '  ge = grp.entities',
        f'  oc = ge.add_circle({ctr}, {normal}, {mm(r_out)}, {n})',
        '  ge.add_face(oc)',
        f'  ge.add_circle({ctr}, {normal}, {mm(r_in)}, {n})',
        '  ge.grep(Sketchup::Face).min_by { |f| f.bounds.diagonal }.erase!',
        '  face = ge.grep(Sketchup::Face).first',
        f'  face.reverse! if face.normal.{comp} < 0',
        f'  face.pushpull({mm(height)})',
    ]
    if color:
        lines += _mat(name, color, alpha)
    lines.append('')
    return '\n'.join(lines)


# ── Parts ─────────────────────────────────────────────────────────────────────
def plate():
    """ICP-01 front plate — Ø180 × 18, Ø40 light aperture (thru), Ø90 scene taper (marker), Ø52
    disc-seat counterbore (camera face), 4× M6 mount holes @ Ø150, 2 dowels @ ±60, 4× M5 thumb taps."""
    out = [ruby_annulus("ICP-01 Front plate", 0, PLATE_Y0, 0, PDH_PLATE_OD / 2, PDH_APERTURE / 2,
                        PDH_PLATE_T, axis="y", color=C_PLATE, n=72)]
    # disc-seat counterbore (Ø52 recess on the camera face) — a shallow ring marker
    out.append(ruby_annulus("Disc seat counterbore", 0, SEAT_Y, 0, PDH_DISC_SEAT_D / 2, PDH_APERTURE / 2,
                            PDH_DISC_SEAT_DEP, axis="y", color="#C4CCD4", n=48))
    # scene-side taper mouth (Ø90) — a shallow ring marker on the scene face
    out.append(ruby_annulus("Scene taper mouth", 0, PLATE_Y0, 0, PDH_TAPER_BORE / 2, PDH_APERTURE / 2,
                            2, axis="y", color="#C4CCD4", n=48))
    # mount holes (4× M6 @ Ø150) — through markers
    for i in range(PDH_MOUNT_N):
        a = math.radians(45 + i * 360.0 / PDH_MOUNT_N)
        out.append(ov.ruby_cylinder(f"M6 mount hole {i+1}", (PDH_MOUNT_BC / 2) * math.cos(a), PLATE_Y0,
                                    (PDH_MOUNT_BC / 2) * math.sin(a), PDH_MOUNT_D / 2, PDH_PLATE_T,
                                    axis="y", color="#5A5A5A", n=16))
    # 2 dowels (vertical, ±60)
    for sgn in (-1, 1):
        out.append(ov.ruby_cylinder(f"Dowel {sgn}", 0, PLATE_Y0, sgn * PDH_DWL_OFF, PDH_DWL_D / 2,
                                    PDH_PLATE_T, axis="y", color="#8A8A8A", n=12))
    return '\n'.join(out)


def washer():
    """Neoprene light-seal washer — Ø56/Ø40 × 1.5, in the disc-seat counterbore floor."""
    return ruby_annulus("Neoprene light-seal washer", 0, SEAT_Y, 0, PDH_WASHER_OD / 2, PDH_WASHER_ID / 2,
                        PDH_WASHER_T, axis="y", color=C_WASHER, n=48)


def disc():
    """Interchangeable disc — Ø50 × 1 (SS-302 pinhole shim, or a lens cell), on the washer; the
    Ø2.17 pinhole is the aperture (shown proud so it reads)."""
    dz = SEAT_Y + PDH_WASHER_T
    return '\n'.join([
        ov.ruby_cylinder("ICP-02 Disc (pinhole / lens)", 0, dz, 0, PDH_DISC_OD / 2, 1.5, axis="y", color=C_DISC, n=48),
        ov.ruby_cylinder("Pinhole aperture (Ø2.17)", 0, dz - 0.5, 0, PDH_PINHOLE_D / 2 + 1.0, 2.5, axis="y", color=C_PIN, n=20),
    ])


def ring():
    """ICP-03 circular retaining ring — Ø90/Ø44 × 5, on the camera face, clamping the disc rim."""
    return ruby_annulus("ICP-03 Retaining ring", 0, PLATE_Y1, 0, PDH_RING_OD / 2, PDH_RING_ID / 2,
                        PDH_RING_T, axis="y", color=C_RING, n=64)


def thumb_screws():
    """4× M5 knurled thumb screws @ Ø74 — through the ring into the plate."""
    out = []
    for i in range(PDH_TS_N):
        a = math.radians(45 + i * 360.0 / PDH_TS_N)
        tx, tz = (PDH_TS_PCD / 2) * math.cos(a), (PDH_TS_PCD / 2) * math.sin(a)
        out.append(ov.ruby_cylinder(f"M5 thumb screw shaft {i+1}", tx, SEAT_Y, tz, PDH_TS_D / 2,
                                    PLATE_Y1 + PDH_RING_T - SEAT_Y, axis="y", color=C_STEEL, n=12))
        out.append(ov.ruby_cylinder(f"Knurled knob {i+1}", tx, PLATE_Y1 + PDH_RING_T, tz, 6, 6,
                                    axis="y", color=C_TS, n=20))
    return '\n'.join(out)


def labels_ruby():
    def lab(text, pt, vec):
        p = f'[{mm(pt[0])},{mm(pt[1])},{mm(pt[2])}]'
        v = f'[{mm(vec[0])},{mm(vec[1])},{mm(vec[2])}]'
        return f'  t = entities.add_text("{text}", {p}, {v}); t.layer = model.layers["Labels"]'
    rows = [
        ("ICP-01 FRONT PLATE (Ø180)", (PDH_PLATE_OD / 2 - 15, PLATE_Y0, 0), (55, -20, 40)),
        ("ICP-03 RETAINING RING\n+ 4 thumb screws", (PDH_RING_OD / 2, PLATE_Y1 + PDH_RING_T, 0), (60, 30, 40)),
        ("ICP-02 DISC — pinhole / lens\n(quick-change)", (0, PLATE_Y1 + PDH_RING_T, PDH_RING_ID / 2 - 4), (0, 45, 70)),
        ("Ø40 LIGHT APERTURE\n(Ø90 scene taper)", (0, PLATE_Y0, -PDH_APERTURE / 2), (-70, -20, -50)),
    ]
    return '\n'.join(lab(*r) for r in rows)


def generate_ruby():
    body = '\n'.join([
        ov.component("ICP-01 Front plate", "Plate", plate()),
        ov.component("Neoprene washer", "Washer", washer()),
        ov.component("ICP-02 Disc", "Disc", disc()),
        ov.component("ICP-03 Retaining ring", "Ring", ring()),
        ov.component("Thumb screws", "Thumb screws", thumb_screws()),
    ])
    tags_ruby = '\n'.join(f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'
    scenes = [
        ("Assembled", ["Plate", "Washer", "Disc", "Ring", "Thumb screws"]),
        ("Labeled", ["Plate", "Washer", "Disc", "Ring", "Thumb screws", "Labels"]),
    ]
    def slit(s):
        name, tags = s
        return f'["{name}", [' + ', '.join(f'"{t}"' for t in tags) + ']]'
    scenes_ruby = '[' + ', '.join(slit(s) for s in scenes) + ']'

    sf_meta = ov.sketchfab_meta_ruby(
        "TBS-001 Pinhole Disc Holder",
        "The pinhole-end front board of The Big Shoebox Project — a compact quick-change disc holder: "
        "an interchangeable pinhole disc (or lens cell) clamped against a light-seal washer by a "
        "circular retaining ring with four thumb screws.",
        ov.model_uid("pinhole-disc-holder"), "tbs sketchup pinhole", force_name=True)

    return f'''# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/ — do not edit this .rb directly.
model = Sketchup.active_model
model.start_operation("TBS-001 Pinhole Disc Holder", true)
entities = model.active_entities
opts = model.options["UnitsOptions"]; opts["LengthUnit"]=2; opts["LengthFormat"]=0; opts["LengthPrecision"]=1

to_erase = entities.to_a.select {{ |e| e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text) || e.is_a?(Sketchup::SectionPlane) }}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each {{ |p| model.pages.erase(p) }}

{sf_meta}
{tags_ruby}

{body}

# ── Labels (Labels tag — shown only in the "Labeled" scene) ──
{labels_ruby()}

{ov.license_note()}

model.definitions.purge_unused
model.materials.purge_unused
keep_tags = {keep}; dl = model.layers[0]
model.layers.to_a.each {{ |l| next if l==dl||keep_tags.include?(l.name); model.layers.remove(l,true) rescue nil }}

model.layers.each {{ |l| l.visible = true }}
bb = model.bounds; ctr = bb.center
dir = Geom::Vector3d.new(-0.5, 0.8, 0.35); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.6)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents

{scenes_ruby}.each {{ |name, tags|
  model.layers.each {{ |l| l.visible = (l == dl || tags.include?(l.name)) }}
  model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
  model.active_view.zoom_extents
  page = model.pages.add(name); page.use_camera = true
}}
model.layers.each {{ |l| l.visible = true }}
model.layers["Labels"].visible = false

model.commit_operation

{{ success: true, model: "pinhole-disc-holder", scenes: model.pages.count,
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   plate_od: {PDH_PLATE_OD} }}.to_json
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate the TBS-001 Pinhole Disc Holder model")
    parser.add_argument("--save", action="store_true", help="Write Ruby to src/models/pinhole-disc-holder.rb")
    parser.add_argument("--send", action="store_true", help="Send to the ACTIVE SketchUp document (clears it first)")
    args = parser.parse_args()

    ruby = generate_ruby()
    if args.save:
        out = os.path.join(os.path.dirname(__file__), "pinhole-disc-holder.rb")
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
