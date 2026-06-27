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
CDK    = "#3A3A42"                       # dark fittings / motor cans
DVB    = 46                              # diverter body cube
DVL    = 55                              # diverter port stub length
C_CHECK = "#E8801C"                      # ORANGE — one-way / check valves (vs YELLOW diverters)
# Shurflo-2088-style pump (matches the wall P-02): a motor CAN + a head box, two ports out the
# head FRONT face (offset ±PORT_DZ in Z, OUT upper / IN lower).  All panel pumps conform to it.
PCAN_R, PCAN_L = 46, 150                 # motor can radius / length
PHW, PHD, PHH  = 70, 96, 112             # pump head box: X depth, Yd, Z
PORT_DZ = 36                             # port offset above/below the head center
Z_PMP   = 1400                           # pump head-center row
Z_ACC0  = 1860                           # ACC-01 BOTTOM — raised so the discharge plumbs into it
PX      = FACE_X - PHW - PCAN_L          # 4884 — pump head FRONT face (faces −X), motor butts panel


def pump_unit(nm, fx, fy, fz, face=1, color=None):
    """Shurflo-2088-style pump laid along X.  (fx,fy,fz)=head FRONT-face center; head faces
    +X (face=1, motor behind at −X) or −X (face=−1).  Two front-face ports offset ±PORT_DZ in
    Z.  Tips via pump_out()/pump_in() with the same (fx,fy,fz,face)."""
    color = color or ov.C_PUMP
    hx0 = fx - PHW if face > 0 else fx
    p = [ov.ruby_box(nm + " head", hx0, fy - PHD / 2, fz - PHH / 2, PHW, PHD, PHH, color=CDK)]
    mx = hx0 - PCAN_L if face > 0 else hx0 + PHW
    p.append(ov.ruby_cylinder(nm + " motor", mx, fy, fz, PCAN_R, PCAN_L, color=color, axis="x"))
    for tag, dz in (("out", +PORT_DZ), ("in", -PORT_DZ)):
        x0 = fx if face > 0 else fx - 30
        p.append(ov.ruby_cylinder(f"{nm} {tag} port", x0, fy, fz + dz, RP, 30, color=CDK, axis="x"))
    return p


def pump_out(fx, fy, fz, face=1): return (fx + face * 30, fy, fz + PORT_DZ)
def pump_in(fx, fy, fz, face=1):  return (fx + face * 30, fy, fz - PORT_DZ)


def _side_entry(p, nm, approach, x, yface, z, into, col, drop=-150):
    """Tote side-entry near the top, from the corridor.  `approach` = the FULL leg waypoint
    list UP TO the approach-turn point (x, af, z); this is concatenated with the in-tote
    penetration so the leg + entry is ONE pipe_run (every 90° gets a swept elbow).  Convention:
    the 90° approach turn is 120mm BEFORE the flange (≥75mm), flange on the corridor face,
    150mm penetration + elbow + 150mm vertical leg, ORANGE anti-siphon check valve on approach."""
    af  = yface - into * 120                # approach turn, 120mm before the flange
    yin = yface + into * 150                # 150mm penetration into the tote
    p.append(ov.ruby_pipe_run(nm + " entry", list(approach) + [(x, yin, z), (x, yin, z + drop)], RP, color=col))
    p.append(ov.ruby_cylinder(nm + " flange", x, yface - into * 8, z, 36, 16, color=ov.C_STEEL, axis="y"))
    p.append(ov.ruby_box(nm + " check valve", x - 20, af - 18, z - 18, 40, 36, 40, color=C_CHECK))
    return af


