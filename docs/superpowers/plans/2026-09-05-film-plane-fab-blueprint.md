<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Film-Plane Fabrication Blueprint Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Elevate the film-plane drawing set from mechanism-design level to a shop-buildable fabrication blueprint by adding 9 one-part-per-sheet detail drawings (Sheets 12–20), reconciling the existing 11 sheets, and clearing the open audit flags.

**Architecture:** Extend the single existing generator `src/generators/generate_film_plane_mechanism.py` with new `sheet12()`–`sheet20()` functions (continuous numbering, shared helpers, one `dependencies.yml` output group). Every sheet is drawn purely from `tbs_constants.py`, verified against the live `film-plane-mechanism.skp`, and label-tidied. No mechanism redesign; a geometry change only happens if interference triage forces one, via the normal constant→cascade→send path with Alvin's sign-off.

**Tech Stack:** Python 3, matplotlib (Agg), the repo's `tbs_drawing`/`tbs_title_block` helpers, `tbs_constants.py` single-source constants; verification via `lint.py`, `check_consistency.py`, `check_interference.py`, `tidy_labels.py`, `parts.py`, `costing.py`, and read-only SketchUp `eval_ruby`.

**Spec:** `docs/superpowers/specs/2026-09-05-film-plane-fab-blueprint-design.md`

## Global Constraints

Copied verbatim from the spec + CLAUDE.md; every task's requirements implicitly include these.

- **Draw from constants, never literals.** No numeric literal in a label string — reference the constant (`f"{RAIL_LEN}mm"`, not `"2200mm"`). Enforced by the `lint.py` "hardwired literal in staged file" check.
- **Every `draw_dim_*` label carries an explicit `mm`** (f-string and literal alike).
- **American English spelling** throughout (center, color, aluminum, analyze).
- **License header** (`# SPDX-License-Identifier: AGPL-3.0-only` / `# © 2026 Alvin Richards`) on every tracked `.py`/`.md`. The generator already has it; new `.md` need it.
- **Fasteners** follow `skills/skill_fastener_convention.md`: any fastener into a hollow wall engages the inner/bore-side edge and aligns with the metal thickness; use the `ruby_bolt`/`draw_bolt` sign convention; respect edge-distance/grip.
- **`.skp` is single-writer** — never `--send`/save the model without a verified doc match; **Alvin is the sole saver + Sketchfab uploader**; commit the `.skp` only after he confirms "saved + uploaded".
- **Drive every regen/re-send from `lint.py --cascade <CONST>`**, never grep or memory.
- **Commit source as work lands** (per-sheet), do not batch behind the `.skp`.
- **`git add` explicit paths only** — never `-A`/globs.
- **Gate suite (all green before every commit):** the pre-commit hook runs `lint.py`. Before the phase-closing commits also run `check_consistency.py`, `check_interference.py --bolts`, `tidy_labels.py`, `parts.py --check`, `costing.py --check-registry`, and the gallery `comm` audit.

## The Standard Sheet Build Cycle

Tasks 2–10 each draw ONE new sheet. The unique *drawing content* is spelled out per task; the mechanical build/verify cycle below is identical for each and is referenced (not repeated) in those tasks. This is a deliberate adaptation for diagram work: a sheet's "implementation" is ~100–200 lines of iterative matplotlib best written by modeling on a named existing sibling function, then judged visually — not reproducible as literal source in a plan. Each new sheet function models on the cited sibling sheet in the same file.

