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
import massing_corridor_panel as cp        # the new corridor plumbing panel (same connected system)

# ── band + wall ──────────────────────────────────────────────────────────────
X0, X1 = 2700, 4674            # wet-end clear mounting band on the pinhole wall (Yd0)
WALL_X0, WALL_X1 = 0, ov.C_LEN # 0..5893 — the FULL pinhole wall (context spans the whole length)
C_HGT, C_WID = ov.C_HGT, ov.C_WID
DECK_Z = ov.WALKWAY_H          # 130
DECK_W = ov.WALKWAY_W          # 300 — standard near walkway (evaluate whether it fits)
VIEW_DEPTH = DECK_W + 300      # 600 — show from the wall out to 300mm PAST the walkway, then stop

C_PERSON = "#806040"
C_DECK   = "#9C7B4D"


def context():
    """Pinhole wall + a FULL-depth floor/ceiling (so the full IBC tanks sit on it), with
    a faint marker line at the 300mm-past-walkway depth for reference."""
    bx, bw = WALL_X0, WALL_X1 - WALL_X0          # the FULL pinhole wall length
    p = []
    p.append(ov.ruby_box("Pinhole wall", bx, -ov.WALL_T, 0, bw, ov.WALL_T, C_HGT,
                         color=ov.C_SHELL, alpha=0.30))
    p.append(ov.ruby_box("Floor", bx, 0, -ov.WALL_T, bw, C_WID, ov.WALL_T,
                         color=ov.C_SHELL, alpha=0.16))
    # (container ceiling omitted in this view)
    # faint reference line at the 300mm-past-walkway depth
    p.append(ov.ruby_box("Depth ref (Yd %d)" % VIEW_DEPTH, bx, VIEW_DEPTH - 2, 0, bw, 4, C_HGT,
                         color="#2060A0", alpha=0.10))
    return "\n".join(p)


def walkway_full():
    """Real walkway geometry so the cantilevers + brackets read: perimeter decks
    (near with punch-out, stopping at the IBC; left; right — FAR deck erased post-build),
    the wall gusset brackets, and the IBC-end cantilever arms."""
    p = []
    for fn in ("walkways", "walkway_brackets", "ibc_cantilever_arms"):
        try:
            r = getattr(ov, fn)()
            p.append("\n".join(r) if isinstance(r, (list, tuple)) else r)
        except Exception as e:
            print(f"  (skip {fn}: {e})", file=sys.stderr)
    return "\n".join(p)


def film_plane_beams():
    """The RIGHT-side (IBC-end) film-plane SUPPORT BEAMS (40x40 rails, full depth in Yd) +
    their wall-seat SADDLE BRACKETS.  The LEFT-side (cargo-door end) rails are omitted in
    this view to keep the wet end readable."""
    rail = 40
    z_bot = ov.RAIL_OFF_BOT
    z_top = ov.C_HGT - ov.RAIL_OFF - rail
    x_right = ov.RAIL_X_R - rail
    p = []
    for zl, rz in (("bot", z_bot), ("top", z_top)):
        p.append(ov.ruby_box(f"FP support beam R-{zl}", x_right, 0, rz, rail, C_WID, rail,
                             color=ov.C_STEEL))
    corners = {"TR": (x_right, z_top), "BR": (x_right, z_bot)}
    p.append(ov.film_plane_saddles(corners))     # right-end wall-seat saddle brackets only
    return "\n".join(p)


def deck():
    """Near walkway along the pinhole wall — STOPS at the IBC (does not pass it), with
    its punch-out (widened to WALKWAY_NEAR_WIDE_W over X1155-2629)."""
    p = []
    p.append(ov.ruby_box("Near walkway (stops at IBC)", WALL_X0, 0, DECK_Z - 15,
                         ov.IBC_COL_X - WALL_X0, DECK_W, 15, color=C_DECK, alpha=0.9))
    p.append(ov.ruby_box("Near walkway punch-out", ov.WALKWAY_NEAR_WIDE_X_L, DECK_W, DECK_Z - 15,
                         ov.WALKWAY_NEAR_WIDE_X_R - ov.WALKWAY_NEAR_WIDE_X_L,
                         ov.WALKWAY_NEAR_WIDE_W - DECK_W, 15, color=C_DECK, alpha=0.9))
    return "\n".join(p)


