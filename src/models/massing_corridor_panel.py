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


def diverter(name, cx, cy, cz, run="x", branch="z-", handle="y+", color=None, L=10, r=13):
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
DVL    = 10                              # diverter port socket length — real 1/2" socket 3-way ball valve
#   is 2.62"/66.5mm overall (US Plastics #30667), i.e. ports reach only ~33mm from center (DVB/2+DVL)
C_CHECK = "#8A2BE2"                      # PURPLE — one-way / check valves (vs YELLOW diverters)
# UPRIGHT pump (filter-style): a vertical body + cap with BOTH ports out the TOP, exiting along
# ±X (face dir), offset ±26 in Yd (OUT +Yd, IN −Yd).  All pumps (incl. the wall P-02) conform.
PVB_R, PVB_H, PCAP_H = 50, 180, 30       # vertical body radius / height, head/cap height
PXC     = FACE_X - 120                    # 4984 — pump body center X (upright, in front of the panel)
Z_ACC0  = 1780                            # ACC-01 BOTTOM — raised clear of the pipe runs below it
MERGE4  = (ov.IBC_COL_X + 730, YD_FAR - 200, ov.IBC_PALLET_H + ov.IBC_H_1000 - 106)  # (5404,1116,1230) — +130 toward sealed end
                                          # shared IBC-4 waste merge — moved BACK toward the sealed
                                          # end (behind the pumps/panel), so the grey riser clears
                                          # the pumps.  DV-01 (wall) + DV-02 join here → one entry.
GAPX  = ov.PROC_TRAY_X_R + 12             # 4641 — in the gap between the tray right edge (4629) and the
                                          # frame upright (4654): the ONLY place to cross between the
                                          # outside-rim strip (Yd<80) and the corridor (Rule 5a, around the
                                          # tray).  Cross HORIZONTALLY here at a z clear of the FP rail (z510).
TRAY_STRIP_Y = 60                         # outside the tray near rim (Yd80): the around-the-rim run lane
GAP_CORR_Y = 1150                         # corridor-side approach Yd — clear of the front upright (Yd1046–1096)
BROWN_TAP = (4880, CTR_Y - (PVB_R + 30), ov.IBC_PALLET_H + 90)   # (4880,1101,258) — the SINGLE shared
                                          # IBC-3 bottom tap T: run ALONG X (P-02 leaves −X to the
                                          # wall, P-05 leaves +X to the pump), dip on the −Yd branch.
                                          # Feeds BOTH P-02 (wall loop) and P-05 → one tote penetration.


def pump_unit(nm, cx, cy, cz0, axis="x", face=1, color=None):
    """UPRIGHT pump with IN and OUT on OPPOSITE sides near the top — the same pattern as the
    filters (straight-through).  `axis` = the port line ("x": ports along ±X; "y": along ±Yd);
    `face` = the sign of the OUT side (+1 → OUT on +axis / IN on −axis; −1 flips).  Tips via
    pump_in()/pump_out()."""
    color = color or ov.C_PUMP
    top = cz0 + PVB_H
    p = [ov.ruby_cylinder(nm + " body", cx, cy, cz0, PVB_R, PVB_H, color=color, axis="z"),
         ov.ruby_cylinder(nm + " head", cx, cy, top, PVB_R + 3, PCAP_H, color=CDK, axis="z")]
    pz = top - 18                                # ports near the top (like the filter cap ports)
    for tag, sd in (("in", -face), ("out", face)):
        if axis == "x":
            x0 = (cx + PVB_R) if sd > 0 else (cx - PVB_R - 30)
            p.append(ov.ruby_cylinder(f"{nm} {tag} port", x0, cy, pz, RP, 30, color=CDK, axis="x"))
        else:
            y0 = (cy + PVB_R) if sd > 0 else (cy - PVB_R - 30)
            p.append(ov.ruby_cylinder(f"{nm} {tag} port", cx, y0, pz, RP, 30, color=CDK, axis="y"))
    return p


def pump_out(cx, cy, cz0, axis="x", face=1):
    pz = cz0 + PVB_H - 18
    return (cx + face * (PVB_R + 30), cy, pz) if axis == "x" else (cx, cy + face * (PVB_R + 30), pz)
def pump_in(cx, cy, cz0, axis="x", face=1):
    pz = cz0 + PVB_H - 18
    return (cx - face * (PVB_R + 30), cy, pz) if axis == "x" else (cx, cy - face * (PVB_R + 30), pz)