1. **Add constant imports** the sheet needs to the top-of-file `from tbs_constants import (...)` blocks (only ones not already imported).
2. **Write the `sheetN()` function**, modeled on the cited sibling (same figure/axes setup, `title_block(ax_tb, "SHEET N OF 20", drawing_title="MOVEABLE FILM PLANE", ...)`, `reset_label_registry()` at entry, `fig.savefig(f"{DIAGRAMS_DIR}/film-plane-sheetN.png", dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)` + the `print(f"  → …")`). Draw the views/dims/callouts in that task's spec.
3. **Add `sheetN()` to the `__main__` dispatch** in numeric position.
4. **Render:** `/usr/bin/python3 src/generators/generate_film_plane_mechanism.py` (matplotlib needs `/usr/bin/python3`) — confirm the new PNG writes and the run ends "Done." with no traceback.
5. **Tidy labels** (arg is the GENERATOR, not the PNG): `/usr/bin/python3 src/generators/tidy_labels.py --fix src/generators/generate_film_plane_mechanism.py` (static), then `--overflow <generator>` (mechanical off-frame/collision), regenerate, then a crop-zoom visual pass per `skills/skill_tidy_labels.md`. Per the accuracy/speed tradeoff: run `--fix` + `--overflow` reliably, fix real defects on one crop pass, don't pixel-peep. `git checkout -- diagrams/` any PNG this rewrote that this task didn't intend to change.
6. **Verify vs 3D (read-only):** the live `film-plane-mechanism` model is open — query the matching component's bounds/positions via `eval_ruby` and confirm the sheet's key dims match. If the live doc is ever NOT that model, DO NOT touch it — note the mismatch and move on (constants are the source of truth regardless).
7. **Register the PNG:** add it to `dependencies.yml` under the `generate_film_plane_mechanism.py` outputs, and add an entry to `all-diagrams.md` §7 in sheet order.
8. **Gate:** `python3 src/generators/lint.py` green.
9. **Commit** the generator + PNG + `dependencies.yml` + `all-diagrams.md` with an explicit file list.

---

### Task 1: Phase-0 groundwork — triage, bolt fix, stale-comment sweep

**Files:**
- Modify: `TODO.md` (record interference triage outcome)
- Modify: `src/generators/tbs_constants.py` (stale comment literals; bolt edge-distance fix if constant-driven)
- Modify: `src/generators/generate_film_plane_mechanism.py` and/or `src/models/generate_film_plane_mechanism_model.py` (only if the bolt 7<9 fix needs a geometry/drawn change)

**Interfaces:**
- Produces: confirmed real values for `SKATE_AXLE_LEN` (60), `SKATE_ROLLER_W` (20), `UJOINT_YOKE_L` (34.2), `XSLIDE_STROKE` (300) — the later sheets consume these. A written seated-vs-real classification of the interference flags.

- [ ] **Step 1: Read the six skills.** `skills/skill_diagram_structure.md`, `skill_label_placement.md`, `skill_fastener_convention.md`, `skill_tidy_labels.md`, `skill_model_consistency.md`, `skill_report_writing.md`.

- [ ] **Step 2: Capture the interference baseline.** Run `python3 src/generators/check_interference.py --bolts 2>&1 | tee` and the full model-wide run; record the film-plane counts.

- [ ] **Step 3: Classify the ~164 corner-mechanism flags.** For each contact class (U-rail↔depth-rail, cross-slide↔carriage, gib↔bar, UHMW↔bar, skate-roller↔flange, U-joint↔yoke), decide seated/benign (intended contact — annotate) vs real clash (fix). Write the outcome as a short triage block under the film-plane section of `TODO.md`. Escalate to Alvin any flag that would need a geometry change before touching a constant.

- [ ] **Step 4: Resolve the frame-corner bolt 7<9 edge-distance** in the X-slide shaft support (widen the support/flange or relocate the hole). If it's constant-driven, edit the constant; if drawn-only, fix the drawing. Re-run `check_interference.py --bolts` and confirm that flag clears.

- [ ] **Step 5: Sweep stale comment literals** in `tbs_constants.py`: `FP_W` comment "= 4499mm", `PH_X` comment "= 2399mm", `RAIL_SPAN` comment "= 4499mm" (and any siblings) → update to the current computed values (4389 / 2454 / 4389) or drop the literal in favor of the derivation. Values are computed, so this is comments only — no cascade.

- [ ] **Step 6: Confirm the 4 dead-constant values** against their subsystem source (skate/U-joint/cross-slide specs). They already hold real values; just verify before the sheets draw them.

- [ ] **Step 7: Gate + commit.**

