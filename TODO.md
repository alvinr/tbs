<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
<!-- Working/internal tracker — NOT published (not registered in publish.sh). -->
# TODO & Actions — TBS-001

The **single record** of outstanding actions across the project. Review and tick here; add new
items as they arise. Tick `[x]` when done (leave a one-line note), or delete once it's clearly
historical. Detailed sub-trackers are linked where the detail is extensive.

**Completed sub-trackers (for reference):** [editorial review](editorial-review-todo.md) — DONE 49/49.

---

## ★ MAJOR MILESTONE — manufacturing-ready blueprints (ALL drawing sets) — OPEN

_Alvin's call (2026-07-16): the current 2D sets are arrangement-faithful schematics (true-proportion +
topologically correct, reconciled to the 3D) but NOT manufacturing blueprints. The milestone is a
**definitive, dimensionally-correct, shippable-to-a-fabricator drawing package for EVERY subsystem** —
precise hole positions, tolerances, fastener callouts, datums, section views, material/finish, driven
parametrically from `tbs_constants` so they can't drift. Do the **film-plane corner mechanism FIRST** (below)
as the template, then roll the same standard out across all sets (film plane, water/tray/spray, IBC frame,
walkway, hinged panel, light lock, electrical, optics, …)._

### Definitive corner-mechanism engineering drawing (film plane — FIRST / template)

- [ ] Fully-dimensioned multi-view detail of ONE corner: the weight rail + skate, the wide carriage plate,
  the Z (tilt) + X (swing) 316 flat-bar cross-slides, the Ruland U-joint, the L-bracket, and the 6061 frame
  angle — with **precise hole positions** (PCD/edge distances), **fastener callouts** (J1–J5: sizes, thread,
  torque), section views, material/finish notes, and a datum/tolerance scheme. Dimensionally exact.
- [ ] Drive it from `tbs_constants` (or add the missing constants: cross-slide bar section — currently
  `XSLIDE_*` are `reserved` — U-joint model dims, hole PCDs) so the drawing can't drift from the 3D. This
  is also what firms the (still un-quantified) cross-slide bending SF and the per-corner load.
- [ ] Reconcile the TL/TR (guide) corner: it is the mirror (film below its guide rail) — the drawing set
  should cover both bottom (weight) and top (guide) corners.

## Weight model — film-plane moving mass undercounts the ACM backing — OPEN

_Surfaced 2026-07-16. `generate_weight_analysis._film_plane_carriage_weight()` = frame + 92 clamps +
4 carriages ≈ 32 kg, but does NOT include the ~53 kg Dibond ACM backing (9.6 m² × ~5.5 kg/m²) that
moves with the plane. So the "Film plane carriage" line (and thus total-dry + CG) under-books the
moving plane by ~50 kg._

- [ ] Add the ACM backing mass to the film-plane moving-mass term (RHO/area from the dibond-acm-film
  part), re-inject the weight blocks + PNGs, and re-check the CG/floor-load. Also feeds the (still
  un-quantified) per-corner load used to firm the cross-slide section.

## Film-plane report reconciliation (leadscrew Option A → U-channel redesign) — PROSE DONE, BOM GATED

_Surfaced 2026-07-16 during the frame material fix. Prose reconciled 2026-07-17 (commit 47d87d10).
The remaining §7 parts BOM is gated on confirmed prices._

- [x] `film-plane-mechanism-report.md` §1/§4/§8/§9 — replaced the leadscrew Option-A narrative with the
  304 U-channel + acetal skate + 316 flat-bar Z/X cross-slide + Ruland US12-6-6-SS U-joint + cam-clamp
  design; dropped handwheels/Acme/rod-end/pivot-pin/PA-14 + old-vs-new archaeology; §4 image now Sheet 7
  (front elevation); Sketchfab embed + `models/sketchfab.json` → film-plane-mechanism 572b… .
