#!/usr/bin/env python3
"""check_interference.py — pipe-vs-solid interference audit for the live SketchUp model.

Hand-routing pipes in the dense corridor kept reintroducing collisions (pipe through frame,
through cantilever, through pump, pipe-on-pipe).  This queries the BUILT model, gets every leaf
group's world AABB, classifies them, and reports any PIPE box that overlaps a SOLID it does not
connect to.  Permitted penetrations (Rule 5 exceptions) are skipped: IBC tanks and ply panels.

    python3 src/models/check_interference.py          # report interferences

Run it after every geometry change (this is the discipline that stops the regression).
"""
import sys, os, json
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
        return ("filter", None)
    if any(k in n for k in ("upright", "frame rail", "foot plate", "foot anchor", "rear-panel bracket",
                            "front portal", "panel mount", "retaining bar", "wall hanger", "through-bolt",
                            "front bar", "d-ring")):
        return ("frame", None)
    if any(k in n for k in ("rwk", "cantilever", "long beam", "end beam", "bearer", "upright clamp",
                            "saddle", "gusset", "fp support beam")):
        return ("cantilever", None)
    # PERMITTED penetrations / not obstacles (skip as obstacles)
    if any(k in n for k in ("ibc ", "tote", "pinhole wall", "floor", "ceiling", "end wall", "deck",
                            "walkway", "panel", "backing", "ply", "spine", "context", "scale", "person",
                            "depth ref", "label")):
        return ("skip", None)
    # PIPE (a pipe run segment, elbow, or fitting on a line)
    if ("->" in name or any(k in n for k in (" entry", "pickup", "suction", "equaliz", " tap ",
            "merge", "trunk", "fill ", "drain port", "riser", " inlet", "supply", "dead-leg",
            "spray bar", " port"))):
        return ("pipe", None)
    return ("other", None)


def overlap(a, b, tol):
    """True if AABBs a,b overlap by more than `tol` mm on every axis (shrunk by tol)."""
    for i in range(3):
        if min(a["mx"][i], b["mx"][i]) - max(a["mn"][i], b["mn"][i]) <= tol:
            return False
    return True


def main():
    data = json.loads(send_ruby(RUBY))
    pipes, solids = [], []
    for g in data:
        cat, key = classify(g["n"])
        g["cat"], g["key"] = cat, key
        if cat == "pipe":
            pipes.append(g)
        elif cat in ("pump", "acc", "filter", "frame", "cantilever"):
            solids.append(g)

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
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
