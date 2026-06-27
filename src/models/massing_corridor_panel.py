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
C_HANDLE = "#C0202A"                      # red diverter handle


def _arm(nm, cx, cy, cz, axis, sd, body, L, r, color):
    """One port stub of a fitting — a cylinder from the body face outward along an axis."""
    if axis == "x":
        x0 = cx + body / 2 if sd > 0 else cx - body / 2 - L
        return ov.ruby_cylinder(nm, x0, cy, cz, r, L, color=color, axis="x")
    if axis == "y":
        y0 = cy + body / 2 if sd > 0 else cy - body / 2 - L
        return ov.ruby_cylinder(nm, cx, y0, cz, r, L, color=color, axis="y")
    z0 = cz + body / 2 if sd > 0 else cz - body / 2 - L
    return ov.ruby_cylinder(nm, cx, cy, z0, r, L, color=color, axis="z")


def diverter(name, cx, cy, cz, run="x", branch="z-", handle="y+", color=None, L=55, r=13):
    """3-way diverter = a standard T-port valve (3 coplanar ports, handle perpendicular).
    The 3 pipes lie in a plane (seen face-on as a T); the RED handle projects out of that
    plane toward the operator.  `run` is the through-run axis (both ways); `branch` is the
    divert port as axis+sign (default 'z-' = exits the underside); `handle` is the axis+sign
    the handle projects (default 'y+' for a pinhole-wall mount; use 'x-' on the corridor
    panel, which faces -X).  Valve body kept yellow (color defaults to C_VALVE)."""
    color = color or ov.C_VALVE
    body = 46
    ba, bs = branch[0], (+1 if "+" in branch else -1)
    ha, hs = handle[0], (+1 if "+" in handle else -1)
    p = [ov.ruby_box(f"{name} body", cx - body / 2, cy - body / 2, cz - body / 2, body, body, body, color=color)]
    p.append(_arm(f"{name} run +", cx, cy, cz, run, +1, body, L, r, color))
    p.append(_arm(f"{name} run -", cx, cy, cz, run, -1, body, L, r, color))
    p.append(_arm(f"{name} branch", cx, cy, cz, ba, bs, body, L, r, color))
    # RED handle: stem out along the `handle` axis, lever bar along the run axis at the tip
    p.append(_arm(f"{name} handle stem", cx, cy, cz, ha, hs, body, 42, 6, C_HANDLE))
    tip = {"x": (cx + hs * (body / 2 + 48), cy, cz),
           "y": (cx, cy + hs * (body / 2 + 48), cz),
           "z": (cx, cy, cz + hs * (body / 2 + 48))}[ha]
    lx, ly, lz = tip
    if run == "x":
        p.append(ov.ruby_box(f"{name} handle lever", lx - 32, ly - 8, lz - 7, 64, 16, 14, color=C_HANDLE))
    elif run == "y":
        p.append(ov.ruby_box(f"{name} handle lever", lx - 8, ly - 32, lz - 7, 16, 64, 14, color=C_HANDLE))
    else:
        p.append(ov.ruby_box(f"{name} handle lever", lx - 8, ly - 7, lz - 32, 16, 14, 64, color=C_HANDLE))
    return "\n".join(p)


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


def tote_restraint():
    """Front retaining bars (trap the direct-stacked totes against the side/end walls) + the
    exterior wall anchor plates — ported from ov.ibc_rack (dropped when the deep box was
    forked).  Lives with the IBC stack, not the pump frame."""
    p = []
    front_x = ov.IBC_COL_X - 20            # 4654 — bars in the gap just in front of the tote face
    bar_d, bar_zs = 20, (560, 1760)        # 50×20×3 RHS bars, two tiers
    # Bars span the full width in two segments, clearing the central plumbing-corridor opening.
    for y0, y1 in ((0, YD_NEAR + S), (YD_FAR - S, ov.C_WID)):
        for bz in bar_zs:
            p.append(ov.ruby_box("Front Retaining Bar", front_x, y0, bz, bar_d, y1 - y0, S, color=ov.C_STEEL))
    # Wall joist hangers + exterior backing plates (4× M12 through-bolts) at each bar wall-end.
    ext_pt, ext_pw, ext_ph = 8, 100, 135
    for wall_yd, din in ((0, 1), (ov.C_WID, -1)):
        for bz in bar_zs:
            ht, dep = 4, 70
            p_y = wall_yd if din > 0 else wall_yd - ht
            s_y = wall_yd if din > 0 else wall_yd - dep
            p.append(ov.ruby_box("Wall Hanger Plate", front_x - 8, p_y, bz - 30, S + 16, ht, S + 70, color=ov.C_STEEL))
            p.append(ov.ruby_box("Wall Hanger Seat", front_x - 4, s_y, bz - ht, S + 8, dep, ht, color=ov.C_STEEL))
            ecx = front_x - 8 + (S + 16) / 2
            ecz = bz + S / 2
            plate_y = (-ov.WALL_T - ext_pt) if din > 0 else (ov.C_WID + ov.WALL_T)
            bolt_cy = (-ov.WALL_T - ext_pt) if din > 0 else (ov.C_WID - 10)
            p.append(ov.ruby_box("IBC Wall Backing Plate (ext)",
                                 ecx - ext_pw / 2, plate_y, ecz - ext_ph / 2, ext_pw, ext_pt, ext_ph, color=ov.C_STEEL))
            for dx in (-ext_pw / 2 + 18, ext_pw / 2 - 18):
                for dz in (-ext_ph / 2 + 22, ext_ph / 2 - 22):
                    p.append(ov.ruby_cylinder("IBC Wall Through-Bolt M12", ecx + dx, bolt_cy, ecz + dz, 7, 58,
                                              color=C_BOLT, axis="y"))
    return "\n".join(p)


