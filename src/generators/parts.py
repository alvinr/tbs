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
def self_check() -> list[str]:
    """Every system present in the registry must sum to costing.EXPECTED[system]."""
    errs = []
    for sys in systems():
        if sys not in costing.EXPECTED:
            continue
        exp = costing.EXPECTED[sys]
        got = system_total(sys)
        exp_lh = (exp[0], exp[2]) if len(exp) == 3 else exp
        if got != exp_lh:
            errs.append(f"{sys}: registry {got} != costing.EXPECTED {exp_lh}")
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
