#!/usr/bin/env python3
"""check_interference.py — pipe-vs-solid interference audit for the live SketchUp model.

Hand-routing pipes in the dense corridor kept reintroducing collisions (pipe through frame,
through cantilever, through pump, pipe-on-pipe).  This queries the BUILT model, gets every leaf
group's world AABB, classifies them, and reports:
  1. PIPE-vs-SOLID — any pipe box that overlaps a solid it does not connect to.  Permitted
     penetrations (Rule 5 exceptions) are skipped: IBC tanks and ply panels.
  2. PIPE-on-PIPE — any two pipe RUNS that overlap without being the same run or meeting at a
     shared junction fitting (tee/cross/diverter).

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
    """Collapse a run's segment/elbow leaves to one identity: ruby_pipe_run names straights
    '<run>' and elbows '<run> elbow', so strip the elbow suffix."""
    return name[:-6] if name.endswith(" elbow") else name


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

    TOL = 3.0   # mm — ignore mere touching
    hits = []
    for pipe in pipes:
        for sol in solids:
            # a pipe is allowed to meet the component it connects to (name references its key)
            if sol["key"] and sol["key"].lower() in pipe["n"].lower():
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

    # ── pipe-on-pipe ─────────────────────────────────────────────────────────
    # Two pipe RUNS that overlap collide UNLESS they're the same run (adjacent segments share an
    # elbow) or they meet at a shared junction fitting (tee/cross/diverter — a legitimate
    # connection).  This is the case the pipe-vs-solid pass can't see.
    runs = [p for p in pipes if is_run(p["n"])]
    junctions = [g for g in data if is_junction(g["n"])]
    JTOL = 20.0   # mm — a run end "abuts" a junction if within this of its fitting body
    # Two runs are CONNECTED if they both abut a common junction (tee/cross/diverter/valve); they
    # then share plumbing (e.g. a short out-and-back to a sample valve) and any overlap is legit.
    abut = defaultdict(set)
    for r in runs:
        rb = run_base(r["n"])
        for ji, J in enumerate(junctions):
            if near(r, J, JTOL):
                abut[rb].add(ji)
    pp = []
    for i in range(len(runs)):
        for j in range(i + 1, len(runs)):
            a, b = runs[i], runs[j]
            ra, rb = run_base(a["n"]), run_base(b["n"])
            if ra == rb or not overlap(a, b, TOL):
                continue
            if abut[ra] & abut[rb]:        # connected at a shared junction → not colliding
                continue
            pp.append((a, b))

    print(f"pipe-on-pipe={len(pp)}")
    seen2 = set()
    for a, b in pp:
        k = tuple(sorted((run_base(a["n"]), run_base(b["n"]))))
        if k in seen2:
            continue
        seen2.add(k)
        c = [round((max(a["mn"][i], b["mn"][i]) + min(a["mx"][i], b["mx"][i])) / 2) for i in range(3)]
        print(f"  PIPE  {run_base(a['n']):42.42s} ({a['p']})")
        print(f"    x  PIPE       {run_base(b['n']):38.38s}  near ({c[0]},{c[1]},{c[2]})")
    return 1 if (hits or pp) else 0


if __name__ == "__main__":
    sys.exit(main())
