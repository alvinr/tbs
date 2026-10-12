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
from matplotlib.patches import Rectangle, Circle

import tbs_constants as k
import generate_ibc_frame_drawing as ibc
from tbs_title_block import title_block
from tbs_drawing import leader, hatch_rect

FONT = {"fontfamily": "monospace"}
C_OUT, C_DIM, C_CL, C_STEEL = k.C_OUT, k.C_DIM, k.C_CL, k.C_STEEL
C_IBC, C_WK, C_PIV = "#1F6FB2", "#C8541E", "#2E8B4A"   # system colors
C_MEMBER = "#9AA7B0"
C_PLATE = "#7C8B99"
C_PLY = "#D9C39A"

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

    # ── LEFT: section detail of the stack (vertical exaggeration) ──────────────
    ax = fig.add_axes([0.05, 0.40, 0.46, 0.50]); ax.axis("off")
    ax.set_xlim(0, 300); ax.set_ylim(-40, 140); ax.set_aspect("auto")

    def sx(v): return v           # horizontal mm 1:1
    def sy(v): return v           # vertical mm 1:1 (layers are thin but legible here)

    base_y = 40
    # steel cross-member (C-section stub, in section) under the plywood
    mx = 150
    hatch_rect(ax, sx(mx-45), sy(base_y), sx(90), sy(4), color=C_STEEL)      # top flange
    ax.add_patch(Rectangle((sx(mx-45), sy(base_y)), sx(90), sy(4), fill=False, edgecolor=C_OUT, lw=1.2))
    ax.add_patch(Rectangle((sx(mx-45), sy(base_y-56)), sx(6), sy(56), facecolor=C_STEEL, edgecolor=C_OUT, lw=1.0))  # web down
    ax.text(sx(mx), sy(base_y-28), "STEEL\nCROSS-MEMBER\n~4mm C-section", ha="center", va="center", fontsize=6, color=C_DIM, **FONT)

    # plywood deck (full width)
    ax.add_patch(Rectangle((sx(10), sy(base_y+4)), sx(280), sy(28), facecolor=C_PLY, edgecolor=C_OUT, lw=1.0, zorder=2))
    ax.text(sx(265), sy(base_y+18), "28mm PLY", ha="right", va="center", fontsize=6, color="#6B5A33", **FONT)

    # sub-plate (on top of ply, full width)
    plate_y = base_y + 32
    hatch_rect(ax, sx(10), sy(plate_y), sx(280), sy(8), color=C_PLATE)
    ax.add_patch(Rectangle((sx(10), sy(plate_y)), sx(280), sy(8), fill=False, edgecolor=C_OUT, lw=1.4, zorder=3))
    ax.text(sx(20), sy(plate_y+4), "SUB-PLATE ~8mm STEEL", ha="left", va="center", fontsize=6.5, color=C_OUT, **FONT)

    # winged TEK through plate + ply into the member flange (J1a)
    tek_x = mx
    ax.plot([sx(tek_x), sx(tek_x)], [sy(plate_y+8), sy(base_y)], color="#8A1A1A", lw=2.6, zorder=5)
    ax.add_patch(Circle((sx(tek_x), sy(plate_y+8)), sx(5), facecolor="#8A1A1A", edgecolor="white", lw=0.5, zorder=6))
    leader(ax, sx(tek_x), sy(base_y+2), sx(tek_x-70), sy(base_y-20),
           "J1a / WF4a  winged #14x3.25\" TEK\n(self-taps the member; wings ream the ply)",
           fs=6, color="#8A1A1A", font=FONT, ha="center")

    # foot base-plate on the sub-plate, bolted into a tapped boss (J1b)
    foot_x = 235
    ax.add_patch(Rectangle((sx(foot_x-40), sy(plate_y+8)), sx(80), sy(12), facecolor=C_STEEL, edgecolor=C_OUT, lw=1.2, zorder=4))
    ax.text(sx(foot_x), sy(plate_y+14), "FOOT", ha="center", va="center", fontsize=6, color=C_DIM, **FONT)
    # tapped boss below the plate
    ax.add_patch(Rectangle((sx(foot_x-8), sy(plate_y-14)), sx(16), sy(14), facecolor=C_PLATE, edgecolor=C_OUT, lw=1.0, zorder=4))
    ax.plot([sx(foot_x), sx(foot_x)], [sy(plate_y+20), sy(plate_y-12)], color=C_OUT, lw=2.2, zorder=5)
    ax.add_patch(Rectangle((sx(foot_x-7), sy(plate_y+20)), sx(14), sy(4), facecolor=C_OUT, zorder=6))   # bolt head
    leader(ax, sx(foot_x), sy(plate_y-12), sx(foot_x+5), sy(plate_y-34),
           "J1b / WF4b  M12x30 into a\nTAPPED BOSS (drive from above,\nno underside access)",
           fs=6, color=C_OUT, font=FONT, ha="left")

    ax.text(sx(150), sy(128), "SECTION — anchor stack (vertical scale exaggerated)",
            ha="center", fontsize=7.5, fontweight="bold", color=C_OUT, **FONT)

    # ── RIGHT TOP: schematic plate footprints over the two clusters ────────────
    axp = fig.add_axes([0.55, 0.52, 0.42, 0.38])
    plot_region(axp, -120, 5240, "", holes_on=False)
    axp.set_xlim(-160, k.C_LEN + 160)
    # IBC single plate over the 4 feet
    ibc_fx = [f[0] for f in ibc_feet()]; ibc_fy = [f[1] for f in ibc_feet()]
    px0, px1 = min(ibc_fx)-110, max(ibc_fx)+110
    py0, py1 = min(ibc_fy)-110, max(ibc_fy)+110
    axp.add_patch(Rectangle((px0, py0), px1-px0, py1-py0, facecolor=C_PLATE, alpha=0.32,
                            edgecolor=C_IBC, lw=1.8, ls=(0, (6, 3)), zorder=3))
    # walkway continuous plate under the 5-leg line (door-sill to first members)
    axp.add_patch(Rectangle((-20, min(k.LEFT_WK_CANT_LEG_YDS)-110), 360,
                            max(k.LEFT_WK_CANT_LEG_YDS)-min(k.LEFT_WK_CANT_LEG_YDS)+220,
                            facecolor=C_PLATE, alpha=0.32, edgecolor=C_WK, lw=1.8, ls=(0, (6, 3)), zorder=3))
    axp.text((px0+px1)/2, py1+120, "IBC: ONE plate, 4 feet", ha="center", fontsize=6.5, color=C_IBC, **FONT)
    axp.text(170, max(k.LEFT_WK_CANT_LEG_YDS)+170, "WALKWAY: ONE continuous\nplate, 5 legs + door sill",
             ha="center", fontsize=6.5, color=C_WK, **FONT)
    axp.text(k.C_LEN*0.5, k.C_WID+200, "PLAN — sub-plate footprints (dashed) over the nominal grid",
             ha="center", fontsize=7.5, fontweight="bold", color=C_OUT, **FONT)

    # ── RIGHT BOTTOM: the BIG container-dependent note ─────────────────────────
    nb = fig.add_axes([0.55, 0.14, 0.42, 0.33]); nb.axis("off")
    nb.add_patch(Rectangle((0.0, 0.0), 1.0, 1.0, facecolor="#FFF3E0", edgecolor="#C8541E",
                           lw=2.0, transform=nb.transAxes))
    nb.text(0.5, 0.92, "!!  PLATE DIMENSIONS ARE CONTAINER-DEPENDENT  !!",
            ha="center", va="top", fontsize=8.5, fontweight="bold", color="#9A3B10",
            transform=nb.transAxes, **FONT)
    nb.text(0.04, 0.78,
            "Container floor cross-members are NOT standardized:\n"
            "  - ISO 1496-1 only caps them <=1000mm apart\n"
            "  - CIMC: C-section SPA-H Corten, ~4-4.5mm, ~45mm\n"
            "    top flange, ~122mm high, but PITCH + STATIONS\n"
            "    vary by maker; forklift pockets interrupt them.\n\n"
            "ON THE ACQUIRED CONTAINER, finalize:\n"
            "  1. plate length / width (span 3+ members; a\n"
            "     >=1000mm plate ALWAYS crosses >=1 member)\n"
            "  2. TEK clearance-hole positions (drill to the\n"
            "     SURVEYED member flanges + the door sill)\n"
            "  3. TEK count (2-3 per member crossed)\n\n"
            "The feet/legs + tapped-boss pattern do NOT change\n"
            "- only the plate adapts to the box.",
            ha="left", va="top", fontsize=6.6, color="#5A3A20", transform=nb.transAxes, **FONT)

    tb = fig.add_axes([0.0, 0.0, 1.0, 1.0]); tb.axis("off")
    title_block(tb, "SHEET 2 OF 2",
                drawing_title="FLOOR-ANCHOR SUB-PLATE STANDARD",
                subtitle="SECTION STACK + PLATE FOOTPRINTS + CONTAINER-DEPENDENT NOTE",
                scale_note="NTS — representative", doc_id="TBS-240 · Floor Anchoring")


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
