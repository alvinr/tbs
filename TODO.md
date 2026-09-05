<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
<!-- Working/internal tracker — NOT published (not registered in publish.sh). -->
# TODO & Actions — TBS-001

The **single record** of OUTSTANDING actions — open `[ ]` and in-progress `[~]` only.
Add new items as they arise; tick to `[x]` and delete once done (this file is pruned to
outstanding work, not a history log). Detailed sub-trackers are linked where the detail is extensive.

---

## ⏳ Light-trap parts-quote — pending Alvin research (2026-08-24)

- [~] **Brush + holder — KEEP AS-IS for now (2026-08-24, Alvin: "drive to completed blueprints, optimize cost later").** Leave `ll-wiper-brush` (#4 3/16″ est) + `ll-wiper-holder` (Tanis Al est) + the current drawing (Sheets 4/6/7) unchanged — the design is complete; only the price is an estimate. **Cost-optimization candidate for later:** Grainger 18A417 brush + 18A320 holder (confirmed 1/8″ backing pair, 3/4″/19mm trim; only in 10-packs → $270+$259 for a 4-need — expensive as-is; a by-the-foot source would cut it). If adopted later, re-spec the drawing/constants to 1/8″ backing/19mm trim → cascade Sheets 4/6/7/10.
- [~] **Edge channel — KEEP AS-IS for now** (same "optimize later" call). `ll-edge-channel` stays est; candidate = McMaster 9001K723 (6063 Al confirmed, 3/64″ wall, $18.18/8 ft) + 8× L-clips still to source.

---

## 🧩 Hinged panel — HDPE surround: cut sheets + drum join + frame connection (2026-08-27, Alvin) — SEEDS THE NEXT BLUEPRINT ROUND (hinged panel)

> Deferred out of the light-trap blueprint (merged/released). These are the starting scope for the **next**
> blueprint round: the **hinged panel** (`hingepanel-*`). Pick up here when that round begins.

- [ ] **HDPE surround cut sheets + drum-join detail.** The hinged panel's HDPE surround (the skin around
  the Ø800 light-trap housing) has no fabrication cut sheets yet. Draw them: the flat-pattern cut sheet(s)
  for the surround HDPE, AND the joint detail for how the **upper and lower floor** (the panel's top/bottom
  surfaces around the drum) **join to the outer drum housing** — the transition/seal where the surround
  meets the Ø800 housing at the top and bottom. Add to the hinged-panel drawing set + report; coordinate
  with the light-trap Sheet 2 (housing cut sheet) so the surround↔housing interface is single-sourced.
- [ ] **Resolve why the HDPE surround is not connected to the frame.** In the current hinged-panel model
  the HDPE surround reads as disconnected from the panel steel frame — establish the actual attachment
  (fasteners / bond / U-channel retainer / rivets) and either add it to the model + a detail, or document
  why it floats. Reconcile the 2D + 3D + report once resolved.

## 🛠 Tooling / infra

