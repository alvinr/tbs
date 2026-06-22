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
- [x] water-system-report.md  — *DONE (2026-06-21): owner of prints_per_resupply + blue_supply_l. The 8–10-vs-13 print confusion is resolved (now "9–11 on fresh Blue alone, ~14 with recycling"). Heavy values pass done via the 1,600→1,800L / 13→14-print design revision (§4 capacity table, water balance, max-fill, top-up, cooling overhead — all rebased). Converted the recurring canonical restatements (prints_per_resupply ×6, blue_supply_l ×3) to fact placeholders so this owner doc auto-cascades; §1 film-plane dims already fact-held. No drift in §5–12. Also fixed the §7 hose-routing paragraph (was the old pinhole-wall pump-manifold design → now the equipment-panel-in-corridor design, consistent with §4.4 + plumbing-panel-report; the matching stale spots in equipment-layout §2.2/§7 were corrected too) and §1 stacking-table typos. Remaining (separate Phase-1 track): the §9 parts-list cost total ($3,262–$4,881) is hand-maintained, not yet a costing.py block; the §5/§8 P&ID coordinates (sump X=2399, zone X-ranges, 4459×2200 tray) are intentionally kept as descriptive context.*
- [ ] ibc-stacking-report.md
- [x] equipment-layout-report.md  — *DONE (2026-06-21): single-sourced the headline geometry (film_plane_width_mm 4499 ×4, container_interior_length_mm 5893, film_plane_height_mm 2388, prints_per_resupply, blue_supply_l) as fact placeholders; §5 IBC-frame cost → generated costing block ($955–$1,455, was a stale $500–800); §10 max-swing drift 25.7°→28°. Reworked §8 into a two-state Camera-ready/Supply-exhausted water table with the 400L process-loss balance, max-fill capacity + on-site top-up (later cascaded to the 1,800L/14-print revision). §6.1 seal table slimmed to a pointer (hinged-panel §6); §10 reduced to a current-design summary (dropped the Old/colonnade column + 55-gal-drum archaeology). §2 coordinate position tables intentionally left as diagram-of-record detail.*
- [ ] plumbing-panel-report.md
- [ ] electrical-report.md
- [ ] electrical-safety-report.md
- [ ] daily-energy-report.md
- [ ] ventilation-report.md
- [ ] light-trap-selection.md
- [ ] hinged-panel-report.md
- [ ] walkway-report.md
- [ ] right-walkway-cantilever-study.md
- [x] processing-tray-and-spray-bar.md  — *DONE (2026-06-22): corrections — comma thousands-sep the linter can't see (4,459 / 2,229 / 2,340 / 101,972mm⁴), §3.6 numbering gap (3.6.5→3.6.4), unit tidy (liters→L); fixed the operating water weight (~233kg/117kg water → ~175kg/59kg — was ~2× the 6mm-flood volume). Cost reconciliation: §6 tray/spray subtotals + total → costing.py blocks; the WATER line items rebased to this dedicated report's detailed BOM (tray $1,177→$1,300–$2,015 — was undercounting shims/pickup/liner/hardware; spray $210→$235–$299), cascaded to project-cost-breakdown §5, scenarios, funding-proposal, master-shopping, cost-analysis. New SPRAY_BEAM_SPAN constant + injection-only facts (pinhole_x_mm, film_plane_left/right_x_mm, spray_beam_span_mm — no aliases; values collide with unrelated uses); 14 restatements wrapped. Downstream: slimmed water-system §8 (full) + master-shopping (kept supplier rows, fixed cost) tray/spray BOMs to point here. Engine fix: costing keys can span multiple docs + inject/check ALL occurrences (was first-only). Detail dims (Z-table coordinates, carriage/beam geometry) intentionally left as diagram-of-record.*
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

- [x] project-cost-breakdown.md  — *DONE (2026-06-20): fully single-sourced from costing.py — 10 section detail tables, the scenario summary, §7.1 chemistry, §7.3 process-comparison Cyanotype row (all-in = §7.1 + $3/print consumables), and the §11 budget scenarios A/B/C are all generated blocks (generating §11 fixed latent drifts). Prose engineering dims (4499×2388, 116 sq ft, 13 prints, 1,600L) are fact placeholders. Only genuine external estimates (CDL/truck/transport ranges) remain hand-kept.*
- [x] cost-analysis-report.md  — *DONE (2026-06-20): summarizes the Mid column, now generated from costing.py — §2 capital/recurring buckets (capital = grand Mid − §7/§8/§9) + §3 system ranking (sections × Mid + % of capital) are blocks; mid-total/capital/consumable/water-% inline. Generating fixed a stale "28%" water figure → 23%. Editorial savings-lever estimates left as prose. (Was missing from this list.)*
- [ ] master-shopping-list.md  — *ditto*
- [ ] chemistry-shopping-list.md  — *ditto*
- [ ] sensitizer-trials.md

## C. Summary / outward-facing

- [x] project-summary.md  — *DONE (2026-06-20): home page (= published index.md). All owned figures single-sourced — Scale table fully generated via fact placeholders + costing blocks (container/film dims, focal, pinhole, f#, image area, front-board, image-shift, film-plane, prints, per-print/50-run costs); soft values (exposure, recycling %, imperial, λ) left as prose. (Note: README.md is no longer a symlink to this — it's a standalone repo/build guide.)*
- [x] funding-proposal.md  — *DONE (2026-06-20): the restated figures are now single-sourced — cost numbers via costing.py inline blocks (L1 total, scenario span, per-print/tier/50-run, combined band) and engineering numbers via fact placeholders (front-board ±5.3°, film-plane ±40°/±28°, pinhole Ø2.17, film zone 4499×2388). Generated + gated, so they can't drift from their owners — the right model for a standalone pitch (funders won't click through to "referenced" figures).*

## D. Operating

- [x] operating-manual.md  — *DONE (2026-06-20): procedural doc, so most values stay as step guidance. (a) The §0.2/§0.3 chemistry tier tables now single-source the AmFe/ferricyanide masses from `costing.py` TIERS — AmFe per-print g + 50-print kg + ferri per-print g are generated `costing:om-*` blocks (generating reconciled lean ferri 87 g → 86 g); the Ware strengths (g/100 ml), water, and dichromate stay as recipe constants. (b) Trimmed the raw diagram coordinates an operator locates physically, not by measuring — pivot Ø89mm, duct X=1200mm, cooler X=1450–2050mm, walkway X=470/770/950, film-rail X=150mm. Kept operational values: angles (~56° swing, 30° solar, 5° level), the Ø200mm duct size they connect, 150mm clamp centers, spray-bar Yd positions, timings, temps.*

## E. Meta / index / skill (NOT report content — likely SKIP or treat separately)

- [ ] CLAUDE.md  — project instructions (not a report)
- [ ] component-dependency-map.md  — the map itself (becomes data in Phase 4)
- [ ] all-diagrams.md  — diagram gallery/index
- [x] engineering-diagrams.md  — *DONE (2026-06-21): index/overview page — SKIP for value substitution (carries no owned figures; all numbers live in the linked detail reports). Copy-edited prose typos and refreshed the system/area lists (solar sub-system, walkway in all three areas, ventilation path).*
- [ ] skill_label_placement.md  — drawing skill

## F. PoC (TBS-002)

- [ ] mini-tbs-poc.md  — *small-scale proof-of-concept design*
- [ ] mini-tbs-shopping-list.md  — *PoC procurement*

---

*Tip: when you clear a file, tick it and (optionally) note what moved out, so we can spot any number
that should become a `facts.yml` entry instead of being deleted outright.*
