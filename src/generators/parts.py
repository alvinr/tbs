#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""parts.py — the UNIFIED PARTS REGISTRY (drift-reduction Phase 5).

The single source of every purchasable item: quantity, type, supplier, unit-cost band, the
verified physical SIZE (folds in component-dimension-audit), and the cyanotype chemistry tiers.

From this ONE source, GENERATED views:
  • master-shopping-list.md — by TYPE, qty summed across systems, grouped by SUPPLIER (procurement).
  • each report's §Parts-List — by SYSTEM (emit_system).
  • component-dimension-audit.md — real-vs-modeled size reconciliation (emit_dimension_audit).
  • chemistry-shopping-list.md — cyanotype-only shopping (emit_chemistry).
costing.py's section totals reconcile to system_total() (lint-gated via costing.py --check-registry).

parts.py is the PROCUREMENT SOURCE OF RECORD (firm low/high item costs); costing.py is the scenario
layer (mid + budgeting bands) on top. Every system here must sum to its costing reconcile target.

# ─────────────────────────────────────────────────────────────────────────────────────────────
# TODO (ONGOING): VERIFY EVERY SPEC-DRIVEN PART's identity + price against current supplier listings.
# The bands below are an April-2026 basis (indicative low/high, pre-quote), and many hardware rows also
# lack a verified identity — no part number, the fit-critical dim (bore/thread/Ø) buried in `spec`, and
# a few carry a SKU whose format doesn't match the named supplier (a McMaster number under a Grainger
# row). Those can't be priced or ordered as-is. The `parts identity` lint advisory surfaces them.
# Workflow for the JS-/account-gated suppliers the web pass can't read (McMaster/Roton/Grainger/…):
# 1. python3 src/generators/build_parts_worklist.py → (re)generates parts-worklist.csv (merges fills)
# 2. fill the new_* columns from your logged-in supplier session (SKU, URL, fit dims, price)
# 3. python3 src/generators/apply_parts_csv.py parts-worklist.csv → writes them back here, scoped
# 4. python3 src/generators/parts.py --inject + costing.py --inject + lint.py → cascade + prove
# A band edit cascades automatically (master/report/cost blocks regenerate; costing reconciliation
# gate proves consistency). Update the master header's "Basis:" line when the refresh completes.
# ─────────────────────────────────────────────────────────────────────────────────────────────
"""
from __future__ import annotations
import argparse
import os
import re
from dataclasses import dataclass

import costing # reconciliation guardrail (EXPECTED) + the cost cascade it still owns
from tbs_constants import CLAMP_N_TOTAL, CLAMP_FILLER_D # muslin clamp count (3 edges) + L-channel filler depth

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ── The part record ──────────────────────────────────────────────────────────
@dataclass(frozen=True)
class Part:
    key: str # stable identity — the SAME physical part shares one key across systems,
    desc: str # so the by-type view sums its qty (e.g. 'm12x90-ss-bolt').
    type: str # taxonomy category (see TYPES)
    system: str # owning report section ('ventilation', 'water', 'electrical', …)
    qty: float # quantity in this system
    unit: str # 'ea' | 'm' | 'sheet' | 'roll' | 'lot' | 'job' | 'kg' | …
    low: float # UNIT cost band (line cost = qty × unit band)
    high: float
    supplier: str = "" # primary supplier
    supplier_alt: str = "" # fallback supplier
    url: str = ""
    part_no: str = ""
    spec: str = ""
    note: str = ""
    # sizing — folded-in component-dimension-audit (optional; sized/clash-relevant components only)
    dims: str = "" # verified physical envelope from the datasheet, e.g. '330×172×214'
    datasheet: str = "" # datasheet / catalog source
    modeled_const: str = "" # tbs_constants name(s) holding the modeled size (real-vs-modeled check)
    audit_status: str = "" # ✅ FIXED | ⚠ OPEN | confirm
    # chemistry — folded-in cyanotype shopping (optional)
    tier: str = "" # '' | 'lean' | 'standard' | 'rich'
    # plumbing-panel split (water system only) — keyword-only so existing positional calls are unaffected
    panel: str = "" # '' | 'Corridor' | 'Pinhole Wall' — drives the per-panel sub-lists in plumbing-report.md


def line(p: Part) -> tuple[float, float]:
    """(low, high) line cost = qty × unit band."""
    return (p.qty * p.low, p.qty * p.high)


# Taxonomy — the procurement TYPE buckets the master pivots on.
TYPES = [
    "container", "steel-structural", "stainless-sheet", "aluminum", "plastics-sheet",
    "timber-ply", "fasteners-hardware", "bearings-motion", "plumbing-fittings", "water-equipment",
    "electrical-power", "electrical-distribution", "seals-gaskets", "adhesives-finishes",
    "fabric-textile", "ducting-ventilation", "chemistry-reagents", "substrate-fabric",
    "tools-safety", "fabrication-labor",
]


# ── The registry ─────────────────────────────────────────────────────────────
# Populated system-by-system. Each system's line-cost sum must equal costing.EXPECTED[system]
# (the migration guardrail, asserted by self_check()).
#
# ── STAINLESS-GRADE POLICY (reconciled 2026-08-13) ───────────────────────────
# The cyanotype wash is ferric­ammonium­citrate / ferricyanide + citric acid — NO CHLORIDE. So 316's
# only advantage (chloride-pitting resistance) is UNUSED here. Grade selection is therefore:
#   • 304 (A2) — the DEFAULT for all wet/splash structural stainless (rails, plates, cross-slides,
#     skate, tray, and wet-zone fasteners). 316 is NOT metallurgically justified anywhere in this build.
#   • 316 — used ONLY by deliberate choice, not necessity: `bolt-m6-tray` (standing-wash tray seam, Alvin's
#     belt-and-suspenders call). Do NOT spec new 316 for corrosion alone — 304 covers it.
#   • 410 (martensitic) — self-drilling screws ONLY (`*-floor-anchor`, `walkway-floor-anchors`); needed to
#     self-drill steel (304 can't). Functional, not corrosion.
#   • Grade 8.8 ZINC — kept ONLY for the M12 structural through-bolts (`bolt-m12x65`/`x70`): strength
#     (800 MPa) is the driver and the heads sit OUTSIDE the container (inspectable/replaceable), shank in
#     the wall (not immersed). Going stainless without a strength loss would need A4-80 (=316) — not worth
#     it here (Alvin 2026-08-13). Small M6/M8 wet-zone fasteners went zinc→304 (modest load, A2-70 fine).
#   • Chrome-steel bearing (`sp-thrust-bearing` 51118) — bearing steel + annual grease; stainless S51118
#     is an optional humidity upgrade. `filter-machine-screws` stay zinc (dry, behind the housings).
PARTS: list[Part] = [
    # ═══ ventilation (§5b) — proves the schema; sums to EXPECTED['ventilation'] = 824 ═══
    Part("axial-fan-150", "150×150×50mm axial fans (12V DC)", "ducting-ventilation",
         "ventilation", 2, "ea", 25, 25, "Amazon", part_no="B091BTFBD9", url="https://www.amazon.com/dp/B091BTFBD9",
         spec="12V DC, ~150–200 CFM each — DA15050B12H (B091BTFBD9), 150×150×50mm, 12V 1.80A, dual-ball. ⚠ NOT the GDSTIME/Wathai '15050' Amazon fans (those are 110/120V AC) — this is the 12V DC part. Price est — confirm.",
         dims="150×150×50", modeled_const="FAN_DIAM/FAN_BODY_D", audit_status="✅ FIXED"),
    Part("evap-cooler-mc18m", "Evaporative cooler", "ducting-ventilation",
         "ventilation", 1, "ea", 109, 109, "Home Depot", part_no="MC18MT", url="https://www.homedepot.com/p/321429692",
         spec="Hessaire MC18M, 120V AC, {{fact:cooler_cfm_rated}} CFM (run low), {{fact:evap_cooler_w_ac}}W",
         dims="508×254×711", datasheet="Hessaire MC18M", modeled_const="EVAP_W/EVAP_D/EVAP_H",
         audit_status="✅ RESOLVED"),
    Part("cooler-inverter", "Cooler inverter — Victron Phoenix 12/375 GFCI", "electrical-power", "ventilation", 1, "ea", 132.60, 132.60,
         "Inverter Supply", "PKYS", part_no="PIN123750510", url="https://www.invertersupply.com/index.php?main_page=product_info&products_id=200695",
         spec="Victron Phoenix 12/375 120V VE.Direct GFCI (12V→120V, 375VA/300W) — GFCI in the faceplate outlet satisfies the wet-cooler requirement (no separate GFCI needed). Firm $132.60."),
    Part("shade-cloth-80", "Shade cloth — 70% (10×20 ft)", "fabric-textile",
         "ventilation", 1, "ea", 30.50, 30.50, "Amazon", "Farm supply", part_no="B075J93DTJ", url="https://www.amazon.com/dp/B075J93DTJ",
         spec="Perfect Sunblock 10×20 ft 70% shade cloth with grommets (B075J93DTJ), $30.50 firm (2026-07-30). 80% grade is uncommon; 70% chosen (any 70–90% works for the cooler/canopy shade)."),
    # Shade-canopy frame (20×10 ft), itemized 2026-07-27 from the $120 "Canopy frame" lot:
    Part("canopy-emt-conduit", '1.5" EMT conduit, 10 ft', "steel-structural",
         "ventilation", 6, "stick", 21.86, 21.86, "Home Depot", part_no="550210000", url="https://www.homedepot.com/p/304229415", spec='Shade-canopy frame legs + top rails. 1" EMT, 6× 10-ft sticks (downsized from 1.5" 2026-07-27 — adequate for a shade-cloth canopy).'),
    Part("canopy-emt-fittings", "EMT canopy fittings (couplings, corner ells, connectors)", "steel-structural",
         "ventilation", 8, "ea", 1.45, 1.45, "Home Depot", part_no="12210", url="https://www.homedepot.com/p/100135091", spec="1\" EMT set-screw couplings joining the straight frame runs (×8). Corner turns handled by the 1\" pull elbows (canopy-emt-elbows)."),
    Part("canopy-emt-base", "EMT canopy base plates + ground stakes (×4)", "steel-structural",
         "ventilation", 1, "4-pack", 16.29, 16.29, "Home Depot", part_no="PDB-F-1-4", url="https://www.homedepot.com/p/317889187", spec="PIPE DECOR 1\" black-iron floor flange 4-pack — one per leg base (×4). Add ground stakes/guys if free-standing."),
    Part("canopy-emt-elbows", "EMT canopy corner pull elbows (×4)", "steel-structural",
         "ventilation", 4, "ea", 11.85, 11.85, "Home Depot", part_no="94510", url="https://www.homedepot.com/p/203776547", spec="Halex 1\" EMT rigid pull elbow at the 4 top-frame corners (chose bought elbows over field-bending)."),
    Part("baffle-metal-fan", "Baffle duct sheet metal (fans)", "steel-structural",
         "ventilation", 1, "lot", 30, 30, "Local sheet metal", "Home Depot", spec="22 ga galvanized, 2 × 300mm stubs"),
    Part("baffle-metal-cooler", "Baffle duct sheet metal (cooler)", "steel-structural",
         "ventilation", 1, "lot", 20, 20, "Local sheet metal", "Home Depot", spec="22 ga galvanized, 1 × 300mm stub, Ø200mm"),
    Part("flex-duct-200", "200mm insulated flex duct", "ducting-ventilation",
         "ventilation", 1, "coil", 62.68, 62.68, "Home Depot", part_no="23-183-08-25", url="https://www.homedepot.com/p/314398619", spec='Rubber-Cal 8" × 25 ft flexible ducting coil (one coil covers the cooler riser run with margin)'),
    Part("duct-elbow-200", "200mm 90° duct elbow", "ducting-ventilation",
         "ventilation", 1, "ea", 14.69, 14.69, "Home Depot", part_no="MF-90E8", url="https://www.homedepot.com/p/100187427", spec='Master Flow 8" 90° adjustable galvanized elbow (model 90E8), cooler riser to wall stub'),
    Part("duct-collar-clamp", "Duct collar + hose clamp", "ducting-ventilation",
         "ventilation", 1, "set", 16.23, 16.23, "Home Depot", part_no="DSCF8", url="https://www.homedepot.com/p/100211540", spec='Master Flow 8" starting collar/take-off (DSCF8 $8.98, Home Depot) + worm-drive band clamp (McMaster 4866N35 $7.25) = $16.23/set to secure the flex duct.'),
    Part("duct-cap-200", "Weatherproof duct cap", "ducting-ventilation",
         "ventilation", 1, "ea", 11.98, 11.98, "Home Depot", part_no="8DC", url="https://www.homedepot.com/p/100396923", spec='Master Flow 8" round removable duct cap'),
    Part("deutsch-dt-2pin", "Deutsch DT 2-pin connectors (Amphenol AT2PS-CKIT)", "electrical-distribution",
         "ventilation", 2, "set", 4, 4, "Waytek Wire", part_no="AT2PS-CKIT", url="https://www.waytekwire.com/product/amphenol-sine-systems-at2ps-ckit-2-pin",
         spec="Amphenol AT2PS-CKIT 2-pin connector kit (DT-compatible), IP67 — Fan B flex connector (×2 sets). Same part as deutsch-dt-2pin-elec. $4/set est — confirm at order."),
    Part("coiled-cable-16awg", "16 AWG coiled (retractile) cable, 2-cond", "electrical-distribution",
         "ventilation", 1, "ea", 25.99, 25.99, "Amazon", "Grainger", part_no="B0GYFNXM9Z", url="https://www.amazon.com/dp/B0GYFNXM9Z",
         spec="MECCANIXITY retractable coiled cable, 16 AWG 2-conductor, 10 ft extended (B0GYFNXM9Z), $25.99 firm (2026-07-30). Fan B flex on the swinging hinged panel — takes the ~56° transport swing. Proper 2-conductor. Deutsch DT 2-pin ends."),
    Part("cooler-power-cable", "Cooler external power cable", "electrical-distribution",
         "ventilation", 1, "ea", 20, 20, "Waytek Wire", "Amazon", spec="1.5m, 14 AWG 2-cond, Deutsch DT 2-pin plugs each end"),
    Part("ratchet-strap-25", "Ratchet straps, 25mm", "fasteners-hardware",
         "ventilation", 1, "4-pack", 9.97, 9.97, "Home Depot", part_no="FH0829", url="https://www.homedepot.com/p/312994495", spec='Cooler stowage. Husky 12 ft × 1" ratchet tie-downs, S-hook, 4-pack — design uses 2, 2 spare'),
    # plywood-base-12 RETIRED 2026-07-27 — the cooler stowage base plate (600×350) is now cut from the
    # full panel-fanb-ply 4×8 sheet (use panel-fanb-ply instead); a separate ½" panel line was
    # redundant given the leftover from that sheet. See panel-fanb-ply.

    # ═══ water family (split per owning report; reconciled to costing.WATER lines — water-system §8
    # item-sums after the 2026 reconciliation). The §8 group ("water") = storage+pumps+filter+valves+
    # pipe+wiring+consumables; the frame/tray/spray are SEPARATE systems (their own reports). ═══
    # — storage (395–720) —
    Part("ibc-tote-1000l", "IBC tote (1,000 L caged)", "water-equipment",
         "water", 4, "ea", 150, 150, "SoCal reconditioner", "Repackify",
         url="https://www.repackify.com/buy-ibc-totes/california",
         spec="Reconditioned food-grade (prior-food-contents) 275-gal/1000L caged composite tote, DN50 butterfly valve (S60×6 thread); side-entry fittings near top. ~$150/ea local SoCal (Container Exchanger food-grade lots have a ~12-tote min; buy 4 local). Firm ~$150.",
         dims="1219×1016×1168", modeled_const="IBC_W/IBC_D/IBC_H_1000", audit_status="✅ FIXED (v2)"),
    Part("bulkhead-2in", 'Bulkhead fitting 2" NPT (polypropylene)', "plumbing-fittings",
         "water", 3, "ea", 21.14, 21.14, "US Plastic Corp", part_no="32200", url="https://www.usplastic.com/catalog/item.aspx?itemid=32200",
         spec="X1/X3/X4 external fill/drain ports — 2\" PP bulkhead tank fitting with EPDM gaskets, clamped through a drilled hole in the container end wall over a flat backing doubler (NOT welded; the corrugation is bridged by the doubler). PP matches the FRPP camlocks it mates. US Plastic 32200 (alt listing itemid 65995), $21.14 firm (2026-07-29) — SS (McMaster 4464K115 $136.70) was over-spec for a plain water port. UV: end wall largely shaded; use brass if long direct-sun exposure.",
         note="Price verified 2026-07-12 (McMaster 4464K115, $136.70 ea)."),
    # — pumps (315–345) —
    Part("shurflo-2088", "Shurflo 2088-554-144 pump (×5 — P-01 Blue supply / P-02 Brown recycle-spray / P-03 waste evac / P-04 tray drain / P-05 Brown drain)", "water-equipment",
         "water", 5, "ea", 100, 100, "Amazon", "Fresh Water Systems",
         part_no="B00C1M6B1C",
         url="https://www.amazon.com/dp/B00C1M6B1C",
         spec='12VDC, 3.5 GPM, 45 PSI, 1/2" NPSM ports; 5 identical pumps, one per water-system duty (P-01..P-05). 2026-07-27: consolidated from 5 lines; firm $100 ea (Amazon B00C1M6B1C)',
         dims="216×127×114", datasheet="Shurflo 2088-554-144", modeled_const="PUMP_D×PUMP_YD_SPAN×Z",
         audit_status="✅ FIXED (minor) — protrusion PUMP_D 100→114", panel="Corridor"),
    Part("seaflo-accumulator", "SeaFlo accumulator (0.75 L)", "water-equipment",
         "water", 2, "ea", 35.99, 35.99, "Amazon",
         url="https://www.amazon.com/dp/B01MUYL8F8",
         spec='0.75 L, 125 PSI, 1/2" MNPT', part_no="SFAT-075-125-01",
         dims="200×127×125", datasheet="SeaFlo SFAT-075-125-01", modeled_const="Ø127×200 cyl",
         note="Two: ACC-01 damps the main filter loop (corridor); ACC-02 damps the recycle-spray pump P-02 on the filter skid.",
         audit_status="✅ FIXED — cylinder 150→200", panel="Corridor"),
    # shurflo-bracket RETIRED 2026-07-31 — the mounting bracket ships with the Shurflo 2088-554-144 pump (Alvin confirmed); −$50.
    # — corridor plumbing-panel structure (3D-derived exterior ply; previously uncosted) —
    Part("corridor-panel-ply-18", "Corridor plumbing-panel ply (23/32\" exterior)", "timber-ply",
         "water", 1, "sheet", 29.30, 29.30, "Home Depot", part_no="303564747",
         url="https://www.homedepot.com/p/23-32-in-x-4-ft-x-8-ft-RTD-Southern-Yellow-Pine-Wood-Sheathing-Plywood-129323/303564747",
         spec='4×8 ft 23/32\" (18mm) RTD Southern Yellow Pine exterior sheathing — rear backing board + drain-riser spine + 3× pump-run side support boards (far + near-lower ~399×420, near-upper ~399×690, #29, cut from the sheet leftover — ~0.62 m² of a 2.97 m² sheet) + spacer offcuts. STANDARD exterior per project rule. Firm $29.30 (Home Depot 2026-07-23). Seal cut edges.',
         panel="Corridor"),
    Part("corridor-panel-ply-25", "Pump-mount shirt ply (23/32\" exterior)", "timber-ply",
         "water", 1, "sheet", 29.30, 29.30, "Home Depot", part_no="303564747",
         url="https://www.homedepot.com/p/23-32-in-x-4-ft-x-8-ft-RTD-Southern-Yellow-Pine-Wood-Sheathing-Plywood-129323/303564747",
         spec='4×8 ft 23/32\" (18mm) RTD Southern Yellow Pine exterior sheathing — pump-mount shirt (~610×1650 cut) behind P-01..P-05 + 6× spacer blocks. Same SKU as ply-18; 5× Shurflo 2088 (~6.5 kg total) need no more than 3/4\". STANDARD exterior per project rule. Firm $29.30 (Home Depot 2026-07-23). May nest with ply-18 in one sheet at cut — carried separate for margin. Double-layer locally if extra pump-rail stiffness wanted.',
         panel="Corridor"),
    Part("pinhole-panel-ply-18", "Pinhole-wall filter-skid backing ply (23/32\" exterior)", "timber-ply",
         "water", 2, "sheet", 29.30, 29.30, "Home Depot", part_no="303564747",
         url="https://www.homedepot.com/p/23-32-in-x-4-ft-x-8-ft-RTD-Southern-Yellow-Pine-Wood-Sheathing-Plywood-129323/303564747",
         spec='4×8 ft 23/32\" (18mm) RTD Southern Yellow Pine exterior sheathing — pinhole-wall backing panel (~1795×1440) that the 3× Big Blue filters + the P-04/SV-02/DV-02 skid row + ACC-02 machine-screw to (via back-face pronged tee-nuts — tnut-quarter/tnut-fivesixteen, #30). PIECED from 2 sheets (butt-jointed): the 1795×1440 face exceeds a single 4×8 sheet 1219mm width. Same SKU as the corridor panels; STANDARD exterior per project rule (dry mounting backboard, NOT marine). Firm $29.30 (Home Depot 2026-07-23). Seal cut edges.',
         panel="Pinhole Wall"),
    # Corridor plumbing-panel mount, itemized 2026-07-27 from the $25–50 hardware lot:
    Part("corridor-panel-brackets", "6× steel angle brackets (corridor panel → IBC uprights)", "fasteners-hardware",
         "water", 6, "ea", 2.5, 6.5, "Home Depot",
         spec="L-brackets fixing the corridor plumbing panel to the IBC-frame back uprights — TEK-screwed to the post (J8, 2× #14 self-drillers per bracket — no weld, bolt-on to the pre-painted frame), rear panel fastened J4 (M8 into captive tee-nut), per ibc-stacking-report §3.5. Price est.",
         panel="Corridor"),
    Part("corridor-panel-fasteners", "Corridor panel mount fasteners (shirt-to-panel screws + lag bolts)", "fasteners-hardware",
         "water", 1, "lot", 10, 11, "Home Depot",
         spec="Shirt-to-panel screws + lag bolts landing the brackets into the panel/uprights. Price est.",
         panel="Corridor"),
    Part("bracket-tek-screws", "36× #14 self-drilling TEK screws (bracket → post, J8/J9)", "fasteners-hardware",
         "water", 36, "ea", 0.30, 0.55, "Home Depot", supplier_alt="McMaster-Carr",
         spec="#14 × 1in HWH self-drilling TEK screw, #4/5 point (drills the ~6–8mm steel-to-steel: angle leg + the 3mm RHS post wall), 410 SS for the damp container. Attach the corridor-panel L-brackets (J8, 2×6=12) + the side-panel pipe-run L-brackets (J9, 2×12=24) to the IBC posts — NO weld, so the brackets bolt onto a pre-painted frame with no hot work. Price est. per-ea (sold in 100-boxes).",
         panel="Corridor"),
    # — #29 pump-run supports: 2 side ply boards (cut from corridor-panel-ply-18) + welded L-brackets + cushioned P-clips —
    Part("pump-support-brackets", "12× steel L-brackets (side-panel pipe-run boards) + 4 skid standoff clamps", "fasteners-hardware",
         "water", 1, "lot", 12, 24, "Metal Supermarkets", supplier_alt="Home Depot",
         spec="12× steel L-brackets TEK-screwed to the IBC side-post inner faces (2 per post × 3 side-panel boards: far, near-lower, near-upper) — the side-wall boards carry the PIPE runs (P-clips), NOT pumps; the boards bolt to the landing legs (rear-panel method); + 4 short standoff brackets carrying the forward SV-01/DV-02 skid lines. Cut from 1×1×1/8 steel angle offcuts — attached J9 (2× #14 self-drillers per bracket, no weld), boards fastened J5 (¼-20 into captive tee-nut), per ibc-stacking-report §3.5. MATERIAL est.; FAB (cut) = shop quote (material-now rule). (Registry key kept as 'pump-support-brackets' for cost continuity; they support the pump-run PIPING.)",
         panel="Corridor"),
    Part("pipe-support-clips", "39× cushioned pipe P-clips (3/4\" pipe)", "fasteners-hardware",
         "water", 39, "ea", 0.55, 0.95, "Home Depot", supplier_alt="McMaster-Carr",
         spec="Cushioned (rubber-lined) pipe P-clips securing the pump risers/runs to the ply support boards + spine + skid panel (#29): corridor side boards 17 (far 6 + near-lower 4 + near-upper 7), drain-riser spine 10 (6 riser + 4 far-side X-port lines), filter-skid 12 (6 risers + 6 runs) = 39. Sized for OD21 (3/4\") PVC. Zinc + EPDM cushion. Price est. — firm at blueprint.",
         panel="Corridor"),
    # — filter (286–485): 3 separate 4.5×20 housings on a slotted-angle skid frame (§3.1/§7.2) —
    Part("bigblue-housing", 'Big Blue filter housing 4.5"×20" (separate)', "water-equipment",
         "water", 3, "ea", 83.30, 83.30, "Amazon", part_no="B0137680E6", url="https://www.amazon.com/dp/B0137680E6", dims="Ø184×594",
         spec='Ø184×594mm/housing (4.5×20), 1" NPT ports, accepts standard 20"×4.5" cartridges (verified 2026-07-27) — three SEPARATE Pentair Pentek 150234 high-flow PP housings on the mounting brackets',
         datasheet="Pentek 4.5×20 BB", modeled_const="BB_OD/BB_H",
         audit_status="3-separate design of record (2026-07): combo → 3 separate housings + frame per plumbing-report §3.1/§7.2. Prices indicative — firm at the Aug-2026 re-price.", panel="Pinhole Wall"),
    Part("filter-skid-frame", "Big Blue housing mounting brackets (×3)", "water-equipment",
         "water", 3, "ea", 10.50, 10.50, "Fresh Water Systems", part_no="150061", url="https://www.freshwatersystems.com/products/mounting-bracket-white-single-housing-for-10-20-big-blue-housings", spec="Pentair 150061 zinc-plated single-housing mounting bracket, one per 4.5×20 Big Blue (×3), machine-screwed to the 18mm ply backing via back-face pronged tee-nuts (#30, re-torqueable). Purpose-built — replaces the welded slotted-angle frame (2026-07-27).", panel="Pinhole Wall"),
    # filter-ubracket RETIRED 2026-07-22 — Big Blue housings have mounting-hole ears; lag-screw straight to the ply backing
    # ── #30 captive-tee-nut conversion (2026-08-07): every REMOVABLE ply-mount joint moves from a
    #    wood/lag screw to a machine screw into a back-face 4-prong tee-nut (re-torqueable, no thread-strip).
    Part("filter-machine-screws", "Zinc machine screws — filter housings to ply tee-nuts", "fasteners-hardware",
         "water", 8, "ea", 1.57, 1.57, "Home Depot", part_no="831121", url="https://www.homedepot.com/p/Everbilt-5-16-in-18-x-2-1-2-in-Phillips-Slotted-Round-Head-Machine-Screw-831121/317478933", spec="2 per housing × 3 = 6 needed (+2 spare) — Everbilt 5/16\"-18 × 2½\" ZINC round-head machine screw through the 150061 bracket ear + 25mm standoff + 18mm ply into a back-face pronged tee-nut (tnut-fivesixteen). Machine-screw joint replaces the 5/16 lag screws (#30) — re-torqueable, serviceable. ZINC not SS (dry backboard mount behind the housings — not immersion; Alvin). Sold individually (screw + nut; nut unused). Firm $1.57 ea (Home Depot 2026-08-07).", panel="Pinhole Wall"),
    Part("tnut-fivesixteen", "5/16\"-18 pronged tee-nut (filter housings)", "fasteners-hardware",
         "water", 2, "4-pack", 1.57, 1.57, "Home Depot", "McMaster-Carr", part_no="825091", url="https://www.homedepot.com/p/Everbilt-5-16-in-18-Zinc-Plated-Tee-Nut-4-Pack-825091/317478996", spec="Everbilt 5/16\"-18 zinc 4-prong tee-nut, 3/8\" (9.5mm) barrel — seats from the BACK of the 18mm ply (no front punch-through). 6 needed (2 per Big Blue housing × 3) + 2 spare → 2× 4-pack. Mates filter-machine-screws. Firm $1.57/4-pack (Home Depot 2026-08-07). Bulk alt: McMaster 50-pack $7.47.", panel="Pinhole Wall"),
    Part("tnut-quarter", "1/4\"-20 pronged tee-nut (ply-mount interfaces)", "fasteners-hardware",
         "water", 10, "4-pack", 1.57, 1.57, "Home Depot", part_no="825001", url="https://www.homedepot.com/p/Everbilt-1-4-in-20-Zinc-Plated-Tee-Nut-4-Pack-825001/317478995", spec="Everbilt 1/4\"-20 zinc 4-prong tee-nut, 5/16\" (8mm) barrel — seats from the BACK of the 18mm ply. Captive re-torqueable anchor for every ¼-20 ply-mount interface (#30, 2026-08-07): P-04/SV-02/DV-02 skid row (6), ACC-01/02 (4), pump-mount shirt 5× Shurflo (10), valve brackets (6), EP panel (4), chem shelf (4), Fan-B band (2) = 36 + 4 spare → 10× 4-pack. Mostly water; the EP/shelf/Fan-B pieces (~10) are minor cross-system, carried on this one hardware line. Firm $1.57/4-pack (Home Depot 2026-08-07)."),
    Part("panel-machine-screws", "1/4\"-20 zinc machine screws (ply-mount interfaces)", "fasteners-hardware",
         "water", 10, "4-pack", 1.57, 1.57, "Home Depot", part_no="826771", url="https://www.homedepot.com/p/Everbilt-1-4-in-20-x-1-in-Combo-Truss-Head-Zinc-Plated-Machine-Screw-4-Pack-826771/317479749", spec="Everbilt ¼-20 × 1\" ZINC combo truss-head machine screw into the tnut-quarter pronged tee-nuts — the machine-screw half of every ¼-20 ply-mount joint (36 + spare → 10× 4-pack = 40). Length 1\" gives full tee-nut engagement with ~3mm back protrusion. ZINC not SS (dry backboard mounts; Alvin). Firm $1.57/4-pack (Home Depot 2026-08-07)."),
    Part("filter-hdpe-spacer", "Plywood offcut spacer blocks 25mm (filter skid)", "water-equipment",
         "water", 1, "lot", 0, 0, "offcuts", spec="25mm standoff blocks between the housing's mounting ears and the ply backing — sump-bowl hang clearance (the housing machine-screws through them into the back-face tee-nuts). Cut from PLYWOOD OFFCUTS (2026-07-25 — no need for HDPE; dry standoff, not a wet-immersion part).", panel="Pinhole Wall"),
    # filter-jumper RETIRED 2026-07-27 — the F-01→F-02→F-03 inter-housing jumpers are now itemized as
    # 1" PVC stock (pvc-1in) + 1" slip elbows (elbow-el100) + slip×NPT adapters (pvc-transition-adapters);
    # keeping the bundled "lot" line double-counted the pipe/elbows/adapters.
    Part("cartridge-sediment", 'MPP 5-micron sediment cartridge 4.5"×20"', "water-equipment",
         "water", 2, "ea", 30.83, 30.83, "Amazon", part_no="B0CJCVZ1L5", url="https://www.amazon.com/dp/B0CJCVZ1L5", spec="Pentek DGD-5005-20 dual-gradient-density 5-micron sediment cartridge (F-1 stage); ~50-print interval. $61.66/2-pack = $30.83 ea.", panel="Pinhole Wall"),
    Part("cartridge-kdf", 'KDF-55 heavy-metal cartridge 4.5"×20"', "water-equipment",
         "water", 1, "ea", 79.83, 79.83, "Amazon", part_no="B0DY1ZK47Z", url="https://www.amazon.com/dp/B0DY1ZK47Z", spec="KDF-55 media for dissolved iron/metal removal (F-2 stage); ~60-print interval. Aquaboon 20×4.5 KDF whole-house cartridge (proper KDF media — supersedes the earlier VEVOR chlorine-only cartridge).", panel="Pinhole Wall"),
    Part("cartridge-carbon", 'CTO carbon block cartridge 4.5"×20"', "water-equipment",
         "water", 2, "ea", 39.90, 39.90, "Amazon", part_no="B07ZHPB6MB", url="https://www.amazon.com/dp/B07ZHPB6MB", spec="Coconut shell activated carbon block (F-3 stage); ~40-print interval. Aquaboon CTO, $79.79/2-pack = $39.90 ea (same brand as the KDF/sediment cartridges).", panel="Pinhole Wall"),
    # — valves & fittings (333–567) —
    Part("valve-v050fp-corridor", 'Banjo V050FP ball valve 1/2" FNPT', "plumbing-fittings",
         "water", 3, "ea", 24.14, 24.14, "Grainger", spec="PP full-port quarter-turn 2-way; pump-suction isolation BV-01 (P-01), BV-02 (P-05), BV-06 (P-03). Grainger firm $24.14 (checked 2026-08-07; was US Plastic $44.27).", panel="Corridor", part_no="803HZ1", url="https://www.grainger.com/product/803HZ1"),
    Part("valve-v050fp-wall", 'Banjo V050FP ball valve 1/2" FNPT', "plumbing-fittings",
         "water", 1, "ea", 24.14, 24.14, "Grainger", spec="PP full-port quarter-turn 2-way; pump-suction isolation BV-03 (P-02). Grainger firm $24.14 (checked 2026-08-07; was US Plastic $44.27).", panel="Pinhole Wall", part_no="803HZ1", url="https://www.grainger.com/product/803HZ1"),
    Part("valve-v050fp-supply", 'Banjo V050FP ball valve 1/2" FNPT', "plumbing-fittings",
         "water", 2, "ea", 24.14, 24.14, "Grainger", spec="PP full-port 2-way; BV-04 (TAP-01 chem-tap isolation) + BV-05b (spray-bar ON/OFF, at the spray-bar feed). Grainger firm $24.14 (checked 2026-08-07). Spray selection is split into TWO 1/2\" valves — this 2-way for on/off + a 1/2\" 3-way Blue/Brown selector (valve-3way-half) — replacing a single 3/4\" 3-way L-port (no reducers, no L-port OFF-detent risk).", part_no="803HZ1", url="https://www.grainger.com/product/803HZ1"),
    Part("valve-v100fp", 'Banjo V100FP ball valve 1" FNPT', "plumbing-fittings",
         "water", 6, "ea", 49.45, 49.45, "US Plastic Corp", "Amazon", spec="PP full-port; V1/V3/V4, VB1–VB3 (IBC fill/drain)", part_no="30653", url="https://www.usplastic.com/catalog/item.aspx?itemid=30653"),
    Part("valve-3way-half", '3-way diverter valve 1/2" FNPT', "plumbing-fittings",
         "water", 2, "ea", 23.99, 23.99, "US Plastic Corp", spec="L/T-port PVC-compatible; 3W-DV-02 (tray drain) + BV-05a (spray Blue/Brown SELECTOR — 2 inlets Blue+Brown → 1 outlet to BV-05b on/off). Same valve as the diverters.", panel="Corridor", part_no="22365", url="https://www.usplastic.com/catalog/item.aspx?itemid=22365"),
    Part("valve-3way-1in", '3-way diverter valve 1" FNPT', "plumbing-fittings",
         "water", 1, "ea", 61.31, 61.31, "US Plastic Corp", spec="L/T-port; 3W-DV-01 (filter output)", panel="Pinhole Wall", part_no="31268", url="https://www.usplastic.com/catalog/item.aspx?itemid=31268"),
    Part("sample-tap-sv01", 'pH sample tap (SV-01) — 1/2" PP ball valve + barb spout + branch tee', "plumbing-fittings",
         "water", 1, "ea", 19.26, 19.26, "US Plastic Corp", part_no="36903", url="https://www.usplastic.com/catalog/item.aspx?itemid=36903", spec='Filtered-water sample draw before 3W-DV-01; 1/2" PP sample valve (US Plastic 36903) + downturned 1/2" hose barb on a 1"×1/2" reducing branch tee, panel face above spill line', panel="Pinhole Wall"),
    Part("sample-tap-sv02", 'pH sample tap (SV-02) — 1/2" PP ball valve + barb spout + branch tee', "plumbing-fittings",
         "water", 1, "ea", 19.26, 19.26, "US Plastic Corp", part_no="36903", url="https://www.usplastic.com/catalog/item.aspx?itemid=36903", spec="pH sample on the P-04 tray-drain discharge, before 3W-DV-02; same build/SKU as SV-01 (US Plastic 36903 $19.26 — priced under SV-01; applied to SV-02 as the identical build)", panel="Corridor"),
    Part("camlock-2in", '2" polypropylene camlock pairs (M+F)', "plumbing-fittings",
         "water", 4, "pair", 22.93, 22.93, "US Plastic Corp", spec="External bulkhead connections (X1/X3/X4 + spare). 2026-07-27: pair = US Plastic 30754 female coupler $16.23 + 30619 male adapter $6.70 = $22.93 (Banjo FRPP, EPDM)", part_no="30754", url="https://www.usplastic.com/catalog/item.aspx?itemid=30754"),
    Part("elbow-half", '1/2" PVC Sch-40 slip 90° elbow', "plumbing-fittings",
         "water", 14, "ea", 0.74, 0.74, "Home Depot", part_no="PVC023000600HD", url="https://www.homedepot.com/p/203812033", spec="All pump-driven run bends. Charlotte PVC Sch-40 90° S×S — CONFIRMED slip / solvent-cement (2026-07-28), NOT threaded."),
    Part("elbow-el100", '1" PVC Sch-40 slip 90° elbow', "plumbing-fittings",
         "water", 4, "ea", 1.52, 1.52, "Home Depot", part_no="PVC023001000HD", url="https://www.homedepot.com/p/203812125", spec='1" PVC slip run bends (joint convention §5.1): IBC bends, filter outlet to DV-01. 2026-07-27 fork b — was threaded Banjo FRPP $4.59. Charlotte PVC023001000HD 90° S×S.'),
    Part("tee-half", '1/2" PVC Sch-40 slip tee', "plumbing-fittings",
         "water", 6, "ea", 0.81, 0.81, "Home Depot", part_no="PVC024000600HD", url="https://www.homedepot.com/p/203812195", spec="Blue suction/discharge tees, branches. Charlotte PVC Sch-40 S×S×S — CONFIRMED slip / solvent-cement (2026-07-28), NOT threaded."),
    Part("tee-100", '1" PVC Sch-40 slip tee', "plumbing-fittings",
         "water", 3, "ea", 2.13, 2.13, "Home Depot", part_no="PVC024001000HD", url="https://www.homedepot.com/p/203812199", spec='1" PVC slip run tees (joint convention §5.1): 3× IBC drain. 2026-07-27: X1 fill split dropped — X1 is a 4-way cross (cross-100), not a tee. Charlotte PVC024001000HD S×S×S.'),
    # Joint convention §5.1 (fork c): one slip×MNPT male adapter where the glued PVC run lands on each
    # threaded component. Sized to the run at each landing — ½" and 1" only (the ¾" spray run ends in
    # barbed irrigation fittings, not threaded PVC). Counts are a P&ID takeoff (2026-07-28), firm with the fab.
    Part("pvc-adapter-half", '1/2" PVC slip×MNPT male adapter', "plumbing-fittings",
         "water", 24, "ea", 0.79, 0.79, "Home Depot", part_no="PVC021090600HD", url="https://www.homedepot.com/p/203811636", spec='½" landings (24 — P&ID takeoff 2026-07-28, +ACC-02 2026-08-04): 6× BV ball valves (BV-01–06, run side) + 5× pump discharges (P-01–05, hose→run) + 3W-DV-02 (3 ports) + SV-01/SV-02 taps (2) + accumulator ACC-01 (1, slip×FPT) + accumulator ACC-02 (2 — inline IN+OUT on the recycle-spray line) + 2× ½" unions (4, slip×MNPT each side) + bushing-reducer ½" run side (1). Charlotte PVC021090600HD.'),
    Part("pvc-adapter-1in", '1" PVC slip×MNPT male adapter', "plumbing-fittings",
         "water", 26, "ea", 1.16, 1.16, "Home Depot", part_no="PVC021091000HD", url="https://www.homedepot.com/p/203811640", spec='1" landings (26 — P&ID takeoff 2026-07-28): 6× V100 valves (V1/V3/V4, VB1–3, run side) + 8× s60-adapter IBC-valve landings (each lands on its own 1" glued-run segment) + 3W-DV-01 (3 ports) + CV-1 (2 ports) + 5× filter housing ports (F-01 OUT, F-02 IN/OUT, F-03 IN/OUT; F-01 IN = bushing-reducer) + 2× Blue equalization bulkheads. Charlotte PVC021091000HD.'),
    Part("cross-100", '1" PVC 4-way cross fitting', "plumbing-fittings",
         "water", 1, "ea", 5.99, 5.99, "Amazon", part_no="B0CGGV74MB", url="https://www.amazon.com/dp/B0CGGV74MB", spec="X1 fresh-fill 4-way (confirmed 2026-07-27): X1 inlet + IBC-1 + IBC-2 + DV-01 blue-recycle riser all join here on the corridor spine, then distribute to both Blue totes. 1\" PVC cross — slip glue joint, gravity/low-pressure fill. Design of record: the 3D model + corridor panel-layout + plumbing-report all build this cross."),
    # Joint convention §5.1 — Option C hybrid (2026-07-27): permanent slip couplings on the run,
    # true unions only where a whole sub-assembly pulls as a unit (per-component service is already
    # covered by the threaded ports on pumps/filters/valves).
    Part("coupling-half", '1/2" PVC Sch-40 slip coupling', "plumbing-fittings",
         "water", 4, "ea", 0.74, 0.74, "Home Depot", part_no="PVC021000600HD", url="https://www.homedepot.com/p/203811331", spec="Permanent solvent-weld run joins (4×). Charlotte PVC Sch40 S×S coupling."),
    Part("union-half", '1/2" PVC union (serviceable break)', "plumbing-fittings",
         "water", 2, "ea", 4.96, 4.96, "Home Depot", part_no="PVCU12F", url="https://www.homedepot.com/p/317901071", spec="True hand-unscrew unions at the 2 points where a whole sub-assembly must come out as a unit (pump manifold + filter-bank inlet). Apollo ½\" PVC FIP×FIP (threaded) union — lands on the slip run via a slip×MNPT adapter each side (4 total across the 2 unions, in the pvc-adapter-half allowance)."),
    Part("bushing-reducer", '1/2"×1" NPT bushing reducer', "plumbing-fittings",
         "water", 1, "ea", 2.86, 2.86, "Home Depot", part_no="PVC021121800HD", url="https://www.homedepot.com/p/204836713", spec="P-02 riser → F1 filter inlet — THREADED (lands on the filter = hard component, per the joint convention). Charlotte PVC Sch40 1×½ reducer bushing"),
    # IBC tote → 1" PVC run: FLEXIBLE-JUMPER connection (2026-07-29). A semi-rigid plumbing
    # panel flexing against fixed totes would fatigue a solvent-welded PVC joint, so a short 1" flex
    # hose de-couples each tote outlet from the rigid run. Chain per tote (×8):
    # S60x6 valve → s60-adapter (→2"MNPT) → s60-reducer (→1"FNPT) → ibc-flex-barb-m → flex hose
    # (cut from the tray-suction-hose coil) → ibc-flex-barb-f → pvc-adapter-1in (1"MNPT) → glued 1" PVC.
    # Camlock idea dropped — quick-release not a driver (totes are fixed in place once installed).
    Part("s60-adapter", 'S60×6 female buttress → 2" MNPT IBC tote adapter', "plumbing-fittings",
         "water", 8, "ea", 9.99, 9.99, "Amazon", part_no="B095SCHBC6", url="https://www.amazon.com/Granatan-Adapter-Buttress-Fittings-Connector/dp/B095SCHBC6", spec='IBC DN50 tote outlet (male S60×6) → 2" male NPT, polypropylene (Granatan). No US single-piece S60→1" NPT exists (the 1" ones are BSP or garden-hose thread), so reduce 2"→1" via s60-reducer. $9.99 firm (2026-07-29).'),
    Part("s60-reducer", '2"→1" PVC Sch-80 reducing coupling (FNPT×FNPT)', "plumbing-fittings",
         "water", 8, "ea", 3.21, 3.21, "Home Depot", part_no="PVC021071300HD", url="https://www.homedepot.com/p/203811533", spec='Charlotte 2"×1" PVC Sch-40 reducer bushing, SPIGOT×SLIP (solvent-weld), $3.21 (2026-07-29). INTERFACE FLAG: the s60-adapter output is 2" MALE NPT and a spigot×slip bushing is glue-only, so it needs a 2" MPT×socket transition to mate (or swap to a 2"FNPT×1" reducer). Verify the tote-adapter interface at the bench.'),
    Part("ibc-flex-barb-m", '1" MNPT × 1" hose barb (Banjo HB100)', "plumbing-fittings",
         "water", 8, "ea", 1.79, 1.79, "US Plastic Corp", part_no="31527", url="https://www.usplastic.com/catalog/item.aspx?itemid=135135", spec='Tote-side barb — 1" MNPT threads onto the reduced tote-adapter port; flex hose slips onto the barb. Banjo HB100 glass-reinforced PP, 300 psi. $1.79 firm (2026-07-29).'),
    Part("ibc-flex-barb-f", '1" FNPT × 1" hose barb (Banjo)', "plumbing-fittings",
         "water", 8, "ea", 3.00, 3.00, "US Plastic Corp", part_no="31544", url="https://www.usplastic.com/catalog/item.aspx?itemid=135154", spec='Run-side barb — flex hose slips on; its 1" FNPT receives the pvc-adapter-1in (1" MNPT) that glues to the run. Banjo glass-reinforced PP. $3.00 firm (2026-07-29).'),
    Part("ibc-flex-clamp", '#20 stainless hose clamp (10-pack)', "fasteners-hardware",
         "water", 2, "10-pack", 18.52, 18.52, "Home Depot", part_no="IDL0410PK", url="https://www.homedepot.com/p/330548109", spec='2 clamps per flex jumper × 8 = 16 (2× 10-packs, 4 spare). Apollo 300-series SS #12 (½in–1¼in), external. $18.52/10-pack (2026-07-29). SIZE FLAG: verify the #12 (max 1¼in) closes over the 1¼in-OD tray-suction hose + barb — a #16 may be needed if it bottoms out.'),
    Part("blue-equalization-tie", '1" bulkhead tank-body fittings (Blue equalization cross-tie)', "plumbing-fittings",
         "water", 2, "ea", 12.62, 12.62, "US Plastic Corp", spec='Low tank-body penetration in each Blue tote (IBC-1 + IBC-2) for the 1" equalization cross-tie that self-balances the two Blue levels (run made from the 1" PVC stock). Confirmed firm $12.62 (2026-07-28); SKU 32194 (alternate listing itemid 65992).', part_no="32194", url="https://www.usplastic.com/catalog/item.aspx?itemid=32194"),
    Part("check-valve-1in", '1" NPT spring check valve (CV1 — X1 gravity fill)', "plumbing-fittings",
         "water", 1, "ea", 23.66, 23.66, "US Plastic Corp", spec='PVC body, EPDM seal, 1" FNPT × FNPT. Only CV-1 (X1 fill) remains — the Shurflo 2088 pumps have integral check valves, so CV-2/CV-3/CV-4 are redundant and dropped', part_no="31415", url="https://www.usplastic.com/catalog/item.aspx?itemid=31415"),
    Part("ribbon-support-beam", "Steel flat bar 25×3mm — ribbon support cross-brace", "steel-structural",
         "water", 2, "3ft bar", 17.57, 17.57, "McMaster-Carr", part_no="6775T37", url="https://www.mcmaster.com/6775T37-6775T373/", dims="25×3mm × 3 ft", spec="Low-carbon steel flat bar 25×3mm × 3 ft. Welded between the two right-walkway long bearers at 4 stations to carry the under-walkway pipe ribbon (four corridor↔pinhole lines); 4 braces ~300mm each = cut from 2× 3-ft bars (2 spare pieces).", panel="Corridor"),
    Part("ribbon-pipe-clip", "Cushioned pipe clip", "fasteners-hardware",
         "water", 16, "ea", 0.50, 0.50, "Amazon", part_no="B01HPE188Q", url="https://www.amazon.com/dp/B01HPE188Q", spec="Cushioned clamp for ½\" pipe (0.84\"/21mm OD); secures the four under-walkway ribbon lines to the support cross-braces (4 lines × 4 supports). Sold in 20-packs at $9.99 ($0.50/ea); one pack covers the 16 + spares.", panel="Corridor"),
    Part("ptfe-tape", "Thread seal tape (PTFE)", "adhesives-finishes",
         "water", 4, "roll", 2, 2, "Home Depot", spec='1/2" wide, 260" roll'),
    # — pipe (80–114) —
    Part("pvc-half", '1/2" PVC Sch-40 pipe', "plumbing-fittings",
         "water", 8, "stick", 4.81, 4.81, "Home Depot", part_no="30-05010HD",
         url="https://www.homedepot.com/p/319692959",
         spec="All pump-driven runs (~80 ft = 8× 10-ft sticks), PVC Sch-40 solvent-weld (IPEX potable-pressure). Matches pump port size."),
    Part("pvc-1in", '1" PVC Sch-40 pressure pipe', "plumbing-fittings",
         "water", 4, "stick", 8.65, 8.65, "Home Depot", part_no="22405", url="https://www.homedepot.com/p/319692953", spec="IPEX 1\"×10 ft white PVC Sch-40 POTABLE PRESSURE water pipe (model 22405); ~40 ft = 4× 10-ft sticks; filter inter-stage/outlet + IBC internal fill/drain manifold + X1 fill + equalization tie. Pressure-rated (2026-07-28). Re-count DONE 2026-07-29: 2→4 sticks — the IBC-zone 1\" internal fill/drain (§5 pipe table, ~39 ft total) was omitted from the old 20 ft estimate."),
    Part("pvc-three-quarter", '3/4" PVC Sch-40 pipe', "plumbing-fittings",
         "water", 2, "stick", 5.76, 5.76, "Home Depot", part_no="PVC-04007-0600", url="https://www.homedepot.com/p/100348472", spec="Spray bar run, PVC Sch-40 pressure pipe (plain end), 2× 10-ft sticks. $5.76/stick (sent $576 — read as a decimal typo; ¾\" pressure pipe sits between the ½\" $4.81 and 1\" $8.65). Re-count vs actual run length."),
    Part("braided-hose", '1/2" ID reinforced braided PVC hose', "plumbing-fittings",
         "water", 3, "length", 5.94, 5.94, "US Plastic Corp", spec="Pump flexible connections — a braided ½\" jumper on BOTH ports (suction + discharge) of all 5 pumps for vibration isolation (#29; P-04's suction is the 1\" tray-drain hose, so 9 ½\" jumpers). Short corridor jumpers cut from 3× 6ft lengths (~18 ft). De-couples each pump from the rigid PVC run so the solvent-weld joints can't fatigue-crack.", part_no="60703", url="https://www.usplastic.com/catalog/item.aspx?itemid=60703"),
    Part("pump-flex-barb", '1/2" barbed coupling (pump flex jumpers)', "plumbing-fittings",
         "water", 1, "20-pack", 12.48, 12.48, "Home Depot", part_no="318470443", url="https://www.homedepot.com/p/Rain-Bird-1-2-in-Barbed-Couplings-for-Drip-Tubing-Brown-20-Pack-BC50-20/318470443", spec="Rain Bird BC50-20 ½\" barbed coupling — 2 per braided pump-flex jumper × 9 = 18 (+2 spare) → 1× 20-pack. Barbs into the braided-hose ends (clamped). INTERFACE FLAG: the pump ½\" NPSM port takes a ½\" MNPT×barb adapter (drawn from the ½\" adapter allowance) — verify the barb-to-port interface at the bench. Firm $12.48/20-pack (Home Depot 2026-08-07)."),
    Part("pump-flex-clamp", '1/2"–1 1/4" SS hose clamp (pump flex jumpers)', "fasteners-hardware",
         "water", 2, "10-pack", 17.98, 17.98, "Home Depot", part_no="202262870", url="https://www.homedepot.com/p/Everbilt-1-2-1-1-4-in-Stainless-Steel-Hose-Clamp-10-Pack-671255E/202262870", spec="Everbilt 671255E ½–1¼\" SS hose clamp — 2 per braided pump-flex jumper × 9 = 18 (+2 spare) → 2× 10-pack. Secures each barb joint. Firm $17.98/10-pack (Home Depot 2026-08-07)."),
    # — electrical, wiring only (35) —
    Part("water-wire-14awg", "14 AWG duplex marine wire", "electrical-distribution",
         "water", 25, "ft", 0.68, 0.68, "Waytek Wire", part_no="MCB14-2", url="https://www.waytekwire.com/product/multi-conductor-marine-cable-mcb14-2", spec="Tinned-copper 2-conductor marine cable, cut to 25 ft (pump feed run)"),
    Part("water-powerpole", "Anderson Powerpole connectors 30A", "electrical-distribution",
         "water", 5, "pair", 1.30, 1.30, "Powerwerx", url="https://powerwerx.com/anderson-powerpole-connectors-30amp-unassembled", spec="Pump connections — one pair per pump (P-01..P-05). Sold in 10-pair packs at $12.99 (unassembled 30A); one pack covers the 5 pairs + spares."),
    Part("water-blade-fuses", "15A blade fuse", "electrical-distribution",
         "water", 1, "pack", 7.99, 7.99, "Amazon", part_no="B07WP5FWJJ", url="https://www.amazon.com/dp/B07WP5FWJJ", spec="15A ATC/ATO blade fuse, 100-pack — pump Circuit C single feed (all pumps) + spares."),
    # — processing consumables (241) —
    Part("ldpe-sheeting", "6-mil black LDPE sheeting", "tools-safety",
         "water", 1, "roll", 54.85, 54.85, "Home Depot", part_no="59803", url="https://www.homedepot.com/p/332821399", spec="Film-Gard 8 ft × 100 ft × 6-mil black poly (800 sq ft). Water splash/light-proof sheeting + the tray liners are cut from this same roll (tray-liner line retired 2026-07-27 — same material, ~10 liners/roll). Re-count area if the water use alone exceeds 800 sq ft."),
    Part("ph-meter", "Apera Instruments AI311 PH60 pH meter", "tools-safety",
         "water", 1, "ea", 79.76, 79.76, "Amazon", part_no="B01ENFOIQE",
         url="https://www.amazon.com/dp/B01ENFOIQE",
         spec="Waterproof, 0–16 range, ±0.01 accuracy"),
    Part("ph-calibration", "pH calibration solution set", "tools-safety",
         "water", 1, "set", 7.99, 7.99, "Amazon", part_no="B09DCP4HNH", url="https://www.amazon.com/dp/B09DCP4HNH", spec="BOJACK pH 4.00 + 6.86 + 9.18 buffer powder sachets — meter recalibration"),
    Part("citric-acid", "Citric acid, food grade, 6 lb", "tools-safety",
         "water", 2, "bag", 29.98, 29.98, "Amazon", part_no="B0F1CKRT7G", url="https://www.amazon.com/dp/B0F1CKRT7G", spec="pH adjustment (acidifier), 6 lb/bag"),
    Part("ghs-labels", "Chemical-resistant labels (GHS)", "tools-safety",
         "water", 1, "pack", 23.99, 23.99, "Amazon", part_no="B0BWFW5481", url="https://www.amazon.com/dp/B0BWFW5481", spec="GHS pre-printed pictogram secondary-container labels, perforated — for the 4 IBC totes (pictograms pre-printed; hand-write the reagent name). Amazon B0BWFW5481 $23.99 firm (2026-08-01)."),
    Part("nitrile-gloves", "Nitrile gloves, box of 100", "tools-safety",
         "water", 2, "box", 14.99, 14.99, "Amazon", part_no="B0CMZ5VXMS", url="https://www.amazon.com/dp/B0CMZ5VXMS", spec="TitanFlex nitrile, textured, box of 100 (size M/L)."),
    # — ibc-frame (ibc-stacking-report §9.1) — itemized, sums to costing frame (955–1,455) —
    Part("ibcf-rhs", "2×2×0.120in steel SHS (6 m bulk lengths)", "steel-structural",
         "ibc-frame", 4, "ea", 30, 45, "Metal Supermarkets", spec="Deep 4-leg box uprights (front + back pair) + top/bottom rings + front retaining bars + panel-mount rail (~24 m; front retaining bars DOUBLED to 8 (2/tote face, 50×20×3, ~8.8 m) after the EN 12195-1 loaded-transport case — ibc_frame_load.py; the 50×20×3 bars are a separate section from the 2×2 uprights, lumped here as bulk steel pending the Phase-D split). MATERIAL = 2×2×⅛in A500 square tube (US equiv, confirmed 2026-08-01). SOURCING: full 6m/20-24ft sticks minimize splices but ship only by freight — online cut-to-size shops cap at 96in (UPS max: AllMetals/InchOfMetal 96in, Speedy $7.27/ft cut-retail ≤90in). So the ~$120-180 (4×$30-45) est is realistic BULK full-length pricing (~$1.50-2.50/ft); firm it from a local steel-yard / MetalsDepot 24ft freight quote — NOT an online cut-to-size lookup (which overprices bulk ~3×)."),
    Part("ibcf-feet", "12mm steel plate, 150 × 150 cut", "steel-structural",
         "ibc-frame", 4, "ea", 5, 10, "Metal Supermarkets", spec="Deep-box upright floor flange feet (one per leg; front feet reach under the tray)"),
    Part("ibcf-hangers", "4mm folded plate", "steel-structural",
         "ibc-frame", 8, "ea", 7.5, 12.5, "local fab", spec="Simpson-style U-pocket wall joist hangers — 8 IDENTICAL 2-bolt hangers, one per front retaining bar (the pair uses identical hangers for fab simplicity — Alvin 2026-08-14). Each through-bolted (2× M12×65) to its own exterior 60×205×8 backing plate on the outside of the container side wall. Wall penetrations unchanged at 16 (8 hangers × 2 = old 4 × 4)."),
    Part("ibcf-dring", "Weld-on lashing ring, 1½\" ID", "fasteners-hardware",
         "ibc-frame", 8, "ea", 4.95, 4.95, "McMaster-Carr", part_no="3028T31",
         url="https://www.mcmaster.com/3028t31/",
         spec="Zinc-plated steel weld-on tie-down rings — 1½\" (38mm) inside × ½\" thick, 6,600 lb WLL; fillet-welded to the front retaining bars (4 per tier × 2 tiers). Integrated weld base — no separate mount plate. Ring (6,600 lb) exceeds the 2\"-strap-limited 3,333 lb (~1,512 kg) assembly WLL.",
         note="Confirm weld-base footprint fits the 50mm front-bar face at order; grind zinc plating back at the weld zone before welding."),
    Part("ibcf-strap", '2" (50mm) ratchet strap, 3,333 lb WLL', "fasteners-hardware",
         "ibc-frame", 4, "ea", 16.98, 16.98, "Home Depot", part_no="82827", url="https://www.homedepot.com/p/331257450", spec="Transport securing, over each stack (2 per stack × 2 stacks). Keeper 82827 heavy-duty 2\"×27ft, 3,333 lb (~1,512 kg) WLL / 10,000 lb break — width corrected 25mm→50mm (a 1\" strap can't hold the 1,100 kg the restraint needs). EN 12195-1 vert tie-down SF 3.1 loaded (ibc_frame_load.py)."),
    Part("ibcf-antislip-mat", "Certified anti-slip cargo matting (μ≥0.6)", "seals-gaskets",
         "ibc-frame", 4, "ea", 10, 20, "Uline / cargo-securing supplier",
         spec="Certified anti-slip rubber matting under each tote interface (4: 2 on the container floor + 2 on the lower-tote cage tops). Raises the sliding friction μ 0.2→0.6 per EN 12195-1 Annex B, cutting the front-bar forward-blocking demand ~3× (bar SF 1.59 bar-alone → 4.77 with mat; ibc_frame_load.py). Cut to the tote pallet footprint (~1.0×1.2 m). REQUIRES a certified/tested μ≥0.6 product (untested rubber caps at μ 0.2).",
         note="Firm the exact SKU + μ certificate at procurement (spec needs a tested EN 12195-1 Annex B μ≥0.6 rating)."),
    Part("ibcf-floor-anchor", "Self-drilling structural screw, #14×3¼″ winged, 410 SS", "fasteners-hardware",
         "ibc-frame", 16, "ea", 1.02, 1.02, "Fasteners Plus", "ASMC", part_no="F14C325FDC",
         url="https://www.fastenersplus.com/products/14-x-3-1-4-self-drilling-flat-head-screw-with-wings-410-stainless-steel-pkg-100",
         spec="4 deep-box flange feet × 4 each. Self-drills the 6mm foot plate + 28mm plywood and taps the ~4mm steel crossmember — LAND EACH FOOT OVER A CROSSMEMBER (~450mm centers). Wings ream the plate/ply clearance then snap off at the steel. 410 SS (martensitic — self-drills steel; 316 can't). The IBC dead load bears in compression on the floor; the screws resist sliding/uplift only. Through-bolt 316 + backing nut instead where a crossmember underside is reachable. $1.02/ea (100-pk)."),
    Part("bolt-m12x40", "M12×40 hex bolt, 18-8 SS", "fasteners-hardware",
         "ibc-frame", 24, "ea", 14.73 / 10, 14.73 / 10, "McMaster-Carr", part_no="92314A744",
         url="https://www.mcmaster.com/92314A744/",
         spec="Front-bar fasteners: 16 = corridor-end cleats (J2, 2 each × 8 bars — the open cleat needs 2 for anti-rotation) + 8 = wall-end vertical retention bolts (J7, 1 CENTERED per bar, down through the bar into the pocket seat; reverted from 2 on 2026-08-15 — redundancy not strength, the pocket + the fixed corridor cleat already stop the bar rotating, and 1 centered bolt clears the seat edges). Short grip → M12×40 fully threaded is correct. McMaster 92314A744: M12×1.75 × 40mm 18-8 stainless hex head screw — confirmed vs the eng-specs PDF (M12×1.75, 40mm, 18-8 SS). $14.73/pack of 10 firm (2026-08-01; 24 used → 3 packs). (Wall-hanger through-bolts are the M12×65 below.)"),
    Part("bolt-m12x65", "M12×65 hex through-bolt, Grade 8.8 zinc, partial-thread", "fasteners-hardware",
         "ibc-frame", 16, "ea", 15.95 / 10, 15.95 / 10, "McMaster-Carr", part_no="91280A728",
         url="https://www.mcmaster.com/91280A728/",
         spec="IBC wall-hanger through-bolts (2 each × 8 hangers = 16) — through the corrugated side wall to the exterior 60×205×8 backing plate (hex heads outside). Grip = 8mm plate + ~30mm corrugation + 4mm hanger flange ≈ 42–54mm → M12×65 partial-thread (the fully-threaded M12×40 could not span it). $15.95/pack of 10 → 2 packs for 16. Pad with 1–2 M12 flat washers if the actual corrugation is <30mm."),
    Part("nut-m12-plain", "M12 hex nut, plain", "fasteners-hardware",
         "ibc-frame", 16, "ea", 12.78 / 50, 12.78 / 50, "McMaster-Carr", part_no="90591A181", url="https://www.mcmaster.com/90591A181/", spec="Plain hex nut (inside the container) — M12×65 wall-hanger through-bolts (+ split lock washer). $12.78/pack of 50. Pitch M12×1.75 coarse — confirmed vs 90591A181 PDF 2026-07-29."),
    Part("washer-m12-flat", "M12 flat washer, zinc", "fasteners-hardware",
         "ibc-frame", 64, "ea", 9.71 / 100, 9.71 / 100, "McMaster-Carr", part_no="91166A290", url="https://www.mcmaster.com/91166a290/", spec="Flat washers, M12×65 wall-hanger bolts — 2 functional + 2 shim/bolt (shims pad the grip if corrugation <30mm). $9.71/pack of 100."),
    Part("washer-m12-split", "M12 split lock washer, zinc", "fasteners-hardware",
         "ibc-frame", 16, "ea", 11.97 / 100, 11.97 / 100, "McMaster-Carr", part_no="91202A246", url="https://www.mcmaster.com/91202A246/", spec="Split lock washer under each nut — M12×65 wall-hanger bolts (plain nut + split = locked). $11.97/pack of 100."),
    Part("ibcf-wall-backing", "Steel backing plate 60×205×8mm", "steel-structural",
         "ibc-frame", 8, "ea", 4, 7, "Metal Supermarkets", spec="Exterior wall backing plates — 8 identical, one per 2-bolt hanger — flat 60×205×8mm steel on the OUTSIDE of the container side wall (hex heads outside), 2× M12 holes; spreads the totes' transport thrust into the thin corrugated wall so the through-bolts can't pull through."),
    Part("ibcf-fabrication", "Welding / fabrication (frame assembly)", "fabrication-labor",
         "ibc-frame", 1, "lot", 688, 1018, "local fab", spec="~14–20 hrs labor (deep 4-leg box — the ring/back-upright welds sit at the upper end of the range)"),
    Part("ibcf-paint", "Primer + paint", "adhesives-finishes",
         "ibc-frame", 1, "lot", 30, 50, "Hardware store", spec="Anti-corrosion coating"),
    # — tray (processing-tray-and-spray-bar §6.1) — itemized, sums to costing tray (1,300–2,015) —
    Part("tray-ss-sheet", "304 SS sheet, 16-gauge (1.5mm), 2B mill finish", "stainless-sheet",
         "tray", 2, "ea", 305, 425, "Online Metals", spec="2,175 × 2,200mm panels. 2B mill finish (dropped from #4 brushed 2026-08-02 — the brush is a cosmetic upcharge, unneeded for a drain pan; ~15% est saving vs #4, keeps 16-ga rigidity + 304). Firm at a 2B quote. See tray-research.md."),
    Part("tray-fabrication", "Fabrication (cut, brake, weld, press sump)", "fabrication-labor",
         "tray", 1, "lot", 450, 850, "local sheet metal", spec="Two panels + a ~40mm center-seam lap (shingle-oriented downhill) + sump well"),
    Part("tray-hdpe-shim", "HDPE sheet, laminated to 1-1/4\" (slope shims)", "plastics-sheet",
         "tray", 1, "lot", 295.96, 295.96, "US Plastic Corp", part_no="46039+42591",
         url="https://www.usplastic.com/catalog/item.aspx?itemid=31840",
         spec="5 tapered slope shims (2\"×86.6\" = 50×2,200mm, 20→30mm taper). US Plastic max sheet = 1\", so LAMINATE two 24×48 sheets to 1-1/4\" then taper-cut (Option B: 1 mid-length butt splice/strip — fine for a floor-bonded compression shim). Combo = 3/4\" (US Plastic 46039 $177.58) + 1/2\" (42591 $118.38) = $295.96; the 3/4\"+1/2\" split keeps the taper cut inside the 3/4\" top layer so the glue line stays buried (the 1\"+1/4\" combo, same price, would cut through the seam). Taper-cut bundles with the tray fab."),
    Part("tray-loctite", "Loctite PL Premium construction adhesive", "adhesives-finishes",
         "tray", 2, "tube", 5.97, 5.97, "Home Depot", part_no="1390595", url="https://www.homedepot.com/p/319654545", spec="Shim-to-floor bond. Loctite PL Premium 10 oz, sold as a 2-pack ($11.94 → $5.97/tube)"),
    Part("tray-foot-valve", '1" brass foot valve with SS filter', "plumbing-fittings",
         "tray", 1, "ea", 14.23, 14.23, "misterworker", part_no="95953", url="https://www.misterworker.com/en-us/meclube/f1-brass-foot-valve-with-stainless-steel-filter/95953.html", spec="Sump pickup foot valve — Meclube F1 brass body + SS filter screen (misterworker 95953). $14.23 firm 2026-07-28."),
    Part("tray-suction-hose", '1" reinforced PVC suction hose, 25 ft', "plumbing-fittings",
         "tray", 1, "25ft coil", 65.65, 65.65, "Home Depot", part_no="6213100025", url="https://www.homedepot.com/p/310837595", spec="Sump pickup tube → P-04. HYDROMAXX 1\" clear flexible PVC suction/discharge hose, white reinforced helix; 25 ft coil — ~6 ft for the sump pickup + ~12 ft for the 8 IBC flex jumpers (18\" each, 2026-07-29 flexible-connection design) = ~18 ft used, ~7 ft spare. $65.65 firm 2026-07-28 (Home Depot stocks the 25 ft length)."),
    Part("tray-silicone-gasket", "Silicone gasket strip", "seals-gaskets",
         "tray", 1, "ea", 17, 25, "CountryMax (Aqueon)", spec="Silicone sealant bed in the center-seam lap joint (between the overlapped panels) + a top bead — the seam seal", part_no="015952", url="https://www.countrymax.com/aqueon-silicone-clear-aquarium-sealant-10oz-bottle/"),
    Part("bolt-m6-tray", "M6×1.0 × 16 hex bolt, 316 SS — tray center-seam lap joint", "fasteners-hardware",
         "tray", 12, "ea", 15.86 / 25, 15.86 / 25, "McMaster-Carr", part_no="93635A210", url="https://www.mcmaster.com/93635A210/", spec="Tray center-seam LAP-joint bolts (316 SS, wet zone) + M6 serrated flange nuts underneath. Through both overlapped 1.5mm panels + silicone bed. Grip ≈ 4mm → M6×16. Pitch M6×1.0 coarse. $15.86/pack of 25."),
    Part("nut-m6-flange", "M6×1.0 flange nut, serrated SS", "fasteners-hardware",
         "tray", 12, "ea", 4.71 / 100, 4.71 / 100, "McMaster-Carr", part_no="96194A101", url="https://www.mcmaster.com/96194A101/", spec="Serrated flange nut — tray panel bolts. Pitch M6×1.0 coarse — confirmed vs 96194A101 PDF 2026-07-29 (matches the mating bolt). $4.71/pack of 100."),
    # tray-liner RETIRED 2026-07-27 — the per-session containment liner is cut from the same
    # 6-mil black poly roll as ldpe-sheeting (Film-Gard 8 ft × 100 ft, ~10 liners/roll); a
    # separate $8 line double-counted the material. See ldpe-sheeting.
    # — spray (processing-tray-and-spray-bar §6.2) — itemized, sums to costing spray (287–375;
    # the $1/$3 report-subtotal rounding is absorbed into the AL-plate estimate so the block total
    # matches the canonical figure) —
    Part("spray-al-shs", '304 SS square tube 1½×1½×0.062in, single 17ft4in *', "steel-structural",
         "spray", 1, "ea", 183.00, 183.00, "Metals Depot",
         url="https://www.metalsdepot.com/stainless-steel-products/304-stainless-steel-square-tube",
         spec="1½×1½×0.062in (38×38×1.6mm) 304-SS SQUARE tube. SINGLE 17ft4in (5,283mm) length spans the full-width 4,399mm beam with margin — NO butt weld. The 1½in square depth (up from the old 40×25) holds the full-width span to ~11mm wet sag (L/395), flattened by ~12mm pre-camber; wall barely affects sag (self-weight-dominated). Metals Depot $183 confirmed 2026-08-03. (Metric 40×25/40×40 nominals are NOT stock — see the beam re-source TODO.)",
         note="* pre-camber ~12mm up at mid-span so it deflects flat under the wet load (SS beam ~1.9 kg/m; raw wet sag ~L/395)",
         dims="38×38×1.6", modeled_const="SPRAY_BAR_BEAM_W/SPRAY_BAR_BEAM_H"),
    Part("spray-al-plate", '6061-T6 AL plate 3/16" (5mm)', "aluminum",
         "spray", 1, "ea", 124.88, 124.88, "Metal Supermarkets", part_no="6061-sheet-12x20x0.1875", url="https://www.metalsupermarkets.com/product/aluminum-sheet-6061/", dims="12×20×3/16in", spec="Carriage plates + spacer blocks cut from one 12×20×3/16in sheet. Metal Supermarkets $124.88 firm (2026-08-01, cut-to-size retail); an online 6061 sheet supplier is likely cheaper — worth comparing at purchase (not yet quoted)."),
    Part("spray-ldpe-pipe", '3/4" LDPE irrigation poly pipe, 100 ft', "plumbing-fittings",
         "spray", 1, "100ft roll", 31.24, 31.24, "DripDepot", part_no="3552", url="https://www.dripdepot.com/polyethylene-tubing-size-three-quarter-inch-0-820-inch-inside-diameter-by-0-940-inch-od-length-100-feet", spec="Side-mounted spray manifold, clipped to the beam's inboard face. DripDepot 3552 ¾\" poly tubing (0.820\" ID × 0.940\" OD ≈ 20.8×23.9mm); 100 ft roll, ~15 ft used on the ~3.86m beam (balance spare). $31.24 firm 2026-07-28."),
    Part("spray-nozzles", "90° spray jets, barbed", "plumbing-fittings",
         "spray", 5, "10-pack", 3.47, 3.47, "Home Depot", part_no="110B", url="https://www.homedepot.com/p/302581648", spec="DIG 110B 90° spray jets, 10-pack ×5 = 50 (44 used, 6 spare); side-tapped into the poly manifold, spray straight down. Nozzles now run the FULL beam width (4,399mm) — 90° down-jets clear the overhead grate, so no reason to stop at the open zone. Pitch 100mm → 44 jets edge-to-edge — see processing-tray §3.9."),
    # spray-manifold + spray-feed-tube + spray-barbed-feed RETIRED 2026-07-28 (— Option 1,
    # single center feed). The ¾" side manifold (ID ~20mm) is hugely over-bored for 3.5 GPM feeding
    # 39 small jets — pressure is uniform end-to-end (~0.1 PSI drop over 3.86m) from a single center
    # feed, so the distribution manifold, the 7 ¼" feed tubes, and their barbed-tee taps aren't needed.
    # The ½" flex hose now feeds the manifold center through one inlet tee (spray-brass-barb).
    Part("spray-retainer-clips", 'Figure-8 end clamps, 3/4in poly', "fasteners-hardware",
         "spray", 1, "10-pack", 4.20, 4.20, "DripDepot", url="https://www.dripdepot.com/figure-8-tubing-end-clamp-size-three-quarter-inch",
         spec='Figure-8 fold-back end closures that crimp the 3/4" poly manifold ends shut — DripDepot 10-pack, $4.20 firm (2026-07-30).'),
    Part("spray-skate-wheel", "Acetal roller wheels ×4 (Delrin rod stock, Ø32×20, Ø10 bore)", "bearings-motion",
         "spray", 1, "1 ft rod", 10.97, 10.97, "McMaster-Carr", part_no="8576K23",
         url="https://www.mcmaster.com/8576K23/",
         spec='Solid acetal (Delrin), flat tread. Cut from 1-1/4" (31.75mm) Delrin rod into 4 × 20mm slugs; drill Ø10.5 running-clearance bore — the acetal plain bore IS the bearing (self-lubricating on the Ø10 304 SS axle; no ball bearing — the ferricyanide/citric wash rules steel bearings out). One 1 ft (305mm) rod yields all 4 (parting/facing waste). Light-duty ~2.6 kg/wheel wet; 2 per carriage, low-profile for grate clearance. OD Ø31.75 = Ø32 nominal (−0.25mm).',
         dims="Ø31.75 rod → 4× Ø32×20, Ø10.5 bore",
         note="One 1 ft (305mm) 1-1/4in Delrin rod (McMaster 8576K23) makes all 4 wheels; price verified 2026-07-12."),
    Part("spray-brass-barb", '1/2" PVC barbed tee (flex hose → manifold center feed)', "plumbing-fittings",
         "spray", 1, "5-pack", 2.85, 2.85, "DripDepot", part_no="1084", url="https://www.dripdepot.com/barb-tubing-tee-size-half-inch", spec="DripDepot 1084 ½\" PVC barbed tee (PVC), $0.57 ea × 5-pack = $2.85; the SINGLE center-feed inlet — ½\" flex hose → manifold center. 1 used. Firm 2026-07-28."),
    Part("spray-pool-pole", "Telescoping aluminum pool pole, 4–8 ft", "aluminum",
         "spray", 1, "ea", 15, 15, "Amazon", part_no="B0FHPSPD4T", url="https://www.amazon.com/dp/B0FHPSPD4T",
         spec="Standard pool skimmer handle — POOLPURE telescopic aluminum, 4–8 ft (B0FHPSPD4T, exact). ~$15–20 est — confirm."),
    Part("spray-braided-hose", '1/2" reinforced braided PVC hose, ~15 ft', "plumbing-fittings",
         "spray", 1, "10ft roll", 12.99, 12.99, "Home Depot", part_no="T12006003", url="https://www.homedepot.com/p/304185193",
         spec='BV-05b → beam feed (~4 m coiled). UDP 1/2"ID×3/4"OD clear braided vinyl (T12006003), $12.99/10ft firm (2026-07-30). 10 ft ≈ 3 m — a 4 m coiled run may need a 2nd roll.'),
    Part("spray-axle-pin", "10mm × 60mm 304 SS axle pin (4-pack)", "fasteners-hardware",
         "spray", 1, "pack", 5, 5, "Amazon", part_no="B0816MQ5T6",
         url="https://www.amazon.com/uxcell-Single-Hole-Clevis-Pins/dp/B0816MQ5T6", spec="Wheel axle pins — uxcell 10×60mm 304 SS clevis pins, 4-pack (B0816MQ5T6, exact: 14mm head, 3.2mm cotter hole)."),
    Part("spray-saddle-clamp", "Axle saddle clamps ×8 (304 SS flat-bar stock)", "fasteners-hardware",
         "spray", 1, "2 ft bar", 9.84, 9.84, "McMaster-Carr", part_no="8992K794",
         url="https://www.mcmaster.com/8992K794/", spec='Axle retention — formed from 1/8" (3.18mm) × 3/4" (19mm) 304 SS flat bar, wrapped over the Ø10 axle (1mm cradle clearance) with two ~12mm feet bolted up through the carriage plate (2× Ø5.5 M5). ~48mm developed per saddle; all 8 cut from one 2 ft (610mm) length of flat bar. A stamped conduit saddle clamp is only ~0.5mm — too thin for a rolling-carriage axle retainer. Alt: 304 SS + EPDM Adel loop clamp ~3/8–7/16\" ID.', dims="3.18×19 flat bar, ~48mm dev/pc", note="One 2 ft (610mm) 1/8x3/4 304 flat bar (McMaster 8992K794) yields all 8 saddles; formed + drilled (waste per part); price verified 2026-07-12."),
    Part("bolt-m6x20", "M6×1.0 × 20 hex bolt, 304 SS (A2-70)", "fasteners-hardware",
         "spray", 16, "ea", 17.77 / 50, 17.77 / 50, "McMaster-Carr", part_no="91287A137", url="https://www.mcmaster.com/91287A137/", spec="Carriage plate, beam clamp, saddle fasteners (M6×1.0). 304 SS A2-70 — upgraded from zinc 2026-08-13 (the spray is in the WET cyanotype zone; 304 is corrosion-adequate — the wash has no chloride → 316 unneeded; A2-70 700 MPa ample for the clamp load). McMaster 91287A137 $17.77/pack of 50 firm (Alvin 2026-08-13)."),
    Part("nut-m6-nyloc", "M6×1.0 hex nut, nyloc SS", "fasteners-hardware",
         "spray", 16, "ea", 4.77 / 100, 4.77 / 100, "McMaster-Carr", part_no="90576A115", url="https://www.mcmaster.com/90576A115/", spec="Nyloc nut — M6×20 spray fasteners. Pitch M6×1.0 coarse — confirmed vs 90576A115 PDF 2026-07-29 (matches the M6×1.0 bolt). $4.77/pack of 100."),
    Part("spray-self-tap", "Self-tapping SS screws (8-pack)", "fasteners-hardware",
         "spray", 4, "ea", 0.44, 0.64, "Lowe's (Hillman)", part_no="3691866",
         url="https://www.lowes.com/pd/Hillman-25-Count-10-x-1-in-Stainless-Steel-Self-Drilling-Interior-Exterior-Sheet-Metal-Screws/3691866",
         spec="Ball-joint flange to beam top wall. #10×1 SS self-drill, 25-pk ~$11–16 (per-unit est)."),
    Part("spray-ball-joint", "M12 rod-end bearing (uxcell SA12TK, 4-pack)", "bearings-motion",
         "spray", 1, "4-pack", 19.59, 19.59, "Amazon", part_no="B0C7N16RQ9", url="https://www.amazon.com/uxcell-SA12TK-Bearing-M12x1-75-Self-Lubricating/dp/B0C7N16RQ9",
         spec="Multi-axis spray-arm articulation — uxcell SA12TK male rod-end bearing, M12×1.75 self-lubricating (B0C7N16RQ9), $19.59/4-pack firm (2026-07-30). Rod-end bearing (upgrade from the go-kart tie-rod candidate); 4-pack = 1 used + spares."),
    Part("spray-beam-clamp", "SS beam clamp plates (4, cut from 1× 2 ft 304 flat bar)", "fasteners-hardware",
         "spray", 1, "2 ft bar", 35.33, 35.33, "McMaster-Carr", part_no="8992K512",
         url="https://www.mcmaster.com/8992K512/",
         spec="2 top + 2 bottom beam-clamp plates (1/4\"/6.35mm 304, beam-to-carriage sandwich, countersunk underside bolts), cut from one 2 ft flat bar (8992K512); + 4× 25mm 6061 AL spacers (from offcut). 1/4\" chosen for stiffness (bolts grip the beam, not bend the plates). Stack-up: plates thicken OUTWARD (wheel/carriage/beam fixed) — bottom plate Z22.6–29 (2.6mm clear of the Z20 roll surface), top plate Z54–60.4."),
    Part("spray-arm-tube", "6061-T6 AL round tube 25mm OD × 2mm wall, 8 ft", "aluminum",
         "spray", 1, "ea", 64.03, 64.03, "McMaster-Carr", part_no="9056K36", url="https://www.mcmaster.com/9056K36-9056K122/",
         spec="Arm tube — slit ~30mm at the bottom for the clamp-collar pinch onto the adapter's Ø21 spigot. McMaster 9056K36 $64.03 (firm 2026-07-25), 8 ft stock (only the ~500mm arm is used; balance is spare) — the old 500mm cut line was too short to order.", note="2026-07-25: specified the 8ft stock length (min order) — the 500mm cut was too short a line item."),
    Part("spray-arm-adapter", "Arm-to-stud adapter, turned 6061-T6 AL (anodized)", "aluminum",
         "spray", 1, "ea", 12, 18, "Local machine shop", spec="Reducer coupling: M12×1.75 tapped bore (onto the ball-joint stud, locked with an M12 jam nut) → Ø21 male spigot the slit arm tube slips over. ~40mm long; anodized to match the AL tube (galvanic). Turned one-off / est."),
    Part("spray-arm-jamnut", "M12×1.75 jam nut, SS", "fasteners-hardware",
         "spray", 1, "ea", 8.38 / 10, 8.38 / 10, "McMaster-Carr", spec="Locks the arm adapter on the ball-joint M12 stud. McMaster 90381A102: 18-8 SS thin-profile hex nut, M12×1.75 coarse — confirmed vs the 90381A102 PDF 2026-07-29 (matches the stud + arm-adapter bore). $8.38/pack of 10.", part_no="90381A102", url="https://www.mcmaster.com/90381A102/"),
    Part("spray-arm-collar", "Clamp-style shaft collar, 25mm/1\" bore, SS", "fasteners-hardware",
         "spray", 1, "ea", 28, 33, "Ruland", spec="Over the slit arm-tube bottom; its integral clamp screw squeezes the Ø25×2 tube onto the adapter's Ø21 spigot — rotational adjust + lift-off for transport. Replaces the loose M6 pinch bolt. Confirm SKU/bore/price at order.", part_no="CL-16-ST", url="https://www.ruland.com/cl-16-st.html"),
    Part("spray-zip-ties", "Nylon zip ties, 8in (200mm)", "fasteners-hardware",
         "spray", 1, "100-pack", 2.68, 2.68, "Harbor Freight", part_no="34635", url="https://www.harborfreight.com/8-inch-black-cable-ties-pack-of-100-34635.html", spec="Hose to arm tube — 8in UV-resistant black nylon, 100-pack (6 used + spares). Harbor Freight $2.68 firm (2026-08-01)."),

    # ═══ electrical (§6) — fully itemized from master §6; point estimates summing to ~$2,345
    # (reconciles to EXPECTED['power'] $2,350 within tolerance). Demonstrates the procurement-real
    # granularity the by-type/by-supplier BOM needs. ═══
    # — Solar & battery (primary power), ≈$1,329 —
    Part("solar-panel-200w", "Solar panel, 200W monocrystalline 12V (Renogy RSP200D)", "electrical-power",
         "electrical", 3, "ea", 169.99, 169.99, "Off Grid Stores", "Renogy", part_no="RSP200D-US",
         url="https://offgridstores.com/products/renogy-200-watt-12-volt-monocrystalline-solar-panel"),
    Part("mppt-100-50", "Victron SmartSolar MPPT 100/50 charge controller", "electrical-power",
         "electrical", 1, "ea", 193.80, 193.80, "Powerwerx", "altE Store", part_no="SCC110050210",
         url="https://powerwerx.com/victron-scc110050210-smartsolar-mppt-10050"),
    Part("lifepo4-100ah", "LiFePO4 battery, 100Ah 12V (Renogy Core Series)", "electrical-power",
         "electrical", 1, "ea", 306.46, 306.46, "Off Grid Stores", "Renogy", part_no="RBT12100LFP-US",
         url="https://offgridstores.com/products/renogy-12v-100ah-core-series-deep-cycle-lithium-iron-phosphate-battery",
         dims="260×169×211", datasheet="Renogy 12V 100Ah Core Series", modeled_const="BA_W/BA_D/BA_H",
         audit_status="✅ FIXED", note="Core Series — side busbar terminals (simpler vertical stacking), 10.5 kg; provisioned for optional 2nd pack (+$306)"),
    Part("shore-charger", "Victron Blue Smart IP65 12/15 shore backup charger", "electrical-power",
         "electrical", 1, "ea", 152.15, 152.15, "Inverter Service Center", "Powerwerx", part_no="BPC121531104R",
         url="https://inverterservicecenter.com/blue-smart-ip65-charger-12-15-1-victron-bpc121531104r"),
    Part("nema-inlet", "NEMA 5-15R weatherproof inlet (flush power panel)", "electrical-distribution",
         "electrical", 1, "ea", 9.98, 9.98, "Amazon", part_no="B0CLDC8X5J", url="https://www.amazon.com/dp/B0CLDC8X5J"),
    Part("cooler-ac-outlet", "Cooler AC outlet — WR duplex receptacle + in-use cover", "electrical-distribution",
         "electrical", 1, "set", 24.51, 24.51, "Home Depot", part_no="W5320-T0W", url="https://www.homedepot.com/p/202078774",
         spec="Circuit-E cooler outlet on the ep-ext-enclosure — the cooler plugs in here. Leviton W5320-T0W 15A/125V tamper+weather-resistant duplex receptacle ($5.43) + Leviton 5981-UCL raintight while-in-use device-mount cover ($19.08) = $24.51. NOT a GFCI receptacle — the GFCI is upstream at the Victron inverter. Mounts through a 1-gang cutout in the enclosure wall (device-mount cover, no box needed)."),
    Part("solar-mount-frame", "Solar panel adjustable tilt mount set (per panel)", "electrical-power",
         "electrical", 3, "ea", 35.99, 35.99, "Amazon", "Renogy", part_no="RNG-MTS-TMB-G1-US",
         url="https://www.amazon.com/Renogy-Adjustable-Solar-Panel-Brackets/dp/B07CSKFWK7", spec="One adjustable tilt-bracket set per 200W panel (4 fixed + 2 tilt L-brackets, rated to 220W) — 3 sets for the 3-panel array."),
    Part("pv-cable-10awg", "PV cable 10 AWG + MC4 connectors (11 ft extension pair)", "electrical-distribution",
         "electrical", 1, "lot", 30, 30, "Signature Solar", part_no="1534034", url="https://signaturesolar.com/11ft-10awg-pv-wire-extension-black-red/",
         spec="Signature Solar 1534034 — 11 ft 10 AWG PV wire extension (black + red), male/female MC4 both ends, 30A, outdoor/waterproof (Pacific Coast Wire). Array → MPPT. $30 firm (2026-07-30)."),
    Part("pv-array-disconnect", "PV array disconnect — Blue Sea 6006 DC battery switch (NEC 690.13)",
         "electrical-power", "electrical", 1, "ea", 33.60, 33.60, "Waytek Wire", part_no="6006",
         url="https://www.waytekwire.com/product/blue-sea-systems-6006-m-series-battery-switch",
         spec="Blue Sea 6006 m-Series single-circuit ON/OFF DC battery switch — load-break disconnect on the PV array + (array → MPPT). 300A / 48V DC (≫ our ~22V Voc / ~30A Isc = ~38A required; the array is 3×200W in PARALLEL, 12V nominal, not a high-V string). 2× M10 tin-copper studs (ring lugs), 55×55mm face × 64mm deep, isolating cover with snap-off sides = wire access any direction. Mounts on the EP backboard's IP65 disconnect cluster (with the main disconnect + master pump switch) — the array cables run from the power-panel-box MC4 bulkheads to here."),
    # power-panel-plate + power-panel-gasket RETIRED 2026-07-28 — the external power panel is now a proper
    # IP-rated McMaster enclosure (ep-ext-enclosure) with its own sealed lid + gasket, superseding the
    # flush aluminum face plate + neoprene gasket. See ep-ext-enclosure.
    # power-panel-plate/gasket/frame + the McMaster ep-ext-enclosure + power-panel-wall-gland all RETIRED
    # 2026-07-28 — final design is a FABRICATED flanged penetration box (below): the 4 weatherproof
    # exterior interfaces (MC4/inlet/outlet/E-stop) surface-mount + seal to its front face and are exposed
    # (all IP65-67), the box opens to the container interior for wiring, and its flange seals to the ribbed
    # wall with flashing + silicone. No IP enclosure needed (components are already weatherproof); the
    # non-weatherproof gear (Blue Sea disconnect + terminals) lives on the EP backboard's IP65 area instead.
    Part("power-panel-box", "Fabricated flanged wall-penetration box (front face + flange)", "steel-structural",
         "electrical", 1, "lot", 60, 100, "Local fab",
         spec="Sheet-metal flanged box spanning the corrugations: front face (exterior) cut for the 4 weatherproof interfaces — 3× MC4 bulkhead pairs, shore NEMA inlet, cooler outlet (1-gang), 22mm E-stop — each surface-mounted + gasket-sealed; shallow surround; exterior flange; OPEN to the container interior for wiring. Front face + gasketed opaque components + flashed flange = light-tight (pinhole camera). Local fab (cut/brake/weld + cutouts)."),
    Part("power-panel-flashing", "Ribbed-wall flashing + silicone (power-panel box seal)", "seals-gaskets",
         "electrical", 1, "lot", 15, 30, "Hardware store",
         spec="Formed flashing to bridge the corrugation crests around the box flange + UV/weather silicone bead — seals the exterior box-to-wall interface WATER-tight AND LIGHT-tight (any perimeter gap = light into the container). Applied over the ribbed wall the box flange can't seat flat against."),
    Part("bolt-m6x20", "M6×1.0 × 20 hex bolt, 304 SS (A2-70)", "fasteners-hardware",
         "electrical", 4, "ea", 17.77 / 50, 17.77 / 50, "McMaster-Carr", part_no="91287A137", url="https://www.mcmaster.com/91287A137/", spec="Power-panel bolt: face plate 3mm + gasket 3mm into the welded raised frame's M6 weld-nut (~12mm grip → M6×20). 304 SS A2-70 — upgraded from zinc 2026-08-13 (the panel face is exterior/weather-facing; 304 is adequate, no chloride). McMaster 91287A137 $17.77/pack of 50 firm (Alvin 2026-08-13)."),
    Part("nut-m6-plain", "M6×1.0 hex nut, plain SS", "fasteners-hardware",
         "electrical", 4, "ea", 3.42 / 100, 3.42 / 100, "McMaster-Carr", part_no="90591A151", url="https://www.mcmaster.com/90591A151/", spec="Plain hex nut — panel-mount bolts. Pitch M6×1.0 coarse — confirmed vs 90591A151 PDF 2026-07-29. $3.42/pack of 100."),
    Part("washer-m6-flat", "M6 flat washer, SS", "fasteners-hardware",
         "electrical", 8, "ea", 4.51 / 100, 4.51 / 100, "McMaster-Carr", part_no="91455A120", url="https://www.mcmaster.com/91455a120/", spec="Flat washers (2/bolt) — panel mount. $4.51/pack of 100."),
    Part("mc4-bulkhead", "MC4 bulkhead passthrough pairs, IP67 panel-mount", "electrical-distribution",
         "electrical", 3, "pair", 2.99, 2.99, "Powerwerx", part_no="MC4-Bulkhead", url="https://powerwerx.com/mc4-bulkhead-passthrough-solar-input",
         spec="Powerwerx MC4 bulkhead passthrough (+/− pair), threaded panel-mount into the ep-ext-enclosure wall — one pair per panel (3× 200W parallel array enters on 3 separate MC4 pairs, each ~15A, within the 30A MC4 rating; combined inside on the disconnect/busbar, NOT on one over-rated MC4). Passthrough = MC4 both sides, so add short MC4→ring-lug pigtails inside to land on the Blue Sea studs."),
    # — Distribution & wiring, ≈$1,016 —
    Part("fuse-block-5026", "Blue Sea 5026 fuse block, 12-circuit ST-blade", "electrical-distribution",
         "electrical", 1, "ea", 59.40, 59.40, "Off Grid Stores", "West Marine", part_no="5026",
         url="https://offgridstores.com/products/blue-sea-5026-st-blade-fuse-block-w-cover-12-circuit-w-negative-bus"),
    Part("mrbf-200a", "200A main fuse (Blue Sea 5187) + single MRBF holder (5191)", "electrical-distribution",
         "electrical", 1, "ea", 45.57, 45.57, "Blue Sea", "Defender Marine", part_no="5187+5191",
         url="https://defender.com/en_us/blue-sea-systems-single-mrbf-terminal-fuse-block-5191", spec="Battery main: one 200A MRBF terminal fuse (5187, $16.58) in a single MRBF terminal block (5191, $28.99, mounts on the 3/8\" battery post). ABYC E-11."),
    Part("battery-disconnect", "Battery main disconnect — Blue Sea 6006 m-Series (300A)", "electrical-distribution",
         "electrical", 1, "ea", 36.26, 36.26, "Off Grid Stores", "West Marine", part_no="6006",
         url="https://offgridstores.com/products/blue-sea-6006-m-series-mini-battery-switch-single-circuit-on-off-red"),
    Part("ml-rbs-contactor", "Remote battery switch — Blue Sea ML-RBS 500A magnetic-latch (E-stop trip)",
         "electrical-distribution", "electrical", 1, "ea", 263.84, 263.84, "Inverter Supply", "Powerwerx", part_no="7700",
         url="https://www.invertersupply.com/index.php?main_page=product_info&products_id=5288"),
    Part("estop-external", "External emergency cut-off — red mushroom switch", "electrical-distribution",
         "electrical", 1, "ea", 12.74, 12.74, "Harfington", part_no="a19061100ux1510", url="https://www.harfington.com/products/p-1071142",
         spec="uxcell a19061100ux1510 red mushroom E-stop switch, $12.74 (Harfington, firm 2026-07-25). Switch element ONLY — mounted in the weatherproof control-station box below (estop-external-enclosure).",
         note="2026-07-25: 'just the switch' — houses in the estop-external-enclosure control station box."),
    # estop-external-enclosure RETIRED 2026-07-28 — the exterior E-stop is now a 22mm button mounted directly
    # on the ep-ext-enclosure door, so its own separate control-station box is redundant.
    Part("estop-internal", "Interior emergency cut-off — red mushroom switch (paralleled to exterior)",
         "electrical-distribution", "electrical", 1, "ea", 12.74, 12.74, "Harfington", part_no="a19061100ux1510", url="https://www.harfington.com/products/p-1071142",
         spec="uxcell a19061100ux1510 red mushroom E-stop switch, $12.74 (Harfington, firm 2026-07-25). Switch only — interior panel-mounted.",
         note="2026-07-25: 'just the switch'."),
    Part("mppt-charge-fuse", "MPPT charge-line fuse — 60A ANL + holder", "electrical-distribution",
         "electrical", 1, "ea", 43.38, 43.38, "Powerwerx", "Amazon", part_no="5005-BSS", url="https://powerwerx.com/blue-sea-5005-anl-fuse-block-cover",
         spec="Blue Sea 5005 ANL fuse block + cover ($36.39, Powerwerx 5005-BSS) + BOJACK ANL-60 fuse 3-pack ($6.99, Amazon B08JPH6Q5H — 1 used, 2 spare). Protects the MPPT->battery 6 AWG charge lead close to the battery (§7.3). $43.38 firm (2026-07-31)."),
    Part("shore-output-fuse", "Shore-charger output fuse — 20A inline (sealed holder + fuse)", "electrical-distribution",
         "electrical", 1, "ea", 7.30, 7.30, "Waytek Wire", part_no="46047", url="https://www.waytekwire.com/product/sealed-ato-atc-fuse-holder-assembly-46047",
         spec="Waytek 46047 sealed (waterproof) in-line ATO/ATC fuse-holder assembly ($7.13) + Waytek 47020 20A ATOF blade fuse (Littelfuse 0287020, $0.17). $7.30 firm (2026-07-30). On the shore-charger output lead."),
    Part("battery-terminal-covers", "Battery terminal covers (pair), insulating boots", "electrical-distribution",
         "electrical", 1, "pair", 2.88, 2.88, "Waytek Wire", part_no="23501", url="https://www.waytekwire.com/product/23501-straight-in-battery",
         spec="Waytek 23501 (VTE 415N6V02) red + 23500 (VTE 415N6V14) black straight-in battery boots, 6-4 Ga — insulate the +/− post terminals. $1.44 ea × 2 = $2.88 firm (2026-07-30). Black mate: waytekwire.com/product/23500-straight-in-battery-boot."),
    Part("wet-zone-connectors", "Sealed wet-zone connectors — 6× Deutsch DT 2-pin pairs (pump circuits)",
         "electrical-distribution", "electrical", 1, "lot", 27.42, 27.42, "buyDeutsch", part_no="DT06-2S",
         url="https://www.buydeutsch.com/collections/dt-series/products/dt06-2s",
         spec="6 sealed DT 2-pin pairs — one per Shurflo 2088 pump (P-01..P-05, Circuit C) + 1 spare, so each pump unplugs in the wet zone. Per pair: DT04-2P receptacle ($1.21) + W2P ($0.18) + DT06-2S plug ($1.39) + W2S ($0.21) + 2x 0460-202-16141 pins ($0.25) + 2x 0462-201-16141 sockets ($0.54) = $4.57; x6 = $27.42 firm (2026-07-31, individual buyDeutsch items — DSC-KT1 assortment/tool kit $198 is overkill). Separate from deutsch-dt-2pin-elec (exterior) + deutsch-dt-2pin (Fan B)."),
    Part("pump-switches", "Master pump switch (Circuit C) — IP67 sealed rocker/disconnect 12V 16A", "electrical-distribution",
         "electrical", 1, "ea", 7.99, 7.99, "Amazon", "Waytek Wire", spec="One manual cutoff for the whole pump circuit, mounted on the EP (per-pump switches removed; each Shurflo runs on its internal pressure switch)", part_no="B0GF2ZBD1W", url="https://www.amazon.com/dp/B0GF2ZBD1W"),
    Part("pump-dist-block", "Pump distribution block — 12V DC common busbar, 10-gang", "electrical-distribution",
         "electrical", 1, "ea", 15, 15, "Blue Sea", "Amazon", part_no="2300", url="https://www.bluesea.com/products/2300",
         spec="Blue Sea 2300 Common 150A BusBar, 10-gang w/ cover — the Circuit-C pump +/− distribution on the corridor panel back (§7.3): switched 14 AWG feed in, 16 AWG branches to each column pump. Price $15 est — CONFIRM: the 2300 typically runs ~$28-32, so this line may rise ~$15."),
    Part("dielectric-grease", "Dielectric grease, marine-grade (terminal protection)", "adhesives-finishes",
         "electrical", 1, "ea", 8.99, 8.99, "Amazon", part_no="B0D6R543V2",
         url="https://www.amazon.com/dp/B0D6R543V2",
         spec="BTAS marine-grade dielectric grease — connector/terminal corrosion protection. $8.99 firm (2026-07-31)."),
    # tinned-marine-wire RETIRED 2026-07-30 → folded into the per-gauge wire-<ga>awg-<color> spools
    # (all tinned hook-up; its $30 is absorbed into the $110 re-distributed wire budget).
    Part("cable-grommets", "Cable grommets / glands — steel-shell penetrations", "electrical-distribution",
         "electrical", 1, "lot", 27.86, 27.86, "Amazon", part_no="B09K5GNFHF",
         url="https://www.amazon.com/YUFANNET-Assortment-Grommets-Automotive-Electrical/dp/B09K5GNFHF",
         spec="200-pc rubber grommet assortment (8 sizes, B09K5GNFHF $8.88) to protect wires through drilled steel + a strain-relief NPT cable-gland kit (B08R84YJ7X, nylon IP68, $18.98) for sealed wall/enclosure entries. $27.86 both kits."),
    Part("bonding-kit", "Equipotential bonding kit — 6 AWG jumper + ring lugs", "electrical-distribution",
         "electrical", 1, "ea", 95.79, 95.79, "Grainger", part_no="21WJ56",
         url="https://www.grainger.com/product/PANDUIT-Grounding-Jumper-Wire-Kit-21WJ56",
         spec="Panduit grounding jumper kit — 6 AWG, 60in, 45deg bent ring lugs (factory irreversible-compression terminals). Equipotential bond: container body -> battery-neg busbar (§7.6). $95.79 firm (2026-07-31)."),
    Part("ep-backing-panel", "EP plywood backing panel (18mm, ~700×2000mm)", "timber-ply",
         "electrical", 1, "4'×8' sheet", 68.98, 68.98, "Home Depot", part_no="454559", url="https://www.homedepot.com/p/203414066",
         spec='18mm SANDEPLY Sande hardwood plywood, full 4\'×8\' sheet, cut to the ~700×2000mm backboard (fits with margin — 1220×2440mm stock) — '
              'the wall-mounted surface every EP component fixes to (MPPT on its forward sub-panel, battery bank, '
              'inverter, main + PV disconnects); the DC-distribution terminals (fuse block + busbars) '
              'sit in a small IP65 enclosure bolted to it. Add DIN rail + standoffs for the DIN gear. '
              '(Not fire-rated — acceptable for a small 12V DC system; seal/paint before mounting.)'),
    Part("ip65-enclosure", "IP65 enclosure 213×213×133mm (fuse block + busbars, on the plywood)", "electrical-distribution",
         "electrical", 1, "ea", 46.93, 46.93, "Polycase", "Amazon", part_no="ZH-080804", url="https://www.polycase.com/zh-080804",
         spec='Weatherproof IP65 box bolted to the plywood backboard, sealing the DC-distribution '
              'terminals (Blue Sea 5026 fuse block + the +/- busbars + charge-line fuse) against '
              'splash/dust. Its back panel is the plywood; the disconnect knob and cable glands pass '
              'through the face.'),
    # — Circuit wiring: tinned hook-up primary, per-gauge red+black 100ft spools (§7.3 conductor
    # schedule). 2026-07-30: retired the wiring-kit + tinned-marine-wire catch-alls → per-gauge
    # SKUs, ALL tinned hook-up (Waytek has no marine <14AWG anyway). The $110
    # catch-all budget is re-distributed by run length (cost-neutral); confirm each spool price at order.
    Part("wire-12awg-red", "12 AWG tinned hook-up wire, red — 100ft (Circuit F)", "electrical-distribution",
         "electrical", 1, "spool", 13, 13, "Waytek Wire", part_no="WRT12-2", url="https://www.waytekwire.com/product/wrt12-2-hook-up-wire-tinned-copper",
         spec="Circuit F film-plane actuators (~6m). Tinned copper UL-1015. WRT12-2 (red, pattern-inferred); confirm SKU/price at order."),
    Part("wire-12awg-blk", "12 AWG tinned hook-up wire, black — 100ft (Circuit F)", "electrical-distribution",
         "electrical", 1, "spool", 13, 13, "Waytek Wire", part_no="WRT12-0", url="https://www.waytekwire.com/product/wrt12-0-hook-up-wire-tinned-copper",
         spec="Circuit F return (~6m). Tinned copper UL-1015. WRT12-0 (black, pattern-inferred); confirm SKU/price at order."),
    Part("wire-14awg-red", "14 AWG tinned hook-up wire, red — 100ft (Circuit C feed / AC)", "electrical-distribution",
         "electrical", 1, "spool", 14, 14, "Waytek Wire", part_no="WRT14-2", url="https://www.waytekwire.com/product/wrt14-2-hook-up-wire-tinned-copper",
         spec="Circuit C pump feed + inverter AC out + Circuit G white-LED feed (~14m; 14 AWG for the ~6.3A COB load). Tinned copper UL-1015. WRT14-2 (red, confirmed); price est — confirm at order."),
    Part("wire-14awg-blk", "14 AWG tinned hook-up wire, black — 100ft (Circuit C feed / AC)", "electrical-distribution",
         "electrical", 1, "spool", 14, 14, "Waytek Wire", part_no="WRT14-0", url="https://www.waytekwire.com/product/wrt14-0-hook-up-wire-tinned-copper",
         spec="Circuit C + Circuit G returns (~14m). Tinned copper UL-1015. WRT14-0 (black, pattern-inferred); confirm SKU/price at order."),
    Part("wire-16awg-red", "16 AWG tinned hook-up wire, red — 100ft (Circuits A/B/G + branches)", "electrical-distribution",
         "electrical", 1, "spool", 16, 16, "Waytek Wire", part_no="WRT16-2", url="https://www.waytekwire.com/product/wrt16-2-hook-up-wire-tinned-copper",
         spec="Circuits A/B fans + C pump branches (~18m; Circuit G moved to 14 AWG for the COB load). Tinned copper UL-1015. WRT16-2 (red, confirmed); price est — confirm at order."),
    Part("wire-16awg-blk", "16 AWG tinned hook-up wire, black — 100ft (Circuits A/B/G + branches)", "electrical-distribution",
         "electrical", 1, "spool", 16, 16, "Waytek Wire", part_no="WRT16-0", url="https://www.waytekwire.com/product/wrt16-0-hook-up-wire-tinned-copper",
         spec="Circuits A/B/C-branch returns (~18m). Tinned copper UL-1015. WRT16-0 (black, confirmed); price est — confirm at order."),
    Part("wire-18awg-red", "18 AWG tinned hook-up wire, red — 100ft (Circuit D + E-stop)", "electrical-distribution",
         "electrical", 1, "spool", 12, 12, "Waytek Wire", part_no="WQT18-2", url="https://www.waytekwire.com/product/wqt18-2-hook-up-wire-tinned-copper",
         spec="Circuit D safelight + E-stop loop (~20m). Tinned copper UL-1007. WQT18-2 (red, confirmed); price est — confirm at order."),
    Part("wire-18awg-blk", "18 AWG tinned hook-up wire, black — 100ft (Circuit D + E-stop)", "electrical-distribution",
         "electrical", 1, "spool", 12, 12, "Waytek Wire", part_no="WQT18-0", url="https://www.waytekwire.com/product/wqt18-0-hook-up-wire-tinned-copper",
         spec="Circuit D + E-stop returns (~20m). Tinned copper UL-1007. WQT18-0 (black, confirmed); price est — confirm at order."),
    Part("battery-cable-2-0", "2/0 AWG battery cable, 3ft (battery–fuse–busbar)", "electrical-distribution",
         "electrical", 1, "lot", 25.99, 25.99, "Amazon", part_no="B0B3HD7CWP", url="https://www.amazon.com/dp/B0B3HD7CWP"),
    Part("anderson-powerpole", "Anderson Powerpole 30A connectors, 50 pairs (unassembled)", "electrical-distribution",
         "electrical", 1, "kit", 55, 55, "Powerwerx", part_no="1327", url="https://powerwerx.com/1327bk-anderson-powerpole-housing-red",
         spec="Anderson Powerpole 30A — 50 red+black housing pairs = 100x Powerwerx 1327 housings @ $0.55 = $55. 30A contacts (1332) are the mating part (small separate buy — confirm). $0.55/housing firm (2026-07-31)."),
    Part("deutsch-dt-2pin-elec", "Deutsch DT 2-pin connectors, IP67 (exterior penetrations)", "electrical-distribution",
         "electrical", 10, "set", 3, 3, "Waytek Wire", part_no="AT2PS-CKIT", url="https://www.waytekwire.com/product/amphenol-sine-systems-at2ps-ckit-2-pin",
         spec="Amphenol AT2PS-CKIT 2-pin connector kit (DT-compatible: plug + receptacle + wedgelocks + contacts), IP67 — one per exterior penetration. Price $3/set est — confirm at order."),
    Part("pvc-trunking", "40×25mm PVC cable trunking, 5m", "electrical-distribution",
         "electrical", 4, "ea", 18.52, 18.52, "Amazon", "Home Depot (Wiremold)", part_no="B0DK6GMHGL",
         url="https://www.amazon.com/GenSDH-Raceway-Speaker-Concealer-Coffee-Width/dp/B0DK6GMHGL",
         spec="40mm PVC raceway + snap cover — one 5 m channel ($74.07, B0DK6GMHGL) cut into the 4 runs ($18.52 ea). Cheaper electrical-grade alt if cost matters: Legrand Wiremold NMW1 $13.57/5 ft (Home Depot)."),
    Part("corrugated-conduit", "10mm split corrugated wire loom, drop runs", "electrical-distribution",
         "electrical", 10, "m", 2.46, 2.46, "Amazon", part_no="B017L3GWIW",
         url="https://www.amazon.com/Split-Wire-Loom-Tubing-Polyethylene/dp/B017L3GWIW",
         spec="Electriduct 3/8\" (10mm ID) pre-slit PE convoluted loom — $14.99/20 ft roll ($2.46/m); buy 2× 20 ft for the ~10 m of drop runs."),
    Part("wire-label-kit", "Brady M210 wire label printer kit", "electrical-distribution",
         "electrical", 1, "ea", 194, 194, "Amazon", "DigiKey", part_no="M210-KIT",
         url="https://www.digikey.com/en/products/detail/brady-corporation/M210-KIT/16643735"),
    Part("led-strip", "HitLights 12V COB LED strip 4000K, 16.4ft reel (Circuit G, ×2)", "electrical-distribution",
         "electrical", 2, "reel", 37.28, 42.28, "HitLights", part_no="L2712V-40D3-1630-U",
         url="https://hitlights.com/products/premium-12v-cob-led-strip-light-single-color-ul-listed-16-4ft-ip-20-white-pcb",
         spec="12V DC COB LED strip, 4000K neutral, 16.4ft reel — 426 lm/ft, 4.2 W/ft, CRI 90+, dimmable, cuttable. Circuit G white work lighting = 3 ceiling runs: 2× ~2,162mm over the tray parallel to the X=520/2270 drum-side red safelights + 1× ~1,176mm running the IBC/plumbing corridor length (~5.5m total → ~7,670 lm ≈ ~548 lux, ~76W/6.3A). 2 reels cover the runs (~18 ft). Circuit G fed in 14 AWG for the ~6.3A load. PRIMARY: L2712V-40D3-1630-U premium UL-listed white PCB $42.28; cheaper alt L0512V-403-1630-U-BLK standard black PCB $37.28 (both 4000K, confirmed 2026-07-30). Mounts in led-channel; COB = even, hot-spot-free; dimmable."),
    Part("led-channel", "LED Profiles 981 slimline channel + diffuser, 8 ft (×6)", "electrical-distribution",
         "electrical", 6, "8ft length", 27.00, 27.00, "LED Profiles", part_no="981ASL", url="https://ledprofiles.com/collections/all-led-channels/products/slimline-ultra-low-profile-led-channel-981-series",
         spec="Alberko/LED Profiles 981ASL Ultra-Low-Profile aluminum LED channel (6063-T5 clear-anodized, 14.9×6.86mm) with snap-in FROSTED diffuser (D34) — houses BOTH the Circuit-G white strips AND the Circuit-D red COB safelights (8mm strips fit the ≤12.70mm slot; the diffuser disperses the COB for an even wash). 6× 8 ft (2.44m) sticks, one per run: 3 white (2 tray ~2.16m + 1 corridor ~1.18m) + 3 red safelight (~1.67m each). $27.00 ea ($25.65 @5+). End caps + mounting clips are accessories — confirm bundled or add (~$10)."),
    Part("led-connectors", "LED strip connectors + 12V PWM dimmers (Circuits G + D)", "electrical-distribution",
         "electrical", 1, "lot", 31.90, 31.90, "Super Bright LEDs", part_no="LDK-8A",
         url="https://www.superbrightleds.com/ldk-8a-12-24-volt-dc-single-color-led-dimmer",
         spec="~8x solderless clamp-on strip->pigtail connectors (8mm single-color 22AWG, $1.49 ea = $11.92) + 2x LDK-8A 12/24V PWM dimmers ($9.99 ea = $19.98) — Circuit-G white + Circuit-D red, both dimmable. $31.90 firm (2026-07-31)."),
    Part("safelight-strip", "SBL COB 12V red LED safelight strip, 5m reel (Circuit D)", "electrical-distribution",
         "electrical", 1, "reel", 89.99, 89.99, "Super Bright LEDs", part_no="STN-B-BRED-O12A-08F5M-12V",
         url="https://www.superbrightleds.com/led-strips-and-bars/5m-rgb-single-color-cob-led-strip-light-cob-series-led-tape-light-ip20-24v-red-green-blue+color-red+volts-12~vdc",
         spec="Super Bright LEDs Even-Glow COB 12V red (620nm), 5m reel — 2.4 W/ft (7.87 W/m), 40W/reel, 3.3A, 8mm wide, cuttable every 25mm, PWM-dimmable, IP20 (dry — ceiling, away from splash), UL-2108 (cut sheet COB2-IP20-Color-5m). Circuit-D safelight: 3 ceiling runs (X=520/2270/4170) cut from ONE reel → ~1,667mm each (5m total, ~40W). Red is cyanotype-safe (UV/blue only). In 981 channels + frosted diffuser (disperses the COB, matching the white). Circuit D stays 5A/18AWG — 40W=3.3A splits across 3 branches, no wire bump. $89.99 firm (2026-07-30). NOTE: the 3D models still show the reds at their nominal ~2.16m coverage; they're cut to ~1.67m to fit the one reel."),
    Part("pullcord-switch", "Pull-cord ceiling switch, 12V 6A SPST", "electrical-distribution",
         "electrical", 2, "ea", 121.99, 121.99, "americandoorsupply", part_no="CPM-1", url="https://americandoorsupply.com/products/ceiling-pull-switch-spst-nema-4-w-rotg-pivoting-cam"),
    Part("ground-stake", 'Copper-bonded ground rod, 8ft × ⅝" + acorn clamp', "electrical-distribution",
         "electrical", 1, "lot", 26.56, 26.56, "Home Depot", part_no="615880UPC",
         url="https://www.homedepot.com/p/ERICO-5-8-in-x-8-ft-Copper-Ground-Rod-615880UPC/202195738", spec="ERICO 615880UPC 5/8\"×8ft copper-bonded rod ($22.78) + bronze acorn ground-rod clamp GOEC5/8LDB ($3.78)."),
    Part("ground-wire-4awg", "4 AWG ground wire, green/yellow, 20ft", "electrical-distribution",
         "electrical", 1, "lot", 52, 52, "AutomationDirect", part_no="MTW4GYL-1",
         url="https://www.automationdirect.com/adc/shopping/catalog/bulk_wire_-a-_cable/single_conductor_wire_-a-_cable/mtw4gyl-1",
         spec="20ft AutomationDirect MTW4GYL-1 (4 AWG MTW, green/yellow) — the main panel -> 8ft ground stake earth conductor (§7.6, ~3m used, rest spare) + ring-lug terminal. $52 firm (2026-07-31, 20ft min buy)."),

    # ═══ container (§1) — mirrors costing.CONTAINER → exact $2,300–$4,300 ═══
    Part("container-20ft", "20 ft ISO container — CW (cargo-worthy) grade", "container",
         "container", 1, "ea", 2000, 3500, "containermgt.com", "local depot"),
    Part("container-delivery", "Delivery — short haul (<50 miles), tilt-bed", "fabrication-labor",
         "container", 1, "job", 300, 800, "Commercial tilt-bed hire"),

    # ═══ interior (§2) — mirrors costing.INTERIOR → exact $950–$1,350 ═══
    Part("light-sealing-mat", "Light-sealing materials (interior conversion)", "seals-gaskets",
         "interior", 1, "lot", 157, 178, "Amazon (bundle)", "Amazon"),
    Part("interior-paint", "Interior matte-black paint", "adhesives-finishes",
         "interior", 5, "gal", 24.98, 24.98, "Home Depot", part_no="PR31301", url="https://www.homedepot.com/p/316173659", spec="BEHR PRO Jet Black Dead Flat interior (ECC-10-2), ~400 sq ft/gal. 5 gal = 2 coats over the ~53 m² interior blackout + film wall + margin — re-count coverage at paint-out."),
    # image-plane-backing RETIRED 2026-07-22 — the same ACM backing as film 'dibond-acm-film'
    # (bonded to the moveable film-plane frame); the old fixed-wall backing line was a double-count.
    Part("interior-ventilation", "Ventilation (inline fans + light-trap baffles) — interior-conversion allowance",
         "ducting-ventilation", "interior", 1, "lot", 80, 130, "Amazon"),
    # Personnel-door hardware, itemized 2026-07-27 from the $50–100 "Door & access upgrades" lot:
    Part("door-hinges", "Personnel-door hinges (heavy-duty, ×3)", "fasteners-hardware",
         "interior", 3, "ea", 5, 8, "Home Depot", spec="Weather-rated butt hinges for the personnel access door. Price est."),
    Part("door-latch-lock", "Weatherproof door latch/lock set", "fasteners-hardware",
         "interior", 1, "ea", 20, 45, "Home Depot", spec="Lockable latch/handle set for the personnel door. Price est."),
    Part("door-weatherseal", "Door perimeter weatherstrip + threshold", "adhesives-finishes",
         "interior", 1, "lot", 10, 22, "Home Depot", spec="Light-tight/weather seal around the personnel door + threshold sweep. Price est."),
    Part("door-handle-hw", "Door pull handle + misc mounting hardware", "fasteners-hardware",
         "interior", 1, "ea", 39.10, 39.10, "McMaster-Carr", part_no="3570N12", url="https://www.mcmaster.com/3570N12/", spec="McMaster 3570N12 pull handle for the personnel door + mounting screws/anchors."),
    # misc-conversion-hw kept as a CONTINGENCY BUFFER (not itemized) — a deliberate "unknown-unknowns"
    # allowance for a first-of-kind container conversion; inventing line items here would be false precision.
    Part("misc-conversion-hw", "Misc. conversion hardware (contingency buffer)", "fasteners-hardware",
         "interior", 1, "lot", 80, 130, "Home Depot", spec="Deliberate contingency allowance for unforeseen conversion hardware — NOT itemized by design. Draw down as real needs surface during build."),

    # ═══ optics (§3) — mirrors costing.OPTICS → exact $95–$240 ═══
    Part("pinhole-shim", "Custom laser-drilled pinhole — SS-302/304 shim, 3×3", "stainless-sheet",
         "optics", 1, "ea", 40, 100, "Lenox Laser", part_no="SS-3/8-DISC", url="https://lenoxlaser.com/shop/optical-apertures/standard-apertures/standard-aperture/",
         note="Ø2.17mm optical element — Lenox SS-3/8-DISC standard aperture (302 SS, 3/8\" mounted disc). ⏳ DEFERRED to v1.0: config-dependent $22-100, firm via RFQ (1-800-49-HOLES) at design-complete."),
    Part("pinhole-backing-plate", "Steel backing plate 6×6×⅛ + welded frame", "steel-structural",
         "optics", 1, "ea", 20, 40, "Metal Supermarkets", "local fab"),
    Part("shutter-plate", "Shutter plate (⅛ steel 10×8) + slide channel", "steel-structural",
         "optics", 1, "ea", 25, 50, "local fab"),
    Part("pinhole-retaining-ring", "Disc retaining ring (Al 6061-T6, M52×0.75)", "aluminum",
         "optics", 1, "ea", 15, 25, "local fab", spec="Ø52 bore × M52×0.75 external thread, 3× M4 grub screws — screws into the plate counterbore to clamp the Ø50 pinhole disc flat; removable for swap/clean"),

    # ═══ film (film-plane-mechanism-report §7) — itemized; structural+frame+saddles, sums to costing
    # FILM minus the clamp lines (= 3,102). The muslin clamps are the separate 'clamp' system below. ═══
    # — Structural & Rails (6061 Al U-channel + acetal skate + 304 cross-slide + Belden U-joint corner mechanism) —
    # Replaced the superseded Option-A leadscrew drive (HGR20/Acme/handwheel/rod-end) 2026-07-19.
    Part("fp-u-channel", '6061-T6 Al U-channel depth rail 3×1½"×0.2" (76×38mm), 8 ft', "aluminum",
         "film", 4, "ea", 81.99, 81.99, "Grainger", part_no="795M51", url="https://www.grainger.com/product/795M51",
         spec="4 depth rails, one per corner, running wall-to-wall (~2,362mm, Yd0→C_WID) along the optical axis — an acetal skate rides inside each to set that corner's depth/focus. 6061-T6 aluminum, SAME 76×38 section. Structural check: 6061-T6 yield (~276 MPa) EXCEEDS annealed 304 (~215 MPa) so strength is fine; the ~3× lower E gives ~1mm sag vs ~0.4mm over the 2.36m span — optically irrelevant at f/1088, and flatness is carried by the ACM backing (same logic as the Al frame). Also ~34 kg lighter across the 4 rails. SOURCING: each rail must be ONE continuous piece ≥2,362mm (the skate can't cross a splice). Grainger 795M51 (6061 Al U-channel, 3×1½×0.2\" wall) is stocked in 8 ft (2,438mm) lengths — one uncut stick spans the 2,362mm rail with margin, so 4 sticks = 4 rails, no splice. $81.99/8ft firm (2026-07-29)."),
    Part("fp-ujoint", "Belden SSNBUJ750x3/8KB needle-bearing U-joint (3/8\" keyway bore, 45deg, SS, booted)", "bearings-motion",
         "film", 4, "ea", 252.13, 252.13, "Grainger", part_no="41D816",
         url="https://www.grainger.com/product/BELDEN-Universal-Joint-Stainless-41D816",
         spec='One per corner — supplies the tilt+swing angular DOF. Belden SSNBUJ750x3/8KB (Grainger 41D816): 3/8" KEYWAY bore (3/32x3/64 key) locked by a set screw, 0.75" OD, 2-11/16" (68.3mm) overall, 45deg max operating angle, STAINLESS, NEEDLE-BEARING (upgrade from the old plain pin-and-block), 95 in-lb static breaking torque (far above the near-zero positioning load; backlash optically irrelevant at f/1088). COMES FACTORY-BOOTED — integral bellows OD 1-9/32" (32.54mm) x OL 1-1/4" (31.75mm), so NO separate boot part. $252.13 ea firm (Grainger 2026-08-13); x4 = $1,008.52. Retention J3/J4: keyed 3/8" stub (3/32x3/64 keyseat + key) + set screw.'),
    Part("fp-ujoint-key", '3/32" sq × 3/64 SS machine keys (×8) — U-joint keyway', "fasteners-hardware",
         "film", 1, "lot", 6, 10, "McMaster-Carr",
         spec="8 keys (2/corner) for the SSNBUJ750x3/8KB 3/32x3/64 keyway — cut to length from 3/32in square 304 SS key stock; each keys the 3/8in stub to the joint bore (torque + anti-rotation), the joint set screw locks it axially. Cheap lot; firm at order."),
    Part("fp-shaft-support", "McMaster 4040N12 304 shaft support", "bearings-motion",
         "film", 4, "ea", 58, 58, "McMaster-Carr", part_no="4040N12", url="https://www.mcmaster.com/4040N12/",
         spec="Two-piece 304 clamp securing the U-joint INPUT stub to the X (swing) slide, one per corner. $58 ea firm."),
    Part("fp-stub-shaft", '3/8" 304/304L SS rod — U-joint stub shafts (1× 3 ft)', "steel-structural",
         "film", 1, "lot", 13, 13, "McMaster-Carr", part_no="89535K87", url="https://www.mcmaster.com/89535K87/",
         spec='Input + output stub shafts into the U-joint (2/corner ×4 = 8 short stubs, ~60–80mm each ≈ 560–640mm + kerf). ONE 3 ft (914mm) length ($13.25 firm) yields all 8 with margin. Each stub gets a 3/32×3/64 KEYSEAT for the SSNBUJ750x3/8KB keyway bore (fp-ujoint-key) — keyed for anti-rotation, then locked axially by the joint set screw (J3/J4).'),
    # fp-skate DECOMPOSED 2026-07-22 → off-the-shelf rollers/axles + fab carriage plate (mirrors the spray skate)
    Part("fp-skate-roller", "1-1/4\" OD acetal load rollers — Delrin rod (cut ×8)", "bearings-motion",
         "film", 1, "1 ft rod", 10.97, 10.97, "McMaster-Carr", part_no="8576K23",
         url="https://www.mcmaster.com/8576K23-8576K232/",
         spec="Load rollers — 2 per skate × 4 = 8, cut 20mm wide from one 1 ft 1-1/4\" OD (Ø31.75 ≈ Ø32) Delrin rod (8576K23, same stock as the spray skate), each drilled Ø10 bore to spin on the axle pin. Gravity-seated on the U-channel bottom flange."),
    Part("fp-skate-keeper", "3/4\" OD acetal keeper rollers — Delrin rod (cut ×8)", "bearings-motion",
         "film", 1, "4 ft rod", 14.60, 14.60, "McMaster-Carr", part_no="8497K276",
         url="https://www.mcmaster.com/8497K276-8497K273/",
         spec="Keeper rollers — 2 per skate × 4 = 8, cut 20mm wide from a 3/4\" OD (Ø19.05 ≈ Ø20) Delrin rod (8497K276, 4 ft — min stock, ample spare), each drilled Ø10 bore; captive under the U-channel top flange. $14.60/4ft firm."),
    Part("fp-skate-axle", "10mm × 60mm 304 SS axle pins (4-pack) — skate axles", "fasteners-hardware",
         "film", 4, "pack", 5, 5, "Amazon", part_no="B0816MQ5T6",
         url="https://www.amazon.com/uxcell-Single-Hole-Clevis-Pins/dp/B0816MQ5T6",
         spec="16 skate axles (4 per skate × 4) — the same 10mm×60mm 304 SS clevis/axle pins the spray skate uses; 4 packs = 16 pins. The acetal rollers spin on these Ø10 pins. 304 (splash zone, matches the spray). $5/4-pack = $20."),
    Part("fp-carriage-plate", "Skate carriage plate (×4) — fab", "steel-structural",
         "film", 4, "ea", 34, 59, "local fab",
         spec="One carriage plate per corner — carries the 4 rollers on their axles + the inboard lip; the U-joint/cross-slide stack bolts to it. The only fab piece of the skate. FIRM DESIGN (Sheet 3 View A): 80×181×6mm 6061-T6 (aluminum; grown to 181 tall so the top keeper-axle row clears its ≥2×Ø10 edge distance). Hole pattern: 4× Ø10 stub-axle holes on a 40(Yd)×38(Z) grid + 4× M8 (J1) to the Z-slide (28×44) + 2× M4 for the cam-clamp base; all holes ≥2×Ø from the edges. Est. cost — firm at fab quote."),
    Part("fp-cross-slide", "304 flat-bar Z (tilt) + X (swing) cross-slides + UHMW pad + gib", "steel-structural",
         "film", 4, "set", 79, 129, "Metal Supermarkets", "McMaster-Carr",
         spec="One 2-axis cross-slide stack per corner — 304 flat-bar Z (tilt) + X (swing) slides on UHMW pads with an adjustable gib. MOUNT DEEP: the 38.1mm bar dimension runs in the gravity/load direction, NOT flat (Sheet 10 load case — deep SF≈10 vs flat 1.7; flat fails a 2× factor). FLAT-BAR STOCK: 304 SS ¼\"×1½\" (6.35×38.1mm); 8 pieces (4× ~345mm Z-tilt + 4× ~365mm X-swing) ≈ 2.84m cut length → order 2× 8ft lengths (bars grown from the ~250mm est to hold ±40°/±28°: the cross-slide stroke needs travel + carriage — corner blueprint 2026-08-10). 304 (not 316) — the cyanotype wash has no chloride, so 316's pitting resistance is unused; 304 is adequate in the splash zone. FLAT BAR FIRM: Metal Supermarkets ¼×1½×8ft 304 $134.73 (2026-08-01); 2× 8ft = $269.46 = ~$67/set of bar. UHMW pad + brass-tip gib + cut/assemble fab still est — the $316–516 range brackets bar + those adds; get a fab quote to firm the balance."),
    Part("fp-cam-clamp", "McMaster 5128A63 low-profile hold-down toggle clamp (rail brake)", "fasteners-hardware",
         "film", 12, "ea", 12.93, 12.93, "McMaster-Carr", part_no="5128A63", url="https://www.mcmaster.com/5128A63/",
         spec="Cam rail-brake — 3 per corner × 4. Low-profile hold-down toggle clamp: base ~19×22mm (2× M4×0.7, ~15.7mm hole spacing), ~7.6mm profile closed, ~69mm handle, hold-down reach ~22mm, adjustable spindle. Mounts on the carriage plate (small mount tab/bracket to seat the base + aim the spindle); the UHMW-padded spindle pinches DOWN on the U-channel TOP FLANGE to lock the skate at depth for the shot + transport (self-reacting — load rollers react on the bottom flange, Section A-A / Sheet 3). $12.93 ea firm (2026-07-30). Handle needs swing clearance vs the rail/ACM — verify at the bench."),
    Part("corner-l-plate", "Corner plate 304 SS (U-joint mount)", "steel-structural",
         "film", 4, "ea", 58.90, 58.90, "Metal Supermarkets", "Online Metals", dims='6×8×¼in',
         spec='¼" 304 SS plate, 6"×8" blank bent into an L-bracket — the frame-corner ↔ U-joint mount. Carries the concentrated U-joint corner load in STEEL, not aluminum; stainless for the cyanotype splash zone + galvanic match to the 303 SS U-joint. NOT expendable (the perimeter angle stays expendable 6061). Metal Supermarkets $58.90 ea firm (2026-08-01) — confirm the press-brake bend is included or added.'),
    # — Film Plane Frame (1,046) —
    Part("alu-angle-2x2", 'Aluminum angle 2"×2"×1/8" (6061-T6, plain) — 16 ft lengths', "aluminum",
         "film", 3, "16 ft length", 176.06, 176.06, "Metal Supermarkets", "Online Metals",
         url="https://www.onlinemetals.com/en/buy/aluminum/2-x-2-x-0-125-aluminum-angle-6061-t6/pid/987",
         spec="6061-T6 angle (NOT 2024/7075 — corrosion + weldability). PLAIN mill finish (NOT anodized) — the film-plane PERIMETER FRAME, EXPENDABLE (inspect-annually / replace-on-pitting; bare 6061 pits sooner than anodized in the splash zone, so a shorter interval — anodizing is an option for longer life). 1/8in wall — frame sag is optically irrelevant at f/1088 and the ACM backing carries flatness, so only the wall is thinned; the 2in leg (the capture channel) is kept. WELD-FREE cut plan from 3× 16 ft (192\") lengths: 2 lengths → the two horizontal edges (4,389mm each, one per length, 488mm offcut); 1 length → both vertical edges (2,094mm ×2 from one 16 ft). No mid-span splices — only the 4 corner joints are welded/bolted. Metal Supermarkets 192\" @ $176.06 (2026-07-31). One frame — re-order to replace.",
         note="Expendable plain-6061; add 16ft lengths if pre-buying spares."),
    Part("dibond-acm-film", "Dibond ACM panel 3mm (black), 4×8 sheet", "plastics-sheet",
         "film", 4, "sheet", 95, 95, "Central Coast Plastics", "TAP Plastics",
         spec="4× 48×96\" black 3mm ACM sheets as full-height VERTICAL STRIPS (Option A) — 3 vertical butt seams, splice-battened behind; no horizontal seam (2094mm plane height fits one 2438mm sheet). Covers the {{fact:film_plane_width_mm}}×{{fact:film_plane_height_mm}}mm rigid backing (4389 ÷ 1219 = 4 strips). 3mm (the black-stocked thickness) is slightly less stiff but flatness is carried by the 6061 frame + clamps and is optically irrelevant at f/1088. SUPPLIER: Curbell Plastics does NOT stock black ACM/Dibond (confirmed 2026-08-03 — cannot supply; do not re-source there); black via Central Coast Plastics / TAP Plastics. Price TBC ($95/sheet placeholder, qty 4)."),
    Part("epdm-foam-tape", 'Black EPDM foam tape 1"×½"', "seals-gaskets",
         "film", 2, "roll", 22.37, 22.37, "McMaster-Carr", "Grainger", part_no="8694K88",
         url="https://www.mcmaster.com/8694K88/",
         spec="25 ft rolls — 2 (50 ft) cover the ~43 ft film-plane perimeter primary seal",
         note="Provisional qty: right-sized to the ~43 ft perimeter. Revisit with the EPDM-seal review."),
    Part("rosco-duvetyne", "Impact 9oz Duvetyne 57\" × 10yd (B&H)", "fabric-textile",
         "film", 1, "ea", 69, 69, "B&H Photo", part_no="1775270", url="https://www.bhphotovideo.com/c/product/1775270-REG/impact_dr9_10_9_oz_duvetyne_10.html",
         spec='Impact DR9-10 (B&H #1775270) 9oz black light-absorbing duvetyne, 57"×10yd, $69 (research 2026-07-30). B&H does not stock Rosco brand; the Impact house brand is equivalent. 57" vs the 60" spec — fine (cut/hung). 16oz = DR16-10 if heavier wanted.'),
    Part("poly-sheeting-film", "4-mil black poly sheeting", "tools-safety",
         "film", 1, "roll", 40.12, 40.12, "Home Depot", part_no="51982", url="https://www.homedepot.com/p/332820356", spec="Film-Gard 10 ft × 100 ft × 4-mil black poly (film-plane blackout). 4-mil is fully opaque for a light-seal (opacity is the black pigment, not the gauge) — 6-mil was over-spec for a non-structural curtain."),
    Part("gorilla-tape", '2" black Gorilla Tape', "adhesives-finishes",
         "film", 6, "roll", 9.94, 9.94, "Home Depot", "Amazon", part_no="106718", url="https://www.homedepot.com/p/316372144", spec='Gorilla 30 yd × 1.88" black tape'),
    # — Wall-Seat Saddles (440; rev12 ×6, the 2 BR ends are walkway combined plates) —
    Part("wall-seat-saddle-8mm", "Wall-seat saddle 8mm A36 plate (ICP-11)", "steel-structural",
         "film", 1, "sheet", 216, 216, "Metal Supermarkets",
         dims="610×760×8mm (24×30in)",
         spec="8mm A36 mild-steel plate, 610×760mm (24×30in) — nests all 6 saddles' back-plates (150×200) + exterior plates (150×200) + gusset triangles (from 3× 200×110). Laser/plasma cut to the piece dims; weld by owner ($0 labor). QUOTE NEEDED — local metal/fab shop, not online. $216 placeholder (part of the old $318 saddle line, split 8mm/10mm) pending quote."),
    Part("wall-seat-saddle-10mm", "Wall-seat saddle 10mm A36 plate (ICP-11)", "steel-structural",
         "film", 1, "sheet", 102, 102, "Metal Supermarkets",
         dims="610×254×10mm (24×10in)",
         spec="10mm A36 mild-steel plate, 610×254mm (24×10in) — nests the 6 saddle seats (150×110). Cut to size; weld by owner ($0 labor). QUOTE NEEDED — local metal/fab shop, not online. $102 placeholder (split from the old $318 saddle line) pending quote."),
    Part("bolt-m12x65", "M12×65 hex through-bolt, Grade 8.8 zinc, partial-thread", "fasteners-hardware",
         "film", 28, "ea", 15.95 / 10, 15.95 / 10, "McMaster-Carr", part_no="91280A728",
         url="https://www.mcmaster.com/91280A728/",
         spec="ICP-12: wall-sandwich through-bolt (4/saddle ×6 + 4 spare), sized for the 30mm-corrugation grip (~50mm), partial thread. $15.95/pack of 10 → 3 packs for 28. Pad with 1–2 M12 flat washers if the actual container corrugation is <30mm."),
    Part("nut-m12-plain", "M12 hex nut, plain", "fasteners-hardware",
         "film", 28, "ea", 12.78 / 50, 12.78 / 50, "McMaster-Carr", part_no="90591A181", url="https://www.mcmaster.com/90591A181/", spec="Plain hex nut — M12×65 wall-sandwich bolts (+ split lock washer). $12.78/pack of 50. Pitch M12×1.75 coarse — confirmed vs 90591A181 PDF 2026-07-29."),
    Part("washer-m12-flat", "M12 flat washer, zinc", "fasteners-hardware",
         "film", 112, "ea", 9.71 / 100, 9.71 / 100, "McMaster-Carr", part_no="91166A290", url="https://www.mcmaster.com/91166a290/", spec="Flat washers, M12×65 wall-sandwich bolts — 2 functional + 2 shim/bolt (shims pad the grip if corrugation <30mm). $9.71/pack of 100."),
    Part("washer-m12-split", "M12 split lock washer, zinc", "fasteners-hardware",
         "film", 28, "ea", 11.97 / 100, 11.97 / 100, "McMaster-Carr", part_no="91202A246", url="https://www.mcmaster.com/91202A246/", spec="Split lock washer under each nut — M12×65 wall-sandwich bolts (plain nut + split = locked). $11.97/pack of 100."),
    # M12 nyloc nut — verified ALTERNATIVE locking (Option B), NOT USED (chose plain nut + split washer):
    # McMaster 94645A230, $10.08/pack of 10 = $1.008 ea. Swap in (and drop the split washers) if
    # adopting nyloc locking for the M12 through-bolts; ~+$70 over the 110 bolts. https://www.mcmaster.com/94645A230/
    Part("saddle-m8-thumb", "M8×25mm knurled thumbscrew DIN 464", "fasteners-hardware",
         "film", 12, "ea", 11.8, 11.8, "McMaster-Carr", "Maedler", spec="ICP-13: left-rail drop-in hold-down; 2/saddle ×4 left + 4 spare", part_no="92581A540", url="https://www.mcmaster.com/92581A540/"),
    Part("bolt-m8-fixing", "M8×1.25 × 25 hex bolt, 304 SS (A2-70) — right-rail end fixing (ICP-14)", "fasteners-hardware",
         "film", 8, "ea", 13.91 / 50, 13.91 / 50, "McMaster-Carr", part_no="91310A535", url="https://www.mcmaster.com/91310A535/", spec="ICP-14: right depth-rail end flange → wall seat hold-down (does NOT cross the wall). Grip = 0.2\" (5.08mm) 795M51 channel base + 10mm seat ≈ 15mm → M8×25 (short → fully threaded). Pitch M8×1.25 coarse (matches the M8 plain nut). 304 SS A2-70 — upgraded from zinc 2026-08-13 (the film plane wets during development; 304 is adequate, no chloride). McMaster 91310A535 $13.91/pack of 50 firm (Alvin 2026-08-13)."),
    Part("nut-m8-plain", "M8×1.25 hex nut, plain SS", "fasteners-hardware",
         "film", 8, "ea", 7.53 / 100, 7.53 / 100, "McMaster-Carr", part_no="90591A161", url="https://www.mcmaster.com/90591A161/", spec="Plain hex nut — M8 right-rail fixing. Pitch M8×1.25 coarse — confirmed vs 90591A161 PDF 2026-07-29 (matches the bolt). $7.53/pack of 100."),
    # ═══ clamp (film-clamp-mechanism-report §4) — split out of FILM; itemized, sums to the FILM
    # clamp lines (off-the-shelf nylon clamps + HDPE filler) ═══
    Part("muslin-clamp", "Nylon spring clamp, 3½″ (Pittsburgh 69289)", "fasteners-hardware",
         "clamp", CLAMP_N_TOTAL, "ea", 1.99, 2.99, "Harbor Freight", "Amazon", part_no="69289",
         url="https://www.harborfreight.com/3-12-in-nylon-spring-clamp-69289.html",
         spec="Inert fiberglass/nylon spring clamp with swivel pads — no corrosion in the cyanotype splash zone (replaces the custom steel-bracket clip). Clips over the filler-filled L-frame edge to grip the muslin; the jaw must clear ~55mm (2\" leg + ACM + muslin), so a ≥3\" clamp. Top + 2 side edges only (bottom = walkway/swing clearance). Confirm the open-jaw ≥2\" at purchase; 2½\" 69290 is the smaller-body fallback."),
    Part("clamp-filler", "HDPE filler strip (L-channel packer)", "plastics-sheet",
         "clamp", 1, "lot", 30, 70, "TAP Plastics", "McMaster-Carr",
         spec=f"Inert HDPE strip, {CLAMP_FILLER_D:g}mm deep (= frame leg − ACM − muslin − angle), filling the aluminum-angle L channel along the 3 clamped edges (~8.6 m) so the nylon clamp bites a solid full-depth sandwich. Cut to suit; chemistry-safe (same family as the tray liner). Firm at fab."),

    # ═══ lightlock (hinged-panel §8.2) — housing + drum; sums to costing.LIGHTLOCK ($1,385–$2,070) ═══
    Part("ll-hdpe-housing", "3/16\" UV-stab HDPE sheet, black — 48×96 (×3)", "plastics-sheet",
         "lightlock", 3, "sheet", 184.99, 184.99, "US Plastics", "TAP Plastics", part_no="46685",
         url="https://www.usplastic.com/catalog/item.aspx?itemid=136962&catid=705",
         spec="Ø900 fixed housing shell (~65 ft²), rolled + extrusion-welded from 3× 4×8 ft 3/16\" (≈5mm) UV-stab HDPE sheets — the 111\" circumference needs 3× 48\" sheet widths (2 fall ~15\" short). ~33% offcut on the 3rd sheet; a 5×10 ft sheet would cut to 2 (optimize at order). US Plastics 46685 $184.99/sheet."),
    Part("ll-pp-drum", "1/8\" black HDPE sheet — 48×96 (×3)", "plastics-sheet",
         "lightlock", 3, "sheet", 123.34, 123.34, "US Plastics", "TAP Plastics", part_no="46684",
         url="https://www.usplastic.com/catalog/item.aspx?itemid=136961&catid=705",
         spec="Ø864 revolving drum shell (~65 ft²) — rolled + extrusion-welded 1/8\" HDPE (106.9\" circ needs 3× 48\" widths). The shell is a light-tight cover over the steel shaft + caps + edge-stiffening, so its 1/8\" is non-structural (lighter = easier revolve, less bearing load). The 2 end caps are STRUCTURAL (they carry the stub shafts into the SKF 6215 bearings) → 3/16\" HDPE (LT_CAP_T), cut from the housing 46685 offcut — no extra sheet. All HDPE, weld-compatible. US Plastics 46684 $123.34/sheet."),
    Part("ll-skf-bearing", "SKF 6215-2RS1 sealed bearing", "bearings-motion",
         "lightlock", 2, "ea", 60.59, 60.59, "Bearings Direct", "McMaster-Carr", part_no="6215-2RS", url="https://bearingsdirect.com/6215-2rs-ball-bearing-75x130x25-sealed-6215-2nse/", spec="Top and bottom (drum rotation). Ø75 bore × Ø130 OD × 25mm wide, C=52.7 kN, both-sides sealed (6215-2RS / 6215-2NSE; SKF designation 6215-2RS1). Buy the ABEC-1 grade: the drum is a hand-rotated, low-speed, low-load light-lock — the tighter ABEC-3 tolerance buys nothing here (SKF's standard 6215-2RS1 is Normal/P0 = ABEC 1). VERIFIED $60.59 ea at Bearings Direct 2026-07-18. ALT: McMaster 6138K125 @ $394.88 ea — a heavy commodity-bearing premium, prefer the distributor."),
    Part("ll-stub-shafts", "75mm Ø × 150mm steel stub shaft", "steel-structural",
         "lightlock", 2, "ea", 15, 25, "steel service center", spec="Bearing shafts"),
    Part("ll-wiper-seal", "Felt/brush wiper strip + 12mm closed-cell neoprene", "seals-gaskets",
         "lightlock", 1, "lot", 40, 75, "Frost King + Canal Rubber", spec="Drum↔housing rotating seal (opening edges + top/bottom rings) + drum top/bottom", part_no="BP17A", url="https://www.doitbest.com/product/146005/"),
    Part("ll-silicone-sealant", "Silicone bead sealant (black, UV-stable)", "adhesives-finishes",
         "lightlock", 1, "ea", 19.91, 19.91, "Home Depot", part_no="RDX1001bl",
         url="https://www.homedepot.com/p/331895623",
         spec="Bearing-housing / light-trap seam seal. Maxisil black natural-stone silicone, 10.5 oz (weather/UV grade, neutral-cure — not a mildewcide bath caulk)."),
    Part("ll-grab-rail", "100mm Ø SS grab rail", "fasteners-hardware",
         "lightlock", 1, "ea", 25, 45, "Marine Fiberglass Direct", spec="Interior handle, 400mm cut length", url="https://www.marinefiberglassdirect.com/products/16-stainless-steel-safety-grab-bar-bolt-on-for-marine-dock-deck-boat-pool-hot-tub"),
    Part("ll-matte-finish", "Matte-black interior finish", "adhesives-finishes",
         "lightlock", 1, "ea", 40, 70, "local", spec="Black-pigmented sheet (no etch-prime); scuff + flat-black touch-in at welds"),
    Part("ll-fasteners", "Stainless fasteners + nylon isolation washers", "fasteners-hardware",
         "lightlock", 1, "lot", 45, 60, "US Plastic + Amazon", spec="Steel shaft/bearing ↔ plastic shell joints (no galvanic couple)", part_no="92674", url="https://www.usplastic.com/catalog/item.aspx?itemid=155501"),
    Part("ll-fabrication", "Plastic fabrication (roll 2 cylinders, hot-air / extrusion weld, fit, bearings)", "fabrication-labor",
         "lightlock", 1, "lot", 800, 1150, "Local plastic fab", spec="16–22 hrs labor"),

    # ═══ swing (hinged-panel §8.3) — swing pivot hardware; sums to SWINGPIVOT minus door ($520–$880) ═══
    Part("sp-pivot-post", "Ø89×8mm CHS pivot post + machined hub / thrust collar", "steel-structural",
         "swing", 1, "ea", 180, 300, "Metal Supermarkets", "Speedy Metals",
         spec="Upgrades the reused film far-left upright; carries the ~3.6 kN·m swing cantilever — SF 3.7 in S355. PIPE sourced: 3\" NPS Sch 80 (Ø88.9 OD × 7.6mm wall), 36\" ≈ $135 (Speedy Metals). The machined hub / thrust collar + 2 journal bands (Ra ~0.4 µm, iglide runs on soft shafts) are FAB → pending blueprints. Band held est pending the fab quote."),
    Part("sp-thrust-bearing", "Thrust ball bearing, 51118 (Ø90 bore, single-direction)", "bearings-motion",
         "swing", 1, "ea", 80.03, 80.03, "Bearings Direct", "Amazon / VXB", part_no="51118",
         url="https://bearingsdirect.com/51118-thrust-ball-bearing-90x120x22-grooved-ubc-usbc/",
         spec="Carries the ~330 kg (3.24 kN) vertical load at the post base; thrust-only (radial + moment taken by the iglide sleeves). 51118 = 90 × 120 × 22mm, static Cₒ ≈190 kN → SF >50; single-direction (gravity-down). Ø90 bore matches the Ø89 post — the machined thrust collar bears on the shaft washer. Commodity part: generic ~$25–40, branded FAG/SKF ~$50–85 (do NOT buy at Motion/Applied industrial list ~$430). Chrome steel: grease + wipe annually (humid darkroom); stainless S51118 available ~$100+ if preferred."),
    Part("sp-sleeve-bearings", "iglide J flange bushing, Ø90 bore (JFM-9095-100)", "bearings-motion",
         "swing", 2, "ea", 130.53, 130.53, "igus", part_no="JFM-9095-100",
         url="https://www.igus.com/iglide-ibh/flange-bearings/product-details/iglide-j-m?artnr=JFM-9095-100",
         spec="Top + bottom radial location of the post. igus iglide J self-lubricating polymer, Ø90 ID × Ø95 OD × Ø103 flange × 100 mm long. The FLANGE gives axial location against the hub face; the OD is a light press into the hub bore. Axial load is on the 51118 thrust bearing. Maintenance-free, no oil; inert plastic — chemical-resistant (iglide J passed the igus chemical filter; iglide X isn't offered at Ø90). Service pressure ≈1.3 N/mm² vs ≈35 N/mm² allowable (>25× margin); runs on the unhardened S355 post. $130.53/ea, ships in days — replaces the made-to-order GGB DU (3-mo lead)."),
    Part("sp-drum-cage", "Drum support cage, 1.5×1.5×0.120in steel SHS", "steel-structural",
         "swing", 1, "lot", 70, 120, "local fab", spec="Steel frame carrying the Ø900 housing + drum on the swinging leaf. #26: 40×40×3 nominal → 1.5×1.5×0.120in stock (the closest US size; material is inside the local-fab lot, so no separate per-ft line)."),
    Part("sp-wall-stays", "Top + bottom wall stays + 4-bolt anchor plates", "fasteners-hardware",
         "swing", 2, "set", 45, 60, "Fasteners Plus", spec="Transport lock — M16 turnbuckle + eye/hook rods + inside/outside wall plates", part_no="JETBGV58X6", url="https://www.fastenersplus.com/products/5-8-x-6-jaw-eye-galvanized-turnbuckle"),
    Part("sp-rail-saddles", "Drop-in rail saddles + tapered dowels", "steel-structural",
         "swing", 4, "ea", 20, 32.5, "local fab", "McMaster-Carr", spec="For the 2 removable left film rails (TL + BL); dowels set the film datum"),
    # ═══ door (hinged-panel §8.4) — fixed door frame; sums to the SWINGPIVOT door lines ($335–$550) ═══
    Part("sp-door-frame-rhs", "2×2×0.120in steel SHS (6 m bulk lengths)", "steel-structural",
         "door", 3, "ea", 30, 40, "Metal Supermarkets", spec="Frame members"),
    Part("sp-door-seal-lips", "Tight-seal nylon strip brush + aluminum holder (~4.7 m, top + bottom)", "seals-gaskets",
         "door", 1, "lot", 129, 129, "McMaster-Carr", part_no="74405T12", url="https://www.mcmaster.com/74405T12-74405T126/", spec="Top + bottom door-frame light seals (paths #3–#4) — 2× McMaster 74405T12 nylon Tight-Seal Strip Brush (8 ft, 1\" overall height, $28.88 ea) in 2× McMaster 8813T53 aluminum holder channel (8 ft, $35.37 ea) = $128.50 firm; covers full panel width top + bottom (~2× C_WID ≈ 4.7 m ≈ 15.5 ft, from 4× 8 ft lengths). The swinging panel edge SWEEPS THROUGH the bristles, so a brush (not a compression EPDM, which would drag under the sideways sweep) — same principle as the drum-opening brush seals.", note="Changed 2026-07-18 from 3mm steel seal lips + panel-edge EPDM compression to a strip brush: the top/bottom seal is swept through by the swinging panel, so a brush is the correct type. Brush 74405T12 ($28.88/8ft), holder 8813T53 ($35.37/8ft) — prices verified 2026-07-18."),
    Part("sp-door-fab", "Welding / fabrication", "fabrication-labor",
         "door", 1, "lot", 200, 350, "local fab", spec="Frame assembly + wall attachment"),

    # ═══ panel (hinged-panel §8.1) — panel structure; sums to costing.PANEL ($1,124–$1,691) ═══
    Part("panel-rhs-frame", "2×2×0.120in steel SHS (6 m bulk lengths)", "steel-structural",
         "panel", 4, "ea", 30, 40, "Metal Supermarkets", spec="Frame perimeter + internal members"),
    Part("panel-pp-skins", "1/8\" black HDPE sheet (48×96)", "plastics-sheet",
         "panel", 4, "sheet", 123.34, 123.34, "US Plastics", "TAP Plastics", part_no="46684",
         url="https://www.usplastic.com/catalog/item.aspx?itemid=136961&catid=705",
         spec="Panel skins, both faces (~12 m², 4× 4×8 ft sheets) — rev11, replaces 18mm ply. 1/8\" HDPE is nearest stock to the 4mm PANEL_SKIN_T nominal (weld-compatible with the HDPE housing/drum); the U-channel grid (~400–450mm centers) keeps the skin flat, so the 0.8mm is immaterial. US Plastics 46684 $123.34/sheet."),
    Part("panel-fanb-ply", "Pressure-treated pine plywood (Fan B mount band + cooler base)", "timber-ply",
         "panel", 1, '4\'×8\' ¾" sheet', 69.68, 69.68, "Home Depot", part_no="231428", url="https://www.homedepot.com/p/206343229",
         spec='¾" CC pressure-treated pine, full 4\'×8\' sheet. Fan B mount band (610×1220mm, one corner bottom→1,125mm) '
              'AND the cooler stowage base plate (600×350) are both cut from this one sheet (plywood-base-12 retired 2026-07-27). '
              'PT is defensible at the vented cargo-door end; plenty of leftover from one sheet.'),
    Part("panel-corner-stiffener", '1"×1"×1/8" Al angle, 8 ft — corner-zone stiffener grid', "aluminum",
         "panel", 4, "ea", 12.20, 12.20, "Grainger", part_no="2EYP1", url="https://www.grainger.com/product/2EYP1",
         spec="Corner-zone anti-oil-can rib grid — light-tightness is carried by the two black HDPE skins and the latch/fan load by the RHS frame + ply band, so the corner only needs stiffening against oil-can. Per corner: 1 vertical (2,258mm) + 2 horizontal (653mm) 1\"×1\"×1/8\" (25×25×3.2mm) Al angle ribs, ~325×750mm bays, holding both 1/8\" HDPE skins flat within the 40mm framed cavity. The leaf is VERTICAL, so skin self-weight is in-plane; the grid only resists out-of-plane oil-can (works with the U-channel skin retainers at ~400-450mm centers, report §2.5). ~7.1m installed → 4× 8 ft (2,438mm) sticks for clean piece-fit (2 sticks → the 2 verticals, 2 → the 4 horizontals + spare). ~2.9 kg installed. Grainger 2EYP1 $12.20/8ft firm (2026-07-29)."),
    Part("panel-epdm-gasket", "20mm EPDM gasket (per meter, closed-cell)", "seals-gaskets",
         "panel", 21, "m", 1.13, 2.46, "Amazon (OKAYASU)", spec="Perimeter seal (~10 m) + housing-surround ring (~6 m) + 2× vertical cut seals at Yd180/2287 (~5 m)", part_no="B089GJQ96Z", url="https://www.amazon.com/dp/B089GJQ96Z"),
    Part("panel-u-channel", "Aluminum U-channel, 1/8-panel (per meter)", "aluminum",
         "panel", 40, "m", 3, 5, "Online Metals", spec="Gasket retainer + 1/8\" HDPE-skin retention (perimeter + housing-surround + stiffener grid). SECTION: aluminum '1/8-panel' U-channel — inner slot ~3.2mm (captures the 3.18mm/PANEL_SKIN_T HDPE skin), ~10–12mm legs, ~1.5mm wall. TOTAL LENGTH: 40m (pick a stock 1/8-panel profile; only the 3.18mm slot is fixed by the skin)."),
    Part("panel-southco-latch", "Southco C2-33 cam compression latch", "fasteners-hardware",
         "panel", 4, "ea", 19, 26, "Southco", "McMaster-Carr", spec="Interior-mounted corner latches (compress the perimeter + cut + lip seals)"),
    Part("panel-b2-bay", "1/8\" black HDPE sheet (48×96, ×2)", "plastics-sheet",
         "panel", 2, "sheet", 123.34, 123.34, "US Plastics", "TAP Plastics", part_no="46684",
         url="https://www.usplastic.com/catalog/item.aspx?itemid=136961&catid=705",
         spec="B2 punch-out bay — 4-wall light-tight tube (~890mm deep) around the housing (rev11); 4 walls, 2 per 4×8 sheet. 1/8\" HDPE nearest stock to 4mm (weld-compatible with the HDPE housing/drum); EPDM lip cut from the panel-epdm perimeter roll (not billed here). US Plastics 46684 $123.34/sheet."),
    Part("panel-paint", "Flat black paint (RAL 9005)", "adhesives-finishes",
         "panel", 1, "qt", 10, 20, "local", spec="Bay/weld touch-in (HDPE skins are pre-pigmented black)"),
    Part("panel-grab-handle", "304 SS D-grab pull handle (~300mm) + 2× M8 SS bolts + backing plate, matte-black", "fasteners-hardware",
         "panel", 1, "ea", 70, 90, "StrongAr Hardware", spec="Interior pull handle — through-bolted to the frame (§4.3). 304 chosen over 316 (~$186); interior / non-wet location.", url="https://www.strongarhardware.com/pro-line-series-ladder-pull-handle-back-to-back-matte-black-powder-coated-finish-316-exterior-grade-stainless-steel-alloy/"),

    # ═══ shelf (§7 chem-prep) — mirrors costing.SHELF → exact $203 ═══
    Part("shelf-phenolic-ply", "UV-coated white plywood (work surface)", "timber-ply",
         "shelf", 1, '4\'×8\' 18mm sheet', 73.28, 73.28, "Home Depot", part_no="BPI6WUV2I", url="https://www.homedepot.com/p/302874373",
         spec='Swaner 18mm × 4\'×8\' UV-coated white hardwood ply (1220×2440mm), cut to 300×600. UV-coated face gives a sealed, wipeable work surface — substitute for the phenolic concrete-form sheet (same purpose, readily stocked).'),
    Part("shelf-steel-shs", "25×25×3 mm steel SHS", "steel-structural",
         "shelf", 1, "lot", 30, 30, "Online Metals", "Metal Supermarkets", spec="6 m (frame + spill lip)"),
    Part("shelf-piano-hinge", "Continuous (piano) hinge, 600 mm", "fasteners-hardware",
         "shelf", 1, "ea", 23.56, 23.56, "Wurth Baer Supply", spec="Weld-on continuous piano hinge, 1-1/4\" open width (32 mm) × 23-5/8\" (600 mm) long, stainless/steel", dims="32mm open × 600mm", part_no="LSN8-32-600", url="https://wurthbaersupply.com/product/711558/1-1-4-WELD-ON-PIANO-HINGE-23-5-8-L-LSN8-32-600"),
    Part("shelf-folding-stays", "Folding shelf stays/brackets, zinc", "fasteners-hardware",
         "shelf", 2, "ea", 12, 12, "Amazon", "McMaster-Carr", spec="Zinc-plated steel folding shelf bracket (fold-flat, ~30–50 kg rating); qty 2 = 1 pair. Zinc chosen over stainless — mounting is dry/hidden, not splash-facing (Alvin 2026-08-01). ~$12 ea est; firm SKU + price at purchase."),
    Part("shelf-wall-cleat", "Wall mounting cleat + anchors", "steel-structural",
         "shelf", 1, "lot", 18, 18, "Local fab", spec="6 mm steel cleat + 2 stay anchors (slotted)"),
    Part("shelf-wall-backing", "Shelf mount backing plates, 8mm steel (welded, ×3)", "steel-structural",
         "shelf", 3, "ea", 6, 10, "Local fab", spec="Flat 8mm steel backing plates welded to the pinhole-wall interior crests — one behind the hinge cleat + one per stay anchor — giving flat, solid load anchors with M8 weld-nuts."),
    Part("bolt-m8-wall", "M8×1.25 × 25 hex bolt, Grade 8.8 zinc — shelf cleat + stay mount", "fasteners-hardware",
         "shelf", 12, "ea", 18.51 / 50, 18.51 / 50, "McMaster-Carr", part_no="91280A534", url="https://www.mcmaster.com/91280A534/", spec="Clamps the shelf hinge cleat (6mm) + 2 stay anchors to their welded 8mm backing plates (M8 weld-nut). Grip ≈ 14mm → M8×25. Pitch M8×1.25 coarse. $18.51/pack of 50 (same 91280A534 as the film ICP-14 fixing)."),
    Part("nut-m8-plain", "M8×1.25 hex nut, plain SS", "fasteners-hardware",
         "shelf", 12, "ea", 7.53 / 100, 7.53 / 100, "McMaster-Carr", part_no="90591A161", url="https://www.mcmaster.com/90591A161/", spec="Plain hex nut — shelf wall bolts. Pitch M8×1.25 coarse — confirmed vs 90591A161 PDF 2026-07-29 (matches the bolt). $7.53/pack of 100."),
    Part("washer-m8-flat", "M8 flat washer, SS", "fasteners-hardware",
         "shelf", 12, "ea", 3.32 / 100, 3.32 / 100, "McMaster-Carr", part_no="91166A270", url="https://www.mcmaster.com/91166A270/", spec="Flat washer (1/bolt) — shelf wall bolts. $3.32/pack of 100."),
    Part("shelf-transport-latch", "Transport latch (over-center/barrel), zinc", "fasteners-hardware",
         "shelf", 1, "ea", 8, 8, "Amazon", spec="Zinc over-center draw/toggle latch — secures the folded board for transport. Zinc (dry/hidden, not splash-facing — Alvin 2026-08-01). ~$8 est; firm SKU + price at purchase."),
    Part("bolt-m5x16-csk", "M5×16 countersunk screw, A2-70 SS", "fasteners-hardware",
         "shelf", 8, "ea", 11.54 / 100, 11.54 / 100, "McMaster-Carr", part_no="91420A326", url="https://www.mcmaster.com/91420A326/", spec="Ply panel attachment (same M5×16 CSK as the clamp clips — 91420A326)"),
    Part("shelf-gusset-plates", "Corner gusset plate, 3 mm", "steel-structural",
         "shelf", 4, "ea", 1.25, 1.25, "Steel offcut", spec="50×50 mm triangular"),
    Part("shelf-paint", "Flat black epoxy spray paint", "adhesives-finishes",
         "shelf", 1, "can", 12, 12, "Hardware store", spec="frame + hardware finish"),
    Part("shelf-pvc-pipe", '½" PVC Sch-40 pipe (tap relocation)', "plumbing-fittings",
         "shelf", 1, "stick", 4.81, 4.81, "Home Depot", part_no="30-05010HD", url="https://www.homedepot.com/p/319692959", spec="Extend the blue supply trunk ~1.3 m left to TAP-01 (PVC Sch-40, per the joint convention). IPEX ½\" × 10 ft — same stick as pvc-half; one covers the run."),

    # ═══ walkway (§10) — re-decomposed to match the report (fab bundled into each bracket, no
    # separate fab line) → $2,005–$2,985 (reconciles to EXPECTED walkway $2,000–$2,975 within tol) ═══
    Part("walkway-grp-panel", "Molded GRP grating (American Grating, cut-to-size)", "plastics-sheet",
         "walkway", 1, "lot", 830, 1050, "American Grating", "McNichols",
         spec="1\" MS-S-100 vinyl-ester grit, ~48 ft² cut to the walkway sections. PRIMARY: American Grating public list ≈ $830 (2× 3'×10' @ $415); band to $1,050 covers freight + edge cut — firm cut quote + SoCal freight still to confirm. SECONDARY (firm, shipped): McNichols 2× 48\"×144\" @ $796.77 = $1,593.54 + freight → $2,049.98 shipped (firm 2026-07-24) — ~2× the American list; held as the firm fallback while the American quote is pending. NB McNichols' sheet is 4'×12' (bigger than the American 3'×10'), so switching to it would re-nest the cut plan. Cut plan: grp-grating-quote.md."),
    Part("walkway-grp-sealant", "GRP grating edge-seal kit", "adhesives-finishes",
         "walkway", 1, "kit", 40, 60, "Fibergrate", spec="Fibergrate Sealing & Bonding Kit — molded FRP cut edges are field-SEALED (epoxy), not snap-trimmed; ½-pint kit seals ~20–40 linear ft of cut edge."),
    Part("walkway-drum-exit-grp", "Drum-exit punch-out grating", "plastics-sheet",
         "walkway", 1, "lot", 50, 65, "McNichols", spec="Extra GRP landing (~0.23 m²) at the light-lock exit"),
    Part("walkway-std-brackets", "Cantilever bracket — standard (near/far)", "steel-structural",
         "walkway", 13, "ea", 30, 50, "Local fab",
         spec="8mm steel plate: 150mm vert leg + 300mm arm + 70mm gusset, welded (4 near + 9 far at 457mm centers)"),
    Part("walkway-wide-brackets", "Cantilever bracket — widened (near)", "steel-structural",
         "walkway", 5, "ea", 40, 70, "Local fab",
         spec="10mm steel plate: 200mm vert leg + 500mm arm + 70mm gusset, welded (EP/battery/slit zone, X1055–3083 = 5 bays)"),
    Part("bolt-m12x65", "M12×65 hex through-bolt, Grade 8.8 zinc, partial-thread", "fasteners-hardware",
         "walkway", 59, "ea", 15.95 / 10, 15.95 / 10, "McMaster-Carr", part_no="91280A728",
         url="https://www.mcmaster.com/91280A728/",
         spec="Cantilever-bracket wall bolts (3 per std + 4 per widened), sized for the 30mm-corrugation grip (~48–50mm), partial thread. Pad with 1–2 M12 flat washers if the actual container corrugation is <30mm."),
    Part("nut-m12-plain", "M12 hex nut, plain", "fasteners-hardware",
         "walkway", 59, "ea", 12.78 / 50, 12.78 / 50, "McMaster-Carr", part_no="90591A181", url="https://www.mcmaster.com/90591A181/", spec="Plain hex nut — M12×65 cantilever bolts (+ split lock washer). $12.78/pack of 50. Pitch M12×1.75 coarse — confirmed vs 90591A181 PDF 2026-07-29."),
    Part("washer-m12-flat", "M12 flat washer, zinc", "fasteners-hardware",
         "walkway", 236, "ea", 9.71 / 100, 9.71 / 100, "McMaster-Carr", part_no="91166A290", url="https://www.mcmaster.com/91166a290/", spec="Flat washers, M12×65 cantilever bolts — 2 functional + 2 shim/bolt (shims pad the grip if corrugation <30mm)."),
    Part("washer-m12-split", "M12 split lock washer, zinc", "fasteners-hardware",
         "walkway", 59, "ea", 11.97 / 100, 11.97 / 100, "McMaster-Carr", part_no="91202A246", url="https://www.mcmaster.com/91202A246/", spec="Split lock washer under each nut — M12×65 cantilever bolts (plain nut + split = locked)."),
    Part("walkway-reinf-plates", "Reinforcing plate (exterior)", "steel-structural",
         "walkway", 18, "ea", 4.1667, 7.2222, "Local fab", spec="6mm steel: 100×180mm std (×13) + 120×220mm widened (×5)"),
    Part("walkway-transition-plates", "Transition bearing plate", "steel-structural",
         "walkway", 2, "ea", 2.5, 5, "Local fab", spec="40×500×5mm flat bar, welded to bracket arm top at width transitions"),
    Part("walkway-cantilever-frame", "Right walkway cantilever frame (long + end beams)", "steel-structural",
         "walkway", 1, "lot", 125, 153, "MetalsDepot", "Metal Supermarkets",
         spec="2×1×0.120in steel tube — 2 long beams ({{fact:container_width_mm}}mm) + 2 end beams (300mm) that make the closed rectangle, ~5.4 m (17.6 ft) of tube. The 2 center cantilever ARMS are a SEPARATE part (walkway-cantilever-arms) — a SOLID 2×1 flat bar, because each arm is half-lapped over both long beams and a notched HOLLOW tube opens into a weak channel (a notched partial section must be solid). Firm: MetalsDepot 2×1×0.120 $76.20/12ft stick ($6.35/ft) — 2 sticks (24 ft) cover the beams with spare; retail cut-to-size runs ~3× ($16.72/ft, Metal Supermarkets) so bulk-stick it. 2026-08-07."),
    Part("walkway-cantilever-arms", "Right walkway center cantilever arms (solid bar)", "steel-structural",
         "walkway", 2, "ea", 18, 30, "MetalsDepot", "Metal Supermarkets",
         spec="SOLID 2×1in (50.8×25.4mm) mild-steel flat bar, 325mm each — the 2 arms that pick the walkway rectangle up at mid-span off the IBC front uprights. Solid (not tube) so the half-lap notch keeps its strength: notch REBALANCED to the moment — deep arm notch at the tip (M≈30 Nm, arm keeps 5.4mm), shallow at the post end (M≈334 Nm, arm keeps 16mm — the outer beam takes the deep notch); both SF≈1.5+ (ibc_frame_load.arm_notch_check). MetalsDepot 2×1 rectangle bar ~$13/ft; a ~3ft cut covers both arms with spare. ESTIMATE — firm at fab."),
    Part("walkway-right-cleats", "Wall cleat (left corners)", "steel-structural",
         "walkway", 2, "ea", 10, 17.5, "Local fab", spec="8mm steel: back-plate + exterior plate + shelf, through-bolted to the wall"),
    Part("walkway-corner-plates", "Combined corner plate (right corners)", "steel-structural",
         "walkway", 2, "ea", 25, 40, "Local fab",
         spec="10mm steel, 150mm wide — carries the walkway right beam AND the bottom film rail"),
    Part("bolt-m12x70", "M12×70 hex through-bolt, Grade 8.8 zinc, partial-thread", "fasteners-hardware",
         "walkway", 20, "ea", 17.36 / 10, 17.36 / 10, "McMaster-Carr", part_no="91280A732",
         url="https://www.mcmaster.com/91280A732/",
         spec="Right-walkway wall cleats + combined corner plates, sized for the deepest 30mm-corrugation grip (~54mm), partial thread. (The 2 center arms no longer use these — they bolt via the J6 end-plate, see bolt-m12x100.) $17.36/pack of 10. Pad with 1–2 M12 flat washers if the actual container corrugation is <30mm."),
    Part("bolt-m12x100", "M12×100 hex through-bolt, Grade 8.8 zinc", "fasteners-hardware",
         "walkway", 8, "ea", 1.9, 2.4, "McMaster-Carr",
         spec="J6 walkway-arm end-plate joint — 4 per arm × 2 arms, through the front upright into the rear backing plate (a bolted moment couple over the 90mm bolt spacing). Runs with a nyloc nut + an internal crush sleeve so torque can't dish the hollow upright. ESTIMATE — firm SKU at fab."),
    Part("walkway-arm-endplates", "Walkway-arm end + backing plates (J6)", "steel-structural",
         "walkway", 4, "ea", 3, 6, "Local fab",
         spec="70×130×8mm mild-steel plate, 4× Ø13 for M12 at 30×90 pitch — 2 end-plates (welded to the arm ends) + 2 rear backing plates (plain), one set per arm. Cut+drill from A36 flat plate."),
    Part("walkway-arm-sleeves", "Walkway-arm J6 crush sleeves", "steel-structural",
         "walkway", 8, "ea", 0.75, 1.5, "Local fab",
         spec="Internal spacer/crush tube (~Ø14 ID over the M12) cut to the upright bore depth — one per J6 through-bolt (4/arm × 2) so tightening can't collapse the hollow RHS upright. Cut from steel tube offcut."),
    Part("nut-m12-plain", "M12 hex nut, plain", "fasteners-hardware",
         "walkway", 24, "ea", 12.78 / 50, 12.78 / 50, "McMaster-Carr", part_no="90591A181", url="https://www.mcmaster.com/90591A181/", spec="Plain hex nut — M12×70 right-walkway bolts (+ split lock washer). $12.78/pack of 50. Pitch M12×1.75 coarse — confirmed vs 90591A181 PDF 2026-07-29."),
    Part("washer-m12-flat", "M12 flat washer, zinc", "fasteners-hardware",
         "walkway", 96, "ea", 9.71 / 100, 9.71 / 100, "McMaster-Carr", part_no="91166A290", url="https://www.mcmaster.com/91166a290/", spec="Flat washers, M12×70 right-walkway bolts — 2 functional + 2 shim/bolt (shims pad the grip if corrugation <30mm)."),
    Part("washer-m12-split", "M12 split lock washer, zinc", "fasteners-hardware",
         "walkway", 24, "ea", 11.97 / 100, 11.97 / 100, "McMaster-Carr", part_no="91202A246", url="https://www.mcmaster.com/91202A246/", spec="Split lock washer under each nut — M12×70 right-walkway bolts (plain nut + split = locked)."),
    Part("walkway-floor-legs", "Floor-leg cantilever bracket (left walkway, ×5)", "steel-structural",
         "walkway", 5, "ea", 13, 21, "MetalsDepot", "Local fab",
         spec="2×2×0.120in SHS post (~115mm) + 2×1×0.120in arm (2 reach X470, 3 extended to X770) + 128×60×8mm foot plate. #26: arm 2×⅞→2×1 (2×⅞ non-stock); post 50→50.8 (2in). Material firm (MetalsDepot 2×1 $6.35/ft + 2×2 $22.99/ft ret); cut/weld fab deferred to a shop quote."),
    Part("walkway-floor-anchors", "Self-drilling structural screw, #14×2″ HWH, 410 SS", "fasteners-hardware",
         "walkway", 20, "ea", 0.35, 0.55, "Bridge Fasteners", "ASMC",
         url="https://www.bridgefasteners.com/products/14-x-2-hex-washer-head-self-drilling-screws-410-stainless-steel-self-tapping-full-thread",
         spec="4 per foot plate (20 total). Self-drills the 6mm plate + 28mm plywood (structural bite in the ply — wedge/concrete anchors don't hold in a ply-over-steel container floor). Hex washer head bears on the plate. 410 SS. Simpson SDWS 316 (pre-drilled plate holes) if max corrosion is wanted."),
    Part("walkway-holddown-clips", "Grating clips", "fasteners-hardware",
         "walkway", 30, "ea", 1, 1.6667, "McNichols", "McMaster-Carr", spec="Removable spring clips, stainless"),
]


# ── Chemistry (cyanotype, tier-tagged) — PRELIMINARY (subject to sensitizer-trials.md) ──
# Built from costing's tier model + price constants so they can never drift from the cost source.
# Only the cyanotype (chosen) process is in the registry; the alt-process comparison is the
# process-comparison.md Research doc. Each reagent is tagged by tier; only the DEFAULT tier (+ the
# tier-less muslin) enters the build views (master / grand) — the other tiers are alternatives.
def _chem_parts() -> list[Part]:
    out = []
    for t in costing.TIERS:
        out.append(Part(f"amfe-{t.key}", "Ferric ammonium oxalate (AmFe)", "chemistry-reagents",
                        "chemistry", t.amfe_kg, "kg", costing.PRICE_AMFE_PER_KG, costing.PRICE_AMFE_PER_KG,
                        "Artcraft Chemicals", "Photographers' Formulary",
                        url="https://artcraftchemicals.com/products/ferric-ammonium-oxalate-part-1684?variant=42896857825527",
                        spec="Part A (Ware New Cyanotype sensitizer); warm water to dissolve. $29.12/1 lb (Artcraft Chemicals, confirmed 2026-07-26) = $64.20/kg (Class 6.1, UPS Ground only; bulk quote likely lower than 1-lb packs).", tier=t.key))
        out.append(Part(f"ferri-{t.key}", "Potassium ferricyanide", "chemistry-reagents",
                        "chemistry", t.ferri_kg, "kg", costing.PRICE_FERRI_PER_KG, costing.PRICE_FERRI_PER_KG,
                        "Artcraft Chemicals", url="https://artcraftchemicals.com/products/potassium-ferricyanide-part-1275",
                        spec="Part B (Ware New Cyanotype). $104.12/4.5 lb (Artcraft Chemicals, firm 2026-07-26) = $51.01/kg.", tier=t.key))
        out.append(Part(f"dichromate-{t.key}", "Ammonium dichromate", "chemistry-reagents",
                        "chemistry", 1, "run", costing.DICHROMATE_RUN, costing.DICHROMATE_RUN,
                        "Artcraft Chemicals", url="https://artcraftchemicals.com/products/ammonium-bi-dichromate-part-1022",
                        spec="Part B additive; contrast enhancer (Cat-1A carcinogen — handle with care). $33.66/0.5 lb (Artcraft Chemicals, firm 2026-07-26); trace use, ~$25/run allowance (one 0.5-lb pack per run).", tier=t.key))
    out.append(Part("muslin", 'Unbleached muslin, 60" wide', "substrate-fabric",
                    "chemistry", costing.MUSLIN_ROLLS, "roll", costing.MUSLIN_ROLL_PRICE, costing.MUSLIN_ROLL_PRICE,
                    "Fabric Direct", url="https://www.fabricdirect.com/shop/craft-fabric/broadcloth-and-muslin-fabric/essence-60-medium-weight-muslin-fabric-unbleached-150-yard-roll/",
                    spec=f"150-yd roll; ~{costing.MUSLIN_YARDS} yd for {costing.PRINTS} prints (+15% waste)"))
    return out


PARTS.extend(_chem_parts())


# ── Roll-ups ─────────────────────────────────────────────────────────────────
def _in_build(p: Part) -> bool:
    """Tier-tagged alternatives (lean/rich) are NOT in the build — only the default tier + tier-less."""
    return (not p.tier) or p.tier == costing.DEFAULT_TIER


def systems() -> list[str]:
    return sorted({p.system for p in PARTS if _in_build(p)})


def by_system(sys: str) -> list[Part]:
    return [p for p in PARTS if p.system == sys and _in_build(p)]


def system_total(sys: str) -> tuple[int, int]:
    lo = sum(line(p)[0] for p in by_system(sys))
    hi = sum(line(p)[1] for p in by_system(sys))
    return (round(lo), round(hi))


def grand() -> tuple[int, int]:
    return (round(sum(line(p)[0] for p in PARTS if _in_build(p))),
            round(sum(line(p)[1] for p in PARTS if _in_build(p))))


def by_type() -> dict[str, list[Part]]:
    out: dict[str, list[Part]] = {}
    for p in PARTS:
        if _in_build(p):
            out.setdefault(p.type, []).append(p)
    return out


# Canonical supplier names — fold case/spelling variants so the by-supplier consolidation aggregates
# correctly. The distinct local shops (structural fab / sheet-metal / plastic fab) stay separate —
# they're different vendors a buyer quotes independently.
_SUPPLIER_CANON = {
    "local fab": "Local fab", "local": "Local fab",
    "local sheet metal": "Local sheet metal", "lumber yard": "Lumber yard",
    "steel service center": "Steel service center", "local depot": "Local depot",
}


def canon_supplier(s: str) -> str:
    return _SUPPLIER_CANON.get(s, s)


def by_supplier() -> dict[str, list[Part]]:
    out: dict[str, list[Part]] = {}
    for p in PARTS:
        if _in_build(p):
            out.setdefault(canon_supplier(p.supplier) or "—", []).append(p)
    return out


def chemistry_parts() -> list[Part]:
    return [p for p in PARTS if p.system == "chemistry"]


def emit_chemistry() -> str:
    """The cyanotype shopping table — per-tier reagents + substrate, computed from costing's tiers."""
    by = {(p.tier, p.desc): p for p in chemistry_parts()}
    muslin = next(p for p in chemistry_parts() if p.key == "muslin")
    tiers = costing.TIERS
    hdr = "| Reagent | Supplier | " + " | ".join(
        f"{t.label}{' (default)' if t.key == costing.DEFAULT_TIER else ''}" for t in tiers) + " |"
    rows = [hdr, "|" + "---|" * (len(tiers) + 2)]
    for desc, sup in (("Ferric ammonium oxalate (AmFe)", "Artcraft Chemicals"),
                      ("Potassium ferricyanide", "Artcraft Chemicals"),
                      ("Ammonium dichromate", "Artcraft Chemicals")):
        cells = []
        for t in tiers:
            p = by[(t.key, desc)]
            lo = line(p)[0]
            cells.append(f"{p.qty:g} {p.unit} / {_money(lo)}" if p.unit == "kg" else _money(lo))
        rows.append(f"| {desc} | {sup} | " + " | ".join(cells) + " |")
    chem = [f"**{_money(costing.tier_costs(t)['chem_subtotal'])}**" for t in tiers]
    rows.append("| **Chemistry subtotal** | | " + " | ".join(chem) + " |")
    rows.append(f"| Unbleached muslin (substrate) | Fabric Direct | "
                + " | ".join(_money(line(muslin)[0]) for _ in tiers) + " |")
    tot = [f"**{_money(costing.tier_costs(t)['section_total'])}**" for t in tiers]
    rows.append("| **Total (50 prints)** | | " + " | ".join(tot) + " |")
    pp = [f"**{_money(costing.tier_costs(t)['per_print'])}**" for t in tiers]
    rows.append("| **Per print** | | " + " | ".join(pp) + " |")
    return "\n".join(rows)


