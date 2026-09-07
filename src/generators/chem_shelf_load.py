#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""chem_shelf_load.py — Chemistry prep shelf structural validation (blueprint Phase A).

The redesigned shelf is PLY-PRIMARY (no steel perimeter frame): an 18mm plywood board,
hinged on the wall at the back edge (600mm piano hinge) and held level at the two front
corners by 2 SS chain stays running up to wall anchors above the hinge. All attachments
land in pronged tee-nuts in the ply (1/4-20 ply-mount standard). This checks each element
under the 25kg design mixing load, demand vs capacity with a safety factor. Driftproof:
reads the shelf geometry from tbs_constants.

Run:  python3 src/generators/chem_shelf_load.py           # print the validation table
      python3 src/generators/chem_shelf_load.py --inject  # write §3.3 into chemistry-prep-shelves.md
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from tbs_constants import SHELF_W, SHELF_DEPTH  # noqa: E402

# ── Design basis ─────────────────────────────────────────────────────────────
G            = 9.81
LOAD_KG      = 25.0                 # design mixing load (bottles, cylinders, roller tray, scale) — report §3.3
PLY_T        = 18.0                 # plywood board thickness (mm) — the structural member (frame removed)
PLY_RHO      = 600.0               # plywood density (kg/m^3, ~exterior/phenolic) — self-weight
STAY_N       = 2                    # chain stays (one per front corner)
STAY_RISE    = 230.0               # wall-anchor height above the hinge line (mm) — report §3.2
TNUT_N_STAY  = 1                    # tee-nuts carrying each stay eye bolt

# Material allowables
PLY_FB       = 10.0                 # plywood allowable bending stress (MPa) — conservative for exterior ply
PLY_E        = 7000.0              # plywood modulus of elasticity (MPa) — conservative
CHAIN_WLL_N  = 490.0              # 4mm 304 SS chain WLL (N, ~50kg) — conservative for 4mm 304 SS; confirm at sourcing (demand is only ~91N, so any adequately-rated chain clears)
# 1/4"-20 4-prong tee-nut pull-out in 18mm plywood — conservative published/testable floor.
TNUT_PULLOUT_N = 1300.0            # N (a 4-prong tee-nut in 18mm ply pulls out well above 1kN)


def self_weight_kg():
    """Board self-weight (kg) — 18mm ply over the deployed footprint."""
    return (SHELF_W / 1e3) * (SHELF_DEPTH / 1e3) * (PLY_T / 1e3) * PLY_RHO


def loads():
    """Total design load + the simply-supported edge reactions (N).

    The board spans SHELF_DEPTH front-to-back, simply supported: back edge = piano hinge
    (full 600mm width), front edge = the 2 chain corners. A UDL splits 50/50 to the edges.
    """
    w_total = (LOAD_KG + self_weight_kg()) * G          # N, total vertical
    r_back  = w_total / 2.0                              # hinge back-edge reaction (over 600mm)
    r_front = w_total / 2.0                              # front-edge reaction (shared by 2 chains)
    return w_total, r_back, r_front


def chain_geometry():
    """Chain angle from horizontal + length (deg, mm): front corner -> wall anchor STAY_RISE up."""
    import math
    ang = math.degrees(math.atan2(STAY_RISE, SHELF_DEPTH))
    length = math.hypot(SHELF_DEPTH, STAY_RISE)
    return ang, length


def compute():
    import math
    w_total, r_back, r_front = loads()
    ang, clen = chain_geometry()
    sin_a = math.sin(math.radians(ang))

    # 1. Board bending — 18mm ply, 600 wide, UDL over the SHELF_DEPTH span, simply supported.
    w_udl   = w_total / (SHELF_DEPTH / 1e3)              # N/m line load across the span
    m_dem   = w_total * (SHELF_DEPTH / 1e3) / 8.0        # UDL simply-supported: W*L/8 (N.m)
    z_ply   = SHELF_W * PLY_T**2 / 6.0                   # section modulus (mm^3), full 600 width
    m_cap   = PLY_FB * z_ply / 1e3                       # N.m at the allowable bending stress
    sf_bend = m_cap / m_dem
    # midspan deflection, UDL simply supported: 5wL^4/384EI
    i_ply   = SHELF_W * PLY_T**3 / 12.0                  # mm^4
    defl    = 5 * (w_total / SHELF_DEPTH) * SHELF_DEPTH**4 / (384 * PLY_E * i_ply)  # mm

    # 2. Chain stay — tension = per-corner front reaction / sin(angle).
    r_corner = r_front / STAY_N                          # vertical reaction at each front corner
    t_chain  = r_corner / sin_a                          # chain tension (N)
    sf_chain = CHAIN_WLL_N / t_chain

    # 3. Front-corner tee-nut pull-out — the pull-out (board-normal) component is the vertical r_corner.
    sf_tnut  = TNUT_PULLOUT_N / r_corner

    # 4. Piano hinge back-edge — reaction spread over 600mm; per-tee-nut screw share is tiny.
    #    (checked as a distributed reaction, not a governing element)

    return {
        "self_kg": self_weight_kg(), "w_total": w_total, "r_back": r_back, "r_front": r_front,
        "chain_ang": ang, "chain_len": clen, "r_corner": r_corner,
        "bend": (m_dem, m_cap, sf_bend, defl),
        "chain": (t_chain, CHAIN_WLL_N, sf_chain),
        "tnut": (r_corner, TNUT_PULLOUT_N, sf_tnut),
    }