def ibc_slice():
    """A thin slice of the near IBC column at its front face (X=IBC_COL_X) — shows the
    space to the LEFT (high X) is taken, so the wet end can't extend past it."""
    return ov.ruby_box("IBC slice (space taken)", ov.IBC_COL_X, ov.BLUE_IBC_Y, 0,
                       120, VIEW_DEPTH - ov.BLUE_IBC_Y, 2 * ov.IBC_H_1000,
                       color=ov.C_IBC_BLUE, alpha=0.30)


# Other equipment ALREADY mounted on the pinhole wall (Yd0) — the wet-end layout has to
# coexist with these.  electrical() = panel + inverter + batteries.
OTHER_WALL_EQUIP = [("Electrical (panel/inverter/batteries)", "electrical")]


def other_equipment():
    p = []
    for _label, fn in OTHER_WALL_EQUIP:
        try:
            p.append(getattr(ov, fn)())
        except Exception as e:
            print(f"  (skip {fn}: {e})", file=sys.stderr)
    return "\n".join(p)


# Flat-T red-handle 3-way diverter — shared with the corridor module (DV-01 on the wall,
# DV-02 on the corridor panel) and kept there to avoid a circular import.
C_HANDLE = cp.C_HANDLE
diverter = cp.diverter


def kit():
    """Pinhole-wall FILTER sub-loop (Stage B, agreed labels).  Chain:
    IBC-3 (Brown buffer) → P-02 → F1 → F2 → F3 → SV-01 (sample) → DV-01 → Blue/Grey IBC.
    Mounted HIGH so the walkway stays clear; PUMP on the side FURTHEST from the IBCs
    (low X); FILTERS shifted toward the IBCs (high X); SV-01 + DV-01 dropped to WAIST for
    easy reach.  Plumbing orthogonal, perpendicular port stubs, routed around the bodies."""
    p = []
    fr = ov.BB_OD / 2          # 92
    BB_H, cap_h = ov.BB_H, 78
    f_top = C_HGT - 48
    f_bot = f_top - BB_H       # 2000 — the high tier
    fcy = fr + 12              # 104 — filter center Yd (sump back near the wall)
    cap_z = f_bot + BB_H - cap_h / 2   # 2301 — filter cap port centerline
    tie = cap_z                # ports are STRAIGHT/horizontal (in-line filter) — no down-elbow
    rp = ov.PUMP_PIPE_OD / 2   # 10.5
    yL, yS = 230, 295          # feed lane / suction+exit lane (clear of the bodies, Yd ≤ 196)
    yW = 35                    # wall plane — pipes/valves mounted on the plywood backing
    waist = 1000               # SV-01 + DV-01 reach height
    cdk = "#222228"

    FX = {"F1": 3300, "F2": 3638, "F3": 3976}                      # spacing tightened (jumper −40%)
    def f_in(nm):  return (FX[nm] - (fr + 30), fcy, tie)           # IN  port (−X)
    def f_out(nm): return (FX[nm] + (fr + 30), fcy, tie)           # OUT port (+X)

    # ── 3 Big Blue filters — F1 50µm / F2 KDF-55 / F3 GAC; STRAIGHT in-line ±X ports ──
    for nm, fx in FX.items():
        p.append(ov.ruby_cylinder(f"Filter {nm} sump", fx, fcy, f_bot, fr, BB_H - cap_h, color=ov.C_FILTER))
        p.append(ov.ruby_cylinder(f"Filter {nm} cap", fx, fcy, f_bot + BB_H - cap_h, fr + 3, cap_h, color=cdk))
        for tag, sd in (("in", -1), ("out", +1)):
            p.append(ov.ruby_pipe_run(f"Filter {nm} {tag} port",
                [(fx + sd * (fr - 6), fcy, cap_z), (fx + sd * (fr + 30), fcy, cap_z)], rp, color=cdk))
        p.append(ov.ruby_cylinder(f"Filter {nm} PR button", fx, fcy, f_bot + BB_H, 6, 9, color=ov.C_STEEL))

    # ── P-02 — UPRIGHT, IN/OUT on OPPOSITE sides along X (same pattern as the filters): OUT (+X)
    #    feeds straight into F1; IN (−X) takes the suction from the shared Brown tap. ──
    p2cx  = f_in("F1")[0] - (cp.PVB_R + 30) - 40                   # body center: OUT tip 40mm before F1
    p2cy  = fcy                                                    # same Yd lane as the filters
    p2cz0 = cap_z - (cp.PVB_H - 18)                               # OUT/IN port height at the cap level
    p += cp.pump_unit("Pump P-02 (Brown)", p2cx, p2cy, p2cz0, axis="x", color=ov.C_PUMP)
    p2_out = cp.pump_out(p2cx, p2cy, p2cz0, "x")                  # OUT port — exits +X (→ F1)
    p2_in  = cp.pump_in(p2cx, p2cy, p2cz0, "x")                   # IN port — exits −X (suction)

    # ── SV-01 sample tap (projects forward to yL for cup access) + flat-T 3W-DV-01 mounted
    #    back on the plywood (yW), both at WAIST level for easy reach ──
    svx, dvx = 4250, 4430
    p.append(cp.sample_valve("SV-01 sample valve", svx, yL, waist - 25, h=70))
    p.append(diverter("3W-DV-01", dvx, yW, waist, run="x", branch="z-", color=ov.C_VALVE))

    # ── PLUMBING ──
    def pipe(nm, wp, col): p.append(ov.ruby_pipe_run(nm, wp, rp, color=col))
    # 1. IBC-3 (Brown) suction → P-02 inlet, drawn FROM the shared bottom tap (cp.BROWN_TAP — a
    #    T also feeding P-05, so IBC-3 has ONE bottom penetration).  Down to the floor, along the
    #    wall base (Yd80, clear of the grey DV-01 waste drop at yW=35), up to P-02's +Yd IN port.
    yB = 80
    tx, ty, tz = cp.BROWN_TAP
    pipe("IBC-3 (Brown) tap -> P-02 inlet",   # AROUND the tray (Rule 5a): corridor run clear of the upright,
         [(tx, ty, tz), (tx, cp.GAP_CORR_Y, tz), (cp.GAPX, cp.GAP_CORR_Y, tz), (cp.GAPX, cp.TRAY_STRIP_Y, tz),
          (p2_in[0], cp.TRAY_STRIP_Y, tz), (p2_in[0], cp.TRAY_STRIP_Y, p2_in[2]), p2_in], ov.C_IBC_BROWN)  # cross at the gap, strip, up
    p.append(cp.ball_valve("BV-03 (P-02 suction)", p2_in[0], cp.TRAY_STRIP_Y, waist, "z"))   # at SV-01 reach height
    # 2. P-02 OUT (+X) → F1 inlet — straight, in line (same axis as the filter chain)
    pipe("P-02 -> F1", [p2_out, f_in("F1")], ov.C_IBC_BROWN)
    # 3. filter-skid jumpers F1→F2→F3 — straight pipe between the adjacent in-line ports
    #    (combo unit; the ports face each other in the gap, so no around-the-body routing)
    for a, b in (("F1", "F2"), ("F2", "F3")):
        pipe(f"{a} out -> {b} in", [f_out(a), f_in(b)], ov.C_IBC_BROWN)
    # 4. F3 outlet → SV-01: a 90° "collection" elbow brings it back to the WALL/backing, then
    #    the drop runs DOWN the wall (yW, clamped to the ply for support) to waist → SV-01.
    pipe("F3 -> SV-01 (wall-mounted drop)",
         [f_out("F3"), (f_out("F3")[0], yW, tie), (svx, yW, tie), (svx, yW, waist), (svx, yL, waist)], ov.C_FILTER)
    # after SV-01 the run returns to the plywood (yW) BEFORE routing on to DV-01 — keeps the
    # narrow walkway clear (only SV-01's sample spout projects forward to yL)
    pipe("SV-01 -> DV-01", [(svx, yL, waist), (svx, yW, waist), (dvx, yW, waist)], ov.C_FILTER)
    # 5. DV-01 → Blue IBC (IBC-2, run +X) + Waste IBC (IBC-4, off the UNDERSIDE branch).  Each
    #    enters near the TOP via the convention: the 90° entry turn is ENTRY_OFF mm BEFORE the
    #    flange (perpendicular approach stub), then flange (outside) + 150mm in + elbow + 150mm
    #    drop, with a check valve on the approach (anti-siphon).
    xf = ov.IBC_COL_X                            # tote front face (X4674)
    ENTRY_OFF = 120                              # the entry turn is >=75mm before the flange
    # Blue leg → Blue IBC (top tote), FRONT-face entry near top — leg + 150mm penetration + drop
    # are ONE run so every 90 gets a swept elbow; ORANGE anti-siphon check valve on the approach.
    bz = 2 * ov.IBC_H_1000 - 180                 # ~2156 — Blue tote near-top entry
    yBlue = 600                                   # leave the pinhole wall: turn out to Yd600 BEFORE
                                                  # entering the Blue tote front face (not against the wall)
    pipe("DV-01 -> Blue IBC (IBC-2)",
         [(dvx, yW, waist), (xf - ENTRY_OFF, yW, waist), (xf - ENTRY_OFF, yW, bz),
          (xf - ENTRY_OFF, yBlue, bz), (xf + 150, yBlue, bz), (xf + 150, yBlue, bz - 150)], ov.C_BLUE)
    p.append(ov.ruby_cylinder("Blue IBC (IBC-2) flange", xf - 8, yBlue, bz, 36, 16, color=ov.C_STEEL, axis="x"))
    p.append(cp.check_valve("Blue IBC (IBC-2) check valve", xf - 60, yBlue, bz, "x"))   # in-line on the X approach
    # Waste leg (off the underside branch) → Waste IBC (IBC-4, far-bottom).  Drops to the floor,
    # runs UNDER the walkway into the PLUMBING CORRIDOR, and enters from the CORRIDOR side
    # (Yd1316 face) — leg + 150mm penetration + drop ONE run, ORANGE check valve.
    # routes to the SHARED IBC-4 merge tee (where DV-02's waste leg also arrives) so a SINGLE
    # pipe makes the tote entry — see cp.MERGE4 / cp.plumbing()'s "IBC-4 (Waste)" entry.
    # arrives at the merge tee from the −Yd side (the tee's run; DV-02 comes in on the branch) so
    # the two waste legs do not overlap.
    # crosses under the walkway at Z70 (clear of the IBC frame), runs +X along the corridor gap
    # toward the SEALED END, and rises BEHIND the pumps/panel into the merge tee's underside branch
    # (so it never passes through the pumps or the frame).
    # DV-01 waste → AROUND the tray (Rule 5a): along the outside strip (Yd35) to the gap past the tray
    # right edge, drop, cross to the corridor at the gap, and run low to the merge — never over the tray.
    mx, my, mz = cp.MERGE4
    pipe("DV-01 -> IBC-4 merge",   # strip at z10 UNDER the FP saddle gusset/cleat past x4617, step to z20
         [(dvx, yW, waist), (4280, yW, waist), (4280, yW, 10), (4625, yW, 10), (4625, yW, 30),
          (cp.GAPX, yW, 30), (cp.GAPX, my, 30), (cp.GAPX, my, 60), (mx, my, 60), (mx, my, mz)],
         ov.C_IBC_WASTE)   # (clear of the corridor foot plate z0–12), cross, rise clear of the rail, merge
    return "\n".join(p)


