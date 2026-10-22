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

- [x] **Finish the left-rail-move (260) stale-value cleanup (2026-10 fab-tolerance sweep).** *DONE 2026-10-21.* Fixed the 3 named items — (a) the superseded bearer-beam/3-floor-leg comment block in `tbs_constants.py` rewritten to the current 5-floor-leg-cantilever design; (b) the drum-exit punch-out comment re-derived to the current values (reach 880 / 600mm punch-out over Yd 800–1560); (c) the spray-manifold end-X in `processing-tray-and-spray-bar.md` → the beam ends X=310 / X=4,599. Also swept the broader residue `check_consistency` CHECK A surfaced: `generate_walkway_diagram.py` (retired edge-beam header block → current cantilever; visible "TRAY RIM"/"FLOOR-LEG…" labels and `X=170/470/770/140` → `280/580/880/250`; stale inline `# NNN` comments), `generate_spray_bar_diagram.py` + `generate_floorplan_diagram.py` comments, and the stale `LEFT_WK_CANT_FOOT_X0 ≈147` comment (→110). Drawings were already correct (constant-driven); only comments + rendered labels were stale. *Left (ambiguous — not clearly left-rail residue): the Sheet-4 butt-joint "full-width edge beam (X=470)" + "X=470 bearer (Detail E)" refs, and walkway-report §post "sub-plate at X=140mm" (likely the sub-plate centre 0–280, i.e. current) — verify against the near/butt-joint geometry before touching.*
- [x] **Remove the 23 reserved/unused fab-part constants (2026-10 fab-tolerance audit).** *DONE 2026-10-21.* Audited all 23: **17 DROPPED** (genuinely dead — `CORNER_PLATE_BEND_R` already gone; plus `UJOINT_HUB_L`, `UJOINT_BOOT_LEN`, `CAM_CLAMP_BASE_W/D`, `CAM_CLAMP_HOLE_SP`, `CAM_CLAMP_N`, `BRACE_T`, `EP_RISE_X_P`, and five redundant aliases of still-used constants: `RWK_HL`→`RWK_HL_TIP`, `SPRAY_BAR_HOLE_SP`→`SPRAY_BAR_NOZZLE_PITCH`, `SPRAY_BAR_BORE`, `SPRAY_BAR_HOLE_DIA`, `LT_EDGE_CHAN_N/RIVET_PITCH/END_BOLT/T/W`→`LT_HBAR_*`). **6 were CHECK-E false positives** — actually consumed by the facts-injection system (`EVAP_CFM_RATED`, `IBC_CEILING_CLEARANCE_MM`, `BLUE_SUPPLY_GAL`, `COLLECTION_FILL_L`, `LOST_L` via `facts.yml constant:` refs) or the dependency-map injector (`XSLIDE_N` via `cdm:`); their `# reserved` annotation was removed (and the stale `# = 630/434` comments on `COLLECTION_FILL_L`/`LOST_L` fixed to the computed 622/465). **CHECK E was taught** to scan `facts.yml` + `component-dependency-map.md` so facts/cdm-wired constants are no longer mis-flagged. CHECK E now reports 0 dead.
- [x] **Tolerance/datum blocks — DONE 2026-10-14. Every tolerance/note block now renders via `draw_notes`.**
  Swept the hand-rolled `fig.add_axes` + `Rectangle` + text-loop pattern onto `tbs_drawing.draw_notes` (bold
  first-line title + bordered box): `generate_shelf_diagram.py` (`_tol_block`), `generate_pinhole_disc_holder.py`
  (`_tol_block`, PDH sheet 3), and `generate_electrical_diagram.py` (the power-box notes block, sheet 9). All
  output-equivalent (verified visually). **`generate_ibc_frame_drawing.py` was already compliant** — its
  `_datum_tol_block` already called `draw_notes` (the TODO over-listed it from a text-match). Gotcha captured for
  the future: `draw_notes` `pad_x`/`pad_y` default to `spacing`, which bleeds the border left of a fig-coord rect
  — pass small explicit pads (see the shelf/PDH fixes).
