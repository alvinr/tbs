# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
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
PRICE_AMFE_PER_KG  = 60.00     # Photographers' Formulary — ammonium iron(III) oxalate (AmFe)
PRICE_FERRI_PER_KG = 24.29     # Bostick & Sullivan — potassium ferricyanide
DICHROMATE_RUN     = 25.00     # ammonium dichromate — trace contrast agent, per run
MUSLIN_ROLL_PRICE  = 100.00    # Fabric Direct — 60" x 150-yd unbleached muslin roll
MUSLIN_ROLLS       = 3         # ~388 yd / 150 -> 3 rolls (still 3 rolls after the FP_H 2138->2094 area drop)
MUSLIN_YARDS       = 388       # 2026-07-17: 50 prints × 101 sqft × 1.15 waste = 5,808 sqft ÷ 5 ft = ~1,162 linear ft = 388 yd (was 399 at 104 sqft)


# ── Ware New Cyanotype concentration tiers (per 50-print run) ────────────────
# AmFe : ferricyanide is held at Ware's 3:1 by weight; the tier sets the strength.
# The production tier is pinned by sensitizer-trials.md; Standard ½-Ware is the default.
@dataclass(frozen=True)
class Tier:
    key: str
    label: str
    amfe_kg: float
    ferri_kg: float


TIERS = [                             # AmFe/ferri kg for a 50-print run — sized to the active plane
    Tier("lean",     "Lean ⅓-Ware",     11.4,  3.8),   # 2026-07-17: ×0.97944 (FP_H 2138→2094, plane 9.62→9.42 m²)
    Tier("standard", "Standard ½-Ware",  17.1,  5.7),   # 120 ml/m²/coat × 2 × 9.42 m² @ 15 g/100 ml → ~340 g/print
    Tier("rich",     "Rich full-Ware",   34.2, 11.4),
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
        f"| Photographers' Formulary (~${PRICE_AMFE_PER_KG:.0f}/kg) |",
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
    LineItem("M12×65 partial-thread bolts + nuts + washers (×58)", 137, 137, 137, "91280A728 $1.595 + plain nut 90591A181 $0.256 + 4 flat 91166A290 + split 91202A246 /bolt; 3 per std bracket (42) + 4 per widened (16)"),
    LineItem("Transition bearing plates, 40×500×5mm flat bar (×2)", 5, 8, 10, "Welded to arm top at width transitions"),
    LineItem("Right walkway cantilever frame, 40×40×3mm SHS (8m)", 28, 34, 40, "rev12: closed rectangle + 2× 405mm center arms"),
    LineItem("Right walkway wall cleats, 8mm steel (×2)", 20, 28, 35, "Left corners — through-bolted to the wall"),
    LineItem("Combined corner plates, 10mm steel (×2)", 50, 65, 80, "Right corners — shared with the bottom film rail"),
    LineItem("M12×70 partial-thread bolts + nuts/washers (~24)", 60, 60, 60, "91280A732 $1.736 + plain nut + 4 flat + split /bolt; wall cleats + combined plates + 2 center-arm U-clamps"),
    LineItem("316 SS hold-down clips (FRP M/G-clip, ×20)", 25, 32, 40, "Near/far/right walkway GRP grating retention"),
    LineItem("Drum-exit punch-out — extra GRP grating (~0.23 m²)", 50, 57, 65, "600mm-deep landing at the light-lock exit"),
    LineItem("Left floor-leg cantilever brackets (×5)", 55, 75, 95, "50×50×3 SHS posts + 40×40×3 arms + foot plates"),
    LineItem("Floor screws — #14×2″ HWH 410 SS self-drilling (×20)", 7, 9, 11, "2026-07-22: wedge anchors → structural self-drillers (ply-over-steel container floor); Bridge Fasteners ~$0.35–0.55 ea"),
    LineItem("Fabrication (brackets, cantilever frame, install)", 424, 590, 750, "14 std + 4 widened brackets, right cantilever frame, 5 left floor-leg brackets, install; bracket scope matches the walkway-report §10 all-in figures; trimmed −$30/−$58 to reconcile with the parts registry after the M12 bolts firmed to real flat prices"),
]


# §5 Processing water system — the §5 sub-table is Low/High only; the scenario column needs Mid,
# computed here as the per-item midpoint. Line items own the truth (the hand-typed sub-table total
# $4,128/$6,201 and scenario $4,143/$5,180/$6,216 both drifted from the items, which sum to
# $4,063/$6,104). Source: project-cost-breakdown.md §5.
WATER = [
    LineItem("Water storage (4× IBC totes, 3× bulkhead fittings @ $137 ea, X1 fill tee)", 730, 871, 1010),
    LineItem("IBC stacking frame (RHS deep 4-leg box + 4 feet + retaining bars + hangers + 8 weld-on lashing rings + fab)", 982, 1222, 1461, "2026-07-22: floor anchors → #14×3¼″ 410 SS self-drillers (land feet over crossmembers) −$14/−$44; M12×40 hanger bolt FMW 1634027"),
    LineItem("Pumps and accumulator (P-01..P-05 + ACC-01, 5× mount brackets)", 480, 508, 536),
    LineItem("Corridor plumbing panel structure (18mm marine-ply backing board + drain-riser spine, 25mm pump-mount shirt, mount brackets + fasteners)", 215, 298, 380),
    LineItem("Under-walkway pipe-ribbon supports (4× welded cross-braces + 16 pipe clips)", 24, 36, 48),
    LineItem("Filter skid (3× Big Blue 4.5×20 separate housings on slotted-angle frame + cartridges)", 293, 392, 489, "2026-07-22: U-bracket retired → lag screws to ply backing −$18/−$21"),
    LineItem("Valves and fittings (6× BV ball valves, X1 4-way cross, S60×6 adapters, CV1, SV-01 + SV-02 taps, Blue equalization tie)", 699, 909, 1119, "2026-07-22: S60×6 adapter re-spec'd female-buttress×2\"NPT + 2→1\" bushing (CPP HMFN/20UD/027) +$48/+$24"),
    LineItem("Pipe (HDPE, spray bar)", 80, 97, 114),
    LineItem("Processing tray (304 SS panels + fabrication, shim strips, sump pickup, liner, hardware)", 1293, 1655, 2016, "2026-07-22: tray silicone gasket re-priced (Aqueon $17–25)"),
    LineItem("Spray bar assembly (40×25 SS RHS beam, side LDPE manifold, 26 nozzles, manifold + 7 feed tubes, 4 Ø32 wheels, ball joint, arm + turned adapter + jam nut + clamp collar, hose)", 349, 405, 461, "2026-07-22: arm jam nut/collar/self-tap/beam-clamp re-priced to real SKUs (Ruland CL-16-ST, Bobco flat-bar) +$47/+$66"),
    LineItem("Electrical (wiring only — fuse block in Electrical Report)", 37, 37, 37),
    LineItem("Processing consumables (6-mil poly, pH meter, citric acid)", 242, 260, 278),
]