# ── Emitters (markdown) ──────────────────────────────────────────────────────
def _money(v: float) -> str:
    return f"${round(v):,}"


import facts as _facts # live fact-marker expansion inside generated spec cells

_FACT_TOKEN = re.compile(r"\{\{fact:([a-z0-9_]+)\}\}")


def _expand(text: str) -> str:
    """Expand {{fact:KEY}} tokens to a live fact marker carrying the CURRENT value, so a generated
    parts block can restate a single-sourced fact without freezing it: parts.py --inject and
    facts.py --inject then write the identical string, and both lint gates stay consistent."""
    return _FACT_TOKEN.sub(
        lambda m: f"<!-- BEGIN fact:{m.group(1)} -->{_facts._fmt(_facts.FACTS[m.group(1)])}"
                  f"<!-- END fact:{m.group(1)} -->", text)


def _item_cell(p: Part) -> str:
    """Item name, hyperlinked to the part URL when the registry carries one; part_no appended."""
    name = f"[{p.desc}]({p.url})" if p.url else p.desc
    return f"{name} ({p.part_no})" if p.part_no else name


def emit_system(sys: str) -> str:
    """A report's §Parts-List (by-system view). Registry insertion order (faithful to the report);
    renders spec + URL-linked item + qty + supplier(+alt) + cost band + a system-total row."""
    rows = ["| Item | Spec | Qty | Supplier | Est. cost |", "|------|------|-----|----------|-----------|"]
    for p in by_system(sys): # insertion order, not type-sorted
        lo, hi = line(p)
        cost = _money(lo) if round(lo) == round(hi) else f"{_money(lo)}–{_money(hi)}"
        sup = canon_supplier(p.supplier) + (f" / {canon_supplier(p.supplier_alt)}" if p.supplier_alt else "")
        rows.append(f"| {_item_cell(p)} | {_expand(p.spec) or '—'} | {p.qty:g} {p.unit} | {sup} | {cost} |")
    lo, hi = system_total(sys)
    tot = _money(lo) if lo == hi else f"{_money(lo)}–{_money(hi)}"
    rows.append(f"| **{sys.title()} total** | | | | **{tot}** |")
    return "\n".join(rows)


