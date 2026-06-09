#!/usr/bin/env python3
"""Plan-view ROTATION STUDY — split panel (cut @ Yd653) clearing the NEAR upright.

Top-down. The film plane has TWO left uprights: the FAR one (Yd2262) is the pivot;
the NEAR one (Yd100) is in the path of the panel's near edge. So the panel is CUT at
Yd653 (= PANEL_CORNER_YD_L, between Fan B @ Yd365 and the drum aperture @ Yd713):

  FAR section  Yd653..2362 (+ drum)  → rotates with the frame; every point is closer
                                        to the pivot than the near upright → clears it
  NEAR section Yd0..653  (+ Fan B)   → separated; stays at the door (does not sweep
                                        the near upright)

Also overlays the tray + walkways (Z note: frame underside hangs at Z130 — clears the
tray rim Z50, tangent to the walkway grates Z130; the left walkway lifts out).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon

C_WID = 2362
PANEL_T = 120
DRUM_CX, DRUM_CY, DRUM_R = -400, 1181, 450
FP_Y = 2262
CUT = 653                           # panel cut (PANEL_CORNER_YD_L), between fan & drum
FAN_YD = 365
NEAR_UPRIGHT = (150, 100)           # near film-plane upright (obstacle)
HX, HY = 175, FP_Y + 25             # pivot = centre of the FAR upright
SWING = 56


def rot(pts, deg):
    th = np.radians(deg); c, s = np.cos(th), np.sin(th)
    return [(HX + (x - HX) * c - (y - HY) * s,
             HY + (x - HX) * s + (y - HY) * c) for (x, y) in pts]


def draw_far(ax, deg, color, alpha, lw=2.0):
    """The rotating FAR panel section (Yd653..2362) + drum."""
    panel = [(0, CUT), (PANEL_T, CUT), (PANEL_T, C_WID), (0, C_WID)]
    p = rot(panel, deg)
    d = rot([(DRUM_CX, DRUM_CY)], deg)[0]
    ax.add_patch(Polygon(p, closed=True, fill=False, ec=color, alpha=alpha, lw=lw))
    ax.add_patch(Circle(d, DRUM_R, fill=False, ec=color, alpha=alpha, lw=lw))
    return d


fig, ax = plt.subplots(figsize=(14, 7.8))
ax.add_patch(Rectangle((-1000, 0), 4300, C_WID, fill=False, ec="k", lw=1.2))
ax.plot([0, 0], [-60, C_WID + 60], "k--", lw=1.0)
ax.text(-30, -250, "cargo door (X0)", ha="left", fontsize=8)

# ── floor obstacles (light) ──
ax.add_patch(Rectangle((170, 80), 3130, 2200, fill=True, fc="#9fd0d8", ec="#3a8a96", alpha=0.18))
ax.text(2500, 1180, "processing tray (rim Z50)", color="#1a6a76", fontsize=8, ha="center")
ax.add_patch(Rectangle((170, 0), 3130, 300, fill=True, fc="#b0b0b8", alpha=0.35))
ax.add_patch(Rectangle((170, 2062), 3130, 300, fill=True, fc="#b0b0b8", alpha=0.35))
ax.text(2700, 150, "near walkway (Z130)", fontsize=7, ha="center", va="center")
ax.add_patch(Rectangle((170, 0), 300, C_WID, fill=True, fc="#e0a060", alpha=0.18, hatch="//"))

# ── film-plane uprights ──
ax.plot([150, 3300], [FP_Y, FP_Y], color="#2060A0", lw=1.5, alpha=0.6)
ax.plot([NEAR_UPRIGHT[0]], [NEAR_UPRIGHT[1]], "^", color="#C00000", ms=13, zorder=6)
ax.text(NEAR_UPRIGHT[0] + 70, NEAR_UPRIGHT[1], "NEAR upright (obstacle)\nX150, Yd100", color="#C00000", fontsize=8, va="center")
ax.plot([HX], [HY], "s", color="r", ms=11, zorder=6)
ax.text(HX + 70, HY + 40, "FAR upright = pivot", color="r", fontsize=8)

# ── rotating FAR section (cut..2362) sweep ──
for t in (0, 28, SWING):
    col = "#159A3C" if t == 0 else ("#1763C8" if t == SWING else "#9a9a9a")
    draw_far(ax, t, col, 1.0 if t in (0, SWING) else 0.45, lw=2.0 if t in (0, SWING) else 1.0)
fsw = [rot([(0, CUT)], t)[0] for t in np.linspace(0, SWING, 30)]
ax.plot([f[0] for f in fsw], [f[1] for f in fsw], color="#1763C8", lw=1, ls=":")
ax.text(900, 1500, "FAR section sweep —\nstays clear of the near upright", color="#1763C8", fontsize=8, ha="center")

# ── fixed NEAR section (0..653) + Fan B — stays at the door ──
ax.add_patch(Polygon([(0, 0), (PANEL_T, 0), (PANEL_T, CUT), (0, CUT)], closed=True,
                     fill=True, fc="#C8A060", ec="#8a6020", alpha=0.55, lw=1.5))
ax.text(60, 330, "NEAR section\n(Yd0-653, fixed)\n+ Fan B", color="#6a4010", fontsize=8, va="center")
ax.plot([60], [FAN_YD], "o", color="#444", ms=7); ax.text(120, FAN_YD, "Fan B (Yd365)", fontsize=7, va="center")
# cut line
ax.plot([-30, 200], [CUT, CUT], color="#a000a0", lw=2.5, ls=(0, (4, 2)))
ax.text(230, CUT, f"CUT @ Yd{CUT}\n(between fan & drum)", color="#a000a0", fontsize=8, va="center")

ax.text(-150, 1900, "CAMERA (0°)", color="#159A3C", fontsize=8.5)
d_lock = rot([(DRUM_CX, DRUM_CY)], SWING)[0]
ax.text(d_lock[0], d_lock[1] - DRUM_R - 80, f"LOCKED {SWING}°", color="#1763C8", fontsize=9, ha="center")

ax.set_xlim(-1100, 3400)
ax.set_ylim(-320, 2750)
ax.set_aspect("equal")
ax.set_xlabel("X — into container (mm)")
ax.set_ylabel("Yd — width (mm)")
ax.set_title(f"Split panel: FAR section rotates (clears near upright), NEAR section (cut @ Yd{CUT}) fixed", fontsize=11)
ax.grid(True, alpha=0.2)
plt.tight_layout()
import os
out = os.path.join(os.path.dirname(__file__), "..", "..", "diagrams", "rotation-study.png")
plt.savefig(out, dpi=120)
print("saved", os.path.abspath(out))