# §1 Container — clean 2-item table; the scenario Mid was $3,150 but the items give $3,300.
CONTAINER = [
    LineItem("20 ft container — CW grade", 2000, 2750, 3500, "containermgt.com"),
    LineItem("Delivery — short haul (<50 miles)", 300, 550, 800, "Commercial tilt-bed hire"),
]

# §6 Housed revolving-door light lock (plastic-skin) — detail already = scenario.
# §6 = hinged-panel-report.md §8.2 (housing + drum). Line items mirror that BOM.
LIGHTLOCK = [
    LineItem("5mm UV-stabilized HDPE — Ø900 housing shell (~7 m²)", 180, 230, 280, "rolled + extrusion-welded; TAP / Online Metals"),
    LineItem("4mm PP — Ø864 drum shell + top/bottom caps (~7 m²)", 150, 195, 240, "TAP / Curbell"),
    LineItem("6215-2RS sealed bearing ×2 (Ø75×130×25, ABEC-1)", 121, 121, 121, "$60.59 ea firm, Bearings Direct; alt McMaster 6138K125 $394.88"),
    LineItem("75mm Ø × 150mm steel stub shafts (×2)", 30, 40, 50, "steel service center"),
    LineItem("Felt/brush wiper + 12mm neoprene (drum↔housing seal)", 40, 57, 75, "Frost King BP17A brush + 1/2\" neoprene by yard"),
    LineItem("Silicone bead sealant (bearing housing)", 6, 8, 10, "generic black UV silicone, Home Depot"),
    LineItem("100mm Ø SS grab rail (400mm cut)", 25, 35, 45, "16\" marine SS grab bar; 316 $45 / 304 ~$25"),
    LineItem("Matte-black interior finish", 40, 55, 70, "scuff + flat-black touch-in"),
    LineItem("Stainless fasteners + nylon isolation washers (no galvanic couple)", 45, 52, 60, "US Plastic 92674 shoulder washers + SS fastener kit"),
    LineItem("Plastic fabrication — roll + weld 2 cylinders, fit (16–22 hrs)", 800, 975, 1150, "Local plastic fab"),
]

# §6b = hinged-panel-report.md §8.3 (swing pivot) + §8.4 (fixed door frame). Line items mirror both.
SWINGPIVOT = [
    # §8.3 swing pivot hardware
    LineItem("Ø89×8 CHS pivot post + machined hub / thrust collar", 180, 240, 300, "carries ~3.6 kN·m swing cantilever; Metal Supermarkets / local fab"),
    LineItem("Thrust ball bearing, 51118 (Ø90 bore, single-direction)", 80, 80, 80, "Bearings Direct $80.03 firm; SF>50 on the 3.24 kN axial"),
    LineItem("iglide J flange bushings, Ø90 bore (×2)", 261, 261, 261, "igus JFM-9095-100 $130.53 ea, ships in days (replaced the $211/ea 3-mo-lead GGB DU)"),
    LineItem("Drum support cage, 40×40×3mm SHS", 70, 95, 120, "Local fab"),
    LineItem("Top + bottom wall stays + 4-bolt anchor plates", 90, 105, 120, "5/8\" turnbuckle (JETBGV58X6) + eye rods + fab plates"),
    LineItem("Drop-in rail saddles + tapered dowels (×4, removable left film rails)", 80, 105, 130, "Local fab / McMaster"),
    # §8.4 fixed door frame
    LineItem("Fixed door frame — 50×50×3 RHS members (×3)", 90, 105, 120, "Metal Supermarkets"),
    LineItem("Fixed door frame — top/bottom strip-brush light seals (2× 74405T12 brush + 2× 8813T53 holder)", 129, 129, 129, "McMaster $28.88+$35.37/8ft ×2 = $128.50 firm; seal paths #3–#4 — panel sweeps through the bristles"),
    LineItem("Fixed door frame — welding/fabrication + wall attachment", 200, 275, 350, "Local fab"),
]

# §6c = hinged-panel-report.md §8.1 (panel structure). Line items mirror that BOM. This section was
# MISSING from the model — the stepped panel itself (frame, skins, EPDM, latches, B2 bay, handle) had
# no home, so the grand total undercounted the hinged panel by its full cost.
PANEL = [
    LineItem("50×50×3mm RHS mild steel — frame perimeter + members (4× 6m)", 120, 140, 160, "Metal Supermarkets"),
    LineItem("4mm black PP sheet — panel skins both faces (~12 m², ×4)", 260, 340, 420, "rev11; TAP / Curbell"),
    LineItem("18mm exterior-grade plywood — Fan B mount band (0.5 sheet)", 30, 40, 50, "Home Depot"),
    LineItem("3mm aluminum plate — corner-zone core plates (×2)", 360, 410, 460, "Online Metals"),
    LineItem("20mm EPDM gasket — perimeter + housing-surround + cut seals (~21 m)", 24, 38, 52, "OKAYASU 3/4\"×1/8\"×65ft EPDM ×2 rolls (~$52/21m)"),
    LineItem("Aluminum U-channel — gasket + PP-skin retention (~40 m)", 120, 160, 200, "Online Metals"),
    LineItem("Southco C2-33 cam compression latch (×4)", 76, 90, 104, "Southco / McMaster"),
    LineItem("4mm PP + EPDM lip — B2 punch-out bay (4-wall tube ~890mm)", 60, 90, 120, "rev11"),
    LineItem("Flat-black paint (RAL 9005) — bay/weld touch-in", 10, 15, 20, "local"),
    LineItem("304 SS D-grab pull handle (~300mm) + 2× M8 + backing plate", 70, 80, 90, "matte-black, §4.3; chose 304 over 316 (~$186); interior/non-wet"),
]

