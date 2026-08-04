#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""check_interference.py — pipe-vs-solid interference audit for the live SketchUp model.

Hand-routing pipes in the dense corridor kept reintroducing collisions (pipe through frame,
through cantilever, through pump, pipe-on-pipe).  This queries the BUILT model, gets every leaf
group's world AABB, classifies them, and reports:
  1. PIPE-vs-SOLID — any pipe box that overlaps a solid it does not connect to.  Permitted
     penetrations (Rule 5 exceptions) are skipped: IBC tanks and ply panels.
  2. PIPE-on-PIPE CROSSINGS — any two pipe RUNS whose CENTERLINES pass within (r_a + r_b) of each
     other (the pipes physically share space), excluding the same run, runs joined end-to-end, and
     runs meeting at a shared junction fitting (tee/cross/diverter/valve).  Uses true segment-to-
     segment distance, not AABB overlap, so parallel neighbours and Z-staggered over/unders (a clear
     gap) do NOT flag — only pipes actually crossing through each other.

    python3 src/models/check_interference.py          # report both

Run it after every geometry change (this is the discipline that stops the regression).
"""
import sys, os, json
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sketchup_client import send_ruby

RUBY = r'''
require 'json'
m = Sketchup.active_model
out = []
walk = nil
walk = lambda { |ents, t, parent|
  ents.each { |e|
    if e.is_a?(Sketchup::ComponentInstance)
      pn = (e.name.nil? || e.name.empty?) ? parent : e.name
      walk.call(e.definition.entities, t * e.transformation, pn)
    elsif e.is_a?(Sketchup::Group)
      has_geom = e.entities.any? { |x| x.is_a?(Sketchup::Face) }
      has_sub  = e.entities.any? { |x| x.is_a?(Sketchup::Group) || x.is_a?(Sketchup::ComponentInstance) }
      walk.call(e.entities, t * e.transformation, parent) if has_sub
      if has_geom
        b = e.bounds
        xs = []; ys = []; zs = []
        (0..7).each { |i| p = t * b.corner(i); xs << p.x.to_mm; ys << p.y.to_mm; zs << p.z.to_mm }
        out << {n: e.name.to_s, p: parent.to_s,
                mn: [xs.min, ys.min, zs.min], mx: [xs.max, ys.max, zs.max]}
      end
    end
  }
}
walk.call(m.entities, Geom::Transformation.new, "root")
out.to_json
'''

# ── classification ─────────────────────────────────────────────────────────
PUMP_KEYS = ["P-01", "P-02", "P-03", "P-04", "P-05"]


def classify(name):
    n = name.lower()
    # SOLID obstacles a pipe must NOT pass through
    if "pump " in n:
        key = next((k for k in PUMP_KEYS if k.lower() in n), None)
        return ("pump", key)
    if "accumulator" in n or n.startswith("acc-01"):
        return ("acc", "ACC-01")
    if "filter" in n and "->" not in name:
        import re
        m = re.search(r"\bf(\d)\b", n)           # key = "F1"/"F2"/"F3" so a pipe naming that
        return ("filter", f"F{m.group(1)}" if m else None)   # filter (it connects to) is excluded
    if any(k in n for k in ("upright", "frame rail", "foot plate", "foot anchor", "rear-panel bracket",
                            "front portal", "panel mount", "retaining bar", "wall hanger", "through-bolt",
                            "front bar", "d-ring")):
        return ("frame", None)
    if "grate" in n:                   # the walkway GRATE (a surface) — the sump drain may loop
        return ("grate", "sump")       # up THROUGH it and back down (key "sump" excludes the drain)
    if "walkway near bracket" in n and "gusset" in n:
        return ("skip", None)          # the bracket gusset is a TRIANGLE — its low-outer corner is open
                                       # (a pipe tucks under it against the tray rim); AABB would over-flag
    if any(k in n for k in ("rwk", "cantilever", "long beam", "end beam", "bearer", "upright clamp",
                            "saddle", "gusset", "fp support beam", "walkway near bracket", "walkway bracket")):
        return ("cantilever", None)
    if ("tray" in n or "print on" in n) and "->" not in name:
        return ("skip", None)          # the real tray geometry is an OPEN basin; the footprint
                                       # exclusion is enforced by a synthetic box (see main)
    # PERMITTED penetrations / not obstacles (skip as obstacles)
    if any(k in n for k in ("ibc ", "tote", "pinhole wall", "floor", "ceiling", "end wall", "deck",
                            "walkway", "panel", "backing", "ply", "spine", "context", "scale", "person",
                            "depth ref", "label")):
        return ("skip", None)
    # PIPE (a pipe run segment, elbow, or fitting on a line)
    if ("->" in name or any(k in n for k in (" entry", "pickup", "suction", "equaliz", " tap ",
            "merge", "trunk", "fill ", "drain port", "riser", " inlet", "supply", "dead-leg",
            "spray bar", " port", "branch", "tap-0", "bv-0 riser"))):
        return ("pipe", None)
    return ("other", None)


def overlap(a, b, tol):
    """True if AABBs a,b overlap by more than `tol` mm on every axis (shrunk by tol)."""
    for i in range(3):
        if min(a["mx"][i], b["mx"][i]) - max(a["mn"][i], b["mn"][i]) <= tol:
            return False
    return True


def near(a, b, margin):
    """True if AABBs a,b overlap OR sit within `margin` mm of each other on every axis."""
    for i in range(3):
        if min(a["mx"][i], b["mx"][i]) - max(a["mn"][i], b["mn"][i]) < -margin:
            return False
    return True


# ── centerline geometry (precise pipe-on-pipe crossing detection) ────────────
# AABB overlap can't tell a real crossing from two parallel neighbours or an end-to-end join, so the
# pipe-on-pipe pass reduces each pipe leaf to its CENTERLINE and measures the true distance between
# lines.  Every straight pipe segment is axis-aligned, so its AABB is tight and the centerline exact.
def _sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def _add(a, b): return (a[0] + b[0], a[1] + b[1], a[2] + b[2])
def _scl(a, s): return (a[0] * s, a[1] * s, a[2] * s)
def _dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def _len(a):    return _dot(a, a) ** 0.5
def _clip(x, lo, hi): return lo if x < lo else hi if x > hi else x


def rep_of(g):
    """Reduce a pipe leaf's AABB to a centerline primitive: a dominant-axis box → an axis-aligned
    segment ('seg', A, B, radius); a near-cubic box (elbow/fitting body) → a sphere ('pt', c, radius)."""
    mn, mx = g["mn"], g["mx"]
    dims = [mx[i] - mn[i] for i in range(3)]
    mid = [(mn[i] + mx[i]) / 2 for i in range(3)]
    order = sorted(range(3), key=lambda i: dims[i])          # ascending extent
    la = order[2]
    if dims[la] > 2 * dims[order[1]] + 1:                    # one axis clearly dominates → straight
        A = list(mid); B = list(mid); A[la] = mn[la]; B[la] = mx[la]
        r = (dims[order[0]] / 2) or (dims[order[1]] / 2)
        return ("seg", tuple(A), tuple(B), max(r, 3.0))
    return ("pt", tuple(mid), max(dims) / 2)


def _seg_seg(p1, q1, p2, q2):
    """Closest distance + points between two 3D segments (Ericson, Real-Time Collision Detection)."""
    d1 = _sub(q1, p1); d2 = _sub(q2, p2); r = _sub(p1, p2)
    a = _dot(d1, d1); e = _dot(d2, d2); f = _dot(d2, r)
    if a <= 1e-9 and e <= 1e-9:
        s = t = 0.0
    elif a <= 1e-9:
        s = 0.0; t = _clip(f / e, 0, 1)
    else:
        c = _dot(d1, r)
        if e <= 1e-9:
            t = 0.0; s = _clip(-c / a, 0, 1)
        else:
            b = _dot(d1, d2); denom = a * e - b * b
            s = _clip((b * f - c * e) / denom, 0, 1) if denom > 1e-12 else 0.0
            t = (b * s + f) / e
            if t < 0:   t = 0.0; s = _clip(-c / a, 0, 1)
            elif t > 1: t = 1.0; s = _clip((b - c) / a, 0, 1)
    c1 = _add(p1, _scl(d1, s)); c2 = _add(p2, _scl(d2, t))
    return _len(_sub(c1, c2)), c1, c2


def _seg_pt(p1, q1, p):
    d = _sub(q1, p1); a = _dot(d, d)
    s = 0.0 if a <= 1e-9 else _clip(_dot(_sub(p, p1), d) / a, 0, 1)
    c1 = _add(p1, _scl(d, s))
    return _len(_sub(c1, p)), c1, p


def closest(r1, r2):
    """Min distance + the two closest points between two centerline primitives (seg/pt)."""
    if r1[0] == "seg" and r2[0] == "seg":
        return _seg_seg(r1[1], r1[2], r2[1], r2[2])
    if r1[0] == "seg":
        return _seg_pt(r1[1], r1[2], r2[1])
    if r2[0] == "seg":
        d, c2, c1 = _seg_pt(r2[1], r2[2], r1[1]); return d, c1, c2
    return _len(_sub(r1[1], r2[1])), r1[1], r2[1]


def _radius(rep): return rep[3] if rep[0] == "seg" else rep[2]
def _ends(rep):   return [rep[1], rep[2]] if rep[0] == "seg" else [rep[1]]


# A pipe RUN (from ruby_pipe_run) is always named "A -> B"; fittings/valves never are.  JUNCTIONS are
# the points where pipes legitimately MEET — tees, crosses, diverters, and in-line valves (a run can
# end at a sample/ball valve where the next run begins).  Two runs overlapping at a shared junction are
# CONNECTED, not colliding, so they're excluded from the pipe-on-pipe check.
JUNCTION_KEYS = ("tee", " cross", "diverter", "3w-dv", "merge", "socket cuff", "tap t",
                 "valve", "bv-0", "sv-0", "sample")


def is_junction(name):
    if "->" in name:
        return False                  # that's a pipe run, not a fitting body
    n = name.lower()
    return any(k in n for k in JUNCTION_KEYS)


def run_base(name):
    """Collapse the leaves of ONE logical line (source→dest) to a single identity.  ruby_pipe_run
    names straights '<run>' and elbows '<run> elbow'; a connection is often modeled in parts that
    are co-located BY DESIGN ('<run> entry', '<run> flex jumper') — strip all such descriptor
    suffixes so those parts aren't reported as crossing each other."""
    n = name
    changed = True
    while changed:
        changed = False
        for suf in (" elbow", " flex jumper", " jumper", " entry"):
            if n.endswith(suf):
                n = n[:-len(suf)]; changed = True
    return n


