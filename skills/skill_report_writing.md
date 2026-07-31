<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
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

**Strip coordinates from prose and spec-table cells — describe location _qualitatively_.**
This was *the* most frequent editorial edit (2026-06-23, across electrical / ventilation /
walkway / film-plane / ibc / hinged-panel / processing-tray): deleting `X=`/`Yd=`/`Z=` mm
values from running text and table cells, leaving a feature-relative description. The
diagram (and its position tables) hold the numbers; the prose says *where* by reference to
a part the reader can see. If a feature name already locates it, the coordinate is noise.

- `Fan A … at the sealed end wall (X=5,893mm), below the X1 fill port (Yd=1,181mm, Z=2,000mm)`
  → `Fan A … at the sealed end wall, in the plumbing corridor below the X1 fill port`
- `Four brackets (at X≈1,156, X≈1,612, X≈2,070, X≈2,526mm) … ribs at 457mm centers`
  → `Four brackets in this zone … ribs`
- `2×2 stack in the right end zone (X=4,674–5,893mm)` → `2×2 stack in the right end zone`
- `the service loop hangs in the ceiling zone above Z=2,200mm` → `…hangs in the ceiling zone`

Keep a coordinate only when the coordinate *is* the thing being specified (a penetration's
drill position; the `equipment-layout §2` position tables). Qualitative anchors —
"by the pinhole wall", "at the IBC front", "near floor level", "the corridor edges",
"low / high" — are preferred over the numbers everywhere else.

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
`plumbing-report` for the pumps, `hinged-panel-report` for the seals). Detail
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
- **Never add a Chronology / Change-log / "design record" / "how we got here"
  section to a report body**, and don't narrate a switch (`Ruland → Belden (−$653)`,
  `was 304 SS`, dated entries). The reader wants to know what the design **is**, not
  its evolution. A report *is* the definitive record of the current design — that is
  exactly why it must not carry history. The paper trail lives in `RELEASE.md` and the
  `tbs_constants.py` rev-history, never the report. (This applies to the injected
  Parts-List too: a part `spec=` that flows into a report must describe the current
  part, not "replaced the old one at half the cost.")

**Archaeology is more than an Old column.** The 2026-06-23 pass stripped all of the
following from report bodies — each is the same smell, and each was a recurring hand-edit:

- **Rev tags and dates in headings and asides.** `Wall-Seat Saddles (rev 11 — replaces the
  brace cage; rev 12 combines…)` → `Wall-Seat Saddles`; `Note (Option A, 2026-06-06):` →
  `Note:`; `Quantities basis (rev 12):` → `Quantities:`. Drop `(Option A)` / `(rev N)`
  suffixes from headings entirely — the design has one name, the current one.
- **"former X → now Y" / "no longer required" framing.** `eliminated the former
  15–20-minute tray install step; now requires only the swing` → state only what it is now.
- **Before/after metrics.** `cut ~72 kg (movable 283 → 226 kg)`, `the earlier scheme
  stretched it ~40%` → delete; give the *current* weight/size, nothing it used to be.
- **"Adopted vs Residual / not-adopted option" trade sub-sections.** A living report carries
  the chosen design, not a catalogue of rejected options (`### 2.5 Weight-Reduction —
  Adopted + Residual` → `### 2.5 Weight-Reduction`). If the rationale is genuinely worth
  keeping, move it to a standalone **decision record** (see `right-walkway-cantilever-study`,
  reframed from a live "proposal" to an adopted decision record) — not the report body.
- **"mis-spec" / corrected-mistake notes.** `the AC Infinity S6 was a mis-spec: it's a
  320 mm inline fan` → just name the correct part.

Net effect: editorial passes are **subtractive**. The author's edits ran ~2:1 deletions to
insertions — leaner prose, current state only. Also cut redundant restatements at the
sentence level (a `6" (150mm) diameter` when `150×150×50mm` follows; a `Yd range (mm)`
table column the `Width` column already implies).

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
   location was wrong in 2 of ~6 places; `plumbing-report` was the tiebreaker.
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
