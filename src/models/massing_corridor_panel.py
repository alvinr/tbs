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
C_CHECK = "#8A2BE2"                      # PURPLE — one-way / check valves (vs YELLOW diverters)
# UPRIGHT pump (filter-style): a vertical body + cap with BOTH ports out the TOP, exiting along
# ±X (face dir), offset ±26 in Yd (OUT +Yd, IN −Yd).  All pumps (incl. the wall P-02) conform.
PVB_R, PVB_H, PCAP_H = 50, 180, 30       # vertical body radius / height, head/cap height
PXC     = FACE_X - 120                    # 4984 — pump body center X (upright, in front of the panel)
Z_ACC0  = 1380                            # ACC-01 BOTTOM
MERGE4  = (ov.IBC_COL_X + 300, YD_FAR - 200, ov.IBC_PALLET_H + ov.IBC_H_1000 - 106)  # (4974,1116,1230)
                                          # shared IBC-4 waste merge: DV-01 (wall) + DV-02 join here,
                                          # then ONE pipe enters the tote (Z below the Brown entry)


def pump_unit(nm, cx, cy, cz0, face=-1, color=None):
    """UPRIGHT pump (like the filters): vertical body + cap, two ports out the TOP exiting along
    ±X (face dir), offset ±26 in Yd (OUT +Yd, IN −Yd).  cz0 = body base Z.  Port tips via
    pump_out()/pump_in() with the same (cx,cy,cz0,face)."""
    color = color or ov.C_PUMP
    top = cz0 + PVB_H
    p = [ov.ruby_cylinder(nm + " body", cx, cy, cz0, PVB_R, PVB_H, color=color, axis="z"),
         ov.ruby_cylinder(nm + " head", cx, cy, top, PVB_R + 3, PCAP_H, color=CDK, axis="z")]
    pz = top + PCAP_H / 2
    for tag, dy in (("out", +26), ("in", -26)):
        x0 = cx + PVB_R if face > 0 else cx - PVB_R - 30
        p.append(ov.ruby_cylinder(f"{nm} {tag} port", x0, cy + dy, pz, RP, 30, color=CDK, axis="x"))
    return p


def pump_out(cx, cy, cz0, face=-1): return (cx + face * (PVB_R + 30), cy + 26, cz0 + PVB_H + PCAP_H / 2)
def pump_in(cx, cy, cz0, face=-1):  return (cx + face * (PVB_R + 30), cy - 26, cz0 + PVB_H + PCAP_H / 2)


def _side_entry(p, nm, approach, x, yface, z, into, col, drop=-150, check=True):
    """Tote side-entry near the top, from the corridor.  `approach` = the FULL leg waypoint
    list UP TO the approach-turn point (x, af, z); this is concatenated with the in-tote
    penetration so the leg + entry is ONE pipe_run (every 90° gets a swept elbow).  Convention:
    the 90° approach turn is 120mm BEFORE the flange (≥75mm), flange on the corridor face,
    150mm penetration + elbow + 150mm vertical leg, ORANGE anti-siphon check valve on approach
    (unless `check=False` — e.g. when a single shared check sits upstream of a fill tee)."""
    af  = yface - into * 120                # approach turn, 120mm before the flange
    yin = yface + into * 150                # 150mm penetration into the tote
    p.append(ov.ruby_pipe_run(nm + " entry", list(approach) + [(x, yin, z), (x, yin, z + drop)], RP, color=col))
    p.append(ov.ruby_cylinder(nm + " flange", x, yface - into * 8, z, 36, 16, color=ov.C_STEEL, axis="y"))
    if check:
        p.append(ov.ruby_box(nm + " check valve", x - 20, af - 18, z - 18, 40, 36, 40, color=C_CHECK))
    return af


