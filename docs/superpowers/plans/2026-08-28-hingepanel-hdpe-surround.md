<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Hinged Panel — HDPE Surround Fabrication Set Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the missing HDPE-surround fabrication blueprints (flat-pattern cut sheets + housing/frame interface details) to the hinged-panel set, connect the surround to the frame in 2D+3D, and reconcile the stale drum geometry left by the Ø900→Ø800 resize.

**Architecture:** Two new sheets appended to the existing `generate_hingepanel_diagram.py` (following its per-sheet function + `title_block()` pattern), a new HDPE-surround solid added to the lighttrap 3D model's `hinge_panel()`, a new report section, and a parts/cost cascade for the surround rivets. All new geometry single-sources off existing `tbs_constants.py` values so it can't drift from the light-trap housing sheets.

**Tech Stack:** Python 3 + matplotlib (2D generators), SketchUp Ruby via MCP (3D), the repo's own gate suite (`lint.py`, `check_consistency.py`, `manifest.py`, `tidy_labels.py`), MkDocs publish chain.

## Global Constraints

- **American English spelling throughout** — center, color, aluminum, analyze.
- **Single source of truth:** never hardcode a value that a constant already owns. New sheet geometry references `DRUM_D` / `DRUM_R` / `LT_HOUSING_R` / `APERTURE_R` / `DRUM_H_LT` / `LT_RIVET_D` / `LT_RIVET_HOLE` / `LT_RIVET_PITCH` — no literal `800`/`400`/`2100`/`3.18` in label strings.
- **SPDX header** on every new/edited `.py`/`.rb`/`.md` (Python: `# SPDX-License-Identifier: AGPL-3.0-only` / `# © 2026 Alvin Richards`; Markdown: HTML-comment form). Gate-enforced.
- **Generated diagrams go in `diagrams/`**; every new PNG must be registered in `all-diagrams.md`, `publish.sh` (`DIAG_FILES`), `setup_docs.py` (`DIAG_IMAGE_FILES`), and `dependencies.yml` — audited by `lint.py`.
- **Models are generated from code only.** For the 3D task: edit the generator → `--save` → verify live doc is `lighttrap` → `--send` → ALVIN saves + re-uploads → only then commit the `.skp`. `eval_ruby` is read-only. Alvin is the sole `.skp` writer.
- **Never `git add -A`/globs.** `git add` the explicit file list only.
- **Any drawing-spec change** updates the report parts list + `master-shopping-list.md` + `project-cost-breakdown.md` in the same commit.
- **Blind-rivet convention:** follow `skills/skill_fastener_convention.md` (fastener engages the inner/bore-side edge, aligns with metal thickness).
- **Add a `RELEASE.md [Unreleased]` bullet as work lands**, not later.
- **Commit, don't publish** per task (deploy only on request / after merge).

## File Structure

- `src/generators/generate_hingepanel_diagram.py` — MODIFY: fix `DRUM_H` import; add `sheet7()` (surround cut sheets) + `sheet8()` (join + rivet details); update `__main__` dispatch; bump every `SHEET N OF 6` title-block to the new total.
- `src/generators/tbs_constants.py` — MODIFY: clean stale `# 450` inline comments (lines ~358, ~366).
- `src/models/generate_lighttrap_model.py` — MODIFY: add HDPE surround skin + upper/lower floor caps + rivet connection to `hinge_panel()`; clean stale `Ø900` comments.
- `hinged-panel-report.md` — MODIFY: new §2.6 (HDPE Surround Fabrication, embeds Sheets 7 & 8); frame-connection resolution into §2.2; §3.1 drum-top Z reconciled to `DRUM_H_LT`.
- `parts.py` — MODIFY: add the surround blind-rivet line (+ any added HDPE area) to the panel-structure system.
- `all-diagrams.md`, `publish.sh`, `src/generators/setup_docs.py`, `dependencies.yml` — MODIFY: register the two new PNGs (and fix the stray duplicate `hingepanel-sheet5.png` in `setup_docs.py:183`).
- `master-shopping-list.md`, `project-cost-breakdown.md` — MODIFY: cascade the rivet cost.
- `RELEASE.md` — MODIFY: `[Unreleased]` bullet.

---

### Task 1: Reconcile stale drum geometry (DRUM_H drift + stale comments + registration bug)

Lowest-risk, unblocks clean sheets. No new drawing — just single-sourcing and stale-literal cleanup.

