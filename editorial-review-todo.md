<!-- Working/internal tracker — NOT registered in publish.sh (not published). -->
# Editorial Review TODO — remove diagram-encapsulated detail from the reports

**Purpose:** the reports repeat dimensional detail that the **diagrams already carry** (Z-positions,
mm coordinates, bolt PCDs, exact placements). Repeated data is data that can drift. Systematically
review each `.md` and move that detail to the diagram-of-record, keeping the prose about intent.

**Remove from prose** (the diagram is the source of record):
- Exact Z heights / mm coordinates / X-positions of parts
- Bolt PCDs, hole patterns, fastener positions, clearances given as raw numbers
- Anything a reader would verify by *measuring the drawing*, not reading the text

**Keep in prose:**
- Design intent, rationale, trade-offs, the "why"
- Sourced engineering claims (with their hyperlinks)
- Part numbers / specs / suppliers needed for procurement
- Headline figures that define the system (focal length, f-number, image-plane size)

**How:** replace a repeated coordinate with a pointer — "see [<diagram>] (sheet N)". When a number is
also a `tbs_constants` value or a `costing.py`/`facts.yml` fact, prefer the reference so it can be linted.

---

## A. Engineering reports (primary targets — most likely to repeat dimensions)

- [ ] container-report.md
- [ ] pinhole-report.md
- [ ] pinhole-camera-construction.md
- [ ] pinhole-optics-report.md
- [ ] pinhole-option-b-optics.md
- [ ] film-plane-mechanism-report.md  — *heavy mm/angle detail; cross-check vs the FPM sheets*
- [ ] film-plane-mechanism-analysis.md  — *superseded doc; flagged out-of-date at top — decide retire vs trim*
- [ ] film-clamp-mechanism-report.md  — *had hardcoded ±tilt/swing; verify it now references constants*
- [ ] tilt-swing-board-report.md
- [ ] tilt-swing-board-analysis.md
- [ ] water-system-report.md  — *8–10 vs 13 prints assumption now clarified; check other repeated figures*
- [ ] ibc-stacking-report.md
- [ ] equipment-layout-report.md  — *had a 42°/clearance Z that the tray diagram carries*
- [ ] equipment-panel-report.md
- [ ] electrical-report.md
- [ ] electrical-safety-report.md
- [ ] daily-energy-report.md
- [ ] ventilation-report.md
- [ ] light-trap-selection.md
- [ ] hinged-panel-report.md
- [ ] walkway-report.md
- [ ] right-walkway-cantilever-study.md
- [ ] processing-tray-and-spray-bar.md
- [ ] chemistry-prep-shelves.md
- [ ] weight-distribution-report.md
- [ ] container-transport-options.md
- [ ] lens-options.md
- [ ] lens-vs-pinhole-exposure.md
- [ ] photosensitive-plane-options.md
- [ ] complete-distortion-renders.md  — *prose ±angles now corrected to Option A; check for stray dims*
- [ ] component-dimension-audit.md  — *this one is intentionally dimensional — likely keep as-is*
- [ ] licensing.md

## B. Cost & shopping (numbers move to costing.py — Phase 1; prose editorial still applies)

- [ ] project-cost-breakdown.md  — *tables to be generated from costing.py; trim prose dims*
- [ ] master-shopping-list.md  — *ditto*
- [ ] chemistry-shopping-list.md  — *ditto*
- [ ] sensitizer-trials.md

## C. Summary / outward-facing

- [ ] project-summary.md  (= README.md, symlink — edit project-summary.md only)
- [x] funding-proposal.md  — *DONE (2026-06-20): the restated figures are now single-sourced — cost numbers via costing.py inline blocks (L1 total, scenario span, per-print/tier/50-run, combined band) and engineering numbers via fact placeholders (front-board ±5.3°, film-plane ±40°/±28°, pinhole Ø2.17, film zone 4499×2388). Generated + gated, so they can't drift from their owners — the right model for a standalone pitch (funders won't click through to "referenced" figures).*

## D. Operating

- [ ] operating-manual.md  — *procedural; keep step values, trim restated geometry*

## E. Meta / index / skill (NOT report content — likely SKIP or treat separately)

- [ ] CLAUDE.md  — project instructions (not a report)
- [ ] component-dependency-map.md  — the map itself (becomes data in Phase 4)
- [ ] all-diagrams.md  — diagram gallery/index
- [ ] engineering-diagrams.md  — diagram index
- [ ] skill_label_placement.md  — drawing skill

---

*Tip: when you clear a file, tick it and (optionally) note what moved out, so we can spot any number
that should become a `facts.yml` entry instead of being deleted outright.*