```bash
python3 src/generators/lint.py
python3 src/generators/check_consistency.py
git add TODO.md src/generators/tbs_constants.py
# add the generator/model files ONLY if Step 4 changed a drawn geometry
git commit -m "Film-plane blueprint Phase 0: interference triage + bolt edge-distance + stale-comment sweep"
```

---

### Task 2: Sheet 12 — Depth rail (3×1½ 6061 U-channel)

**Model on:** `sheet4()` (rail mounting / transport drop-in) and `sheet11()` (flange + bolt detail).

**Files:**
- Modify: `src/generators/generate_film_plane_mechanism.py` (add `sheet12()`, dispatch, bump title blocks — see Task 11)
- Create: `diagrams/film-plane-sheet12.png`
- Modify: `dependencies.yml`, `all-diagrams.md`

**Interfaces:**
- Consumes: `FP_RAIL_WEB` (76), `FP_RAIL_FLANGE` (38), `RAIL_LEN` (2200), `FP_CORNER_SEAT_PLATE_W`, `FP_CORNER_SEAT_PROJ`, `FP_CORNER_SEAT_T`, `FP_CORNER_SEAT_PLATE_T`.
- Produces: `sheet12()`.

**Drawing spec (one part per sheet — the depth rail):**
- **View A — side elevation of the full rail:** the 3×1½ U-channel at `RAIL_LEN` cut length, web `FP_RAIL_WEB` × flange `FP_RAIL_FLANGE`, flange opening toward the film. Dimension overall length, web, flange, wall thickness.
- **View B — end section** (channel profile) with the acetal-skate capture envelope ghosted, dimensioned web/flange/inside-gap.
- **View C — two rail variants side by side:** the **fixed-right** rail permanently flanged to its wall seat (show the wall-seat flange hole pattern from `FP_CORNER_SEAT_*`) vs the **drop-in-left** transport rail (stub + lift-out, no wall flange). Callout the difference.
- Fastener callouts per `skill_fastener_convention` for the wall-seat flange bolts (into the seat plate — engage inner face).
- Notes block: material (6061-T6), cut length, 1mm sag optically irrelevant at f/1088, flatness carried by ACM.

- [ ] **Step 1:** Run the Standard Sheet Build Cycle (steps 1–9) for `sheet12()` with the drawing spec above.

---

### Task 3: Sheet 13 — Acetal skate (4-wheel)

**Model on:** `sheet3()` (corner carriage detail — the skate is already sketched there).

**Files:**
- Modify: `src/generators/generate_film_plane_mechanism.py`
- Create: `diagrams/film-plane-sheet13.png`
- Modify: `dependencies.yml`, `all-diagrams.md`

**Interfaces:**
- Consumes: `SKATE_ROLLER_OD` (31.75), `SKATE_KEEPER_OD` (19.05), `SKATE_ROLLER_W` (20), `SKATE_AXLE_OD` (10), `SKATE_AXLE_LEN` (60), `SKATE_ROLLER_SP` (40), `CARRIAGE_PLATE_W` (80), `CARRIAGE_PLATE_H` (181), `CARRIAGE_PLATE_T` (6), `CARRIAGE_AXLE_ROW_SP` (38).
- Produces: `sheet13()`. **Wires the dead constants `SKATE_AXLE_LEN`, `SKATE_ROLLER_W`.**

**Drawing spec (the acetal skate assembly):**
- **View A — skate in the channel (end section):** two Ø`SKATE_ROLLER_OD` load rollers gravity-seated on the bottom flange + two Ø`SKATE_KEEPER_OD` keeper rollers captive under the top flange, all on Ø`SKATE_AXLE_OD`×`SKATE_AXLE_LEN` 304 axles. Dimension roller ODs, axle, the load/keeper row gap `CARRIAGE_AXLE_ROW_SP`.
- **View B — carriage plate (flat):** `CARRIAGE_PLATE_W`×`CARRIAGE_PLATE_H`×`CARRIAGE_PLATE_T` 6061 plate with the axle-bore pattern (load row + keeper row, pitch `SKATE_ROLLER_SP`), edge distances dimensioned. This is a hole table — list bore Ø and coordinates.
- **View C — roller detail:** width `SKATE_ROLLER_W`, bore for axle, material Delrin/acetal.
- Notes: gravity-seated load path, keeper rollers only take uplift/tilt, 304 axle clevis-pin spec.