**Files:**
- Modify: `src/generators/generate_hingepanel_diagram.py:58` (and import line 31)
- Modify: `src/generators/tbs_constants.py` (~lines 358, 366 inline comments)
- Modify: `src/models/generate_lighttrap_model.py` (stale `Ø900` comments: lines ~74, ~122, ~205, ~299, ~348)
- Modify: `src/generators/setup_docs.py:183` (stray duplicate `hingepanel-sheet5.png`)

**Interfaces:**
- Produces: `DRUM_H` in the hingepanel generator now equals `DRUM_H_LT` (2100), imported not hardcoded — every later sheet and Task-4 model read the reconciled height.

- [ ] **Step 1: Capture the pre-change render baseline**

The gate compares against a fresh regen, not HEAD (committed PNGs may be stale). Regenerate first to get a clean baseline:
Run: `python3 src/generators/generate_hingepanel_diagram.py`
Then stage nothing yet — this is the baseline the DRUM_H change will diff against.

- [ ] **Step 2: Import `DRUM_H_LT` and delete the hardcoded `DRUM_H`**

In `generate_hingepanel_diagram.py`, add `DRUM_H_LT` to the `from tbs_constants import ...` line (31), then replace line 58:
```python
DRUM_H  = DRUM_H_LT     # housing/drum height (floor → top bearing, mm) — single-sourced (was hardcoded 2200)
```
Leave line 60 (`DRUM_CY = DRUM_H / 2`) and all downstream uses unchanged — they now track 2100.

- [ ] **Step 3: Clean the stale inline comments**

`tbs_constants.py`: fix the `# 450` comments on the `DRUM_R` (line ~358) and `LT_HOUSING_R = DRUM_R` (line ~366) lines to read `# 400` (value is `DRUM_D // 2 = 400`, Ø800).
`generate_lighttrap_model.py`: change every `Ø900` in comments/docstrings (lines ~74, ~122, ~205, ~299, ~348) to `Ø800`. **Comment-only edits — no geometry change, so the model stays byte-identical and needs no re-send.**
`setup_docs.py:183`: delete the duplicate `"hingepanel-sheet5.png",` line (sheet5 is already listed at line 181).

- [ ] **Step 4: Regenerate and confirm only drum-height-bearing sheets changed**

