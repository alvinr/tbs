"""costing.py — single source of truth for TBS-001 cost line items + derived totals.

WHY THIS EXISTS
---------------
Cost figures were hand-transcribed into project-cost-breakdown.md, master-shopping-list.md,
chemistry-shopping-list.md and funding-proposal.md, and the totals were summed by hand. So a
single change (e.g. the muslin feet-as-yards correction) drifted across docs, and the totals
fell out of sync with their line items. This module OWNS the line items; the markdown tables
are GENERATED from it, and `check()` asserts the values are internally consistent. Once the
docs are regenerated from here, the commit-time linter (see drift-reduction-plan.md, Phase 3)
re-checks the published tables against `costing.py` so the user never has to read for drift.

STATUS: Phase 1 vertical slice — the Printmaking / cyanotype block (the most-drifted section).
The same data->derive->emit->check pattern extends section-by-section to the whole build.

USAGE:  python3 src/generators/costing.py            # print the tables + run the self-check
        python3 src/generators/costing.py --check    # check only (exit 1 on mismatch)
"""
from __future__ import annotations

import sys
from dataclasses import dataclass

# ── Run basis ────────────────────────────────────────────────────────────────
PRINTS = 50            # edition size every per-run figure is based on

# ── Unit prices (USD) — each carries its source for traceability ─────────────
PRICE_AMFE_PER_KG  = 60.00     # Bostick & Sullivan — ammonium iron(III) oxalate (AmFe)
PRICE_FERRI_PER_KG = 24.29     # Bostick & Sullivan — potassium ferricyanide
DICHROMATE_RUN     = 25.00     # ammonium dichromate — trace contrast agent, per run
MUSLIN_ROLL_PRICE  = 100.00    # Fabric Direct — 60" x 150-yd unbleached muslin roll
MUSLIN_ROLLS       = 3         # ~445 yd / 150 -> 3 rolls (the feet-as-yards correction)
MUSLIN_YARDS       = 445       # ~1,334 linear ft = 445 yd (was mislabelled 1,340 yd)


# ── Ware New Cyanotype concentration tiers (per 50-print run) ────────────────
# AmFe : ferricyanide is held at Ware's 3:1 by weight; the tier sets the strength.
# The production tier is pinned by sensitizer-trials.md; Standard ½-Ware is the default.
@dataclass(frozen=True)
class Tier:
    key: str
    label: str
    amfe_kg: float
    ferri_kg: float


TIERS = [
    Tier("lean",     "Lean ⅓-Ware",     13.0,  4.3),
    Tier("standard", "Standard ½-Ware",  19.5,  6.5),
    Tier("rich",     "Rich full-Ware",   39.0, 13.0),
]
DEFAULT_TIER = "standard"


# ── Derived figures (computed once, never transcribed) ───────────────────────
def muslin_cost() -> float:
    return MUSLIN_ROLLS * MUSLIN_ROLL_PRICE          # -> 300


def tier_costs(t: Tier) -> dict:
    amfe = t.amfe_kg * PRICE_AMFE_PER_KG
    ferri = t.ferri_kg * PRICE_FERRI_PER_KG
    chem = amfe + ferri + DICHROMATE_RUN
    total = chem + muslin_cost()
    return {
        "amfe": amfe, "ferri": ferri, "dichromate": DICHROMATE_RUN,
        "chem_subtotal": chem, "muslin": muslin_cost(),
        "section_total": total, "per_print": total / PRINTS,
    }


def _r(x: float, base: int) -> int:
    """Round to the nearest `base` — one rounding rule, applied consistently."""
    return int(round(x / base) * base)


def dollars(x: float, base: int = 1) -> str:
    return f"${_r(x, base):,}"


def by_key(key: str) -> dict:
    return tier_costs(next(t for t in TIERS if t.key == key))


