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
    Part("axial-fan-150", "150×150×50mm axial panel fan (12V DC)", "ducting-ventilation",
         "ventilation", 2, "ea", 25, 25, "Amazon", spec="GDSTIME/Wathai 15050-12V",
         dims="150×150×50", modeled_const="FAN_DIAM/FAN_BODY_D", audit_status="✅ FIXED"),
    Part("evap-cooler-mc18m", "Evaporative cooler — Hessaire MC18M (120V AC, 1,300 CFM)", "ducting-ventilation",
         "ventilation", 1, "ea", 130, 130, "Hessaire", "Amazon",
         url="https://hessaire.com/mobile-cooling/1300-cfm-mobile-cooler",
         dims="559×305×711", datasheet="Hessaire MC18M", modeled_const="EVAP_W/EVAP_D/EVAP_H",
         audit_status="✅ RESOLVED"),
    Part("cooler-inverter", "Cooler inverter — Victron Phoenix 12/375 GFCI + DC fuse/disconnect + GFCI outlet",
         "electrical-power", "ventilation", 1, "ea", 275, 275, "Victron", "Amazon"),
    Part("shade-cloth-80", "80% shade cloth, 20×10 ft", "fabric-textile",
         "ventilation", 1, "ea", 80, 80, "Amazon", "Farm supply"),
    Part("canopy-frame-emt", 'Canopy frame — 1.5" EMT conduit + fittings', "steel-structural",
         "ventilation", 1, "lot", 120, 120, "Home Depot"),
    Part("baffle-metal-fan", "Baffle-duct sheet metal (fans), 22 ga galvanized", "steel-structural",
         "ventilation", 1, "lot", 30, 30, "Local sheet metal", "Home Depot"),
    Part("baffle-metal-cooler", "Baffle-duct sheet metal (cooler, Ø200), 22 ga galvanized", "steel-structural",
         "ventilation", 1, "lot", 20, 20, "Local sheet metal", "Home Depot"),
    Part("flex-duct-200", "Ø200mm insulated flex duct, ~1.2m", "ducting-ventilation",
         "ventilation", 1, "ea", 22, 22, "Home Depot", "McMaster-Carr"),
    Part("duct-elbow-200", "Ø200mm 90° galvanized duct elbow", "ducting-ventilation",
         "ventilation", 1, "ea", 14, 14, "Home Depot"),
    Part("duct-collar-clamp", "Ø200mm duct collar + hose clamp", "ducting-ventilation",
         "ventilation", 1, "ea", 12, 12, "Home Depot"),
    Part("duct-cap-200", "Ø200mm removable weatherproof duct cap", "ducting-ventilation",
         "ventilation", 1, "ea", 8, 8, "Home Depot"),
    Part("deutsch-dt-2pin", "Deutsch DT 2-pin weatherproof connector set", "electrical-distribution",
         "ventilation", 2, "set", 4, 4, "Waytek Wire"),
    Part("coiled-cable-16awg", "16 AWG silicone coiled cable, 1m 2-cond (Fan B flex)", "electrical-distribution",
         "ventilation", 1, "ea", 15, 15, "Waytek Wire", "Amazon"),
    Part("cooler-power-cable", "Cooler external power cable, 1.5m 14 AWG + Deutsch plugs", "electrical-distribution",
         "ventilation", 1, "ea", 20, 20, "Waytek Wire", "Amazon"),
    Part("ratchet-strap-25", "Ratchet strap, 25mm (cooler stowage)", "fasteners-hardware",
         "ventilation", 2, "ea", 6, 6, "Home Depot", "Amazon"),
    Part("plywood-base-12", "Plywood base plate, 12mm 600×350 (cooler stowage)", "timber-ply",
         "ventilation", 1, "ea", 8, 8, "Home Depot", "Lumber yard"),

    # ═══ water (§5) — mirrors costing.WATER (sub-group granularity → exact $4,211–$6,297). The
    # bundled lines (frame/tray/spray/valves) carry the full sub-group cost under their dominant
    # type; finer per-item type-splitting is a later pass (the master's itemized subtotals have
    # drifted from costing, so splitting now would break exact reconciliation). ═══
    Part("water-storage", "Water storage — 4× IBC totes + 3× bulkhead fittings + fill tee",
         "water-equipment", "water", 1, "lot", 395, 720, "Container Exchanger", "Uline",
         note="bundle: totes + bulkheads + tee"),
    Part("ibc-stacking-frame", "IBC stacking frame — RHS restraint portal + feet + retaining bars + hangers + fab",
         "steel-structural", "water", 1, "lot", 955, 1455, "Metal Supermarkets", "local fab",
         note="bundle: steel sections + fabrication labor"),
    Part("water-pumps", "Pumps + accumulator — P-01/P-02/P-04 manifold + P-03",
         "water-equipment", "water", 1, "lot", 305, 355, "Amazon", "PexUniverse",
         note="bundle: 4 pumps + accumulator + brackets"),
    Part("filter-skid", "Filter skid — 3× Big Blue housings + cartridges",
         "water-equipment", "water", 1, "lot", 265, 370, "Amazon", "US Water Systems"),
    Part("water-valves-fittings", "Valves + fittings — S60×6 adapters, check valves CV1/CV3/CV4",
         "plumbing-fittings", "water", 1, "lot", 390, 630, "Amazon", "PexUniverse",
         note="bundle: ~15 valves/adapters/fittings"),
    Part("water-pipe-hdpe", "Pipe — HDPE, spray-bar feed", "plumbing-fittings",
         "water", 1, "lot", 100, 140, "Ferguson", "Home Depot"),
    Part("processing-tray", "Processing tray — 304 SS panels + fabrication, shim strips, sump pickup, liner, hardware",
         "stainless-sheet", "water", 1, "lot", 1300, 2015, "Online Metals", "local sheet metal",
         note="bundle: SS sheet + fabrication labor; split sheet↔fab in a later pass"),
    Part("spray-bar", "Spray bar — beam, LDPE pipe, 26 nozzles, manifold + 7 feed tubes, 4 wheels, ball joint, arm, hose",
         "aluminum", "water", 1, "lot", 235, 299, "Online Metals", "Amazon",
         note="bundle: extrusion + irrigation parts"),
    Part("water-wiring", "Water-system wiring (fuse block in Electrical Report)",
         "electrical-distribution", "water", 1, "lot", 35, 35, "Amazon"),
    Part("processing-consumables", "Processing consumables — 6-mil poly, pH meter, citric acid",
         "tools-safety", "water", 1, "lot", 231, 278, "Amazon"),

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
    Part("shelf-phenolic-ply", "Phenolic-faced plywood, 18mm (300×600)", "timber-ply",
         "shelf", 1, "ea", 60, 60, "Home Depot", "lumber yard"),
    Part("shelf-steel-shs", "25×25×3mm steel SHS — frame + spill lip (6m)", "steel-structural",
         "shelf", 1, "lot", 30, 30, "Online Metals", "Metal Supermarkets"),
    Part("shelf-piano-hinge", "Continuous (piano) hinge, 600mm", "fasteners-hardware",
         "shelf", 1, "ea", 20, 20, "McMaster-Carr"),
    Part("shelf-folding-stays", "Folding shelf stays/brackets (×2, fold-flat)", "fasteners-hardware",
         "shelf", 2, "ea", 12, 12, "Amazon", "McMaster-Carr"),
    Part("shelf-wall-cleat", "Wall mounting cleat + 2 stay anchors (6mm steel, slotted)", "steel-structural",
         "shelf", 1, "lot", 18, 18, "local fab"),
    Part("shelf-m8-bolts", "M8 wall bolts + washers/nuts (~12)", "fasteners-hardware",
         "shelf", 1, "lot", 12, 12, "McMaster-Carr"),
    Part("shelf-transport-latch", "Transport latch (over-center / barrel)", "fasteners-hardware",
         "shelf", 1, "ea", 8, 8, "Amazon"),
    Part("shelf-csk-screws", "M5×16 CSK screws (×8) — ply panel", "fasteners-hardware",
         "shelf", 8, "ea", 0.5, 0.5, "McMaster-Carr"),
    Part("shelf-gusset-plates", "Corner gusset plates, 3mm (×4)", "steel-structural",
         "shelf", 4, "ea", 1.25, 1.25, "steel offcut"),
    Part("shelf-paint", "Flat-black epoxy spray paint", "adhesives-finishes",
         "shelf", 1, "ea", 12, 12, "hardware store"),
    Part("shelf-hdpe-pipe", '½" HDPE pipe — TAP-01 trunk extension (~1.5m)', "plumbing-fittings",
         "shelf", 1, "lot", 10, 10, "irrigation supply"),

    # ═══ walkway (§9) — mirrors costing.WALKWAY → exact $2,000–$2,975 ═══
    Part("walkway-grp-grating", "Molded GRP (fiberglass) grating, 15mm (vinyl-ester, grit top, ~4.5 m²)",
         "plastics-sheet", "walkway", 1, "lot", 970, 1260, "McNichols", "Grating Pacific",
         note="incl. 1474×500mm near-walkway bump-out"),
    Part("walkway-std-brackets", "Standard wall brackets, 8mm steel plate (×14)", "steel-structural",
         "walkway", 14, "ea", 8, 12.5, "local fab", note="150mm vert × 300mm arm"),
    Part("walkway-wide-brackets", "Widened wall brackets, 10mm steel plate (×4)", "steel-structural",
         "walkway", 4, "ea", 18, 28, "local fab", note="EP/battery/slit zone; 200×500mm"),
    Part("walkway-reinf-plates", "Reinforcing plates, std 100×180×6mm (×14) + wide 120×220×6mm (×4)",
         "steel-structural", "walkway", 1, "lot", 47, 73, "local fab"),
    Part("walkway-m12-bolts", "M12×60mm hex bolts + nuts + washers (×58)", "fasteners-hardware",
         "walkway", 58, "set", 0.98, 1.5, "McMaster-Carr"),
    Part("walkway-transition-plates", "Transition bearing plates, 40×500×5mm flat bar (×2)", "steel-structural",
         "walkway", 2, "ea", 2.5, 5, "local fab"),
    Part("walkway-cantilever-frame", "Right walkway cantilever frame, 40×40×3mm SHS (8m)", "steel-structural",
         "walkway", 1, "lot", 28, 40, "Metal Supermarkets", note="rev12: closed rectangle + 2× 405mm arms"),
    Part("walkway-right-cleats", "Right walkway wall cleats, 8mm steel (×2)", "steel-structural",
         "walkway", 2, "ea", 10, 17.5, "local fab"),
    Part("walkway-corner-plates", "Combined corner plates, 10mm steel (×2)", "steel-structural",
         "walkway", 2, "ea", 25, 40, "local fab", note="shared with bottom film rail"),
    Part("walkway-throughbolts", "M12 through-bolts + nuts/washers (~24)", "fasteners-hardware",
         "walkway", 1, "lot", 30, 50, "McMaster-Carr"),
    Part("walkway-holddown-clips", "316 SS hold-down clips (FRP M/G-clip, ×20)", "fasteners-hardware",
         "walkway", 20, "ea", 1.25, 2, "McNichols", "McMaster-Carr"),
    Part("walkway-drum-exit-grp", "Drum-exit punch-out — extra GRP grating (~0.23 m²)", "plastics-sheet",
         "walkway", 1, "lot", 50, 65, "McNichols", note="600mm landing at light-lock exit"),
    Part("walkway-floor-legs", "Left floor-leg cantilever brackets (×5)", "steel-structural",
         "walkway", 5, "ea", 11, 19, "local fab", note="50×50×3 posts + 40×40×3 arms + foot plates"),
    Part("walkway-floor-anchors", "M10 wedge floor anchors (×20)", "fasteners-hardware",
         "walkway", 20, "ea", 1.25, 2.25, "McMaster-Carr"),
    Part("walkway-fabrication", "Fabrication (brackets, cantilever frame, install)", "fabrication-labor",
         "walkway", 1, "job", 454, 808, "local fab", note="matches walkway-report §10 all-in bracket figures"),
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