def rear_panel():
    """The single 18mm marine-ply REAR panel, recessed into the back-wall opening (flush with
    the back posts' −X inside face), cut to the inside-of-frame opening."""
    pz0, ph = S, (TOP_Z - S) - S
    return ov.ruby_box("Rear panel (18mm marine ply)", BACK_X, YD_NEAR + S, pz0,
                       EQT, (YD_FAR - S) - (YD_NEAR + S), ph, color=ov.C_PLY)


# ── corridor-panel equipment placement (equipment hangs −X off the rear panel) ──
FACE_X = BACK_X                          # 5104 — rear-panel plane; equipment hangs −X toward the mouth
COL_L  = YD_NEAR + 63                    # 1109 — left (Brown-side) pump column
COL_R  = YD_FAR - 63                     # 1253 — right (Waste-side) pump column
CTR_Y  = (YD_NEAR + YD_FAR) / 2          # 1181 — corridor center
RP     = ov.PUMP_PIPE_OD / 2            # 1/2" pipe radius
PW, PH = 114, 200                        # pump body: X-depth, height
Z_PUMP = ov.PUMP_H_LO                    # 1370 — pump row
Z_ACC  = Z_PUMP + PH + 150               # 1720 — ACC-01 / Stage-A valve row
CDK    = "#3A3A42"                       # dark fittings / motor cans
DVB    = 46                              # diverter body cube
DVL    = 55                              # diverter port stub length


def _pump(nm, yd, z, color=None):
    """A Shurflo-style transfer pump hung −X off the panel (motor can + in/out nipples)."""
    color = color or ov.C_PUMP
    x0 = FACE_X - PW
    p = [ov.ruby_box(nm, x0, yd - 127 / 2, z, PW, 127, PH, color=color),
         ov.ruby_cylinder(nm + " motor", FACE_X - 34, yd, z + PH / 2, 44, 34, color=CDK, axis="x")]
    for tag, dz in (("in", 38), ("out", PH - 38)):
        p.append(ov.ruby_cylinder(f"{nm} {tag} port", x0 - 26, yd, z + dz, RP, 26, color=CDK, axis="x"))
    return p


def _pin(yd):  return (FACE_X - PW - 26, yd, Z_PUMP + 38)        # pump in-port tip
def _pout(yd): return (FACE_X - PW - 26, yd, Z_PUMP + PH - 38)   # pump out-port tip


def _side_entry(p, nm, x, yface, z, into, col):
    """Tote side-entry near the top, from the corridor: the 90° approach turn is 120mm
    BEFORE the flange (≥75mm), flange on the corridor face, 150mm penetration + elbow +
    150mm drop into the tote, with an anti-siphon check valve on the approach."""
    af  = yface - into * 120                # approach start, 120mm before the flange
    yin = yface + into * 150                # 150mm into the tote
    p.append(ov.ruby_pipe_run(nm + " entry", [(x, af, z), (x, yin, z), (x, yin, z - 150)], RP, color=col))
    p.append(ov.ruby_cylinder(nm + " flange", x, yface - into * 8, z, 36, 16, color=ov.C_STEEL, axis="y"))
    p.append(ov.ruby_box(nm + " check valve", x - 20, af - 18, z - 18, 40, 36, 40, color=ov.C_VALVE))
    return af


def equipment():
    """Active processing pumps + Stage-A diverter on the corridor plumbing panel:
    P-01 (Blue supply) + ACC-01, P-04 (tray-drain transfer), SV-02 sample tap, 3W-DV-02.
    (P-02 + the filters live on the pinhole wall; the P-03/P-05 drain pumps sit on the
    corridor drain risers — added separately.)"""
    p = []
    p += _pump("Pump P-01 (Blue supply)", COL_L, Z_PUMP, ov.C_PUMP)
    p += _pump("Pump P-04 (Tray drain)",  COL_R, Z_PUMP, ov.C_PUMP)
    p.append(ov.ruby_cylinder("ACC-01 Accumulator", FACE_X - 64, COL_L, Z_ACC, 127 / 2, 200, color=ov.C_ACC))
    # SV-02 sample tap (on the P-04 discharge) + downturned spout
    svx, sv_z = FACE_X - 60, Z_PUMP + PH + 20
    p.append(ov.ruby_box("SV-02 sample valve", svx - 25, COL_R - 25, sv_z, 50, 50, 64, color=ov.C_VALVE))
    p.append(ov.ruby_cylinder("SV-02 sample spout", svx, COL_R, sv_z - 90, 6, 90, color=ov.C_VALVE))
    # 3W-DV-02 — Stage-A diverter: input on the underside (from P-04/SV-02), through-run to
    # Brown(−Yd)/Waste(+Yd), red handle out of the panel (−X) toward the operator.
    p.append(diverter("3W-DV-02", FACE_X - 70, CTR_Y, Z_ACC, run="y", branch="z-", handle="x-", color=ov.C_VALVE))
    return "\n".join(p)


