# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""Pipe-support + connection audit for the water model (water.skp source, no SketchUp needed).

Three checks, all run against an in-process build of generate_pinhole_water_panel:

  floating_clips   — every P-clip strap must sit ON a pipe/tube centerline.  A clip whose pipe turned
                     away (an elbow/jog moved under it) is a support bracket holding nothing.
  ply_penetrations — a pipe may cross a plywood panel only along its thin axis, through a drilled
                     hole at least as big as the pipe; no hole, an undersized hole, or a pipe running
                     inside the ply fails (the clash checker treats ply as passable, so it can't see this).
  collapsed_elbows — (also: every ruby_pipe_run leg must be axis-aligned — a leg that moves on two axes
                     is drawn as a diagonal pipe no one can build.)
                     every elbow in a ruby_pipe_run needs straight leg on both sides (one tangent
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
    """Build water.rb in-process, recording every elbow whose legs are too short for it, every
    straight pipe segment, and every plywood part (with its drilled holes)."""
    import tbs_draw as d
    short = set()
    segs, plies = [], []
    orig = d.ruby_pipe_run
    orig_pipe, orig_box = d.ruby_pipe, d.ruby_box

    def wrap_pipe(name, p1, p2, r, *a, **k):
        segs.append((name, tuple(map(float, p1)), tuple(map(float, p2)), float(r)))
        return orig_pipe(name, p1, p2, r, *a, **k)

    def wrap_box(name, x, y, z, w, dd, h, color=None, *a, **k):
        if color == d.C_PLY and "block" not in name:
            plies.append((name, (x, y, z), (x + w, y + dd, z + h), k.get("holes") or [], k.get("hole_axis")))
        return orig_box(name, x, y, z, w, dd, h, color, *a, **k)

    def wrap(name, waypoints, r, color=None, alpha=None, elbow_r=None, n=16, seg=8, mute=0.0):
        R = elbow_r if elbow_r is not None else 2.0 * r
        V = []
        for p in waypoints:
            q = tuple(float(c) for c in p)
            if not V or math.dist(q, V[-1]) > 1e-6:
                V.append(q)
        for i in range(1, len(V)):
            if sum(abs(V[i][k] - V[i - 1][k]) > 0.5 for k in range(3)) > 1:
                short.add(f"{name} @diagonal leg {i}")
        W = [V[0]]                                     # merge collinear points (no elbow there — as ruby_pipe_run does)
        for i in range(1, len(V) - 1):
            u = [V[i][k] - W[-1][k] for k in range(3)]
            w = [V[i + 1][k] - V[i][k] for k in range(3)]
            cr = math.hypot(u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])
            if cr > 1e-6 * (math.hypot(*u) * math.hypot(*w) + 1e-9) or sum(u[k] * w[k] for k in range(3)) < 0:
                W.append(V[i])
        V = W + [V[-1]] if len(V) > 1 else V
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

    d.ruby_pipe_run, d.ruby_pipe, d.ruby_box = wrap, wrap_pipe, wrap_box
    try:
        import generate_pinhole_water_panel as pw
        ruby = pw.build()
    finally:
        d.ruby_pipe_run, d.ruby_pipe, d.ruby_box = orig, orig_pipe, orig_box
    return ruby, short, segs, plies


def ply_penetrations(segs, plies, bite=1.0):
    """Pipes that enter a plywood part.  A pipe may pass THROUGH a ply panel only along its thin axis
    and only through a drilled hole at least as big as the pipe; any other overlap (no hole, an
    undersized hole, or a pipe running inside/along the panel) is reported."""
    AX = {"x": 0, "y": 1, "z": 2}
    PLANE = {"x": (1, 2), "y": (0, 2), "z": (0, 1)}
    out = {}
    for nm, a, b, r in segs:
        if "stripe" in nm or r <= 0:
            continue
        L = math.dist(a, b)
        if L < 1e-6:
            continue
        dirv = [(b[i] - a[i]) / L for i in range(3)]
        n = max(2, int(L / 2.0))
        for pn, lo, hi, holes, hax in plies:
            if any(max(a[i], b[i]) + r < lo[i] or min(a[i], b[i]) - r > hi[i] for i in range(3)):
                continue
            for k in range(n + 1):
                q = [a[i] + dirv[i] * L * k / n for i in range(3)]
                inside = True
                for i in range(3):
                    if abs(dirv[i]) > 0.99:            # along the pipe axis: the centerline itself
                        inside &= lo[i] < q[i] < hi[i]
                    else:                              # across it: the pipe wall bites in by > `bite`
                        inside &= lo[i] - (r - bite) < q[i] < hi[i] + (r - bite)
                if not inside:
                    continue
                ok = False
                if hax and abs(dirv[AX[hax]]) > 0.99:
                    i0, i1 = PLANE[hax]
                    ok = any(math.hypot(q[i0] - ha, q[i1] - hb) + r <= hr + 0.5 for ha, hb, hr in holes)
                if not ok:
                    key = (nm, pn)
                    if key not in out:
                        out[key] = f"{nm} → {pn} at ({q[0]:.0f},{q[1]:.0f},{q[2]:.0f})" + (
                            " — passes through with no/undersized hole" if hax and abs(dirv[AX[hax]]) > 0.99
                            else " — runs inside the ply")
                    break
    return sorted(out.values())


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
    ruby, short, segs, plies = build_instrumented()
    if baseline:
        ply = [f"ply: {m.split(' at (')[0]}" for m in ply_penetrations(segs, plies)]
        with open(ALLOWLIST, "w") as f:
            f.write("# Pre-existing short elbow legs + ply penetrations (ratchet baseline — shrink this, never grow it)\n")
            f.write("\n".join(sorted(short) + sorted(ply)) + "\n")
        return []
    allowed = set()
    if os.path.exists(ALLOWLIST):
        allowed = {ln.strip() for ln in open(ALLOWLIST) if ln.strip() and not ln.startswith("#")}
    msgs = [f"floating clip: {m}" for m in floating_clips(ruby)]
    msgs += [f"ply penetration: {m}" for m in ply_penetrations(segs, plies)
             if f"ply: {m.split(' at (')[0]}" not in allowed]
    msgs += [f"collapsed elbow (leg shorter than its elbow — bad connection): {s}"
             for s in sorted(short - allowed)]
    return msgs


if __name__ == "__main__":
    msgs = run(baseline="--baseline" in sys.argv)
    for m in msgs:
        print("  " + m)
    print(f"{len(msgs)} pipe-support/connection problem(s)")
    sys.exit(1 if msgs else 0)
