<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
<!-- Working/internal tracker — NOT published (not registered in publish.sh). -->
# TODO & Actions — TBS-001

The **single record** of outstanding actions across the project. Review and tick here; add new
items as they arise. Tick `[x]` when done (leave a one-line note), or delete once it's clearly
historical. Detailed sub-trackers are linked where the detail is extensive.

**Completed sub-trackers (for reference):** [editorial review](editorial-review-todo.md) — DONE 49/49.

---

## 🛠 Tooling / infra

- [ ] **Solid-joint seam audit + butt-vs-weld convention (3D readability).** Overlapping same-color solid
  members render with NO seam line, so distinct parts read as one fused piece (found 2026-08-14 at the IBC
  retaining-bar → corridor-upright joint — the bar ran *through* the post). This is a general 3D issue, but
  it can't be a blanket "no overlaps" rule: interpenetration is intentional for **welded** joints (a weld
  fuses → continuous is correct) and for fasteners sunk in plates. The distinction is **semantic (weld vs
  bolt), not geometric**. **Plan:** (1) extend `check_interference.py` with a `--solids` pass that lists
  SAME-material solid↔solid overlaps above a volume threshold (excluding fasteners) as a review WARNING —
  reuses the existing AABB machinery; triage each as weld (leave) vs bolted/cleated (butt it). (2) Codify the
  convention in the model skill: **bolted/cleated joints BUTT** (member ends at the mating face → visible
  seam), **welded joints MAY overlap** (reads continuous). Not an auto-fix ("Intersect Faces" everywhere
  over-draws + mangles the generated geometry). (Alvin 2026-08-14.)

- [ ] **Pipe-through-surface seam audit (3D readability) — same class as the beam fix above.** Where a pipe
  passes *through* a surface (e.g. a plywood panel, a wall, a plate), the penetration shows NO seam/butt line
  — the pipe reads as fused into the panel instead of passing through a drilled hole. We fixed the analogous
  case for solid *beams* (butt at the mating face); pipes need the same treatment at panel/wall penetrations.
  **Plan:** extend the solid-seam `--solids` pass (or a sibling `--pipes`) in `check_interference.py` to flag
  pipe↔surface intersections (cylinder passing through a plate/panel solid) as a review WARNING, then per
  penetration either (a) draw a short collar/grommet ring at the surface (the visible hole + seam), or (b)
  split the pipe at the surface so each side butts the face. Reuse the pipe registry already parsed for the
  clash audit. (Alvin 2026-08-15.)

