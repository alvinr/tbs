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
from tbs_constants import (IBC_FRAME_RHS, IBC_FOOT_PLATE, IBC_FOOT_PLATE_T,  # noqa: E402
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


def main():
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


if __name__ == "__main__":
    main()
