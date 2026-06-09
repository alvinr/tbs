#!/usr/bin/env python3
"""Plan-view ROTATION STUDY — edge-hinge, INSET pivot, PARTIAL swing.

Top-down. The rigid frame (panel + central light-trap drum) swings about a VERTICAL
axle `x` that sits at the FILM-PLANE far upright (X150, Yd2262) — inset from the
container corner — so the pivot reuses that structural line. It swings only as far
as needed to pull the protruding drum/bay inboard of the door plane (X0) so the
cargo doors can close, then LOCKS at that transport angle (not 90°).

  x = panel/frame swing axle at the film-plane far upright (150,2262) + floor bearing
  o = drum's own revolve axle (central; spins here for the light trap)
  w = felt edge seal on the near side
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon

C_WID = 2362
PANEL_T = 120
DRUM_CX, DRUM_CY, DRUM_R = -400, 1181, 450
BAY_X0, BAY_X1 = -890, 0
APER_L, APER_R = 713, 1649
FP_Y = 2262

HX, HY = 150, FP_Y          # pivot at the film-plane far upright (inset)


def rot(pts, deg):
    th = np.radians(deg); c, s = np.cos(th), np.sin(th)
    return [(HX + (x - HX) * c - (y - HY) * s,
             HY + (x - HX) * s + (y - HY) * c) for (x, y) in pts]


def min_x_protruding(deg):
    """min X of the protruding mass (bay box + drum) at swing `deg`."""
    bay = rot([(BAY_X0, APER_L), (BAY_X0, APER_R), (BAY_X1, APER_L), (BAY_X1, APER_R)], deg)
    drum_c = rot([(DRUM_CX, DRUM_CY)], deg)[0]
    return min([p[0] for p in bay] + [drum_c[0] - DRUM_R])


# solve the lock angle: smallest swing that pulls the drum/bay inboard of X0
LOCK = next(t for t in np.arange(0, 95, 0.5) if min_x_protruding(t) >= 0)


def draw_frame(ax, deg, color, alpha, lw=2.0):
    panel = [(0, 0), (PANEL_T, 0), (PANEL_T, C_WID), (0, C_WID)]
    bay = [(BAY_X0, APER_L), (BAY_X1, APER_L), (BAY_X1, APER_R), (BAY_X0, APER_R)]
    p, b = rot(panel, deg), rot(bay, deg)
    d = rot([(DRUM_CX, DRUM_CY)], deg)[0]
    ax.add_patch(Polygon(p, closed=True, fill=False, ec=color, alpha=alpha, lw=lw))
    ax.add_patch(Polygon(b, closed=True, fill=False, ec=color, alpha=alpha * 0.7, lw=lw * 0.7, ls="--"))
    ax.add_patch(Circle(d, DRUM_R, fill=False, ec=color, alpha=alpha, lw=lw))
    ax.plot([d[0]], [d[1]], "+", color=color, ms=7, alpha=alpha)
    return d


fig, ax = plt.subplots(figsize=(13.5, 7.6))

# ── context ──
ax.add_patch(Rectangle((-1000, 0), 4300, C_WID, fill=False, ec="k", lw=1.2))
ax.plot([0, 0], [-60, C_WID + 60], "k--", lw=1.0)
ax.text(-30, -170, "cargo door (X0)\n(open during swing)", ha="left", fontsize=8)
ax.plot([150, 3300], [FP_Y, FP_Y], color="#2060A0", lw=2.5)
ax.text(2100, FP_Y + 75, "FILM PLANE screen (Yd2262, far wall)", color="#2060A0", fontsize=8)
ax.plot([150, 150], [100, FP_Y], color="#C00000", lw=4, solid_capstyle="butt")
ax.text(210, 1050, "LEFT film rails\nREMOVE for transport\n(pivot reuses the\nfar upright @ X150)", color="#C00000", fontsize=7.5, va="center")
ax.add_patch(Rectangle((0, 0), 3300, 260, fill=True, fc="#cfcfcf", ec="none", alpha=0.7))
ax.text(1700, 130, "EQUIPMENT (near wall — stays accessible)", fontsize=8, va="center", ha="center")

# ── swept band of the protruding drum centre, 0 → LOCK ──
dsweep = [rot([(DRUM_CX, DRUM_CY)], t)[0] for t in np.linspace(0, LOCK, 30)]
ax.plot([d[0] for d in dsweep], [d[1] for d in dsweep], color="#d08000", lw=1.2, ls=":")
ax.text(250, 1500, "drum swings in\n(0 → lock)", color="#a06000", fontsize=7.5)

# ── frame: camera, mid, locked ──
draw_frame(ax, 0, "#159A3C", 1.0)
draw_frame(ax, LOCK / 2, "#9a9a9a", 0.5, lw=1.2)
d_lock = draw_frame(ax, LOCK, "#1763C8", 1.0)

ax.add_patch(Circle((DRUM_CX, DRUM_CY), DRUM_R, fill=True, fc="#159A3C", alpha=0.12))
ax.text(DRUM_CX, DRUM_CY, "drum o\n(camera,\nout door)", ha="center", va="center", fontsize=7, color="#0a6")
ax.text(-150, 1850, "CAMERA\nframe shut across door", color="#159A3C", fontsize=8.5)
ax.add_patch(Circle(d_lock, DRUM_R, fill=True, fc="#1763C8", alpha=0.12))
ax.text(d_lock[0], d_lock[1], "drum\n(stowed)", ha="center", va="center", fontsize=7, color="#1763C8")
ax.text(d_lock[0], d_lock[1] - DRUM_R - 90, f"TRANSPORT — locked at {LOCK:.0f}°\n(just clears the door plane)",
        color="#1763C8", fontsize=9, ha="center")

# x pivot, w seal, lock
ax.plot([HX], [HY], "s", color="r", ms=12, zorder=6)
ax.text(HX + 60, HY + 40, "x = SWING AXLE @ film-plane\nfar upright (150,2262)\n+ floor thrust bearing", color="r", fontsize=8, va="bottom")
ax.plot([0], [0], "D", color="#E06000", ms=9, zorder=6)
ax.text(60, -40, "w = felt edge seal", color="#E06000", fontsize=8)
ax.plot([d_lock[0]], [d_lock[1] - DRUM_R - 40], "*", color="#B8860B", ms=15)
ax.text(d_lock[0] + 90, d_lock[1] - DRUM_R - 40, "LOCK", color="#8a6", fontsize=8, va="center")

ax.set_xlim(-1100, 3400)
ax.set_ylim(-380, 2750)
ax.set_aspect("equal")
ax.set_xlabel("X — into container (mm)")
ax.set_ylabel("Yd — width (mm)")
ax.set_title("Cargo-door frame — edge hinge at film-plane upright, PARTIAL swing (plan view)\n"
             f"swing {LOCK:.0f}° to pull the drum/bay inboard of X0 so doors close, then lock", fontsize=10)
ax.grid(True, alpha=0.2)
plt.tight_layout()
import os
out = os.path.join(os.path.dirname(__file__), "..", "..", "diagrams", "rotation-study.png")
plt.savefig(out, dpi=120)
print(f"saved {os.path.abspath(out)}  (lock angle {LOCK:.1f} deg)")