def tee(nm, cx, cy, cz, run="x", branch="z-", color=None):
    """Pipe TEE / T-connector fitting (socket × socket × socket, e.g. a Sch-40 PVC tee): a straight
    RUN (two collinear ports along `run`) + a perpendicular BRANCH (`branch` = axis+sign), one
    fitting body fatter than the pipe, with a raised SOCKET CUFF at each of the 3 ends.  Centered
    on the run/branch intersection (cx,cy,cz)."""
    color = color or "#9AA0A8"            # neutral fitting grey (PVC)
    br, cr, cl = RP + 5, RP + 9, 12       # body radius, socket-cuff radius, cuff length
    half, bl = 30, 36                     # run half-length, branch reach
    ba, bs = branch[0], (1 if "+" in branch else -1)
    p = []
    # RUN body (centered, both ways) + BRANCH body (centre outward)
    run0 = {"x": (cx - half, cy, cz), "y": (cx, cy - half, cz), "z": (cx, cy, cz - half)}[run]
    p.append(ov.ruby_cylinder(nm + " run", run0[0], run0[1], run0[2], br, 2 * half, color=color, axis=run))
    brn0 = {"x": ((cx if bs > 0 else cx - bl), cy, cz),
            "y": (cx, (cy if bs > 0 else cy - bl), cz),
            "z": (cx, cy, (cz if bs > 0 else cz - bl))}[ba]
    p.append(ov.ruby_cylinder(nm + " branch", brn0[0], brn0[1], brn0[2], br, bl, color=color, axis=ba))
    # SOCKET CUFFS at the 3 ends (raised bell sockets the pipe inserts into)
    ends = {"x": [(cx - half, cy, cz, "x"), (cx + half - cl, cy, cz, "x")],
            "y": [(cx, cy - half, cz, "y"), (cx, cy + half - cl, cz, "y")],
            "z": [(cx, cy, cz - half, "z"), (cx, cy, cz + half - cl, "z")]}[run]
    bend = {"x": ((cx + bl - cl) if bs > 0 else (cx - bl), cy, cz, "x"),
            "y": (cx, (cy + bl - cl) if bs > 0 else (cy - bl), cz, "y"),
            "z": (cx, cy, (cz + bl - cl) if bs > 0 else (cz - bl), "z")}[ba]
    for ex, ey, ez, ax in ends + [bend]:
        p.append(ov.ruby_cylinder(nm + " socket cuff", ex, ey, ez, cr, cl, color=color, axis=ax))
    return "\n".join(p)


def check_valve(nm, px, py, pz, axis, color=None):
    """In-line one-way / check valve: a short barrel the pipe runs THROUGH, centered on the pipe
    centerline (px,py,pz) and oriented ALONG the run (`axis`).  Check valves are IN-LINE devices —
    they sit on a STRAIGHT length of pipe, never straddling an elbow."""
    color = color or C_CHECK
    L, r = 48, RP + 7
    if axis == "x": return ov.ruby_cylinder(nm, px - L / 2, py, pz, r, L, color=color, axis="x")
    if axis == "y": return ov.ruby_cylinder(nm, px, py - L / 2, pz, r, L, color=color, axis="y")
    return ov.ruby_cylinder(nm, px, py, pz - L / 2, r, L, color=color, axis="z")


C_BV = "#7A8088"                              # ball-valve body — chrome/steel grey (distinct from
                                              # PURPLE check valves and YELLOW diverters)


def ball_valve(nm, px, py, pz, axis, color=None, hdir="+y"):
    """In-line MANUAL ball valve: a short barrel the pipe runs THROUGH (centered on the pipe
    centerline, oriented ALONG `axis`) plus a clear RED lever handle — a stem out perpendicular
    to the run with a lever bar at its tip (like the diverter handles) so it reads as a hand
    valve.  Like a check valve it sits on a STRAIGHT length of pipe, never on an elbow."""
    color = color or C_BV
    L, r = 44, RP + 8                          # barrel length / radius
    HS, HSr, LV = 28, 6, 48                    # handle stem length / radius, lever-bar length
    p = []
    if axis == "x":                            # horizontal barrel along X — handle sticks UP (+Z)
        p.append(ov.ruby_cylinder(nm, px - L / 2, py, pz, r, L, color=color, axis="x"))
        p.append(ov.ruby_cylinder(nm + " handle stem", px, py, pz + r, HSr, HS, color=C_HANDLE, axis="z"))
        p.append(ov.ruby_box(nm + " handle", px - LV / 2, py - 7, pz + r + HS, LV, 14, 9, color=C_HANDLE))
    elif axis == "y":                          # horizontal barrel along Yd — handle sticks UP (+Z)
        p.append(ov.ruby_cylinder(nm, px, py - L / 2, pz, r, L, color=color, axis="y"))
        p.append(ov.ruby_cylinder(nm + " handle stem", px, py, pz + r, HSr, HS, color=C_HANDLE, axis="z"))
        p.append(ov.ruby_box(nm + " handle", px - 7, py - LV / 2, pz + r + HS, 14, LV, 9, color=C_HANDLE))
    else:                                      # vertical barrel — handle sticks out horizontally toward `hdir`
        p.append(ov.ruby_cylinder(nm, px, py, pz - L / 2, r, L, color=color, axis="z"))
        ux, uy = {"+y": (0, 1), "-y": (0, -1), "+x": (1, 0), "-x": (-1, 0)}[hdir]
        if uy:                                 # stem along Yd, lever a vertical bar at the tip
            p.append(ov.ruby_cylinder(nm + " handle stem", px, (py + r) if uy > 0 else (py - r - HS), pz, HSr, HS, color=C_HANDLE, axis="y"))
            p.append(ov.ruby_box(nm + " handle", px - 7, py + uy * (r + HS) - (0 if uy > 0 else 9), pz - LV / 2, 14, 9, LV, color=C_HANDLE))
        else:                                  # stem along X, lever a vertical bar at the tip
            p.append(ov.ruby_cylinder(nm + " handle stem", (px + r) if ux > 0 else (px - r - HS), py, pz, HSr, HS, color=C_HANDLE, axis="x"))
            p.append(ov.ruby_box(nm + " handle", px + ux * (r + HS) - (0 if ux > 0 else 9), py - 7, pz - LV / 2, 9, 14, LV, color=C_HANDLE))
    return "\n".join(p)