def _bottom_pickup(p, nm, x, yface, into, col, riser_path):
    """Tote BOTTOM pickup: penetrate the corridor face near the base, the 90° bend points DOWN to
    the FLOOR (dip tube), then back up through the flange and along `riser_path` to the pump inlet
    — ONE pipe_run (elbows everywhere).  Flange + ORANGE check valve."""
    z0  = ov.IBC_PALLET_H + 90              # base pickup level
    yin = yface + into * 150                # 150mm penetration into the tote
    wps = [(x, yin, 40), (x, yin, z0), (x, yface - into * 120, z0)] + list(riser_path)
    p.append(ov.ruby_pipe_run(nm + " pickup", wps, RP, color=col))
    p.append(ov.ruby_cylinder(nm + " pickup flange", x, yface - into * 8, z0, 36, 16, color=ov.C_STEEL, axis="y"))
    p.append(ov.ruby_box(nm + " pickup check valve", x - 20, (yface - into * 120) - 18, z0 - 18, 40, 36, 40, color=C_CHECK))


# Pump rows + key fittings on the panel (UPRIGHT pumps; ports at the top, face −X)
R1, R2 = 300, 560                         # pump base rows (low — knee/shin height)
ACCX   = FACE_X - 90                       # 5014 — ACC-01 center X
SVX    = PXC - PVB_R - 70                  # 4864 — SV-02 / DV-02 stand in front of the pumps
DVZ    = 1180                              # 3W-DV-02 center Z


def equipment():
    """The four processing pumps (P-01 Blue, P-04 tray-drain, P-05 Brown-drain, P-03 Waste-drain),
    ACC-01, SV-02 sample tap and 3W-DV-02 — all on the corridor plumbing panel.  (P-02 + the
    filters live on the pinhole wall.)  Pumps are UPRIGHT (filter-style), ports out the top."""
    p = []
    p += pump_unit("Pump P-01 (Blue supply)", PXC, COL_L, R1)
    p += pump_unit("Pump P-04 (Tray drain)",  PXC, COL_R, R1)
    p += pump_unit("Pump P-05 (Brown drain)", PXC, COL_L, R2)
    p += pump_unit("Pump P-03 (Waste drain)", PXC, COL_R, R2)
    p.append(ov.ruby_cylinder("ACC-01 Accumulator", ACCX, COL_L, Z_ACC0, 127 / 2, 200, color=ov.C_ACC))
    # SV-02 sample tap (on the P-04 discharge) + downturned spout
    p.append(ov.ruby_box("SV-02 sample valve", SVX - 25, COL_R - 25, 1000, 50, 50, 60, color=ov.C_VALVE))
    p.append(ov.ruby_cylinder("SV-02 sample spout", SVX, COL_R, 1000 - 90, 6, 90, color=ov.C_VALVE))
    # 3W-DV-02 — Stage-A diverter (input underside from P-04/SV-02; run to Brown −Yd / Waste +Yd;
    # red handle out the panel −X toward the operator).
    p.append(diverter("3W-DV-02", SVX + 20, CTR_Y, DVZ, run="y", branch="z-", handle="x-", color=ov.C_VALVE))
    return "\n".join(p)