def emit_panel(panel: str) -> str:
    """plumbing-report.md per-panel §Parts-List — the water-system equipment tagged to this plumbing
    panel (Corridor / Pinhole Wall). Panel-mounted equipment only; the full water BOM (pipe, totes,
    external ports, consumables) lives in water-system-report.md's §Parts-List."""
    items = [p for p in by_system("water") if p.panel == panel]
    rows = ["| Item | Spec | Qty | Supplier | Est. cost |", "|------|------|-----|----------|-----------|"]
    lo_t = hi_t = 0.0
    for p in items:
        lo, hi = line(p); lo_t += lo; hi_t += hi
        cost = _money(lo) if round(lo) == round(hi) else f"{_money(lo)}–{_money(hi)}"
        sup = canon_supplier(p.supplier) + (f" / {canon_supplier(p.supplier_alt)}" if p.supplier_alt else "")
        rows.append(f"| {_item_cell(p)} | {_expand(p.spec) or '—'} | {p.qty:g} {p.unit} | {sup} | {cost} |")
    tot = _money(lo_t) if round(lo_t) == round(hi_t) else f"{_money(lo_t)}–{_money(hi_t)}"
    rows.append(f"| **{panel} Plumbing Panel total** | | | | **{tot}** |")
    return "\n".join(rows)


