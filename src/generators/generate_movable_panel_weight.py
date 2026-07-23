#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""First-principles weight breakdown of the MOVABLE (swinging) part of the
cargo-door hinged panel — TBS-001 rev 10.

The panel + light-trap drum SWING ~56° about the vertical Ø89 pivot post for
transport. "Movable" here means everything that rotates about that pivot. The two
FIXED strips (Yd 0–PANEL_CUT_YD and PIVOT_YD–C_WID) and the FIXED pivot post are
EXCLUDED; transport-only lock hardware (wall stays, rail saddles) is reported
separately because it is engaged only when the leaf is swung in.

This is the companion analysis to generate_weight_analysis.py (which carries the
whole-camera inventory). The two reconcile: this file isolates the swing zone and
deducts the Ø900 housing aperture from the center skins, so its sandwich figure is
lower than the whole-panel _panel_weight() there.

Run:
    python3 src/generators/generate_movable_panel_weight.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import tbs_constants as k

# ── Material densities (kg/m³) — same set as generate_weight_analysis.py ──
RHO_STEEL = 7850      # mild / Corten steel
RHO_ALUM  = 2700      # 5052 aluminum
RHO_PLY   = 600       # marine plywood
RHO_HDPE  = 950       # HDPE — ALL light-lock plastic (housing 3/16", drum/skins/bay 1/8"; 2026-07-22)
RHO_EPDM  = 140       # closed-cell EPDM/neoprene compression foam (typ.)

# 50×50×3 SHS section: 50² − 44² = 564 mm² → 4.43 kg/m (first-principles; EN table 4.35)
RHS_KG_PER_M = (50**2 - 44**2) * 1e-6 * RHO_STEEL

H = k.C_HGT / 1000.0          # panel height 2.388 m (matches whole-camera model)


def _rows():
    """Return [(group, item, detail, kg), ...] for the movable assembly."""
    rows = []
    def add(g, item, detail, kg): rows.append((g, item, detail, kg))

    # Swing-zone widths (Yd, m), split by the stepped-profile zones
    w_near = (k.PANEL_CORNER_YD_L - k.PANEL_CUT_YD) / 1000.0   # 180→653
    w_ctr  = k.PANEL_CENTER_W / 1000.0                          # 653→1709
    w_far  = (k.PIVOT_YD - k.PANEL_CORNER_YD_R) / 1000.0        # 1709→2287
    aperture = math.pi * (k.LT_HOUSING_R / 1000.0) ** 2         # Ø900 opening

    # ── A. Stepped framed panel (swing zone only) — rev11: 1/8" HDPE skins + Fan ply band ──
    ts = k.PANEL_SKIN_T / 1000.0                                # 0.00318 m HDPE skin
    band = (k.PANEL_FAN_BAND_Z - k.PANEL_FLOOR_GAP) / 1000.0    # ply band height ≈ 0.995 m
    add("A Sandwich", "Fan ply band (18mm)", f"Fan B corner, {w_near:.3f}m × {band:.2f}m, 2 faces",
        2 * (w_near * band) * 0.018 * RHO_PLY)
    add("A Sandwich", "HDPE corner skins (1/8\")", f"near above band + far, 2 faces",
        2 * (w_near * (H - band) + w_far * H) * ts * RHO_HDPE)
    add("A Sandwich", "Corner Al core plates", f"3mm 5052, {w_near+w_far:.3f}m × {H:.2f}m",
        (w_near + w_far) * H * 0.003 * RHO_ALUM)
    frame_len = 2 * (w_ctr + H) + 4 * w_ctr
    add("A Sandwich", "Center RHS frame", f"50×50×3 SHS, {frame_len:.1f}m total",
        frame_len * RHS_KG_PER_M)
    add("A Sandwich", "HDPE center skins (1/8\")", "2×1/8\" HDPE, Ø900 aperture deducted",
        2 * (w_ctr * H - aperture) * ts * RHO_HDPE)

    # ── B. Fixed Ø900 housing (bolts into panel, swings with it) ──
    open_frac = k.LT_OPENING_DEG / 360.0
    Hd = (k.DRUM_H_LT - k.PANEL_FLOOR_GAP) / 1000.0            # suspended height ≈ 2.12 m
    house_circ = math.pi * (2 * k.LT_HOUSING_R / 1000.0)
    add("B Housing", "HDPE housing shell", f"Ø900×3/16\", two {k.LT_OPENING_DEG}° openings",
        house_circ * (1 - 2 * open_frac) * Hd * (k.LT_HOUSING_T / 1000.0) * RHO_HDPE)
    add("B Housing", "Steel flange/hub + bearing mounts", "bolt inserts, isolation", 6.0)

    # ── C. Rotating drum ──
    drum_circ = math.pi * (2 * k.LT_DRUM_OR / 1000.0)
    td = k.LT_DRUM_T / 1000.0
    cap_area = math.pi * (k.LT_DRUM_OR / 1000.0) ** 2 * (1 - open_frac)
    add("C Drum", "HDPE C-shell", f"Ø864×1/8\", one {k.LT_OPENING_DEG}° opening",
        drum_circ * (1 - open_frac) * Hd * td * RHO_HDPE)
    add("C Drum", "HDPE end caps (2)", "C-shaped, 1/8\"", 2 * cap_area * td * RHO_HDPE)
    add("C Drum", "Steel stub shafts (2)", "Ø75×150",
        2 * math.pi * (0.0375 ** 2) * 0.150 * RHO_STEEL)
    add("C Drum", "SKF 6215 bearings (2)", "sealed deep-groove", 2 * 1.3)
    add("C Drum", "HDPE edge stiffeners (2)", "~0.30 kg/m", 2 * Hd * 0.30)
    add("C Drum", "Grab rail + misc", "interior pull rail, fasteners", 4.0)

    # ── D. B2 punch-out bay (1/8" HDPE 4-wall tube + front face) ──
    bay_depth = (k.BAY_BACK_X - k.BAY_FRONT_X) / 1000.0
    bay_w = (k.DRUM_CAGE_YD_R - k.DRUM_CAGE_YD_L) / 1000.0
    bay_area = (2 * bay_depth * Hd + 2 * bay_depth * bay_w
                + max(bay_w * Hd - aperture, 0))
    add("D Bay", "Punch-out bay walls", f"1/8\" HDPE, {bay_area:.2f}m² ({bay_depth:.2f}m deep)",
        bay_area * ts * RHO_HDPE)

    # ── E. Drum support cage (light steel box frame) ──
    cage_depth = (k.DRUM_CAGE_X1 - k.DRUM_CAGE_X0) / 1000.0
    cage_edges = 4 * Hd + 4 * cage_depth + 4 * bay_w
    add("E Cage", "Drum support cage frame", f"~25×25×3 angle, {cage_edges:.1f}m box",
        cage_edges * 1.0)

    # ── F. Seals on the moving leaf ──
    xsec = 0.020 * 0.020
    perim = 2 * H + 2 * (w_near + w_ctr + w_far)
    add("F Seals", "Perimeter EPDM gasket", f"20mm, {perim:.1f}m", perim * xsec * RHO_EPDM)
    add("F Seals", "Housing-surround EPDM ring", "20mm, Ø900", house_circ * xsec * RHO_EPDM)
    add("F Seals", "Drum wipers + felt/brush", "top/bottom + opening edges", 2.0)

    # ── G. Latches ──
    add("G Latches", "Cam latches (4)", "~0.5 kg each", 4 * 0.5)

    # ── H. Pivot interface (rotates with the leaf) ──
    add("H Pivot (rotating)", "Thrust + journal bearings", "carry leaf at pivot", 8.0)
    add("H Pivot (rotating)", "Pivot collar / hub", "clamps to leaf", 5.0)
    return rows