# ── Emitters (markdown the docs should contain — never hand-typed) ───────────
def emit_cost_breakdown_7_1() -> str:
    """The project-cost-breakdown.md §7.1 three-tier 'Chemistry and substrate' table."""
    c = {t.key: tier_costs(t) for t in TIERS}
    L, S, R = c["lean"], c["standard"], c["rich"]
    rows = [
        "| Item (50 prints) | Lean (⅓-Ware) | **Standard (½-Ware) — default** | Rich (full-Ware) | Source |",
        "|---|---|---|---|---|",
        f"| Ammonium iron(III) oxalate (AmFe) | {TIERS[0].amfe_kg:g} kg / ~{dollars(L['amfe'],10)} "
        f"| **{TIERS[1].amfe_kg:g} kg / ~{dollars(S['amfe'],10)}** | {TIERS[2].amfe_kg:g} kg / ~{dollars(R['amfe'],10)} "
        f"| Bostick & Sullivan (~${PRICE_AMFE_PER_KG:.0f}/kg) |",
        f"| Potassium ferricyanide (3:1 ratio) | {TIERS[0].ferri_kg:g} kg / ~{dollars(L['ferri'])} "
        f"| **{TIERS[1].ferri_kg:g} kg / ~{dollars(S['ferri'])}** | {TIERS[2].ferri_kg:g} kg / ~{dollars(R['ferri'])} "
        f"| Bostick & Sullivan (${PRICE_FERRI_PER_KG}/kg) |",
        f"| Ammonium dichromate (contrast, 0.1–0.4%) | ~{dollars(DICHROMATE_RUN)} | **~{dollars(DICHROMATE_RUN)}** "
        f"| ~{dollars(DICHROMATE_RUN)} | Photographers' Formulary |",
        f"| Unbleached cotton muslin, 60″ — {MUSLIN_ROLLS} × 150-yd rolls (~{MUSLIN_YARDS} yd) "
        f"| ~{dollars(muslin_cost())} | **~{dollars(muslin_cost())}** | ~{dollars(muslin_cost())} | Fabric Direct (~$100/roll) |",
        f"| **Cyanotype total — 50 prints** | **~{dollars(L['section_total'],10)}** "
        f"| **~{dollars(S['section_total'],10)}** | **~{dollars(R['section_total'],10)}** | |",
    ]
    return "\n".join(rows)


def printmaking_scenario() -> tuple[int, int, int]:
    """The cost-breakdown §7 scenario row + master §9 headline: Low=Lean / Mid=Std / High=Rich."""
    return (_r(by_key("lean")["section_total"], 10),
            _r(by_key("standard")["section_total"], 10),
            _r(by_key("rich")["section_total"], 10))


# ── Per-section line items (migrating in section by section; total is COMPUTED) ──
@dataclass(frozen=True)
class LineItem:
    label: str
    low: int
    mid: int
    high: int
    note: str = ""


def total(items: list[LineItem]) -> tuple[int, int, int]:
    return (sum(i.low for i in items), sum(i.mid for i in items), sum(i.high for i in items))


def point(label: str, cost: int, note: str = "") -> LineItem:
    """A single-value BOM item (low=mid=high) — for report BOMs that are point estimates."""
    return LineItem(label, cost, cost, cost, note)


