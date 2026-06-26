#!/usr/bin/env python3
"""massing_pinhole_wall.py — EXPLORATORY massing (pinhole-wall-mount branch).

Block massing of the wet end (pumps + ACC + filters) wall-mounted on the PINHOLE
WALL (Yd=0) in the clear band X2700-4674, arranged by the RAKE-BY-DEPTH principle:
the deepest items (Big Blue filters) ride HIGH, the shallow items (pumps, ACC) sit
LOW, keeping the torso band clear.  Includes the (widened) near-walkway deck and a
1750mm person for scale.  No plumbing yet — geometry feasibility only.

    python3 src/models/massing_pinhole_wall.py --send   # build in the live SketchUp doc
"""
import sys, os, argparse
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))   # repo root (src/models -> src -> root)
sys.path.insert(0, _HERE)
import generate_sketchup_model as ov

# ── band + wall ──────────────────────────────────────────────────────────────
X0, X1 = 2700, 4674            # clear mounting band on the pinhole wall (Yd0)
C_HGT, C_WID = ov.C_HGT, ov.C_WID
DECK_Z = ov.WALKWAY_H          # 130
DECK_W = 550                   # WIDENED near-walkway deck (vs 300) so you walk BESIDE the kit

C_PERSON = "#806040"
C_DECK   = "#9C7B4D"


def context():
    p = []
    # pinhole wall (a slab just behind Yd0) + floor + ceiling slabs over the band
    p.append(ov.ruby_box("Pinhole wall (context)", X0 - 50, -ov.WALL_T, 0,
                         (X1 - X0) + 100, ov.WALL_T, C_HGT, color=ov.C_SHELL, alpha=0.25))
    p.append(ov.ruby_box("Floor (context)", X0 - 50, 0, -ov.WALL_T,
                         (X1 - X0) + 100, 1200, ov.WALL_T, color=ov.C_SHELL, alpha=0.18))
    p.append(ov.ruby_box("Ceiling (context)", X0 - 50, 0, C_HGT,
                         (X1 - X0) + 100, 1200, ov.WALL_T, color=ov.C_SHELL, alpha=0.10))
    # IBC stack face hint (band ends here)
    p.append(ov.ruby_box("IBC face (context)", ov.IBC_COL_X, 0, 0, 30, 1046, 2 * ov.IBC_H_1000,
                         color=ov.C_IBC_BLUE, alpha=0.12))
    return "\n".join(p)


def deck():
    return ov.ruby_box("Near walkway deck (widened 550)", X0 - 50, 0, DECK_Z - 15,
                       (X1 - X0) + 100, DECK_W, 15, color=C_DECK, alpha=0.9)


def kit():
    p = []
    fr = ov.BB_OD / 2          # 92
    BB_H = ov.BB_H             # 340
    # ── FILTERS — deepest, HIGH (cap-up row near the ceiling); in-line ±X ports chain F1->F2->F3
    f_top = C_HGT - 48         # cap top just under the ceiling
    f_bot = f_top - BB_H       # body bottom ≈ 2000
    for i, fx in enumerate((3120, 3520, 3920)):
        p.append(ov.ruby_cylinder(f"Filter F{i+1} (Ø184)", fx, fr + 10, f_bot, fr, BB_H - 70,
                                  color=ov.C_FILTER))
        p.append(ov.ruby_cylinder(f"Filter F{i+1} cap", fx, fr + 10, f_top - 70, fr + 3, 70,
                                  color="#222228"))
    # ── PUMPS — shallow, at SHOULDER height (Z~1330-1550) so legs/feet are clear (no kicking)
    pw, pd, ph = ov.PUMP_W, ov.PUMP_YD_SPAN, 218     # 114 x 127 x 218
    pz = 1330                                         # body bottom ≈ shoulder
    for i, cx in enumerate((2860, 3180, 3500, 3820, 4140)):
        p.append(ov.ruby_box(f"Pump P-0{i+1}", cx - pw / 2, 12, pz, pw, pd, ph, color=ov.C_PUMP))
        p.append(ov.ruby_box(f"Pump P-0{i+1} head", cx - pw / 2, 12, pz + ph, pw, 68, 40,
                             color="#3A3A42"))
    # ── ACC — shallowest, shoulder height too, at the IBC end of the row
    p.append(ov.ruby_cylinder("ACC-01 (Ø127)", 4430, 127 / 2 + 12, 1350, 127 / 2, 200, color=ov.C_ACC))
    return "\n".join(p)


