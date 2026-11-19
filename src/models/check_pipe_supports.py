# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""Pipe-support + connection audit for the water model (water.skp source, no SketchUp needed).

Two checks, both run against an in-process build of generate_pinhole_water_panel:

  floating_clips   — every P-clip strap must sit ON a pipe/tube centerline.  A clip whose pipe turned
                     away (an elbow/jog moved under it) is a support bracket holding nothing.
  collapsed_elbows — every elbow in a ruby_pipe_run needs straight leg on both sides (one tangent
                     length at a run end, two between elbows).  A shorter leg shrinks the swept elbow,
                     so the run no longer meets its port/fitting cleanly (how the pump connections broke
                     when the riser planes crowded the pump ports, 2026-11-18).  Ratchet: legs that were
                     already short are listed in pipe_elbow_allowlist.txt; anything NEW fails.

    python3 src/models/check_pipe_supports.py            # report; exit 1 on a failure
    python3 src/models/check_pipe_supports.py --baseline # rewrite the collapsed-elbow allowlist
"""
import math
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [_HERE, os.path.join(_HERE, "..", "generators")]
ALLOWLIST = os.path.join(_HERE, "pipe_elbow_allowlist.txt")
_NUM = r"(-?[\d.]+?)\.mm"


def build_instrumented():
    """Build water.rb in-process, recording every elbow whose legs are too short for it."""
    import tbs_draw as d
    short = set()
    orig = d.ruby_pipe_run

    def wrap(name, waypoints, r, color=None, alpha=None, elbow_r=None, n=16, seg=8, mute=0.0):
        R = elbow_r if elbow_r is not None else 2.0 * r
        V = []
        for p in waypoints:
            q = tuple(float(c) for c in p)
            if not V or math.dist(q, V[-1]) > 1e-6:
                V.append(q)
        for i in range(1, len(V) - 1):
            a, b, c = V[i - 1], V[i], V[i + 1]
            u = [b[k] - a[k] for k in range(3)]
            w = [c[k] - b[k] for k in range(3)]
            lu, lw = math.hypot(*u), math.hypot(*w)
            th = math.acos(max(-1.0, min(1.0, sum(u[k] * w[k] for k in range(3)) / (lu * lw))))
            if th < 1e-3:
                continue
            T = R * math.tan(th / 2.0)
            need_in = T * (1 if i == 1 else 2)
            need_out = T * (1 if i == len(V) - 2 else 2)
            if lu < 0.98 * need_in or lw < 0.98 * need_out:
                short.add(f"{name} @vertex {i}")
        return orig(name, waypoints, r, color, alpha, elbow_r, n, seg, mute)

    d.ruby_pipe_run = wrap
    try:
        import generate_pinhole_water_panel as pw
        ruby = pw.build()
    finally:
        d.ruby_pipe_run = orig
    return ruby, short


def _axes(ruby):
    """Centerline segments of every straight pipe (ruby_pipe) and round body/tube (ruby_cylinder)."""
    segs = []
    for m in re.finditer(r'grp\.name = "([^"]*)"\n\s*ge = grp\.entities\n\s*vec = Geom::Vector3d\.new\('
                         + _NUM + ", " + _NUM + ", " + _NUM + r"\)\n\s*circle = ge\.add_circle\(\["
                         + _NUM + "," + _NUM + "," + _NUM + r"\], vec, " + _NUM, ruby):
        v = [float(m.group(i)) for i in (2, 3, 4)]
        a = [float(m.group(i)) for i in (5, 6, 7)]
        segs.append((m.group(1), a, [a[i] + v[i] for i in range(3)]))
    for m in re.finditer(r'grp\.name = "([^"]*)"\n\s*ge = grp\.entities\n\s*circle = ge\.add_circle\(\['
                         + _NUM + "," + _NUM + "," + _NUM + r"\], \[([-\d,]+)\], " + _NUM
                         + r".*?cface\.pushpull\(" + _NUM + r"\)", ruby, re.S):
        c = [float(m.group(i)) for i in (2, 3, 4)]
        nrm = [float(x) for x in m.group(5).split(",")]
        h = float(m.group(7))
        segs.append((m.group(1), c, [c[i] + nrm[i] * h for i in range(3)]))
    return [s for s in segs if "stripe" not in s[0]]


def _dseg(p, a, b):
    ab = [b[i] - a[i] for i in range(3)]
    L2 = sum(x * x for x in ab) or 1e-9
    t = max(0.0, min(1.0, sum((p[i] - a[i]) * ab[i] for i in range(3)) / L2))
    return math.dist(p, [a[i] + t * ab[i] for i in range(3)])


def floating_clips(ruby, tol=3.0):
    """P-clip straps (not shim blocks, not the Cct-C cable clips) with no pipe through them."""
    segs = _axes(ruby)
    out = []
    for m in re.finditer(r'grp\.name = "([^"]*P-clip)"\n\s*face = grp\.entities\.add_face\((.*?)\)\n.*?'
                         r"pushpull\(([-\d.]+)\.mm\)", ruby, re.S):
        nm = m.group(1)
        if nm.startswith("Cct"):
            continue
        P = [[float(v) for v in re.findall(_NUM, p)] for p in re.findall(r"\[([^\]]*)\]", m.group(2))]
        xs, ys = [p[0] for p in P], [p[1] for p in P]
        cx, cz = (min(xs) + max(xs)) / 2, P[0][2] + float(m.group(3)) / 2
        probe = [(cx, min(ys) + k * (max(ys) - min(ys)) / 20, cz) for k in range(21)]
        best = min(min(_dseg(q, a, b) for q in probe) for _, a, b in segs)
        if best > tol:
            out.append(f"{nm} at X{cx:.0f} Z{cz:.0f} — nearest pipe {best:.1f}mm away")
    return out


def run(baseline=False):
    ruby, short = build_instrumented()
    if baseline:
        with open(ALLOWLIST, "w") as f:
            f.write("# Pre-existing short elbow legs (ratchet baseline — shrink this, never grow it)\n")
            f.write("\n".join(sorted(short)) + "\n")
        return []
    allowed = set()
    if os.path.exists(ALLOWLIST):
        allowed = {ln.strip() for ln in open(ALLOWLIST) if ln.strip() and not ln.startswith("#")}
    msgs = [f"floating clip: {m}" for m in floating_clips(ruby)]
    msgs += [f"collapsed elbow (leg shorter than its elbow — bad connection): {s}"
             for s in sorted(short - allowed)]
    return msgs


if __name__ == "__main__":
    msgs = run(baseline="--baseline" in sys.argv)
    for m in msgs:
        print("  " + m)
    print(f"{len(msgs)} pipe-support/connection problem(s)")
    sys.exit(1 if msgs else 0)
