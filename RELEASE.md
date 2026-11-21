<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Release Log — The Big Shoebox Project (TBS-001)

Version history for the project. Each tagged [GitHub release](https://github.com/alvinr/tbs/releases)
has a dated section below summarizing what changed since the previous release. Versioning is
informal `MAJOR.MINOR` — this is a design + documentation repository, not shipped software.

## How releases work — the gate

Between releases, **jot every notable change under [Unreleased]** as it lands (one bullet per
change). That running list is the source we curate from. **Cutting a release is gated on this
file** — a release must not ship without a changelog entry:

1. Make sure **[Unreleased]** captures everything since the last tag.
2. Promote it: rename `## [Unreleased]` → `## [X.Y] — YYYY-MM-DD` and start a fresh empty
   **[Unreleased]** above it.
3. Commit, tag, and create the GitHub release from that section's notes.

**`bash scripts/release.sh X.Y`** automates steps 2–3 (promote → regenerate version-stamped diagrams →
commit → **publish the site + brochure** → tag → `gh release create`) and **refuses to proceed if
[Unreleased] is empty**, which is what enforces the gate. Cutting a release always deploys, so there
is no separate publish step to run afterward.

---

## [Unreleased]

- **IBC transport restraint re-checked on the US standard (FMCSA 49 CFR 393.102).** The load case uses the 0.8 g breaking-strength and 0.435 g working-load-limit criteria, credits no bare friction and credits the friction mats at the unrated 50% (393.108(g)). Front bars: SF 1.49 alone and 3.97 with the mats; straps are checked on the 393.106(d) half-weight rule. Load-case sheet, report §3.4/§4.4, parts and drawing notes updated.
- **Pinhole wall described correctly as a long side wall.** The pinhole and disc-holder reports, the engineering-diagrams caption, the adapter constant comment, the parts spec and the disc-holder model description had called it the container's end ("nose") wall.
- **Pinhole mount bolts modeled as real fasteners.** The bolt length, washer and thread engagement live in `tbs_constants` (with a build-time check that the thread stays between 0.8·D and the adapter thickness), and the Sheet 3 label, the parts spec and the 3D bolts all read them. In 3D each bolt is an M6×25 shank, a socket head and a washer, so the bolt-grip audit now covers them.
- **Focal length measured from the actual pinhole: 2,337.5mm, Ø2.15 pinhole, f/1087.** The pinhole sits in the shim on the carrier's camera face, 24.5mm inboard of the wall (`PH_INBOARD`), so the focal length (`PH_F`) is the container width less that offset. The Rayleigh pinhole is derived from it (Ø2.15) and the f-number follows. Exposure figures are recomputed (about 0.2% shorter). The optical cone in 2D and 3D starts at the pinhole.
- **Pinhole carrier bore countersunk.** The bore behind the shim is a 100° countersink opening to Ø14.9 on the scene face; the straight Ø6 bore clipped everything beyond about 21° off-axis, which would have vignetted the film-plane edges (about 47° off-axis at the corners).
- **Plate O-ring shown in 3D:** in the disc-holder model (own tag, labeled) and on construction step 5.1.
- **3D pinhole mount moved inside the wall.** The overview builder now puts the wall-frame adapter, disc-holder plate and retaining ring on the interior face, matching Sheet 3 and the reports; the superseded 100×100 mount plate is gone. Mount bolts sourced: McMaster 92314A669 M6×25.
- **Pinhole front plate sealed with an O-ring.** The seal groove moves out to Ø171, clear of the Ø150 mount-bolt holes and sized for a stock 170mm ID × 2.5mm black nitrile O-ring, and is dimensioned on disc-holder Sheet 2 (3.4mm wide × 1.9mm deep); the O-ring is added to the parts list. The mount bolts are respecced as M6×25 + washer (M6×20 engaged only 2mm of thread); both are pending sourcing.
- **Spray-bar carriage build steps moved to the Construction Report (§8.1).** Processing Tray §3.6 keeps the parts and the four fabrication and acceptance requirements: 200mm wheel spacing, nyloc nuts at 4 N·m, flat two-wheel stance, and grating clearance with straight tracking.
- **Processing Tray & Spray Bar: review fixes.** The spray supply path is drawn as a vertical flow diagram. The Operation section is folded into the design sections: muslin fit → §2.8, clearance over the laid muslin → §3.4, beam removal → Maintenance. Procedures stay in the Operating Manual.
- **Pinhole Wall report: what/why pass.** The adapter is welded (Ø240 × 6mm S275, Ø120 aperture, over a Ø150 wall cut), matching Sheet 3 and the parts list. The plate seals in its Ø160 rear-face groove. A light-trap step that isn't in the design is removed. The dark slide and carrier washer are listed, Sheet 3 is shown inline and a parts pointer is added.
- **Operating manual: Blue totes filled before departure.** Step 0.1.1 fills both Blue totes to the standard fill (1,800 L) before the container is lifted, matching the deployment-trip transport case.
- **IBC totes quoted at their US size:** 275 gal (1,041 L), with the 1,000 L design fill cap kept as headspace. The IBC Stacking drawings list now includes the load-case and floor-anchoring sheets.
- **Processing Tray & Spray Bar: what/why pass + factual fixes.** Weight table re-summed (dry ~10.9 / wet ~12.1 kg — it read 13.3 / 14.4; ~3.0 kg per wheel), beam clamp and ball-joint screw callouts match the 38mm × 1.6mm-wall square beam, flow per nozzle 0.08 GPM, acetal (not nylon) wheels in text + Sheet 2, Brown recycle (P-02 / ACC-02) shown as a spray source alongside Blue, P-04 discharge routed through the filter train, all 11 drawing sheets listed, design-history asides removed.
- **Separate drum-exit grating purchase dropped** (`walkway-drum-exit-grp`, $50/$57/$65): the punch-out is integral to the left lift-out piece and nests on the two stock panels, so walkway and the grand total each fall by that amount.
- **GRP grating cut plan generated from the 3D.** The cut plan had hand-typed inch dimensions and an outdated piece list (single 93″ right deck, 163.7″ near/far runs, separate widening strips), and its generator — like the two film-plane joint studies — had been writing to a retired `diagrams/` path since the image move, so none had regenerated. All three now write to `DIAGRAMS_DIR`. The cut plan takes each of the nine grate outlines from the walkway model's shared outline functions (the 3D builders were refactored onto them, byte-identical), splits the two >10 ft runs at the panel length, and nests them on their real shapes — still 2× 36″×120″ panels. Walkway Report: near-deck widening span corrected to X1,165–3,193 (fact placeholders; was 1,055–3,083) and the piece count stated; the GRP quote doc's stale hand cut list is replaced by the generated plan.
- **Python environment: Homebrew 3.14 venv + `requirements.txt`.** The project `.venv` moves from Xcode's Python 3.9 to Homebrew 3.14 (matplotlib 3.11, numpy 2.5); dependencies are now recorded in `requirements.txt` (fpdf2 pinned at 2.8.4 for the brochure). Scripts and the commit hook call bare `python3` with the venv activated — `publish.sh` no longer hard-codes `/usr/bin/python3`. All 11 model hashes were unchanged; the diagrams were regenerated once under the new matplotlib (text-rendering pixel shifts only).
- **Plywood mounting brackets = one-piece 1×1×3/16 angle; wall hangers welded.** The 6 rear-panel and 12 side-board brackets are cut from the same 1×1×3/16 steel angle as the right-walkway grating bearer (`STEEL_ANGLE_LEG` / `STEEL_ANGLE_T`), TEK-screwed (not welded); the 3D draws each as a single continuous L (was two butted boxes), and Plates 5/6, the support-board section, the frame BOM text and the cut list follow (Plate 6 length 120 → 50mm to match the model). Plumbing §4.3 said the side brackets were welded — corrected. The wall joist hangers are 4mm plate weldments (W5), not folded; §3.8 now lists the welded sub-parts (W3–W6) alongside the box rather than calling it the only weldment.
- **IBC Stacking: what/why pass.** §3 reordered (weld schedule back under §3.5; floor anchoring §3.6, datums §3.7, assembly §3.8, cut list §3.9 — there were two §3.7s and a §3.4a after §3.5); the cost summary is generated (totes 4 × $150 = $600, totals frame + totes — the old table read $300–$900 and its total didn't add); IBC-3 is reused for wash 1 (not returned to Blue); end-wall bulkheads clamp over a backing doubler (not welded); design-history asides removed.
- **Hand-typed money worklist cleared.** Stale copies of cost-model values are now placeholders: the cyanotype tier run costs in Process Comparison and the Master Shopping List (Lean $1,250 → $1,230, Standard $1,710 → $1,680, Rich $3,100 → $3,040; Lean chemistry $951 → $930), the per-print figures, the processing-tray range in Tray Research, and the 2nd battery pack in Cost Analysis + Electrical. Figures that match a model value by coincidence (other processes' quotes, the TBS-002 kit) are listed in `lint.py` `_MONEY_COINCIDENCE`; the warning is clean and the raw-$ baselines are lowered.
- **Walkway Routing Sections: ribbon lanes corrected.** The text and the B-B/C-C/D-D drawings still named the retired IBC-3 → P-02 and tray-sump → P-04 lines; the ribbon carries P-02 → ACC-02, the Blue trunk → TAP-01, the DV-02 waste → IBC-4 (now drawn gray) and the SV-01 → DV-01 filtered return. The back bottom rail top reads Z70.8 throughout; findings restated as the design.
- **Plumbing §5 flow diagrams drawn vertically** (one component per line, waste branches to the side), naming every valve and switch on each path; the Brown drain-out (IBC-3 → BV-02 → P-05 → X3) is now drawn.
- **Spray valves single-sourced at their real positions.** `BV05_Z` (950) placed both spray valves in the 2D while the 3D had them at Z700 / Z900 with a typed −150mm X nudge. Now `BV05_X` = pinhole X − 150 (shared riser), `BV05_Z` = 700 (selector) and `BV06_Z` = 900 (on/off), read by the 3D builder, the pinhole-wall elevation, the spray-bar sheet and the near-walkway riser hole. The elevation now draws the 3D topology: Blue trunk up into BV-05, recycled Brown into its side, mixed riser up to BV-06, hose off BV-06.
- **Valve tags renumbered — no letter suffixes.** The spray selector BV-05a is now **BV-05**, the spray on/off BV-05b is **BV-06**, and the P-03 waste-drain suction (was BV-06) is **BV-07**, across every report, the Operating Manual, the parts registry, the 2D sheets (pinhole-wall elevation, spray bar 1/7, panel layout + spine A, water system, electrical 4, support detail) and the 3D models. References to the valve the spray hose leaves from now name BV-06 (the on/off), and the flow chains read BV-05 → BV-06 → spray bar.
- **Drain-pump switches S-05 / S-03.** The 2-pole EP master switch energized all four corridor pumps during every wash, including the drain pumps P-05 / P-03, whose suction valves are closed then — so they could not build pressure, their pressure switches would never stop them, and C1's 15A fuse would carry three running pumps. Each drain pump now has a local sealed 1-pole rocker (S-05, S-03) on the corridor near-upper side board, each mounted level with and beside its suction valve (S-05 by BV-02, S-03 by BV-06) since they are operated together, OFF except during a pump-out. 3D (water model: switches + rerouted + leads through drilled holes, interference-clean), Electrical Sheets 1/4/7, the near-upper board blueprint, parts/costing (+$20/$30/$40, SKU pending), Electrical §7.3, Plumbing §2.2 and the manual (setup check, valve matrix, pump-out, pack-down) updated. Plumbing §2.2 also corrected: the spray selector BV-05a — not the suction valves — chooses P-01 vs P-02, and C1's fuse covers one working pump while C2 carries P-04 alone.
- **Energy model: tote pump-out corrected.** `calculate_energy_budget.py` and Daily Energy §6 assumed each tote gravity-drained through a low port and the pump lifted only a ~120 L residual (~36 Wh per dump run). X3/X4 sit above the bottom-tier totes, so both are pumped out entirely: the volume is now the run's recovered water (622 L per collection tote, unchanged by the dichromate split) → ~115 Wh per dump run (~5% of a 3-print day), with full 1,000 L totes as the ceiling. Light and day-share figures are generated too.
- **Plumbing Report: what/why pass + factual fixes.** DV-01 outputs to Brown IBC-3 (not Blue IBC-2); the filter-inlet reducer is on the DV-02 output (not P-02); P-05 shares the near-column IBC-3 tap; filter brackets are Pentair 244718; Blue manifold is PVC; the protrusion envelope covers only the corridor panel and states the real clearance to the film rail. Stale "still open" joint-convention items, design-history and price-archaeology asides removed; raw $ in the report 5 → 0 (ratchet lowered). Parts panel tags corrected (BV-03 corridor, SV-02 pinhole wall). §2 "Panel Specifications" (corridor panel only, all rows duplicated elsewhere) removed; panel mounting merged into one section covering both panels; sections renumbered with inbound links updated.
- **Operating Manual valve references corrected.** The manual named valves that don't exist ("isolation valve V1" on the fill line, "VB1/VB2/VB3" on the Blue manifold) and mislabeled BV-06 as the chemistry tap (it is the P-03 waste-drain suction; the tap is BV-04). Every step now names the real valves: 0.1.2 sets the tote butterflies + BV-01/BV-03 open and BV-02/BV-04/BV-05b/BV-06 closed; the valve matrix lists all six BVs; TU.2 fills through CV-1 (controlled at the bowser); TU.3 opens/closes BV-02/BV-06 and the IBC-4 valve around a pump-out; the cooler fills from TAP-01 via BV-04. Also fixed: P-02 is the recycle-spray pump (not the filter feed — that is P-04), so the filter-change procedure isolates via P-04 + 3W-DV-02; the unverifiable "2.5–3.5 bar" check (no gauge in the design) became a spray-bar flow check. External ball valves at X1/X3/X4 rejected: BV-02/BV-06 + caps isolate the drains; a lockable port cover box is on TODO.
- **End-wall port caps; Plumbing §6.3 corrected.** 3× 2" camlock dust caps for X1/X3/X4 added to the registry (SKU pending, $6–15 ea est; water +$18/$32/$45) — the manual already said to re-cap the ports but the BOM had no caps. Plumbing §6.3 said IBC-4 gravity-drains through X4; X4 sits above the tote, so it is pumped only (P-03). Water §7 states the port leak protection; manual adds a caps-on / drain-suctions-closed pack-down check (5.5.14) and re-cap after a Blue top-up.
- **New report: Wash-Water Classification.** The regulatory analysis that sat in Water System §2.3 (federal/California rules, the iron-only baseline, the four-step D007 chromium calculation, the generator category and episodic-event rule) is its own research report; the water report keeps the results and the DV-02 wash-1 separation they drive. Chromium and generator-category facts now owned there; Sensitizer Trials T6/T7 and the manual point to it. Registered in nav and home table; web-only (not in the brochure). Home-table descriptions for the Pinhole Report (still described the retired plate system) and Equipment Layout corrected.
- **Water System: what/why pass; DV-01 pH band reconciled.** The Brown-return accept band is pH 6–7.5 everywhere (the schematic, Operating Manual §4.2 and Plumbing Report said 6–7 while the buffer is held below 7.5, leaving 7–7.5 undefined). The band is now `BROWN_PH_LO`/`BROWN_PH_HI` in `tbs_constants.py`, injected into all three docs, and the manual's "never return water above pH 8" step is corrected to the same 7.5 limit. Flood depth single-sourced as a fact; §6 flow-through wash stated as the design.
- **Line-of-sight and floor-plan diagrams draw the chemistry prep shelf** (deployed, on the pinhole wall); line-of-sight runs it through the same cone check — clear in plan by ~456 mm. Line-of-sight also stops showing false red borders: the elevation colors an item red only when it is inside the cone in both views, and the floor-level tray (under the cone by design) no longer reads as a clash or prints a stray "IN CONE" label.
- **Equipment Layout: what/why pass.** Zone boundaries and the transport swing are fact placeholders; the chemistry prep shelf is listed in the pinhole-wall zone (clear of the cone); history asides cut; sources point pumps to the Plumbing Report.
- **Editorial review checks for design-history language.** `style_lint.py` gains a `hist` column (retired / replaced by / formerly / no longer / "now lives" / "(was X)"), and the Track 1 criteria name it explicitly: a report describes the current design, not how it got there (skill §D). All hits rewritten to state the current design (32 across 25 docs, now 0): e.g. the pinhole report's "former Ø600 plate was retired" note, the right-walkway cantilever study recast as design rationale (cantilever vs ceiling-hung, its implementation log removed), film-clamp, plywood, tray-beam, corner-plate and IBC bracket asides. "No longer UV-sensitive"-type physical statements are exempt.
- **Cost breakdown §9 now sums its own lines.** The "Licenses & permits" summary row was a fixed $220 / $790 / $1,620 that matched none of its subsections; it is now computed in `costing.py` from the location permit, business license and misc. lines, with the one-time CDL in the High column only (the baseline is commercial hire, which needs no CDL) → $10 / $300 / $7,320. §9.3 is the section-total table; CDL leaves the optional-additions table (no double count). Grand total $27,640 / $32,229 / $45,318. Scenario C's CDL line, a hand-typed $4,500, now uses the same CDL figure as §9 High ($6,570).
- **2D water sheets brought back to the 3D.** ibc-stacking Sheet 5 drew the retired routing (filter return into IBC-2); it now shows DV-01 recycle → IBC-3 on a pH pass and the waste merge into IBC-4 through CV-2/CV-3, with the legend and notes rewritten. Sheet 4 no longer lists P-04 as a corridor pump. water-system Sheet 1 labels the 1" equalization tie and shows its flex jumpers. On the pinhole-wall elevation, P-04's ports are drawn to the datasheet reach and its suction enters at port height. The SV-02 marker now sits on its pipe: `PWP_SV02_Z` was the valve's base while both sheets read it as the center, so it is now the true center and the 3D derives the base from it (same geometry). The bridge-arc crossing is replaced by the skill's flush break. Labels are at the 4.0 legibility floor and moved off the pipes they named. The 3D F1 label read "50um"; it is a 5-micron cartridge. Walkway E-E listed IBC-3 → P-02 three times because its capture saw runs the builder constructs and then drops; it now keeps only runs that reach the model. Its tags no longer hide under the pipes. The four panel sheets (corridor front elevation, spine views A/B, pinhole panel) now take their routes, valve centers, clips and flex jumpers from an in-process build of water.skp, so they can't drift from the model. The spine views drop the retired DV-01 Blue-recycle riser, show X1 as a tee, and add CV-2/CV-3. The pinhole panel draws the extended board's low runs, clips and corner notches. Electrical Sheet 4's pump boxes use the datasheet envelope. Two 3D fixes came out of the 2D pass: the X4 waste pickup had a diagonal leg (an 18.5mm Yd jog spread across a 1.4m rise), now squared onto the spine lane; and the ACC-02 → BV-05 hop over the P-04 suction riser is derived from the riser's X (the port change had moved the riser into it). The spine's far (+Yd) face is now an accepted standoff exception (`SPINE_FAR_FLUSH_OK`), no longer pending review: its nine clips (P-05 → X3, P-03 → X4 and the X4 drop) sit on 6.5mm shims because the lane is fixed by the pump-port turn; the plumbing report says so. X3 moved so its line is clamped: after crossing the spine, P-05 → X3 used to drop onto a Yd1109 lane 97mm off the spine with no support. It now turns onto the spine's near-face clip lane (an 18mm block, one new P-clip) and runs straight to the end wall, so X3 sits at Yd1177.5 / Z1502 (was Yd1109 / Z1700), with one riser and two elbows fewer (`X3_CROSS_X`). Spine View A draws the new tail. The end-wall port heights are now single-sourced: `EXT_DRAIN_3_H` / `EXT_DRAIN_4_H` had stayed at an old Z400 / Z200 the 3D never used, so IBC-stacking Sheets 3–5 drew X3/X4 near the floor. They are now Z1502 / Z1620, and the corridor model builds the X3/X4 (and X1, `EXT_FILL_1_H`) ports from them, refusing an X3 height off the straight P-05 run. `check_pipe_supports` now also fails any non-axis-aligned pipe leg (the spray-bar feed hoses and one battery cable are ratcheted as legitimate diagonals). Review fixes: ACC-01 and ACC-02 draw their IN/OUT port stubs so every run lands on a port, P-01 → ACC-01 IN gets its 90° elbow, and the TAP-01 riser elbows into its spout; its isolation valve is labeled BV-04 (BV-06 is the P-03 suction valve) on the elevation and in chemistry-prep-shelves.md. Walkway E-E draws the four pumps and ACC-01 solid, so a unit's suction and discharge runs (opposite-Yd ports on one Z, collapsed by the projection) read as meeting on the unit rather than at a missing elbow.
- **Pump draw corrected to the Shurflo 2088-554-144 datasheet.** `PUMP_DRAW_A` was 7.5A (90W), labeled "datasheet" but not on it; the datasheet's peak is 5.2A at 30 PSI, so the pumps are now 5.2A / 62W (`PUMP_DRAW_W` derives from it). The daily-energy report follows: per print 758 → 735Wh, a 3-print day 2,383 → 2,313Wh, the electrical §3 all-on peak 543 → 487W. Its pump rows, wash-pumping figures, dump-run table and 4-print battery overrun were hand-typed and are now `energy:` placeholders, as is the §3 peak (`peak_w()`). Electrical Sheet 1's ENERGY SUMMARY is now computed from the energy budget (it had been hand-keyed), and Sheets 1/4/5 print the pump wattage and current from the constants. New fact `pump_draw_w` covers the report prose.
- **Waste disposal: chromium-bearing by default (the dichromate contrast agent stays).** Every print puts chromium(VI) from the ammonium dichromate into the wash water, so the "low-toxicity, sewer-acceptable" claims no longer held. Water-system §2 adds dichromate to the wash-water table (and corrects FAC → ferric ammonium oxalate), cites the EPA D007 chromium limit (5.0 mg/L, 40 CFR 261.24), and notes the filter train is not credited with removing chromium. §4.3 always sends both Brown (X3) and Waste (X4) to a licensed hazardous-waste hauler, manifested (no lab-test exception — California's rules are stricter than the federal limit). IBC-4 stays in the frame and is pumped out (the old sealed/UN-labeled tote-transport wording is gone). The operating manual (§0.3 warning, DV-02 guidance, 5.1.1, TU.3), funding proposal, process comparison, chemistry shopping list, plumbing and daily-energy reports now say the same. The dichromate dose was stated three ways (~10g/print, 1kg/50 prints, ~1–4g); it is 2.6–10.4g per print (0.1–0.4% of ~2.6L), and the master list's ferricyanide row (130g / 6.5kg, stale) is now a costing placeholder (112g / 5.6kg).
- **New money checks in `lint.py`.** Hand-typed dollar figures were invisible to every check.
  - **GATE:** the per-doc count of raw `$` figures outside generated blocks can only go down (`_MONEY_RAW_BASELINE`; 805 figures across published docs today).
  - **WARNING:** flags a raw figure that equals a non-round value the cost model owns. It is fed by the new `costing.py --money-values`.
  - **Also generated now:** cost breakdown §9.3, the per-deployment permits table.
- **Cost breakdown: hand-typed money figures replaced by generated values.**
  - **Hand-typed $ figures outside generated blocks:** 171 → 71. The remaining 71 are sourced research quotes that each appear only once.
  - **Generated from `costing.py`:** the optional-additions table, the §9.1 CDL table, the §10 per-print and per-deployment running costs, the §7 muslin and per-print figures, and the location-permit rows.
  - **Single-sourced in `costing.py`:** research quotes that appeared in more than one place (delivery bands, QuickLoadz trailer, CDL components, location permit, lens range).
  - **Removed duplicates:** the §2 interior hand tables now link to the registry, and the §3.2 lens table now points to Lens Options.
  - **Errors fixed by generating:** CDL all-in $4,345 → $4,245 (the components didn't add up); per-print running cost $71 → $42 (muslin had been ~$43 a print, and is $6); §7.2 AmFe $75 → $21 a print.
- **T6/T7 wash-water checks are now test plans.** Both run first as a bench test alongside T1. 1 m² muslin pieces are washed in three baths of ~6.2 L each, which gives full-scale concentrations, so the disposal route is known before the build; each is then confirmed once on the real totes.
  - **T6 (baseline):** a 96-hour fish bioassay (LC50 ≥ 500 mg/L; DFG 1988 method per 22 CCR 66260.11), total/free cyanide, the Title 22 metals panel and pH.
  - **T7 (dichromate):** total chromium and Cr(VI) in bath 1, in baths 2 and 3, and in the 2+3 mix. Brown passes at ≤ 2.5 mg/L; full-scale, that means washes 2–3 may carry ≤ 0.47 g of chromium per print, which is 52% of the chromium at a 0.1% dose but only 13% at 0.4%. A mass balance checks the ≥ 45% washout assumption.
  - **Lab handling:** an ELAP-accredited lab, with containers, preservation and holding times per 40 CFR 136.3 Table II. All figures are computed constants injected as facts. Water §2.3 now describes the bench-then-confirm sequence.
- **Operator-value conflicts resolved.**
  - **Plumbing §3.2:** pump power now matches the electrical design. C1 (15A) feeds the four corridor pumps, one at a time; C2 (10A) feeds P-04, which runs concurrently for the flow-through wash. Both sit under the 2-pole EP master switch, with 14 AWG branches.
  - **Spray-bar park position:** the bar parks at the pinhole-wall end. Manual §4.1 adds the park-and-roll muslin loading, and §4.2.1 starts from there.
  - **Times:** mode conversion is ~10 min (manual §1.3/§5.5/§5.6, hinged-panel and light-trap reports). The dark-adaptation check is 5 min (manual §1.4.4/§1.8.3, maintenance).
  - **Transport order:** the apron strips come out before the cam latches are released (§5.5.7/5.5.8).
  - **Stale details:** the plate swap is ~30 s (lens-vs-pinhole), and the dead "Equipment Layout §4" reference in ventilation §5.3 is gone.
  - **Sensitizer working volume:** 2.2 L (Part A/B 1.1 L each) is now placeholder-injected across the manual and master list. The master list's distilled water per 50 prints is derived: 110 L, was 130 L.
- **Design reports state what and why; the operating manual holds the how.** Operating instructions were swept out of the design reports: plumbing, processing tray, IBC stacking, chemistry shelves, chemistry list, hinged panel, light trap, ventilation, weight, container, film plane, muslin clamps, electrical, electrical safety, daily energy, walkway, pinhole disc holder and photosensitive-plane options. Imperative steps became declarative design statements that link to the manual, and each report's maintenance table became a design summary. The operating manual gains:
  - a full **Maintenance** section (water storage, plumbing and filter skid with the cartridge-replacement procedure, tray and spray bar, IBC frame, chemistry shelf, hinged panel and light trap, ventilation, film plane, muslin clamps, electrical, walkway and pinhole disc holder)
  - §1.9 film-plane tilt, swing and focus setting
  - §0.6 transport booking (DOT route, axle placement)
  - "Changing the Front-Board Carrier"
  - shore-power RCD/GFCI and no-AC-inside checks in §1.5
  - chemistry-shelf deploy and stow
  - muslin pre-wash in §0.4.7
  - transport steps in §5.5 (corner lock, muslin screen and brace cage, cooler cord and inverter disconnect, fuses off, tote straps)
  - a caution against bleaching a tote that still holds wash-water residue
- **Ammonium dichromate is now a creative option, not part of the design.** The iron-only Ware sensitizer is the baseline. Water-system §2 is restructured: §2.1 sets out the baseline and the option, §2.2 the wash water, and §2.3 the waste classification for each case. The baseline is non-hazardous, confirmed by a one-time check (new trial T6). The dichromate option is D007 hazardous. Under the option, DV-02 sends wash 1 straight to IBC-4 (~46 L/print, keeping the chromium out of the filters and the recycle loop). Brown is hazardous until measured (new trial T7). The generator-category table covers both cases: separating wash 1 keeps a 15-print month below the large-quantity threshold once Brown measures clean. §4.2/§4.3 describe DV-02's role and give disposal by chemistry. Operating instructions moved from the report to the manual: citric-acid dosing, glove guidance and the maintenance schedule (§9/§10 are now design-only). The operating manual adds a "Chemistry Choice" section and splits Part B (§0.3) into baseline and dichromate steps. Its §4.2 sets DV-02 by chemistry for pass 1, adds the pH-correction steps and a new low-contrast troubleshooting row. §5.1 now routes leftover sensitizer and roller rinse to Waste and gives disposal per chemistry, and a new Maintenance section is added. The dichromate dose is derived (2.2–8.8 g/print, 0.11–0.44 kg per 50 prints) in the master list, chemistry list and manual. Parts, costing, funding proposal, chemistry list and plumbing report mark the dichromate optional; the $25/run allowance is kept so the option stays funded.
- **Water §2 waste classification — derived basis.** A new "Waste classification — basis" subsection works the chromium through from Ware's recipe: the dichromate dose over a ~2.2L working volume gives 0.91–3.63g chromium per print. At ~83L recovered per print, that is 11–43.7 mg/L, or 2.2–8.7× the 5 mg/L limit (federal D007 = California's soluble limit, STLC). A print would have to keep more than 55% of its chromium for the water to pass. The subsection also covers the federal generator category: more than 1 print a month exceeds the very-small threshold, and 13 prints a month reaches the large-quantity threshold. All figures are computed constants injected as facts. The California, generator-category and episodic-event sources are cited.
- **Corridor plumbing panel weighed from its parts.** `plumbing_panel_mass.py` sums the ply pieces (cut-sheet dimensions, spine profile less its holes), the four corridor pumps (2.18kg, datasheet), ACC-01 (360g + 0.75L), water-filled ½"/1" Sch-40 PVC clipped to the corridor box from an in-process water.skp build (0.16 / 0.32 lb/ft), plus fittings, valves and P-clips: ~51kg. The IBC-frame service check (`M_PANEL_KG`) had used a 20kg estimate, now ~84 N per rear-panel bracket (still trivial). The weight model had the panel as 4.5kg, so dry weight rises 3,268 → 3,314kg. The weight report's Blue max-fill table and its CG/tip prose were hand-typed; they are now computed (`MAX_BLUE_FILL_PER_TOTE_L`, tip = atan(half-width / Z_cg)). The operating manual's top-up step no longer points at the dropped IBC-2 float alert.
- **Safelight draw calculated from the cut sheet; pump weight corrected.** Circuit D is one 5m SBL red COB reel cut into the three ceiling runs; at 2.4 W/ft ([COB2 cut sheet](https://www.superbrightleds.com/led-strips-and-bars/5m-rgb-single-color-cob-led-strip-light-cob-series-led-tape-light-ip20-24v-red-green-blue+color-red+volts-12~vdc)) that is 16.4ft × 2.4 = 39W (3.3A), now `SAFELIGHT_W` in `tbs_constants.py`. Electrical Sheets 1/2 had printed 15W and the report 40W; both now read the constant (new fact `safelight_w`). The daily-energy per-print phase rows (W and Wh) are `energy:` placeholders too, so a load change cascades. All-on peak 487 → 486W. The pump-mount shirt spec gave the five Shurflo pumps as ~6.5kg total; the datasheet is 2.18kg each, ~10.9kg.
- **IBC-2 low-level float switch dropped.** It was named in the water report and carried in the registry ($8–20, SKU pending) but never designed in (no mount, alert or circuit), and it is not needed. Removed from the report, `parts.py`, the shopping list and the water-storage cost line (water −$8/$14/$20).
- **Schematics and plans authored in mm.** Water System Sheet 2 (equipment plan) had the container squeezed into a 12×5 canvas with unequal X/Y factors (a ~4% stretch) and labeled with the exterior size; it is now a 1:1 mm plan from the constants, which also corrects TAP-01's position, the corridor panel (now from the 3D rear panel + pump column), the spray bar (single-feed beam), the tray panel size, and adds the pinhole-wall filter skid. The not-to-scale schematics drawn in figure inches (Water Sheet 1, Electrical Sheet 1 and View C, Ventilation Sheet 1) are re-authored in sheet mm with no visual change. Water Sheet 1's filter labels now read 5µm / KDF-55 / GAC (F1 had read 50µ, F2 5µ). The *diagrams authored in mm* gate also catches ratio-form scale constants and axes whose limits are the figure size in inches; CLAUDE.md records that schematics use sheet mm.
- **water.skp review fixes.** The drain-riser spine now carries the X1 fill: the X1 tee and its inlet run are centered on the spine's thickness and rest on its top edge (`SPINE_Z1` = X1_TEE_Z − pipe radius = Z2239.5), notched (2mm clearance) for the full X1 tee fitting (its run body, +X branch body and socket cuff) and for the in-line X1 check valve; the notch sizes come from the same `TEE_*` / `CV_*` constants the fittings are built from. The spine is a profiled prism (`spine_profile()`, also drawn on Spine Views A/B); it loses the old X1 hole and its cut-sheet blank is 680 × 1960mm. `ruby_prism` gains round holes on the Y axis. The spray-bar hose no longer leaves the open top of the BV-05b riser: an elbow at the riser top turns +Yd off the wall and the coiled hose barbs into its outlet. The Circuit C feed drop and pump bus behind the corridor panel ran straight through the X4 waste pickup where it turns through the panel at Z1700; the cable now dog-legs +Yd around it (between the pipe and the spine face), with no pipe or ply hole moved. `check_interference` missed it because its crossing pass only compared arrow-named runs and classified the `Cct C bus` as neither pipe nor solid: every `Cct …` conductor is now a pipe, and arrow-less pipe runs (bottom pickups, buses, branches) are crossing-checked too, an overlap at one of their ends counting as a tee onto the other line. The stricter check then caught a clash in electrical.skp that dated from the C1/C2 fuse split: fuse E sat directly behind the battery − 2/0 riser, so the Cct E feed ran inside it. The riser lane (`EP_RISE_X_M`) moves past fuse F to under the PV disconnect's center, whose two PV feed legs now land ±24mm either side of center (`PV_LEG_DX`, was ±18) so the riser passes between them; the Cct E feed keeps its route and lands 30mm along the inverter top, clear of the Battery + drop. In electrical.skp the PV interior MC4 stubs, pigtails, ± buses and the PV array disconnect (surface-mounted on the interior access panel) are their own component on the Power Core tag (the PV feeds no longer stop in mid-air when the External Panel tag is off), and the Power Core / External Panel scenes drop the chem shelf, the fan-load ghosts and the transport-stay plates (new Context Loads tag) plus the ceiling cable-trunk saddle clips (their `Clips` tag was never registered, so they had sat on Layer0 in every scene). `ruby_clip_run` no longer drops a cable clip onto an elbow: a clip that would land within one clip-width of a bend slides back along its leg (eight such clips in electrical.skp, e.g. the E-stop link clip 7mm under its top bend).
- **Pipe elbows show both joint lines; pump ports drawn to the datasheet; flex jumpers on the Blue equalization tie.** Every swept elbow was built along an inscribed 8-chord arc, so its far end face sat square to the last chord, not to the next pipe. That end ring was tilted ~5.6°, half of it buried in the adjoining pipe, and the joint line vanished at most elbow exits. Elbows now sweep the circumscribed polygon (tangent at both ends), so both rings sit square; this lives in the shared drawing helper, so every model with elbows picks it up on its next re-send. The corridor and skid pumps' port stubs now match the [Shurflo 2088-554-144 spec sheet](https://assets.freshwatersystems.com/images/skvxfhchi3wsmu9p29is/2088-554-144.pdf) (1/2"-14 NPSM male, 127mm across the port tips = `PUMP_YD_SPAN`): 13.5mm stubs, was 30mm. A ½" FNPT×slip adapter leg carries each run to its turn elbow, so the side-board riser planes are unchanged. The 1" IBC-1↔IBC-2 equalization tie was the only rigid tote-to-tote run; it now lands on each tote through a 1" flex jumper like every other tote connection (barbs M+F 8→10, SS clamps 2→3 10-packs; water +$28). The skid's tray-sump suction clip moved from just off the ply edge (X2760) onto the panel (X2830).
- **Pump ports: elbow on the port, flex jumper after the turn; pinhole skid ply extended to the floor plates; every ply crossing gets its hole.** Each corridor pump run now turns one elbow radius out of its port, and the braided flex jumper moved onto the first straight leg after that turn (`port_jumper()`). That let the side-board risers move out to the pump-column limit, 5.5mm (near) / 4.5mm (far) on a ply block, and took the suction runs out of the near board (they had been drawn 3.5mm inside it). The pinhole-wall skid panel now extends down to the near-walkway cantilever wall-plate tops (Z200; 1,795×2,160, still two 4×8 sheets) with two corner notches for the right-rail end flange and saddle plate. The low runs (tray-sump suction, the three corridor drops) now clip to the ply under one rule (`wall_clip()`), leaving only the runs left of the panel on the bare wall; ACC-02 keeps its Z920 base. The support/connection GATE gained a ply-penetration check (a pipe may cross ply only along its thin axis, through a hole at least its size). It found the missing spine holes (X1 fill → IBC-2, the IBC-4 waste entry, and the 1" Blue equalization tie through a ½" hole), a rear-panel hole for P-03 → X4, and two Cct C bus holes through the shirt and rear panel. Hole lists are now module constants, so the cut sheet counts them, and the cut sheet lists the notches and the pipe-clip standoff blocks (from offcuts).
- **Pump connections restored; new lint gate for pipe support + connection.** Shimming the corridor side-board risers out 18mm pushed them into the pump ports, collapsing the port→riser legs to ~8mm, so the pipes stopped meeting the pumps. The board faces are 234mm apart, and the pump plus its ports (160mm) leaves no room for an 18mm block plus a full elbow on each side. Those risers are back at 2.5mm as a logged exception. The new GATE *water pipes supported + connected* (`src/models/check_pipe_supports.py`) builds the water model and fails on (a) any P-clip whose strap is not on a pipe and (b) any NEW elbow whose leg is too short for it (ratchet on `pipe_elbow_allowlist.txt`, 48 pre-existing short legs). It caught and fixed: the two ACC-02 clips sitting in the port jog (moved onto the run), a far-board clip above the end of the P-01 → ACC-01 riser, and an F3 → SV-01 elbow. Also: DV-02 now has a ply mounting block, and the black P-03 → X4 line moved onto the Brown P-05 → X3 lane offset (10.5mm, blocked) pending the spine review.
- **Water pipe clips now sit on ply-offcut standoff blocks; pipes stand >= 18mm off the face.** A clip audit found the pipe-to-face spacing ran anywhere from 0 to 82mm with no consistent rule: the spine and side-board risers were flush, the skid lane was 6.5mm off, and on the spine's far face one Brown line was 10.5mm off while the black line beside it was flush. With no clearance, in-line fittings and check valves can't clear the ply. Every clip is now drawn as an 18mm-ply offcut block plus a strap (`clip_on_block()`, cut to depth for the wider standoffs). The spine risers + IBC-4 merge tee, the corridor side-board risers, the Blue #1 return lane, and the pinhole-skid lane all moved out to one block off their face. That re-laid four nearby runs to stay clash-free: the DV-01 waste lane now passes 30mm in front of the DV-02 riser, the three corridor drops moved to Yd69, and the Blue trunk's corridor crossing dropped to Z200. The clash check is clean (0 interferences, 0 crossings). The helper refuses a clip under 18mm, and lint refuses a raw clip box. The spine far-face X3/X4 lines are exempted pending the spine-relocation review.
- **Check valves CV-2 / CV-3 added on the two waste legs into IBC-4.** The DV-01 reject leg and the DV-02 waste leg meet at a tee just before the IBC-4 top entry. Without a one-way valve on each, one leg can back-feed the other, and with DV-01 set to waste the IBC-4 riser column can drain back through DV-01 into the filter train. The pumps' integral checks sit upstream of the diverters, so they don't cover this. The 2D schematic already drew CV-2/CV-3; the 3D model, BOM (`check-valve-half` ×2, SKU pending, +$20–40), costing, and the water-system/plumbing reports now match. Also: the DV-02 waste leg's rear-panel clearance hole sat 25mm below the pipe (Z65 vs Z90); pipe and hole now read one constant (`WASTE_PANEL_Z`). The clash checker now ignores the mixed-line stripe sleeves.
- **One pipe-color convention across every 2D diagram and 3D model: Blue = fresh, Brown = used/recycled, near-black = waste, a blue/brown stripe = a Blue-or-Brown line.** The audit found the filtered line (F3 → SV-01 → DV-01) in filter-housing blue, waste pipes in mid-grey, the X3/X4 end-wall ports in check-valve purple, near-black port stubs that would read as waste, and a duplicate blue on the spray hose. The fluid palette now lives once in `tbs_constants.py` (`C_PIPE_FRESH / _RECYCLE / _WASTE / _FITTING`) and both the 2D and 3D generators import it. Everything downstream of the BV-05a selector (BV-05a → BV-05b, the spray hose and feed, the spray bar) carries Brown on wash 1 and Blue on washes 2–3, so it is **striped**: brown sleeve bands in 3D (`ruby_mixed_pipe_run`, `ruby_coil_cord(color2=…)`), a blue line with a brown dash overlay in 2D (`draw_mixed_pipe`). Port stubs are now neutral fitting grey, X3/X4 are steel like X1, and the spray-bar flex is yellow like every other flex, so black means waste only. Applied to the water, corridor and spray-bar models and to 17 sheets (water-system 1–4, panel-layout, pinhole-panel, spine views A/B, pinhole-wall elevation, walkway sections 1–4, support detail 1–2, IBC stacking 4–5), with legends updated. Codified as plumbing-skill rule 8 + CLAUDE.md, and enforced by a new `lint.py` GATE (*water pipes use the fluid color convention*).
- **Water model — the DV-01 recycle leg is now Brown, not Blue.** The routing was already correct (DV-01 sends filtered water to the IBC-3 Brown buffer on a pH pass and to IBC-4 on a fail, per water-system-sheet1). But the recycle leg was drawn in the Blue-circuit color, and it climbs the far support board beside IBC-4 before crossing into IBC-3, so it read as a blue pipe running into the waste tote. It carries filtered used water, so it's now Brown-circuit (`C_IBC_BROWN`); stale comments around it corrected. Re-sent into water.skp; the shared leg also lands in ibc-stack, construction, and overview. The X1 fresh-fill **4-way cross is now a tee**: its fourth port was where the recycle used to join Blue, and nothing connects to it now (BOM: cross-100 → a 4th 1" tee, −$4; grand total → $27,810 / $32,675 / $39,570).
- **Plumbing-panel plywood labelled as standard exterior, not marine.** The corridor plumbing panel and pinhole-wall backing board are dry mounting backboards, and the BOM already specs standard exterior sheathing. But the IBC Stacking (Sheet 4) and Panel Layout (panel-layout, pinhole-panel) diagram labels, the dependency-map caption, and several code comments still said "marine ply". Labels corrected and the three sheets regenerated.
- **Wash order — recycled Brown is now the FIRST wash (was the second).** The first wash is where the unexposed sensitizer leaches out, so its bath is the dirtiest whatever it starts as; reusing filtered Brown there and finishing on two clean Blue washes is the counter-flow order. Blue use per print is unchanged (still 2 Blue washes), so every print count holds. The first print after a resupply finds IBC-3 empty and runs wash 1 on Blue, which doesn't change the count. Cascaded through `tbs_constants.py`, the water-system report (§1–§4), the cost breakdown, the water.skp description (now built from the computed constants instead of a stale hand-typed blurb), and the **operating manual**: §4.2 wash steps reordered (P-02 Brown pass first, then P-01 Blue ×2), the valve matrix re-columned, and the DV-01 decision corrected. The manual had DV-01 returning filtered water to Blue IBC-2 at pH 6.5–8.0; it now returns to the IBC-3 Brown buffer at pH 6–7, matching the schematic and the plumbing report. Daily-energy endurance table: the stale "~620 Wh" per print now injects the energy model's `per-print-wh`.
- **Water-system report — editorial pass; every water figure now computed and injected.** The report still carried values from an older 16-gal-per-wash model (16/32/48 gal, "14-print run", "9–14 prints on fresh Blue alone", "~40%" recycling gain) while the model computes **15 gal/wash, 30 gal net Blue, 10 prints without recycling, 15 with, +50%, ~17 at max fill**. New computed constants + facts (`PRINTS_NO_RECYCLE`, `RECYCLE_SUPPLY_GAIN_PCT`, `PRINTS_MAX_FILL`, `IBC_CAPACITY_L`, `BLUE_PER_PRINT_L_R`; facts `tray_flood_gal`, `blue_per_print_gal`, `blue_per_print_l`, `prints_max_fill`, `loss_per_print_l`, …) now inject them, and the same stale figures were fixed in the daily-energy report, operating manual, and cost breakdown. Subtractive pass (~2:1): pipe sizing → Plumbing §5, per-print pump energy → Daily Energy, filter housing/intervals → Plumbing §3.1/§10, coordinate position table + duplicate floor plan → Equipment Layout, the hand-summed (and stale) cost table → Project Cost Breakdown §5, supplier list → Master Shopping List. Fixed contradictions: the Brown reuse rule now says wash 2 (was "first wash"), DV-01 recycles to the IBC-3 buffer (not "back to Blue"), the safety note no longer says the pumps run one at a time (supply + drain run concurrently on C1/C2), and fact placeholders no longer sit inside code fences (where they rendered as raw comments). Section numbering kept; inbound §-pointers in 6 reports re-checked and corrected.
- **Equipment-layout report — editorial pass: refocused on *why each zone exists + what is placed there*, cut the duplication.** The report is the shadow-free *positional* rationale, so it now states only what goes in each zone and why, pointing to the floor-plan diagram (the to-scale layout of record) for positions instead of restating them. Dropped the four §2 coordinate tables (the floor plan carries them), the §5 IBC-frame design spec + supplier list (owned by the [IBC Stacking report](docs/ibc-stacking-report.md) + the master BOM — point 3, "no parts list"), the §8 water-capacity summary (system *capability*, owned by Water System §4 — point 5), and the §10 parameter recap (restated §1 + the diagram — point 7). **Egress** moved to its mechanism's owner: a new **hinged-panel §4.4 (Emergency Egress — Path Clearance)** consolidates the path-clearance proof with the panel-swing / drum-jam mechanism that report already documents (point 6). Net **11 sections → 5** (zones · zone-by-zone layout · line-of-sight · transport-mode positions · references). Fixed the orphaned inbound §-pointers across 8 docs (container / electrical / ibc-stacking / light-trap / weight / ventilation / cost-breakdown / dependency-map) and removed the now-redundant `eq-ibc-frame-cost` costing block (ibc-stacking already owns the frame band via `ibc-frame-low/high`). Surfaced a **new BOM requirement** (point 4, in TODO.md): tag each `parts.py` part with its layout **zone** and add a left / right / center / pinhole-wall filter to the Master Shopping List, mirroring the existing system filter.
- **Diagrams must be authored in millimetres — new lint GATE, and Ventilation Sheet 4 rebuilt mm-native.** The Fan-A grille fab blueprint (Sheet 4) had been drawn in an arbitrary 24×14 data-unit canvas with a scale factor (`sc = 0.019`) and fractional coordinates — a deviation from every other sheet, which draw directly in mm. Rewrote it mm-native (frame 320, Ø150 bore, M4 pitch 100, TEK pitch 145, section at x=560; front view 1:1, the 5 mm section thickness exaggerated by an explicit named `T_EXAG = 9` stated in the scale note), which also removed the hand-tuned dimension offsets. Codified the rule as a **HARD RULE in CLAUDE.md** (Drawing Style Conventions) and a **`lint.py` GATE** (*diagrams authored in mm (no canvas scale factor)*) that flags any `def f(mm)` coordinate helper shrinking mm by >5× (literal or via a small-float variable), while leaving legitimate thin-section exaggeration (`mm*3`) and mild compression (`mm/1.35`) alone.
- **Ventilation Fan-A grille — added an exterior aluminum mounting frame for the corrugated wall, with its own fab blueprint.** A flat louvre grille can't seat on the corrugated end wall (it only touches the crests, leaving gaps over the valleys), so the grille now mounts to a flat **6061-T6 aluminum frame (320×320×5 mm, Ø150 bore)** on the exterior face. The frame is **#14 TEK self-drilled to the corrugation crests — outboard of the grille** so the screws drive from outside — and sealed over the valleys (no through-bolt); the grille fixes to the frame with **4× flat-ended M4 screws into tapped holes** — the tap may break through; the screw is short so its flat end can't project past the frame's back face onto the wall. Fan B is unchanged (flat plywood). Registry part `fan-grille-al-plate` (+$20/$40 ventilation); cascaded through costing (§5b · EXPECTED ventilation **→ 788 / 828** · grand total **→ $27,814 / $32,679 / $39,574**), the ventilation report §4.2, Sheet 2 (assembly), and a **new Sheet 4 — the frame fab blueprint** (front view + section · M4 blind taps + Ø5.5 TEK clearances · monochrome; registered in publish/setup/gallery/deps). Part of the corrugation-rendition sweep: **pinhole-disc-holder Sheet 3** was also updated (drawing only) to show the trapezoid flute with the Ø240 adapter welded to the crests, instead of a flat slab.
- **Electrical Sheet 9 — the container-wall corrugation is now drawn to-scale as a trapezoid, not a sharp peak.** The wall-securing detail (Panel B) drew the corrugated side wall as a triangular sawtooth, so the flange appeared to seat on a *point*. Researched the real ISO-typical side-wall profile (manufacturer trapezium: crest 72 · web 68 · valley 70 · depth 36 · pitch 278 mm; ISO 668 standardizes sizes, not corrugation geometry — so it's typical, not universal) and rebuilt the section to a true 1:1 trapezoid with flat crests and flat valleys, depth = the project's `CONTAINER_CORRUGATION_DEPTH` (30 mm). A **valley is centered on the mounting bolt** so the interior backing plate bears on the valley's interior face and the bolt grip spans the full corrugation depth (per the design); the flange seats on the flat 72 mm crests above and below and bridges over the valley (flashing/silicone fills the gap). Fastener thickness stays exaggerated; the profile is dimensioned on the sheet. **Sheet 6** (penetration box) had the same zigzag and got the same trapezoid treatment (a pitch-compressed schematic flute, since its wall bands are too short for the to-scale 278 mm pitch). A cross-generator inventory confirmed these two were the only sharp-peak corrugation drawings; everything else is a flat slab labeled "corrugated" (no profile) or, in walkway Sheets 2/7, a square hollow-rib box — both tracked in TODO.md as optional follow-ups.

- **Report-wide parts reconciliation sweep — every engineering report now links to its filtered slice of the Master Shopping List, and 5 parts named in reports but missing from the registry were backfilled.** Each report's §Parts-List was audited against the single-source registry for completeness (the electrical §8 precedent, applied across all systems). Unlike electrical §8, the other reports' parts tables were already registry-injected (no hand-keyed drift) — but the reconciliation surfaced **5 genuine registry omissions**, each a discrete item a report names but the registry never carried: **spray manifold cushioned pipe clips** (+$8/$15), **IBC-2 Blue-supply low-level float switch** (+$8/$20), **IBC front-bar L-cleat angles ×8** (+$6/$20) — all in §5 water system — plus **weatherproof fan louvre grilles ×2** (§5b ventilation, +$20/$40) and the **right-walkway grating-bearer L-angle** (§6a, +$25/$75). Project TOTAL **+$67/$108/$150 → ~$27,799 / $32,664 / $39,559**. Every report's `## Parts List` now opens with a pointer to its **[Master Shopping List filtered view](master-shopping-list.md?system=…)** (multi-system reports use the comma-list filter, e.g. `?system=tray,spray`). Reports with no gaps: hinged-panel (4 blocks), film-plane, clamp, front-board, chemistry-prep-shelves, processing-tray. **ventilation-report §9** was then fully consolidated to the electrical-§8 pattern — the embedded `parts:ventilation` table dropped in favor of a reference to the filtered master BOM (its cost band stays in costing §5b); `ventilation` + the stale `electrical` entry removed from `parts.py` `SYSTEM_DOC`. The **same consolidation was then applied to all remaining reports** (water-system, plumbing, processing-tray, ibc-stacking, walkway, film-plane, film-clamp, pinhole-disc-holder, hinged-panel, chemistry-prep-shelves): every embedded `parts:<system>` table dropped in favor of the filtered-master-BOM reference, so **no report embeds a per-system parts table any more** (`SYSTEM_DOC` is now empty; the two plumbing panel sub-lists retired). Cost summaries (processing-tray, ibc, hinged-panel), film-plane's wall-seat-saddle / muslin-clamp / sourcing design content, and all cross-references were preserved and fixed (the ibc report now links to `?system=ibc-frame,water` so the totes surface; empty parts-subsections removed and the surviving cost tables relabeled). Per the owner's call the brochure PDF is left as-is: **the Project Cost Breakdown page (already in the brochure) is the PDF's parts/cost coverage** — it carries the same section- and subsystem-level costs and names every major component, so the itemized master BOM (SKUs, suppliers, per-part quantities) is deliberately kept **web-only** for the builder/buyer rather than added to the prospectus. (Brochure-parts decision closed.) Cascaded through `parts.py`, `costing.py` (WATER/WALKWAY/VENTILATION lists + EXPECTED water/walkway/ventilation/grand_total), and the scenario / funding / cost-analysis / master-summary injections. The reconciliation also **resolved the walkway standard-bracket count drift**: the registry/cost side was deliberately 11 (3 near + 8 far, per the 3D station math) but the walkway load-analysis generator (`walkway_load.py` §10.1/§10.4/§10.5 blocks) and the `costing.WALKWAY` labels still read 13/×59 — now propagated to 11/×53 everywhere, which surfaced a stale fastener count (the cantilever bolts had been corrected to 53 but their nuts/split-washers were left at 59 and flat washers at 236): fixed to 53/53/212, **−$5** (net sweep total therefore **+$62/$103/$145 → ~$27,794 / $32,659 / $39,554**). **Open (tracked in TODO.md):** the brochure PDF does not carry the full by-type BOM, so electrical/container/interior/optics parts are absent from the PDF — a decision on whether to include the Master Shopping List in the brochure.
- **Electrical §8 parts list de-duplicated, a missing part backfilled, and the Master Shopping List gains a system deep-link filter.** The electrical report's hand-keyed **§8 parts table** — a drift-prone second copy of the parts registry (its prices had already diverged, e.g. the cooler inverter at ~$210 vs the registry's $132.60) — is replaced by the injected cost summary plus a link into the **[Master Shopping List filtered to the electrical system](master-shopping-list.md?system=electrical)**. Reconciling §8 against the registry exposed one genuine gap: the **inverter DC protection** (40 A ANL fuse + holder + dedicated DC disconnect on the Circuit-E inverter feed, **$40**) was listed in §8 but never in `parts.py`, so the electrical total under-counted a part **required by the Electrical Safety Report §7.6 rule 4**. Backfilled into the registry → electrical system total **$3,432 → $3,472**, systems grand total **$3,930 → $3,970**, project TOTAL **+$40** ($27,732 / $32,556 / $39,409). Separately, the BOM tables were already click-sortable; added a `?system=<a>,<b>,…` query-param **filter** to the tablesort init so a report can land the reader on just its slice of the by-type BOM (collapsing the empty type sections — fixed so Material's runtime table wrapper collapses too, leaving no empty gap). The Master Shopping List also carries an **on-page multi-select chip bar** (built from the systems present in the tables, so it never drifts) to add/remove systems without leaving the page; chips read and rewrite the same `?system=` param (OR-matched, shareable, no reload) — JS bumped to `?v=6`. Cascaded through `parts.py`, `costing.py` (Distribution line · §5a · EXPECTED power/grand), the scenario / funding / cost-analysis tables, and the master summary.
- **Circuit C split into two independently-fused pump branches (B′) — enables a continuous flow-through wash.** The tray-drain pump (P-04) moves to its own fuse **C2** (10 A / 16 AWG), separate from the corridor pumps **C1** (15 A / 14 AWG), so a supply pump and the drain can run concurrently without any fuse at 100% of rating. A single **2-pole (DPST) master pump switch** still kills every pump in one throw — each pole carries only one 7.5 A pump, so nothing is uprated. Blue Sea 5026 goes 6→7 used. Cost **+$5** (single-pole → 2-pole switch, $7.99→$12.99); electrical system total **$3,459→$3,464**. Cascaded through the power budget (§3, peak 463→543 W), circuit list (§7.2), §7.3 wiring, parts/costing/shopping, the fuse-schedule + one-line + schematic diagrams (sheets 1/4/5/7), and the operating-manual fuse check. The 3D fuse-block re-send (electrical/overview/construction/water) is **pending** — tracked in docs/TODO.md. The wash **procedure** stays the fill-then-drain cycle; adopting continuous flow-through is a separate operating/water change (needs the water report's hydraulic sign-off that P-04 holds the tray level).
- **Film-plane electric actuation removed from the design (Circuit F retired).** The optional PA-14 motorized-corner upgrade is dropped project-wide — the film plane is positioned manually only. *Electrical:* the actuator circuit is gone from the §3 power budget (peak **533 W → 463 W** — the 533 was also stale, pre-106 W white LED), the per-session energy table, and the §7.2 circuit schedule; the remaining circuits are **renumbered contiguously A–F** (the white-LED circuit, formerly **G**, is now **F** — no gap), and the Blue Sea 5026 block is **6 used / 6 spare**. Per-session consumption recalculated **845 → 837 Wh** (the 8.3 Wh actuator line removed), and the stale §3.1 continuous table reconciled to the 106 W white-light figure (792 + 45 = 837). *Cost:* the actuators were never in the electrical BOM, so the electrical total is unchanged; removed the cost-analysis §4 lever #2 (this unbanks the **$827** documentation only — not in the roll-up, no total change) and renumbered the remaining levers, the project-cost-breakdown §4.4 PA-14 upgrade table, and the master-shopping optional add. Cascaded through `calculate_energy_budget.py`, `generate_electrical_diagram.py` (sheets regenerated), `generate_electrical_model.py`, `parts.py` (12 AWG spool relabeled F→G), `costing.py`, and the operating manual. The 3D re-send (electrical / overview / construction / water drop the Fuse-F block) is pending the live SketchUp session (TODO).
- **IBC frame joint marks — renamed the opaque `J1–J9` scheme to human-descriptive marks.** The §3.5 fastener schedule and every reference now use part-grouped marks: **FA1/FA2** floor-anchor, **BC-C/BC-W** front bar-cleat (corridor/wall), **WH** wall-hanger, **CJ** cantilever-arm joint (walkway↔upright), **RP1/RP2** rear panel, **SP1/SP2** side-panel pipe-run. A reader identifies the joint from the mark; the schedule carries a one-line family legend. The rename also resolved a latent collision — `J1–J5` was reused, unscoped, by the film-plane corner gimbal — by moving the IBC marks off `J` (now unambiguously film). `CJ` was chosen over `CA` to avoid colliding with the ~22 "California" tokens in the supplier lists. Cascaded through the 2D IBC drawings + plate-schedule + load-case diagrams, `parts.py`, `costing.py`, `master-shopping-list`, the walkway cross-refs, and the 3D model part-names (re-sent to Sketchfab: water, overview, ibc-stack, construction, walkway, film-plane-mechanism); dated change-history (RELEASE.md, costing notes) left as archival.
- **System-report reconcile — swept the ~24 published engineering reports against the current design.** An audit (6 parallel passes) found drift clustered in a handful of reports, now fixed: retired parts/mechanisms still named (processing-tray's 7-feed manifold → single center feed + 26→43 nozzles; the retired tilt-swing board → pinhole disc holder in the weight report; walkway "U-clamps" → J6 end-plate; "4× Southco" → 2× McMaster 1619A74 cam latches); cross-report spec drift (shade cloth 80→70%, EMT 1.5"→1", battery "2-pack standard"→1-pack, pump-panel labels, chem-shelf basis, chem-shelf deck 130→140mm, tray cost/finish, film-plane left rail X150→X260); plus content adds (apron-strip removal in the transport sequences, the beam-notch EPDM seal row). Two diagrams regenerated at the source — spray-bar Sheets 7+9 (single center feed) and the walkway-sections (the ribbon cross-brace corrected 40×10 → 25×3 flat bar across the 2D **and** the 3D water/overview/construction models). Fixed three stale `tbs_constants` inline comments and two stale memory notes the audit exposed.
- **Fastener standardization — a consolidation pass (−2 SKUs, 64 → 62).** Merged the two duplicate M8×25 **304 SS** rows onto one SKU (92314A711, pack of 50 — the ICP-14 rail-fixing folded off the retired steel 91310A535, upgrading it to SS for the wet film zone; 40 on one pack) and the dry M8 flat washer onto the film SS washer 98689A673 (retired 91166A270; 36 on one pack). Net cost −$7 (film −$8 / shelf +$1); grand total → 27,709 / 32,533 / 39,387. (The 10 remaining no-SKU rows are all brackets/clips/door/strap items — the firm-at-build class.)
- **Cost-analysis bucket B closed as COMPLETE.** The §4 savings-lever roll-up and both still-available levers (container grade = computed CW−WWT, solar = drop 1× 200W panel) already derive in `costing.py`, and the phantom battery lever (moot — the standard is already 1×100 Ah) was already dropped — bucket B's substantive goal was met back on 2026-07-05 (a stale memory had it flagged open). Reframed the lingering "STILL OPEN" comment + the §4 derivation note: the decided levers (tray, battery, valves) keep their saving as a declared estimate band **by design** — each is a path not taken, so pricing a full alternative would single-source a figure for an option that won't be built. No cost or figure change.

## [0.19] — 2026-11-08

- **Light-trap bottom light seal redesigned as a PULL-OUT CORNER APRON** (replaces the fold-down apron). A **fixed full-width base** (floor → drum cage, never moves) closes the center; the two corner zones are closed by **removable pull-out strips** that locate in a 45° chamfer seat at the bottom and butt the swinging leaf's exterior lip at the top. Each strip is held by surface draw latches — two interior, at the strip↔base joint, and two exterior "span" latches bridging the leaf lip batten B1 and a new strip batten B2 on the door side (kept off the interior face so nothing projects into the darkroom and fouls the left lift-out film beam). For transport the strips lift off and stow inside, so the panel swings through the empty corner. Cascaded across hingepanel Sheet 16, the 3D model, parts/costing, the plywood cut sheets, the operating manual, and `hinged-panel-report.md`.

- **3D — overview + construction now carry the full detailed cargo-door panel + apron** (matching lighttrap), routed through the existing `panel_pivot()` aggregation; removed the retired piano-hinge geometry; the 1619A74 cam-latch handle now renders as one continuous L (added a `ruby_sphere` elbow). All three `.skp` regenerated, saved, and pushed to Sketchfab in place (same URLs); manifest current.

- **Light-trap 3D context floor** re-datumed to the true cargo-door closing plane (`DOOR_HINGE_X` = −85), so the door frame + apron read INSIDE the container end and the drum bay reads as the deployed external light-lock vestibule. Floor-only — any wall/ceiling ghost intercepts the panel-swing dynamic component.

- **Light-trap 2D fixes + a real light leak closed.** Sheet 4 shell→cap lap corrected (laps flush at the 25mm rim lip); Sheet 10 Detail B redrawn for the beam-through-notch geometry; and a **closed-cell EPDM foam light-seal added at the 4 axle-beam wall penetrations** (new `ll-beam-notch-seal` part, Sheets 2/9/10 + 3D geometry) — the notch had none.

- **Operating manual — reconciled to the current design, with a new living-procedure rule.** Added the pull-out apron to the setup + transport procedures; fixed stale panel-latch callouts; corrected the electrical drift (added **Circuit G** white LED lighting + pump **P-05**, removed the nonexistent "Circuit D white mode"); corrected the **cooler carry-weight** (Hessaire MC18M is **16 lb ≈ 7 kg**, not 20 kg — [datasheet](https://www.alphachooser.com/air_conditioners--hessaire_mc18m--air_conditioner-specs-and-profile), now single-sourced); and reworded the shutter step (sliding plate, no position indicator). Added a **CLAUDE.md HARD RULE** — a design change that affects operation must update `operating-manual.md` in the same work.

- **Audit tooling hardened — three drift gates.** (1) `check_interference.py --solids` same-color interpenetration sanctioning — the whole overview set triaged **110 → 0** unexplained (welded joints, one-piece parts, bearing fits, sliding clamps, box-model AABB artifacts). (2) `--bolts` grip-bolt orientation / edge-distance lint promoted to a committed ratchet riding the interference report — every flag sanctioned with a reason, **0 open** (including the light-trap skin blind-rivets, with the construction piano-hinge pierce fixed at source). (3) `check_consistency.py` **CHECK G** duplicate-emitter coverage (name-match + geometry-equality + alias net). Plus a CLAUDE.md rule never to propose cutting a release.

- **Single-source / drift fixes.** Film-plane active area corrected **101 → 99 sq ft**, and the chemistry cost tiers now **derive** from a new `IMAGE_AREA_M2` constant (ends that drift class; budget −$20/$30/$60). Un-registered-values audit single-sourced a batch — the spray-beam span + nozzle count, pump current, Blue fill, battery energy, and ratchet-strap WLL — each wrapped as an injection placeholder so it can't re-drift.

- **Procurement — Master-BOM SKU backfill.** Added missing SKUs and prices.

## [0.18] — 2026-10-21

- **5mm fab-cut-dimension audit (all fabricated parts).** Enforce the 5mm cut rule on every fabricated part, sweeping all ~382 dimensional `tbs_constants`, the model `_CUT`/`_BLANK` dims, and the `parts.py` fab rows; the set was almost entirely compliant (on-5, COTS stock, thickness/diameter, interface-pinned). Two off-grid plates rounded: **`CARRIAGE_PLATE_H` 181 → 185** (skate carriage plate, 6mm 6061 — UP, to keep the keeper-axle edge margin) and the far-left flange-bracket flange + backing-plate pair **120×96 → 120×100** (8mm A36 — DOWN, so the TL flange top and its pivot-roof-plate clearance hold). The carriage audit also exposed a 2D↔3D divergence — the 3D corner builder drew the plate from its own ceiling-capped geometry instead of the fabricated part — now single-sourced: both 3D emitters (`corner_skate_parts` + `plane_carriage`) wired to `CARRIAGE_PLATE_W/H/T`, datum'd to the keeper row via a new `CARRIAGE_PLATE_KEEPER_EDGE` (28mm), the same 185mm part at all 4 corners. Re-sent + pushed the affected corner models; 0 clashes. Two exemptions documented in-place: the corner L-gusset (laser/waterjet DXF profile, not a saw/shear cut) and `XSLIDE_GIB_W` (stock brass flat-bar width).
- **Left-rail-move (260) stale-value cleanup (TODO #21).** Swept the pre-260 residue left in rationale comments and rendered labels (the drawings were already constant-driven, so geometry was correct): the retired bearer-beam/3-floor-leg block in `tbs_constants.py` rewritten to the current 5-floor-leg cantilever, the drum-exit punch-out and `LEFT_WK_CANT_FOOT_X0` comments re-derived; the LDPE manifold ends in `processing-tray-and-spray-bar.md` corrected to X=310 / X=4,599; and the walkway/spray/floor-plan generators' Detail-C header, visible labels (tray rim, floor-leg) and inline comments updated to 280/250/580/880.
- **Dead-constant sweep — resolved the 23 reserved/unused `tbs_constants` (TODO #22).** 17 dropped (dead design intent + five redundant aliases of still-used constants); 6 were CHECK-E false positives actually consumed by the facts-injection or dependency-map injectors (`EVAP_CFM_RATED`, `IBC_CEILING_CLEARANCE_MM`, `BLUE_SUPPLY_GAL`, `COLLECTION_FILL_L`, `LOST_L`, `XSLIDE_N`) — their wrong `# reserved` annotation removed and two stale comments fixed. Taught CHECK E to also scan `facts.yml` + `component-dependency-map.md`, so facts/cdm-wired constants are no longer mis-flagged; CHECK E now reports 0 dead. No generator/model/diagram changed.
- **Corner cleanup — retired the redundant Sheet 8, fixed the 4040N12 count, dropped the dead bend-radius constant.** Sheet 8 drew the U-joint through-axis along X/Z, contradicting Sheet 9 and the 3D (axis = Y), and a corrected version merely duplicated Sheet 9 — so it was retired (gap left, "OF 18" kept) and its teaching folded into Sheet 9, with its J1/J2 cross-refs repointed to the Sheet 12 fastener schedule. The 4040N12 shaft-support count went 2→1 per corner (only the input stub needs a support — matching `parts.py`, the report, Sheet 9, and the 3D), and `CORNER_PLATE_BEND_R` was confirmed dropped (a flat L-gusset has no bend).
- **Film-plane corner gimbal reconciled — 2D and 3D now represent the real mechanism; corner mount re-spec'd to a flat laser-cut ¼″ L-gusset.** The real gimbal mounts inboard at the film-frame corner (only the skate reaches the rail), not outboard over the depth rail as the schematic box implied. Rebuilt the shared corner builder: the U-joint is a real Belden Ø19×68 cylinder on through-axis Y with coaxial input/output stubs and 304 flat-bar cross-slides, the whole gimbal nesting within the skate-carriage depth (~87mm behind the frame, clearing the ~100mm to the container back wall — no focus cap needed). The corner mount is now a flat ¼″ 304 L-gusset with both legs coplanar in the frame plane (the bent angle's second leg fouled the carriage packaging), modeled as one L-profile; the BR depth rail now butts the IBC combined corner plate instead of passing through it. Paper reconcile across `parts.py`/BOM, `costing.py`, Sheet 16 (fab), Sheet 9 (assembly), and report prose, all moved from "stock 4×4×¼ angle" to "laser-cut ¼″ flat L-gusset"; J5 frame bolts 2→4; cost-neutral (~$25–40/pc).
- **Pinhole-disc-holder 3D — M5 → M6 component names reconciled.** The disc-holder model's thumb-screw tapped-hole and knob components were still named `M5` while the geometry was already M6 (`PDH_TS_D=6`); flipped the label/comment text, re-sent, and re-pushed in place (same UID), `source_hash` refreshed. Geometry unchanged — a stale-label fix only.
- **Plywood cut-sheet — remaining piece dims single-sourced + two board sizes reconciled.** Every cut-sheet piece now shares one source with the generator that draws it: the shirt standoff cleat (40×720) derives from new `SHIRT_CLEAT_*` constants, and the pinhole backing height from a new `PWP_PANEL_H=1,440` both the `water` model and registry read. Two drifted registry dims corrected to the authoritative drawing — center baffle 1056×217 → 986×130, EP electrical backboard 700×2000 → 364×1424. Confirmed the evap-cooler stow base's transit location and fixed its stale "cargo-door end" note. Models byte-identical (no re-send); schedule still nests to 4 sheets / 47 cuts, no cost change.
- **Corridor/light-trap panel drift reconciled — one size per board across cut sheet, 2D, and 3D.** Reconciled board dimensions that diverged between the three places they're drawn: `panel_layout.py` (fully hard-coded and stale vs the 3D) now derives from `generate_corridor_water_panel` — rear-panel top 2,246 → 1,900, shirt 25 → 18mm, spine end 5,560 → 5,780, pump-run Z corrected, with the restating notes/labels converted to f-strings; the pinhole-wall ply backing now reads `PWP_PANEL_*`; the pivot stub cut size 200 → 125mm (the `corridor-panel-ply-25` key, actually 18mm, renamed to `corridor-panel-shirt-ply`); and the center light baffle 3D extent corrected to Z0→130 (full floor→cage). `lighttrap.skp` re-sent + re-pushed in place.

## [0.17] — 2026-10-19

- **Chemistry prep-shelf blueprint closed out.** Added the datum and general-tolerance block to the two fab sheets (datum A = board back/hinge edge, B = left edge; ±0.2mm holes; deployed level ±1mm over the 225mm depth) so the set meets the manufacturing-ready standard, and resolved the four open review decisions — HDPE spill lip on all four edges, UV-coated white-ply face (retiring the stale "phenolic" prose), the reused cam latch, and the SS hinge screw — plus the stale "M5 → flange-bolt" TODO, superseded by the ¼-20 tee-nut redesign.
- **Diagram style single-sourced into `tbs_constants` — DPI, font, background, and the full color palette.** Every generator had been copy-pasting its raster DPI, font dict, page background, and `C_*` palette colors as local literals — the structural source of "restated value drifts." All now import the one canonical value, so a style change can't diverge across the set. Resolved the shades that had already drifted (container wall, steel, dimension text, …) to a single value each, and added a non-blocking `lint.py` advisory that flags any new local palette redefinition the moment it lands. Also corrected the stale `X=150` optical-left-edge value to `260` — including two callouts that printed the wrong boundary on the drawing, now interpolated from `RAIL_X_L` so they can't re-drift — and hoisted the duplicated container dimensions onto `C_LEN`/`C_WID`/`C_HGT`.
- **Repository reorganized — one home per file, co-located with its tooling.** The project root is now config plus the three repo-meta files (`CLAUDE.md`, `README.md`, `RELEASE.md`) only; everything else moved to where it belongs. All Markdown sources → `docs/`; all 162 tracked images → `docs/assets/`, co-located with the docs that cite them as `assets/<name>` so GitHub renders them in-repo and PR review works (which broke once the `.md` moved); `dependencies.yml` → `src/generators/` beside its loader; `requirements.txt` → `src/`; the three shell scripts → `scripts/`; `interference-report.txt` → `src/models/` beside `check_interference.py`; and `parts-worklist.csv` → `src/generators/` beside `parts.py`. Every move is a git rename — single-source intact, the generator stays each diagram's source of truth — and the generated brochure PDFs now write straight into gitignored `published/assets/` instead of loitering at root. All path-dependent tooling (`publish.sh`, the injectors, `setup_docs.py`, `lint.py`, `deps.py`) was rewired; publish still ships only the registered subset.
- **3D-model palette unified + in-model credit URL updated.** The SketchUp material colors that shadowed the 2D palette now import from `tbs_constants` too, so steel/aluminum/film/pump/fan are one value across 2D and 3D.
- **Diagrams moved onto the shared drawing helpers, plus a blueprint-polish pass.** Refactored more generators (line-of-sight, floorplan, joint-study, tray-slope, light-trap, portrait) off raw matplotlib onto the `tbs_drawing` leader/dimension/rect helpers, so they gain the house ticks and styling. Fixed collapsing title blocks on the tray-slope and light-trap sheets, swept loose annotations onto the bordered NOTES style across the electrical sheets, corrected fittings and callouts on the panel-spine and weight-analysis sheets, and rebuilt walkway-sections Sheet 4 as a faithful corridor-plumbing elevation captured live from the `water.skp` builders so it tracks the 3D model.

## [0.16] — 2026-10-13

- **Custom domain + analytics.** The site now serves at [thebigshoebox.org](https://thebigshoebox.org) (apex) — the old `alvinr.github.io/tbs` project URL and `www.` both 301-redirect to it, with HTTPS enforced. A committed `CNAME` is carried into the build by `publish.sh` so `gh-deploy --force` can't wipe it, and `site_url` / `SITE_URL` / the brochure footer / README / funding proposal all point at the new domain. Google Analytics 4 (`G-5GT2XBPGV9`) was added via Material's native `extra.analytics` config, so the tag renders in every page's `<head>` (all 50 pages).
- **Floor-anchor sub-plate (strongback) — new project-wide floor-fastening standard.** Container floor cross-members aren't dimensionally standardized ([ISO 1496-1](https://law.resource.org/pub/us/cfr/ibr/004/iso.1496-1.1990.pdf) only caps the spacing), so feet/legs can't be bolted straight to a member. Each floor-fastened system now bolts up into tapped bosses on a shared steel **sub-plate** laid on the floor and self-tapped (winged #14×3¼″ 410-SS) into whatever cross-members + door sill it spans — drive-from-above, no underside access; plate size + TEK count are finalized on the acquired container. IBC frame (**J1**): the 4 feet bolt to one plate; walkway floor-legs (**WF4**): one continuous plate under the 5-leg line. A new single-sheet `floor-anchor-map` diagram (cross-member map + sub-plate footprints + section stack + container-dependent note) is embedded in the IBC-stacking (§3.4a) and walkway (§5.1a) reports with the research sources; the winged TEK carries a firm supplier SKU; the construction sequence stages the plate as its own Phase-1 step (1.7) ahead of the cantilevers that bolt to it (3.7); and the owning IBC Sheet 1 foot callout gained its missing J1 mark.
- **Film-plane corner mechanism + water routing (3D).** Coped the TR saddle-seat corner clear of the swing-drive input stub (~5mm) and terminated the SWING cross-slide at the wheel-channel opening — both were overshooting the structure. Single-sourced the captured-skate carriage into one `corner_skate_parts()` builder shared by the install and Movement scenes (the demo had been missing the wheel axles, keeper rollers/axles, retainer bolts, and cam brake), and regrouped/ghosted the Movement pivot hardware so the articulation reads cleanly at angle. The blue supply trunk's drop moved to the ribbon slot, past the tray edge, so it no longer falls over the open tray basin.
- **Fabrication blueprints — last gaps closed.** Added three monochrome, fully-dimensioned shop sheets to the spray-bar set : the beam + manifold station layout, the wheel-carriage plate (6061-T6), and the 304-SS processing-tray pan — each with a datum/tolerance block, so all three fabricated parts now have shop-ready drawings. Reconciled the stale numbers the 2026-08-11 left-rail widening (FP_X_L 150→260) never cascaded into prose/parts — nozzle count 44→43, beam span 4,399→4,289mm, panel 2,195mm, sump 180mm — plus the matching inline `tbs_constants.py` comments and the spray-bar cost line. The chemistry-prep-shelf 5-sheet set was verified complete and current.
- **Diagram polish + label-overflow accuracy.** Rebuilt the `tidy_labels.py --overflow` check to measure each label against the figure-canvas edge (the real clip boundary) and skip `bbox_inches="tight"` saves, which can't clip — cutting false positives from ~136 to a handful of genuine clips, all fixed (IBC Sheet 1 margins widened; tray-slope + GRP cut-plan given tight saves; the set now reports zero canvas clips). Blueprint follow-ups from the all-systems audit: the routing-sections denominator "OF 5" → "OF 6", the pinhole-disc carrier Ø6 light bore dimensioned (new `PDH_CARRIER_BORE`) with its scale note corrected, a "Conatiner" typo fixed, and self-contained tolerance / clearance-drill notes added to the film-plane fab sheets (13/14/15/16/18).
- **Tooling — model-aggregation ratchet completed.** Added the `lint.py` `gate_overview_aggregation` gate that locks the overview model to its sanctioned aggregator/container/composition builders, so it can never silently re-grow an owned builder and drift from its sub-model (the Cct-E / Cct-C class of bug) — completing the aggregation plan begun in 0.15.

## [0.15] — 2026-10-08

- **Overview collapsed to a thin aggregator (model refactor).** Shared Ruby-drawing infrastructure (primitives, 38-color palette, model metadata) was extracted to a neutral `tbs_draw.py`, and ~60 geometry builders moved from the overview into their owner sub-models (walkway, IBC, spray-bar, electrical, water, film-plane, light-trap). The overview is now ~13 container-level builders composing those sub-models, so each component lives in exactly one place and the overview can't drift from its parts. See [model-aggregation-plan.md](model-aggregation-plan.md).
- **Electrical model de-drifted + single-sourced (3D).** Every circuit traces from its own colored fuse to its load through single-owner `em` builders — the Cct-C pump distribution, the Cct-E/Cct-C EP feeds, the lighting fixtures + pull switches, the evaporative cooler, and the Fan-B flex were each formerly duplicated between the overview and electrical and are now unified (fixing several drifted positions and a disconnected conductor). Added an EP control-panel redesign (two full-width ply cross-members, surface controls wired from the rear) and external-EP inner-face MC4 string landings. `check_interference` gained conductor-skip + shared-junction fixes that surfaced real crossings; all models now run **0 pipe crossings**.
- **Circuit-G work lighting — corrected + rewired.** The illuminance was restated from bare lumens ÷ area to the honest **maintained ~330 lux** (coefficient-of-utilization + light-loss-factor on the matte-black interior, which adds essentially no inter-reflected light); the design is **4 COB runs** (3 over the tray + 1 corridor) rewired to **12 AWG on a 15A fuse** (led-channel 6→7).
- **Water/plumbing pipe supports + routing (3D).** A full support audit added **P-clips / saddle straps across both plumbing panels, the corridor skid, and the electrical runs** (→ 87 pipe clips + 58 conduit clips; `check_interference` now treats a clip as intended pipe contact). Routing was cleaned up: the tray-sump suction and DV-02 waste rerouted up/around the pinhole wall and over the IBC frame rails; the corridor skid boards raised with the suction valves dropped + rotated into the corridor; grate pipe-clearance cutouts added; and the right-walkway outer beam split into two simply-supported segments over an open corridor bay (no section-gutting notch). 0 crossings across models.
- **Structural — IBC frame + cantilever details.** Front foot plates trimmed off the tote footprint; the front bottom ring-rail lowered + narrowed so the blue trunk clears and the foot bolts straddle it; half-lap hold-down TEK screws seat flush on the arm; the two-segment outer-beam check holds (SF 7.1).
- **Procurement + BOM.** The `interior-ventilation` allowance retired as a double-count of the itemized darkroom ventilation; the Belden U-joint, the pre-keyed 316 rotary shaft, and the square key firmed against datasheets; McMaster/Grainger fastener SKUs locked; plywood consolidated into one cut-sheet schedule + MAXRECTS nesting ([plywood-cut-sheets.md](plywood-cut-sheets.md) — 4 stock sheets, 2 grades, −$148); the parts worklist is down to its last open rows.
- **Diagrams + docs.** Gallery-only diagrams cleared **9 → 0** (each embedded in or homed to an owning report); the three portrait diagrams refreshed to the active film plane (4,389 × 2,094mm, pinhole X=2,454, ~86° × 48° FOV) with a new `portrait-photography.md`; the superseded `film-corner-gimbal` diagram retired in favor of the off-the-shelf U-joint corner; a new Construction nav group added.

## [0.14] — 2026-09-30

- **Hingepanel blueprint review (rounds 1–7).** Reviewed and refined all 17 sheets of the hinged light-trap panel — geometry, dimensioning, labels, cut/section details, and standardized note blocks (`draw_notes`).
- **Electrical penetration box — fabrication blueprint (Sheets 8 + 9).** Added two monochrome single-part fab sheets for the flanged wall-penetration box — a dimensioned face-plate cut layout and a box assembly + wall-mount section — each with a material/finish/tolerance block; corrected a stale §5.4 note (set renumbered to "of 9").
- **Electrical Sheet 8 dimensioning + witness-line convention.** The face-plate fab sheet now traces every stacked dimension to its feature with a dotted witness line, and locates cutouts by edge-distance + internal W×H (round holes stay center-located); the convention was added to `CLAUDE.md`.
- **Diagram-usage audit — every diagram now lives in an owning report.** Mapped all 150 generated PNGs to the reports that embed them and placed the 13 that were gallery-only — headlined by eight film-plane fabrication-detail sheets into the film-plane report, plus the joint studies, Mini-TBS, and the pinhole-wall elevation by kind.
- **Transport-stay lock reworked.** Spread the two wall stays to the frame limits (Z310 / Z2210 → a 1,900mm operator passage) to open the egress gap and lower stay tension; shrank the anchor plates to 150×150 (4× M16 on a 90mm square); and retargeted the plate clamp to the EP plywood backing, opening clearance from a 3mm near-touch to 30mm.
- **Swung-panel door clearance corrected (+59mm → +29mm).** Now measured to the *closed cargo-door inner face* — the ~60mm door leaf sits +30mm inboard — via a single-sourced `CARGO_DOOR_LEAF_T`; the panel still clears, but the headline no longer overstates it by the door thickness.
- **3D drift fixes — cargo panel + tray sump (overview + construction).** Reconciled two overview-model drifts to the light-trap model: the cargo-door panel now draws the correct stepped 40/120 envelope (corner zones + Fan-B band = `PANEL_CORNER_T` 40mm, not the 120mm center thickness they'd drifted to), and the tray-sump pickup moved to Yd104 (`PWP_FILTER_YD`) so it sits under the riser and clears the blue trunk. Cascaded to overview + construction.
- **Construction report reconciled to the 3D model.** Corrected Phase 4/5 step drift (E-stop installs with the interior panel; added the missing Fan-B / chem-shelf step; the light trap split into drum cage / HDPE skins / outer surround + spray bar) and fixed four typos.
- **Sketchfab first-upload papercut fixed.** `push_sketchfab` no longer stamps an all-zeros placeholder uid (which made a brand-new model's first upload fail), and it re-syncs the model title/description to the generator unless they were edited in the Sketchfab UI.

## [0.13] — 2026-09-25

- **Disc holder — buildable 4-sheet drawing set + interactive 3D model.** TBS-PDH: **Sheet 1** general arrangement, **Sheet 2** fabrication blueprints (plate / retaining ring / carrier, fully dimensioned), **Sheet 3** the wall-frame adapter + a section through the container wall (the mount, weld, bolts and the carrier/ring/seal stack), **Sheet 4** the Copal/Compur lens board with a lens cross-section (a straight barrel + integral flange through the board hole, a rear retaining ring clamping the board, glass elements at the barrel ends). CNC-shop tolerance block on the fab sheets.
- **Front board: a fixed pinhole disc holder that also takes large-format lenses** (replaces the tilt-swing front standard and the separate Ø600 pinhole/lens plate). A pinhole is a point aperture — turning or tilting the board only moves where the image lands, it gives no perspective control (that lives in the film plane) — so a movable front standard buys nothing. The front board is a simple **Ø180 × 18mm** plate: a Ø110 scene-side taper narrows to a **Ø72** aperture, and a **Ø82 × 6mm** seat holds an interchangeable **Ø80 × 5mm carrier** — a pinhole board (SS-302 shim, Ø2.17 / 1.5 / 3.0) or, when a sharp controllable optic is wanted, a **Copal/Compur 0/1/3 lens board** (34.6 / 41.6 / 65.0mm holes). A neoprene washer light-seals the carrier; a **Ø120** retaining ring on **4× M6 knurled thumb screws @ Ø100** clamps it for a tool-free 30-second swap; the plate bolts (4× M6 @ Ø150) to a **Ø240 × 6mm** steel wall-frame adapter welded over the corrugation. Front-board cost **$305–$636**.
- **Release + drawing-skill tooling hardened.** `release.sh` no longer aborts at its confirmation
  prompt when run without a TTY (tool shell / CI / pipe) — it proceeds automatically there, still
  prompts an interactive terminal, and honors `RELEASE_ASSUME_YES=1`. The 10-day "Tidy labels" run
  was mined for gaps the drawing skills didn't cover: `skill_diagram_structure.md` gained "write
  label code to be hand-editable" (explicit per-label calls, no placement loops or wrapper
  forwarders) and "current-design-only / single-part-monochrome" content rules, and `tidy_labels.py
  --check` gained two flag-only rules — a dimension baked into a label string that equals a constant
  (the string-embedded hardcode `lint.py` can't see) and a `RETIRED`/"for reference" archaeology
  label.
- **Chem-shelf 3D re-send completed.** The 0.12 chem-shelf redesign (steel frame → 18mm ply-primary,
  1/4-20 tee-nuts, chain stays) had its overview/construction `.skp` re-send deferred; both are now
  re-sent, re-uploaded to Sketchfab, and committed, so the 3D matches the shipped 2D/parts design.
- **Hinged-panel transport lock pulled onto its own Sheet 17.** Sheet 12 was a grab-bag; the transport
  lock now has a focused sheet — general arrangement, the **panel-side receiver lug** (a new fab detail: a
  12mm steel eye lug, Ø17 pin hole dimensioned with edge-distance + centered chain, 6mm fillet-welded to
  the stile), and the near-wall anchor — plus a full spec block. Sheet 12 slimmed to cam-latch + brush
  strip. Lug/plate sizes single-sourced (`LT_STAY_*`); parts `sp-wall-stays` lists the lug.
- **Transport-lock 3D built to match Sheet 17.** The lighttrap model now draws the leaf free-edge
  steel stile (2×2×0.120 RHS, previously only referenced by `LOCK_BOLT`) and two **receiver lugs** as
  plates at right angles to the vertical frame, welded on the **outboard face** (toward the container
  opening) so the panel still clears them when it swings — visible in both DCs. The transport stay now
  runs from the wall eye to the lug pin hole as an angled rod (eye clevis + barrel + hook clevis),
  connecting in the transport position. Lug/stile geometry cascades into `overview`/`construction`
  (both re-sent).
- **Film-plane lift-out: pinhole-end length splice now hides on swing.** In transport the removable
  film-plane beam lifts out and hides, but its pinhole-end **length splice** (the plate joining the beam,
  top and bottom) stayed visible — it was classified into the root-sibling *fixed* rig, which a swing
  `_hidden_formula` never recomputes. Added `"Length splice"` to `corner()`'s `_REM` classifier so the
  splice lifts out with the beam (a swing-DC child). `keep="all"` (overview / standalone film-plane
  model) is byte-identical.
- **Hinged-panel transport-stay wall anchor — 2D detail added.** The wall anchor was modeled
  in 3D (interior + exterior 200×200×12 plate pair + 4× M16 through-bolts) but had no dimensioned 2D detail.
  Single-sourced the plate/bolt sizes to `tbs_constants` (`LT_STAY_*`) and added hingepanel **Sheet 12
  Detail D** (plate front view + bolt gauge + plate-pair section); report §5.2 + parts `sp-wall-stays` updated.
  Also verified the cargo-door-wall EPDM/strip-brush split is consistent across report/3D/parts. Model geometry
  unchanged (constants promoted, values identical) — no 3D re-send.

## [0.12] — 2026-09-10

The light-trap / hinged-panel blueprint round, a build-wide fastener-standardization
pass, the chemistry-prep-shelf blueprint, and housekeeping.

### Light-trap & hinged-panel blueprint

- **Fixed housing redesigned to a weld-free "slide-together" kit.** The extrusion-welded HDPE tube is
  replaced by a mechanical assembly: two 100° arc panels slide into four full-height opening-edge aluminum
  H-mullions, with the sill/header band pieces glued +
  riveted into the mullions' opposite slots — **no welded seam**. The housing skin now extends to the frame
  beams' **outer** faces and blind-rivets directly to them (the rolled rim-angle lap is dropped), notched
  where the two axle beams pass through. Four formed **1"×1"×1/8" 6061-T6 aluminum equal-leg angle** support
  strips run rail-to-rail across each opening so the mullions and caps bolt to
  a member.
- **Floor/roof caps simplified to plain plates; HDPE surround attachment reconciled.** The caps are plain HDPE
  plates riveted to the frame-beam outer faces and to the support strips, with the housing skin butting the cap
  underside on a caulk bead (no cut-out, no neoprene). The HDPE surround is documented as lapping +
  blind-riveting the **drum cage** (which wraps it and is welded into the panel frame).
- **Drum & housing opening edges framed; housing channels moved bonded → rivet-only.** The rotating drum's 80°
  opening jambs gain a riveted 6063-T5 aluminum U-channel (new `ll-drum-channel`).

### Fastener standardization

- **Fastener families consolidated across the build.** A standardization pass cut one-off threads and duplicate
  SKUs: the zinc wall through-bolts unify to a single **M12×70** length (123 bolts; shorter grips shimmed with a
  washer); the **#14 self-drilling TEK** unifies to one SKU; the filter-housing ply-mount folds into the
  **1/4-20** standard (the 5/16"-18 family retired); the tilt-swing board's central **M16×55 → M8×1.0×50** (reusing
  the board's own fine-pitch thread); and the optical-plate mounting bolt is itemized (was a drawing label only)
  and switched to hex. M10 was evaluated for elimination but **kept** as a justified uniform single-CSK family
  (thin light-trap hosts can't take an M12 flat head), and ⅛" blind rivets stay two grip SKUs (no single grip
  spans both lap ranges). The **M5 family is fully retired** (its last use, the chem-shelf ply attachment, moved
  to 1/4-20 tee-nuts).

### Chemistry-prep-shelf blueprint

- **Prep shelf redesigned as a plywood-primary structure.** Removed the welded 25×25×3 steel perimeter frame,
  folding-bracket stays, gussets, and M5 CSK; **18 mm plywood** is now the primary structure with all
  attachments in pronged **1/4-20 tee-nuts**. Added 2 SS chain stays, a bolt-on SS piano hinge, and a reused
  cam-latch; validated by `chem_shelf_load.py` (board SF 44, chain 5.4, tee-nut 20). `SHELF_T` 22→18.
- **Fabrication sheets (Sheets 4–5) added + firmed.** Dimensioned fab-detail sheets: board cut + per-hole
  tee-nut drill positions, hinge cleat + 8 mm backing plates (1:1), and a full fastener schedule. The detail
  firmed along the way: the piano hinge upsized to a **3″ extra-clearance hinge** (14835A77, **+$50**) to give
  the board tee-nut row real plywood edge distance (row moved to 25 mm); hinge screws reconciled to **8** (both
  leaves drilled); the cleat→backing M8 bolts set to **4** (one per hinge bolt); and the backing plates **tap M8
  directly** (no rear access — the loose-nut/weld-nut was dropped). Registered for publish + embedded in the
  report §3.5.

## [0.11] — 2026-09-06

- **Film-plane fabrication blueprint — mechanism-design → shop-buildable (Sheets 1–18).** Elevated the
  film-plane drawing set to a full fabrication blueprint matching the hinged-panel/light-trap standard — seven
  new per-part detail sheets, each drawn from `tbs_constants`, verified against the live 3D model, with cut
  lengths, hole coordinates, weld schedules, and firm part SKUs.
  - *Design corrections (five review passes):* re-spec'd the corner plate from a press-brake ¼ 6×8 plate to
    stock 4×4×¼in 304 angle (−$76…−$135, no forming); lengthened the wall-seat back-plate so both M12 rows
    clear the seat; ACM now butts the frame's vertical leg above the fillet ridge; member sections redrawn as
    single continuous extrusions/angles; wall-seat + far-left-bracket bolts drawn per the head-outside/nut-inside
    convention (with hidden-line X-clearance on Sheet 11); dropped two views redundant with Sheets 3/9; fixed
    the aspect-squashed drill holes; and relocated the perimeter muslin clamp-layout to Operating Manual §2.4.
  - *Fasteners — sourced & fully itemized:* retired the M5 axle-saddle screw → M6×20 (consolidated onto the
    shared `bolt-m6x20`) and itemized every previously-unregistered film-fab fastener with firm McMaster SKUs —
    16× 1/8×3/4in 304 flat-bar saddles, M4 cam-clamp bolt-through, M8 J1/J2 through-bolt + nut (M8×25 for the
    14mm grip), and the ACM→frame stainless self-drilling TEK screw. **+$72 to the FILM section**; costing
    self-check, report parts list, and the diagram gallery all cascaded.
  - *Constants & drift:* wired 4 previously-dead constants (`SKATE_ROLLER_W`, `SKATE_AXLE_LEN`, `XSLIDE_STROKE`,
    `UJOINT_YOKE_L`) + added `FP_RAIL_WALL_T`/`FP_RAIL_STOCK_LEN`, and swept stale constant/report values
    (X-travel 263→257mm, angle 3/16→1/8in, `FP_W`/`PH_X`/`RAIL_SPAN` comments). Phase-0 interference/bolt triage
    found no structural defects (the "7<9" flag is the catalog-fixed McMaster 4040N12 fit).

- **Fastener standardization — inventoried, decided, first cut.** Compiled every bolt/screw/nut/washer/rivet
  from `parts.py` (incl. threads bundled in structural/labor lots) into a design-for-assembly review
  (`fastener-standardization.md`): metric families targeted 6→4 (M5 + M10 to be eliminated), lengths ~12→~7.
  Per-family decisions recorded with their blueprint gates. Executed the one change needing no new geometry —
  **M6 nuts 3→2** (the plain electrical panel-mount nut folded into nyloc; one M6 anti-vibration nut). Surfaced
  two registry gaps (M10, M4 used but not itemized as SKUs) to close at their sheet rounds.

- **Hinged-panel cleanup — drum depth-center single-sourced + report completed.** The 2D hinged-panel
  drum sat 30mm off the 3D: Sheet 3 (drum vertical section) and Sheet 6 (HDPE floor-cap cut sheet) still
  derived the drum depth-center from the pre-resize `BAY_FRONT_X + DRUM_R + 40` (−450) instead of the shared
  `DRUM_CX` (−420) that the 3D, Sheet 2, and light-trap already use — now single-sourced off the constant, so
  2D and 3D agree. The container floor plan's swung-drum ghost was likewise hardcoded at the old −400 center
  (contradicting its own −420 label) — wired to `DRUM_CX`. Embedded the eight missing hinged-panel fabrication
  sheets (8, 9, 11, 12, 13, 14, 15, 16) in the report, so all 16 sheets are now shown. Fixed stale
  drum-height arithmetic in two Sheet 3 comments.

## [0.10] — 2026-09-04

- **New blueprint set — the hinged light-trap panel (cargo-door end).** A 16-sheet fabrication set for the
  swinging cargo-door panel and its revolving-drum light lock: panel elevation, plan cross-section, drum
  vertical section, rotating-transport / swing-clearance plan, interior pull-handle mount, HDPE-surround
  flat-pattern cut sheets + housing-join details, steel-frame general arrangement (interior + exterior
  mirror), pivot-post assembly, Fan-B plywood cut sheet, frame hardware (2× lift-and-turn cam latches +
  transport stay + brush strips), plywood→frame captive-tee-nut attachment, frame→pivot-post connection,
  transport bottom-clearance section, and the fold-down light aprons (incl. the Detail F hinge-line seal).
  The revolving-drum light-lock verification (person-fit + light-tight-at-every-rotation) lives on
  **Light-Trap Sheet 7**. Registered across the gallery / publish / setup / deps / report, drawn to the
  house label + fastener conventions with every dimension carrying an explicit `mm`.

- **Panel design — swing pivot, lighter door frame, fold-down floor-gap seal.** The panel + drum swing
  ~56° about a fixed Ø89 CHS pivot post that carries the panel, so the container cargo-door frame is a
  non-structural **50×20×3 RHS** section (reuses the IBC retaining-bar stock), bolted M10 into the door
  opening with the opening-edge U-channel welded to it. The **217mm** under-leaf floor gap — raised to clear
  the bare walkway cantilever legs through the swing — is closed by two bottom-hinged plywood fold-down
  aprons + a fixed center baffle, sealed by top/edge brushes, 45° chamfer lap joints, and an exterior
  lapping-board + compressed-foam labyrinth over the piano hinge. Two interior lift-and-turn cam latches on
  the opening edge give inward egress.

- **Ventilation Sheet 3 — Fan-B mount.** Fan B rides the swinging panel and bolts to its 18mm ply band via
  captive tee-nuts (distinct from wall-mounted Fan A on M10); added the dedicated mount plan and scoped the
  "identical fans" claim to the fan body. Fan mounts specced to real hardware (Fan-A L-bracket + Tek screws
  around the wall hole; fan-to-duct M5 corner screws; turned-out duct flanges).

- **Light-trap 3D model — full fabrication detail, zero-drift with the 2D.** Bay HDPE side/roof/floor walls
  are the outer skin, blind-riveted on a full perimeter straight to the integrated steel cage posts (Al
  L-angle rails backing the vertical HDPE edges); vertical EPDM baffles close the drum housing↔cage
  side-wall gaps; top/bottom 50×50 cage beams tie the drum cage to the frame; the film-plane fixed left rig
  stays put through the swing (only the lift-out rail removes); the cam latch is an L-shaped lift-and-turn
  handle; and the fold-down apron carries the hinge-line lapping-board/foam seal. Sheet 2 re-based on the
  shared drum/cage constants so the plan matches the model exactly.

- **Reports + single-source reconcile.** The hinged-panel report describes the current design only —
  rev-tags, old-vs-new archaeology, and raw location coordinates stripped from the prose and the injected
  parts specs; American spelling + thousands separators fixed; specs verified (Ø800 housing, the 50×20×3
  door frame vs the 2×2×0.120 panel/cage frame). Every spec change cascaded through `parts.py` / `costing.py`
  and the container / equipment-layout / cost-breakdown reports.

## [0.9] — 2026-08-27

- **Lighttrap Revoloving Drum detaile design and blueprint**
The lighttrap had a light-weight design that defined the major parameters. What was missing was a deatiled design down to the fabrication blueprints for the deatils of the mechanism.
  - **Design:** the drum end **caps are 8mm 6061-T6 aluminum** (bolted 4×M10 stub-shaft flanges), the **shell->cap and housing->frame joints are lap-and-fasten** (rolled 25×25×3 Al rim-angle + 1/8" 18-8 SS blind rivets @ ~60mm + 3M DP8010 bond/light-seal, superseding the extrusion weld), and a **steel welded box cage integrated with the swing-panel weldment** carries the bearings and the fixed outer skin (free HDPE opening edges stiffened by bonded Al U-channels in place of jamb posts). The **drum was resized Ø900->Ø800** (Ø764 drum, ~Ø758 bore) and re-centered to fit the transport-fixed cage; **interior 1,970mm clear** (`DRUM_H_LT` 2,100; cage top 2,217).
  - **Hub (both ends, Sheets 5/6):** cap -> **Ø160 steel stub-shaft flange** -> **Ø75 shaft** -> **SKF 6215-2RS1** -> **Ø240 bearing ring** (upper, isolated Al) / **collar** (lower, steel) -> **Ø240×12 steel mount plate** (ring/collar bolted 6/8×M10 CSK; plate welded to the beam) -> **50×50 axle beam**. The drum **hangs** from the upper bearing (above its cap, below the top beam); the lower bearing **floats** above the bottom beam. Axial retention: inner race by DIN 471 shaft circlips (+ a bolted Ø90×4 **end-retainer plate** on the upper load-bearing shaft); outer race **located** (upper - Ø122 shoulder + DIN 472 ring) / **floating** (lower - plain Ø130 H7 bore).
  - **Seals:** the ≈13mm running gap is closed circumferentially by **4× #4 (3/16") nylon strip brushes** (anodized-Al straight-flange holders DP8010-bonded + riveted to the drum OD at 93° spacing) and axially by **cap<->frame neoprene wiper + silicone bead** top and bottom; a Sheet 7 light-path study proves no straight-through or over-the-top path at any rotation. - **Interior pull handle** (off-the-shelf McMaster 1871A65) bolts to a steel stile that plugs + M10-CSK-bolts to the two Al caps - the pull load lands in the caps, with no fastener through the HDPE wall.

- **Film-plane corner wall-mounts + IBC foot ↔ tray clash.** Resolved
  the film-plane left-bracket + tray/IBC cluster. **Tray clash:** the two FRONT IBC floor feet were shifted
  outboard (derived from the tray edge) so their plate + anchors clear the processing-tray basin — the plate
  spec is unchanged, only the station moves. **Left film-rail wall mounts:** restored the budgeted wall-seat
  **saddles** the redesign had dropped — seat + gusset + **upstand** on the container-facing face (rail bears
  on the inside face, not the outer edge), back-plate lengthened so the gusset welds fully, and the rail ends
  trimmed to butt the plate. The two far-LEFT ends land on the
  Ø89 **pivot post** (it carries their weight) so they get a lighter flange **tie** (interior flange + exterior
  plate + 4× M12) instead — sized to clear the post + roof-mount plate. All wall-bolt **heads sit outside**.

## [0.8] — 2026-08-19

- **Walkway blueprint.** Reworked the walkway into a full fabrication blueprint set. Reworked the cantilevers so the near and far ones use the same fabrication. Added floor bolts to the right cantilevers, clearing the processing tray. Reworked the shared container-wall plates with the film-plane beam and walkway beam. Performed structural validation + IBC/OSHA bracket analysis, which required upgrading the cantilever arms to conform to the standards. Added a grate cut-sheet plan.

- **Walkway F1 → water re-route (branch `walkway-bp`).** Shortening the right walkway (F1) moved the outer
  long beam inboard into the under-walkway pipe channel. Fixed the two clashes it caused: **#1** the 4 ribbon
  lanes (`RIBBON_LANE_X`) were hardcoded for the old wider channel — now **derived** from the inner-outboard..
  outer-inboard beam gap so they can't drift again; **#2** the near-corner SV-01/DV-02 risers were speared by
  the end-beam butt-line inset — the **near RWk end beam is un-inset to Yd0** to clear them. (Two pre-existing
  under-corridor clashes — recycle×J6-plate, lines×IBC-frame-rail — are logged in TODO, not from this work.)

- **Sketchfab re-upload automated (in-place, hands-free).** The manual "re-upload each `.skp` to Sketchfab"
  step at the end of every model cascade is now scripted. `push_sketchfab.py` uses `PUT /v3/models/{uid}` to
  replace a model's geometry **in place** — same URL, viewer settings/materials/name preserved — instead of the
  old create-new-model-and-delete-old dance (which reset viewer settings each time). A single-writer guard
  refuses to push unless the live doc is the saved `<name>.skp`; legacy behavior stays available behind `--new`.
  Validated end-to-end (a scratch box→box+cylinder lifecycle and a real overview push to its existing UID).
  A wrapper — `send_model.py <name> --send --push` — combines the rebuild + push in one command: it delegates
  the build to the model's generator, then (token-gated) offers to push *after you validate*. It prompts in a
  terminal and skips safely with a note in a non-interactive shell, so an agent can't push unvalidated geometry.

- **3D models: single-owner dedup pass + a ratchet gate.** Components were being re-implemented in more than
  one model generator (the drift behind "the detail is right in one model, wrong in another"). Added a `lint.py`
  **ratchet gate** — no component name may be emitted as a `ruby_*` literal in >1 model file — and consolidated
  4 clusters to a single owning builder each that the other models call: **electrical** (em owns cable trunking,
  inverter box, master switch — overview's full-length trunking corrected to em's fitted extent), **Fan B box**
  (lighttrap), **processing tray** (overview owns the sloped pan; the spray-bar model now shows the *same* tray
  ghosted instead of a flat copy), **walkway Far/Near decks** (walkway model). 17 cross-file duplicates → 5,
  and the 5 are documented (2 permanent context ghosts + 3 real drifts the audit surfaced: cargo-door panel
  thickness 120 vs 40 mm, sump-pickup Yd 155 vs 104, and the mini-tbs scale-toy wall — all tracked in TODO).

- **Process: attack the orientation-rework class (retro follow-up).** A two-release retro found the biggest
  rework driver is fastener **orientation/interface** — bolts dimensionally correct but pointed the wrong way,
  through the wrong face, wrong length, or too near an edge (the J2/J7 3 mm-edge flaw, "bolts projecting past
  the plates"), caught only when a render was eyeballed. Three concrete fixes: (1) **`check_interference.py
  --bolts`** — a read-only lint that, for every structural grip bolt, finds the members its centerline pierces
  and flags EDGE (< 1.5·D), FLOATING, PROJECT (prototype; 15 flags on overview incl. a real J6 top-bolt edge);
  (2) **`skills/skill_fastener_convention.md`** — codifies the `ruby_bolt` axis/head/nut sign convention + the
  edge-distance/grip/accessibility rules so builders stop guessing; (3) **`manifest --update <name>`** now scopes
  to the named model(s) instead of rewriting every hash (it twice clobbered un-sent models' hashes this session).

- **3D-model hygiene (post-0.7).** Three drift/readability items off the tracker: (1) **retired the dead
  `ibc_rack()`** — the old single-portal frame builder (X4734), dead in the live model but a drift risk, moved
  out of `generate_sketchup_model.py` into its sole consumer (the archived right-cantilever study) so overview
  can't silently revert to the pre-redesign frame; (2) **fixed the real J6 clash** — the walkway cantilever-arm
  rear backing plate dipped ~10 cm³ into the corridor bottom X-rail at each front upright; raised its bottom to
  butt the rail top (Z62.8), moment joint untouched, `--solids`-verified gone on the live model; (3) the RWk end
  beam↔long-beam butt was already resolved — narrowed the remaining seam-audit sliver (long-beam ends ↔ wall
  cleat) for a walkway-open pass. Cascade: `ibc_cantilever_arms` re-sent to all 5 models (ibc-stack / walkway /
  construction / water / overview — saved + uploaded); `manifest --check` clean.

## [0.7] — 2026-08-17

- **IBC bar-restraint redesign — J2/J7 L-cleats + single horizontal M12×65 (edge-distance fix), full cascade.**
  The front retaining bars previously bolted VERTICALLY through the 20 mm-wide face of the 50×20 RHS, leaving a
  Ø14 hole only ~3 mm of edge. Redesigned **both** bar ends (corridor J2 + wall J7) to the same detail: the bar
  **drops into an 8 mm-plate L-angle** (welded to the upright / wall backing plate) and a **single horizontal
  M12×65** runs through the L's vertical leg + the bar's tall 50 mm web — ~18 mm edge. Retaining bars doubled to
  **2 per tier (8 total)** for the EN 12195-1 loaded-transport case; wall hangers **inside-aligned** to the
  corridor face (not the back surface); D-rings repitched **clear of the cleat legs**; **16 nut-side backing
  plates** added. Cascaded end-to-end: frame Sheets 1–6 + the Plate Fabrication Schedule, all **five** SketchUp
  models (ibc-stack / water / overview / construction / film-plane re-sent + uploaded), `parts.py` (M12×65 ×16 +
  `ibcf-cleat-backing` ×16), `costing.py`, and `ibc-stacking-report.md`. Interference re-audit against the live
  model confirms the redesign **adds no new clash** (all 10 remaining are pre-existing pipe-routing).

- **J6 walkway-arm → corridor-upright joint firmed.** The cantilever-arm end connection went from 4 bolts to
  **2 (a central vertical column)** on a **65×130 end-plate** with a simple 5 mm fillet all round, and the arm
  uprights now seat on their foot plates. Flagged the one **real** residual clash — the lower J6 bolt vs the
  corridor bottom X-rail — for a post-release 3D fix (notch the rail / drop its start).

- **IBC 2D diagram-standard pass — units, leaders, and outlines.** Swept the whole IBC frame + plate set to the
  drawing standards: **`mm` on every dimension** (de-crowded the sub-30 mm micro-dims to notes), **re-targeted
  Sheet 1 leaders** after the 2-bars-per-tier change (they had anchored in the empty gap between the paired
  bars), redrew the **container wall as a full-height ghost outline** (matching the tote outlines) and dropped
  the stray beam-tip wall boxes on Sheet 6, plus an editorial + tidy-labels tidy across the set.

- **IBC Frame Blueprints (rollup).** The above sits on a broader blueprint push over this cycle: bar-end cleats
  moved to the outside edge, the 2-ring / 8-weld map (Sheet 6), notch-TEK detail (Sheet 5), the member cut
  list, and TEK screws securing the cantilevers to the walkway frame.

- **NEW tooling — 3D readability seam audits (`check_interference.py --solids / --pipes / --seams`).**
  Two READ-ONLY, advisory passes against the live model that surface a *drawing* defect (distinct parts
  rendering as one fused piece because no seam shows), distinct from a clash. `--solids` lists same-color
  solid↔solid interpenetrations (3-axis overlap — a member run *through* another, not a butt) above a
  volume threshold, each tagged `weld` (leave) or `BUTT?` (bolted/cleated → butt at the mating face).
  `--pipes` flags pipes driven through the full thickness of a panel/wall/plate slab with no drilled-hole
  seam (fix: collar ring, or split to butt). The butt-vs-weld convention is codified in
  `skills/skill_model_consistency.md`. (The per-hit geometry fixes are a triaged follow-on — TODO.md.)

- **Half-lap hold-down — #14 TEK screw per lap (Sheet 5 detail + model + parts).** The long beams sat on the
  arm's bearing seat by gravity only; added a positive fastener so they're secured. One **#14 self-drilling TEK
  screw per half-lap** (4 total: 2 arms × 2 crossings), driven **from the underside** through a Ø7 clearance
  hole in the beam, self-tapping into the **solid arm** above (anti-lift/anti-slide; the head sits in the
  ~6.6 mm gap and clears the traveling spray beam). New **HALF-LAP HOLD-DOWN section** on Sheet 5 (hatched arm
  on top / beam with the hole below / screw from underside), 3D model gains the 4 screws, `parts.py` +
  `walkway-arm-holddown` (4× #14 TEK + washer), costing +$2/$3/$4, report §3.4 note.

- **Walkway cantilever arm → SOLID 2×1 flat bar + rebalanced half-lap notch (structural fix + full cascade).**
  A review flagged the arm's half-lap notch as dangerously thin. Root cause: the arm half-laps over **both**
  right-walkway long beams, and a notched **hollow** tube opens into a weak channel (the un-notched LEFT
  cantilevers can stay tube; this one can't). Added the missing check — `ibc_frame_load.arm_notch_check()`
  computes the moment at each notch (worst case = full arm load at the tip): outer notch **334 N·m**, inner
  **31 N·m**. Fix: the arm becomes a **solid 2×1 flat bar**, and the notch is **rebalanced to the moment** —
  deep arm notch at the tip (low moment, arm keeps 5.4 mm / inner beam keeps 20), and at the post end the
  **outer beam** takes the deep notch so the arm keeps 16 mm (**SF ≈ 1.6**). A continuous-beam check
  (`outer_beam_frame_check`) firmed the outer beam: its thin 9.4 mm notch is a **bearing seat** (a thin
  channel can't carry the support hogging), so the beam spans simply-supported on its **full section — SF ≈ 7,
  ~2 mm** deflection under a person. Cascade: 3D model (`_rwk_xbeam` solid X-segments + per-crossing
  split, `_rwk_long_beam` split param, `ibc_cantilever_arms` J6 clamp→end-plate), `parts.py` (arm split out
  as solid bar + J6 end-plate hardware: 8× M12×100, 4 plates, 8 crush sleeves; −4 clamp bolts), costing
  reconciled (+$62/$85/$108 walkway), Sheet 5 + report §3.4 updated. (3D `.skp` re-send to follow.)

- **Fix — walkway Sheet 6 (floor-leg cantilever): post drawn over the anchor holes.** In both VIEW A
  (section) and VIEW B (plan) one of the two M10 anchor columns fell under the 50×50 post footprint —
  unbuildable (can't drive a floor anchor through the post). Both anchor columns now sit **outboard of the
  post** in each view, using one shared formula (`fx0+14`, `fx0+fl-post-14`) so the section and plan agree.

- **NEW — IBC frame Sheet 5: walkway cantilever-arm fabrication (`ibc-frame-sheet5.png`).** The 2 walkway
  cantilever arms that hang off the IBC front uprights are now drawn as a fabrication sheet in the IBC-frame set
  (keeping all the IBC-frame metal together rather than deferring to a separate walkway blueprint). The arm
  crosses **both** right-walkway long beams (`RWK_BEARER_XS`), so it has **two** half-lap notches, not one.
  Three views: a fully-dimensioned VIEW A side elevation (notch widths + gaps 50.8 / 198.4 / 50.8 / 25 → reach
  325, half-lap depth 20 notched of the 25.4), a PLAN VIEW showing each notch as a full-width half-lap (beam
  width 50.8), and an END-PLATE / rear-backing-plate detail (70 × 130, 4× Ø13 for M12 at 30 × 90 pitch, with the
  arm weld footprint shadow-marked). Sheet count bumped to OF 5; registered in the gallery / publish.sh /
  setup_docs / dependencies.yml and embedded in report §3.5 + §8. The two "detailed in the walkway blueprint"
  notes re-scoped to point at Sheet 5. (2D only; the 3D ibc-stack arm + full model cascade to follow.)

- **NEW — IBC frame load-case sheet (`ibc-frame-load-case.png`).** `ibc_frame_load.py` gained a `--png` render:
  a one-page load-case drawing — the transport load-path elevation with the EN 12195-1 arrows (0.8 g fwd /
  1.0 g down / 0.5 g lateral), the method box (coefficients, f_s, μ, the blocking inequality, both fill
  states), and the full demand/capacity/**SF matrix** for every restraint element (bars with/without the mat,
  wall-hanger + cleat bolts, wall bearing, lash strap, walkway-arm clamp, upright) — all driven from the same
  `compute()` the validation table uses. Registered + embedded in report §3.4. Completes the IBC-frame
  blueprint's visual set (the film-plane Sheet 10 analogue).

- **Rear-panel + pipe-run brackets: welds → TEK screws (W6/W7 → J8/J9).** The two light bracket-to-post
  joints are no longer welded — they attach with **2× #14 self-drilling TEK screws** each, so the brackets
  bolt onto a **pre-welded, pre-painted frame with no hot work** and stay adjustable (they carry only light
  static loads; the load-bearing bar cleat stays welded, W3). Weld schedule drops W6/W7 (W8 ribbon-beam →
  W6); fastener schedule gains **J8** (rear-panel bracket, 12) + **J9** (pipe-run L, 24); Detail D/E redrawn
  with the TEK screws; Plate 5/6 "weld leg" → "screw leg". Added a `bracket-tek-screws` part (36× #14, 410 SS,
  +$11/$20); the two bracket specs de-welded; costing reconciled.

- **Plate schedule — fuller hole dimensioning, Plate 3 redrawn, stock standardized, J7 reverted to 1.**
  Plates 4/5/6 carry BOTH L-legs' outside lengths on the L-section end view + a hole-center dim on the
  drilled-leg face; Plate 2 gains a hole-center-to-edge dim; the Plate 5/6 hole-size note moved to Sheet 2.
  **Plate 3 (wall-hanger pocket) redrawn** into two proper **FACE views** — back-plate + seat/fillet face
  with the drill holes dimensioned. The pocket **back-plate + seat standardized to 60 mm** to reuse the
  Plate 2 backing stock (were 67/59). **J7 reverted to 1 centered bolt/bar** (from 2, 16→8 M12×40, −$12):
  the 2nd was redundancy not strength, and at the wall the pocket + the fixed 2-bolt corridor cleat already
  stop the bar rotating — one centered bolt also clears the seat edges cleanly. Detail A + report §3.5 + costing updated.

- **IBC frame Sheet 4 — detail-correction sweep (B/D/F + tone).** DETAIL D redrawn per the sketch as a
  welded **L-bracket** off the post with the rear panel bolted to its upstand via an **M8 hex + washer into a
  pronged tee-nut** — and the tee-nut moved to the ply **back face** (bolt tension pulls the flange against the
  wood, the correct orientation). DETAIL B cleat bolts now span the bar+cleat stack exactly so head/nut seat
  **flush** (no exposed shank). DETAIL F elevation bolts shortened to bear on the clamp-plate faces (were
  projecting past the plates). Steel fills **lightened to sheet 3's tone** for readability.

- **NEW — IBC Plate Fabrication Schedule (2 sheets).** `generate_ibc_plate_schedule.py` draws every plate in
  the IBC/corridor metal **1:1** (with a 100 mm scale bar) so a shop can cut and drill each: Sheet 1 —
  structural plates (IBC foot 150×150×12 / 4× Ø14 @ 100 sq PCD; wall-hanger backing 60×205×8 / 2× Ø14 @ 169;
  wall-hanger pocket, folded 4 mm, J3 + J7 holes); Sheet 2 — angle brackets (bar-end cleat, rear-panel tab,
  side-panel pipe-run L), each as an L-section end + a drilled-leg face with hole Ø, center positions from a
  datum edge, thickness, material, and qty. Hole positions are the diagram-of-record; sizes trace to the foot
  constants + the current corridor model (deliberately NOT the shared `FP_CORNER_SEAT_*`, which is the film-plane
  corner-seat spec). Registered in the gallery / publish.sh / setup_docs / dependencies.yml and embedded in
  report §8.

- **IBC frame Sheet 4 — DETAIL F: walkway arm → front-upright connection.** Added the sixth detail inset:
  how each right-walkway cantilever arm attaches to a front corridor upright. Corrected from an assumed
  weld to the ACTUAL design (per `ibc_cantilever_arms`) — a **bolted clamp**: 2 clamp plates wrap the
  upright + 2× M12 through-bolts at two Z levels (no weld). Reclassified the connection across the whole
  blueprint: `ibc_frame_load.py` now checks it as a 2-bolt clamp (couple over the ~37 mm bolt spacing,
  **SF 3.8**, up from the SF 3.3 weld estimate); report §3.4 (clamp, not weld), §3.5 (new fastener **J6**;
  **W9 removed** from the weld schedule), and §8 (Sheet 4 now A–F). Clamp hardware is procured with the
  walkway-arm assembly (walkway blueprint), not double-counted in this frame's BOM.

- **IBC detail sheets consolidated + corrected per review.** Fabrication details now live on a single sheet
  (`ibc-frame-sheet4`), reworked per feedback: DETAIL A hanger as a SECTION (bolts through the backing
  plate + wall + pocket — not the bar; vertical pair 50 mm clear; standard bolt-in-section symbols),
  DETAIL B cleat as a section with vertical bolts, DETAIL C two lash rings each on its weld plate with
  ring-pitch/bar-end dims + a jagged bar break, DETAILS D/E captive tee-nut as a rectangle + countersunk
  screw. `ibc-stacking-sheet2` repurposed from duplicate fastening details to a **securing arrangement**
  (the 8 lash-point locations + strap routing — the rigger's plan; construction → Frame Sheet 4), dropping
  the operational ratchet-buckle close-up.

- **IBC equipment panel top dropped to open the Fan A air path.** The corridor equipment panel (18mm
  rear ply + 25mm pump-mount shirt) was capped at Z2191/2256, blocking airflow through the panel to the
  sealed-end Fan A exhaust. Dropped **both plies to Z1900** — the underside of the Fan A baffle window
  (Z1900–2100) — so the corridor is open across the fan. New driftproof `PANEL_TOP_Z = FAN_A_H −
  DUCT_HEIGHT/2` (was a stale `DV_Z + DVB` tie to a DV-02 that Phase-2 relocated to the pinhole-wall
  skid). The **top pair of welded frame bolt-tabs** ("Rear-panel bracket") dropped 2176→1780 to sit
  under the new panel top. Also corrected the rear-panel ply label marine→exterior (dry backing, per the
  plywood rule). In the water model the corridor panel is now drawn **solid in every scene** (un-muted +
  the redundant "solid" LOD duplicate dropped, its orphan tag purged) so the shirt/backing read as a
  solid backdrop rather than the faint 0.18-alpha ghost. Re-sent the 6 models that draw the shared
  corridor frame/panel (overview, water, walkway, construction, film-plane-mechanism, ibc-stack). No
  BOM/cost change (same sheets, cut shorter).

## [0.6] — 2026-08-13

- **Film-plane LEFT edge pulled inboard of the pivot hub (`FP_X_L` 150→260).** Resolved a hard
  clash found once the detailed corner was in the light-trap: the backing-side carriage rode straight into
  the swing-pivot hub. Resolved by bringing the film plane inside the swing-pivot.
  Costs ~110mm image width (`FP_W` 4499→4389, active area 101→99 sq ft); the
  now-asymmetric plane re-centers the pinhole (`PH_X` 2399→2454, +55mm). Cascaded to facts/CLAUDE.md optics
  table, 11 diagram generators, and 8 SketchUp models. NB: the removable-rail lift-out STAYS — the inboard
  move clears the pivot region but the panel's long swing arc still crosses the rail in the near/removable
  zone (Yd ~1950–2066), so that section must still lift out for transport.

- **Film-plane corner mechanism — definitive engineering blueprint (milestone template, branch
  `corner-eng-design`).** Upgraded one corner from arrangement-schematic to fabricator-ready, driven
  from `tbs_constants` so it can't drift: sheets 3/4/8/9 dimensioned (skate roller ODs + 40mm pitch;
  rail wall-flange bolt pattern; cross-slide bar section/travel/gib/UHMW; U-joint envelope Ø19.1/68/bore
  9.53/±45°, J5 hole pattern, L-plate 6×8 bend); **J1–J5 fastener schedule with torque/class/washer/locker**
  (M8 24 N·m, M6 10 N·m, setscrews ~2.5 N·m); a **datum + tolerance scheme** (datums A/B/C + GD&T). Firmed
  the load (162 N/corner, section SF 4.5/27) and, to hold ±40°/±28°, grew the cross-slide bar (+$135 film).

- **Stainless-grade reconciliation (304 vs 316) — system-wide policy.** The cyanotype wash has no
  chloride, so 316's pitting resistance is unused → **304 (A2) is the default** for all wet structural
  stainless; 316 is metallurgically unneeded (kept only on the tray seam bolt by choice). Codified as a
  policy block in the `parts.py` registry header. The actual corrosion gap was zinc fasteners in wet zones,
  so upgraded `bolt-m6x20` (×2) + `bolt-m8-fixing` → 304 A2-70; the M12 structural through-bolts keep
  Grade 8.8 zinc (strength + exterior inspectable heads). 410 self-drillers + chrome-steel bearing kept.

- **Film-plane corner — Phase-1c load case computed + decided → Sheet 10.** New `fp_corner_load.py` (driven from
  `tbs_constants`, renders `film-plane-sheet10.png`). **C2** verifies the cross-slide travel: Z (tilt ±40°)
  = 245mm and X (swing ±28°) = 257mm exactly match `XSLIDE_Z/X_TRAVEL`. **C1** the per-corner load (W/4 =
  124N) → X-slide bending safety factor — bar orientation is decisive, **DEEP** (38.1mm in the load
  direction) SF≈10, **FLAT** a marginal 1.7 (fails at ×2). **DEEP** was chosen on this basis.

- **Film-plane blueprint: Sheet 7 upgraded from system-arrangement to fabricator-grade GA.** Added the
  frame-fabrication content a shop needs: DETAIL A corner joint (45° miter + TIG fillet, per the joint
  decision) with the 2"×2"×3/16" 6061-T6 angle callout; the ACM backing strip layout (4 vertical Dibond
  strips, 3× 1219 + 1× 732 mm, 3 butt seams, splice-battened); and the 58× nylon-spring-clamp stations
  @ 150 mm (top + 2 sides).

- **Model `.rb` retired from git → `dependencies.yml` source_hash manifest; Sketchfab UID
  consolidated.** The 10 generated SketchUp `.rb` were committed only as a diff/staleness proxy for
  the binary `.skp`; they're now gitignored, replaced by a per-model `source_hash` in
  `dependencies.yml` — `sha256` of the regenerated, identity-stripped, float-normalized `.rb`
  (`src/generators/manifest.py`; `lint.py --verify-all` recomputes + compares, `manifest.py --update`
  refreshes). Same drift tripwire, no expanded Ruby in the repo, and immune to the float-noise that
  spuriously flagged the old byte-diff. Also folded the model registry into `dependencies.yml`: each
  model now carries its `uid` + `embed_files` there as the single home (generators read the uid via
  `ov.model_uid()` instead of hardcoding it; `push_sketchfab.py` reads/rewrites it), resolving the
  UID drift (it lived in both the generators and the 6-of-10 `models/sketchfab.json`, which is now
  retired). New `lint.py` gate: models must declare a valid uid/embed_files/source_hash.

- **Pump-run support-detail fabrication sheet (#29 follow-up).** New `generate_support_detail.py`
  → `support-detail-sheet1/2.png`. Sheet 1 = face-on board elevations (far / near / near-upper —
  18mm ply, 4 L-brackets each, risers + P-clip rows, fully dimensioned); Sheet 2 = the L-bracket
  flush-mount plan section (post inner face → 6mm weld leg → 45mm landing leg → ply seated flush,
  fastened with an M6 countersunk flat-head screw into a captive pronged tee-nut), a P-clip
  cross-section, and a fabrication schedule (3 boards / 12 brackets /
  39 clips). Geometry imported from the `cp` model constants so it can't drift. Embedded in
  plumbing-report §5.3; registered in the gallery, publish, setup_docs, and dependencies.yml.

- **Pump-run support boards in the IBC plumbing corridor (#29 follow-up).** The cantilevered pump
  risers on the two corridor side walls now land on **three 18mm ply boards** (far wall + lower and
  upper near-wall boards), each recessed **flush**
  in the window between the front & rear side-posts (399mm wide) on **welded steel L-brackets** (one
  leg welded to each post inner face, the ply bolted to the landing leg — the rear-panel method), with
  the risers held by **cushioned P-clips**. The **same P-clip method was extended** to the **drain-riser spine**
  (the 3 gray waste risers — X4 waste / DV-02 / DV-01→merge) and the **filter-skid panel** (the
  3 vertical runs — DV-02→F1 + tray-sump→P-04, F3→SV-01 already there —
  plus the horizontal runs: brown ± ACC-02 flush, and standoff clamps on the blue ± SV-01 and the
  brown DV-02 row). **Operability + review pass:** BV-03 handle rotated to −X (cargo door); a second
  **upper near board (Z1260–1950)** backs BV-02/BV-06 + the brown P-05 (Z1300) and gray P-03 (Z1902)
  horizontals; BV-02/BV-06 handles rotated +Yd into the corridor and their loops pulled to the
  **walkway edge (X4770)** for reach, labels moved to the valve centers on the operator side;
  spine far-side X-port lines (P-05→X3, P-03→X4) clamped; the DV-01→IBC-3 tote entry dropped to
  Z1080 with the flange seated on the cage edge and the run simplified (straight in, no drop-jog).
  **BOM/cost:** 3 ply side boards (cut from the
  corridor 4×8 offcut — no added ply), 12 welded L-brackets, 39 cushioned 3/4" P-clips →
  **+$33/$46/$61 water** (grand total $26,024/$30,492/$37,028).

- **SketchUp `--send` memory-bloat investigation (tooling, not published).** Ran a full investigation
  into the SketchUp process ballooning over repeated `--send` (TODO tooling item). Falsified the
  "Ruby allocations not freed" hypothesis empirically (isolated `TOPLEVEL_BINDING.dup`, flat Ruby heap
  across 12 re-sends, zero globals/constants/closures, `purge_unused` clean); root cause is SketchUp's
  **C++ allocator retaining freed pages** (not reclaimed by GC/purge/File>New — only a restart clears
  it). No code fix; mitigation is workflow (restart during heavy send sessions). Written up in
  `sketchup-memory-investigation.md` (repo-internal, not a TBS artifact). Follow-up hardening:
  added `materials.purge_unused` to the two water builders that lacked it (now standard across
  all 11 generators, self-cleaning orphan materials each rebuild); `layers.purge_unused`
  deliberately not added (the existing `keep_tags` prune is stricter and scene-safe).

- **Spray-beam removal cycle (#28) closed as no-lift / park-and-roll.** Decided against a lift-out
  mechanism: the muslin loads by parking the gantry at the near end and rolling the beam back over
  the laid fabric (report §4.2), and beam service is via the right-walkway grate (§4.3). Verified the
  **9mm beam-to-floor gap** from the constants (Ø32 wheel radius 16 − 7mm bracket drop, constant across
  the traverse) → **~8.5mm over the 0.5mm muslin**, wheels running outboard on bare floor.

- **Structural sections re-specced to stock imperial tube (#26) + mid-span support confirmed (#27).**
  The walkway/floor-leg/IBC/brace members were carried in metric-nominal sizes that aren't sold in the
  US. Re-specced to confirmed stock: the shaved right-walkway long beams, the 2 mid-span center arms,
  and the 5 floor-leg arms → **2×1×0.120in steel** (2×⅞ is non-stock — MetalsDepot/Metal Supermarkets
  carry only 2×1; $6.35/ft bulk); the IBC frame, film-plane brace, floor-leg posts, and swing/hinged-panel
  frames → **2×2×0.120in** (50→50.8); the tray bearer → **2×2×0.125in 6061 Al**. 2×1 is *deeper* than
  2×⅞, so the arms get **stronger** (SF≈2.5 vs 2.1) — Option B keeps the deck height, trading 3.4mm of
  spray-beam clearance (15→11.6mm). Real 2×1 pricing corrected the RWK frame (+$107/+$123
  walkway; the old $28–40 was a guess for a non-stock section); grand total → $25,991/$30,446/$36,967.
  8 diagrams + 6 model `.rb` regenerated (`.skp` re-send pending).

- **Braided flex on both ports of every pump (#29).** Extended vibration isolation from inlet-only
  to **both the suction and discharge** of all five pumps — a braided ½" jumper de-couples each pump
  from the rigid PVC run so vibration can't fatigue-crack a solvent-weld joint (P-04's suction is the
  1" tray-drain hose → 9 new ½" jumpers). Shown on the water-system P&ID (a flex coil on both ports
  of P-01…P-05); BOM adds the 3rd braided length + **18× ½" barb couplings** (Rain Bird BC50-20) +
  **18× SS clamps** (Everbilt 671255E), **+$55** water. Plumbing-report §5.2 made explicit.

- **Ball-valve sourcing + BV-05 spray selector re-designed as two 1/2″ valves.** The five 1/2″ 2-way
  isolation valves (BV-01/02/03/04/06) re-sourced Banjo V050FP → **Grainger 803HZ1 at $24.14** (from
  US Plastic $44.27, **−$120**). No 1/2″ 3-way L-port is stocked (only 3/4″ Banjo V075BL $72.88 +
  reducers), so **BV-05 became two 1/2″ valves**: **BV-05a** (3-way Blue/Brown selector, reuse the
  #22365 divert valve) + **BV-05b** (2-way spray on/off, **wall-mounted** above the selector, off the
  moving spray-bar pole) — all 1/2″, no reducers, no L-port OFF-detent risk, ~$37 under the L-port
  (net water cost this pair: **−$96**). Modeled in all four 3D models (water/overview/construction/
  ibc-stack); plumbing report §4.1 rewritten. The **overview** opening camera was also turned 180° to
  look into the container from the far wall.

- **Sump→P-04 suction re-routed off the pinhole wall.** The tray-drain suction ran as a tall riser
  straight up the pinhole wall (a clash); it now rises only ~150 mm above the walkway deck, turns 90°
  toward the skid, runs above the walkway, then a second 90° turn up into P-04 at the skid.

- **Muslin re-cut to fit the washable tray; spray-beam lift-out resolved operationally.** The muslin
  is now cut to the **washable tray area** — **4,359 × 2,000 mm** (`MUSLIN_CUT_W/H`), narrower AND
  shorter than the film-plane ACM+frame (4,499 × 2,094) so it lies flat clear of the side rims and the
  near-rim sump well; the tray, not the optics, is the size constraint (captured print ~94 of the
  101 sq ft plane; muslin yardage 388→360 yd, still 3 rolls, no cost change).

- **Spray-bar + processing-tray redesign — full-width beam, center-draining tray.** The spray beam
  went to a **full-width 1½×1½×0.062″ square tube with 44 nozzles** (from the short 40×25 section);
  the tray floor was re-sloped to a **Yd-only 1:200 fall** (far rim high → near rim low, level across X)
  feeding a **near-rim gutter that itself falls 1:200 in X to a single center sump well at X=2399**
  (replacing the old IBC-corner drain). The sump pickup **pops up through the walkway on a vertical
  riser**. Cascaded through the constants, every 2D sheet, and re-sent every affected 3D model
  (overview / spraybar / walkway / construction / ibc-stack / water).

- **Walkway support shaved to 2×⅞″ for spray-beam clearance.** The right-walkway long-beam and the
  left floor-leg arms dropped 40×40 → **2×⅞″** (soffit Z80/75 → Z93) so the full-width beam clears by
  ≥15 mm. (Follow-up mid-span stiffening is tracked in `TODO.md`.)

- **Phase-2 water topology — the tray drain now feeds the filter train.** Re-plumbed so tray-drain
  water is **filtered before returning to the totes**: **P-04 (tray-drain) relocated from the corridor
  to the pinhole-wall filter skid** (P-04 → SV-02 → 3W-DV-02 → F1/F2/F3 → SV-01 → 3W-DV-01 → IBC-3
  recycle / IBC-4 waste), and **P-02 (recycled-spray) took P-04's corridor slot** (P-02 → ACC-02 →
  3W-BV-05 spray selector). Blue supply isolated; the recycle loop closed. The Sheet-1 P&ID schematic
  was redrawn to match, and water.skp rebuilt (skid-panel reorg, ribbons routed onto the ply,
  3W-BV-05 dropped clear of the aperture).

- **BOM / cost reconciliation.** Added **ACC-02** and the **pinhole-wall filter-skid backing ply**
  (exterior grade, not marine) to the registry; reconciled the `project-cost-breakdown.md` §5
  water-system table to `costing.WATER` (fixed a positional-fill row-shift that broke the table
  arithmetic). Single-sourced the skid constants, SV-01's raised height, and the muslin cut size.

- **Tooling / process hardening.**
  - **Cascade tracking now follows the module-import graph** — a model that reuses another module's
    builders (e.g. `water.skp` via `import generate_sketchup_model`) inherits its constant deps, so
    the `--cascade` re-run list catches builder-reuse models the old grep scan missed.
  - **Pipe-crossing audit enforced by a lint gate** — `check_interference.py` detects crossings by
    centerline distance (no more join false-positives) and a commit gate blocks a reroute unless the
    interference report is refreshed.
  - **Water model normalized** — `--save` now writes a committed, deterministic `water.rb`, so
    `lint --verify-all` byte-verifies it like the other nine models instead of nagging "re-send
    manually" every run.

- **Materials.** Black ACM (dibond) re-sourced to Central Coast Plastics after Curbell couldn't
  supply (price TBC). Muslin set to the image plane exactly (no hem).

## [0.5] — 2026-08-02

- **Part/SKU reconciliation.** Major rework and reconcilaition of all the parts that need to be ordered to construction the poject. This required some rework of systems to accomodate what could be ordered vs. what is theoretically possible. All priced and firmed up in the registry to get a more concrete costing. Until we have a full set of blueprints, the fabrication estimates will need to wait, so this is still an unknown in the overall costing.

- **Fastener BOM decomposed into bolts / washers / nuts for ordering.** Split the 11 bundled
  "bolt + nut + washer" kit lines into separate component parts, using **shared keys** so nuts and
  washers total **by size + type across the whole build** (M12 flat washers **220**, M12 plain nuts
  **110**, M5×16 CSK screws **184**, …) while bolts stay itemized **by size × length**. The master
  BOM's fastener section now reads as a purchasing block.

- **Muslin clip re-design**. Removed the bespoke clamp design and replaced it with off the shelf spring loaded quick-grips.

- **Right-walkway muslin-rod / beam clash resolved by cranking the inner cantilever beam.** The muslin's
  rigid bottom rod must drop straight down at the tray edge through the muslin-drop notch,
  but the inner long beam of the cantilever rectangle sits directly under it. Rather than cut the beam at
  mid-span of its ~1.1m end bay, the inner beam is **cranked outboard 100mm** (the full notch depth) over
  the notch with ~100mm angled ramps each side. Sheet 3 (Detail A) shows the crank + rod
  slot; report §4.1 + docstring updated. No new parts.

- **Walkway decks reworked to continuous cut pieces** — bump-out & punch-out now integral, not
  butt-jointed add-ons.** The near-walkway EP/battery bump-out and the left lift-out's drum-exit
  punch-out were each modeled as a *separate* box butt-jointed onto the deck — which reads as
  "needs its own support." Both are now **one continuous L-cut** (new shared `near_fixed_deck_grate`
  + `left_liftout_grate` prism helpers), matching how they're cut from flat GRP stock: no mid-deck
  joint at either widening. The muslin-drop notch folds into the same left piece. Only the four
  corner joins and the **one unavoidable near/far sheet seam** (molded GRP tops out at 3′×10′, and
  the near run is ~3.9m) remain as joints — the seam is placed away from the bump shoulders. The
  bump-out itself is carried by the deeper 500mm-arm wall-cantilever brackets at 457mm rib centers.

- **Light-lock plastics firmed — one weld-compatible HDPE.**
  Priced all four light-lock/panel plastic parts to actual [US Plastics](https://www.usplastic.com/)
  sheet: the Ø900 housing to **3/16″ HDPE** ([46685](https://www.usplastic.com/catalog/item.aspx?itemid=136962&catid=705),
  3 sheets = $555) and the drum, panel skins, and B2 bay to **1/8″ HDPE**
  ([46684](https://www.usplastic.com/catalog/item.aspx?itemid=136961&catid=705), $123.34/sheet).
  This consolidated the drum/skins/bay off the nominal *4mm PP* onto HDPE — all light-lock plastic is
  now **one weld-compatible material** (PP↔HDPE won't extrusion-weld). Booked the real **1/8″ (3.18mm)**
  thickness through the constants + weight model (`LT_DRUM_T`/`PANEL_SKIN_T`/`BAY_WALL_T` → 3.18), cutting
  the swinging-panel assembly **~12 kg** (panel 171→161, drum 38→36; structure 584→572, dry 3,238→3,226).
  The drum's 2 **end caps stay 3/16″** (`LT_CAP_T`, thicker than the 1/8″ shell) — they carry the stub
  shafts into the SKF 6215 bearings, so the hub load path keeps its stiffness; cut from the housing offcut.

- **Wall through-bolts finalized: partial-thread, right-sized to the container-wall grip.** A grip
  analysis against the ISO container spec (side-wall corrugation ~25–30mm, not the ~38mm the prose
  assumed) showed the M12×80/×90 through-bolts were oversized. Re-sized every wall bolt. Designed for the **30mm worst-case grip**
  with a flat-washer shim allowance (2→4 M12 washers/bolt) so the bolt spec is robust across 25–30mm
  corrugation with **no container measurement needed** — pad to suit. Added `CONTAINER_CORRUGATION_DEPTH`
  constant.

- **Film-plane seal parts sourced; parts-identity lint fully clear.** Swapped the EPDM foam tape to
  [McMaster 8694K88](https://www.mcmaster.com/8694K88/) (1"×½", 25 ft rolls) and right-sized the qty
  to **2 rolls (50 ft)** against the ~43 ft film-plane perimeter — the old 3×50 ft = 150 ft was ~3.5×
  over (provisional).

- **IBC transport lashing → weld-on tie-down rings.** Sourced the restraint lashing points to
  [McMaster 3028T31](https://www.mcmaster.com/3028t31/) — a 1½" ID × ½" thick, 6,600 lb WLL,
  zinc-plated-steel **weld-on** ring — replacing the plain-D-ring + separate-mounting-plate approach
  with a single integrated weld-on part (fillet-welded straight to the front retaining bars, no
  plate, no retainer). The 6,600 lb ring far exceeds the 25mm-strap-limited 1,100 kg assembly WLL,
  so the full spec holds with no downrating. Report §4.1 + Sheet 1 label + BOM + the IBC frame cost
  band updated (−$15/−$30).

- **Fix: 4 gallery diagrams were broken images on the site** — the film-plane corner-joint study
  diagrams (`film-joint-options`, `film-joint-study-gimbal`, `film-joint-study-ujoint`,
  `film-corner-gimbal`) were listed in `all-diagrams.md` but not registered in `publish.sh` /
  `setup_docs.py`, so their PNGs never synced to `published/assets/` (404 on the live gallery). Added
  them to both sync registries and re-published. (Shipped broken in 0.4 — the lint gallery-gate checks
  the markdown lists every PNG but not that each is wired for syncing.)

## [0.4] — 2026-07-20

- **Film Plane Redesign** - Major rebuild of how the film plane pivots around the four corners. A new 3d model was created **`film-plane-mechanism.skp`** and `film-plane.skp` was retired along with its generator. The design centers around a U-Joint on each corner along with 2 slides per corner for articulation. The U-joint funnels
  the whole corner into a **304 stainless corner plate**. Parts are SKU's all reconciled along with the budget estimate.

- **Light-trap door top/bottom seals → strip brush** — the two horizontal door-frame seals the
  swinging panel edge *sweeps across* were changed from a steel seal-lip + EPDM compression to a
  **nylon-filament strip brush**. The panel/drum-box top edge's deliberate ~30mm overlap is now recorded
  as intended bristle engagement, **not** a clash.

- **Film-plane muslin clamp: cam-lever → spring clip** — retired the cam-lever toggle for a spring
  clip: a fixed jaw bolted to the ALU frame upstand (countersunk bolts, nuts on the inside) + a
  spring-loaded jaw that pinches the muslin + a neoprene pad onto the ACM board, squeeze-to-open
  (torsion spring holds closed).

- **TBS-002 "Mini-TBS" classroom camera** — the proof-of-concept two-box cardboard pinhole
  camera was recast as an educational design (Part I teaching / Part II build) and refined
  throughout: the film plane became a cut-cardboard flap (no foam board), push-pin paper
  mounting, a pin-load-seal-coat-dry coating sequence done by feel in the sealed box (no
  safelight), a single wash tray, a re-centered pinhole, and — the key fix — print extraction
  through the boxes' **own top flaps** (built flaps-up) instead of a custom-cut wall. Added an
  interactive **Sketchfab 3D model** (ghosted boxes joined with gray tape; clickable shutter,
  film-plane panel, and top flaps) embedded in the doc, generated from a new
  `generate_mini_tbs_model.py` with geometry single-sourced from `mini_tbs_constants.py`.

- **Site footer + theme overrides** — the footer now reads inline as
  `© 2026 Alvin Richards — Released under GNU AGPLv3. Version v0.3` instead of dropping the bare
  `v0.3` onto its own right-justified line (which wrapped and read oddly), and the Material theme
  overrides moved from `overrides/` to **`src/overrides/`** (`custom_dir` updated in `mkdocs.yml` +
  `setup_docs.py`; the footer partial is `src/overrides/partials/copyright.html`).

## [0.3] — 2026-07-09

- **Fix: an arch-broken heavy dep no longer blocks commits** — the weight generator guarded optional
  numpy/matplotlib with `except ModuleNotFoundError`, which does NOT catch a wrong-arch/ABI `dlopen`
  failure (a *bare* `ImportError`), so an arm64 numpy under an x86_64 python crashed the `weight` lint
  gate and blocked check-in. Broadened the guards to `except ImportError` (degrade to the math path),
  added a `lint.py` check that flags the narrow pattern, and documented the rule (CLAUDE.md § Optional
  Heavy Dependencies).
- **2d label cleanup** - pass to clean up messy and unreadable labels on all 2d diagrams
- **IBC report — diagrams inline** — the IBC stacking report embedded its 8 construction sheets only in
  the §8 gallery; each sheet now also appears **inline next to the section it illustrates** (cross-section
  + frame elevations in §3, fastening details in §4, bulkhead ports in §6, internal plumbing in §7),
  matching the other reports. The §8 gallery stays on the site but is `brochure:skip`-ped so the PDF
  shows the inline set only (no double-embed).
- **Brochure reconciliation** — Reduced dead space in the document (e.g. heading spacing, diagram size), removed sections that were not required (e.g. operating manual), followed format style of github site, and general re-organization of the PDF content.
- **3D overview scene + label pass** — reworked the per-subsystem scenes so each reads cleanly: the
  Ventilation scene gains the Fan A/B power cables (own tag) routed back to the EP, drops the
  plumbing-panel pump wiring, and shows only the evap-cooler (Cct E) circuit at the external panel — the
  PV + E-stop runs split onto a new "EP Ext Wiring" tag, kept in the Electrical scene. Labeled-scene
  leaders fixed (Fan B exits the cargo-door end, the filter-skid leader lands on the filters) and the
  solar array is ghosted so the exterior labels read through it.
- **Spray-bar supply hose** — added the flexible coiled feed from BV-05 (90° elbow → coil) up to the
  raised spray-bar feed pole, in both the overview and water models.
- **Spray-bar carriage bolts** — the tray-facing clamp-bolt heads are now drawn **countersunk** (a flush
  frustum seated in the clamp underside, top nut still proud) in the 3D model, matching the 2D detail.
- **Walkway top-rail brackets** — restored the film-plane **top-rail wall-seat saddle brackets**
  (interior back-plate + exterior through-bolted plate, at both the near and far walls) that the walkway
  model had dropped; the bottom rail stays on the shared combined corner plate.
- **Electrical focus model** — dropped the ghost ceiling so the model orbits freely without it occluding
  the gear, and added the two fan-feed callouts (Cct-A → Fan A at the sealed end; Cct-B → Fan B wall box
  + flex jumper) to the Labeled scene.
- **Water model cleanup** — the pinhole-wall water model drops the external EP panel + evap cooler, adds
  the spray bar for context, removes the green PV / gray E-stop EP cables, and reconnects the purple
  Cct-C pump feed to the panel's own master switch.
- **Non-destructive Sketchfab metadata** — the in-model metadata stamp is now fill-only-if-blank, so a
  regenerate / re-send never overwrites a model's saved title, description, tags, or stable UID.

## [0.2] — 2026-07-07
- **Electrical Panel Redesign** — the EP was reorganized into a tall narrow **vertical column** (battery
  packs re-stacked vertically, gear above, PV array disconnect dropped to operator reach) to fit the one
  clear wall band between the pinhole, chem shelf, and transport-stay anchors; the layout is formalized
  into `tbs_constants`. The 5026 fuse block and the IP65
  enclosure was corrected to its real datasheet footprint. The overview's EP now **delegates to the electrical model's builders**, eliminating
  the hand-maintained duplicate that kept drifting. Cascaded to the 2D (battery drawn as the stacked pair;
  Sheet-5 panel layout redrawn as the full column) and the weight CG. The near-walkway 500mm **widened
  access band** was then re-worked around the EP + chem shelf. The **EP column relocated left**
  to fit inside it, and the **chem-shelf
  depth trimmed 300→225** for walk-around clearance (275mm past the shelf, 328mm behind the EP).
- **Reconcile part dimensions** - resolved a number of drifts from the actual part dimensions vs. what had been
  codified and drawn in 2d and 3d models. Some parts rectified were evap cooler, skate wheels, film plane pivot, saddle straps etc.
- **Drift-tooling hardening** — added `lint.py --verify-all`, a staging-independent full sweep that
  regenerates every model `.rb` and byte-compares it against the working tree, catching **committed-stale**
  outputs that the staged-diff missing-cascade check can miss; wired it into the `publish.sh` deploy gate.
  Promoted the release-only `check_unused_imports` to a per-commit `lint.py` advisory and cleaned the 14 imports
  the EP re-lay had orphaned.
- **Single-source facts audit** — registered 5 previously-unpoliced system constants as `facts.yml` facts
  (corridor width, container rib spacing, IBC stack height, widened near-walkway, clamp spacing), each a
  `constant:` reference with a tight, verified alias, so a future prose restatement of these now trips the
  drift gate; wrapped the corridor-width restatements in `plumbing-report §3.2` as auto-updating placeholders.
- **Distortion-render de-duplication** — `tilt-swing-board-analysis §4` re-embedded the same nine C0–C8
  combined renders that `distortion-renders §3` (the dedicated gallery) already owns; §4 now points to the
  gallery and keeps only its unique content — the projection model and per-configuration optical analysis
  (renamed "Combined Distortion Analysis").
- **Walkway grating corrected 15mm → 25mm** — the 15mm molded-FRP grate was a **bogus spec**: the thinnest
  molded FRP made is 1"/25mm. Corrected to 25mm; the extra 10mm is absorbed **upward**, verified against the full 56° hinge-panel swing arc (arc only crosses the removable lift-out decks + open tray). Cascaded: film-plane
  bottom rail `RAIL_OFF_BOT` 150→160
  (−10mm image, FP wall anchors move), battery + evap-stow +10mm, grate weight 11→12.7 kg/m²

## [0.1] — 2026-07-03

Initial release of the basic design of all system components, and their integration
