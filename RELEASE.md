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

- **Stainless-grade reconciliation (304 vs 316) — system-wide policy.** The cyanotype wash has no
  chloride, so 316's pitting resistance is unused → **304 (A2) is the default** for all wet structural
  stainless; 316 is metallurgically unneeded (kept only on the tray seam bolt by choice). Codified as a
  policy block in the `parts.py` registry header. The actual corrosion gap was zinc fasteners in wet zones,
  so upgraded `bolt-m6x20` (×2) + `bolt-m8-fixing` → 304 A2-70; the M12 structural through-bolts keep
  Grade 8.8 zinc (strength + exterior inspectable heads). 410 self-drillers + chrome-steel bearing kept.

- **Film-plane U-joint selected: Belden SSNBUJ750x3/8KB (Grainger 41D816).** Reviewed the plain
  UJ-SS750x375 datasheet (dims confirmed) but it has no retention, so switched to the **needle-bearing,
  keyed (3/32×3/64 key) + set-screw, factory-booted** stainless variant (45° confirmed, $252.13 ea). BOM:
  new `fp-ujoint` + `fp-ujoint-key`, dropped the separate `fp-ujoint-boot` (integral boot); costing +~$403
  → grand-total mid $30,627→**$31,032**. Cascaded the part number + "needle-bearing / keyed / factory-booted"
  across the constants (`UJOINT_BOOT_OD` 32.54), Sheets 3/8/9 (J3/J4 → keyed stub + key), the film-plane
  report, blueprint spec, and cost breakdown. **The 3D model (`film-plane-mechanism`) label re-send is
  pending** (code updated, needs a `--send` + save).