def tap01_supply():
    """Blue supply trunk along the pinhole wall → spray-bar tap (BV-05) + TAP-01 chem tap (BV-04).
    Based on overview.skp's spray_bar_plumbing, but the wall trunk runs at the TRAY-RIM edge (Yd69,
    butted to the near rim) so it tucks UNDER the triangular near-walkway cantilever brackets — the
    Yd12-against-the-wall path ran straight through the bracket plates/bolts.  BV-04/BV-05 off-panel."""
    yd, fz = ov.PROC_TRAY_YD_NEAR - 11, ov.SPRAY_BAR_FEED_Z   # 69 — butt the tray near rim (Yd80), under the triangle
    pr, tr = ov.PUMP_PIPE_OD / 2, ov.TAP_PIPE_OD / 2
    p = []
    # AROUND the tray (Rule 5a): the corridor trunk ends at the gap (GAPX, CTR_Y, z60); cross to the
    # outside-rim strip there, drop to the trunk height, then the wall trunk runs along the strip (Yd12).
    p.append(ov.ruby_pipe_run("Blue trunk: corridor -> outside-rim strip",
        [(4660, cp.GAP_CORR_Y, 60), (cp.GAPX, cp.GAP_CORR_Y, 60), (cp.GAPX, yd, 60), (cp.GAPX, yd, fz)], pr, color=ov.C_BLUE))
    p.append(ov.ruby_cylinder("Blue Supply Trunk (1/2in HDPE)",
        ov.TAP_X, yd, fz, pr, cp.GAPX - ov.TAP_X, color=ov.C_BLUE, axis="x"))
    # BV-05 spray-bar isolation (riser + valve at the pinhole centerline)
    p.append(ov.ruby_cylinder("BV-05 Riser", ov.BV02_X, yd, fz, pr, ov.BV02_Z - fz, color=ov.C_BLUE, axis="z"))
    p.append(cp.ball_valve("BV-05 (spray-bar isolation)", ov.BV02_X, yd, ov.BV02_Z, "z"))
    # TAP-01 chem branch (3/4in) up over the shelf + BV-04 isolation (overview path)
    p.append(ov.ruby_pipe_run("TAP-01 Branch (3/4in)",
        [(ov.TAP_X, yd, fz), (ov.TAP_X, yd, ov.SHELF_STOW_TOP_Z),
         (ov.TAP_X, yd + 100, ov.SHELF_STOW_TOP_Z), (ov.TAP_X, yd + 100, ov.TAP_Z)], tr, color=ov.C_BLUE))
    p.append(cp.ball_valve("BV-04 (chem tap isolation)", ov.TAP_X, yd, 1010, "z"))
    return "\n".join(p)


