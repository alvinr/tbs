#!/usr/bin/env python3
"""massing_corridor_panel.py — EXPLORATORY (pinhole-wall-mount branch).

The NEW corridor plumbing panel.  Starts from the deep-box IBC restraint/equipment frame
as it stood at the fork, but with ONLY the REAR (far-wall) panel — the left/waste-wall
panel is gone (the filters moved to the pinhole wall).  The four returned pumps
(P-01/P-03/P-04/P-05) + ACC-01 and the Stage-A tray-drain chain (SV-02 + DV-02) will mount
on the rear panel facing the operator (added next).  Reuses generate_sketchup_model helpers.

    python3 src/models/massing_corridor_panel.py --send --save   # build into the ACTIVE (blank) doc, save corridor-panel.skp
"""
import sys, os, argparse
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, _HERE)
import generate_sketchup_model as ov

# ── deep-box frame geometry (from the fork; one source) ──
S       = ov.IBC_FRAME_RHS               # 50×50 RHS
TOP_Z   = 2 * ov.IBC_H_1000 - 40         # 2296 — frame reaches near the stack top
YD_NEAR, YD_FAR = 1046, 1316             # plumbing-corridor edges
FRONT_X = ov.IBC_COL_X - 20              # 4654 — front uprights on the wall-bar line
DEPTH   = 450                            # deep box (≈⅓ tote depth)
BACK_X  = FRONT_X + DEPTH                 # 5104 — the REAR panel plane (pumps mount here, face -X)
EQT     = ov.EQPANEL_T                    # 18mm ply
C_BOLT  = "#3A3A42"


def frame():
    """Deep 4-leg box (uprights + butt-jointed rings + feet) with REAR-panel brackets only."""
    p = []
    up_yds = (YD_NEAR, YD_FAR - S)
    box_xs = (FRONT_X, BACK_X)
    for ux in box_xs:                                  # 4 corner uprights
        for yd in up_yds:
            p.append(ov.ruby_box("Frame upright", ux, yd, 0, S, S, TOP_Z, color=ov.C_STEEL))
    for rz in (0, TOP_Z - S):                          # bottom + top rings, rails BUTT between uprights
        for ux in box_xs:
            p.append(ov.ruby_box("Frame rail (Yd)", ux, YD_NEAR + S, rz, S, (YD_FAR - S) - (YD_NEAR + S), S, color=ov.C_STEEL))
        for yd in up_yds:
            p.append(ov.ruby_box("Frame rail (X)", FRONT_X + S, yd, rz, BACK_X - (FRONT_X + S), S, S, color=ov.C_STEEL))
    # floor feet (150×150×12 plate + 4× M12) under each upright
    fp, ft, bpc = ov.IBC_FOOT_PLATE, ov.IBC_FOOT_PLATE_T, ov.IBC_FOOT_BOLT_PCD // 2
    for ux in box_xs:
        for yd in up_yds:
            cx, cy = ux + S / 2, yd + S / 2
            p.append(ov.ruby_box("Foot plate", cx - fp / 2, cy - fp / 2, 0, fp, fp, ft, color=ov.C_STEEL))
            for dx in (-bpc, bpc):
                for dy in (-bpc, bpc):
                    p.append(ov.ruby_cylinder("Foot anchor M12", cx + dx, cy + dy, 0, 7, ft + 4, color=C_BOLT, axis="z"))
    # REAR-panel mount brackets only (on the back uprights, set back behind the inside face)
    bw, bproj = 60, 40
    for py, pdir in ((YD_NEAR + S, +1), (YD_FAR - S, -1)):
        for bz in (120, TOP_Z / 2, TOP_Z - 120):
            p.append(ov.ruby_box("Rear-panel bracket", BACK_X + EQT, (py if pdir > 0 else py - bproj), bz - bw / 2,
                                 30, bproj, bw, color=ov.C_STEEL))
    return "\n".join(p)


def rear_panel():
    """The single 18mm marine-ply REAR panel, recessed into the back-wall opening (flush with
    the back posts' −X inside face), cut to the inside-of-frame opening."""
    pz0, ph = S, (TOP_Z - S) - S
    return ov.ruby_box("Rear panel (18mm marine ply)", BACK_X, YD_NEAR + S, pz0,
                       EQT, (YD_FAR - S) - (YD_NEAR + S), ph, color=ov.C_PLY)


def context():
    """Ghost of the IBC stack + a floor slice so the corridor frame reads in place."""
    p = []
    p.append(ov.component("IBC Stack", "IBC Stack", ov.ibc_stack(alpha=0.20)))
    x0 = 4300
    p.append(ov.component("Floor (context)", "Context",
             ov.ruby_box("Floor", x0, 0, -ov.WALL_T, ov.C_LEN - x0, ov.C_WID, ov.WALL_T, color=ov.C_SHELL, alpha=0.16)))
    return "\n".join(p)


def build():
    comps = [context(),
             ov.component("Corridor frame (deep box)", "Frame", frame()),
             ov.component("Rear panel (ply)", "Rear Panel", rear_panel())]
    body = "\n".join(comps)
    tags = ["IBC Stack", "Context", "Frame", "Rear Panel"]
    tags_ruby = "".join(f'  model.layers.add({t!r}) unless model.layers[{t!r}]\n' for t in tags)
    return f'''model = Sketchup.active_model
model.start_operation("Corridor panel massing", true)
entities = model.active_entities
to_erase = entities.to_a.select {{ |e| e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text) }}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each {{ |pg| model.pages.erase(pg) }}
opts = model.options["UnitsOptions"]; opts["LengthUnit"]=2; opts["LengthFormat"]=0
{tags_ruby}{body}
pg = model.pages.add("Corridor panel")
model.commit_operation
{{ ok: true }}.to_json
'''


SKP_PATH = os.path.abspath(os.path.join(_ROOT, "models", "corridor-panel.skp"))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--send", action="store_true", help="build into the ACTIVE SketchUp doc (open a blank doc first!)")
    ap.add_argument("--save", action="store_true", help="save the active doc as models/corridor-panel.skp")
    a = ap.parse_args()
    ruby = build()
    if a.send:
        from sketchup_client import send_ruby
        print(send_ruby(ruby))
        if a.save:
            print(send_ruby(f'Sketchup.active_model.save({SKP_PATH!r}) ? "saved {SKP_PATH}" : "FAIL"'))
    else:
        print(ruby[:300])