def plumbing():
    """Stage-A tray-drain chain (P-04 → SV-02 → 3W-DV-02 → IBC-3 Brown / IBC-4 Waste) + the Blue
    supply (Blue #1 → P-01 → ACC-01 → trunk).  Routing rules: every segment is single-axis (no
    diagonals); each pump port leaves with a perpendicular −X stub; each run gets its OWN X depth
    lane so pipes never share a plane (no pipe-through-pipe); horizontal runs sit at Z levels
    clear of the pump bodies (tops ≤ 770)."""
    p = []
    def pipe(nm, wp, col): p.append(ov.ruby_pipe_run(nm, wp, RP, color=col))
    p1o, p1i = pump_out(PXC, COL_L, R1), pump_in(PXC, COL_L, R1)
    p4o, p4i = pump_out(PXC, COL_R, R1), pump_in(PXC, COL_R, R1)
    tip = DVB / 2 + DVL                                  # 78 — diverter port-stub tip
    dvx = SVX + 20                                        # 4884 — DV-02 X
    dvm, dvp = CTR_Y - tip, CTR_Y + tip                  # 1103 / 1259 — DV-02 run−/run+ Yd
    xe  = ov.IBC_COL_X + 300                             # 4974 — tote side-entry X
    bz  = ov.IBC_PALLET_H + ov.IBC_H_1000 - 60           # 1276 — Brown near-top entry
    wz  = MERGE4[2]                                       # 1230 — Waste entry (below Brown, no clash)
    blz = ov.IBC_H_1000 + ov.IBC_PALLET_H + 64           # 1400 — Blue near top
    GAP = 1166                                            # Yd lane in the gap BETWEEN the pump columns

    # P-04 SUCTION ← tray sump  (lane 4760): −X stub, down, out the corridor mouth
    pipe("P-04 suction (from tray sump)",
         [p4i, (4760, 1227, 495), (4760, 1227, 360), (4500, 1227, 360), (4500, CTR_Y, 360), (4500, CTR_Y, 300)],
         ov.C_IBC_BROWN)
    # P-04 DISCHARGE → SV-02 → DV-02 underside branch  (riser in the SV-02 plane, X4864)
    pipe("P-04 -> SV-02 -> DV-02",
         [p4o, (SVX, 1279, 495), (SVX, 1279, 1000), (SVX, COL_R, 1000), (SVX, CTR_Y, 1000),
          (dvx, CTR_Y, 1000), (dvx, CTR_Y, DVZ - tip)], ov.C_IBC_BROWN)
    # DV-02 → IBC-3 Brown  (run− port at dvm → up → across to xe → penetrate)
    _side_entry(p, "DV-02 -> IBC-3 (Brown)",
                [(dvx, dvm, DVZ), (dvx, dvm, bz), (xe, dvm, bz)], xe, YD_NEAR, bz, -1, ov.C_IBC_BROWN)
    # DV-02 → SHARED IBC-4 merge  (run+ port at dvp; DV-01 from the wall joins here → one entry)
    pipe("DV-02 -> IBC-4 merge",
         [(dvx, dvp, DVZ), (dvx, dvp, wz), (MERGE4[0], dvp, wz), (MERGE4[0], MERGE4[1], wz)], ov.C_IBC_WASTE)
    p.append(ov.ruby_box("IBC-4 waste merge tee", MERGE4[0] - 16, MERGE4[1] - 16, MERGE4[2] - 16, 32, 32, 32, color=ov.C_STEEL))
    _side_entry(p, "IBC-4 (Waste)", [MERGE4, (xe, YD_FAR - 120, wz)], xe, YD_FAR, wz, +1, ov.C_IBC_WASTE)

    # BLUE #1 → P-01 suction  (lane 4830)
    _side_entry(p, "Blue #1 -> P-01 suction",
                [p1i, (4830, 1083, 495), (4830, 1083, blz), (4830, GAP, blz), (xe, GAP, blz)],
                xe, YD_NEAR, blz, -1, ov.C_BLUE)
    # P-01 → ACC-01 IN  (lane 4890 up, then +X over the pumps into the ACC base; 150 drop)
    aci = Z_ACC0 - 150                                    # 1230 — ACC IN turn (150 below the tank)
    pipe("P-01 -> ACC-01 (in)",
         [p1o, (4890, 1135, 495), (4890, 1135, aci), (ACCX, 1135, aci), (ACCX, COL_L - 22, aci), (ACCX, COL_L - 22, Z_ACC0)],
         ov.C_BLUE)
    # ACC-01 OUT → supply trunk  (260 drop before turning, lane 4810, out the mouth)
    aco = Z_ACC0 - 260                                    # 1120 — ACC OUT turn (clear of the IN at 1230)
    pipe("ACC-01 -> Blue supply trunk (-> spray bar)",
         [(ACCX, COL_L + 22, Z_ACC0), (ACCX, COL_L + 22, aco), (4810, COL_L + 22, aco),
          (4810, CTR_Y, aco), (4810, CTR_Y, 300), (4500, CTR_Y, 300)], ov.C_BLUE)
    return "\n".join(p)


def end_wall():
    """Faint sealed END WALL slice (X-ports live on it).  Built on the Context layer so it does
    NOT clutter the pipes-only 'Plumbing' scene."""
    return ov.ruby_box("End wall (context)", ov.C_LEN, 0, 0, ov.WALL_T, ov.C_WID, ov.C_HGT,
                       color=ov.C_SHELL, alpha=0.12)