def backing():
    """18mm marine-ply backing for the whole wall sub-loop — secured to the container wall;
    the pump, filters and valves mount on it and the pipes clamp to it for support (so the
    sub-loop installs as one panel, mirroring the corridor rear panel)."""
    return ov.ruby_box("Wall backing (18mm ply)", 2780, 0, 920, 1720, ov.EQPANEL_T, 1440, color=ov.C_PLY)


def person():
    # 1.75m scale figure standing ON the near walkway, FACING the IBC totes (+X):
    # depth (front-back) along X, shoulders along Yd.
    px, py = 3050, 200          # on the near walkway deck — nudged out so the back clears the ply
    z = DECK_Z
    pp = []
    pp.append(ov.ruby_box("Person legs", px - 100, py - 80, z, 200, 160, 850, color=C_PERSON, alpha=0.28))
    pp.append(ov.ruby_box("Person torso", px - 90, py - 150, z + 850, 180, 300, 600, color=C_PERSON, alpha=0.28))
    pp.append(ov.ruby_cylinder("Person head (scale 1.75m)", px, py, z + 1450, 100, 230, color=C_PERSON, alpha=0.32))
    return "\n".join(pp)


def right_walkway():
    """Partial view of the RIGHT walkway (runs in Yd across the container at X≈4329-4629)
    — only the slice within the limited depth (Yd0..VIEW_DEPTH), for spatial context where
    it passes the wet-end's IBC end."""
    return ov.ruby_box("Right walkway (partial)", ov.WALKWAY_RIGHT_X, 0, DECK_Z - 15,
                       ov.WALKWAY_RIGHT_W, VIEW_DEPTH, 15, color=ov.C_WALKWAY, alpha=0.9)


