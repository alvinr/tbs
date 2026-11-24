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
src/generators/style_lint.py` is an advisory checker (robotic tells, design-history language,
word-count/bloat, thresholds per track) — it never rewrites engineering values. Run it per doc before
ticking; a doc is not done while its **hist** column is non-zero.

**How to use:** `[ ]` = not started · `[~]` = in progress · `[x]` = done. Put a one-line note after each
doc as it's reviewed (what was cut / what changed). Don't mark `[x]` unless told (per CLAUDE.md).

---

## Track 2 — Personal voice (Home + Proposal)

- [x] project-summary.md  *(Home — source synced → index.md by publish.sh)* — voiced to first person (concede-then-punch), front-board claim corrected (pinhole-point vs field-camera, no deprecated-tilt echo), width → "about 14ft", solar/battery + off-grid line added. 0 tells / 0 stiff.
- [x] funding-proposal.md  *(Proposal)*— already largely in-voice (§1/§4/§9 kept as the benchmark); defect fixes, width-drift → ~14ft, solar/battery aligned, '99 sq ft' injected, §2/§8 imperial via computed facts, artistic-vision extension (exposure → motion/ghosting), Construction link added.

---

## Track 1 — Terse engineering (everything else reader-facing)

**Reset 2026-11-20 for the what/why pass.** Every Track 1 doc is re-reviewed against the rule in
`skills/skill_report_writing.md` §F: a design report is the *what* and *why* (and how it's built);
the *how* of operation lives only in the operating manual. **Describe the current design, not how we
got here** (§D): no "was retired", "replaced by", "formerly", "no longer", "now lives", "(was $X)" —
state what the design is and why; history goes in RELEASE.md. `style_lint.py <doc>` lists these as
`history:` lines (2026-11-20: 32 hits across 25 docs found and rewritten; now 0). Notes from the earlier terseness pass
are kept after each entry.

### Costing
- [x] project-cost-breakdown.md  — what/why pass 2026-11-20, confirmed complete (owner): §12 "Research Gaps" to-do list → §12 Cost Confidence (stale rows dropped: tube saddle clamps, ball-lock pins, Grimco ACM, 8-saddle count); §4 saddle anchoring corrected (4 saddles + 2 pivot-post plates + 2 shared BR plates); §4 tilt/swing placeholders; §6/§6a broken sentences fixed; §7.2 per-print table generated from costing.py (was AmFe $75 → $21, rows didn't sum); §7.1 AmFe 260–780 g → 222–668 g; summary line-7 note de-archaeologized (hand-keyed $1,250/$1,710/$3,100 drifted from the generated $1,230/$1,680/$3,040). Cleanup 2026-11-20: hand-typed $ outside generated blocks 171 → 71 (remaining are single-home sourced research quotes); §2 hand tables → registry link; §3.2 lens table → Lens Options pointer; optional additions, §9.1 CDL table, §10 running costs generated; repeated quotes (delivery, trailer, CDL, permits, lens) single-sourced in costing.py; fixed CDL all-in $4,345 → $4,245 and per-print running $71 → $42 (muslin was ~$43/print, is $6). Prior pass: confirmed complete (owner). Verified it is a section/subsystem cost rollup (not a part-by-part BOM) — same totals as the master BOM, every major component named, no SKU/supplier/qty; decided it is the brochure PDF's parts/cost coverage (the itemized BOM stays web-only).

### Construction — Equipment & Water
- [x] equipment-layout-report.md  — what/why pass 2026-11-20, confirmed complete (owner): zone X ranges + transport swing → fact placeholders; chemistry prep shelf added to the pinhole-wall zone (it sits in the optical X span, clear of the cone near the wall — the report said the optical zone held only rails/tray/walkway); "Reducing the film plane…" → stated as the design; "New Layout" alt text and the "600L tote does not exist" aside cut; sources corrected (pumps → Plumbing Report) + shelf source. Line-of-sight + floor plan diagrams now draw the shelf.
- [x] water-system-report.md  — what/why pass 2026-11-20, confirmed complete (owner): DV-01 accept band reconciled to pH 6–7.5 (schematic said 6–7 while §4.2/§2.2 hold the buffer below 7.5, leaving 7–7.5 undefined) — same fix in the Operating Manual §4.2 (incl. step 4.2.9 "above pH 8" → 7.5) and Plumbing Report; band now BROWN_PH_LO/HI constants injected as facts (ASCII schematics keep literal text); flood depth → fact placeholder (owner: tray report), raw "~103 sq ft" dropped; §6 "instead of filling and dwelling / only P-04's runtime rises" → stated as the design; §4.1 cross-tie bullet tightened. §2 chemistry/waste and §9/§10 were rewritten this session and left as is.
- [x] plumbing-report.md  — what/why pass 2026-11-20, confirmed complete (owner): factual fixes — DV-01 outputs go to Brown IBC-3 (table said Blue IBC-2); filter-inlet reducer is on the DV-02 output (said P-02); P-05 shares the near-column IBC-3 tap (said far column); filter bracket is Pentair 244718 (said 150061, the retired kit); Blue manifold is PVC (said HDPE); P-04 lift is to the filter bank (said ~900mm head; the heads sit near the ceiling); §7.4 protrusion table listed the filter housings, which are on the other panel, and a "653mm clear" with no basis → corridor-panel items only, tip ≈ X4744 clear of the X4,649 rail; BV-06 named as the 6th 2-way valve. History cut: intro blockquote duplicating §1; §5.1 "(a) resolved 2026-07-27 … still open (b)(c)" paragraph (both done); "raised / added / re-routed / dropped" support-board phrasing; "replaced the welded frame −$85"; valve re-sourcing prices; "#29/#30" ticket refs. §4.4 now covers SV-02. Corridor width → placeholder. parts.py panel tags fixed (BV-03 → Corridor, SV-02 → Pinhole Wall). 3,527 → 3,329 words. Then: §2 "Panel Specifications" deleted (one panel only; rows duplicated §1, §7.1, the drawing and the cut sheets) — white face folded into §1; mounting merged into one §6.1 covering both panels; sections renumbered and inbound links repointed (water, electrical, manual, energy, dependency map). Then: §2.2 pump-selection/fuse text corrected + drain-pump switches S-05/S-03; valve tags renumbered (BV-05/06/07, no suffixes); §5 flow diagrams redrawn vertically (+ Brown drain-out path).
- [x] walkway-routing-sections.md  — what/why pass 2026-11-20, confirmed complete (owner): the ribbon's four lines were stale in the text AND the B-B/C-C/D-D drawings (IBC-3→P-02 + tray-sump→P-04, both retired when P-02 moved to the corridor and P-04 to the skid) → P-02→ACC-02, Blue trunk→TAP-01, DV-02 waste→IBC-4 (gray, was drawn brown), SV-01→DV-01; F-F "blue SV-01 lane" → brown; finding 6 back-rail top Z65 → Z70.8 (matches E-E + constants); "Interference & clearance findings" → "Clearances" with the history ("tray-datum correction", "now lifts", "two remaining items") stated as the design; "passing" grammar; See Also → Plumbing §7.1.
- [x] ibc-stacking-report.md  — what/why pass 2026-11-20, confirmed complete (owner) 2026-11-21: §3 order fixed (the weld schedule sat inside "3.4a Floor anchoring", and there were two §3.7s) → 3.5 Fastener + Weld · 3.6 Floor Anchoring · 3.7 Datum · 3.8 Assembly · 3.9 Cut List, refs + Walkway §4 link repointed; §9 cost summary was wrong (totes $300–$900 vs 4 × $150 firm; Total $1,280 ≠ $1,380 + $300) → tote + totals generated from costing; IBC-3 "recycled back to Blue" → reused for wash 1; §6 "welded reinforcing plate" → clamped backing doubler (per parts registry) + dust caps; "Pinhole Wall Plumbing Panel" → Filter Skid; history cut ("Doubled from one", "unchanged at 16 / the old 4×4", "now use the SAME", "moved forward", "600 L/640 L are fill levels", #30); corridor width + ceiling clearance → placeholders; cut-list lash-ring note "2 per tier" → 2 per lower bar. Resolved (owner): hangers are welded (W5); §3.8 lists the welded sub-parts; plywood brackets are one-piece 1×1×3/16 angle (walkway-bearer stock). Owner review 2026-11-21: tote quoted at its US size (275 gal = 1,041 L, design cap 1,000 L — new facts); transport restraint re-run on FMCSA 49 CFR 393.102 (bars SF 1.49 / 3.97 with the mat, was 1.59 / 4.77 on EN 12195-1; straps on the 393.106(d) half-weight rule; mats credited at the unrated 50%); §8 now lists the load-case and floor-anchor sheets and points at the gallery (§14/§15). Open: tote connections via the DN50 valve (TODO).
- [x] processing-tray-and-spray-bar.md  — what/why pass 2026-11-21, confirmed complete (owner) 2026-11-21: §3.7 weight table didn't add up (parts sum 10.9 kg dry, table said 13.3; manifold water 1.09 kg vs the 1.22 L computed) → dry ~10.9 / wet ~12.1 kg, ~3.0 kg per wheel (was 2.6); beam clamp plates sandwich the 38mm (1½in) square beam (said "25mm RHS"); ball-joint screws go into the 1.6mm beam wall (said 3mm); flow per nozzle 0.08 GPM (said 0.09); acetal wheels (said nylon — text + Sheet 2 labels); spray bar carries Brown (P-02/ACC-02) for wash 1 as well as Blue (P-01) — §3.1, §3.9, supply path; P-04 discharge runs through the filter train to IBC-3 (said DV-02 → IBC-3 direct); §5 lists all 11 sheets (said seven); history cut ("old corner sump", "old mid-span splice", "pitch was tightened 150→100", TODO pointer); nozzle count → fact placeholder. Weight report "40×25 SS beam" → 1½in square. Owner review 2026-11-21: §3.10 supply path drawn vertically; §4 Operation dissolved — muslin fit → §2.8, the park-and-roll clearance → §3.4, beam removal + manual pointers → §6 Maintenance; §5–§8 → §4–§7. §3.6 trimmed to the four fab/acceptance requirements; bench steps moved to construction-report §8.1, then back to §3.6 on 2026-11-23 (build steps live in the subsystem report).

### Construction — Electrical & Ventilation
- [ ] electrical-report.md  — confirmed complete (owner). §8 de-duplicated (hand-keyed parts table → filtered-BOM link + injected cost summary); inverter DC protection backfilled (§7.6 rule 4); weather/lightning pre-step + corner-casting earth note added; prose already terse.
- [ ] electrical-safety-report.md  — confirmed complete (owner). §7.3 corner-casting earth note + §7.6 DC-protection rule (drove the inverter-DC-protection backfill); prose already terse.
- [ ] ventilation-report.md  — confirmed complete (owner). §9 consolidated to the filtered-master-BOM reference; §5.1 Fan-B wiring verified (silicone-jacketed descriptor dropped); louvre-grille part added; prose terse.

### Construction — Film Plane & Pinhole
- [x] pinhole-report.md  — what/why pass 2026-11-21, confirmed complete (owner) 2026-11-21: "welded (or bolted)" adapter → welded (Ø240 × 6 S275, Ø120 aperture, wall aperture Ø150 — as Sheet 3 + parts); the "perimeter light-trap step / labyrinth" isn't in the design → removed; plate→adapter seal is the Ø160 groove in the plate's rear face (said gasket or O-ring in the adapter); carrier washer + dark slide added to §5; Sheet 3 embedded in §3; new §6 Parts pointer (optics + front-board systems); unused Rayleigh / McMaster sources dropped. Open: mount-bolt length + plate seal not in the BOM (TODO).
- [x] film-plane-mechanism-report.md  — what/why pass 2026-11-21, confirmed complete (owner) 2026-11-21: §5 corner depths recomputed for the current 4,389 × 2,094 plane (they were for an older 4,499 × 2,138 plane, so the listed 40°/28° were really ~41°/~28.8°) and the formula note corrected; §2 table split the width (2,362) from the focal length (2,338) and the container height (2,388) from the film height (2,094), pinhole X = 2,454 (centered on the film plane, not the wall); wall-seat saddles 6 → 4 (+ 2 combined BR plates + 2 far-left pivot-post flanges, per parts.py); rails run wall-to-wall 2,362 (not the focal length); Z travel 245; broken opening sentence, Sheet 1/2/3 captions and a typo-ridden line rewritten; history cut (brace cage, "now", gusset "fouled"); stale $440 subtotal dropped; muslin link → Processing Tray §2.8; U-channel source → Grainger 795M51 (dropped the spray-arm Ruland collar); "scene end" → pinhole wall. Owner follow-ups 2026-11-21: Sheet 5 Table 1 max tilt/swing depths now computed (508/1854, 151/2211); Rise/Fall + Shift rows removed (report + analysis doc + Sheet 3 note); Sheet 3 rail material 304 → 6061-T6. Splice removed (8 ft sticks confirmed); subsections numbered; left rail described as removable + stub; §4.7 Light Sealing + the EPDM strip + Duvetyne removed (no light path to seal).
- [ ] film-clamp-mechanism-report.md  — IN PROGRESS: what/why pass 2026-11-21: parent-report description fixed ("independent actuation" → paired slide-and-clamp corners). BLOCKED on a design gap: the report (and manual §2.4) clamp the muslin by wrapping it over the frame edge, but the muslin is cut to the tray (4,249 × 2,000) and sits ~70mm inside the frame; tbs_constants calls its clamping "inboard on the ACM face (field detail)" — undesigned. Parked 2026-11-21: magnetic mount proposal in TODO.md (🧲); editorial continues on the next reports.
- [x] pinhole-disc-holder-report.md  — what/why pass 2026-11-21, confirmed complete (owner) 2026-11-22: history cut (superseded Ø600 plate, "up from M5", "(correct) renders"); "Four elements" → five; rise/fall dropped from §4 (the film plane gives tilt + swing only) and renders pointed at distortion-renders.md; adapter welded to the interior crests; O-ring added to service items; source 6 retitled (pinhole wall + adapter; optics → Pinhole Optics Report). Optics, countersink, O-ring and M6×25 bolt content already current from today's design work.

### Construction — Misc & Sequence
- [x] walkway-report.md  — terseness pass (4,138 → ~3,700 words): fixed 3 broken sentences, collapsed duplicate bolt-"Attachment" + load-path paragraphs, dropped the "winged" label (unnecessary over self-tapping) + diagram-restated dims. Author editorial folded in. what/why pass 2026-11-22, confirmed complete (owner) 2026-11-22: near/right access lists match the equipment layout (no tilt-swing adjusters; pumps + filters on the corridor panel); right walkway is 245mm and its grating clips to the 2×1 rectangle beams (said L-angle); Sheet 9 X range → placeholders (said 1,055–3,083, actual 1,165–3,193); combined corner plate carries BR only (said BR/TR); left walkway §5.1/§5.3 duplicate tables merged, post at X≈250 (said 140), arm clears the spray bar by ~22mm (said 15); punch-out optical check restated (deck Z140 below the film's Z160 bottom edge — said 'left of the cone', X≥150); cooler 508×254×711 fits the 500mm deck (said 350mm deep, overhangs); grating open area ~70% (said 40%), bearing-bar row dropped (steel-grating spec), resin note → cyanotype chemistry (said developer/fixer); clip pitch 610mm (said ~914 and 'fixed in Phase D'); rib pull-through SF 8 (said 7); Sheet 1 plan embedded; Sheet 5 caption fixed; history cut (deck raise, superseded edge beam, arm redesigns). Generators fixed 2026-11-22: walkway_load.py (§5.2 refs, foot-plate holes Ø13 for M12, redesign notes cut) + a computed soffit-clearance check over the 1:200 tray (rim ≥8.6mm, spray beam ≥11.5mm, both at the far rim) in §9; Sheet 4/5 notes (X880, computed clearances, no '+50mm raise'). Widened-bracket SF 1.83 accepted for now (owner).
- [x] hinged-panel-report.md  — confirmed complete (owner) 2026-11-22. What/why pass: §1 broken sentence; §2.1 table separator fixed + center frame = 2×2×0.120 SHS (said 84mm RHS); housing-surround seal → light path #5 (said #8); §2.5 rewritten as Skin Material (weight-reduction history cut); SKF 6215 ratings corrected to 68.9 kN dynamic / 49 kN static / −40…+120°C (said 52.7 kN, 0–120°C) and cited; drum top/bottom wipers seal against the frame plates (said ceiling/floor mount plates, per light-trap-selection); §3.6 daylight test points to §3.3 (duplicate cut); §4.1 pivot rows point to §5.5; pull handle is on rivet-nuts (said through-bolted) and the movable mass ~200 kg (said 139); stays are lug + turnbuckle + wall anchor (said hook/eye); §5.3 cage underside Z140 clears posts by 25mm and tray rim (Z70–81) by ≥59mm (said 217mm gap clears by 25/70) — walkway §5.4 corrected to match (said Z130 / 15mm); duplicated §5.4 Sheet-4 paragraph cut; history cut (reused/upgraded upright, waste drums, old sliding-carriage seals, 'now'); code names dropped; broken Engineering Diagrams + self-referencing source rows removed. Follow-ups landed: §2.4 injected from the rebuilt generate_movable_panel_weight.py (≈277 kg + pivot loads), pivot plates moved onto the left floor-anchor sub-plate (200×140×20, 4× M12), M16 stay-anchor crush sleeves.
- [x] chemistry-prep-shelves.md  — confirmed complete (owner) 2026-11-23. What/why pass 2026-11-22: sensitizer named ferric ammonium oxalate (project convention); history cut (removed steel frame, M5 screws, TAP-01 "relocated/unchanged"); overhead clearance re-based on the stowed top Z1,300 vs the ceiling-corner trunking (said 425mm — no source); spec sources added (hinge 14835A77, latch 1619A74, ply BPI6WUV2I), unrelated ISO 668 row dropped; broken root-path link to chem-shelf-blueprint-spec.md removed; operating manual §1.7.3 + maintenance now name the chain stays (said the stays "lock"). Chain WLL (3392T51, 1,200 lb, 3/16in) and eyebolt capacity (3014T45, 500 lb vertical, 30% at 45°) now from the owner-checked McMaster pages; eyebolt governs at SF 7. Tee-nut pull-out 1,300 N and ply Fb 10 MPa labeled in §3.3 as conservative assumptions (owner call: mixing-only load, margins 20/44). §1 purpose list no longer claims coating happens at the shelf (sensitizer is applied on the film-plane board). Eyebolts relabeled steel (3014T45 plain, 4843T13 galvanized), accepted for splash exposure; 30%-at-45° derating accepted (McMaster publishes no 45° value).
- [x] construction-report.md  — confirmed complete (owner) 2026-11-23. What/why pass 2026-11-23: step 1.7 left floor sub-plate added (was in the 3D model, missing from the report) and 3.7 now bolts to it; 1.3 return lines named by destination (said "blue recycle"/"gray waste", wrong palette); Phase 4 circuits are A–F (said Blue/Brown/Black, the water colors); 3D-render notes cut from 3.1; §8→§9 model cross-refs; See Also: IBC frame is Phase 1 (said 3); 5.1 matches the model. Owner calls: sub-plate laid at 1.6, before the hinge panel (1.7) whose pivot plate bolts to it — construction model reordered to match; §8.1 spray-bar carriage build steps moved back to processing-tray-and-spray-bar.md §3.6 (step 5.6 points there).
- [x] plywood-cut-sheets.md  — confirmed complete (owner) 2026-11-23. What/why pass 2026-11-23: stock counts were stale (said 4 sheets / 50 cuts, SYP A–C + UV-white D; the drawing is 5 sheets / 55 cuts, SYP A–D + UV-white E) — prose now defers counts to the drawing and the stock table is corrected; history cut (down-from-8, PT re-grade, "now shares"); purpose lists every piece (pipe-clip blocks, cooler base, lip battens); stock rows link their Home Depot SKUs; parts.py EP backboard ~700×2,000 → ~365×1,425 (the schedule's derived size). Follow-ups landed: Sheet 2 legend glyph replaced, cut badges spaced and leaders leveled; Sheet 1 notes clear of the title block, "(was N)" dropped; cooler base moved to the UV-white sheet so SYP packs on 3 sheets (4 total, 55 cuts), pump-mount shirt shares those sheets (−$30).

### Shopping
- [x] master-shopping-list.md  — confirmed complete (owner) 2026-11-23. What/why pass 2026-11-23: intro said "grouped by build area" with an April/July 2026 basis — now states it is generated from the registry, by material type; "AmFe"/"ammonium iron(III) oxalate" → ferric ammonium oxalate (registry desc too); "sensitiser" → sensitizer; unbalanced italic in the BOM intro; Supplier Directory rebuilt from the registry's suppliers (15 of 29 listed suppliers supplied nothing — Photographers' Formulary, Bostick & Sullivan, Grimco, Automation Overstock, Renogy, altE, West Marine, Container Exchanger, Ferguson, Pacific Coast Steel, Curbell, B&H, Grating Pacific, Hessaire, Victron); See Also chemistry row described alternative processes the list no longer carries. §2 is now the complete BOM: the §4 printmaking tools + §5 safety/PPE tables moved into parts.py (systems print-tools / safety, tools-safety type, SKUs pending) and costing lines 10/11 derive from them; §3 recipe cut (owned by chemistry-shopping-list); now §1–§4. Earlier: sections numbered 1–7 (were unnumbered + 9/10/11 borrowed from the summary rows); generated BOM headings demoted to ### (removes the duplicate H2); electrical + electrical-safety "Master Shopping List §6" links now point at the electrical filter.
- [x] chemistry-shopping-list.md  — confirmed complete (owner) 2026-11-23. What/why pass 2026-11-23: restructured into numbered §1–§6; stale hand totals cut ("~$1,653 · ~$33/print" vs the generated $1,683/$34; "April 2026 pricing, † confirmed"); muslin basis was the full 99 sq ft image plane (5,980 sq ft, 399 yd) — the muslin is cut to the 91 sq ft washable tray area, so the run is ~5,232 sq ft / 349 yd (still 3 rolls, $300), now derived in costing from MUSLIN_AREA_SQFT and injected (costing's MUSLIN_YARDS was a stale 360); AmFe/"ammonium iron(III) oxalate" → ferric ammonium oxalate; dichromate waste link → wash-water-classification §4 (was water-system §2.3, moved); unsourced "no hazmat shipping … Photographers' Formulary" claim cut; reagent source → Artcraft (the registry supplier), Bostick row (no link) dropped; "Potassium Ferricyanide — Same as above" row folded into the fallback prose. process-comparison.md muslin rows now injected (were 360/399 yd).

### Transportation
- [x] container-transport-options.md  — confirmed complete (owner) 2026-11-23. What/why pass 2026-11-23: scoped to the 20 ft container, every option kept (owner call); the report assumed an EMPTY container (4,850 lb) — it now uses the fitted camera, derived and injected by generate_weight_analysis.py (dry 3,390 kg / 7,470 lb, loaded 5,190 kg / 11,440 lb, fit-out 1,190 kg); §1 rebuilt as "What Gets Moved"; Option D re-scoped to the dry camera (loaded trailer ~17,000 lb is beyond a pickup rig); Option C/E, regulatory and §9.1 weight lines re-based; 40 ft columns/rows cut; unnumbered subtitle H2 dropped; intro names the commercial-hire budget baseline. Owner: outbound tilt-bed leg runs Blue full — Option A now quotes the loaded 11,440 lb haul weight and a ~25° bed-tilt limit (asin 0.435 g, the IBC frame's 49 CFR 393.102 forward WLL case); operating manual §0.6.3 added.
- [ ] weight-distribution-report.md  — IN PROGRESS: what/why pass 2026-11-23 (awaiting owner review): §3 component tables were hand-typed and stale (hinged panel 161 vs 136 kg, drum 69 vs 59, battery 13 vs 11, corridor plumbing 5 vs 52, chem shelf 7 vs 6, film depth rails 18 kg missing — rows did not sum to the injected subtotals); every row is now injected from generate_weight_analysis.py; drum Ø fact placeholder; stale panel arithmetic + grating history/cost sentence cut; "three states" → four; walkway is the largest structural subsystem (said second after the panel); §5 sub-headings numbered 5.1–5.5; sources point at the processing-tray and hinged-panel reports. Container basis now the Hapag-Lloyd 20' Standard figures (owner-supplied 2026-11-23): tare 2,200 → 2,350 kg, max gross 24,000 → 30,480 kg, as CONTAINER_TARE_KG / ISO_MAX_GROSS_KG in the generator and injected (dry 3,540 kg, loaded transport 5,340 kg).

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
- [ ] wash-water-classification.md  — new 2026-11-20: water-system-report §2.3 classification analysis moved here (rules, baseline, D007 calculation, generator category); water report keeps the results + DV-02 separation.
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
