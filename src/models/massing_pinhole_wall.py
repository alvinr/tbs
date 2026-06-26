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
    # ── PUMPS — shallow, LOW row (bodies on a wall rail); 5 across
    pw, pd, ph = ov.PUMP_W, ov.PUMP_YD_SPAN, 218     # 114 x 127 x 218
    pz = 270
    for i, cx in enumerate((2860, 3180, 3500, 3820, 4140)):
        p.append(ov.ruby_box(f"Pump P-0{i+1}", cx - pw / 2, 12, pz, pw, pd, ph, color=ov.C_PUMP))
        p.append(ov.ruby_box(f"Pump P-0{i+1} head", cx - pw / 2, 12, pz + ph, pw, 68, 40,
                             color="#3A3A42"))
    # ── ACC — shallowest, low, at the IBC end of the row
    p.append(ov.ruby_cylinder("ACC-01 (Ø127)", 4430, 127 / 2 + 12, 250, 127 / 2, 200, color=ov.C_ACC))
    return "\n".join(p)


def person():
    # simple standee on the deck, standing JUST clear of the pump projection (~165)
    px, py = 2760, 200
    body = ov.ruby_box("Person (1750, scale)", px - 225, py, DECK_Z, 450, 330, 1500, color=C_PERSON)
    head = ov.ruby_cylinder("Person head", px, py + 165, DECK_Z + 1500, 110, 250, color=C_PERSON)
    return body + "\n" + head


def build():
    comps = [
        ov.component("Context", "Context", context()),
        ov.component("Walkway Deck", "Deck", deck()),
        ov.component("Wet-end kit (raked)", "Kit", kit()),
        ov.component("Person (scale)", "Scale", person()),
    ]
    body = "\n".join(comps)
    return f'''model = Sketchup.active_model
model.start_operation("Pinhole-wall massing", true)
entities = model.active_entities
to_erase = entities.to_a.select {{ |e| e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text) }}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
opts = model.options["UnitsOptions"]; opts["LengthUnit"]=2; opts["LengthFormat"]=0
["Context","Deck","Kit","Scale"].each {{ |t| model.layers.add(t) unless model.layers[t] }}
{body}
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
