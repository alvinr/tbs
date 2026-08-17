#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""ibc_frame_load.py — IBC stacking-frame transport-restraint load case (EN 12195-1:2010).

Phase A of the IBC-frame blueprint (see ibc-frame-blueprint-spec.md). Computes the EN 12195-1
design forces on the restraint frame for BOTH transport fill states (drained = tare only, and
loaded = top-tier Blue totes full) and checks each restraint element demand-vs-capacity with a
safety factor. Driftproof: reads member/geometry constants from tbs_constants.

EN 12195-1:2010 method (researched + cited in ibc-frame-blueprint-spec.md §Load basis):
  • acceleration coefficients: c_x = 0.8 g forward / 0.5 g rearward; c_y = 0.5 g lateral
    (0.6 g sideways-tipping); c_z = 1.0 g down (friction-credit term).
  • blocking / positive restraint (sliding balance):  BC >= f_s * m * g * (c - mu * c_z)
  • safety factor f_s = 1.25 forward, 1.1 sideways/rearward.
  • friction mu = 0.2 (conservative: plastic tote pallet on steel cage / unlisted-pair fallback;
    the standard caps unlisted / not-broom-clean pairs at 0.2; plastic-pallet-on-plywood = 0.25).

Run:  python3 src/generators/ibc_frame_load.py           # print the validation table
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from tbs_constants import (IBC_FRAME_RHS, IBC_FRAME_T, IBC_FOOT_PLATE, IBC_FOOT_PLATE_T,  # noqa: E402
                           CONTAINER_CORRUGATION_DEPTH,
                           IBC_FRONT_BAR_D, IBC_FRONT_BAR_W, IBC_FRONT_BAR_T,
                           IBC_FRONT_BAR_N_PER_TIER)

# ── EN 12195-1:2010 load basis ───────────────────────────────────────────────
G       = 9.81
CX_FWD  = 0.8      # forward / braking
CX_REAR = 0.5      # rearward
CY_LAT  = 0.5      # lateral / cornering (sliding)
CZ      = 1.0      # vertical down (friction-credit)
FS_FWD  = 1.25     # safety factor, forward
FS_OTH  = 1.10     # safety factor, sideways / rearward
MU      = 0.20     # sliding friction (conservative, plastic/steel unlisted-pair fallback)

# ── Design masses (kg) — the frame restrains the TOTES ───────────────────────
TOTE_TARE   = 65      # 1000L caged composite tare (weight-distribution-report.md)
TOTE_FILL_L = 900     # camera-ready standard Blue fill per top tote (L) -> kg at 1000 kg/m^3
M_DRAINED   = TOTE_TARE                    # nominal transport: totes empty (site-filled)
M_LOADED    = TOTE_TARE + TOTE_FILL_L      # over-spec bound: a full top-tier Blue tote (965 kg)

# ── Member / fastener properties ─────────────────────────────────────────────
# Front retaining bar 50x20x3 RHS, oriented 20mm-deep in the -X (forward) load direction
# (50mm vertical, gap-constrained by the 25mm film-rail clearance) -> bends about its WEAK axis.
BAR_H_LOAD = float(IBC_FRONT_BAR_D)   # section depth in the forward (bending) direction (mm)
BAR_W      = float(IBC_FRONT_BAR_W)   # section width (vertical) (mm)
BAR_T      = float(IBC_FRONT_BAR_T)   # wall (mm)
BAR_SPAN   = 1046.0   # wall-hanger -> upright-cleat span (mm)
FY_A500B   = 317.0    # A500 Gr.B square tube min yield (46 ksi, MPa)
FU_MILD    = 400.0    # mild-steel Fu for bearing (58 ksi, MPa)
WALL_T     = 1.6      # container corrugated side-wall sheet thickness (mm)

# M12 fasteners (coarse 1.75): tensile stress area
AS_M12   = 84.3       # mm^2
N_HANGER_BOLTS = 2    # M12x65 Gr.8.8 per wall hanger (one identical hanger per bar)
N_CLEAT_BOLTS  = 2    # M12x40 A2-70 per bar-end cleat
FUB_88   = 800.0      # Gr.8.8 ultimate (MPa)
FUB_A2   = 700.0      # A2-70 (18-8 SS) ultimate (MPa)

# Lashing (per stack)
STRAP_WLL_N = 3333 * 4.4482   # 2" ratchet strap assembly WLL (lb -> N) = 14,826 N
RING_WLL_N  = 6600 * 4.4482   # weld-on lashing ring WLL