def drains_ports():
    """The X1/X3/X4 end-wall bulkhead ports + their lines: X1 fresh-fill (single check → tee →
    BOTH Blue totes) and the X3/X4 drains (tote-bottom pickups → panel pumps P-05/P-03 → ports).
    The pumps themselves are on the panel (equipment())."""
    p = []
    def pipe(nm, wp, col): p.append(ov.ruby_pipe_run(nm, wp, RP, color=col))
    ew = ov.C_LEN                                        # 5893 — end wall

    # ── X1 FILL: camlock → SINGLE one-way valve → tee → BOTH Blue totes (no per-branch checks) ──
    x1z, tx = 2250, 5500
    p.append(ov.ruby_cylinder("X1 fill camlock (end wall)", ew - 60, CTR_Y, x1z, 26, 60, color=ov.C_STEEL, axis="x"))
    p.append(ov.ruby_box("X1 one-way valve", tx + 70 - 20, CTR_Y - 20, x1z - 18, 44, 40, 40, color=C_CHECK))
    p.append(ov.ruby_box("X1 fill tee", tx - 16, CTR_Y - 16, x1z - 16, 32, 32, 32, color=ov.C_STEEL))
    pipe("X1 -> one-way -> tee", [(ew - 60, CTR_Y, x1z), (tx + 16, CTR_Y, x1z)], ov.C_BLUE)
    for yface, into, nm in ((YD_NEAR, -1, "Blue #1"), (YD_FAR, +1, "Blue #2")):
        _side_entry(p, f"X1 fill -> {nm}",
                    [(tx, CTR_Y, x1z), (tx, yface - into * 120, x1z), (5200, yface - into * 120, x1z)],
                    5200, yface, x1z, into, ov.C_BLUE, check=False)

    # ── X3 / X4 DRAINS: tote-BOTTOM pickup (bend points DOWN to floor) → panel pump → end port.
    #    Single-axis segments; pickup risers + discharges each on their own X depth lane. ──
    for nm, col, yface, into, pcy, port_z, lane, riser in (
            ("X3 Brown (P-05)", ov.C_IBC_BROWN, YD_NEAR, -1, COL_L, 1700, 4740, 5240),
            ("X4 Waste (P-03)", ov.C_IBC_WASTE, YD_FAR,  +1, COL_R, 1620, 4720, 5200)):
        pin  = pump_in(PXC, pcy, R2)                     # drain-pump inlet (top of P-05/P-03)
        pout = pump_out(PXC, pcy, R2)                    # drain-pump outlet
        z0   = ov.IBC_PALLET_H + 90                      # base pickup level
        ay   = yface - into * 120                        # corridor approach Yd, 120mm off the face
        # bottom pickup: dip to the floor + elbow, out the flange, up the riser, into the pump inlet
        _bottom_pickup(p, nm, riser, yface, into, col,
                       [(riser, ay, 760), (pin[0], ay, 760), (pin[0], pin[1], 760), pin])
        # pump discharge → −X stub → up → +X over the panel to the end-wall drain port (camlock)
        p.append(ov.ruby_cylinder(f"{nm} drain port (end wall)", ew - 60, pcy, port_z, 22, 60, color=C_CHECK, axis="x"))
        pipe(f"{nm} -> end-wall port", [pout, (lane, pout[1], 755), (lane, pout[1], port_z), (ew - 60, pout[1], port_z), (ew - 60, pcy, port_z)], col)
    return "\n".join(p)


def context():
    """Ghost of the IBC stack + a floor slice so the corridor frame reads in place."""
    p = []
    p.append(ov.component("IBC Stack", "IBC Stack", ov.ibc_stack(alpha=0.20)))
    x0 = 4300
    p.append(ov.component("Floor (context)", "Context",
             ov.ruby_box("Floor", x0, 0, -ov.WALL_T, ov.C_LEN - x0, ov.C_WID, ov.WALL_T, color=ov.C_SHELL, alpha=0.16)))
    p.append(ov.component("End wall (context)", "Context", end_wall()))
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
