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

    python3 src/models/check_interference.py          # clash audit (pipe-vs-solid + pipe-on-pipe)

Run it after every geometry change (this is the discipline that stops the regression).

Two READ-ONLY readability passes (advisory, non-gating) surface DRAWING defects where distinct parts
render as one fused piece because no seam line shows — a semantic-triage review list, not a clash:
  --solids  SAME-color solid<->solid interpenetrations (a member run THROUGH another, not a butt).
            Triage each: welded/cast → leave (a weld reads continuous); bolted/cleated → butt at the
            mating face so a seam shows.
  --pipes   pipes driven THROUGH a thin surface slab (panel/wall/plate) and emerging the far side with
            no drilled-hole seam.  Fix: a collar/grommet ring at the face, or split the pipe to butt it.
  --seams   both readability passes.
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
        # dominant COLOR — group material, else the first face's material (both_sides helpers
        # set face material only).  Two leaves that render as one fused piece share this RGB.
        mt = e.material
        if mt.nil?
          f = e.entities.find { |x| x.is_a?(Sketchup::Face) && x.material }
          mt = f ? f.material : nil
        end
        co = (mt && mt.color) ? [mt.color.red, mt.color.green, mt.color.blue] : nil
        out << {n: e.name.to_s, p: parent.to_s, co: co,
                mn: [xs.min, ys.min, zs.min], mx: [xs.max, ys.max, zs.max]}
      end
    end
  }
}
walk.call(m.entities, Geom::Transformation.new, "root")
({title: m.title.to_s, g: out}).to_json
'''

# Canonical audit artifact — the lint gate requires this refreshed whenever a plumbing routing
# generator is committed.  It records which live model was audited and carries a routing-sources-sha
# (a hash of every src/models routing generator's content); the gate re-computes that sha from the
# to-be-committed sources and blocks unless the report's sha matches — so a reroute can't land
# without the crossing/clash audit having been re-run against the live model.
_ROOT_DIR   = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPORT_PATH = os.path.join(_ROOT_DIR, "interference-report.txt")
# CALL-syntax markers (a mention in a comment must NOT count) — keep in sync with lint.py.
ROUTING_MARKERS = ("ruby_pipe_run(", "ruby_flex_run(", "ribbon_run(", "spipe(")


def routing_sources_sha(root):
    """sha of every src/models/*.py that CALLS a pipe-routing helper — identifies the routing
    source set the report attests to.  lint.py's gate recomputes this identically from the index."""
    import glob, hashlib
    parts = []
    for p in sorted(glob.glob(os.path.join(root, "src", "models", "*.py"))):
        if os.path.basename(p) == "check_interference.py":
            continue                      # the audit tool defines the markers as literals — not a generator
        try:
            t = open(p, encoding="utf-8").read()
        except OSError:
            continue
        if any(mk in t for mk in ROUTING_MARKERS):
            parts.append(os.path.relpath(p, root).replace(os.sep, "/") + "\0" + t)
    return hashlib.sha256("\0".join(parts).encode()).hexdigest()[:12]

# ── classification ─────────────────────────────────────────────────────────
PUMP_KEYS = ["P-01", "P-02", "P-03", "P-04", "P-05"]


def classify(name):
    n = name.lower()
    # SOLID obstacles a pipe must NOT pass through
    # The ceiling CABLE TRUNKING (a 40x25 PVC bundling channel) holds every circuit — cables running in
    # it are bundled, not colliding.  Skip it as an obstacle (its name matches the "trunk" pipe keyword).
    if "cable trunking" in n:
        return ("skip", None)
    # A Cct-* POWER cable often NAMES its destination ("... -> pump wireway") — it is a cable, not the
    # pump solid it feeds; let it keep its normal (pipe/skip) classification below, never "pump".
    if "pump " in n and not n.startswith("cct "):
        key = next((k for k in PUMP_KEYS if k.lower() in n), None)
        return ("pump", key)
    if "accumulator" in n or n.startswith("acc-01"):
        return ("acc", "ACC-01")
    if "filter" in n and "->" not in name and not n.startswith("cct "):   # a Cct-* cable may name "filter skid" — it's a cable, not the filter
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


# ── readability seam audits (--solids / --pipes) ─────────────────────────────
# Two SAME-material solids that interpenetrate render with NO seam line, so distinct parts read as one
# fused piece; likewise a pipe driven THROUGH a panel/wall shows no drilled-hole seam.  Neither is a
# clash (the geometry is intentional) — they are DRAWING readability defects.  These two passes surface
# them as review WARNINGS for semantic triage (weld/cast → leave; bolted/cleated/drilled → butt or
# collar).  They do NOT gate and do NOT touch the default report.

# Fasteners legitimately sink into the parts they clamp — never a readability defect; excluded from
# --solids.  Also excluded: context/scale/label helpers and translucent ghosts (no seam to read).
_FASTENER_KEYS = ("bolt", "screw", " nut", "washer", "tek", "anchor", " lag", "rivet", "stud",
                  "threaded rod", "u-joint", "u joint", "gib", "pad", "shim", "dowel", " m6",
                  " m8", " m10", " m12", "coach", "hold-down", "holddown")
_NONSOLID_KEYS = ("context", "scale", "person", "label", "depth ref", "ghost", "dim", "leader",
                  "arrow", "text", "annotation")


def is_fastener(name):
    n = name.lower()
    return any(k in n for k in _FASTENER_KEYS)


def is_readable_solid(name):
    n = name.lower()
    return not (is_fastener(name) or any(k in n for k in _NONSOLID_KEYS))


def _ovl_vol(a, b):
    """Interpenetration volume (mm^3) of two AABBs, 0 if they only touch/clear."""
    v = 1.0
    for i in range(3):
        d = min(a["mx"][i], b["mx"][i]) - max(a["mn"][i], b["mn"][i])
        if d <= 0:
            return 0.0
        v *= d
    return v


# SANCTIONED same-color solid overlaps — NOT readability defects: the overlap is intentional and a
# butt would be WRONG.  Each entry is (pat_a, pat_b, reason); a hit matches if the two names contain the
# two patterns (either order).  Once the clean end-butts are done (posts↔plates, RWk end-beams), every
# remaining flagged overlap falls in one of these by-design classes.  (The J6 backing plate ↔ frame rail
# corner is deliberately NOT here — it is a real structural congestion to resolve in design, so it stays
# an OPEN flag.)
_SANCTIONED_SOLID = [
    # ONE-PIECE formed / welded parts drawn as overlapping primitives (no real seam exists):
    ("u-rail", "u-rail", "one formed U-channel (web + flanges)"),
    ("wall cleat plate", "wall cleat shelf", "one welded L-cleat (plate + shelf)"),
    ("wall cleat ext plate", "wall cleat shelf", "one welded L-cleat (ext plate + shelf)"),
    ("door frame", "door frame", "one welded door frame (stiles/top/threshold)"),
    ("fp combined", "fp combined", "one combined corner plate (seat + rail seat + plate)"),
    ("drum c-shell", "drum bottom cap", "one welded drum (shell + cap)"),
    ("drum c-shell", "drum top cap", "one welded drum (shell + cap)"),
    ("housing arc", "drum", "light-trap housing + drum assembly"),
    ("drum c-shell", "grab rail", "grab rail welded to the drum shell"),
    ("drum", "bay wall", "drum seated in the light-trap bay"),
    ("housing arc", "bay wall", "housing arc seated in the light-trap bay"),
    # ASSEMBLED fan unit (baffle duct + frame + plates + flange bolt/weld together):
    ("fan", "fan", "one fan assembly (duct/frame/baffle/flange)"),
    # COMPRESSION seals (must interpenetrate the frame/drum to seal — a butt would leave a gap):
    ("seal", "", "compression seal (EPDM/brush) squeezed into its frame"),
    ("brush seal", "", "compression brush seal"),
    ("gasket", "", "compression gasket"),
    # BEARING / shaft fits and shrink/press collars:
    ("bearing", "shaft", "bearing bore on its shaft (interference fit)"),
    ("thrust collar", "pivot post", "thrust collar clamped on the pivot post"),
    # LIQUID contents inside a vessel (not a solid seam):
    ("bath", "", "chemistry bath liquid inside the tray/spray/manifold"),
    ("water in manifold", "poly manifold", "concentric spray manifolds"),
    # SEATED structural connections — the member bears IN/ON a cleat/seat by design (the engagement
    # represents the bearing; a flush butt would float the beam off its seat):
    ("long beam", "wall cleat plate", "left long beam seated in its wall cleat"),
    ("end beam", "wall cleat plate", "end beam seated in its wall cleat"),
    ("long beam", "fp combined", "right long beam seated on the combined corner plate"),
    ("pivot post", "roof mount plate", "pivot post seated in its roof mount"),
]


def is_sanctioned_solid(a_name, b_name):
    na, nb = a_name.lower(), b_name.lower()
    for pa, pb, _r in _SANCTIONED_SOLID:
        if (pa in na and (pb == "" or pb in nb)) or (pa in nb and (pb == "" or pb in na)):
            return True
    return False


def solids_pass(data, min_overlap_mm=2.0, min_vol_mm3=1000.0):
    """SAME-color solid<->solid interpenetrations (a member passing THROUGH another, not merely
    butting a face) above a volume threshold.  Butted joints touch on one axis only (overlap ~0 on the
    mating axis) so they don't flag; a bar run THROUGH a post overlaps on all three axes and does.
    Same RGB is the trigger because that's exactly when the shared material erases the seam.
    Intentional by-design overlaps (compression seals, formed one-piece sections, seated connections,
    bearing fits) are partitioned off via is_sanctioned_solid so only OPEN defects are flagged."""
    sols = [g for g in data
            if g.get("co") and is_readable_solid(g["n"])
            and classify(g["n"])[0] not in ("pipe", "skip")]
    hits = []
    for i in range(len(sols)):
        A = sols[i]
        for j in range(i + 1, len(sols)):
            B = sols[j]
            if A["co"] != B["co"]:
                continue                              # different color → the seam already reads
            if run_base(A["n"]) == run_base(B["n"]):
                continue                              # parts of one logical member
            if not overlap(A, B, min_overlap_mm):     # true 3-axis interpenetration, not a butt
                continue
            vol = _ovl_vol(A, B)
            if vol < min_vol_mm3:
                continue
            c = [round((max(A["mn"][k], B["mn"][k]) + min(A["mx"][k], B["mx"][k])) / 2) for k in range(3)]
            hits.append((vol, A, B, c))
    hits.sort(key=lambda h: -h[0])
    # partition: intentional by-design overlaps (sanctioned) vs OPEN readability defects.  Dedupe on the
    # sorted name pair so a phased/duplicated model doesn't multi-count the same joint.
    seen, open_hits, sanctioned = set(), [], 0
    for vol, A, B, c in hits:
        k = tuple(sorted((A["n"], B["n"])))
        if k in seen:
            continue
        seen.add(k)
        if is_sanctioned_solid(A["n"], B["n"]):
            sanctioned += 1
        else:
            open_hits.append((vol, A, B, c))
    print(f"same-color solid interpenetrations: {len(open_hits)} OPEN + {sanctioned} sanctioned(OK)  "
          f"(OPEN = a real fused-seam defect: butt at the mating face, or notch a true crossing)")
    for vol, A, B, c in open_hits:
        print(f"  OPEN  {A['n']:40.40s} ({A['p']})")
        print(f"    x   {B['n']:40.40s}  overlap {vol/1000:.1f}cm^3 @ ({c[0]},{c[1]},{c[2]})")
    return len(open_hits)


# Surfaces a pipe is drilled THROUGH (a hole + collar should show); the pipe reads as fused into the
# slab when it just interpenetrates.  A pipe that ENDS at / stops short of a face butts cleanly — only
# a pipe crossing the FULL thickness and emerging the far side is the no-seam defect.
_SURFACE_KEYS = ("panel", "ply", " wall", "plate", "deck", "backing", "grate", "floor", "ceiling",
                 "bulkhead", "baffle", "board")


def is_surface(name):
    n = name.lower()
    return any(k in n for k in _SURFACE_KEYS) and not is_fastener(name)


# SANCTIONED pipe-through-surface penetrations — NOT readability defects.  --pipes tests the surface's
# AABB, which neither a drilled hole nor a thin tilted pan shrinks, so it can't tell these are fine; this
# is the fixed record.  Two kinds:
#   • DRILLED — the panel carries a real clearance hole (the `holes=` lists in
#     generate_corridor_water_panel.py rear_panel(), cut with ruby_box's coplanar-pushpull drill).  ADD a
#     pair here whenever a new penetration is drilled (mirror the generator's holes= entry).
#   • BY-DESIGN — the penetration is the component's own function through a razor-thin skin (e.g. the sump
#     drain through the 2mm SS tray pan — a real drain fitting; the "13mm slab" --pipes sees is only the
#     tilted pan's Z-AABB, not a real thickness, so a separate drawn hole adds nothing).
_SANCTIONED_PIPE = [
    ("blue #1 -> p-01",        "pump-mount ply shirt"),
    ("p-05 -> x3 end-wall",    "pump-mount ply shirt"),
    ("x4 waste (p-03) pickup", "pump-mount ply shirt"),
    ("cct c branch p-02",      "pump-mount ply shirt"),
    ("cct c branch p-05",      "pump-mount ply shirt"),
    ("dv-01 -> ibc-4 merge",   "rear panel"),
    ("dv-02 waste -> ibc-4",   "rear panel"),
    ("blue #1 -> p-01",        "rear panel"),
    ("p-05 -> x3 end-wall",    "rear panel"),
    ("x4 waste (p-03) pickup", "rear panel"),
    ("cct c branch p-02",      "rear panel"),
    ("cct c branch p-05",      "rear panel"),
    ("blue equalization",      "drain-riser backing spine"),
    ("tray sump -> p-04",      "processing tray floor"),   # BY-DESIGN sump drain through the 2mm pan
]


def is_sanctioned_pipe(pipe_name, surf_name):
    pn, sn = pipe_name.lower(), surf_name.lower()
    return any(pk in pn and sk in sn for pk, sk in _SANCTIONED_PIPE)


def pipes_pass(data, margin=1.0):
    """Pipes driven THROUGH a thin surface slab (perpendicular, emerging the far side) with no
    drilled-hole seam.  Flags only full-thickness through-penetrations — a pipe that stops at/within a
    face is a clean butt.  Fix per hit: draw a short collar/grommet ring at the face, or split the pipe
    at the surface so each side butts it."""
    pipes = [g for g in data if classify(g["n"])[0] == "pipe"]
    surfs = [g for g in data if is_surface(g["n"])]
    hits = []
    for p in pipes:
        rep = rep_of(p)
        if rep[0] != "seg":
            continue                                  # elbow/fitting body, not a straight run
        A, B = rep[1], rep[2]
        la = max(range(3), key=lambda k: abs(B[k] - A[k]))    # pipe long axis
        pmin, pmax = min(A[la], B[la]), max(A[la], B[la])
        # pipe in-plane center (the two axes that are NOT the run axis)
        for s in surfs:
            dims = [s["mx"][k] - s["mn"][k] for k in range(3)]
            ta = min(range(3), key=lambda k: dims[k])         # surface thin axis
            if ta != la:
                continue                              # pipe runs along the face, not through it
            # full-thickness crossing: pipe spans past BOTH faces on the thin axis
            if not (pmin < s["mn"][ta] - margin and pmax > s["mx"][ta] + margin):
                continue
            # pipe passes within the surface's in-plane footprint
            inplane = [k for k in range(3) if k != ta]
            pc = [(A[k] + B[k]) / 2 for k in range(3)]
            if all(s["mn"][k] - margin <= pc[k] <= s["mx"][k] + margin for k in inplane):
                thick = dims[ta]
                c = [round(pc[k]) if k != ta else round((s["mn"][ta] + s["mx"][ta]) / 2) for k in range(3)]
                hits.append((thick, p, s, c))
    hits.sort(key=lambda h: -h[0])
    seen = set()
    open_hits, sanctioned = [], 0
    for thick, p, s, c in hits:
        k = (p["n"], s["n"])
        if k in seen:
            continue
        seen.add(k)
        if is_sanctioned_pipe(p["n"], s["n"]):
            sanctioned += 1
        else:
            open_hits.append((thick, p, s, c))
    print(f"pipe-through-surface penetrations={len(open_hits)} open + {sanctioned} sanctioned(OK)  "
          f"(fix: drill a clearance hole via ruby_box holes=, or split the pipe so each side butts it)")
    for thick, p, s, c in open_hits:
        print(f"  PIPE  {p['n']:42.42s} ({p['p']})")
        print(f"    thru {s['n']:42.42s}  {thick:.0f}mm slab @ ({c[0]},{c[1]},{c[2]})")
    return len(open_hits)


def main():
    payload = json.loads(send_ruby(RUBY))
    title = payload.get("title", "?")
    data = payload["g"]
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
    RIBBON_LINES = ("-> p-02 inlet", "single filtered line", "corridor -> ribbon", "p-04 suction",
                    "dv-02 waste -> ibc-4", "p-02 -> acc-02")

    TOL = 3.0   # mm — ignore mere touching
    hits = []
    for pipe in pipes:
        for sol in solids:
            # a pipe is allowed to meet the component it connects to (name references its key)
            if sol["key"] and sol["key"].lower() in pipe["n"].lower():
                continue
            # Cct-* POWER cables terminate INTO the pumps / master switch they feed (all "pump"-category
            # solids, incl. "Pump zone ghost" + "Master pump switch") — a connection, not a collision.
            if pipe["n"].lower().startswith("cct ") and sol["cat"] == "pump":
                continue
            # the sanctioned under-walkway ribbon may cross the tray footprint AND push up/down through
            # the grate (the loop-over penetrations) — but NOT any real structural solid
            if sol["cat"] in ("tray", "grate") and any(r in pipe["n"].lower() for r in RIBBON_LINES):
                continue
            if overlap(pipe, sol, TOL):
                hits.append((pipe, sol))

    print(f"model={title}  pipes={len(pipes)} solids={len(solids)}  interferences={len(hits)}")
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


def _readability(which):
    """Run the seam-readability passes against the live model (READ-ONLY query)."""
    payload = json.loads(send_ruby(RUBY))
    title = payload.get("title", "?")
    data = payload["g"]
    print(f"model={title}  leaves={len(data)}")
    n = 0
    if which in ("solids", "all"):
        n += solids_pass(data)
    if which in ("pipes", "all"):
        n += pipes_pass(data)
    return 0 if n == 0 else 0   # advisory only — never a nonzero (non-gating) exit


if __name__ == "__main__":
    if "--solids" in sys.argv:
        sys.exit(_readability("solids"))
    if "--pipes" in sys.argv:
        sys.exit(_readability("pipes"))
    if "--readability" in sys.argv or "--seams" in sys.argv:
        sys.exit(_readability("all"))
    if "--write" in sys.argv:
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = main()
        sys.stdout.write(buf.getvalue())
        header = f"routing-sources-sha: {routing_sources_sha(_ROOT_DIR)}\n"
        with open(REPORT_PATH, "w") as fh:
            fh.write(header + buf.getvalue())
        print(f"\n(written to {os.path.relpath(REPORT_PATH)})")
        sys.exit(rc)
    sys.exit(main())