- [ ] **Label-overflow backlog — cross-generator `--overflow` sweep (2026-08-25).** New render-based
  `tidy_labels.py --overflow` (measures each label's bbox vs the axes frame; skips tiny insets) swept all 41
  generators clean (0 render errors) and found **49 genuinely off-frame labels** (one-sided ≥15%; ~163 sub-15%
  are tight-bbox noise, ignore). **DEFERRED until after the light-trap blueprint is done** (light-trap's own
  overflows are being fixed now, in-flight). Tackle the rest **one generator per tidy pass** (skill discipline —
  render → crop-zoom → verify), priority by count/severity:
  - **film_plane_mechanism** (10, worst +52%) — Sheet 9 section titles + U-joint/M6 leaders over-reaching left.
  - **weight_analysis** (9, +35%) — Sheet 1 "Total / CG" stats boxes hang off the BOTTOM (P8 notes placement).
  - **ibc_frame_drawing** (9, +19%) — Sheet 1 DATUMS + member-schedule table off left (P8).
  - **shelf_diagram** (3, +33%), **joint_study** (4, +19%), then walkway/electrical/tray_redesign/corner_gimbal/
    portrait_viz (1 ea, +15–26%).
  - **spray_bar Sheet 7 `"38×38×1.6mm 304-SS square"` +192% off left** — ANOMALY: anchored at a main-view coord
    (`CARRIAGE_YD_CENTER`) inside a section-panel axes with a different x-range, so it lands outside its panel.
    Look directly — likely a real placement bug, not a wide label.
  - Re-run `tidy_labels.py --overflow src/generators/generate_*.py` after each pass to confirm the list shrinks.
- [ ] **3D single-owner dedup pass (2026-08-18) — cleaned 12 of 17 cross-file duplicate emitters; 3 real
  drifts SURFACED, blocked on decisions.** Built the `lint.py` ratchet gate (no NEW cross-file duplicate
  emitter) and consolidated 4 clusters to a single owning builder each: **electrical** (em owns cable trunking
  [overview's full-length copy corrected to em's fitted extent], inverter box, master switch), **Fan B box**
  (lighttrap), **processing tray** (overview `processing_tray(alpha=)` — spraybar now shows the real sloped pan
  ghosted, not a flat copy), **walkway Far/Near** (wm `far_deck()`/`near_removable_deck()`). **REMAINING 3 real
  findings to resolve, then consolidate + remove from `_EMITTER_DUP_ALLOW`:**
  - **Fan B mount band / cargo-door panel thickness** — overview draws the door + band at `PANEL_CENTER_T=120`mm,
    lighttrap at **40**mm. Which door thickness is right? Unify the PANEL representation, then the band → lighttrap.
  - **Tray sump strainer foot position** — cp puts it at **Yd155** (center pickup), pw at **Yd104** (under the
    riser), 51mm apart + different color. Resolve the real sump-pickup Yd (+ pw riser routing), then → cp.
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

- [ ] **Reconcile ALL 3D builders — the models are partial VIEWS of ONE design, not alternatives (Alvin
  2026-08-17, HARD PRINCIPLE).** A design change must reflect in **every** model when they regenerate; the
  model must not drift. The GOOD pattern already exists — the IBC front bars are one shared builder
  (`generate_corridor_water_panel.py` `tote_restraint()`) that overview/ibc-stack/water all call, so the
  4-bar + cleat + M12×65 + hex-bolt changes flow to every model on regen. The DRIFT RISK is **dead/divergent
  re-implementations left lying around**. **PROGRESS 2026-08-17:** `ibc_rack()` (the OLD single-portal 2-bar+stub
  front-bar frame, X4734) was RELOCATED out of the live `generate_sketchup_model.py` into its sole consumer, the
  archived right-cantilever study — so the live module can no longer accidentally re-wire it (overview can't
  silently revert). **REMAINING:** audit every component drawn in >1 model and confirm each is ONE shared builder
  each model *selects* (its view), never a copy; wire a `check_consistency.py` gate that flags a second geometry
  emitter for the same named part.

- [ ] **`--solids` larger sanctioning pass (model-wide, beyond the named categories).** The
  `check_interference.py --solids` sanctioned list currently covers only the categories triaged in the
  walkway/IBC/light-trap/fan/tray work (one-piece formed parts, compression seals, bearing fits, liquid
  contents, seated connections). Run model-wide it still surfaces **~164 OPEN in the film-plane corner
  gimbal alone** (U-rail↔depth-rail, cross-slides, gibs, UHMW pads, trolley/U-joint) plus a few other
  mechanisms — mostly intentional one-piece/bolted/bearing overlaps that just aren't classified yet. To
  make `--solids` report globally clean: walk each mechanism, butt/notch the genuine fused-seam defects,
  and extend `_SANCTIONED_SOLID` with the rest (each with a reason). Larger effort; do per-mechanism.
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
  flagging. Run against the **overview** model (has all structural members) for the full list. (Alvin 2026-08-14.)

- [~] **Pipe-through-surface seam audit (3D readability) — same class as the beam fix above.** A pipe
  passing *through* a surface (plywood panel, wall, plate) shows NO seam/butt line — reads as fused into the
  panel. **TOOLING DONE (2026-08-16):** `check_interference.py --pipes` flags pipes whose centerline crosses
  the FULL thickness of a panel/wall/plate slab and emerges the far side. On the water model it finds 13
  penetrations: **pump-mount ply shirt** (suction entries + Cct-C power branches), **rear panel (18mm ply)**
  (DV merges, X-port drains, suction), **drain-riser backing spine**, **processing tray floor** (sump→P-04
  drain). **REMAINING — fix each:** either (a) draw a short collar/grommet ring at the face, or (b) split the
  pipe so each side butts it. Each fix = generator edit + re-send (single-writer). (Alvin 2026-08-15.)

## ⚡ Parts firm-up tracker — buckets by when they're actionable

### Bucket 1 — ACTIONABLE NOW
- [~] **Aug 2026 full re-price — SWEEP COMPLETE across all 6 systems (2026-08-01).** electrical / water / spray = 100% firm-priced; film / ibc-frame / shelf = material drivers firm, fab + bulk-steel deferred (rule below). Grand total settled **$25,874 / $30,346 / $36,874**. Notable moves: spray beam → single 16 ft 0.062in SS tube (no butt weld, sag-checked, −$394); corner L-plates $58.90 ea; U-joint boots, GHS labels, citric acid, pH buffers, zip ties, powerpole, blade fuses, ph-cal all firmed; wall-seat-saddle split into 8mm/10mm plate lines; bolt-m12x40 → 18-8 SS 92314A744. **Rule established** ([[feedback_material_now_fab_later]]): quote RAW MATERIAL now (the driver); defer fab (cut/bend/weld) to post-blueprint; bulk structural steel = steel-yard/freight quote, NOT online cut-to-size (which caps at 96in + overprices ~3×). **Deferred (owner-side, not blocked on me):**
  - **Fab quotes (post-blueprint):** film cross-slide assembly (¼in bar firm $134.73, + UHMW/gib/fab), the 2 wall-seat-saddle plate cuts + weld.
  - **Steel-yard bulk quotes:** `ibcf-rhs`/`ibcf-feet`/`ibcf-wall-backing` (2×2×⅛ A500 + A36 plate), `shelf-steel-shs` (1×1×⅛ A500 6 m). Estimates are realistic bulk figures.
  - **At-purchase confirms:** `shelf-folding-stays` + `shelf-transport-latch` (zinc chosen, estimates hold).
- [ ] **Master-BOM SKU backfill.** Branded rows that don't yet carry a registry `part_no` — Alvin's supplier paste-check; each SKU auto-appears in the master on the next `--inject`.
### Cost-reduction opportunities (grounding — analysis 2026-07-31)
Ranked by saving potential, analogous to the SS→ALU depth-rail switch (`fp-u-channel` $2,173→$328). Each
needs a dedicated follow-up to model + cascade before committing. Cost by system for context: chemistry
$5,466 · film $4,216–4,572 · container $2,300–4,300 · electrical $3,431–3,496 · water $3,370 · walkway
$1,979–2,825 · lightlock $2,046–2,516 · tray $1,583–2,271.
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
- [ ] **Front-bar J2/J7 joint — crush through the hollow bar (design review at quote time, Alvin 2026-08-17).**
  The J2 corridor cleat + J7 wall-end bolts run VERTICALLY through the 50mm HOLLOW 50×20×3 RHS bar (M12×65).
  Torquing a bolt through a hollow section pinches its two walls — resolve before fab: add an internal
  spacer/crush-sleeve at each bolt, OR grip only the cleat leg + the bar's bottom flange (short grip, which
  would restore M12×40). Decide with the fabricator when getting quotes; then reconcile the bolt length +
  spacer part back through Detail B / parts.py / the 3D. (SKU re-source is the separate Bucket-1 item.)