def emit_master() -> str:
    """The by-TYPE procurement BOM + the supplier-consolidation headline. Type sections and the rows
    within each are ordered ALPHABETICALLY (the table cuts across systems, so name is easiest to scan;
    the published tables are also click-sortable by any column)."""
    bt = by_type()
    out = ["## Procurement BOM — by material type\n"]
    for t in sorted(bt): # type sections A–Z
        items = bt[t]
        out.append(f"### {t}\n")
        out.append("| Item | Qty | Supplier | Systems | Est. cost |")
        out.append("|------|-----|----------|---------|-----------|")
        # aggregate the same key across systems (identity fields — desc/url/part_no/supplier — are
        # shared by every row of a key, so keep a representative Part `p` to render the item cell)
        agg: dict[str, dict] = {}
        for p in items:
            a = agg.setdefault(p.key, {"p": p, "qty": 0.0, "unit": p.unit,
                                       "sup": canon_supplier(p.supplier), "sys": set(), "lo": 0.0, "hi": 0.0})
            a["qty"] += p.qty
            a["sys"].add(p.system)
            lo, hi = line(p); a["lo"] += lo; a["hi"] += hi
        sub_lo = sub_hi = 0.0
        # Fasteners read as a purchasing block: bolts (by size×length) → washers → nuts → other
        # hardware, each by thread size (M5<M6<…). Other type sections stay A–Z by item name.
        def _fsort(x):
            k = x["p"].key
            cls = 0 if k.startswith("bolt-") else 1 if k.startswith("washer-") else 2 if k.startswith("nut-") else 3
            mm = re.search(r"m(\d+)", k)
            return (cls, int(mm.group(1)) if mm else 999, k)
        order = (sorted(agg.values(), key=_fsort) if t == "fasteners-hardware"
                 else sorted(agg.values(), key=lambda x: x["p"].desc.lower()))
        for a in order: # rows A–Z by item name (fasteners: by class/size)
            cost = _money(a["lo"]) if round(a["lo"]) == round(a["hi"]) else f"{_money(a['lo'])}–{_money(a['hi'])}"
            out.append(f"| {_item_cell(a['p'])} | {a['qty']:g} {a['unit']} | {a['sup']} | "
                       f"{', '.join(sorted(a['sys']))} | {cost} |")
            sub_lo += a["lo"]; sub_hi += a["hi"]
        st = _money(sub_lo) if round(sub_lo) == round(sub_hi) else f"{_money(sub_lo)}–{_money(sub_hi)}"
        out.append(f"| **{t} subtotal** | | | | **{st}** |\n")
    # supplier consolidation
    out.append("## Supplier consolidation (largest orders first)\n")
    out.append("| Supplier | Line items | Types | Est. cost |")
    out.append("|----------|-----------|-------|-----------|")
    sup_rows = []
    for sup, items in by_supplier().items():
        lo = sum(line(p)[0] for p in items); hi = sum(line(p)[1] for p in items)
        types = sorted({p.type for p in items})
        sup_rows.append((sup, len(items), types, lo, hi))
    for sup, n, types, lo, hi in sorted(sup_rows, key=lambda r: -r[4]):
        cost = _money(lo) if round(lo) == round(hi) else f"{_money(lo)}–{_money(hi)}"
        out.append(f"| {sup} | {n} | {', '.join(types)} | {cost} |")
    return "\n".join(out)


