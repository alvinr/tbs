#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""generate_pinhole_water_panel.py — EXPLORATORY massing (pinhole-wall-mount branch).

Block massing of the wet end (pumps + ACC + filters) wall-mounted on the PINHOLE
WALL (Yd=0) in the clear band X2700-4674, arranged by the RAKE-BY-DEPTH principle:
the deepest items (Big Blue filters) ride HIGH, the shallow items (pumps, ACC) sit
LOW, keeping the torso band clear.  Includes the (widened) near-walkway deck and a
1750mm person for scale.  No plumbing yet — geometry feasibility only.

    python3 src/models/generate_pinhole_water_panel.py --send   # build in the live SketchUp doc
"""
import sys, os, argparse
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))   # repo root (src/models -> src -> root)
sys.path.insert(0, _HERE)
import generate_sketchup_model as ov
import generate_corridor_water_panel as cp        # the new corridor plumbing panel (same connected system)

# ── Sketchfab upload metadata (stamped onto the model on every --send) ────────
#    Read from the live water.skp 2026-07-03 (the model's own current title/description).
SF_TITLE = "TBS-001 Water Model"
SF_ID    = "1dae932430924e9b993e153a16f485fc"   # stable Sketchfab UID — re-uploads REPLACE this model
SF_TAGS  = "sketchup"
SF_DESC  = (
    "The camera operates in remote locations with no municipal water or drainage. "
    "This document specifies a self-contained three-circuit water system that:\n\n"
    "Stores sufficient clean water for 9–14 full-size prints between resupply runs on "
    "fresh Blue alone (~14 prints once Brown wash-2 recycling is counted — see §below) "
    "Recycles used wash water through a three-stage filter train, extending usable supply by "
    "approximately 40% Contains all waste water in a closed, transportable IBC for proper "
    "off-site disposal Runs entirely on 12V DC, compatible with a solar/battery off-grid power system."
)

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


# Cascade hint: walkway_full() reuses ov.walkways(), which draws the near-wide bump-out and the
# muslin-drop notches — so water.skp inherits WALKWAY_NEAR_WIDE_X_R, WALKWAY_MUSLIN_NOTCH_L_X0,
# WALKWAY_MUSLIN_NOTCH_R_X0. Named here so the grep-based missing-cascade check flags water.skp
# when any of them change (the deps are indirect via ov.*, which the import scan can't see).
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
    z_top = ov.C_HGT - ov.RAIL_OFF_TOP - rail
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

# Context-muting parameters — ONE place so every muted system matches: the IBC tanks
# (built muted via ov.ibc_stack(mute=)) and the in-place-muted context tags below all use
# these.  Desaturate the color this fraction toward ov.MUTE_NEUTRAL, at this alpha.
MUTE_DESAT, MUTE_ALPHA = 0.65, 0.18
# Context systems shown as a quiet faded backdrop (NOT the key plumbing/kit/supply) — desaturated
# in place keeping a faint tint.  Everything that is enclosure/structure rather than a water
# component is muted, so in EVERY scene only the plumbing reads boldly (easier to validate).
MUTE_TAGS = ["Pinhole Equipment", "Processing Tray", "IBC Frame", "Corridor Frame", "Corridor Panel",
             "Walkway", "Film Plane", "Pinhole", "Backing"]


def other_equipment():
    # Interior EP (fuse block / busbars / MPPT / battery + contactor) as pinhole-wall context. The
    # external power panel AND the evap cooler — both drawn by em.external_panel() — are DROPPED from
    # the water model (cleanup 2026-07-07). The overview no longer calls this (it draws its own EP).
    import generate_electrical_model as em
    return "\n".join([em.power_core(external_links=False), em.battery()])


def spray_bar():
    """Spray-bar gantry (beam + carriages + feed pole) — context so the BV-05 supply coil has the bar
    to connect to. Reuses the detailed spray-bar builders, same as the overview's spray_bar()."""
    import generate_spraybar_model as sb
    return "\n".join([sb.build_beam(), sb.build_carriages(include_floor=False), sb.build_feed_pole()])


# Flat-T red-handle 3-way diverter — shared with the corridor module (DV-01 on the wall,
# DV-02 on the corridor panel) and kept there to avoid a circular import.
C_HANDLE = cp.C_HANDLE
diverter = cp.diverter

# 3W-DV-01 center — single source for the geometry (kit()) AND the label anchor, so the
# callout can never drift off the diverter again when DV-01 is relocated.
DV01_CX, DV01_CY, DV01_CZ = 4800, cp.CTR_Y + 60, 235   # +100mm toward the sealed (high-X) end so the port turns run square (DCY drives the filtered-line ribbon notch — don't nudge in Yd without decoupling it)


