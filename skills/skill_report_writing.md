---
name: report-writing
description: House style for the TBS-001 reports — what belongs in prose vs single-sourced vs the diagram, how to cite sources, terminology/spelling conventions, and the anti-patterns (duplication, old-vs-new archaeology, raw restated values) that cause narrative drift. Read before writing or editing any report `.md`.
metadata:
  type: reference
---

## Purpose

The reports (`*.md`) are the project's narrative layer. They drift in two ways:
**values** drift (the same number restated in many places, going stale
independently — see `skill_model_consistency.md` and the facts/costing tooling),
and **narrative** drifts (stale design descriptions, duplicated detail, old-vs-new
archaeology, inconsistent terminology). This skill governs the narrative. Apply it
whenever writing a new report or doing an "editorial" pass on an existing one.

**The governing principle:** *every sentence earns its place.* A report carries
**intent, rationale, and the headline figures** that define the system. Everything
else is a reference — to a single-source value, to a diagram-of-record, or to the
owning report. If a number or detail is maintained in two places, it is already
drifting.

---

## A. The triage — prose vs single-source vs diagram

Every figure in a report is one of three things. Decide which before you write it.

| Keep in prose | Single-source (placeholder/block) | Move to the diagram-of-record |
|---|---|---|
| Design intent, rationale, trade-offs, the "why" | Any value owned by `tbs_constants.py` / `costing.py` / `facts.yml` | Exact Z heights, X/Yd coordinates, part positions |
| Headline figures that *define* the system (focal length, f-number, image-plane size) | Restated geometry (film width, container length), prices, print counts, supply volumes | Bolt PCDs, hole patterns, fastener positions, clearances given as raw numbers |
| Sourced engineering claims (with hyperlinks) | Anything that recurs across docs and could disagree | Anything a reader would verify by *measuring the drawing*, not reading the text |
| Part numbers / specs / suppliers needed to procure | — | — |

When you'd otherwise write a repeated coordinate, write a pointer instead:
*"…at the sump (see [Floor Plan](…) sheet 2)."* The §2 position tables in
`equipment-layout-report.md` are the deliberate exception — they **are** a
diagram-of-record in table form, so their coordinates stay.

---

## B. Single-source every restated value — placeholder-*first*

If a value has an owner, **wrap it in a placeholder, don't type it raw** — even
though the alias-scan would catch a disagreement. Raw values are *policed* but not
*auto-updated*; placeholders are regenerated on every constant change.

- Engineering value → `facts.yml` fact placeholder `<!-- BEGIN fact:KEY -->…<!-- END fact:KEY -->`.
- Money → `costing.py` block `<!-- BEGIN costing:KEY -->…<!-- END costing:KEY -->`.
- See `facts.yml` header for the store-selection rule; never put a cost in `facts.yml`.

**Owner docs especially.** A report that is the registered `owner:` of a fact must
*generate* its own canonical statement, not restate it. Lesson (2026-06-21): the
1,600→1,800 L revision required hand-editing "14 prints"/"1,800 L" in a dozen raw
prose spots in `water-system-report.md` — the doc that *owns* those facts. Had they
been placeholders, the injector would have done it for free.