def equipment():
    """Active processing pumps + Stage-A diverter on the corridor plumbing panel:
    P-01 (Blue supply) + ACC-01, P-04 (tray-drain transfer), SV-02 sample tap, 3W-DV-02.
    (P-02 + the filters live on the pinhole wall; P-03/P-05 are in drains_ports().)"""
    p = []
    p += pump_unit("Pump P-01 (Blue supply)", PX, COL_L, Z_PMP, face=-1)
    p += pump_unit("Pump P-04 (Tray drain)",  PX, COL_R, Z_PMP, face=-1)
    # ACC-01 — raised so the P-01 discharge plumbs up into its base
    p.append(ov.ruby_cylinder("ACC-01 Accumulator", FACE_X - 64, COL_L, Z_ACC0, 127 / 2, 200, color=ov.C_ACC))
    # SV-02 sample tap (on the P-04 discharge riser) + downturned spout
    svx, sv_z = PX - 30, Z_PMP + 220
    p.append(ov.ruby_box("SV-02 sample valve", svx - 25, COL_R - 25, sv_z, 50, 50, 60, color=ov.C_VALVE))
    p.append(ov.ruby_cylinder("SV-02 sample spout", svx, COL_R, sv_z - 90, 6, 90, color=ov.C_VALVE))
    # 3W-DV-02 — Stage-A diverter (input underside from P-04/SV-02; run to Brown −Yd / Waste +Yd;
    # red handle out the panel −X toward the operator).
    p.append(diverter("3W-DV-02", PX + 20, CTR_Y, Z_PMP + 320, run="y", branch="z-", handle="x-", color=ov.C_VALVE))
    return "\n".join(p)


def plumbing():
    """Stage-A tray-drain chain (P-04 → SV-02 → 3W-DV-02 → IBC-3 Brown / IBC-4 Waste) plus
    the Blue supply (Blue #1 → P-01 → ACC-01 → trunk to the spray bar)."""
    p = []
    def pipe(nm, wp, col): p.append(ov.ruby_pipe_run(nm, wp, RP, color=col))
    p4o, p4i = pump_out(PX, COL_R, Z_PMP, -1), pump_in(PX, COL_R, Z_PMP, -1)
    p1o, p1i = pump_out(PX, COL_L, Z_PMP, -1), pump_in(PX, COL_L, Z_PMP, -1)
    portx = PX - 30                                      # 4854 — pump-port tip X
    svx, sv_z = portx, Z_PMP + 220
    dvx, dv_z = PX + 20, Z_PMP + 320
    tip = DVB / 2 + DVL                                  # 78
    xe = ov.IBC_COL_X + 300                              # 4974 — tote side-entry X station
    bz = ov.IBC_PALLET_H + ov.IBC_H_1000 - 60            # 1276 — near top of the lower (Brown/Waste) tote

    # P-04 suction ← processing-tray sump (hose exits the corridor mouth toward the optical zone)
    pipe("P-04 suction (from tray sump)",
         [p4i, (portx, COL_R, 1300), (4500, CTR_Y, 1300), (4500, CTR_Y, 320)], ov.C_IBC_BROWN)
    # P-04 discharge → SV-02 → DV-02 underside input
    pipe("P-04 -> SV-02 -> DV-02",
         [p4o, (svx, COL_R, sv_z), (svx, CTR_Y, sv_z), (dvx, CTR_Y, sv_z), (dvx, CTR_Y, dv_z - tip)],
         ov.C_IBC_BROWN)
    # DV-02 → IBC-3 Brown / IBC-4 Waste side-entries near the top (one continuous run each)
    _side_entry(p, "DV-02 -> IBC-3 (Brown)",
                [(dvx, CTR_Y - tip, dv_z), (dvx, YD_NEAR + 120, dv_z), (dvx, YD_NEAR + 120, bz), (xe, YD_NEAR + 120, bz)],
                xe, YD_NEAR, bz, -1, ov.C_IBC_BROWN)
    _side_entry(p, "DV-02 -> IBC-4 (Waste)",
                [(dvx, CTR_Y + tip, dv_z), (dvx, YD_FAR - 120, dv_z), (dvx, YD_FAR - 120, bz), (xe, YD_FAR - 120, bz)],
                xe, YD_FAR, bz, +1, ov.C_IBC_WASTE)

    # Blue supply: Blue #1 side-entry near the top → P-01 suction (one continuous run)
    blz = ov.IBC_H_1000 + ov.IBC_PALLET_H + 64           # ~1400 — upper Blue tote, near top
    _side_entry(p, "Blue #1 -> P-01 suction",
                [p1i, (portx, COL_L, blz), (portx, YD_NEAR + 120, blz), (xe, YD_NEAR + 120, blz)],
                xe, YD_NEAR, blz, -1, ov.C_BLUE)
    # P-01 discharge → up clear of the pump → into the raised ACC-01 base; supply trunk tees off
    accx = FACE_X - 64
    pipe("P-01 -> ACC-01", [p1o, (portx, COL_L, Z_ACC0), (accx, COL_L, Z_ACC0)], ov.C_BLUE)
    pipe("Blue supply trunk (-> spray bar)",
         [p1o, (4500, COL_L, Z_PMP + PORT_DZ), (4500, CTR_Y, Z_PMP + PORT_DZ), (4500, CTR_Y, 520)], ov.C_BLUE)
    return "\n".join(p)