def sample_valve(nm, cx, cy, cz, h=60, color=None, spout="z-"):
    """Sample / test tap: a small valve body + a downturned sample spout + a RED HANDWHEEL on top
    (stem + flat disc) so it clearly reads as a valve.  `cz` = body base Z, `h` = body height.
    `spout`: "z-" drops straight down (default); an axis+sign like "-x" projects the spout OUT to that
    side then turns down — use it when the valve sits in-line on a vertical riser (so the spout clears
    the pipe and a cup fits under it)."""
    color = color or ov.C_VALVE
    p = [ov.ruby_box(nm, cx - 25, cy - 25, cz, 50, 50, h, color=color)]
    if spout == "z-":
        p.append(ov.ruby_cylinder(nm + " spout", cx, cy, cz - 90, 6, 90, color=color, axis="z"))
    else:                                  # project sideways (clear of an in-line riser) then turn DOWN
        sa = "x" if "x" in spout else ("y" if "y" in spout else "z")
        ss = -1 if "-" in spout else 1
        way = {"x": [(cx, cy, cz + 12), (cx + ss * 58, cy, cz + 12), (cx + ss * 58, cy, cz - 60)],
               "y": [(cx, cy, cz + 12), (cx, cy + ss * 58, cz + 12), (cx, cy + ss * 58, cz - 60)]}[sa]
        p.append(ov.ruby_pipe_run(nm + " spout", way, 6, color=color))
    p.append(ov.ruby_cylinder(nm + " handwheel stem", cx, cy, cz + h, 5, 16, color=C_HANDLE, axis="z"))
    p.append(ov.ruby_cylinder(nm + " handwheel", cx, cy, cz + h + 16, 30, 10, color=C_HANDLE, axis="z"))
    return "\n".join(p)


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
    if check:   # in-line on the straight Yd approach, just outside the flange
        p.append(check_valve(nm + " check valve", x, yface - into * 60, z, "y"))
    return af


def _bottom_pickup(p, nm, x, yface, into, col, riser_path):
    """Tote BOTTOM pickup: penetrate the corridor face near the base, the 90° bend points DOWN to
    the FLOOR (dip tube), then back up through the flange and along `riser_path` to the pump inlet
    — ONE pipe_run (elbows everywhere).  Flange (no foot valve — the pump self-primes and has an
    integral check valve, so a dedicated check here is redundant)."""
    z0  = ov.IBC_PALLET_H + 90              # base pickup level (just above the pallet)
    yin = yface + into * 150                # 150mm penetration into the tote
    # after the elbow inside the tote the dip tube descends only 50mm (a short standpipe), NOT to the floor
    wps = [(x, yin, z0 - 50), (x, yin, z0), (x, yface - into * 120, z0)] + list(riser_path)
    p.append(ov.ruby_pipe_run(nm + " pickup", wps, RP, color=col))
    p.append(ov.ruby_cylinder(nm + " pickup flange", x, yface - into * 8, z0, 36, 16, color=ov.C_STEEL, axis="y"))


