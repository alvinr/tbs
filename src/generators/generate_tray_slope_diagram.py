#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""Processing-tray drainage: the Yd-only surface slope + the self-draining near-rim gutter
that falls 1:200 inward to a single CENTER pickup.

Sheets (all read tbs_constants — single source):
  1. Plan — Yd surface fall + near-rim gutter converging to the center pickup + spray beam.
  2. Section A-A (Yd-Z) — the surface falls far→near into the gutter (beam rides the surface).
  3. Section B-B (X-Z, near rim) — gutter V-slopes to the center pickup; the LEVEL beam clears
     the level walkway support arms.
  4. Details — near-rim fall-off + the gutter's inward X-slope, both inside the 20mm sump budget.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyArrow, Circle

from tbs_constants import PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR, PROC_TRAY_D, PROC_TRAY_FLOOR_Z_LOW, PROC_TRAY_FLOOR_Z_HIGH, PROC_TRAY_DRAIN_X, PROC_TRAY_SUMP_W, PROC_TRAY_SUMP_Z, PROC_TRAY_GUTTER_W, PROC_TRAY_GUTTER_Z_CENTER, PROC_TRAY_GUTTER_Z_END, tray_floor_z, tray_gutter_floor_z, SPRAY_BEAM_X_L, SPRAY_BEAM_X_R, SPRAY_BAR_BEAM_BOT_RISE, SPRAY_BAR_BEAM_H, SPRAY_BAR_BEAM_TOP_RISE, WALKWAY_LEFT_X, WALKWAY_RIGHT_X, WALKWAY_W, WALKWAY_H, WALKWAY_GRATE_T, LEFT_WK_CANT_ARM_Z0, DIAGRAMS_DIR
from tbs_title_block import title_block

TOTAL_SHEETS = 4
XC = PROC_TRAY_DRAIN_X                       # 2399 — center pickup
L_ARM_Z = LEFT_WK_CANT_ARM_Z0               # 75 — left cantilever-arm underside
R_ARM_Z = LEFT_WK_CANT_ARM_Z0                # right frame underside now MATCHES the left (Z75)
GRATE_B = WALKWAY_H - WALKWAY_GRATE_T        # 115 — grate bottom
C_SURF = "#8a6d3b"; C_WATER = "#0B3D66"; C_GUT = "#7EA8D8"
C_BEAM = "#8892A0"; C_WK = "#C8D8E8"; C_STEEL = "#B0B0B8"


