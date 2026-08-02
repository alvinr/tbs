#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_tray_redesign.py — PROPOSAL diagrams for the processing-tray
304-SS -> welded-polypropylene redesign (branch: tray-redesign).

Sheet 1: construction cross-section (Yd-Z), vertical-exaggerated — the welded-PP
         basin on a sloped plywood sub-floor, sump, weld detail + an SS-vs-PP
         seam comparison inset.
Sheet 2: plan — PP 4-sheet butt-weld layout vs the current SS 2-panel lap seam.

These are for design review only; nothing in parts.py / tbs_constants.py changes
until the proposal is approved.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

from tbs_constants import C_OUT, C_CL, C_DIM, C_STEEL, C_GASKT, C_WOOD, PROC_TRAY_W, PROC_TRAY_D, PROC_TRAY_RIM, PROC_TRAY_PITCH, DIAGRAMS_DIR, DIAGRAM_DPI
from tbs_title_block import title_block
from tbs_drawing import draw_dim_h, draw_dim_v, leader

C_PP   = "#7CA88C"   # polypropylene basin (green-grey)
C_PLY  = C_WOOD      # plywood sub-floor
TOTAL_SHEETS = 2


def _weld(ax, x, y, r=9, color="#C0392B"):
    """Field-weld flag: filled triangle (hot-air / extrusion PP weld)."""
    ax.add_patch(Polygon([(x - r, y), (x + r, y), (x, y + 1.7 * r)],
                         closed=True, fc=color, ec="none", zorder=20))