def drains_ports():
    """The two waste-evacuation pumps (P-05 Brown / P-03 Waste) on the corridor drain risers,
    the X1/X3/X4 end-wall bulkhead ports, and the X1 fresh-fill tee to BOTH Blue totes."""
    p = []
    def pipe(nm, wp, col): p.append(ov.ruby_pipe_run(nm, wp, RP, color=col))
    ew = ov.C_LEN                                        # 5893 — sealed end wall (X-ports live here)
    p.append(ov.ruby_box("End wall (context)", ew, 0, 0, ov.WALL_T, ov.C_WID, ov.C_HGT, color=ov.C_SHELL, alpha=0.12))

    # ── X1 FILL (fresh, Blue): 2" camlock at the end-wall centerline (Z2250) → tee → BOTH Blue
    #    totes (each side-enters its corridor face near the top) ──
    x1z, tx = 2250, 5500
    p.append(ov.ruby_cylinder("X1 fill camlock (end wall)", ew - 60, CTR_Y, x1z, 26, 60, color=C_CHECK, axis="x"))
    p.append(ov.ruby_box("X1 fill tee", tx - 16, CTR_Y - 16, x1z - 16, 32, 32, 32, color=ov.C_STEEL))
    pipe("X1 -> fill tee", [(ew - 60, CTR_Y, x1z), (tx + 16, CTR_Y, x1z)], ov.C_BLUE)
    for yface, into, nm in ((YD_NEAR, -1, "Blue #1"), (YD_FAR, +1, "Blue #2")):
        _side_entry(p, f"X1 fill -> {nm}",
                    [(tx, CTR_Y, x1z), (tx, yface - into * 120, x1z), (5200, yface - into * 120, x1z)],
                    5200, yface, x1z, into, ov.C_BLUE)

    # ── X3 / X4 DRAIN risers (corridor gap) + P-05 / P-03 up to the end-wall ports ──
    for nm, pump, rx, ry, col, yface, into in (
            ("X3 Brown", "P-05", 5400, COL_L, ov.C_IBC_BROWN, YD_NEAR, -1),
            ("X4 Waste", "P-03", 5340, COL_R, ov.C_IBC_WASTE, YD_FAR,  +1)):
        botz, port_z = ov.IBC_PALLET_H + 90, 1700        # tote-base pickup / end-wall port height
        yin = yface + into * 150                          # 150mm penetration into the tote
        # tote pickup: 150mm dip + elbow inside, out through the flange, elbow to the riser
        pipe(f"{nm} pickup", [(rx, yin, botz + 120), (rx, yin, botz), (rx, ry, botz)], col)
        p.append(ov.ruby_cylinder(f"{nm} pickup flange", rx, yface - into * 8, botz, 30, 16, color=ov.C_STEEL, axis="y"))
        p.append(ov.ruby_box(f"{nm} pickup check valve", rx - 20, (yface + into * 70) - 18, botz - 18, 40, 36, 40, color=C_CHECK))
        # vertical drain riser + the Shurflo pump on it (faces −X toward the operator)
        p.append(ov.ruby_cylinder(f"{nm} drain riser", rx, ry, botz, RP, port_z - botz, color=col, axis="z"))
        p += pump_unit(f"Pump {pump} ({nm} drain)", rx - 20, ry, 940, face=-1)
        # end-wall drain port (camlock) + riser-top run to it
        p.append(ov.ruby_cylinder(f"{nm} drain port (end wall)", ew - 60, ry, port_z, 22, 60, color=C_CHECK, axis="x"))
        pipe(f"{nm} riser -> end-wall port", [(rx, ry, port_z), (ew - 60, ry, port_z)], col)
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
             ov.component("Corridor plumbing", "Plumbing", plumbing()),
             ov.component("Corridor drains + X-ports", "Drains", drains_ports())]
    body = "\n".join(comps)
    tags = ["IBC Stack", "Context", "Frame", "Rear Panel", "Equipment", "Plumbing", "Drains"]
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