def emit_system(sys: str) -> str:
    """A report's §Parts-List (by-system view)."""
    rows = ["| Item | Spec | Qty | Supplier | Est. cost |", "|------|------|-----|----------|-----------|"]
    for p in sorted(by_system(sys), key=lambda x: x.type):
        lo, hi = line(p)
        cost = _money(lo) if round(lo) == round(hi) else f"{_money(lo)}–{_money(hi)}"
        sup = p.supplier + (f" / {p.supplier_alt}" if p.supplier_alt else "")
        rows.append(f"| {p.desc} | {p.spec or '—'} | {p.qty:g} {p.unit} | {sup} | {cost} |")
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


# ── Self-check (the migration guardrail) ─────────────────────────────────────
# reconciliation key: registry system → the costing.EXPECTED entry it must sum to.
# Defaults to the same name; only electrical maps to the differently-named 'power' rollup.
_RECONCILE = {"electrical": "power"}


def reconcile_key(sys: str) -> str:
    return _RECONCILE.get(sys, sys)


def self_check() -> list[str]:
    """Every migrated system must sum to its costing.EXPECTED entry (±$10 absorbs rounding)."""
    errs = []
    for sys in systems():
        key = reconcile_key(sys)
        if key not in costing.EXPECTED:
            errs.append(f"{sys}: no costing.EXPECTED['{key}'] to reconcile against")
            continue
        exp = costing.EXPECTED[key]
        exp_lh = (exp[0], exp[2]) if len(exp) == 3 else exp
        got = system_total(sys)
        if abs(got[0] - exp_lh[0]) > 10 or abs(got[1] - exp_lh[1]) > 10:
            errs.append(f"{sys}: registry {got} != costing.EXPECTED[{key}] {exp_lh}")
    return errs


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="reconcile each migrated system vs costing")
    ap.add_argument("--system", help="print a system's parts table")
    ap.add_argument("--master", action="store_true", help="print the by-type procurement BOM")
    args = ap.parse_args()
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
