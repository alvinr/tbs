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
_RECONCILE = {"ventilation": "ventilation", "water": "water", "electrical": "power"}


def self_check() -> list[str]:
    """Every migrated system must sum to its costing.EXPECTED entry (±$10 absorbs rounding)."""
    errs = []
    for sys in systems():
        key = _RECONCILE.get(sys)
        if not key or key not in costing.EXPECTED:
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