# §6a Perimeter walkway — line items own the truth; the section total sums them (was hand-typed
# at $1,801/$2,186/$2,572, $25–35 low). Source: project-cost-breakdown.md §6a / generate_walkway_diagram.
WALKWAY = [
    LineItem("Molded GRP (fiberglass) grating, 15mm (vinyl-ester, grit top)", 970, 1115, 1260, "~4.5 m² (incl. 1474×500mm near-walkway bump-out); McNichols / Grating Pacific"),
    LineItem("Standard wall brackets, 8mm steel plate (×14)", 112, 143, 175, "Near/far walls; 150mm vert × 300mm arm"),
    LineItem("Widened wall brackets, 10mm steel plate (×4)", 72, 90, 112, "EP/battery/slit zone; 200mm vert × 500mm arm"),
    LineItem("Reinforcing plates, std 100×180×6mm (×14) + wide 120×220×6mm (×4)", 47, 60, 73, "Welded to wall exterior behind each bracket"),
    LineItem("M12×60mm hex bolts + nuts + washers (×58)", 57, 72, 87, "3 per std bracket (42) + 4 per widened (16)"),
    LineItem("Transition bearing plates, 40×500×5mm flat bar (×2)", 5, 8, 10, "Welded to arm top at width transitions"),
    LineItem("Right walkway cantilever frame, 40×40×3mm SHS (8m)", 28, 34, 40, "rev12: closed rectangle + 2× 405mm center arms"),
    LineItem("Right walkway wall cleats, 8mm steel (×2)", 20, 28, 35, "Left corners — through-bolted to the wall"),
    LineItem("Combined corner plates, 10mm steel (×2)", 50, 65, 80, "Right corners — shared with the bottom film rail"),
    LineItem("M12 through-bolts + nuts/washers (~24)", 30, 40, 50, "Wall cleats + combined plates + 2 center-arm U-clamps"),
    LineItem("316 SS hold-down clips (FRP M/G-clip, ×20)", 25, 32, 40, "Near/far/right walkway GRP grating retention"),
    LineItem("Drum-exit punch-out — extra GRP grating (~0.23 m²)", 50, 57, 65, "600mm-deep landing at the light-lock exit"),
    LineItem("Left floor-leg cantilever brackets (×5)", 55, 75, 95, "50×50×3 SHS posts + 40×40×3 arms + foot plates"),
    LineItem("M10 wedge floor anchors (×20)", 25, 35, 45, "4 per foot plate; sealed floor penetrations"),
    LineItem("Fabrication (brackets, cantilever frame, install)", 280, 360, 440, "14 std + 4 widened brackets, right cantilever frame, 5 left floor-leg brackets, install"),
]


# §5 Processing water system — the §5 sub-table is Low/High only; the scenario column needs Mid,
# computed here as the per-item midpoint. Line items own the truth (the hand-typed sub-table total
# $4,128/$6,201 and scenario $4,143/$5,180/$6,216 both drifted from the items, which sum to
# $4,063/$6,104). Source: project-cost-breakdown.md §5.
WATER = [
    LineItem("Water storage (4× IBC totes, 3× bulkhead fittings, X1 fill tee)", 395, 558, 720),
    LineItem("IBC stacking frame (RHS restraint portal + feet + retaining bars + hangers + fab)", 955, 1205, 1455),
    LineItem("Pumps and accumulator (P-01/P-02/P-04 manifold + P-03)", 305, 330, 355),
    LineItem("Filter skid (3× Big Blue housings + cartridges)", 265, 318, 370),
    LineItem("Valves and fittings (S60×6 adapters, check valves CV1/CV3/CV4)", 390, 510, 630),
    LineItem("Pipe (HDPE, spray bar)", 100, 120, 140),
    LineItem("Processing tray (304 SS, fabricated, 2 panels)", 1177, 1517, 1857),
    LineItem("Spray bar assembly (beam, LDPE pipe, 26 nozzles, manifold, 4 wheels, ball joint, arm, hose)", 210, 237, 264),
    LineItem("Electrical (wiring only — fuse block in Electrical Report)", 35, 35, 35),
    LineItem("Processing consumables (6-mil poly, pH meter, citric acid)", 231, 255, 278),
]

# §1 Container — clean 2-item table; the scenario Mid was $3,150 but the items give $3,300.
CONTAINER = [
    LineItem("20 ft container — CW grade", 2000, 2750, 3500, "containermgt.com"),
    LineItem("Delivery — short haul (<50 miles)", 300, 550, 800, "Commercial tilt-bed hire"),
]