- [x] **Audit every sheet's page size — DONE 2026-10-14 (two passes).** Prompted by shelf-sheet4, where an
  `aspect="equal"` data axes was narrower than the figure, so a figure-coord block floated in the right margin
  *beyond* the title block. Fix pattern: size `figsize` so its aspect ≈ the data aspect (`xrange/yrange`) → the
  data axes fills the width → the title block (drawn on `ax`) spans the whole page; keep side blocks in **data**
  coords.
  - **Pass 1 (horizontal):** a harness ran every generator with `Figure.savefig` patched to compare each sheet's
    widest axes against the content x-union. 4 flags, all false positives (pinhole-panel, PDH sheet3/4 — title
    block on a dedicated full-width axes; film-joint-options — concept diagram, no title block). Shelf already fixed.
  - **Pass 2 (vertical — added after this pass MISSED a real one):** the horizontal check did **not** catch
    `electrical-sheet5`, where the true-scale panel elevation (BAT 1 bottoms at `BA_H_LO`=160) ran **into** the
    title block (bottom 7% of `ylim`). Found by eye, fixed (dropped the ylim floor). Then patched `title_block`
    to flag content dipping into the bottom title-block band: re-ran the whole set → electrical-sheet5 clears, plus
    4 **floor-background false positives** (lighttrap-sheet1, walkway-sections 3/4/5 — a ground/floor fill reaches
    the band but the white-filled title block sits cleanly below it; verified sheet3 + lighttrap by eye).
  - Canvas-edge clipping stays covered by `tidy_labels --overflow` (0.16 = zero genuine clips). No other sheet needs
    a page-size change. (Lesson: a title-block overlap can be **vertical** — content dropping into the band — not
    just a horizontal float.)
- [~] **Model-aggregation — Phases 0–3 DONE** (overview is now a thin aggregator; full history in [`model-aggregation-plan.md`](model-aggregation-plan.md)). Phase 3 (2026-10-10) added the `lint.py` ratchet gate `gate_overview_aggregation` locking overview to its sanctioned builder set, so it can never silently re-grow an owned builder and drift from its sub-model. **Remaining (optional polish, not blocking):** the two orphans `shelf` + `light_seal` are allowlisted as accepted (no sub-model home) — if a `context`/furniture owner is created, move them there and drop the allowlist entries (the ratchet flags the stale entries to keep the move honest).
- [x] **Label-overflow sweep — RESOLVED 2026-10-10.** The old `--overflow` measured each label vs its
  **axes data-box**, which over-reported badly: ~136 flags, but with `bbox_inches="tight"` (the house convention
  on most sheets) the canvas expands to include any margin label, so nearly all were deliberate margin captions
  that render fine. **Fixed the check to measure against the FIGURE CANVAS edge** (the real clip boundary) and
  skip tight saves entirely — the only save that can cut a label. Genuine clips found + fixed: **ibc_frame Sheet 1**
  (cut-list + datum/tolerance blocks off a full-bleed axis → widened the margin), **tray_slope + grp_cutplan**
  (edge scale/coordinate labels → gave the saves `bbox_inches="tight"`). Diagram set now reports **zero genuine
  canvas clips**. Remaining `--overflow` output is CROWDED advisories only (title-block labels deliberately close;
  bbox-whitespace over-reporting on multi-line labels — confirm on crop-zoom, not gating).
  - ✅ **spray_bar Sheet 7 `+192%` off-left FIXED (2026-09-28)** — it was a hidden DUPLICATE beam-section label
    on the nozzle panel; dropped it (beam is called out on ax_cf + dimensioned on ax_nz).
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
  - **(2026-10-09) within-file dedup** — the film-plane captured-skate carriage (rollers/axles/keepers/carriage
    plate/retainer bolts/cam-brake) was duplicated between `corner()` (install) and the `movement()` demo; the
    demo copy had drifted (missing the axles/keepers/brake). Extracted to `corner_skate_parts()`, now shared by
    both — `corner()` output byte-identical, Movement scene completed.

