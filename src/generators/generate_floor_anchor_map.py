# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""Floor-anchor map + sub-plate (strongback) standard.

The container floor cross-members are NOT standardized (ISO 1496-1 only caps
them ≤1000mm apart; CIMC ~300mm, but pitch + stations vary by maker), so the
floor-secured feet/legs cannot be bolted straight to a member — a member can't
be guaranteed under each fixed bolt position.

Sheet 1 — the problem: a NOMINAL cross-member grid in plan with every floor-
anchored foot (IBC frame ×4, left-walkway floor-legs ×5, pivot post ×1) overlaid
to scale, showing the current bolt positions fall in the gaps.

Sheet 2 — the standard: a self-tapped SUB-PLATE (strongback) spanning several
members, with the feet/legs bolting UP into tapped bosses on the plate. Plate
dimensions + TEK count are container-dependent (finalized on the acquired box).
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon

import tbs_constants as k
import generate_ibc_frame_drawing as ibc
from tbs_title_block import title_block
from tbs_drawing import leader, hatch_rect, draw_notes, draw_dim_h

FONT = {"fontfamily": "monospace"}
C_OUT, C_DIM, C_CL, C_STEEL = k.C_OUT, k.C_DIM, k.C_CL, k.C_STEEL
C_IBC, C_WK, C_PIV = "#1F6FB2", "#C8541E", "#2E8B4A"   # system colors
C_MEMBER = "#9AA7B0"
C_PLATE = "#7C8B99"
C_PLY = "#D9C39A"
C_BOLT = "#3A3A42"     # bolt/TEK heads + shanks (house convention)

PITCH = 305.0           # ~12 in NOMINAL (representative — varies by maker)
BAND = 50.0             # screwable top-flange band width shown (~45mm CIMC)
MEMBERS = [round(i * PITCH) for i in range(int(k.C_LEN / PITCH) + 1)]

g, rhs = ibc.FRAME_X0_GLOBAL, ibc.FRAME_RHS
FP, PCD = k.IBC_FOOT_PLATE, k.IBC_FOOT_BOLT_PCD


def ibc_feet():
    out = []
    for fx, dx in ((ibc.FX_FRONT, k.IBC_FRONT_FOOT_DX), (ibc.FX_BACK, 0)):
        cx = g + fx + rhs / 2 + dx
        for yd in (ibc.POST_NEAR_YD, ibc.POST_FAR_YD):
            cy = yd + rhs / 2
            holes = [(cx + sx, cy + sy) for sx in (-PCD/2, PCD/2) for sy in (-PCD/2, PCD/2)]
            out.append((cx, cy, FP, FP, holes))
    return out


def wk_feet():
    fx0, fl, fw = k.LEFT_WK_CANT_FOOT_X0, k.LEFT_WK_CANT_FOOT[0], k.LEFT_WK_CANT_FOOT[1]
    out = []
    for yd in k.LEFT_WK_CANT_LEG_YDS:
        cx, cy = fx0 + fl / 2, yd
        holes = [(fx0 + dx, yd + sy) for dx in k.LEFT_WK_CANT_FOOT_BOLT_DX
                 for sy in (-k.LEFT_WK_CANT_FOOT_BOLT_DY, k.LEFT_WK_CANT_FOOT_BOLT_DY)]
        out.append((cx, cy, fl, fw, holes))
    return out


def pivot_feet():
    import math
    cx, cy, pcd = k.PIVOT_X, k.PIVOT_YD, 170.0
    holes = [(cx + pcd/2 * math.cos(math.radians(a)), cy + pcd/2 * math.sin(math.radians(a)))
             for a in range(0, 360, 60)]
    return [(cx, cy, 220, 220, holes, True)]


ALL = [ibc_feet(), wk_feet(), pivot_feet()]


def draw_grid(ax, x0, x1):
    for i, mx in enumerate(MEMBERS):
        if mx < x0 - BAND or mx > x1 + BAND:
            continue
        end = (i == 0 or mx >= MEMBERS[-1] - 1)
        ax.add_patch(Rectangle((mx - BAND/2, 0), BAND, k.C_WID, facecolor=C_MEMBER,
                               edgecolor="none", alpha=0.55 if end else 0.33, zorder=1))
        ax.plot([mx, mx], [0, k.C_WID], color=C_MEMBER, lw=0.6, ls=(0, (2, 3)), zorder=1)