- [ ] **Explore the Sketchfab Data API (Python) to automate model re-upload.** [Sketchfab Data API v3 — Python](https://sketchfab.com/developers/data-api/v3/python).
  Today the single-writer protocol ends with ALVIN manually re-uploading each `.skp` to Sketchfab (same model UID). Investigate driving that upload programmatically (PATCH/upload to the existing model UID via the Data API + a token), so a re-send could optionally push to Sketchfab without the manual step. Respect the single-writer rule (ALVIN still saves the `.skp`); the API would replace only the *upload* leg. Prereqs: API token handling, per-model UID already lives in `dependencies.yml` (`push_sketchfab.py` reads it), verify the API supports replacing a model's source file in place.

- [x] **Reconcile the `project-cost-breakdown.md` §5 water-system breakdown table to `costing.py` — DONE 2026-08-05.** Root cause: `costing._render_detail` is a POSITIONAL value fill (keeps the doc's hand-edited labels, rewrites value cells from `WATER[di]` by row index). Inserting the pinhole-wall ply as `WATER` item #5 shifted every value from #5 on up by one row while the doc kept 13 labels — so labels/values misaligned and the last item ($257 consumables) fell off the bottom (TOTAL≠sum by $257). Fix = insert the missing **ply label row** at position 5, then `--inject` refilled all 14 values correctly (Filter skid $541, Valves $922, Pipe $84, tray $1,473/$2,121, spray $584/$596, consumables $257). Rows now sum to $6,579/$7,730 = the TOTAL; "table arithmetic" lint [OK].

- [x] **SketchUp generator memory balloons over repeated `--send` — INVESTIGATED 2026-08-10, NOT a code bug ([sketchup-memory-investigation.md](sketchup-memory-investigation.md)).** The "Ruby allocations not being freed" hypothesis is **falsified end-to-end**: the plugin evals each script in an isolated `TOPLEVEL_BINDING.dup` (locals don't persist across sends — verified `cross_call_local: "isolated"`), our generated `.rb` creates **zero** globals/constants/closures, Ruby `heap_live` stays flat (~80k–250k slots) across 12 re-sends, and `purge_unused` leaves 0 orphan defs. The bloat is **SketchUp's C++ allocator high-water-marking** — it retains freed pages (session peak 4.2 GB; an *empty* model after File>New still holds 2.5 GB) and `GC`/`purge_unused`/document-close do **not** reclaim it. DC observers exonerated (Test D: `dc_defs`/timers/observers all flat). **Only quitting/restarting SketchUp reclaims it.** No code fix; the mitigation is workflow — **restart SketchUp during heavy send sessions** (gauge: `footprint -p <pid>`), and prefer a small/targeted model when iterating. (Alvin 2026-08-05, resolved 2026-08-10.)

## ⚡ Parts firm-up tracker (active) — 3 buckets by when they're actionable

_Everything sourceable today is sourced (parts-identity SKU/URL lint at zero). What remains,
bucketed by WHEN it can be acted on:_

**Open DESIGN items:**
- [x] **Re-source ALL structural beams to imperial off-the-shelf sizes (#26).** DONE 2026-08-07 for the walkway/floor-leg/IBC/brace/tray set: RWK long beams + 2 center arms + floor-leg arms → 2×1×0.120 steel (2×⅞ non-stock; MetalsDepot $6.35/ft); IBC frame + film-plane brace + floor-leg posts + swing/hinged-panel frames → 2×2×0.120 (50→50.8); tray bearer → 2×2×0.125 6061 Al. Option B keeps the deck (spray clearance 15→11.6mm); 2×1 deeper ⇒ arms SF≈2.5. Constants + 2D + parts/cost (+$107/+$123 walkway) + reports + 6 model .rb done; **.skp re-send DONE 2026-08-08 in the #29 cascade** (overview/ibc-stack/construction re-sent + uploaded; walkway/film-plane/lighttrap re-sent in the earlier #26 handoff). **2026-08-07 (round 2):** drum cage → **1.5×1.5×0.120** (fab-lot label) + cargo-door light-trap frame → **2×2×0.120** (`door_frame()` s=50→50.8; overview reuses it) DONE. Also completed the stale-literal sweep the first #26 commit missed — IBC-frame/panel-frame/RWK labels across component-dependency-map, hinged-panel-report, weight-distribution-report, container/equipment-layout reports, costing LineItems, `generate_ibc_frame_drawing.py` (FRAME_RHS 50→50.8 + labels), `generate_ibc_stacking_diagram.py`, `generate_hingepanel_diagram.py`, and the weight calcs (`generate_movable_panel_weight.py` + `generate_weight_analysis.py`: RHS 4.43→4.57 kg/m; weight blocks re-injected). **Angle-rail residual RESOLVED 2026-08-07:** `WALKWAY_ANGLE_IRON` (50×50×5) was a **phantom** — no such constant, a stale §1 row + "angle iron welded to end wall" prose from the retired right-walkway design. The LIVE member is the right-walkway **L-angle grate bearer**, re-specced 25×25×5 → **1×1×3/16in stock** (prose-only, not costed); fixed the §1 row, equipment-layout, and the walkway-diagram docstring to the cantilever-rectangle design. **#26 fully complete.** _Original:_ The models spec many members in **metric nominal** The models spec many members in **metric nominal** (spray beam was 40×25; right walkway cantilever arm 40×40 + long-beam 40×35; left floor-leg 50×50; tray bearer 50×50 Al; etc.) — but square/rectangular tube is **only sold in imperial** (2", 1¾", 1½" square + rectangular like 2×¾, 2×1). None of the 40mm / 50mm nominals are stock. Sweep every `*_RHS` / `*_SHS` / beam-section constant and re-spec to a **confirmed available** imperial size (record supplier + SKU), then cascade section changes to the 2D/3D + parts + cost. The spray beam is already done (→ 1½×1½×0.062 Metals Depot $183) and the right long-beam is heading to 2×¾ (Metal Supermarkets) in the walkway-shave commit — this item covers the **rest** (arms, floor-legs, tray bearer, any remaining 40/50mm sections).
- [x] **Walkway-support mid-span stiffness (#27).** RESOLVED 2026-08-07 — the mid-span support was already modeled + costed (2 center cantilever arms off the IBC corridor uprights, half-lapped where the long beams cross); this pass cleaned up the stale "a mid-span support *is planned*" language across walkway-report §4.1/§4.2 + the constants/model comments to present tense, and re-ran the deflection/strength check against the real 2×1×0.120 section (SF≈2.5 single-arm, deflection well under 1mm with the arms). Left floor-leg ~3mm bounce still accepted. _Original:_ **Walkway-support mid-span stiffness (2×⅞ shave).** The right-walkway frame long-beam + the left floor-leg arms were shaved 40×40 → **2×⅞in** (soffit Z80/75 → Z93) to clear the full-width 1½ spray beam by ≥15mm. The shallower section is less stiff: the right bearer goes ~1.5mm → ~5.5mm midspan over its ~1m bay, and the left floor-leg cantilever ~0.9mm → ~3mm at the tip. Add **mid-span support(s)** (a 3rd cantilever arm/post) to the right frame to bring it back under ~1mm — the anchor point (a post at Yd≈1,770 in the right-walkway floor, or a 3rd corridor upright) needs a fab detail. Left floor-leg ~3mm bounce accepted (Alvin, 2026-08-03) but revisit if it reads as too springy. Cascade the added support to the RWK model + walkway 2D/3D + parts.
- [x] **Spray-beam lift-out gap — CLOSED 2026-08-07 as NO-LIFT / park-and-roll (accepted, Alvin).** Decision: **no lift-out mechanism.** (a) Loading the muslin — **park-and-roll** (report §4.2): roll the gantry to the near end, feed the muslin through the far drop-slot, lay it flat, roll the beam back over it. **Verified from the constants:** beam-to-floor gap = `SPRAY_BAR_BEAM_BOT_RISE` = 16 (Ø32 wheel radius) − 7 (bracket drop) = **9mm**, constant across the traverse (`spray_beam_bot_z = tray_floor_z + 9`); over the 0.5mm muslin = **~8.5mm clearance**; wheels run outboard of the muslin (centers X≈200/4,599 vs muslin edges X≈220/4,579) on bare floor. (b) Maintenance/cleaning — **extract the beam through the right-walkway grate** (§4.3). No `SPRAY_BAR_*` / 2D / 3D change needed.
- [x] **Flexible connectors on BOTH sides of every pump (#29).** DONE — braided ½" flex jumper on suction + discharge of all 5 pumps (P-04 suction = the 1" tray hose → 9 new ½" jumpers). P&ID schematic (flex coil both ports of P-01…P-05), parts.py (braided-hose 2→3 lengths + Rain Bird BC50-20 barb couplings ×18 + Everbilt 671255E SS clamps ×18), costing +$55 water, plumbing-report §5.2. **2026-08-08:** 2D flex coils on the corridor + P-04-skid panel-layout elevations + 3D yellow jumpers at every pump port (water/overview/ibc-stack/construction re-sent + uploaded). Pressure OK — reinforced braided PVC suits the 45 PSI discharge. _Original:_ The pumps (P-01…P-05) vibrate in service; rigidly-coupled solvent-weld PVC joints will **fatigue-crack**. Confirm the jumper's pressure/temperature rating suits the pump discharge side.
- [x] **Pipe support review after the flex-connector insertions (#29 follow-up).** RESOLVED 2026-08-08 (#29). The corridor pump risers, the drain-riser spine runs, and the filter-skid runs now land on **3 flush 18mm ply support boards + 12 welded steel L-brackets + 39 cushioned 3/4" P-clips** (plumbing-report §5.3; +$33/$46/$61 water; interference re-audit 0 crossings). The **8 IBC-tote jumpers need no added support** — each spans a now-clamped run end (held on the boards/spine) and a rigid tote port whose entry **flange bolts to the tote cage** (a support in its own right), so both ends of every tote jumper are anchored. _Original:_ Adding a braided flex jumper de-couples each pump from the rigid run — but a rigid pipe that was *held up by* its solvent-welded pump/fitting connection may now be **unsupported** across that joint (the flex can't carry a bending/gravity load). **Action:** walk every run that got a flex jumper (both ports of P-01/P-02/P-03/P-05 + P-04 discharge, and the 8 IBC-tote jumpers) and check whether the newly-free pipe end needs an **added clamp/saddle/bracket**. (Alvin 2026-08-07.)
- [x] **Pump-run support-detail fabrication sheet (#29 follow-up) — DONE 2026-08-10.** New generator `generate_support_detail.py` → 2 sheets: **Sheet 1 board elevations** (far / near / near-upper, face-on — 18mm ply, 4 L-brackets each, risers + P-clip rows, fully dimensioned) + **Sheet 2 mounting details** (L-bracket flush-mount plan section: post inner face → 6mm weld leg → 45mm landing leg → 18mm ply seated flush, fastened with an M6 countersunk flat-head machine screw into a captive pronged tee-nut — the weight-bearing joint; P-clip cross-section mounted at right angles to the board with a #10 wood screw — pipe restraint only, no tee-nut; fabrication schedule 3 boards / 12 brackets / 39 clips; notes). Geometry imported from `generate_corridor_water_panel` (SB_* constants) so it can't drift. Registered: `all-diagrams.md` §14, `publish.sh`, `setup_docs.py`, `dependencies.yml`; embedded in plumbing-report §5.3. (Alvin 2026-08-09.)
- [x] **Captive T-nuts for all plywood-mounted components.** DONE 2026-08-07 (#30) — every removable ply-mount joint (3× filter housings, P-04/SV-02/DV-02 skid row, ACC-01/02, 5× pump shirt, valve brackets, EP, shelf, Fan-B band) converted lag/wood-screw → machine-screw into a back-face 4-prong tee-nut. Firm zinc tee-nuts: ¼-20 Everbilt 825001 $1.57/4pk (×10) + 5/16-18 Everbilt 825091 $1.57/4pk (×2). Machine screws downgraded SS→zinc (dry mounts), all firm: ¼-20×1" Everbilt 826771 $1.57/4pk ×10 + 5/16-18×2½" Everbilt 831121 $1.57 ea ×8. parts.py + costing (+$32 water) + plumbing-report §3.1/§7.2 + BOM cascaded, gates green. _Original scope:_ Every component that machine-screws to plywood — filters (Pentair 150061 brackets), the P-04/SV-02/DV-02 skid row, ACC-01/ACC-02, the corridor pumps' mount shirt, valve brackets, the EP panel, the shelf, the Fan-B band — should land on a **captive T-nut** (pronged/blind or threaded insert) set into the ply, not a wood/lag screw, wherever a removable/re-torqueable machine-screw joint is wanted (serviceability, no thread-strip in ply). **Action:** enumerate every ply-mount interface, pick the **thread size + pitch per component** (match each component's own fastener — e.g. M6/M8 for the filter brackets, ¼-20 for pump-rail/shelf, etc.), confirm 18mm ply vs T-nut barrel length + front-vs-back install, then **add + price** the T-nuts (qty per interface) in `parts.py` → cascade BOM / master-shopping-list / cost. (Alvin 2026-08-05.)
- [x] **Right walkway muslin-notch — beam clash — RESOLVED 2026-07-23.** The inner cantilever-rectangle long beam under the notch (X4329) is **cranked outboard 100mm** (full notch depth) over Yd1812–2162 with angled ramps, vacating the notch footprint so the rigid muslin rod drops straight at the tray edge — beam stays ONE continuous uncut member. `_rwk_inner_beam_cranked` (overview/walkway/water), Sheet 3 + report §4.1 updated. Left notch was already clear (between floor-leg brackets).

### Bucket 1 — ACTIONABLE NOW
- [x] **Cyanotype chemistry consolidated to Artcraft (bulk) — DONE 2026-07-26.** Bulk-price research (2 agents) + Alvin's confirmed Artcraft packs → all three reagents re-sourced to **Artcraft Chemicals**: ferric ammonium oxalate **$218.16→$64.20/kg** ($29.12/1 lb; the big mover), potassium ferricyanide **$60.80→$51.01/kg** ($104.12/4.5 lb), ammonium dichromate → Artcraft $33.66/0.5 lb (trace, $25/run allowance holds). Cascaded: costing tiers (Standard total **$4,400→$1,710**, per-print **$88→$34**), grand total **→$27,262–$39,454**, parts registry, all injected docs + prose restatements. **process-comparison.md re-inverted: cyanotype ($1,250 lean) is cheapest again**, below gum ($1,592) — "why cyanotype" reframed to cost + archival/hazard/simplicity. Remaining bulk option: request an Artcraft ~38-lb AmFe quote (could drop below $64/kg). Use FULL reagent names not "AmFe" per [[feedback_full_chemical_names]].
- [x] **Fastener thread-pitch cross-check — DONE 2026-07-29.** Every bolt↔nut pair verified against the eng-specs datasheets (via pypdf): M12×1.75 (90591A181 nut ↔ 91280A728/732 + 1634027 bolts), M8×1.25 (90591A161 ↔ 91280A534), M6×1.0 (96194A101/90591A151/90576A115 ↔ 93635A210/91280A330), M5×0.8 (91420A326). All coarse + matching — the M8×1.0-fine vs 1.25-coarse trap is clean. "confirm vs SKU PDF" caveats closed in the registry; the 2 missing PDFs (90591A181, 90576A115) downloaded, 1634027 pitch confirmed from the FMW listing.
- [x] **Plumbing joint-convention cascade — DONE 2026-07-29.** All sub-items complete: PVC slip run, transition-
  adapter P&ID takeoff (½"22/1"26), all SKUs firmed, PVC stick recount (1"→4), and the IBC-tote FLEXIBLE-JUMPER
  connection (2D schematic coils + 3D corrugated jumpers across all 5 models) + the spray nozzle-pitch overshoot fix.
  Residual: only the 2 bench flags in Bucket 3 (s60-reducer interface, clamp size). Original notes ↓ (historical).
  Rule established (plumbing-report §5.1): the run is **solvent-weld
  PVC (slip)**; **threaded NPT only where it lands on a hard component** (pumps, filters, valves, check
  valve, tank bulkheads, sample taps, accumulator) via a **slip×NPT transition adapter**. Settled: the 4
  ½" run fittings are PVC Sch-40 slip (Home Depot Charlotte); the bushing at the filter is threaded.
  - [x] **(a) Pipe material HDPE → PVC — DONE 2026-07-27** (justification in plumbing-report §5.2). Run
    is **PVC Sch-40 solvent-weld**; renamed `hdpe-half`→`pvc-half`, `hdpe-1in`→`pvc-1in`,
    `hdpe-three-quarter`→`pvc-three-quarter`; `filter-jumper` + §5 table + the "1" HDPE stock" spec refs
    (s60-adapter, blue-equalization-tie, valve-3way-half) all re-labeled PVC. Prices kept as estimates
    → **re-price/re-count PVC when sourced** (PVC = 10-ft sticks vs the assumed 20-ft; Home Depot).
  - [x] **(b) 1" run tees/elbows → PVC slip — DONE 2026-07-27.** `tee-100` (qty 3+1 consolidated with
    `tee-100-hdpe` → qty 4) and `elbow-el100` re-spec'd from threaded Banjo FRPP ($14.19 tee / $4.59
    elbow) to **1" PVC Sch-40 slip** at Home Depot (est ~$1.50 tee / ~$1 elbow). Saved ~$65. **Source
    exact Home Depot SKU/price** (still an estimate range).
  - [x] **(c) Transition adapters — ADDED + SKUs SOURCED 2026-07-27; COUNT FIRMED via P&ID takeoff 2026-07-28.**
    `pvc-adapter-half`/`pvc-adapter-1in`: PVC slip×NPT male adapters where the glued run meets each threaded
    component. Unit prices firm (½" PVC021090600HD $0.79, 1" PVC021091000HD $1.16). **Trace done:** ½" **22**
    (6 BV + 5 pump discharges + 3 DV-02 + 2 SV taps + 1 ACC + 4 union sides + 1 bushing) + 1" **26** (6 V100 +
    8 s60-adapter IBC landings + 3 DV-01 + 2 CV-1 + 5 filter ports + 2 equalization bulkheads) = 48 (+$8;
    costing §5 + grand_total cascaded). Alvin's calls: unions = 4 (both sides), s60 = all 8 land on run.
  - [x] **X1 topology — DONE 2026-07-27.** Water schematic (sheet 1) rerouted so the DV-01 blue recycle JOINS
    the X1 fill header (4-way cross), not a separate IBC-2 side-entry; water-report prose + §5 pipe table
    tee→cross; `tee-100` dropped its redundant X1-fill-split tee (qty 4→3). All 5 artifacts (parts, schematic,
    panel-layout, 3D model, reports) now agree on the X1 4-way cross (`cross-100`, Amazon B0CGGV74MB $5.99).
  - [x] **`union-half` — RESOLVED 2026-07-27 (Option C hybrid).** Split into `coupling-half` (4× permanent
    Charlotte slip couplings $0.74) + `union-half` (2× true ½" PVC service unions ~$3–4 at the pump manifold
    + filter-bank inlet). Per-component service is already covered by the threaded ports, so only 2 mid-run
    breaks needed. Residual: source the ½" PVC union SKU/price.
  - [x] **PVC run priced/firmed 2026-07-27.** `pvc-half` ($4.81×8), `pvc-1in` (Charlotte PVC040100600RS
    $8.65×2 — ⚠ listing is DWV not pressure; OK at 45 PSI, flagged), `pvc-three-quarter` (PVC-04007-0600
    $5.76×2), slip `tee-100`/`elbow-el100` all firm at Home Depot. `filter-jumper` bundle **retired** into
    itemized pipe + elbows + adapters (was double-counting). Residual: re-count stick qtys vs final routing.
- [x] **spray-nozzle pattern — RESOLVED 2026-07-28 (Option b, 90° down-jets).** Alvin chose 90° down-jets (DIG
  110B) over flat-fan/180° — directs the wash onto the print, not sideways/up. Pitch tightened `SPRAY_BAR_NOZZLE_PITCH`
  150→100mm (26→39 jets) for edge-to-edge coverage of the 90° footprint. Cascaded: constant, 2D spray-bar diagram,
  report §3.2/§3.9, part (4× 10-packs). All 3 .skp (spraybar, overview, construction) re-sent + saved + uploaded — DONE 2026-07-28.
- [x] **External power panel — GEOMETRY cascade — DONE 2026-07-28 (report §5.4 prose + parts + component sourcing + 2D + 3D).**
  Design FINAL (Alvin): a **fabricated flanged wall-penetration box** (`power-panel-box`) — the 4 weatherproof interfaces
  (3× MC4 bulkheads Powerwerx, shore inlet, cooler outlet W5320-T0W + 5981-UCL, 22mm E-stop) surface-mount + seal to its
  front face and are exposed; box opens to the interior for wiring; flange sealed to the ribbed wall with **flashing +
  silicone** (`power-panel-flashing`), light- + water-tight. Blue Sea 6006 disconnect relocated to the **EP backboard**.
  (Superseded ideas: original flush plate; a McMaster IP enclosure — both retired.) GEOMETRY REDRAW (2026-07-28):
  DONE — **electrical-sheet6** VIEW A drawn with component-accurate glyphs (`component_glyphs.py`: MC4 bulkhead, NEMA
  weatherproof inlet, W5320 WR duplex under 5981-UCL cover, 22mm E-stop) + VIEW B section shows the penetration box with
  cover caps in profile; **3D `external_panel()`** (shared by electrical/overview/construction) rebuilt flush plate → flange
  front face + open shroud, WR duplex + covers, new consts `PWR_PANEL_BOX_D`/`PWR_PANEL_SHROUD_T`; **electrical.skp sent +
  verified**; assembly-fab / floorplan / pinhole-wall-elevation flush-mount wording → penetration box.
  DONE 2026-07-28 — all 3 `.skp` (electrical / overview / construction) sent, verified (flange Y−65..−62, shroud open to
  Y+28, WR outlet raised 25mm Z1903..1963), saved + uploaded by Alvin, committed. View B also shows all 3 PV pairs →
  busbar → MPPT and legible gold/orange AC wiring. Cascade COMPLETE.
- [x] **panel-corner-plates → corner stiffener grid — DONE 2026-07-29 (Alvin: "frame it").** The solid 3mm 5052 Al corner cores ($586, ~2 half-wasted sheets, ~25 kg) were REDUNDANT: light-tightness is the two black HDPE skins, latch/fan load is the RHS frame + ply band, so the plate only stiffened. Replaced with a light **1"×1"×1/8" 6061 Al angle rib grid** (`panel-corner-stiffener`, 1 vertical + 2 horizontal ribs/corner, ~325×750mm bays) that holds the skins flat — the leaf is vertical so skin self-weight is in-plane, only out-of-plane oil-can needs resisting (works with the U-channel skin retainers, §2.5). **Saves ~$530 (line $586→~$44) + ~22 kg.** Cascaded: constants, parts (retired plate), costing §6c + grand (**→$25,921/$30,511/$37,151**), both weight models + §2.4 table + §2.1/§2.5 prose, 2D Sheet-2 cross-section (rib not solid band). NO .skp re-send (3D draws the 40mm envelope, not the core). SKU firmed 2026-07-29: **Grainger 2EYP1** 1×1×1/8 Al angle $12.20/8ft × 4 = $48.80 (the 12ft 897KL0 at $88.80 was ~5× the per-ft price, rejected). Grand total **→$25,938/$30,516/$37,144**.
- [~] **Aug 2026 full re-price — SWEEP COMPLETE across all 6 systems (2026-08-01).** electrical / water / spray = 100% firm-priced; film / ibc-frame / shelf = material drivers firm, fab + bulk-steel deferred (rule below). Grand total settled **$25,874 / $30,346 / $36,874**. Notable moves: spray beam → single 16 ft 0.062in SS tube (no butt weld, sag-checked, −$394); corner L-plates $58.90 ea; U-joint boots, GHS labels, citric acid, pH buffers, zip ties, powerpole, blade fuses, ph-cal all firmed; wall-seat-saddle split into 8mm/10mm plate lines; bolt-m12x40 → 18-8 SS 92314A744. **Rule established** ([[feedback_material_now_fab_later]]): quote RAW MATERIAL now (the driver); defer fab (cut/bend/weld) to post-blueprint; bulk structural steel = steel-yard/freight quote, NOT online cut-to-size (which caps at 96in + overprices ~3×). **Deferred (owner-side, not blocked on me):**
  - **Fab quotes (post-blueprint):** film cross-slide assembly (¼in bar firm $134.73, + UHMW/gib/fab), the 2 wall-seat-saddle plate cuts + weld.
  - **Steel-yard bulk quotes:** `ibcf-rhs`/`ibcf-feet`/`ibcf-wall-backing` (2×2×⅛ A500 + A36 plate), `shelf-steel-shs` (1×1×⅛ A500 6 m). Estimates are realistic bulk figures.
  - **At-purchase confirms:** `shelf-folding-stays` + `shelf-transport-latch` (zinc chosen, estimates hold).
- [ ] **Master-BOM SKU backfill.** Branded rows that don't yet carry a registry `part_no` — Alvin's supplier paste-check; each SKU auto-appears in the master on the next `--inject`.
- [x] **BV-05 spray selector — RESOLVED 2026-08-07 as a 2-valve split** (not a 3-way L-port). No 1/2" 3-way L-port is stocked (only 3/4" Banjo V075BL $72.88 + reducers), so BV-05 = **BV-05a** (1/2" 3-way Blue/Brown selector, reuse US Plastic #22365 $23.99) + **BV-05b** (1/2" 2-way on/off at the spray-bar feed, Grainger 803HZ1 $24.14). All 1/2", no reducers, no L-port OFF-detent risk, ~$37 cheaper. Parts/costing/report done (+$24). **Remaining: split `3W-BV-05` in the 3D model into the selector + on/off (re-send water/overview/construction/ibc-stack).**

### Cost-reduction opportunities (grounding — analysis 2026-07-31)
Ranked by saving potential, analogous to the SS→ALU depth-rail switch (`fp-u-channel` $2,173→$328). Each
needs a dedicated follow-up to model + cascade before committing. Cost by system for context: chemistry
$5,466 · film $4,216–4,572 · container $2,300–4,300 · electrical $3,431–3,496 · water $3,370 · walkway
$1,979–2,825 · lightlock $2,046–2,516 · tray $1,583–2,271.
- [x] **Tray: 304 SS retained — DECIDED 2026-08-02 (the "SS→PP ~$1,000–1,400" was a myth).** Full evaluation in
  [tray-research.md](tray-research.md) (published, Research section): PP sheet ($258/sheet) isn't cheaper than SS
  and needs a sub-floor — PP saves only ~$550–920 and only if self-welded; the one big saving (a liner on a
  sub-structure, ~$1,150–1,850) fails the **rigid-surface** requirement (Alvin: needed to handle the large print).
  So SS stays, decided on fab/procurement/skill + leak-risk. **Adopted the retained-material lever: `tray-ss-sheet`
  #4 brushed → 2B mill finish (−$110/−$150 est, drain pan needs no brush; keep 16-ga + 304).** Grand → $25,764/30,216/36,724.
- [x] **Ruland U-joints → Belden UJ-SS750x375 — ADOPTED 2026-07-31 (~$653 saving).** `fp-ujoint` re-spec'd to Belden UJ-SS750x375 @ $112.68 (×4, backup Grainger 806V18) + `fp-ujoint-boot` → Belden 806VF1 nitrile boot $40.25; keyway/twist-lock → setscrew; cascaded across parts/costing/2D Sheet 3/3D model. Original research note ↓.
- [ ] ~~Ruland U-joints → Belden UJ-SS750x375 — ~$652 saving (RESEARCHED 2026-07-31, ready to adopt).~~
  `fp-ujoint` = $1,104 (4× Ruland USKC12-6-6-SS @ $276, 3/8" bore, 303 SS, 45°/axis). **Direct drop-in
  alternative found: Belden UJ-SS750x375** ([MROSupply $112.68](https://www.mrosupply.com/shaft-couplings-and-collars/2561134_uj-ss750x375_belden/)) —
  **3/8" (0.375") bore, 0.75" OD, 45° max angle, 303/416 stainless, pin-and-block friction bearing** (same
  bearing type + same materials as the Ruland it replaces; 175 in-lbf rated / 875 ult — the corner is a
  *static positioning* joint, near-zero torque). Matches every hard requirement: 3/8" bore ✓, 45° (covers
  the ±40° tilt) ✓, stainless for the chloride-free cyanotype wash ✓. Backlash is a non-issue — at **f/1088
  the depth of field makes mm-scale film-plane position error optically irrelevant** (why we relaxed the
  zero-backlash worry). **4 × $112.68 = $450.72 vs $1,104 → saves ~$653.** Watch: setscrew bore (vs Ruland
  keyway+clamp — fine at low torque, or spec the `-K` keyway variant); keep a boot for the wet zone (Belden
  offers washdown boots, or reuse the `fp-ujoint-boot` concept). Adopt → re-spec `fp-ujoint`, cascade
  (film §5a... film system, grand), update Sheet 3 / film-plane-mechanism model U-joint callout.
- [ ] **Ferric ammonium oxalate (AmFe) — $4,026, biggest single cost (sourcing lever, not a switch).**
  `amfe-rich/standard/lean` = $2,196+$1,098+$732 @ $64.20/kg. Core chemistry — the lever is bulk/cheaper
  supplier or trimming the *rich* coat tier, not a material swap. Even 15% ≈ $600. Follow-up: chemistry
  sourcing pass (also `ferri-rich` potassium ferricyanide $582).

### Bucket 2 — ACTIONABLE WHEN BLUEPRINTS FINALIZED (v1.0)
- [ ] **`pinhole-shim`** — Lenox SS-3/8-DISC laser-drilled pinhole; firm via RFQ once the optics drawing set is design-complete.

### Bucket 3 — ACTIONABLE ON BUILD
- [ ] **Container corrugation depth — PARKED pending physical measurement (EARLY procurement gate, post-blueprints).** The design side is CLOSED and robust to the unknown: `CONTAINER_CORRUGATION_DEPTH=30` (conservative max of the 25–30mm ISO side-wall range), the IBC wall-hangers use **M12×65 partial-thread** sized for the 42–54mm worst-case grip, and the BOM already carries **2 shim washers per bolt** (`91166A290`) to pad the grip if the real wall measures shallower. **Gate action (do FIRST, before ordering any wall fastener / bracket plate):** once the actual container is on site, **measure the real side-wall corrugation peak-to-valley**; if <30mm, confirm the shim count and whether M12×65 can drop to a shorter partial-thread length; apply **A36** to the final bracket-plate specs. No desk work possible — needs the physical container.
- [ ] **Walkway grating.** American Grating is primary (~$830 public list, banded $830–$1,050 for freight/cut); get the **firm cut quote + SoCal freight** at build. **McNichols is a FIRM SHIPPED fallback: 2× 48″×144″ @ $796.77 = $1,593.54 + $456 freight = $2,049.98 shipped (firm 2026-07-24)** — ~2× the American estimate, and its 4′×12′ sheet would re-nest the cut plan if chosen.
- [ ] **Container** — `container-20ft` (±$1,500) + `container-delivery` (±$500), firm at purchase.
- [ ] **Fab estimates.** All `*-fabrication` lines (`tray-fabrication`, `ll-fabrication`, `ibcf-fabrication`, `sp-door-fab`) + `tray-ss-sheet`, the film-plane fab (skate carriage, 304 cross-slides, cam clamp), and the `sp-pivot-post` collar — quote to shops once the drawing set ships. ≈±$1,500.
- [ ] **Buy the film-plane U-joints (`fp-ujoint`).** Belden **SSNBUJ750x3/8KB** (Grainger **41D816**) — needle-bearing, 3/8" keyway + set screw, stainless, 45°, factory-booted. **$252.13 ea × 4 = $1,008.52**, + 8× 3/32×3/64 SS machine keys (`fp-ujoint-key`, ~$6–10 lot) + keyseat the 3/8" stubs. Firm-priced (2026-08-13); purchase at build. **Confirm the set-screw torque spec with Belden/Grainger** (datasheet gives static breaking 95 in-lb only). Supersedes the retired plain UJ-SS750x375 + separate 806VF1 boot.
- [x] **Film-plane corner — load case DONE + DECIDED (blueprint Phase 1c, 2026-08-13).** `fp_corner_load.py` → **Sheet 10** (`film-plane-sheet10.png`). C2 travel verified (Z 245 / X 257 mm = `XSLIDE_Z/X_TRAVEL`, promoted `reserved→firm`). C1: per-corner load 124 N; **DECISION (Alvin): bars mounted DEEP** → SF ≈ 10 (flat 1.7, not used). Recorded on Sheet 10 + blueprint spec §Phase 1c + `parts.py` fp-cross-slide spec.
- [x] **KEEP (Alvin 2026-08-13): the load-case sheet is promoted to film-plane Sheet 10** (`film-plane-sheet10.png`), no longer scratch. Set renumbered 9→10.
- [ ] **IBC flex-connection `s60-reducer` interface (bench).** The sourced reducer (Charlotte `PVC021071300HD`, 2"×1" Sch-40) is **spigot×slip (solvent-weld)**, but the tote adapter (Granatan S60→2") outputs **2" MALE NPT** — a spigot×slip bushing is glue-only, so it needs a **2" MPT×socket transition** to mate (or swap to a **2"FNPT×1" reducer**). Verify/resolve the tote-adapter interface at the bench. (Alvin 2026-07-29.)
- [ ] **IBC flex-connection clamp size (bench).** `ibc-flex-clamp` is an Apollo **#12** (½"–1¼", `IDL0410PK`). The flex hose is cut from the 1"-ID / **1¼"-OD** tray-suction coil, so over a barb the OD approaches/*exceeds* the #12's 1¼" max — **verify the #12 closes and seals; step up to #16 if it bottoms out.** (Alvin 2026-07-29.)

**304→316 SS audit + cost-cut — DONE 2026-07-29.** Cyanotype wash has no chloride, so 316's pitting resistance was unused across the splash zone. Downgraded: `fp-cross-slide` 316→304; `bulkhead-2in` 304 SS→**PP** (US Plastic 32200 $21.14); `fp-u-channel` depth rails 304→**6061 Al** (Grainger 795M51 8 ft, $328 vs $2,173 — biggest single line); `bolt-m6-tray` KEPT 316 (Alvin). Spray-beam Al downgrade REVERTED (3× sag over 3.86m needed an up-sized section for a ~$25 save). Weight model gap fixed (fixed depth rails were omitted → +18.4 kg). All 2D/3D/reports cascaded; film-plane-mechanism.skp re-sent (rails now aluminum). Grand total **→$26,476/$31,053/$37,682**.

**Recently firmed (this drive):** light-lock plastics → US Plastics HDPE; drum caps 3/16″ (`LT_CAP_T`); electrical 13 parts + 2 E-stops + battery → Renogy Core; walkway grating supplier → American Grating primary; tray shims → HDPE plate; **corridor ply both parts 23/32″ RTD $29.30** (ply-18 + ply-25, standard-not-marine rule); `cooler-inverter`, `ibc-tote-1000l`, `sp-pivot-post` pipe. Design: walkway deck continuity + bump extended a 2nd rib to IBC (5 widened brackets) + muslin notches (5 models); walkway sheets merged (5) + new Sheet 9 near-wall bump-out; water/film-plane Sketchfab name/desc fix.

---

## Deliverable — standalone TBS-002 brochure — DONE 2026-07-26
- [x] **Standalone `tbs-002-brochure.pdf`** — teacher-facing classroom brochure. `generate_brochure.py`
  now takes `--edition {tbs001,tbs002}` (default tbs001, unchanged): the tbs002 edition builds a
  project-forward cover + a "For Teachers — At a Glance" quick-reference page (ages, session time,
  group size, cost, curriculum, safety-at-a-glance) + the two mini-TBS docs. The mini-TBS docs are
  dropped from the TBS-001 PDF (via the tbs001 `exclude` set) but stay on the site. `publish.sh` builds
  both PDFs; both PDFs are gitignored (generated on publish). The **TBS-002 booklet is hosted for download**:
  publish.sh stages it in `published/assets/tbs-002-brochure.pdf` before the build, linked as
  "Printable Instructions" from the Educational Program nav + the TBS-002 page. (The TBS-001
  prospectus PDF remains a local artifact, not hosted.)

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

- [x] **Fully-dimensioned multi-view detail of ONE corner — DONE 2026-08-10 (branch `corner-eng-design`).**
  Sheets 3/4/8/9 dimensioned to blueprint grade: skate roller ODs + Ø10 axle + 40mm pitch (Sheet 3), rail
  wall-flange bolt pattern + M8×25 (Sheet 4), cross-slide bar section/travel/gib/UHMW (Sheet 8), U-joint
  envelope (Ø19.1/68/bore 9.53/±45°) + J5 hole pattern (edge 25.4/pair 38) + L-plate 6×8 bend R6.35 (Sheet 9).
  **Fastener callouts J1–J5 with torque/class/washer/locker** (M8 24 N·m, M6 10 N·m, setscrews ~2.5 N·m; Sheet 8).
  **Datum/tolerance scheme** (datums A/B/C + general + per-feature GD&T; Sheet 9). U-joint = Belden (not Ruland),
  cross-slides = 304 (not 316) — both reconciled.
- [x] **Drive it from `tbs_constants` — DONE 2026-08-10.** Promoted `XSLIDE_*` reserved→firm; added the corner
  constants (bar section, U-joint envelope from the Belden datasheet, skate rollers + pitch, cam-clamp, L-plate
  blank + hole PCDs + bend R). Firmed the load: per-corner static 162 N, cross-slide section SF 4.5 weak / 27
  strong. Bar grown ~250→345/365mm to hold ±40°/±28° (+$135 film, cascaded).
- [x] **Reconcile the TL/TR (guide) corner — DONE 2026-08-10.** Both corners = SAME web-vertical rail + captured
  skate (keeper/capture rollers react tip-force vs gravity). 3D model reworked flat→web-vertical (verified:
  film 160–2252 = 2092mm ≈ FP_H 2094; no FP_H change — the flat model was over-drawing 38mm); Sheet 3 guide note.
  (Sheet 10 was tried as a separate guide sheet then reverted — wrong wheels + redundant with Sheet 3.)

### IBC stacking frame (SECOND subsystem — tracking doc `ibc-frame-blueprint-spec.md`)

- [x] **Phase A — EN 12195-1 transport-restraint validation + redesign — DONE 2026-08-14.** `ibc_frame_load.py`
  (new) computes the load case; the self-contained camera transports **loaded** (965 kg top tote, 0.8 g fwd)
  → the single weak-axis 50×20×3 front bar **fails (SF 0.79)**. Redesign **R5** (Alvin): **2 bars/tote face**
  (4→8) **+ certified anti-slip mat** (μ 0.2→0.6) **+ 2 straps/stack** → SF 1.59 bar-alone / 4.77 w/ mat.
  Cascaded: constants, 3D `tote_restraint()` (5 models re-sent), weight (90→119 kg), parts (+mat) + costing
  (+$40/$80), 2D ibc-frame/ibc-stacking sheets, report §3.2/§3.4 (computed table + citations).
- [ ] **Phase B — fastener + weld schedule.** J1…Jn (bolt size/grade/torque/washer/locker: foot anchors,
  cleat M12×40, wall-hanger M12×65, backing-plate) + W1…Wn (fillet leg + symbol + all-around/stitch:
  uprights↔rings, feet↔uprights, bars↔cleats, ring→bar, hanger folds; from the Phase-A weld-throat demand).
- [ ] **Phases C–E (deferred):** datums/tolerances (GD&T); fab-detail sheets (member cut list, foot/hanger/
  backing-plate details, weld map, verify vs `ibc-stack.skp`); optional rendered load-case sheet.

## Weight model — film-plane moving mass undercounts the ACM backing — DONE 2026-07-25

_Fixed: `_film_plane_carriage_weight()` now adds the Dibond ACM backing (`RHO_ACM_4MM = 4.75 kg/m²`,
validated vs the 3A Composites/Curbell DIBOND datasheet — not the loose 5.5 — × the FP_W×FP_H face
≈ 45 kg). Film-plane carriage line 21 → 66 kg. Weight blocks re-injected + 5 PNGs regenerated;
§3.3 component row + the max-Blue-fill tip table hand-reconciled; CG/ISO still well within (loaded
util 21%). The per-corner load for the cross-slide section is still un-quantified (see the film-plane
milestone) but now has the correct moving mass to draw from._

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
- [x] **Reconcile the two film-plane 3D models — DONE 2026-07-19.** _(⤳ **REVERSED 2026-07-20** — Alvin's call to **retire** `film-plane.skp` instead of keeping both; see "Retire the superseded film-plane.skp" below.)_ `film-plane.skp` geometry was ported to the built U-channel/skate/U-joint design earlier this session (`_corner_parts()`, committed); `component-dependency-map.md` §3.1 now describes it as U-channel (not Option-A leadscrew) and a **film-plane-mechanism row was added** with the split of responsibility (mechanism = bolt-level single-corner detail; film-plane = same design at whole-plane scale + the animated DCs). ~~Both are~~ Both are
  KEPT (film-plane.skp is NOT retired). `film-plane.skp` = the full film-plane model (older Option-A
  leadscrew DC); `film-plane-mechanism.skp` = the current corner mechanism (U-channel/skate/U-joint). They
  describe overlapping geometry and have diverged — reconcile so the full model carries the current
  corner design (or define a clear split of responsibility). The report now embeds film-plane-mechanism; both
  stay registered in `dependencies.yml`. Also: `component-dependency-map.md` §3.1 model table (line ~480)
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

- [x] **Master shopping list — add a part number for each primary supplier — DONE 2026-07-21.** The master by-type BOM (`emit_master`) now renders each line through the same `_item_cell` convention the per-report §Parts-Lists use — the item name is hyperlinked to its supplier URL and the registry `part_no` is appended `(SKU)` — so an order can be placed directly from the master. Every registry row that carries a `part_no` now shows it (17 SKUs + 22 URL-linked at time of change); the remaining branded rows show no SKU only because the *registry itself* doesn't carry one yet — that data backfill is the job of the parts-identity worklist item below (Alvin's supplier paste-check), and each SKU auto-appears in the master on the next `parts.py --inject`. (Alvin 2026-07-19.)
- [ ] **Reconcile the EPDM gasket on the cargo-door-facing wall of the hinge panel.** Now that the top/bottom door seals are strip brushes, re-check the panel perimeter / housing-surround EPDM on the cargo-door-facing (exterior) wall of the hinge panel — confirm what stays EPDM vs brush and that the 3D/report/parts agree. (Alvin 2026-07-19.)
- [ ] **Revisit film-plane EPDM foam-tape coverage.** Qty set **provisionally to 2× 25 ft rolls** (McMaster 8694K88, 50 ft) — right-sized to the ~43 ft film-plane perimeter (the old 3×50 ft = 150 ft was ~3.5× over). When reviewing the EPDM seals, confirm a single perimeter run + corner/overlap allowance is covered by 50 ft, else bump to 3 rolls. `parts.py` `epdm-foam-tape` carries a "provisional qty" note. (2026-07-21.)

## Through-bolt grips — bracket assembly spec (precedes bolt length/thread finalization)

- [x] **Formalize the container wall corrugation depth + re-size the wall through-bolts — DONE 2026-07-21 (measurement gate PARKED, see Bucket 3).** ISO research: standard **side-wall corrugation ≈ 25mm (1″)** (25–30mm range; 1.6–2.0mm sheet); **end-wall ≈ 36mm** trapezium (pitch 278, outer 2.0mm / inner 1.6mm) — [DiscoverContainers](https://www.discovercontainers.com/shipping-container-components-classifications/), [FreightAmigo](https://www.freightamigo.com/en/blog/international-relocation/shipping-container-dimensions-and-wall-thickness-essential-guide-for-logistics-and-relocation/). Added `CONTAINER_CORRUGATION_DEPTH=30` (conservative max; the through-bolts pass the long **side** walls); recomputed each wall through-bolt grip → the old M12×80/×90 were oversized → shortened to **M12×65 partial-thread** (≈50% cheaper) with 2 shim washers/bolt to pad a shallower real wall. **Residual = physical measurement only**, now parked as an early procurement gate (Bucket 3). Bracket plate material = **A36 mild steel** (apply to film-saddle / walkway-bracket / right-walkway-cleat / IBC-hanger plate specs at build). (2026-07-21.)
- [x] **IBC wall-hanger M12×40 grip conflict — DONE 2026-07-25 (exterior through-wall retained).** Alvin's call: keep the exterior through-wall sandwich. Wall-hanger through-bolts → **M12×65 ×16** (the partial-thread SKU that spans the ~42-54mm grip); front-bar → upright cleats stay **M12×40 ×8**. Added M12 nuts (16) + washers (64 flat + 16 split) + the 4 exterior 100×135×8 backing plates (were uncosted). Count reconciled to **24 total** (was an under-counted 12). parts.py + costing (LineItem + EXPECTED, +$59/+$72) + report §3.2/§3.4 + injected §5 BOM + 2D Detail B / frame-drawing all say 4× M12×65 hangers; 3D bolt left a generic cylinder (spec in 2D/parts — not worth re-sending 5 models for a 7mm visual). lint + verify-all green.
- [x] **Reconcile fastener thread pitches (bolt vs nut, per size) vs the datasheets — DONE 2026-07-29.** All coarse + matching, verified from the eng-specs PDFs: M5×0.8, M6×1.0, M8×1.25, M12×1.75. `bolt-m8-fixing`/`-wall` (91280A534) confirmed **M8×1.25 coarse** (not the M8×1.0 fine adjustment screw — that trap is clean). Registry "confirm vs SKU PDF" caveats replaced with "confirmed vs <SKU> PDF". Non-coarse specials remain self-consistent (front-board M8×1.0 fine not in parts.py; pinhole ring M52×0.75). Residual: `spray-arm-jamnut` (Amazon B007IA07PS) recorded M12×1.75 but no datasheet — low risk, single jam nut.
- [x] **Processing-tray center-seam joint — DONE 2026-07-21.** Resolved as a **~40mm shingle-oriented lap** (uphill panel laps *over* the downhill one so water sheets off the step on the 1:200 floor), **silicone-bedded** (lap + top bead), bolted with **12× M6×16 316-SS (93635A210) + serrated flange nuts** underneath. `bolt-m6-tray` sourced + priced. New detail sheet **spray-bar-sheet8** (`draw_sheet8`, "Detail C — Center-Seam Shingle-Lap Joint") drawn + registered (gallery + publish.sh + setup_docs.py) + embedded in report §2.6; report §2.1/§2.6 + parts updated.
- [x] **Design the spray-arm pinch-clamp geometry — DONE 2026-07-21.** Resolved the Ø12-stud-in-Ø21-tube mismatch: a **turned 6061-T6 AL adapter** (M12 female bore onto the stud + M12 jam nut → Ø21 male spigot) reduces the stud to the tube bore; the arm-tube bottom is **slit ~30mm** and an off-the-shelf **25mm/1" clamp-style shaft collar** pinches the tube onto the spigot (rotational adjust + lift-off for transport). The loose `bolt-m6-pinch` + its nut are **retired** (replaced by the collar's integral screw). Parts (`spray-arm-adapter`, `spray-arm-jamnut`, `spray-arm-collar`) added; `spray-bar-sheet2` redrawn; report §arm table + prose updated; +$20/$33 on spray.
- [x] **Resolve the pinhole END-wall mount detail — DONE 2026-07-21.** Both mounts get **welded flat backing** on the corrugated end wall (crest-mounted, no corrugation bridging): the flush power panel gets a **raised 8mm steel weld-in frame** around the cutout (flat sealing surface + M6 weld-nuts) → `bolt-m6-panel` = **M6×20**; the shelf hinge cleat + 2 stay anchors get **8mm welded backing plates** (M8 weld-nuts) → `bolt-m8-wall` = **M8×25**. Both short → fully threaded, grip ~12–14mm. Parts added (`power-panel-frame`, `shelf-wall-backing ×3`); electrical-sheet6 VIEW B + shelf-sheet3 redrawn to show the welded backing; reports updated; +$15/$25 power, +$18/$30 shelf.

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

## Muslin clamp → off-the-shelf clamp — DONE 2026-07-25

_Shipped as an **off-the-shelf nylon spring clamp** (Pittsburgh 69289, 3½″ fiberglass body + swivel
pads; 2½″ 69290 fallback) biting the ALU-angle + HDPE-filler + ACM sandwich — no fabrication. The
intermediate bespoke "spring clip" and the original "cam-lever toggle" are both retired. Fully
cascaded: `film-clamp-mechanism-report.md`, `parts.py` (`muslin-clamp` 69289 + `clamp-filler`),
`tbs_constants.py` (bespoke `CLAMP_BASE/LEVER/JAW/OPEN_GAP/SPRING_F` deleted; only
`CLAMP_SPACING`/`CLAMP_FILLER_D`/`CLAMP_N_*` remain), and Sheet 6
(`generate_film_plane_mechanism.sheet6()` — Panels A/B/C, no Panel D, no cam-lever). Frame section =
L (2×2 angle); the offset-T alternative was drawn then reverted — parked, not pursued._

## Walkway pop-out extension past the pinhole — DONE 2026-07-23

_Built + fully cascaded (rev 2026-07-23b): the near-walkway bump-out was extended a 2nd rib toward
the IBC to `WALKWAY_NEAR_WIDE_X_R = 3083` (band X1055–3083, 5 widened brackets) — a full standing bay
past the pinhole (X2399) on the IBC/filter side. Cascaded to `tbs_constants.py`, Sheet 9 (Detail F),
`walkway-report.md` §3.2 + BOM, and the 4 .skp models (walkway/overview/water/film-plane). Current
extent accepted (Alvin 2026-07-25) — "an IBC-width past the pinhole" is met by the full-bay
extension; no further geometry change._

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
- [x] **FP_H cascade — `.skp` re-sends DONE 2026-07-20.** Branch `film-plane-redesign`:
  the active film-plane height is now **2,094mm** (top rail lowered 44mm via the `RAIL_OFF`→`RAIL_OFF_TOP`/`RAIL_OFF_BOT`
  split). Constants, parts/costing, all FP_H diagrams, weight, and the report prose/config table are cascaded + committed.
  - [x] **overview.skp — DONE 2026-07-20.** Re-sent `generate_sketchup_model.py` into the live doc; verified FP top
    rails at Z2244 (= C_HGT − RAIL_OFF_TOP) + bottom rails at Z160; Alvin saved + re-uploaded (UID `e624e210…`);
    `overview.skp` + `overview.rb` committed (`105ec8bc`). `lint.py --verify-all` now fully clean.
  - [x] **film-plane-mechanism.skp — DONE 2026-07-20.** Confirmed current: a fresh `--save` regen was
    byte-identical to the committed `.rb`, so the model was already built from the post-FP_H code. Re-sent into
    the live doc anyway to be certain; Alvin saved + re-uploaded (UID `572b4aaa…`); `.skp` committed.
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

## Retire the superseded `film-plane.skp` + its generator — DONE 2026-07-20

_Alvin 2026-07-20: `film-plane.skp` (the older full-plane "Option A" model) is superseded by
`film-plane-mechanism.skp` + `generate_film_plane_mechanism_model.py` — retired. Reversed the
2026-07-19 "both KEPT" reconciliation above. `overview.skp` carries the film-plane geometry inline and
**stays** — this retired only the standalone film-plane model._

- [x] Deleted `src/models/generate_film_plane_model.py`, `src/models/film-plane.rb`, and `models/film-plane.skp`.
- [x] Removed the `film-plane` script→output entry from `dependencies.yml`; the `lint.py --verify-all`
  model set derives from `dependencies.yml`, so it dropped 7 → 6 automatically.
- [x] Removed the `film-plane` entry from `models/sketchfab.json`. **Alvin's manual step:** decide whether
  to unpublish the dormant Sketchfab model (UID `bb5394a8983a491fa541088b901c24f8`) or leave it. The report
  embeds **film-plane-mechanism**, not film-plane, so no report embed changed.
- [x] Dropped the `film-plane` row from `component-dependency-map.md` §3.1 and fixed the
  film-plane-mechanism row's cross-reference to it.
- [x] Grep sweep clean (no stragglers in `publish.sh` / `setup_docs.py` / docs); `lint.py` +
  `lint.py --verify-all` green. Added a `[Unreleased]` RELEASE.md entry.

**Parked working-tree files (2026-07-20):**
- `src/models/film-plane.rb` — **RESOLVED:** deleted with the model (the stale regen went with it).
- `overrides/partials/copyright.html` → `src/overrides/partials/copyright.html` — **RESOLVED 2026-07-20:**
  it was a half-finished move (file copied to `src/overrides/` + deleted from root, but `custom_dir` never
  updated — would have broken the footer version stamp). Finished the move: `git mv` to `src/overrides/`,
  updated `custom_dir: overrides` → `src/overrides` in **both** `mkdocs.yml` and `setup_docs.py`; verified a
  build renders the "Version v0.3" footer from the new path.

## Cost / data modeling
- [x] **Reconcile 304 vs 316 stainless — DONE 2026-08-13.** Codified a **stainless-grade policy** in the
  `parts.py` registry header: the cyanotype wash has **no chloride**, so 316's pitting resistance is unused →
  **304 (A2) is the default** for all wet/splash structural stainless; **316 is metallurgically unneeded**
  anywhere (kept only on `bolt-m6-tray` by Alvin's belt-and-suspenders choice). The real gap was the reverse —
  **zinc fasteners in wet zones** — so upgraded `bolt-m6x20` (×2: spray + panel) and `bolt-m8-fixing` → **304
  A2-70** (resolved their ⚠ VALIDATE flags). **M12 structural through-bolts KEPT Grade 8.8 zinc** (strength
  800 MPa + heads sit outside the container, inspectable; going stainless w/o a strength loss = A4-80/316,
  not worth it — Alvin). 410 self-drillers + the 51118 chrome-steel bearing kept (functional). **Sub-TODO
  DONE 2026-08-13:** 304 A2 SKUs sourced + firm-priced — M6×20 McMaster **91287A137** $17.77/50, M8×25
  McMaster **91310A535** $13.91/50 (`checked_date` stamped); the ±$1–3 registry shift reconciled into the
  FILM (−1) + spray (+3) costing aggregates; all gates green.
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
- [x] **Register the film-plane joint-study generators in `dependencies.yml` — DONE 2026-07-20.** Added
  `corner_gimbal` (→ `film-corner-gimbal.png`), `joint_options` (→ `film-joint-options.png`), and
  `joint_study` (→ `film-joint-study-gimbal.png` + `film-joint-study-ujoint.png`) to the `generators:` block;
  `lint.py` `dependencies.yml valid` gate green (each script references its declared outputs), so the
  missing-cascade sweep now covers them.
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