def _material_of(item):
    s = item.lower()
    if "ply" in s: return "Plywood"               # fan ply band only
    if "al core" in s or "aluminum" in s: return "Aluminum"
    if "hdpe" in s or "bay" in s: return "HDPE"   # all light-lock plastic is HDPE (skins, drum, bay)
    if "epdm" in s or "wiper" in s: return "EPDM/other"
    return "Steel"


def main():
    rows = _rows()
    groups = {}
    for g, item, detail, kg in rows:
        groups.setdefault(g, []).append((item, detail, kg))

    print("=" * 74)
    print("  MOVABLE (SWINGING) PANEL ASSEMBLY — first-principles weight breakdown")
    print(f"  Swing zone Yd {k.PANEL_CUT_YD}-{k.PIVOT_YD} mm  |  "
          f"{k.SWING_LOCK_DEG} deg swing about Ø{k.PIVOT_POST_OD} pivot")
    print("=" * 74)
    grand = 0.0
    for g in sorted(groups):
        sub = sum(r[2] for r in groups[g])
        grand += sub
        print(f"\n  {g}   —   subtotal {sub:6.1f} kg")
        for item, detail, kg in groups[g]:
            print(f"      {kg:7.2f} kg   {item:32s} {detail}")
    print("\n" + "-" * 74)
    print(f"  MOVABLE ASSEMBLY TOTAL (carried-rotating):   {grand:6.1f} kg")

    locks = [("Top + bottom wall stays", 6.0), ("Drop-in rail saddles (4)", 4.0)]
    print("\n  Transport-only lock hardware (engaged only when swung):")
    for item, kg in locks:
        print(f"      {kg:7.2f} kg   {item}")
    print(f"  MOVABLE + transport locks:                   {grand + sum(v for _, v in locks):6.1f} kg")

    mats = {}
    for g, item, detail, kg in rows:
        mats[_material_of(item)] = mats.get(_material_of(item), 0.0) + kg
    print("\n  By material (movable assembly):")
    for m, kg in sorted(mats.items(), key=lambda x: -x[1]):
        print(f"      {kg:7.1f} kg ({kg/grand*100:4.1f}%)   {m}")
    print("=" * 74)


if __name__ == "__main__":
    main()