- [x] `component-dependency-map.md` §3.1 component roster + §3 diagram-matrix note → U-channel design.
- [~] `film-plane-mechanism-analysis.md` — scope note fixed (stops claiming it describes the built
  mechanism; optics §3/§5/§6 affirmed; hardware/BOM → report). **STILL OPEN (task #30):** the §4
  mechanism + §7 BOM + §8 maintenance are a leadscrew decision-record snapshot — DECIDE keep-collapse-
  to-optics-only vs **retire** (it's nav-labeled "(superseded)" and its optics overlap distortion-renders).
- [x] **Reconcile the two film-plane 3D models — DONE 2026-07-19.** `film-plane.skp` geometry was ported to the built U-channel/skate/U-joint design earlier this session (`_corner_parts()`, committed); `component-dependency-map.md` §3.1 now describes it as U-channel (not Option-A leadscrew) and a **film-plane-mechanism row was added** with the split of responsibility (mechanism = bolt-level single-corner detail; film-plane = same design at whole-plane scale + the animated DCs). ~~Both are~~ Both are
  KEPT (film-plane.skp is NOT retired). `film-plane.skp` = the full film-plane model (older Option-A
  leadscrew DC); `film-plane-mechanism.skp` = the current corner mechanism (U-channel/skate/U-joint). They
  describe overlapping geometry and have diverged — reconcile so the full model carries the current
  corner design (or define a clear split of responsibility). The report now embeds film-plane-mechanism; both
  stay in `models/sketchfab.json`. Also: `component-dependency-map.md` §3.1 model table (line ~480)
  still documents only the film-plane row (leadscrew DC) with no film-plane-mechanism row — update once the
  two models are reconciled (deferred: describes 3D internals under Alvin's active review).
- [x] **§7 parts BOM — DONE 2026-07-19.** Swapped the 11 leadscrew SKUs → the U-channel mechanism (1262T21 U-channel $362/6ft, USKC12-6-6-SS U-joint $276, UBOOT boot, 4040N12 support $58, 89535K87 3ft stub rod $13.25, acetal skate, 316 cross-slides, cam clamps, 304 corner plate); costing §4.1 + EXPECTED + report §7 + master + cost-breakdown reconciled (+$2.9k mid; film $6,063–7,039); prose swept (funding/equipment/summary/dimension-audit). Skate/cross-slide/cam-clamp are fab estimates — firm at order. ~~GATED on Alvin's SKU paste-check.~~ `parts.py` film section still holds the 11
  leadscrew SKUs (hgr20-rail, hgh20ca, acme-leadscrew/nut, handwheel-8in, locking-collar, crossslide-
  hgr15/hgh15ca/plate, rod-end-bearing, pivot-pin) → the report §7 table + master §4 inject them. Swap
  to the Sheet-5 corner hardware (Ruland **USKC12-6-6-SS keyway-clamp U-joint @ $276** + UBOOT12/19-NI-KIT,
  McMaster 4040N12 supports, 89535K873 3/8" KEYED stubs, Ø32 acetal rollers on Ø10 316 axles, carriage
  plate, 316 flat-bar cross-slides + UHMW + gib, cam clamps, 1262T21 U-channel). **Blocked:** McMaster
  blocks crawlers, so 4040N12 / 1262T21 / 89535K873 SKUs could not be auto-verified. Alvin to paste-check:
  4040N12 (304 shaft support), 1262T21 ($/ft), 89535K873 (3/8" 304 rod). Confirmed: **U-joint USKC12-6-6-SS
  $276**, boot $22–29, 10mm 316 rod $33–50/ft, UHMW $23–93/sheet. Then reconcile parts.py + costing (film
  band + grand_total move up ~$1.5–2.5k — the U-joint alone is $276×4) → §7 auto-injects; retires the
  parts-identity dead-SKU lint warnings. This is also the FP_W/FP_H dead-BOM retirement folded in.

- [ ] **Master shopping list — add a part number for each primary supplier.** The per-supplier shopping tables should carry the primary-supplier SKU for every line (many rows list a supplier but no part number), so an order can be placed directly. (Alvin 2026-07-19.)
- [ ] **Reconcile the EPDM gasket on the cargo-door-facing wall of the hinge panel.** Now that the top/bottom door seals are strip brushes, re-check the panel perimeter / housing-surround EPDM on the cargo-door-facing (exterior) wall of the hinge panel — confirm what stays EPDM vs brush and that the 3D/report/parts agree. (Alvin 2026-07-19.)

## Film-plane U-joint — research a cheaper alternative — OPEN

_Alvin 2026-07-17: chose **Ruland USKC12-6-6-SS** (keyway+clamp, **$276 ea**) as the interim part —
expensive at ×4 corners = **$1,104**. Research a cheaper joint that meets the FULL spec below (a MISUMI
HS-10-A-A at $96 was a candidate but its max angle was unconfirmed and its material must be verified)._

**Spec the U-joint MUST meet (one per corner ×4):**
- **Type:** single universal joint (2-axis — tilt + swing).
- **Bore:** 3/8" (9.5 mm) both ends — or metric (10 mm), then the 304 stubs resize to match.
- **Material: STAINLESS** (303/304/316) — it sits in the cyanotype **splash (wet) zone**; plain carbon/
  alloy steel (e.g. MISUMI's default S45C HS series) would rust and is NOT acceptable.
- **Max operating angle: ≥ 40°** — the plane tilts ±40° (`MAX_TILT_DEG`) and each corner's U-joint bends
  the full angle (rigid plane; the joint is the only angular DOF). Swing needs ±28°.
- **Shaft securing: POSITIVE** — keyway+clamp (as the USKC) OR set-screw-on-a-flat + threadlocker/Nypatch.
  A bare point-contact set screw is NOT acceptable (backs out under transport vibration).
- **Envelope:** ~0.745" OD × 2.688" L (Ruland size 12) or similar — fits the corner-plate/carriage stack.
- **Cost target:** << $276 ea. Candidates to chase: MISUMI HS-series **stainless** (confirm ≥40° angle;
  ~$96), McMaster stainless U-joints (SKU crawler-blocked — needs a human paste-check), Belden UJ-SS
  set-screw stainless (~$126–178). Update Sheets 3/5/8/9 + the BOM if a cheaper part is adopted.

## Muslin clamp → spring clip redesign (Sheet 6) — IN PROGRESS

_Alvin review 2026-07-17: the muslin clamp is NOT a cam-lever toggle — it's a **spring clip**:
a FIXED jaw bolted to the ALU frame edge (countersunk bolts) + a SPRING-loaded jaw that pinches the
muslin against the frame edge; squeeze the handle to open (torsion spring holds closed). Sheet 6
Panel A redrawn to this; Panel B removed (redundant — open/closed now a ghost + arc on Panel A);
CLAMP NOTES relocated + rewritten. NOT committed yet._

- [ ] **Panel A frame is the L (2×2 angle) for now.** An **offset-T** cross-section (flange holds the
  ACM + bolts to the corner carriage; ACM flush to the clamp edge) was drawn then **reverted at
  Alvin's request — PARKED**. Resolve the frame section (L vs offset-T) with Alvin later.
- [ ] **Sheet 6 Panels C (plan) + D (elevation) still show the OLD cam-lever design** — awaiting
  Alvin's call: redraw to the spring clip, or trim as redundant (like B).
- [ ] **Downstream cascade once the drawing locks:** `film-clamp-mechanism-report.md` (describes a
  cam-lever toggle), the `clamp` BOM in `parts.py` ("Cam-lever spring clamp"), and the `CLAMP_*`
  constants (`CLAMP_BASE_W/H/T`, `CLAMP_LEVER_L`, `CLAMP_OPEN_GAP`… base-plate/lever dims don't map
  to a spring clip) all need reconciling to the spring clip.

## Walkway pop-out extension — revisit past the pinhole — OPEN

_Surfaced 2026-07-17 (Alvin)._

- [ ] Extend the walkway pop-out (punch-out bay) another IBC-width **past the pinhole, toward the
  filter skid** — revisit the right/pinhole-end walkway so the deck reaches further along that end.
  Study the clearance vs the pinhole wall, filter skid, and IBC stack; cascade to the walkway 2D
  (`generate_walkway_diagram.py`) + 3D (`walkway.skp` / `overview.skp`) + master-shopping-list.

## Full audit (2026-07-04) — 53 confirmed findings → [audit-2026-07.md](audit-2026-07.md)
_Multi-agent audit across all subsystems × 5 dimensions (3 high / 28 med / 22 low), every finding independently verified. Verdict: **design is sound — no structural/optical defect**; the debt is documentation cascade-leakage. Full detail + per-finding fixes in the linked report; fix in priority order:_

_**✅ COMPLETE (2026-07-05):** all 53 findings resolved and pushed — G1–G6 (cascade/table/comment sweeps), ①·pinhole ring + ③·filter + D-ring (design decisions), and every ② datasheet blocker (wheel, pin, saddle, Powerpole, evap). All gates green throughout. (Sketchfab re-uploads are Alvin's standing manual step — not tracked here.)_

- [x] **① 3 high-severity contradictions — DONE.** BV-05 valve, pump 100→114, and the **pinhole disc retaining ring** — Alvin chose the **ring** (more serviceable): report §4/§9 rewritten, plate-drawing threaded-bore callout (M52×0.75), registry + cost (+$15/$25 optics) all reconciled, gates green.
- [x] **② Datasheet blockers — DONE.** All five settled (see ②·1–5 below): spray skate wheel, film-plane pivot pin, evap cooler, spray saddle strap, Powerpole count.
- [x] **③ Design-of-record — DONE.** **Filter** = 3 separate + slotted-angle frame (registry itemized, −$50/−$65). **D-ring count = 8** (Alvin, matches §4.1 + the 4-strap routing): `parts.py` qty 4→8, the **2D frame drawing** now draws 4/tier (8 total, verified on re-render), §9.1 BOM re-injects to 8 ea/$40–70, cost cascaded (+$20/+$35). *(The 3D overview does **not** model D-rings — that code was in the retired dead `ibc_rack()`; the live `cp.tote_restraint()` builds bars + hangers only, so **no overview re-send is needed** for this. See the 2D↔3D-parity follow-up below.)*
- [x] **④ Big cascade repair — DONE (G2/G3).** Drum +50 top-position refs → Z2250 (the drum *body* height correctly stays 2200 — the audit's `DRUM_H` bump was a false positive caught on re-render); RWK arm 405→325, walkway open-area 1,662→1,762, Fan A 2200→2000, F-01 50→5μm, LED 3rd panel, ext-panel-X, drum footprint.
- [x] **⑤ Hand-maintained-table sweep — DONE (G4).** weight-report battery/EP/plumbing rows + battery-Z constant (CG re-injected), ibc §9.3 total, cost-breakdown AmFe supplier/CV/P-05, ventilation Circuit E, fan labels.
- [x] **⑥ Low-severity comment refreshes — DONE (G6).** far-Yd/Z60/6-uprights comments, spraybar Ø8→Ø10, pinhole X=2874→2399, cost bands; + 2D derivations (evap-duct X, shelf evap-Z). *(dead `IBC_WBKT`/`BRACKET_*` constants → folded into the unused-imports cleanup below.)*

### ② Datasheet blockers — work through one by one
_Each needs a call (or a re-source), then the noted cascade. Independent — take them in any order._

- [x] **②·1 Spray skate wheel — DONE.** Re-spec'd to a **solid acetal (Delrin) Ø32×20×Ø10 plain-bore wheel** riding on the existing Ø10 **304 SS** axle — corrosion-immune + self-lubricating, no carbon-steel ball bearings (the ferricyanide/citric wash ruled the uxcell PE-body/steel-bearing part out). Kept the exact design geometry (Ø32×20×10) so **no cost/2D/3D cascade**; dropped the unsupported ≥25 kg rating (actual ~2.6 kg/wheel). Turned from McMaster acetal rod or an equivalent POM plain-bore roller. Every off-the-shelf 32-OD idler was confirmed 40mm-wide + steel-bearing, so a solid plain-bore wheel is the corrosion-safe route (316 SS bearing Ø30×9 was the no-machining alternative but changes geometry + is metal-on-tray).
- [x] **②·2 Film-plane pivot pin — DONE.** Pin was **1″ (25.4mm)** — 0.4mm too big to enter the metric `GIR25-DO` rod-end's **25.0mm** bore. Kept the well-specced metric rod-end and swapped the pin to **Ø25mm × 200mm SS316, slip-fit** (a metric Ø25 SS precision shaft/clevis pin; dropped the wrong McMaster #98173A150 1″ SKU — confirm the 25mm SKU at order). Same $8/qty-8 → no cost cascade; 0.4mm is below drawing resolution → no 2D/3D regen. Fixed the registry + the injected `parts:film` block + both hand-maintained BOM rows (cost-breakdown, analysis doc). _(2026-07-12: length corrected **200→80mm** — 200mm was an error, the longest stocked Ø25 clevis pin is 80mm and it amply spans the rod-end eye + bracket clevis. Spec, `dims`, Sheet-3 callout, and both BOM rows updated.)_
- [x] **②·3 Evap cooler — DONE.** MC18M was modeled 22×12×28in (559×305×711); official Hessaire spec is **20×10×28in (508×254×711)** — web-verified (the 22×12 was a retailer overstatement). `EVAP_W 559→508`, `EVAP_D 305→254`. Same part/$130/85W → **no cost or weight cascade**. Stow re-verified (X1450–1958, 51mm roomier). Constants + 2D + reports committed; **overview + electrical 3D re-sent, verified (cooler box 508×254×711), saved + committed.** *(Part identity was already Hessaire MC18M since 2026-06-15 — the "Portacool" note was stale.)*
- [x] **②·4 Spray saddle strap — DONE.** The report's **2mm** was the right design for a rolling-carriage axle retainer; the *cited part* (Amazon Boxonly stamped conduit clamp) was the flimsy ~0.5mm one. Re-spec'd to a **formed 2mm 304 SS saddle** (bent from McMaster multipurpose-304 flat bar, 2 bolt feet over the Ø10 axle) — matches the report, corrosion-safe, robust. Noted a 304 SS + EPDM **Adel loop clamp** (~3/8–7/16″ ID) as the off-the-shelf alternative. Same cost/qty → no cascade; dropped "conduit-style" from §3.4 wording.
- [x] **②·5 Powerpole connector count — DONE.** Alvin: **one pair per pump** → 4 → **5 pair** (P-01..P-05). +$2 cascaded through the costing WATER "Electrical (wiring only)" line, §5 EXPECTED, and grand total; BOM now 5 pair / $10; all gates green.

---

## Scheduled
- [ ] **Verify spec-driven parts (identity + price)** — 55 rows from JS-/account-gated suppliers
  (McMaster/Roton/Grainger/…) need a human to pin the exact SKU, product URL, fit-critical dim
  (bore/thread/Ø), and current price — the automated web pass can't read those suppliers. Also fixes
  4 SKU↔supplier mismatches + 12 SKUs missing a URL (surfaced by the `parts identity` lint advisory).
  Workflow: `build_parts_worklist.py` → fill `parts-worklist.csv` (new_* cols, merges on re-run) →
  `apply_parts_csv.py parts-worklist.csv` → `parts.py --inject` + `costing.py --inject` + `lint.py`.
  Alvin fills at his own cadence from logged-in supplier sessions. (Reminder block atop `parts.py`.)

## Material validation — soak tests (deferred)
Physical coupon soaks in the actual potassium-ferricyanide / citric-acid wash, deferred until the
bath is available. Both are cheap; nothing downstream is finalized until they pass.
- [ ] **UHMW pad coupon soak** — confirm virgin UHMW-PE survives the wash. It is the one
  medium-confidence item in the Option-B film-plane slide (UHMW pads on 316 flat-bar ways):
  compatibility charts list citric acid explicitly, but potassium ferricyanide is only *inferred*
  from the mild-oxidizer class. Soak a scrap ~24 h in the real bath; check for swelling, softening,
  discoloration, and mass change. Fallback if it fails: acetal copolymer (POM-C) pads.
- [ ] **Muslin soak test** — validate the muslin (cyanotype substrate) in the wash: dimensional
  stability when wet, adhesion to the ACM backing sheet, and whether it holds under the perimeter
  cam clamps. (Paired with the UHMW test — same bath, same session.)

## Design / 3D (deferred)
- [ ] **FP_H 2,388→2,138 cascade — `.skp` re-sends PENDING (code side DONE).** Branch `film-plane-redesign`:
  the active film-plane height dropped to 2,138mm (low-profile wheels-on-pipe corner, BUILD 140→110). Constants,
  parts/costing (clamp 92→90, −$8/$13/$18), all FP_H diagrams, weight, and the report prose/config table are
  cascaded + committed; `overview.rb` (film-plane geometry) and `film-plane-mechanism.rb` (BUILD 110) regenerated.
  **Alvin owes two re-saves:** (1) open **overview.skp** → re-send `generate_sketchup_model.py` → save + re-upload;
  (2) open **film-plane-mechanism.skp** (still BUILD 140 in repo) → re-send `generate_film_plane_mechanism_model.py` → save +
  re-upload. Commit each `.skp` after its upload. (Corner-gimbal Sketchfab UID `572b4aaa2d394de1b8852160d7cdcfc3`.)
- [x] **spraybar.skp axle-saddle re-spec — DONE.** The axle-retention saddle was re-specced to a fabricated
  1/8" (3.18mm) × 3/4" (19mm) 304 SS flat-bar clamp with 12mm M5 feet (was a schematic 2mm/6mm-wide token that
  couldn't hold its own bolt). 2D (sheet 2 cross-section + sheet 6 plan) + `parts.py`/report/master +
  `generate_spraybar_model.py` + `spraybar.rb` committed; **`spraybar.skp` re-sent + verified live** (8 saddles,
  19mm wide, clearing the wheel by 2mm each side, seated on the extended axle stub) → **Alvin saved + re-uploaded
  2026-07-12**, `.skp` committed. Overview does NOT model the saddle (prose only), so no overview re-send owed.
- [x] **lint blind spot — missing-cascade only diffs the working tree — RESOLVED.** Root cause: `warn_missing_cascade`
  inspects `git diff --cached` (staged) only, so it's inert on unstaged/post-commit changes and downgrades to a
  cheap fallback for wide (>5-consumer) changes — a constant committed without its full cascade slipped through
  (the film-plane/ibc-stack/spraybar models). Fix: added `lint.py --verify-all` — a staging-independent full sweep
  that regenerates all 7 model `.rb` in place + byte-compares vs the working tree (deterministic → clean signal),
  with `--diagrams` for the noisier PNG pass. Wired into the `publish.sh` deploy gate (blocks on stale models).
  The water model (`.skp`, no `.rb`) is flagged as un-verifiable. Tested: a constant bump flags the 5 dependent
  models + exits 1; the deflection/grating sweep now passes clean.
- [x] **Walkway grate deflection — RESOLVED.** The 15mm grate was a bogus spec (molded FRP's thinnest is
  1"/25mm — McNichols MS-S-100, 2.60 lb/sf). At the real 25mm a 100kg operator mid-span (457mm) deflects
  ~2.5mm — well within the ¼" (6mm) pedestrian limit (MS-S-100 ΔC datasheet); the 100mm overhang is
  negligible (short cantilever). Grate corrected to 25mm + deck raised 130→140 (Option A).
- [x] **Film-plane tilted corner vs the raised deck — RESOLVED (clears).** The Option-A film plane rides its
  corners on FIXED-Z rails (bottom rail = `RAIL_OFF_BOT` 160); tilt/swing move the corners in DEPTH (Yd),
  not Z, so the plane's bottom EDGE stays at Z160 across its full width — 20mm above the Z140 deck at every
  tilt/swing. The only element that dips lower (the corner carriage/rod-end, ~Z135) rides the FP rail lines
  (X150 / X4649), which are OUTSIDE the walkway X span (470–4629). So the film plane clears the walkway grate
  everywhere across its Yd travel + full tilt/swing range — no notch needed. (Also fixed a stale RZ_BOT comment.)
- [x] **Overview / assembly-overview / electrical-diagram corridor-filter staleness — DONE.**
  assembly-overview (relabel corridor zone → pumps+ACC, ADD pinhole-wall Filter panel zone, legend) and
  electrical-diagram (every "pumps+filters" → "water pumps"; P-01/03/04/05 corridor + P-02 wall) fixed.
  **Overview needed no change** — its `F1_Z`/`F2_Z`/`F3_Z` usage is in the dead `equipment_panel`/
  `water_plumbing` functions (zero call sites; "safe to delete"), and the live overview already draws
  the pinhole-wall design via `cp.*`/`pw.*`. **Dead-code + constant retirement DONE 2026-07-05:** deleted
  the 4 dead builders (347 lines) + the legacy `FSKID_X`/`FSKID_YD`/`FSKID_Z_LO`/`F1_Z`/`F2_Z`/`F3_Z`
  constants; live FSKID_X consumers rewired to `EQPANEL_X - BB_OD` (PNGs pixel-identical, overview.rb
  byte-identical).
- [x] **EP interior rework — REACH RE-LAY DONE in code + electrical 3D verified; overview re-send + Sketchfab pending.**
  _2026-07-06: gear dropped into the no-stool reach zone (all maintenance items Z1010–1560, was to 2100) —
  disconnect cluster (main·master·PV·E-stop) grouped at ~Z1045, Blue Sea 5026 fuse block + busbars at chest
  height, MPPT display dropped from ~1970 to ~1460; 5026 corrected to real 164×39×84; Sheet 5 fully redrawn;
  pinhole-wall/assembly/line-of-sight + weight CG + report captions cascaded; all gates green.
  **COMPLETE — electrical + overview + film-plane (EP context ghost) all re-sent, saved + uploaded to
  Sketchfab; committed (348cdedc + f4ae78dd), pushed to main.** (Say the word to tick this done.)_
  — Original scope: the IP65 enclosure internals —
  the A–G blade-fuse stack, the +/− busbars, and the wiring/circuit routing — have accreted to the
  point they're **not operator-usable**: fuses/terminals are cramped and hard to reach/trace for
  service and reset. Re-lay the internal layout for real serviceability (fuse access, labeled
  terminals, wire runs, clearances) and cascade it through the 3D (`electrical.skp` `power_core()`
  + the duplicated overview `ov.electrical()`) and the 2D (`generate_electrical_diagram.py` Sheet 5
  enclosure elevation + fuse schedule). `_pump_circuit()` re-org'd 2-column → single vertical
  column (4 corridor pumps at real AFF Z 615/940/1340/1740 per `panel-layout.png`; P-02 offset as the
  pinhole-wall pump). Was the only LIVE 2-column layout — overview/ibc-stack already use the `cp.*`
  single-column builders (overview's `equipment_panel`/`water_plumbing` are documented dead code).
  `electrical.rb` regenerated; **electrical.skp re-send pending** (see re-upload list — model not open).
- [x] **Film-plane 2D redraw (Option A) — DONE.** DC left as-is (2026-07-05 decision — a rigid DC can't
  animate the cross-slides). Redrew all 6 FPM sheets from the stale "4-CORNER INDEPENDENT / compound
  tilt+swing independently" framing to **Option A** (rigid plane, coordinated pairs; titles → OPTION A;
  Table 1 COMPOUND→COMBINED "limited, coordinated"; combined config kept but relabelled "(limited)" since
  the constants allow limited combined rigid rotation — only C7 compound *twist* is dropped). FPD dead
  compound special-case removed (output unchanged). Report's 3 prose phrasings aligned to "coordinated
  pairs". Verified visually (sheets 1/4/6); drift gates green. *(Analysis doc left as-is — it's the
  labelled historical analysis of the old stretching design.)*
- [x] **3D D-rings added — DONE.** Added 8 D-ring cylinders to the shared `cp.tote_restraint()` (4/tier on the front bars, mirroring the 2D). Overview sent + **verified 8 in the live model** (4/4 by tier). Shared function → the **ibc-stack + water** models pick them up on their next send. *(Dead `ibc_rack()` D-ring code left for a future delete.)*

## Cost / data modeling
- [ ] **Reconcile 304 vs 316 stainless steel usage — whole-system function + cost — OPEN.** Audit every SS
  part in `parts.py` (rails, U-channel, corner plates, U-joints, flat-bar cross-slides, shaft supports,
  stub rod, tray, fasteners, shim, etc.) for its grade (304 vs 316), decide the grade each part actually
  needs (corrosion exposure — cyanotype/wet-process wash vs dry structure — vs cost), and reconcile so the
  choice is consistent and justified system-wide. 316 carries a marine/chemical-immunity premium; use it
  only where the wet chemistry warrants it, 304 elsewhere. Update `parts.py` grades + costs and the reports
  in the same pass.
- [x] **Cost-analysis Bucket B — DONE (2026-07-05).** Solar lever computed (drop 1× `solar-panel-200w`);
  two **phantom levers** removed (film banked into the manual standard; battery already 1×100Ah). The
  two remaining alternatives were **decided by Alvin, not modeled**: **keep 304 SS tray** (poly needs a
  support frame over the 4.5m span — declined) and **keep molded GRP grating** (declined the ~$800
  galvanized revert — worth the 62 kg + corrosion immunity). Both marked *Decided 2026-07-05* in §4/§5.
  Available build-savings now = lever 1 (container) + 5 (solar) = ~$1,500 (6%); the rest are
  banked/decided/moot. All cost gates green.
- [x] **Un-registered values audit — DONE.** The scoped candidates were mostly already registered in
  the 2026-07 full audit (59mm door / 52mm headroom / 97·85 W cooler / 630·1260 L now have constants + facts).
  The real remaining gap = system CONSTANTS restated in prose but policed by NO fact. Registered 2026-07-06:
  `corridor_width_mm` (CORRIDOR_W, 8 docs), `container_rib_spacing_mm` (457, 3), `ibc_stack_height_mm` (2336, 3),
  `walkway_near_wide_w_mm` (500, 3) — all `constant:` refs w/ tight aliases, lint green. **Remaining candidates
  Added `clamp_spacing_mm` (CLAMP_SPACING, 3 docs, clamp-only alias so it skips the identical nozzle 150mm).
  Assessed + deliberately LEFT the rest per the single-source rule: DUCT_HEIGHT/DEPTH (polysemous — Ø200 cooler
  duct vs 200×300 fan duct vs 300 baffle), DRUM_D/R (only 1 clean restatement, already in-cell), EVAP_DUCT_X
  (a diagram-of-record POSITION — stays in the diagram). **5 facts total registered; the drift-prone restated
  system values are now policed.** Method for any future find: `grep facts.yml constant:<NAME>` → tight alias → verify.

## Docs / gallery
- [x] **Gallery-only diagrams — DONE (won't-do).** Gallery-only PNGs are fine without a dedicated owning report — they live in the `all-diagrams.md` visual index. That gallery is now **excluded from the brochure PDF** (`BROCHURE_EXCLUDE`) so the 100+ images don't bloat it.
- [x] **`tilt-swing-board-analysis.md` §4 — DONE 2026-07-07 (point-to-gallery).** Chose point-to-gallery over
  merge: distortion-renders §3 (the dedicated renders gallery) owns the 9 C0–C8 images; §4 renamed "Combined
  Distortion Analysis", keeps its UNIQUE value (projection model + per-config optical analysis prose) but no
  longer re-embeds the 9 renders + summary grid — it opens with a pointer to the gallery §3. Intra-doc anchor
  updated, inline line-71 TODO removed, all gates green. (Checkbox left for Alvin.)
- [x] **`component-dependency-map.md` — DONE.** Portacool note was already resolved (§1.8 = Hessaire
  MC18M). "See Also" done: extended the full **Reports:** + **Diagrams:** cross-ref pair (previously only
  on §1.8) to all 17 §1 registry entries — reports researched with verified section refs, diagrams from
  the §3 matrix. Injector blocks unchanged + green.
- [x] **`plumbing-report.md` §3.2 — LIGHT RE-REVIEW DONE 2026-07-06.** Section is clean post master-switch→EP
  cascade: master switch correctly described as on the EP (not the corridor), canonical IDs, no archaeology,
  American spelling, pump body dims left in prose (procurement spec per skill §A). One improvement: wrapped the
  3 raw "270mm corridor" restatements as `corridor_width_mm` placeholders (placeholder-first). Gates green.
  (Editorial "done" mark + this checkbox left for Alvin per skill §H.4.)

## Code hygiene
- [x] **Unused imports — DONE.** Removed **181** unused imports across 31 files (verified every generator + model runs clean, gates green, no output change). New stdlib checker `src/generators/check_unused_imports.py` (re-export-aware, `--fix`) is a **release gate** in `release.sh` so it can't drift back.
- [x] **`generate_pinhole_water_panel.py:511` refactor — DONE.** Water-panel context is now built muted **at source** via a `muted()` context manager (`ruby_box/cylinder/tri` resolve mute/alpha against it); the fragile post-build `mute_groups` re-coloring pass + its allow-list are retired. Verified visually-identical (same round(c*(1-f)+n*f) formula; 261 muted + 17 full steel, same split) and byte-transparent for other models.

## Paused directions
- [x] **`ibc-reconfig-v2` — DONE.** The IBC-layout redesign was resolved — the deep 4-leg direct-stack restraint box is the current design (reflected in `tbs_constants`, ibc-stacking-report, and the models).