# ── Block injection (docs ← registry) ────────────────────────────────────────
# Each generated view lives in a doc wrapped in `<!-- BEGIN parts:KEY -->` / `<!-- END parts:KEY -->`.
# Whole-block style: the table is regenerated entirely from the emitter. inject() rewrites it;
# the lint gate (check_blocks) blocks a commit if any block ever diverges from the registry.
_DOC_MASTER = "master-shopping-list.md"

# system → the report doc that carries its §Parts-List `parts:<system>` block (Phase 2b).
SYSTEM_DOC = {
    "water": "water-system-report.md", "electrical": "electrical-report.md",
    "ventilation": "ventilation-report.md", "film": "film-plane-mechanism-report.md",
    "panel": "hinged-panel-report.md", "lightlock": "hinged-panel-report.md",
    "swing": "hinged-panel-report.md", "door": "hinged-panel-report.md",
    "shelf": "chemistry-prep-shelves.md", "walkway": "walkway-report.md",
    "ibc-frame": "ibc-stacking-report.md",
    "tray": "processing-tray-and-spray-bar.md", "spray": "processing-tray-and-spray-bar.md",
    "clamp": "film-clamp-mechanism-report.md",
}
# Deliberately NOT block-generated (these systems live in the master BOM only, no per-report §Parts
# block): container + interior (project-level rollups), optics (pinhole §9 is an optical-ASSEMBLY
# spec — H7 bores / g6 fits / weld notes + an optional lens add-on, not a procurement table),
# electrical (§8 is a curated cross-system electrical+cooling summary, not a pure parts list).


