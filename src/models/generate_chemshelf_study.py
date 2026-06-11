#!/usr/bin/env python3
"""TBS-001 — Fold-down Chemistry Shelf STUDY (review-only 3D model).

Explores relocating the chem prep shelf to the WIDENED near-walkway section, LEFT
of the battery bank, as a wall-hinged FOLD-DOWN shelf so it no longer interacts
with the film-plane swing (it is only deployed while mixing, before exposure):

  - Piano hinge along the shelf BACK edge on the pinhole wall (Yd0) at the work
    surface height Z=SHELF_H (1075, same as the current shelf — 945mm above the deck).
  - IN USE: folds DOWN to horizontal, held level by a pair of STAYS from the wall
    above (they carry the shelf + chemistry load).
  - TRANSPORT: folds UP flat against the wall (Z1075 -> ~1375), latched.
  - The evap cooler (stow X1450-2050, top Z950) slides UNDER the deployed shelf
    (underside Z1050) and tucks below it when folded up.

Usage (build into the ACTIVE blank SketchUp doc — review only, no .skp committed yet):
    python3 src/models/generate_chemshelf_study.py --save        # write .rb
    python3 src/models/generate_chemshelf_study.py --save --send # build into the ACTIVE (blank) doc
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "generators"))
import generate_sketchup_model as ov
import tbs_constants as k

ruby_box, ruby_cylinder, ruby_pipe = ov.ruby_box, ov.ruby_cylinder, ov.ruby_pipe

# ── Fold-down shelf geometry (the proposal) ──────────────────────────────────
SX_L, SX_R = 1180, 1780             # shelf X span (600 wide), LEFT of the batteries (BA_X=1810)
SDEP       = 300                    # shelf depth into the walkway (Yd) when deployed
STOP_Z     = k.SHELF_H              # 1075 — work-surface top (same as current)
ST         = 25                     # shelf slab thickness
SBOT_Z     = STOP_Z - ST            # 1050 — underside
LIP        = 15                     # spill-lip height
STAY_Z     = STOP_Z + 230           # wall stay anchor, above the hinge
DECK_Z     = k.WALKWAY_H            # 130 — walkway deck top
WIDE_XL    = k.WALKWAY_NEAR_WIDE_X_L  # 1155
WIDE_XR    = k.WALKWAY_NEAR_WIDE_X_R  # 2629
WIDE_W     = k.WALKWAY_NEAR_WIDE_W    # 500 — widened walkway depth

C_SHELF = "#C8B06A"   # chem shelf (warm gold)
C_HINGE = "#707880"   # steel hinge / stays
C_EVAPC = "#9AB0C0"   # evap cooler ghost

TAP_NEW_X = SX_L - 50   # 1130 — TAP-01 relocated LEFT of the shelf (battery bank is to the right)

TAGS = ["Context", "Equipment", "Shelf Deployed", "Shelf Stowed", "Evap", "Tap", "Labels"]


def context():
    """Pinhole-wall end ghost around the widened walkway: floor, ceiling, pinhole
    wall, and the widened near-walkway grate (X~1000-2400)."""
    x0, x1, t = 900, 2500, k.WALL_T
    xl = x1 - x0
    return '\n'.join([
        ruby_box("Floor (context)", x0, 0, -t, xl, WIDE_W + 200, t, color=ov.C_SHELL, alpha=0.22),
        ruby_box("Ceiling (context)", x0, 0, k.C_HGT, xl, WIDE_W + 200, t, color=ov.C_SHELL, alpha=0.08),
        ruby_box("Pinhole wall (context)", x0, -t, 0, xl, t, k.C_HGT, color=ov.C_SHELL, alpha=0.16),
        # widened near-walkway grate (the deck the operator stands on)
        ruby_box("Widened walkway grate (Z115-130)", WIDE_XL, 0, DECK_Z - k.WALKWAY_GRATE_T,
                 WIDE_XR - WIDE_XL, WIDE_W, k.WALKWAY_GRATE_T, color=ov.C_WALKWAY, alpha=0.6),
    ])


def equipment():
    """Pinhole-wall equipment the shelf must sit clear of: the battery bank (low,
    to the RIGHT of the shelf), the EP (high), and the power panel (high, flush)."""
    parts = [
        ruby_box(f"Battery bank (X{k.BA_X}-{k.BA_X+k.BA_W}, Z{k.BA_H_LO}-{k.BA_H_HI})",
                 k.BA_X, 0, k.BA_H_LO, k.BA_W, k.BA_D, k.BA_H_HI - k.BA_H_LO,
                 color=ov.C_BATT, alpha=0.5),
        ruby_box(f"Electrical panel (Z{k.EP_H_LO}-{k.EP_H_HI})",
                 k.EP_X, 0, k.EP_H_LO, k.EP_W, 160, k.EP_H_HI - k.EP_H_LO,
                 color=ov.C_ELEC, alpha=0.4),
        ruby_box("Power panel (flush, high)",
                 k.PWR_PANEL_X, 0, k.PWR_PANEL_Z, k.PWR_PANEL_W, 6, k.PWR_PANEL_H,
                 color=ov.C_ELEC, alpha=0.35),
    ]
    return '\n'.join(parts)


def _shelf_slab(name, x0, y0, z0, wx, wy, wz, *, alpha=1.0):
    """A shelf board + spill lip (front + two sides)."""
    out = [ruby_box(name, x0, y0, z0, wx, wy, wz, color=C_SHELF, alpha=alpha)]
    return out


def shelf_deployed():
    """The shelf folded DOWN to horizontal (in use): slab + spill lip + the piano
    hinge on the wall + two stays from the wall above carrying the load."""
    parts = []
    # board (top at STOP_Z)
    parts.append(ruby_box("Chem shelf board (deployed)", SX_L, 0, SBOT_Z, SX_R - SX_L, SDEP, ST,
                          color=C_SHELF))
    # spill lip: front edge + two ends
    parts.append(ruby_box("Lip front", SX_L, SDEP - 6, STOP_Z, SX_R - SX_L, 6, LIP, color=C_SHELF))
    for ex in (SX_L, SX_R - 6):
        parts.append(ruby_box("Lip end", ex, 0, STOP_Z, 6, SDEP, LIP, color=C_SHELF))
    # piano hinge along the back edge on the wall (Yd0, Z=STOP_Z)
    parts.append(ruby_cylinder("Piano hinge (back edge)", SX_L, 0, STOP_Z - 6,
                               6, SX_R - SX_L, color=C_HINGE, axis="x"))
    # two stays from the wall (above the hinge) to the front corners — carry the load
    for sx in (SX_L + 25, SX_R - 25):
        parts.append(ruby_pipe(f"Stay X{sx}", (sx, 0, STAY_Z), (sx, SDEP - 10, STOP_Z),
                               6, color=C_HINGE))
        # small wall bracket the stay anchors to
        parts.append(ruby_box("Stay wall anchor", sx - 12, 0, STAY_Z - 12, 24, 8, 24, color=C_HINGE))
    return '\n'.join(parts)


def shelf_stowed():
    """The shelf folded UP for transport (ghost): a vertical slab against the wall,
    Z STOP_Z..STOP_Z+SDEP, plus a latch at the top."""
    parts = []
    z0, z1 = STOP_Z, STOP_Z + SDEP                # 1075..1375
    parts.append(ruby_box("Chem shelf board (stowed/transport)", SX_L, 0, z0,
                          SX_R - SX_L, ST, z1 - z0, color=C_SHELF, alpha=0.35))
    # transport latch near the top
    parts.append(ruby_box("Transport latch", (SX_L + SX_R) / 2 - 30, 0, z1 - 30,
                          60, 18, 24, color=C_HINGE, alpha=0.6))
    return '\n'.join(parts)


def relocated_tap():
    """TAP-01 relocated to the LEFT of the shelf (X~1130) since the battery bank is to
    the right. A 3/4" branch riser on the pinhole wall + BV-06 isolation valve + a
    spout reaching over the shelf's left end to fill containers."""
    tx = TAP_NEW_X
    top = STOP_Z + SDEP   # 1375 — align the tap top with the stowed (folded-up) shelf top
    parts = [
        ruby_cylinder("Tap branch riser (3/4 HDPE)", tx, 18, 850, 12, top - 850, color=ov.C_BLUE, axis="z"),
        ruby_box("BV-06 (blue isolation)", tx - 18, 4, 1010, 36, 36, 40, color=C_HINGE),
        ruby_pipe("Tap spout (out)", (tx, 18, top), (tx, 110, top), 10, color=ov.C_BLUE),
        ruby_pipe("Tap spout (down)", (tx, 110, top), (tx, 110, 1150), 10, color=ov.C_BLUE),
    ]
    return '\n'.join(parts)