# §6 Housed revolving-door light lock (plastic-skin) — detail already = scenario.
LIGHTLOCK = [
    LineItem("5mm UV-HDPE sheet — Ø900 housing shell (~7 m²)", 180, 230, 280, "TAP Plastics / Online Metals"),
    LineItem("4mm PP sheet — Ø864 drum shell + caps + steel stub shafts ×2", 180, 215, 270, "TAP / Curbell + steel service center"),
    LineItem("SKF 6215-2RS1 sealed bearing (×2)", 90, 110, 130, "Bearing World / Applied Industrial"),
    LineItem("Seals — neoprene wiper + silicone + brush (drum↔housing)", 90, 110, 130, "McMaster-Carr"),
    LineItem("Hardware — SS grab rail + M10 stainless bolts (×14)", 60, 75, 90, "McMaster / Fastenal"),
    LineItem("Nylon isolation washers + stainless fasteners (no galvanic couple)", 25, 32, 40, "McMaster-Carr"),
    LineItem("Matte-black interior finish", 40, 55, 70, "Rattle-can / local shop"),
    LineItem("Plastic fabrication — roll + weld 2 cylinders, cap/shaft/bearing fit (16–22 hrs)", 800, 975, 1150, "Local plastic fab shop"),
]

# §6b Panel swing pivot — detail already = scenario.
SWINGPIVOT = [
    LineItem("Ø89×8 CHS pivot post + machined hub / thrust collar", 180, 220, 260, "Metal Supermarkets / local fab"),
    LineItem("Thrust + journal bearings (12″ turntable thrust + 2× 89mm bronze sleeve)", 180, 210, 250, "VXB + McMaster SAE 841"),
    LineItem("Drum support cage, 40×40×3mm SHS", 80, 90, 110, "Local fab"),
    LineItem("Top + bottom wall stays + 4-bolt anchor plates", 120, 140, 160, "Turnbuckles + rods + plates"),
    LineItem("Drop-in rail saddles + tapered dowels (×4, removable left film rails)", 90, 110, 130, "Local fab / McMaster"),
]


# §2 Interior conversion — the detail "Section total" category breakdown is correct ($950/$1,138/
# $1,350); the SCENARIO row ($970/$1,140/$1,310) was the drifted one.
INTERIOR = [
    LineItem("Light-sealing materials", 150, 178, 210),
    LineItem("Interior paint", 100, 130, 160),
    LineItem("Image-plane flat backing (Dibond ACM)", 490, 550, 620),
    LineItem("Ventilation (inline fans + light-trap baffles)", 80, 100, 130),
    LineItem("Door & access upgrades", 50, 70, 100),
    LineItem("Misc. conversion hardware", 80, 110, 130),
]

# §3 Optics — pinhole plate (§3.1; the optional lens §3.2 is NOT in the base total). Detail
# ($95/$165/$240) is correct; the scenario row ($80/$150/$280) was drifted.
OPTICS = [
    LineItem("Custom laser-drilled pinhole, SS-302/304 shim, 3×3", 50, 100, 150, "Lenox Laser"),
    LineItem("Steel backing plate 6×6×⅛, welded frame", 20, 30, 40),
    LineItem("Shutter plate (⅛ steel, 10×8) + slide channel", 25, 35, 50),
]


# §5b Ventilation & cooling — single-value BOM (point estimates). Source: ventilation-report.md.
# Items sum to $824; the report total was STALE at $769 (the last 4 items were added without
# updating it). The cost-breakdown §5b scenario ($770/$830/$920) is a budget band around this.
VENTILATION = [
    point("150×150×50mm axial fans ×2 (12V DC)", 50),
    point("Evaporative cooler (Hessaire MC18M)", 130),
    point("Cooler inverter (Victron Phoenix 12/375 GFCI + DC fuse/disconnect + GFCI outlet)", 275),
    point("Shade canopy — 80% shade cloth (20×10 ft)", 80),
    point('Canopy frame (1.5" EMT conduit + fittings)', 120),
    point("Baffle duct sheet metal (fans)", 30),
    point("Baffle duct sheet metal (cooler, Ø200)", 20),
    point("200mm insulated flex duct", 22),
    point("200mm 90° duct elbow", 14),
    point("Duct collar + hose clamp", 12),
    point("Weatherproof duct cap", 8),
    point("Deutsch DT 2-pin connectors (Fan B flex ×2)", 8),
    point("16 AWG silicone coiled cable (Fan B flex)", 15),
    point("Cooler external power cable", 20),
    point("Ratchet straps ×2 (cooler stowage)", 12),
    point("Plywood base plate (cooler stowage)", 8),
]

