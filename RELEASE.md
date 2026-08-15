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

**`bash release.sh X.Y`** automates steps 2–3 (promote → commit → tag → `gh release create`) and
**refuses to proceed if [Unreleased] is empty**, which is what enforces the gate.

---

## [Unreleased]

- **IBC frame Sheet 4 — fourth review pass + label tidy.** DETAIL A: the J7 retention bolt is now **vertical**
  (down through the bar into the seat), not horizontal into the wall plate. DETAIL B: **flipped horizontally**
  (corridor upright on the right, bar running left to the wall) so it reads as the wall-on-left assembly.
  DETAIL D: the rear panel is bolted **through the welded metal tab into a pronged tee-nut in the ply** (M8 hex,
  J4), replacing the countersunk-from-ply-face depiction — matches the schedule. DETAIL E: renamed **side-panel
  pipe-run L-bracket** (the near/far side-wall boards carry the pipe runs via P-clips, **not pumps**) across the
  drawing, report §3.5, and the parts spec. Ran the label skill over the sheet — terse in-cell tags, prose moved
  to a **tightened single-spaced notes band** (added Cleat (B) + a consolidated "Where used" line), no more
  crossing text.

- **IBC frame Sheet 4 — third review pass (A/B/D/F).** DETAIL A: the wall-hanger weld is reassigned to
  the PLATE weldment (seat↔pocket back-plate, W5) and the retaining bar is now **bolted** to the pocket
  (new fastener **J7**, an M12 retention bolt — 1 per bar × 8), so the bar is removable, not welded, to
  the hanger (+8× M12×40 in the BOM, +$12). DETAIL B: added a jagged break so the bar reads as continuing
  to the wall hanger. DETAIL D: where-used note made specific (3 per back upright × 2 = 6; see Sheet 2/3).
  DETAIL F: added a **PLAN SECTION** (top-down) beside the elevation so it lines up with the 3D model, and
  corrected the clamp bolt pitch label (was 112 mm → **~37 mm**, matching `ibc_cantilever_arms`). Report
  §3.5 gains J7 + the W5 clarification.

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

- **IBC frame blueprint Phase D detail insets → new Sheet 4 (Fabrication Details).** `ibc-frame-sheet4`
  draws the connections a shop builds from — **A** wall joist hanger (per-bar 2-bolt, 50 mm bolt
  clearance, 60×205×8 backing plate), **B** bar→upright cleat, **C** weld-on lashing ring, **D** rear-panel
  bracket, **E** pump-support L-bracket, **F** walkway arm→upright clamp — each with its weld (W) + fastener
  (J) callout and a notes cell.
  Registered in the gallery / publish.sh / setup_docs and embedded in report §3.5 + §8 (frame set now 4
  sheets). Completes the IBC-corridor metal blueprint (A–E) — validated design + fastener/weld/tolerance
  schedules + cut list + detail sheet.

- **IBC frame blueprint scope EXTENDED to the whole IBC-corridor metal construction.** The deep-box frame
  is one welded structure serving three roles, so the review now also covers the plumbing-corridor metal
  that shares it. Added **service + walkway load cases** (`ibc_frame_load.py`): the plumbing panel + pumps
  (~33 N/bracket, trivial) and the right-walkway cantilever (each arm ~1.2 kN at 325 mm = a 395 N·m moment
  into the front upright → upright bending **SF 6.9**, arm→upright bolted-clamp connection **SF 3.8**) —
  both non-governing vs the EN 12195-1 transport case. Extended report §3.4 (service cases), §3.5 (J4 panel-
  bracket bolts, J5 pump-support-board fixings, J6 arm clamp; welds W6 panel-bracket, W7 L-bracket, W8
  ribbon-beam), §3.6 (panel-mount + L-bracket landing tolerances), and the sheet-1 cut list (+6 rear-
  panel brackets, +12 pump-support L-brackets, +4 ribbon cross-beams). Walkway-arm CONNECTION checked here;
  the arm's own detailing stays with the walkway blueprint (Alvin's boundary).