def evap_ghost():
    """The evap cooler in its stow position — slides UNDER the deployed shelf
    (top Z950 vs shelf underside Z1050) and tucks below the folded-up shelf."""
    return ruby_box(f"Evap cooler (stow, top Z{k.EVAP_STOW_Z + k.EVAP_H})",
                    k.EVAP_STOW_X, 0, k.EVAP_STOW_Z, k.EVAP_W, k.EVAP_D, k.EVAP_H,
                    color=C_EVAPC, alpha=0.3)


# (x, y, z, text, leader dx, dy, dz) — mm
POINT_LABELS = [
    ((SX_L + SX_R) / 2, SDEP, STOP_Z, "CHEM SHELF — fold-down\n(deployed, Z1075 = 945 above deck)", -150, 650, 500),
    (SX_L, 0, STOP_Z, "PIANO HINGE on pinhole wall\n(back edge, Z1075)", -350, -250, 350),
    (SX_R - 25, SDEP - 10, STOP_Z, "STAY (carries the load)\nfolds flat when stowed", 250, 450, 350),
    ((SX_L + SX_R) / 2, ST, STOP_Z + SDEP, "FOLDS UP for transport\n(vertical, Z1075-1375)", 200, -350, 250),
    (k.BA_X, 0, k.BA_H_HI, "Battery bank\n(shelf sits LEFT of it)", 350, -350, 350),
    (k.EVAP_STOW_X + k.EVAP_W / 2, k.EVAP_D, k.EVAP_STOW_Z + k.EVAP_H,
     "Evap slides UNDER\n(top Z950 < shelf Z1050)", 0, 600, 250),
    (TAP_NEW_X, 110, STOP_Z + SDEP, "TAP-01 RELOCATED\nleft of the shelf (X~1130)\ntop aligned w/ stowed shelf (Z1375)", -350, 350, 250),
]