- [ ] **Step 1:** Run the Standard Sheet Build Cycle for `sheet13()`.

---

### Task 4: Sheet 14 — Cam clamp / rail brake

**Model on:** `sheet3()` (clamp shown in context) and `sheet12()` (rail section for the brake face).

**Files:**
- Modify: `src/generators/generate_film_plane_mechanism.py`
- Create: `diagrams/film-plane-sheet14.png`
- Modify: `dependencies.yml`, `all-diagrams.md`

**Interfaces:**
- Consumes: `CAM_CLAMP_BASE_W` (22), `CAM_CLAMP_BASE_D` (19), `CAM_CLAMP_HOLE_SP` (15.7), `CAM_CLAMP_N` (3), `FP_RAIL_FLANGE`.
- Produces: `sheet14()`.

**Drawing spec (the cam-lever rail brake):**
- **View A — cam clamp elevation:** base `CAM_CLAMP_BASE_W`×`CAM_CLAMP_BASE_D`, cam lever in the locked and released positions (ghost the released), the brake pad bearing on the U-channel flange.
- **View B — mounting footprint (plan):** the 2× M4 base holes at `CAM_CLAMP_HOLE_SP`, referenced to the carriage plate.
- **View C — arrangement:** `CAM_CLAMP_N` clamps per corner on the carriage, spacing along the rail.
- Fastener callouts (M4 into the carriage plate), edge distance.
- Notes: hand-throw lock holds through exposure + transport; no leadscrew.

- [ ] **Step 1:** Run the Standard Sheet Build Cycle for `sheet14()`.

---

### Task 5: Sheet 15 — Cross-slide stack (Z + X)

**Model on:** `sheet8()` (frame ↔ cross-slide attachment) and `sheet10()`/`fp_corner_load.py` (load-case geometry — deep-mount orientation).

**Files:**
- Modify: `src/generators/generate_film_plane_mechanism.py`
- Create: `diagrams/film-plane-sheet15.png`
- Modify: `dependencies.yml`, `all-diagrams.md`

**Interfaces:**
- Consumes: `XSLIDE_Z_BAR_LEN` (345), `XSLIDE_X_BAR_LEN` (365), `XSLIDE_BAR_W` (38.1), `XSLIDE_BAR_T` (6.35), `XSLIDE_GIB_W` (12), `XSLIDE_GIB_T` (6.35), `XSLIDE_UHMW_T` (3.2), `XSLIDE_CARR_WALL` (8), `XSLIDE_STROKE` (300), `XSLIDE_Z_TRAVEL` (245), `XSLIDE_X_TRAVEL` (263).
- Produces: `sheet15()`. **Wires the dead constant `XSLIDE_STROKE`.**

**Drawing spec (the 2-axis cross-slide):**
- **View A — Z (tilt) bar** ¼×1½ 304 flat, cut length `XSLIDE_Z_BAR_LEN`; **View B — X (swing) bar** cut length `XSLIDE_X_BAR_LEN`. Dimension bar width `XSLIDE_BAR_W`, thickness `XSLIDE_BAR_T`, end holes.
- **View C — carriage section showing DEEP MOUNT:** the bar captured with the 38.1 mm dimension in the load direction (the load-case decision), UHMW pads `XSLIDE_UHMW_T` on the bearing faces, brass-tip gib `XSLIDE_GIB_W`×`XSLIDE_GIB_T` on one edge, carriage wall `XSLIDE_CARR_WALL`. Dimension the stroke `XSLIDE_STROKE` and annotate it against the computed foreshortening travel (Z `XSLIDE_Z_TRAVEL`, X `XSLIDE_X_TRAVEL`) — resolve spec §8 open question by labeling 300 as the drawn stroke with margin over 245/263.
- Notes: deep-mount SF≈10 vs flat SF≈1.7; gib drag holds the gravity Z axis while clamping.

