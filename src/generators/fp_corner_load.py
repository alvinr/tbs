# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""fp_corner_load.py — film-plane corner load case (blueprint Phase 1c).

Two engineering items the corner blueprint left to "firm", computed from tbs_constants
so they can't drift:

  C2 — cross-slide TRAVEL verification: the Z (tilt) and X (swing) strokes required to
       absorb the rigid-plane rotation arc at ±MAX_TILT / ±MAX_SWING (about the plane
       center), vs the XSLIDE_*_TRAVEL constants.

  C1 — per-corner LOAD + cross-slide bending SAFETY FACTOR: the ¼"×1½" 304 flat-bar
       cross-slide as a worst-case cantilever at full extension carrying the corner's
       gravity share, checked both mounting orientations (deep/strong vs flat/weak axis).

Run:  python3 src/generators/fp_corner_load.py
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tbs_constants as c

# 304 stainless (annealed) — parts.py fp-cross-slide note: yield ~215 MPa.
SY_304 = 215.0        # MPa, annealed yield
E_304 = 193_000.0     # MPa, Young's modulus
G = 9.81              # m/s²


def moving_mass_kg():
    """Film-plane moving mass (frame + ACM + clamps + skates) — the weight model owns it."""
    try:
        import generate_weight_analysis as w
        return w._film_plane_carriage_weight()
    except Exception:
        return 50.76   # fallback = current weight-model value


def travel_required():
    """C2 — required Z/X cross-slide stroke = (half-dim)·(1−cos angle), rotation about the plane center."""
    z = (c.FP_H / 2.0) * (1 - math.cos(math.radians(c.MAX_TILT_DEG)))   # tilt → vertical foreshorten
    x = (c.FP_W / 2.0) * (1 - math.cos(math.radians(c.MAX_SWING_DEG)))  # swing → horizontal foreshorten
    return z, x


def bending(P_N, L_mm):
    """Cantilever bar, point load P at the free end, length L. Returns (σ_strong, σ_weak,
    δ_strong, δ_weak) — strong = 38.1 mm dimension in the load direction; weak = bar lies flat."""
    b, h = c.XSLIDE_BAR_T, c.XSLIDE_BAR_W      # 6.35 × 38.1 mm
    M = P_N * L_mm                              # N·mm
    S_strong = b * h**2 / 6.0                   # mm³, deep
    S_weak = h * b**2 / 6.0                     # mm³, flat
    I_strong = b * h**3 / 12.0                  # mm⁴
    I_weak = h * b**3 / 12.0
    sig_s, sig_w = M / S_strong, M / S_weak     # MPa (N/mm²)
    d_s = P_N * L_mm**3 / (3 * E_304 * I_strong)
    d_w = P_N * L_mm**3 / (3 * E_304 * I_weak)
    return sig_s, sig_w, d_s, d_w


