#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""parts.py — the UNIFIED PARTS REGISTRY (drift-reduction Phase 5).

The single source of every purchasable item: quantity, type, supplier, unit-cost band, the
verified physical SIZE (folds in component-dimension-audit), and the cyanotype chemistry tiers.

From this ONE source, GENERATED views:
  • master-shopping-list.md     — by TYPE, qty summed across systems, grouped by SUPPLIER (procurement).
  • each report's §Parts-List    — by SYSTEM (emit_system).
  • component-dimension-audit.md — real-vs-modeled size reconciliation (emit_dimension_audit).
  • chemistry-shopping-list.md   — cyanotype-only shopping (emit_chemistry).
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
#   1. python3 src/generators/build_parts_worklist.py   → (re)generates parts-worklist.csv (merges fills)
#   2. fill the new_* columns from your logged-in supplier session (SKU, URL, fit dims, price)
#   3. python3 src/generators/apply_parts_csv.py parts-worklist.csv   → writes them back here, scoped
#   4. python3 src/generators/parts.py --inject + costing.py --inject + lint.py   → cascade + prove
# A band edit cascades automatically (master/report/cost blocks regenerate; costing reconciliation
# gate proves consistency). Update the master header's "Basis:" line when the refresh completes.
# ─────────────────────────────────────────────────────────────────────────────────────────────
"""
from __future__ import annotations
import argparse
import os
import re
from dataclasses import dataclass

import costing  # reconciliation guardrail (EXPECTED) + the cost cascade it still owns
from tbs_constants import CLAMP_N_TOTAL, CLAMP_FILLER_D  # muslin clamp count (3 edges) + L-channel filler depth

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ── The part record ──────────────────────────────────────────────────────────
@dataclass(frozen=True)
class Part:
    key: str            # stable identity — the SAME physical part shares one key across systems,
    desc: str           #   so the by-type view sums its qty (e.g. 'm12x90-ss-bolt').
    type: str           # taxonomy category (see TYPES)
    system: str         # owning report section ('ventilation', 'water', 'electrical', …)
    qty: float          # quantity in this system
    unit: str           # 'ea' | 'm' | 'sheet' | 'roll' | 'lot' | 'job' | 'kg' | …
    low: float          # UNIT cost band (line cost = qty × unit band)
    high: float
    supplier: str = ""        # primary supplier
    supplier_alt: str = ""    # fallback supplier
    url: str = ""
    part_no: str = ""
    spec: str = ""
    note: str = ""
    # sizing — folded-in component-dimension-audit (optional; sized/clash-relevant components only)
    dims: str = ""            # verified physical envelope from the datasheet, e.g. '330×172×214'
    datasheet: str = ""       # datasheet / catalog source
    modeled_const: str = ""   # tbs_constants name(s) holding the modeled size (real-vs-modeled check)
    audit_status: str = ""    # ✅ FIXED | ⚠ OPEN | confirm
    # chemistry — folded-in cyanotype shopping (optional)
    tier: str = ""            # '' | 'lean' | 'standard' | 'rich'
    # plumbing-panel split (water system only) — keyword-only so existing positional calls are unaffected
    panel: str = ""           # '' | 'Corridor' | 'Pinhole Wall' — drives the per-panel sub-lists in plumbing-report.md


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
PARTS: list[Part] = [
    # ═══ ventilation (§5b) — proves the schema; sums to EXPECTED['ventilation'] = 824 ═══
    Part("axial-fan-150", "150×150×50mm axial fans", "ducting-ventilation",
         "ventilation", 2, "ea", 25, 25, "Amazon", spec="12V DC, ~150–200 CFM each (GDSTIME/Wathai 15050)",
         dims="150×150×50", modeled_const="FAN_DIAM/FAN_BODY_D", audit_status="✅ FIXED"),
    Part("evap-cooler-mc18m", "Evaporative cooler", "ducting-ventilation",
         "ventilation", 1, "ea", 185, 230, "Hessaire", "Amazon",
         url="https://hessaire.com/mobile-cooling/1300-cfm-mobile-cooler",
         spec="Hessaire MC18M, 120V AC, {{fact:cooler_cfm_rated}} CFM (run low), {{fact:evap_cooler_w_ac}}W",
         dims="508×254×711", datasheet="Hessaire MC18M", modeled_const="EVAP_W/EVAP_D/EVAP_H",
         audit_status="✅ RESOLVED"),
    Part("cooler-inverter", "Cooler inverter — Victron Phoenix 12/375 GFCI", "electrical-power", "ventilation", 1, "ea", 132.60, 132.60,
         "Inverter Supply", "PKYS", part_no="PIN123750510", url="https://www.invertersupply.com/index.php?main_page=product_info&products_id=200695",
         spec="Victron Phoenix 12/375 120V VE.Direct GFCI (12V→120V, 375VA/300W) — GFCI in the faceplate outlet satisfies the wet-cooler requirement (no separate GFCI needed). Firm $132.60."),
    Part("shade-cloth-80", "Shade canopy — 80% shade cloth", "fabric-textile",
         "ventilation", 1, "ea", 80, 80, "Amazon", "Farm supply", spec="20 × 10 ft"),
    Part("canopy-frame-emt", "Canopy frame", "steel-structural",
         "ventilation", 1, "lot", 120, 120, "Home Depot", spec='1.5" EMT conduit + fittings'),
    Part("baffle-metal-fan", "Baffle duct sheet metal (fans)", "steel-structural",
         "ventilation", 1, "lot", 30, 30, "Local sheet metal", "Home Depot", spec="22 ga galvanized, 2 × 300mm stubs"),
    Part("baffle-metal-cooler", "Baffle duct sheet metal (cooler)", "steel-structural",
         "ventilation", 1, "lot", 20, 20, "Local sheet metal", "Home Depot", spec="22 ga galvanized, 1 × 300mm stub, Ø200mm"),
    Part("flex-duct-200", "200mm insulated flex duct", "ducting-ventilation",
         "ventilation", 1, "ea", 22, 22, "Home Depot", "McMaster-Carr", spec="Ø200mm × 1.2m, aluminum foil jacket"),
    Part("duct-elbow-200", "200mm 90° duct elbow", "ducting-ventilation",
         "ventilation", 1, "ea", 14, 14, "Home Depot", spec='Ø200mm (8") galvanized, cooler riser to wall stub'),
    Part("duct-collar-clamp", "Duct collar + hose clamp", "ducting-ventilation",
         "ventilation", 1, "ea", 12, 12, "Home Depot", spec="Ø200mm, galvanized"),
    Part("duct-cap-200", "Weatherproof duct cap", "ducting-ventilation",
         "ventilation", 1, "ea", 8, 8, "Home Depot", spec="Ø200mm, removable"),
    Part("deutsch-dt-2pin", "Deutsch DT 2-pin connectors", "electrical-distribution",
         "ventilation", 2, "set", 4, 4, "Waytek Wire", spec="Fan B flex connector (×2 sets)"),
    Part("coiled-cable-16awg", "16 AWG silicone coiled cable", "electrical-distribution",
         "ventilation", 1, "ea", 15, 15, "Waytek Wire", "Amazon", spec="1m, 2-conductor (Fan B flex)"),
    Part("cooler-power-cable", "Cooler external power cable", "electrical-distribution",
         "ventilation", 1, "ea", 20, 20, "Waytek Wire", "Amazon", spec="1.5m, 14 AWG 2-cond, Deutsch DT 2-pin plugs each end"),
    Part("ratchet-strap-25", "Ratchet straps, 25mm", "fasteners-hardware",
         "ventilation", 2, "ea", 6, 6, "Home Depot", "Amazon", spec="Cooler stowage"),
    Part("plywood-base-12", "Plywood base plate (cooler stowage)", "timber-ply",
         "ventilation", 1, '2\'×4\' ½" panel', 8, 8, "Home Depot", "Lumber yard",
         spec='½" (12mm) plywood project panel (610×1220mm), cut to 600×350'),

    # ═══ water family (split per owning report; reconciled to costing.WATER lines — water-system §8
    # item-sums after the 2026 reconciliation). The §8 group ("water") = storage+pumps+filter+valves+
    # pipe+wiring+consumables; the frame/tray/spray are SEPARATE systems (their own reports). ═══
    # — storage (395–720) —
    Part("ibc-tote-1000l", "IBC tote (1,000 L caged)", "water-equipment",
         "water", 4, "ea", 150, 150, "SoCal reconditioner", "Repackify",
         url="https://www.repackify.com/buy-ibc-totes/california",
         spec="Reconditioned food-grade (prior-food-contents) 275-gal/1000L caged composite tote, DN50 butterfly valve (S60×6 thread); side-entry fittings near top. ~$150/ea local SoCal (Container Exchanger food-grade lots have a ~12-tote min; buy 4 local). Firm ~$150.",
         dims="1219×1016×1168", modeled_const="IBC_W/IBC_D/IBC_H_1000", audit_status="✅ FIXED (v2)"),
    Part("bulkhead-2in", 'Bulkhead fitting 2" NPT (304 SS)', "plumbing-fittings",
         "water", 3, "ea", 136.70, 136.70, "McMaster-Carr", part_no="4464K115",
         url="https://www.mcmaster.com/4464K115", spec="External fill/drain port, welded through container wall",
         note="Price verified 2026-07-12 (McMaster 4464K115, $136.70 ea)."),
    # — pumps (315–345) —
    Part("shurflo-2088-p1", "Shurflo 2088-554-144 pump (P-01 Blue supply)", "water-equipment",
         "water", 1, "ea", 80, 89, "Fresh Water Systems", "Amazon",
         url="https://www.amazon.com/Shurflo-2088-554-144-Fresh-Gallons-Minute/dp/B00C1M6B1C",
         spec='12VDC, 3.5 GPM, 45 PSI, 1/2" NPSM ports',
         dims="216×127×114", datasheet="Shurflo 2088-554-144", modeled_const="PUMP_D×PUMP_YD_SPAN×Z",
         audit_status="✅ FIXED (minor) — protrusion PUMP_D 100→114", panel="Corridor"),
    Part("shurflo-2088-p2", "Shurflo 2088-554-144 pump (P-02 filter loop)", "water-equipment",
         "water", 1, "ea", 80, 89, "Fresh Water Systems", "Amazon",
         url="https://www.amazon.com/Shurflo-2088-554-144-Fresh-Gallons-Minute/dp/B00C1M6B1C",
         spec='12VDC, 3.5 GPM, 45 PSI, 1/2" NPSM ports', panel="Pinhole Wall"),
    Part("shurflo-2088-p3", "Shurflo 2088-554-144 pump (P-03 waste evacuation)", "water-equipment",
         "water", 1, "ea", 80, 89, "Fresh Water Systems", "Amazon", spec="12VDC, 3.5 GPM, 45 PSI; empties IBC-4 residual below X4 (~120L)", panel="Corridor"),
    Part("shurflo-2088-p4", "Shurflo 2088-554-144 pump (P-04 tray drain transfer)", "water-equipment",
         "water", 1, "ea", 80, 89, "Fresh Water Systems", "Amazon", spec="12VDC, 3.5 GPM, 45 PSI; tray drain to IBC-3 (~900mm lift)", panel="Corridor"),
    Part("shurflo-2088-p5", "Shurflo 2088-554-144 pump (P-05 Brown drain)", "water-equipment",
         "water", 1, "ea", 80, 89, "Fresh Water Systems", "Amazon", spec="12VDC, 3.5 GPM, 45 PSI; evacuates IBC-3 (Brown) residual to the X3 end-wall port", panel="Corridor"),
    Part("seaflo-accumulator", "SeaFlo accumulator (0.75 L)", "water-equipment",
         "water", 1, "ea", 30, 41, "Environmental Marine", "Amazon",
         url="https://www.amazon.com/Seaflo-Accumulator-Control-Internal-Bladder/dp/B01MUYL8F8",
         spec='0.75 L, 125 PSI, 1/2" MNPT', part_no="SFAT-075-125-01",
         dims="200×127×125", datasheet="SeaFlo SFAT-075-125-01", modeled_const="Ø127×200 cyl",
         audit_status="✅ FIXED — cylinder 150→200", panel="Corridor"),
    Part("shurflo-bracket", "Shurflo pump mounting bracket", "fasteners-hardware",
         "water", 5, "ea", 10, 10, "Amazon", spec="Stainless, 2088 series — one per pump (P-01..P-05)"),
    # — corridor plumbing-panel structure (3D-derived marine ply; previously uncosted) —
    Part("corridor-panel-ply-18", "Corridor plumbing-panel marine ply (18mm)", "timber-ply",
         "water", 1, "sheet", 179, 250, "Public Lumber", "Woodworkers Source",
         url="https://publiclumber.com/products/3-4-18mm-4x8-hydrotek-marine-plywood",
         spec='4×8 ft 18mm Hydrotek marine plywood (BS 1088 equiv) — rear backing board + drain-riser spine + spacer offcuts; ~1.3 m² used. $250 Public Lumber SoCal / $179 Woodworkers Source AZ. ⚠ MARINE IS ~3-4× standard: a plumbing backboard sees no marine loads — exterior BC/ACX (~$55-70/sheet) would cut this ~$130-190. Decision open.',
         panel="Corridor"),
    Part("corridor-panel-ply-25", "Pump-mount shirt marine ply (25mm)", "timber-ply",
         "water", 1, "piece", 212, 212, "Dunn Lumber",
         url="https://www.dunnlumber.com/marine-grade-abx-1-inches-softwood-face-plywood-4-feet-x-8-feet-net-thickness-1-16-inches-marineab1.html",
         spec='1" (25mm) AB marine plywood 4×8, ~610×1650 cut piece — pump-mount shirt behind P-01..P-05 + 6× spacer blocks. Firm $211.88 Dunn Lumber. ⚠ MARINE premium — exterior AC ply would cut this substantially (see ply-18). Decision open.',
         panel="Corridor"),
    Part("corridor-panel-mount", "Corridor panel mount hardware (brackets + fasteners)", "fasteners-hardware",
         "water", 1, "lot", 25, 50, "Home Depot",
         spec='6× steel angle brackets (panel → IBC-frame front-portal uprights), shirt-to-panel screws, lag bolts. Price est.',
         panel="Corridor"),
    # — filter (286–485): 3 separate 4.5×20 housings on a slotted-angle skid frame (§3.1/§7.2) —
    Part("bigblue-housing", 'Big Blue filter housing 4.5"×20" (separate)', "water-equipment",
         "water", 3, "ea", 38, 62, "AllFilters", "Amazon", dims="Ø184×594",
         spec='Ø184×594mm/housing (4.5×20), 1" NPT ports — three SEPARATE housings on the slotted-angle skid frame (Pentek / iSpring / Geekpure)',
         datasheet="Pentek 4.5×20 BB", modeled_const="BB_OD/BB_H",
         audit_status="3-separate design of record (2026-07): combo → 3 separate housings + frame per plumbing-report §3.1/§7.2. Prices indicative — firm at the Aug-2026 re-price.", panel="Pinhole Wall"),
    Part("filter-skid-frame", "Slotted steel angle frame 25×25×3mm (filter skid)", "water-equipment",
         "water", 1, "lot", 25, 45, "Home Depot", spec="~2.5 m 25×25×3mm slotted steel angle + fasteners; bolts to the 18mm ply backing (adjustable housing height)", panel="Pinhole Wall"),
    # filter-ubracket RETIRED 2026-07-22 — Big Blue housings have mounting-hole ears; lag-screw straight to the ply backing
    Part("filter-lag-screws", "SS lag/wood screws — filter housings to ply backing", "fasteners-hardware",
         "water", 6, "ea", 0.5, 1.5, "Home Depot", spec="2 per housing × 3 — 5/16 SS lag/wood screws through the housing's mounting-hole ears into the 18mm plywood backing (no custom bracket). Pin SKU at order.", panel="Pinhole Wall"),
    Part("filter-hdpe-spacer", "HDPE spacer blocks 25mm (filter skid)", "water-equipment",
         "water", 1, "lot", 12, 22, "McMaster-Carr", spec="25mm HDPE standoff blocks between the housing's mounting ears and the ply backing — sump-bowl hang clearance (the housing lag-screws through them into the ply)", panel="Pinhole Wall"),
    Part("filter-jumper", '1" HDPE inter-housing jumpers', "plumbing-fittings",
         "water", 1, "lot", 18, 32, "Ferguson", spec='F-01 OUT→F-02 IN, F-02 OUT→F-03 IN — 1" HDPE + 90° elbows routed outside the bodies', panel="Pinhole Wall"),
    Part("cartridge-sediment", 'MPP 5-micron sediment cartridge 4.5"×20"', "water-equipment",
         "water", 2, "ea", 12, 20, "Amazon", spec="Melt-blown polypropylene depth filter (F-1 stage); ~50-print interval", panel="Pinhole Wall"),
    Part("cartridge-kdf", 'KDF-55 heavy-metal cartridge 4.5"×20"', "water-equipment",
         "water", 1, "ea", 65, 95, "FilterWay", "Amazon", spec="KDF-55 media for dissolved iron/metal removal (F-2 stage); ~60-print interval", panel="Pinhole Wall"),
    Part("cartridge-carbon", 'CTO carbon block cartridge 4.5"×20"', "water-equipment",
         "water", 2, "ea", 16, 30, "RonAqua", "Amazon", spec="Coconut shell activated carbon block (F-3 stage); ~40-print interval", panel="Pinhole Wall"),
    # — valves & fittings (333–567) —
    Part("valve-v050fp-corridor", 'Banjo V050FP ball valve 1/2" FNPT', "plumbing-fittings",
         "water", 3, "ea", 30, 45, "Barn Door Ag", "Amazon", spec="PP full-port quarter-turn; pump-suction isolation BV-01 (P-01), BV-02 (P-05), BV-06 (P-03)", panel="Corridor"),
    Part("valve-v050fp-wall", 'Banjo V050FP ball valve 1/2" FNPT', "plumbing-fittings",
         "water", 1, "ea", 30, 45, "Barn Door Ag", "Amazon", spec="PP full-port quarter-turn; pump-suction isolation BV-03 (P-02)", panel="Pinhole Wall"),
    Part("valve-v050fp-supply", 'Banjo V050FP ball valve 1/2" FNPT', "plumbing-fittings",
         "water", 2, "ea", 30, 45, "Barn Door Ag", "Amazon", spec="PP full-port; supply isolation BV-04 (TAP-01 chem tap), BV-05 (spray-bar feed)"),
    Part("valve-v100fp", 'Banjo V100FP ball valve 1" FNPT', "plumbing-fittings",
         "water", 6, "ea", 33, 55, "Barn Door Ag", "Amazon", spec="PP full-port; V1/V3/V4, VB1–VB3 (IBC fill/drain)"),
    Part("valve-3way-half", '3-way diverter valve 1/2" FNPT', "plumbing-fittings",
         "water", 1, "ea", 12, 22, "Amazon", spec="L/T-port HDPE-compatible; 3W-DV-02 (tray drain)", panel="Corridor"),
    Part("valve-3way-1in", '3-way diverter valve 1" FNPT', "plumbing-fittings",
         "water", 1, "ea", 18, 30, "Amazon", spec="L/T-port; 3W-DV-01 (filter output)", panel="Pinhole Wall"),
    Part("sample-tap-sv01", 'pH sample tap (SV-01) — 1/2" PP ball valve + barb spout + branch tee', "plumbing-fittings",
         "water", 1, "ea", 10, 18, "Amazon", spec='Filtered-water sample draw before 3W-DV-01; Banjo V050FP 1/2" PP ball valve + downturned 1/2" hose barb on a 1"×1/2" reducing branch tee, panel face above spill line', panel="Pinhole Wall"),
    Part("sample-tap-sv02", 'pH sample tap (SV-02) — 1/2" PP ball valve + barb spout + branch tee', "plumbing-fittings",
         "water", 1, "ea", 10, 18, "Amazon", spec="pH sample on the P-04 tray-drain discharge, before 3W-DV-02; same build as SV-01", panel="Corridor"),
    Part("camlock-2in", '2" polypropylene camlock pairs (M+F)', "plumbing-fittings",
         "water", 4, "pair", 5, 8, "Amazon", spec="External bulkhead connections (X1/X3/X4 + spare)"),
    Part("elbow-half", '1/2" NPT 90° elbow polypropylene', "plumbing-fittings",
         "water", 14, "ea", 2, 4, "Amazon", spec="All pump-driven run bends"),
    Part("elbow-el100", 'Banjo EL100-90 elbow 1" NPT', "plumbing-fittings",
         "water", 4, "ea", 4, 6, "Barn Door Ag", "Amazon", spec="PP 90°; IBC bends, filter outlet to DV-01"),
    Part("tee-half", '1/2" NPT polypropylene tee', "plumbing-fittings",
         "water", 6, "ea", 2, 4, "Amazon", spec="Blue suction/discharge tees, branches"),
    Part("tee-100", 'Banjo TEE100 equal tee 1" NPT', "plumbing-fittings",
         "water", 3, "ea", 5, 7, "Barn Door Ag", "Amazon", spec="PP; IBC drain tees (the X1 fill is now a 4-way cross)"),
    Part("cross-100", '1" NPT 4-way cross fitting', "plumbing-fittings",
         "water", 1, "ea", 8, 14, "Amazon", spec="X1 fresh-fill 4-way: X1 inlet + IBC-1 + IBC-2 + DV-01 blue recycle return (was a 3-way tee). Cost est."),
    Part("union-half", '1/2" NPT polypropylene union', "plumbing-fittings",
         "water", 6, "ea", 4, 6, "Amazon", spec="Maintenance disconnects on pump runs"),
    Part("bushing-reducer", '1/2"×1" NPT bushing reducer', "plumbing-fittings",
         "water", 1, "ea", 3, 5, "Amazon", spec="P-02 riser to F1 filter inlet"),
    Part("s60-adapter", 'S60×6 female-buttress → 2" NPT + 2→1" bushing', "plumbing-fittings",
         "water", 8, "ea", 14, 18, "CPP.parts", "Amazon", spec='IBC DN50 valve to 1" HDPE. The DN50 valve is a MALE S60×6, so the adapter is FEMALE S60×6 buttress × 2" male NPT PP (a 1" NPT-female config isn\'t stocked); add a 2→1" PP reducer bushing to land on 1" HDPE.', part_no="HMFN/20UD/027", url="https://us.cpp.parts/collections/fits-s60x6"),
    Part("blue-equalization-tie", '1" bulkhead tank-body fittings (Blue equalization cross-tie)', "plumbing-fittings",
         "water", 2, "ea", 6, 12, "Amazon", spec='Low tank-body penetration in each Blue tote (IBC-1 + IBC-2) for the 1" equalization cross-tie that self-balances the two Blue levels (run made from the 1" HDPE stock). Cost est.'),
    Part("check-valve-1in", '1" NPT spring check valve (CV1 — X1 gravity fill)', "plumbing-fittings",
         "water", 1, "ea", 8, 14, "Amazon", spec='PVC body, EPDM seal, 1" FNPT × FNPT. Only CV-1 (X1 fill) remains — the Shurflo 2088 pumps have integral check valves, so CV-2/CV-3/CV-4 are redundant and dropped'),
    Part("ribbon-support-beam", "Steel flat bar 25×3mm — ribbon support cross-brace", "steel-structural",
         "water", 4, "ea", 2, 4, "Home Depot", spec="Welded between the two right-walkway long bearers at 4 stations to carry the under-walkway pipe ribbon (the four corridor↔pinhole lines); ~300mm each", panel="Corridor"),
    Part("ribbon-pipe-clip", "Cushioned pipe clip", "fasteners-hardware",
         "water", 16, "ea", 1, 2, "Amazon", spec="Secures the four under-walkway ribbon lines to the support cross-braces (4 lines × 4 supports)", panel="Corridor"),
    Part("ptfe-tape", "Thread seal tape (PTFE)", "adhesives-finishes",
         "water", 4, "roll", 2, 2, "Home Depot", spec='1/2" wide, 260" roll'),
    # — pipe (80–114) —
    Part("hdpe-half", '1/2" SDR-11 HDPE pipe', "plumbing-fittings",
         "water", 4, "stick", 6, 10, "Ferguson", url="https://www.ferguson.com",
         spec="All pump-driven runs (80 ft); matches pump port size"),
    Part("hdpe-1in", '1" SDR-11 HDPE pipe', "plumbing-fittings",
         "water", 1, "stick", 12, 18, "Ferguson", spec="Food-safe blue-stripe 20 ft; filter outlet + IBC lines"),
    Part("tee-100-hdpe", 'Banjo TEE100 equal tee, 1" HDPE NPT', "plumbing-fittings",
         "water", 1, "ea", 5, 7, "Barn Door Ag", "Amazon", spec="X1 fill tee — splits the fill to both Blue totes"),
    Part("hdpe-three-quarter", '3/4" SDR-11 HDPE pipe', "plumbing-fittings",
         "water", 2, "stick", 10, 15, "Ferguson", spec="Spray bar run, 20 ft sticks"),
    Part("braided-hose", '1/2" ID reinforced braided PVC hose', "plumbing-fittings",
         "water", 2, "length", 12, 24, "Amazon", spec="Pump inlet flexible connection, 6 ft per pump"),
    # — electrical, wiring only (35) —
    Part("water-wire-14awg", "14 AWG duplex marine wire", "electrical-distribution",
         "water", 1, "roll", 22, 22, "Amazon", spec="Tinned copper, 25 ft"),
    Part("water-powerpole", "Anderson Powerpole connectors 30A", "electrical-distribution",
         "water", 5, "pair", 2, 2, "Amazon", spec="Pump connections — one pair per pump (P-01..P-05)"),
    Part("water-blade-fuses", "15A blade fuse", "electrical-distribution",
         "water", 1, "ea", 5, 5, "Amazon", spec="Pump Circuit C (single feed, all pumps)"),
    # — processing consumables (241) —
    Part("ldpe-sheeting", "6-mil black LDPE sheeting", "tools-safety",
         "water", 1, "roll", 66, 70, "Home Depot", spec="20 ft × 100 ft roll"),
    Part("ph-meter", "Apera Instruments AI311 PH60 pH meter", "tools-safety",
         "water", 1, "ea", 100, 110, "Apera Instruments", "Amazon",
         url="https://www.amazon.com/Apera-Instruments-AI311-Replaceable-2-00-16-00/dp/B01ENFOIQE",
         spec="Waterproof, 0–16 range, ±0.01 accuracy"),
    Part("ph-calibration", "pH calibration solution set", "tools-safety",
         "water", 1, "set", 10, 10, "Amazon", spec="pH 4 + pH 7 buffer sachets"),
    Part("citric-acid", "Citric acid, food grade, 5 lb", "tools-safety",
         "water", 2, "bag", 14, 14, "Amazon", spec="pH adjustment (acidifier)"),
    Part("ghs-labels", "Chemical-resistant labels (GHS)", "tools-safety",
         "water", 1, "pack", 20, 20, "Amazon", spec="For IBC totes"),
    Part("nitrile-gloves", "Nitrile gloves, box of 100", "tools-safety",
         "water", 2, "box", 9, 20, "Amazon", spec="Size M/L"),
    # — ibc-frame (ibc-stacking-report §9.1) — itemized, sums to costing frame (955–1,455) —
    Part("ibcf-rhs", "50 × 50 × 3mm RHS mild steel (6 m lengths)", "steel-structural",
         "ibc-frame", 4, "ea", 30, 45, "Metal Supermarkets", spec="Deep 4-leg box uprights (front + back pair) + top/bottom rings + front retaining bars + panel-mount rail (~19.5 m)"),
    Part("ibcf-feet", "12mm steel plate, 150 × 150 cut", "steel-structural",
         "ibc-frame", 4, "ea", 5, 10, "Metal Supermarkets", spec="Deep-box upright floor flange feet (one per leg; front feet reach under the tray)"),
    Part("ibcf-hangers", "4mm folded plate", "steel-structural",
         "ibc-frame", 4, "ea", 7.5, 12.5, "local fab", spec="Simpson-style wall joist hangers"),
    Part("ibcf-dring", "Weld-on lashing ring, 1½\" ID", "fasteners-hardware",
         "ibc-frame", 8, "ea", 4.95, 4.95, "McMaster-Carr", part_no="3028T31",
         url="https://www.mcmaster.com/3028t31/",
         spec="Zinc-plated steel weld-on tie-down rings — 1½\" (38mm) inside × ½\" thick, 6,600 lb WLL; fillet-welded to the front retaining bars (4 per tier × 2 tiers). Integrated weld base — no separate mount plate. Ring far exceeds the 25mm-strap-limited 1,100 kg assembly WLL.",
         note="Confirm weld-base footprint fits the 50mm front-bar face at order; grind zinc plating back at the weld zone before welding."),
    Part("ibcf-strap", "25mm ratchet strap, 1,100 kg WLL", "fasteners-hardware",
         "ibc-frame", 4, "ea", 7.5, 12.5, "Amazon", spec="Transport securing, over each stack"),
    Part("ibcf-floor-anchor", "Self-drilling structural screw, #14×3¼″ winged, 410 SS", "fasteners-hardware",
         "ibc-frame", 16, "ea", 1.02, 1.02, "Fasteners Plus", "ASMC", part_no="F14C325FDC",
         url="https://www.fastenersplus.com/products/14-x-3-1-4-self-drilling-flat-head-screw-with-wings-410-stainless-steel-pkg-100",
         spec="4 deep-box flange feet × 4 each. Self-drills the 6mm foot plate + 28mm plywood and taps the ~4mm steel crossmember — LAND EACH FOOT OVER A CROSSMEMBER (~450mm centers). Wings ream the plate/ply clearance then snap off at the steel. 410 SS (martensitic — self-drills steel; 316 can't). The IBC dead load bears in compression on the floor; the screws resist sliding/uplift only. Through-bolt 316 + backing nut instead where a crossmember underside is reachable. $1.02/ea (100-pk)."),
    Part("bolt-m12x40", "M12×40 hex bolt, Grade 8.8", "fasteners-hardware",
         "ibc-frame", 12, "ea", 0.71, 1.44, "FMW Fasteners", "US Bolt Kits", part_no="1634027",
         url="https://www.fmwfasteners.com/products/m12-1-75-x-40-hex-cap-screw-8-8-din-933-zinc-plated-fully-threaded",
         spec="Wall hangers (2 each) + front-bar cleats. M12×40 8.8 zinc DIN933; FMW 1634027 $1.44ea / US Bolt Kits $0.71ea."),
    Part("ibcf-fabrication", "Welding / fabrication (frame assembly)", "fabrication-labor",
         "ibc-frame", 1, "lot", 688, 1018, "local fab", spec="~14–20 hrs labor (deep 4-leg box — the ring/back-upright welds sit at the upper end of the range)"),
    Part("ibcf-paint", "Primer + paint", "adhesives-finishes",
         "ibc-frame", 1, "lot", 30, 50, "Hardware store", spec="Anti-corrosion coating"),
    # — tray (processing-tray-and-spray-bar §6.1) — itemized, sums to costing tray (1,300–2,015) —
    Part("tray-ss-sheet", "304 SS sheet, 16-gauge (1.5mm), #4 brushed", "stainless-sheet",
         "tray", 2, "ea", 360, 500, "Online Metals", spec="2,229 × 2,200mm panels"),
    Part("tray-fabrication", "Fabrication (cut, brake, weld, press sump)", "fabrication-labor",
         "tray", 1, "lot", 450, 850, "local sheet metal", spec="Two panels + a ~40mm center-seam lap (shingle-oriented downhill) + sump well"),
    Part("tray-hdpe-shim", "1-1/4\" HDPE plate, cut-to-size (slope shims)", "plastics-sheet",
         "tray", 1, "lot", 210, 300, "US Plastic Corp", "K-Mac Plastics",
         spec="5 tapered slope shims (50mm × 2,200mm, 20→30mm taper) RIP from ONE 1-1/4\" HDPE plate cut-to-size ~14×84\" (~7 ft²) — full-length one-piece strips (no splice); taper-cut bundles with the tray fab. ~$33–38/ft². Plate route ≈1/6 the solid-bar cost ($1,656)."),
    Part("tray-loctite", "Loctite PL Premium construction adhesive", "adhesives-finishes",
         "tray", 2, "tube", 7.5, 7.5, "Home Depot", spec="Shim-to-floor bond"),
    Part("tray-foot-valve", '1" SS foot valve with strainer screen', "plumbing-fittings",
         "tray", 1, "ea", 20, 20, "Amazon", spec="Sump pickup tube"),
    Part("tray-suction-hose", '1" reinforced suction hose, 6 ft', "plumbing-fittings",
         "tray", 1, "ea", 15, 15, "Amazon", spec="Pickup tube to P-04"),
    Part("tray-silicone-gasket", "Silicone gasket strip", "seals-gaskets",
         "tray", 1, "ea", 17, 25, "CountryMax (Aqueon)", spec="Silicone sealant bed in the center-seam lap joint (between the overlapped panels) + a top bead — the seam seal", part_no="015952", url="https://www.countrymax.com/aqueon-silicone-clear-aquarium-sealant-10oz-bottle/"),
    Part("bolt-m6-tray", "M6×1.0 × 16 hex bolt, 316 SS — tray center-seam lap joint", "fasteners-hardware",
         "tray", 12, "ea", 15.86 / 25, 15.86 / 25, "McMaster-Carr", part_no="93635A210", url="https://www.mcmaster.com/93635A210/", spec="Tray center-seam LAP-joint bolts (316 SS, wet zone) + M6 serrated flange nuts underneath. Through both overlapped 1.5mm panels + silicone bed. Grip ≈ 4mm → M6×16. Pitch M6×1.0 coarse. $15.86/pack of 25."),
    Part("nut-m6-flange", "M6×1.0 flange nut, serrated SS", "fasteners-hardware",
         "tray", 12, "ea", 4.71 / 100, 4.71 / 100, "McMaster-Carr", part_no="96194A101", url="https://www.mcmaster.com/96194A101/", spec="Serrated flange nut — tray panel bolts. Pitch M6×1.0 (coarse, baseline — confirm vs SKU PDF, must match the mating bolt). $4.71/pack of 100."),
    Part("tray-liner", "6-mil black LDPE sheet, 10 ft × 8 ft", "tools-safety",
         "tray", 1, "ea", 8, 8, "Home Depot", spec="Containment liner (consumable, per session)"),
    # — spray (processing-tray-and-spray-bar §6.2) — itemized, sums to costing spray (287–375;
    #   the $1/$3 report-subtotal rounding is absorbed into the AL-plate estimate so the block total
    #   matches the canonical figure) —
    Part("spray-al-shs", '304 SS RHS 40×25×3mm, 8 ft *', "steel-structural",
         "spray", 2, "ea", 48, 72, "Online Metals",
         spec="40×25×3mm rectangular tube, laid flat (low profile); 2 sticks butt-welded to span",
         note="* pre-camber ~15mm up at mid-span so it deflects flat under self-weight (SS beam ~2.8 kg/m; raw sag L/257)",
         dims="40×25×3", modeled_const="(model uses 40×25×3)"),
    Part("spray-al-plate", '6061-T6 AL plate 3/16" (5mm)', "aluminum",
         "spray", 1, "ea", 16, 28, "Online Metals", spec="Carriage plates + spacer blocks (~300 × 500mm sheet)"),
    Part("spray-ldpe-pipe", '3/4" LDPE irrigation poly pipe, 15 ft', "plumbing-fittings",
         "spray", 1, "ea", 10, 10, "Amazon", spec="Side-mounted spray manifold, clipped to the beam's inboard face (OD 25mm, ID 19mm)"),
    Part("spray-nozzles", "Flat-fan irrigation spray nozzles, barbed", "plumbing-fittings",
         "spray", 26, "ea", 30 / 26, 50 / 26, "Amazon", spec="180° fan pattern; side-tapped into the poly manifold, spray down-and-in"),
    Part("spray-manifold", 'Distribution manifold, 1/2" → 7 barb outlets', "plumbing-fittings",
         "spray", 1, "ea", 12, 12, "Amazon", spec="Mounted at ball joint, splits feed to tubes"),
    Part("spray-feed-tube", '1/4" irrigation poly tube', "plumbing-fittings",
         "spray", 1, "ea", 6, 6, "Amazon", spec="Manifold to beam feed points (~7m total)"),
    Part("spray-barbed-feed", "Barbed tees, tube into the side poly manifold", "plumbing-fittings",
         "spray", 7, "ea", 10 / 7, 10 / 7, "Amazon", spec="Feed tube to the side poly manifold, 7 feed points"),
    Part("spray-retainer-clips", 'SS/nylon retainer clips for 3/4" LDPE', "fasteners-hardware",
         "spray", 2, "ea", 2, 2, "Amazon", spec="Fold-back end closures"),
    Part("spray-skate-wheel", "Acetal roller wheels ×4 (Delrin rod stock, Ø32×20, Ø10 bore)", "bearings-motion",
         "spray", 1, "1 ft rod", 10.97, 10.97, "McMaster-Carr", part_no="8576K23",
         url="https://www.mcmaster.com/8576K23/",
         spec='Solid acetal (Delrin), flat tread. Cut from 1-1/4" (31.75mm) Delrin rod into 4 × 20mm slugs; drill Ø10.5 running-clearance bore — the acetal plain bore IS the bearing (self-lubricating on the Ø10 304 SS axle; no ball bearing — the ferricyanide/citric wash rules steel bearings out). One 1 ft (305mm) rod yields all 4 (parting/facing waste). Light-duty ~2.6 kg/wheel wet; 2 per carriage, low-profile for grate clearance. OD Ø31.75 = Ø32 nominal (−0.25mm).',
         dims="Ø31.75 rod → 4× Ø32×20, Ø10.5 bore",
         note="One 1 ft (305mm) 1-1/4in Delrin rod (McMaster 8576K23) makes all 4 wheels; price verified 2026-07-12."),
    Part("spray-brass-barb", '1/2" barb × 1/2" hose barb, brass', "plumbing-fittings",
         "spray", 1, "ea", 4, 4, "Amazon", spec="Flex hose to manifold inlet"),
    Part("spray-pool-pole", "Telescoping aluminum pool pole, 4–8 ft", "aluminum",
         "spray", 1, "ea", 15, 15, "Amazon", spec="Standard pool skimmer handle"),
    Part("spray-braided-hose", '1/2" reinforced braided PVC hose, 15 ft', "plumbing-fittings",
         "spray", 1, "ea", 15, 15, "Amazon", spec="BV-02 to beam feed (4 m coiled)"),
    Part("spray-axle-pin", "10mm × 60mm 304 SS axle pin (4-pack)", "fasteners-hardware",
         "spray", 1, "pack", 5, 5, "Amazon",
         url="https://www.amazon.com/uxcell-Single-Hole-Clevis-Pins/dp/B0816MQ5T6", spec="Wheel axle pins"),
    Part("spray-saddle-clamp", "Axle saddle clamps ×8 (304 SS flat-bar stock)", "fasteners-hardware",
         "spray", 1, "2 ft bar", 9.84, 9.84, "McMaster-Carr", part_no="8992K794",
         url="https://www.mcmaster.com/8992K794/", spec='Axle retention — formed from 1/8" (3.18mm) × 3/4" (19mm) 304 SS flat bar, wrapped over the Ø10 axle (1mm cradle clearance) with two ~12mm feet bolted up through the carriage plate (2× Ø5.5 M5). ~48mm developed per saddle; all 8 cut from one 2 ft (610mm) length of flat bar. A stamped conduit saddle clamp is only ~0.5mm — too thin for a rolling-carriage axle retainer. Alt: 304 SS + EPDM Adel loop clamp ~3/8–7/16\" ID.', dims="3.18×19 flat bar, ~48mm dev/pc", note="One 2 ft (610mm) 1/8x3/4 304 flat bar (McMaster 8992K794) yields all 8 saddles; formed + drilled (waste per part); price verified 2026-07-12."),
    Part("bolt-m6x20", "M6×1.0 × 20 hex bolt, Grade 8.8 zinc", "fasteners-hardware",
         "spray", 16, "ea", 17.86 / 100, 17.86 / 100, "McMaster-Carr", part_no="91280A330", url="https://www.mcmaster.com/91280A330/", spec="Carriage plate, beam clamp, saddle fasteners (M6×1.0). $17.86/pack of 100. ⚠ VALIDATE: 91280A330 is zinc-plated but the spray sits in the WET cyanotype zone — a 316-SS M6×20 resists corrosion better."),
    Part("nut-m6-nyloc", "M6×1.0 hex nut, nyloc SS", "fasteners-hardware",
         "spray", 16, "ea", 4.77 / 100, 4.77 / 100, "McMaster-Carr", part_no="90576A115", url="https://www.mcmaster.com/90576A115/", spec="Nyloc nut — M6×20 spray fasteners. Pitch M6×1.0 (coarse, baseline — confirm vs SKU PDF, must match the bolt). $4.77/pack of 100."),
    Part("spray-self-tap", "Self-tapping SS screws (8-pack)", "fasteners-hardware",
         "spray", 4, "ea", 0.44, 0.64, "Lowe's (Hillman)", part_no="3691866",
         url="https://www.lowes.com/pd/Hillman-25-Count-10-x-1-in-Stainless-Steel-Self-Drilling-Interior-Exterior-Sheet-Metal-Screws/3691866",
         spec="Ball-joint flange to beam top wall. #10×1 SS self-drill, 25-pk ~$11–16 (per-unit est)."),
    Part("spray-ball-joint", "Ø20mm ball joint, zinc socket, M12 stud", "bearings-motion",
         "spray", 1, "ea", 12, 12, "Amazon", spec="Multi-axis arm articulation"),
    Part("spray-beam-clamp", "SS beam clamp plates (4, cut from 1× 2 ft 304 flat bar)", "fasteners-hardware",
         "spray", 1, "2 ft bar", 35.33, 35.33, "McMaster-Carr", part_no="8992K512",
         url="https://www.mcmaster.com/8992K512/",
         spec="2 top + 2 bottom beam-clamp plates (1/4\"/6.35mm 304, beam-to-carriage sandwich, countersunk underside bolts), cut from one 2 ft flat bar (8992K512); + 4× 25mm 6061 AL spacers (from offcut). 1/4\" chosen for stiffness (bolts grip the beam, not bend the plates). Stack-up: plates thicken OUTWARD (wheel/carriage/beam fixed) — bottom plate Z22.6–29 (2.6mm clear of the Z20 roll surface), top plate Z54–60.4."),
    Part("spray-arm-tube", "6061-T6 AL round tube 25mm OD × 2mm wall, 500mm", "aluminum",
         "spray", 1, "ea", 6, 6, "Online Metals", spec="Arm tube — slit ~30mm at the bottom for the clamp-collar pinch onto the adapter's Ø21 spigot"),
    Part("spray-arm-adapter", "Arm-to-stud adapter, turned 6061-T6 AL (anodized)", "aluminum",
         "spray", 1, "ea", 12, 18, "Local machine shop", spec="Reducer coupling: M12×1.75 tapped bore (onto the ball-joint stud, locked with an M12 jam nut) → Ø21 male spigot the slit arm tube slips over. ~40mm long; anodized to match the AL tube (galvanic). Turned one-off / est."),
    Part("spray-arm-jamnut", "M12×1.75 jam nut, SS", "fasteners-hardware",
         "spray", 1, "ea", 0.7, 0.9, "Amazon", spec="Locks the arm adapter on the ball-joint M12 stud (M12×1.75 coarse).", part_no="B007IA07PS", url="https://www.amazon.com/M12-1-75-Plain-Finish-Stainless-Steel/dp/B007IA07PS"),
    Part("spray-arm-collar", "Clamp-style shaft collar, 25mm/1\" bore, SS", "fasteners-hardware",
         "spray", 1, "ea", 28, 33, "Ruland", spec="Over the slit arm-tube bottom; its integral clamp screw squeezes the Ø25×2 tube onto the adapter's Ø21 spigot — rotational adjust + lift-off for transport. Replaces the loose M6 pinch bolt. Confirm SKU/bore/price at order.", part_no="CL-16-ST", url="https://www.ruland.com/cl-16-st.html"),
    Part("spray-zip-ties", "Nylon zip ties, 200mm", "fasteners-hardware",
         "spray", 6, "ea", 1 / 6, 1 / 6, "Amazon", spec="Hose to arm tube"),

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
         "electrical", 1, "ea", 175.95, 175.95, "Powerwerx", "altE Store", part_no="BPC121531104R",
         url="https://powerwerx.com/victron-bpc121531104r-bluesmart-ip65-1215"),
    Part("nema-inlet", "NEMA 5-15R weatherproof inlet (flush power panel)", "electrical-distribution",
         "electrical", 1, "ea", 25, 25, "Amazon"),
    Part("solar-mount-frame", "Solar panel adjustable tilt mount set (per panel)", "electrical-power",
         "electrical", 3, "ea", 35.99, 35.99, "Amazon", "Renogy", part_no="RNG-MTS-TMB-G1-US",
         url="https://www.amazon.com/Renogy-Adjustable-Solar-Panel-Brackets/dp/B07CSKFWK7", spec="One adjustable tilt-bracket set per 200W panel (4 fixed + 2 tilt L-brackets, rated to 220W) — 3 sets for the 3-panel array."),
    Part("pv-cable-10awg", "PV cable 10 AWG + MC4 connectors", "electrical-distribution",
         "electrical", 1, "lot", 30, 30, "Amazon"),
    Part("pv-array-disconnect", "PV array disconnect — DC load-break isolator, 50A/150VDC (NEC 690.13)",
         "electrical-power", "electrical", 1, "ea", 40, 40, "AutomationDirect", "Amazon",
         url="https://www.automationdirect.com/"),
    Part("power-panel-plate", "Aluminum face plate 340×240×3mm (flush power panel)", "aluminum",
         "electrical", 1, "ea", 18, 18, "Online Metals", url="https://www.onlinemetals.com"),
    Part("power-panel-gasket", "Neoprene gasket 340×240×3mm (panel weatherseal)", "seals-gaskets",
         "electrical", 1, "ea", 21, 42, "Pres-Bond", part_no="NE4112-12X12-XFV", url="https://presbond.com/products/2c1-closed-cell-neoprene-foam-sheet-12-x-12-acrylic-adhesive"),
    Part("power-panel-frame", "Power-panel raised mounting frame, 8mm steel (welded)", "steel-structural",
         "electrical", 1, "ea", 15, 25, "Local fab", spec="Flat 8mm steel frame (~340×240 outer, 280×180 opening) welded onto the pinhole-wall corrugation crests around the cutout — a flat, sealable surface for the face plate + gasket, with 4× M6 weld-nuts. Sits a few mm proud (raised, not flush)."),
    Part("bolt-m6x20", "M6×1.0 × 20 hex bolt, Grade 8.8 zinc", "fasteners-hardware",
         "electrical", 4, "ea", 17.86 / 100, 17.86 / 100, "McMaster-Carr", part_no="91280A330", url="https://www.mcmaster.com/91280A330/", spec="Power-panel bolt: face plate 3mm + gasket 3mm into the welded raised frame's M6 weld-nut (~12mm grip → M6×20). $17.86/pack of 100. ⚠ VALIDATE: 91280A330 is zinc but the panel face is exterior (weather-facing) — a 316-SS M6×20 resists corrosion better."),
    Part("nut-m6-plain", "M6×1.0 hex nut, plain SS", "fasteners-hardware",
         "electrical", 4, "ea", 3.42 / 100, 3.42 / 100, "McMaster-Carr", part_no="90591A151", url="https://www.mcmaster.com/90591A151/", spec="Plain hex nut — panel-mount bolts. Pitch M6×1.0 (coarse, baseline — confirm vs SKU PDF). $3.42/pack of 100."),
    Part("washer-m6-flat", "M6 flat washer, SS", "fasteners-hardware",
         "electrical", 8, "ea", 4.51 / 100, 4.51 / 100, "McMaster-Carr", part_no="91455A120", url="https://www.mcmaster.com/91455a120/", spec="Flat washers (2/bolt) — panel mount. $4.51/pack of 100."),
    Part("mc4-bulkhead", "MC4 bulkhead connector pairs, IP67 panel-mount", "electrical-distribution",
         "electrical", 3, "pair", 8.33, 8.33, "Amazon"),
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
         "electrical-distribution", "electrical", 1, "ea", 348.59, 348.59, "Powerwerx", "West Marine", part_no="7700",
         url="https://powerwerx.com/blue-sea-7700-ml-rbs-remote-battery-switch"),
    Part("estop-external", "External emergency cut-off — red mushroom IP66/NEMA 4X + control loop", "electrical-distribution",
         "electrical", 1, "ea", 47.93, 47.93, "McMaster-Carr", part_no="6741K41", url="https://www.mcmaster.com/6741K41/", spec="McMaster 6741K41 $47.93 (firm 2026-07-23) — BACO 22mm plastic red mushroom, pull-to-release, SPST-NC, IP66/IP69K/NEMA 4X (weather + corrosion)."),
    Part("estop-internal", "Interior emergency cut-off — red mushroom IP66 metal (paralleled to exterior)",
         "electrical-distribution", "electrical", 1, "ea", 42.27, 42.27, "McMaster-Carr", part_no="8382K45", url="https://www.mcmaster.com/8382K45/", spec="McMaster 8382K45 $42.27 (firm 2026-07-23) — 22mm metal red mushroom, pull-to-release, SPST-NC, IP66/NEMA 4."),
    Part("mppt-charge-fuse", "MPPT charge-line fuse — 60A ANL/MIDI + holder", "electrical-distribution",
         "electrical", 1, "ea", 15, 15, "Blue Sea", "Amazon"),
    Part("shore-output-fuse", "Shore-charger output fuse — 20A inline", "electrical-distribution",
         "electrical", 1, "ea", 5, 5, "Amazon"),
    Part("battery-terminal-covers", "Battery terminal covers (pair), insulating boots", "electrical-distribution",
         "electrical", 1, "pair", 10, 10, "Amazon"),
    Part("wet-zone-connectors", "Sealed wet-zone connectors — Deutsch DT / adhesive heat-shrink",
         "electrical-distribution", "electrical", 1, "lot", 25, 25, "Waytek Wire"),
    Part("pump-switches", "Master pump switch (Circuit C) — IP67 sealed rocker/disconnect 12V 16A", "electrical-distribution",
         "electrical", 1, "ea", 10, 10, "Amazon", "Waytek Wire", spec="One manual cutoff for the whole pump circuit, mounted on the EP (per-pump switches removed; each Shurflo runs on its internal pressure switch)"),
    Part("pump-dist-block", "Pump distribution block — 12V DC + / − bus, 6-way", "electrical-distribution",
         "electrical", 1, "ea", 15, 15, "Blue Sea", "Amazon"),
    Part("dielectric-grease", "Dielectric grease, marine-grade (terminal protection)", "adhesives-finishes",
         "electrical", 1, "ea", 10, 10, "Amazon"),
    Part("tinned-marine-wire", "Tinned marine wire 14/16 AWG, ~25ft (wet-zone runs)", "electrical-distribution",
         "electrical", 1, "lot", 30, 30, "Waytek Wire"),
    Part("cable-grommets", "Cable grommets / glands — steel-shell penetrations", "electrical-distribution",
         "electrical", 1, "lot", 27.86, 27.86, "Amazon", part_no="B09K5GNFHF",
         url="https://www.amazon.com/YUFANNET-Assortment-Grommets-Automotive-Electrical/dp/B09K5GNFHF",
         spec="200-pc rubber grommet assortment (8 sizes, B09K5GNFHF $8.88) to protect wires through drilled steel + a strain-relief NPT cable-gland kit (B08R84YJ7X, nylon IP68, $18.98) for sealed wall/enclosure entries. $27.86 both kits."),
    Part("bonding-kit", "Equipotential bonding kit — 6 AWG + ring lugs", "electrical-distribution",
         "electrical", 1, "ea", 20, 20, "Amazon"),
    Part("ep-backing-panel", "EP plywood backing panel (18mm, ~700×2000mm)", "timber-ply",
         "electrical", 1, "sheet", 60, 60, "Home Depot", "Lumber yard",
         spec='18mm sealed plywood backboard, ~700×2000mm cut from a 4×8 sheet — the wall-mounted '
              'surface every EP component fixes to (MPPT on its forward sub-panel, battery bank, '
              'inverter, main + PV disconnects); the DC-distribution terminals (fuse block + busbars) '
              'sit in a small IP65 enclosure bolted to it. Add DIN rail + standoffs for the DIN gear.'),
    Part("ip65-enclosure", "IP65 enclosure ~200×220×140mm (fuse block + busbars, on the plywood)", "electrical-distribution",
         "electrical", 1, "ea", 60, 60, "Polycase", "Amazon",
         spec='Weatherproof IP65 box bolted to the plywood backboard, sealing the DC-distribution '
              'terminals (Blue Sea 5026 fuse block + the +/- busbars + charge-line fuse) against '
              'splash/dust. Its back panel is the plywood; the disconnect knob and cable glands pass '
              'through the face.'),
    Part("wiring-kit", "Wiring kit — 12/14/16/18 AWG tinned, 50ft/color", "electrical-distribution",
         "electrical", 1, "kit", 80, 80, "Waytek Wire", "Amazon"),
    Part("battery-cable-2-0", "2/0 AWG battery cable, 3ft (battery–fuse–busbar)", "electrical-distribution",
         "electrical", 1, "lot", 30, 30, "Amazon"),
    Part("anderson-powerpole", "Anderson Powerpole 30A connectors, 50 pairs", "electrical-distribution",
         "electrical", 1, "kit", 40, 40, "Powerwerx", url="https://powerwerx.com"),
    Part("deutsch-dt-2pin-elec", "Deutsch DT 2-pin connectors, IP67 (exterior penetrations)", "electrical-distribution",
         "electrical", 10, "set", 3, 3, "Waytek Wire"),
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
    Part("led-flat-panel", "12V LED flat panel 300×600mm, 20W 4000K", "electrical-distribution",
         "electrical", 3, "ea", 25, 25, "Amazon"),
    Part("pullcord-switch", "Pull-cord ceiling switch, 12V 6A SPST", "electrical-distribution",
         "electrical", 2, "ea", 8, 8, "Amazon"),
    Part("ground-stake", 'Copper-bonded ground rod, 8ft × ⅝" + acorn clamp', "electrical-distribution",
         "electrical", 1, "lot", 26.56, 26.56, "Home Depot", part_no="615880UPC",
         url="https://www.homedepot.com/p/ERICO-5-8-in-x-8-ft-Copper-Ground-Rod-615880UPC/202195738", spec="ERICO 615880UPC 5/8\"×8ft copper-bonded rod ($22.78) + bronze acorn ground-rod clamp GOEC5/8LDB ($3.78)."),
    Part("ground-wire-4awg", "4 AWG ground wire, green/yellow, 3m", "electrical-distribution",
         "electrical", 1, "lot", 15, 15, "Amazon"),

    # ═══ container (§1) — mirrors costing.CONTAINER → exact $2,300–$4,300 ═══
    Part("container-20ft", "20 ft ISO container — CW (cargo-worthy) grade", "container",
         "container", 1, "ea", 2000, 3500, "containermgt.com", "local depot"),
    Part("container-delivery", "Delivery — short haul (<50 miles), tilt-bed", "fabrication-labor",
         "container", 1, "job", 300, 800, "Commercial tilt-bed hire"),

    # ═══ interior (§2) — mirrors costing.INTERIOR → exact $950–$1,350 ═══
    Part("light-sealing-mat", "Light-sealing materials (interior conversion)", "seals-gaskets",
         "interior", 1, "lot", 157, 178, "Amazon (bundle)", "Amazon"),
    Part("interior-paint", "Interior matte-black paint", "adhesives-finishes",
         "interior", 1, "lot", 100, 160, "Home Depot"),
    # image-plane-backing RETIRED 2026-07-22 — the same ACM backing as film 'dibond-acm-film'
    # (bonded to the moveable film-plane frame); the old fixed-wall backing line was a double-count.
    Part("interior-ventilation", "Ventilation (inline fans + light-trap baffles) — interior-conversion allowance",
         "ducting-ventilation", "interior", 1, "lot", 80, 130, "Amazon"),
    Part("door-access-upgrades", "Door & access upgrades", "fasteners-hardware",
         "interior", 1, "lot", 50, 100, "Home Depot"),
    Part("misc-conversion-hw", "Misc. conversion hardware", "fasteners-hardware",
         "interior", 1, "lot", 80, 130, "Home Depot"),

    # ═══ optics (§3) — mirrors costing.OPTICS → exact $95–$240 ═══
    Part("pinhole-shim", "Custom laser-drilled pinhole — SS-302/304 shim, 3×3", "stainless-sheet",
         "optics", 1, "ea", 40, 100, "Lenox Laser", part_no="SS-3/8-DISC", url="https://lenoxlaser.com/shop/optical-apertures/standard-apertures/standard-aperture/",
         note="Ø2.17mm optical element — Lenox SS-3/8-DISC standard aperture (302 SS, 3/8\" mounted disc); config-dependent $22-100, confirm the exact Ø2.17mm price via their RFQ (1-800-49-HOLES)."),
    Part("pinhole-backing-plate", "Steel backing plate 6×6×⅛ + welded frame", "steel-structural",
         "optics", 1, "ea", 20, 40, "Metal Supermarkets", "local fab"),
    Part("shutter-plate", "Shutter plate (⅛ steel 10×8) + slide channel", "steel-structural",
         "optics", 1, "ea", 25, 50, "local fab"),
    Part("pinhole-retaining-ring", "Disc retaining ring (Al 6061-T6, M52×0.75)", "aluminum",
         "optics", 1, "ea", 15, 25, "local fab", spec="Ø52 bore × M52×0.75 external thread, 3× M4 grub screws — screws into the plate counterbore to clamp the Ø50 pinhole disc flat; removable for swap/clean"),

    # ═══ film (film-plane-mechanism-report §7) — itemized; structural+frame+saddles, sums to costing
    # FILM minus the clamp lines (= 3,102). The muslin clamps are the separate 'clamp' system below. ═══
    # — Structural & Rails (304 U-channel + acetal skate + 316 cross-slide + Ruland U-joint corner mechanism) —
    # Replaced the superseded Option-A leadscrew drive (HGR20/Acme/handwheel/rod-end) 2026-07-19.
    Part("fp-u-channel", '304 U-channel depth rail 3×1½" (76×38mm)', "steel-structural",
         "film", 6, "ea", 362.12, 362.12, "McMaster-Carr", part_no="1262T41", url="https://www.mcmaster.com/1262T41-1262T21/",
         spec="4 depth rails, one per corner, running wall-to-wall (~2,362mm, Yd0→C_WID) along the optical axis — an acetal skate rides inside each to set that corner's depth/focus. $362.12/6ft firm. NOTE: a 2,362mm rail exceeds a 6ft (1,829mm) length, and the skate can't cross a splice — so buy 8ft lengths (4 rails) or confirm the continuous-length SKU/price at order. Qty 6× 6ft here is the conservative $-estimate."),
    Part("fp-ujoint", "Ruland USKC12-6-6-SS U-joint (keyway+clamp, 303 SS)", "bearings-motion",
         "film", 4, "ea", 276, 276, "Ruland", part_no="USKC12-6-6-SS", url="https://www.ruland.com/us12-6-6-ss.html",
         spec='One per corner — supplies the tilt+swing angular DOF (45°/axis); 3/8" bores, 303 stainless (wet zone), twist-locked. $276 ea firm — INTERIM part; a cheaper joint is under research (see TODO). The U-joint alone is $276×4 = $1,104.'),
    Part("fp-ujoint-boot", "Ruland UBOOT12/19-NI-KIT nitrile boot", "seals-gaskets",
         "film", 4, "ea", 30.59, 30.59, "Ruland", part_no="UBOOT12/19-NI-KIT",
         url="https://www.ruland.com/uboot12-19-ni-kit.html",
         spec="Nitrile boot over each U-joint — keeps cyanotype splash out of the joint."),
    Part("fp-shaft-support", "McMaster 4040N12 304 shaft support", "bearings-motion",
         "film", 4, "ea", 58, 58, "McMaster-Carr", part_no="4040N12", url="https://www.mcmaster.com/4040N12/",
         spec="Two-piece 304 clamp securing the U-joint INPUT stub to the X (swing) slide, one per corner. $58 ea firm."),
    Part("fp-stub-shaft", '3/8" 304/304L SS rod — U-joint stub shafts (1× 3 ft)', "steel-structural",
         "film", 1, "lot", 13, 13, "McMaster-Carr", part_no="89535K87", url="https://www.mcmaster.com/89535K87/",
         spec='Input + output stub shafts into the U-joint (2/corner ×4 = 8 short stubs, ~60–80mm each ≈ 560–640mm + kerf). ONE 3 ft (914mm) length ($13.25 firm) yields all 8 with margin. Plain 304 rod — the USKC clamp grips it (keyway optional).'),
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
         spec="16 skate axles (4 per skate × 4) — the same 10mm×60mm 304 SS clevis/axle pins the spray skate uses; 4 packs = 16 pins. The acetal rollers spin on these Ø10 pins. 304 (splash zone, matches the spray). $5/4-pack = $20 — replaced the $88/600mm 316 precision rod (overkill for a plain-bearing axle)."),
    Part("fp-carriage-plate", "Skate carriage plate (×4) — fab", "steel-structural",
         "film", 4, "ea", 34, 59, "local fab",
         spec="One carriage plate per corner — carries the 4 rollers on their axles + the inboard lip; the U-joint/cross-slide stack bolts to it. The only fab piece of the skate. Est. — firm at fab quote."),
    Part("fp-cross-slide", "316 flat-bar Z (tilt) + X (swing) cross-slides + UHMW pad + gib", "steel-structural",
         "film", 4, "set", 45, 95, "Metal Supermarkets", "McMaster-Carr",
         spec="One 2-axis cross-slide stack per corner — 316 flat-bar Z and X slides on UHMW pads with an adjustable gib, absorbing the across-rail rotation travel. UHMW $23–93/sheet; 316 flat bar cut to length. Firm at order (est.)."),
    Part("fp-cam-clamp", "Cam-lever rail brake (skate lock)", "fasteners-hardware",
         "film", 12, "ea", 8, 15, "McMaster-Carr", "Amazon",
         spec="Three per corner — a cam-lever brake locks the acetal skate to the U-channel after the corner is slid to depth (no leadscrews); holds for the exposure + transport. Firm SKU/price at order (est.)."),
    Part("corner-l-plate", "Corner plate 304 SS (U-joint mount)", "steel-structural",
         "film", 4, "ea", 38, 52, "Metal Supermarkets", "Online Metals",
         spec='¼" 304 SS plate, ~6"×8" L-bracket — the frame-corner ↔ U-joint mount. Carries the concentrated U-joint corner load in STEEL, not aluminum; stainless for the cyanotype splash zone + galvanic match to the 303 SS U-joint. NOT expendable (the perimeter angle stays expendable 6061).'),
    # — Film Plane Frame (1,046) —
    Part("alu-angle-2x2", 'Aluminum angle 2"×2"×3/16" (6061-T6, plain) — 16 ft lengths', "aluminum",
         "film", 3, "16 ft length", 208.41, 208.41, "Metal Supermarkets", "Online Metals",
         url="https://www.mcmaster.com/8982K509-8982K479/",
         spec="6061-T6 angle (NOT 2024/7075 — corrosion + weldability). PLAIN mill finish (NOT anodized) — the film-plane PERIMETER FRAME, EXPENDABLE (inspect-annually / replace-on-pitting; bare 6061 pits sooner than anodized in the splash zone, so a shorter interval — anodizing is an option for longer life). WELD-FREE cut plan from 3× 16 ft (192\") lengths: 2 lengths → the two horizontal edges (4,499mm each, one per length, 378mm offcut); 1 length → both vertical edges (2,094mm ×2 from one 16 ft). No mid-span splices — only the 4 corner joints are welded/bolted. Metal Supermarkets 192\" @ $208.41 (cheaper per length than 8 ft @ $116.31 AND drops the welds). One frame — re-order to replace. McMaster 8982K509 (url) = catalog reference.",
         note="304 SS swap evaluated 2026-07-16 (~$1,650–2,200, +32 kg) rejected — expendable plain-6061 per Alvin. Re-spec'd 10×8ft (~1.85 frames) → 3×16ft (1 weld-free frame): −$538. Add 16ft lengths if pre-buying spares."),
    Part("dibond-acm-film", "Dibond ACM panel 4mm (black), 4×8 sheet", "plastics-sheet",
         "film", 4, "sheet", 95, 95, "Curbell Plastics", "Central Coast Plastics",
         url="https://www.curbellplastics.com/product-category/material/aluminum-composite-material-acm/dibond-panels/",
         spec="4× 48×96\" black 4mm ACM sheets as full-height VERTICAL STRIPS (Option A) — 3 vertical butt seams, splice-battened behind; no horizontal seam (2094mm plane height fits one 2438mm sheet). Covers the {{fact:film_plane_width_mm}}×{{fact:film_plane_height_mm}}mm rigid backing (4499 ÷ 1219 = 4 strips). $95/sheet firm; qty corrected 6→4."),
    Part("epdm-foam-tape", 'Black EPDM foam tape 1"×½"', "seals-gaskets",
         "film", 2, "roll", 22.37, 22.37, "McMaster-Carr", "Grainger", part_no="8694K88",
         url="https://www.mcmaster.com/8694K88/",
         spec="25 ft rolls — 2 (50 ft) cover the ~43 ft film-plane perimeter primary seal",
         note="Provisional qty: right-sized to the ~43 ft perimeter (old 3×50ft=150ft was ~3.5× over). Revisit with the EPDM-seal review."),
    Part("rosco-duvetyne", "Rosco Duvetyne", "fabric-textile",
         "film", 1, "ea", 95, 95, "B&H Photo", "Rosco direct", spec='60" wide, 10 yd'),
    Part("poly-sheeting-film", "6-mil black poly sheeting", "tools-safety",
         "film", 1, "roll", 66, 70, "Home Depot", "Uline", spec="10 ft × 100 ft"),
    Part("gorilla-tape", '2" black Gorilla Tape', "adhesives-finishes",
         "film", 6, "roll", 9, 13, "Home Depot", "Amazon", spec="35 yd rolls"),
    # — Wall-Seat Saddles (440; rev12 ×6, the 2 BR ends are walkway combined plates) —
    Part("wall-seat-saddle", "Mild steel plate 8mm (laser/plasma cut + welded)", "steel-structural",
         "film", 6, "ea", 53, 53, "Metal Supermarkets", "Online Metals",
         spec="ICP-11: back-plate + exterior plate + seat + gusset per saddle; ~21 kg over 6 saddles"),
    Part("bolt-m12x65", "M12×65 hex through-bolt, Grade 8.8 zinc, partial-thread", "fasteners-hardware",
         "film", 28, "ea", 15.95 / 10, 15.95 / 10, "McMaster-Carr", part_no="91280A728",
         url="https://www.mcmaster.com/91280A728/",
         spec="ICP-12: wall-sandwich through-bolt (4/saddle ×6 + 4 spare), sized for the 30mm-corrugation grip (~50mm), partial thread. $15.95/pack of 10 → 3 packs for 28. Pad with 1–2 M12 flat washers if the actual container corrugation is <30mm."),
    Part("nut-m12-plain", "M12 hex nut, plain", "fasteners-hardware",
         "film", 28, "ea", 12.78 / 50, 12.78 / 50, "McMaster-Carr", part_no="90591A181", url="https://www.mcmaster.com/90591A181/", spec="Plain hex nut — M12×65 wall-sandwich bolts (+ split lock washer). $12.78/pack of 50."),
    Part("washer-m12-flat", "M12 flat washer, zinc", "fasteners-hardware",
         "film", 112, "ea", 9.71 / 100, 9.71 / 100, "McMaster-Carr", part_no="91166A290", url="https://www.mcmaster.com/91166a290/", spec="Flat washers, M12×65 wall-sandwich bolts — 2 functional + 2 shim/bolt (shims pad the grip if corrugation <30mm). $9.71/pack of 100."),
    Part("washer-m12-split", "M12 split lock washer, zinc", "fasteners-hardware",
         "film", 28, "ea", 11.97 / 100, 11.97 / 100, "McMaster-Carr", part_no="91202A246", url="https://www.mcmaster.com/91202A246/", spec="Split lock washer under each nut — M12×65 wall-sandwich bolts (plain nut + split = locked). $11.97/pack of 100."),
    # M12 nyloc nut — verified ALTERNATIVE locking (Option B), NOT USED (chose plain nut + split washer):
    #   McMaster 94645A230, $10.08/pack of 10 = $1.008 ea. Swap in (and drop the split washers) if
    #   adopting nyloc locking for the M12 through-bolts; ~+$70 over the 110 bolts. https://www.mcmaster.com/94645A230/
    Part("saddle-m8-thumb", "M8×25mm knurled thumbscrew DIN 464", "fasteners-hardware",
         "film", 12, "ea", 3, 3, "Amazon", "Maedler", spec="ICP-13: left-rail drop-in hold-down; 2/saddle ×4 left + 4 spare"),
    Part("bolt-m8-fixing", "M8×1.25 × 25 hex bolt, Grade 8.8 zinc — right-rail end fixing (ICP-14)", "fasteners-hardware",
         "film", 8, "ea", 18.51 / 50, 18.51 / 50, "McMaster-Carr", part_no="91280A534", url="https://www.mcmaster.com/91280A534/", spec="ICP-14: right depth-rail end flange → wall seat hold-down (does NOT cross the wall). Grip = 3/16\" (4.76mm) 1262T21 channel base + 10mm seat ≈ 15mm → M8×25 (short → fully threaded). Pitch M8×1.25 coarse (matches the M8 plain nut). $18.51/pack of 50. ⚠ VALIDATE: 91280A534 is zinc — the film plane wets during development; a 316-SS M8×25 resists corrosion better."),
    Part("nut-m8-plain", "M8×1.25 hex nut, plain SS", "fasteners-hardware",
         "film", 8, "ea", 7.53 / 100, 7.53 / 100, "McMaster-Carr", part_no="90591A161", url="https://www.mcmaster.com/90591A161/", spec="Plain hex nut — M8 right-rail fixing. Pitch M8×1.25 (coarse, baseline — confirm vs SKU PDF, must match the bolt). $7.53/pack of 100."),
    # ═══ clamp (film-clamp-mechanism-report §4) — split out of FILM; itemized, sums to the FILM
    # clamp lines (off-the-shelf nylon clamps + HDPE filler) ═══
    Part("muslin-clamp", "Nylon spring clamp, 3½″ (Pittsburgh 69289)", "fasteners-hardware",
         "clamp", CLAMP_N_TOTAL, "ea", 3, 4, "Harbor Freight", "Amazon", part_no="69289",
         url="https://www.harborfreight.com/3-12-in-nylon-spring-clamp-69289.html",
         spec="Inert fiberglass/nylon spring clamp with swivel pads — no corrosion in the cyanotype splash zone (replaces the custom steel-bracket clip). Clips over the filler-filled L-frame edge to grip the muslin; the jaw must clear ~55mm (2\" leg + ACM + muslin), so a ≥3\" clamp. Top + 2 side edges only (bottom = walkway/swing clearance). Confirm the open-jaw ≥2\" at purchase; 2½\" 69290 is the smaller-body fallback."),
    Part("clamp-filler", "HDPE filler strip (L-channel packer)", "plastics-sheet",
         "clamp", 1, "lot", 30, 70, "TAP Plastics", "McMaster-Carr",
         spec=f"Inert HDPE strip, {CLAMP_FILLER_D:g}mm deep (= frame leg − ACM − muslin − angle), filling the aluminum-angle L channel along the 3 clamped edges (~8.7 m) so the nylon clamp bites a solid full-depth sandwich. Cut to suit; chemistry-safe (same family as the tray liner). Firm at fab."),

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
         "lightlock", 1, "ea", 6, 10, "Home Depot",
         spec="Bearing-housing / light-trap seam seal. Generic — source a black exterior/UV silicone at Home Depot (GE/DAP/Permatex black RTV); prefer a weather/UV grade over a mildewcide bath caulk. ~$6–10/tube."),
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
         spec="Top + bottom radial location of the post. igus iglide J self-lubricating polymer, Ø90 ID × Ø95 OD × Ø103 flange × 100 mm long. The FLANGE gives axial location against the hub face; the OD is a light press into the hub bore. Axial load is on the 51118 thrust bearing. Maintenance-free, no oil; inert plastic — chemical-resistant (iglide J passed the igus chemical filter; iglide X isn't offered at Ø90). Service pressure ≈1.3 N/mm² vs ≈35 N/mm² allowable (>25× margin); runs on the unhardened S355 post. $130.53/ea, ships in days — replaces the made-to-order GGB DU (was $211/ea, 3-mo lead)."),
    Part("sp-drum-cage", "Drum support cage, 40 × 40 × 3mm SHS", "steel-structural",
         "swing", 1, "lot", 70, 120, "local fab", spec="Steel frame carrying the Ø900 housing + drum on the swinging leaf"),
    Part("sp-wall-stays", "Top + bottom wall stays + 4-bolt anchor plates", "fasteners-hardware",
         "swing", 2, "set", 45, 60, "Fasteners Plus", spec="Transport lock — M16 turnbuckle + eye/hook rods + inside/outside wall plates", part_no="JETBGV58X6", url="https://www.fastenersplus.com/products/5-8-x-6-jaw-eye-galvanized-turnbuckle"),
    Part("sp-rail-saddles", "Drop-in rail saddles + tapered dowels", "steel-structural",
         "swing", 4, "ea", 20, 32.5, "local fab", "McMaster-Carr", spec="For the 2 removable left film rails (TL + BL); dowels set the film datum"),
    # ═══ door (hinged-panel §8.4) — fixed door frame; sums to the SWINGPIVOT door lines ($335–$550) ═══
    Part("sp-door-frame-rhs", "50 × 50 × 3mm RHS mild steel (6 m lengths)", "steel-structural",
         "door", 3, "ea", 30, 40, "Metal Supermarkets", spec="Frame members"),
    Part("sp-door-seal-lips", "Tight-seal nylon strip brush + aluminum holder (~4.7 m, top + bottom)", "seals-gaskets",
         "door", 1, "lot", 129, 129, "McMaster-Carr", part_no="74405T12", url="https://www.mcmaster.com/74405T12-74405T126/", spec="Top + bottom door-frame light seals (paths #3–#4) — 2× McMaster 74405T12 nylon Tight-Seal Strip Brush (8 ft, 1\" overall height, $28.88 ea) in 2× McMaster 8813T53 aluminum holder channel (8 ft, $35.37 ea) = $128.50 firm; covers full panel width top + bottom (~2× C_WID ≈ 4.7 m ≈ 15.5 ft, from 4× 8 ft lengths). The swinging panel edge SWEEPS THROUGH the bristles, so a brush (not a compression EPDM, which would drag under the sideways sweep) — same principle as the drum-opening brush seals.", note="Changed 2026-07-18 from 3mm steel seal lips + panel-edge EPDM compression to a strip brush: the top/bottom seal is swept through by the swinging panel, so a brush is the correct type. Brush 74405T12 ($28.88/8ft), holder 8813T53 ($35.37/8ft) — prices verified 2026-07-18."),
    Part("sp-door-fab", "Welding / fabrication", "fabrication-labor",
         "door", 1, "lot", 200, 350, "local fab", spec="Frame assembly + wall attachment"),

    # ═══ panel (hinged-panel §8.1) — panel structure; sums to costing.PANEL ($1,124–$1,691) ═══
    Part("panel-rhs-frame", "50 × 50 × 3mm RHS mild steel (6 m lengths)", "steel-structural",
         "panel", 4, "ea", 30, 40, "Metal Supermarkets", spec="Frame perimeter + internal members"),
    Part("panel-pp-skins", "1/8\" black HDPE sheet (48×96)", "plastics-sheet",
         "panel", 4, "sheet", 123.34, 123.34, "US Plastics", "TAP Plastics", part_no="46684",
         url="https://www.usplastic.com/catalog/item.aspx?itemid=136961&catid=705",
         spec="Panel skins, both faces (~12 m², 4× 4×8 ft sheets) — rev11, replaces 18mm ply. 1/8\" HDPE is nearest stock to the 4mm PANEL_SKIN_T nominal (weld-compatible with the HDPE housing/drum); the U-channel grid (~400–450mm centers) keeps the skin flat, so the 0.8mm is immaterial. US Plastics 46684 $123.34/sheet."),
    Part("panel-fanb-ply", "Exterior-grade plywood (Fan B mount band)", "timber-ply",
         "panel", 1, '2\'×4\' ¾" panel', 30, 50, "Home Depot",
         spec='¾" (18mm) exterior-grade project panel (610×1220mm); Fan B mount band, one corner bottom→1,125mm'),
    Part("panel-corner-plates", "3mm aluminum plate 5052-H32 (48×96)", "aluminum",
         "panel", 2, "ea", 293.16, 293.16, "M&K Metal", "Industrial Metal Supply", part_no="52SH125408",
         url="https://www.mkmetal.net/5052-h32sht.125x48x96", spec="Corner-zone core plates — 3mm (.125\") 5052-H32, 48×96\" sheet, one 653mm-wide plate per sheet → 2 sheets. Firm $293.16/sheet (M&K Metal SoCal)."),
    Part("panel-epdm-gasket", "20mm EPDM gasket (per meter, closed-cell)", "seals-gaskets",
         "panel", 21, "m", 1.13, 2.46, "Amazon (OKAYASU)", spec="Perimeter seal (~10 m) + housing-surround ring (~6 m) + 2× vertical cut seals at Yd180/2287 (~5 m)", part_no="B089GJQ96Z", url="https://www.amazon.com/dp/B089GJQ96Z"),
    Part("panel-u-channel", "Aluminum U-channel (per meter)", "aluminum",
         "panel", 40, "m", 3, 5, "Online Metals", spec="Gasket retainer + PP-skin retention (perimeter + housing-surround + stiffener grid)"),
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
    Part("shelf-phenolic-ply", "Phenolic-faced plywood (work surface)", "timber-ply",
         "shelf", 1, '4\'×8\' ¾" sheet', 60, 60, "Home Depot", "lumber yard",
         spec='¾" (18mm) phenolic-faced concrete-form sheet (1220×2440mm), cut to 300×600'),
    Part("shelf-steel-shs", "25×25×3 mm steel SHS", "steel-structural",
         "shelf", 1, "lot", 30, 30, "Online Metals", "Metal Supermarkets", spec="6 m (frame + spill lip)"),
    Part("shelf-piano-hinge", "Continuous (piano) hinge, 600 mm", "fasteners-hardware",
         "shelf", 1, "ea", 22.68, 35.72, "Wurth LAC", spec="stainless/steel, ~32 mm leaf", part_no="LSN8-32-600", url="https://wurthlac.com/product/165974/"),
    Part("shelf-folding-stays", "Folding shelf stays/brackets", "fasteners-hardware",
         "shelf", 2, "ea", 12, 12, "Amazon", "McMaster-Carr", spec="fold-flat, ~30–50 kg rating"),
    Part("shelf-wall-cleat", "Wall mounting cleat + anchors", "steel-structural",
         "shelf", 1, "lot", 18, 18, "Local fab", spec="6 mm steel cleat + 2 stay anchors (slotted)"),
    Part("shelf-wall-backing", "Shelf mount backing plates, 8mm steel (welded, ×3)", "steel-structural",
         "shelf", 3, "ea", 6, 10, "Local fab", spec="Flat 8mm steel backing plates welded to the pinhole-wall interior crests — one behind the hinge cleat + one per stay anchor — giving flat, solid load anchors with M8 weld-nuts."),
    Part("bolt-m8-wall", "M8×1.25 × 25 hex bolt, Grade 8.8 zinc — shelf cleat + stay mount", "fasteners-hardware",
         "shelf", 12, "ea", 18.51 / 50, 18.51 / 50, "McMaster-Carr", part_no="91280A534", url="https://www.mcmaster.com/91280A534/", spec="Clamps the shelf hinge cleat (6mm) + 2 stay anchors to their welded 8mm backing plates (M8 weld-nut). Grip ≈ 14mm → M8×25. Pitch M8×1.25 coarse. $18.51/pack of 50 (same 91280A534 as the film ICP-14 fixing)."),
    Part("nut-m8-plain", "M8×1.25 hex nut, plain SS", "fasteners-hardware",
         "shelf", 12, "ea", 7.53 / 100, 7.53 / 100, "McMaster-Carr", part_no="90591A161", url="https://www.mcmaster.com/90591A161/", spec="Plain hex nut — shelf wall bolts. Pitch M8×1.25 (coarse, baseline — confirm vs SKU PDF, must match the bolt). $7.53/pack of 100."),
    Part("washer-m8-flat", "M8 flat washer, SS", "fasteners-hardware",
         "shelf", 12, "ea", 3.32 / 100, 3.32 / 100, "McMaster-Carr", part_no="91166A270", url="https://www.mcmaster.com/91166A270/", spec="Flat washer (1/bolt) — shelf wall bolts. $3.32/pack of 100."),
    Part("shelf-transport-latch", "Transport latch (over-center/barrel)", "fasteners-hardware",
         "shelf", 1, "ea", 8, 8, "Amazon", spec="secures the folded board"),
    Part("bolt-m5x16-csk", "M5×16 countersunk screw, A2-70 SS", "fasteners-hardware",
         "shelf", 8, "ea", 11.54 / 100, 11.54 / 100, "McMaster-Carr", part_no="91420A326", url="https://www.mcmaster.com/91420A326/", spec="Ply panel attachment (same M5×16 CSK as the clamp clips — 91420A326)"),
    Part("shelf-gusset-plates", "Corner gusset plate, 3 mm", "steel-structural",
         "shelf", 4, "ea", 1.25, 1.25, "Steel offcut", spec="50×50 mm triangular"),
    Part("shelf-paint", "Flat black epoxy spray paint", "adhesives-finishes",
         "shelf", 1, "can", 12, 12, "Hardware store", spec="frame + hardware finish"),
    Part("shelf-hdpe-pipe", '½" HDPE pipe (tap relocation)', "plumbing-fittings",
         "shelf", 1, "lot", 10, 10, "Irrigation supply", spec="extend the blue supply trunk ~1.3 m left to TAP-01"),

    # ═══ walkway (§10) — re-decomposed to match the report (fab bundled into each bracket, no
    # separate fab line) → $2,005–$2,985 (reconciles to EXPECTED walkway $2,000–$2,975 within tol) ═══
    Part("walkway-grp-panel", "Molded GRP grating (McNichols quote, cut-to-size)", "plastics-sheet",
         "walkway", 1, "lot", 3035.73, 3035.73, "McNichols", "American Grating",
         spec="1\" MS-S-100 vinyl-ester grit, ~48 ft² cut to the walkway sections. FIRM: McNichols quote 2026-3819515 = $3,035.73 (see quotes/2026-3819515.pdf). ⚠ ALTERNATIVE: American Grating public price for the IDENTICAL spec ≈ $830 (2× 3'×10' @ $415) — ~3.6× cheaper; reconsider supplier vs McNichols' cut/vinyl-ester special-order/freight premium. Cut plan: grp-grating-quote.md."),
    Part("walkway-grp-sealant", "GRP grating edge-seal kit", "adhesives-finishes",
         "walkway", 1, "kit", 40, 60, "Fibergrate", spec="Fibergrate Sealing & Bonding Kit — molded FRP cut edges are field-SEALED (epoxy), not snap-trimmed; ½-pint kit seals ~20–40 linear ft of cut edge."),
    Part("walkway-drum-exit-grp", "Drum-exit punch-out grating", "plastics-sheet",
         "walkway", 1, "lot", 50, 65, "McNichols", spec="Extra GRP landing (~0.23 m²) at the light-lock exit"),
    Part("walkway-std-brackets", "Cantilever bracket — standard (near/far)", "steel-structural",
         "walkway", 14, "ea", 30, 50, "Local fab",
         spec="8mm steel plate: 150mm vert leg + 300mm arm + 70mm gusset, welded (5 near + 9 far at 457mm centers)"),
    Part("walkway-wide-brackets", "Cantilever bracket — widened (near)", "steel-structural",
         "walkway", 4, "ea", 40, 70, "Local fab",
         spec="10mm steel plate: 200mm vert leg + 500mm arm + 70mm gusset, welded (EP/battery/slit zone)"),
    Part("bolt-m12x65", "M12×65 hex through-bolt, Grade 8.8 zinc, partial-thread", "fasteners-hardware",
         "walkway", 58, "ea", 15.95 / 10, 15.95 / 10, "McMaster-Carr", part_no="91280A728",
         url="https://www.mcmaster.com/91280A728/",
         spec="Cantilever-bracket wall bolts (3 per std + 4 per widened), sized for the 30mm-corrugation grip (~48–50mm), partial thread. Pad with 1–2 M12 flat washers if the actual container corrugation is <30mm."),
    Part("nut-m12-plain", "M12 hex nut, plain", "fasteners-hardware",
         "walkway", 58, "ea", 12.78 / 50, 12.78 / 50, "McMaster-Carr", part_no="90591A181", url="https://www.mcmaster.com/90591A181/", spec="Plain hex nut — M12×65 cantilever bolts (+ split lock washer). $12.78/pack of 50."),
    Part("washer-m12-flat", "M12 flat washer, zinc", "fasteners-hardware",
         "walkway", 232, "ea", 9.71 / 100, 9.71 / 100, "McMaster-Carr", part_no="91166A290", url="https://www.mcmaster.com/91166a290/", spec="Flat washers, M12×65 cantilever bolts — 2 functional + 2 shim/bolt (shims pad the grip if corrugation <30mm)."),
    Part("washer-m12-split", "M12 split lock washer, zinc", "fasteners-hardware",
         "walkway", 58, "ea", 11.97 / 100, 11.97 / 100, "McMaster-Carr", part_no="91202A246", url="https://www.mcmaster.com/91202A246/", spec="Split lock washer under each nut — M12×65 cantilever bolts (plain nut + split = locked)."),
    Part("walkway-reinf-plates", "Reinforcing plate (exterior)", "steel-structural",
         "walkway", 18, "ea", 4.1667, 7.2222, "Local fab", spec="6mm steel: 100×180mm std (×14) + 120×220mm widened (×4)"),
    Part("walkway-transition-plates", "Transition bearing plate", "steel-structural",
         "walkway", 2, "ea", 2.5, 5, "Local fab", spec="40×500×5mm flat bar, welded to bracket arm top at width transitions"),
    Part("walkway-cantilever-frame", "Right walkway cantilever frame", "steel-structural",
         "walkway", 1, "lot", 28, 40, "Metal Supermarkets",
         spec="40×40×3mm SHS — 2 long beams ({{fact:container_width_mm}}mm) + 2 end beams (300mm) + 2 center arms (325mm), ~8 m"),
    Part("walkway-right-cleats", "Wall cleat (left corners)", "steel-structural",
         "walkway", 2, "ea", 10, 17.5, "Local fab", spec="8mm steel: back-plate + exterior plate + shelf, through-bolted to the wall"),
    Part("walkway-corner-plates", "Combined corner plate (right corners)", "steel-structural",
         "walkway", 2, "ea", 25, 40, "Local fab",
         spec="10mm steel, 150mm wide — carries the walkway right beam AND the bottom film rail"),
    Part("bolt-m12x70", "M12×70 hex through-bolt, Grade 8.8 zinc, partial-thread", "fasteners-hardware",
         "walkway", 24, "ea", 17.36 / 10, 17.36 / 10, "McMaster-Carr", part_no="91280A732",
         url="https://www.mcmaster.com/91280A732/",
         spec="Right-walkway wall cleats + combined corner plates + 2 center-arm U-clamps, sized for the deepest 30mm-corrugation grip (~54mm), partial thread. $17.36/pack of 10. Pad with 1–2 M12 flat washers if the actual container corrugation is <30mm."),
    Part("nut-m12-plain", "M12 hex nut, plain", "fasteners-hardware",
         "walkway", 24, "ea", 12.78 / 50, 12.78 / 50, "McMaster-Carr", part_no="90591A181", url="https://www.mcmaster.com/90591A181/", spec="Plain hex nut — M12×70 right-walkway bolts (+ split lock washer). $12.78/pack of 50."),
    Part("washer-m12-flat", "M12 flat washer, zinc", "fasteners-hardware",
         "walkway", 96, "ea", 9.71 / 100, 9.71 / 100, "McMaster-Carr", part_no="91166A290", url="https://www.mcmaster.com/91166a290/", spec="Flat washers, M12×70 right-walkway bolts — 2 functional + 2 shim/bolt (shims pad the grip if corrugation <30mm)."),
    Part("washer-m12-split", "M12 split lock washer, zinc", "fasteners-hardware",
         "walkway", 24, "ea", 11.97 / 100, 11.97 / 100, "McMaster-Carr", part_no="91202A246", url="https://www.mcmaster.com/91202A246/", spec="Split lock washer under each nut — M12×70 right-walkway bolts (plain nut + split = locked)."),
    Part("walkway-floor-legs", "Floor-leg cantilever bracket (left walkway, ×5)", "steel-structural",
         "walkway", 5, "ea", 11, 19, "Local fab",
         spec="50×50×3mm SHS post (~115mm) + 40×40×3mm SHS arm (2 reach X470, 3 extended to X770) + 128×60×8mm foot plate"),
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
        out.append(Part(f"amfe-{t.key}", "Ammonium iron(III) oxalate (AmFe)", "chemistry-reagents",
                        "chemistry", t.amfe_kg, "kg", costing.PRICE_AMFE_PER_KG, costing.PRICE_AMFE_PER_KG,
                        "Photographers' Formulary", "Bostick & Sullivan",
                        url="https://stores.photoformulary.com/ammonium-ferric-oxalate/",
                        spec="Part A; warm water to dissolve", tier=t.key))
        out.append(Part(f"ferri-{t.key}", "Potassium ferricyanide", "chemistry-reagents",
                        "chemistry", t.ferri_kg, "kg", costing.PRICE_FERRI_PER_KG, costing.PRICE_FERRI_PER_KG,
                        "Bostick & Sullivan", url="https://www.bostick-sullivan.com/product/potassium-ferricyanide-250gm/",
                        spec="Part B", tier=t.key))
        out.append(Part(f"dichromate-{t.key}", "Ammonium dichromate", "chemistry-reagents",
                        "chemistry", 1, "run", costing.DICHROMATE_RUN, costing.DICHROMATE_RUN,
                        "Photographers' Formulary", spec="Part B additive; contrast enhancer (Cat-1A carcinogen — handle with care)", tier=t.key))
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
    for desc, sup in (("Ammonium iron(III) oxalate (AmFe)", "Photographers' Formulary"),
                      ("Potassium ferricyanide", "Bostick & Sullivan"),
                      ("Ammonium dichromate", "Photographers' Formulary")):
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


import facts as _facts  # live fact-marker expansion inside generated spec cells

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
    for p in by_system(sys):                                    # insertion order, not type-sorted
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
    panel (Corridor / Pinhole Wall).  Panel-mounted equipment only; the full water BOM (pipe, totes,
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
    for t in sorted(bt):                                        # type sections A–Z
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
        for a in order:                                                     # rows A–Z by item name (fasteners: by class/size)
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
_AUDIT_ORDER = ["ibc-tote-1000l", "lifepo4-100ah", "shurflo-2088-p1", "bigblue-housing",
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
    return [f"{rel}  parts:{key} -> {st}" for rel, key, st in inject(write=False)
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
_CLAMP_LINES = ("Muslin clamp",)   # matches both "Muslin clamps …" (clamps) + "Muslin clamp filler …" (HDPE)


def _split_sum(lst, prefixes, keep: bool):
    sel = [li for li in lst if any(li.label.startswith(p) for p in prefixes) == keep]
    return (sum(li.low for li in sel), sum(li.high for li in sel))


def reconcile_target(sys: str):
    """The (low, high) the registry system must sum to."""
    if sys in _WATER_SPLIT:
        li = next(l for l in costing.WATER if l.label.startswith(_WATER_SPLIT[sys]))
        return (li.low, li.high)
    if sys == "water":                                          # WATER minus the three split-out lines
        return _split_sum(costing.WATER, _WATER_SPLIT.values(), keep=False)
    if sys == "clamp":                                          # the two clamp lines of FILM
        return _split_sum(costing.FILM, _CLAMP_LINES, keep=True)
    if sys == "film":                                           # FILM minus the clamp lines
        return _split_sum(costing.FILM, _CLAMP_LINES, keep=False)
    if sys == "door":                                           # the "Fixed door frame" lines of SWINGPIVOT
        return _split_sum(costing.SWINGPIVOT, ("Fixed door frame",), keep=True)
    if sys == "swing":                                          # SWINGPIVOT minus the door lines
        return _split_sum(costing.SWINGPIVOT, ("Fixed door frame",), keep=False)
    if sys == "chemistry":                                      # build = the DEFAULT tier total (+ muslin)
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
            print(f"  [{st:>7}] {rel}  parts:{key}")
        raise SystemExit(0)
    if args.check_blocks:
        probs = check_blocks()
        print("\n".join(f"  STALE: {p}" for p in probs) if probs else "✓ all parts: doc blocks current")
        raise SystemExit(1 if probs else 0)
    if args.check or not (args.system or args.master):
        errs = self_check()
        if errs:
            print("✗ parts registry reconciliation FAILED:")
            [print("   -", e) for e in errs]
            raise SystemExit(1)
        print(f"✓ parts registry reconciles with costing  ({len(systems())} system(s): {', '.join(systems())})")
    if args.system:
        print(emit_system(args.system))
    if args.master:
        print(emit_master())
