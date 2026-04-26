#!/usr/bin/env python3
"""
generate_logos.py — Three logo concepts for the Giant Pinhole Camera project.

  logo-option1.png  —  Scientific blueprint
  logo-option2.png  —  60s IBM / Research Division
  logo-option3.png  —  Haring / Bauhaus / Kodak
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Ellipse, Wedge, Arc
from matplotlib.path import Path
import matplotlib.patheffects as pe
import matplotlib.transforms as transforms

# ── Shared helpers ────────────────────────────────────────────────────────────

def save(fig, fname, dpi=150):
    fig.savefig(fname, dpi=dpi, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  → {fname}")

def outlined_text(ax, x, y, txt, fs, color, outline, **kw):
    t = ax.text(x, y, txt, fontsize=fs, color=color, **kw)
    t.set_path_effects([
        pe.withStroke(linewidth=3.5, foreground=outline)
    ])
    return t

# ═══════════════════════════════════════════════════════════════════════════════
# OPTION 1 — SCIENTIFIC BLUEPRINT
# ═══════════════════════════════════════════════════════════════════════════════

def make_logo1():
    NAVY   = "#0A1628"
    WHITE  = "#E8EEF4"
    CYAN   = "#4FC3F7"
    AMBER  = "#FFB300"
    GRID   = "#1A2E45"

    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor(NAVY)
    ax.set_facecolor(NAVY)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Subtle grid ──
    for x in range(0, 101, 5):
        ax.axvline(x, color=GRID, lw=0.4, alpha=0.6)
    for y in range(0, 101, 5):
        ax.axhline(y, color=GRID, lw=0.4, alpha=0.6)

    # ── Container cross-section ──
    CAM_X, CAM_Y, CAM_W, CAM_H = 22, 32, 56, 28
    ax.add_patch(Rectangle((CAM_X, CAM_Y), CAM_W, CAM_H,
                            fc="none", ec=WHITE, lw=1.8, zorder=3))
    # Internal surface hatching (image plane — right wall)
    for i in range(8):
        yy = CAM_Y + i * (CAM_H / 7)
        ax.plot([CAM_X + CAM_W, CAM_X + CAM_W + 2],
                [yy, yy - 2], color=WHITE, lw=0.8, alpha=0.5, zorder=3)

    # ── Pinhole ──
    PH_X = CAM_X
    PH_Y = CAM_Y + CAM_H / 2
    ph = Circle((PH_X, PH_Y), 0.9, fc=CYAN, ec=WHITE, lw=1.2, zorder=6)
    ax.add_patch(ph)
    ax.text(PH_X - 1.5, PH_Y + 3, "Ø 2.17 mm", color=CYAN, fontsize=6,
            ha="right", va="bottom", fontfamily="monospace", zorder=7)
    # Leader line
    ax.plot([PH_X - 1.5, PH_X - 0.5], [PH_Y + 2.5, PH_Y + 0.5],
            color=CYAN, lw=0.8, zorder=5)

    # ── Subject — stick figure (left of camera) ──
    SX = 10
    # Body
    ax.plot([SX, SX], [PH_Y - 7, PH_Y - 2], color=WHITE, lw=1.8, zorder=4)
    # Head
    head = Circle((SX, PH_Y - 0.5), 1.7, fc="none", ec=WHITE, lw=1.5, zorder=4)
    ax.add_patch(head)
    # Arms
    ax.plot([SX - 3, SX + 3], [PH_Y - 4, PH_Y - 4], color=WHITE, lw=1.5, zorder=4)
    # Legs
    ax.plot([SX, SX - 2.5], [PH_Y - 7, PH_Y - 10.5], color=WHITE, lw=1.5, zorder=4)
    ax.plot([SX, SX + 2.5], [PH_Y - 7, PH_Y - 10.5], color=WHITE, lw=1.5, zorder=4)

    # ── Subject label ──
    ax.text(SX, PH_Y - 13.5, "SUBJECT", color=WHITE, fontsize=5.5, ha="center",
            fontfamily="monospace", alpha=0.8)
    ax.plot([SX, SX], [PH_Y - 12.5, PH_Y - 11.5], color=WHITE, lw=0.8, alpha=0.5)
    ax.text(SX, PH_Y + 4, "3,440 mm", color=WHITE, fontsize=5.5, ha="center",
            fontfamily="monospace", alpha=0.6)

    # ── Light rays: subject → pinhole ──
    ray_origins = [(SX - 3, PH_Y + 6), (SX, PH_Y + 2), (SX + 3, PH_Y - 8)]
    for rx, ry in ray_origins:
        ax.annotate("", xy=(PH_X, PH_Y), xytext=(rx, ry),
                    arrowprops=dict(arrowstyle="-|>", color=AMBER,
                                   lw=0.9, mutation_scale=8, alpha=0.7),
                    zorder=5)

    # ── Light rays: pinhole → image plane (inverted) ──
    img_targets = [(CAM_X + CAM_W, PH_Y - 6.5),
                   (CAM_X + CAM_W, PH_Y),
                   (CAM_X + CAM_W, PH_Y + 8)]
    for ix, iy in img_targets:
        ax.annotate("", xy=(ix, iy), xytext=(PH_X, PH_Y),
                    arrowprops=dict(arrowstyle="-|>", color=AMBER,
                                   lw=0.9, mutation_scale=8, alpha=0.7),
                    zorder=5)

    # ── Inverted image on back wall ──
    IX = CAM_X + CAM_W + 1.5
    IY = PH_Y
    # Inverted stick figure (smaller)
    ax.plot([IX, IX], [IY + 1.5, IY + 5], color=CYAN, lw=1.2, alpha=0.75, zorder=4)
    head2 = Circle((IX, IY + 6.2), 1.2, fc="none", ec=CYAN, lw=1.2, alpha=0.75, zorder=4)
    ax.add_patch(head2)
    ax.plot([IX - 2, IX + 2], [IY + 3, IY + 3], color=CYAN, lw=1.0, alpha=0.75, zorder=4)
    ax.plot([IX, IX - 1.5], [IY + 1.5, IY - 1.5], color=CYAN, lw=1.0, alpha=0.75, zorder=4)
    ax.plot([IX, IX + 1.5], [IY + 1.5, IY - 1.5], color=CYAN, lw=1.0, alpha=0.75, zorder=4)
    ax.text(IX + 0.5, IY - 4, "IMAGE\n(INVERTED)", color=CYAN, fontsize=5,
            ha="left", fontfamily="monospace", alpha=0.8)

    # ── Focal length dimension ──
    FL_Y = CAM_Y - 4
    ax.annotate("", xy=(CAM_X + CAM_W, FL_Y), xytext=(CAM_X, FL_Y),
                arrowprops=dict(arrowstyle="<->", color=WHITE, lw=0.9,
                                mutation_scale=8))
    ax.text(CAM_X + CAM_W / 2, FL_Y - 2, "f = 2,362 mm", color=WHITE,
            ha="center", fontsize=6, fontfamily="monospace")

    # ── Rayleigh formula box ──
    ax.add_patch(FancyBboxPatch((18, 7), 64, 12,
                                boxstyle="round,pad=0.5",
                                fc="#0D1F35", ec=CYAN, lw=1.2, zorder=4))
    ax.text(50, 16.5, r"$d = 1.9\sqrt{f \cdot \lambda}$",
            color=AMBER, fontsize=14, ha="center", va="center",
            fontfamily="monospace", zorder=5)
    ax.text(50, 10.5,
            r"$d = 2.17\,\mathrm{mm}$   $f\!/\!1088$   $\lambda = 550\,\mathrm{nm}$",
            color=WHITE, fontsize=8.5, ha="center", va="center",
            fontfamily="monospace", zorder=5)

    # ── f-number badge ──
    ax.add_patch(Circle((85, 84), 8.5, fc=CYAN, ec=WHITE, lw=1.4, zorder=4))
    ax.text(85, 85.5, "f/", color=NAVY, fontsize=10, ha="center", va="center",
            fontweight="bold", fontfamily="monospace", zorder=5)
    ax.text(85, 81.5, "1088", color=NAVY, fontsize=9, ha="center", va="center",
            fontweight="bold", fontfamily="monospace", zorder=5)

    # ── Title ──
    ax.text(50, 96.5, "GIANT  PINHOLE  CAMERA",
            color=WHITE, fontsize=13, ha="center", va="center",
            fontweight="bold", fontfamily="monospace", zorder=5)
    ax.text(50, 93, "OPTICAL DESIGN SPECIFICATION — OPTION B",
            color=CYAN, fontsize=6.5, ha="center", va="center",
            fontfamily="monospace", alpha=0.85, zorder=5)

    # ── Corner registration marks ──
    for cx, cy in [(3, 3), (97, 3), (3, 97), (97, 97)]:
        for dx, dy in [(0, 3), (3, 0)]:
            ax.plot([cx, cx + dx * (1 if cx < 50 else -1)],
                    [cy, cy + dy * (1 if cy < 50 else -1)],
                    color=WHITE, lw=1, alpha=0.4)

    save(fig, "assets/logo-option1.png")


# ═══════════════════════════════════════════════════════════════════════════════
# OPTION 2 — 60s IBM / RESEARCH DIVISION
# ═══════════════════════════════════════════════════════════════════════════════

def make_logo2():
    IBM_BLUE  = "#006496"
    IBM_MID   = "#1F70C1"
    IBM_RED   = "#C8102E"
    WHITE     = "#FFFFFF"
    CREAM     = "#F5F0E8"
    GREY      = "#D4D4D4"
    DARK      = "#1A1A2E"

    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor(IBM_BLUE)
    ax.set_facecolor(IBM_BLUE)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Halftone-style dot grid background ──
    for gx in np.arange(2, 100, 4):
        for gy in np.arange(2, 100, 4):
            r = 0.35 + 0.2 * np.sin(gx * 0.3) * np.cos(gy * 0.25)
            c = Circle((gx, gy), r, fc="#1A5276", ec="none", zorder=1)
            ax.add_patch(c)

    # ── Punch card holes along top ──
    for i, px in enumerate(np.linspace(8, 92, 18)):
        ax.add_patch(Rectangle((px - 1.2, 94), 2.4, 4,
                                fc=IBM_BLUE, ec=WHITE, lw=0.8,
                                joinstyle="round", zorder=4))

    # ── Main white card area ──
    ax.add_patch(FancyBboxPatch((6, 12), 88, 79,
                                boxstyle="round,pad=0.8",
                                fc=CREAM, ec=WHITE, lw=2.5, zorder=3))

    # ── IBM-style horizontal rule bars ──
    for y, col, h in [(88, IBM_BLUE, 2.5), (14.5, IBM_RED, 1.5)]:
        ax.add_patch(Rectangle((6, y), 88, h, fc=col, ec="none", zorder=4))

    # ── Title bar ──
    ax.text(50, 89.5, "GIANT  PINHOLE  CAMERA",
            color=WHITE, fontsize=12.5, ha="center", va="center",
            fontweight="bold", zorder=5)
    ax.text(50, 16.5, "CAMERA  RESEARCH  DIVISION  ·  FIELD  UNIT  No. 1",
            color=WHITE, fontsize=6.5, ha="center", va="center",
            fontfamily="monospace", zorder=5)

    # ── FIGURE A — Scientist with camera (left) ──
    # Lab coat figure
    FX = 27
    FY = 54

    # Body (lab coat — white rectangle)
    ax.add_patch(FancyBboxPatch((FX - 5.5, FY - 14), 11, 16,
                                boxstyle="round,pad=0.5",
                                fc=WHITE, ec=GREY, lw=1.5, zorder=5))
    # Lapels
    ax.plot([FX - 5.5, FX - 1], [FY + 2, FY - 4], color=GREY, lw=1.2, zorder=6)
    ax.plot([FX + 5.5, FX + 1], [FY + 2, FY - 4], color=GREY, lw=1.2, zorder=6)
    # Pocket protector
    ax.add_patch(Rectangle((FX - 4.5, FY - 8), 4, 4.5,
                            fc=IBM_BLUE, ec=DARK, lw=0.8, zorder=6))
    # Pens in protector
    for pi, px in enumerate([FX - 3.8, FX - 2.5, FX - 1.2]):
        ax.plot([px, px], [FY - 8, FY - 4.5], color=IBM_RED if pi == 0 else WHITE,
                lw=1.5, zorder=7)
    # Shirt & tie
    ax.add_patch(Rectangle((FX - 1.2, FY - 8), 2.4, 3.5,
                            fc=IBM_RED, ec="none", zorder=6))
    # Head
    ax.add_patch(Circle((FX, FY + 6), 5,
                         fc="#F5CBA7", ec=DARK, lw=1.5, zorder=6))
    # Glasses
    for gx in [FX - 2.5, FX + 0.8]:
        ax.add_patch(Circle((gx, FY + 6.5), 1.8, fc="none",
                             ec=DARK, lw=1.2, zorder=7))
    ax.plot([FX - 0.7, FX + 0.8], [FY + 6.5, FY + 6.5], color=DARK, lw=1, zorder=7)
    # Hair
    ax.add_patch(Arc((FX, FY + 7.5), 10, 5, theta1=0, theta2=180,
                     color=DARK, lw=3, zorder=7))
    # Arms
    ax.plot([FX - 5.5, FX - 9], [FY + 0, FY - 4], color=WHITE, lw=6, zorder=5,
            solid_capstyle="round")
    ax.plot([FX - 5.5, FX - 9], [FY + 0, FY - 4], color=GREY, lw=1.2, zorder=6,
            solid_capstyle="round")
    ax.plot([FX + 5.5, FX + 9], [FY + 0, FY - 3], color=WHITE, lw=6, zorder=5,
            solid_capstyle="round")
    ax.plot([FX + 5.5, FX + 9], [FY + 0, FY - 3], color=GREY, lw=1.2, zorder=6,
            solid_capstyle="round")
    # Legs / trousers
    for lx, la in [(FX - 3, -2), (FX + 3, 2)]:
        ax.add_patch(Rectangle((lx - 2, FY - 22), 4, 8,
                                fc="#2C3E50", ec=DARK, lw=1, zorder=5))
    # Shoes
    for sx in [FX - 3, FX + 3]:
        ax.add_patch(Ellipse((sx, FY - 22), 6, 2.5,
                              fc=DARK, ec=DARK, lw=0.8, zorder=6))
    # Label
    ax.text(FX, FY - 27, "OPERATOR\nFIELD UNIT A",
            color=IBM_BLUE, fontsize=6, ha="center", va="center",
            fontfamily="monospace", fontweight="bold")

    # ── CAMERA BODY (centre) ──
    CX, CY = 50, 52
    # Body
    ax.add_patch(FancyBboxPatch((CX - 9, CY - 7), 18, 14,
                                boxstyle="round,pad=0.8",
                                fc="#2C3E50", ec=DARK, lw=2, zorder=5))
    # Pinhole plate
    ax.add_patch(Circle((CX - 9, CY), 3.5, fc=IBM_BLUE, ec=WHITE, lw=1.5, zorder=6))
    ax.add_patch(Circle((CX - 9, CY), 0.6, fc=WHITE, ec=WHITE, lw=0.5, zorder=7))
    ax.text(CX - 9, CY - 5.5, "PINHOLE\nØ2.17mm",
            color=IBM_BLUE, fontsize=5, ha="center", fontfamily="monospace")
    # Lens plate
    ax.add_patch(Circle((CX + 9, CY), 3.5, fc="#1A5276", ec=WHITE, lw=1.5, zorder=6))
    ax.add_patch(Circle((CX + 9, CY), 2.2, fc="#4A90D9", ec=WHITE, lw=0.5, zorder=7))
    # f-number badge
    ax.add_patch(Circle((CX, CY + 3), 4, fc=IBM_RED, ec=WHITE, lw=1, zorder=7))
    ax.text(CX, CY + 3.4, "f/", color=WHITE, fontsize=6, ha="center",
            va="center", fontweight="bold", zorder=8)
    ax.text(CX, CY + 1.8, "1088", color=WHITE, fontsize=5.5, ha="center",
            va="center", fontweight="bold", fontfamily="monospace", zorder=8)
    # Tripod legs
    for tx, ty in [(CX - 6, CY - 14), (CX, CY - 15), (CX + 6, CY - 14)]:
        ax.plot([CX, tx], [CY - 7, ty], color=DARK, lw=2, zorder=4)

    # ── FIGURE B — Scientist with clipboard (right) ──
    GX = 73
    GY = FY

    # Lab coat
    ax.add_patch(FancyBboxPatch((GX - 5.5, GY - 14), 11, 16,
                                boxstyle="round,pad=0.5",
                                fc=WHITE, ec=GREY, lw=1.5, zorder=5))
    ax.plot([GX - 5.5, GX - 1], [GY + 2, GY - 4], color=GREY, lw=1.2, zorder=6)
    ax.plot([GX + 5.5, GX + 1], [GY + 2, GY - 4], color=GREY, lw=1.2, zorder=6)
    # Pocket protector
    ax.add_patch(Rectangle((GX + 1, GY - 8), 4, 4.5,
                            fc=IBM_BLUE, ec=DARK, lw=0.8, zorder=6))
    for pi, px in enumerate([GX + 1.7, GX + 3.0, GX + 4.3]):
        ax.plot([px, px], [GY - 8, GY - 4.5], color=IBM_RED if pi == 1 else WHITE,
                lw=1.5, zorder=7)
    # Head
    ax.add_patch(Circle((GX, GY + 6), 5, fc="#F5CBA7", ec=DARK, lw=1.5, zorder=6))
    # Glasses
    for gx in [GX - 2.5, GX + 0.8]:
        ax.add_patch(Circle((gx, GY + 6.5), 1.8, fc="none", ec=DARK, lw=1.2, zorder=7))
    ax.plot([GX - 0.7, GX + 0.8], [GY + 6.5, GY + 6.5], color=DARK, lw=1, zorder=7)
    ax.add_patch(Arc((GX, GY + 7.5), 10, 5, theta1=0, theta2=180,
                     color=DARK, lw=3, zorder=7))
    # Clipboard
    ax.add_patch(FancyBboxPatch((GX + 7, GY - 8), 7, 9,
                                boxstyle="round,pad=0.3",
                                fc=CREAM, ec=DARK, lw=1.2, zorder=6))
    ax.add_patch(Rectangle((GX + 9, GY + 1.5), 3, 1,
                            fc=IBM_BLUE, ec=DARK, lw=0.8, zorder=7))
    for ly in [GY - 1, GY - 3, GY - 5]:
        ax.plot([GX + 7.8, GX + 13.2], [ly, ly], color=DARK, lw=0.7, zorder=7)
    # Arm holding clipboard
    ax.plot([GX + 5.5, GX + 10], [GY + 0, GY - 2], color=WHITE, lw=6, zorder=5,
            solid_capstyle="round")
    ax.plot([GX + 5.5, GX + 10], [GY + 0, GY - 2], color=GREY, lw=1.2, zorder=6,
            solid_capstyle="round")
    ax.plot([GX - 5.5, GX - 8], [GY + 0, GY - 4], color=WHITE, lw=6, zorder=5,
            solid_capstyle="round")
    ax.plot([GX - 5.5, GX - 8], [GY + 0, GY - 4], color=GREY, lw=1.2, zorder=6)
    # Legs
    for lx in [GX - 3, GX + 3]:
        ax.add_patch(Rectangle((lx - 2, GY - 22), 4, 8,
                                fc="#2C3E50", ec=DARK, lw=1, zorder=5))
    for sx in [GX - 3, GX + 3]:
        ax.add_patch(Ellipse((sx, GY - 22), 6, 2.5,
                              fc=DARK, ec=DARK, lw=0.8, zorder=6))
    ax.text(GX, GY - 27, "OPERATOR\nFIELD UNIT B",
            color=IBM_BLUE, fontsize=6, ha="center", va="center",
            fontfamily="monospace", fontweight="bold")

    # ── Spec panel ──
    ax.add_patch(FancyBboxPatch((8, 19), 84, 7,
                                boxstyle="round,pad=0.4",
                                fc=IBM_BLUE, ec=IBM_MID, lw=1, zorder=5, alpha=0.15))
    specs = "f = 2,362 mm   ·   d = 2.17 mm   ·   f/1088   ·   λ = 550 nm   ·   IMAGE PLANE 5,893 × 2,388 mm"
    ax.text(50, 22.5, specs, color=IBM_BLUE, fontsize=6.2, ha="center", va="center",
            fontfamily="monospace", fontweight="bold", zorder=6)

    save(fig, "assets/logo-option2.png")


# ═══════════════════════════════════════════════════════════════════════════════
# OPTION 3 — HARING / BAUHAUS / KODAK
# ═══════════════════════════════════════════════════════════════════════════════

def make_logo3():
    KODAK_Y = "#FFD100"
    KODAK_R = "#E3001B"
    BAUHAUS_B = "#1B3B6F"
    BAUHAUS_R = "#D62828"
    BLACK  = "#0D0D0D"
    WHITE  = "#FFFFFF"

    OUTLINE = 3.5   # Haring stroke weight (in points)

    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor(KODAK_Y)
    ax.set_facecolor(KODAK_Y)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_aspect("equal")
    ax.axis("off")

    # ── Bauhaus outer frame ──
    for lw, col, inset in [(6, BLACK, 0), (3, KODAK_R, 2.5), (1.5, BLACK, 4.5)]:
        ax.add_patch(Rectangle((inset, inset), 100 - 2*inset, 100 - 2*inset,
                                fc="none", ec=col, lw=lw, zorder=2))

    # ── Kodak film sprocket holes — left and right strips ──
    for side_x in [5.5, 94.5]:
        ax.add_patch(Rectangle((side_x - 2, 8), 4, 84, fc=KODAK_R, ec=BLACK,
                                lw=1.5, zorder=3))
        for hy in np.linspace(14, 86, 9):
            ax.add_patch(FancyBboxPatch((side_x - 1.2, hy - 1.8), 2.4, 3.6,
                                        boxstyle="round,pad=0.3",
                                        fc=KODAK_Y, ec=BLACK, lw=0.8, zorder=4))

    # ── Bauhaus geometric composition: background shapes ──
    # Large blue circle (top right)
    ax.add_patch(Circle((72, 72), 22, fc=BAUHAUS_B, ec=BLACK, lw=OUTLINE, zorder=3))
    # Red triangle (bottom left area)
    tri = plt.Polygon([(18, 12), (42, 12), (30, 35)],
                      fc=BAUHAUS_R, ec=BLACK, lw=OUTLINE, zorder=3)
    ax.add_patch(tri)
    # Small yellow square
    ax.add_patch(Rectangle((62, 18), 14, 14, fc=KODAK_Y, ec=BLACK, lw=OUTLINE, zorder=4))

    # ── HARING-STYLE MAIN FIGURE ──
    # A dynamic figure with camera — thick black outlines, solid fills
    # Standing, arms raised, "holding" the camera/light

    def haring_person(ax, cx, cy, scale=1.0,
                      body_col=WHITE, head_col=WHITE):
        lw = OUTLINE * scale * 1.1
        # Head
        ax.add_patch(Circle((cx, cy + 14*scale), 5*scale,
                             fc=head_col, ec=BLACK, lw=lw, zorder=6))
        # Body
        ax.add_patch(Ellipse((cx, cy + 2*scale), 10*scale, 16*scale,
                              fc=body_col, ec=BLACK, lw=lw, zorder=6))
        # Left arm — raised up
        arm_pts_L = np.array([
            [cx - 5*scale, cy + 7*scale],
            [cx - 12*scale, cy + 15*scale],
            [cx - 16*scale, cy + 20*scale],
        ])
        ax.plot(arm_pts_L[:, 0], arm_pts_L[:, 1], color=BLACK, lw=lw*1.8,
                solid_capstyle="round", solid_joinstyle="round", zorder=5)
        ax.plot(arm_pts_L[:, 0], arm_pts_L[:, 1], color=body_col, lw=lw*1.2,
                solid_capstyle="round", solid_joinstyle="round", zorder=6)
        # Right arm — extended
        arm_pts_R = np.array([
            [cx + 5*scale, cy + 7*scale],
            [cx + 14*scale, cy + 14*scale],
            [cx + 20*scale, cy + 12*scale],
        ])
        ax.plot(arm_pts_R[:, 0], arm_pts_R[:, 1], color=BLACK, lw=lw*1.8,
                solid_capstyle="round", solid_joinstyle="round", zorder=5)
        ax.plot(arm_pts_R[:, 0], arm_pts_R[:, 1], color=body_col, lw=lw*1.2,
                solid_capstyle="round", solid_joinstyle="round", zorder=6)
        # Legs — striding
        leg_L = np.array([
            [cx, cy - 6*scale],
            [cx - 6*scale, cy - 16*scale],
            [cx - 4*scale, cy - 22*scale],
        ])
        leg_R = np.array([
            [cx, cy - 6*scale],
            [cx + 6*scale, cy - 14*scale],
            [cx + 8*scale, cy - 22*scale],
        ])
        for pts in [leg_L, leg_R]:
            ax.plot(pts[:, 0], pts[:, 1], color=BLACK, lw=lw*1.8,
                    solid_capstyle="round", zorder=5)
            ax.plot(pts[:, 0], pts[:, 1], color=body_col, lw=lw*1.2,
                    solid_capstyle="round", zorder=6)

    # Main figure — centred, KODAK red body
    haring_person(ax, 42, 45, scale=1.1, body_col=BAUHAUS_R, head_col=BAUHAUS_R)

    # ── HARING-STYLE CAMERA at right arm endpoint ──
    # Camera body
    ax.add_patch(FancyBboxPatch((58, 52), 16, 12,
                                boxstyle="round,pad=1.2",
                                fc=BLACK, ec=BLACK, lw=OUTLINE, zorder=7))
    # Lens/pinhole aperture circle (Haring radiant style)
    ax.add_patch(Circle((58, 58), 4.5, fc=KODAK_Y, ec=BLACK, lw=OUTLINE, zorder=8))
    ax.add_patch(Circle((58, 58), 1.5, fc=BLACK, ec=BLACK, lw=1, zorder=9))

    # ── Haring radiant marks from pinhole (light/energy) ──
    angles = np.linspace(160, 340, 9)
    for ang in angles:
        rad = np.radians(ang)
        x0 = 58 + 5.8 * np.cos(rad)
        y0 = 58 + 5.8 * np.sin(rad)
        x1 = 58 + 11  * np.cos(rad)
        y1 = 58 + 11  * np.sin(rad)
        ax.plot([x0, x1], [y0, y1], color=BLACK, lw=2.5,
                solid_capstyle="round", zorder=7)

    # ── Second small Haring figure (in camera frame — the subject) ──
    haring_person(ax, 80, 65, scale=0.45, body_col=BAUHAUS_B, head_col=BAUHAUS_B)

    # ── Radiant marks from raised hand of main figure ──
    hand_x, hand_y = 26, 65
    for ang in np.linspace(60, 200, 7):
        rad = np.radians(ang)
        ax.plot([hand_x + 3*np.cos(rad), hand_x + 7*np.cos(rad)],
                [hand_y + 3*np.sin(rad), hand_y + 7*np.sin(rad)],
                color=BLACK, lw=2.2, solid_capstyle="round", zorder=6)

    # ── TITLE — Bauhaus bold geometric type ──
    # Top banner (black strip)
    ax.add_patch(Rectangle((12, 90), 76, 7.5, fc=BLACK, ec="none", zorder=5))
    ax.text(50, 93.8, "GIANT PINHOLE CAMERA",
            color=KODAK_Y, fontsize=12, ha="center", va="center",
            fontweight="bold", zorder=6)

    # Bottom: GPC monogram + spec
    ax.add_patch(FancyBboxPatch((12, 10), 15, 10,
                                boxstyle="round,pad=0.5",
                                fc=BLACK, ec=KODAK_R, lw=2, zorder=5))
    ax.text(19.5, 15, "GPC", color=KODAK_Y, fontsize=14, ha="center", va="center",
            fontweight="bold", zorder=6)

    ax.text(32, 15, "f/1088  ·  2.17mm  ·  140 sq ft",
            color=BLACK, fontsize=7.5, ha="left", va="center",
            fontweight="bold", fontfamily="monospace", zorder=6)

    save(fig, "assets/logo-option3.png")


# ── Run all ───────────────────────────────────────────────────────────────────
print("Generating logo options...")
make_logo1()
make_logo2()
make_logo3()
print("Done.")