# Pumps in a SINGLE vertical column (like the filter row) at (PXC, CTR_Y); IN −Yd / OUT +Yd.
# Order bottom → top: P-01, [ACC-01 dead-leg], P-04, P-05, P-03 (ACC sits above P-01).
PSTACK = {"P-01": 280, "P-04": 940, "P-05": 1340, "P-03": 1740}  # base Z
PIY, POY = CTR_Y - (PVB_R + 30), CTR_Y + (PVB_R + 30)            # 1101 (IN) / 1261 (OUT) manifold Yd
def _piz(key): return PSTACK[key] + PVB_H - 18                    # port Z for a stack key
# ── BACK-OF-PANEL routing: LONG vertical risers run BEHIND the rear panel (no pump ports there),
#    penetrating the ply; SHORT interconnects stay on the front.  Each long riser gets a UNIQUE Yd
#    lane, and the Yd-jog onto that lane is done on the FRONT (at x=PXC, unique z per port) BEFORE
#    penetrating, so the penetrations and the back verticals never share a plane. ──
BLANE = BACK_X + EQT + 60                                        # 5182 — back-of-panel riser plane
# Unique Yd lanes spread across the clear back band BETWEEN the corner uprights (near upright
# Yd1046–1096, far upright Yd1296–1346) → keep lanes inside ~1105–1285, ≥30mm apart:
BL_P01, BL_P05, BL_P04 = 1115, 1145, 1175                        # IN-side suction back-lanes
BL_P04OUT, BL_DVBR, BL_DVWST = 1195, 1225, 1250                  # OUT/top back-lanes (clear of far upright Yd1266)
SV_Z   = 2020                              # SV-02 (on the P-04 discharge, above the stack)
DV_Z   = 2220                              # 3W-DV-02 center Z — raised the max clean headroom UNDER the
#   frame top rail (z2246); a bigger raise (toward the requested +300) needs the feed/legs reworked to
#   thread the ring opening — they currently drop/rise at the ring edges (Yd1103/1259) and clip the rails
# ACC-01 — SeaFlo bladder accumulator: a single BOTTOM port, plumbed as a vertical DEAD-LEG teed
# onto the Blue supply line (like the pumps/filters tee in, but the tank's only port is underneath).
ACC_Z0, ACC_R = 540, 63.5                   # ACC-01 base Z (in the column, above P-01); Ø127 body
ACC_PZ = ACC_Z0 + 28                        # ACC-01 IN/OUT port Z — at the BOTTOM of the body (the
                                            # SeaFlo's ports are underneath); pump-shaped, ports low
def acc_in():  return (PXC, CTR_Y + ACC_R + 30, ACC_PZ)   # +Yd (from P-01 OUT)
def acc_out(): return (PXC, CTR_Y - ACC_R - 30, ACC_PZ)   # −Yd (to the supply trunk)


def equipment():
    """The four processing pumps (P-01 Blue, P-04 tray-drain, P-05 Brown-drain, P-03 Waste-drain),
    ACC-01, SV-02 sample tap and 3W-DV-02 — all on the corridor plumbing panel.  (P-02 + the
    filters live on the pinhole wall.)  Pumps are UPRIGHT (filter-style), ports out the top."""
    p = []
    for label, key in (("Pump P-01 (Blue supply)", "P-01"), ("Pump P-04 (Tray drain)", "P-04"),
                       ("Pump P-05 (Brown drain)", "P-05"), ("Pump P-03 (Waste drain)", "P-03")):
        p += pump_unit(label, PXC, CTR_Y, PSTACK[key], axis="y")
    # ACC-01 — SeaFlo SFAT-075-125-01 (0.75 L): Ø127 × 200mm overall (per component-dimension-audit).
    # Drawn like the filters/pumps: a vertical body with IN/OUT on OPPOSITE sides (IN +Yd from
    # P-01, OUT −Yd to the trunk), in line on the Blue supply.
    acc_h = 174                                  # body 174 + 26 cap = 200 overall (to spec)
    p.append(ov.ruby_cylinder("ACC-01 Accumulator", PXC, CTR_Y, ACC_Z0, ACC_R, acc_h, color=ov.C_ACC))
    p.append(ov.ruby_cylinder("ACC-01 head", PXC, CTR_Y, ACC_Z0 + acc_h, ACC_R + 2, 26, color=CDK, axis="z"))
    for tag, sd in (("in", +1), ("out", -1)):
        y0 = (CTR_Y + ACC_R) if sd > 0 else (CTR_Y - ACC_R - 30)
        p.append(ov.ruby_cylinder(f"ACC-01 {tag} port", PXC, y0, ACC_PZ, RP, 30, color=CDK, axis="y"))
    # SV-02 sample tap on the P-04 discharge (+Yd manifold), above the stack — body + spout + handwheel
    # SV-02 sample tap — TEED off the central feed riser out to the −X aisle so the valve body/handwheel
    # are clear of the through-riser and the ±Yd diverter legs (spout drops straight for cup access)
    sv_x = PXC - 95
    p.append(tee("SV-02 tap tee", PXC, CTR_Y, SV_Z + 25, run="z", branch="x-"))
    p.append(ov.ruby_pipe_run("SV-02 tap", [(PXC, CTR_Y, SV_Z + 25), (sv_x + 25, CTR_Y, SV_Z + 25)], RP, color=ov.C_VALVE))
    p.append(sample_valve("SV-02 sample valve", sv_x, CTR_Y, SV_Z, h=60))
    # 3W-DV-02 — Stage-A diverter above the stack (input underside; run to Brown −Yd / Waste +Yd)
    p.append(diverter("3W-DV-02", PXC, CTR_Y, DV_Z, run="y", branch="z-", handle="x-", color=ov.C_VALVE))
    return "\n".join(p)


