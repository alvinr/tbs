<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
<!-- Working/internal tracker — NOT published (not registered in publish.sh). -->
# TODO & Actions — TBS-001

The **single record** of OUTSTANDING actions — open `[ ]` and in-progress `[~]` only.
Add new items as they arise; tick to `[x]` and delete once done (this file is pruned to
outstanding work, not a history log). Detailed sub-trackers are linked where the detail is extensive.

---

## ⏳ Light-trap parts-quote — pending research (2026-08-24)

- [~] **Brush + holder — KEEP AS-IS for now (2026-08-24: "drive to completed blueprints, optimize cost later").** Leave `ll-wiper-brush` (#4 3/16″ est) + `ll-wiper-holder` (Tanis Al est) + the current drawing (Sheets 4/6/7) unchanged — the design is complete; only the price is an estimate. **Cost-optimization candidate for later:** Grainger 18A417 brush + 18A320 holder (confirmed 1/8″ backing pair, 3/4″/19mm trim; only in 10-packs → $270+$259 for a 4-need — expensive as-is; a by-the-foot source would cut it). If adopted later, re-spec the drawing/constants to 1/8″ backing/19mm trim → cascade Sheets 4/6/7/10.
- [~] **Edge channel — KEEP AS-IS for now** (same "optimize later" call). `ll-edge-channel` stays est; candidate = McMaster 9001K723 (6063 Al confirmed, 3/64″ wall, $18.18/8 ft) + 8× L-clips still to source.

---

## 🛠 Tooling / infra

- [ ] **Model-drift audit — the overview should be the UNION of the sub-models, not a re-implementation (2026-10-05).** Found while wiring the EP: the **overview drew its OWN electrical circuit wiring** (grey fan feeds / conduit drops / lighting conduits / Cct-C feed in `generate_sketchup_model.py` `lighting_wiring()`/`fan_wiring()`) instead of reusing `em.circuit_runs()` — so the color-coded per-fuse circuits in **electrical.skp** never appeared in **overview**, and the two drifted. Being fixed now by bringing `circuit_runs()` into the overview. **Broader action:** audit EVERY component the overview re-draws vs its owning sub-model (lighting/fan loads vs `em.context` ghosts; pumps vs water; fan-B/light-trap vs lighttrap; walkway brackets — see [[project_walkway_bracket_duplication]] and [[project_overview_electrical_duplication]]) and make the overview COMPOSE the sub-models (shared single-owner builders) rather than keep parallel copies. List the drifted pairs + decide a single owner for each.
- [ ] **Two pre-existing pipe-vs-solid clashes surfaced by the `check_interference` fix (2026-10-05).** The crossing
  check was skipping any conductor whose name contained a solid keyword ("… → **panel** GFCI", "… → pinhole **wall**");
  fixing that (routed runs are always pipes) revealed two latent pipe-vs-solid clashes OUTSIDE the EP — neither
  introduced by the EP work (both at X≈4600). Investigate + resolve each (confirm real vs by-design, then reroute the
  pipe or notch/butt the solid):
  - `Input stub 3/8 (X slide → U-joint) TR` ↔ `Saddle seat TR far` — film-plane mechanism, far TR corner (~4596,2245,2252); ~6mm overlap.
  - `Blue supply trunk → spray bar / TAP-01` ↔ processing-tray exclusion zone (~4616,1161,147) — water system near the tray.
- [ ] **Label-overflow backlog — cross-generator `--overflow` sweep (2026-08-25).** New render-based
  `tidy_labels.py --overflow` (measures each label's bbox vs the axes frame; skips tiny insets) swept all 41
  generators clean (0 render errors) and found **49 genuinely off-frame labels** (one-sided ≥15%; ~163 sub-15%
  are tight-bbox noise, ignore). **UNBLOCKED** (light-trap blueprint shipped); the owner-led diagram review is
  complete (2026-09-30), so this is now background tooling hygiene — tackle opportunistically,
  **one generator per tidy pass** (skill discipline —
  render → crop-zoom → verify), priority by count/severity:
  - **film_plane_mechanism** (10, worst +52%) — pre-existing overflow/crowding on Sheets **1–11** only (Sheet 2 section
    titles ±19–20%, Sheet 1 "LEFT RAIL" +17%, Sheet 3/4 crowding, Sheet 6 +8%; `CARRIAGE_YD_CENTER` panel overflow).
    The fab-blueprint round (2026-09-05, `filmplane-bp`) renumbered the set to **20 sheets** and left these untouched
    (out of blueprint scope); the NEW Sheets **12–20 are already tidy-clean**. One tidy pass over 1–11 remains.
  - **weight_analysis** (9, +35%) — Sheet 1 "Total / CG" stats boxes hang off the BOTTOM (P8 notes placement).
  - **ibc_frame_drawing** (9, +19%) — Sheet 1 DATUMS + member-schedule table off left (P8).
  - **shelf_diagram** (3, +33%), **joint_study** (4, +19%), then walkway/electrical/tray_redesign/corner_gimbal/
    portrait_viz (1 ea, +15–26%).
  - Re-run `tidy_labels.py --overflow src/generators/generate_*.py` after each pass to confirm the list shrinks.
  - ✅ **spray_bar Sheet 7 `+192%` off-left FIXED (2026-09-28)** — it was a hidden DUPLICATE beam-section label
    on the nozzle panel (not the `CARRIAGE_YD_CENTER` hypothesis); dropped it (beam is called out on ax_cf +
    dimensioned on ax_nz). This bullet stays only as the note that the anomaly is resolved; delete on next prune.
- [~] **Consolidated plywood cut-sheet generator — BUILT 2026-09-30, cut-optimized + published 2026-10-01.**
  `generate_plywood_cutsheets.py` + `plywood-cut-sheets.md`: a plywood registry (every `timber-ply` part, cut
  dims single-sourced from `tbs_constants` where geometry-driven, else spec/report literals; cost/SKU keyed to
  `parts.py`) → a schedule sheet + a per-stock nesting sheet. **18mm standardization + Fan-B PT→SYP re-grade +
  a 5mm-tolerance guillotine packer dropped the stock from 8 part-by-part → 4 sheets (−$148).** The nest is
  guillotine-cuttable (90° edge-to-edge), with numbered saw-cut lines + per-sheet cut counts (4 sheets, 45 cuts).
  Sheets lettered A–D; cleats = one cut-to-length strip. Drifts reconciled (18mm, shelf 600×225, Fan-B 1225).
  **Residual (open):** (a) refactor each *consumer* generator to import the shared piece dims from the registry
  instead of its own literal (the "so each consumer references it" half — not yet done).
- [~] **3D single-owner dedup pass (2026-08-18) — cleaned the cross-file duplicate emitters.** Built the
  `lint.py` ratchet gate (no NEW cross-file duplicate emitter) and consolidated each cluster to a single owning
  builder: **electrical** (em owns cable trunking, inverter box, master switch), **Fan B box** (lighttrap),
  **processing tray** (overview `processing_tray(alpha=)`), **walkway Far/Near** (wm `far_deck()`/`near_removable_deck()`),
  and (2026-10-01) **Fan-B mount band** → `lt.fan_b_mount_panel(alpha)` (lighttrap swings it, overview draws it
  static) + **tray sump strainer foot** → `cp.sump_strainer_foot()` (cp owns, pw calls). Both dropped from
  `_EMITTER_DUP_ALLOW`; the Fan-B band extent was resolved by the swinging-panel reconciliation (473×943, bottom
  at the floor-gap line 282 — single-sourced across 2D + 3D). **REMAINING (accepted, no action):**
  The 3rd finding is accepted:
  - **Pinhole wall (mini_tbs)** — ACCEPTED as-is: mini_tbs is a scale toy (BOX_W×BOX_H), pw a real wall section;
    different representations (like the context floors). No action unless mini_tbs is retired.
  (The 2 `Floor`/`Floor (context)` ghosts are permanent allowlist — featureless per-model context.)

- [ ] **`check_interference.py --bolts` — orientation/grip lint (PROTOTYPE landed 2026-08-17).** New read-only
  advisory pass: for every structural grip bolt it finds the members its centerline pierces and flags **EDGE**
  (center-to-edge < 1.5·D — the J2/J7 3mm-edge class that kept slipping to review), **FLOATING** (pierces no
  member), **PROJECT** (shank runs past the grip). Bounding-box based, scoped to structural steel (film-plane
  precision mechanism + liquids excluded), drawn-D so slightly conservative. **Triage the 15 current overview
  flags:** the genuine one is **RWk J6 top bolt 15.3mm from the end-plate top edge** (make `RWK_J6_EP_H` ~6mm
  taller, or accept); **Frame-corner bolt 7<9 in the X-slide shaft support** (film-plane bracket — confirm);
  the `0.6/2.0mm in beam upper/lower` are half-lap remnant clips (benign if the remnant isn't load-bearing
  there); IBC wall-bolt 18<21 is nominal-OK (drawn D14 vs M12). **Next:** wire it into the pre-send routine +
  a lint advisory; consider a `bolted_joint()` emitter so orientation is correct-by-construction (retro item A).

- [ ] **Reconcile ALL 3D builders — the models are partial VIEWS of ONE design, not alternatives (2026-08-17, HARD PRINCIPLE).** A design change must reflect in **every** model when they regenerate; the
  model must not drift. The GOOD pattern already exists — the IBC front bars are one shared builder
  (`generate_corridor_water_panel.py` `tote_restraint()`) that overview/ibc-stack/water all call, so the
  4-bar + cleat + M12×65 + hex-bolt changes flow to every model on regen. The DRIFT RISK is **dead/divergent
  re-implementations left lying around**. **PROGRESS 2026-08-17:** `ibc_rack()` (the OLD single-portal 2-bar+stub
  front-bar frame, X4734) was RELOCATED out of the live `generate_sketchup_model.py` into its sole consumer, the
  archived right-cantilever study — so the live module can no longer accidentally re-wire it (overview can't
  silently revert). **AUDIT DONE (2026-09-28):** swept every model builder — **no new/untracked duplicate
  emitters**; every multi-model component resolves to ONE shared builder the other models *call*, except the 5
  already-tracked clusters (2 live BLOCKED drifts = Fan-B band + tray sump foot [see the dedup item ↑], 2
  accepted = pinhole-wall representation + walkway-bracket LOD, 2 permanent Floor ghosts). The existing detection
  is two-tier in `lint.py`: the static `_cross_file_emitter_dups()` ratchet (name + `ruby_*` literal) **plus** a
  runtime geometry-equality harness (`_DUP_PAIRS`/`_record()`) for same-part-different-label copies (EP core,
  walkway bracket). **REMAINING (the only open piece):** a `check_consistency.py` gate — but rather than reinvent,
  have it *call* `lint._cross_file_emitter_dups()` + run the `_DUP_PAIRS` equality checks, and add a name-alias
  layer so a same-part / different-label copy can't slip past the pure name-match. Lower priority than resolving
  the 2 live drifts.

- [ ] **`--solids` larger sanctioning pass (model-wide, beyond the named categories).** The
  `check_interference.py --solids` sanctioned list currently covers only the categories triaged in the
  walkway/IBC/light-trap/fan/tray work (one-piece formed parts, compression seals, bearing fits, liquid
  contents, seated connections). Run model-wide it still surfaces **~164 OPEN in the film-plane corner
  gimbal alone** (U-rail↔depth-rail, cross-slides, gibs, UHMW pads, trolley/U-joint) plus a few other
  mechanisms — mostly intentional one-piece/bolted/bearing overlaps that just aren't classified yet. To
  make `--solids` report globally clean: walk each mechanism, butt/notch the genuine fused-seam defects,
  and extend `_SANCTIONED_SOLID` with the rest (each with a reason). Larger effort; do per-mechanism.
  - **Film-plane blueprint Phase-0 triage (2026-09-05, `filmplane-bp`).** Ran `check_interference.py`
    against the live `film-plane-mechanism` model. **Pipe/solid OPEN = 0.** `--solids` = **165 OPEN**,
    dominated by U-channel **web↔flange self-overlap** (one-piece extrusion modeled as boxes — intentional),
    seated **rail↔frame** contacts, and **stub↔bore** fits — no fused-seam defect in the sample; matches the
    "mostly intentional, just unclassified" characterization above. The detail sheets (12–20) draw these as
    designed. Full `_SANCTIONED_SOLID` classification stays THIS separate task, not the blueprint.
    `--bolts` = **21 flags, none a genuine structural defect:** the frame-corner **7mm<9mm** (×8) is M6 into
    the purchased **McMaster 4040N12 shaft-support clamp** (catalog-fixed hole pattern, precision fit — NOT a
    1.5×D-in-steel structural grip; can't widen/move a bought part's hole), frame-corner "in Input stub 3/8"
    (4.8<9) is a worst-edge artifact (can't get 9mm edge in a 9.53mm stub), thumb-screw/rail-fixing PROJECT
    33mm is by-design (graspable), IBC wall bolt 18<21 is nominal-OK. **These precision/catalog bolts should
    be added to the `--bolts` `_MECH_KEYS` filter** (deferred — lint hygiene, not blueprint).
  - **Two bolt flags for ALVIN, outside the corner-mechanism sheet scope:** `Foot anchor M12 edge 5mm in
    Frame rail (Yd)` and `FP combined beam TEK screw 55mm past grip` (far-left combined beam, Sheet 11 area) —
    the TEK projection looks like a real drawn-length issue; worth a separate look, not part of Sheets 12–20.
  (Scoped out of the 2026-08-16 named-category pass.)

- [~] **Solid-joint seam audit + butt-vs-weld convention (3D readability).** Overlapping same-color solid
  members render with NO seam line, so distinct parts read as one fused piece (found 2026-08-14 at the IBC
  retaining-bar → corridor-upright joint — the bar ran *through* the post). **TOOLING DONE (2026-08-16):**
  `check_interference.py --solids` lists SAME-color solid↔solid interpenetrations (3-axis overlap, so butts
  don't flag) above a volume threshold, sorted, each tagged `weld` or `BUTT?` (bolted/cleated). Convention
  codified in `skills/skill_model_consistency.md` (§Readability seam audits). **REMAINING — triage + fix:**
  the pass reports ~60 on the water model (33 `BUTT?`); most `BUTT?` are actually welds (foot-plate↔post,
  filter cap↔port = molded). **PROGRESS 2026-08-17:** **RWk J6 backing plate ↔ frame rail** — FIXED (see the
  J6 item above; the plate now butts the rail top). **RWk end beam ↔ long beams** — already butts (right_walkway_
  cantilever lines 950–953). **REMAINING:** the RWk **long-beam ENDS ↔ wall-cleat back-plates** (the inner/outer
  beams run to Yd0/C_WID and poke ~8mm into the 8mm cleat back-plate) — inset each beam end by the plate thickness
  so it butts. Readability only (not a real clash); do it when **overview/walkway** is open (can't verify against
  the live ibc-stack). Also on ibc-stack `--solids`: **9 OPEN are by-design** (filter cap↔port ×6 molded, bar↔
  D-ring holder, the two-leg welded L-cleats) — pending a **sanction list** in check_interference so they stop
  flagging. Run against the **overview** model (has all structural members) for the full list. (2026-08-14.)

- [~] **Pipe-through-surface seam audit (3D readability) — same class as the beam fix above.** A pipe
  passing *through* a surface (plywood panel, wall, plate) shows NO seam/butt line — reads as fused into the
  panel. **TOOLING DONE (2026-08-16):** `check_interference.py --pipes` flags pipes whose centerline crosses
  the FULL thickness of a panel/wall/plate slab and emerges the far side. On the water model it finds 13
  penetrations: **pump-mount ply shirt** (suction entries + Cct-C power branches), **rear panel (18mm ply)**
  (DV merges, X-port drains, suction), **drain-riser backing spine**, **processing tray floor** (sump→P-04
  drain). **REMAINING — fix each:** either (a) draw a short collar/grommet ring at the face, or (b) split the
  pipe so each side butts it. Each fix = generator edit + re-send (single-writer). (2026-08-15.)

## ⚡ Parts firm-up tracker — buckets by when they're actionable

### Bucket 1 — ACTIONABLE NOW
- [~] **Aug 2026 full re-price — SWEEP COMPLETE across all 6 systems (2026-08-01).** electrical / water / spray = 100% firm-priced; film / ibc-frame / shelf = material drivers firm, fab + bulk-steel deferred (rule below). Grand total settled **$25,874 / $30,346 / $36,874**. Notable moves: spray beam → single 16 ft 0.062in SS tube (no butt weld, sag-checked, −$394); corner L-plates $58.90 ea; U-joint boots, GHS labels, citric acid, pH buffers, zip ties, powerpole, blade fuses, ph-cal all firmed; wall-seat-saddle split into 8mm/10mm plate lines; bolt-m12x40 → 18-8 SS 92314A744. **Rule established** ([[feedback_material_now_fab_later]]): quote RAW MATERIAL now (the driver); defer fab (cut/bend/weld) to post-blueprint; bulk structural steel = steel-yard/freight quote, NOT online cut-to-size (which caps at 96in + overprices ~3×). **Deferred (owner-side, not blocked on me):**
  - **Fab quotes (post-blueprint):** film cross-slide assembly (¼in bar firm $134.73, + UHMW/gib/fab), the 2 wall-seat-saddle plate cuts + weld.
  - **Steel-yard bulk quotes:** `ibcf-rhs`/`ibcf-feet`/`ibcf-wall-backing` (2×2×⅛ A500 + A36 plate), `shelf-steel-shs` (1×1×⅛ A500 6 m). Estimates are realistic bulk figures.
  - **At-purchase confirms:** `shelf-folding-stays` + `shelf-transport-latch` (zinc chosen, estimates hold).
- [ ] **Master-BOM SKU backfill.** Branded rows that don't yet carry a registry `part_no` — the supplier paste-check; each SKU auto-appears in the master on the next `--inject`.
### Cost-reduction opportunities (grounding — analysis 2026-07-31)
Ranked by saving potential, analogous to the SS→ALU depth-rail switch (`fp-u-channel` $2,173→$328). Each
needs a dedicated follow-up to model + cascade before committing. Cost by system for context: chemistry
$5,466 · film $4,216–4,572 · container $2,300–4,300 · electrical $3,431–3,496 · water $3,370 · walkway
$1,979–2,825 · lightlock $2,046–2,516 · tray $1,583–2,271.
- [ ] **Ferric ammonium oxalate (AmFe) — $4,026, biggest single cost (sourcing lever, not a switch).**
  `amfe-rich/standard/lean` = $2,196+$1,098+$732 @ $64.20/kg. Core chemistry — the lever is bulk/cheaper
  supplier or trimming the *rich* coat tier, not a material swap. Even 15% ≈ $600. Follow-up: chemistry
  sourcing pass (also `ferri-rich` potassium ferricyanide $582).

### Bucket 2 — ACTIONABLE WHEN BLUEPRINTS FINALIZED (v1.0)
- [ ] **Front-bar J2/J7 joint — crush through the hollow bar (design review at quote time, 2026-08-17).**
  Each L-cleat runs 1 HORIZONTAL M12×65 through the L's vertical leg + the bar's 50mm web (both 3mm web walls),
  with a 40×50×8 backing plate on the far web. The backing plate stops the far wall dishing under the nut, but
  torquing a bolt through both walls can still draw the 50mm web together (crush) — resolve before fab: add an
  internal spacer/crush-sleeve at each bolt. Decide with the fabricator at quote; then reconcile the spacer part
  through Detail B / parts.py / the 3D. **Do NOT "restore M12×40"** — the single horizontal M12×65 through the
  tall web is the confirmed design of record (the 2× M12×40 vertical joint left only ~3mm edge; reverting
  reintroduces that defect — see fastener-standardization.md).
- [ ] **Fastener standardization (part-reconcile branch) — remaining open items** (decisions/details in `fastener-standardization.md`):
  - **Tilt-swing board** — design chat: socket-vs-hex heads, M8×1.0 fine vs M8×1.25 coarse pitch, A4/316 vs 304/zinc, and itemize its off-registry fasteners (M8×1.0×80 / M12×45 / M16×55 SHCS / M6 set screws / dowel pins) into `parts.py`.
  - **M5 → flange bolt + nyloc** — deferred to the chem-shelf design (no blueprint yet).
  - **Filter bracket 244718 — confirm URL + price** (switched to the bracket-only Pentair 244718; $10.50 kit price held as a conservative placeholder, `filter-skid-frame`).
- [ ] **`pinhole-shim`** — Lenox SS-3/8-DISC laser-drilled pinhole; firm via RFQ once the optics drawing set is design-complete.

### Bucket 3 — ACTIONABLE ON BUILD
- [ ] **Container corrugation depth — PARKED pending physical measurement (EARLY procurement gate, post-blueprints).** The design side is CLOSED and robust to the unknown: `CONTAINER_CORRUGATION_DEPTH=30` (conservative max of the 25–30mm ISO side-wall range), the IBC wall-hangers use **M12×70 partial-thread** sized for the 42–54mm worst-case grip, and the BOM already carries **2 shim washers per bolt** (`91166A290`) to pad the grip if the real wall measures shallower. **Gate action (do FIRST, before ordering any wall fastener / bracket plate):** once the actual container is on site, **measure the real side-wall corrugation peak-to-valley**; if <30mm, confirm the shim count and whether M12×70 can drop to a shorter partial-thread length; apply **A36** to the final bracket-plate specs. No desk work possible — needs the physical container.
- [ ] **Walkway grating.** American Grating is primary (~$830 public list, banded $830–$1,050 for freight/cut); get the **firm cut quote + SoCal freight** at build. **McNichols is a FIRM SHIPPED fallback: 2× 48″×144″ @ $796.77 = $1,593.54 + $456 freight = $2,049.98 shipped (firm 2026-07-24)** — ~2× the American estimate, and its 4′×12′ sheet would re-nest the cut plan if chosen.
- [ ] **Container** — `container-20ft` (±$1,500) + `container-delivery` (±$500), firm at purchase.
- [ ] **Fab estimates.** All `*-fabrication` lines (`tray-fabrication`, `ll-fabrication`, `ibcf-fabrication`, `sp-door-fab`) + `tray-ss-sheet`, the film-plane fab (skate carriage, 304 cross-slides, cam clamp), and the `sp-pivot-post` collar — quote to shops once the drawing set ships. ≈±$1,500.
- [ ] **Buy the film-plane U-joints (`fp-ujoint`).** Belden **SSNBUJ750x3/8KB** (Grainger **41D816**) — needle-bearing, 3/8" keyway + set screw, stainless, 45°, factory-booted. **$252.13 ea × 4 = $1,008.52**, + 8× 3/32×3/64 SS machine keys (`fp-ujoint-key`, ~$6–10 lot) + keyseat the 3/8" stubs. Firm-priced (2026-08-13); purchase at build. **Confirm the set-screw torque spec with Belden/Grainger** (datasheet gives static breaking 95 in-lb only). Supersedes the retired plain UJ-SS750x375 + separate 806VF1 boot.
- [ ] **IBC flex-connection `s60-reducer` interface (bench).** The sourced reducer (Charlotte `PVC021071300HD`, 2"×1" Sch-40) is **spigot×slip (solvent-weld)**, but the tote adapter (Granatan S60→2") outputs **2" MALE NPT** — a spigot×slip bushing is glue-only, so it needs a **2" MPT×socket transition** to mate (or swap to a **2"FNPT×1" reducer**). Verify/resolve the tote-adapter interface at the bench. (2026-07-29.)
- [ ] **IBC flex-connection clamp size (bench).** `ibc-flex-clamp` is an Apollo **#12** (½"–1¼", `IDL0410PK`). The flex hose is cut from the 1"-ID / **1¼"-OD** tray-suction coil, so over a barb the OD approaches/*exceeds* the #12's 1¼" max — **verify the #12 closes and seals; step up to #16 if it bottoms out.** (2026-07-29.)

---

## ★ MAJOR MILESTONE — manufacturing-ready blueprints (ALL drawing sets) — OPEN

_the call (2026-07-16): the current 2D sets are arrangement-faithful schematics (true-proportion +
topologically correct, reconciled to the 3D) but NOT manufacturing blueprints. The milestone is a
**definitive, dimensionally-correct, shippable-to-a-fabricator drawing package for EVERY subsystem** —
precise hole positions, tolerances, fastener callouts, datums, section views, material/finish, driven
parametrically from `tbs_constants` so they can't drift. Do the **film-plane corner mechanism FIRST** (below)
as the template, then roll the same standard out across all sets (film plane, water/tray/spray, IBC frame,
walkway, hinged panel, light lock, electrical, optics, …)._

- [~] **★ FINAL cross-cutting step — fastener standardization (LARGELY EXECUTED 2026-09-07, branch `part-reconcile`).** Full status + rationale live in **`fastener-standardization.md`** (target revised to metric families **6→5** — M5 retires, M10 KEPT). **Done this pass:** IBC J2/J7 spec reconciled to M12×65; M8 washer text/key/duty; **M12 wall bolts unified to one zinc length (×70)**; **5/16→1/4 ply-mount** (5/16 family retired); **#14 TEK unified** (90822A620); **optical-plate M12×40 itemized + socket→hex**; **TSB central M16→M8×1.0**. **Reversed on evidence:** M10 KEPT (thin light-trap hosts preclude M12 CSK); ⅛″ rivet consolidation INFEASIBLE (no grip spans both laps). **Remaining:**
  - **M5 → flange bolt + nyloc** — deferred to the chem-shelf design (no blueprint yet).
  - **TSB registry merge** — deferred to the TSB blueprint review (see the TSB item above).
  - **Tilt-swing A4/316→304 material downgrades** on non-structural fasteners — confirm at the TSB review.
  - **BOM-gap itemization** (M4 grubs, M4 cam-mounts, M12 pivot anchors/hinge brackets) — each blocked on a length dim; itemize per the owning sheet, don't assume.
  - **#14 TEK washer + M8×1.0×50 central SKUs** — SKU-pending items to firm at order.

- [~] **Chemistry prep shelf — blueprint round IN PROGRESS (2026-09-07).** Spec `chem-shelf-blueprint-spec.md`
  (ply-primary redesign: no steel frame; tee-nut attachments; 2 SS chain stays; M5 eliminated) + `chem_shelf_load.py`
  (Phase A — validated: board-bending SF 44, chain SF 5.4, tee-nut SF 20) DONE; all hardware sourced (hinge
  1582A457, eye bolts 3014T45/4843T13, chain 3392T51, links 8947T25, latch = reuse 1619A74). **Remaining = one
  coherent cascade** (pair the 3D re-send with the `overview`-model session): (1) `SHELF_T` 22→18 + new tee-nut/
  chain/stay constants; (2) fab-detail drawings (`generate_shelf_diagram.py` → board+tee-nut hole positions,
  bolt-on-hinge detail, chain/eye/wall-anchor detail, 8mm backing-plate 1:1 schedule; regenerate); (3) `parts.py`
  shelf rebuild (drop 25×25×3 SHS + M5 CSK + folding bracket + gussets; add tee-nuts/1-4-20 SS screw/eye bolts/
  chain/links/bolt-on hinge; latch→1619A74) + costing; (4) report `chemistry-prep-shelves.md` §3.1/3.2/3.3(load
  block)/6/7 to the new design; (5) 3D `chem_shelf()` builder (remove frame, add chain stays) → overview re-send.
  **2D CASCADE DONE 2026-09-07** — items (1)–(4) landed (SHELF_T 22→18, parts+costing reconciled, report + shelf/
  pinhole/weight diagrams regenerated, hardware firm-sourced). **3D DONE (verified 2026-09-28):** the `shelf()`
  builder was rebuilt to the ply-primary design (18mm board + spill lips + piano hinge + 2 SS chain stays, no
  steel frame) and is wired into overview / construction / electrical; the rebuild rode along in a later overview
  re-send. (NOTE 2026-09-30: several `.skp` are now stale again after the corner-zone/sump geometry changes —
  tracked in the *Stale `.skp` re-send batch* item above, not a shelf regression.)
  **Fab-detail sheets DONE 2026-09-07** (Sheets 4 board fab + 5 wall plates/schedule). Residual (only): datum/tolerance
  callouts (Phase C) if the shelf goes to a fabricator.
- [ ] **Walkway — RIGHT-walkway wall-cleat blank promotion (minor residual from Phase 1.2).** The wall-cleat
  blank (`_rwk_wall_cleat`: plate 90×8, shelf 90×55×10) is still a model-local literal; promote to
  `WALKWAY_CLEAT_*` constants if/when the cleat gets its own 1:1 cut sheet (the §10.5 plate schedule already
  lists it). *(The grate-clip pitch was resolved in Phase D — `WALKWAY_GRATE_CLIP_PITCH` = 610mm/24".)*
- [ ] **IBC frame — joint-mark naming (J1–J9) revisit (2026-08-18).** The bare `J#` joint
  marks read as opaque / hard to identify with. Consider human-descriptive marks for the IBC connection
  schedule — but it's cross-cutting (IBC report + drawings + parts + costing + master-shopping-list), so do
  it as its OWN IBC-blueprint task, keeping the schedule internally consistent. See
  [[feedback_joint_mark_must_label_diagram]].
- [~] **Water — sump-pickup rerouted AROUND the pinhole wall (2026-10-02).** `skid_plumbing()` Leg 1
  redone: riser up at X2386 → to the wall at deck level → vertical rise to Z230 (clears the Near-5/6
  cantilever wall-plates, top Z200) → +X along the wall to the P-04 climb; standard P-clips in the
  cantilever gaps, driven by one `wall_run_z` param. `water.skp` re-sent + Sketchfab-pushed; interference
  clean. Shared-builder cascade re-sent + Sketchfab-pushed + committed: **water · overview · ibc-stack ·
  construction** (all 4 that call `skid_plumbing()`). Stale Phase-1 prose reconciled in
  `water-system-report.md` + `processing-tray-and-spray-bar.md` §2.3 to the around-the-wall routing.
  **REMAINING:** (c) optionally revisit the BV-05 −150 nudge + the ACC-02→BV-05 hump-over now the suction
  no longer crosses the face.

## Scheduled
- [ ] **Source the genuinely-open parts rows** — the `parts-worklist.csv` default now carries only the
  actionable rows (identity / source-price); the bare **PRICE-VERIFY** sweep is **DEFERRED to near-
  fabrication** (2026-10-02 call: accept the current estimates, re-price everything closer to build —
  see the Bucket-1 re-price item + the `parts.py` reminder). Currently open: **1 IDENTIFY** (`pdh-washer`
  neoprene seal) + **4 SOURCE-PRICE** (`interior-ventilation`, `spray-retainer-clips`, `cooler-power-cable`,
  `water-powerpole`). The SKU↔supplier flags were false positives (Grainger SKUs share McMaster's format)
  and are resolved — the worklist now carries the lint's URL exemption.
  Workflow: `build_parts_worklist.py` → fill `parts-worklist.csv` (new_* cols, merges on re-run) →
  `apply_parts_csv.py parts-worklist.csv` → `parts.py --inject` + `costing.py --inject` + `lint.py`.
  **Near-fab re-price:** `build_parts_worklist.py --all` regenerates the full ~113-row price-verify sweep;
  fill at the owner's own cadence from logged-in supplier sessions.

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