- **Film-plane corner — Belden U-joint reviewed + carriage-plate hole pattern firmed.** Reviewed the
  Belden UJ-SS750x375 datasheet (`eng-specs/`): OD 19.05 / length 68.3 / 45° all confirmed. Finding: the
  plain part has **no keyway/set-screw** — moving to the **set-screw bore variant** (part # pending) so
  both bores clamp the 3/8″ stub (J3/J4). Captured the **boot envelope** (`UJOINT_BOOT_OD` 33.34 /
  `UJOINT_BOOT_LEN` 31.75, from the vendor OL 1.25″ / OD 1-5/16″). And firmed the **carriage plate** at
  **80×181×6 mm 6061-T6** (`CARRIAGE_PLATE_*`, grown +10 for keeper-axle edge distance) with its hole
  pattern — 4× Ø10 stub-axle (40×38) + 4× M8 (J1) + 2× M4 (cam), all ≥2×Ø from edges — drawn on Sheet 3
  View A and firmed in the `fp-carriage-plate` BOM spec.

- **Film-plane corner — Phase-1c load case computed + decided → Sheet 10.** New `fp_corner_load.py` (driven from
  `tbs_constants`, renders `film-plane-sheet10.png`). **C2** verifies the cross-slide travel: Z (tilt ±40°)
  = 245mm and X (swing ±28°) = 257mm exactly match `XSLIDE_Z/X_TRAVEL`. **C1** the per-corner load (W/4 =
  124N) → X-slide bending safety factor — bar orientation is decisive, **DEEP** (38.1mm in the load
  direction) SF≈10, **FLAT** a marginal 1.7 (fails at ×2). **DECISION (Alvin): bars mounted DEEP.**
  Promoted the review sheet to **film-plane Sheet 10** (set renumbered 9→10); the decision is annotated on
  the sheet and recorded in the blueprint spec §Phase 1c (`XSLIDE_*` `reserved→firm`), the parts spec, and
  the fabrication sheets (Sheet 3 note + Sheet 8 cross-slide "MOUNT DEEP" callouts).

- **Film-plane material-drift sweep + wired `CORNER_PLATE_T`.** The corner blueprint changed the depth
  rail 304 SS → 6061-Al and the cross-slides 316 → 304 SS, but stale labels survived in living docs —
  swept "304 U-channel"→6061-Al and "316 cross-slide"→304 in `funding-proposal`, `project-cost-breakdown`
  (prose + BOM row), `project-summary`, and a `parts.py` comment (source of truth was already 304/6061-Al).
  Also wired the previously-dangling `CORNER_PLATE_T` (¼") constant into the Sheet-9 corner-plate label
  (was a hardcoded `¼"`). Logged the still-open Phase-1c load/bending-SF + XSLIDE-travel review in TODO.

- **Film-plane Sheet 1: carried the ALU-frame dimension style.** The plan-view span dim is relabeled
  "RAIL SPAN" → **ALU FRAME WIDTH 4389mm** and colored the frame's blue, matching Sheet 7, so it reads
  as a frame dimension distinct from the gray container envelope (INTERIOR LENGTH). And **repurposed the
  right-side vertical dim** — formerly the optical axis / focal length (not of interest on the plan) — to
  **ALU FRAME HEIGHT 2094mm** (blue, marked "into page — REF", since a top-down plan can't show height
  spatially), so the frame's full W×H reads on Sheet 1. (Sheet 2 left as the swing/motion diagram — it
  doesn't reference the static frame.)

- **Film-plane blueprint: Sheet 7 upgraded from system-arrangement to fabricator-grade GA.** Added the
  frame-fabrication content a shop needs: DETAIL A corner joint (45° miter + TIG fillet, per the joint
  decision) with the 2"×2"×3/16" 6061-T6 angle callout; the ACM backing strip layout (4 vertical Dibond
  strips, 3× 1219 + 1× 732 mm, 3 butt seams, splice-battened); and the 58× nylon-spring-clamp stations
  @ 150 mm (top + 2 sides). Also fixed a rail-material drift — the rail was labeled both "304" and
  "6061-Al"; it is 6061-Al 76×38 U-channel throughout now. (Sheets 1 & 2 to follow.)

- **Film-plane blueprint: fixed stale `X150` left-rail labels** on the 2D sheets — the corner-edge
  resolution moved the left rail to X260 (`FP_X_L`) and the geometry auto-followed the constant, but
  five hardcoded callout/comment strings still read "X150". Now reference `RAIL_X_L` so they can't drift
  again (rendered labels use `X{RAIL_X_L}`). Groundwork for taking Sheets 1/2/7 to fabricator grade.

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

- **Editorial + FP_X_L=260 doc-consistency sweep.** Wrapped 26 restated values in `<!-- fact:KEY -->`
  placeholders so they auto-cascade (corridor 270, rib 457, walkway 500, clamp 150, IBC stack 2,336 —
  the last gaining `display: comma`); fixed the American-spelling gate (`grey`→`gray`); and finished the
  FP_X_L=260 leftovers in the position/mass tables (left/optical zone 150→260, tray 170→280). The tray
  narrowed to 4,349mm, so its modeled mass drops 116→114 kg — cascaded through the weight model (dry
  3,254→3,252, loaded 5,054→5,052 kg) and its 5 diagrams. Also fixed a pre-existing weight-model drift:
  the film-plane carriage mass in the detail table (57→51 kg, now wrapped in the `wt-comp-film` injector
  so it can't drift) and its generator note (92→58 clamps, now derived from `CLAMP_N_TOTAL`).

- **Film-plane LEFT edge pulled inboard of the pivot hub (`FP_X_L` 150→260).** Resolved a hard
  clash found once the detailed corner was in the light-trap: the backing-side carriage rode the X150
  rail straight into the swing-pivot hub (which can't be relieved — strength — nor passed through).
  Explored outboard vs inside vs pinhole/optics trades; chose **inside** — relocate the whole left corner
  (rail + carriage + frame) inboard, past the hub's r60 bearing (reaches X235). Also **pinned `PIVOT_X` at
  175** (was `RAIL_X_L + BRACE_RHS//2`, so the post had been chasing the rail — the reason the first
  attempt at 244 didn't clear). Costs ~110mm image width (`FP_W` 4499→4389, active area 101→99 sq ft); the
  now-asymmetric plane re-centers the pinhole (`PH_X` 2399→2454, +55mm). Cascaded to facts/CLAUDE.md optics
  table, 11 diagram generators, and 8 SketchUp models. NB: the removable-rail lift-out STAYS — the inboard
  move clears the pivot region but the panel's long swing arc still crosses the rail in the near/removable
  zone (Yd ~1950–2066), so that section must still lift out for transport.

- **Detailed corner mechanism reused into every container-scale model + parked film + web-vertical
  rail cascade.** Both film rails stood web-vertical (new single-sourced `FP_RAIL_*` block: ZC_BOT 270 /
  ZC_TOP 2300 / section 76×38); the combined BR corner plate grew to back the Z270 rail. `overview`,
  `walkway`, `water`, `lighttrap` now embed the real fpm corner (rails + skate + carriage + cross-slides
  + U-joint + 304 corner plate) via `fpm.corner()` reuse — one source, no duplication. Added a `keep=`
  fixed/removable filter to `fpm.corner()` so lighttrap's Panel-Swing DC keeps only the removable rail
  section (fixing a shared-material over-match that had hidden the brackets in transport). Film plane
  parked 50mm forward of the hinge post for legibility (`FP_Y_PARK`, display-only). Walkway film beams
  split onto a `Film Plane Left` tag (dropped from the Right-Cantilever scene) + scene reorder; lighttrap
  roof/side-walls removed for orbiting.

- **Film-plane corner mechanism — definitive engineering blueprint (milestone template, branch
  `corner-eng-design`).** Upgraded one corner from arrangement-schematic to fabricator-ready, driven
  from `tbs_constants` so it can't drift: sheets 3/4/8/9 dimensioned (skate roller ODs + 40mm pitch;
  rail wall-flange bolt pattern; cross-slide bar section/travel/gib/UHMW; U-joint envelope Ø19.1/68/bore
  9.53/±45°, J5 hole pattern, L-plate 6×8 bend); **J1–J5 fastener schedule with torque/class/washer/locker**
  (M8 24 N·m, M6 10 N·m, setscrews ~2.5 N·m); a **datum + tolerance scheme** (datums A/B/C + GD&T). Firmed
  the load (162 N/corner, section SF 4.5/27) and, to hold ±40°/±28°, grew the cross-slide bar (+$135 film).
  Reconciled the drift: cross-slide 316→304, U-joint Ruland→Belden, rail supplier/material, and the top
  (guide) corner from flat→**web-vertical with the same captured skate** as the bottom — which corrected the
  3D model (film top 2290→2252) to match the existing `FP_H`=2094 (no FP_H/optics cascade). `film-plane-mechanism.skp`
  re-sent + re-uploaded. _(Not yet merged to main.)_

- **Pump-run support-detail fabrication sheet (#29 follow-up).** New `generate_support_detail.py`
  → `support-detail-sheet1/2.png`. Sheet 1 = face-on board elevations (far / near / near-upper —
  18mm ply, 4 L-brackets each, risers + P-clip rows, fully dimensioned); Sheet 2 = the L-bracket
  flush-mount plan section (post inner face → 6mm weld leg → 45mm landing leg → ply seated flush,
  fastened with an M6 countersunk flat-head screw into a captive pronged tee-nut), a P-clip
  cross-section, and a fabrication schedule (3 boards / 12 brackets /
  39 clips). Geometry imported from the `cp` model constants so it can't drift. Embedded in
  plumbing-report §5.3; registered in the gallery, publish, setup_docs, and dependencies.yml.

- **Construction sequence — far support board staged one click later.** In the Phase 1
  click-to-build, the far-wall pump-run support board (DV-01/P-02/P-01 risers) now reveals on
  **click 4 (with Fan A)** instead of click 3 — click 3 drops in only the near-wall boards. Added
  a `sides=` filter to `cp.support_boards()` and a `boards=` param to `cp.equipment()` (both
  default to all, so overview/water are unchanged); construction step 1.3 draws `boards=("near",
  "near-upper")` and step 1.4 adds `support_boards(sides=("far",))`. Construction-only re-send;
  geometry set unchanged (interference 0/0).

- **Pump-run support boards in the IBC plumbing corridor (#29 follow-up).** The cantilevered pump
  risers on the two corridor side walls now land on **three 18mm ply boards** (far wall + lower and
  upper near-wall boards), each recessed **flush**
  in the window between the front & rear side-posts (399mm wide) on **welded steel L-brackets** (one
  leg welded to each post inner face, the ply bolted to the landing leg — the rear-panel method), with
  the risers held by **cushioned P-clips**. The five risers were pulled **flush onto the boards**: the
  **DV-01 recycle line re-routed** off IBC-3, across and **down the far board**, then two 90° turns into
  DV-01 (was standing 75mm proud); P-02 discharge / P-01→ACC-01 / P-02 suction nudged to the board plane;
  P-05 inlet already there. The **same P-clip method was extended** to the **drain-riser spine**
  (the 3 gray waste risers — X4 waste / DV-02 / DV-01→merge) and the **filter-skid panel** (the
  3 vertical runs — DV-02→F1 + tray-sump→P-04 nudged to the Yd35 clip plane, F3→SV-01 already there —
  plus the horizontal runs: brown ± ACC-02 flush, and standoff clamps on the blue ± SV-01 and the
  brown DV-02 row). **Operability + review pass:** BV-03 handle rotated to −X (cargo door); a second
  **upper near board (Z1260–1950)** backs BV-02/BV-06 + the brown P-05 (Z1300) and gray P-03 (Z1902)
  horizontals; BV-02/BV-06 handles rotated +Yd into the corridor and their loops pulled to the
  **walkway edge (X4770)** for reach, labels moved to the valve centers on the operator side;
  spine far-side X-port lines (P-05→X3, P-03→X4) clamped; the DV-01→IBC-3 tote entry dropped to
  Z1080 with the flange seated on the cage edge and the run simplified (straight in, no drop-jog).
  3D done in **water** (`.skp` saved + uploaded). **BOM/cost:** 3 ply side boards (cut from the
  corridor 4×8 offcut — no added ply), 12 welded L-brackets, 39 cushioned 3/4" P-clips →
  **+$33/$46/$61 water** (grand total $26,024/$30,492/$37,028). **Cascade complete:**
  overview/ibc-stack/construction re-sent + uploaded; interference re-audit clean (0 crossings,
  after a hump on ACC-02→BV-05 to clear the nudged tray-sump riser); plumbing-report §5.3
  support-scheme narrative; panel-layout 2D shows the side boards edge-on on their L-brackets.

- **Diagram polish.** Film-plane **Sheet 6** clamp notes single-spaced + word-wrapped to fit the box
  (was double-spaced with note 5 overflowing); **Sheet 4** notes box shrunk to fit the text (was ~2×
  too wide); **pinhole-wall-elevation** now draws a proper **crossover** (semicircle jump) where the
  ACC-02→BV-05 recycle run crosses the P-04 sump-pickup riser — it was reading as a joint. Round 2:
  **Sheet 9** note block reduced to ~50% page width + line-wrapped to fit; **water-system Sheet 3**
  notes box widened 5%.

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
  spray-beam clearance (15→11.6mm). **#27:** the mid-span support was already modeled + costed (2 center
  arms off the IBC uprights) — cleaned up the stale "*planned*" language to present tense and re-ran the
  deflection/strength check against the real section. Real 2×1 pricing corrected the RWK frame (+$107/+$123
  walkway; the old $28–40 was a guess for a non-stock section); grand total → $25,991/$30,446/$36,967.
  8 diagrams + 6 model `.rb` regenerated (`.skp` re-send pending).

- **Braided flex on both ports of every pump (#29).** Extended vibration isolation from inlet-only
  to **both the suction and discharge** of all five pumps — a braided ½" jumper de-couples each pump
  from the rigid PVC run so vibration can't fatigue-crack a solvent-weld joint (P-04's suction is the
  1" tray-drain hose → 9 new ½" jumpers). Shown on the water-system P&ID (a flex coil on both ports
  of P-01…P-05); BOM adds the 3rd braided length + **18× ½" barb couplings** (Rain Bird BC50-20) +
  **18× SS clamps** (Everbilt 671255E), **+$55** water. Plumbing-report §5.2 made explicit. **3D done:**
  a corrugated flex jumper on both ports of the 4 corridor pumps (P-01/P-05/P-03/P-02) + P-04's discharge
  on the skid = 9 jumpers, reusing the `_flex_jumper` builder (capped so it can't overshoot the turn).
  All flex connectors (pump + IBC-tote) now render **bright yellow** (`C_FLEX #FFD500`) so a jumper
  stands out from the same-color pipe it splices. The **panel-layout 2D elevations** now show a gold
  flex coil at every pump port too (corridor column P-01/P-02/P-05/P-03 both ports + the P-04 skid
  discharge). All 7 affected models re-sent + saved. #29 complete.

- **Captive tee-nuts for every removable ply-mount joint (#30).** Every machine-screw interface into
  the 18mm exterior ply — 3× Big Blue filter housings, the P-04/SV-02/DV-02 skid row, ACC-01/02, the
  5× Shurflo pump-mount shirt, valve brackets, the EP panel, the chem shelf, and the Fan-B band — now
  lands on a **back-face 4-prong tee-nut** with a machine screw instead of a wood/lag screw: a
  re-torqueable, serviceable joint that can't strip the ply. Firm hardware: **¼-20** (Everbilt 825001,
  $1.57/4-pk) + **5/16-18** (Everbilt 825091, $1.57/4-pk) zinc pronged tee-nuts, ~8–9.5mm barrels that
  seat from the back of 18mm ply. Machine screws downgraded SS→**zinc** (dry backboard mounts). The
  filter joint converts lag→machine-screw; plumbing-report §3.1/§7.2 rewritten (the retired
  slotted-angle frame text removed). Zinc machine screws firm too (¼-20 Everbilt 826771, 5/16-18
  831121, both $1.57). Net **+$32** water; grand total → $25,829/$30,281/$36,789.

- **Ball-valve sourcing + BV-05 spray selector re-designed as two 1/2″ valves.** The five 1/2″ 2-way
  isolation valves (BV-01/02/03/04/06) re-sourced Banjo V050FP → **Grainger 803HZ1 at $24.14** (from
  US Plastic $44.27, **−$120**). No 1/2″ 3-way L-port is stocked (only 3/4″ Banjo V075BL $72.88 +
  reducers), so **BV-05 became two 1/2″ valves**: **BV-05a** (3-way Blue/Brown selector, reuse the
  #22365 divert valve) + **BV-05b** (2-way spray on/off, **wall-mounted** above the selector, off the
  moving spray-bar pole) — all 1/2″, no reducers, no L-port OFF-detent risk, ~$37 under the L-port
  (net water cost this pair: **−$96**). Modeled in all four 3D models (water/overview/construction/
  ibc-stack); plumbing report §4.1 rewritten. The **overview** opening camera was also turned 180° to
  look into the container from the far wall.
  Follow-up: **fixed a BV-02/BV-05 numbering collision.** The pinhole-wall spray constants
  (`BV02_X/YD/Z`) actually positioned the spray selector, so they and every spray-context label
  were renamed **BV-02 → BV-05** (constant, wall-elevation, spray-bar diagram, hose BOM, operating
  manual wash procedure + valve matrix now carry BV-05a/BV-05b). The real **BV-02** now names only
  the corridor P-05 (Brown drain) suction isolation valve. Value-preserving rename — no `.skp`
  re-send.

- **Sump→P-04 suction re-routed off the pinhole wall.** The tray-drain suction ran as a tall riser
  straight up the pinhole wall (a clash); it now rises only ~150 mm above the walkway deck, turns 90°
  toward the skid, runs above the walkway, then a second 90° turn up into P-04 at the skid. Cascaded
  through `skid_plumbing()` into **water/overview/construction/ibc-stack** (all reuse it), and the 2D
  **pinhole-wall-elevation + water Sheet 4** cross-section were redrawn to match; interference audit
  clean (0 pipe crossings, the re-route added none). The **ibc-stack opening camera** was retargeted to
  the filter-skid panel viewed from inside the container. **BV-05** documented as a 3-way **L-PORT**
  spray selector (Blue-open / Brown-open / closed; a placeholder in the BOM — real L-port SKU to source,
  see TODO).

- **Muslin re-cut to fit the washable tray; spray-beam lift-out resolved operationally.** The muslin
  is now cut to the **washable tray area** — **4,359 × 2,000 mm** (`MUSLIN_CUT_W/H`), narrower AND
  shorter than the film-plane ACM+frame (4,499 × 2,094) so it lies flat clear of the side rims and the
  near-rim sump well; the tray, not the optics, is the size constraint (captured print ~94 of the
  101 sq ft plane; muslin yardage 388→360 yd, still 3 rolls, no cost change). **No lift mechanism:** the
  beam parks at the pinhole-wall end, the muslin is fed through the far drop-slot and pulled to it, then
  the beam rolls back over the laid muslin to wash; deep maintenance extracts the beam through the
  removable right-walkway grate (processing-tray report §4 + op-manual). Sump pickup nudged 13 mm
  (`PROC_TRAY_DRAIN_X` 2,399→2,386) so the riser lands in a clear walkway-bracket bay. New
  `MUSLIN_CUT_*`/`MUSLIN_AREA_SQFT` constants + muslin-cut facts. *(5 model `.skp` — water/overview/
  construction/ibc-stack/spraybar — pending re-send for the 13 mm sump shift.)*

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

- **2D drawing set rebuilt to the skid design.** `pinhole-wall-elevation`, `pinhole-panel`, and
  `corridor-panel` sheets were rebuilt to the current wet-end (filter skid + corridor split), and
  **water-system Sheets 3 & 4** rewritten to the center-drain design (Yd-only slope plan; sump-riser
  cross-section → P-04 on the filter skid). Suction enters P-04's top per convention; ACC-02 → BV-05
  spray connection drawn; filter-skid flow uses the pipe-drawing convention.

- **P-04↔P-02 wiring + roster swap cascaded everywhere.** The pump swap was carried through
  `electrical.skp` (Circuit-C wiring parity), the electrical report + 2D diagram + layout prose, and a
  closure sweep of every corridor-roster reference (weight analysis, ibc-stacking legend, cost
  breakdown, component-dependency-map, water-system equipment table) so no doc still lists P-04 on the
  corridor.

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