def z_rhs(h_load, w, t):
    """Elastic section modulus (mm^3) of a rectangular hollow section bending about the axis
    whose depth-in-load-direction is h_load (width w)."""
    i = (w * h_load**3 - (w - 2*t) * (h_load - 2*t)**3) / 12.0
    return i / (h_load / 2.0)


def blocking_force(m, c, fs):
    """EN 12195-1 net horizontal design force a blocking device must resist (N)."""
    return fs * m * G * (c - MU * CZ)


def bolt_shear_cap(fub, n):
    """Ultimate shear capacity of n M12 bolts through the threads (N)."""
    return n * 0.6 * fub * AS_M12


def blocking_force_mu(m, c, fs, mu):
    return fs * m * G * (c - mu * CZ)


def compute(m, label, mu=MU, bar=(BAR_H_LOAD, BAR_W, BAR_T), n_bars_per_tote=1, n_straps=1):
    """All element checks for one per-tote design mass m.

    mu               friction credit (0.20 bare plastic/steel; 0.60 certified anti-slip mat)
    bar              (depth-in-load, width, wall) mm of the front retaining bar section
    n_bars_per_tote  bars sharing one tote face (2 = upper+lower, each takes half the face load)
    n_straps         ratchet straps per stack (vertical tie-down share)
    """
    bc_fwd = blocking_force_mu(m, CX_FWD, FS_FWD, mu)   # forward thrust the front bar must block
    bc_lat = blocking_force_mu(m, CY_LAT, FS_OTH, mu)   # lateral (side-wall-trapped; hanger secondary)

    # 1. Front retaining bar(s) — UDL bending; load shared across n_bars_per_tote, weak axis
    z = z_rhs(bar[0], bar[1], bar[2])
    m_cap = z * FY_A500B / 1e3                       # N.m per bar
    m_dem = (bc_fwd / n_bars_per_tote) * (BAR_SPAN / 1e3) / 8.0   # UDL: BC*L/8 per bar (N.m)
    sf_bar = m_cap / m_dem

    # 2. Wall-hanger bolt group — PER-BAR reaction: each bar carries BC/n_bars and is simply
    # supported (wall + upright ends), so each bar's wall-end = BC/(2*n_bars), into a 2-bolt hanger
    r_wall = bc_fwd / (2.0 * n_bars_per_tote)
    sf_hanger_bolt = bolt_shear_cap(FUB_88, N_HANGER_BOLTS) / r_wall
    # wall bearing / tear-out at the 2 holes in the 1.6mm corrugated wall (backing plate spreads it)
    bear_cap = N_HANGER_BOLTS * FU_MILD * 12.0 * WALL_T
    sf_wall_bear = bear_cap / r_wall

    # 3. Front-bar -> upright cleat, 2x M12x40 A2-70 in shear (per-bar upright-end reaction)
    r_upr = bc_fwd / (2.0 * n_bars_per_tote)
    sf_cleat = bolt_shear_cap(FUB_A2, N_CLEAT_BOLTS) / r_upr

    # 4. Lashing strap vertical tie-down (n_straps/stack) vs the tote weight it must hold seated
    sf_strap = (n_straps * STRAP_WLL_N) / (m * G)

    return {
        "label": label, "m": m, "bc_fwd": bc_fwd, "bc_lat": bc_lat, "mu": mu, "bar_sec": bar,
        "bar": (m_dem, m_cap, sf_bar),
        "hanger_bolt": (r_wall, bolt_shear_cap(FUB_88, N_HANGER_BOLTS), sf_hanger_bolt),
        "wall_bear": (r_wall, bear_cap, sf_wall_bear),
        "cleat": (r_upr, bolt_shear_cap(FUB_A2, N_CLEAT_BOLTS), sf_cleat),
        "strap": (m * G, STRAP_WLL_N, sf_strap),
    }


def _fmt(r):
    bs = r["bar_sec"]
    z = z_rhs(*bs)
    lines = [
        f"\n=== {r['label']}  (per-tote m = {r['m']:.0f} kg) ===",
        f"  bar {bs[1]:.0f}x{bs[0]:.0f}x{bs[2]:.0f} RHS  mu={r['mu']:.2f}",
        f"  EN 12195-1 forward blocking force BC = f_s*m*g*(c_x - mu*c_z)"
        f" = 1.25*{r['m']:.0f}*9.81*(0.8-{r['mu']:.2f}) = {r['bc_fwd']:.0f} N",
        f"  {'element':<34}{'demand':>12}{'capacity':>12}{'SF':>8}",
        f"  {'-'*66}",
    ]
    def row(name, tup, unit):
        d, c, sf = tup
        flag = "  <-- GOVERNS / FAIL" if sf < 1.0 else ("  <-- marginal" if sf < 1.5 else "")
        lines.append(f"  {name:<34}{d:>9.0f}{unit:<3}{c:>9.0f}{unit:<3}{sf:>7.2f}{flag}")
    row(f"front bar bending (Z={z:.0f}mm3, wk)", r["bar"], "Nm")
    row("wall-hanger bolts (2x M12x65 8.8)", r["hanger_bolt"], "N")
    row("wall bearing (1.6mm, 2 holes)", r["wall_bear"], "N")
    row("bar->upright cleat (2x M12x40 A2)", r["cleat"], "N")
    row("lashing strap (vert tie-down)", r["strap"], "N")
    return "\n".join(lines)