- [ ] **Step 1:** Run the Standard Sheet Build Cycle for `sheet15()`.

---

### Task 6: Sheet 16 — U-joint install

**Model on:** `sheet4()` (U-joint sections) and `sheet9()` (frame + ACM ↔ U-joint ↔ X-slide).

**Files:**
- Modify: `src/generators/generate_film_plane_mechanism.py`
- Create: `diagrams/film-plane-sheet16.png`
- Modify: `dependencies.yml`, `all-diagrams.md`

**Interfaces:**
- Consumes: `UJOINT_OD` (19.05), `UJOINT_LEN` (68.3), `UJOINT_YOKE_L` (34.2), `UJOINT_HUB_L` (24.1), `UJOINT_BOOT_OD` (32.54), `UJOINT_BOOT_LEN` (31.75), `UJOINT_STUB_OD` (9.53), `UJOINT_BORE` (9.53), `UJOINT_ANGLE` (45).
- Produces: `sheet16()`. **Wires the dead constant `UJOINT_YOKE_L`.**

**Drawing spec (the Belden SSNBUJ750x3/8KB install):**
- **View A — U-joint elevation** at full extension and at `UJOINT_ANGLE`: overall `UJOINT_LEN`, yoke OD `UJOINT_OD`, single-yoke length `UJOINT_YOKE_L`, hub depth `UJOINT_HUB_L`, integral boot center OD `UJOINT_BOOT_OD` × `UJOINT_BOOT_LEN`.
- **View B — stub-shaft install:** the 3/8" `UJOINT_STUB_OD` 304 stub keyseated into the `UJOINT_BORE` bore, key + set screw, held in the McMaster 4040N12 two-piece clamp support. Dimension the keyseat.
- **View C — corner assembly context:** corner plate → U-joint → X-slide carriage (reference Sheet 17/15).
- Notes: needle-bearing, factory-integral boot, confirm set-screw torque with Belden; 8× SS keys for 4 corners.

- [ ] **Step 1:** Run the Standard Sheet Build Cycle for `sheet16()`.

---

### Task 7: Sheet 17 — 304 corner plate + carriage plates L/R

**Model on:** `sheet9()` (the connection detail that already carries this plate).

**Files:**
- Modify: `src/generators/generate_film_plane_mechanism.py`
- Create: `diagrams/film-plane-sheet17.png`
- Modify: `dependencies.yml`, `all-diagrams.md`

**Interfaces:**
- Consumes: `CORNER_PLATE_W`, `CORNER_PLATE_H`, `CORNER_PLATE_T`, `CORNER_PLATE_HOLE_EDGE`, `CORNER_PLATE_HOLE_SP`, `CORNER_PLATE_BEND_R`, plus `CARRIAGE_PLATE_W/H/T` for cross-reference.
- Produces: `sheet17()`.

**Drawing spec (the 304 stainless corner plate — a flat-pattern + bent part):**
- **View A — flat pattern:** overall `CORNER_PLATE_W`×`CORNER_PLATE_H`×`CORNER_PLATE_T`, bend line at `CORNER_PLATE_BEND_R`, full hole table (frame-bolt holes + U-joint stub hole) with edge distance `CORNER_PLATE_HOLE_EDGE` and spacing `CORNER_PLATE_HOLE_SP`.
- **View B — formed elevation:** the plate bent, showing the frame leg on one face and the U-joint stub boss on the other.
- **View C — L vs R handedness** note (mirror pair).
- Fastener callouts: frame bolts (into the 6061 angle) + the U-joint stub hole; edge distances dimensioned.
- Notes: steel (not expendable Al) because the U-joint funnels the corner load into a few bolts; 304 for galvanic match to the SS U-joint.

- [ ] **Step 1:** Run the Standard Sheet Build Cycle for `sheet17()`.

---

### Task 8: Sheet 18 — Film-plane frame weldment

**Model on:** `sheet7()` (four-corner frame front elevation, to scale).

**Files:**
- Modify: `src/generators/generate_film_plane_mechanism.py`
- Create: `diagrams/film-plane-sheet18.png`
- Modify: `dependencies.yml`, `all-diagrams.md`