# component-dimension-audit.md §1 findings — generated from the parts carrying size data, in this
# order. The registry IS the single source of the verified real-vs-modeled sizes; the doc's §2 detail
# (sources, reasoning) + §3 catalog checklist + §4 decision log stay hand-maintained narrative.
_AUDIT_ORDER = ["ibc-tote-1000l", "lifepo4-100ah", "shurflo-2088", "bigblue-housing",
                "axial-fan-150", "evap-cooler-mc18m", "seaflo-accumulator", "spray-al-shs"]


def emit_dimension_audit() -> str:
    by_key = {p.key: p for p in PARTS}
    rows = ["| # | Component | Real product (datasheet) | Modeled | Verdict |",
            "|---|-----------|--------------------------|---------|---------|"]
    for i, key in enumerate(_AUDIT_ORDER, 1):
        p = by_key[key]
        real = p.dims + (f" — {p.datasheet}" if p.datasheet else "")
        rows.append(f"| {i} | {p.desc} | {_expand(real)} | `{p.modeled_const}` | {_expand(p.audit_status)} |")
    return "\n".join(rows)


def _block_pat(key: str) -> "re.Pattern":
    return re.compile(r"(<!-- BEGIN parts:" + re.escape(key) + r" -->\n)(.*?)"
                      r"(\n<!-- END parts:" + re.escape(key) + r" -->)", re.DOTALL)