def sheet1():
    fig = plt.figure(figsize=(11, 8.5))
    ax = fig.add_axes([0.07, 0.30, 0.88, 0.63])

    # ---- vertical-exaggerated Yd-Z section (x = Yd mm, y = Z mm * EXAG) ----
    EXAG = 7.0
    def Z(z): return z * EXAG
    near, far = 0, PROC_TRAY_D                     # Yd 0..2200 (near rim -> far rim)
    z_low, z_hi = 20, 20 + PROC_TRAY_PITCH         # PP floor top: 20 near(sump) -> 30 far
    ply_t = 18                                     # plywood sub-floor nominal thickness
    pp_t  = 4.8                                    # 3/16" PP
    rim   = PROC_TRAY_RIM

    # container floor (ground) + hatch
    ax.plot([near - 120, far + 120], [Z(0), Z(0)], color=C_OUT, lw=1.6, zorder=4)
    for gx in range(int(near) - 100, int(far) + 140, 90):
        ax.plot([gx, gx - 45], [Z(0), Z(0) - 26], color=C_DIM, lw=0.6, zorder=3)
    ax.text(far + 120, Z(0) - 30, "container floor (Z0)", fontsize=6.5,
            color=C_DIM, ha="right", va="top")

    # sloped plywood sub-floor (wedge: thicker at far to make the 1:200 fall)
    ply_near_top = z_low - pp_t
    ply_far_top  = z_hi - pp_t
    ax.add_patch(Polygon([(near, Z(0)), (far, Z(0)),
                          (far, Z(ply_far_top)), (near, Z(ply_near_top))],
                         closed=True, fc=C_PLY, ec=C_OUT, lw=1.2, zorder=6))

    # welded-PP basin: floor (follows slope) + near & far rim walls + sump well
    # floor slab
    ax.add_patch(Polygon([(near, Z(z_low - pp_t)), (far, Z(z_hi - pp_t)),
                          (far, Z(z_hi)), (near, Z(z_low))],
                         closed=True, fc=C_PP, ec=C_OUT, lw=1.4, zorder=8))
    # far rim wall (up)
    ax.add_patch(Rectangle((far - pp_t, Z(z_hi)), pp_t, Z(rim),
                           fc=C_PP, ec=C_OUT, lw=1.4, zorder=9))
    # near rim wall (up, past the sump)
    ax.add_patch(Rectangle((near, Z(z_low)), pp_t, Z(rim),
                           fc=C_PP, ec=C_OUT, lw=1.4, zorder=9))
    # sump well: PP drops SUMP_Z below the floor at the near/low corner
    sump_w, sump_drop = 150, 20
    ax.add_patch(Polygon([(near, Z(z_low - pp_t)), (near, Z(z_low - pp_t - sump_drop)),
                          (near + sump_w, Z(z_low - pp_t - sump_drop)),
                          (near + sump_w, Z(z_low - pp_t))],
                         closed=True, fc=C_PP, ec=C_OUT, lw=1.4, zorder=8.5))
    # foot-valve pickup in the sump
    ax.add_patch(Rectangle((near + 40, Z(z_low - pp_t - sump_drop) + 3), 26, Z(28),
                           fc=C_STEEL, ec=C_OUT, lw=1.0, zorder=11))
    leader(ax, near + 53, Z(z_low - pp_t - sump_drop) + Z(20), near + 430, Z(z_hi + rim) - Z(6),
           "1\" foot-valve pickup -> P-04", fs=6.2, color=C_OUT)

    # weld flags — floor-to-wall corners + one representative floor butt-weld
    _weld(ax, near + pp_t + 2, Z(z_low) + 2)
    _weld(ax, far - pp_t - 2, Z(z_hi) + 2)
    _weld(ax, (near + far) / 2, Z((z_low + z_hi) / 2 - pp_t) + 2)
    leader(ax, (near + far) / 2, Z((z_low + z_hi) / 2 - pp_t) + 20, (near + far) / 2 + 250,
           Z(z_hi + rim) - Z(4), "hot-air / extrusion PP welds\n(seamless, watertight)",
           fs=6.2, color="#C0392B")

    # dimensions
    draw_dim_h(ax, near, far, Z(z_hi + rim) + 42, f"tray depth {PROC_TRAY_D:,}mm (Yd)")
    draw_dim_v(ax, far + 90, Z(z_hi), Z(z_hi + rim), f"rim {rim}mm")
    draw_dim_v(ax, near - 95, Z(z_low - pp_t - sump_drop), Z(z_low - pp_t),
               f"sump {sump_drop}mm")
    ax.annotate("", xy=(far - 250, Z(z_hi - pp_t) + 6), xytext=(near + 250, Z(z_low - pp_t) + 6),
                arrowprops=dict(arrowstyle="->", color=C_CL, lw=1.0))
    ax.text((near + far) / 2, Z(z_low) - 8, "1:200 fall to sump", fontsize=6.4,
            color=C_CL, ha="center", va="top", style="italic")

    ax.text(near, Z(z_hi + rim) + 78, "WELDED-PP BASIN on a sloped plywood sub-floor",
            fontsize=9, color=C_OUT, fontweight="bold", va="bottom")
    ax.text(far, Z(ply_far_top) - 14, "sloped exterior-ply sub-floor\n(sets the fall + continuous support)",
            fontsize=6.2, color="#6B4E2E", ha="right", va="top")

    ax.set_xlim(near - 260, far + 260)
    ax.set_ylim(Z(0) - 70, Z(z_hi + rim) + 150)
    ax.set_aspect("equal"); ax.axis("off")

    # ---- comparison inset: SS lap seam vs PP butt weld ----
    axc = fig.add_axes([0.09, 0.10, 0.40, 0.17]); axc.axis("off")
    axc.set_xlim(0, 100); axc.set_ylim(0, 34)
    axc.text(0, 33, "SEAM: current SS vs proposed PP", fontsize=7.5,
             color=C_OUT, fontweight="bold", va="top")
    # SS lap (two overlapped panels + bolt + silicone)
    axc.add_patch(Rectangle((4, 14), 44, 4, fc=C_STEEL, ec=C_OUT, lw=1.0))
    axc.add_patch(Rectangle((30, 17.5), 44, 4, fc=C_STEEL, ec=C_OUT, lw=1.0))
    axc.add_patch(Rectangle((33, 13.5), 8, 1.6, fc=C_GASKT, ec="none"))
    axc.plot([37, 37], [12, 23], color=C_OUT, lw=1.2)
    axc.text(37, 9, "40mm lap: silicone + M6 bolt", fontsize=5.6, color=C_DIM, ha="center")
    axc.text(2, 20, "SS", fontsize=6.5, color=C_OUT, fontweight="bold")
    # PP butt weld
    axc.add_patch(Rectangle((4, 3), 42, 4, fc=C_PP, ec=C_OUT, lw=1.0))
    axc.add_patch(Rectangle((48, 3), 42, 4, fc=C_PP, ec=C_OUT, lw=1.0))
    _weld(axc, 47, 7, r=2.4)
    axc.text(47, 0.5, "butt weld: seamless, no hardware", fontsize=5.6, color="#C0392B", ha="center")

    ax_tb = fig.add_axes([0.04, 0.005, 0.92, 0.05])
    title_block(ax_tb, f"SHEET 1 OF {TOTAL_SHEETS}",
                drawing_title="PROCESSING TRAY — WELDED-PP OPTION (EVALUATED, NOT ADOPTED)",
                subtitle="research record — the SS basin was retained (see tray-research.md)", doc_id="TBS-RES-TRAY")
    ax_tb.set_axis_off()
    out = os.path.join(DIAGRAMS_DIR, "tray-redesign-sheet1.png")
    fig.savefig(out, dpi=DIAGRAM_DPI); plt.close(fig)
    print(f"  {out} saved")


