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
- [ ] water-system-report.md  — IN PROGRESS: what/why pass 2026-11-20 (awaiting owner review): DV-01 accept band reconciled to pH 6–7.5 (schematic said 6–7 while §4.2/§2.2 hold the buffer below 7.5, leaving 7–7.5 undefined) — same fix in the Operating Manual §4.2 (incl. step 4.2.9 "above pH 8" → 7.5) and Plumbing Report; band now BROWN_PH_LO/HI constants injected as facts (ASCII schematics keep literal text); flood depth → fact placeholder (owner: tray report), raw "~103 sq ft" dropped; §6 "instead of filling and dwelling / only P-04's runtime rises" → stated as the design; §4.1 cross-tie bullet tightened. §2 chemistry/waste and §9/§10 were rewritten this session and left as is.
- [ ] plumbing-report.md
- [ ] walkway-routing-sections.md
- [ ] ibc-stacking-report.md
- [ ] processing-tray-and-spray-bar.md

### Construction — Electrical & Ventilation
- [ ] electrical-report.md  — confirmed complete (owner). §8 de-duplicated (hand-keyed parts table → filtered-BOM link + injected cost summary); inverter DC protection backfilled (§7.6 rule 4); weather/lightning pre-step + corner-casting earth note added; prose already terse.
- [ ] electrical-safety-report.md  — confirmed complete (owner). §7.3 corner-casting earth note + §7.6 DC-protection rule (drove the inverter-DC-protection backfill); prose already terse.
- [ ] ventilation-report.md  — confirmed complete (owner). §9 consolidated to the filtered-master-BOM reference; §5.1 Fan-B wiring verified (silicone-jacketed descriptor dropped); louvre-grille part added; prose terse.

### Construction — Film Plane & Pinhole
- [ ] pinhole-report.md
- [ ] film-plane-mechanism-report.md
- [ ] film-clamp-mechanism-report.md
- [ ] pinhole-disc-holder-report.md

### Construction — Misc & Sequence
- [ ] walkway-report.md  — terseness pass (4,138 → ~3,700 words): fixed 3 broken sentences, collapsed duplicate bolt-"Attachment" + load-path paragraphs, dropped the "winged" label (unnecessary over self-tapping) + diagram-restated dims. Author editorial folded in.
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
