<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
<!-- Working/internal tracker — NOT registered in publish.sh (not published). -->
# Editorial Review TODO — voice & terseness pass (two-track)

**Purpose:** make the writing sound intentional, not generic/robotic, and **cut word count everywhere**.
People don't read. Two tracks, one mandate (be terse):

- **Track 1 — terse engineering (the default, almost everything).** Reports are dense with numbers that
  don't tell the reader *what a drawing is* or *why*. Lead with the point; say what the drawing is and why
  in one plain line; let the drawing carry the dimensions. Plain, authoritative, no hedging, no archaeology.
  **Goal: measurable word-count reduction** without losing a spec or a "why."
- **Track 2 — personal & engaging (Home + Proposal only).** Outward-facing, for audience-building /
  fundraising / the MFA proposal — must *sound like the author*: first person, candid, wry, concede-then-
  argue, long-setup→short-punch, everyday analogies for hard ideas, humor that drops away for the sincere
  moments. Still terse — personal ≠ flowery.

**Mechanism:** the house-style rules live in `skills/skill_report_writing.md` (§Voice). `python3
src/generators/style_lint.py` is an advisory checker (robotic tells + word-count/bloat, thresholds per
track) — it never rewrites engineering values. Run it per doc before ticking.

**How to use:** `[ ]` = not started · `[~]` = in progress · `[x]` = done. Put a one-line note after each
doc as it's reviewed (what was cut / what changed). Don't mark `[x]` unless told (per CLAUDE.md).

---

## Track 2 — Personal voice (Home + Proposal)

- [x] project-summary.md  *(Home — source synced → index.md by publish.sh)* — voiced to first person (concede-then-punch), front-board claim corrected (pinhole-point vs field-camera, no deprecated-tilt echo), width → "about 14ft", solar/battery + off-grid line added. 0 tells / 0 stiff.
- [x] funding-proposal.md  *(Proposal)*— already largely in-voice (§1/§4/§9 kept as the benchmark); defect fixes, width-drift → ~14ft, solar/battery aligned, '99 sq ft' injected, §2/§8 imperial via computed facts, artistic-vision extension (exposure → motion/ghosting), Construction link added.

---

## Track 1 — Terse engineering (everything else reader-facing)

### Costing
- [ ] project-cost-breakdown.md

### Construction — Equipment & Water
- [ ] equipment-layout-report.md
- [ ] water-system-report.md
- [ ] plumbing-report.md
- [ ] walkway-routing-sections.md
- [ ] ibc-stacking-report.md
- [ ] processing-tray-and-spray-bar.md

### Construction — Electrical & Ventilation
- [x] electrical-report.md  — confirmed complete (owner). §8 de-duplicated (hand-keyed parts table → filtered-BOM link + injected cost summary); inverter DC protection backfilled (§7.6 rule 4); weather/lightning pre-step + corner-casting earth note added; prose already terse.
- [x] electrical-safety-report.md  — confirmed complete (owner). §7.3 corner-casting earth note + §7.6 DC-protection rule (drove the inverter-DC-protection backfill); prose already terse.
- [ ] ventilation-report.md

### Construction — Film Plane & Pinhole
- [ ] pinhole-report.md
- [ ] film-plane-mechanism-report.md
- [ ] film-clamp-mechanism-report.md
- [ ] pinhole-disc-holder-report.md

### Construction — Misc & Sequence
- [x] walkway-report.md  — terseness pass (4,138 → ~3,700 words): fixed 3 broken sentences, collapsed duplicate bolt-"Attachment" + load-path paragraphs, dropped the "winged" label (unnecessary over self-tapping) + diagram-restated dims. Author editorial folded in.
- [ ] hinged-panel-report.md
- [ ] chemistry-prep-shelves.md
- [ ] construction-report.md
- [ ] plywood-cut-sheets.md

### Shopping
- [ ] master-shopping-list.md
- [ ] chemistry-shopping-list.md

### Transportation
- [ ] container-transport-options.md
- [ ] weight-distribution-report.md

### Operating
- [ ] operating-manual.md

### Research
- [ ] daily-energy-report.md
- [ ] container-report.md
- [ ] pinhole-optics-report.md
- [ ] pinhole-option-b-optics.md
- [ ] lens-vs-pinhole-exposure.md
- [ ] lens-options.md
- [ ] photosensitive-plane-options.md
- [ ] sensitizer-trials.md
- [ ] portrait-photography.md
- [ ] film-plane-mechanism-analysis.md
- [ ] light-trap-selection.md
- [ ] cost-analysis-report.md
- [ ] tray-research.md
- [ ] right-walkway-cantilever-study.md
- [ ] process-comparison.md

### Educational Program (TBS-002)
- [ ] mini-tbs/mini-tbs-poc.md
- [ ] mini-tbs/mini-tbs-shopping-list.md

---

## N/A — not voice targets (galleries, machine-generated, boilerplate)

These carry no reader prose to re-voice; skipped by design. Listed with checkboxes so the
`lint.py` "editorial-review list covers every published doc" check stays satisfied — leave
them unchecked (they are *skip*, not *to-do*).

- [ ] all-diagrams.md  *(N/A — diagram gallery, no prose)*
- [ ] engineering-diagrams.md  *(N/A — diagram gallery)*
- [ ] distortion-renders.md  *(N/A — image gallery)*
- [ ] component-dependency-map.md  *(N/A — injected machine doc)*
- [ ] component-dimension-audit.md  *(N/A — audit table)*
- [ ] licensing.md  *(N/A — license boilerplate)*

Non-published (no coverage entry needed): `index.md` *(generated from project-summary.md —
never edit directly)*; `skill_label_placement.md` *(skill reference)*; the trackers
`TODO.md`, `unused-imports-todo.md`, `editorial-review-todo.md`.

---

## Internal working docs — LEFT AS-IS (unpublished; out of scope for this pass)

Not on the site; not re-voiced. Listed for completeness only.

- audit-2026-07.md, drift-reduction-plan.md, model-aggregation-plan.md, spray-tray-redesign-plan.md
- fastener-standardization.md, sketchup-memory-investigation.md, grp-grating-quote.md
- film-plane-corner-rationale.md, film-plane-joint-research.md
- chem-shelf-blueprint-spec.md, fp-corner-blueprint-spec.md, ibc-frame-blueprint-spec.md, walkway-blueprint-spec.md