**Interfaces:**
- Consumes: `FP_W` (4389), `FP_H` (2094), `FP_ANGLE_LEG`, `FP_ANGLE_T`, `DIBOND_T`.
- Produces: `sheet18()`.

**Drawing spec (the welded 6061 angle frame — one weldment):**
- **View A — full front elevation** to scale: fixed-size rigid rectangle `FP_W`×`FP_H`, 2×2×1/8 (`FP_ANGLE_LEG`/`FP_ANGLE_T`) 6061 angle perimeter. Dimension overall W/H, leg, thickness.
- **View B — corner detail:** coped/mitered corner joint with the **weld schedule** (fillet size, weld symbol per convention, all four corners).
- **View C — section through a member:** the L-angle with the ACM/Dibond backing (`DIBOND_T`) seated in the leg, the corner-plate bolt holes.
- Notes: expendable part (bare 6061 in the splash zone — inspect annually, replace on pitting); ACM carries flatness; corner-plate bolt pattern references Sheet 17.

- [ ] **Step 1:** Run the Standard Sheet Build Cycle for `sheet18()`.

---

### Task 9: Sheet 19 — Wall-seat saddles

**Model on:** `sheet11()` (far-left bracket → pivot-post + far-wall attachment) and `sheet4()` (right flanged seat).

**Files:**
- Modify: `src/generators/generate_film_plane_mechanism.py`
- Create: `diagrams/film-plane-sheet19.png`
- Modify: `dependencies.yml`, `all-diagrams.md`

**Interfaces:**
- Consumes: `FP_CORNER_SEAT_PLATE_W`, `FP_CORNER_SEAT_PROJ`, `FP_CORNER_SEAT_T`, `FP_CORNER_SEAT_PLATE_T`, `C_WID`, `WALL_T`.
- Produces: `sheet19()`.

**Drawing spec (the wall-seat saddle weldments — 8/10 mm plate):**
- **View A — saddle elevation:** the plate saddle at the right-hand rail seats, plate width `FP_CORNER_SEAT_PLATE_W`, projection `FP_CORNER_SEAT_PROJ`, the 8 mm/10 mm plate lines (`FP_CORNER_SEAT_T` / `FP_CORNER_SEAT_PLATE_T`).
- **View B — flat-pattern cut sheets** for the two plate cuts with the weld schedule joining them.
- **View C — mounting to the container wall:** hole pattern into the wall, fastener callouts (engage the wall/backing per convention), edge distances.
- Notes: it's a load-bearing seat for the fixed-right rails (contrast Sheet 11's lateral-tie-only far-left bracket); 2 saddles.

- [ ] **Step 1:** Run the Standard Sheet Build Cycle for `sheet19()`.

---

### Task 10: Sheet 20 — Assembly / exploded + fastener schedule

**Model on:** `sheet3()` (mechanism master) + `sheet5()` (spec/BOM table layout).

**Files:**
- Modify: `src/generators/generate_film_plane_mechanism.py`
- Create: `diagrams/film-plane-sheet20.png`
- Modify: `dependencies.yml`, `all-diagrams.md`

**Interfaces:**
- Consumes: all corner-assembly constants already imported (skate, cross-slide, U-joint, corner plate, cam clamp) + the fastener families.
- Produces: `sheet20()`.

**Drawing spec (corner assembly + master fastener schedule):**
- **View A — exploded corner assembly:** depth rail → skate/carriage → cam clamps → Z-slide → X-slide → U-joint → corner plate → frame, with balloon callouts keyed to the sheet numbers (12–19).
- **View B — fastener schedule table:** every fastener in the corner (M4 cam-clamp, M6/M8 carriage + rail-fixing, M12 wall-seat), with size, grade (304 in the wet zone per policy), qty per corner, and **edge distance** confirmed against `check_interference.py --bolts`.
- Notes: assembly/positioning sequence (roll skate to depth → set Z/X slides → throw cam clamp → U-joint twist-lock).

