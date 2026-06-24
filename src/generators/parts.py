#!/usr/bin/env python3
"""parts.py — the UNIFIED PARTS REGISTRY (drift-reduction Phase 5).

The single source of every purchasable item: quantity, type, supplier, unit-cost band, the
verified physical SIZE (folds in component-dimension-audit), and the cyanotype chemistry tiers.

From this ONE source, GENERATED views (Phase 2):
  • master-shopping-list.md     — by TYPE, qty summed across systems, grouped by SUPPLIER (procurement).
  • each report's §Parts-List    — by SYSTEM (emit_system).
  • component-dimension-audit.md — real-vs-modeled size reconciliation (emit_dimension_audit).
  • chemistry-shopping-list.md   — cyanotype-only shopping (emit_chemistry).
And (Phase 3) costing.py section totals derive from system_total().

This file is being built incrementally — see /Users/.../plans (Phase 0..3). Right now ONE system
(ventilation) is populated end-to-end to prove the schema + the costing reconciliation guardrail:
every system present here must sum to costing.EXPECTED[system].
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
    Part("plywood-base-12", "Plywood base plate", "timber-ply",
         "ventilation", 1, "ea", 8, 8, "Home Depot", "Lumber yard", spec="12mm, 600 × 350mm (cooler stowage)"),

    # ═══ water family (split per owning report; reconciled to costing.WATER lines — water-system §8
    # item-sums after the 2026 reconciliation). The §8 group ("water") = storage+pumps+filter+valves+
    # pipe+wiring+consumables; the frame/tray/spray are SEPARATE systems (their own reports). The §8
    # bundles below are placeholders pending full itemization (Increment 2). ═══
    # — storage (395–720) —
    Part("ibc-tote-1000l", "IBC tote 1,000L (275 gal), food-grade, used/rinsed", "water-equipment",
         "water", 4, "ea", 80, 150, "Container Exchanger",
         url="https://containerexchanger.com/geo-sale-ads/us-ca/bulk-containers/ibc-totes-for-sale",
         spec="Caged composite tote, DN50 butterfly valve (S60×6 thread); side-entry fittings near top"),
    Part("bulkhead-2in", 'Bulkhead fitting 2" NPT (304 SS)', "plumbing-fittings",
         "water", 3, "ea", 25, 40, "McMaster-Carr", part_no="4464K115",
         url="https://www.mcmaster.com/4464K115", spec="External fill/drain port, welded through container wall"),
    # — pumps (315–345) —
    Part("shurflo-2088-p12", "Shurflo 2088-554-144 pump (P-01, P-02)", "water-equipment",
         "water", 2, "ea", 55, 70, "Amazon",
         url="https://www.amazon.com/Shurflo-2088-554-144-Fresh-Gallons-Minute/dp/B00C1M6B1C",
         spec='12VDC, 3.5 GPM, 45 PSI, 1/2" NPSM ports'),
    Part("shurflo-2088-p3", "Shurflo 2088-554-144 pump (P-03 waste evacuation)", "water-equipment",
         "water", 1, "ea", 65, 65, "Amazon", spec="12VDC, 3.5 GPM, 45 PSI; empties IBC-4 residual below X4 (~120L)"),
    Part("shurflo-2088-p4", "Shurflo 2088-554-144 pump (P-04 tray drain transfer)", "water-equipment",
         "water", 1, "ea", 65, 65, "Amazon", spec="12VDC, 3.5 GPM, 45 PSI; tray drain to IBC-3 (~900mm lift)"),
    Part("seaflo-accumulator", "SeaFlo pressure accumulator", "water-equipment",
         "water", 1, "ea", 35, 35, "Amazon",
         url="https://www.amazon.com/Seaflo-Accumulator-Control-Internal-Bladder/dp/B01MUYL8F8",
         spec='0.75 L, 125 PSI, 1/2" MNPT'),
    Part("shurflo-bracket", "Shurflo pump mounting bracket", "fasteners-hardware",
         "water", 4, "ea", 10, 10, "Amazon", spec="Stainless, 2088 series (3× manifold + 1× IBC corridor for P-03)"),
    # — filter (282–445) —
    Part("bigblue-3stage", 'Big Blue 3-stage combo filter unit 4.5"×10"', "water-equipment",
         "water", 1, "ea", 200, 300, "Amazon", dims="Ø184×333",
         spec='Ø184×333mm/housing, 1" NPT ports, integrated bracket (Express Water / Geekpure / iSpring)'),
    Part("cartridge-sediment", 'MPP 5-micron sediment cartridge 4.5"×10"', "water-equipment",
         "water", 3, "ea", 6, 10, "Amazon", spec="Melt-blown polypropylene depth filter (F-1 stage)"),
    Part("cartridge-kdf", 'KDF-55 heavy-metal cartridge 4.5"×10"', "water-equipment",
         "water", 2, "ea", 20, 35, "Amazon", spec="KDF-55 media for dissolved iron/metal removal (F-2 stage)"),
    Part("cartridge-carbon", 'CTO carbon block cartridge 4.5"×10"', "water-equipment",
         "water", 3, "ea", 8, 15, "Amazon", spec="Coconut shell activated carbon block (F-3 stage)"),
    # — valves & fittings (333–567) —
    Part("valve-v050fp", 'Banjo V050FP ball valve 1/2" FNPT', "plumbing-fittings",
         "water", 4, "ea", 6, 10, "Amazon", spec="PP full-port quarter-turn; BV-01, BV-02 + spares"),
    Part("valve-v100fp", 'Banjo V100FP ball valve 1" FNPT', "plumbing-fittings",
         "water", 6, "ea", 10, 16, "Amazon", spec="PP full-port; V1/V3/V4, VB1–VB3 (IBC fill/drain)"),
    Part("valve-v075fp", 'Banjo V075FP ball valve 3/4" FNPT', "plumbing-fittings",
         "water", 1, "ea", 8, 12, "Amazon", spec="PP full-port; BV-06 (chemistry tap shut-off)"),
    Part("valve-3way-half", '3-way diverter valve 1/2" FNPT', "plumbing-fittings",
         "water", 1, "ea", 12, 22, "Amazon", spec="L/T-port HDPE-compatible; 3W-DV-02 (tray drain)"),
    Part("valve-3way-1in", '3-way diverter valve 1" FNPT', "plumbing-fittings",
         "water", 1, "ea", 18, 30, "Amazon", spec="L/T-port; 3W-DV-01 (filter output)"),
    Part("camlock-2in", '2" polypropylene camlock pairs (M+F)', "plumbing-fittings",
         "water", 4, "pair", 5, 8, "Amazon", spec="External bulkhead connections (X1/X3/X4 + spare)"),
    Part("elbow-half", '1/2" NPT 90° elbow polypropylene', "plumbing-fittings",
         "water", 14, "ea", 2, 4, "Amazon", spec="All pump-driven run bends"),
    Part("elbow-el100", 'Banjo EL100-90 elbow 1" NPT', "plumbing-fittings",
         "water", 4, "ea", 3, 5, "Amazon", spec="PP 90°; IBC bends, filter outlet to DV-01"),
    Part("tee-half", '1/2" NPT polypropylene tee', "plumbing-fittings",
         "water", 6, "ea", 2, 4, "Amazon", spec="Blue suction/discharge tees, branches"),
    Part("tee-100", 'Banjo TEE100 equal tee 1" NPT', "plumbing-fittings",
         "water", 4, "ea", 4, 6, "Amazon", spec="PP; IBC fill/drain tees"),
    Part("union-half", '1/2" NPT polypropylene union', "plumbing-fittings",
         "water", 6, "ea", 4, 6, "Amazon", spec="Maintenance disconnects on pump runs"),
    Part("bushing-reducer", '1/2"×1" NPT bushing reducer', "plumbing-fittings",
         "water", 1, "ea", 3, 5, "Amazon", spec="P-02 riser to F1 filter inlet"),
    Part("s60-adapter", 'S60×6 to 1" NPT adapter', "plumbing-fittings",
         "water", 8, "ea", 8, 15, "Amazon", spec='IBC DN50 valve to 1" HDPE; PP S60×6 male × 1" NPT female'),
    Part("check-valve-1in", '1" NPT spring check valve (CV1/CV3/CV4)', "plumbing-fittings",
         "water", 3, "ea", 8, 14, "Amazon", spec='PVC body, EPDM seal, 1" FNPT × FNPT'),
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
    Part("water-blade-fuses", "10A blade fuses (pack)", "electrical-distribution",
         "water", 1, "pack", 5, 5, "Amazon", spec="Pump circuits (C1–C4)"),
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
         "ibc-frame", 4, "ea", 30, 45, "Metal Supermarkets", spec="Front-portal uprights + front retaining bars + panel-mount rail"),
    Part("ibcf-feet", "12mm steel plate, 150 × 150 cut", "steel-structural",
         "ibc-frame", 2, "ea", 5, 10, "Metal Supermarkets", spec="Upright floor flange feet"),
    Part("ibcf-hangers", "4mm folded plate", "steel-structural",
         "ibc-frame", 4, "ea", 7.5, 12.5, "local fab", spec="Simpson-style wall joist hangers"),
    Part("ibcf-dring", "25mm welded D-ring", "fasteners-hardware",
         "ibc-frame", 4, "ea", 5, 8.75, "McMaster-Carr", part_no="3641T29", spec="Lashing holders on the front bars, 6mm mount plates"),
    Part("ibcf-strap", "25mm ratchet strap, 1,100 kg WLL", "fasteners-hardware",
         "ibc-frame", 4, "ea", 7.5, 12.5, "Amazon", spec="Transport securing, over each stack"),
    Part("ibcf-floor-anchor", "M12 floor anchor (wedge/sleeve, container floor)", "fasteners-hardware",
         "ibc-frame", 8, "ea", 1.875, 3.75, "McMaster-Carr", spec="Upright flange feet, 4 each"),
    Part("ibcf-m12-bolt", "M12 × 40 bolt, Grade 8.8", "fasteners-hardware",
         "ibc-frame", 12, "ea", 1, 22 / 12, "McMaster-Carr", spec="Wall hangers (2 each) + front-bar cleats"),
    Part("ibcf-fabrication", "Welding / fabrication (frame assembly)", "fabrication-labor",
         "ibc-frame", 1, "lot", 688, 1018, "local fab", spec="~14–20 hrs labor (single front portal)"),
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
    # — spray (processing-tray-and-spray-bar §6.2) — itemized, sums to costing spray (235–299;
    #   the $1/$3 report-subtotal rounding is absorbed into the AL-plate estimate so the block total
    #   matches the canonical figure) —
    Part("spray-al-shs", '6061-T6 AL SHS 1-1/2"×1-1/2"×1/8", 8 ft', "aluminum",
         "spray", 2, "ea", 18, 28, "Online Metals", spec="40×40×3mm, joined with internal sleeve"),
    Part("spray-al-plate", '6061-T6 AL plate 3/16" (5mm)', "aluminum",
         "spray", 1, "ea", 16, 28, "Online Metals", spec="Carriage plates + spacer blocks (~300 × 500mm sheet)"),
    Part("spray-al-bar", "30×30mm AL solid bar, 150mm", "aluminum",
         "spray", 1, "ea", 8, 12, "Online Metals", spec="Internal splice sleeve"),
    Part("spray-ldpe-pipe", '3/4" LDPE irrigation poly pipe, 15 ft', "plumbing-fittings",
         "spray", 1, "ea", 10, 10, "Amazon", spec="Internal spray pipe (OD 25mm, ID 19mm)"),
    Part("spray-nozzles", "Flat-fan irrigation spray nozzles, barbed", "plumbing-fittings",
         "spray", 26, "ea", 30 / 26, 50 / 26, "Amazon", spec="180° fan pattern, barbed inlet"),
    Part("spray-manifold", 'Distribution manifold, 1/2" → 7 barb outlets', "plumbing-fittings",
         "spray", 1, "ea", 12, 12, "Amazon", spec="Mounted at ball joint, splits feed to tubes"),
    Part("spray-feed-tube", '1/4" irrigation poly tube', "plumbing-fittings",
         "spray", 1, "ea", 6, 6, "Amazon", spec="Manifold to beam feed points (~7m total)"),
    Part("spray-barbed-feed", "Barbed feed fittings, through beam top", "plumbing-fittings",
         "spray", 7, "ea", 10 / 7, 10 / 7, "Amazon", spec="Tube to poly pipe, 7 feed points"),
    Part("spray-retainer-clips", 'SS/nylon retainer clips for 3/4" LDPE', "fasteners-hardware",
         "spray", 2, "ea", 2, 2, "Amazon", spec="Fold-back end closures"),
    Part("spray-skate-wheel", "Nylon skate wheel, 50mm × 20mm, 10mm bore", "bearings-motion",
         "spray", 4, "ea", 3, 5, "McMaster-Carr",
         url="https://www.mcmaster.com/products/rollers/skate-wheels-1~/", spec="Flat tread, ≥25 kg rated (2 per carriage)"),
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
         "spray", 16, "ea", 7 / 16, 7 / 16, "McMaster-Carr", spec="Carriage plate, beam clamp, saddle, splice fasteners"),
    Part("spray-self-tap", "Self-tapping SS screws (8-pack)", "fasteners-hardware",
         "spray", 4, "ea", 5 / 4, 5 / 4, "McMaster-Carr", spec="Ball-joint flange to beam top wall"),
    Part("spray-ball-joint", "Ø20mm ball joint, zinc socket, M12 stud", "bearings-motion",
         "spray", 1, "ea", 12, 12, "Amazon", spec="Multi-axis arm articulation"),
    Part("spray-beam-clamp", "SS beam clamp plates (top + bottom) + spacers (40mm)", "fasteners-hardware",
         "spray", 4, "ea", 2.5, 2.5, "McMaster-Carr", spec="Beam to carriage plate (sandwich, bolted)"),
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
    Part("pump-switches", "Pump switches (Circuit C) — IP67 sealed rocker 12V 16A", "electrical-distribution",
         "electrical", 5, "ea", 6, 6, "Amazon", "Waytek Wire"),
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

    # ═══ film (§4) — mirrors costing.FILM → exact $3,538–$4,088 ═══
    Part("hgr20-rails-carriages", "Linear guide rails HGR20 2,200mm (×4) + carriages HGH20CA (×8)",
         "bearings-motion", "film", 1, "set", 324, 324, "Amazon", "Automation Overstock",
         note="2 carriages per rail"),
    Part("acme-leadscrews", 'Acme leadscrews ¾"-6 8 ft (×4) + bronze nuts (×4)', "bearings-motion",
         "film", 1, "set", 428, 428, "McMaster-Carr", note="manual handwheel drive"),
    Part("handwheels-collars", 'Handwheels 8" (×4) + locking collars SS316 (×4)', "bearings-motion",
         "film", 1, "set", 188, 188, "McMaster-Carr"),
    Part("corner-l-plates", 'Corner bracket L-plates, ¼" alum 6×8 (×4)', "aluminum",
         "film", 4, "ea", 20, 20, "Online Metals"),
    Part("crossslide-hgr15", "Option-A cross-slides — HGR15 rails (×8) + HGH15CA (×8) + intermediate plates (×4)",
         "bearings-motion", "film", 1, "set", 356, 356, "Amazon", note="floating-corner X–Z stage"),
    Part("rod-end-bearings", "Rod-end spherical bearings GIR25-DO (×8) + pivot pins SS316 (×8)",
         "bearings-motion", "film", 1, "set", 240, 240, "McMaster-Carr"),
    Part("alu-angle-2x2", "Aluminum angle 2×2×3/16 8 ft (×10)", "aluminum",
         "film", 10, "ea", 22, 22, "Online Metals"),
    Part("dibond-acm-film", "Dibond ACM 4mm 4×8 sheets (×6) — single rigid plane", "plastics-sheet",
         "film", 6, "sheet", 85, 85, "TAP Plastics", note="Option A: no folding hinge"),
    Part("light-seal-set-film", "Light-seal set — EPDM tape (×3) + Rosco Duvetyne + 6-mil poly + Gorilla tape (×6)",
         "seals-gaskets", "film", 1, "set", 316, 316, "Rosco", "McMaster-Carr"),
    Part("cam-lever-clamps", "Cam-lever spring clamps, muslin (×92)", "fasteners-hardware",
         "film", 92, "ea", 3, 8, "Amazon", note="$3/$8 ea — the section's main Low/High driver"),
    Part("clamp-mounting-hw", "Clamp mounting — M5×16 SS bolts/Nylocks (×184+184) + neoprene jaw strip",
         "fasteners-hardware", "film", 1, "lot", 70, 70, "McMaster-Carr"),
    Part("wall-seat-saddles", "Wall-seat saddles ×8 — 8mm steel plate, cut + welded (ICP-11)", "steel-structural",
         "film", 8, "ea", 47.5, 58.75, "local fab", note="~28 kg total; back-plate + seat + gusset"),
    Part("saddle-fasteners", "Saddle fasteners — M12 through-bolts (×36) + M8 thumbscrews (×12) + M8 rail bolts (×12)",
         "fasteners-hardware", "film", 1, "lot", 150, 150, "McMaster-Carr", note="ICP-12/13/14"),

    # ═══ lightlock (§7) — mirrors costing.LIGHTLOCK → exact $1,385–$2,070 ═══
    Part("ll-hdpe-housing", "5mm UV-stabilized HDPE — Ø900 housing shell (~7 m²)", "plastics-sheet",
         "lightlock", 1, "lot", 180, 280, "TAP Plastics", "Online Metals", note="rolled + extrusion-welded"),
    Part("ll-pp-drum", "4mm PP — Ø864 drum shell + top/bottom caps (~7 m²)", "plastics-sheet",
         "lightlock", 1, "lot", 150, 240, "TAP Plastics", "Curbell"),
    Part("ll-skf-bearing", "SKF 6215-2RS1 sealed bearing (×2)", "bearings-motion",
         "lightlock", 2, "ea", 45, 65, "Bearing World", "Applied"),
    Part("ll-stub-shafts", "75mm Ø × 150mm steel stub shafts (×2)", "steel-structural",
         "lightlock", 2, "ea", 15, 25, "steel service center"),
    Part("ll-wiper-seal", "Felt/brush wiper + 12mm neoprene (drum↔housing seal)", "seals-gaskets",
         "lightlock", 1, "lot", 40, 60, "McMaster-Carr"),
    Part("ll-silicone-sealant", "Silicone bead sealant (bearing housing)", "adhesives-finishes",
         "lightlock", 1, "ea", 10, 15, "McMaster-Carr"),
    Part("ll-grab-rail", "100mm Ø SS grab rail (400mm cut)", "fasteners-hardware",
         "lightlock", 1, "ea", 15, 25, "McMaster-Carr"),
    Part("ll-matte-finish", "Matte-black interior finish", "adhesives-finishes",
         "lightlock", 1, "job", 40, 70, "local", note="scuff + flat-black touch-in"),
    Part("ll-fasteners", "Stainless fasteners + nylon isolation washers (no galvanic couple)", "fasteners-hardware",
         "lightlock", 1, "lot", 30, 50, "McMaster-Carr"),
    Part("ll-fabrication", "Plastic fabrication — roll + weld 2 cylinders, fit (16–22 hrs)", "fabrication-labor",
         "lightlock", 1, "job", 800, 1150, "Local plastic fab"),

    # ═══ swingpivot (§8.3–8.4) — mirrors costing.SWINGPIVOT → exact $855–$1,430 ═══
    Part("sp-pivot-post", "Ø89×8 CHS pivot post + machined hub / thrust collar", "steel-structural",
         "swingpivot", 1, "ea", 180, 300, "Metal Supermarkets", "local fab", note="carries ~3.6 kN·m swing cantilever"),
    Part("sp-thrust-bearing", "Turntable thrust bearing, 12″ (Ø305) 1000 lb", "bearings-motion",
         "swingpivot", 1, "ea", 40, 60, "VXB"),
    Part("sp-sleeve-bearings", "Flanged sleeve (journal) bearings, Ø90 bore (×2)", "bearings-motion",
         "swingpivot", 2, "ea", 30, 55, "McMaster-Carr", note="SAE 841 bronze"),
    Part("sp-drum-cage", "Drum support cage, 40×40×3mm SHS", "steel-structural",
         "swingpivot", 1, "lot", 70, 120, "local fab"),
    Part("sp-wall-stays", "Top + bottom wall stays + 4-bolt anchor plates", "fasteners-hardware",
         "swingpivot", 2, "set", 45, 80, "McMaster-Carr", note="turnbuckles + rods + plates"),
    Part("sp-rail-saddles", "Drop-in rail saddles + tapered dowels (×4, removable left film rails)", "steel-structural",
         "swingpivot", 4, "ea", 20, 32.5, "local fab", "McMaster-Carr"),
    Part("sp-door-frame-rhs", "Fixed door frame — 50×50×3 RHS members (×3)", "steel-structural",
         "swingpivot", 3, "ea", 30, 40, "Metal Supermarkets"),
    Part("sp-door-seal-lips", "Fixed door frame — top/bottom seal lips (3mm steel ~110×4m)", "steel-structural",
         "swingpivot", 1, "lot", 45, 80, "Metal Supermarkets", note="seal paths #3–#4"),
    Part("sp-door-fab", "Fixed door frame — welding/fabrication + wall attachment", "fabrication-labor",
         "swingpivot", 1, "job", 200, 350, "local fab"),

    # ═══ panel (§8.1) — mirrors costing.PANEL → exact $1,124–$1,691 ═══
    Part("panel-rhs-frame", "50×50×3mm RHS mild steel — frame perimeter + members (4× 6m)", "steel-structural",
         "panel", 4, "ea", 30, 40, "Metal Supermarkets"),
    Part("panel-pp-skins", "4mm black PP sheet — panel skins both faces (~12 m², ×4)", "plastics-sheet",
         "panel", 4, "sheet", 65, 105, "TAP Plastics", "Curbell", note="rev11"),
    Part("panel-fanb-ply", "18mm exterior-grade plywood — Fan B mount band (0.5 sheet)", "timber-ply",
         "panel", 1, "lot", 30, 50, "Home Depot"),
    Part("panel-corner-plates", "3mm aluminum plate — corner-zone core plates (×2)", "aluminum",
         "panel", 2, "ea", 180, 230, "Online Metals"),
    Part("panel-epdm-gasket", "20mm EPDM gasket — perimeter + housing-surround + cut seals (~21 m)", "seals-gaskets",
         "panel", 21, "m", 4, 6, "McMaster-Carr"),
    Part("panel-u-channel", "Aluminum U-channel — gasket + PP-skin retention (~40 m)", "aluminum",
         "panel", 40, "m", 3, 5, "Online Metals"),
    Part("panel-southco-latch", "Southco C2-33 cam compression latch (×4)", "fasteners-hardware",
         "panel", 4, "ea", 15, 25, "Southco", "McMaster-Carr"),
    Part("panel-b2-bay", "4mm PP + EPDM lip — B2 punch-out bay (4-wall tube ~890mm)", "plastics-sheet",
         "panel", 1, "lot", 60, 120, "TAP Plastics", note="rev11"),
    Part("panel-paint", "Flat-black paint (RAL 9005) — bay/weld touch-in", "adhesives-finishes",
         "panel", 1, "lot", 10, 20, "local"),
    Part("panel-grab-handle", "316 SS D-grab pull handle (~300mm) + 2× M8 + backing plate", "fasteners-hardware",
         "panel", 1, "ea", 20, 35, "McMaster-Carr", note="matte-black, §4.3"),

    # ═══ shelf (§7 chem-prep) — mirrors costing.SHELF → exact $203 ═══
    Part("shelf-phenolic-ply", "Phenolic-faced plywood, 18 mm", "timber-ply",
         "shelf", 1, "ea", 60, 60, "Home Depot", "lumber yard", spec="cut to 300×600 mm"),
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
         "walkway", 1, "lot", 970, 1260, "McNichols", "Grating Pacific",
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
         spec="40×40×3mm SHS — 2 long beams ({{fact:container_width_mm}}mm) + 2 end beams (300mm) + 2 center arms (405mm), ~8 m"),
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


# ── Roll-ups ─────────────────────────────────────────────────────────────────
def systems() -> list[str]:
    return sorted({p.system for p in PARTS})


def by_system(sys: str) -> list[Part]:
    return [p for p in PARTS if p.system == sys]


def system_total(sys: str) -> tuple[int, int]:
    lo = sum(line(p)[0] for p in by_system(sys))
    hi = sum(line(p)[1] for p in by_system(sys))
    return (round(lo), round(hi))


def grand() -> tuple[int, int]:
    return (round(sum(line(p)[0] for p in PARTS)),
            round(sum(line(p)[1] for p in PARTS)))


def by_type() -> dict[str, list[Part]]:
    out: dict[str, list[Part]] = {}
    for p in PARTS:
        out.setdefault(p.type, []).append(p)
    return out


def by_supplier() -> dict[str, list[Part]]:
    out: dict[str, list[Part]] = {}
    for p in PARTS:
        out.setdefault(p.supplier or "—", []).append(p)
    return out


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
        sup = p.supplier + (f" / {p.supplier_alt}" if p.supplier_alt else "")
        rows.append(f"| {_item_cell(p)} | {_expand(p.spec) or '—'} | {p.qty:g} {p.unit} | {sup} | {cost} |")
    lo, hi = system_total(sys)
    tot = _money(lo) if lo == hi else f"{_money(lo)}–{_money(hi)}"
    rows.append(f"| **{sys.title()} total** | | | | **{tot}** |")
    return "\n".join(rows)


def emit_master() -> str:
    """The by-TYPE procurement BOM + the supplier-consolidation headline."""
    out = ["## Procurement BOM — by material type\n"]
    for t in TYPES:
        items = by_type().get(t, [])
        if not items:
            continue
        out.append(f"### {t}\n")
        out.append("| Item | Qty | Supplier | Systems | Est. cost |")
        out.append("|------|-----|----------|---------|-----------|")
        # aggregate the same key across systems
        agg: dict[str, dict] = {}
        for p in items:
            a = agg.setdefault(p.key, {"desc": p.desc, "qty": 0.0, "unit": p.unit,
                                       "sup": p.supplier, "sys": set(), "lo": 0.0, "hi": 0.0})
            a["qty"] += p.qty
            a["sys"].add(p.system)
            lo, hi = line(p); a["lo"] += lo; a["hi"] += hi
        sub_lo = sub_hi = 0.0
        for a in sorted(agg.values(), key=lambda x: -x["hi"]):
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
    "lightlock": "light-trap-selection.md", "panel": "hinged-panel-report.md",
    "shelf": "chemistry-prep-shelves.md", "walkway": "walkway-report.md",
    "optics": "pinhole-report.md", "ibc-frame": "ibc-stacking-report.md",
    "tray": "processing-tray-and-spray-bar.md", "spray": "processing-tray-and-spray-bar.md",
}


def _block_pat(key: str) -> "re.Pattern":
    return re.compile(r"(<!-- BEGIN parts:" + re.escape(key) + r" -->\n)(.*?)"
                      r"(\n<!-- END parts:" + re.escape(key) + r" -->)", re.DOTALL)


def _blocks() -> dict:
    """key -> (doc, emitter_fn). Only WIRED blocks are registered (added incrementally per phase)."""
    b = {"master": (_DOC_MASTER, emit_master)}
    # per-system §Parts-List blocks (Phase 2b) — only those already placed in their doc.
    for sys, doc in SYSTEM_DOC.items():
        b[sys] = (doc, lambda s=sys: emit_system(s))
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


def _water_line(prefix: str):
    return next(li for li in costing.WATER if li.label.startswith(prefix))


def reconcile_target(sys: str):
    """The (low, high) the registry system must sum to."""
    if sys in _WATER_SPLIT:
        li = _water_line(_WATER_SPLIT[sys])
        return (li.low, li.high)
    if sys == "water":                                          # WATER minus the three split-out lines
        rest = [li for li in costing.WATER
                if not any(li.label.startswith(p) for p in _WATER_SPLIT.values())]
        return (sum(li.low for li in rest), sum(li.high for li in rest))
    exp = costing.EXPECTED[reconcile_key(sys)]
    return (exp[0], exp[2]) if len(exp) == 3 else exp


def self_check() -> list[str]:
    """Every migrated system must sum to its costing reconcile target (±$10 absorbs rounding)."""
    errs = []
    for sys in systems():
        key = reconcile_key(sys)
        if sys not in _WATER_SPLIT and sys != "water" and key not in costing.EXPECTED:
            errs.append(f"{sys}: no costing.EXPECTED['{key}'] to reconcile against")
            continue
        tgt = reconcile_target(sys)
        got = system_total(sys)
        if abs(got[0] - tgt[0]) > 10 or abs(got[1] - tgt[1]) > 10:
            errs.append(f"{sys}: registry {got} != costing target {tgt}")
    return errs


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