# ── "Labeled" scene callouts (point-anchored on the kit; instance-anchored on pinhole/elec) ──
LABEL_POINTS = [  # (x, y, z, text, leader dx,dy,dz)
    # ── pinhole-wall FILTER sub-loop (leaders point +Yd, out toward the operator) ──
    (3058, 104, 2300, "P-02\n(filter feed)", 0, 520, 250),
    (3300, 102, 2305, "F1 (50um)",   0, 560, 80),
    (3638, 102, 2305, "F2 (KDF-55)", 0, 560, 80),
    (3976, 102, 2305, "F3 (GAC)",    0, 560, 80),
    (4250, 230, 1000, "SV-01\n(sample)", 0, 430, 520),
    (4430, 35,  1000, "DV-01\n(3-way)",  0, 430, 740),
    # ── corridor plumbing panel: single-column pumps + ACC + Stage-A (leaders point −X, out the mouth) ──
    (cp.PXC, cp.PIY, cp._piz("P-01") - 150, "P-01 (Blue supply)", -700, 0, -150),
    (cp.PXC, cp.PIY, cp._piz("P-04") - 150, "P-04 (Tray drain)",  -800, 0, -150),
    (cp.PXC, cp.PIY, cp._piz("P-05") - 150, "P-05 (Brown drain)", -900, 0,  150),
    (cp.PXC, cp.PIY, cp._piz("P-03") - 150, "P-03 (Waste drain)", -1000, 0, 150),
    (cp.PXC, cp.CTR_Y, cp.ACC_Z0 + 150, "ACC-01\n(accumulator)", -700, 0, 250),
    (cp.PXC, cp.POY, cp.SV_Z, "SV-02\n(sample)", -700, 200, 0),
    (cp.PXC, cp.CTR_Y, cp.DV_Z, "DV-02 (3-way)", -700, 0, 200),
    # ── ball valves (in-panel pump-suction isolation; BV-01/02 on the BACK-of-panel risers) ──
    (cp.BLANE, cp.BL_P01, cp._piz("P-01") + 150, "BV-01", 350, 0, 250),
    (cp.BLANE, cp.BL_P05, cp._piz("P-05") - 170, "BV-02", 350, 0, 250),
    (2978, 80, 1000, "BV-03", 0, 520, 200),
    (5022, cp.PIY, cp._piz("P-03"), "BV-06", -1000, 0, 150),
    # ── per-tank anti-siphon check valves ──
    (ov.C_LEN - 200, cp.CTR_Y, 2250, "CV-1\n(X1 fill)", -600, 300, 0),
    (ov.IBC_COL_X - 60, 600, 2 * ov.IBC_H_1000 - 180, "CV-2\n(IBC-2 return)", 0, 450, 200),
    (ov.IBC_COL_X + 300, cp.YD_NEAR + 60, ov.IBC_PALLET_H + ov.IBC_H_1000 - 60, "CV-3\n(IBC-3 return)", -600, 250, 200),
    (ov.IBC_COL_X + 700, cp.YD_FAR - 60, cp.MERGE4[2], "CV-4\n(IBC-4 waste)", -600, 250, 200),
]
# Off-panel / context labels — shown ONLY in the full "Labeled" scene (Labels Context tag), kept
# OUT of the "Plumbing (labeled)" scene so their leaders don't clutter the plumbing view.
LABEL_CONTEXT_POINTS = [
    (ov.TAP_X, 112, ov.TAP_Z, "TAP-01\n(chem tap)", 0, 450, 300),
    (ov.TAP_X, 12, 1010, "BV-04", -450, 0, 250),
    (ov.BV02_X, 12, ov.BV02_Z, "BV-05\n(spray bar)", 0, 450, 250),
]
LABEL_INSTANCES = [
    ("Pinhole Assembly", "PINHOLE\n(optical ref)", 0, 700, 350),
    ("Other pinhole-wall equipment", "ELECTRICAL\n(panel/inverter/batteries)", 0, 850, 500),
    ("IBC Tanks (full)", "IBCs\n(space NOT available)", -300, 900, 300),
]