def is_run(name):
    """A real pipe RUN to test for crossings — excludes flanges (fittings on a run) and the
    electrical cable bundles (legitimately run together)."""
    n = name.lower()
    if "->" not in name or "flange" in n:
        return False
    return not any(k in n for k in ("cable", "busbar", "awg", " wire", "lug", "conduit"))


def main():
    data = json.loads(send_ruby(RUBY))
    pipes, solids = [], []
    for g in data:
        cat, key = classify(g["n"])
        g["cat"], g["key"] = cat, key
        if cat == "pipe":
            pipes.append(g)
        elif cat in ("pump", "acc", "filter", "frame", "cantilever", "tray", "grate"):
            solids.append(g)

    # The processing tray is a TOTAL EXCLUSION ZONE: no pipe may cross its footprint at deck level.
    # (The real basin is open geometry, so enforce the footprint with a synthetic box.)  Only the
    # sump drain — which connects to the sump — is allowed (key "sump").
    solids.append({"n": "PROCESSING TRAY (exclusion zone)", "p": "synthetic", "cat": "tray", "key": "sump",
                   "mn": [170, 80, 0], "mx": [4629, 2280, 130]})

    # SANCTIONED Rule 5a exception: the four corridor↔pinhole-wall lines run as a flat RIBBON in the
    # dead space UNDER the right-walkway grate (over the tray's outer margin, below the grate), by
    # design — they loop UP over the cantilevers (never through them).  Excluded from the tray box
    # only (still fully checked against every real solid: cantilevers, beams, frame, equipment).
    RIBBON_LINES = ("-> p-02 inlet", "single filtered line", "corridor -> ribbon", "p-04 suction")

    TOL = 3.0   # mm — ignore mere touching
    hits = []
    for pipe in pipes:
        for sol in solids:
            # a pipe is allowed to meet the component it connects to (name references its key)
            if sol["key"] and sol["key"].lower() in pipe["n"].lower():
                continue
            # the sanctioned under-walkway ribbon may cross the tray footprint AND push up/down through
            # the grate (the loop-over penetrations) — but NOT any real structural solid
            if sol["cat"] in ("tray", "grate") and any(r in pipe["n"].lower() for r in RIBBON_LINES):
                continue
            if overlap(pipe, sol, TOL):
                hits.append((pipe, sol))

    print(f"pipes={len(pipes)} solids={len(solids)}  interferences={len(hits)}")
    seen = set()
    for pipe, sol in hits:
        k = (pipe["n"], sol["n"])
        if k in seen:
            continue
        seen.add(k)
        c = [round((pipe["mn"][i] + pipe["mx"][i]) / 2) for i in range(3)]
        print(f"  PIPE  {pipe['n']:42.42s} ({pipe['p']})")
        print(f"    x  {sol['cat'].upper():10s} {sol['n']:38.38s}  near ({c[0]},{c[1]},{c[2]})")

    # ── pipe-on-pipe CROSSINGS (precise centerline test) ─────────────────────
    # Two pipe RUNS COLLIDE when their centerlines pass within (r_a + r_b) — the pipes physically
    # share space — UNLESS: same run (adjacent segments), they meet at a shared junction fitting
    # (tee/cross/diverter/valve), or the near point is a JOIN (both leaves touch there at an endpoint =
    # an end-to-end connection, e.g. a run and its own flex jumper).  A properly Z-STAGGERED crossing
    # (a clear over/under gap) does NOT share space and is NOT flagged — only pipes actually crossing
    # THROUGH each other are.  This replaces the old whole-box AABB overlap (flagged parallel
    # neighbours + joins, missed thin crossings).
    leaves = [p for p in pipes if is_run(p["n"])]
    for L in leaves:
        L["rep"] = rep_of(L)
    junctions = [g for g in data if is_junction(g["n"])]
    JTOL = 20.0   # mm — a run end "abuts" a junction if within this of its fitting body
    abut = defaultdict(set)
    for L in leaves:
        rb = run_base(L["n"])
        for ji, J in enumerate(junctions):
            if near(L, J, JTOL):
                abut[rb].add(ji)
    JOINTOL = 25.0        # a near point this close to an endpoint of BOTH leaves = an end-to-end join
    worst = {}            # run-base pair -> (gap, midpoint, dist, clearance); keep the deepest overlap
    for i in range(len(leaves)):
        A = leaves[i]; ra = run_base(A["n"]); repA = A["rep"]; rA = _radius(repA)
        for j in range(i + 1, len(leaves)):
            B = leaves[j]; rb = run_base(B["n"])
            if ra == rb or (abut[ra] & abut[rb]):
                continue
            repB = B["rep"]; rB = _radius(repB)
            d, cA, cB = closest(repA, repB)
            clear = rA + rB
            if d >= clear - 0.5:                       # not sharing space (incl. staggered crossings)
                continue
            nearA = min(_len(_sub(cA, e)) for e in _ends(repA))
            nearB = min(_len(_sub(cB, e)) for e in _ends(repB))
            if nearA <= JOINTOL and nearB <= JOINTOL:  # end-to-end JOIN, not a crossing
                continue
            key = tuple(sorted((ra, rb)))
            gap = d - clear                            # negative = interpenetration depth
            if key not in worst or gap < worst[key][0]:
                mid = tuple(round((cA[k] + cB[k]) / 2) for k in range(3))
                worst[key] = (gap, mid, round(d), round(clear))

    print(f"pipe-on-pipe crossings={len(worst)}")
    for key in sorted(worst, key=lambda k: worst[k][0]):
        gap, mid, d, clear = worst[key]
        print(f"  PIPE  {key[0]:44.44s}")
        print(f"    x  PIPE  {key[1]:44.44s}  cross ({mid[0]},{mid[1]},{mid[2]})  centreline {d}mm < {clear}mm")
    return 1 if (hits or worst) else 0


if __name__ == "__main__":
    sys.exit(main())
