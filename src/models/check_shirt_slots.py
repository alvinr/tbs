#!/usr/bin/env python3
"""check_shirt_slots.py — verify the pump-mount ply 'shirt' is not impaled by IN-PLANE pipes.

check_interference.py SKIPS pipe-through-ply (treats penetrations as permitted), so it does NOT
catch pipes that lie in the plane of the shirt.  A pipe crossing the shirt PERPENDICULAR (along X,
through the 25mm thickness) only needs a round drilled hole — OK.  A pipe running IN the shirt plane
(a vertical riser or a Yd-run whose X sits inside the shirt band) would need a routed-out RECTANGULAR
slot — NOT OK.  This queries the live model and flags any pipe segment that is in-plane within the
shirt's X-band, so the shirt fix can be verified.

    python3 src/models/check_shirt_slots.py
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sketchup_client import send_ruby

# Shirt X-band (front..back).  Keep in sync with rear_panel()'s shirt: front ≈ PXC+ACC_R+4, 25mm thick.
import massing_corridor_panel as cp
SX0 = cp.PXC + cp.ACC_R + 4
SX1 = SX0 + 25
SY0, SY1 = cp.YD_NEAR + cp.S, cp.YD_FAR - cp.S      # shirt Yd span
SZ0, SZ1 = 275, 1925                                # shirt Z span (bottom raised to clear the low suction elbow)

RUBY = r'''
require 'json'
m = Sketchup.active_model
out = []
walk = nil
walk = lambda { |ents, t|
  ents.each { |e|
    if e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance)
      ee = e.is_a?(Sketchup::Group) ? e.entities : e.definition.entities
      if ee.any? { |x| x.is_a?(Sketchup::Face) }
        b=e.bounds; xs=[];ys=[];zs=[]
        (0..7).each{|i| p=(t*e.transformation)*b.corner(i); xs<<p.x.to_mm; ys<<p.y.to_mm; zs<<p.z.to_mm}
        out << {n:e.name.to_s, mn:[xs.min,ys.min,zs.min], mx:[xs.max,ys.max,zs.max]}
      end
      walk.call(ee, t*e.transformation)
    end
  }
}
walk.call(m.entities, Geom::Transformation.new)
out.to_json
'''


def ov(a0, a1, b0, b1):
    return a0 < b1 and b0 < a1


def main():
    data = json.loads(send_ruby(RUBY))
    print(f"shirt band X[{SX0:.1f},{SX1:.1f}] Yd[{SY0},{SY1}] Z[{SZ0},{SZ1}]")
    slots, holes, solids = [], 0, []
    for d in data:
        n = d['n']
        low = n.lower()
        if 'shirt' in low or 'ply' in low or 'panel' in low:
            continue
        mn, mx = d['mn'], d['mx']
        if not (ov(mn[0], mx[0], SX0, SX1) and ov(mn[1], mx[1], SY0, SY1) and ov(mn[2], mx[2], SZ0, SZ1)):
            continue
        xs, ys, zs = mx[0]-mn[0], mx[1]-mn[1], mx[2]-mn[2]
        # a pipe SEGMENT is ~21mm in its two cross-section axes; a solid body is fat in 2+ axes.
        is_pipey = (n.startswith(('Filter', 'Pump', 'ACC')) is False)
        # perpendicular crosser: long in X (spans through the band) -> round hole, OK
        if xs > 40:
            holes += 1
            continue
        # in-plane: short in X (sits in the band) and long in Yd or Z -> would need a SLOT
        if ys > 40 or zs > 40:
            slots.append((n, [round(mn[0]), round(mx[0])], [round(mn[1]), round(mx[1])], [round(mn[2]), round(mx[2])]))
        else:
            # small in all axes within the band — a fitting/elbow/solid sitting in the shirt
            solids.append((n, [round(mn[0]), round(mx[0])], [round(mn[1]), round(mx[1])], [round(mn[2]), round(mx[2])]))
    print(f"\nperpendicular crossings (round holes, OK): {holes}")
    print(f"\nIN-PLANE segments needing a RECTANGULAR SLOT (NOT OK): {len(slots)}")
    for n, x, y, z in sorted(slots):
        print(f"  SLOT  {n[:44]:44} X{x} Yd{y} Z{z}")
    print(f"\nsmall bodies/fittings sitting in the shirt band (check): {len(solids)}")
    for n, x, y, z in sorted(solids):
        print(f"  body  {n[:44]:44} X{x} Yd{y} Z{z}")
    return len(slots)


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