def labels_ruby():
    rows = []
    for x, y, z, text, dx, dy, dz in LABEL_POINTS:
        rows.append(
            f'anc = Geom::Point3d.new({ov.mm(x)},{ov.mm(y)},{ov.mm(z)})\n'
            f'txt = entities.add_text("{text}", anc, Geom::Vector3d.new({ov.mm(dx)},{ov.mm(dy)},{ov.mm(dz)}))\n'
            f'txt.layer = model.layers["Labels"] rescue nil')
    for x, y, z, text, dx, dy, dz in LABEL_CONTEXT_POINTS:   # off-panel labels → Labels Context tag
        rows.append(
            f'anc = Geom::Point3d.new({ov.mm(x)},{ov.mm(y)},{ov.mm(z)})\n'
            f'txt = entities.add_text("{text}", anc, Geom::Vector3d.new({ov.mm(dx)},{ov.mm(dy)},{ov.mm(dz)}))\n'
            f'txt.layer = model.layers["Labels Context"] rescue nil')
    for name, text, dx, dy, dz in LABEL_INSTANCES:
        rows.append(
            f'inst = entities.grep(Sketchup::ComponentInstance).find {{ |i| i.name == "{name}" }}\n'
            f'if inst\n'
            f'  bb = inst.bounds\n'
            f'  anc = Geom::Point3d.new(bb.center.x, bb.min.y, bb.center.z)\n'
            f'  txt = entities.add_text("{text}", anc, Geom::Vector3d.new({ov.mm(dx)},{ov.mm(dy)},{ov.mm(dz)}))\n'
            f'  txt.layer = model.layers["Labels Context"] rescue nil\n'   # context labels (PINHOLE/ELEC/IBC) — full scene only
            f'end')
    return '\n'.join(rows)