def labels_ruby():
    rows = []
    for x, y, z, text, dx, dy, dz in POINT_LABELS:
        rows.append(
            f'anc = Geom::Point3d.new({ov.mm(x)}, {ov.mm(y)}, {ov.mm(z)})\n'
            f'txt = entities.add_text("{text}", anc, Geom::Vector3d.new({ov.mm(dx)}, {ov.mm(dy)}, {ov.mm(dz)}))\n'
            f'txt.layer = model.layers["Labels"] rescue nil')
    return '\n'.join(rows)


def generate_ruby():
    comps = [
        ov.component("Container (ghost)", "Context", context()),
        ov.component("Pinhole-wall equipment", "Equipment", equipment()),
        ov.component("Chem Shelf (deployed)", "Shelf Deployed", shelf_deployed()),
        ov.component("Chem Shelf (stowed)", "Shelf Stowed", shelf_stowed()),
        ov.component("Evap cooler (ghost)", "Evap", evap_ghost()),
        ov.component("TAP-01 (relocated)", "Tap", relocated_tap()),
    ]
    body = '\n'.join(comps)
    tags_ruby = '\n'.join(f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'
    comp_tags = [t for t in TAGS if t != "Labels"]
    scenes = [
        ("Combined", comp_tags),
        ("Deployed (in use)", ["Context", "Equipment", "Shelf Deployed", "Evap", "Tap"]),
        ("Stowed (transport)", ["Context", "Equipment", "Shelf Stowed", "Evap", "Tap"]),
        ("Labeled", TAGS),
    ]
    scenes_ruby = '[' + ', '.join(
        '["%s", [%s]]' % (n, ', '.join(f'"{t}"' for t in tags)) for n, tags in scenes) + ']'

    return f'''model = Sketchup.active_model
model.start_operation("TBS-001 Fold-down Chem Shelf Study", true)
entities = model.active_entities
opts = model.options["UnitsOptions"]; opts["LengthUnit"]=2; opts["LengthFormat"]=0; opts["LengthPrecision"]=1
to_erase = entities.to_a.select {{ |e| e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text) }}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each {{ |p| model.pages.erase(p) }}

{tags_ruby}

{body}

{labels_ruby()}

{ov.license_note()}

model.definitions.purge_unused
model.materials.purge_unused
keep_tags = {keep}
default_layer = model.layers[0]
model.layers.to_a.each {{ |l| model.layers.remove(l, true) rescue nil unless l == default_layer || keep_tags.include?(l.name) }}

model.layers.each {{ |l| l.visible = (l.name != "Labels") }}
bb = model.bounds; ctr = bb.center
dir = Geom::Vector3d.new(0.55, -0.74, 0.4); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.4)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents
{scenes_ruby}.each {{ |name, tags|
  model.layers.each {{ |l| l.visible = (l == default_layer || tags.include?(l.name)) }}
  page = model.pages.add(name); page.use_camera = true
}}
model.layers.each {{ |l| l.visible = true }}
model.commit_operation
{{ success: true, model: "Fold-down Chem Shelf Study",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   scenes: model.pages.count }}.to_json
'''


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--save", action="store_true")
    p.add_argument("--send", action="store_true")
    args = p.parse_args()
    ruby = generate_ruby()
    if args.save:
        out = os.path.join(os.path.dirname(__file__), "chemshelf-study.rb")
        open(out, "w").write(ruby)
        print(f"  {out} saved ({len(ruby)} bytes)")
    if args.send:
        from sketchup_client import send_ruby, SketchupError
        try:
            print(f"  SketchUp: {send_ruby(ruby)}")
        except SketchupError as e:
            print(f"  error: {e}", file=sys.stderr); sys.exit(1)
    if not args.save and not args.send:
        print(ruby)