def draw_foot(ax, f, holes_on=True, hole_r=9):
    cx, cy, w, h, holes = f[0], f[1], f[2], f[3], f[4]
    rnd = len(f) > 5 and f[5]
    col = C_PIV if rnd else (C_IBC if cx > 3000 else C_WK)
    if rnd:
        ax.add_patch(Circle((cx, cy), w/2, facecolor=col, alpha=0.22, edgecolor=col, lw=1.4, zorder=4))
    else:
        ax.add_patch(Rectangle((cx-w/2, cy-h/2), w, h, facecolor=col, alpha=0.22,
                               edgecolor=col, lw=1.4, zorder=4))
    if not holes_on:
        return
    for hx, hy in holes:
        on = any(abs(hx - mx) <= BAND/2 for mx in MEMBERS)
        ax.add_patch(Circle((hx, hy), hole_r, facecolor=("#1A7D32" if on else "#C21D1D"),
                            edgecolor="white", lw=0.6, zorder=6))


def plot_region(ax, x0, x1, title, holes_on=True, hole_r=9, plate=None):
    ax.set_xlim(x0, x1); ax.set_ylim(-120, k.C_WID + 120)
    ax.set_aspect("equal"); ax.axis("off")
    draw_grid(ax, x0, x1)
    ax.add_patch(Rectangle((max(x0, 0), 0), min(x1, k.C_LEN)-max(x0, 0), k.C_WID,
                           fill=False, edgecolor=C_OUT, lw=1.6, zorder=2))
    if plate:                                                 # (px0, py0, pw, ph, col)
        px0, py0, pw, ph, col = plate
        ax.add_patch(Rectangle((px0, py0), pw, ph, facecolor=C_PLATE, alpha=0.30,
                               edgecolor=col, lw=1.8, ls=(0, (6, 3)), zorder=3))
    for grp in ALL:
        for f in grp:
            if x0 - 200 <= f[0] <= x1 + 200:
                draw_foot(ax, f, holes_on=holes_on, hole_r=hole_r)
    if title:
        ax.text((x0+x1)/2, k.C_WID + 150, title, ha="center", va="bottom",
                fontsize=8, fontweight="bold", color=C_OUT, **FONT)


# ──────────────────────────────────────────────────────────────────────────────
def sheet1(fig):
    fig.suptitle("FLOOR-ANCHOR MAP — cross-member grid vs. floor-secured items (PLAN, looking down)",
                 fontsize=12, fontweight="bold", y=0.975, **FONT)
    ax_plan = fig.add_axes([0.04, 0.60, 0.92, 0.30])
    plot_region(ax_plan, -160, k.C_LEN + 160, "", holes_on=False)
    ax_plan.text(k.C_LEN*0.52, k.C_WID/2, "(no floor anchors in the central ~4.3 m)",
                 ha="center", va="center", fontsize=8.5, color="#888", style="italic", **FONT)
    ax_plan.text(0, k.C_WID + 190, "DOOR-END SILL", fontsize=6.5, color=C_DIM, ha="left", **FONT)
    ax_plan.text(k.C_LEN, k.C_WID + 190, "SEALED-END SILL", fontsize=6.5, color=C_DIM, ha="right", **FONT)
    ax_plan.text(k.C_LEN*0.5, -250,
                 f"X (container length, mm) ->   nominal ~{int(PITCH)}mm cross-member pitch, ~16-23 members typical",
                 ha="center", fontsize=7, color=C_DIM, **FONT)

    ax_near = fig.add_axes([0.04, 0.17, 0.44, 0.36])
    plot_region(ax_near, -120, 520, "DOOR-END CLUSTER  (walkway floor-legs x5 + pivot post)")
    ax_seal = fig.add_axes([0.52, 0.17, 0.44, 0.36])
    plot_region(ax_seal, 4480, 5240, "SEALED-END CLUSTER  (IBC frame feet x4, corridor)")

    leader(ax_near, 170, k.LEFT_WK_CANT_LEG_YDS[0], 360, k.LEFT_WK_CANT_LEG_YDS[0]-230,
           "walkway leg: 2 anchors only 40mm\napart (X130/170) - can't span a\n~255mm bay",
           fs=6, color=C_WK, font=FONT, ha="left")
    leader(ax_near, k.PIVOT_X, k.PIVOT_YD, 320, k.PIVOT_YD+40,
           "pivot O220, 6x M12 on O170 -\nby the door-end sill",
           fs=6, color=C_PIV, font=FONT, ha="left")
    leader(ax_seal, 4664, ibc.POST_NEAR_YD+rhs/2, 4760, 600,
           "IBC foot 150sq, 4x M12 @100 PCD -\nspans ~1/3 bay; only 1 bolt column\ncan reach a member",
           fs=6, color=C_IBC, font=FONT, ha="left")

    _legend(fig)
    _caveat(fig,
            "GRID IS REPRESENTATIVE - a 20ft container has ~16-23 cross-members at ~300mm, but exact stations + any forklift pockets "
            "VARY by maker (verify on the actual box). The green/red marks only show fall against this NOMINAL grid; the standard on "
            "Sheet 2 removes the dependency on them entirely.")