def _tb(fig, sheet, subtitle, scale_note):
    ax = fig.add_axes([0.04, 0.005, 0.92, 0.055]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    title_block(ax, f"SHEET {sheet} OF {TOTAL_SHEETS}", drawing_title="PROCESSING TRAY — DRAINAGE",
                subtitle=subtitle, scale_note=scale_note)


def _save(fig, name):
    path = os.path.join(DIAGRAMS_DIR, name)
    fig.savefig(path, dpi=150); plt.close(fig); print(f"  {path} saved")


# ── Sheet 1 — PLAN ────────────────────────────────────────────────────────────
def sheet1():
    fig = plt.figure(figsize=(13, 8.4))
    ax = fig.add_axes([0.06, 0.12, 0.90, 0.80]); ax.set_aspect("equal")
    XL, XR, YN, YF = PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR
    ax.add_patch(Rectangle((XL, YN), XR - XL, PROC_TRAY_D, facecolor="#EAF1F7", edgecolor="#2060A0", lw=1.6))
    for wk in [(XL, 0, XR - XL, 300), (XL, 2062, XR - XL, 300),
               (WALKWAY_LEFT_X, 300, WALKWAY_W, 1762), (WALKWAY_RIGHT_X, 300, WALKWAY_W, 1762)]:
        ax.add_patch(Rectangle(wk[:2], wk[2], wk[3], facecolor=C_WK, edgecolor="#7a7a7a", lw=0.7, alpha=0.85))
    for x in (900, 1700, XC, 3100, 3900):
        ax.add_patch(FancyArrow(x, 1750, 0, -950, width=14, head_width=70, head_length=90,
                     color="#2E8B57", alpha=.8, length_includes_head=True))
    ax.text(XC, 1930, "SURFACE falls far → near (Yd only — LEVEL across X)", ha="center",
            fontsize=10, color="#1E6E1E", fontweight="bold")
    gy = YN + PROC_TRAY_GUTTER_W / 2
    ax.add_patch(Rectangle((XL, YN), XR - XL, PROC_TRAY_GUTTER_W, facecolor=C_GUT, edgecolor="#204060", lw=1.0))
    ax.add_patch(FancyArrow(900, gy, XC - 1350, 0, width=10, head_width=55, head_length=90, color=C_WATER, length_includes_head=True))
    ax.add_patch(FancyArrow(3900, gy, -(XC - 1350), 0, width=10, head_width=55, head_length=90, color=C_WATER, length_includes_head=True))
    ax.add_patch(Circle((XC, gy), 70, facecolor=C_WATER, edgecolor="k", zorder=6))
    ax.text(XC, YN - 130, "single CENTER pickup\n(P-04 suction pops out of the walkway,\nruns under it to the IBC end)",
            ha="center", va="top", fontsize=8.5, color=C_WATER, fontweight="bold")
    ax.text(XC, YN + PROC_TRAY_GUTTER_W + 55, "near-rim GUTTER falls both ways → center", ha="center", fontsize=8.5, color=C_WATER)
    ax.add_patch(Rectangle((SPRAY_BEAM_X_L, 1180 - 20), SPRAY_BEAM_X_R - SPRAY_BEAM_X_L, 40, facecolor=C_BEAM, edgecolor="#111", lw=1.0))
    ax.text(XC, 1140, "spray beam — level across X (clears the walkway arms)", ha="center", fontsize=8, color="#111")
    for xx, lab in [(XL - 55, "A"), ]:
        ax.text(xx, YF + 40, "A", fontsize=12, fontweight="bold", color="#B00"); ax.text(xx, YN - 40, "A", fontsize=12, fontweight="bold", color="#B00")
    ax.plot([XL - 55, XL - 55], [YN, YF], color="#B00", lw=0.8, ls=":")
    ax.text(XC - 340, YN - 250, "B", fontsize=12, fontweight="bold", color="#B00"); ax.text(XR + 60, YN - 250, "B", fontsize=12, fontweight="bold", color="#B00")
    ax.plot([XC, XR + 60], [YN - 20, YN - 20], color="#B00", lw=0.8, ls=":")
    ax.set_xlim(XL - 200, XR + 200); ax.set_ylim(YN - 320, YF + 120)
    ax.set_xlabel("X (mm)"); ax.set_ylabel("Yd (mm)")
    ax.set_title("PLAN — Yd surface slope (green) + near-rim gutter to a single center pickup (blue)", fontsize=11)
    ax.grid(True, ls=":", lw=0.4, alpha=0.4)
    _tb(fig, 1, "PLAN — YD SURFACE FALL + NEAR-RIM GUTTER TO CENTER PICKUP", "PLAN — TO SCALE")
    _save(fig, "tray-slope-sheet1.png")


# ── Sheet 2 — SECTION A-A (Yd-Z) ────────────────────────────────────────────────
def sheet2():
    fig = plt.figure(figsize=(12, 6.0))
    ax = fig.add_axes([0.07, 0.16, 0.88, 0.72])
    yds = list(range(PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR + 1, 20))
    ax.plot(yds, [tray_floor_z(XC, y) for y in yds], color=C_SURF, lw=2.4)
    ax.fill_between(yds, [tray_floor_z(XC, y) - 3 for y in yds], [tray_floor_z(XC, y) for y in yds], color=C_STEEL)
    ax.add_patch(Rectangle((PROC_TRAY_YD_NEAR, PROC_TRAY_GUTTER_Z_CENTER), PROC_TRAY_GUTTER_W,
                 PROC_TRAY_FLOOR_Z_LOW - PROC_TRAY_GUTTER_Z_CENTER, facecolor=C_GUT, edgecolor="#204060"))
    ax.text(PROC_TRAY_YD_NEAR + PROC_TRAY_GUTTER_W + 10, 6, "near-rim gutter", fontsize=8, color=C_WATER)
    yb = 1200
    ax.add_patch(Rectangle((yb - 40, tray_floor_z(XC, yb) + SPRAY_BAR_BEAM_BOT_RISE), 80, SPRAY_BAR_BEAM_H,
                 facecolor=C_BEAM, edgecolor="#111"))
    ax.text(yb, tray_floor_z(XC, yb) + SPRAY_BAR_BEAM_TOP_RISE + 3, "spray beam\n(rides the surface)", ha="center", fontsize=7.5)
    ax.annotate(f"{PROC_TRAY_FLOOR_Z_HIGH - PROC_TRAY_FLOOR_Z_LOW:.0f}mm fall over {PROC_TRAY_D}mm (1:200)",
                xy=(PROC_TRAY_YD_FAR, PROC_TRAY_FLOOR_Z_HIGH), xytext=(1200, 55), fontsize=8.5, color=C_SURF,
                arrowprops=dict(arrowstyle="->", color=C_SURF))
    ax.set_xlim(0, PROC_TRAY_YD_FAR + 60); ax.set_ylim(0, 80)
    ax.set_xlabel("Yd (mm):  near rim (L) → far rim (R)"); ax.set_ylabel("Z (mm), exaggerated")
    ax.set_title("SECTION A-A — surface falls far→near into the near-rim gutter", fontsize=11)
    ax.grid(True, ls=":", lw=0.4, alpha=0.4)
    _tb(fig, 2, "SECTION A-A — YD SURFACE FALL INTO THE GUTTER", "VERTICAL SCALE EXAGGERATED")
    _save(fig, "tray-slope-sheet2.png")


# ── Sheet 3 — SECTION B-B (X-Z at the near rim) ─────────────────────────────────
def sheet3():
    fig = plt.figure(figsize=(13, 5.6))
    ax = fig.add_axes([0.06, 0.17, 0.90, 0.70])
    XL, XR = PROC_TRAY_X_L, PROC_TRAY_X_R
    xs = list(range(XL, XR + 1, 40))
    ax.plot(xs, [tray_gutter_floor_z(x) for x in xs], color=C_WATER, lw=2.0)
    ax.fill_between(xs, [tray_gutter_floor_z(x) for x in xs], [PROC_TRAY_FLOOR_Z_LOW] * len(xs), color="#CFE0F2", alpha=.6)
    ax.plot([XL, XR], [PROC_TRAY_FLOOR_Z_LOW, PROC_TRAY_FLOOR_Z_LOW], color=C_SURF, lw=1.5)
    ax.add_patch(Rectangle((XC - PROC_TRAY_SUMP_W / 2, 0), PROC_TRAY_SUMP_W, PROC_TRAY_GUTTER_Z_CENTER, facecolor=C_WATER))
    ax.text(XC, -3, "center pickup well → Z0", ha="center", va="top", fontsize=8, color=C_WATER)
    ax.add_patch(Rectangle((SPRAY_BEAM_X_L, PROC_TRAY_FLOOR_Z_LOW + SPRAY_BAR_BEAM_BOT_RISE),
                 SPRAY_BEAM_X_R - SPRAY_BEAM_X_L, SPRAY_BAR_BEAM_H, facecolor=C_BEAM, edgecolor="#111"))
    ax.text(XC, PROC_TRAY_FLOOR_Z_LOW + SPRAY_BAR_BEAM_TOP_RISE + 5, "spray beam — LEVEL across X", ha="center", fontsize=8.5, color="#111")
    ax.add_patch(Rectangle((WALKWAY_LEFT_X, L_ARM_Z), WALKWAY_W, GRATE_B - L_ARM_Z, facecolor=C_WK, edgecolor="#204060"))
    ax.text(WALKWAY_LEFT_X + WALKWAY_W / 2, L_ARM_Z + 6, f"L arm Z{L_ARM_Z}", ha="center", fontsize=7.5, color="#204060")
    ax.add_patch(Rectangle((WALKWAY_RIGHT_X, R_ARM_Z), WALKWAY_W, GRATE_B - R_ARM_Z, facecolor=C_WK, edgecolor="#204060"))
    ax.text(WALKWAY_RIGHT_X + WALKWAY_W / 2, R_ARM_Z + 6, f"R arm Z{R_ARM_Z}", ha="center", fontsize=7.5, color="#204060")
    beam_top = PROC_TRAY_FLOOR_Z_LOW + SPRAY_BAR_BEAM_TOP_RISE
    ax.annotate(f"beam top Z{beam_top:.0f} — clears the arms", xy=(1200, beam_top), xytext=(1500, beam_top + 22),
                fontsize=8, color="#2E8B57", arrowprops=dict(arrowstyle="->", color="#2E8B57"))
    ax.set_xlim(XL - 100, XR + 100); ax.set_ylim(-6, GRATE_B + 8)
    ax.set_xlabel("X (mm):  left end → center pickup → right end"); ax.set_ylabel("Z (mm), exaggerated")
    ax.set_title("SECTION B-B — gutter V-slopes to the center pickup; the level beam clears the walkway arms", fontsize=10.5)
    ax.grid(True, ls=":", lw=0.4, alpha=0.4)
    _tb(fig, 3, "SECTION B-B — GUTTER TO CENTER PICKUP + BEAM CLEARANCE", "VERTICAL SCALE EXAGGERATED")
    _save(fig, "tray-slope-sheet3.png")


# ── Sheet 4 — details: near-rim fall-off + gutter X-slope in the 20mm budget ─────
def sheet4():
    fig = plt.figure(figsize=(13, 6.2))
    # left: Yd-Z fall-off at the center section
    ax = fig.add_axes([0.06, 0.16, 0.42, 0.72])
    ax.axhline(0, color="#333", lw=2)
    ax.plot([500, 200], [tray_floor_z(XC, 500), PROC_TRAY_FLOOR_Z_LOW], color=C_SURF, lw=2.2)
    ax.plot([200, 160], [PROC_TRAY_FLOOR_Z_LOW, PROC_TRAY_FLOOR_Z_LOW], color=C_SURF, lw=2.2)
    ax.add_patch(Polygon([(160, PROC_TRAY_FLOOR_Z_LOW), (160, PROC_TRAY_GUTTER_Z_CENTER),
                 (95, PROC_TRAY_GUTTER_Z_CENTER), (80, PROC_TRAY_FLOOR_Z_LOW)], closed=True, facecolor=C_GUT, edgecolor="#204060"))
    ax.add_patch(Rectangle((100, 0), 40, PROC_TRAY_GUTTER_Z_CENTER, facecolor=C_WATER))
    ax.annotate("", xy=(60, 0), xytext=(60, PROC_TRAY_FLOOR_Z_LOW), arrowprops=dict(arrowstyle="<->", color="#B00", lw=1.3))
    ax.text(52, PROC_TRAY_FLOOR_Z_LOW / 2, f"{PROC_TRAY_SUMP_Z}mm\nbudget", fontsize=8, color="#B00", ha="right", va="center", fontweight="bold")
    ax.text(300, 40, "fall-off into the gutter", fontsize=8.5, color=C_WATER)
    ax.set_xlim(40, 510); ax.set_ylim(-8, 150); ax.set_xlabel("Yd (mm): near rim → inboard"); ax.set_ylabel("Z (mm), exag.")
    ax.set_title("Near-rim fall-off (center)", fontsize=9.5); ax.grid(True, ls=":", lw=0.4, alpha=0.4)
    # right: gutter inward X-slope in the 20mm budget
    ax2 = fig.add_axes([0.55, 0.16, 0.42, 0.72])
    XL, XR = PROC_TRAY_X_L, PROC_TRAY_X_R
    xs = list(range(XL, XR + 1, 40))
    ax2.axhline(0, color="#333", lw=2); ax2.axhline(PROC_TRAY_FLOOR_Z_LOW, color=C_SURF, lw=1.8)
    ax2.plot(xs, [tray_gutter_floor_z(x) for x in xs], color=C_WATER, lw=2.2)
    ax2.fill_between(xs, [tray_gutter_floor_z(x) for x in xs], [PROC_TRAY_FLOOR_Z_LOW] * len(xs), color="#CFE0F2", alpha=.6)
    ax2.text(XC, PROC_TRAY_GUTTER_Z_CENTER + 2.6, f"gutter falls 1:200 → center ({PROC_TRAY_GUTTER_Z_END - PROC_TRAY_GUTTER_Z_CENTER:.0f}mm)",
             ha="center", fontsize=8, color=C_WATER, fontweight="bold")
    ax2.text(XC, PROC_TRAY_FLOOR_Z_LOW + 3, "tray surface Z20 (level across X)", ha="center", fontsize=8, color=C_SURF)
    ax2.set_xlim(0, XR + 100); ax2.set_ylim(-4, 28); ax2.set_xlabel("X (mm): end → center pickup → end"); ax2.set_ylabel("Z (mm), exag.")
    ax2.set_title("Gutter inward slope, within the 20mm budget", fontsize=9.5); ax2.grid(True, ls=":", lw=0.4, alpha=0.4)
    _tb(fig, 4, "DETAILS — NEAR-RIM FALL-OFF + GUTTER INWARD SLOPE", "VERTICAL SCALE EXAGGERATED")
    _save(fig, "tray-slope-sheet4.png")


if __name__ == "__main__":
    sheet1(); sheet2(); sheet3(); sheet4()