def sheet2():
    fig = plt.figure(figsize=(11, 8.5))

    # ---- proposed PP: seamless 4-sheet butt-weld layout ----
    axp = fig.add_axes([0.07, 0.55, 0.88, 0.38])
    W, D = PROC_TRAY_W, PROC_TRAY_D
    axp.add_patch(Rectangle((0, 0), W, D, fc="#EAF2ED", ec=C_OUT, lw=1.8, zorder=3))
    # 4 sheets: 2 across (X) x 2 deep (Yd) — 48x96in (1219x2438) each, butt-welded
    sx, sy = W / 2, D / 2
    for i in (1,):
        axp.plot([sx, sx], [0, D], color="#C0392B", lw=1.8, zorder=6)   # vertical butt weld
        axp.plot([0, W], [sy, sy], color="#C0392B", lw=1.8, zorder=6)   # horizontal butt weld
    for cx, cy, t in [(sx/2, sy/2, "sheet 1"), (sx*1.5, sy/2, "sheet 2"),
                       (sx/2, sy*1.5, "sheet 3"), (sx*1.5, sy*1.5, "sheet 4")]:
        axp.text(cx, cy, t, fontsize=7, color=C_DIM, ha="center", va="center")
    # sump corner
    axp.add_patch(Rectangle((W - 158, 0), 158, 100, fc=C_PP, ec=C_OUT, lw=1.2, zorder=7))
    leader(axp, W - 79, 50, W - 620, 260, "corner sump well", fs=6.4, color=C_OUT)
    draw_dim_h(axp, 0, W, D + 90, f"{PROC_TRAY_W:,}mm")
    draw_dim_v(axp, -70, 0, D, f"{PROC_TRAY_D:,}mm")
    axp.text(0, D + 150, "PROPOSED — welded PP: 4 sheets, butt-welded into ONE seamless basin (red = welds)",
             fontsize=8.5, color=C_OUT, fontweight="bold", va="bottom")
    axp.set_xlim(-160, W + 60); axp.set_ylim(-40, D + 210)
    axp.set_aspect("equal"); axp.axis("off")

    # ---- current SS: 2 panels + center lap seam ----
    axs = fig.add_axes([0.07, 0.13, 0.88, 0.32])
    axs.add_patch(Rectangle((0, 0), W, D, fc="#EEEFF1", ec=C_OUT, lw=1.8, zorder=3))
    axs.add_patch(Rectangle((W/2 - 20, 0), 40, D, fc=C_GASKT, ec=C_OUT, lw=1.0, alpha=0.5, zorder=6))
    for cx, t in [(W/4, "SS panel 1 (2,229x2,200)"), (W*3/4, "SS panel 2 (2,229x2,200)")]:
        axs.text(cx, D/2, t, fontsize=7, color=C_DIM, ha="center", va="center")
    for by in range(180, int(D), 360):
        axs.plot(W/2, by, marker="o", ms=3, color=C_OUT, zorder=7)
    leader(axs, W/2 + 12, D - 260, W*0.70, D - 360,
           "40mm lap seam: 12x M6 bolts + silicone (leak path)", fs=6.4, color=C_OUT)
    axs.text(0, D + 150, "CURRENT — 304 SS: 2 panels + a bolted/siliconed center lap seam",
             fontsize=8.5, color=C_OUT, fontweight="bold", va="bottom")
    axs.set_xlim(-160, W + 60); axs.set_ylim(-40, D + 240)
    axs.set_aspect("equal"); axs.axis("off")

    ax_tb = fig.add_axes([0.04, 0.005, 0.92, 0.05])
    title_block(ax_tb, f"SHEET 2 OF {TOTAL_SHEETS}",
                drawing_title="PROCESSING TRAY — PP SHEET LAYOUT / SEAM (EVALUATED OPTION)",
                subtitle="research record — welded-PP layout vs the retained SS lap seam", doc_id="TBS-RES-TRAY")
    ax_tb.set_axis_off()
    out = os.path.join(DIAGRAMS_DIR, "tray-redesign-sheet2.png")
    fig.savefig(out, dpi=DIAGRAM_DPI); plt.close(fig)
    print(f"  {out} saved")


if __name__ == "__main__":
    sheet1()
    sheet2()