def _legend(fig):
    leg = fig.add_axes([0.04, 0.015, 0.92, 0.12]); leg.axis("off")
    leg.add_patch(Rectangle((0.005, 0.1), 0.02, 0.6, facecolor=C_MEMBER, alpha=0.5, transform=leg.transAxes))
    leg.text(0.03, 0.4, "nominal cross-member band", fontsize=7, va="center", transform=leg.transAxes, **FONT)
    leg.add_patch(Circle((0.30, 0.42), 0.008, facecolor="#1A7D32", transform=leg.transAxes))
    leg.text(0.315, 0.4, "anchor ON a member", fontsize=7, va="center", transform=leg.transAxes, **FONT)
    leg.add_patch(Circle((0.47, 0.42), 0.008, facecolor="#C21D1D", transform=leg.transAxes))
    leg.text(0.485, 0.4, "anchor in a GAP (vs nominal grid)", fontsize=7, va="center", transform=leg.transAxes, **FONT)
    for i, (c, t) in enumerate([(C_IBC, "IBC feet"), (C_WK, "walkway legs"), (C_PIV, "pivot")]):
        leg.add_patch(Rectangle((0.70+i*0.10, 0.33), 0.015, 0.18, facecolor=c, alpha=0.3, edgecolor=c, transform=leg.transAxes))
        leg.text(0.72+i*0.10, 0.4, t, fontsize=7, va="center", transform=leg.transAxes, **FONT)


def _caveat(fig, text):
    cav = fig.add_axes([0.04, -0.02, 0.92, 0.05]); cav.axis("off")
    cav.text(0.005, 0.5, text, fontsize=6.3, color=C_DIM, va="center",
             transform=cav.transAxes, wrap=True, **FONT)