- **IBC frame blueprint Phase C + D-core: datum/tolerance scheme + fab-sheet detailing.** Report §3.6
  adds the datum scheme (A = 4-foot plane, B = front-upright faces, C = corridor CL) + functional
  tolerances (foot coplanarity ±1.5, upright plumb ±2/2296, diagonal square ±3, hole PCDs, corridor width
  +2/−0; general ISO 13920 Class B, welds AWS D1.1). `ibc-frame-sheet1` now carries a **member cut list**
  (lengths computed from the frame constants) + a **DATUMS & TOLERANCES** callout block, and the fab notes
  fold in the §3.5 weld schedule. Cleaned stale sheet literals (100×80→60×205 backing plate, ~119→~123 kg,
  bar Z560/1760→Z500/950+1500/1950). Remaining Phase-D refinement (dedicated hanger-fold / backing-plate /
  cleat / lashing-ring detail insets) tracked in `ibc-frame-blueprint-spec.md`.

- **IBC frame blueprint Phase B: fastener + weld schedule.** Added `ibc-stacking-report.md` §3.5 — every
  bolted joint (J1 floor self-drillers ×16 driven-to-seat; J2 bar→upright cleat M12×40 A2-70 ×16 @ ~50 N·m
  + anti-seize; J3 wall-hanger through-bolt M12×65 Gr.8.8 ×16 @ ~90 N·m) with grade/torque/washer/locking,
  and every weld (W4 lashing-ring→bar 6 mm fillet SF 9.1, W3 cleat→upright 4 mm SF 37, W1/W2/W5 minimum
  practical fillets), sizes computed in `ibc_frame_load.py`, torques cited (Fastenal/Bossard/ITW-Buildex).
  Caught a Phase-A miss along the way — the bar→upright cleat bolts were still qty 8; doubled to **16** with
  the 8 bars (+$12 ibc-frame). Grand-total mid → ~$31,158.

- **IBC stacking frame — blueprint Phase A: EN 12195-1 transport-restraint validation + redesign.** Took
  the IBC restraint frame from a qualitative "it's trapped" note to a computed load case
  (`ibc_frame_load.py`, new). The camera runs **self-contained**, so it transports **with water aboard** —
  the [EN 12195-1:2010](https://cdn.standards.iteh.ai/samples/32961/4592590bcf194f1a8ffa917a5db7d258/SIST-EN-12195-1-2011.pdf)
  loaded case (0.8 g forward braking, a full 965 kg top tote) governs. The single 50×20×3 front bar is
  weak-axis (20 mm in the load direction, film-rail-slot-limited) and **fails (bending SF 0.79)**. Redesign
  **R5**: **two 50×20×3 bars per tote face** (4→8) **+ certified anti-slip matting** (μ 0.2→0.6) **+ 2
  straps/stack** → bar **SF 1.59 bar-alone / 4.77 with the mat**, all downstream elements SF ≥ 8, drained
  state SF ≥ 12. Fab-detailed the restraint in the 3D model: bars **butt** the corridor uprights + the
  wall-hanger back plates (cleated joints read as joined, not one continuous piece); **8 identical per-bar
  2-bolt wall hangers** (16 through-bolts = same 16 wall penetrations as before) with the bolts stacked
  vertically, **50 mm clear of the seat** for wrench access; the pair spread ~450 mm so each hanger has
  room. Cascaded through `tbs_constants` (IBC_FRONT_BAR_*), the 3D `tote_restraint()` (5 models re-sent),
  the weight model (frame 90→123 kg), `parts.py` (+anti-slip mat, 8 hangers + 8 backing plates) + costing
  (+$78/$146 ibc-frame), the ibc-frame/ibc-stacking 2D sheets, and `ibc-stacking-report.md` §3.2/§3.4. New
  tracking doc `ibc-frame-blueprint-spec.md`; Phase B (fastener + weld schedule) next.

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

_Nothing yet — add a bullet per notable change here as work lands._

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