- [ ] **`pinhole-shim`** — Lenox SS-3/8-DISC laser-drilled pinhole; firm via RFQ once the optics drawing set is design-complete.

### Bucket 3 — ACTIONABLE ON BUILD
- [ ] **Container corrugation depth — PARKED pending physical measurement (EARLY procurement gate, post-blueprints).** The design side is CLOSED and robust to the unknown: `CONTAINER_CORRUGATION_DEPTH=30` (conservative max of the 25–30mm ISO side-wall range), the IBC wall-hangers use **M12×65 partial-thread** sized for the 42–54mm worst-case grip, and the BOM already carries **2 shim washers per bolt** (`91166A290`) to pad the grip if the real wall measures shallower. **Gate action (do FIRST, before ordering any wall fastener / bracket plate):** once the actual container is on site, **measure the real side-wall corrugation peak-to-valley**; if <30mm, confirm the shim count and whether M12×65 can drop to a shorter partial-thread length; apply **A36** to the final bracket-plate specs. No desk work possible — needs the physical container.
- [ ] **Walkway grating.** American Grating is primary (~$830 public list, banded $830–$1,050 for freight/cut); get the **firm cut quote + SoCal freight** at build. **McNichols is a FIRM SHIPPED fallback: 2× 48″×144″ @ $796.77 = $1,593.54 + $456 freight = $2,049.98 shipped (firm 2026-07-24)** — ~2× the American estimate, and its 4′×12′ sheet would re-nest the cut plan if chosen.
- [ ] **Container** — `container-20ft` (±$1,500) + `container-delivery` (±$500), firm at purchase.
- [ ] **Fab estimates.** All `*-fabrication` lines (`tray-fabrication`, `ll-fabrication`, `ibcf-fabrication`, `sp-door-fab`) + `tray-ss-sheet`, the film-plane fab (skate carriage, 304 cross-slides, cam clamp), and the `sp-pivot-post` collar — quote to shops once the drawing set ships. ≈±$1,500.
- [ ] **Buy the film-plane U-joints (`fp-ujoint`).** Belden **SSNBUJ750x3/8KB** (Grainger **41D816**) — needle-bearing, 3/8" keyway + set screw, stainless, 45°, factory-booted. **$252.13 ea × 4 = $1,008.52**, + 8× 3/32×3/64 SS machine keys (`fp-ujoint-key`, ~$6–10 lot) + keyseat the 3/8" stubs. Firm-priced (2026-08-13); purchase at build. **Confirm the set-screw torque spec with Belden/Grainger** (datasheet gives static breaking 95 in-lb only). Supersedes the retired plain UJ-SS750x375 + separate 806VF1 boot.
- [ ] **IBC flex-connection `s60-reducer` interface (bench).** The sourced reducer (Charlotte `PVC021071300HD`, 2"×1" Sch-40) is **spigot×slip (solvent-weld)**, but the tote adapter (Granatan S60→2") outputs **2" MALE NPT** — a spigot×slip bushing is glue-only, so it needs a **2" MPT×socket transition** to mate (or swap to a **2"FNPT×1" reducer**). Verify/resolve the tote-adapter interface at the bench. (Alvin 2026-07-29.)
- [ ] **IBC flex-connection clamp size (bench).** `ibc-flex-clamp` is an Apollo **#12** (½"–1¼", `IDL0410PK`). The flex hose is cut from the 1"-ID / **1¼"-OD** tray-suction coil, so over a barb the OD approaches/*exceeds* the #12's 1¼" max — **verify the #12 closes and seals; step up to #16 if it bottoms out.** (Alvin 2026-07-29.)

---

## ★ MAJOR MILESTONE — manufacturing-ready blueprints (ALL drawing sets) — OPEN

_Alvin's call (2026-07-16): the current 2D sets are arrangement-faithful schematics (true-proportion +
topologically correct, reconciled to the 3D) but NOT manufacturing blueprints. The milestone is a
**definitive, dimensionally-correct, shippable-to-a-fabricator drawing package for EVERY subsystem** —
precise hole positions, tolerances, fastener callouts, datums, section views, material/finish, driven
parametrically from `tbs_constants` so they can't drift. Do the **film-plane corner mechanism FIRST** (below)
as the template, then roll the same standard out across all sets (film plane, water/tray/spray, IBC frame,
walkway, hinged panel, light lock, electrical, optics, …)._

