#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""Structural validation of the TBS-001 perimeter walkway (Phase A of the walkway blueprint).

US IBC/OSHA load basis — IBC-2021 Table 1607.1 (walkways / elevated platforms &
"stairs and exitways"): a 60 psf (2.87 kPa) uniform live load AND a 300 lbf (1.33 kN)
concentrated load applied over a small area at the location producing maximum stress.
Per IBC 1607.1 the concentrated load need NOT be combined with the uniform load — each
member is designed for the worse of the two. For a cantilever the concentrated load at
the free tip governs every arm here.

Sources (every capacity/coefficient cited):
  - IBC-2021 Table 1607.1 minimum live loads
    https://codes.iccsafe.org/content/IBC2021P2/chapter-16-structural-design#IBC2021P2_Ch16_Sec1607
  - OSHA 29 CFR 1910.28/1917 walking-working surfaces (workplace overlay of the same case)
  - Fibergrate molded FRP grating load tables (1" deep, 1"x4" mesh)
    https://www.fibergrate.com/Docs/ProductFiles/load_tables/fgload.pdf
  - Steel A36 / A500B mild steel Fy = 250 MPa; M12 Gr.8.8 Fub = 800 MPa (shared with ibc_frame_load)

Reuses the right-walkway ARM + long-BEAM checks from ibc_frame_load.py — the arm->IBC-upright
connection (joint J6) is IBC-frame-owned (drawn on IBC-frame Sheet 5), so it is CROSS-REFERENCED
here, not re-validated.

Run:  python3 src/generators/walkway_load.py              # print the full validation report
      python3 src/generators/walkway_load.py --inject     # fill the §9 table in walkway-report.md
      python3 src/generators/walkway_load.py --check-blocks
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tbs_constants as k  # noqa: E402
from ibc_frame_load import z_rhs, AS_M12, FUB_88, arm_notch_check, outer_beam_frame_check, service_loads

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_REPORT = os.path.join(_ROOT, "walkway-report.md")

# ── Load basis (US IBC/OSHA — IBC Table 1607.1) ──────────────────────────────
PSF = 47.880259           # 1 lbf/ft^2 -> Pa
LBF = 4.4482216           # 1 lbf -> N
LL_PSF = 60.0             # uniform live load (psf)
LL = LL_PSF * PSF / 1e6   # -> N/mm^2  (2.873e-3)
P_CONC = 300.0 * LBF      # concentrated live load -> 1334 N
SPACING = float(k.WALKWAY_BRACKET_SPACING)   # 457 mm — bracket tributary width

FY = 250.0                # A36 / A500B mild-steel yield (MPa)
E = 200000.0              # steel modulus (MPa)
SF_TARGET = 2.0           # design target on yield (conservative vs code ASD Ω=1.67)

# ── FRP grate (Fibergrate 1" deep, 1"x4" mesh molded — fgload.pdf) ───────────
# At the shortest tabulated span (12" = 305 mm) the 1"x4" grate carries a MAX RECOMMENDED
# uniform load of 2,360 psf (deflection <0.01" at 100 psf); the 300 lb concentrated point at
# 18" span deflects 0.03" (0.8 mm).  Our clear spans (245 mm right / 300 mm near-far) are AT or
# BELOW the shortest tabulated span, so the grate is stiffer/stronger than any tabulated value.
GRATE_MAXREC_PSF = 2360.0
GRATE_CONC_DEFL_MM = 0.8   # 300 lb @ 18" span (conservative; our span is shorter)


def _z_solid(w, h):
    """Elastic section modulus (mm^3) of a solid rectangle, depth h in the bending direction."""
    return w * h * h / 6.0


def _i_rhs(w, h, t):
    """Second moment (mm^4) of a rectangular hollow section, bending about the axis ⟂ depth h."""
    return z_rhs(h, w, t) * h / 2.0


# Each check appends a row (element, demand, capacity, SF, note) and returns a printable block.
ROWS = []


def _row(elem, demand, cap, sf, note):
    ROWS.append((elem, demand, cap, sf, note))


def _cant_arm(reach_mm, w, h, t, label):
    """Cantilever tube arm under the 300 lbf tip point load: moment, capacity, SF, tip deflection."""
    m = P_CONC * reach_mm / 1e3                        # N·m
    z = z_rhs(h, w, t)
    mcap = z * FY / 1e3                                # N·m at yield
    sf = mcap / m
    d = P_CONC * reach_mm ** 3 / (3 * E * _i_rhs(w, h, t))
    return m, mcap, sf, d, f"{label} ({w:.0f}×{h:.0f}×{t:.2f} tube, {reach_mm:.0f} mm cant.)"


# ── 1. Grate span ────────────────────────────────────────────────────────────
def grate_check():
    span = k.WALKWAY_RIGHT_W   # 245 — the shortest (worst) clear span
    sf_unif = GRATE_MAXREC_PSF / LL_PSF
    _row("Grate — uniform", f"{LL_PSF:.0f} psf",
         f"{GRATE_MAXREC_PSF:.0f} psf max-rec", f"{sf_unif:.0f}",
         "Fibergrate 1\" 1×4 molded FRP; span ≤ 12\" tabulated min")
    _row("Grate — concentrated", "300 lbf",
         f"{GRATE_CONC_DEFL_MM:.1f} mm defl", "—",
         "0.03\" @ 18\" span (Fibergrate); less at our shorter span")
    return ("\n## 1. GRATE — molded FRP 1\" 1×4 (Fibergrate load tables) ##\n"
            f"  clear span {span} mm (right deck; near/far {k.WALKWAY_W} mm) — below the 12\" tabulated minimum\n"
            f"  uniform: {LL_PSF:.0f} psf demand vs {GRATE_MAXREC_PSF:.0f} psf max-recommended  -> SF {sf_unif:.0f}; deflection <0.01\" (~0.25 mm) at 100 psf\n"
            f"  concentrated: 300 lbf ~{GRATE_CONC_DEFL_MM:.1f} mm at 18\" span (our span shorter => stiffer). Grate is not the governing element.")


# ── 2-3. Wall-cantilever bracket ARMS (redesigned to IBC/OSHA) ───────────────
def wall_bracket_check():
    ms, mcs, sfs, ds, ls = _cant_arm(k.WALKWAY_W, k.WALKWAY_BRACKET_ARM_W,
                                     k.WALKWAY_BRACKET_ARM_H, k.WALKWAY_BRACKET_ARM_T, "STD arm")
    mw, mcw, sfw, dw, lw = _cant_arm(k.WALKWAY_NEAR_WIDE_W, k.WALKWAY_BRACKET_ARM_W_WIDE,
                                     k.WALKWAY_BRACKET_ARM_H, k.WALKWAY_BRACKET_ARM_T, "WIDE arm")
    _row("Wall bracket STD arm", f"{ms:.0f} N·m", f"{mcs:.0f} N·m", f"{sfs:.2f}",
         f"2×1×0.120 tube, {k.WALKWAY_W} mm; tip defl {ds:.1f} mm (L/{k.WALKWAY_W/ds:.0f})")
    _row("Wall bracket WIDE arm", f"{mw:.0f} N·m", f"{mcw:.0f} N·m", f"{sfw:.2f}",
         f"3×1×0.120 tube, {k.WALKWAY_NEAR_WIDE_W} mm; deflection-governed, tip L/{k.WALKWAY_NEAR_WIDE_W/dw:.0f}")
    return ("\n## 2-3. WALL-CANTILEVER BRACKET ARMS (redesigned; arm depth spray-bar-capped at 25.4 mm) ##\n"
            f"  {ls}: 300 lbf tip -> M {ms:.0f} N·m  cap {mcs:.0f} N·m  SF {sfs:.2f}  |  tip defl {ds:.1f} mm (L/{k.WALKWAY_W/ds:.0f})\n"
            f"  {lw}: 300 lbf tip -> M {mw:.0f} N·m  cap {mcw:.0f} N·m  SF {sfw:.2f}  |  tip defl {dw:.1f} mm (L/{k.WALKWAY_NEAR_WIDE_W/dw:.0f} — governs the widened bracket)\n"
            "  (the as-drawn 8×10 plate arm yielded at ~25 lbf; the tube arm is the redesign.)")


# ── 4-5. Wall bolt group + corrugated-wall pull-through ──────────────────────
def wall_bolt_check():
    # Root moment (concentrated, standard bracket) reacted as a tension-compression couple on the
    # wall bolts: upper bolt(s) tension at Z155, lower bear/compress at Z42 -> lever ~113 mm.
    lever = k.WALKWAY_BRACKET_UPPER_BOLT_Z - k.WALKWAY_BRACKET_BOLT_Z_LO   # 113
    m_std = P_CONC * k.WALKWAY_W / 1e3
    t_up = m_std * 1e3 / lever                       # 1 upper bolt (std triangular pattern)
    t_cap = 0.9 * FUB_88 * AS_M12                     # M12 8.8 tensile (proof) capacity, N
    sf_bolt = t_cap / t_up
    # Corrugated-rib pull-through: the tension punches the 1.6 mm Corten rib around the M12 washer
    # (OD ~24 mm).  Punching-shear perimeter × thickness × 0.6·Fu (Corten Fu ~450 MPa, use 350 shear-safe).
    wall_t, wsh_od, fu_shear = 1.6, 24.0, 0.6 * 350.0
    cap_pt = 3.14159 * wsh_od * wall_t * fu_shear
    sf_pt = cap_pt / t_up
    _row("Wall bolt tension (M12 8.8)", f"{t_up:.0f} N", f"{t_cap:.0f} N", f"{sf_bolt:.0f}",
         f"root-moment couple, {lever:.0f} mm lever")
    _row("Corrugated-rib pull-through", f"{t_up:.0f} N", f"{cap_pt:.0f} N", f"{sf_pt:.0f}",
         "1.6 mm rib punch over M12 washer; needs ≥30 mm corrugation for grip")
    return ("\n## 4-5. WALL BOLT GROUP + CORRUGATED-RIB PULL-THROUGH ##\n"
            f"  root moment {m_std:.0f} N·m -> upper-bolt tension {t_up:.0f} N (lever {lever:.0f} mm)\n"
            f"  M12 8.8 tension cap {t_cap:.0f} N  SF {sf_bolt:.0f}   |   1.6 mm-rib pull-through cap {cap_pt:.0f} N  SF {sf_pt:.0f}\n"
            f"  (pull-through is contingent on the {k.CONTAINER_CORRUGATION_DEPTH} mm corrugation for bolt grip — the parked procurement gate.)")


# ── 6-9. Left-walkway FLOOR-LEG cantilever (arm + post + foot anchors) ────────
def floor_leg_check():
    arm_x0 = k.LEFT_WK_CANT_LEG_X + k.LEFT_WK_CANT_POST / 2
    l_std = k.LEFT_WK_CANT_STD_REACH - arm_x0
    l_wide = k.LEFT_WK_CANT_WIDE_REACH - arm_x0
    ms, mcs, sfs, ds, _ = _cant_arm(l_std, k.LEFT_WK_CANT_ARM_W,
                                    k.WALKWAY_BRACKET_ARM_H, k.WALKWAY_BRACKET_ARM_T, "std")
    mw, mcw, sfw, dw, _ = _cant_arm(l_wide, k.LEFT_WK_CANT_ARM_W_WIDE,
                                    k.WALKWAY_BRACKET_ARM_H, k.WALKWAY_BRACKET_ARM_T, "wide")
    # Post 2x2x0.120 — moment at its base = the worst (widened) tip load × reach
    zp = z_rhs(k.LEFT_WK_CANT_POST, k.LEFT_WK_CANT_POST, k.LEFT_WK_CANT_POST_T)
    m_post = mw
    sf_post = zp * FY / 1e3 / m_post
    # Foot anchors: overturning couple reacted by the 2 outboard #14 screws over the foot length
    foot_l = k.LEFT_WK_CANT_FOOT[0]
    t_anchor = m_post * 1e3 / foot_l / 2.0
    _row("Floor-leg STD arm", f"{ms:.0f} N·m", f"{mcs:.0f} N·m", f"{sfs:.2f}",
         f"2×1×0.120, {l_std:.0f} mm cant.")
    _row("Floor-leg punch-out arm", f"{mw:.0f} N·m", f"{mcw:.0f} N·m", f"{sfw:.2f}",
         f"4×1×0.120, {l_wide:.0f} mm cant. (redesign; 2×1 was SF 1.04)")
    _row("Floor-leg post", f"{m_post:.0f} N·m", f"{zp * FY / 1e3:.0f} N·m", f"{sf_post:.2f}",
         "2×2×0.120 SHS")
    _row("Foot-anchor uplift", f"{t_anchor:.0f} N/screw", "engage steel pan", "≈1",
         f"4× #14 SS self-driller; 2 outboard react the couple over the {foot_l:.0f} mm foot")
    return ("\n## 6-9. LEFT-WALKWAY FLOOR-LEG CANTILEVER (arm + post + foot anchors) ##\n"
            f"  STD arm 2×1 {l_std:.0f} mm: M {ms:.0f} N·m cap {mcs:.0f} SF {sfs:.2f}\n"
            f"  PUNCH-OUT arm 4×1 {l_wide:.0f} mm: M {mw:.0f} N·m cap {mcw:.0f} SF {sfw:.2f}  (redesigned; the 2×1 was SF 1.04)\n"
            f"  post 2×2×0.120: M_base {m_post:.0f} N·m cap {zp * FY / 1e3:.0f} SF {sf_post:.2f}\n"
            f"  foot anchors: ~{t_anchor:.0f} N/screw uplift — the #14 self-drillers MUST engage the steel floor pan (not plywood alone).")


# ── 10. Combined corner plate (shared walkway beam + film rail) ──────────────
def corner_plate_check():
    # The RWK closed rectangle sheds its deck load to 4 corners + 2 mid-span arms. A conservative
    # corner reaction = a person (300 lbf) standing at a corner + the corner's share of the deck.
    deck_uniform = LL * k.WALKWAY_RIGHT_W * (float(k.C_WID) if hasattr(k, "C_WID") else 2388.0)  # N (whole deck)
    r_corner = P_CONC + deck_uniform / 6.0            # person + 1/6 of the deck (4 corners + 2 arms)
    # 10 mm plate on 4× M12 to the wall: bolt shear governs; group cap is huge.
    bolt_cap = 4 * 0.6 * FUB_88 * AS_M12
    sf = bolt_cap / r_corner
    _row("Combined corner plate", f"{r_corner:.0f} N", f"{bolt_cap:.0f} N", f"{sf:.0f}",
         "10 mm plate, 4× M12; shared with the BR film rail")
    return ("\n## 10. COMBINED CORNER PLATE (right corners — shared with the bottom film rail) ##\n"
            f"  corner reaction ~{r_corner:.0f} N (person + deck share) vs 4× M12 shear {bolt_cap:.0f} N  SF {sf:.0f}\n"
            "  10 mm plate, permanently bolted; non-governing.")


# ── 11-12. Right cantilever rectangle + arm->upright J6 (cross-referenced) ────
def cross_refs():
    _row("RWK long beam (cross-ref)", "person + grate", "SF 7.1", "7.1",
         "ibc_frame_load.outer_beam_frame_check — simply-supported full section")
    _row("RWK arm half-lap notch (cross-ref)", "334 N·m", "SF 2.03", "2.03",
         "ibc_frame_load.arm_notch_check — solid-bar rebalanced split")
    _row("Arm→upright J6 (IBC-owned)", "395 N·m", "SF 20", "20",
         "ibc_frame_load.service_loads — drawn on IBC-frame Sheet 5, cross-ref only")
    return ("\n## 11-12. RIGHT CANTILEVER RECTANGLE + ARM→UPRIGHT J6 (cross-referenced) ##\n"
            "  The right-walkway long/end beams + the arm half-lap notch are validated in\n"
            "  ibc_frame_load.py (outer_beam_frame_check / arm_notch_check); the arm→IBC-upright\n"
            "  connection (joint J6) is IBC-frame-owned (IBC-frame Sheet 5) — cross-referenced, not re-checked here.")


# ── Phase B: fastener schedule (WF#) ─────────────────────────────────────────
# Walkway-scoped marks (WF/WW) so they can't collide with the IBC-frame J1–J9 / W1–W5.
# Torque for M12 Gr.8.8 through the (dry) corrugated wall ~90 N·m (matches the IBC J3/J6 wall bolts).
FASTENERS = [
    ("WF1", "Standard bracket → wall rib", "M12×65 hex, [91280A728](https://www.mcmaster.com/91280A728/)",
     "Gr.8.8 zinc", "3/brkt × 13 = 39", "~90 N·m", "flat both ends", "plain nut + split-lock"),
    ("WF2", "Widened bracket → wall rib", "M12×65 hex, [91280A728](https://www.mcmaster.com/91280A728/)",
     "Gr.8.8 zinc", "4/brkt × 5 = 20", "~90 N·m", "flat both ends", "plain nut + split-lock"),
    ("WF3", "Right-walkway wall cleat + combined corner plate → wall", "M12×70 hex, [91280A732](https://www.mcmaster.com/91280A732/)",
     "Gr.8.8 zinc", "20", "~90 N·m", "flat both ends", "plain nut + split-lock"),
    ("WF4", "Floor-leg foot plate → container floor", "#14×2″ HWH self-driller",
     "410 SS", "4/foot × 5 = 20", "driven to seat (no torque spec)", "bonded washer", "thread-forming (self-locking)"),
    ("WF5", "Grating hold-down clip → bracket arm", "M-type FRP grating clip + bolt",
     "316 SS", "pitch TBD — Phase D (McNichols clip datasheet)", "snug", "—", "—"),
]


def fastener_table_md():
    lines = ["| Mark | Joint | Fastener | Grade | Qty | Torque | Washer | Locker |",
             "|------|-------|----------|-------|-----|--------|--------|--------|"]
    for r in FASTENERS:
        lines.append("| " + " | ".join(r) + " |")
    lines.append("| J6 (IBC-owned) | Center-arm end-plate → IBC upright + half-lap hold-down | "
                 "M12×100 + #14 TEK | Gr.8.8 / 410 SS | cross-ref | — | — | see IBC-frame Sheet 5 |")
    return "\n".join(lines)


# ── Phase B: weld schedule (WW#) ─────────────────────────────────────────────
FU_WELD = 480.0   # E70xx electrode ultimate (MPa)


def _fillet_cap_permm(leg):
    """Fillet-weld capacity per mm of length (N/mm) at throat = 0.707·leg, shear 0.6·Fu."""
    return 0.707 * leg * 0.6 * FU_WELD


def _moment_weld(m_nm, depth_mm, weld_len_mm, leg):
    """A root moment carried as a tension/compression couple over the section depth: the flange
    weld (weld_len long) sees force M/depth. Returns (demand N/mm, cap N/mm, SF)."""
    dem = (m_nm * 1e3 / depth_mm) / weld_len_mm
    cap = _fillet_cap_permm(leg)
    return dem, cap, cap / dem


def weld_rows():
    """(mark, joint, leg, note-with-SF). Governing throats load-checked; the rest AWS D1.1 minimums."""
    # WW1 std bracket ARM(2×1)→leg: root moment 400 N·m over the tube depth 25.4, top weld 50.8 long.
    d1, c1, sf1 = _moment_weld(P_CONC * k.WALKWAY_W / 1e3, k.WALKWAY_BRACKET_ARM_H, k.WALKWAY_BRACKET_ARM_W, 5)
    # WW2 widened ARM(3×1)→leg: 667 N·m, top weld 76.2 long.
    d2, c2, sf2 = _moment_weld(P_CONC * k.WALKWAY_NEAR_WIDE_W / 1e3, k.WALKWAY_BRACKET_ARM_H, k.WALKWAY_BRACKET_ARM_W_WIDE, 5)
    # WW6 floor-leg punch-out ARM(4×1)→post: 807 N·m, top weld 101.6 long.
    arm_x0 = k.LEFT_WK_CANT_LEG_X + k.LEFT_WK_CANT_POST / 2
    m_fl = P_CONC * (k.LEFT_WK_CANT_WIDE_REACH - arm_x0) / 1e3
    d6, c6, sf6 = _moment_weld(m_fl, k.WALKWAY_BRACKET_ARM_H, k.LEFT_WK_CANT_ARM_W_WIDE, 5)
    # WW7 floor-leg post→foot: same base moment over the 50.8 post depth, top weld 50.8 long.
    d7, c7, sf7 = _moment_weld(m_fl, k.LEFT_WK_CANT_POST, k.LEFT_WK_CANT_POST, 5)
    return [
        ("WW1", "Std bracket 2×1 arm → 8mm leg (GOVERNING)", "5mm all-round",
         f"root M {P_CONC*k.WALKWAY_W/1e3:.0f} N·m → {d1:.0f} N/mm vs {c1:.0f} N/mm, SF {sf1:.1f}"),
        ("WW2", "Widened 3×1 arm → 10mm leg (GOVERNING)", "5mm all-round",
         f"root M {P_CONC*k.WALKWAY_NEAR_WIDE_W/1e3:.0f} N·m → SF {sf2:.1f}"),
        ("WW3", "Gusset → leg + gusset → arm", "5mm", "braces the arm root; AWS D1.1 min for 8/10mm plate"),
        ("WW4", "Reinforcing plate → exterior wall panel", "5mm stitched", "bearing plate; nominal load, AWS D1.1 min"),
        ("WW5", "Rectangle long ↔ end-beam corners (right walkway)", "5mm", "closed-frame corners; AWS D1.1 min (tube ≤6mm)"),
        ("WW6", "Floor-leg 4×1 arm → 2×2 post (GOVERNING)", "5mm all-round",
         f"root M {m_fl:.0f} N·m → {d6:.0f} N/mm vs {c6:.0f} N/mm, SF {sf6:.1f}"),
        ("WW7", "Floor-leg post → foot plate (GOVERNING)", "5mm all-round",
         f"base M {m_fl:.0f} N·m → SF {sf7:.1f}; also carries the {P_CONC:.0f} N vertical in shear"),
        ("WW8", "Wall cleat — back-plate + shelf + upstand", "5mm", "AWS D1.1 min; the long beam bears on the shelf, TEK-locked"),
        ("WW9", "Combined corner plate — beam seat + upstand", "5mm", "AWS D1.1 min; shared with the BR film rail"),
        ("J6/W (IBC-owned)", "Half-lap seat + arm end-plate welds", "5mm", "IBC-frame schedule — cross-ref, not scheduled here"),
    ]


# ── Phase C: datum + tolerance scheme ────────────────────────────────────────
# Datums registered to the container + the film plane so the walkway lands in the same frame as the
# subsystems it interfaces (the spray bar, the film-plane rail).  General weldment tolerance = ISO 13920
# Class B; welds = AWS D1.1.  Functional (tighter) tolerances are listed per critical feature.
def datums_md():
    return "\n".join([
        "| Datum | Definition | References |",
        "|-------|-----------|------------|",
        "| **A** | Floor plane — the container floor / foot-plate undersides (Z0) | all heights: deck Z140, arm top Z115, bolt Z42/Z155, beam soffit Z89.6 |",
        f"| **B** | The two long wall faces — pinhole wall (Yd0) + film-plane wall (Yd{int(k.C_WID)}) interior faces the brackets bolt to | all Yd bracket/deck positions, bracket spacing 457 |",
        f"| **C** | Rail datum — film-plane rail X{int(k.RAIL_X_L)} (left) / X{int(k.RAIL_X_R)} (right) | the right-walkway outer edge (X{int(k.WALKWAY_RIGHT_X_R)}) + combined corner plate register to C (shared with the film plane) |",
    ])


def tolerances_md():
    dx = k.WALKWAY_BRACKET_BOLT_DX
    rows = [
        ("Deck coplanarity — grate-bearing tops, all 4 sections", "A", "±2 mm", "level walking surface"),
        ("Bracket arm reach (tip X)", "B", "±2 mm", "grate-edge bearing only"),
        (f"Wall-bolt pattern (±{dx}/±{k.WALKWAY_BRACKET_BOLT_DX_WIDE} X, Z{k.WALKWAY_BRACKET_BOLT_Z_LO}/Z{k.WALKWAY_BRACKET_UPPER_BOLT_Z})", "B", "±0.5 mm", "must align reinf-plate + wall holes"),
        (f"Foot-anchor pattern (X +{k.LEFT_WK_CANT_FOOT_BOLT_DX[0]}/+{k.LEFT_WK_CANT_FOOT_BOLT_DX[1]}, ±{k.LEFT_WK_CANT_FOOT_BOLT_DY} Yd)", "A", "±1 mm", "self-drillers are forgiving"),
        (f"Spray-bar slit position (X{int(k.PH_X) if hasattr(k,'PH_X') else 2454})", "C", "±2 mm", "align to the traveling spray bar"),
        ("Muslin notch / drum-exit punch-out position", "B/C", "±3 mm", "clearance features"),
        ("Combined corner-plate seat Z (walkway beam + film rail)", "A+C", "±1 mm", "shared level interface with the film plane"),
        (f"Rectangle beam soffit Z{k.WALKWAY_BRACKET_ARM_Z0:.1f} (spray-bar clearance)", "A", "+2 / −0 mm", "must NOT drop below the spray-bar clearance"),
    ]
    lines = ["| Feature | Datum | Tolerance | Why |", "|---------|-------|-----------|-----|"]
    for f, d, tol, why in rows:
        lines.append(f"| {f} | {d} | {tol} | {why} |")
    lines.append("| *General (all else)* | — | **ISO 13920 Class B** | weldment linear/angular; welds per **AWS D1.1** |")
    return "\n".join(lines)


def weld_table_md():
    lines = ["| Mark | Weld | Leg | Basis / check |",
             "|------|------|-----|---------------|"]
    for mark, joint, leg, note in weld_rows():
        lines.append(f"| {mark} | {joint} | {leg} | {note} |")
    return "\n".join(lines)


def schedules_report():
    out = ["\n########## FASTENER SCHEDULE (WF#) ##########"]
    for r in FASTENERS:
        out.append(f"  {r[0]}: {r[1]} — {r[2]} {r[3]}, {r[4]}, {r[5]}")
    out.append("\n########## WELD SCHEDULE (WW#) — governing throats load-checked ##########")
    for mark, joint, leg, note in weld_rows():
        out.append(f"  {mark}: {joint} — {leg} — {note}")
    out.append("\n########## DATUMS + TOLERANCES (Phase C) ##########")
    out.append("  A = floor plane · B = wall faces · C = film-plane rail datum (X260/X4649)")
    out.append("  general = ISO 13920 Class B; welds = AWS D1.1; functional tolerances per feature (see report §10.3)")
    return "\n".join(out)


# ── Report + table ───────────────────────────────────────────────────────────
def full_report():
    ROWS.clear()
    blocks = [
        f"WALKWAY STRUCTURAL VALIDATION — US IBC/OSHA (IBC Table 1607.1: {LL_PSF:.0f} psf + 300 lbf concentrated)",
        f"  concentrated 300 lbf ({P_CONC:.0f} N) at the tip governs every cantilever; SF on yield (target {SF_TARGET:.1f})",
        grate_check(),
        wall_bracket_check(),
        wall_bolt_check(),
        floor_leg_check(),
        corner_plate_check(),
        cross_refs(),
        # reuse the detailed IBC-frame blocks verbatim (single source):
        arm_notch_check(),
        outer_beam_frame_check(),
        service_loads(),
        schedules_report(),
    ]
    return "\n".join(blocks)


def table_md():
    """The §9 validation table (markdown). Regenerates ROWS first."""
    full_report()
    lines = ["| Element | Design demand | Capacity | SF | Basis |",
             "|---------|---------------|----------|----|-------|"]
    for elem, dem, cap, sf, note in ROWS:
        lines.append(f"| {elem} | {dem} | {cap} | {sf} | {note} |")
    return "\n".join(lines)


# All injected report blocks: key -> function returning the markdown body.
_BLOCKS = {
    "load:validation": table_md,
    "load:fasteners": fastener_table_md,
    "load:welds": weld_table_md,
    "load:datums": datums_md,
    "load:tolerances": tolerances_md,
}


def _block_pat(key):
    return re.compile(r"(<!-- BEGIN " + re.escape(key) + r" -->)(.*?)(<!-- END " + re.escape(key) + r" -->)", re.DOTALL)


def inject_blocks(write=True):
    if not os.path.exists(_REPORT):
        return [("load:*", "NO-REPORT")]
    text = open(_REPORT, encoding="utf-8").read()
    new, results = text, []
    for key, fn in _BLOCKS.items():
        body = "\n" + fn() + "\n"
        pat = _block_pat(key)
        found = False
        for m in pat.finditer(text):
            found = True
            results.append((key, "ok" if m.group(2) == body else "STALE"))
        if not found:
            results.append((key, "MISSING"))
        new = pat.sub(lambda m, body=body: m.group(1) + body + m.group(3), new)
    if write and new != text:
        open(_REPORT, "w", encoding="utf-8").write(new)
    return results


def check_blocks():
    return [f"{k_}: {st}" for k_, st in inject_blocks(write=False) if st != "ok"]


def main():
    if "--inject" in sys.argv:
        for key, st in inject_blocks(True):
            print(f"  {key}: {st}")
    elif "--check-blocks" in sys.argv:
        bad = check_blocks()
        if bad:
            print("✗ walkway load/schedule blocks out of sync (run: walkway_load.py --inject):")
            for b in bad:
                print("   " + b)
            sys.exit(1)
        print("✓ walkway load + fastener/weld blocks in sync")
    else:
        print(full_report())


if __name__ == "__main__":
    main()