# ── Weld schedule (Phase B) ──────────────────────────────────────────────────
# Fillet-weld shear capacity = throat (0.707·leg) × length × 0.6·Fu_electrode. The frame welds carry
# tiny restraint loads, so they are set by the AWS D1.1 minimum practical fillet for the material
# (≥3mm for ≤6mm plate); only the LASHING-RING weld sees a real load (the strap WLL).
FU_WELD = 480.0   # E70xx electrode ultimate (MPa)


def fillet_cap(leg_mm, length_mm):
    return 0.707 * leg_mm * length_mm * 0.6 * FU_WELD   # N


def weld_schedule():
    lines = ["\n########## WELD SCHEDULE (Phase B) ##########",
             f"  {'weld':<40}{'leg':>6}{'demand':>10}{'cap':>10}{'SF':>7}"]
    # W4 — lashing ring -> front bar: carries one strap's WLL; ~110mm fillet around the ring base.
    ring_dem = STRAP_WLL_N
    ring_cap = fillet_cap(6, 110)
    lines.append(f"  {'W4 lashing ring->bar (6mm, all-around)':<40}{'6mm':>6}{ring_dem:>9.0f}{ring_cap:>9.0f}{ring_cap/ring_dem:>7.1f}")
    # W3 — bar-end cleat -> upright: per-bar reaction BC/4 (loaded, bare); ~80mm fillet.
    cleat_dem = blocking_force_mu(M_LOADED, CX_FWD, FS_FWD, MU) / (2.0 * IBC_FRONT_BAR_N_PER_TIER)
    cleat_cap = fillet_cap(4, 80)
    lines.append(f"  {'W3 cleat->upright (4mm)':<40}{'4mm':>6}{cleat_dem:>9.0f}{cleat_cap:>9.0f}{cleat_cap/cleat_dem:>7.1f}")
    lines.append("  W1 upright<->ring (5mm all-around), W2 foot-plate<->upright (6mm all-around),")
    lines.append("  W5 hanger seat<->pocket (4mm) — minimum practical fillets; restraint load << capacity.")
    return "\n".join(lines)


# ── Service + walkway load cases (scope extension: full corridor metal) ───────
# The same deep-box frame also carries the plumbing panel + pumps (rear-panel brackets, back uprights)
# and the right-walkway cantilever arms (front uprights). These are STATIC/SERVICE loads, checked here
# to confirm they are non-governing vs the transport restraint case. (Arm CONNECTION only — the arm's
# own bending is the walkway blueprint's scope.)
M_PANEL_KG   = 20.0    # plumbing panel ply + shirt + 5 pumps/ACC + fittings (est) on 6 rear-panel brackets
N_PANEL_BRK  = 6
M_WK_ARM_KG  = 22.0    # right-walkway dead per arm (44 kg / 2 center arms)
P_PERSON_N   = 1000.0  # one-person point live load (worst case on one arm)
ARM_REACH_M  = (4654 - 4329) / 1000.0   # 0.325 — upright (RWK_X_UP) -> deck left edge (RWK_X_L)


