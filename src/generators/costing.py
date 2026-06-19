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
    Section("1",  "Container purchase & delivery",              2300, 3150, 4300),
    Section("2",  "Interior conversion",                         970, 1140, 1310),
    Section("3",  "Optics — pinhole plate",                       80,  150,  280),
    Section("4",  "Film plane mechanism (4-corner Option A)",   3100, 3650, 4200),
    Section("5",  "Processing water system",                    4143, 5180, 6216),
    Section("5a", "Power & electrical system",                  2025, 2265, 2575),
    Section("5b", "Ventilation & cooling system",                770,  830,  920),
    Section("6",  "Housed revolving-door light lock",           1465, 1802, 2160),
    Section("6a", "Perimeter walkway",                          1801, 2186, 2572),
    Section("6b", "Panel swing pivot",                           650,  770,  910),
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
    "grand_total": (19034, 24313, 32043),
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
    print("\n# Executive Cost Summary — whole build (generated by costing.py)\n")
    print(emit_scenario_table())
    print("\nSelf-check:", "✓ passed" if not errs else "✗ FAILED -> " + "; ".join(errs))
    return 1 if errs else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