# §6d = chemistry-prep-shelves.md §7 (fold-down chemistry prep shelf). Point estimates.
SHELF = [
    point("Phenolic-faced plywood, 18mm (300×600)", 60, "Home Depot / lumber yard"),
    point("25×25×3mm steel SHS — frame + spill lip (6m)", 30, "Online Metals / Metal Supermarkets"),
    LineItem("Continuous (piano) hinge, 600mm", 22, 29, 35, "Würth LSN8-32-600 $22.68 / LSN15 $35.72 (32×600 satin SS)"),
    point("Folding shelf stays/brackets (×2, fold-flat)", 24, "Amazon / McMaster-Carr"),
    point("Wall mounting cleat + 2 stay anchors (6mm steel, slotted)", 18, "Local fab / offcut"),
    LineItem("Wall backing plates, 8mm steel welded (×3: cleat + 2 stays)", 18, 24, 30, "flat load anchors on the corrugated end wall"),
    point("M8 wall bolts + washers/nuts (~12)", 6, "M8×25 bolt 91280A534 $0.37 + nut 90591A161 + washer 91166A270"),
    point("Transport latch (over-center / barrel)", 8, "Amazon"),
    point("M5×16 CSK screws (×8) — ply panel", 1, "91420A326 $0.115 ea"),
    point("Corner gusset plates, 3mm (×4)", 5, "steel offcut"),
    point("Flat-black epoxy spray paint", 12, "hardware store"),
    point("½\" HDPE pipe — TAP-01 trunk extension (~1.5m)", 10, "irrigation supply"),
]


# §2 Interior conversion — the detail "Section total" category breakdown is correct ($950/$1,138/
# $1,350); the SCENARIO row ($970/$1,140/$1,310) was the drifted one.
INTERIOR = [
    LineItem("Light-sealing materials", 157, 168, 178, "blackout bundle: weatherstrip + felt + gaffer"),
    LineItem("Interior paint", 100, 130, 160),
    # Image-plane flat backing RETIRED 2026-07-22 — same ACM as film 'Dibond ACM 4×8 sheets' (double-count)
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
    LineItem("Disc retaining ring (Al 6061-T6, M52×0.75 thread)", 15, 20, 25, "local fab"),
]


# §4 Film plane mechanism (4-corner U-channel + acetal skate + 316 cross-slide + Ruland U-joint).
# Line items own the truth; the section total sums them. The U-joint ($276×4), 4040N12 supports,
# and 304 U-channel rails are firm-priced; the Low/High spread comes from the muslin spring clips
# ($3/$5.50/$8 ea) + the estimated skate / cross-slide / cam-clamp fab lines + the wall-seat saddle
# plate. Source: project-cost-breakdown.md §4.1–4.3 / film-plane-mechanism-report.md.
FILM = [
    # 4.1 Structural & rails (304 U-channel + acetal skate + 316 cross-slides + Ruland U-joint)
    LineItem("304 U-channel depth rails 3×1½\" (1262T21, ×4 wall-to-wall)", 2172, 2172, 2172, "$362/6ft ×6 — 8ft lengths for continuous rails, firm at order"),
    LineItem("Ruland USKC12-6-6-SS U-joints (×4) + nitrile boots (×4)", 1226, 1226, 1226, "$276 ea joint (interim; cheaper alt in research) + $30.59 boot (UBOOT12/19-NI-KIT, verified)"),
    LineItem("McMaster 4040N12 304 shaft supports (×4) + 3/8\" 304 stub rod (89535K87, 3ft)", 245, 245, 245, "$58 ea support + $13.25 rod — firm"),
    LineItem("Acetal skates (×4) — Ø32/Ø20 acetal rollers + 304 axle pins + fab carriage plates", 182, 230, 282, "2026-07-22: decomposed; axle = spray 304 pins (B0816MQ5T6) $20 (was $176 316 rod)"),
    LineItem("316 flat-bar Z/X cross-slides (×4) + UHMW pads + gibs", 180, 280, 380, "2-axis stack per corner; est."),
    LineItem("Cam-lever rail brakes (×12, skate lock)", 96, 138, 180, "3 per corner; est."),
    LineItem("Corner plates, ¼\" 304 SS 6×8 (×4)", 152, 180, 208, "U-joint mount — steel, not aluminum"),
    # 4.2 Film plane frame & backing
    point("Aluminum angle 2×2×3/16 (6061-T6 anodized, expendable) 8 ft (×10)", 1312, "McMaster 8982K509 $131.24/8ft — a service center is cheaper by the length; re-quote to firm"),
    LineItem("Dibond ACM 4mm 4×8 black sheets (×4, Option A strips) — single rigid plane", 380, 380, 380, "Curbell 4mm black $95/sheet firm; 4 full-height vertical strips, 3 vertical seams"),
    LineItem("Light-seal set — EPDM tape (×2) + Rosco Duvetyne + 6-mil poly + Gorilla tape (×6)", 260, 274, 288),
    LineItem("Muslin clamps — nylon spring clamp ×58 (Pittsburgh 69289)", 174, 203, 232, "$3–4 ea; inert fiberglass + swivel pads, top + 2 side edges (bottom = walkway clearance)"),
    LineItem("Muslin clamp filler — HDPE L-channel strip", 30, 50, 70, "inert HDPE packer, ~8.7 m, firm at fab — lets the clamp bite a solid full-depth edge"),
    # 4.3 Wall-seat saddles (rev 11, ICP-11–14) — estimates, confirm at procurement
    point("Wall-seat saddles ×6 — 8mm steel plate, cut + welded (ICP-11)", 318, "rev12: 2 BR ends moved to the walkway combined corner plates; ~$53/saddle"),
    point("Saddle fasteners — M12×65 through-bolts (×28) + M8 thumbscrews (×12) + M8×25 hex bolts (×8)", 106, "ICP-12/13/14; M12×65 91280A728 + plain nut 90591A181 + 4 flat 91166A290 + split 91202A246 per bolt; M8×25 fixing 91280A534 $0.37"),
]


