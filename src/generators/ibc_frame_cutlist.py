#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""ibc_frame_cutlist.py — IBC stacking-frame MEMBER CUT LIST (Phase D fab-detail package).

Computes every cut member of the deep-4-leg restraint frame from the geometry constants (the same
`generate_corridor_water_panel.frame()` / `tote_restraint()` math the 3D model uses), so the cut list
can't drift from the model. Emits a markdown table + a stock-ordering summary (linear feet per section,
so the shop can buy sticks). Run:

    python3 src/generators/ibc_frame_cutlist.py            # print the cut list + stock summary
    python3 src/generators/ibc_frame_cutlist.py --inject   # write it into ibc-stacking-report.md

Lengths are the fabrication CUT sizes (member-to-member butt lengths); add saw kerf per shop practice.
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "models"))
sys.path.insert(0, os.path.dirname(__file__))
import generate_corridor_water_panel as cp   # noqa: E402  (module constants: FRONT_X/BACK_X/YD_*/TOP_Z/PANEL_TOP_Z/EQT)
import generate_sketchup_model as ov          # noqa: E402  (IBC_FRAME_RHS/FOOT_PLATE/FOOT_PLATE_T/FRONT_BAR_D/C_WID)
import tbs_constants as k                      # noqa: E402  (IBC_FOOT_BOLT_D/PCD)

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPORT = os.path.join(_ROOT, "ibc-stacking-report.md")

MM_PER_FT = 304.8


def cut_list():
    """Return the cut members as rows: (item, section/plate, material, cut_size_mm, qty, note)."""
    S = ov.IBC_FRAME_RHS           # 50.8 — 2×2×0.120in SHS
    ft = ov.IBC_FOOT_PLATE_T       # 12 — foot-plate thickness
    fp = ov.IBC_FOOT_PLATE         # 150 — foot-plate side
    hp_t = 4                       # wall-hanger back-plate thickness
    bar_d = ov.IBC_FRONT_BAR_D     # 20 — front bar depth in X (bar section 50×20×3)

    upright_L = cp.TOP_Z - ft                                   # uprights sit on the plate, top at TOP_Z
    rail_yd_L = (cp.YD_FAR - S) - (cp.YD_NEAR + S)              # Yd ring rail (butts between uprights)
    rail_x_L = cp.BACK_X - (cp.FRONT_X + S)                    # X ring rail
    near_bar_L = cp.YD_NEAR - hp_t                             # near-column bar (wall → upright)
    far_bar_L = (ov.C_WID - hp_t) - cp.YD_FAR                  # far-column bar
    # wall-hanger / exterior backing plate height (constant across bars — see tote_restraint)
    bz0 = 500
    ext_ph = (bz0 + S + 57 + 18) - (bz0 - 61 - 18)             # 204.8

    RHS = f"{S:.1f}×{S:.1f}×3 SHS (2×2×0.120in)"
    BAR = "50×20×3 RHS"
    A500 = "A500 Gr.B"
    A36 = "A36 plate"
    rows = [
        # item, section/plate, material, cut size, qty, note
        ("Corner upright", RHS, A500, f"{upright_L:.0f} mm", 4, "full height; sits on the foot plate (Z12→TOP_Z)"),
        ("Ring rail — Yd (cross)", RHS, A500, f"{rail_yd_L:.1f} mm", 4, "2 rings (top+bottom) × 2 X-faces; butts between uprights"),
        ("Ring rail — X (deep)", RHS, A500, f"{rail_x_L:.1f} mm", 4, "2 rings × 2 Yd-faces; ties front↔back uprights"),
        ("Front retaining bar", BAR, A500, f"{near_bar_L:.0f} mm", 8, "2 per tote face (near+far columns identical length)"),
        ("Foot plate", f"{fp}×{fp}×{ft} plate", A36, f"{fp}×{fp}×{ft} mm", 4, "4× Ø{}mm anchor holes on Ø{} PCD".format(int(k.IBC_FOOT_BOLT_D), int(k.IBC_FOOT_BOLT_PCD))),
        ("Exterior wall backing plate", "8 mm plate", A36, f"60×{ext_ph:.1f}×8 mm", 8, "one per wall hanger; spreads the M12×65 load into the corrugated wall"),
        ("Wall joist hanger", "4 mm folded plate", A36, f"back {ext_ph:.0f} + seat 70, ×60 wide", 8, "Simpson-style U-pocket; folded, not welded"),
        ("Front-bar cleat (J2/W3)", "8 mm angle", A36, f"leg 90 + upstand {S + 8:.0f}, ×{bar_d} wide", 8, "L-angle: horizontal leg (bar sits on it) + upstand fillet-welded to the upright"),
        ("Rear-panel bracket (D)", "5 mm angle", A36, "base 40 + upstand, ×60 tall × 30 wide", 6, "L-bracket TEK-screwed to the back uprights (J8) + panel bolts (J4)"),
        ("Weld-on lashing ring", "forged ring + base", "—", "purchased", 8, "not a cut member — 2 per tier on the lower front bars (W4)"),
    ]
    return rows


def stock_summary():
    """Linear length + stick estimate per RHS section (for ordering)."""
    S = ov.IBC_FRAME_RHS
    ft = ov.IBC_FOOT_PLATE_T
    hp_t = 4
    L50 = 4 * (cp.TOP_Z - ft) + 4 * ((cp.YD_FAR - S) - (cp.YD_NEAR + S)) + 4 * (cp.BACK_X - (cp.FRONT_X + S))
    Lbar = 8 * (cp.YD_NEAR - hp_t)   # near = far length
    return [
        (f"{S:.1f}×{S:.1f}×3 SHS (uprights + rings)", L50),
        ("50×20×3 RHS (front bars)", Lbar),
    ]


def render_md():
    lines = ["| Member | Section / plate | Material | Cut size | Qty | Note |",
             "|--------|-----------------|----------|----------|-----|------|"]
    for item, sec, mat, size, qty, note in cut_list():
        lines.append(f"| {item} | {sec} | {mat} | {size} | {qty} | {note} |")
    lines.append("")
    lines.append("**Stock (buy sticks; add saw kerf + ~10% drop):**")
    lines.append("")
    lines.append("| Section | Total cut length | ≈ sticks (24 ft) |")
    lines.append("|---------|------------------|------------------|")
    for sec, L in stock_summary():
        ftlen = L / MM_PER_FT
        lines.append(f"| {sec} | {L / 1000:.2f} m ({ftlen:.1f} ft) | {int(-(-ftlen // 24))} |")
    return "\n".join(lines)


def inject():
    md = render_md()
    with open(REPORT, encoding="utf-8") as fh:
        txt = fh.read()
    block = f"<!-- BEGIN cutlist -->\n{md}\n<!-- END cutlist -->"
    if "<!-- BEGIN cutlist -->" not in txt:
        print("no <!-- BEGIN cutlist --> marker in the report — add the section first")
        return 1
    txt = re.sub(r"<!-- BEGIN cutlist -->.*?<!-- END cutlist -->", block, txt, flags=re.S)
    with open(REPORT, "w", encoding="utf-8") as fh:
        fh.write(txt)
    print(f"injected cut list into {os.path.relpath(REPORT)}")
    return 0


if __name__ == "__main__":
    if "--inject" in sys.argv:
        sys.exit(inject())
    print(render_md())