- [x] **`check_interference.py --bolts` — orientation/grip lint — DONE 2026-10-22.** The read-only pass flags
  every structural grip bolt EDGE (< 1.5·D to a member edge), FLOATING (pierces nothing), or PROJECT (shank past
  the grip). **Wired as a ratchet:** `--write` now appends the `--bolts` section to the committed
  `interference-report.txt`; a `_SANCTIONED_BOLT` baseline tags each flag `[OK <reason>]` or `[OPEN]`; and a
  `lint.py` advisory warns on any `[OPEN]`. Re-triaged against the live overview model (the 2026-08-17 list was
  stale — RWk J6 is already fixed at `RWK_J6_EP_H=190`): all 24 current flags are benign (fastener-type /
  precision-mechanism / non-structural-edge-member / drawn-D / AABB artifacts) and sanctioned with reasons; 0
  OPEN. **Deferred (nice-to-have, not blocking):** a `bolted_joint()` emitter so orientation is
  correct-by-construction (tracked in `skills/skill_fastener_convention.md`).

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
- [x] **Aug 2026 full re-price — SWEEP COMPLETE across all 6 systems (2026-08-01); CLOSED 2026-10-07.** The re-price is done: every system is firm-priced on its material drivers, prices were re-verified on each part touched through the autumn design work (lighting, conduit clips, fan-B/evap reconciliations), and the only remaining items are the **deliberate firm-at-build deferrals** below (fab quotes, steel-yard bulk, at-purchase confirms) — by the material-now/fab-later rule those are not open work, they firm at order. electrical / water / spray = 100% firm-priced; film / ibc-frame / shelf = material drivers firm, fab + bulk-steel deferred (rule below). Grand total settled **$25,874 / $30,346 / $36,874**. Notable moves: spray beam → single 16 ft 0.062in SS tube (no butt weld, sag-checked, −$394); corner L-plates $58.90 ea; U-joint boots, GHS labels, citric acid, pH buffers, zip ties, powerpole, blade fuses, ph-cal all firmed; wall-seat-saddle split into 8mm/10mm plate lines; bolt-m12x40 → 18-8 SS 92314A744. **Rule established** ([[feedback_material_now_fab_later]]): quote RAW MATERIAL now (the driver); defer fab (cut/bend/weld) to post-blueprint; bulk structural steel = steel-yard/freight quote, NOT online cut-to-size (which caps at 96in + overprices ~3×). **Deferred (owner-side, not blocked on me):**
  - **Fab quotes (post-blueprint):** film cross-slide assembly (¼in bar firm $134.73, + UHMW/gib/fab), the 2 wall-seat-saddle plate cuts + weld.
  - **Steel-yard bulk quotes:** `ibcf-rhs`/`ibcf-feet`/`ibcf-wall-backing` (2×2×⅛ A500 + A36 plate), `shelf-steel-shs` (1×1×⅛ A500 6 m). Estimates are realistic bulk figures.
  - **At-purchase confirms:** `shelf-folding-stays` + `shelf-transport-latch` (zinc chosen, estimates hold).
- [ ] **Master-BOM SKU backfill.** Branded rows that don't yet carry a registry `part_no` — the supplier paste-check; each SKU auto-appears in the master on the next `--inject`.
### Cost-reduction opportunities (grounding — analysis 2026-07-31)
Ranked by saving potential, analogous to the SS→ALU depth-rail switch (`fp-u-channel` $2,173→$328). Each
needs a dedicated follow-up to model + cascade before committing. Cost by system for context: chemistry
$5,466 · film $4,216–4,572 · container $2,300–4,300 · electrical $3,431–3,496 · water $3,370 · walkway
$1,979–2,825 · lightlock $2,046–2,516 · tray $1,583–2,271.
- The top-ranked lever — **ferric ammonium oxalate** ($4,026) — is a *sourcing* move (bulk supplier /
  trim the rich coat tier), not a design change, so it has **no design-phase impact → deferred to Bucket 3
  (construction)**, 2026-10-14. The remaining desk-doable levers here are all material swaps already captured
  above or in Bucket 2.

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
  - ~~**Tilt-swing board** fastener itemization~~ — **CLOSED (moot): the tilt-swing mechanism was RETIRED
    2026-09-21** (optically inert) and replaced by the pinhole disc holder; its off-registry fasteners
    (M8×1.0×80 / M12×45 / M16×55 / M6 set screws / dowels) went with it. The successor's fasteners — 4× M6
    mount bolts + 4× M6 thumb screws — are already itemized in `parts.py` (`front-board` system) and carry
    firm SKUs. See `fastener-standardization.md` §Front board.
  - ~~**M5 → flange bolt + nyloc**~~ — **CLOSED (superseded):** the chem-shelf ply-primary redesign retired M5
    by moving the ply attachment to **¼-20 pronged tee-nuts** (not a flange-bolt fold) — the flange-bolt
    prediction was overtaken. No M5 remains anywhere. Chem-shelf blueprint is fab-complete (datum/tolerance
    block added 2026-10-14). See `chem-shelf-blueprint-spec.md` + `fastener-standardization.md` §M5.
  - **Filter bracket 244718 — confirm URL + price** (switched to the bracket-only Pentair 244718; $10.50 kit price held as a conservative placeholder, `filter-skid-frame`).
- [ ] **`pinhole-shim`** — Lenox SS-3/8-DISC laser-drilled pinhole; firm via RFQ once the optics drawing set is design-complete.

