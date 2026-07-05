#!/usr/bin/env python3
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
# TODO (AUGUST 2026): RE-PRICE EVERY PART against current supplier listings — not just the timber-ply
# section. The cost bands below are an April-2026 basis (indicative low/high estimates, pre-quote);
# refresh them all, mark confirmed lines, and re-run `parts.py --inject` + `lint.py`. A cost change
# cascades automatically: edit the band here → the master/report/cost blocks regenerate and the
# costing reconciliation gate proves consistency. (Update the master header's "Basis: April 2026" too.)
# ─────────────────────────────────────────────────────────────────────────────────────────────
"""
from __future__ import annotations
import argparse
import os
import re
from dataclasses import dataclass, field

import costing  # reconciliation guardrail (EXPECTED) + the cost cascade it still owns

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
         "ventilation", 1, "ea", 130, 130, "Hessaire", "Amazon",
         url="https://hessaire.com/mobile-cooling/1300-cfm-mobile-cooler",
         spec="Hessaire MC18M, 120V AC, {{fact:cooler_cfm_rated}} CFM (run low), {{fact:evap_cooler_w_ac}}W",
         dims="559×305×711", datasheet="Hessaire MC18M", modeled_const="EVAP_W/EVAP_D/EVAP_H",
         audit_status="✅ RESOLVED"),
    Part("cooler-inverter", "Cooler inverter", "electrical-power", "ventilation", 1, "ea", 275, 275,
         "Victron", "Amazon", spec="Victron Phoenix 12/375 GFCI (12V→120V) + DC fuse/disconnect + GFCI AC outlet"),
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
         "water", 4, "ea", 80, 150, "Container Exchanger",
         url="https://containerexchanger.com/geo-sale-ads/us-ca/bulk-containers/ibc-totes-for-sale",
         spec="Caged composite tote, DN50 butterfly valve (S60×6 thread); side-entry fittings near top",
         dims="1219×1016×1168", modeled_const="IBC_W/IBC_D/IBC_H_1000", audit_status="✅ FIXED (v2)"),
    Part("bulkhead-2in", 'Bulkhead fitting 2" NPT (304 SS)', "plumbing-fittings",
         "water", 3, "ea", 25, 40, "McMaster-Carr", part_no="4464K115",
         url="https://www.mcmaster.com/4464K115", spec="External fill/drain port, welded through container wall"),
    # — pumps (315–345) —
    Part("shurflo-2088-p1", "Shurflo 2088-554-144 pump (P-01 Blue supply)", "water-equipment",
         "water", 1, "ea", 55, 70, "Amazon",
         url="https://www.amazon.com/Shurflo-2088-554-144-Fresh-Gallons-Minute/dp/B00C1M6B1C",
         spec='12VDC, 3.5 GPM, 45 PSI, 1/2" NPSM ports',
         dims="216×127×114", datasheet="Shurflo 2088-554-144", modeled_const="PUMP_D×PUMP_YD_SPAN×Z",
         audit_status="✅ FIXED (minor) — protrusion PUMP_D 100→114", panel="Corridor"),
    Part("shurflo-2088-p2", "Shurflo 2088-554-144 pump (P-02 filter loop)", "water-equipment",
         "water", 1, "ea", 55, 70, "Amazon",
         url="https://www.amazon.com/Shurflo-2088-554-144-Fresh-Gallons-Minute/dp/B00C1M6B1C",
         spec='12VDC, 3.5 GPM, 45 PSI, 1/2" NPSM ports', panel="Pinhole Wall"),
    Part("shurflo-2088-p3", "Shurflo 2088-554-144 pump (P-03 waste evacuation)", "water-equipment",
         "water", 1, "ea", 65, 65, "Amazon", spec="12VDC, 3.5 GPM, 45 PSI; empties IBC-4 residual below X4 (~120L)", panel="Corridor"),
    Part("shurflo-2088-p4", "Shurflo 2088-554-144 pump (P-04 tray drain transfer)", "water-equipment",
         "water", 1, "ea", 65, 65, "Amazon", spec="12VDC, 3.5 GPM, 45 PSI; tray drain to IBC-3 (~900mm lift)", panel="Corridor"),
    Part("shurflo-2088-p5", "Shurflo 2088-554-144 pump (P-05 Brown drain)", "water-equipment",
         "water", 1, "ea", 65, 65, "Amazon", spec="12VDC, 3.5 GPM, 45 PSI; evacuates IBC-3 (Brown) residual to the X3 end-wall port", panel="Corridor"),
    Part("seaflo-accumulator", "SeaFlo accumulator (0.75 L)", "water-equipment",
         "water", 1, "ea", 35, 35, "Amazon",
         url="https://www.amazon.com/Seaflo-Accumulator-Control-Internal-Bladder/dp/B01MUYL8F8",
         spec='0.75 L, 125 PSI, 1/2" MNPT', part_no="SFAT-075-125-01",
         dims="200×127×125", datasheet="SeaFlo SFAT-075-125-01", modeled_const="Ø127×200 cyl",
         audit_status="✅ FIXED — cylinder 150→200", panel="Corridor"),
    Part("shurflo-bracket", "Shurflo pump mounting bracket", "fasteners-hardware",
         "water", 5, "ea", 10, 10, "Amazon", spec="Stainless, 2088 series — one per pump (P-01..P-05)"),
    # — corridor plumbing-panel structure (3D-derived marine ply; previously uncosted) —
    Part("corridor-panel-ply-18", "Corridor plumbing-panel marine ply (18mm)", "timber-ply",
         "water", 1, "sheet", 120, 200, "marine plywood supplier", "Home Depot",
         spec='4×8 ft 18mm BS 1088 (or equivalent) marine plywood — rear backing board (~170×2196) + drain-riser backing spine (~456×1966) + spacer offcuts; ~1.3 m² used. Price est.',
         panel="Corridor"),
    Part("corridor-panel-ply-25", "Pump-mount shirt marine ply (25mm)", "timber-ply",
         "water", 1, "piece", 70, 130, "marine plywood supplier", "Home Depot",
         spec='25mm BS 1088 (or equivalent) marine plywood, ~610×1650 cut piece — pump-mount shirt behind P-01..P-05 + 6× shirt-to-panel spacer blocks. Price est.',
         panel="Corridor"),
    Part("corridor-panel-mount", "Corridor panel mount hardware (brackets + fasteners)", "fasteners-hardware",
         "water", 1, "lot", 25, 50, "Home Depot",
         spec='6× steel angle brackets (panel → IBC-frame front-portal uprights), shirt-to-panel screws, lag bolts. Price est.',
         panel="Corridor"),
    # — filter (286–485): 3 separate 4.5×20 housings on a slotted-angle skid frame (§3.1/§7.2) —
    Part("bigblue-housing", 'Big Blue filter housing 4.5"×20" (separate)', "water-equipment",
         "water", 3, "ea", 38, 62, "Amazon", dims="Ø184×594",
         spec='Ø184×594mm/housing (4.5×20), 1" NPT ports — three SEPARATE housings on the slotted-angle skid frame (Pentek / iSpring / Geekpure)',
         datasheet="Pentek 4.5×20 BB", modeled_const="BB_OD/BB_H",
         audit_status="3-separate design of record (2026-07): combo → 3 separate housings + frame per plumbing-report §3.1/§7.2. Prices indicative — firm at the Aug-2026 re-price.", panel="Pinhole Wall"),
    Part("filter-skid-frame", "Slotted steel angle frame 25×25×3mm (filter skid)", "water-equipment",
         "water", 1, "lot", 25, 45, "Home Depot", spec="~2.5 m 25×25×3mm slotted steel angle + fasteners; bolts to the 18mm ply backing (adjustable housing height)", panel="Pinhole Wall"),
    Part("filter-ubracket", "Steel U-bracket (filter housing)", "water-equipment",
         "water", 3, "ea", 7, 10, "McMaster-Carr", spec="Wraps the housing head; 2 bolts/bracket through the backing board", panel="Pinhole Wall"),
    Part("filter-hdpe-spacer", "HDPE spacer blocks 25mm (filter skid)", "water-equipment",
         "water", 1, "lot", 12, 22, "McMaster-Carr", spec="25mm HDPE blocks between U-bracket and backing board — sump-bowl hang clearance", panel="Pinhole Wall"),
    Part("filter-jumper", '1" HDPE inter-housing jumpers', "plumbing-fittings",
         "water", 1, "lot", 18, 32, "Ferguson", spec='F-01 OUT→F-02 IN, F-02 OUT→F-03 IN — 1" HDPE + 90° elbows routed outside the bodies', panel="Pinhole Wall"),
    Part("cartridge-sediment", 'MPP 5-micron sediment cartridge 4.5"×20"', "water-equipment",
         "water", 2, "ea", 12, 20, "Amazon", spec="Melt-blown polypropylene depth filter (F-1 stage); ~50-print interval", panel="Pinhole Wall"),
    Part("cartridge-kdf", 'KDF-55 heavy-metal cartridge 4.5"×20"', "water-equipment",
         "water", 1, "ea", 40, 70, "Amazon", spec="KDF-55 media for dissolved iron/metal removal (F-2 stage); ~60-print interval", panel="Pinhole Wall"),
    Part("cartridge-carbon", 'CTO carbon block cartridge 4.5"×20"', "water-equipment",
         "water", 2, "ea", 16, 30, "Amazon", spec="Coconut shell activated carbon block (F-3 stage); ~40-print interval", panel="Pinhole Wall"),
    # — valves & fittings (333–567) —
    Part("valve-v050fp-corridor", 'Banjo V050FP ball valve 1/2" FNPT', "plumbing-fittings",
         "water", 3, "ea", 6, 10, "Amazon", spec="PP full-port quarter-turn; pump-suction isolation BV-01 (P-01), BV-02 (P-05), BV-06 (P-03)", panel="Corridor"),
    Part("valve-v050fp-wall", 'Banjo V050FP ball valve 1/2" FNPT', "plumbing-fittings",
         "water", 1, "ea", 6, 10, "Amazon", spec="PP full-port quarter-turn; pump-suction isolation BV-03 (P-02)", panel="Pinhole Wall"),
    Part("valve-v050fp-supply", 'Banjo V050FP ball valve 1/2" FNPT', "plumbing-fittings",
         "water", 2, "ea", 6, 10, "Amazon", spec="PP full-port; supply isolation BV-04 (TAP-01 chem tap), BV-05 (spray-bar feed)"),
    Part("valve-v100fp", 'Banjo V100FP ball valve 1" FNPT', "plumbing-fittings",
         "water", 6, "ea", 10, 16, "Amazon", spec="PP full-port; V1/V3/V4, VB1–VB3 (IBC fill/drain)"),
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
         "water", 4, "ea", 3, 5, "Amazon", spec="PP 90°; IBC bends, filter outlet to DV-01"),
    Part("tee-half", '1/2" NPT polypropylene tee', "plumbing-fittings",
         "water", 6, "ea", 2, 4, "Amazon", spec="Blue suction/discharge tees, branches"),
    Part("tee-100", 'Banjo TEE100 equal tee 1" NPT', "plumbing-fittings",
         "water", 3, "ea", 4, 6, "Amazon", spec="PP; IBC drain tees (the X1 fill is now a 4-way cross)"),
    Part("cross-100", '1" NPT 4-way cross fitting', "plumbing-fittings",
         "water", 1, "ea", 8, 14, "Amazon", spec="X1 fresh-fill 4-way: X1 inlet + IBC-1 + IBC-2 + DV-01 blue recycle return (was a 3-way tee). Cost est."),
    Part("union-half", '1/2" NPT polypropylene union', "plumbing-fittings",
         "water", 6, "ea", 4, 6, "Amazon", spec="Maintenance disconnects on pump runs"),
    Part("bushing-reducer", '1/2"×1" NPT bushing reducer', "plumbing-fittings",
         "water", 1, "ea", 3, 5, "Amazon", spec="P-02 riser to F1 filter inlet"),
    Part("s60-adapter", 'S60×6 to 1" NPT adapter', "plumbing-fittings",
         "water", 8, "ea", 8, 15, "Amazon", spec='IBC DN50 valve to 1" HDPE; PP S60×6 male × 1" NPT female'),
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
         "water", 1, "ea", 4, 6, "Amazon", spec="X1 fill tee — splits the fill to both Blue totes"),
    Part("hdpe-three-quarter", '3/4" SDR-11 HDPE pipe', "plumbing-fittings",
         "water", 2, "stick", 10, 15, "Ferguson", spec="Spray bar run, 20 ft sticks"),
    Part("braided-hose", '1/2" ID reinforced braided PVC hose', "plumbing-fittings",
         "water", 2, "length", 10, 10, "Amazon", spec="Pump inlet flexible connection, 6 ft per pump"),
    # — electrical, wiring only (35) —
    Part("water-wire-14awg", "14 AWG duplex marine wire", "electrical-distribution",
         "water", 1, "roll", 22, 22, "Amazon", spec="Tinned copper, 25 ft"),
    Part("water-powerpole", "Anderson Powerpole connectors 30A", "electrical-distribution",
         "water", 4, "pair", 2, 2, "Amazon", spec="Pump connections"),
    Part("water-blade-fuses", "15A blade fuse", "electrical-distribution",
         "water", 1, "ea", 5, 5, "Amazon", spec="Pump Circuit C (single feed, all pumps)"),
    # — processing consumables (241) —
    Part("ldpe-sheeting", "6-mil black LDPE sheeting", "tools-safety",
         "water", 1, "roll", 100, 100, "Home Depot", spec="20 ft × 100 ft roll"),
    Part("ph-meter", "Apera Instruments AI311 PH60 pH meter", "tools-safety",
         "water", 1, "ea", 55, 55, "Amazon",
         url="https://www.amazon.com/Apera-Instruments-AI311-Replaceable-2-00-16-00/dp/B01ENFOIQE",
         spec="Waterproof, 0–16 range, ±0.01 accuracy"),
    Part("ph-calibration", "pH calibration solution set", "tools-safety",
         "water", 1, "set", 10, 10, "Amazon", spec="pH 4 + pH 7 buffer sachets"),
    Part("citric-acid", "Citric acid, food grade, 5 lb", "tools-safety",
         "water", 2, "bag", 14, 14, "Amazon", spec="pH adjustment (acidifier)"),
    Part("ghs-labels", "Chemical-resistant labels (GHS)", "tools-safety",
         "water", 1, "pack", 20, 20, "Amazon", spec="For IBC totes"),
    Part("nitrile-gloves", "Nitrile gloves, box of 100", "tools-safety",
         "water", 2, "box", 14, 14, "Amazon", spec="Size M/L"),
    # — ibc-frame (ibc-stacking-report §9.1) — itemized, sums to costing frame (955–1,455) —
    Part("ibcf-rhs", "50 × 50 × 3mm RHS mild steel (6 m lengths)", "steel-structural",
         "ibc-frame", 4, "ea", 30, 45, "Metal Supermarkets", spec="Deep 4-leg box uprights (front + back pair) + top/bottom rings + front retaining bars + panel-mount rail (~19.5 m)"),
    Part("ibcf-feet", "12mm steel plate, 150 × 150 cut", "steel-structural",
         "ibc-frame", 4, "ea", 5, 10, "Metal Supermarkets", spec="Deep-box upright floor flange feet (one per leg; front feet reach under the tray)"),
    Part("ibcf-hangers", "4mm folded plate", "steel-structural",
         "ibc-frame", 4, "ea", 7.5, 12.5, "local fab", spec="Simpson-style wall joist hangers"),
    Part("ibcf-dring", "25mm welded D-ring", "fasteners-hardware",
         "ibc-frame", 4, "ea", 5, 8.75, "McMaster-Carr", part_no="3641T29", spec="Lashing holders on the front bars, 6mm mount plates"),
    Part("ibcf-strap", "25mm ratchet strap, 1,100 kg WLL", "fasteners-hardware",
         "ibc-frame", 4, "ea", 7.5, 12.5, "Amazon", spec="Transport securing, over each stack"),
    Part("ibcf-floor-anchor", "M12 floor anchor (wedge/sleeve, container floor)", "fasteners-hardware",
         "ibc-frame", 16, "ea", 1.875, 3.75, "McMaster-Carr", spec="4 deep-box flange feet × 4 anchors each"),
    Part("ibcf-m12-bolt", "M12 × 40 bolt, Grade 8.8", "fasteners-hardware",
         "ibc-frame", 12, "ea", 1, 22 / 12, "McMaster-Carr", spec="Wall hangers (2 each) + front-bar cleats"),
    Part("ibcf-fabrication", "Welding / fabrication (frame assembly)", "fabrication-labor",
         "ibc-frame", 1, "lot", 688, 1018, "local fab", spec="~14–20 hrs labor (deep 4-leg box — the ring/back-upright welds sit at the upper end of the range)"),
    Part("ibcf-paint", "Primer + paint", "adhesives-finishes",
         "ibc-frame", 1, "lot", 30, 50, "Hardware store", spec="Anti-corrosion coating"),
    # — tray (processing-tray-and-spray-bar §6.1) — itemized, sums to costing tray (1,300–2,015) —
    Part("tray-ss-sheet", "304 SS sheet, 16-gauge (1.5mm), #4 brushed", "stainless-sheet",
         "tray", 2, "ea", 360, 500, "Online Metals", spec="2,229 × 2,200mm panels"),
    Part("tray-fabrication", "Fabrication (cut, brake, weld, press sump)", "fabrication-labor",
         "tray", 1, "lot", 450, 850, "local sheet metal", spec="Two panels with center flange + sump well"),
    Part("tray-hdpe-shim", "HDPE flat bar, 50mm wide", "plastics-sheet",
         "tray", 5, "ea", 8, 15, "Online Metals", spec="Tapered shim strips, 2,200mm each"),
    Part("tray-loctite", "Loctite PL Premium construction adhesive", "adhesives-finishes",
         "tray", 2, "tube", 7.5, 7.5, "Home Depot", spec="Shim-to-floor bond"),
    Part("tray-foot-valve", '1" SS foot valve with strainer screen', "plumbing-fittings",
         "tray", 1, "ea", 20, 20, "Amazon", spec="Sump pickup tube"),
    Part("tray-suction-hose", '1" reinforced suction hose, 6 ft', "plumbing-fittings",
         "tray", 1, "ea", 15, 15, "Amazon", spec="Pickup tube to P-04"),
    Part("tray-silicone-gasket", "Silicone gasket strip", "seals-gaskets",
         "tray", 1, "ea", 20, 20, "McMaster-Carr", spec="Center flange seal"),
    Part("tray-m6-bolts", "M6 SS hex bolts + flange nuts", "fasteners-hardware",
         "tray", 12, "ea", 1, 1, "McMaster-Carr", spec="Panel flange bolts"),
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
    Part("spray-skate-wheel", "Acetal (Delrin) roller wheel, Ø32 × 20mm, Ø10 plain bore", "bearings-motion",
         "spray", 4, "ea", 3, 5, "McMaster-Carr",
         url="https://www.mcmaster.com/products/acetal-round-stock/", spec="Solid acetal (Delrin), flat tread, plain bore — corrosion-immune + self-lubricating on the Ø10 304 SS axle (no carbon-steel ball bearings; the ferricyanide/citric wash rules those out). Turned from acetal rod or an equivalent POM plain-bore roller. Light-duty (~2.6 kg/wheel wet); 2 per carriage, low-profile for grate clearance."),
    Part("spray-brass-barb", '1/2" barb × 1/2" hose barb, brass', "plumbing-fittings",
         "spray", 1, "ea", 4, 4, "Amazon", spec="Flex hose to manifold inlet"),
    Part("spray-pool-pole", "Telescoping aluminum pool pole, 4–8 ft", "aluminum",
         "spray", 1, "ea", 15, 15, "Amazon", spec="Standard pool skimmer handle"),
    Part("spray-braided-hose", '1/2" reinforced braided PVC hose, 15 ft', "plumbing-fittings",
         "spray", 1, "ea", 15, 15, "Amazon", spec="BV-02 to beam feed (4 m coiled)"),
    Part("spray-axle-pin", "10mm × 60mm 304 SS axle pin (4-pack)", "fasteners-hardware",
         "spray", 1, "pack", 5, 5, "Amazon",
         url="https://www.amazon.com/uxcell-Single-Hole-Clevis-Pins/dp/B0816MQ5T6", spec="Wheel axle pins"),
    Part("spray-saddle-clamp", "304 SS saddle clamp, 10mm (10-pack)", "fasteners-hardware",
         "spray", 8, "ea", 10 / 8, 10 / 8, "Amazon",
         url="https://www.amazon.com/Boxonly-Fixing-Stainless-Saddle-Tension/dp/B0CG1CNQKX", spec="Axle retention, bolted to plate underside"),
    Part("spray-m6-bolts", "M6×20 SS bolts + nyloc nuts", "fasteners-hardware",
         "spray", 16, "ea", 7 / 16, 7 / 16, "McMaster-Carr", spec="Carriage plate, beam clamp, saddle fasteners"),
    Part("spray-self-tap", "Self-tapping SS screws (8-pack)", "fasteners-hardware",
         "spray", 4, "ea", 5 / 4, 5 / 4, "McMaster-Carr", spec="Ball-joint flange to beam top wall"),
    Part("spray-ball-joint", "Ø20mm ball joint, zinc socket, M12 stud", "bearings-motion",
         "spray", 1, "ea", 12, 12, "Amazon", spec="Multi-axis arm articulation"),
    Part("spray-beam-clamp", "SS beam clamp plates (top + bottom) + spacers (25mm)", "fasteners-hardware",
         "spray", 4, "ea", 2.5, 2.5, "McMaster-Carr", spec="Beam to carriage plate (sandwich, countersunk underside bolts)"),
    Part("spray-arm-tube", "6061-T6 AL round tube 25mm OD × 2mm wall, 500mm", "aluminum",
         "spray", 1, "ea", 6, 6, "Online Metals", spec="Arm tube"),
    Part("spray-pinch-bolt", "M6 SS hex bolt + nut", "fasteners-hardware",
         "spray", 1, "ea", 1, 1, "McMaster-Carr", spec="Pinch bolt for arm tube"),
    Part("spray-zip-ties", "Nylon zip ties, 200mm", "fasteners-hardware",
         "spray", 6, "ea", 1 / 6, 1 / 6, "Amazon", spec="Hose to arm tube"),

    # ═══ electrical (§6) — fully itemized from master §6; point estimates summing to ~$2,345
    # (reconciles to EXPECTED['power'] $2,350 within tolerance). Demonstrates the procurement-real
    # granularity the by-type/by-supplier BOM needs. ═══
    # — Solar & battery (primary power), ≈$1,329 —
    Part("solar-panel-200w", "Solar panel, 200W monocrystalline 12V", "electrical-power",
         "electrical", 3, "ea", 133, 133, "Renogy",
         url="https://www.renogy.com/200-watt-12-volt-monocrystalline-solar-panel/"),
    Part("mppt-100-50", "Victron SmartSolar MPPT 100/50 charge controller", "electrical-power",
         "electrical", 1, "ea", 200, 200, "altE Store", url="https://www.altestore.com"),
    Part("lifepo4-100ah", "LiFePO4 battery, 100Ah 12V (Renogy Smart Lithium)", "electrical-power",
         "electrical", 1, "ea", 350, 350, "Renogy",
         url="https://www.renogy.com/12v-100ah-smart-lithium-iron-phosphate-battery/",
         dims="330×172×214", datasheet="Renogy 12V 100Ah Smart Lithium", modeled_const="BA_W/BA_D/BA_H",
         audit_status="✅ FIXED", note="busbar provisioned for optional 2nd pack (+$375)"),
    Part("shore-charger", "Victron Blue Smart IP65 12/15 shore backup charger", "electrical-power",
         "electrical", 1, "ea", 150, 150, "altE Store", url="https://www.altestore.com"),
    Part("nema-inlet", "NEMA 5-15R weatherproof inlet (flush power panel)", "electrical-distribution",
         "electrical", 1, "ea", 25, 25, "Amazon"),
    Part("solar-mount-frame", "Solar panel ground-mount tilt frame, 30°", "electrical-power",
         "electrical", 1, "ea", 80, 80, "Renogy", url="https://www.renogy.com"),
    Part("pv-cable-10awg", "PV cable 10 AWG + MC4 connectors", "electrical-distribution",
         "electrical", 1, "lot", 30, 30, "Amazon"),
    Part("pv-array-disconnect", "PV array disconnect — DC load-break isolator, 50A/150VDC (NEC 690.13)",
         "electrical-power", "electrical", 1, "ea", 40, 40, "AutomationDirect", "Amazon",
         url="https://www.automationdirect.com/"),
    Part("power-panel-plate", "Aluminum face plate 340×240×3mm (flush power panel)", "aluminum",
         "electrical", 1, "ea", 18, 18, "Online Metals", url="https://www.onlinemetals.com"),
    Part("power-panel-gasket", "Neoprene gasket 340×240×3mm (panel weatherseal)", "seals-gaskets",
         "electrical", 1, "ea", 6, 6, "McMaster-Carr"),
    Part("power-panel-bolts", "M6 bolt+nut+washer set, SS (panel mount)", "fasteners-hardware",
         "electrical", 4, "set", 1.25, 1.25, "McMaster-Carr"),
    Part("mc4-bulkhead", "MC4 bulkhead connector pairs, IP67 panel-mount", "electrical-distribution",
         "electrical", 3, "pair", 8.33, 8.33, "Amazon"),
    # — Distribution & wiring, ≈$1,016 —
    Part("fuse-block-5026", "Blue Sea 5026 fuse block, 12-circuit ST-blade", "electrical-distribution",
         "electrical", 1, "ea", 55, 55, "Amazon", "West Marine"),
    Part("mrbf-200a", "200A main fuse — MRBF terminal-mount (ABYC E-11)", "electrical-distribution",
         "electrical", 1, "ea", 25, 25, "Amazon"),
    Part("battery-disconnect", "Battery main disconnect — Blue Sea m-Series 300A isolator", "electrical-distribution",
         "electrical", 1, "ea", 40, 40, "West Marine", "Amazon"),
    Part("ml-rbs-contactor", "Remote battery switch — Blue Sea ML-RBS 500A magnetic-latch (E-stop trip)",
         "electrical-distribution", "electrical", 1, "ea", 150, 150, "West Marine", "Amazon"),
    Part("estop-external", "External emergency cut-off — red mushroom IP66 + control loop", "electrical-distribution",
         "electrical", 1, "ea", 30, 30, "AutomationDirect", "Amazon"),
    Part("estop-internal", "Interior emergency cut-off — red mushroom IP65 (paralleled to exterior)",
         "electrical-distribution", "electrical", 1, "ea", 25, 25, "AutomationDirect", "Amazon"),
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
         "electrical", 1, "lot", 15, 15, "McMaster-Carr"),
    Part("bonding-kit", "Equipotential bonding kit — 6 AWG + ring lugs", "electrical-distribution",
         "electrical", 1, "ea", 20, 20, "Amazon"),
    Part("ip65-enclosure", "IP65 enclosure 300×200×130mm (fuse block + MPPT)", "electrical-distribution",
         "electrical", 1, "ea", 60, 60, "Amazon"),
    Part("wiring-kit", "Wiring kit — 12/14/16/18 AWG tinned, 50ft/color", "electrical-distribution",
         "electrical", 1, "kit", 80, 80, "Waytek Wire", "Amazon"),
    Part("battery-cable-2-0", "2/0 AWG battery cable, 3ft (battery–fuse–busbar)", "electrical-distribution",
         "electrical", 1, "lot", 30, 30, "Amazon"),
    Part("anderson-powerpole", "Anderson Powerpole 30A connectors, 50 pairs", "electrical-distribution",
         "electrical", 1, "kit", 40, 40, "Powerwerx", url="https://powerwerx.com"),
    Part("deutsch-dt-2pin-elec", "Deutsch DT 2-pin connectors, IP67 (exterior penetrations)", "electrical-distribution",
         "electrical", 10, "set", 3, 3, "Waytek Wire"),
    Part("pvc-trunking", "40×25mm PVC cable trunking, 5m", "electrical-distribution",
         "electrical", 4, "ea", 10, 10, "McMaster-Carr"),
    Part("corrugated-conduit", "10mm corrugated conduit, drop runs (McMaster 7828K48)", "electrical-distribution",
         "electrical", 10, "m", 3, 3, "McMaster-Carr", part_no="7828K48"),
    Part("wire-label-kit", "Brady M210 wire label kit", "electrical-distribution",
         "electrical", 1, "ea", 80, 80, "Amazon"),
    Part("led-flat-panel", "12V LED flat panel 300×600mm, 20W 4000K", "electrical-distribution",
         "electrical", 3, "ea", 25, 25, "Amazon"),
    Part("pullcord-switch", "Pull-cord ceiling switch, 12V 6A SPST", "electrical-distribution",
         "electrical", 2, "ea", 8, 8, "Amazon"),
    Part("ground-stake", 'Copper ground stake, 8ft × ⅝" dia', "electrical-distribution",
         "electrical", 1, "ea", 20, 20, "Home Depot"),
    Part("ground-wire-4awg", "4 AWG ground wire, green/yellow, 3m", "electrical-distribution",
         "electrical", 1, "lot", 15, 15, "Amazon"),

    # ═══ container (§1) — mirrors costing.CONTAINER → exact $2,300–$4,300 ═══
    Part("container-20ft", "20 ft ISO container — CW (cargo-worthy) grade", "container",
         "container", 1, "ea", 2000, 3500, "containermgt.com", "local depot"),
    Part("container-delivery", "Delivery — short haul (<50 miles), tilt-bed", "fabrication-labor",
         "container", 1, "job", 300, 800, "Commercial tilt-bed hire"),

    # ═══ interior (§2) — mirrors costing.INTERIOR → exact $950–$1,350 ═══
    Part("light-sealing-mat", "Light-sealing materials (interior conversion)", "seals-gaskets",
         "interior", 1, "lot", 150, 210, "McMaster-Carr", "Amazon"),
    Part("interior-paint", "Interior matte-black paint", "adhesives-finishes",
         "interior", 1, "lot", 100, 160, "Home Depot"),
    Part("image-plane-backing", "Image-plane flat backing — Dibond ACM", "plastics-sheet",
         "interior", 1, "lot", 490, 620, "TAP Plastics", "Online Metals"),
    Part("interior-ventilation", "Ventilation (inline fans + light-trap baffles) — interior-conversion allowance",
         "ducting-ventilation", "interior", 1, "lot", 80, 130, "Amazon"),
    Part("door-access-upgrades", "Door & access upgrades", "fasteners-hardware",
         "interior", 1, "lot", 50, 100, "Home Depot"),
    Part("misc-conversion-hw", "Misc. conversion hardware", "fasteners-hardware",
         "interior", 1, "lot", 80, 130, "Home Depot"),

    # ═══ optics (§3) — mirrors costing.OPTICS → exact $95–$240 ═══
    Part("pinhole-shim", "Custom laser-drilled pinhole — SS-302/304 shim, 3×3", "stainless-sheet",
         "optics", 1, "ea", 50, 150, "Lenox Laser", note="Ø2.17mm; the optical element"),
    Part("pinhole-backing-plate", "Steel backing plate 6×6×⅛ + welded frame", "steel-structural",
         "optics", 1, "ea", 20, 40, "Metal Supermarkets", "local fab"),
    Part("shutter-plate", "Shutter plate (⅛ steel 10×8) + slide channel", "steel-structural",
         "optics", 1, "ea", 25, 50, "local fab"),

    # ═══ film (film-plane-mechanism-report §7) — itemized; structural+frame+saddles, sums to costing
    # FILM minus the clamp lines (= 3,102). The muslin clamps are the separate 'clamp' system below. ═══
    # — Structural & Rails (1,616) —
    Part("hgr20-rail", "Linear guide rail HGR20", "bearings-motion",
         "film", 4, "ea", 45, 45, "Automation Overstock", "McMaster-Carr", part_no="5901T777", spec="2,200mm"),
    Part("hgh20ca-carriage", "Rail carriage HGH20CA", "bearings-motion",
         "film", 8, "ea", 18, 18, "Automation Overstock", "McMaster-Carr", spec="Flanged block"),
    Part("acme-leadscrew", 'Acme leadscrew ¾"-6', "bearings-motion",
         "film", 4, "ea", 95, 95, "Roton Products", "McMaster-Carr", part_no="6289K36", spec="8 ft length"),
    Part("acme-nut", 'Acme nut bronze ¾"-6', "bearings-motion",
         "film", 4, "ea", 12, 12, "Roton Products", "McMaster-Carr", part_no="6289K512"),
    Part("handwheel-8in", 'Handwheel 8" dia', "bearings-motion",
         "film", 4, "ea", 35, 35, "Grainger", "McMaster-Carr", part_no="6440K64", spec='¾" bore, cast aluminum'),
    Part("locking-collar", "Locking collar SS316", "bearings-motion",
         "film", 4, "ea", 12, 12, "McMaster-Carr", "Fastenal", part_no="6436K12", spec='¾" bore'),
    Part("corner-l-plate", "Corner bracket L-plate", "aluminum",
         "film", 4, "ea", 20, 20, "Metal Supermarkets", "Online Metals", spec='¼" alum. plate, 6"×8"'),
    Part("crossslide-hgr15", "Cross-slide rail HGR15 (Option A)", "bearings-motion",
         "film", 8, "ea", 25, 25, "Automation Overstock", "McMaster-Carr", spec="300mm, X-Z stage"),
    Part("crossslide-hgh15ca", "Cross-slide carriage HGH15CA (Option A)", "bearings-motion",
         "film", 8, "ea", 12, 12, "Automation Overstock", "McMaster-Carr", spec="Flanged block"),
    Part("crossslide-plate", "Cross-slide intermediate plate (Option A)", "aluminum",
         "film", 4, "ea", 15, 15, "Metal Supermarkets", "Online Metals", spec='¼" alum., joins X slide to Z slide'),
    Part("rod-end-bearing", "Rod-end spherical bearing", "bearings-motion",
         "film", 8, "ea", 22, 22, "McMaster-Carr", "Amazon Industrial", part_no="60645K73", spec="GIR25-DO or equiv., 25mm bore"),
    Part("pivot-pin", "Pivot pin SS316", "fasteners-hardware",
         "film", 8, "ea", 8, 8, "McMaster-Carr", "Fastenal", spec='Ø25mm × 200mm — slip-fit in the 25mm rod-end bore (a 1\"/25.4mm pin is 0.4mm oversize and will not enter). Metric Ø25 SS precision shaft/clevis pin; confirm exact SKU at order.'),
    # — Film Plane Frame (1,046) —
    Part("alu-angle-2x2", 'Aluminum angle 2"×2"×3/16"', "aluminum",
         "film", 10, "ea", 22, 22, "Metal Supermarkets", "Online Metals", spec="8 ft lengths"),
    Part("dibond-acm-film", "Dibond ACM panel 4mm", "plastics-sheet",
         "film", 6, "sheet", 85, 85, "Grimco", "Signwarehouse",
         spec="4 ft × 8 ft sheets — single rigid backing, {{fact:film_plane_width_mm}}×{{fact:film_plane_height_mm}}mm"),
    Part("epdm-foam-tape", 'Black EPDM foam tape 1"×½"', "seals-gaskets",
         "film", 3, "roll", 28, 28, "McMaster-Carr", "Grainger", part_no="8614K84", spec="50 ft rolls"),
    Part("rosco-duvetyne", "Rosco Duvetyne", "fabric-textile",
         "film", 1, "ea", 95, 95, "B&H Photo", "Rosco direct", spec='60" wide, 10 yd'),
    Part("poly-sheeting-film", "6-mil black poly sheeting", "tools-safety",
         "film", 1, "roll", 65, 65, "Home Depot", "Uline", spec="10 ft × 100 ft"),
    Part("gorilla-tape", '2" black Gorilla Tape', "adhesives-finishes",
         "film", 6, "roll", 12, 12, "Home Depot", "Amazon", spec="35 yd rolls"),
    # — Wall-Seat Saddles (440; rev12 ×6, the 2 BR ends are walkway combined plates) —
    Part("wall-seat-saddle", "Mild steel plate 8mm (laser/plasma cut + welded)", "steel-structural",
         "film", 6, "ea", 53, 53, "Metal Supermarkets", "Online Metals",
         spec="ICP-11: back-plate + exterior plate + seat + gusset per saddle; ~21 kg over 6 saddles"),
    Part("saddle-m12-bolt", "M12×90mm hex through-bolt + nut + washers, SS", "fasteners-hardware",
         "film", 28, "ea", 2.5, 2.5, "McMaster-Carr", "Amazon", spec="ICP-12: wall sandwich through-bolt; 4/saddle ×6 + 4 spare"),
    Part("saddle-m8-thumb", "M8×25mm knurled thumbscrew DIN 464", "fasteners-hardware",
         "film", 12, "ea", 3, 3, "Amazon", "Maedler", spec="ICP-13: left-rail drop-in hold-down; 2/saddle ×4 left + 4 spare"),
    Part("saddle-m8-hex", "M8 hex fixing bolt + nut, SS", "fasteners-hardware",
         "film", 8, "ea", 2, 2, "McMaster-Carr", "Amazon", spec="ICP-14: right-rail permanent fixing; 2/saddle ×2 TR + spare"),
    # ═══ clamp (film-clamp-mechanism-report §4) — split out of FILM; itemized, sums to the FILM
    # clamp lines (clamps 276–736 + mounting 76) = 352–812 ═══
    Part("cam-lever-clamp", "Cam-lever spring clamp", "fasteners-hardware",
         "clamp", 92, "ea", 3, 8, "McMaster-Carr", "Amazon", spec="Toggle-style, ~5N, neoprene jaw (Destaco equiv. / generic)"),
    Part("clamp-m5-bolt", "M5×16 SS socket head bolt", "fasteners-hardware",
         "clamp", 184, "ea", 0.25, 0.25, "McMaster-Carr", "Bolt Depot", part_no="91292A128", spec="A2-70 stainless"),
    Part("clamp-m5-nut", "M5 SS Nylock nut", "fasteners-hardware",
         "clamp", 184, "ea", 0.08, 0.08, "McMaster-Carr", "Bolt Depot", part_no="93625A200", spec="A2-70 stainless"),
    Part("clamp-neoprene", "Neoprene strip 60A", "seals-gaskets",
         "clamp", 1, "roll", 15, 15, "McMaster-Carr", "Grainger", part_no="8614K44", spec="35mm × 6mm, self-adhesive, 10m"),

    # ═══ lightlock (hinged-panel §8.2) — housing + drum; sums to costing.LIGHTLOCK ($1,385–$2,070) ═══
    Part("ll-hdpe-housing", "5mm UV-stabilized HDPE sheet (black)", "plastics-sheet",
         "lightlock", 1, "lot", 180, 280, "TAP Plastics", "Online Metals",
         spec="Ø900 fixed housing shell — LT_HOUSING_T (rolled + extrusion-welded, ~7 m²)"),
    Part("ll-pp-drum", "4mm black polypropylene sheet", "plastics-sheet",
         "lightlock", 1, "lot", 150, 240, "TAP Plastics", "Curbell",
         spec="Ø864 revolving drum shell + top/bottom caps — LT_DRUM_T (~7 m²)"),
    Part("ll-skf-bearing", "SKF 6215-2RS1 sealed bearing", "bearings-motion",
         "lightlock", 2, "ea", 45, 65, "Bearing World", "Applied", spec="Top and bottom (drum rotation)"),
    Part("ll-stub-shafts", "75mm Ø × 150mm steel stub shaft", "steel-structural",
         "lightlock", 2, "ea", 15, 25, "steel service center", spec="Bearing shafts"),
    Part("ll-wiper-seal", "Felt/brush wiper strip + 12mm closed-cell neoprene", "seals-gaskets",
         "lightlock", 1, "lot", 40, 60, "McMaster-Carr", spec="Drum↔housing rotating seal (opening edges + top/bottom rings) + drum top/bottom"),
    Part("ll-silicone-sealant", "Silicone bead sealant (black, UV-stable)", "adhesives-finishes",
         "lightlock", 1, "ea", 10, 15, "McMaster-Carr", spec="Bearing housing seal"),
    Part("ll-grab-rail", "100mm Ø SS grab rail", "fasteners-hardware",
         "lightlock", 1, "ea", 15, 25, "McMaster-Carr", spec="Interior handle, 400mm cut length"),
    Part("ll-matte-finish", "Matte-black interior finish", "adhesives-finishes",
         "lightlock", 1, "ea", 40, 70, "local", spec="Black-pigmented sheet (no etch-prime); scuff + flat-black touch-in at welds"),
    Part("ll-fasteners", "Stainless fasteners + nylon isolation washers", "fasteners-hardware",
         "lightlock", 1, "lot", 30, 50, "McMaster-Carr", spec="Steel shaft/bearing ↔ plastic shell joints (no galvanic couple)"),
    Part("ll-fabrication", "Plastic fabrication (roll 2 cylinders, hot-air / extrusion weld, fit, bearings)", "fabrication-labor",
         "lightlock", 1, "lot", 800, 1150, "Local plastic fab", spec="16–22 hrs labor"),

    # ═══ swing (hinged-panel §8.3) — swing pivot hardware; sums to SWINGPIVOT minus door ($520–$880) ═══
    Part("sp-pivot-post", "Ø89×8mm CHS pivot post + machined hub / thrust collar", "steel-structural",
         "swing", 1, "ea", 180, 300, "Metal Supermarkets", "local fab",
         spec="Upgrades the reused film far-left upright; carries the ~3.6 kN·m swing cantilever — SF 3.7 in S355"),
    Part("sp-thrust-bearing", "Turntable thrust bearing, 12″ (Ø305) 1000 lb", "bearings-motion",
         "swing", 1, "ea", 40, 60, "VXB", spec="Carries the ~330 kg (3.24 kN) vertical load at the post base; thrust-only"),
    Part("sp-sleeve-bearings", "Flanged sleeve (journal) bearing, Ø90 bore", "bearings-motion",
         "swing", 2, "ea", 30, 55, "McMaster-Carr", spec="Top + bottom radial location of the post / hub (SAE 841 bronze)"),
    Part("sp-drum-cage", "Drum support cage, 40 × 40 × 3mm SHS", "steel-structural",
         "swing", 1, "lot", 70, 120, "local fab", spec="Steel frame carrying the Ø900 housing + drum on the swinging leaf"),
    Part("sp-wall-stays", "Top + bottom wall stays + 4-bolt anchor plates", "fasteners-hardware",
         "swing", 2, "set", 45, 80, "McMaster-Carr", spec="Transport lock — M16 turnbuckle + eye/hook rods + inside/outside wall plates"),
    Part("sp-rail-saddles", "Drop-in rail saddles + tapered dowels", "steel-structural",
         "swing", 4, "ea", 20, 32.5, "local fab", "McMaster-Carr", spec="For the 2 removable left film rails (TL + BL); dowels set the film datum"),
    # ═══ door (hinged-panel §8.4) — fixed door frame; sums to the SWINGPIVOT door lines ($335–$550) ═══
    Part("sp-door-frame-rhs", "50 × 50 × 3mm RHS mild steel (6 m lengths)", "steel-structural",
         "door", 3, "ea", 30, 40, "Metal Supermarkets", spec="Frame members"),
    Part("sp-door-seal-lips", "3mm steel plate/angle (~110mm × ~4 m)", "steel-structural",
         "door", 1, "lot", 45, 80, "Metal Supermarkets", spec="Top + bottom seal lips — threshold upstand + frame-top downstand; seal paths #3–#4"),
    Part("sp-door-fab", "Welding / fabrication", "fabrication-labor",
         "door", 1, "lot", 200, 350, "local fab", spec="Frame assembly + wall attachment"),

    # ═══ panel (hinged-panel §8.1) — panel structure; sums to costing.PANEL ($1,124–$1,691) ═══
    Part("panel-rhs-frame", "50 × 50 × 3mm RHS mild steel (6 m lengths)", "steel-structural",
         "panel", 4, "ea", 30, 40, "Metal Supermarkets", spec="Frame perimeter + internal members"),
    Part("panel-pp-skins", "4mm black PP plastic sheet (1220 × 2,440mm)", "plastics-sheet",
         "panel", 4, "sheet", 65, 105, "TAP Plastics", "Curbell", spec="Panel skins, both faces (~12 m²) — rev11, replaces 18mm ply"),
    Part("panel-fanb-ply", "Exterior-grade plywood (Fan B mount band)", "timber-ply",
         "panel", 1, '2\'×4\' ¾" panel', 30, 50, "Home Depot",
         spec='¾" (18mm) exterior-grade project panel (610×1220mm); Fan B mount band, one corner bottom→1,125mm'),
    Part("panel-corner-plates", "3mm aluminum plate (1220 × 2,440mm)", "aluminum",
         "panel", 2, "ea", 180, 230, "Online Metals", spec="Corner zone core plates"),
    Part("panel-epdm-gasket", "20mm EPDM gasket (per meter, closed-cell)", "seals-gaskets",
         "panel", 21, "m", 4, 6, "McMaster-Carr", spec="Perimeter seal (~10 m) + housing-surround ring (~6 m) + 2× vertical cut seals at Yd180/2287 (~5 m)"),
    Part("panel-u-channel", "Aluminum U-channel (per meter)", "aluminum",
         "panel", 40, "m", 3, 5, "Online Metals", spec="Gasket retainer + PP-skin retention (perimeter + housing-surround + stiffener grid)"),
    Part("panel-southco-latch", "Southco C2-33 cam compression latch", "fasteners-hardware",
         "panel", 4, "ea", 15, 25, "Southco", "McMaster-Carr", spec="Interior-mounted corner latches (compress the perimeter + cut + lip seals)"),
    Part("panel-b2-bay", "4mm black PP sheet + EPDM lip", "plastics-sheet",
         "panel", 1, "lot", 60, 120, "TAP Plastics", spec="B2 punch-out bay — 4-wall light-tight tube (~890mm deep) around the housing (rev11)"),
    Part("panel-paint", "Flat black paint (RAL 9005)", "adhesives-finishes",
         "panel", 1, "qt", 10, 20, "local", spec="Bay/weld touch-in (PP skins are pre-pigmented black)"),
    Part("panel-grab-handle", "316 SS D-grab pull handle (~300mm) + 2× M8 SS bolts + backing plate, matte-black", "fasteners-hardware",
         "panel", 1, "ea", 20, 35, "McMaster-Carr", spec="Interior pull handle — through-bolted to the frame (§4.3)"),

    # ═══ shelf (§7 chem-prep) — mirrors costing.SHELF → exact $203 ═══
    Part("shelf-phenolic-ply", "Phenolic-faced plywood (work surface)", "timber-ply",
         "shelf", 1, '4\'×8\' ¾" sheet', 60, 60, "Home Depot", "lumber yard",
         spec='¾" (18mm) phenolic-faced concrete-form sheet (1220×2440mm), cut to 300×600'),
    Part("shelf-steel-shs", "25×25×3 mm steel SHS", "steel-structural",
         "shelf", 1, "lot", 30, 30, "Online Metals", "Metal Supermarkets", spec="6 m (frame + spill lip)"),
    Part("shelf-piano-hinge", "Continuous (piano) hinge, 600 mm", "fasteners-hardware",
         "shelf", 1, "ea", 20, 20, "McMaster-Carr", spec="stainless/steel, ~32 mm leaf"),
    Part("shelf-folding-stays", "Folding shelf stays/brackets", "fasteners-hardware",
         "shelf", 2, "ea", 12, 12, "Amazon", "McMaster-Carr", spec="fold-flat, ~30–50 kg rating"),
    Part("shelf-wall-cleat", "Wall mounting cleat + anchors", "steel-structural",
         "shelf", 1, "lot", 18, 18, "Local fab", spec="6 mm steel cleat + 2 stay anchors (slotted)"),
    Part("shelf-m8-bolts", "M8 wall bolts + washers/nuts", "fasteners-hardware",
         "shelf", 12, "ea", 1, 1, "McMaster-Carr", spec="hinge cleat + stay anchors into the wall ribs"),
    Part("shelf-transport-latch", "Transport latch (over-center/barrel)", "fasteners-hardware",
         "shelf", 1, "ea", 8, 8, "Amazon", spec="secures the folded board"),
    Part("shelf-csk-screws", "M5×16 mm CSK screws", "fasteners-hardware",
         "shelf", 8, "ea", 0.5, 0.5, "McMaster-Carr", spec="ply panel attachment"),
    Part("shelf-gusset-plates", "Corner gusset plate, 3 mm", "steel-structural",
         "shelf", 4, "ea", 1.25, 1.25, "Steel offcut", spec="50×50 mm triangular"),
    Part("shelf-paint", "Flat black epoxy spray paint", "adhesives-finishes",
         "shelf", 1, "can", 12, 12, "Hardware store", spec="frame + hardware finish"),
    Part("shelf-hdpe-pipe", '½" HDPE pipe (tap relocation)', "plumbing-fittings",
         "shelf", 1, "lot", 10, 10, "Irrigation supply", spec="extend the blue supply trunk ~1.3 m left to TAP-01"),

    # ═══ walkway (§10) — re-decomposed to match the report (fab bundled into each bracket, no
    # separate fab line) → $2,005–$2,985 (reconciles to EXPECTED walkway $2,000–$2,975 within tol) ═══
    Part("walkway-grp-grating", "Molded GRP (fiberglass) grating", "plastics-sheet",
         "walkway", 1, "lot", 965, 1250, "McNichols", "Grating Pacific",
         spec="15mm, vinyl-ester resin, grit top, ~38mm mesh; ~4.5 m² (4 sections)"),
    Part("walkway-drum-exit-grp", "Drum-exit punch-out grating", "plastics-sheet",
         "walkway", 1, "lot", 50, 65, "McNichols", spec="Extra GRP landing (~0.23 m²) at the light-lock exit"),
    Part("walkway-std-brackets", "Cantilever bracket — standard (near/far)", "steel-structural",
         "walkway", 14, "ea", 30, 50, "Local fab",
         spec="8mm steel plate: 150mm vert leg + 300mm arm + 70mm gusset, welded (5 near + 9 far at 457mm centers)"),
    Part("walkway-wide-brackets", "Cantilever bracket — widened (near)", "steel-structural",
         "walkway", 4, "ea", 40, 70, "Local fab",
         spec="10mm steel plate: 200mm vert leg + 500mm arm + 70mm gusset, welded (EP/battery/slit zone)"),
    Part("walkway-m12-bolts", "M12×80mm through-bolt kit", "fasteners-hardware",
         "walkway", 58, "ea", 1.5, 2.5, "McMaster-Carr", spec="Hex bolt + 2× washers + nut, grade 8.8 (3 per std + 4 per widened)"),
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
    Part("walkway-throughbolts", "M12 through-bolt kit (right walkway)", "fasteners-hardware",
         "walkway", 24, "ea", 1.25, 2.0833, "McMaster-Carr", spec="Wall cleats + combined plates + 2 center-arm U-clamps to the IBC uprights"),
    Part("walkway-floor-legs", "Floor-leg cantilever bracket (left walkway, ×5)", "steel-structural",
         "walkway", 5, "ea", 11, 19, "Local fab",
         spec="50×50×3mm SHS post (~115mm) + 40×40×3mm SHS arm (2 reach X470, 3 extended to X770) + 128×60×8mm foot plate"),
    Part("walkway-floor-anchors", "M10 wedge floor anchors", "fasteners-hardware",
         "walkway", 20, "ea", 1.25, 2.25, "McMaster-Carr", spec="4 per foot plate (20 total), sealed into the container floor"),
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
        # aggregate the same key across systems
        agg: dict[str, dict] = {}
        for p in items:
            a = agg.setdefault(p.key, {"desc": p.desc, "qty": 0.0, "unit": p.unit,
                                       "sup": canon_supplier(p.supplier), "sys": set(), "lo": 0.0, "hi": 0.0})
            a["qty"] += p.qty
            a["sys"].add(p.system)
            lo, hi = line(p); a["lo"] += lo; a["hi"] += hi
        sub_lo = sub_hi = 0.0
        for a in sorted(agg.values(), key=lambda x: x["desc"].lower()):   # rows A–Z by item name
            cost = _money(a["lo"]) if round(a["lo"]) == round(a["hi"]) else f"{_money(a['lo'])}–{_money(a['hi'])}"
            out.append(f"| {a['desc']} | {a['qty']:g} {a['unit']} | {a['sup']} | "
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
_CLAMP_LINES = ("Cam-lever spring clamps", "Clamp mounting")


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