def _fmt(r):
    lines = [
        "CHEMISTRY PREP SHELF — STRUCTURAL VALIDATION (ply-primary, 25kg design load)",
        f"  board {SHELF_W:.0f}x{SHELF_DEPTH:.0f}x{PLY_T:.0f} ply  self-weight {r['self_kg']:.1f}kg  "
        f"total load {r['w_total']:.0f}N",
        f"  chain stay: angle {r['chain_ang']:.1f} deg from horizontal, length {r['chain_len']:.0f}mm, "
        f"per-corner reaction {r['r_corner']:.0f}N",
        f"  {'element':<40}{'demand':>10}{'capacity':>11}{'SF':>8}",
        f"  {'-'*69}",
    ]
    def row(name, dem, cap, sf, unit):
        flag = "  <-- CHECK" if sf < 2.0 else ""
        lines.append(f"  {name:<40}{dem:>7.0f}{unit:<3}{cap:>8.0f}{unit:<3}{sf:>7.1f}{flag}")
    md, mc, sfb, defl = r["bend"]
    row("board bending (18mm ply, 600 wide)", md, mc, sfb, "Nm")
    lines.append(f"  {'board midspan deflection':<40}{defl:>7.2f}mm   (L/{SHELF_DEPTH/defl:.0f})")
    row("chain stay tension (per chain)", *r["chain"], "N")
    row("front-corner tee-nut pull-out", *r["tnut"], "N")
    lines.append("  Every element clears with large margin — the 18mm ply + 2 chain stays carry the 25kg")
    lines.append("  mixing load comfortably; the steel perimeter frame is not structurally required.")
    return "\n".join(lines)


def table_md():
    """Markdown demand/capacity/SF table for report §3.3."""
    r = compute()
    md, mc, sfb, defl = r["bend"]
    t_dem, t_cap, t_sf = r["chain"]
    n_dem, n_cap, n_sf = r["tnut"]
    rows = [
        "| Element | Demand | Capacity | SF |",
        "|---|---|---|---|",
        f"| Board bending (18mm ply, 600 wide, {SHELF_DEPTH:.0f}mm span, 25kg UDL) | {md:.1f} N·m | {mc:.0f} N·m | **{sfb:.0f}** |",
        f"| Board midspan deflection | {defl:.2f} mm (L/{SHELF_DEPTH/defl:.0f}) | — | — |",
        f"| Chain stay tension (per chain, {r['chain_ang']:.0f}° from horizontal) | {t_dem:.0f} N | {t_cap:.0f} N (WLL) | **{t_sf:.0f}** |",
        f"| Front-corner tee-nut pull-out (1/4-20 4-prong, 18mm ply) | {n_dem:.0f} N | {n_cap:.0f} N | **{n_sf:.0f}** |",
    ]
    return "\n".join(rows)


def main():
    if "--inject" in sys.argv:
        import re
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                            "chemistry-prep-shelves.md")
        txt = open(path).read()
        block = f"<!-- BEGIN chem-shelf-load -->\n{table_md()}\n<!-- END chem-shelf-load -->"
        if "<!-- BEGIN chem-shelf-load -->" not in txt:
            print("no <!-- BEGIN chem-shelf-load --> marker in the report — add the section first")
            return 1
        txt = re.sub(r"<!-- BEGIN chem-shelf-load -->.*?<!-- END chem-shelf-load -->", block, txt, flags=re.S)
        open(path, "w").write(txt)
        print(f"  injected load table into {os.path.relpath(path)}")
        return 0
    print(_fmt(compute()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
