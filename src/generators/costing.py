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

import os
import re
import sys
from dataclasses import dataclass

# ── Run basis ────────────────────────────────────────────────────────────────
PRINTS = 50            # edition size every per-run figure is based on
PER_PRINT_CONSUMABLES = 3   # §7.3 all-in basis: water/citric/pH per print BEYOND §7.1 chem+substrate

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
    point("Fixed RHS door frame (50×50×3 RHS seal landing + EPDM seals)", 462, "the hinged light-trap panel's seal-landing frame — master §7a; was omitted from the cost-breakdown"),
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


# §4 Film plane mechanism (4-corner Option A, manual handwheel actuation). Line items own the truth;
# the section total sums them. The only documented source of Low/High spread is the cam-lever muslin
# clamps ($3/$5.50/$8 ea × 92 = $276/$506/$736) plus a modest band on the est. wall-seat saddle plate;
# everything else is single-source-specced (point()). Folding this BOM in raised the §4 floor ~$480:
# the hand-set summary ($3,100/$3,650/$4,200) sat BELOW the section's own bill of materials.
# Source: project-cost-breakdown.md §4.1–4.3 / film-plane-mechanism-report.md.
FILM = [
    # 4.1 Structural & rails (HGR20 carriage + Option-A floating cross-slides)
    point("Linear guide rails HGR20 2,200mm (×4) + carriages HGH20CA (×8)", 324, "2 carriages per rail"),
    point("Acme leadscrews ¾\"-6 8 ft (×4) + bronze nuts (×4)", 428, "manual handwheel drive"),
    point("Handwheels 8\" (×4) + locking collars SS316 (×4)", 188),
    point("Corner bracket L-plates, ¼\" alum 6×8 (×4)", 80),
    point("Option-A cross-slides — HGR15 rails (×8) + HGH15CA (×8) + intermediate plates (×4)", 356, "floating-corner X–Z stage"),
    point("Rod-end spherical bearings GIR25-DO (×8) + pivot pins SS316 (×8)", 240),
    # 4.2 Film plane frame & backing
    point("Aluminum angle 2×2×3/16 8 ft (×10)", 220),
    point("Dibond ACM 4mm 4×8 sheets (×6) — single rigid plane", 510, "Option A: no folding hinge"),
    point("Light-seal set — EPDM tape (×3) + Rosco Duvetyne + 6-mil poly + Gorilla tape (×6)", 316),
    LineItem("Cam-lever spring clamps, muslin (×92)", 276, 506, 736, "$3/$5.50/$8 ea — the section's main Low/High driver"),
    point("Clamp mounting — M5×16 SS bolts/Nylocks (×184+184) + neoprene jaw strip", 70),
    # 4.3 Wall-seat saddles (rev 11, ICP-11–14) — estimates, confirm at procurement
    LineItem("Wall-seat saddles ×8 — 8mm steel plate, cut + welded (ICP-11)", 380, 425, 470, "~28 kg total; back-plate + seat + gusset"),
    point("Saddle fasteners — M12 through-bolts (×36) + M8 thumbscrews (×12) + M8 rail bolts (×12)", 150, "ICP-12/13/14"),
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


FRONT_BOARD_MID = 1470   # tilt-swing front board — source: tilt-swing-board-report.md (not a SECTIONS row)


def _sec(sid: str) -> Section:
    return next(s for s in SECTIONS if s.sid == sid)


def emit_funding_level1() -> str:
    """funding-proposal.md Level 1 — Core Build: each section's Mid + the (separate) front board,
    plus 10% contingency. A 2nd VIEW of the same costing source (so it can't drift)."""
    rows = [
        ("20ft container (Cargo Worthy grade) + delivery", _sec("1").mid),
        ("Interior conversion (light-seal, paint, image-plane backing)", _sec("2").mid),
        ("Pinhole plate (precision laser-drilled, SS-302, interchangeable frame)", _sec("3").mid),
        ("Film plane mechanism (4-corner Option A, manual actuation)", _sec("4").mid),
        ("Tilt-swing front board mechanism", FRONT_BOARD_MID),
        ("Housed revolving-door light trap (plastic-skin Ø900 housing + C-shell drum, bearings, seals, fabrication)", _sec("6").mid),
        ("Processing water system (tray, spray bar, 3-stage filtration, IBC stacking frame)", _sec("5").mid),
        ("Power & electrical (600W solar · LiFePO4 · MPPT · distribution · protection · lighting)", _sec("5a").mid),
        ("Ventilation & cooling (2 fans · evap cooler + 12V→120V inverter · light-safe ducting)", _sec("5b").mid),
        ("Perimeter walkway (4 sections + drum-exit punch-out)", _sec("6a").mid),
        ("Panel swing pivot (Ø89 post + bearings + cage + wall stays)", _sec("6b").mid),
        ("Cyanotype chemistry + muslin substrate (50-print run, Standard tier)", _sec("7").mid),
    ]
    sub = sum(v for _, v in rows)
    cont = _r(sub * 0.10, 10)
    out = ["| Item | Cost |", "|------|------|"]
    out += [f"| {label} | ${v:,} |" for label, v in rows]
    out.append(f"| Contingency (10%) | ~${cont:,} |")
    out.append(f"| **Level 1 total** | **~${sub + cont:,}** |")
    return "\n".join(out)


def emit_master_summary() -> str:
    """master-shopping-list.md summary — 3rd VIEW (Low/High, the master's groupings) from costing.
    Excludes transport/permits (master = base build + 50-print run); adds tools + safety (§10/§11)."""
    rows = [
        ("1. Container & delivery", _sec("1")),
        ("2. Interior conversion (light-seal, paint, backing)", _sec("2")),
        ("3. Pinhole optics plate", _sec("3")),
        ("4. Film plane mechanism (4-corner Option A, manual, incl. wall-seat saddles + cross-slides)", _sec("4")),
        ("5. Print washing — water system (incl. IBC stacking frame)", _sec("5")),
        ("6. Electrical — power, circuits, wiring", _sec("5a")),
        ("7. Housed revolving-door light lock (plastic-skin custom fabrication)", _sec("6")),
        ("7a. Panel swing pivot (Ø89 pivot post + bearings + cage + wall stays + rail saddles)", _sec("6b")),
        ("7b. Perimeter walkway (4 sections + drum-exit punch-out)", _sec("6a")),
        ("8. Cooling & ventilation", _sec("5b")),
        ("9. Printmaking chemistry — cyanotype, 50 prints (Low = Lean, High = Rich tier)", _sec("7")),
        ("10. Printmaking tools & consumables", TOOLS),
        ("11. Safety & PPE", SAFETY),
    ]
    out = ["| Area | Low | High |", "|------|-----|------|"]
    lo = hi = 0
    for label, s in rows:
        out.append(f"| {label} | ${s.low:,} | ${s.high:,} |")
        lo, hi = lo + s.low, hi + s.high
    out.append(f"| **TOTAL (base build + 50-print run)** | **~${lo:,}** | **~${hi:,}** |")
    return "\n".join(out)


def master_total() -> tuple:
    ids = ("1", "2", "3", "4", "5", "5a", "6", "6b", "6a", "5b", "7")
    lo = sum(_sec(i).low for i in ids) + TOOLS.low + SAFETY.low
    hi = sum(_sec(i).high for i in ids) + TOOLS.high + SAFETY.high
    return (lo, hi)


def funding_level1_total() -> int:
    sub = (_sec("1").mid + _sec("2").mid + _sec("3").mid + _sec("4").mid + FRONT_BOARD_MID
           + _sec("6").mid + _sec("5").mid + _sec("5a").mid + _sec("5b").mid + _sec("6a").mid
           + _sec("6b").mid + _sec("7").mid)
    return sub + _r(sub * 0.10, 10)


# Funding-proposal Level 2/3 ranges (deployment + documentation — funding-doc-specific, not in the
# 13 build sections). The combined first-year band is computed from them + Level 1.
FUNDING_L2 = (1350, 2800)   # transport + permits + water resupply (one deployment)
FUNDING_L3 = (2000, 4000)   # video + photography + publication


def funding_combined() -> tuple[int, int]:
    l1 = funding_level1_total()
    return (l1 + FUNDING_L2[0] + FUNDING_L3[0], l1 + FUNDING_L2[1] + FUNDING_L3[1])


# ── §11 Complete Budget Scenarios — the build rows are pulled from the costing sections (Low for A,
# Mid for B) so they can't drift; the grade/transport/permit/lens choices that AREN'T a section
# midpoint are explicit editorial picks. Totals are computed. (Generating this corrected a couple of
# hand-maintained drifts: scenario-B light trap 1,800 -> the §6 Mid 1,802, and the derived C figures.)
SCEN_A = {"container": 1800, "transport": 400, "permits": 50}          # WWT grade, local deployment
SCEN_B = {"container": 3150, "lens": 800, "transport": 900, "permits": 300}
SCEN_C = {"cdl": 4500, "trailer": 35000, "truck_lo": 50000, "truck_hi": 80000}


def _scenario_a_rows() -> list:
    return [
        ("Container (WWT) + delivery", SCEN_A["container"]),
        ("Interior conversion (minimal)", _sec("2").low),
        ("Pinhole plate", _sec("3").low),
        ("Film plane mechanism (manual Option A, incl. wall-seat saddles + cross-slides)", _sec("4").low),
        ("Water system (incl. processing tray, spray bar, IBC stacking frame)", _sec("5").low),
        ("Power & electrical system (solar · 1× LiFePO4 · distribution · lighting · protection · pump switches)", _sec("5a").low),
        ("Ventilation & cooling system (2 fans · evap cooler + inverter · light-safe baffle-duct fab · shade canopy)", _sec("5b").low),
        ("Revolving drum light trap (plastic-skin custom fabrication)", _sec("6").low),
        ("Perimeter walkway (4 sections, removable, GRP grating)", _sec("6a").low),
        ("Panel swing pivot (Ø89 pivot + bearings + cage + wall stays + saddles)", _sec("6b").low),
        ("Cyanotype chemistry + substrate (50 prints)", _sec("7").low),
        ("Transport per deployment (local)", SCEN_A["transport"]),
        ("Permits (minimal)", SCEN_A["permits"]),
    ]


def _scenario_b_rows() -> list:
    return [
        ("Container (CW) + delivery", SCEN_B["container"]),
        ("Interior conversion (full)", _sec("2").mid),
        ("Pinhole plate", _sec("3").mid),
        ("Film plane mechanism (manual Option A + wall-seat saddles + cross-slides)", _sec("4").mid),
        ("Water system (incl. processing tray, spray bar, IBC stacking frame)", _sec("5").mid),
        ("Power & electrical system (solar · 1× LiFePO4 · distribution · lighting · protection · pump switches)", _sec("5a").mid),
        ("Ventilation & cooling system (2 fans · evap cooler + inverter · light-safe baffle-duct fab · shade canopy)", _sec("5b").mid),
        ("Revolving drum light trap (plastic-skin custom fabrication)", _sec("6").mid),
        ("Perimeter walkway (4 sections, removable, GRP grating)", _sec("6a").mid),
        ("Panel swing pivot (Ø89 pivot + bearings + cage + wall stays + saddles)", _sec("6b").mid),
        ("Cyanotype chemistry + substrate (50 prints)", _sec("7").mid),
        ("Rodenstock Apo-Ronar 1,200mm lens", SCEN_B["lens"]),
        ("Transport per deployment (50–100 miles)", SCEN_B["transport"]),
        ("Permits (typical public land)", SCEN_B["permits"]),
    ]


def _scen_table(rows: list, total_label: str) -> str:
    out = ["| Item | Cost |", "|------|------|"]
    for lbl, v in rows:
        out.append(f"| {lbl} | ${v:,} |")
    out.append(f"| **{total_label}** | **~${sum(v for _, v in rows):,}** |")
    return "\n".join(out)


def emit_scenario_a() -> str:
    return _scen_table(_scenario_a_rows(), "Scenario A total")


def emit_scenario_b() -> str:
    return _scen_table(_scenario_b_rows(), "Scenario B total (excl. CDL)")


def emit_scenario_c() -> str:
    b_less = sum(v for _, v in _scenario_b_rows()) - SCEN_B["transport"]   # B build, owned transport
    base = b_less + SCEN_C["cdl"] + SCEN_C["trailer"]
    rows = [
        (f"Scenario B build (less the ${SCEN_B['transport']:,} commercial transport, replaced here by owned transport)", f"${b_less:,}"),
        ("CDL Class A training + medical + DMV", f"${SCEN_C['cdl']:,}"),
        ("QuickLoadz self-loading trailer", f"${SCEN_C['trailer']:,}"),
        ("Ford F-350+ pickup (if needed)", f"${SCEN_C['truck_lo']:,}–${SCEN_C['truck_hi']:,} (new)"),
    ]
    out = ["| Item | Cost |", "|------|------|"]
    for lbl, v in rows:
        out.append(f"| {lbl} | {v} |")
    out.append(f"| **Scenario C total** | **~${base + SCEN_C['truck_lo']:,}–${base + SCEN_C['truck_hi']:,}** |")
    return "\n".join(out)


# ── cost-analysis-report.md — §2 capital/recurring buckets + §3 system ranking, both DERIVED from the
# section Mids (this report summarises the Mid column), so they can't drift. Generating §3 + the
# water-% inline also retired the stale '28%' the prose carried from the old water/capital figures.
_CA = "cost-analysis-report.md"
_OM = "operating-manual.md"
_EL = "equipment-layout-report.md"
_IBC = "ibc-stacking-report.md"


def capital_mid() -> int:
    """One-time build capital = grand Mid − consumable (§7) − recurring transport (§8) − permits (§9)."""
    return grand_total()[1] - _sec("7").mid - _sec("8").mid - _sec("9").mid


def _pct(mid: int, cap: int) -> str:
    p = mid / cap * 100
    return f"{round(p)}%" if p >= 1 else f"{p:.1f}%"


def emit_ca_buckets() -> str:
    return "\n".join([
        "| Bucket | Mid | What it is |",
        "|---|--:|---|",
        f"| **Capital build** (one-time hardware) | **${capital_mid():,}** | The systems you build once — this is where build-savings live |",
        f"| Consumable (per 50-print batch) | ${_sec('7').mid:,} | Cyanotype chemistry + substrate (Standard ½-Ware) — recurs every batch |",
        f"| Recurring (per deployment) | ${_sec('8').mid:,} | Commercial-hire transport |",
        f"| Soft / regulatory | ${_sec('9').mid:,} | Licenses & permits |",
    ])


# (system label, section id, note) — the §3 ranking, sorted by Mid descending in the emitter.
_CA_SYSTEMS = [
    ("Processing water system", "5",  "Tray (304 SS) + IBC frame dominate"),
    ("Film-plane mechanism",    "4",  "Carriages, Option-A cross-slides, cam-lever clamps, wall-seat saddles"),
    ("Container + delivery",    "1",  "Grade-dependent (CW vs WWT)"),
    ("Power & electrical",      "5a", "Battery + solar + distribution + protection"),
    ("Perimeter walkway",       "6a", "GRP grating + steel cantilevers"),
    ("Light lock",              "6",  "Plastic-skin custom fabrication"),
    ("Swing pivot",             "6b", "Pivot post + bearings + cage + fixed RHS door frame"),
    ("Interior conversion",     "2",  "Insulation, sealing, safelight"),
    ("Ventilation & cooling",   "5b", "Fans + cooler + inverter + baffle-duct fab + canopy"),
    ("Optics — pinhole",        "3",  "Trivial (it is a pinhole)"),
]


def emit_ca_ranking() -> str:
    cap = capital_mid()
    rows = sorted(((lbl, _sec(sid).mid, note) for lbl, sid, note in _CA_SYSTEMS), key=lambda r: -r[1])
    out = ["| System | Mid | % of capital | Notes |", "|---|--:|--:|---|"]
    for lbl, mid, note in rows:
        out.append(f"| **{lbl}** | ${mid:,} | {_pct(mid, cap)} | {note} |")
    return "\n".join(out)


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
    return Section("7", "Printmaking — 50 prints (cyanotype; Low=Lean, Mid=Standard, High=Rich tier)", lo, mid, hi)


# Labels match the cost-breakdown "Executive Cost Summary" EXACTLY, so emit_scenario_table()
# regenerates that table verbatim — it is INJECTED into the <!-- costing:scenario --> block, and
# the linter gate fails if the doc block ever diverges. (Computed totals where a line-item list
# owns the section; direct values for the estimate/BOM sections 4/5a/8/9.)
SECTIONS = [
    Section("1",  "Container purchase & delivery", *total(CONTAINER)),
    Section("2",  "Interior conversion", *total(INTERIOR)),
    Section("3",  "Optics — pinhole plate", *total(OPTICS)),
    Section("4",  "Film plane mechanism (4-corner Option A, incl. wall-seat saddles + cross-slides)", *total(FILM)),
    Section("5",  "Processing water system (incl. tray, spray bar, IBC stacking frame)", *total(WATER)),
    Section("5a", "Power & electrical system (solar · 1× LiFePO4 · MPPT · distribution · lighting · protection · pump switches)", 2025, 2265, 2575),
    Section("5b", "Ventilation & cooling system (2 fans · evap cooler **+ 12V→120V inverter** · light-safe baffle-duct fab · shade canopy)",
            total(VENTILATION)[0], total(VENTILATION)[0] + 60, total(VENTILATION)[0] + 150),
    Section("6",  "Housed revolving-door light lock (plastic-skin custom fabrication)", *total(LIGHTLOCK)),
    Section("6a", "Perimeter walkway (4 sections + drum-exit punch-out)", *total(WALKWAY)),
    Section("6b", "Panel swing pivot + fixed door frame (Ø89 post + bearings + cage + wall stays + rail saddles)", *total(SWINGPIVOT)),
    _printmaking_section(),
    Section("8",  "Transportation (per deployment)", 300, 750, 2000),
    Section("9",  "Licenses & permits", 220, 790, 1620),
]

# Master-shopping-list-only sections (not in the cost-breakdown's 13). Low/Mid/High estimates.
TOOLS = Section("10", "Printmaking tools & consumables", 350, 425, 500)
SAFETY = Section("11", "Safety & PPE", 120, 150, 180)


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


# ── Block injector — make the doc cost tables true OUTPUTS of costing.py ──────
# Each doc wraps a table in `<!-- BEGIN costing:KEY -->` / `<!-- END costing:KEY -->`. Two styles:
#   WHOLE  — the table is regenerated entirely from a generator fn (scenario, §7.1).
#   DETAIL — NUMBERS-ONLY: rewrite just the value cells (cols 1..len(fields)) from the line items,
#            preserving the doc's labels / Notes / format. Handles Low/Mid/High and Low/High
#            tables, with or without a Notes column. inject() regenerates; the linter gate
#            (check_blocks) blocks a commit if any block ever diverges from costing.py.
_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_F = "project-cost-breakdown.md"


def _whole_blocks() -> dict:
    return {"scenario": (_F, emit_scenario_table), "chemistry-7-1": (_F, emit_cost_breakdown_7_1),
            "scenario-a": (_F, emit_scenario_a), "scenario-b": (_F, emit_scenario_b),
            "scenario-c": (_F, emit_scenario_c),
            "ca-buckets": (_CA, emit_ca_buckets), "ca-ranking": (_CA, emit_ca_ranking),
            "funding-level1": ("funding-proposal.md", emit_funding_level1),
            "master-summary": ("master-shopping-list.md", emit_master_summary)}


def _detail_blocks() -> dict:
    lmh = ("low", "mid", "high")
    return {
        "container": (_F, CONTAINER, lmh), "interior": (_F, INTERIOR, lmh),
        "optics": (_F, OPTICS, lmh), "film": (_F, FILM, lmh), "water": (_F, WATER, ("low", "high")),
        "lightlock": (_F, LIGHTLOCK, lmh), "walkway": (_F, WALKWAY, lmh),
        "swingpivot": (_F, SWINGPIVOT, lmh),
    }


def _block_pat(key: str) -> "re.Pattern":
    return re.compile(r"(<!-- BEGIN costing:" + re.escape(key) + r" -->\n)(.*?)"
                      r"(\n<!-- END costing:" + re.escape(key) + r" -->)", re.DOTALL)


def _inline_pat(key: str) -> "re.Pattern":
    # INLINE block — a single generated value embedded mid-sentence (no surrounding newlines), so a
    # prose figure (e.g. the funding Level-1 total) is a true OUTPUT of costing.py while the pitch
    # prose stays hand-edited. The HTML-comment markers render invisibly in MkDocs.
    return re.compile(r"(<!-- BEGIN costing:" + re.escape(key) + r" -->)([^\n]*?)"
                      r"(<!-- END costing:" + re.escape(key) + r" -->)")


_FUND = "funding-proposal.md"


def _inline_blocks() -> dict:
    """key -> (file, fn) where fn() returns the exact inline string (the generated cost figure)."""
    lo, _mid, hi = grand_total()
    cl, ch = funding_combined()
    return {
        "fund-l1-total":       (_FUND, lambda: f"${funding_level1_total():,}"),
        "fund-scenario-span":  (_FUND, lambda: f"${round(lo, -3):,}–${round(hi, -3):,}"),
        "fund-perprint":       (_FUND, lambda: f"${_r(by_key('standard')['per_print'], 1):,}"),
        "fund-perprint-range": (_FUND, lambda: f"${_r(by_key('lean')['per_print'], 1)}–{_r(by_key('rich')['per_print'], 1)}"),
        "fund-50run":          (_FUND, lambda: f"${_r(by_key('standard')['section_total'], 10):,}"),
        "fund-combined":       (_FUND, lambda: f"${cl:,}–{ch:,}"),
        # project-summary.md (the home page) spec table — was a stale $38 / $1,900 pair.
        "summary-perprint":    ("project-summary.md", lambda: f"${_r(by_key('standard')['per_print'], 1):,}"),
        "summary-50run":       ("project-summary.md", lambda: f"${_r(by_key('standard')['section_total'], 10):,}"),
        # project-cost-breakdown §7.3 process comparison — Cyanotype ALL-IN row (§7.1 per-print +
        # PER_PRINT_CONSUMABLES), so it stays tied to §7.1 instead of drifting.
        "s73-pp-std":          (_F, lambda: f"${_pp('standard')}"),
        "s73-pp-range":        (_F, lambda: f"${_pp('lean')}–{_pp('rich')}"),
        "s73-50run-std":       (_F, lambda: f"${_pp('standard') * PRINTS:,}"),
        "s73-50run-range":     (_F, lambda: f"${_pp('lean') * PRINTS:,}–{_pp('rich') * PRINTS:,}"),
        # cost-analysis-report.md prose figures.
        "ca-mid-total":        (_CA, lambda: f"${grand_total()[1]:,}"),
        "ca-capital":          (_CA, lambda: f"${capital_mid():,}"),
        "ca-consumable":       (_CA, lambda: f"${_sec('7').mid:,}"),
        "ca-water-pct":        (_CA, lambda: f"{round(_sec('5').mid / capital_mid() * 100)}"),
        # operating-manual.md §0.2/§0.3 chemistry tier masses (from the TIERS).
        "om-amfe-g-lean":      (_OM, lambda: f"{_amfe_g('lean')}"),
        "om-amfe-g-standard":  (_OM, lambda: f"{_amfe_g('standard')}"),
        "om-amfe-g-rich":      (_OM, lambda: f"{_amfe_g('rich')}"),
        "om-amfe-kg-lean":     (_OM, lambda: _kg_fmt(_tier('lean').amfe_kg)),
        "om-amfe-kg-standard": (_OM, lambda: _kg_fmt(_tier('standard').amfe_kg)),
        "om-amfe-kg-rich":     (_OM, lambda: _kg_fmt(_tier('rich').amfe_kg)),
        "om-ferri-g-lean":     (_OM, lambda: f"{_ferri_g('lean')}"),
        "om-ferri-g-standard": (_OM, lambda: f"{_ferri_g('standard')}"),
        "om-ferri-g-rich":     (_OM, lambda: f"{_ferri_g('rich')}"),
        # equipment-layout-report.md §5 IBC stacking frame price band (from the WATER line item).
        "eq-ibc-frame-cost":   (_EL, lambda: f"${_ibc_frame().low:,}–${_ibc_frame().high:,}"),
        # ibc-stacking-report.md §9 frame cost (low/high split for the two-column BOM tables).
        "ibc-frame-low":       (_IBC, lambda: f"${_ibc_frame().low:,}"),
        "ibc-frame-high":      (_IBC, lambda: f"${_ibc_frame().high:,}"),
    }


def _pp(tier: str) -> int:
    """All-in per-print for §7.3 = §7.1 chem+substrate per-print + the processing consumables."""
    return _r(by_key(tier)['per_print'], 1) + PER_PRINT_CONSUMABLES


# operating-manual.md §0.2/§0.3 chemistry tier tables — the AmFe/ferricyanide masses restate the
# TIERS, so they fill from there (per-print g = tier kg ÷ PRINTS; 50-print = tier kg).
def _tier(key: str) -> Tier:
    return next(t for t in TIERS if t.key == key)


def _amfe_g(key: str) -> int:
    return round(_tier(key).amfe_kg * 1000 / PRINTS)


def _ferri_g(key: str) -> int:
    return round(_tier(key).ferri_kg * 1000 / PRINTS)


def _kg_fmt(v: float) -> str:
    return str(int(v)) if float(v).is_integer() else f"{v:g}"


# equipment-layout-report.md §5 — the IBC stacking frame line item owns its own price band.
def _ibc_frame() -> LineItem:
    return next(li for li in WATER if li.label.startswith("IBC stacking frame"))


def _reformat_cell(cell: str, value: int) -> str:
    """Replace the number in a value cell, preserving its whitespace / $ / ~ / ** formatting."""
    m = re.match(r"^(\s*\**~?\$?)([\d,]+)(\**\s*)$", cell)
    return f"{m.group(1)}{value:,}{m.group(3)}" if m else cell


def _render_detail(content: str, items: list, fields: tuple) -> str:
    """Numbers-only: rewrite each data/total row's value cells from the items; keep everything else."""
    tot = total(items)
    fidx = {"low": 0, "mid": 1, "high": 2}
    out, di = [], 0
    for ln in content.split("\n"):
        cells = ln.split("|")
        if len(cells) < 4:                                          # not a value-bearing row
            out.append(ln)
            continue
        inner = [c.strip() for c in cells[1:-1]]
        if all(c == "" or set(c) <= set("-:") for c in inner):      # separator
            out.append(ln)
            continue
        is_total = "total" in inner[0].lower()
        if not is_total and not re.match(r"^\s*\**~?\$?[\d,]+\**\s*$", cells[2]):
            out.append(ln)                                          # header / non-numeric row
            continue
        for k, f in enumerate(fields):
            ci = 2 + k
            if ci < len(cells) - 1:
                cells[ci] = _reformat_cell(cells[ci], tot[fidx[f]] if is_total else getattr(items[di], f))
        if not is_total:
            di += 1
        out.append("|".join(cells))
    return "\n".join(out)


def _apply(rel: str, key: str, regen, write: bool) -> tuple:
    path = os.path.join(_REPO, rel)
    text = open(path, encoding="utf-8").read()
    m = _block_pat(key).search(text)
    if not m:
        return (rel, key, "missing")
    new = regen(m.group(2))
    if m.group(2) == new:
        return (rel, key, "ok")
    if write:
        open(path, "w", encoding="utf-8").write(text[:m.start(2)] + new + text[m.end(2):])
        return (rel, key, "updated")
    return (rel, key, "STALE")


def _apply_inline(rel: str, key: str, fn, write: bool) -> tuple:
    path = os.path.join(_REPO, rel)
    text = open(path, encoding="utf-8").read()
    m = _inline_pat(key).search(text)
    if not m:
        return (rel, key, "missing")
    new = fn()
    if m.group(2) == new:
        return (rel, key, "ok")
    if write:
        open(path, "w", encoding="utf-8").write(text[:m.start(2)] + new + text[m.end(2):])
        return (rel, key, "updated")
    return (rel, key, "STALE")


def inject(write: bool = True) -> list:
    """Regenerate every marked block. Returns (file, key, 'ok'|'updated'|'STALE'|'missing')."""
    out = []
    for key, (rel, fn) in _whole_blocks().items():
        out.append(_apply(rel, key, lambda cur, fn=fn: fn(), write))
    for key, (rel, items, fields) in _detail_blocks().items():
        out.append(_apply(rel, key, lambda cur, it=items, fl=fields: _render_detail(cur, it, fl), write))
    for key, (rel, fn) in _inline_blocks().items():
        out.append(_apply_inline(rel, key, fn, write))
    return out


def check_blocks() -> list:
    """Linter helper: list of problems (a doc block that is stale or missing its markers)."""
    return [f"{rel}  costing:{key} -> {st}" for rel, key, st in inject(write=False) if st != "ok"]


# ── Self-check (regression guard — the canonical numbers, asserted) ──────────
EXPECTED = {                       # the figures the docs are reconciled to (this session)
    "muslin": 300,
    "lean":     {"chem": 909,  "total": 1210, "per_print": 24},  # 909 not 910: consistent ferri rounding ($104, not the doc's hand-rounded $105)
    "standard": {"chem": 1353, "total": 1650, "per_print": 33},
    "rich":     {"chem": 2681, "total": 2980, "per_print": 60},
    "grand_total": (19928, 25088, 32370),  # §4 film plane folded to its BOM (+438/+163/−112) on top of the §6b door frame
    "walkway": (1826, 2214, 2607),
    "water": (4063, 5085, 6104),
    "container": (2300, 3300, 4300),
    "lightlock": (1465, 1802, 2160),
    "swingpivot": (1112, 1232, 1372),
    "interior": (950, 1138, 1350),
    "optics": (95, 165, 240),
    "film": (3538, 3813, 4088),   # §4 BOM folded in (was hand-set $3,100/$3,650/$4,200, below its own BOM)
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
                       ("interior", INTERIOR), ("optics", OPTICS), ("film", FILM), ("ventilation", VENTILATION),
                       ("power", POWER)):
        if total(items) != EXPECTED[key]:
            errs.append(f"{key} {total(items)} != {EXPECTED[key]}")
    if grand_total() != EXPECTED["grand_total"]:
        errs.append(f"grand total {grand_total()} != {EXPECTED['grand_total']}")
    return errs


def main(argv: list[str]) -> int:
    if "--inject" in argv:
        for rel, key, st in inject(write=True):
            print(f"  [{st:>7}] {rel}  costing:{key}")
        return 0
    if "--check-blocks" in argv:
        probs = check_blocks()
        if probs:
            print("✗ doc blocks out of sync with costing.py (run: costing.py --inject):")
            for p in probs:
                print("   -", p)
            return 1
        print("✓ all costing blocks match the docs")
        return 0
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