# §5b Ventilation & cooling — single-value BOM (point estimates). Source: ventilation-report.md.
# Items sum to $824; the report total was STALE at $769 (the last 4 items were added without
# updating it). The cost-breakdown §5b scenario ($770/$830/$920) is a budget band around this.
VENTILATION = [
    point("150×150×50mm axial fans ×2 (12V DC)", 50),
    LineItem("Evaporative cooler (Hessaire MC18M)", 185, 208, 230),
    LineItem("Cooler inverter (Victron Phoenix 12/375 GFCI + DC fuse/disconnect + GFCI outlet)", 153, 214, 275),
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
    LineItem("Solar & battery (3× 200W panels, MPPT 100/50, 1× 100Ah LiFePO4, shore charger, mounts, PV cabling, PV disconnect, panel)", 1236, 1340, 1443),
    LineItem("Distribution & wiring (plywood backboard + IP65 enclosure, fuse block, disconnect, contactor, 2× E-stop, charge/shore fuses, protection, conduit, LED, master pump switch, power-panel raised weld-in frame)", 1440, 1549, 1659, "2026-07-22: grommets/conduit/trunking re-priced to real SKUs (−$34 low/−$7 high); power-panel neoprene gasket (Pres-Bond)"),
]


FRONT_BOARD_MID  = 1470   # tilt-swing front board §12.4 LOW total — source: tilt-swing-board-report.md
FRONT_BOARD_HIGH = 2440   # §12.4 HIGH total (CNC + anodise + custom bellows upper band)


def _sec(sid: str) -> Section:
    return next(s for s in SECTIONS if s.sid == sid)


def emit_funding_level1() -> str:
    """funding-proposal.md Level 1 — Core Build: each section's Mid + the (separate) front board,
    plus 10% contingency. A 2nd VIEW of the same costing source (so it can't drift)."""
    rows = [
        ("20ft container (Cargo Worthy grade) + delivery", _sec("1").mid),
        ("Interior conversion (light-seal, paint, ventilation, door)", _sec("2").mid),
        ("Pinhole plate (precision laser-drilled, SS-302, interchangeable frame)", _sec("3").mid),
        ("Film plane mechanism (4-corner U-channel + acetal skate + Ruland U-joint)", _sec("4").mid),
        ("Tilt-swing front board mechanism", FRONT_BOARD_MID),
        ("Housed revolving-door light trap (plastic-skin Ø900 housing + C-shell drum, bearings, seals, fabrication)", _sec("6").mid),
        ("Processing water system (tray, spray bar, 3-stage filtration, IBC stacking frame)", _sec("5").mid),
        ("Power & electrical (600W solar · LiFePO4 · MPPT · distribution · protection · lighting)", _sec("5a").mid),
        ("Ventilation & cooling (2 fans · evap cooler + 12V→120V inverter · light-safe ducting)", _sec("5b").mid),
        ("Perimeter walkway (4 sections + drum-exit punch-out)", _sec("6a").mid),
        ("Panel swing pivot + fixed door frame (Ø89 post + bearings + cage + wall stays + door frame)", _sec("6b").mid),
        ("Hinged panel structure (stepped frame + PP skins + Al core + EPDM + latches + B2 bay + handle)", _sec("6c").mid),
        ("Chemistry prep shelf (fold-down board + frame + hinge/stays + tap trunk extension)", _sec("6d").mid),
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
        ("2. Interior conversion (light-seal, paint, ventilation)", _sec("2")),
        ("3. Pinhole optics plate", _sec("3")),
        ("4. Film plane mechanism (4-corner U-channel + acetal skate + 316 cross-slide + U-joint, incl. wall-seat saddles)", _sec("4")),
        ("5. Print washing — water system (incl. IBC stacking frame)", _sec("5")),
        ("6. Electrical — power, circuits, wiring", _sec("5a")),
        ("7. Housed revolving-door light lock (plastic-skin custom fabrication)", _sec("6")),
        ("7a. Panel swing pivot + fixed door frame (Ø89 post + bearings + cage + wall stays + rail saddles + door frame)", _sec("6b")),
        ("7b. Perimeter walkway (4 sections + drum-exit punch-out)", _sec("6a")),
        ("7c. Hinged panel structure (stepped frame + PP skins + Al core + EPDM + cam latches + B2 bay + pull handle)", _sec("6c")),
        ("7d. Chemistry prep shelf (fold-down board + steel frame + hinge/stays + TAP-01 trunk extension)", _sec("6d")),
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
    ids = ("1", "2", "3", "4", "5", "5a", "6", "6b", "6c", "6d", "6a", "5b", "7")
    lo = sum(_sec(i).low for i in ids) + TOOLS.low + SAFETY.low
    hi = sum(_sec(i).high for i in ids) + TOOLS.high + SAFETY.high
    return (lo, hi)


def funding_level1_total() -> int:
    sub = (_sec("1").mid + _sec("2").mid + _sec("3").mid + _sec("4").mid + FRONT_BOARD_MID
           + _sec("6").mid + _sec("5").mid + _sec("5a").mid + _sec("5b").mid + _sec("6a").mid
           + _sec("6b").mid + _sec("6c").mid + _sec("6d").mid + _sec("7").mid)
    return sub + _r(sub * 0.10, 10)


# Funding-proposal Level 2/3 ranges (deployment + documentation — funding-doc-specific, not in the
# 13 build sections). The combined first-year band is computed from them + Level 1.
FUNDING_L2 = (1025, 2750)   # transport ($1,000–2,400) + permits ($0–300) + water resupply ($25–50), one deployment
FUNDING_L3 = (2000, 5000)   # videography ($1,000–2,500) + photography ($500–1,000) + publication ($500–1,500)


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
        ("Film plane mechanism (4-corner U-channel + U-joint, incl. wall-seat saddles)", _sec("4").low),
        ("Water system (incl. processing tray, spray bar, IBC stacking frame)", _sec("5").low),
        ("Power & electrical system (solar · 1× LiFePO4 · distribution · lighting · protection · master pump switch)", _sec("5a").low),
        ("Ventilation & cooling system (2 fans · evap cooler + inverter · light-safe baffle-duct fab · shade canopy)", _sec("5b").low),
        ("Revolving drum light trap (plastic-skin custom fabrication)", _sec("6").low),
        ("Perimeter walkway (4 sections, removable, GRP grating)", _sec("6a").low),
        ("Panel swing pivot + fixed door frame (Ø89 pivot + bearings + cage + wall stays + saddles + door frame)", _sec("6b").low),
        ("Hinged panel structure (stepped frame + PP skins + Al core + EPDM + latches + B2 bay + handle)", _sec("6c").low),
        ("Chemistry prep shelf (fold-down board + tap trunk extension)", _sec("6d").low),
        ("Cyanotype chemistry + substrate (50 prints)", _sec("7").low),
        ("Transport per deployment (local)", SCEN_A["transport"]),
        ("Permits (minimal)", SCEN_A["permits"]),
    ]