Leave **derived variants** as prose (e.g. "9–11 on fresh Blue alone", "~13 effective
prints", "~15–16 with max fill") — they aren't the canonical value, so policing them
would false-positive. Only the canonical figure gets a placeholder.

---

## C. One source-of-record — summaries point, they don't restate

The same *detailed* content must not be maintained in two reports. A summary
references the owner; it does not copy its table. We hit this three times in one
week, each fixed by slimming the copy to a pointer:

- the 5-row **light-seal table** duplicated in `equipment-layout §6.1.1` and
  `hinged-panel-report §6` → slimmed to a one-line summary + pointer;
- the **water capacity / max-fill / top-up** analysis duplicated in
  `equipment-layout §8` and `water-system §4` → moved to the owner, summary points;
- the **pump location** stated in `water-system §7`, `equipment-layout §2.2/§7/§9.2`
  → two were stale and contradicted the others.

Rule: pick the owning report for each subsystem (the dedicated one —
`equipment-panel-report` for the pumps, `hinged-panel-report` for the seals). Detail
lives there; every other mention is a sentence + a link.

---

## D. No "old vs new" archaeology in a living doc

Comparison tables that carry an **Old** column silently accumulate stale design
history — `55-gal drums`, `colonnade`, the old pinhole X, `Portacool Jetstream`. A
living report describes the **current** design only.

- Put history in a **changelog**, not the body (the `tbs_constants.py` header
  rev-history block is the pattern — keep it; it's the design's paper trail).
- `equipment-layout §10` is the model: it was reduced from an Old-vs-New table to a
  single current-design `Parameter | Value` summary.
- A `# (eliminated in rev N)` comment in a generator that still *describes* the
  removed geometry is the same smell — delete the description, keep at most a
  one-line "this zone is now X."

---

## E. Source citation

Every engineering claim links to a citable source — peer-reviewed paper,
manufacturer datasheet, standard, or textbook — and **the link is a hyperlink**:
`[Source Name](URL)`. No bare titles, catalog names, or standard numbers without a
URL. Reports end with a **Source References** section.

---

## F. Voice, structure, tables

- **Voice:** declarative, precise, present-tense ("The tray drains to a sump well"),
  no marketing register. State the fact, then the rationale.
- **Structure:** numbered `##` sections; a short Purpose/Executive Summary up top;
  Source References at the end. Match the section pattern of sibling reports.
- **Tables over paragraphs** for parameter lists; one row per item; bold the
  value, not the whole row. A two-state table ("Camera ready / Supply exhausted")
  beats an ambiguous single "Capacity" column.
- **Don't restate a number the table already shows** in the prose beneath it.
- **Consolidate redundant rows** (the §10 waste handling: two rows → one).
- Fix the small stuff: typos, stray spaces, double words, em-dash vs hyphen.

---

## G. Terminology, units, spelling

- **American English throughout:** center, color, aluminum, analyze, fiber,
  meter, liter (not centre/colour/aluminium/analyse/fibre/metre/litre).
- **Canonical component IDs** — use the exact ID from `tbs_constants.py` / the
  owning report, never a synonym: pumps `P-01…P-05`; totes `IBC-1…IBC-4`; bulkhead
  ports `X1/X3/X4`; valves `BV-…`, `3W-DV-…`, `V1`; filters `F-1…F-3`; circuits
  **Blue / Brown / Black**; parts `ICP-XX`; camera `TBS-001`.
- **Consistent units:** mm for geometry, L/gal paired where useful (state both once,
  then pick one), `±N°` for angles. **Thousands separators on every 4+ digit quantity:**
  a number that carries a unit or `$` gets a comma — `4,499mm`, `X=2,399`, `1,800 L`,
  `$1,800`, `24,000 kg`. Bare product/model numbers, years, and f-numbers do **not**
  (`Shurflo 2088`, `MX 1000`, `2026`, `f/1088`). Enforced by `editorial_lint.py` (advisory).
  **This is a prose convention only — engineering diagrams keep mm labels comma-free**
  (standard drafting practice), so a doc reads `4,499mm` while its diagram-of-record reads
  `4499mm`. That difference is by design, not drift; `editorial_lint` scans docs only.
- **Watch the overloaded number.** "600 L" has meant a fill level *and* a tote size
  *and* a collection volume — disambiguate ("600 L is a **fill level**, not a tote
  size; all four totes are identical 1000 L vessels"). Same for `2362` (focal length
  = container width = egress width) and `2388` (film height = container height) —
  these are injection-only facts precisely because they're ambiguous.

---

## H. The editorial-pass workflow

1. **Verify before rewriting.** When a value looks stale, check the *subsystem's
   dedicated report* (the authoritative source) before changing it — the pump
   location was wrong in 2 of ~6 places; `equipment-panel-report` was the tiebreaker.
2. **Triage** every figure with §A; **single-source** per §B; **de-duplicate** per
   §C; **strip archaeology** per §D.
3. **Run the tooling:** `facts.py --inject`, `lint.py` (placeholders + alias
   agreement must pass), and `check_consistency.py` for stale literals.
4. **Don't mark the editorial item done** — leave the `editorial-review-todo.md`
   checkbox alone unless the user explicitly says to tick it (status is theirs).

---

## Future enforcement (planned validator — not yet built)

The mechanical subset of this skill is intended to become commit-time lint checks,
with the **unambiguous ones as blocking gates** and the judgment-y ones advisory:

- **gate:** American-spelling violations; bare source references missing a hyperlink.
- **advisory:** banned stale terms (`55-gal`, `colonnade`, `Portacool Jetstream`,
  retired constant values); a value the alias registry recognizes but which sits raw
  outside a placeholder block ("should be a placeholder"); thousands-separator
  inconsistency; a published report missing its Source References section.

Until that exists, this skill is enforced by reading it before each editorial pass.