def person():
    # A clearly-human standee for scale (1750 tall) standing on the deck, back to the wall.
    # Stick-ish proportions so it reads as a PERSON, not equipment.
    px, py = 2760, 230
    z = DECK_Z
    pp = []
    # legs
    pp.append(ov.ruby_box("Person legs", px - 80, py, z, 160, 200, 850, color=C_PERSON, alpha=0.55))
    # torso (narrower front-back)
    pp.append(ov.ruby_box("Person torso", px - 150, py + 10, z + 850, 300, 180, 600, color=C_PERSON, alpha=0.55))
    # head
    pp.append(ov.ruby_cylinder("Person head (scale 1.75m)", px, py + 100, z + 1450, 100, 230, color=C_PERSON, alpha=0.6))
    return "\n".join(pp)


# Whole-container CONTEXT — the real overview equipment (everything EXCEPT the corridor
# wet-end being replaced: equipment_panel + water_plumbing).  optical_cone is included so
# we can SEE the kit clears the light path.
CONTEXT = [
    ("Container Shell", "Shell", "container_shell"),
    ("Walkways", "Walkways", "walkways"),
    ("Processing Tray", "Processing Tray", "processing_tray"),
    ("Pinhole Assembly", "Pinhole", "pinhole_assembly"),
    ("Optical Cone", "Optical Cone", "optical_cone"),
    ("Film Plane Mechanism", "Film Plane", "film_plane_mechanism"),
    ("Spray Bar", "Spray Bar", "spray_bar"),
    ("IBC Stack", "IBC Stack", "ibc_stack"),
    ("IBC Rack", "IBC Rack", "ibc_rack"),
    ("Light-Trap Drum", "Light Trap", "light_trap_drum"),
    ("Light-Trap Bay", "Light Trap", "light_trap_bay"),
    ("Light-Trap Door Frame", "Light Seal", "light_trap_frame"),
    ("Light Seal & Hinges", "Light Seal", "light_seal"),
    ("Electrical", "Electrical", "electrical"),
    ("Evap Cooler & Duct", "Evap Cooler", "evap_cooler"),
    ("Fans A & B", "Fans", "fans"),
    ("Chemistry Shelf", "Shelf", "shelf"),
    ("Water/Waste Hookups", "Water Hookups", "water_hookups"),
]


def build():
    comps, tags = [], set()
    for name, tag, fn in CONTEXT:
        try:
            comps.append(ov.component(name, tag, getattr(ov, fn)()))
            tags.add(tag)
        except Exception as e:                       # skip any context piece that can't build on this branch
            print(f"  (skip context {name}: {e})", file=sys.stderr)
    # the NEW pinhole-wall wet-end massing + proposed widened deck + scale figure
    for name, tag, b in [("Proposed widened deck", "Deck", deck()),
                         ("Wet-end kit (raked)", "Kit", kit()),
                         ("Person (scale)", "Scale", person())]:
        comps.append(ov.component(name, tag, b)); tags.add(tag)
    body = "\n".join(comps)
    tags_ruby = "".join(f'  model.layers.add({t!r}) unless model.layers[{t!r}]\n' for t in sorted(tags))
    return f'''model = Sketchup.active_model
model.start_operation("Pinhole-wall layout", true)
entities = model.active_entities
to_erase = entities.to_a.select {{ |e| e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text) }}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each {{ |pg| model.pages.erase(pg) }}
opts = model.options["UnitsOptions"]; opts["LengthUnit"]=2; opts["LengthFormat"]=0
{tags_ruby}{body}
# one combined scene, whole length
pg = model.pages.add("Pinhole-wall layout")
model.commit_operation
{{ ok: true }}.to_json
'''


SKP_PATH = os.path.abspath(os.path.join(_ROOT, "models", "pinhole-wall.skp"))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--send", action="store_true", help="build into the ACTIVE SketchUp doc (open a blank doc first!)")
    ap.add_argument("--save", action="store_true", help="after building, save the active doc as models/pinhole-wall.skp")
    a = ap.parse_args()
    ruby = build()
    if a.send:
        from sketchup_client import send_ruby
        print(send_ruby(ruby))
        if a.save:
            print(send_ruby(f'Sketchup.active_model.save({SKP_PATH!r}) ? "saved {SKP_PATH}" : "FAIL"'))
    else:
        print(ruby[:400])
