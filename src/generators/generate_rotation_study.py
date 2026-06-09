#!/usr/bin/env python3
"""Plan-view ROTATION STUDY — swing arc vs the processing tray + walkways.

Top-down. The rigid frame (panel + central drum) swings 56° about the vertical axle
`x` at the film-plane far upright (X150, Yd2262). This overlays the SWEPT footprint
(frame drawn at intermediate angles) on the floor obstacles to check clearance:

  processing tray  X170..4629  Yd80..2280   (rim Z50)
  near walkway     Yd0..300                 (grate Z115..130)
  far walkway      Yd2062..2362             (grate Z115..130)
  left walkway     X170..470                (REMOVABLE — lifts out for transport)

Z note: the frame hangs at the panel floor-gap Z130, so its swinging underside is at
Z130 — clears the tray rim (Z50) by 80mm, but is TANGENT to the fixed near/far
walkway grates (Z130). The left walkway (in the swing) is removed for transport.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon

C_WID = 2362
PANEL_T = 120
DRUM_CX, DRUM_CY, DRUM_R = -400, 1181, 450
BAY_X0 = -890
APER_L, APER_R = 713, 1649
FP_Y = 2262
HX, HY = 175, FP_Y + 25             # CENTRE of the far film-plane upright (X150-200, Yd2262-2312)
SWING = 56                          # locked transport angle (matches the 3D model)


def rot(pts, deg):
    th = np.radians(deg); c, s = np.cos(th), np.sin(th)
    return [(HX + (x - HX) * c - (y - HY) * s,
             HY + (x - HX) * s + (y - HY) * c) for (x, y) in pts]


def draw_frame(ax, deg, color, alpha, lw=2.0):
    panel = [(0, 0), (PANEL_T, 0), (PANEL_T, C_WID), (0, C_WID)]
    p = rot(panel, deg)
    d = rot([(DRUM_CX, DRUM_CY)], deg)[0]
    ax.add_patch(Polygon(p, closed=True, fill=False, ec=color, alpha=alpha, lw=lw))
    ax.add_patch(Circle(d, DRUM_R, fill=False, ec=color, alpha=alpha, lw=lw))
    return d


fig, ax = plt.subplots(figsize=(14, 7.6))
ax.add_patch(Rectangle((-1000, 0), 4300, C_WID, fill=False, ec="k", lw=1.2))
ax.plot([0, 0], [-60, C_WID + 60], "k--", lw=1.0)
ax.text(-30, -240, "cargo door (X0)", ha="left", fontsize=8)

# ── floor obstacles ──
ax.add_patch(Rectangle((170, 80), 3130, 2200, fill=True, fc="#9fd0d8", ec="#3a8a96", alpha=0.30, lw=1))
ax.text(2300, 1180, "PROCESSING TRAY (basin, rim Z50)", color="#1a6a76", fontsize=9, ha="center")
ax.add_patch(Rectangle((170, 0), 3130, 300, fill=True, fc="#b0b0b8", ec="#777", alpha=0.55))
ax.text(2300, 150, "NEAR walkway (grate Z115-130)", fontsize=7.5, ha="center", va="center")
ax.add_patch(Rectangle((170, 2062), 3130, 300, fill=True, fc="#b0b0b8", ec="#777", alpha=0.55))
ax.text(2300, 2212, "FAR walkway (grate Z115-130)", fontsize=7.5, ha="center", va="center")
ax.add_patch(Rectangle((170, 0), 300, C_WID, fill=True, fc="#e0a060", ec="#a06000", alpha=0.30, hatch="//"))
ax.text(320, 1500, "LEFT walkway\nREMOVABLE\n(out for transport)", color="#804000", fontsize=7, ha="center", va="center", rotation=90)
# film plane + removable left rails
ax.plot([150, 3300], [FP_Y, FP_Y], color="#2060A0", lw=2.0)
ax.text(2600, FP_Y + 70, "film plane (Yd2262)", color="#2060A0", fontsize=7.5)
ax.plot([150, 150], [100, FP_Y], color="#C00000", lw=3, alpha=0.5)

# ── swept footprint of the frame, 0 → SWING ──
for t in (0, 14, 28, 42, SWING):
    col = "#159A3C" if t == 0 else ("#1763C8" if t == SWING else "#9a9a9a")
    al = 1.0 if t in (0, SWING) else 0.4
    draw_frame(ax, t, col, al, lw=2.0 if t in (0, SWING) else 1.0)
# shade the drum's swept band
dsw = [rot([(DRUM_CX, DRUM_CY)], t)[0] for t in np.linspace(0, SWING, 30)]
ax.add_patch(Polygon([(HX, HY)] + dsw, closed=True, fc="#f0a000", ec="none", alpha=0.10))

ax.text(-150, 1850, "CAMERA (0°)", color="#159A3C", fontsize=8.5)
d_lock = rot([(DRUM_CX, DRUM_CY)], SWING)[0]
ax.text(d_lock[0], d_lock[1] - DRUM_R - 90, f"LOCKED {SWING}°", color="#1763C8", fontsize=9, ha="center")
ax.plot([HX], [HY], "s", color="r", ms=11, zorder=6)
ax.text(HX + 70, HY + 60, "axle x (150,2262)", color="r", fontsize=8)

# ── findings box ──
ax.text(-1050, 2640,
        "CLEARANCE:  swept footprint overlaps the tray + walkways in plan, BUT the frame hangs at Z130 (floor gap):\n"
        "  • TRAY rim Z50  → frame underside Z130 clears it by 80mm  ✓ (the +50 walkway raise pays off here)\n"
        "  • NEAR/FAR walkway grates Z130 → frame underside Z130 = TANGENT → confirm a few mm gap (lower the grate locally / lift the frame)\n"
        "  • LEFT walkway is in the swing → it's the removable lift-out → out for transport  ✓",
        fontsize=8, va="top", family="monospace",
        bbox=dict(boxstyle="round", fc="#fffbe6", ec="#caa"))

ax.set_xlim(-1100, 3400)
ax.set_ylim(-300, 2950)
ax.set_aspect("equal")
ax.set_xlabel("X — into container (mm)")
ax.set_ylabel("Yd — width (mm)")
ax.set_title(f"Rotation swing ({SWING}°) vs processing tray + walkways (plan view)", fontsize=11)
ax.grid(True, alpha=0.2)
plt.tight_layout()
import os
out = os.path.join(os.path.dirname(__file__), "..", "..", "diagrams", "rotation-study.png")
plt.savefig(out, dpi=120)
print("saved", os.path.abspath(out))