def kit(part="all", p02_on_corridor=False):
    """Pinhole-wall FILTER sub-loop (Stage B, agreed labels).  Chain:
    IBC-3 (Brown buffer) → P-02 → F1 → F2 → F3 → SV-01 (sample) → DV-01 → Blue/Grey IBC.
    Mounted HIGH so the walkway stays clear; PUMP on the side FURTHEST from the IBCs
    (low X); FILTERS shifted toward the IBCs (high X); SV-01 + DV-01 dropped to WAIST for
    easy reach.  Plumbing orthogonal, perpendicular port stubs, routed around the bodies.

    Construction-model splits (default "all" = the full skid, byte-identical):
      • "recycle"       — ONLY the blue DV-01→X1 recycle line (corridor run to the IBC panel; Phase 1)
      • "waste"         — ONLY the grey DV-01→IBC-4 merge line (corridor run to the IBC panel; Phase 1)
      • "brown_ribbon"  — ONLY the brown IBC-3→P-02 suction's under-grate RIBBON portion (Phase 3, 3.2)
      • "skid"          — the skid bodies + on-panel plumbing + the short brown RISE to P-02, but NOT
                          the three lines above (they install earlier)."""
    p = []
    fr = ov.BB_OD / 2          # 92
    BB_H, cap_h = ov.BB_H, 78
    f_top = ov.PWP_FILTER_TOP_Z
    f_bot = f_top - BB_H       # 2000 — the high tier
    fcy = ov.PWP_FILTER_YD     # 104 — filter center Yd (sump back near the wall)
    cap_z = f_bot + BB_H - cap_h / 2   # 2301 — filter cap port centerline
    tie = cap_z                # ports are STRAIGHT/horizontal (in-line filter) — no down-elbow
    rp = ov.PUMP_PIPE_OD / 2   # 10.5
    yL, yS = 230, 295          # feed lane / suction+exit lane (clear of the bodies, Yd ≤ 196)
    yW = 35                    # wall plane — pipes/valves mounted on the plywood backing
    waist = ov.PWP_WAIST_Z     # SV-01 + DV-01 reach height
    cdk = "#222228"

    FX = {"F1": ov.PWP_FILTER_X1, "F2": ov.PWP_FILTER_X2, "F3": ov.PWP_FILTER_X3}   # single-source (tbs_constants)
    def f_in(nm):  return (FX[nm] - (fr + 30), fcy, tie)           # IN  port (−X)
    def f_out(nm): return (FX[nm] + (fr + 30), fcy, tie)           # OUT port (+X)

    # ── 3 Big Blue filters — F1 50µm / F2 KDF-55 / F3 GAC; STRAIGHT in-line ±X ports ──
    for nm, fx in FX.items():
        p.append(ov.ruby_cylinder(f"Filter {nm} sump", fx, fcy, f_bot, fr, BB_H - cap_h, color=ov.C_FILTER))
        p.append(ov.ruby_cylinder(f"Filter {nm} cap", fx, fcy, f_bot + BB_H - cap_h, fr + 3, cap_h, color=cdk))
        for tag, sd in (("in", -1), ("out", +1)):
            if nm == "F3" and tag == "out":
                continue        # F3 OUT stub drawn separately below — it TURNS the collection elbow
            p.append(ov.ruby_pipe_run(f"Filter {nm} {tag} port",
                [(fx + sd * (fr - 6), fcy, cap_z), (fx + sd * (fr + 30), fcy, cap_z)], rp, color=cdk))
        p.append(ov.ruby_cylinder(f"Filter {nm} PR button", fx, fcy, f_bot + BB_H, 6, 9, color=ov.C_STEEL))

    # ── P-02 — UPRIGHT, IN/OUT on OPPOSITE sides along X (same pattern as the filters): OUT (+X)
    #    feeds straight into F1; IN (−X) takes the suction from the shared Brown tap. ──
    p2cx  = ov.PWP_P02_X                                          # body center: OUT tip 40mm before F1
    p2cy  = fcy                                                    # same Yd lane as the filters
    p2cz0 = cap_z - (cp.PVB_H - 18)                               # OUT/IN port height at the cap level
    if not p02_on_corridor:                                      # P-02 relocated to the corridor column (water.skp)
        p += cp.pump_unit("Pump P-02 (Brown)", p2cx, p2cy, p2cz0, axis="x", color=ov.C_PUMP)
    p2_out = cp.pump_out(p2cx, p2cy, p2cz0, "x")                  # OUT port — exits +X (→ F1)
    p2_in  = cp.pump_in(p2cx, p2cy, p2cz0, "x")                   # IN port — exits −X (suction)

    # ── SV-01 sample tap stays on the plywood at the wall (sample cup access at waist).  3W-DV-01 is
    #    RELOCATED into the rear corridor so the filtered line runs as ONE pipe and only splits there ──
    svx = ov.PWP_SV01_X
    sv_y = yW + 75             # SV-01 projects only 75mm forward of the wall (cup access; was yL=230)
    p.append(cp.sample_valve("SV-01 sample valve", svx, sv_y, waist - 25, h=70))
    tipd = cp.DVB / 2 + cp.DVL                  # 33 — diverter port-stub tip reach
    DCX, DCY, DCZ = DV01_CX, DV01_CY, DV01_CZ   # DV-01 at the CORRIDOR-ENTRY TURN (just inside the mouth,
    #   reachable from the right walkway), shifted +60mm AWAY from the pinhole wall (+Yd) — the practical
    #   max at the mouth before the front-far frame upright (Yd1266+).  The single filtered line turns in
    #   here and splits; blue + waste legs run back across the corridor (low lane, under the ACC)
    p.append(diverter("3W-DV-01", DCX, DCY, DCZ, run="x", branch="y-", handle="z+", color=ov.C_VALVE))

    # ── PLUMBING ──
    def pipe(nm, wp, col): p.append(ov.ruby_pipe_run(nm, wp, rp, color=col))
    # 1. IBC-3 (Brown) suction → P-02 inlet, drawn FROM the shared bottom tap (cp.BROWN_TAP — a
    #    T also feeding P-05, so IBC-3 has ONE bottom penetration).  Down to the floor, along the
    #    wall base (Yd80, clear of the grey DV-01 waste drop at yW=35), up to P-02's +Yd IN port.
    yB = 80
    tx, ty, tz = cp.BROWN_TAP
    # UNDER-WALKWAY RIBBON (lane 0): IBC-3 tap (corridor) → loop UP over the first cantilever →
    # down into the ribbon channel → −Yd to the near-rim strip → rise up the wall to P-02's IN port.
    # split for the construction model: the under-grate RIBBON portion lays with the other ribbons
    # (Phase 3, step 3.2, before the grate); the short RISE to P-02 stays with the skid (3.5).
    brown_pre = ([(tx - 30, ty, tz), (4720, ty, tz), (4720, ty, 65)]               # tap → −X → down to the corridor pickup (past the tray edge)
                 + cp.ribbon_run(0, (4720, ov.RWK_RIBBON_NOTCH_YDS[0], 65), (2960, 55, 25), up_yd=cp.RIBBON_YD_DOWN))  # rise to flush, cross the NOTCHED beam (lane-0 Yd); crest at the SHARED line-1 Yd (uniform crests, Alvin 2026-07-24)
    brown_rise_wps = [(2960, 55, p2_in[2]), (2960, p2cy, p2_in[2]), p2_in]         # rise to P-02 IN
    brown_full_pipe = ov.ruby_pipe_run("IBC-3 (Brown) tap -> P-02 inlet", brown_pre + brown_rise_wps, rp, color=ov.C_IBC_BROWN)
    if not p02_on_corridor:                                      # this wall suction is replaced by a corridor IBC-3→P-02 run
        p.append(brown_full_pipe)
    brown_ribbon_pipe = ov.ruby_pipe_run("IBC-3 (Brown) tap -> ribbon (under-grate, to P-02)", brown_pre, rp, color=ov.C_IBC_BROWN)
    brown_rise_pipe = ov.ruby_pipe_run("Brown ribbon -> P-02 inlet (rise)", [brown_pre[-1]] + brown_rise_wps, rp, color=ov.C_IBC_BROWN)
    # ^ OFF the tee's −X end; descent OFFSET from the blue trunk (Yd1170 not 1150); −Yd at z25 OVER the
    #   corridor foot-plate, then step DOWN to z10 (2 elbows) to pass UNDER the blue trunk; strip z10 to P-02.
    #   At x2960 the riser is nudged back to Yd43 (off the strip's Yd56) so it clears the Yd69 supply trunk
    #   it would otherwise rise straight through (grey lane Yd24–45 is x≥4269, so x2960 is clear at Yd43).
    if not p02_on_corridor:
        p.append(cp.ball_valve("BV-03 (P-02 suction)", 2960, 43, waist, "z"))   # at SV-01 reach height (moves to the corridor with P-02)
    # 2. (Phase 2) F1 is now fed by DV-02's recycle branch (see skid_plumbing); P-02 OUT → ACC-02 instead.
    # 3. filter-skid jumpers F1→F2→F3 — straight pipe between the adjacent in-line ports
    #    (combo unit; the ports face each other in the gap, so no around-the-body routing)
    for a, b in (("F1", "F2"), ("F2", "F3")):
        pipe(f"{a} out -> {b} in", [f_out(a), f_in(b)], ov.C_IBC_BROWN)
    # 4. F3 outlet → SV-01: the BLACK OUT-port extension turns the 90° "collection" elbow itself
    #    (elbow rendered INSIDE the black fitting, at the extension's end), then the filter-colored
    #    line picks up at the handoff and drops DOWN the wall (yW) to waist → SV-01.
    #    Why draw the elbow in the black run: ruby_pipe_run insets its fillet along the INCOMING leg,
    #    so an elbow at f_out always eats ~one radius back into whatever precedes it — keeping that
    #    leg the same black fitting means nothing colored is intruded and the elbow sits at the
    #    black extension's end (endpoints get no fitting, so f_out must be an interior vertex).
    f3_hand = (f_out("F3")[0], fcy - 40, tie)          # handoff just past the black elbow's -Y exit tangent
    p.append(ov.ruby_pipe_run("Filter F3 out port",
             [(FX["F3"] + (fr - 6), fcy, tie), f_out("F3"), f3_hand], rp, color=cdk))
    # F3 -> SV-01: drop down the wall, then dog-leg IN through SV-01's −X face — the filtered line runs
    # HORIZONTALLY through the valve body (in-line, matching SV-02), box over the through-segment.
    pipe("F3 -> SV-01 (wall-mounted drop)",
         [f3_hand, (f_out("F3")[0], yW, tie), (svx - 60, yW, tie),          # −Yd to the wall, +X to just −X of SV-01
          (svx - 60, yW, waist + 10),                                       # DOWN the wall to the SV-01 in-line height
          (svx - 60, sv_y, waist + 10),                                     # +Yd forward to the valve lane
          (svx + 25, sv_y, waist + 10)], ov.C_FILTER)                       # +X THROUGH the body (in-line) to the +X face
    # after SV-01 the run returns to the plywood (yW) BEFORE routing on to DV-01 — keeps the
    # narrow walkway clear (only SV-01's sample spout projects forward to yL)
    # 4b. SV-01 -> DV-01: ONE filtered line follows the shared surface-perimeter route across the
    #     corridor (the path the blue+waste legs used to BOTH take, stacked) to the relocated DV-01 —
    #     which now SPLITS in the rear corridor, collapsing the old pair of parallel runs into one.
    sz    = cp.SUCT_SURF_Z + 30                   # 235 — surface perimeter lane
    xdrop = ov.RAIL_X_R - 17                      # 4632 — turn DOWN the wall clear of the IBC hanger
    # UNDER-WALKWAY RIBBON (lane 3): SV-01 → down the wall → −Yd along the ribbon → grate slot
    # → across the corridor to DV-01's IN port.
    # Drop SV-01 straight down the wall to a LOW strip level and run under the walkway beams (like the
    # other three lines).  On the corridor side it comes back DOWN just past the cantilever (like the
    # sump), runs under the grate to DV-01's Yd, then rises into DV-01's IN port.
    pipe("SV-01 -> DV-01 (single filtered line)",
         [(svx + 25, sv_y, waist + 10),                                               # leave SV-01's +X face (in-line)
          (svx + 50, sv_y, waist + 10),                                               # +X out (dog-leg)
          (svx + 50, yW, waist + 10),                                                 # −Yd to the wall
          (svx + 50, yW, 20),                                                         # DOWN the wall to below the blue trunk floor (Z38)
          (svx + 50, 60, 20)]                                                         # +Yd (Yd60 clears the end beam)
         + cp.ribbon_run(3, (DCX - 100, DCY, 65), (svx + 50, 60, 20), up_yd=cp.RIBBON_YD_DOWN)[::-1][1:]  # flush across the notched beam; crest rises at the SHARED line-1 Yd (RIBBON_YD_DOWN) so all 4 ribbon crests are uniform (Alvin 2026-07-24)
         + [(DCX - 100, DCY, DCZ),                                                      # rise −X of the port to the IN-port height
            (DCX - tipd, DCY, DCZ)],                                                    # +X 90° turn horizontally into DV-01's −X IN port
         ov.C_FILTER)
    # 5. DV-01 RECYCLE (run+, +X) → IBC-3 BUFFER tote — the recycle loop's buffer; P-02 pulls from IBC-3.
    #    (Was routed to the Blue X1 fill cross; Blue is now FILL-ONLY fresh water, so the filtered recycle
    #    stays isolated in IBC-3 — the contamination fix.)  CV-3 anti-siphon check on the approach.
    r_ex = 4760                                          # entry X on the Brown-tote near face, just −X of DV-01 (clear of the tap 4880 + pump column 4934)
    r_ez = ov.IBC_H_1000 - 38                            # 1130 — Brown top-entry level (= the old DV-02→IBC-3 entry)
    cp._side_entry(p, "DV-01 recycle -> IBC-3 (buffer)",
        [(DCX + tipd, DCY, DCZ),                         # off DV-01's +X recycle port (z235)
         (DCX + tipd + 40, DCY, DCZ),                    # +X OUT of the port (collinear with the +X stub) — swept elbow at the next vertex
         (DCX + tipd + 40, DCY, r_ez),                   # RISE to the Brown top-entry level
         (r_ex, DCY, r_ez)],                             # −X along the corridor to the entry lane
        r_ex, cp.YD_NEAR, r_ez, -1, ov.C_BLUE, drop=-50, check=False)   # −Yd into the Brown tote; no CV-3 — P-04 has an integral check + top entry can't siphon (matches the old DV-02→IBC-3 entry)
    # 6. DV-01 WASTE (branch, z+) → the shared IBC-4 merge tee's z− branch (DV-02's waste also lands here,
    #    on the tee run, so the two legs make ONE tote entry).
    mx, my, mz = cp.MERGE4
    waste_pipe = ov.ruby_pipe_run("DV-01 -> IBC-4 merge",
         [(DCX, DCY - tipd, DCZ), (DCX, 1165, DCZ),                   # SHORT −Yd exit off the branch → 90° elbow sooner
          (mx, 1165, DCZ),                                            # +X across the corridor at Yd1165 — SHIFTED +Yd (toward the
          #   film plane, was 1147) to open a lane for the blue supply trunk; still clears the brown P-02 riser below and
          #   the blue recycle elbow above (−Yd edge 1185)
          (mx, my, DCZ),                                              # −Yd to the merge column at the far end
          (mx, my, mz)], rp, color=ov.C_IBC_WASTE)                    # rise into the merge tee's z− branch
    p.append(waste_pipe)
    if part == "recycle":
        return recycle_pipe
    if part == "waste":
        return waste_pipe
    if part == "brown_ribbon":
        return brown_ribbon_pipe
    if part == "skid":
        # skid geometry only: drop the Phase-1 lines (recycle, waste) + the brown RIBBON (→3.2),
        # and swap in the short brown RISE to P-02.
        drop = {recycle_pipe, waste_pipe, brown_full_pipe}
        return "\n".join([x for x in p if x not in drop] + [brown_rise_pipe])
    return "\n".join(p)


