#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""Corridor plumbing panel mass, summed from its parts.

The panel's ply pieces come from the same cut dimensions the plywood cut sheet uses; the pipe runs,
P-clips and valves come from an in-process build of water.skp, clipped to the corridor box (the rear
panel, shirt, side boards and drain-riser spine). Consumers: the IBC-frame service-load check
(`ibc_frame_load.M_PANEL_KG`) and the weight analysis (`Plumbing — Corridor panel`).

Run:  python3 plumbing_panel_mass.py   (prints the breakdown)
"""
import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_HERE, "..", "models"))

from tbs_constants import PUMP_KG, PLY_RHO_KG_M3, ACC_KG, ACC_L  # noqa: E402

# 1/2" / 1" Sch-40 PVC (Bell Plastics Sch-40 spec sheet: 0.16 / 0.32 lb/ft), water-filled at the
# Sch-40 bore (0.622" / 1.049").
LB_FT_TO_KG_M = 0.45359237 / 0.3048
PIPE_KG_M = {
    "half": 0.16 * LB_FT_TO_KG_M + math.pi * (0.622 * 25.4 / 2000) ** 2 * 1000,
    "one":  0.32 * LB_FT_TO_KG_M + math.pi * (1.049 * 25.4 / 2000) ** 2 * 1000,
}
VALVE_KG = 0.15        # est. — ½" PVC ball / check valve body (each)
CLIP_KG = 0.03         # est. — cushioned P-clip + screws (the ply block is counted as ply)
FITTINGS_FRAC = 0.10   # est. — elbows / tees / adapters, as a share of the pipe mass
CORRIDOR_PUMPS = 4     # P-01 / P-02 / P-03 / P-05 (P-04 is on the pinhole-wall skid)

_CACHE = None


def _capture():
    import tbs_draw as d
    import generate_corridor_water_panel as cwp
    runs, clips, valves = [], [], []
    o_run, o_cyl, o_clip = d.ruby_pipe_run, d.ruby_cylinder, cwp.clip_on_block

    def run(name, wps, r, *a, **k):
        runs.append((name, [tuple(map(float, q)) for q in wps], float(r)))
        return o_run(name, wps, r, *a, **k)

    def cyl(name, cx, cy, cz, *a, **k):
        if name.startswith(("BV-", "CV-")) and "handle" not in name:
            valves.append((name, float(cx), float(cy)))
        return o_cyl(name, cx, cy, cz, *a, **k)

    def clip(nm, cx, cz, face_y, pipe_y, *a, **k):
        clips.append((nm, float(cx), float(pipe_y)))
        return o_clip(nm, cx, cz, face_y, pipe_y, *a, **k)

    d.ruby_pipe_run, d.ruby_cylinder, cwp.clip_on_block = run, cyl, clip
    try:
        import generate_pinhole_water_panel as pw
        ruby = pw.build()
    finally:
        d.ruby_pipe_run, d.ruby_cylinder, cwp.clip_on_block = o_run, o_cyl, o_clip
    runs = [r for r in runs if f'grp.name = "{r[0]}"' in ruby]
    return cwp, runs, clips, valves


def _in_box(cwp, x, yd):
    return x >= cwp.GAPX and cwp.YD_NEAR - 60 <= yd <= cwp.YD_FAR + 60


def _clipped_len(cwp, a, b):
    """Length of segment a→b inside the corridor box (X ≥ GAPX, Yd in the corridor ± a clip lane)."""
    n = 40
    inside = 0
    for i in range(n):
        t = (i + 0.5) / n
        x, yd = a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])
        inside += _in_box(cwp, x, yd)
    return math.dist(a, b) * inside / n


def corridor_panel_mass() -> dict:
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    cwp, runs, clips, valves = _capture()
    t = cwp.EQT / 1000.0
    rho = PLY_RHO_KG_M3

    def board(w, h):
        return w * h * 1e-6 * t * rho

    prof = cwp.spine_profile()
    spine_a = abs(sum(prof[i][0] * prof[i - 1][1] - prof[i - 1][0] * prof[i][1]
                      for i in range(len(prof)))) / 2
    spine_a -= sum(math.pi * r * r for _, _, r in cwp.SPINE_HOLES)
    ply = {
        "rear backing board": board(cwp.YW_CUT, cwp.PH_CUT),
        "drain-riser spine": spine_a * 1e-6 * t * rho,
        "pump-mount shirt": board(cwp.YW_CUT, cwp.PANEL_TOP_Z - cwp.SHIRT_Z0),
        "shirt standoff cleats": board(cwp.SHIRT_CLEAT_W, cwp.SHIRT_CLEAT_N * cwp.SHIRT_CLEAT_H),
        "pump-run side boards": sum(board(cwp.BW_CUT, z1 - z0) for z0, z1 in
                                    (cwp.SB_FAR_Z, cwp.SB_NEAR_Z, cwp.SB_NEAR_UP_Z)),
    }
    pipe_m = {"half": 0.0, "one": 0.0}
    for _, wps, r in runs:
        size = "one" if r >= 14 else "half"
        pipe_m[size] += sum(_clipped_len(cwp, a, b) for a, b in zip(wps, wps[1:])) / 1000.0
    pipe = sum(PIPE_KG_M[s] * m for s, m in pipe_m.items())
    n_clip = sum(_in_box(cwp, x, y) for _, x, y in clips)
    n_valve = sum(_in_box(cwp, x, y) for _, x, y in valves)
    parts = {
        **{f"ply — {k}": v for k, v in ply.items()},
        f"pumps ({CORRIDOR_PUMPS}× Shurflo 2088, {PUMP_KG}kg)": CORRIDOR_PUMPS * PUMP_KG,
        "ACC-01 accumulator + water": ACC_KG + ACC_L,
        f"pipe, water-filled (½\" {pipe_m['half']:.1f}m, 1\" {pipe_m['one']:.1f}m)": pipe,
        f"fittings (est. {FITTINGS_FRAC:.0%} of pipe)": FITTINGS_FRAC * pipe,
        f"valves ({n_valve}× est. {VALVE_KG}kg)": n_valve * VALVE_KG,
        f"P-clips ({n_clip}× est. {CLIP_KG}kg)": n_clip * CLIP_KG,
    }
    _CACHE = {"parts": parts, "total": sum(parts.values())}
    return _CACHE


if __name__ == "__main__":
    m = corridor_panel_mass()
    for k, v in m["parts"].items():
        print(f"  {k:<52s} {v:6.2f} kg")
    print(f"  {'TOTAL':<52s} {m['total']:6.2f} kg")