# §5a Power & electrical — owned at the AUTHORITATIVE subtotal level. The electrical-report §8 BOM
# states the electrical system total $2,265 (= master-shopping-list §6 Solar & battery $1,295 +
# Distribution & wiring $970; = the scenario §5a Mid). The full 43-row combined BOM overlaps the
# §5b ventilation items, so we own the two authoritative subtotals rather than re-entering it.
POWER = [
    point("Solar & battery (3× 200W panels, MPPT 100/50, 1× 100Ah LiFePO4, shore charger, mounts, PV cabling, panel)", 1295),
    point("Distribution & wiring (fuse block, disconnect, contactor, E-stop, protection, conduit, LED, pump switches)", 970),
]


def emit_section_table(items: list[LineItem], total_label: str) -> str:
    """Generate a Low/Mid/High line-item table with a COMPUTED total row."""
    rows = ["| Item | Low | Mid | High | Notes |", "|------|-----|-----|------|-------|"]
    for i in items:
        rows.append(f"| {i.label} | ${i.low:,} | ${i.mid:,} | ${i.high:,} | {i.note} |")
    lo, mid, hi = total(items)
    rows.append(f"| **{total_label}** | **${lo:,}** | **${mid:,}** | **${hi:,}** | |")
    return "\n".join(rows)


# ── Whole-build scenario table (project-cost-breakdown.md "Executive Cost Summary") ──
# Each section's (Low, Mid, High). §7 Printmaking is COMPUTED from the tiers above; the others
# are section totals owned here as data (sub-line-item ownership migrates in section by section).
# The grand TOTAL is *summed*, so it can never drift from its rows — the re-sum is automatic.
@dataclass(frozen=True)
class Section:
    sid: str
    label: str
    low: int
    mid: int
    high: int


def _printmaking_section() -> Section:
    lo, mid, hi = printmaking_scenario()
    return Section("7", "Printmaking — 50 prints (cyanotype)", lo, mid, hi)


SECTIONS = [
    Section("1",  "Container purchase & delivery",              *total(CONTAINER)),  # COMPUTED
    Section("2",  "Interior conversion",                         *total(INTERIOR)),  # COMPUTED
    Section("3",  "Optics — pinhole plate",                       *total(OPTICS)),    # COMPUTED
    Section("4",  "Film plane mechanism (4-corner Option A)",   3100, 3650, 4200),
    Section("5",  "Processing water system",                    *total(WATER)),  # COMPUTED from line items
    Section("5a", "Power & electrical system",                  2025, 2265, 2575),
    Section("5b", "Ventilation & cooling system",                total(VENTILATION)[0],
            total(VENTILATION)[0] + 60, total(VENTILATION)[0] + 150),  # Low = BOM $824; +$60/+$150 band
    Section("6",  "Housed revolving-door light lock",           *total(LIGHTLOCK)),  # COMPUTED
    Section("6a", "Perimeter walkway",                          *total(WALKWAY)),  # COMPUTED from line items
    Section("6b", "Panel swing pivot",                           *total(SWINGPIVOT)),  # COMPUTED
    _printmaking_section(),
    Section("8",  "Transportation (per deployment)",             300,  750, 2000),
    Section("9",  "Licences & permits",                          220,  790, 1620),
]


def grand_total() -> tuple[int, int, int]:
    return (sum(s.low for s in SECTIONS),
            sum(s.mid for s in SECTIONS),
            sum(s.high for s in SECTIONS))