def service_loads():
    lines = ["\n########## SERVICE + WALKWAY LOAD CASES (full corridor frame) ##########"]
    # Plumbing panel + pumps, hung on 6 rear-panel brackets
    panel_per = M_PANEL_KG * G / N_PANEL_BRK
    lines.append(f"  plumbing panel + pumps ~{M_PANEL_KG:.0f} kg / {N_PANEL_BRK} rear-panel brackets"
                 f" = {panel_per:.0f} N/bracket (static — trivial, SF >> 10)")
    # Walkway cantilever arm: dead + person, moment into the FRONT upright at the connection
    p_arm = M_WK_ARM_KG * G + P_PERSON_N
    m_conn = p_arm * ARM_REACH_M
    z_upr = z_rhs(IBC_FRAME_RHS, IBC_FRAME_RHS, IBC_FRAME_T)   # 50.8x50.8x3 upright
    m_cap_upr = z_upr * FY_A500B / 1e3
    # arm->upright connection = a BOLTED END-PLATE (plate welded to the arm end, 2x M12 in a CENTRAL column
    # through the upright into a rear backing plate, per ibc_cantilever_arms). Moment = a tension couple over
    # the ~90mm bolt spacing; with 1 bolt per row the TOP bolt carries the full couple tension.
    couple_sp = 0.090
    f_bolt = m_conn / couple_sp
    bolt_cap = 0.9 * FUB_88 * AS_M12   # M12 8.8 tensile (proof) capacity per bolt (N)
    lines.append(f"  walkway arm tip {p_arm:.0f} N (22kg dead + 1kN person) x {ARM_REACH_M*1000:.0f}mm"
                 f" = {m_conn:.0f} N.m at the upright")
    lines.append(f"  front upright bending (50.8 RHS): cap {m_cap_upr:.0f} N.m  SF {m_cap_upr/m_conn:.1f}")
    lines.append(f"  arm->upright END-PLATE (2x M12 central, {couple_sp*1000:.0f}mm couple): {f_bolt:.0f} N/bolt tension,"
                 f" cap {bolt_cap:.0f} N  SF {bolt_cap/f_bolt:.1f}")
    lines.append("  Both non-governing vs the EN 12195-1 transport case (bar SF 1.59). Arm NOTCH check below; fab on Sheet 5.")
    return "\n".join(lines)


# ── Walkway cantilever ARM — half-lap notch check (solid-bar redesign) ────────
# The arm is a cantilever off the front upright; the two long beams half-lap it. Its OWN section at the
# notches was unchecked above (connection-only). Worst case = the whole arm load at the TIP, so the moment
# at a section = P_arm * (lever from the tip load to that section). Switching the arm to a SOLID bar
# (Z = w*h^2/6 on the kept depth) and REBALANCING the split per crossing — deep ARM notch only where the
# moment ~0 (the tip); deep BEAM notch at the POST END where the arm moment peaks — keeps the arm strong
# with no position change.
# Arm/beam geometry mirrors the RWK_* constants in generate_sketchup_model.py (kept as literals here,
# same as ARM_REACH_M above — this module intentionally does not import the model builders).
RWK_ARM_W    = 50.8              # arm width in Yd (2in) = long-beam width
RWK_AH       = 25.4             # arm depth (1in envelope: Z89.6 -> grate bottom Z115)
RWK_X_UP     = 4654            # front upright (post) X
RWK_X_L      = 4329            # arm tip X (= inner long-beam left edge)
RWK_BEARER_W = 50.8            # long-beam width in X
RWK_BEARER_XS = (4329, 4578.2)  # inner + outer long-beam left edges (RWK_X_R - RWK_BEARER_W)

FY_A36 = 250.0   # solid mild-steel flat-bar min yield (MPa, A36)


def _z_solid(w, h):
    """Elastic section modulus (mm^3) of a SOLID rectangle, depth h in the bending direction."""
    return w * h * h / 6.0


C_WID_MM = 2388.0   # container interior width (Yd) — the long-beam end supports (mirrors C_WID)


def _z_hollow_upper(h, b=None, t=3.05):
    """Elastic modulus (mm^3) of the kept-UPPER portion of a laid-flat RHS after a half-lap removes the
    lower part — an open channel (top flange + two short webs), extreme fiber at the cut. Much weaker than
    a solid bar of the same depth, which is why the arm (not the beam) keeps the deep side at the post."""
    if b is None:
        b = RWK_BEARER_W
    a_f, z_f = b * t, h - t / 2.0            # top flange
    a_w, z_w = 2 * t * h, h / 2.0            # two webs
    a = a_f + a_w
    zc = (a_f * z_f + a_w * z_w) / a
    i = (b * t**3 / 12 + a_f * (z_f - zc)**2) + (2 * (t * h**3 / 12) + a_w * (z_w - zc)**2)
    return i / max(zc, h - zc)