def plumbing():
    """Stage-A tray-drain chain (P-04 → SV-02 → 3W-DV-02 → IBC-3 Brown / IBC-4 Waste) plus
    the Blue supply (Blue #1 → P-01 → ACC-01 → trunk to the spray bar) — all orthogonal,
    kept inside the corridor / off the panel face."""
    p = []
    def pipe(nm, wp, col): p.append(ov.ruby_pipe_run(nm, wp, RP, color=col))
    dv_x, dv_z = FACE_X - 70, Z_ACC
    tip = DVB / 2 + DVL                                   # 78 — diverter port-stub tip offset
    svx, sv_z = FACE_X - 60, Z_PUMP + PH + 20
    xe = ov.IBC_COL_X + 300                              # 4974 — tote side-entry X station
    bz = ov.IBC_PALLET_H + ov.IBC_H_1000 - 60            # 1276 — near top of the lower (Brown/Waste) tote

    # P-04 suction ← processing-tray sump (hose exits the corridor mouth toward the optical zone)
    pipe("P-04 suction (from tray sump)",
         [_pin(COL_R), (FACE_X - PW - 200, COL_R, Z_PUMP + 38), (4500, CTR_Y, Z_PUMP + 38),
          (4500, CTR_Y, 320)], ov.C_IBC_BROWN)
    # P-04 discharge → SV-02 → DV-02 underside input
    pipe("P-04 -> SV-02 -> DV-02",
         [_pout(COL_R), (svx, COL_R, Z_PUMP + PH - 38), (svx, COL_R, sv_z),
          (svx, CTR_Y, sv_z), (dv_x, CTR_Y, dv_z - tip)], ov.C_IBC_BROWN)
    # DV-02 run− (−Yd) → IBC-3 Brown side-entry near the top (corridor face Yd1046)
    pipe("DV-02 -> IBC-3 (Brown)",
         [(dv_x, CTR_Y - tip, dv_z), (dv_x, YD_NEAR + 120, dv_z), (dv_x, YD_NEAR + 120, bz),
          (xe, YD_NEAR + 120, bz)], ov.C_IBC_BROWN)
    _side_entry(p, "IBC-3 (Brown)", xe, YD_NEAR, bz, -1, ov.C_IBC_BROWN)
    # DV-02 run+ (+Yd) → IBC-4 Waste side-entry near the top (corridor face Yd1316)
    pipe("DV-02 -> IBC-4 (Waste)",
         [(dv_x, CTR_Y + tip, dv_z), (dv_x, YD_FAR - 120, dv_z), (dv_x, YD_FAR - 120, bz),
          (xe, YD_FAR - 120, bz)], ov.C_IBC_WASTE)
    _side_entry(p, "IBC-4 (Waste)", xe, YD_FAR, bz, +1, ov.C_IBC_WASTE)

    # Blue supply: Blue #1 base outlet (near col top tote) → P-01 suction
    blz = ov.IBC_H_1000 + ov.IBC_PALLET_H + 64           # ~1400 — base of the upper Blue tote
    p.append(ov.ruby_cylinder("Blue #1 outlet flange", xe, YD_NEAR + 8, blz, 36, 16, color=ov.C_STEEL, axis="y"))
    pipe("Blue #1 -> P-01 suction",
         [(xe, YD_NEAR, blz), (xe, YD_NEAR + 120, blz), (FACE_X - PW - 26, YD_NEAR + 120, blz),
          (FACE_X - PW - 26, COL_L, blz), _pin(COL_L)], ov.C_BLUE)
    # P-01 discharge → ACC-01 → rigid trunk out the mouth toward the spray bar
    pipe("P-01 -> ACC-01",
         [_pout(COL_L), (FACE_X - 64, COL_L, Z_PUMP + PH - 38), (FACE_X - 64, COL_L, Z_ACC)], ov.C_BLUE)
    pipe("Blue supply trunk (-> spray bar)",
         [_pout(COL_L), (FACE_X - PW - 60, COL_L, Z_PUMP + PH - 38), (FACE_X - PW - 60, CTR_Y, Z_PUMP + PH - 38),
          (4500, CTR_Y, Z_PUMP + PH - 38), (4500, CTR_Y, 520)], ov.C_BLUE)
    return "\n".join(p)


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
             ov.component("Rear panel (ply)", "Rear Panel", rear_panel()),
             ov.component("Corridor equipment", "Equipment", equipment()),
             ov.component("Corridor plumbing", "Plumbing", plumbing())]
    body = "\n".join(comps)
    tags = ["IBC Stack", "Context", "Frame", "Rear Panel", "Equipment", "Plumbing"]
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
