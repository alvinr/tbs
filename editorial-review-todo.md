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
- [x] pinhole-report.md  — *DONE (2026-06-23): clean to start (header/footer, editorial_lint, all sources hyperlinked, no costs). Single-sourced the two Key Optical Constants that were restated raw and un-policed (the tight facts.yml aliases didn't reach these phrasings): Ø2.17mm pinhole aperture ×4 → pinhole_diameter_mm; f=2,362mm focal length → focal_length_mm. Rest is detail dims (bore sizes, bolt patterns, dowel/seal/fit geometry) — left as diagram-of-record.*
- [ ] pinhole-camera-construction.md
- [ ] pinhole-optics-report.md
- [ ] pinhole-option-b-optics.md
- [x] film-plane-mechanism-report.md  — *DONE (2026-06-23): single-sourced the system-defining geometry that was restated raw — §2 reference table (length 5,893 → container_interior_length_mm, width 2,362 → focal_length_mm, height 2,388 → film_plane_height_mm), §3 single-axis maxima (40°/28° → film_plane_max_tilt/swing) + 4,499 width, §4 plane size 4,499×2,388 (×2). §7 materials total wired to costing.py (costing:film-total = FILM low \$3,538; was a stale hand-set \$3,100 that sat below its own BOM). Config-table corner depths, per-corner angles, rail X coordinates + per-item BoM prices left as diagram-of-record. (Author also trimmed prose: rail coords in §1, the 'earlier stretching scheme' archaeology in §3, the Option-A date note in §4.)*
- [ ] film-plane-mechanism-analysis.md  — *superseded doc; flagged out-of-date at top — decide retire vs trim*
- [x] film-clamp-mechanism-report.md  — *DONE (2026-06-23): the ±tilt/swing now reference film_plane_max_tilt/swing facts (§1 + §5). Single-sourced the §2 film-plane dims (4,499×2,388 + per-edge lengths ×6 → film_plane_width/height) and wired the §4 clamp-system cost to costing.py (costing:clamp-system-low/high = FILM clamp line $276/$736 + mounting $70 = $346–$806; was a hand-set $330–$790). Added the §1 angle-frame gloss (2"×2"×3/16" L-angle, names the legs). Clamp counts verified (30+30+16+16=92; perimeter 13,774/150≈92). Detail dims (force, neoprene, hem, spacing) + per-item BoM prices left as spec/diagram-of-record.*
- [ ] tilt-swing-board-report.md
- [ ] tilt-swing-board-analysis.md
- [x] water-system-report.md  — *DONE (2026-06-21): owner of prints_per_resupply + blue_supply_l. The 8–10-vs-13 print confusion is resolved (now "9–11 on fresh Blue alone, ~14 with recycling"). Heavy values pass done via the 1,600→1,800L / 13→14-print design revision (§4 capacity table, water balance, max-fill, top-up, cooling overhead — all rebased). Converted the recurring canonical restatements (prints_per_resupply ×6, blue_supply_l ×3) to fact placeholders so this owner doc auto-cascades; §1 film-plane dims already fact-held. No drift in §5–12. Also fixed the §7 hose-routing paragraph (was the old pinhole-wall pump-manifold design → now the equipment-panel-in-corridor design, consistent with §4.4 + plumbing-panel-report; the matching stale spots in equipment-layout §2.2/§7 were corrected too) and §1 stacking-table typos. Remaining (separate Phase-1 track): the §9 parts-list cost total ($3,262–$4,881) is hand-maintained, not yet a costing.py block; the §5/§8 P&ID coordinates (sump X=2399, zone X-ranges, 4459×2200 tray) are intentionally kept as descriptive context.*
- [ ] ibc-stacking-report.md
- [x] equipment-layout-report.md  — *DONE (2026-06-21): single-sourced the headline geometry (film_plane_width_mm 4499 ×4, container_interior_length_mm 5893, film_plane_height_mm 2388, prints_per_resupply, blue_supply_l) as fact placeholders; §5 IBC-frame cost → generated costing block ($955–$1,455, was a stale $500–800); §10 max-swing drift 25.7°→28°. Reworked §8 into a two-state Camera-ready/Supply-exhausted water table with the 400L process-loss balance, max-fill capacity + on-site top-up (later cascaded to the 1,800L/14-print revision). §6.1 seal table slimmed to a pointer (hinged-panel §6); §10 reduced to a current-design summary (dropped the Old/colonnade column + 55-gal-drum archaeology). §2 coordinate position tables intentionally left as diagram-of-record detail.*
- [ ] plumbing-panel-report.md
- [x] electrical-report.md  — *DONE (2026-06-22): corrected energy-script drift (sessions/charge 1.6→1.5, solar sessions/day 4.5→4.2, 2-pack 3.3→3.1, cloudy-day reserve 1.2→1.1 — §3.1/§3.2 had been hand-copied from `calculate_energy_budget.py` and gone stale). Substitutions: blue_supply_l + prints_per_resupply ×2 as fact placeholders. Built an energy block-injector (`calculate_energy_budget.py --inject/--check-blocks` + new lint gate) — 14 `energy:KEY` figures now injected into §3.1/§3.2 so they can't drift again. §8 cost totals → costing blocks (elec-system/canopy/cooling/grand-total; canopy/cooling derived from the §5b VENTILATION BOM). Thousands-sep: '1300 CFM'→'1,300 CFM' across 5 docs + CFM added to editorial_lint's unit list + evap alias made comma-tolerant. Relocated the energy-injection workflow note to README (codebase-management ≠ camera spec); trimmed the matching tooling notes from §3.2 + daily-energy §1/§4/§9. Detail dims (circuit run lengths, Z heights, panel coordinates) intentionally left as descriptive context. Provenance citations to internal generators (other docs) left for their own passes.*
- [x] electrical-safety-report.md  — *DONE (2026-06-23): added the missing SPDX header + AGPLv3 footer. Reconciled the **Circuit-E 120V AC** gap the report omitted — §1 (two AC interfaces), §2 ("one exception" caveat to the 12V-ELV thesis), §3 baseline, §4 Hazard #6, §6 rule, §7 commissioning. One-source-of-record: §5 collapsed from duplicated control-spec tables to a gap→control→spec-pointer map (specs owned by electrical §7.5/§7.6). Then carried the **D1–D5 design changes** in: §5 control map (two E-stops, PV disconnect, charge-line fuse, per-pack MRBF, thermal siting) + §4 reworked to "Residual gap → closed by" with the PV/charge-side gap surfaced. Mechanically clean (editorial_lint).*
- [x] daily-energy-report.md  — *DONE (2026-06-23): added the missing SPDX header + AGPLv3 footer; substituted prints_per_resupply ×3 as fact placeholders; relabeled the ~771 Wh figure as per-SESSION (it clashed with §3's 663 Wh per-print); fixed the 2-pack no-sun reserve 1.2→1.1 day and the 'Black tote is 600 L' → 'fills to ~600 L (1,000 L tote at working fill)'. Single-sourced 17 computed figures via the energy block-injector (extended `_ENERGY_DOCS` + 4 new keys), so daily-energy can't drift from `calculate_energy_budget.py`. **Conceptual fix:** the Brown/Waste pump-out is a per-RESUPPLY dump run (~14 prints / ~4.7 days), not end-of-day — corrected `compute_daily()` to exclude it (daily totals 1,434/2,097/2,760), renamed the model fn, reframed §6 ('Resupply … per dump run, not daily'), dropped the §4 daily drain line, fixed §1 intro, and cascaded to electrical §3.1; trimmed the §7.4 old-80W/220→400 archaeology. Moved under the Operating Manual nav section. Detail dims (P&ID pump table, Z-coordinates) left as descriptive context.*
- [x] ventilation-report.md  — *DONE (2026-06-23): reconciled drifted summary costs (§3 shade $300→$200, §4 fans $60→$50) and single-sourced them + the §9 parts-list total ($824) as costing.py §5b blocks (new vent-total/vent-fans/vent-shade/vent-cooler-inverter keys); dropped the 'fictional Portacool Jetstream' archaeology. New EVAP_CFM_RATED constant + cooler_cfm_rated fact (injection-only) wraps the three 1,300 CFM restatements. Fixed the §7 air-change error: the two fans run in series so the exchange is the ~200 CFM through-flow (not 2×200=400), giving ~14 ACH (was a non-computing 16); folded in the cooler's ~300 CFM of 100% outside air (~30+ ACH running) and cited the darkroom minimum (Kodak ≥10 ACH / 170 CFM, §11 ref 8). Detail dims left as diagram/spec context.*
- [ ] light-trap-selection.md
- [ ] process-comparison.md  — *NEW (2026-06-24): alt-process cost comparison (gum / Van Dyke / salt / Ilford / Liquid Light) extracted from chemistry-shopping-list.md during the parts-registry chemistry fold-in (2d); not yet editorially reviewed*
- [x] hinged-panel-report.md  — *DONE (2026-06-23): single-sourced the transport swing ~56° ×9 via a new panel_swing_deg fact (= SWING_LOCK_DEG); panel outer dims 2,362×2,388 + far-corner Yd → container_width_mm/container_height_mm. Major cost reconciliation (audit): the panel STRUCTURE (§8.1) had NO costing.py home — added §6c PANEL ($1,124/$1,408/$1,691), rebuilt §6 LIGHTLOCK (=§8.2, $1,385/$1,728/$2,070) and §6b SWINGPIVOT (=§8.3+§8.4, $855/$1,143/$1,430) from the report line items; wired the four §8.1–8.4 subtotals + §8.5 rows/total to costing blocks (split §6b via helpers). Fixed the report's internal staleness (§8.1 $1,005→$1,124, §8.3 $560→$520, §8.5 total $3,190→$3,364). Grand total $25,620→$26,865 (mid) — the missing panel. Cascaded to project-cost-breakdown (regen'd §6/§6b detail tables), cost-analysis, funding-proposal, master-shopping. Detail dims (Z/Yd coords, seal geometry) left as diagram-of-record.*
- [x] walkway-report.md  — *DONE (2026-06-23): resolved a three-way §10 cost mismatch (audit) — kept costing.py's split structure but pushed the report's authoritative all-in bracket figures ($742–$1,255) in by raising the §6a Fabrication line (280/360/440→454/634/808); WALKWAY $1,826/$2,214/$2,607→$2,000/$2,488/$2,975, grand total cascaded. §10 fixes: dropped the evap-stowage rows (costed in Ventilation, cross-ref'd), added the drum-exit GRP row, wired the total to costing:walkway-total-low/high. Single-sourced the §2 open-area span (spray_beam_span_mm) and the container coordinates from real facts — new container_width_mm fact (= C_WID, so structural width stops borrowing focal_length_mm) for the 2,362 width refs, 5,893→container_interior_length_mm, 4,649→film_plane_right_x_mm. (Swept container_width_mm/focal_length_mm into 5 more docs as follow-up.) Detail coords + per-item BoM prices left as diagram-of-record.*
- [x] right-walkway-cantilever-study.md  — *DONE (2026-06-23): was stale (framed 'not yet adopted, baseline ceiling-hung', but the cantilever was adopted in rev12 — Walkway §4 is the as-built 'Cantilever Rectangle'). Reframed to an ADOPTED decision record: status → adopted pointing to Walkway §4 (as-built refined the study into a closed rectangle); §1 past-tensed, §3 'Proposed'→'The design'+as-built note, §6 'current/proposed'→'former/adopted', §7 'if approved'→'Implementation (rev12 complete)'. Added See Also (clears no-source-refs flag) + AGPLv3 footer. Moved nav Construction→Misc → Research.*
- [x] processing-tray-and-spray-bar.md  — *DONE (2026-06-22): corrections — comma thousands-sep the linter can't see (4,459 / 2,229 / 2,340 / 101,972mm⁴), §3.6 numbering gap (3.6.5→3.6.4), unit tidy (liters→L); fixed the operating water weight (~233kg/117kg water → ~175kg/59kg — was ~2× the 6mm-flood volume). Cost reconciliation: §6 tray/spray subtotals + total → costing.py blocks; the WATER line items rebased to this dedicated report's detailed BOM (tray $1,177→$1,300–$2,015 — was undercounting shims/pickup/liner/hardware; spray $210→$235–$299), cascaded to project-cost-breakdown §5, scenarios, funding-proposal, master-shopping, cost-analysis. New SPRAY_BEAM_SPAN constant + injection-only facts (pinhole_x_mm, film_plane_left/right_x_mm, spray_beam_span_mm — no aliases; values collide with unrelated uses); 14 restatements wrapped. Downstream: slimmed water-system §8 (full) + master-shopping (kept supplier rows, fixed cost) tray/spray BOMs to point here. Engine fix: costing keys can span multiple docs + inject/check ALL occurrences (was first-only). Detail dims (Z-table coordinates, carriage/beam geometry) intentionally left as diagram-of-record.*
- [x] chemistry-prep-shelves.md  — *DONE (2026-06-23): applied the refined skill IN the pre-pass — stripped X/Yd/Z coordinates from §1/§2/§2.1/§5 narrative (kept §2.2 spatial-constraints table, spec tables, optical-cone proof, assembly steps), dropped the §1 "previous ceiling-hung shelf" archaeology. Wired the §7 cost (~$203) into costing.py as the new §6d SHELF section — it had no costing home, so the grand total was omitting it; cascaded to all cost docs (grand total +$203).*
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
- [x] all-diagrams.md  — *DONE (2026-06-23): audited the gallery against every generated `diagrams/*.png` — 3 sheets were referenced nowhere (electrical-sheet4 Pump Power/Circuit C + sheet5 Main Enclosure Panel Layout; hingepanel-sheet6 Interior Pull Handle), all added in sheet order. No broken refs. Added a standing rule (every new diagram PNG → all-diagrams.md, incl. new sheets on existing generators) to CLAUDE.md workflow + skill_diagram_structure, ENFORCED by a new lint.py warning 'all-diagrams gallery covers every generated diagram PNG'. Gallery is a complete index; no owned figures to single-source (it carries captions only).*
- [x] engineering-diagrams.md  — *DONE (2026-06-21): index/overview page — SKIP for value substitution (carries no owned figures; all numbers live in the linked detail reports). Copy-edited prose typos and refreshed the system/area lists (solar sub-system, walkway in all three areas, ventilation path).*
- [ ] skill_label_placement.md  — drawing skill

## F. PoC (TBS-002)

- [ ] mini-tbs-poc.md  — *small-scale proof-of-concept design*
- [ ] mini-tbs-shopping-list.md  — *PoC procurement*

---

*Tip: when you clear a file, tick it and (optionally) note what moved out, so we can spot any number
that should become a `facts.yml` entry instead of being deleted outright.*
