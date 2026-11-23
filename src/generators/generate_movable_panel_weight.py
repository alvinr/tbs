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
deducts the Ø800 housing aperture from the center skins, so its sandwich figure is
lower than the whole-panel _panel_weight() there.

Run:
    python3 src/generators/generate_movable_panel_weight.py                 # console breakdown
    python3 src/generators/generate_movable_panel_weight.py --inject        # fill hinged-panel-report §2.4
    python3 src/generators/generate_movable_panel_weight.py --check-blocks
"""
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import tbs_constants as k

# ── Material densities (kg/m³) — same set as generate_weight_analysis.py ──
RHO_STEEL = 7850      # mild / Corten steel
RHO_ALUM  = 2700      # 5052 aluminum
RHO_PLY   = 600       # exterior plywood
RHO_HDPE  = 950       # HDPE — ALL light-lock plastic (housing 3/16", drum/skins/bay 1/8"; 2026-07-22)
RHO_EPDM  = 140       # closed-cell EPDM/neoprene compression foam (typ.)

# 2×2×0.120in steel SHS (#26: was 50×50×3 nominal): 50.8² − 44.7² = 582 mm² → 4.57 kg/m
RHS_KG_PER_M = (50.8**2 - 44.7**2) * 1e-6 * RHO_STEEL
# Bottom axle beam: 50×40×3 RHS (LT_BBEAM_H deep)
BBEAM_KG_PER_M = (k.LT_AXLE_BEAM_W * k.LT_BBEAM_H
                  - (k.LT_AXLE_BEAM_W - 2 * k.LT_AXLE_BEAM_T) * (k.LT_BBEAM_H - 2 * k.LT_AXLE_BEAM_T)) * 1e-6 * RHO_STEEL
G = 9.81
PIVOT_MOMENT_DESIGN_KNM = 3.6     # Ø89×8 CHS post sized at SF 3.7 for this moment (report §5.5)
THRUST_DESIGN_KG = 330
M12_PROOF_KN = 84.3 * 600 / 1000  # tensile stress area × 8.8 proof stress            # 51118 thrust-bearing design load (report §5.5)

_REPORT = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "hinged-panel-report.md")

H = k.C_HGT / 1000.0          # panel height 2.388 m (matches whole-camera model)


def _rows():
    """Return [(group, item, detail, kg), ...] for the movable assembly."""
    rows = []
    panel_mid = (0.0, (k.PANEL_CUT_YD + k.PIVOT_YD) / 2)
    drum_c = (float(k.DRUM_CX), float(k.DRUM_CY))
    cage_c = ((k.DRUM_CAGE_X0 + k.DRUM_CAGE_X1) / 2, (k.DRUM_CAGE_YD_L + k.DRUM_CAGE_YD_R) / 2)
    def add(g, item, detail, kg, at=panel_mid): rows.append((g, item, detail, kg, at))

    # Swing-zone widths (Yd, m), split by the stepped-profile zones
    w_near = (k.PANEL_CORNER_YD_L - k.PANEL_CUT_YD) / 1000.0   # 180→653
    w_ctr  = k.PANEL_CENTER_W / 1000.0                          # 653→1709
    w_far  = (k.PIVOT_YD - k.PANEL_CORNER_YD_R) / 1000.0        # 1709→2287
    aperture = math.pi * (k.LT_HOUSING_R / 1000.0) ** 2         # Ø800 opening

    # ── A. Stepped framed panel (swing zone only) — rev11: 1/8" HDPE skins + Fan ply band ──
    ts = k.PANEL_SKIN_T / 1000.0                                # 0.00318 m HDPE skin
    band = (k.PANEL_FAN_BAND_Z - k.PANEL_FLOOR_GAP) / 1000.0    # ply band height ≈ 0.995 m
    add("A Skins + frame", "Fan ply band (18mm)", f"Fan B corner, {w_near:.3f}m × {band:.2f}m, 2 faces",
        2 * (w_near * band) * 0.018 * RHO_PLY, (0.0, (k.PANEL_CUT_YD + k.PANEL_CORNER_YD_L) / 2))
    add("A Skins + frame", "HDPE corner skins (1/8\")", f"near above band + far, 2 faces",
        2 * (w_near * (H - band) + w_far * H) * ts * RHO_HDPE)
    # Corner-zone stiffener grid (weight audit 2026-07-29): 1"×1"×1/8" 6061 Al angle rib
    # grid (per corner 1 vertical + 2 horizontal) replaces the former solid 3mm Al core.
    angle_kg_per_m = (25.4 * 3.175 + (25.4 - 3.175) * 3.175) * 1e-6 * RHO_ALUM
    rib_len = (H + 2 * w_near) + (H + 2 * w_far)
    add("A Skins + frame", "Corner Al stiffener grid", f"1×1×1/8 6061 angle, {rib_len:.2f}m",
        rib_len * angle_kg_per_m)
    frame_len = 2 * (w_ctr + H) + 4 * w_ctr
    add("A Skins + frame", "Center RHS frame", f"2×2×0.120in SHS, {frame_len:.1f}m total",
        frame_len * RHS_KG_PER_M, (0.0, float(k.DRUM_CY)))
    add("A Skins + frame", "HDPE center skins (1/8\")", f"2×1/8\" HDPE, Ø{k.DRUM_D} aperture deducted",
        2 * (w_ctr * H - aperture) * ts * RHO_HDPE, (0.0, float(k.DRUM_CY)))

    # ── B. Fixed Ø800 housing (bolts into panel, swings with it) ──
    open_frac = k.LT_OPENING_DEG / 360.0
    Hd = (k.DRUM_H_LT - k.PANEL_FLOOR_GAP) / 1000.0            # suspended height ≈ 2.12 m
    house_circ = math.pi * (2 * k.LT_HOUSING_R / 1000.0)
    add("B Housing", "HDPE housing shell", f"Ø{k.DRUM_D}×3/16\", two {k.LT_OPENING_DEG}° openings",
        house_circ * (1 - 2 * open_frac) * Hd * (k.LT_HOUSING_T / 1000.0) * RHO_HDPE, drum_c)
    add("B Housing", "Steel flange/hub inserts", "bolt inserts, isolation", 6.0, drum_c)

    # ── C. Rotating drum ──
    drum_circ = math.pi * (2 * k.LT_DRUM_OR / 1000.0)
    td = k.LT_DRUM_T / 1000.0
    cap_area = math.pi * (k.LT_CAP_OD / 2 / 1000.0) ** 2      # FULL metal disc
    add("C Drum", "HDPE C-shell", f"Ø{2 * k.LT_DRUM_OR}×1/8\", one {k.LT_OPENING_DEG}° opening",
        drum_circ * (1 - open_frac) * Hd * td * RHO_HDPE, drum_c)
    add("C Drum", "Al end caps (2)", f"Ø{k.LT_CAP_OD}×{k.LT_CAP_TOP_T:.0f}mm 6061-T6 (bolted hubs)",
        cap_area * ((k.LT_CAP_TOP_T + k.LT_CAP_BOT_T) / 1000.0) * RHO_ALUM, drum_c)
    rim_area = (k.LT_RIM_LEG * k.LT_RIM_T + (k.LT_RIM_LEG - k.LT_RIM_T) * k.LT_RIM_T) * 1e-6
    add("C Drum", "Rim-angle arcs (2)",
        f"{k.LT_RIM_LEG}×{k.LT_RIM_LEG}×{k.LT_RIM_T} rolled R{k.LT_CAP_OD / 2:.0f}, 6061-T6 Al, {k.LT_SHELL_ARC}° arc",
        2 * (k.LT_SHELL_ARC / 360) * math.pi * (k.LT_CAP_OD / 1000.0) * rim_area * RHO_ALUM, drum_c)
    add("C Drum", "Steel stub shafts (2)", f"Ø75×{k.LT_STUB_SHAFT_L}",
        2 * math.pi * (0.0375 ** 2) * (k.LT_STUB_SHAFT_L / 1000.0) * RHO_STEEL, drum_c)
    add("C Drum", "SKF 6215 bearings (2)", "sealed deep-groove", 2 * 1.3, drum_c)
    add("C Drum", "HDPE edge stiffeners (2)", "~0.30 kg/m", 2 * Hd * 0.30, drum_c)
    add("C Drum", "Grab rail + misc", "interior pull rail, fasteners", 4.0, drum_c)

    # ── D. B2 punch-out bay (1/8" HDPE 4-wall tube + front face) ──
    bay_depth = (k.BAY_BACK_X - k.BAY_FRONT_X) / 1000.0
    bay_w = (k.DRUM_CAGE_YD_R - k.DRUM_CAGE_YD_L) / 1000.0
    bay_area = (2 * bay_depth * Hd + 2 * bay_depth * bay_w
                + max(bay_w * Hd - aperture, 0))
    add("D Bay", "Punch-out bay walls", f"1/8\" HDPE, {bay_area:.2f}m² ({bay_depth:.2f}m deep)",
        bay_area * ts * RHO_HDPE, cage_c)

    # ── E. Drum support cage — welded 2×2×0.120 RHS box: 4 posts + 8 perimeter rails + 2 axle beams ──
    cage_depth = (k.DRUM_CAGE_X1 - k.DRUM_CAGE_X0) / 1000.0
    cage_post = (k.LT_CAGE_TOP - k.LT_CAGE_BOT) / 1000.0
    rhs_len = 4 * cage_post + 4 * cage_depth + 4 * bay_w + bay_w
    add("E Cage", "Cage posts + rails + top axle beam", f"2×2×0.120in steel SHS, {rhs_len:.1f}m",
        rhs_len * RHS_KG_PER_M, cage_c)
    add("E Cage", "Bottom axle beam", f"{k.LT_AXLE_BEAM_W}×{k.LT_BBEAM_H}×{k.LT_AXLE_BEAM_T} RHS, {bay_w:.2f}m",
        bay_w * BBEAM_KG_PER_M, drum_c)
    plate = math.pi * (k.LT_BRG_PLATE_OD / 2000.0) ** 2 * (k.LT_BRG_PLATE_T / 1000.0) * RHO_STEEL
    add("E Cage", "Bearing mount plates (2)", f"Ø{k.LT_BRG_PLATE_OD}×{k.LT_BRG_PLATE_T} steel", 2 * plate, drum_c)

    # ── F. Seals on the moving leaf ──
    xsec = 0.020 * 0.020
    perim = 2 * H + 2 * (w_near + w_ctr + w_far)
    add("F Seals", "Perimeter EPDM gasket", f"20mm, {perim:.1f}m", perim * xsec * RHO_EPDM)
    add("F Seals", "Housing-surround EPDM ring", f"20mm, Ø{k.DRUM_D}", house_circ * xsec * RHO_EPDM)
    add("F Seals", "Drum wipers + felt/brush", "top/bottom + opening edges", 2.0)

    # ── G. Latches ──
    add("G Latches", "Cam latches (2)", "~0.5 kg each", 2 * 0.5)

    # ── H. Pivot interface (rotates with the leaf, on the axis) ──
    on_axis = (float(k.PIVOT_X), float(k.PIVOT_YD))
    add("H Pivot (rotating)", "Thrust + journal bearings", "carry leaf at pivot", 8.0, on_axis)
    add("H Pivot (rotating)", "Pivot collar / hub", "clamps to leaf", 5.0, on_axis)
    return rows


def _material_of(item):
    s = item.lower()
    if "ply" in s: return "Plywood"               # fan ply band only
    if "al core" in s or "aluminum" in s or "al stiffener" in s: return "Aluminum"
    if "hdpe" in s or "bay" in s: return "HDPE"   # all light-lock plastic is HDPE (skins, drum, bay)
    if "epdm" in s or "wiper" in s: return "EPDM/other"
    return "Steel"


LOCKS = [("Top + bottom wall stays", 6.0), ("Drop-in rail saddles (4)", 4.0)]


def summary(rows):
    """Totals, by-material split and the swing moment the movable mass puts on the pivot post."""
    total = sum(r[3] for r in rows)
    mats = {}
    for _, item, _, kg, _ in rows:
        mats[_material_of(item)] = mats.get(_material_of(item), 0.0) + kg
    mx = sum(kg * (at[0] - k.PIVOT_X) for *_, kg, at in rows)
    my = sum(kg * (at[1] - k.PIVOT_YD) for *_, kg, at in rows)
    lever_mm = math.hypot(mx, my) / total
    moment_knm = total * G * lever_mm / 1e6
    # Post held at floor AND roof (fixed-fixed, the stiffer case for the floor end): the hub's two
    # bushings put an opposing force pair F = M / bushing spacing on it; superpose the end reactions.
    L = k.C_HGT - k.FLOOR_PLATE_T
    zb = [z + 55 / 2 - k.FLOOR_PLATE_T for z in k.PIVOT_BUSH_Z]          # 55mm bushing width
    F = moment_knm * 1e6 / (zb[1] - zb[0])                              # N
    base_m = base_v = 0.0
    for P, a in ((F, zb[0]), (-F, zb[1])):
        b = L - a
        base_m += P * a * b * b / L ** 2
        base_v += P * b * b * (3 * a + b) / L ** 3
    bolt_t = abs(base_m) / (2 * k.PIVOT_PLATE_BOLT_DY) / 2                # 2 bolts per row, weak axis
    return dict(total=total, locks=sum(v for _, v in LOCKS), mats=mats,
                lever_mm=lever_mm, moment_knm=moment_knm, bush_f_kn=F / 1e3,
                base_m_knm=abs(base_m) / 1e6, base_v_kn=abs(base_v) / 1e3, bolt_t_kn=bolt_t / 1e3)


def table_md():
    rows = _rows()
    sm = summary(rows)
    groups = {}
    for g, item, detail, kg, _ in rows:
        groups.setdefault(g, []).append((item, detail, kg))
    out = ["| Group | Component | Construction | kg |", "|-------|-----------|-------------|---:|"]
    for g in sorted(groups):
        letter, name = g.split(" ", 1)
        items = groups[g]
        for i, (item, detail, kg) in enumerate(items):
            label = f"**{letter} · {name}**" if i == 0 else ""
            out.append(f"| {label} | {item} | {detail} | {kg:.1f} |")
        if len(items) > 1:
            out.append(f"| | **{letter} subtotal** | | **{sum(r[2] for r in items):.1f}** |")
    out.append(f"| | **MOVABLE TOTAL (carried-rotating)** | | **≈{sm['total']:.0f}** |")
    out.append(f"| | *+ transport-only locks (stays + 4 saddles)* | engaged only when swung | +{sm['locks']:.0f} |")
    t = sm["total"]
    mat_txt = ", ".join(f"{m if m.split('/')[0].isupper() else m.lower()} {kg:.0f} kg ({kg / t * 100:.0f}%)"
                        for m, kg in sorted(sm["mats"].items(), key=lambda x: -x[1]))
    out += ["", f"**By material:** {mat_txt}.", "",
            f"**Pivot loads.** The movable mass sits {sm['lever_mm'] / 1000:.2f}m from the swing axis "
            f"(mass-weighted plan centroid), so it puts **{sm['moment_knm']:.1f} kN·m** on the pivot post "
            f"against the {PIVOT_MOMENT_DESIGN_KNM} kN·m the post is sized for, and "
            f"**{t:.0f} kg** on the thrust bearing against its {THRUST_DESIGN_KG} kg design load (§5.5). "
            f"The hub reacts that moment through its two bushings as a {sm['bush_f_kn']:.1f} kN force pair. "
            f"With the post held at floor and roof, the floor end sees {sm['base_v_kn']:.1f} kN shear and "
            f"{sm['base_m_knm']:.2f} kN·m, which loads each floor-plate M12 to {sm['bolt_t_kn']:.1f} kN "
            f"(M12 Gr.8.8 proof load {M12_PROOF_KN:.1f} kN)."]
    return "\n".join(out)


_BLOCKS = {"movable:table": table_md}


def _block_pat(key):
    return re.compile(r"(<!-- BEGIN " + re.escape(key) + r" -->)(.*?)(<!-- END " + re.escape(key) + r" -->)", re.DOTALL)


def inject_blocks(write=True):
    if not os.path.exists(_REPORT):
        return [("movable:*", "NO-REPORT")]
    text = open(_REPORT, encoding="utf-8").read()
    new, results = text, []
    for key, fn in _BLOCKS.items():
        body = "\n" + fn() + "\n"
        pat = _block_pat(key)
        found = False
        for m in pat.finditer(text):
            found = True
            results.append((key, "ok" if m.group(2) == body else "STALE"))
        if not found:
            results.append((key, "MISSING"))
        new = pat.sub(lambda m, body=body: m.group(1) + body + m.group(3), new)
    if write and new != text:
        open(_REPORT, "w", encoding="utf-8").write(new)
    return results


def main():
    rows = _rows()
    groups = {}
    for g, item, detail, kg, _ in rows:
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

    sm = summary(rows)
    print("\n  Transport-only lock hardware (engaged only when swung):")
    for item, kg in LOCKS:
        print(f"      {kg:7.2f} kg   {item}")
    print(f"  MOVABLE + transport locks:                   {grand + sm['locks']:6.1f} kg")
    print(f"\n  Swing moment on pivot post: {sm['moment_knm']:.2f} kN·m at {sm['lever_mm']:.0f} mm "
          f"(design {PIVOT_MOMENT_DESIGN_KNM} kN·m)")

    print("\n  By material (movable assembly):")
    for m, kg in sorted(sm["mats"].items(), key=lambda x: -x[1]):
        print(f"      {kg:7.1f} kg ({kg/grand*100:4.1f}%)   {m}")
    print("=" * 74)


if __name__ == "__main__":
    if "--inject" in sys.argv:
        for key, st in inject_blocks(True):
            print(f"  {key}: {st}")
    elif "--check-blocks" in sys.argv:
        bad = [f"{k_}: {st}" for k_, st in inject_blocks(write=False) if st != "ok"]
        if bad:
            print("✗ movable-panel weight block out of sync (run: generate_movable_panel_weight.py --inject):")
            for b in bad:
                print("   " + b)
            sys.exit(1)
        print("✓ movable-panel weight block in sync")
    else:
        main()