def _blocks() -> dict:
    """key -> (doc, emitter_fn). Only WIRED blocks are registered (added incrementally per phase)."""
    b = {"master": (_DOC_MASTER, emit_master),
         "dimension-audit": ("component-dimension-audit.md", emit_dimension_audit),
         "chemistry": ("chemistry-shopping-list.md", emit_chemistry)}
    # per-system §Parts-List blocks (Phase 2b) — only those already placed in their doc.
    for sys, doc in SYSTEM_DOC.items():
        b[sys] = (doc, lambda s=sys: emit_system(s))
    # plumbing-report.md per-panel sub-lists (the two-panel split — water equipment by panel)
    b["corridor-plumbing-panel"] = ("plumbing-report.md", lambda: emit_panel("Corridor"))
    b["pinhole-wall-plumbing-panel"] = ("plumbing-report.md", lambda: emit_panel("Pinhole Wall"))
    return b


def inject(write: bool = True) -> list:
    """Regenerate every marked parts: block. Returns (file, key, 'ok'|'updated'|'STALE'|'missing')."""
    out = []
    for key, (rel, fn) in _blocks().items():
        path = os.path.join(ROOT, rel)
        text = open(path, encoding="utf-8").read()
        pat = _block_pat(key)
        matches = list(pat.finditer(text))
        if not matches:
            out.append((rel, key, "missing"))
            continue
        body = fn()
        if all(m.group(2) == body for m in matches):
            out.append((rel, key, "ok"))
        elif write:
            open(path, "w", encoding="utf-8").write(
                pat.sub(lambda m: m.group(1) + body + m.group(3), text))
            out.append((rel, key, "updated"))
        else:
            out.append((rel, key, "STALE"))
    return out