def build():
    # Limited-depth view of the FULL pinhole wall: the wet-end kit + the OTHER wall-mounted
    # equipment (own layer/scene) + a shallow context slice (wall + floor/ceiling out to
    # 300mm past the walkway) + scale figure.  Two scenes: wet end / other equipment.
    comps, tags = [], set()
    for name, tag, b in [("Context", "Context", context()),
                         ("Walkways + cantilevers + brackets", "Walkway", walkway_full()),
                         ("Film-plane support beams", "Film Plane", film_plane_beams()),
                         ("Processing tray (ghost)", "Processing Tray", ov.processing_tray()),
                         ("IBC Tanks (full)", "IBC", ov.ibc_stack(alpha=0.35)),
                         ("IBC restraint (bars + wall anchors)", "IBC Frame", cp.tote_restraint()),
                         ("End wall (context)", "Context", cp.end_wall()),
                         ("Pinhole Assembly", "Pinhole", ov.pinhole_assembly()),
                         ("Wall backing (ply)", "Backing", backing()),
                         ("TAP-01 + spray-bar supply", "Supply", tap01_supply()),
                         ("Wet-end kit (raked)", "Kit", kit()),
                         ("Person (scale)", "Scale", person()),
                         ("Other pinhole-wall equipment", "Pinhole Equipment", other_equipment()),
                         ("Corridor frame (deep box)", "Corridor Frame", cp.frame()),
                         ("Corridor rear panel", "Corridor Panel", cp.rear_panel()),
                         ("Corridor equipment", "Corridor Equipment", cp.equipment()),
                         ("Corridor plumbing", "Corridor Plumbing", cp.plumbing()),
                         ("Corridor drains + X-ports", "Corridor Drains", cp.drains_ports())]:
        comps.append(ov.component(name, tag, b)); tags.add(tag)
    tags.add("Labels"); tags.add("Labels Context")
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
# remove the FAR walkway deck AND its cantilever brackets (not wanted in this view)
model.definitions.each {{ |d| d.entities.grep(Sketchup::Group).each {{ |g| g.erase! if g.valid? && g.name =~ /^Walkway Far/ }} }}
# in-model callout labels on the 'Labels' tag (shown only in the Labeled scene)
{labels_ruby()}
v = model.active_view
v.camera = Sketchup::Camera.new(Geom::Point3d.new(800.mm, 6000.mm, 2300.mm), Geom::Point3d.new(2950.mm, 200.mm, 1100.mm), Geom::Vector3d.new(0,0,1), false, 52)
# Ghost the OTHER wall equipment by making its GEOMETRY translucent.  (A global X-ray render
# mode "sticks" across scene changes in SketchUp and leaks into every scene — per-geometry
# alpha does not.)  ModelTransparency stays OFF everywhere.
model.rendering_options["ModelTransparency"] = false
ghost = model.materials["GhostEquip"] || model.materials.add("GhostEquip")
ghost.color = Sketchup::Color.new(150,160,175); ghost.alpha = 0.35   # match the IBC-stack ghost alpha
def ghost_faces(ents, mat)
  ents.each {{ |e|
    if e.is_a?(Sketchup::Face); e.material = mat; e.back_material = mat
    elsif e.is_a?(Sketchup::Group); ghost_faces(e.entities, mat)
    elsif e.is_a?(Sketchup::ComponentInstance); ghost_faces(e.definition.entities, mat)
    end
  }}