def tap01_supply():
    """Blue supply trunk along the pinhole wall → spray-bar tap (BV-05) + TAP-01 chem tap (BV-04).
    Based on overview.skp's spray_bar_plumbing, but the wall trunk runs at the TRAY-RIM edge (Yd69,
    butted to the near rim) so it tucks UNDER the triangular near-walkway cantilever brackets — the
    Yd12-against-the-wall path ran straight through the bracket plates/bolts.  BV-04/BV-05 off-panel."""
    yd, fz = ov.PROC_TRAY_YD_NEAR - 11, ov.SPRAY_BAR_FEED_Z   # 69 — butt the tray near rim (Yd80), under the triangle
    pr, tr = ov.PUMP_PIPE_OD / 2, ov.TAP_PIPE_OD / 2
    bvx = ov.BV02_X - 150   # BV-05 riser nudged 150mm −X (toward the EP) to clear the relocated tray-sump suction at PH_X
    p = []
    # UNDER-WALKWAY RIBBON (lane 1): the corridor blue trunk (dropped clear of the FP rail at X4670, Yd~1132,
    # z60) rises to FLUSH in the tray-edge slot, crosses the notched outer beam, runs −Yd along the ribbon to
    # the outside-rim strip, where the wall trunk continues.  (Moved from lane 2 → lane 1: the middle two lanes
    # swapped so the blue TAP-01 trunk and the brown tray-sump alternate, and the blue/brown no longer cross.)
    p.append(ov.ruby_pipe_run("Blue trunk: corridor -> ribbon -> outside-rim strip",
        cp.ribbon_run(1, (cp.BLUE_TRUNK_HANDOFF_X, cp.GAP_CORR_Y, 60), (cp.RIBBON_LANE_X[1], yd, fz), up_yd=cp.RIBBON_YD_DOWN), pr, color=ov.C_BLUE))  # crest rises at the SHARED line-1 Yd (RIBBON_YD_DOWN) so all 4 ribbon crests are uniform (Alvin 2026-07-24)
    p.append(ov.ruby_cylinder("Blue Supply Trunk (1/2in HDPE)",   # trunk ends at the ribbon lane (clear of the saddle gusset)
        ov.TAP_X, yd, fz, pr, cp.RIBBON_LANE_X[1] - ov.TAP_X, color=ov.C_BLUE, axis="x"))
    # BV-05 3W SELECTOR (fresh ↔ recycled → spray bar) — relocated FORWARD (Yd) + UP (Z) onto a bracket off
    # the pinhole wall, close to the spray-bar pole-top feed (2420,633,1303) so the delivery coil is short.
    #   run = fresh (−Yd, up from the trunk) ↔ spray (+Yd, to the coil); branch = recycled IN (+X, from ACC-02).
    b5x, b5y, b5z = bvx, 350, 1150                     # X kept clear of the sump (2249); forward + up near the pole-top feed
    dvt = cp.DVB / 2 + cp.DVL                          # diverter port-tip reach
    p.append(cp.diverter("3W-BV-05 (spray selector)", b5x, b5y, b5z, run="y", branch="x+", handle="z+", color=ov.C_VALVE))
    # Fresh supply: tap the trunk at the wall, rise, then +Yd into the −Yd fresh port
    p.append(ov.ruby_pipe_run("BV-05 fresh supply (trunk -> selector)",
        [(b5x, yd, fz),                                # tap the blue trunk (Yd69, Z41)
         (b5x, yd, b5z),                               # UP the wall to selector height
         (b5x, b5y - dvt, b5z)], pr, color=ov.C_BLUE))  # +Yd into the −Yd fresh port
    # Spray delivery: +Yd spray port → short coiled hose to the spray-bar pole-top feed (slack for the roll)
    p.append(ov.ruby_coil_cord("Spray-bar supply hose (selector -> spray bar, coiled)",
        [(b5x, b5y + dvt, b5z),                        # off the +Yd spray port
         (2350, 500, 1240),                            # service-coil slack loop
         (2420, 633, 1303)], r=7, color=ov.C_BLUE))    # onto the pole-top feed
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
    return ov.ruby_box("Wall backing (18mm ply)", 2780, 0, 920, 1795, ov.EQPANEL_T, 1440, color=ov.C_PLY)  # +75mm at the +X edge so the grey waste clamps to the ply before it bends into the ribbon


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
_FILT_FCY = ov.BB_OD / 2 + 12              # 104 — filter / P-02 body center Yd (sump back near the wall)
_FILT_CZ  = ov.C_HGT - 48 - ov.BB_H / 2    # 2170 — Big-Blue filter body center Z
# Phase-2 skid row (P-04 · SV-02 · DV-02, under the filters) — single-sourced for skid_row/plumbing/labels
SROW_YD, SROW_Z0 = 104, 1150   # Yd104 = the filter/P-02 wall lane (surface-mounted on the ply, like the other kit)
LABEL_POINTS = [  # (x, y, z, text, leader dx,dy,dz) — (x,y,z) is the arrow TIP = component CENTER
    # ── pinhole-wall FILTER sub-loop (leaders point +Yd, out toward the operator) ──
    (ov.PWP_P02_X, ov.PWP_FILTER_YD, SROW_Z0 + 100, "ACC-02\n(recycle spray)", 0, 470, -180),   # on the skid (P-02's vacated spot)
    (3300, _FILT_FCY, _FILT_CZ, "F1 (50um)",   0, 560, 215),
    (3638, _FILT_FCY, _FILT_CZ, "F2 (KDF-55)", 0, 560, 215),
    (3976, _FILT_FCY, _FILT_CZ, "F3 (GAC)",    0, 560, 215),
    (4250, 110, 1000, "SV-01\n(sample)", 0, 430, 520),   # SV-01 now 75mm off the wall (yW+75)
    (DV01_CX, DV01_CY, DV01_CZ, "DV-01\n(3-way)",  -700, 0, 650),   # relocated to the corridor mouth (see kit())
    # ── Phase-2 skid row under the filters (P-04 · SV-02 · DV-02, relocated from the corridor) — leaders +Yd ──
    (ov.PWP_FILTER_X1, SROW_YD, SROW_Z0 + cp.PVB_H / 2, "P-04\n(tray drain)", 0, 470, -180),
    (ov.PWP_FILTER_X2, SROW_YD, SROW_Z0 + 162, "SV-02\n(sample)", 0, 470, -120),
    (ov.PWP_FILTER_X3, SROW_YD, SROW_Z0 + 162, "DV-02 (3-way)", 0, 470, -180),
    # ── corridor plumbing panel: single-column pumps + ACCs (leaders point −X, out the mouth) ──
    (cp.PXC, cp.CTR_Y, cp.PSTACK["P-01"] + cp.PVB_H / 2, "P-01 (Blue supply)", -700, 0, -150),
    (cp.PXC, cp.CTR_Y, cp.PSTACK["P-04"] + cp.PVB_H / 2, "P-02 (recycle pump)", -800, 0, -150),   # relocated into P-04's vacated slot
    (cp.PXC, cp.CTR_Y, cp.PSTACK["P-05"] + cp.PVB_H / 2, "P-05 (Brown drain)", -900, 0,  150),
    (cp.PXC, cp.CTR_Y, cp.PSTACK["P-03"] + cp.PVB_H / 2, "P-03 (Waste drain)", -1000, 0, 150),
    (cp.PXC, cp.CTR_Y, cp.ACC_Z0 + 87, "ACC-01\n(accumulator)", -700, 0, 250),   # + acc_h/2 (body 174)
    # ── ball valves (in-panel pump-suction isolation; BV-01/02 on the BACK-of-panel risers) ──
    (cp.FRONT_X + 106, cp.YD_NEAR + 67, 1000, "BV-01", -600, 0, 250),   # now on the front walkway-side riser
    (cp.PXC - 86, cp.BV02_YD, cp._piz("P-05") - 85, "BV-02", 350, 0, 250),   # ON the BV-02 valve body (P-05 suction), not the shirt riser
    (cp.BROWN_TAP[0] - 55, cp.PIY - 40, 950, "BV-03", -600, 0, 250),   # ON the corridor P-02 suction riser (relocated with P-02)
    (cp.PXC, cp.PIY, cp._piz("P-03") - 41, "BV-06", -1000, 0, 150),    # inline below the P-03 IN port
    # ── per-tank anti-siphon check valves ──
    (ov.C_LEN - 200, cp.X1_TEE_Y, cp.X1_TEE_Z, "CV-1\n(X1 fill)", -600, 300, 0),   # only CV-1 — pumps' integral checks cover the returns
    # ── end-wall bulkhead ports (tip at the port-body center, 30mm in from the wall) ──
    (ov.C_LEN - 30, cp.X1_TEE_Y, cp.X1_TEE_Z, "X1\n(fresh fill)", -550, 250, 0),
    (ov.C_LEN - 30, cp.COL_L, 1700, "X3\n(brown drain out)", -550, 0, 250),
    (ov.C_LEN - 30, cp.COL_R, 1620, "X4\n(waste drain out)", -550, 0, -250),
]
# Off-panel / context labels — shown ONLY in the full "Labeled" scene (Labels Context tag), kept
# OUT of the "Plumbing (labeled)" scene so their leaders don't clutter the plumbing view.
LABEL_CONTEXT_POINTS = [
    (ov.TAP_X, 112, ov.TAP_Z, "TAP-01\n(chem tap)", 0, 450, 300),
    (ov.TAP_X, 12, 1010, "BV-04", -450, 0, 250),
    (ov.BV02_X - 150, 350, 1150, "3W-BV-05\n(spray selector)", 0, 350, 200),   # ON the relocated selector (forward+up, near the pole-top feed)
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


def panel_power(include_switch=True, part="all"):
    """Circuit-C power + cabling to the TWO plumbing panels ONLY (no other electrical shown).
    Routed to NEVER cross a pipe (plumbing-skill rule): the corridor run lives in the CHASE
    between the pump-mount shirt and the rear panel — a clear vertical channel behind the pump
    bodies. Ceiling feed → master switch + 12V distribution block in the chase → vertical bus
    down the chase → short back-taps to each pump (behind the body). One branch runs along the
    ceiling (in the tote-free corridor lane) to the Pinhole-Wall panel → P-02.

    part="corridor" = everything EXCEPT the final EP drop (the dist block, bus, pump taps, P-02
    branch + the ceiling feed run STOPPING at the pinhole-wall trunk above the EP) — the
    construction model installs this in Phase 1, wired to the pinhole wall. part="ep_link" = just
    the EP-drop segment (+ master switch), connected in Phase 4. "all" (default) = the original
    single feed run + everything, byte-identical."""
    do_corr = part in ("all", "corridor")
    do_link = part in ("all", "ep_link")
    PWR = "#8E44AD"                                 # unique POWER conduit color (purple) — distinct from all water pipes
    cr = 7                                          # conduit radius (14mm OD)
    p = []
    TY, TZ = 20, ov.C_HGT - 13                       # pinhole-wall ceiling trunking line (Yd20), per electrical.skp
    ptop = cp.PSTACK['P-03'] + cp.PVB_H              # 1920 — top of the pump column
    BKX = cp.BACK_X + cp.EQT + 24                    # ~5146 — dist block + bus on the REVERSE of the panel (clear)
    by  = cp.CTR_Y                                    # 1181 — corridor center (tote-free, between back uprights)
    fr = ov.BB_OD / 2
    p2x = (3300 - (fr + 30)) - (cp.PVB_R + 30) - 40  # P-02 body-center X on the pinhole wall
    epx = 1979                                       # EP fuse-block C X (electrical.skp)
    swx = epx + 200                                  # 2179 — master switch 200mm toward the IBC end (clear of the EP kit)
    z_lo = cp.PSTACK['P-01'] + 90                     # 705  — lowest pump tap
    z_hi = cp.PSTACK['P-03'] + 90                     # 1830 — highest pump tap
    zc   = (z_lo + z_hi) / 2                          # 1268 — vertical center of the pump column
    # ── MASTER SWITCH on the ELECTRICAL PANEL — one cutoff upstream of EVERYTHING (avoids a
    #    corridor switch + its through-panel wiring; puts BOTH P-02 and the corridor pumps
    #    downstream of it).  Red disconnect lever like the DV handles. ──
    if include_switch:   # standalone: draw the master switch here + feed off it (swx)
        if do_link:
            p.append(ov.ruby_box("Master pump switch (Cct C, on EP)", swx - 26, 30, 1840, 52, 48, 56, color="#202020"))
            p.append(ov.ruby_box("Master switch lever (OFF cutoff)", swx - 7, 78, 1852, 14, 46, 14, color=cp.C_HANDLE))
        fx, fy, fz = swx, 54, 1896
    else:                # EP present (overview + water): feed off the EP panel's OWN master switch, ON the panel
        import generate_electrical_model as em
        fx, fy, fz = em.MASTER_SW_POS
    # ── feed: EP master switch → Yd20 ceiling trunk (per electrical.skp, clear of the center
    #    LEDs) → down to the corridor 12V DISTRIBUTION BLOCK.  Split at index 2 = (fx,TY,TZ), the
    #    pinhole-wall ceiling trunk above the EP: corridor side (Phase 1) vs EP drop (Phase 4). ──
    feed = [(fx, fy, fz), (fx, fy, TZ), (fx, TY, TZ), (p2x, TY, TZ), (BKX, TY, TZ),
            (BKX, by, TZ), (BKX, by, zc + 48)]
    if part == "all":
        p.append(ov.ruby_pipe_run("Cct C feed (EP master sw -> corridor dist block)", feed, cr, color=PWR))
    else:
        if do_link:
            p.append(ov.ruby_pipe_run("Cct C feed (EP master sw -> pinhole-wall ceiling)", feed[:3], cr, color=PWR))
        if do_corr:
            p.append(ov.ruby_pipe_run("Cct C feed (pinhole-wall ceiling -> corridor dist block)", feed[2:], cr, color=PWR))
    # ── P-02 taps the trunk directly off the master-switch feed → Pinhole-Wall panel ──
    cap_h = 78
    cap_z = ((ov.C_HGT - 48) - ov.BB_H) + ov.BB_H - cap_h / 2
    p2ty = (fr + 12) + cp.PVB_R + 8
    p2z = (cap_z - (cp.PVB_H - 18)) + cp.PVB_H / 2
    if do_corr:
        p.append(ov.ruby_pipe_run("Cct C branch P-02 (Pinhole-Wall panel)",
                 [(p2x, TY, TZ), (p2x, p2ty, TZ), (p2x, p2ty, p2z)], cr, color=PWR))
        # ── 12V DISTRIBUTION BLOCK on the REVERSE of the corridor panel + bus + back-taps to pumps ──
        p.append(ov.ruby_box("12V distribution block (Cct C, rear)", BKX - 24, by - 30, zc - 45, 48, 60, 90, color="#3A3A42"))
        # power bus down the back, with SMOOTH elbows turning into the TOP (P-03) and BOTTOM (P-01)
        # pumps as one continuous run; the two middle pumps tee off the bus.
        xin = cp.PXC + cp.PVB_R - 10                      # 5024 — tap tip, 10mm into each pump back
        p.append(ov.ruby_pipe_run("Cct C bus + P-03/P-01 elbow taps (rear)",
                 [(xin, by, z_hi), (BKX, by, z_hi), (BKX, by, z_lo), (xin, by, z_lo)], cr, color=PWR))
        for key in ("P-04", "P-05"):
            z = cp.PSTACK[key] + 90
            p.append(ov.ruby_pipe_run(f"Cct C branch {key}", [(BKX, by, z), (xin, by, z)], cr, color=PWR))
    return "\n".join(p)


# ── Phase 2: relocated tray-sump processing ROW, mounted on the FILTER SKID under the filters ──
# P-04 (sump pump) · SV-02 (sample tap) · 3W-DV-02 diverter, in a row under F1 / F2 / F3.
# Facing the pinhole wall, right→left = P-04 (low X, beside F1) → SV-02 → DV-02 (high X).
# The sump pickup feeds P-04 directly here.  SROW_YD/SROW_Z0 single-sourced above (near LABEL_POINTS).
def skid_row():
    """The relocated tray-sump processing row on the filter skid (P-04 · SV-02 · 3W-DV-02).
    Bodies only for now — plumbing (sump→P-04→SV-02→DV-02→F1 / waste) follows in Increment 2."""
    p = []
    p += cp.pump_unit("Pump P-04 (Tray drain)", ov.PWP_FILTER_X1, SROW_YD, SROW_Z0, axis="x", face=+1)
    p.append(cp.sample_valve("SV-02 sample valve", ov.PWP_FILTER_X2, SROW_YD, SROW_Z0 + 132, h=60))   # IN-LINE: row line runs THROUGH the body (center Z1312 = P-04 OUT), red handwheel free above, spout below
    p.append(cp.diverter("3W-DV-02", ov.PWP_FILTER_X3, SROW_YD, SROW_Z0 + 162,
                         run="x", branch="z+", handle="y+", color=ov.C_VALVE))   # IN −X (P-04) · waste +X (corridor) · feed z+ (F1); center Z1312 = P-04 OUT (straight run)
    # ACC-02 (recycled-spray accumulator) — on the filter skid, in P-02's vacated spot (X=PWP_P02_X); Ø127 × 200 (= ACC-01)
    p.append(ov.ruby_cylinder("ACC-02 Accumulator", ov.PWP_P02_X, ov.PWP_FILTER_YD, SROW_Z0, cp.ACC_R, 174, color=ov.C_ACC))
    p.append(ov.ruby_cylinder("ACC-02 head", ov.PWP_P02_X, ov.PWP_FILTER_YD, SROW_Z0 + 174, cp.ACC_R + 2, 26, color="#222228", axis="z"))
    # ACC-02 IN/OUT ports — ACC-01 style (horizontal, opposite sides at the body BOTTOM); on ±X here since
    # the −Yd side faces the wall.  IN +X (from the P-02 discharge), OUT −X (to BV-05 / the spray bar).
    acc2z = SROW_Z0 + 28                                 # port Z at the body bottom (= ACC-01's ACC_PZ offset)
    for tag, sd in (("in", +1), ("out", -1)):
        x0 = (ov.PWP_P02_X + cp.ACC_R) if sd > 0 else (ov.PWP_P02_X - cp.ACC_R - 30)
        p.append(ov.ruby_cylinder(f"ACC-02 {tag} port", x0, ov.PWP_FILTER_YD, acc2z, cp.RP, 30, color="#222228", axis="x"))
    return "\n".join(p)


def skid_plumbing():
    """Phase 2 — relocated tray-sump plumbing on the filter skid.  (Legs added incrementally.)"""
    p = []
    rp = ov.PUMP_PIPE_OD / 2
    cdk = "#222228"
    lz = SROW_Z0 + 162                                   # 1312 — row line AT P-04's OUT-port height (straight run, no dog-leg)
    # ── Leg 1: tray sump pickup → P-04 IN  (DIRECT — deletes the long corridor ribbon) ──
    sfz = ov.PROC_TRAY_FLOOR_Z_LOW - ov.PROC_TRAY_SUMP_Z + 3
    sfoot = (ov.PROC_TRAY_DRAIN_X, ov.PROC_TRAY_DRAIN_YD, sfz)          # (2399, 80, 3) — strainer in the well
    p04_in = cp.pump_in(ov.PWP_FILTER_X1, SROW_YD, SROW_Z0, "x", face=+1)   # (3220,130,1312)
    p.append(ov.ruby_pipe_run("Tray sump -> P-04 suction",
        [sfoot, (ov.PROC_TRAY_DRAIN_X, SROW_YD, 3),                      # +Yd along the floor to the P-04 lane, UNDER the blue supply trunk (Z41)
         (ov.PROC_TRAY_DRAIN_X, SROW_YD, 90),                           # up at Yd104 — now clear of the blue trunk (Yd69)
         (p04_in[0] - 20, SROW_YD, 90),                                 # +X UNDER THE WALKWAY (low) to below P-04
         (p04_in[0] - 20, SROW_YD, p04_in[2]),                          # VERTICAL up to P-04's IN-port height
         p04_in], rp, color=ov.C_IBC_BROWN))                           # +X into P-04's −X IN port
    p.append(ov.ruby_cylinder("Tray sump strainer foot", *sfoot, 14, 36, color=cdk, axis="z"))
    # ── Leg 2: P-04 OUT → (SV-02 tap) → DV-02 IN, along the row at lz ──
    p04_out = cp.pump_out(ov.PWP_FILTER_X1, SROW_YD, SROW_Z0, "x", face=+1)   # (3380,130,1312)
    dv_in = (ov.PWP_FILTER_X3 - (cp.DVB / 2 + cp.DVL), SROW_YD, lz)     # DV-02 −X run port (3943,130,1250)
    # the line runs THROUGH SV-02's in-line body at X2 (so no separate tap tee — the sample spout hangs below)
    p.append(ov.ruby_pipe_run("P-04 -> SV-02 -> DV-02",
        [p04_out, (dv_in[0], SROW_YD, lz)], rp, color=ov.C_IBC_BROWN))   # STRAIGHT: lz = P-04 OUT Z (no dog-leg)
    # ── Leg 3a: DV-02 feed (z+ branch) → F1 IN — the RECYCLE leg into the filter train ──
    fr = ov.BB_OD / 2
    f1_in = (ov.PWP_FILTER_X1 - (fr + 30), ov.PWP_FILTER_YD, ov.PWP_FILTER_TOP_Z - 39)   # (3178,104,2301) — matches f_in("F1")
    dv_feed = (ov.PWP_FILTER_X3, SROW_YD, lz + (cp.DVB / 2 + cp.DVL))               # DV-02 z+ branch port (3976,104,1283)
    edge_x = 2830        # near the panel's low-X (pinhole) edge
    p.append(ov.ruby_pipe_run("DV-02 feed -> F1 (recycle)",
        [dv_feed,
         (ov.PWP_FILTER_X3, ov.PWP_FILTER_YD, 1450),      # up just clear of the skid-row tops (~1360)
         (edge_x, ov.PWP_FILTER_YD, 1450),                # −X ALONG THE PANEL SURFACE (Yd104) to the pinhole edge
         (edge_x, ov.PWP_FILTER_YD, f1_in[2]),            # VERTICAL UP at the edge to F1-IN height
         f1_in], rp, color=ov.C_IBC_BROWN))               # +X into F1's −X IN port
    # ── Leg 3b: DV-02 waste (+X port) → IBC-4 (corridor), UNDER THE WALKWAY via the ribbon ──
    # Mirrors the (now-freed) tray-sump ribbon path: out to the near-rim lane FIRST (clear of the tray
    # basin), drop, +X under the walkway to lane 2, up-and-over the cantilever, down into the corridor,
    # then rise onto the IBC-4 merge tee.
    RZ, OVZ = cp.RIBBON_Z, cp.RIBBON_OVER_Z
    wlx   = cp.RIBBON_LANE_X[2]                           # lane 2 — freed now the sump goes direct to P-04
    gapyd = ov.RWK_RIBBON_NOTCH_YDS[2]                    # 1194 — lane-2 outer-beam notch Yd (single-sourced)
    CLIPY = 35                                            # clip plane — flush to the ply (= the F3→SV-01 filtered-line Yd), so the grey clamps to the panel
    hx    = ov.PWP_SV01_X                                 # 4250 — F3→SV-01 filtered line X (the crossing to hump over)
    dv_waste = (ov.PWP_FILTER_X3 + (cp.DVB / 2 + cp.DVL), SROW_YD, lz)   # DV-02 +X waste port (4054,104,1312)
    riseX = cp.MERGE4[0] - 115                            # 5289 — seat-approach X (= old DV-02→IBC-4 drop lane, −x of the tee)
    p.append(ov.ruby_pipe_run("DV-02 waste -> IBC-4",
        [dv_waste,
         (dv_waste[0] + 36, SROW_YD, lz),                 # +X lead-out off the +X waste port
         (dv_waste[0] + 36, CLIPY, lz),                   # −Yd onto the clip plane (flat on the ply — clamped)
         (hx - 100, CLIPY, lz),                            # +X ALONG THE PLY SURFACE to the F3→SV-01 crossing (widened to span the in-line SV-01 dog-legs at svx±60)
         (hx - 100, CLIPY + 35, lz),                       # HUMP over the F3→SV-01 verticals — elbow 1 (+Yd, proud of the panel)
         (hx + 85, CLIPY + 35, lz),                       # elbow 2 (over the filtered line)
         (hx + 85, CLIPY, lz),                            # elbow 3 (−Yd back onto the ply)
         (wlx, CLIPY, lz),                                # elbow 4 → +X along the ply to lane 2 (clamped to the extended ply, up to the bend)
         (wlx, 65, lz),                                   # +Yd clear of the RWk end beam (Yd0) before dropping
         (wlx, 65, RZ),                                   # DROP between the walkway beams into the ribbon (past the end beam, in front of the tray box)
         (wlx, cp.RIBBON_YD_UP, RZ),                      # +Yd along the lane (under the grate) to before the cantilever
         (wlx, cp.RIBBON_YD_UP, OVZ),                     # UP over the cantilever (Rule 5)
         (wlx, cp.RIBBON_YD_DOWN, OVZ),                   # +Yd past the cantilever
         (wlx, cp.RIBBON_YD_DOWN, RZ),                    # DOWN through the grate into the corridor
         (wlx, gapyd, RZ),                                # +Yd to the notch Yd (flush under the grate)
         (cp.RIBBON_SLOT_X, gapyd, RZ),                   # +X through the outer-beam notch to the drop slot
         (cp.RIBBON_SLOT_X, gapyd, 65),                   # DOWN the slot to the corridor entry Z
         (riseX, gapyd, 65),                              # +X to the merge-approach lane
         (riseX, cp.MERGE4[1], 65),                       # jog to the merge Yd at floor
         (riseX, cp.MERGE4[1], cp.MERGE4[2]),             # RISE to the merge Z (1230)
         cp.MERGE4], rp, color=ov.C_IBC_WASTE))           # +X onto the tee's −x run port
    # ── Leg 4: P-02 discharge (corridor) → ACC-02 (skid) — the recycle-spray feed, UNDER THE WALKWAY ──
    # Reverse of the waste leg: off P-02's +Yd OUT, drop into the corridor, ribbon lane 0 back under the
    # walkway to the near rim, then −X along the near rim to the skid and up into ACC-02's bottom IN.
    p2o = cp.pump_out(cp.PXC, cp.CTR_Y, cp.PSTACK["P-04"], "y", 1)      # P-02 OUT (+Yd) (4984,1261,1102)
    L0  = cp.RIBBON_LANE_X[0]                                           # lane 0 (free)
    g0  = ov.RWK_RIBBON_NOTCH_YDS[0]                                    # lane-0 outer-beam notch Yd
    acc2_in = (ov.PWP_P02_X + cp.ACC_R + 30, ov.PWP_FILTER_YD, SROW_Z0 + 28)   # ACC-02 +X IN-port tip (3151.5,104,1178)
    exitX = 4900                                                        # −X of the ACC-01/P-01 column (bodies X≥4921) so the drop clears them
    cpt = (4630, g0, 65)                                                # ribbon entry −X of the near upright (X4646); ribbon_run does the +X to the slot + the notch
    npt = (L0, 65, RZ)                                                  # near-rim junction (Yd65, clear of the end beam)
    lead  = [p2o, (p2o[0], p2o[1] + 30, p2o[2]),                        # +Yd OUT of the +Yd OUT port (stub-collinear) — swept elbow at the next vertex
             (exitX, p2o[1] + 30, p2o[2]),                              # −X OUT of the pump column (+Yd side, above P-01/ACC-01)
             (exitX, p2o[1] + 30, 65),                                  # DROP to the corridor entry Z, clear of the column
             (exitX, cp.CTR_Y, 65),                                     # −Yd to mid-gap Yd1181 (clear of BOTH uprights: 1046-1096 & 1258-1266)
             (cpt[0], cp.CTR_Y, 65),                                    # −X across the uprights' X-span at mid-gap Yd
             cpt]                                                       # −Yd to the notch Yd (1110) on the −X side of the near upright
    cross = cp.ribbon_run(0, cpt, npt)                                  # cpt → over the cantilever → npt
    rX = ov.PWP_P02_X + cp.ACC_R + 54                                   # 3175.5 — riser +X of the IN tip, −X of the sump Leg-1 riser (X3200)
    tail  = [npt, (L0, 65, 65),                                         # drop below the walkway-beam soffit (Z80)
             (rX, 65, 65),                                             # −X UNDER the walkway beams to the riser X (at Yd65)
             (rX, 65, 110),                                            # UP at Yd65 above the sump Leg-1 horizontal (Z90)
             (rX, ov.PWP_FILTER_YD, 110),                              # +Yd onto the ACC-02 wall lane (above Leg 1)
             (rX, ov.PWP_FILTER_YD, acc2_in[2]),                       # UP to the IN-port height
             acc2_in]                                                  # −X into the +X IN port (swept elbow at the vertex)
    p.append(ov.ruby_pipe_run("P-02 -> ACC-02 (recycle spray)",
        lead[:-1] + cross + tail[1:], rp, color=ov.C_IBC_BROWN))
    # ── Leg 5: ACC-02 OUT (−X) → 3W-BV-05 recycled port — closes the recycle-spray loop ──
    acc2_out = (ov.PWP_P02_X - cp.ACC_R - 30, ov.PWP_FILTER_YD, SROW_Z0 + 28)   # ACC-02 −X OUT tip (2964.5,104,1178)
    b5rx = (ov.BV02_X - 150) + (cp.DVB / 2 + cp.DVL)                             # BV-05 +X recycled port tip X (2282)
    p.append(ov.ruby_pipe_run("ACC-02 -> BV-05 (recycled spray)",
        [acc2_out,                                          # off ACC-02's −X OUT port (collinear)
         (b5rx + 40, ov.PWP_FILTER_YD, acc2_out[2]),        # −X along the panel to just +X of the BV-05 port
         (b5rx + 40, 350, acc2_out[2]),                     # +Yd to the BV-05 selector lane (Yd350)
         (b5rx + 40, 350, 1150),                            # down to the port height
         (b5rx, 350, 1150)], rp, color=ov.C_IBC_BROWN))     # −X into the +X recycled port
    return "\n".join(p)


def build():
    # Limited-depth view of the FULL pinhole wall: the wet-end kit + the OTHER wall-mounted
    # equipment (own layer/scene) + a shallow context slice (wall + floor/ceiling out to
    # 300mm past the walkway) + scale figure.  Two scenes: wet end / other equipment.
    comps, tags = [], set()
    # (name, tag, builder) — builders whose tag is in MUTE_TAGS build muted at source via ov.muted().
    for name, tag, builder in [("Context", "Context", context),
                         ("Walkways + cantilevers + brackets", "Walkway", walkway_full),
                         ("Film-plane support beams", "Film Plane", film_plane_beams),
                         ("Processing tray (ghost)", "Processing Tray", ov.processing_tray),
                         ("Spray Bar", "Spray Bar", spray_bar),
                         ("IBC Tanks (full)", "IBC", lambda: ov.ibc_stack(alpha=MUTE_ALPHA, mute=MUTE_DESAT)),
                         ("IBC restraint (bars + wall anchors)", "IBC Frame", cp.tote_restraint),
                         ("End wall (context)", "Context", cp.end_wall),
                         ("Pinhole Assembly", "Pinhole", ov.pinhole_assembly),
                         ("Wall backing (ply)", "Backing", backing),
                         ("TAP-01 + spray-bar supply", "Supply", tap01_supply),
                         ("Wet-end kit (raked)", "Kit", lambda: kit(p02_on_corridor=True)),
                         ("Skid row (P-04 · SV-02 · DV-02)", "Kit", skid_row),
                         ("Skid plumbing", "Kit", skid_plumbing),
                         ("Person (scale)", "Scale", person),
                         ("Other pinhole-wall equipment", "Pinhole Equipment", other_equipment),
                         ("Corridor frame (deep box)", "Corridor Frame", cp.frame),
                         ("Corridor rear panel", "Corridor Panel", cp.rear_panel),
                         ("Corridor equipment", "Corridor Equipment", lambda: cp.equipment(sump_on_skid=True)),
                         ("Corridor plumbing", "Corridor Plumbing", lambda: cp.plumbing(sump_on_skid=True)),
                         ("Corridor drains + X-ports", "Corridor Drains", lambda: cp.drains_ports(sump_on_skid=True)),
                         ("Circuit-C power + cabling (both panels)", "Power", lambda: panel_power(include_switch=False)),
                         ("Ribbon support cross-beams", "Ribbon Supports", cp.ribbon_supports),
                         # SOLID (non-ghost) copies of the two plywood panels, on their own tags — shown
                         # only in the "Plumbing (labeled)" scene so the panels read full-color there while
                         # the overview scenes keep the muted "Corridor Panel"/"Backing" versions.
                         ("Corridor panel (solid)", "Corridor Panel Solid", cp.rear_panel),
                         ("Wall backing (solid)", "Backing Solid", backing)]:
        if tag in MUTE_TAGS:
            with ov.muted(MUTE_DESAT, MUTE_ALPHA):
                b = builder()
        else:
            b = builder()
        comps.append(ov.component(name, tag, b)); tags.add(tag)
    tags.add("Labels"); tags.add("Labels Context")
    body = "\n".join(comps)
    tags_ruby = "".join(f'  model.layers.add({t!r}) unless model.layers[{t!r}]\n' for t in sorted(tags))
    return f'''# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/ — do not edit this .rb directly.
model = Sketchup.active_model
model.start_operation("Pinhole-wall layout", true)
entities = model.active_entities
to_erase = entities.to_a.select {{ |e| e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text) || e.is_a?(Sketchup::ConstructionLine) || e.is_a?(Sketchup::ConstructionPoint) || e.is_a?(Sketchup::Edge) }}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each {{ |pg| model.pages.erase(pg) }}
opts = model.options["UnitsOptions"]; opts["LengthUnit"]=2; opts["LengthFormat"]=0
{ov.sketchfab_meta_ruby(SF_TITLE, SF_DESC, SF_ID, SF_TAGS, force_name=True)}
{tags_ruby}{body}
# remove the FAR walkway deck AND its cantilever brackets (not wanted in this view)
model.definitions.each {{ |d| d.entities.grep(Sketchup::Group).each {{ |g| g.erase! if g.valid? && g.name =~ /^Walkway Far/ }} }}
# in-model callout labels on the 'Labels' tag (shown only in the Labeled scene)
{labels_ruby()}
v = model.active_view
v.camera = Sketchup::Camera.new(Geom::Point3d.new(800.mm, 6000.mm, 2300.mm), Geom::Point3d.new(2950.mm, 200.mm, 1100.mm), Geom::Vector3d.new(0,0,1), false, 52)
# Context/backdrop is built muted AT SOURCE (ov.muted() wraps the MUTE_TAGS builders above), so no
# post-build re-coloring pass is needed.  Keep ModelTransparency OFF so the per-material alpha renders
# as translucency (not a global X-ray that would leak across scenes).
model.rendering_options["ModelTransparency"] = false
def scene(model, name, on)
  model.layers.each {{ |l| l.visible = (l.name == "Layer0" || l == model.layers[0] || on.include?(l.name)) }}
  pg = model.pages.add(name, 4095)
  pg.use_hidden_layers = true rescue nil
  pg
end
scene(model, "Overview", ["Context","Walkway","Film Plane","Processing Tray","Spray Bar","IBC","IBC Frame","Pinhole","Backing","Supply","Kit","Scale","Pinhole Equipment","Corridor Frame","Corridor Panel","Corridor Equipment","Corridor Plumbing","Corridor Drains","Power"])
scene(model, "Plumbing", ["Kit","Supply","Corridor Equipment","Corridor Plumbing","Corridor Drains","Power"])
scene(model, "Plumbing (labeled)", ["Kit","Supply","Corridor Equipment","Corridor Plumbing","Corridor Drains","Power","Labels","Corridor Panel Solid","Backing Solid"])
scene(model, "Plumbing + IBC", ["Kit","Supply","Corridor Equipment","Corridor Plumbing","Corridor Drains","Power","IBC","IBC Frame","Corridor Frame","Corridor Panel","Walkway"])
scene(model, "Labeled", ["Context","Walkway","Film Plane","Processing Tray","Spray Bar","IBC","IBC Frame","Pinhole","Backing","Supply","Kit","Scale","Pinhole Equipment","Corridor Frame","Corridor Panel","Corridor Equipment","Corridor Plumbing","Corridor Drains","Power","Labels","Labels Context"])
model.layers.each {{ |l| l.visible = true }}
model.commit_operation
{{ ok: true }}.to_json
'''


SKP_PATH = os.path.abspath(os.path.join(_ROOT, "models", "water.skp"))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--send", action="store_true", help="build into the ACTIVE SketchUp doc (open a blank doc first!)")
    ap.add_argument("--save", action="store_true", help="after building, save the active doc as models/water.skp")
    a = ap.parse_args()
    ruby = build()
    if a.send:
        from sketchup_client import send_ruby
        print(send_ruby(ruby))
        if a.save:
            print(send_ruby(f'Sketchup.active_model.save({SKP_PATH!r}) ? "saved {SKP_PATH}" : "FAIL"'))
    else:
        print(ruby[:400])