- [~] **★ FINAL cross-cutting step — fastener standardization (INVENTORIED + DECIDED 2026-09-04; branch `fastener-rework`).** Full inventory + the 6-family decisions are captured in **`fastener-standardization.md`** (target: metric families 6→4 — M5 + M10 eliminated; lengths ~12→~7). **Done now:** M6 nuts 3→2 (plain→nyloc merge). **Gated on the owning blueprint (do at each sheet round, standardize against the final set):**
  - **M12** — force wall joints to one length (grip-stack standardization, Lever B) + keep ×100 for J6 + unify ×65 zinc/SS → *IBC-frame + walkway*.
  - **M10 → M12** — eliminate the family (cap-hub / ring-collar / door-frame bolts bump to M12); verify M12 edge-distance on the 8mm cap at Ø120 PCD → *light-trap + hinged-panel*.
  - **M8** — zinc ×25 standard, SS exception = wet film-plane (carriage + ICP-14 rail-fixing); confirm edge-channel/carriage land on ×25 → *film-plane*.
  - **M5 → M6×16 CSK** — retire the family (new CSK SKU); verify clamp-clip head clearance → *film-plane* (next round).
  - **M4** — itemize + keep (cam-clamp base vendor-fixed M4; pinhole grubs precision).
  - **Related:** ⁵⁄₁₆″→¼″ ply-mount (filter housings), #14 self-drillers 4→2, ⅛″ rivets 2 grips→1.
  - **BOM-gap itemization** (M4 grubs, M4 cam-mounts, M12 pivot anchors/hinge brackets) — each blocked on a length dim; itemize per the owning sheet, don't assume.

- [ ] **Light-lock blueprint pass — consider the drum lock mechanism on the FAR side, not the near side
  (Alvin 2026-08-18).** When we do the light-trap/light-lock blueprint, evaluate moving the revolving-drum
  lock mechanism to the far side of the drum so the near-side gap stays clear for operator egress through it.
  (Surfaced during the egress review that retired the swing-out floorplan sheet.)