def plumbing():
    """Stage-A tray-drain chain (P-04 → SV-02 → 3W-DV-02 → IBC-3 Brown / IBC-4 Waste) + the Blue
    supply (Blue #1 → P-01 → ACC-01 → trunk).  Routing rules: every segment is single-axis (no
    diagonals); each pump port leaves with a perpendicular −X stub; each run gets its OWN X depth
    lane so pipes never share a plane (no pipe-through-pipe); horizontal runs sit at Z levels
    clear of the pump bodies (tops ≤ 770)."""
    p = []
    def pipe(nm, wp, col): p.append(ov.ruby_pipe_run(nm, wp, RP, color=col))
    def pin(k):  return (PXC, PIY, _piz(k))              # IN  tip (−Yd manifold side)
    def pout(k): return (PXC, POY, _piz(k))             # OUT tip (+Yd manifold side)
    tip = DVB / 2 + DVL                                  # 78 — diverter port-stub tip
    dvm, dvp = CTR_Y - tip, CTR_Y + tip                  # 1103 / 1259 — DV-02 run−/run+ Yd
    xe  = ov.IBC_COL_X + 300                             # 4974 — tote side-entry X
    bz  = ov.IBC_PALLET_H + ov.IBC_H_1000 - 60           # 1276 — Brown near-top entry
    wz  = MERGE4[2]                                       # 1230 — Waste entry
    blz = ov.IBC_H_1000 + ov.IBC_PALLET_H + 64           # 1400 — Blue near top

    # P-04 SUCTION ← processing-tray SUMP (near-right corner), pickup routing copied from the
    # overview model: riser UP from the sump to a shut-off valve above the deck (over the tray
    # rim), back DOWN through the grate, then a floor-level run into the corridor and up to P-04 IN.
    sumpX, sumpY, sumpZ = ov.PROC_TRAY_DRAIN_X, ov.PROC_TRAY_DRAIN_YD + 75, ov.PROC_TRAY_SUMP_Z  # 4550,155,20
    valveZ = ov.WALKWAY_H + 65                          # 195 — valve body above the deck
    dropX, dropY = sumpX - 70, 50                       # 4480 — return riser in the grate gap, off the end beam
    gapX = (ov.PROC_TRAY_X_R + ov.IBC_COL_X) / 2        # 4651.5 — centered in the tray–IBC gap
    # Original (overview) loop, AROUND the tray (Rule 5a): UP through the walkway grate to the valve
    # above the deck, over in X, TWIST in Yd to OUTSIDE the tray near rim (dropY=50 < tray Yd80),
    # back DOWN through the grate, floor run along the outside strip to the gap past the tray's right
    # edge (x>4629), then up into the corridor and a −Yd stub straight into the P-04 IN port.
    z04 = _piz("P-04")
    p04by = PIY - 76                                      # 1025 — rise the suction in a back-lane −Yd of
    #   the ACC out-port/acc_out line (Yd1088): clears the blue ACC plumbing by ~52mm (was 6mm at PXC),
    #   then TWO 90° turns (rise, then +Yd) into the −Yd-facing P-04 IN port.
    pipe("Tray sump -> P-04 suction",
         [(sumpX, sumpY, sumpZ), (sumpX, sumpY, valveZ), (dropX, sumpY, valveZ), (dropX, dropY, valveZ),
          (dropX, dropY, 10), (gapX, dropY, 10), (gapX, dropY, 65), (4800, dropY, 65),
          (4800, p04by, 65), (PXC, p04by, 65), (PXC, p04by, z04), pin("P-04")],
         ov.C_IBC_BROWN)   # floor run at z10 — UNDER the film-plane saddle gusset (z20–140)
    p.append(ov.ruby_cylinder("Tray sump strainer foot", sumpX, sumpY, sumpZ, 14, 36, color=CDK, axis="z"))
    # P-04 DISCHARGE → up the BACK of the panel (clear of the OUT-port stack), back to the front
    # ABOVE the pumps where it's clear → SV-02 (in-line) → DV-02 underside branch.
    # P-04 OUT leaves convention-style: a short +Yd stub straight OUT of the +Yd-facing OUT port to a
    # front riser, up ABOVE the pumps (clear), then back in to SV-02 (in-line) and DV-02.
    pipe("P-04 -> SV-02 -> DV-02",
         [pout("P-04"), (PXC, POY + 50, z04), (PXC, POY + 50, 1960), (PXC, CTR_Y, 1960), (PXC, CTR_Y, DV_Z - tip)],
         ov.C_IBC_BROWN)   # P-04 OUT → up its OWN +Yd lane (POY+50, clear of the pump-discharge lane POY+30)
    #   → jog to the CENTRAL lane (CTR_Y) above the pumps → SV-02 tap → VERTICALLY
    #   into the underside (z−) branch; central lane keeps the feed/SV-02 clear of the ±Yd diverter legs
    # DV-02 → IBC-3 Brown — drop just below the top rear-panel bracket, then behind the panel (own
    # lane) → down → front → tote entry.
    zpen = 2050                                          # penetrate clear of the top bracket band (2146–2206)
    _side_entry(p, "DV-02 -> IBC-3 (Brown)",   # no CV-3 — P-04 has an integral check valve (check=False)
                [(PXC, dvm, DV_Z), (PXC, dvm - 80, DV_Z), (PXC, dvm - 80, bz), (xe, dvm - 80, bz)],
                xe, YD_NEAR, bz, -1, ov.C_IBC_BROWN, check=False, drop=-50)   # straight DOWN the front −Yd lane
    #   (Yd1068, −Yd of the pump IN ports at Yd1101) — the short-port diverter moved dvm in, so the
    #   leg needs the larger −80 offset to stay on that lane   # short 50mm dip tube inside the tote
    # DV-02 → IBC-4 merge — waste port → drop below the bracket → behind the panel (own lane) → down
    # → +X past the risers to the merge tee (jog to the merge Yd at x=MERGE, clear of the back verticals).
    # leave the +Yd port, turn toward the SEALED END and run 400mm along the top (Yd1229 clears the far
    # upright at 1266 now that the short-port diverter pulled dvp in to 1214), THEN drop and into the merge.
    dvwx = MERGE4[0] - 115                                # drop −x of the tee (top run 75mm shorter) so the
    #   horizontal approach seats on the −x run port as a clear run, not a stub right at the drop
    pipe("DV-02 -> IBC-4 merge",
         [(PXC, dvp, DV_Z), (PXC, dvp + 15, DV_Z), (dvwx, dvp + 15, DV_Z), (dvwx, dvp + 15, wz),
          (dvwx, MERGE4[1], wz), MERGE4], ov.C_IBC_WASTE)   # ~380mm toward the sealed end, drop, then
    #   a horizontal +x run that SEATS on the merge's −x run port (was dropping inside the tee body)
    # 3-way merge: tote entry on +x (run), DV-02 waste on −x (run), DV-01 waste rises into the z− branch
    p.append(tee("IBC-4 waste merge tee", MERGE4[0], MERGE4[1], MERGE4[2], run="x", branch="z-"))
    xe4 = ov.IBC_COL_X + 830                              # 5504 — entry +130 toward the sealed end
    _side_entry(p, "IBC-4 (Waste)", [MERGE4, (xe4, MERGE4[1], wz)], xe4, YD_FAR, wz, +1, ov.C_IBC_WASTE, check=False)   # no CV-4 — P-02/P-04 have integral check valves

    # BLUE #1 → P-01 suction: P-01 IN → front Yd-jog onto its back-lane → penetrate the panel →
    # vertical riser BEHIND the panel (clear of the pump-port stack) → back to the front → near tote.
    # IN approached convention-style (P-04 reference): −Yd stub straight out of the IN port, around
    # the front of the body, up the threading lane (between body Yd1131+ and the near upright Yd≤1096)
    # behind the panel, to the tote.
    z01 = _piz("P-01")
    # BV-01 must be reachable from the −X WALKWAY, so the suction comes FORWARD to a vertical section in the
    # corridor front (bvx, just clear of the front upright x≤4704) instead of rising on the back BLANE riser:
    # P-01 IN → −Yd stub → −X toward the walkway → UP the front vertical (BV-01 at reach height) → back +X
    # and up to the Blue tote near-top.
    bvx, bvy = FRONT_X + 106, YD_NEAR + 67       # 4760 / 1113 — corridor-front lane, clear of the front
    #   upright (Yd≤1096) AND the pump bodies (Yd≥1131) the high run passes at z=blz
    _side_entry(p, "Blue #1 -> P-01 suction",   # flooded suction + P-01's integral check → no foot valve (check=False)
                [pin("P-01"), (PXC, PIY - 30, z01), (bvx, PIY - 30, z01), (bvx, bvy, z01),
                 (bvx, bvy, blz)],
                bvx, YD_NEAR, blz, -1, ov.C_BLUE, check=False, drop=-50)   # entry aligned OVER BV-01's riser
    #   (225mm closer to the walkway) — the suction rises straight into the tote, no +X jog   # short 50mm dip tube inside the tote
    p.append(ball_valve("BV-01 (P-01 suction)", bvx, bvy, 1000, "z", hdir="-x"))   # front vertical section, handle faces the −X walkway operator
    # Blue supply IN LINE through ACC-01 (like a filter in the chain): P-01 OUT → ACC IN (+Yd),
    # ACC OUT (−Yd) → trunk out the mouth to the spray bar.
    # The ACC-IN elbow goes OUT HORIZONTALLY (+Yd into the aisle, clear of the P-01 head below) before
    # dropping to the P-01 OUT blue riser — NOT straight down over the pump.
    inby = CTR_Y + ACC_R + 75                              # 1320 — IN riser well +Yd of the P-01 head (Yd1234)
    pipe("P-01 -> ACC-01 (in)",
         [pout("P-01"), (PXC, inby, _piz("P-01")), (PXC, inby, ACC_PZ), acc_in()], ov.C_BLUE)
    # ACC-01 OUT → supply trunk → out to the gap past the tray right edge (GAPX), dropped to z60 ready
    # to cross to the outside-rim strip (tap01_supply continues it AROUND the tray to BV-05/TAP-01).
    # Leave the −Yd OUT port OUTWARD (−Yd), then run +Yd to the gap in the clear band BETWEEN the P-01 head
    # top (z490) and the ACC body bottom (z540) — z515 clears both by ~15mm.  (The old route ran +Yd at the
    # port's z568 and TUNNELED through the ACC body; z490 then grazed the P-01 head top.)
    trz = (PSTACK["P-01"] + PVB_H + PCAP_H + ACC_Z0) // 2     # 515 — midway P-01 head-top↔ACC body-bottom
    pipe("Blue supply trunk -> spray bar / TAP-01 (off-panel)",
         [acc_out(), (PXC, CTR_Y - ACC_R - 50, ACC_PZ), (PXC, CTR_Y - ACC_R - 50, trz),
          (PXC, GAP_CORR_Y, trz), (4660, GAP_CORR_Y, trz), (4660, GAP_CORR_Y, 60)], ov.C_BLUE)
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

    # ── X1 FILL: camlock → in-line one-way valve → STRAIGHT pipe → T-connector → BOTH Blue totes
    #    (IBC-1 / IBC-2).  ONE check on the inlet; no per-branch checks. ──
    x1z, tx = 2250, 5500
    p.append(ov.ruby_cylinder("X1 fill camlock (end wall)", ew - 60, CTR_Y, x1z, 26, 60, color=ov.C_STEEL, axis="x"))
    p.append(check_valve("X1 one-way valve", ew - 200, CTR_Y, x1z, "x"))   # in-line, just after the camlock
    pipe("X1 camlock -> one-way -> tee (straight)", [(ew - 60, CTR_Y, x1z), (tx, CTR_Y, x1z)], ov.C_BLUE)
    p.append(tee("X1 fill tee", tx, CTR_Y, x1z, run="y", branch="x+"))   # inlet from +X, splits ±Yd to the blues
    # each outlet runs STRAIGHT ±Yd off the tee's run port into its tote (no −X detour)
    for yface, into, nm in ((YD_NEAR, -1, "Blue #1 (IBC-1)"), (YD_FAR, +1, "Blue #2 (IBC-2)")):
        _side_entry(p, f"X1 fill -> {nm}", [(tx, CTR_Y, x1z)], tx, yface, x1z, into, ov.C_BLUE, check=False)

    # ── Blue EQUALIZATION: a low 1" cross-connect tying the BOTTOMS of the two Blue totes together
    #    so their levels equalize.  Straight across, near the sealed end. ──
    beqz, beqx = ov.IBC_H_1000 + ov.IBC_PALLET_H + 40, 5500   # ~1376 — just above the Blue tote bottoms
    p.append(ov.ruby_pipe_run("Blue equalization (IBC-1 <-> IBC-2)",
        [(beqx, YD_NEAR - 150, beqz), (beqx, YD_FAR + 150, beqz)], 16, color=ov.C_BLUE))   # 1" pipe
    p.append(ov.ruby_cylinder("Blue eq flange (IBC-1)", beqx, YD_NEAR - 8, beqz, 36, 16, color=ov.C_STEEL, axis="y"))
    p.append(ov.ruby_cylinder("Blue eq flange (IBC-2)", beqx, YD_FAR - 8, beqz, 36, 16, color=ov.C_STEEL, axis="y"))

    # ── IBC-3 BROWN: ONE shared bottom tap (dip tube → floor) → T-junction (cp.BROWN_TAP) that
    #    feeds BOTH P-05 (drain) and P-02 (wall filter loop) — a single tote penetration. ──
    tx3, ty3, tz3 = BROWN_TAP
    yin3 = YD_NEAR - 150                                  # 896 — penetration into the Brown tote
    p.append(ov.ruby_pipe_run("IBC-3 (Brown) bottom tap (shared P-02/P-05)",
        [(tx3, yin3, tz3 - 50), (tx3, yin3, tz3), (tx3, ty3 - 36, tz3)], RP, color=ov.C_IBC_BROWN))  # into the tee's −Yd branch end
    p.append(ov.ruby_cylinder("IBC-3 (Brown) tap flange", tx3, YD_NEAR - 8, tz3, 36, 16, color=ov.C_STEEL, axis="y"))
    p.append(tee("IBC-3 (Brown) tap T", tx3, ty3, tz3, run="x", branch="y-"))   # dip on −Yd; P-02 −X / P-05 +X
    # (no check valve at the bottom tap — the schematic's CV-3 is at the IBC-3 buffer return TOP;
    #  the shared bottom tap is just the tee feeding P-02/P-05 through BV-03/BV-02)
    # P-05 (Brown drain) suction: shared tap T → +X run end → rise to P-05 IN (−Yd manifold)
    p5i = (PXC, PIY, _piz("P-05")); p5o = (PXC, POY, _piz("P-05"))
    z05 = _piz("P-05")
    pipe("Brown tap -> P-05 inlet",   # OFF the tee's +X run end; IN approached convention-style via the back riser
         [(tx3 + 30, ty3, tz3), (PXC, ty3, tz3), (PXC, BL_P05, tz3), (BLANE, BL_P05, tz3), (BLANE, BL_P05, z05),
          (BLANE, BL_P01, z05), (4900, BL_P01, z05), (4900, PIY - 30, z05), (PXC, PIY - 30, z05), p5i],
         ov.C_IBC_BROWN)        # the front, then a −Yd stub straight into the IN port
    p.append(ball_valve("BV-02 (P-05 suction)", BLANE, BL_P05, z05 - 170, "z"))   # on the back riser
    p.append(ov.ruby_cylinder("X3 Brown drain port (end wall)", ew - 60, COL_L, 1700, 22, 60, color=C_CHECK, axis="x"))
    # P-05 OUT → behind the panel → +X to the end wall + a perpendicular ≥50mm bulkhead stub
    pipe("P-05 -> X3 end-wall port",   # OUT leaves with a +Yd stub straight out of the OUT port
         [p5o, (PXC, POY + 30, p5o[2]), (5060, POY + 30, p5o[2]), (5060, COL_L, p5o[2]),
          (ew - 130, COL_L, p5o[2]), (ew - 130, COL_L, 1700), (ew - 60, COL_L, 1700)], ov.C_IBC_BROWN)

    # ── IBC-4 WASTE: own bottom pickup (bend points DOWN to floor) → P-03 → X4 end-wall port ──
    p3i = (PXC, PIY, _piz("P-03")); p3o = (PXC, POY, _piz("P-03"))
    _bottom_pickup(p, "X4 Waste (P-03)", 5200, YD_FAR, +1, ov.C_IBC_WASTE,   # IN ends convention-style:
                   [(5200, YD_FAR - 120, p3i[2]), (5060, YD_FAR - 120, p3i[2]), (5060, PIY - 30, p3i[2]),
                    (PXC, PIY - 30, p3i[2]), (PXC, PIY, p3i[2])])             # −Yd stub straight into the IN port
    p.append(ball_valve("BV-06 (P-03 suction)", 5022, PIY - 30, p3i[2], "x"))   # waste-drain suction isolation
    p.append(ov.ruby_cylinder("X4 Waste drain port (end wall)", ew - 60, COL_R, 1620, 22, 60, color=C_CHECK, axis="x"))
    pipe("P-03 -> X4 end-wall port",   # OUT leaves with a +Yd stub straight out of the OUT port
         [p3o, (PXC, POY + 30, p3o[2]), (5060, POY + 30, p3o[2]), (5060, COL_R, p3o[2]),
          (ew - 130, COL_R, p3o[2]), (ew - 130, COL_R, 1620), (ew - 60, COL_R, 1620)], ov.C_IBC_WASTE)
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