end
model.entities.grep(Sketchup::ComponentInstance).each {{ |ci|
  ghost_faces(ci.definition.entities, ghost) if ci.layer && ["Pinhole Equipment", "Processing Tray"].include?(ci.layer.name)
}}
def scene(model, name, on)
  model.layers.each {{ |l| l.visible = (l.name == "Layer0" || l == model.layers[0] || on.include?(l.name)) }}
  pg = model.pages.add(name, 4095)
  pg.use_hidden_layers = true rescue nil
  pg
end
scene(model, "Water System", ["Context","Walkway","Film Plane","IBC","IBC Frame","Pinhole","Backing","Supply","Kit","Scale"])
scene(model, "Plumbing", ["Kit","Supply","Corridor Equipment","Corridor Plumbing","Corridor Drains"])
scene(model, "Plumbing (labeled)", ["Kit","Supply","Corridor Equipment","Corridor Plumbing","Corridor Drains","Labels"])
scene(model, "Plumbing + IBC", ["Kit","Supply","Corridor Equipment","Corridor Plumbing","Corridor Drains","IBC"])
scene(model, "Overall", ["Context","Walkway","Film Plane","Processing Tray","IBC","IBC Frame","Pinhole","Backing","Supply","Kit","Scale","Pinhole Equipment","Corridor Frame","Corridor Panel","Corridor Equipment","Corridor Plumbing","Corridor Drains"])
scene(model, "Labeled", ["Context","Walkway","Film Plane","Processing Tray","IBC","IBC Frame","Pinhole","Backing","Supply","Kit","Scale","Pinhole Equipment","Corridor Frame","Corridor Panel","Corridor Equipment","Corridor Plumbing","Corridor Drains","Labels","Labels Context"])
model.layers.each {{ |l| l.visible = true }}
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