Run: `python3 src/generators/generate_hingepanel_diagram.py`
Expected: sheets that dimension the drum height (1, 3, and any using `DRUM_H`) change; the plan-view sheet 2 (mid-height section) is unaffected. Open the changed PNGs and confirm the drum/clear-height now reads 2,100 (not 2,200) and 2,055 → 1,955 clear where applicable.
Run: `python3 -c "import ast,sys; ast.parse(open('src/models/generate_lighttrap_model.py').read())"` (comment edits didn't break syntax).

- [ ] **Step 5: Run the gate suite**

Run: `python3 src/generators/lint.py`
Expected: all GATES OK; the "missing cascade" byte-diff check passes (the regenerated PNGs are staged with the constant change).
Run: `python3 src/generators/check_consistency.py`
Expected: no new stale-literal / 2D↔3D divergence findings (the `Ø900`/`450`/`2200` literals are gone).

- [ ] **Step 6: Commit**

```bash
git add src/generators/generate_hingepanel_diagram.py src/generators/tbs_constants.py src/models/generate_lighttrap_model.py src/generators/setup_docs.py diagrams/hingepanel-sheet1.png diagrams/hingepanel-sheet3.png
git commit -m "hingepanel: single-source DRUM_H off DRUM_H_LT (2200->2100); clean stale 450/Ø900 comments; fix setup_docs dup"
```
(Stage the exact set of PNGs the regen actually changed — check `git status` first and adjust the list.)

---

### Task 2: Close the sheet6 "duplication" flag (RESOLVED — distinct handle)

**Decision (Alvin, 2026-08-28): NOT a duplicate.** `hingepanel-sheet6` is the **panel swing-handle** — the D-grab that swings the whole hinged panel, bolted to the frame jamb (§4.3) — a *separate* handle from the light-trap drum-rotation handle. So **sheet6 is retained as-is**, the set stays at **6 existing sheets** (`FINAL_EXISTING_COUNT = 6`), and the new sheets are firmly **7 & 8**. No renumber, no deletion. TODO L53-61 is resolved by this confirmation.

**Files:**
- Modify: `hinged-panel-report.md` §4.3 — one-line cross-reference clarifying this is the panel-swing handle, distinct from the drum-rotation handle in the light-trap set (folded into Task 6's report edit — no separate commit needed here)
- Modify: `TODO.md` — tick the L53-61 duplication item with the "distinct handle — no action" note

- [ ] **Step 1: Tick the TODO item**

In `TODO.md`, mark the "Light-trap ↔ hinged-panel sheet DUPLICATION" item (L53-61) resolved: `[x]` with note "distinct handle — hingepanel-sheet6 is the panel-swing D-grab (§4.3), not the drum-rotation handle; both retained, cross-referenced." Commit this small edit on its own or fold into Task 6.

```bash
git add TODO.md
git commit -m "hingepanel: close sheet6 duplication flag — panel-swing handle is distinct (no action)"
```

---

### Task 3: Sheet 7 — HDPE surround flat-pattern cut sheets

New sheet drawing the 1/8″ HDPE surround pieces laid flat and fully dimensioned. Follows the existing per-sheet function pattern (`fig, ax = plt.subplots(...)`, draw with `tbs_drawing` helpers, `title_block(...)`, `fig.savefig(...)`). Read `skills/skill_diagram_structure.md` and `skills/skill_label_placement.md` before drawing.

**Files:**
- Modify: `src/generators/generate_hingepanel_diagram.py` — add `sheet7()` + dispatch call; title block `SHEET 7 OF <new total>`
- Modify: `all-diagrams.md`, `publish.sh`, `src/generators/setup_docs.py`, `dependencies.yml` — register `hingepanel-sheet7.png`

**Interfaces:**
- Consumes: `DRUM_D`/`DRUM_R`/`LT_HOUSING_R`, `APERTURE_R` (= `HOUSING_R + 18` = 418 → Ø836 aperture), `LT_RIVET_HOLE`/`LT_RIVET_PITCH`, `PANEL_CENTER_T` (120), `NEW_YD_L`/`NEW_YD_R` (center-zone width) — all from `tbs_constants`/existing generator scope.
- Produces: `diagrams/hingepanel-sheet7.png`.

- [ ] **Step 1: Add the `sheet7()` function**

Draw, as flat developable patterns (HDPE is cut-and-weld like the housing, so each piece is a true flat panel — no bend allowances):
- **Front skin** and **back skin** — the center-zone HDPE face panels, each a rectangle `PANEL_CENTER_T`-zone-wide × panel-height, with the **Ø836 circular aperture** (`2*APERTURE_R`) cut where the housing passes through; dimension the aperture Ø and its center; mark the blind-rivet hole line along the frame-lap edges at `LT_RIVET_PITCH` spacing, hole Ø `LT_RIVET_HOLE`, with a `drill Ø{LT_RIVET_HOLE} ×N @ {LT_RIVET_PITCH}mm` callout.
- **Upper floor** and **lower floor** developments — the horizontal HDPE caps that close the top and bottom of the drum bulge; each is a panel with one straight lap edge (to the skin/frame) and one **curved edge matching the Ø800 housing OD** (`DRUM_D`); dimension the curved-edge radius `= DRUM_R` and the overall cap depth (the ~850mm exterior / ~210mm interior overhang from Sheet 2).
- Use `C_PLASTIC` for the HDPE fill; label material `"1/8″ HDPE"` referencing the constant, not literals.
- Reference constants in every dimension/label string (`f"Ø{DRUM_D}"`, `f"{LT_RIVET_PITCH}mm"`) per the Global Constraints.
- Title block: `SHEET 7 OF 8`, subtitle `"HDPE SURROUND — FLAT-PATTERN CUT SHEETS"`, a **stated scale + scale bar** (match the light-trap cut-sheet precedent, e.g. plan 1:10 with a 100mm bar — no "NTS").

- [ ] **Step 2: Add the dispatch call**

In `__main__`, add `sheet7()` after the last existing sheet call.

- [ ] **Step 3: Render**

Run: `python3 src/generators/generate_hingepanel_diagram.py`
Expected: `diagrams/hingepanel-sheet7.png saved` printed; file exists.

- [ ] **Step 4: Static + visual label pass (tidy_labels skill)**

Run: `python3 src/generators/tidy_labels.py --fix src/generators/generate_hingepanel_diagram.py`
Run: `python3 src/generators/tidy_labels.py --overflow src/generators/generate_hingepanel_diagram.py`
Expected: sheet7 reports 0 off-frame labels. Then **open `diagrams/hingepanel-sheet7.png` and do a crop-zoom read**: every piece labeled, aperture + rivet callouts legible, no overlaps, leaders land on edges. Fix and re-render until clean.

- [ ] **Step 5: Register the PNG in all four files**

Add `hingepanel-sheet7.png` to: `all-diagrams.md` (Hinged Panel section, in sheet order, with an `![...]` line), `publish.sh` `DIAG_FILES`, `setup_docs.py` `DIAG_IMAGE_FILES`, and the `hingepanel_diagram` `outputs:` list in `dependencies.yml`.

- [ ] **Step 6: Gate**

Run: `python3 src/generators/lint.py`
Expected: gallery audit + dependencies.yml + missing-cascade all OK.
Run the gallery audit one-liner (from Task 2 Step 4); expected empty.

- [ ] **Step 7: Commit**

```bash
git add src/generators/generate_hingepanel_diagram.py diagrams/hingepanel-sheet7.png all-diagrams.md publish.sh src/generators/setup_docs.py dependencies.yml
git commit -m "hingepanel Sheet 7: HDPE surround flat-pattern cut sheets"
```

---

### Task 4: Sheet 8 — surround→housing floor-join + surround→frame rivet details

New detail sheet, two sections at stated scale. Read `skills/skill_fastener_convention.md` (rivet profile) before drawing the rivet section.

**Files:**
- Modify: `src/generators/generate_hingepanel_diagram.py` — add `sheet8()` + dispatch; title block `SHEET 8 OF <new total>`
- Modify: `all-diagrams.md`, `publish.sh`, `src/generators/setup_docs.py`, `dependencies.yml` — register `hingepanel-sheet8.png`

**Interfaces:**
- Consumes: `DRUM_R`/`LT_HOUSING_T` (housing OD + 5mm wall), `PANEL_CENTER_T`, `LT_RIVET_D`/`LT_RIVET_HOLE`/`LT_RIVET_PITCH`, the 20mm neoprene surround seal (report §3.4).
- Produces: `diagrams/hingepanel-sheet8.png`.

- [ ] **Step 1: Add the `sheet8()` function — Detail A (floor→housing join)**

Draw a section through the **upper (and lower) floor cap where it meets the Ø800 housing OD**: the HDPE cap butting/lapping the housing wall (`LT_HOUSING_T` = 5mm), the 20mm neoprene compression strip closing the 15mm housing-to-panel radial gap (report §3.4), fully dimensioned. Annotate that the housing cut geometry is single-sourced with **light-trap Sheet 2** (housing cut sheet) so the interface can't drift. Use `C_PLASTIC` (HDPE), `C_GASKT` (neoprene), `C_STEEL`/housing color as appropriate. Thin-section scale convention if the cap is much wider than thick (separate `sx`/`sy`, annotated).

- [ ] **Step 2: Add Detail B (surround→frame blind rivets)**

Section showing the surround HDPE edge **lapped over the steel frame flange and blind-riveted**: draw the rivet as a barrel through the lap engaging the inner/bore-side edge per `skills/skill_fastener_convention.md`, with sealant bead for light-tightness; callout `1/8″ SS blind rivet` referencing `LT_RIVET_D`, `drill Ø{LT_RIVET_HOLE}`, pitch `{LT_RIVET_PITCH}mm`. Note the lap is continuous around the aperture + along the frame edges.

- [ ] **Step 3: Title block + dispatch**

Title block `SHEET 8 OF 8`, subtitle `"HDPE SURROUND — HOUSING JOIN & FRAME RIVET DETAILS"`, stated scale + scale bar. Add `sheet8()` to `__main__`. Bump **every** existing `SHEET N OF 6` title-block string in the generator (sheets 1-6) to `SHEET N OF 8`.

- [ ] **Step 4: Render + label pass**

Run: `python3 src/generators/generate_hingepanel_diagram.py`
Run: `python3 src/generators/tidy_labels.py --fix src/generators/generate_hingepanel_diagram.py` then `--overflow`.
Expected: `hingepanel-sheet8.png saved`, 0 off-frame labels. Open and crop-zoom read: both details legible, rivet barrel on the correct (bore-side) edge, dimensions complete.

- [ ] **Step 5: Register + gate**

Add `hingepanel-sheet8.png` to the four registration files. Run `python3 src/generators/lint.py` + the gallery audit one-liner; expected clean/empty.

- [ ] **Step 6: Commit**

```bash
git add src/generators/generate_hingepanel_diagram.py diagrams/hingepanel-sheet8.png all-diagrams.md publish.sh src/generators/setup_docs.py dependencies.yml
git commit -m "hingepanel Sheet 8: surround->housing join + surround->frame blind-rivet details"
```

---

### Task 5: 3D — model the HDPE surround + floor caps + frame rivet connection

The lighttrap model's `hinge_panel()` currently draws the center zone as **steel frame boxes only** — there is no HDPE surround skin or floor cap, which is why the surround "reads as disconnected from the frame." Add the surround geometry, connected. **Single-writer protocol applies — Alvin sends/saves.**

**Files:**
- Modify: `src/models/generate_lighttrap_model.py` — add surround skin + upper/lower floor caps + rivet representation inside `hinge_panel()` (returns appended to `parts`)
- Modify (after re-send): `src/generators/dependencies.yml` (`source_hash` via `manifest.py --update`)

**Interfaces:**
- Consumes: `NEW_YD_L`/`NEW_YD_R`, `APER_L`/`APER_R`, `HOUSING_R`, `APERTURE_R`, `PANEL_CENTER_T`, `PANEL_Z_BOT`/`PANEL_Z_TOP`, `DRUM_H` (=`DRUM_H_LT`), `C_PLASTIC`.
- Produces: an HDPE surround solid physically lapped to the frame in `lighttrap.skp`.

- [ ] **Step 1: Add the surround skin + floor caps to `hinge_panel()`**

Append HDPE (`C_PLASTIC`) boxes: the front + back center-zone skin faces with the drum aperture, and the horizontal upper/lower floor caps closing the drum bulge, sized from `APER_L`/`APER_R`/`APERTURE_R`/`HOUSING_R` and `PANEL_CENTER_T`. Draw the rivet connection as a short row of small boxes/cylinders along the lap edge (representation, not each rivet) so the surround visibly ties to the steel jambs/header — no floating part.

- [ ] **Step 2: Save the `.rb` and syntax-check**

Run: `python3 src/models/generate_lighttrap_model.py --save`
Expected: writes the `.rb`, does NOT touch the live doc. No Python traceback.
(Use `/usr/bin/python3` for the `--save` if a float-noise verify-all flag appears — per the repo's `.rb` regen note.)

- [ ] **Step 3: Verify the live doc is `lighttrap`, then send**

Query: `Sketchup.active_model.title` via `eval_ruby` (read-only).
Expected: it is the lighttrap model. **If it is NOT lighttrap, STOP and ask Alvin to open it** — do not send into another model's doc.
If it matches: Run `python3 src/models/generate_lighttrap_model.py --send`, then `eval_ruby` (read-only) to confirm the surround boxes exist and lap the frame (bounds abut the jamb/header, no gap).

- [ ] **Step 4: Consistency audit**

Run: `python3 src/generators/check_consistency.py`
Expected: no new lighttrap 2D↔3D divergence — the modeled surround matches Sheets 7/8.

- [ ] **Step 5: Hand off to Alvin for save + upload**

Tell Alvin: "lighttrap clean — save + upload." Wait for his "saved + uploaded" confirmation (he does File>Save + Sketchfab re-upload, same UID).

- [ ] **Step 6: Update the manifest and commit the `.skp`**

After Alvin confirms:
Run: `python3 src/generators/manifest.py --update`
Run: `python3 src/generators/manifest.py --check` (expected: all model `source_hash` current).
```bash
git add src/models/generate_lighttrap_model.py src/generators/dependencies.yml src/models/lighttrap.skp
git commit -m "lighttrap 3D: model the HDPE surround + floor caps riveted to the panel frame"
```
(Confirm the exact `.skp` path from `git status`.)

---

### Task 6: Report section + parts/cost cascade + release note

Documents the new sheets and the frame-connection resolution, and cascades the added rivets through the money layer.

**Files:**
- Modify: `hinged-panel-report.md` — new §2.6; §2.2 frame-connection resolution; §3.1 drum-top Z; embed Sheets 7 & 8; §4.3 cross-reference (if Task 2 kept sheet6)
- Modify: `parts.py` — surround blind-rivet line (+ HDPE area if it grows)
- Modify: `master-shopping-list.md`, `project-cost-breakdown.md` — cascaded cost (auto via `--inject`)
- Modify: `RELEASE.md` — `[Unreleased]` bullet

**Interfaces:**
- Consumes: the two new PNGs (Tasks 3-4) and the resolved frame-connection method (blind rivets).

- [ ] **Step 1: Read the report-writing skill**

Read `skills/skill_report_writing.md` (house style: describe current design only, one source of record, source links, placeholder-first).

- [ ] **Step 2: Add §2.6 HDPE Surround Fabrication**

New subsection after §2.5 embedding Sheet 7 (`![...](assets/hingepanel-sheet7.png)`) and Sheet 8, describing the flat-pattern pieces, the housing floor-join, and the blind-rivet frame connection. Keep it a pointer to the sheets, not a restatement of every dimension.

- [ ] **Step 3: Resolve the frame connection in §2.2**

Replace any "surround floats / TBD attachment" language with the decided method: the HDPE surround is **lapped and SS-blind-riveted to the steel frame flange with a sealant bead** (light-tight), per Sheet 8. Reconcile §3.1 drum-top Z to `DRUM_H_LT` (2,100, not 2,250) using a `fact:` placeholder if that value is single-sourced, else the reconciled literal.

- [ ] **Step 4: Add the rivets to `parts.py` and cascade**

Add a surround-rivet part to the panel-structure system (reuse the light-trap `LT_RIVET_*` SKU family — McMaster 97525A435 housing→frame class), with qty from the rivet count (aperture perimeter + frame edges ÷ `LT_RIVET_PITCH`).
Run: `python3 parts.py --inject` (cascades BOM + report §8 + cost docs).
Run: `python3 costing.py --inject`
Run: `python3 src/generators/facts.py --inject` (if any `fact:` placeholder was added in Step 3).

- [ ] **Step 5: Add the release note**

Add to `RELEASE.md` `[Unreleased]`:
```
- Hinged panel: added the HDPE-surround fabrication set (Sheet 7 flat-pattern cut sheets, Sheet 8 housing-join + frame blind-rivet details), modeled the surround connected to the panel frame in 3D, and reconciled the stale Ø900/2200 drum geometry.
```

- [ ] **Step 6: Gate + commit**

Run: `python3 src/generators/lint.py` (parts/costing doc-blocks, section totals, table arithmetic all OK).
Run: `python3 src/generators/editorial_lint.py hinged-panel-report.md` (American spelling + source links).
Run: `python3 src/generators/check_consistency.py`.
```bash
git add hinged-panel-report.md parts.py master-shopping-list.md project-cost-breakdown.md RELEASE.md
git commit -m "hingepanel: report §2.6 HDPE surround + frame-connection resolution; parts/cost cascade for surround rivets"
```

---

## Self-Review

**Spec coverage:**
- Spec D1 (surround cut sheets) → Task 3. D2 (floor→housing join) → Task 4 Detail A. D3 (frame connection 2D + 3D) → Task 4 Detail B + Task 5. D4 (DRUM_H drift + stale comments) → Task 1; (sheet6 de-dup) → Task 2. Cascade/registration (§4) → distributed through Tasks 1-6 + Task 6. Success criteria (§7) → each has a gate step. All spec sections covered.

**Placeholder scan:** No "TBD/TODO/implement later" in the steps. Sheet numbering is settled (6 existing + 2 new = 8; Task 2 resolved). The only intentionally-unwritten content is the exact matplotlib coordinates for the new sheets — *investigation-dependent by nature*: coordinates follow the existing per-sheet pattern + `tbs_constants`, which the generator already establishes. Each sheet is specified by content, constants, scale, and title block rather than invented coordinates, matching how this generator is authored.

**Type/name consistency:** Constant names (`DRUM_H_LT`, `DRUM_D`, `DRUM_R`, `LT_HOUSING_R`, `LT_HOUSING_T`, `APERTURE_R`, `LT_RIVET_D/HOLE/PITCH`, `PANEL_CENTER_T`, `NEW_YD_L/R`, `APER_L/R`, `C_PLASTIC`, `C_GASKT`) verified against `tbs_constants.py` / the generator + model scope during planning. Sheet count is fixed at 8 throughout. `sheet7()`/`sheet8()` names used identically in their tasks.