- [ ] **Step 1:** Run the Standard Sheet Build Cycle for `sheet20()`.

---

### Task 11: Renumber + reconcile existing Sheets 1–11

**Files:**
- Modify: `src/generators/generate_film_plane_mechanism.py` (sheets 1–9, 11 title blocks + labels)
- Modify: `src/generators/fp_corner_load.py` (Sheet 10 title block)
- Modify: `film-plane-mechanism-report.md`, `film-plane-mechanism-analysis.md`

- [ ] **Step 1: Bump all title blocks** `"SHEET N OF 11"` → `"SHEET N OF 20"` across both generators (sheets 1–11, including Sheet 10 in `fp_corner_load.py`). The new sheets 12–20 already use "OF 20".

- [ ] **Step 2: Fix the 10 over-reaching labels + `CARRIAGE_YD_CENTER` panel overflow.** Run `python3 src/generators/tidy_labels.py diagrams/film-plane-sheet*.png` to list offenders; fix each in the generator (shorten leader tips, move labels inside their section axes). Re-run until clean.

- [ ] **Step 3: Cross-reference the new detail sheets** from the GA/mechanism sheets (e.g. Sheet 3 → "corner plate detailed on Sheet 17", "skate on Sheet 13", etc.) via short label/note additions.

- [ ] **Step 4: Reconcile the report narrative.** In `film-plane-mechanism-report.md`, retitle §Purpose/heading from "Mechanism Design" framing to reflect the completed fabrication set, add the new sheet references in §4/§7, update the EPDM foam-tape qty note. In `film-plane-mechanism-analysis.md`, resolve the "PROSE DONE, BOM GATED" scope note. American spelling + single-source any restated dim as a fact placeholder.

- [ ] **Step 5: Render + gate + commit.**

```bash
python3 src/generators/generate_film_plane_mechanism.py
python3 src/generators/fp_corner_load.py
python3 src/generators/tidy_labels.py diagrams/film-plane-sheet*.png
python3 src/generators/lint.py
python3 src/generators/editorial_lint.py
git add src/generators/generate_film_plane_mechanism.py src/generators/fp_corner_load.py \
        film-plane-mechanism-report.md film-plane-mechanism-analysis.md diagrams/film-plane-sheet*.png
git commit -m "Film-plane blueprint: renumber to 20 sheets + reconcile Sheets 1-11 labels/cross-refs/report"
```

---

### Task 12: Parts + costing cascade, registration, full gate sweep

**Files:**
- Modify: `src/generators/parts.py` (any new fab lines)
- Modify: `mkdocs.yml`, `src/generators/setup_docs.py`, `docs/index.md`, `publish.sh` (register the 9 new PNGs)
- Modify: report `.md` parts-list blocks (auto via `--inject`)
- Modify: `RELEASE.md`

- [ ] **Step 1: Add any new fabrication parts** to `parts.py` under the **material-now/fab-later** rule (raw material as a firm low/high line; fab as a separate deferred line). Most parts already exist — add only genuinely new ones surfaced by the detail sheets.

- [ ] **Step 2: Cascade the registries.**

```bash
python3 src/generators/parts.py --inject
python3 src/generators/parts.py --check
python3 src/generators/costing.py --inject
python3 src/generators/costing.py --check-registry
python3 src/generators/facts.py --inject
```

- [ ] **Step 3: Register the 9 new PNGs** in `dependencies.yml` (done per-sheet — verify complete), `setup_docs.py` `DIAG_IMAGE_FILES`, `publish.sh` `DIAG_FILES`, and confirm `all-diagrams.md` §7 lists all of 12–20. (No new nav entries — detail sheets are gallery-only, embedded via the report.) Bump the report embeds if the sheets are referenced in `mkdocs.yml` nav order.

- [ ] **Step 4: Gallery audit — must be empty.**

```bash
comm -23 <(ls diagrams/*.png | xargs -n1 basename | sort -u) \
         <(grep -oE 'assets/[^)]+\.png' all-diagrams.md | sed 's|assets/||' | sort -u)
```

- [ ] **Step 5: Full gate sweep.**

