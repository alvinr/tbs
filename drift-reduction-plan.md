<!-- Working/internal plan — NOT registered in publish.sh (not published). -->
# Drift-Reduction Plan — single source of truth + commit-time linting

**Goal:** stop document-side drift (transcription / derivation / partial-cascade / duplication)
by (1) **computing** numbers from one source instead of transcribing them, (2) referencing a
**single fact source** in prose, and (3) catching the rest with a **pre-commit linter** that we
refine over time (the way the labeling rules grew). The user should stop having to read for drift —
the machine finds it at commit time.

**Root cause (from the session retro):** the code side (`tbs_constants.py` → generators → 2D/3D)
is single-sourced and *computed*; the document side (reports, shopping lists, cost breakdown,
proposal) is hand-*transcribed*, with hand-summed totals and the same fact restated in 5–8 docs.
All the drift we reconciled lived on the document side. `check_consistency.py` only catches the
*old value of a constant that changed* — blind to numbers that were never constants, to table
arithmetic, and to cross-doc disagreement. Those blind spots are exactly where the drift is.

---

## The three value stores — where a number lives, and why (read before adding a number anywhere)

Having more than one place to put a value is how drift starts. We have **three** stores, separated
by *who consumes the value* — and the rule below keeps each value to exactly one home so they can't
disagree:

| Store | Holds | Consumed by |
|-------|-------|-------------|
| `tbs_constants.py` | geometry & engineering values | code that computes/draws/builds — generators, 3D models, weight/cost scripts |
| `costing.py` | money line items + summed totals | code that sums them into the doc cost tables |
| `facts.yml` | a *registry* of numbers restated in prose + the regex to find them | `lint.py`, to police English across the `.md` docs |

The first two are **machine inputs** (code does arithmetic on them). `facts.yml` is different: it is
**not where a value is used** — it is where the linter learns "this number is repeated in sentences,
here's how to spot it, here's what it must equal."

**Decision rule — does code compute / draw / build with the number?**
- yes, geometry/engineering → `tbs_constants.py`
- yes, it's money → `costing.py`
- no, it only appears in prose but is restated across docs and you want it policed → `facts.yml`:
  - it **is** also a code value → `constant:` **reference** (no copy — reads from `tbs_constants`)
  - it lives **nowhere** in code → `value:` literal — the *only* case facts.yml is itself a source,
    and even then prefer making it a **computed constant first** (see `PRINTS_PER_RESUPPLY`:
    derived in `tbs_constants` from Blue supply ÷ Blue-per-print, then *referenced*), so facts.yml
    stays 100% reference-only.

**Guardrails that keep facts.yml from becoming a 2nd drift vector:**
1. Default to `constant:`. A literal `value:` is a last resort (no code home) — and a candidate to
   convert into a computed constant.
2. Never put a cost in facts.yml — costs live in `costing.py`.
3. `tbs_constants` never imports from `facts` — the dependency points one way (facts → constants),
   so constants stay the root.

---

## Status (2026-06-19) — infrastructure built across all four phases

| Phase | Built | Remaining |
|-------|-------|-----------|
| **1 costing.py** | Printmaking tiers + scenario table + **computed grand total**; **7 sections line-item-owned** (§1,2,3,5,6,6a,6b) + §7 from tiers; `--check` gate | the 5 below; 3-view emitters (master / funding); replace hand-typed tables with generated blocks |

**Cost line-item migration — remaining 5 sections (not all the same):**
- **§4 Film plane** — ✅ **DONE**: folded into the `FILM` line-item list (13 items; clamps carry the documented $276/$506/$736 Low/Mid/High, saddle plate a modest band, rest `point()`). The hand-set summary ($3,100/$3,650/$4,200) sat *below* the section's own BOM — folding it in set §4 = **$3,538/$3,813/$4,088** (+$438/+$163/−$112 to the grand total) and added the `costing:film` gated block. Cascaded into the §11 scenarios, master §4 subtotal, funding Level 1, and the cost-analysis ranking + capital/consumable buckets.
- **§5a Power / §5b Ventilation** — no cost-breakdown detail sub-table; the line items live in `electrical-report.md` / `ventilation-report.md` (the ventilation arithmetic finding is there too). Migratable by sourcing from those reports.
- **§8 Transport / §9 Licences** — option/scenario **estimate ranges**, not line-item sums (8.1/8.2/8.3 are *alternatives*). These appropriately stay as direct section values; don't force line-item migration.
| **2 facts.py** | Dep-free registry (film-plane angles read from constants, prints/resupply) + agreement scan | more facts; `<!-- fact:x -->` injector; one-owner-per-fact prose pass |
| **3 linter** | `lint.py` two-tier + **pre-commit hook** (`.githooks/`); 1 gate (costing) + 3 warnings (facts, arithmetic, cascade) | graduate facts→gate; prose-vs-constant; more rules |
| **4 dependency** | **missing-cascade** check (staged constant change w/ no regenerated output → flags consumers) | hardwired-literal scan; duplication-equality checks; formal `dependencies` data |

**The linter immediately caught 7 real internal inconsistencies (triage list — total ≠ its line items):**
- [ ] `project-cost-breakdown.md:265` water-system total **$4,128 / $6,201** vs line-item sums **$4,063 / $6,104**
- [ ] `project-cost-breakdown.md:316` walkway total **$1,801 / $2,186 / $2,572** vs sums **$1,826 / $2,214 / $2,607**
- [ ] `ventilation-report.md:209` total **$769** vs sum **$824**
- [ ] `weight-distribution-report.md:91` dry total **3,324 kg** vs sum **3,250 kg**