def check_blocks() -> list:
    """Linter helper: list of placed parts: blocks that are stale (a missing marker is not an error —
    blocks are wired incrementally, so a doc without its marker yet is simply skipped)."""
    return [f"{rel} parts:{key} -> {st}" for rel, key, st in inject(write=False)
            if st not in ("ok", "missing")]


# ── Self-check (the migration guardrail) ─────────────────────────────────────
# reconciliation key: registry system → the costing.EXPECTED entry it must sum to.
# Defaults to the same name; only electrical maps to the differently-named 'power' rollup.
_RECONCILE = {"electrical": "power"}


def reconcile_key(sys: str) -> str:
    return _RECONCILE.get(sys, sys)


# costing's monolithic WATER list spans four reports; the registry splits it into four systems, each
# reconciled to its slice of WATER (the §8 group = WATER minus frame/tray/spray).
_WATER_SPLIT = {"ibc-frame": "IBC stacking frame", "tray": "Processing tray", "spray": "Spray bar"}
# costing.FILM bundles the muslin clamps (which physically live in film-clamp-mechanism-report); the
# registry splits them into a 'clamp' system, leaving 'film' = FILM minus these two lines.
_CLAMP_LINES = ("Muslin clamp",) # matches both "Muslin clamps …" (clamps) + "Muslin clamp filler …" (HDPE)


def _split_sum(lst, prefixes, keep: bool):
    sel = [li for li in lst if any(li.label.startswith(p) for p in prefixes) == keep]
    return (sum(li.low for li in sel), sum(li.high for li in sel))


def reconcile_target(sys: str):
    """The (low, high) the registry system must sum to."""
    if sys in _WATER_SPLIT:
        li = next(l for l in costing.WATER if l.label.startswith(_WATER_SPLIT[sys]))
        return (li.low, li.high)
    if sys == "water": # WATER minus the three split-out lines
        return _split_sum(costing.WATER, _WATER_SPLIT.values(), keep=False)
    if sys == "clamp": # the two clamp lines of FILM
        return _split_sum(costing.FILM, _CLAMP_LINES, keep=True)
    if sys == "film": # FILM minus the clamp lines
        return _split_sum(costing.FILM, _CLAMP_LINES, keep=False)
    if sys == "door": # the "Fixed door frame" lines of SWINGPIVOT
        return _split_sum(costing.SWINGPIVOT, ("Fixed door frame",), keep=True)
    if sys == "swing": # SWINGPIVOT minus the door lines
        return _split_sum(costing.SWINGPIVOT, ("Fixed door frame",), keep=False)
    if sys == "chemistry": # build = the DEFAULT tier total (+ muslin)
        tot = costing.EXPECTED[costing.DEFAULT_TIER]["total"]
        return (tot, tot)
    exp = costing.EXPECTED[reconcile_key(sys)]
    return (exp[0], exp[2]) if len(exp) == 3 else exp


def _check_chemistry() -> list[str]:
    """Each tier's reagents must sum to costing.EXPECTED[tier]['chem']; muslin to EXPECTED['muslin']."""
    errs = []
    for t in costing.TIERS:
        chem = round(sum(line(p)[0] for p in chemistry_parts() if p.tier == t.key))
        exp = costing.EXPECTED[t.key]["chem"]
        if abs(chem - exp) > 2:
            errs.append(f"chemistry {t.key}: registry ${chem} != costing.EXPECTED ${exp}")
    muslin = round(line(next(p for p in chemistry_parts() if p.key == "muslin"))[0])
    if muslin != costing.EXPECTED["muslin"]:
        errs.append(f"chemistry muslin: registry ${muslin} != ${costing.EXPECTED['muslin']}")
    return errs


def self_check() -> list[str]:
    """Every migrated system must sum to its costing reconcile target (±$10 absorbs rounding)."""
    special = set(_WATER_SPLIT) | {"water", "clamp", "film", "swing", "door", "chemistry"}
    errs = []
    for sys in systems():
        key = reconcile_key(sys)
        if sys not in special and key not in costing.EXPECTED:
            errs.append(f"{sys}: no costing.EXPECTED['{key}'] to reconcile against")
            continue
        tgt = reconcile_target(sys)
        got = system_total(sys)
        if abs(got[0] - tgt[0]) > 10 or abs(got[1] - tgt[1]) > 10:
            errs.append(f"{sys}: registry {got} != costing target {tgt}")
    return errs + _check_chemistry()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="reconcile each migrated system vs costing")
    ap.add_argument("--system", help="print a system's parts table")
    ap.add_argument("--master", action="store_true", help="print the by-type procurement BOM")
    ap.add_argument("--inject", action="store_true", help="rewrite every placed parts: doc block")
    ap.add_argument("--check-blocks", action="store_true", help="list any stale parts: doc block")
    args = ap.parse_args()
    if args.inject:
        for rel, key, st in inject(write=True):
            print(f" [{st:>7}] {rel} parts:{key}")
        raise SystemExit(0)
    if args.check_blocks:
        probs = check_blocks()
        print("\n".join(f" STALE: {p}" for p in probs) if probs else "✓ all parts: doc blocks current")
        raise SystemExit(1 if probs else 0)
    if args.check or not (args.system or args.master):
        errs = self_check()
        if errs:
            print("✗ parts registry reconciliation FAILED:")
            [print(" -", e) for e in errs]
            raise SystemExit(1)
        print(f"✓ parts registry reconciles with costing ({len(systems())} system(s): {', '.join(systems())})")
    if args.system:
        print(emit_system(args.system))
    if args.master:
        print(emit_master())