def arm_notch_check(sf_target=2.0):
    lines = ["\n########## WALKWAY ARM — HALF-LAP NOTCH CHECK (solid-bar redesign) ##########"]
    p_arm = M_WK_ARM_KG * G + P_PERSON_N
    L = RWK_X_UP - RWK_X_L
    xs = sorted(RWK_BEARER_XS)
    inner_c = xs[0] + RWK_BEARER_W / 2.0     # inner beam centre (near the tip)
    outer_c = xs[1] + RWK_BEARER_W / 2.0     # outer beam centre (near the post)
    d_inner = RWK_X_UP - inner_c
    d_outer = RWK_X_UP - outer_c
    m_inner = p_arm * (L - d_inner) / 1e3    # N.m (load at the tip = worst case for each notch)
    m_outer = p_arm * (L - d_outer) / 1e3
    lines.append(f"  arm load (worst case at tip) P = {p_arm:.0f} N  ·  length {L:.0f} mm  ·  SOLID {RWK_ARM_W:.0f}x{RWK_AH:.0f} bar (Fy {FY_A36:.0f})")
    lines.append(f"  {'crossing':<26}{'from post':>10}{'moment':>9}{'arm keep*':>12}")
    lines.append(f"  {'-'*57}")
    for name, d, m in (("outer notch (post end)", d_outer, m_outer),
                       ("inner notch (tip)", d_inner, m_inner)):
        z_req = sf_target * m * 1e3 / FY_A36
        h_req = (6.0 * z_req / RWK_ARM_W) ** 0.5
        lines.append(f"  {name:<26}{d:>7.0f}mm{m:>7.0f}Nm{h_req:>9.1f}mm")
    lines.append(f"  *arm kept (lower) depth for SF {sf_target:.1f} as a solid bar; envelope = {RWK_AH:.0f} mm")
    keep_post = 16.0
    sf_post = _z_solid(RWK_ARM_W, keep_post) * FY_A36 / 1e3 / m_outer
    lines.append(f"  ADOPTED split — POST (post end): arm keeps {keep_post:.0f} mm solid, SF_arm {sf_post:.2f}; the OUTER")
    lines.append(f"    BEAM takes the remaining {RWK_AH-keep_post:.1f} mm as a BEARING SEAT (carries the vertical")
    lines.append("    reaction, not hogging — see the continuous-beam check below).")
    lines.append("  INNER (tip): arm keeps 5.4 mm (M~30 Nm, SF~2 solid); the inner beam keeps the full 20 mm.")
    return "\n".join(lines)


def outer_beam_frame_check():
    """The outer long beam is half-lapped (notched to 9.4 mm) where the 2 arms cross it — and that notch is
    at a SUPPORT. A 9.4 mm kept-upper hollow channel is far too weak to carry the elastic hogging, so it
    cannot act as a rigid moment joint: it is a BEARING SEAT (the beam's upper 9.4 rests on the arm's lower
    16), i.e. a PINNED support. Designed that way the beam is simply-supported between its 4 bearing points,
    the notch carries only the vertical reaction, and the FULL 25.4 section governs span bending + deflection
    (SS is also the conservative bound for the real continuous beam)."""
    lines = ["\n########## OUTER WALKWAY LONG BEAM — CONTINUOUS-FRAME CHECK ##########"]
    E = 200000.0
    z_full = z_rhs(RWK_AH, RWK_BEARER_W, 3.05)
    i_full = z_full * RWK_AH / 2.0
    sup = [0.0] + sorted((1046.0, 1266.0)) + [C_WID_MM]        # 2 corner + 2 arm supports (RWK_UP_YDS)
    spans = [sup[i + 1] - sup[i] for i in range(len(sup) - 1)]
    lmax = max(spans)
    w = 0.063                                                 # N/mm — GRP grate (half the 300mm deck) + self-weight (light)
    lines.append(f"  supports at Yd {', '.join(f'{s:.0f}' for s in sup)} mm; spans {', '.join(f'{s:.0f}' for s in spans)}; worst {lmax:.0f} mm")
    lines.append(f"  full section Z={z_full:.0f} mm3  I={i_full:.0f} mm4  (2x1x0.120 RHS)")
    for pn in (500.0, 1000.0):                                # person share on one of the 2 close long beams (worst-on-one = 1000)
        m_ss = (w * lmax**2 / 8.0 + pn * lmax / 4.0) / 1e3
        sf = z_full * FY_A500B / 1e3 / m_ss
        d = 5 * w * lmax**4 / (384 * E * i_full) + pn * lmax**3 / (48 * E * i_full)
        lines.append(f"  span SS, person {pn:.0f}N mid: M {m_ss:.0f} Nm  SF {sf:.1f}  |  deflection {d:.1f} mm (L/{lmax/d:.0f})")
    z_notch = _z_hollow_upper(RWK_AH - 16.0)                  # kept-upper 9.4mm channel
    m_cap_notch = z_notch * FY_A500B / 1e3
    m_hog = 3 * 500.0 * lmax / 16.0 / 1e3                     # ~propped-cantilever hogging (person mid long span)
    lines.append(f"  notch (9.4mm kept, Z={z_notch:.0f}) cap {m_cap_notch:.0f} Nm << elastic hogging ~{m_hog:.0f} Nm")
    lines.append("    => the half-lap is a BEARING SEAT / pin, NOT a moment joint: notch carries the vertical")
    lines.append("       reaction only (~0.2 MPa bearing over 50.8x50.8); the beam spans SS on the FULL section.")
    return "\n".join(lines)