(Each needs a human call on which figure is authoritative — left for the editorial/review pass.)

---

## Phase 1 — `costing.py` (STARTED)

A Python module that **owns the cost line items** and **generates** the cost tables; a self-check
asserts the figures are internally consistent. Totals can no longer drift from their components
because they are computed.

- **Created:** `src/generators/costing.py` — Printmaking / cyanotype vertical slice (the most-drifted
  section). Owns the Ware tiers + unit prices + muslin; computes chem subtotals, section totals,
  per-print, the Low/Mid/High scenario row; emits the `project-cost-breakdown.md §7.1` table; `check()`
  is a regression guard. *It already surfaced a $1 published rounding inconsistency (Lean ferricyanide).*
- **Next (this phase, section by section):**
  1. Extend the data model to every cost section (container, interior, optics, film plane, water,
     power, ventilation, light lock, walkway, swing pivot, transport, permits) — each line item with
     `label / qty / unit_price(low,mid,high) / supplier / source-url / section`.
  2. Add emitters for the **three views** of the same line items: cost-breakdown (Low/Mid/High),
     master-shopping-list (Low/High + section totals + grand total), funding-proposal (Level 1 Mid +
     range). One source, three generated tables → they cannot disagree.
  3. Replace the hand-maintained tables in those `.md` files with the generated output (a
     `<!-- BEGIN costing:section -->…<!-- END -->` block the generator fills, like the diagram pattern).
  4. `costing.py --check` re-sums every table and asserts cross-doc agreement.

**Done when:** every cost total in every doc is generated from `costing.py`, and `--check` is clean.

## Phase 2 — `facts.yml` (single source of truth for MD numbers)

A YAML registry of the **cross-referenced non-cost numbers** that are currently restated across docs
(prints/resupply, film-plane angles, image-plane dims, exposure, focal length, pinhole Ø, water
capacities, battery/solar, etc.). Each entry: `value`, `unit`, `derivation`, `owner-doc`, `aliases`.

- Where a number is already a code constant (`MAX_TILT_DEG`, etc.), `facts.yml` **references the
  constant** rather than duplicating it — one value, surfaced to the MD layer. `facts.yml` is now
  **100% reference-only** (no literals): `prints_per_resupply` was the last literal and is now a
  **computed** constant (`PRINTS_PER_RESUPPLY` = Blue supply ÷ Blue-per-print over the real tray
  footprint) that the fact references — so even an operational number derives from first principles.
- A tiny injector fills `<!-- fact:name -->` placeholders in prose, OR (lighter first step) the linter
  just **scans every doc for any registered fact's aliases and flags a stale value**.
- **Canonical owner per fact:** one doc derives it; the others say "see <owner>" and do not restate the
  number (reduces N copies to 1 + N pointers — kills transcription drift at the source).

## Phase 3 — Pre-commit linter (refined over time, like the labeling rules)

Grow `check_consistency.py` into a real linter wired to a **git pre-commit hook**, adding the checks
that map to our blind spots. Start small, add a rule each time we hit a new drift class:

1. **Arithmetic** — re-sum every markdown table that declares a total; fail on mismatch.
2. **Costing reconciliation** — run `costing.py --check`; assert the docs match the generated figures.
3. **Facts-registry agreement** — any registered fact must read the same value everywhere it appears.
4. **Prose-vs-constant** — a number tagged to a `tbs_constants` value must equal it (catches the
   `±42°`-hardcoded-in-prose class).
5. **Run as a gate**, not on demand — drift is rejected at commit, not found by reading.

## Phase 4 — Dependency-as-data (2D↔3D, the user's other drift source)

2D/3D drift happens when a change isn't cascaded — a **missing dependency** or a **hardwired value
instead of a constant**. Encode the machine-readable core of `component-dependency-map.md` (§4) as a
data structure (`dependencies.yml`: `constant → {generators, models, docs}`) the linter consumes, so:

- **Missing-cascade check:** if a `tbs_constants` value changed in a commit, assert every file that
  depends on it was also touched (or its output regenerated).
- **Hardwired-literal check:** flag numeric literals in generators/models that match a constant's value
  but aren't imported from `tbs_constants` (the "should have been a constant" class).
- **Duplication check:** for the known duplicated geometry (`power_core()` ↔ `ov.electrical()`, walkway
  brackets), assert the two emit identical geometry for the shared part — replaces the "NB: keep in
  sync" comments with enforcement.

---

## Working principles to adopt (the practice change)

- **Compute, don't transcribe.** A derived value (total, per-print, scenario) is never hand-typed.
- **One canonical owner per fact.** Others reference it; they do not restate the number.
- **No "provisional / not yet re-summed" states.** Either fully cascade, or make the value computed so
  there is nothing to defer (deferring plants a landmine the user later has to find).
- **Definition of done for a spec change:** canonical value changed in *one* place → all derived values
  recompute → the linter passes clean. Not "the main doc is updated, I'll flag the rest."
- **Editorial:** keep prose; move repeated dimensional detail (Z positions, measurements that the
  diagrams already carry) out of the reports (see `editorial-review-todo.md`) — less restated data is
  less to drift.

## Sequence

Phase 1 (costing.py) → Phase 3 wiring (so costing is gated) → Phase 2 (facts.yml) → Phase 4
(dependency-as-data). Editorial review runs in parallel, user-led.