### Bucket 3 — ACTIONABLE ON BUILD
- [ ] **Ferric ammonium oxalate — chemistry sourcing lever, DEFERRED to construction (2026-10-14).** $4,026, the
  biggest single line (`amfe-rich/standard/lean` = $2,196+$1,098+$732 @ $64.20/kg; plus `ferri-rich` potassium
  ferricyanide $582). It's a **sourcing** lever — bulk/cheaper supplier, or trim the *rich* coat tier (even 15% ≈
  $600) — NOT a material swap or a design change, so it has no bearing on the design phase. Run the chemistry
  sourcing pass at order/construction time, then cascade through `parts.py` → `costing.py`.
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

**► Blueprint-readiness audit — ALL systems reviewed 2026-10-10 (7-way parallel).** Result: **6 of 7 subsystems are manufacturing-ready blueprints; water/tray/spray is the one genuine gap.**
- ✅ **Film-plane** (template) — fab Sheets 13–18 fab-grade, datum/tol scheme Sheet 9, fastener schedule Sheet 12. Polish: sparse explicit hole-Ø drill callouts; rail/saddle (13/18) outside the Sheet-9 tol block.
- ✅ **IBC frame + plate schedule** — cut list, datums/tol, weld map+schedule, 1:1 plate details, fully-dimensioned cantilever arm. Stacking set = GA (correct). J1 mark on Sheet 1. **DONE 2026-10-12:** floor anchoring adopted the **sub-plate (strongback) standard** — feet/legs bolt to a shared steel plate self-tapped into the cross-members (container cross-members aren't standardized; ISO 1496-1). J1→J1a/J1b (IBC) + WF4→WF4a/WF4b (walkway) across §3.4a/§5.1a + parts/costing + blueprint-specs + the new `floor-anchor-map` 2-sheet diagram; cost cascaded.
- [ ] **Floor-anchor sub-plates — finalize on the ACQUIRED container.** Plate dimensions, members spanned, and TEK count are container-dependent (§3.4a / §5.1a): on receipt, survey the cross-member stations + door-end sill + any forklift pockets, then cut each plate and drill its on-site TEK clearance holes to the surveyed steel. (IBC ~650×450×8; walkway ~1900×350×8 continuous — both representative.)
- ✅ **3D models — floor-anchor sub-plate + shortened post (`FLOOR_PLATE_T`).** DONE 2026-10-12: `cp.frame()` + `walkway_model` carry the sub-plate (under the IBC feet + the continuous walkway sill→tray plate), feet/legs raised onto it, posts cut shorter by the plate thickness (frame top fixed), J6 backing-plate follows the raised ring. All **6 models re-sent → saved → pushed to Sketchfab → committed** (overview, walkway, ibc-stack, water, film-plane-mechanism, construction); `manifest.py --check` = all 11 current; `check_interference` = 0. (Residual `check_consistency` "FLOOR_PLATE_T only in 2D" on the ibc-frame pairing is the pre-existing shared-`cp.frame()`-module heuristic artifact, same as `IBC_FOOT_PLATE_T`/`IBC_FRAME_RHS`.)
- ✅ **Winged-TEK SKU URL backfill — DONE 2026-10-12.** `ibcf-floor-tek` + `walkway-floor-tek` (`F14C325FDC`, #14×3¼″ winged self-driller) now carry the Fasteners Plus product URL; parts-identity lint advisory cleared.
- ✅ **Walkway** — datums/tol box, plate schedule, per-bracket fab sheets, WF/WW weld marks. Sheet 3 cantilever plan leans on the cut-list/plate schedule (within GA convention). **Fix:** `walkway_sections` title blocks read "SHEET N OF 5" on sheets 1–5 but the set has 6 sheets → "OF 6".
- ✅ **Hinged panel + light lock** — both fab-grade; lighttrap carries true machine fits (H7/h6, DIN circlip/retaining grooves, datums). Hingepanel has no general-tol note block (acceptable — its only precision joint is COTS bearing/bushing); welds are glyph+prose not AWS symbols (house style).
- ✅ **Electrical** — install-ready: circuit IDs, AWG, OCPD ratings, device + fuse schedule, true-scale panel, fabricated power-box fully dimensioned (Sheets 8–9). Optional: conductor-ampacity column.
- ✅ **Optics/pinhole + chem-shelf** — PDH disc/holder fab-complete (CNC tol block, Ø82 H7 seat holds the optical axis); pinhole-wall elevation = GA (correct); chem-shelf fab-complete. Polish: PDH plate/disc thickness only in captions (no edge dim); 6061 carrier central bore Ø undimensioned; PDH Sheet 2 scale-note mislabel ("1:3" vs ~1:1.15); typo "Conatiner" in pinhole-wall.
- [x] **Water / tray / spray — GAP CLOSED 2026-10-10.** Added the three missing fully-dimensioned, monochrome, datum/tolerance-carrying fab sheets to `generate_spray_bar_diagram.py` (now 11 sheets): **Sheet 9** spray-beam + manifold full-length station layout (cut length 4,289, 43 nozzle stations @100mm, 7 feed-tees @550, carriage-clamp + ball-joint stations, Section A-A; correctly shows NO beam-wall drilling — the saddle-tees tap the external LDPE manifold), **Sheet 10** wheel-carriage plate (280×60×5 6061-T6, notch + 12-hole drilling, 2 req), **Sheet 11** processing-tray pan (304 SS 1.5mm, 2-panel 2,195×2,200, 50mm rim fold, pressed 180×100×20 sump, 12× M6×16 seam pattern, PLAN + exaggerated SECTION). Embedded in the report; registered everywhere; all gates green. Also **reconciled the 2026-08-11 cascade miss** that this exposed: the prose/parts "44 nozzles → 43", "4,399 → 4,289mm span", "2,175 → 2,195mm panel", sump "150 → 180mm", plus the stale `tbs_constants` inline comments. **Residual (COTS-pending, flagged in-code):** the carriage saddle-bolt + clamp-bolt spacings (Sheet 10) are chosen values — confirm vs the Boxonly saddle clamp catalog at order. **3D nozzle-span note — RESOLVED 2026-10-10 (no re-send):** `generate_spraybar_model.py` referenced `PROC_OPEN_X_L..R` for the nozzle span with a "stay in the open zone" comment, implying a 3D-vs-2D drift. Investigated: the open zone (580–4329) and the full beam (310–4599) are **concentric** (both centered on the film-plane center 2454.5), so the symmetric centering formula places the 43 nozzles at the **identical** stations (354.5…4554.5) either way — exactly matching 2D Sheet 9. Changed the span reference to the beam ends (`NXL,NXR = XL,XR`) + fixed the comment so the code intent matches the 2D; `manifest --check` confirms the `.rb` hash is unchanged (byte-identical geometry), so no `.skp` re-send / Sketchfab push was required.

- [~] **★ FINAL cross-cutting step — fastener standardization (LARGELY EXECUTED 2026-09-07, branch `part-reconcile`).** Full status + rationale live in **`fastener-standardization.md`** (target revised to metric families **6→5** — M5 retires, M10 KEPT). **Done this pass:** IBC J2/J7 spec reconciled to M12×65; M8 washer text/key/duty; **M12 wall bolts unified to one zinc length (×70)**; **5/16→1/4 ply-mount** (5/16 family retired); **#14 TEK unified** (90822A620); **optical-plate M12×40 itemized + socket→hex**; **TSB central M16→M8×1.0**. **Reversed on evidence:** M10 KEPT (thin light-trap hosts preclude M12 CSK); ⅛″ rivet consolidation INFEASIBLE (no grip spans both laps). **Remaining:**
  - ~~**M5 → flange bolt + nyloc**~~ — **CLOSED (superseded):** the chem-shelf retired M5 via ¼-20 pronged tee-nuts, not a flange-bolt fold (prediction overtaken); no M5 remains. Chem-shelf fab-complete (tol block added 2026-10-14).
  - ~~**TSB registry merge** / **tilt-swing A4/316→304 downgrades**~~ — **CLOSED (moot):** both were gated on a
    "TSB blueprint review" that no longer exists — the tilt-swing board was **RETIRED 2026-09-21**. The successor
    pinhole-disc-holder fasteners are already in the `parts.py` `front-board` system (4× M6 mount + 4× M6 thumb
    screws, firm SKUs); no registry merge or material downgrade is outstanding.
  - **BOM-gap itemization** (M4 grubs, M4 cam-mounts, M12 pivot anchors/hinge brackets) — each blocked on a length dim; itemize per the owning sheet, don't assume.
  - **#14 TEK washer + M8×1.0×50 central SKUs** — SKU-pending items to firm at order.

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
  `apply_parts_csv.py src/generators/parts-worklist.csv` → `parts.py --inject` + `costing.py --inject` + `lint.py`.
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