def _scenario_b_rows() -> list:
    return [
        ("Container (CW) + delivery", SCEN_B["container"]),
        ("Interior conversion (full)", _sec("2").mid),
        ("Pinhole plate", _sec("3").mid),
        ("Film plane mechanism (4-corner U-channel + U-joint + wall-seat saddles)", _sec("4").mid),
        ("Water system (incl. processing tray, spray bar, IBC stacking frame)", _sec("5").mid),
        ("Power & electrical system (solar · 1× LiFePO4 · distribution · lighting · protection · master pump switch)", _sec("5a").mid),
        ("Ventilation & cooling system (2 fans · evap cooler + inverter · light-safe baffle-duct fab · shade canopy)", _sec("5b").mid),
        ("Revolving drum light trap (plastic-skin custom fabrication)", _sec("6").mid),
        ("Perimeter walkway (4 sections, removable, GRP grating)", _sec("6a").mid),
        ("Panel swing pivot + fixed door frame (Ø89 pivot + bearings + cage + wall stays + saddles + door frame)", _sec("6b").mid),
        ("Hinged panel structure (stepped frame + PP skins + Al core + EPDM + latches + B2 bay + handle)", _sec("6c").mid),
        ("Chemistry prep shelf (fold-down board + tap trunk extension)", _sec("6d").mid),
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
_PT = "processing-tray-and-spray-bar.md"
_WS = "water-system-report.md"
_ELEC = "electrical-report.md"
_VENT = "ventilation-report.md"
_FPM = "film-plane-mechanism-report.md"
_FC  = "film-clamp-mechanism-report.md"
_TSB = "tilt-swing-board-report.md"
_HP  = "hinged-panel-report.md"
_LTS = "light-trap-selection.md"


def capital_mid() -> int:
    """One-time build capital = grand Mid − consumable (§7) − recurring transport (§8) − permits (§9)."""
    return grand_total()[1] - _sec("7").mid - _sec("8").mid - _sec("9").mid


def _pct(mid: int, cap: int) -> str:
    p = mid / cap * 100
    return f"{round(p)}%" if p >= 1 else f"{p:.1f}%"


# ── §4 (cost-analysis-report.md) savings levers ──────────────────────────────
# Each lever's saving is a DELTA (as-built − alternative). Bucket A (done): the container-grade
# lever is a true computed subtraction (CW − WWT, straight off the scenario layer), and the §4
# roll-up + percentage are computed sums of the levers below; the remaining bands are single-
# sourced here as declared estimates (they were hand-typed in the report). This ends the
# duplication and lets the roll-up cascade.
#   Bucket B (partially resolved 2026-07-05): solar is now a computed subtraction (drop 1×
#   solar-panel-200w), and modeling against the BOM showed two "levers" were phantom — film is BANKED
#   (manual is the standard build) and the battery is ALREADY 1×100Ah — so both were dropped from the
#   roll-up (see the SAVINGS_LEVERS note below). STILL OPEN: a costed chem-compatible poly-tray
#   alternative for lever #3 (leave as a band until specced), and — not a §4 lever — a galvanized-steel
#   walkway-grating alt vs the §5 GRP premium.
def _lever_container() -> int:
    return SCEN_B["container"] - SCEN_A["container"]     # CW − WWT grade delta (computed)


# (id, low, high, in_rollup) — only levers that are STILL AVAILABLE feed the §4 roll-up.
# Bucket B (2026-07-05): modeling each alternative against the as-built BOM showed two levers are NOT
# available savings, so they were dropped from the roll-up (they were double-counting):
#   • film   — ACTIONED: manual IS the standard build, so the $827 electric-kit cost is already BANKED,
#              not a saving you can still take.
#   • battery — the costed standard is already 1×100Ah ($350); there is no 200→100Ah drop to make. A
#              2nd pack is a +$375 optional UPGRADE (parts.py lifepo4-100ah note), i.e. an ADD, not a save.
# The available levers: container (computed CW−WWT), solar (computed = drop 1× solar-panel-200w), and
# tray (still a declared band — a chem-compatible poly-tray alternative isn't costed yet).
SAVINGS_LEVERS = [
    ("container", _lever_container(), _lever_container(), True),
    ("film",      827,  827,  False),     # #2 ACTIONED — $827 electric kit is BANKED into the manual standard, not available
    ("tray",      600,  1000, False),     # #3 DECIDED 2026-07-05: KEEP 304 SS (poly needs a support frame over the 4.5m span + poly-weld fab; SS is self-supporting + durable) — declined, out of the roll-up
    ("battery",   375,  375,  False),     # #4 standard is 1×100Ah; the 2nd pack is a +$375 UPGRADE, not a saving
    ("solar",     133,  133,  True),      # #5 computed: drop 1× solar-panel-200w ($133 low=high, parts.py)
    ("valves",    100,  200,  False),     # #6 estimate — no specced alternative
]


def _lever(name: str) -> tuple:
    return next((lo, hi) for n, lo, hi, _ in SAVINGS_LEVERS if n == name)


def _savings_rollup() -> tuple:
    lo = sum(lo for _, lo, _, inc in SAVINGS_LEVERS if inc)
    hi = sum(hi for _, _, hi, inc in SAVINGS_LEVERS if inc)
    return (round(lo / 50) * 50, round(hi / 50) * 50)   # ~rounded to $50 (levers are estimates)


def _savings_pct() -> tuple:
    lo = sum(lo for _, lo, _, inc in SAVINGS_LEVERS if inc)
    hi = sum(hi for _, _, hi, inc in SAVINGS_LEVERS if inc)
    cap = capital_mid()
    return (round(100 * lo / cap), round(100 * hi / cap))


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
    ("Film-plane mechanism",    "4",  "Carriages, Option-A cross-slides, muslin spring clips, wall-seat saddles"),
    ("Container + delivery",    "1",  "Grade-dependent (CW vs WWT)"),
    ("Power & electrical",      "5a", "Battery + solar + distribution + protection"),
    ("Perimeter walkway",       "6a", "GRP grating + steel cantilevers"),
    ("Light lock",              "6",  "Plastic-skin custom fabrication"),
    ("Swing pivot",             "6b", "Pivot post + bearings + cage + fixed RHS door frame"),
    ("Hinged panel structure",  "6c", "Stepped frame + PP skins + Al core + EPDM + latches + B2 bay"),
    ("Chemistry prep shelf",    "6d", "Fold-down phenolic board + frame + hinge/stays + tap extension"),
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
    Section("4",  "Film plane mechanism (4-corner U-channel + acetal skate + U-joint, incl. wall-seat saddles)", *total(FILM)),
    Section("5",  "Processing water system (incl. tray, spray bar, IBC stacking frame)", *total(WATER)),
    Section("5a", "Power & electrical system (solar · 1× LiFePO4 · MPPT · distribution · lighting · protection · master pump switch)", 2665, 2873, 3081),
    Section("5b", "Ventilation & cooling system (2 fans · evap cooler **+ 12V→120V inverter** · light-safe baffle-duct fab · shade canopy)",
            total(VENTILATION)[0], total(VENTILATION)[0] + 60, total(VENTILATION)[0] + 150),
    Section("6",  "Housed revolving-door light lock (plastic-skin custom fabrication)", *total(LIGHTLOCK)),
    Section("6a", "Perimeter walkway (4 sections + drum-exit punch-out)", *total(WALKWAY)),
    Section("6b", "Panel swing pivot + fixed door frame (Ø89 post + bearings + cage + wall stays + rail saddles)", *total(SWINGPIVOT)),
    Section("6c", "Hinged panel structure (stepped frame + PP skins + Al core + EPDM + cam latches + B2 bay + pull handle)", *total(PANEL)),
    Section("6d", "Chemistry prep shelf (fold-down phenolic board + steel frame + hinge/stays + TAP-01 trunk extension)", *total(SHELF)),
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


# ── Registry reconciliation (parts.py is the procurement source of record) ───────────────────────
# Each registry-backed section's firm low/high must equal the sum of its constituent registry
# systems' parts.system_total. The mid + the scenario bands on 5a/5b/7/8/9 are costing-only (a thin
# budgeting layer the procurement registry deliberately doesn't carry), so those are not asserted here.
_SECTION_SYSTEMS = {
    "1": ["container"], "2": ["interior"], "3": ["optics"], "4": ["film", "clamp"],
    "5": ["water", "ibc-frame", "tray", "spray"], "6": ["lightlock"], "6a": ["walkway"],
    "6b": ["swing", "door"], "6c": ["panel"], "6d": ["shelf"],
}


def check_registry() -> list[str]:
    """Linter helper: every registry-backed section's (low, high) == sum of its registry systems."""
    import parts                                                 # late import — parts imports costing
    errs = []
    for sid, syss in _SECTION_SYSTEMS.items():
        sec = _sec(sid)
        lo = sum(parts.system_total(s)[0] for s in syss)
        hi = sum(parts.system_total(s)[1] for s in syss)
        if (sec.low, sec.high) != (lo, hi):
            errs.append(f"§{sid} {syss}: costing ({sec.low}, {sec.high}) != registry ({lo}, {hi})")
    return errs


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
        "s73-pp-std":          ([_F, "photosensitive-plane-options.md"], lambda: f"${_pp('standard')}"),
        "s73-pp-range":        ([_F, "photosensitive-plane-options.md"], lambda: f"${_pp('lean')}–{_pp('rich')}"),
        "s73-50run-std":       (_F, lambda: f"${_pp('standard') * PRINTS:,}"),
        "s73-50run-range":     (_F, lambda: f"${_pp('lean') * PRINTS:,}–{_pp('rich') * PRINTS:,}"),
        # cost-analysis-report.md prose figures.
        "ca-mid-total":        (_CA, lambda: f"${grand_total()[1]:,}"),
        "ca-capital":          (_CA, lambda: f"${capital_mid():,}"),
        "ca-consumable":       (_CA, lambda: f"${_sec('7').mid:,}"),
        "ca-water-pct":        (_CA, lambda: f"{round(_sec('5').mid / capital_mid() * 100)}"),
        # operating-manual.md §0.2/§0.3 chemistry tier masses (from the TIERS).
        "om-amfe-g-lean":      (_OM, lambda: f"{_amfe_g('lean')}"),
        "om-amfe-g-standard":  ([_OM, "master-shopping-list.md"], lambda: f"{_amfe_g('standard')}"),
        "om-amfe-g-rich":      (_OM, lambda: f"{_amfe_g('rich')}"),
        "om-amfe-kg-lean":     (_OM, lambda: _kg_fmt(_tier('lean').amfe_kg)),
        "om-amfe-kg-standard": ([_OM, "master-shopping-list.md"], lambda: _kg_fmt(_tier('standard').amfe_kg)),
        "om-amfe-kg-rich":     (_OM, lambda: _kg_fmt(_tier('rich').amfe_kg)),
        "om-ferri-g-lean":     (_OM, lambda: f"{_ferri_g('lean')}"),
        "om-ferri-g-standard": (_OM, lambda: f"{_ferri_g('standard')}"),
        "om-ferri-g-rich":     (_OM, lambda: f"{_ferri_g('rich')}"),
        # equipment-layout-report.md §5 IBC stacking frame price band (from the WATER line item).
        "eq-ibc-frame-cost":   (_EL, lambda: f"${_ibc_frame().low:,}–${_ibc_frame().high:,}"),
        # ibc-stacking-report.md §9 frame cost (low/high split for the two-column BOM tables).
        "ibc-frame-low":       (_IBC, lambda: f"${_ibc_frame().low:,}"),
        "ibc-frame-high":      (_IBC, lambda: f"${_ibc_frame().high:,}"),
        # processing-tray-and-spray-bar.md §6 BOM subtotals (from the WATER line items).
        # Shared across the dedicated report + the two docs that summarize/point to it.
        "tray-low":            ([_PT, _WS, _CA], lambda: f"${_pt_line('Processing tray').low:,}"),
        "tray-high":           ([_PT, _WS, _CA], lambda: f"${_pt_line('Processing tray').high:,}"),
        # cost-analysis-report.md §4 savings levers (bucket A — see SAVINGS_LEVERS) + §6 light lock
        "ca-lever-container":  (_CA, lambda: f"${_lever('container')[0]:,}"),
        "ca-lever-film":       (_CA, lambda: f"${_lever('film')[0]:,}"),
        "ca-lever-tray-low":   (_CA, lambda: f"${_lever('tray')[0]:,}"),
        "ca-lever-tray-high":  (_CA, lambda: f"${_lever('tray')[1]:,}"),
        "ca-lever-battery":    (_CA, lambda: f"${_lever('battery')[0]:,}"),
        "ca-lever-solar":      (_CA, lambda: f"${_lever('solar')[0]:,}"),
        "ca-lever-valves-low": (_CA, lambda: f"${_lever('valves')[0]:,}"),
        "ca-lever-valves-high":(_CA, lambda: f"${_lever('valves')[1]:,}"),
        # roll-up is flat now (container + solar, both fixed values) — low==high, so a single emitter
        "ca-savings-low":      (_CA, lambda: f"${_savings_rollup()[0]:,}"),
        "ca-savings-pct-low":  (_CA, lambda: f"{_savings_pct()[0]}"),
        "ca-lightlock-mid":    (_CA, lambda: f"${total(LIGHTLOCK)[1]:,}"),
        "spray-low":           ([_PT, _WS], lambda: f"${_pt_line('Spray bar').low:,}"),
        "spray-high":          ([_PT, _WS], lambda: f"${_pt_line('Spray bar').high:,}"),
        "tray-spray-total-low":  (_PT, lambda: f"${_pt_line('Processing tray').low + _pt_line('Spray bar').low:,}"),
        "tray-spray-total-high": (_PT, lambda: f"${_pt_line('Processing tray').high + _pt_line('Spray bar').high:,}"),
        # electrical-report.md §8 system totals (1-pack standard build).
        "elec-system-total":   (_ELEC, lambda: f"${_sec('5a').mid:,}"),
        "elec-canopy-total":   (_ELEC, lambda: f"${_elec_canopy():,}"),
        "elec-cooling-total":  (_ELEC, lambda: f"${_elec_cooling():,}"),
        "elec-grand-total":    (_ELEC, lambda: f"${_elec_grand():,}"),
        # ventilation-report.md §3/§4 strategy costs (the §9 parts-list total now lives in the
        # generated parts:ventilation block) — all from §5b VENTILATION.
        "vent-fans":           (_VENT, lambda: f"${_vent_line('150×150×50mm axial fans').mid:,}"),
        "vent-shade":          (_VENT, lambda: f"${_vent_line('Shade canopy').mid + _vent_line('Canopy frame').mid:,}"),
        "vent-cooler-inverter": (_VENT, lambda: f"${_vent_line('Evaporative cooler').mid + _vent_line('Cooler inverter').mid:,}"),
        # film-plane-mechanism-report.md §7 materials total — the §4 FILM BOM low (base estimate;
        # the old hand-set ~$3,100 sat below this BOM).
        "film-total":          (_FPM, lambda: f"${total(FILM)[0]:,}"),
        # film-clamp-mechanism-report.md §4 — clamp-system band (generic spring clip → quality).
        "clamp-system-low":    (_FC, lambda: f"${_clamp_system('low'):,}"),
        "clamp-system-high":   (_FC, lambda: f"${_clamp_system('high'):,}"),
        # tilt-swing-board-report.md §12.4 — the board's own BOM low (= FRONT_BOARD_MID, which the
        # rest of the model reads); the §12.4 note's film-plane comparison uses film-total above.
        "front-board-total":   (_TSB, lambda: f"${FRONT_BOARD_MID:,}"),
        "front-board-total-high": (_TSB, lambda: f"${FRONT_BOARD_HIGH:,}"),
        # hinged-panel-report.md §8.1–8.5 — the panel's four assemblies (§6c / §6 / §6b-split) + total.
        "hp-panel-low":        (_HP, lambda: f"${total(PANEL)[0]:,}"),
        "hp-panel-high":       (_HP, lambda: f"${total(PANEL)[2]:,}"),
        # LIGHTLOCK total (= §6) — owned by hinged-panel §8.2; also single-sources the custom-fab
        # cost restated in light-trap-selection.md §3.3/§4.5/§6 (a key may live in several docs).
        "hp-housing-low":      ((_HP, _LTS), lambda: f"${total(LIGHTLOCK)[0]:,}"),
        "hp-housing-high":     ((_HP, _LTS), lambda: f"${total(LIGHTLOCK)[2]:,}"),
        "hp-swing-low":        (_HP, lambda: f"${_swing_only('low'):,}"),
        "hp-swing-high":       (_HP, lambda: f"${_swing_only('high'):,}"),
        "hp-doorframe-low":    (_HP, lambda: f"${_door_only('low'):,}"),
        "hp-doorframe-high":   (_HP, lambda: f"${_door_only('high'):,}"),
        "hp-total-low":        (_HP, lambda: f"${_panel_grand('low'):,}"),
        "hp-total-high":       (_HP, lambda: f"${_panel_grand('high'):,}"),
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


# processing-tray-and-spray-bar.md §6 — the tray + spray-bar line items own their price bands.
def _pt_line(prefix: str) -> LineItem:
    return next(li for li in WATER if li.label.startswith(prefix))


# electrical-report.md §8 — the cooler/canopy groupings are subsets of the §5b VENTILATION BOM.
def _vent_line(prefix: str) -> LineItem:
    return next(li for li in VENTILATION if li.label.startswith(prefix))


# film-clamp-mechanism-report.md §4 — the muslin clamp system = the §4 FILM clamp line + its
# mounting line (M5 bolts/Nylocks + neoprene jaw strip).
def _film_line(prefix: str) -> LineItem:
    return next(li for li in FILM if li.label.startswith(prefix))


def _clamp_system(which: str) -> int:    # which = 'low' | 'high'
    return getattr(_film_line("Muslin clamps"), which) + _film_line("Muslin clamp filler").mid


# hinged-panel-report.md §8.3/§8.4 — §6b SWINGPIVOT bundles the swing pivot (§8.3) + door frame (§8.4);
# split them out for the report's separate §8.3/§8.4/§8.5 rows.
def _swing_only(which: str) -> int:
    return sum(getattr(li, which) for li in SWINGPIVOT if not li.label.startswith("Fixed door frame"))


def _door_only(which: str) -> int:
    return sum(getattr(li, which) for li in SWINGPIVOT if li.label.startswith("Fixed door frame"))


def _panel_grand(which: str) -> int:     # §8.5 total = §6 + §6b + §6c
    return getattr(_sec("6"), which) + getattr(_sec("6b"), which) + getattr(_sec("6c"), which)


def _elec_canopy() -> int:    # shade cloth + frame
    return _vent_line("Shade canopy").mid + _vent_line("Canopy frame").mid


def _elec_cooling() -> int:   # cooler + inverter(+DC/outlet) + external power cable
    return (_vent_line("Evaporative cooler").mid + _vent_line("Cooler inverter").mid
            + _vent_line("Cooler external power").mid)


def _elec_grand() -> int:     # electrical system + canopy + cooling
    return _sec("5a").mid + _elec_canopy() + _elec_cooling()


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
    pat = _block_pat(key)
    matches = list(pat.finditer(text))
    if not matches:
        return (rel, key, "missing")
    if all(m.group(2) == regen(m.group(2)) for m in matches):   # every occurrence current
        return (rel, key, "ok")
    if write:
        open(path, "w", encoding="utf-8").write(
            pat.sub(lambda m: m.group(1) + regen(m.group(2)) + m.group(3), text))
        return (rel, key, "updated")
    return (rel, key, "STALE")


def _apply_inline(rel: str, key: str, fn, write: bool) -> tuple:
    path = os.path.join(_REPO, rel)
    text = open(path, encoding="utf-8").read()
    pat = _inline_pat(key)
    matches = list(pat.finditer(text))
    if not matches:
        return (rel, key, "missing")
    new = fn()
    if all(m.group(2) == new for m in matches):                 # every occurrence current
        return (rel, key, "ok")
    if write:
        open(path, "w", encoding="utf-8").write(
            pat.sub(lambda m: m.group(1) + new + m.group(3), text))
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
        for r in ((rel,) if isinstance(rel, str) else rel):     # a key may live in several docs
            out.append(_apply_inline(r, key, fn, write))
    return out


def check_blocks() -> list:
    """Linter helper: list of problems (a doc block that is stale or missing its markers)."""
    return [f"{rel}  costing:{key} -> {st}" for rel, key, st in inject(write=False) if st != "ok"]


# ── Self-check (regression guard — the canonical numbers, asserted) ──────────
EXPECTED = {                       # the figures the docs are reconciled to (this session)
    "muslin": 300,
    "lean":     {"chem": 801,  "total": 1100, "per_print": 22},  # 2026-07-17: chemistry tiers ×0.97944 (plane 9.62→9.42 m²)
    "standard": {"chem": 1189, "total": 1490, "per_print": 30},  # 2026-07-17: ×0.97944
    "rich":     {"chem": 2354, "total": 2650, "per_print": 53},  # 2026-07-17: ×0.97944
    "grand_total": (26199, 31883, 39438),  # 2026-07-22: retired duplicate image-plane-backing ACM (−$490/−$620). Per-change history in git log.
    "walkway": (2062, 2503, 2943),   # 2026-07-22: floor anchors → 410 SS self-drillers (−$18/−$34)   # 2026-07-21: M12 flat washer/split/plain-nut re-price +$27.  2026-07-21: M12 bracket/cleat bolts re-sized 80/cleat→65/70 (91280A728/732 partial, real flat) + 4 washers/bolt, fab line reconciled to parts −$30/−$58 → low +$53/high −$25.  §6a fab line matches walkway-report §10 ($742–$1,255 all-in)
    "water": (5424, 6690, 7949),  # updated 2026-07-22: parts-identity batch — spray-bar (jam nut/collar/self-tap/beam-clamp), tray silicone gasket, S60×6 adapter re-spec, M12×40 hanger bolt. Detail in git log.
    "container": (2300, 3300, 4300),
    "lightlock": (1437, 1768, 2101),   # 2026-07-22: parts-identity batch — wiper seal (Frost King BP17A), grab rail (16" marine SS), SS fasteners+isolation washers re-priced.  §6 = hinged-panel §8.2 (housing + drum) line items
    "swingpivot": (1180, 1395, 1610),   # 2026-07-22: journal bushings → igus iglide J JFM-9095-100 $130.53/ea (from GGB DU $211.25) −$162/pair.  §6b = hinged-panel §8.3 (swing pivot) + §8.4 (door frame)   # 2026-07-22: MB9060DU DU journal bushings firmed $211.25/ea (made-to-order, ~3-mo lead) — +$363/pair over the placeholder.  §6b = hinged-panel §8.3 (swing pivot) + §8.4 (door frame) line items
    "panel": (1130, 1403, 1676),       # 2026-07-22: EPDM gasket re-priced (OKAYASU rolls, −$60/−$74) + grab handle 316→304 (+$50/+$55).  §6c = hinged-panel §8.1 (panel structure)
    "shelf": (214, 227, 239),          # 2026-07-22: piano hinge re-priced (Würth 32×600 satin SS, $22–35).  §6d = chemistry-prep-shelves §7
    "interior": (467, 578, 698),      # 2026-07-22: retired the Image-plane flat-backing ACM line (double-counted the film dibond-acm-film)
    "optics": (110, 185, 265),
    "film": (6833, 7114, 7399),  # updated 2026-07-22: muslin clamp mechanism → off-the-shelf nylon spring clamps (×58) + HDPE filler; retired the custom bracket/spring/neoprene (−$189/−$531). Detail in git log.
    "ventilation": (757, 841, 924),   # §5b BOM (point estimates); report total was stale at $769
    "power": (2676, 2889, 3102),       # 2026-07-22: power-panel neoprene gasket re-priced (Pres-Bond $21–42) +$15/$36.  §5a authoritative subtotal
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
                       ("panel", PANEL), ("shelf", SHELF), ("interior", INTERIOR), ("optics", OPTICS), ("film", FILM),
                       ("ventilation", VENTILATION), ("power", POWER)):
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
    if "--check-registry" in argv:
        probs = check_registry()
        if probs:
            print("✗ section totals diverge from the parts registry (the source of record):")
            for p in probs:
                print("   -", p)
            return 1
        print("✓ every registry-backed section reconciles with parts.system_total")
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