- [ ] **Walkway — RIGHT-walkway wall-cleat blank promotion (minor residual from Phase 1.2).** The wall-cleat
  blank (`_rwk_wall_cleat`: plate 90×8, shelf 90×55×10) is still a model-local literal; promote to
  `WALKWAY_CLEAT_*` constants if/when the cleat gets its own 1:1 cut sheet (the §10.5 plate schedule already
  lists it). *(The grate-clip pitch was resolved in Phase D — `WALKWAY_GRATE_CLIP_PITCH` = 610mm/24".)*
- [ ] **IBC frame — joint-mark naming (J1–J9) revisit (Alvin 2026-08-18).** Alvin finds the bare `J#` joint
  marks opaque / doesn't identify with them. Consider human-descriptive marks for the IBC connection
  schedule — but it's cross-cutting (IBC report + drawings + parts + costing + master-shopping-list), so do
  it as its OWN IBC-blueprint task, keeping the schedule internally consistent. See
  [[feedback_joint_mark_must_label_diagram]].
- [ ] **Water — PRE-EXISTING under-corridor plumbing clashes (surfaced during the walkway F1 water re-route,
  Alvin 2026-08-18; NOT caused by the walkway work).** Two clash groups that predate F1 — the J6 plate (IBC
  upright X4654), the IBC frame rail, and the corridor routing didn't move at F1: (1) **P-02→ACC-02 recycle ×
  RWk J6 arm end-plate** — the recycle's corridor turn at Yd1110 (`RWK_RIBBON_NOTCH_YDS[0]`) clips the arm plate
  at X4646-4654; (2) **several lines (blue trunk · DV-02 waste · P-02 recycle · SV-01) × the IBC corridor frame
  rail** (X4663-4900, Yd1132-1279). Reroute/notch in a focused plumbing pass (plumbing skill). The F1-CAUSED
  clashes are already fixed: #1 ribbon-lane×outer-beam (RIBBON_LANE_X derived from the channel), #2 end-beam×
  near-corner-risers (near RWk end beam un-inset to Yd0).

## Film-plane report reconciliation (leadscrew Option A → U-channel redesign) — PROSE DONE, BOM GATED

_Surfaced 2026-07-16 during the frame material fix. Prose reconciled 2026-07-17 (commit 47d87d10).
The remaining §7 parts BOM is gated on confirmed prices._

- [~] `film-plane-mechanism-analysis.md` — scope note fixed (stops claiming it describes the built
  mechanism; optics §3/§5/§6 affirmed; hardware/BOM → report). **STILL OPEN (task #30):** the §4
  mechanism + §7 BOM + §8 maintenance are a leadscrew decision-record snapshot — DECIDE keep-collapse-
  to-optics-only vs **retire** (it's nav-labeled "(superseded)" and its optics overlap distortion-renders).
- [ ] **Hinge-panel blueprint — swing-panel transport-lock STAY plate detail (Alvin 2026-08-17).** The top +
  bottom wall stays that lock the swung panel at 56° attach to a **plate paired with an exterior plate on the
  OUTSIDE of the container wall** (same interior+exterior backing-plate pattern as the container-wall
  cantilevers / the IBC wall hangers). Design it in the hinge-panel blueprint pass: plate sizes, through-bolt
  pattern, and add the geometry to the 3D (currently the stays/plates are NOT modeled — a 2D↔3D gap like the
  bar cleat was). Reference the existing paired-plate detail. (Alvin also flagged some square-bolt heads in the
  overview near here — confirm which and hex them if they're fasteners.)
- [ ] **Reconcile the EPDM gasket on the cargo-door-facing wall of the hinge panel.** Now that the top/bottom door seals are strip brushes, re-check the panel perimeter / housing-surround EPDM on the cargo-door-facing (exterior) wall of the hinge panel — confirm what stays EPDM vs brush and that the 3D/report/parts agree. (Alvin 2026-07-19.)
- [ ] **Revisit film-plane EPDM foam-tape coverage.** Qty set **provisionally to 2× 25 ft rolls** (McMaster 8694K88, 50 ft) — right-sized to the ~43 ft film-plane perimeter (the old 3×50 ft = 150 ft was ~3.5× over). When reviewing the EPDM seals, confirm a single perimeter run + corner/overlap allowance is covered by 50 ft, else bump to 3 rolls. `parts.py` `epdm-foam-tape` carries a "provisional qty" note. (2026-07-21.)

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