def emit_scenario_table() -> str:
    rows = ["| Category | Low | Mid | High |", "|----------|-----|-----|------|"]
    for s in SECTIONS:
        rows.append(f"| **{s.sid}. {s.label}** | ${s.low:,} | ${s.mid:,} | ${s.high:,} |")
    lo, mid, hi = grand_total()
    rows.append(f"| **TOTAL (excl. own transport, CDL, lens)** | **${lo:,}** | **${mid:,}** | **${hi:,}** |")
    return "\n".join(rows)


# ── Self-check (regression guard — the canonical numbers, asserted) ──────────
EXPECTED = {                       # the figures the docs are reconciled to (this session)
    "muslin": 300,
    "lean":     {"chem": 909,  "total": 1210, "per_print": 24},  # 909 not 910: consistent ferri rounding ($104, not the doc's hand-rounded $105)
    "standard": {"chem": 1353, "total": 1650, "per_print": 33},
    "rich":     {"chem": 2681, "total": 2980, "per_print": 60},
    "grand_total": (19028, 24463, 32020),  # + §5b band nudged so Low = its BOM ($824), whole band +$54
    "walkway": (1826, 2214, 2607),
    "water": (4063, 5085, 6104),
    "container": (2300, 3300, 4300),
    "lightlock": (1465, 1802, 2160),
    "swingpivot": (650, 770, 910),
    "interior": (950, 1138, 1350),
    "optics": (95, 165, 240),
    "ventilation": (824, 824, 824),   # §5b BOM (point estimates); report total was stale at $769
    "power": (2265, 2265, 2265),       # §5a authoritative subtotal ($1,295 + $970)
}


def check() -> list[str]:
    errs = []
    if _r(muslin_cost(), 1) != EXPECTED["muslin"]:
        errs.append(f"muslin {_r(muslin_cost(),1)} != {EXPECTED['muslin']}")
    for t in TIERS:
        c, e = tier_costs(t), EXPECTED[t.key]
        if _r(c["chem_subtotal"], 1) != e["chem"]:
            errs.append(f"{t.key} chem {_r(c['chem_subtotal'],1)} != {e['chem']}")
        if _r(c["section_total"], 10) != e["total"]:
            errs.append(f"{t.key} total {_r(c['section_total'],10)} != {e['total']}")
        if _r(c["per_print"], 1) != e["per_print"]:
            errs.append(f"{t.key} per-print {_r(c['per_print'],1)} != {e['per_print']}")
    if total(WALKWAY) != EXPECTED["walkway"]:
        errs.append(f"walkway {total(WALKWAY)} != {EXPECTED['walkway']}")
    if total(WATER) != EXPECTED["water"]:
        errs.append(f"water {total(WATER)} != {EXPECTED['water']}")
    for key, items in (("container", CONTAINER), ("lightlock", LIGHTLOCK), ("swingpivot", SWINGPIVOT),
                       ("interior", INTERIOR), ("optics", OPTICS), ("ventilation", VENTILATION),
                       ("power", POWER)):
        if total(items) != EXPECTED[key]:
            errs.append(f"{key} {total(items)} != {EXPECTED[key]}")
    if grand_total() != EXPECTED["grand_total"]:
        errs.append(f"grand total {grand_total()} != {EXPECTED['grand_total']}")
    return errs


def main(argv: list[str]) -> int:
    errs = check()
    if "--check" in argv:
        if errs:
            print("✗ costing self-check FAILED:")
            for e in errs:
                print("   -", e)
            return 1
        print("✓ costing self-check passed")
        return 0
    print("# Printmaking — cyanotype §7.1 (generated by costing.py)\n")
    print(emit_cost_breakdown_7_1())
    print("\n# §6a Perimeter walkway — line items (generated by costing.py)\n")
    print(emit_section_table(WALKWAY, "Perimeter walkway total"))
    print("\n# Executive Cost Summary — whole build (generated by costing.py)\n")
    print(emit_scenario_table())
    print("\nSelf-check:", "✓ passed" if not errs else "✗ FAILED -> " + "; ".join(errs))
    return 1 if errs else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