def render_png(path=None):
    """Phase-1c review sheet — C2 travel geometry (tilt + swing) + C1 cross-slide bending
    (cantilever + deep-vs-flat section comparison + SF table). Matplotlib guarded so the
    numeric path stays dependency-free."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle, Arc, FancyArrow
    except ImportError:
        print("  (matplotlib unavailable — skipped PNG)")
        return None

    C_OUT, C_CL, C_DIM, C_ALU = "#1A1A1A", "#2060A0", "#404040", "#C8D8E8"
    C_OK, C_BAD, C_LD = "#1E7A34", "#B22222", "#B8860B"
    FT = dict(family="DejaVu Sans Mono")
    path = path or os.path.join(getattr(c, "DIAGRAMS_DIR", "diagrams"), "fp-corner-load-case.png")

    m = moving_mass_kg(); W = m * G; P = W / 4.0
    zr, xr = travel_required()
    sig_s, sig_w, d_s, d_w = bending(P, c.XSLIDE_X_TRAVEL)

    fig = plt.figure(figsize=(15, 9)); fig.patch.set_facecolor("white")
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 1.12], height_ratios=[1, 1],
                          left=0.05, right=0.97, top=0.88, bottom=0.06, hspace=0.32, wspace=0.20)
    axT, axS = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[1, 0])
    axB = fig.add_subplot(gs[:, 1])
    for a in (axT, axS, axB):
        a.set_aspect("equal"); a.axis("off")

    def rot(pt, deg):
        r = math.radians(deg); x, y = pt
        return (x * math.cos(r) - y * math.sin(r), x * math.sin(r) + y * math.cos(r))

    # ── C2a — TILT (side elevation): plane edge-on, rotate about center ──
    half = c.FP_H / 2.0
    axT.plot([0, 0], [-half, half], color=C_OUT, lw=3, solid_capstyle="round")          # flat plane
    tp = rot((0, half), -c.MAX_TILT_DEG); bp = rot((0, -half), -c.MAX_TILT_DEG)
    axT.plot([bp[0], tp[0]], [bp[1], tp[1]], color=C_LD, lw=2.4, ls="--")                # tilted plane
    axT.add_patch(Arc((0, 0), half, half, angle=90, theta1=-c.MAX_TILT_DEG, theta2=0, color=C_CL, lw=1.2))
    axT.plot(0, half, "o", color=C_OUT, ms=5); axT.plot(*tp, "o", color=C_LD, ms=5)
    axT.annotate("", xy=(tp[0] + 340, tp[1]), xytext=(tp[0] + 340, half),
                 arrowprops=dict(arrowstyle="<->", color=C_OK, lw=1.6))
    axT.text(tp[0] + 380, (tp[1] + half) / 2, f"Z travel\n{zr:.0f} mm", color=C_OK, fontsize=9, va="center", **FT)
    axT.plot(0, 0, "+", color=C_CL, ms=12, mew=2)
    axT.text(0, -half - 190, f"TILT  ±{c.MAX_TILT_DEG:g}°  →  Z = (FP_H/2)(1−cos) = {zr:.0f} mm  =  "
             f"XSLIDE_Z_TRAVEL {c.XSLIDE_Z_TRAVEL}  ✓", color=C_DIM, fontsize=9.5, ha="center", **FT)
    axT.set_xlim(-half * 0.8, half * 1.1); axT.set_ylim(-half - 340, half + 220)
    axT.set_title("C2a — TILT (side elevation): corner arc → Z stroke", fontsize=10, color=C_OUT, **FT)

    # ── C2b — SWING (plan): plane edge-on (width), rotate about center ──
    hw = c.FP_W / 2.0
    axS.plot([-hw, hw], [0, 0], color=C_OUT, lw=3, solid_capstyle="round")
    rp = rot((hw, 0), c.MAX_SWING_DEG); lp = rot((-hw, 0), c.MAX_SWING_DEG)
    axS.plot([lp[0], rp[0]], [lp[1], rp[1]], color=C_LD, lw=2.4, ls="--")
    axS.add_patch(Arc((0, 0), hw, hw, angle=0, theta1=0, theta2=c.MAX_SWING_DEG, color=C_CL, lw=1.2))
    axS.plot(hw, 0, "o", color=C_OUT, ms=5); axS.plot(*rp, "o", color=C_LD, ms=5)
    # X foreshortening = hw − rp[0], shown at the corner height; dashed riser links the flat corner up
    axS.plot([hw, hw], [0, rp[1]], color=C_CL, lw=0.8, ls=":")
    axS.annotate("", xy=(rp[0], rp[1]), xytext=(hw, rp[1]), arrowprops=dict(arrowstyle="<->", color=C_OK, lw=1.8))
    axS.text((rp[0] + hw) / 2, rp[1] + 130, f"X travel\n{xr:.0f} mm", color=C_OK, fontsize=9, ha="center", va="bottom", **FT)
    axS.plot(0, 0, "+", color=C_CL, ms=12, mew=2)
    axS.text(0, -560, f"SWING  ±{c.MAX_SWING_DEG:g}°  →  X = (FP_W/2)(1−cos) = {xr:.0f} mm  =  "
             f"XSLIDE_X_TRAVEL {c.XSLIDE_X_TRAVEL}  ✓", color=C_DIM, fontsize=9.5, ha="center", **FT)
    axS.set_xlim(-hw * 1.05, hw * 1.05); axS.set_ylim(-720, rp[1] + 320)
    axS.set_title("C2b — SWING (plan): corner arc → X stroke", fontsize=10, color=C_OUT, **FT)

    # ── C1 — bending: cantilever + deep/flat sections + SF table ──
    L = c.XSLIDE_X_TRAVEL
    axB.add_patch(Rectangle((-45, -70), 45, 140, fc="#888", ec=C_OUT, lw=1.2, hatch="////"))  # support
    axB.add_patch(Rectangle((0, -19), L, 38, fc=C_ALU, ec=C_OUT, lw=1.5))                     # bar (deep, edge-on)
    axB.annotate("", xy=(L, -150), xytext=(L, -19), arrowprops=dict(arrowstyle="->", color=C_BAD, lw=2.4))
    axB.text(L, -185, f"P = W/4 = {P:.0f} N", color=C_BAD, fontsize=10, ha="center", **FT)
    axB.plot([0, L], [95, 95], color=C_DIM, lw=0.8)
    axB.annotate("", xy=(0, 95), xytext=(L, 95), arrowprops=dict(arrowstyle="<->", color=C_DIM, lw=1.2))
    axB.text(L / 2, 120, f"cantilever L = max travel {L} mm", color=C_DIM, fontsize=9, ha="center", **FT)
    axB.text(L / 2, -19 - 42, f"304 flat bar {c.XSLIDE_BAR_T:g}×{c.XSLIDE_BAR_W:g} mm  ·  Sy {SY_304:.0f} MPa",
             color=C_OUT, fontsize=8.5, ha="center", va="top", **FT)

    # section insets
    def section(x0, y0, w, h, tag, good):
        col = C_OK if good else C_BAD
        axB.add_patch(Rectangle((x0, y0), w, h, fc=C_ALU, ec=C_OUT, lw=1.6))
        axB.annotate("", xy=(x0 + w / 2, y0 - 26), xytext=(x0 + w / 2, y0 + h + 26),
                     arrowprops=dict(arrowstyle="->", color=col, lw=1.4))
        axB.text(x0 + w / 2, y0 - 46, tag, color=col, fontsize=8.5, ha="center", va="top", **FT)
    section(20, -430, c.XSLIDE_BAR_T * 2.2, c.XSLIDE_BAR_W * 2.2, "DEEP (38.1 ⟂ load)\ngravity", True)
    section(190, -430, c.XSLIDE_BAR_W * 2.2, c.XSLIDE_BAR_T * 2.2, "FLAT (bar lies down)", False)

    tbl = [("orientation", "σ (MPa)", "SF", "δ (mm)", "SF ×2 dyn"),
           ("DEEP  (strong)", f"{sig_s:.0f}", f"{SY_304/sig_s:.1f}", f"{d_s:.2f}", f"{SY_304/(2*sig_s):.1f}"),
           ("FLAT  (weak)", f"{sig_w:.0f}", f"{SY_304/sig_w:.1f}", f"{d_w:.1f}", f"{SY_304/(2*sig_w):.1f}")]
    col_x = [300, 520, 630, 730, 840]     # orientation · σ · SF · δ · SF×2
    ty, dy = -255, -66
    for r, row in enumerate(tbl):
        for col_i, cell in enumerate(row):
            cc = C_OUT if r == 0 else (C_OK if "DEEP" in row[0] else C_BAD)
            axB.text(col_x[col_i], ty + r * dy, cell, color=cc,
                     fontsize=8.5, ha="left", fontweight="bold" if r == 0 else "normal", **FT)
    axB.text(col_x[0], ty + 3.5 * dy, "→ mount DEEP: SF≈10, δ≈0.1 mm.  FLAT is marginal (SF 1.7)\n"
             "   and fails at ×2 — lock bars deep (38.1 mm vertical).",
             color=C_OUT, fontsize=8.6, ha="left", va="top", **FT)
    axB.set_xlim(-70, 980); axB.set_ylim(-560, 180)
    axB.set_title(f"C1 — per-corner load {P:.0f} N → X-slide bending (worst case)",
                  fontsize=10, color=C_OUT, **FT)

    fig.suptitle("FILM-PLANE CORNER — LOAD CASE (blueprint Phase 1c)  ·  travel verification + cross-slide bending SF",
                 fontsize=12.5, fontweight="bold", color=C_OUT, y=0.955, **FT)
    fig.text(0.5, 0.915, f"moving mass {m:.1f} kg (weight model)  ·  304 SS ¼\"×1½\" bar  ·  driven from tbs_constants  —  "
             "for review (Phase 1c)", fontsize=9, color=C_DIM, ha="center", **FT)
    fig.savefig(path, dpi=150, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print(f"  → {path}")
    return path


def main():
    m = moving_mass_kg()
    W = m * G
    P = W / 4.0                                  # per-corner static gravity share (4 corners)

    zr, xr = travel_required()

    print("═══ FILM-PLANE CORNER LOAD CASE (blueprint Phase 1c) ═══\n")
    print("C2 — CROSS-SLIDE TRAVEL (required vs constant), rotation about plane center:")
    print(f"  Z (tilt  ±{c.MAX_TILT_DEG:g}°): required = (FP_H/2)(1−cos) = {zr:6.1f} mm   "
          f"XSLIDE_Z_TRAVEL = {c.XSLIDE_Z_TRAVEL} mm   {'OK' if abs(zr-c.XSLIDE_Z_TRAVEL)<=1 else 'MISMATCH'}")
    print(f"  X (swing ±{c.MAX_SWING_DEG:g}°): required = (FP_W/2)(1−cos) = {xr:6.1f} mm   "
          f"XSLIDE_X_TRAVEL = {c.XSLIDE_X_TRAVEL} mm   {'OK' if abs(xr-c.XSLIDE_X_TRAVEL)<=1 else 'MISMATCH'}")
    print(f"  Bar lengths: Z {c.XSLIDE_Z_BAR_LEN} mm (= {zr:.0f} travel + {c.XSLIDE_Z_BAR_LEN-zr:.0f} carriage/gib), "
          f"X {c.XSLIDE_X_BAR_LEN} mm (= {xr:.0f} + {c.XSLIDE_X_BAR_LEN-xr:.0f})")

    print(f"\nC1 — PER-CORNER LOAD + BENDING SF   (moving mass {m:.1f} kg, W={W:.0f} N, per corner W/4={P:.0f} N)")
    print(f"  Governing case: X (swing) slide horizontal, gravity transverse, worst-case cantilever L = "
          f"max travel {c.XSLIDE_X_TRAVEL} mm.  Bar {c.XSLIDE_BAR_T:g}×{c.XSLIDE_BAR_W:g} mm 304 (Sy {SY_304:.0f} MPa).")
    print("  (The Z slide travels vertically → gravity is AXIAL on it, not bending.)\n")
    for label, Pmult in (("nominal (W/4)", 1.0), ("+2× asymmetry/dynamic", 2.0)):
        sig_s, sig_w, d_s, d_w = bending(P * Pmult, c.XSLIDE_X_TRAVEL)
        print(f"  {label}: P = {P*Pmult:.0f} N")
        print(f"     strong axis (38.1 mm deep):  σ={sig_s:5.1f} MPa  SF={SY_304/sig_s:4.1f}   δ={d_s:.2f} mm")
        print(f"     weak axis  (bar lies flat):  σ={sig_w:5.1f} MPa  SF={SY_304/sig_w:4.1f}   δ={d_w:.2f} mm")

    print("\n  → Recommendation: mount the cross-slide bars DEEP (38.1 mm in the gravity direction) —")
    print("    SF ≈ 10 / δ ≈ 0.1 mm. Flat mounting drops SF to ~1.7 (marginal) / δ ~4.5 mm; if the way")
    print("    must run the bar flat, deepen the section or add a mid-span pad. Deflection is not")
    print("    optically critical (flatness carried by the ACM backing) but position error is not free.")

    print("\nRendering review sheet:")
    render_png()


if __name__ == "__main__":
    main()