# ──────────────────────────────────────────────────────────────────────────────
def sheet2(fig):
    fig.suptitle("FLOOR-ANCHOR SUB-PLATE (STRONGBACK) STANDARD — feet/legs bolt to a self-tapped plate",
                 fontsize=12, fontweight="bold", y=0.975, **FONT)

    # ── LEFT: section detail of the anchor stack (thickness exaggerated) ────────
    ax = fig.add_axes([0.04, 0.26, 0.56, 0.62]); ax.axis("off")
    ax.set_xlim(0, 310); ax.set_ylim(-40, 150); ax.set_aspect("auto")

    base_y, mx = 40, 150
    # steel cross-member (C-section stub, in section) under the plywood
    hatch_rect(ax, mx-45, base_y, 90, 4, color=C_STEEL)                                                  # top flange (~45mm)
    ax.add_patch(Rectangle((mx-45, base_y), 90, 4, fill=False, edgecolor=C_OUT, lw=1.2))
    ax.add_patch(Rectangle((mx-45, base_y-50), 6, 50, facecolor=C_STEEL, edgecolor=C_OUT, lw=1.0))        # web down
    ax.text(mx, base_y-28, "STEEL CROSS-MEMBER\n~4mm C-section (~45mm flange)", ha="center", va="center", fontsize=6, color=C_DIM, **FONT)
    # plywood deck + sub-plate on top
    ax.add_patch(Rectangle((10, base_y+4), 290, 28, facecolor=C_PLY, edgecolor=C_OUT, lw=1.0, zorder=2))  # 28mm ply
    ax.text(292, base_y+18, "28mm PLY", ha="right", va="center", fontsize=6, color="#6B5A33", **FONT)
    plate_y = base_y + 32
    hatch_rect(ax, 10, plate_y, 290, 8, color=C_PLATE)
    ax.add_patch(Rectangle((10, plate_y), 290, 8, fill=False, edgecolor=C_OUT, lw=1.4, zorder=3))
    ax.text(18, plate_y+4, "SUB-PLATE ~8mm STEEL", ha="left", va="center", fontsize=6.5, color=C_OUT, **FONT)

    # ── J1a winged TEK — drawn as a screw WITH its diameter (house convention) ──
    tek_x, dia = mx, 7.0                                    # #14 ~Ø6.3mm, drawn to scale
    head_z, tip_z = plate_y + 8, base_y - 8
    body_bot = tip_z + 9
    ax.add_patch(Rectangle((tek_x-11, head_z), 22, 5, fc=C_BOLT, ec=C_OUT, lw=0.8, zorder=8))             # hex-washer head
    ax.add_patch(Rectangle((tek_x-dia/2, body_bot), dia, head_z-body_bot, fc="#6E6E78", ec=C_OUT, lw=1.0, zorder=6))  # shank (shows diameter)
    for tz in range(int(body_bot)+2, int(head_z)-1, 4):                                                  # thread ticks
        ax.plot([tek_x-dia/2, tek_x+dia/2], [tz, tz-2.2], color=C_OUT, lw=0.5, zorder=7)
    for s in (-1, 1):                                                                                     # reaming wings (snap off at the steel)
        ax.plot([tek_x+s*dia/2, tek_x+s*(dia/2+8)], [base_y+16, base_y+22], color=C_BOLT, lw=1.2, zorder=6)
    ax.add_patch(Polygon([(tek_x-dia/2, body_bot), (tek_x+dia/2, body_bot), (tek_x, tip_z)], closed=True, fc="#6E6E78", ec=C_OUT, lw=1.0, zorder=6))  # drill point
    draw_dim_h(ax, tek_x-dia/2, tek_x+dia/2, head_z+13, "Ø6.3", offset=3, fs=5.5, above=True, font=FONT)  # the SCREW DIAMETER
    leader(ax, tek_x-dia/2-1, base_y+10, tek_x-78, base_y-24,
           "J1a / WF4a  winged #14×3.25\" TEK\n(self-taps the member; wings ream the ply)",
           fs=6, color=C_BOLT, font=FONT, ha="center")

    # ── J1b foot → sub-plate tapped boss ───────────────────────────────────────
    foot_x = 248
    ax.add_patch(Rectangle((foot_x-40, plate_y+8), 80, 12, facecolor=C_STEEL, edgecolor=C_OUT, lw=1.2, zorder=4))  # foot
    ax.text(foot_x, plate_y+14, "FOOT", ha="center", va="center", fontsize=6, color=C_DIM, **FONT)
    ax.add_patch(Rectangle((foot_x-9, plate_y-13), 18, 13, facecolor=C_PLATE, edgecolor=C_OUT, lw=1.0, zorder=4))  # tapped boss
    ax.add_patch(Rectangle((foot_x-3.5, plate_y-9), 7, 29, fc="#6E6E78", ec=C_OUT, lw=1.0, zorder=5))             # M12 shank (shows diameter)
    ax.add_patch(Rectangle((foot_x-8, plate_y+20), 16, 4, fc=C_BOLT, ec=C_OUT, lw=0.8, zorder=6))                # hex head
    leader(ax, foot_x, plate_y-11, foot_x-18, base_y-28,
           "J1b / WF4b  M12×30 into a TAPPED BOSS\n(drive from above, no underside access)",
           fs=6, color=C_OUT, font=FONT, ha="center")

    ax.text(155, 140, "SECTION — anchor stack (thickness exaggerated for clarity)",
            ha="center", fontsize=7.5, fontweight="bold", color=C_OUT, **FONT)

    # ── RIGHT: container-dependent notes (standard note block + title footer) ──
    axn = fig.add_axes([0.62, 0.13, 0.35, 0.75]); axn.axis("off")
    axn.set_xlim(0, 1); axn.set_ylim(0, 1)
    draw_notes(axn, [
        "PLATE DIMENSIONS ARE CONTAINER-DEPENDENT",
        "Container floor cross-members are NOT standardized:",
        "  - ISO 1496-1 only caps them ≤1,000mm apart",
        "  - CIMC: C-section SPA-H Corten ~4-4.5mm,",
        "    ~45mm flange, ~122mm high, but PITCH +",
        "    STATIONS vary by maker (forklift pockets",
        "    interrupt them).",
        "",
        "ON THE ACQUIRED CONTAINER, finalize:",
        "  1. plate length/width (span 3+ members; a",
        "     ≥1,000mm plate always crosses ≥1 member)",
        "  2. TEK clearance-hole positions (drill to the",
        "     surveyed member flanges + the door sill)",
        "  3. TEK count (2-3 per member crossed)",
        "",
        "The feet/legs + tapped-boss pattern do NOT",
        "change — only the plate adapts to the box.",
    ], 0.04, 0.96, 0.047, fs=6.6, title_fs=7.3, title_color="#9A3B10", font=FONT, width=0.92)

    tb = fig.add_axes([0.0, 0.0, 1.0, 1.0]); tb.axis("off")
    title_block(tb, "SHEET 2 OF 2",
                drawing_title="FLOOR-ANCHOR SUB-PLATE STANDARD",
                subtitle="ANCHOR-STACK SECTION + CONTAINER-DEPENDENT NOTES",
                scale_note="NTS", doc_id="TBS-240 · Floor Anchoring")


def main():
    for fname, fn in (("floor-anchor-map-sheet1.png", sheet1),
                      ("floor-anchor-map-sheet2.png", sheet2)):
        fig = plt.figure(figsize=(16, 11))
        fn(fig)
        out = os.path.join(k.DIAGRAMS_DIR, fname)
        fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
        plt.close(fig)
        print(f"saved {out}")


if __name__ == "__main__":
    main()