def render_png(path=None):
    """Blueprint load-case SHEET (ibc-frame-load-case.png): frame elevation with the EN 12195-1
    load arrows + a demand/capacity/SF matrix for every restraint element, driven from the same
    compute() the validation table uses. Matplotlib guarded (except ImportError) so the module stays
    import-safe for the dependency-free gates."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle, FancyArrow
    except ImportError:
        return None
    if path is None:
        from tbs_constants import DIAGRAMS_DIR
        path = os.path.join(DIAGRAMS_DIR, "ibc-frame-load-case.png")

    n = IBC_FRONT_BAR_N_PER_TIER
    rL  = compute(M_LOADED,  "loaded",     mu=0.20, n_bars_per_tote=n, n_straps=2)   # governing: no mat
    rLm = compute(M_LOADED,  "loaded+mat", mu=0.60, n_bars_per_tote=n, n_straps=2)   # anti-slip credited
    rD  = compute(M_DRAINED, "drained",    mu=0.20, n_bars_per_tote=n, n_straps=2)
    # service (walkway arm + upright), recomputed from the same constants
    p_arm  = M_WK_ARM_KG * G + P_PERSON_N
    m_conn = p_arm * ARM_REACH_M
    sf_upr = (z_rhs(IBC_FRAME_RHS, IBC_FRAME_RHS, IBC_FRAME_T) * FY_A500B / 1e3) / m_conn
    endplate_cap = 0.9 * FUB_88 * AS_M12                # M12 8.8 tensile capacity/bolt (N)
    sf_endplate = endplate_cap / (m_conn / 0.090)   # 2-bolt central column, 90mm couple, top bolt carries the tension

    C_STEEL = "#8890a0"; C_TOTE = "#c9d4e4"; C_LOAD = "#c0392b"; C_OK = "#1f7a3d"; C_WARN = "#b8860b"

    fig = plt.figure(figsize=(15.5, 9)); fig.patch.set_facecolor("white")
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 1.28], height_ratios=[1.05, 1],
                          left=0.045, right=0.975, top=0.88, bottom=0.06, wspace=0.16, hspace=0.24)
    axE = fig.add_subplot(gs[0, 0]); axM = fig.add_subplot(gs[1, 0]); axT = fig.add_subplot(gs[:, 1])
    for ax in (axE, axM, axT):
        ax.axis("off")

    # ── axE — frame elevation + EN load arrows (schematic, forward = −X to the left) ──
    axE.set_xlim(0, 100); axE.set_ylim(0, 100); axE.set_aspect("auto")
    axE.text(50, 97, "LOAD PATH (transport)", ha="center", fontsize=10, fontweight="bold")
    axE.add_patch(Rectangle((8, 6), 84, 4, fc=C_STEEL, ec="#333"))            # container floor
    axE.text(50, 3, "container floor  ·  4 foot anchors (datum A)", ha="center", fontsize=7, color="#555")
    axE.add_patch(Rectangle((26, 10), 52, 62, fc=C_TOTE, ec="#333"))          # tote stack (2 high)
    axE.plot([26, 78], [41, 41], color="#333", lw=0.7, ls=(0, (4, 2)))
    axE.text(52, 40, "direct-stack junction", ha="center", va="center", fontsize=6.5, color="#555")
    axE.text(52, 60, "4× 1000 L totes\n(2×2, restraint-only)", ha="center", va="center", fontsize=8)
    axE.add_patch(Rectangle((22, 12), 4, 58, fc=C_STEEL, ec="#333"))          # front retaining bars (at the −X face)
    axE.text(16, 55, "front\nbars", ha="center", fontsize=7); axE.plot([20,24],[45,45],color="#333",lw=0.5)
    axE.add_patch(Rectangle((10, 12), 4, 58, fc="#5a6270", ec="#333"))        # wall hanger / side wall
    axE.text(9, 34, "wall\nhanger", ha="right", fontsize=7)
    axE.add_patch(Rectangle((80, 10), 5, 64, fc="#5a6270", ec="#333"))        # corridor upright (cleat end)
    axE.text(86, 40, "upright\n+ cleat", ha="left", fontsize=7)
    # EN arrows on the tote CG
    axE.add_patch(FancyArrow(52, 46, -20, 0, width=1.3, head_width=4, head_length=4, fc=C_LOAD, ec=C_LOAD))
    axE.text(40, 51, "0.8 g fwd", color=C_LOAD, fontsize=8, ha="center", fontweight="bold")
    axE.add_patch(FancyArrow(52, 46, 0, -20, width=1.3, head_width=4, head_length=4, fc=C_LOAD, ec=C_LOAD))
    axE.text(58, 34, "1.0 g ↓", color=C_LOAD, fontsize=8, ha="left", fontweight="bold")
    axE.add_patch(FancyArrow(52, 68, 14, 0, width=0.9, head_width=3, head_length=3, fc="#e08e0b", ec="#e08e0b"))
    axE.text(60, 72, "0.5 g lat", color="#b8860b", fontsize=7.5, ha="center")
    axE.text(50, 0.5, "forward thrust → front bars → (wall hanger J3  +  corridor cleat J2) → frame → floor anchors",
             ha="center", fontsize=6.6, color="#333")

    # ── axM — EN 12195-1 method + states ──
    axM.set_xlim(0, 100); axM.set_ylim(0, 100)
    axM.text(0, 96, "EN 12195-1:2010 — METHOD", fontsize=10, fontweight="bold")
    method = [
        ("Acceleration coefficients", ""),
        ("   c_x = 0.8 g fwd / 0.5 g rear", ""),
        ("   c_y = 0.5 g lateral · c_z = 1.0 g down", ""),
        ("Safety factor  f_s = 1.25 fwd / 1.10 else", ""),
        ("Friction  μ = 0.20 bare (plastic/steel)", ""),
        ("            μ = 0.60 with certified anti-slip mat", ""),
        ("Positive blocking (sliding balance):", ""),
        ("   BC ≥ f_s · m · g · (c − μ·c_z)", ""),
    ]
    for i, (a, _) in enumerate(method):
        axM.text(0, 88 - i*6.2, a, fontsize=8.4, family="monospace",
                 fontweight="bold" if a.endswith(":") or a[0].isupper() and "≥" not in a else "normal")
    axM.text(0, 32, "DESIGN STATES (per top-tier tote):", fontsize=8.6, fontweight="bold")
    axM.text(0, 24, f"   DRAINED (nominal, site-filled): tare {M_DRAINED:.0f} kg  → every element SF ≥ 12",
             fontsize=8.2, family="monospace", color=C_OK)
    axM.text(0, 17, f"   LOADED (over-spec bound): full Blue {M_LOADED:.0f} kg  → the governing case",
             fontsize=8.2, family="monospace", color=C_WARN)
    axM.text(0, 7, "The camera runs disconnected from water; totes ship EMPTY. LOADED is the\nover-spec margin, not the ship state.",
             fontsize=7.2, color="#555")

    # ── axT — SF matrix (governing LOADED case) ──
    axT.set_xlim(0, 100); axT.set_ylim(0, 100)
    axT.text(50, 97, f"RESTRAINT ELEMENT SAFETY FACTORS — LOADED CASE ({M_LOADED:.0f} kg/tote)",
             ha="center", fontsize=10, fontweight="bold")
    cols = [1, 63, 80, 94]   # element · demand · capacity · SF
    axT.text(cols[0], 90, "element", fontsize=8.5, fontweight="bold")
    axT.text(cols[1], 90, "demand", fontsize=8.5, fontweight="bold", ha="right")
    axT.text(cols[2], 90, "capacity", fontsize=8.5, fontweight="bold", ha="right")
    axT.text(cols[3], 90, "SF", fontsize=8.5, fontweight="bold", ha="right")
    axT.plot([0, 100], [87.5, 87.5], color="#333", lw=1)

    rows = [
        ("Front retaining bars ×2/face (μ0.20, no mat)", f"{rL['bar'][0]:,.0f} N·m", f"{rL['bar'][1]:,.0f} N·m", rL['bar'][2], "gov"),
        ("   … same bars + anti-slip mat (μ0.60)",       f"{rLm['bar'][0]:,.0f} N·m", f"{rLm['bar'][1]:,.0f} N·m", rLm['bar'][2], ""),
        ("Wall-hanger bolts J3 (2× M12×65, shear)",      f"{rL['hanger_bolt'][0]:,.0f} N", f"{rL['hanger_bolt'][1]:,.0f} N", rL['hanger_bolt'][2], ""),
        ("Corrugated-wall bearing (backing plate)",      f"{rL['wall_bear'][0]:,.0f} N", f"{rL['wall_bear'][1]:,.0f} N", rL['wall_bear'][2], ""),
        ("Corridor cleat bolts J2 (2× M12×40, shear)",   f"{rL['cleat'][0]:,.0f} N", f"{rL['cleat'][1]:,.0f} N", rL['cleat'][2], ""),
        ("Lash ring + 2\" strap (vertical, per stack)",   f"{rL['strap'][0]:,.0f} N", f"{rL['strap'][1]:,.0f} N", rL['strap'][2], ""),
        ("Walkway-arm end-plate J6 (service, +1 kN)",    f"{m_conn:,.0f} N·m", f"{endplate_cap:,.0f} N", sf_endplate, "svc"),
        ("Front upright bending (service)",              f"{m_conn:,.0f} N·m", "—", sf_upr, "svc"),
    ]
    y = 82
    for label, d, c, sf, tag in rows:
        col = C_WARN if sf < 2 else (C_OK if sf >= 4 else "#333")
        axT.text(cols[0], y, label, fontsize=7.6, family="monospace")
        axT.text(cols[1], y, d, fontsize=8, ha="right", family="monospace", color="#555")
        axT.text(cols[2], y, c, fontsize=8, ha="right", family="monospace", color="#555")
        axT.text(cols[3], y, f"{sf:.2f}", fontsize=8.6, ha="right", fontweight="bold", color=col)
        if tag == "gov":
            axT.text(cols[3]+1.5, y, "◀ governs", fontsize=6.6, color=C_WARN, ha="left", va="center")
        elif tag == "svc":
            axT.text(cols[3]+1.5, y, "svc", fontsize=6.2, color="#888", ha="left", va="center")
        y -= 6.6
    axT.plot([0, 100], [y+3, y+3], color="#333", lw=1)
    axT.text(cols[0], y-3, "Defense in depth: the bars pass on positive blocking ALONE (SF 1.59, mat absent);",
             fontsize=7.6, color="#333")
    axT.text(cols[0], y-9, "the certified anti-slip mat lifts it to SF 4.77. Everything downstream clears SF ≥ 8;",
             fontsize=7.6, color="#333")
    axT.text(cols[0], y-15, "in the DRAINED ship state every element clears SF ≥ 12. Service loads non-governing.",
             fontsize=7.6, color="#333")

    fig.suptitle("IBC STACKING FRAME — TRANSPORT RESTRAINT LOAD CASE  ·  EN 12195-1:2010",
                 fontsize=14, fontweight="bold", y=0.965)
    fig.text(0.5, 0.925, "driven from tbs_constants + ibc_frame_load.py  ·  restraint-only deep 4-leg box  ·  2× 50×20×3 bars/tote + anti-slip mat + 2 straps/stack",
             ha="center", fontsize=9, color="#555")
    fig.text(0.5, 0.018, "IBC FRAME — LOAD CASE  ·  TBS-001  ·  see report §3.4  ·  © 2026 Alvin Richards",
             ha="center", fontsize=8, color="#777")
    fig.savefig(path, dpi=150, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print(f"  {os.path.relpath(path)} saved")
    return path


def main():
    if "--png" in sys.argv:
        render_png()
        return
    print("IBC STACKING-FRAME TRANSPORT RESTRAINT — EN 12195-1:2010")
    print(f"  corrugation={CONTAINER_CORRUGATION_DEPTH}mm  "
          f"frame RHS={IBC_FRAME_RHS}mm  foot={IBC_FOOT_PLATE}x{IBC_FOOT_PLATE}x{IBC_FOOT_PLATE_T}")

    n = IBC_FRONT_BAR_N_PER_TIER   # 2 — adopted design (R5)
    print(f"\n########## AS-DESIGNED — {n} x 50x20x3 bars/tote + anti-slip mat + 2 straps/stack ##########")
    # Bar-alone (mat degraded/absent, mu=0.20) is the defense-in-depth positive-blocking floor;
    # with the certified anti-slip mat (mu=0.60) the margins lift ~3x.
    print(_fmt(compute(M_DRAINED, "DRAINED (nominal — totes empty), bar-alone",
                       n_bars_per_tote=n, n_straps=2)))
    print(_fmt(compute(M_LOADED,  "LOADED — bar-alone (mat absent, mu=0.20)",
                       n_bars_per_tote=n, n_straps=2)))
    print(_fmt(compute(M_LOADED,  "LOADED — with anti-slip mat (mu=0.60)",
                       mu=0.60, n_bars_per_tote=n, n_straps=2)))

    print("\n########## WHY DOUBLED — single 50x20x3 bar fails the loaded case ##########")
    print(_fmt(compute(M_LOADED,  "LOADED — as-was 1 bar/tote, no mat (SUPERSEDED)",
                       n_bars_per_tote=1)))

    print(service_loads())
    print(arm_notch_check())
    print(outer_beam_frame_check())
    print(weld_schedule())


if __name__ == "__main__":
    main()