```bash
python3 src/generators/lint.py
python3 src/generators/check_consistency.py
python3 src/generators/check_interference.py --bolts
python3 src/generators/tidy_labels.py diagrams/film-plane-sheet*.png
```

- [ ] **Step 6: Add the `RELEASE.md [Unreleased]` bullet** describing the film-plane fabrication blueprint (9 new detail sheets, renumber to 20, audit-flag closeout).

- [ ] **Step 7: Commit.**

```bash
git add src/generators/parts.py src/generators/costing.py mkdocs.yml src/generators/setup_docs.py \
        docs/index.md publish.sh dependencies.yml all-diagrams.md RELEASE.md \
        film-plane-mechanism-report.md film-plane-mechanism-analysis.md
git commit -m "Film-plane blueprint: parts/costing cascade + register 9 detail sheets + RELEASE note"
```

---

### Task 13: 3D reconcile + publish (conditional)

**Files:**
- Modify: `src/models/generate_film_plane_mechanism_model.py` (only if a constant/geometry changed in Task 1)
- Modify: `dependencies.yml` (manifest hashes)

**Interfaces:**
- Consumes: the `lint.py --cascade <CONST>` output for any constant changed in Task 1.

- [ ] **Step 1: Decide if 3D is needed.** If no constant/geometry changed across the whole run (labels/comments only), SKIP to Step 5. The new sheets are 2D-only reads of existing constants, so a change is only triggered by a Task-1 triage fix.

- [ ] **Step 2: Compute the authoritative re-run list.** For each changed constant: `python3 src/generators/lint.py --cascade <CONST>` — this is the definitive regen/re-send set (includes `overview` if affected).

- [ ] **Step 3: Regenerate + verify the doc match.** `python3 src/models/generate_film_plane_mechanism_model.py --save`, then query the live doc title via `eval_ruby`. If it IS `film-plane-mechanism` → `--send` and verify read-only. If NOT → STOP, ask Alvin to open it, wait. Repeat for `overview` if the cascade lists it.

- [ ] **Step 4: Hand off to Alvin (single-writer).** Tell him "clean — save + upload", focus-model-first ordering. Wait for "saved + uploaded". Then `python3 src/generators/manifest.py --update` and commit the `.skp` + `dependencies.yml`.

- [ ] **Step 5: Publish.** `bash publish.sh` (deploy on request / after this merge per the publish-cadence rule — confirm with Alvin before pushing).

---

## Self-Review

**Spec coverage:**
- §4 sheet table (12–20) → Tasks 2–10 one-to-one; muslin-into-Sheet-6 → Task 11 Step 4 (report/EPDM) + note. ✓
- §2 open flags: dead constants → Tasks 3/5/6 wire them; ~164 interference → Task 1 Step 3; bolt 7<9 → Task 1 Step 4; label defects → Task 11 Step 2; stale comments → Task 1 Step 5; analysis/EPDM → Task 11 Step 4. ✓
- §5 phases → Task 1 (Phase 0), Tasks 2–10 (Phase 1), Task 11 (Phase 2), Task 12 (Phase 3), Task 13 (Phase 4). ✓
- §6 verification → Standard Sheet Build Cycle steps 4–8 + Task 12 Step 5. ✓
- §7 out-of-scope (no redesign, `.skp` single-writer, fab deferred) → Global Constraints + Task 12 Step 1 + Task 13. ✓
- §8 risks: interference escalation → Task 1 Step 3; muslin → Task 11; `XSLIDE_STROKE` 300 → Task 5 spec. ✓

**Placeholder scan:** no TBD/TODO-as-work; the one deliberate adaptation (diagram source not reproduced literally) is stated with the sibling-model mechanism in "The Standard Sheet Build Cycle." ✓

**Type/name consistency:** constant names verified against `tbs_constants.py` (`CORNER_PLATE_*` for the corner plate vs `CARRIAGE_PLATE_*` for the skate carriage plate — kept distinct); `sheetN()` names match sheet numbers and title-block "SHEET N"; Sheet 10 correctly attributed to `fp_corner_load.py`. ✓
