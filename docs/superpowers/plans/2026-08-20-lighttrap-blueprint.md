<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->

# Revolving Light-Trap Blueprint Set — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a fabrication-grade 6-sheet 2D blueprint set for the revolving light-trap assembly (housing, drum, caps, bearings, seals, grab rail, cage), after freeing the `lighttrap` diagram name from the misnamed ventilation set.

**Architecture:** A new matplotlib generator `src/generators/generate_lighttrap_diagram.py` emits `diagrams/lighttrap-sheet1..6.png` in house style (`tbs_drawing.py` helpers + `tbs_title_block.title_block`), consuming geometry constants from `tbs_constants.py` (no numeric literals in labels). The existing misnamed ventilation generator/PNGs are renamed to `ventilation-*` first. The six sheets embed into `light-trap-selection.md` §9 and register through the standard doc pipeline.

**Tech Stack:** Python 3, matplotlib (Agg), the repo's `tbs_drawing`/`tbs_title_block`/`tbs_constants` modules, MkDocs registration (`publish.sh`, `setup_docs.py`, `mkdocs.yml`, `dependencies.yml`, `all-diagrams.md`).

## Global Constraints

- **License header on every `.py`/`.md`** — `# SPDX-License-Identifier: AGPL-3.0-only` / `# © 2026 Alvin Richards` (Py) or the HTML-comment form (MD). Lint gate blocks commit without it.
- **American English spelling** throughout (center, color, aluminum, analyze).
- **No numeric literal in a label string** — reference the `tbs_constants.py` constant (`f"Ø{DRUM_D}"`, not `"Ø900"`). Lint "hardwired literal in staged file" flags violations.
- **Reuse `tbs_drawing.py` helpers** (`draw_dim_h/v`, `draw_rect`, `draw_circle`, `leader`, `bolt_holes`, `hatch_rect`, `draw_notes`, `draw_cl`) — never re-emit primitives.
- **Palette:** `C_OUT`/`C_CL`/`C_DIM`/`C_ALUM`/`C_STEEL`/`C_GASKT` from `tbs_constants`; plus `C_LT_DRUM` (`#E8E0D0`) for the drum. White background.
- **Thin cross-sections** use split H/V scale funcs + the annotation `HORIZONTAL SCALE 1:N / VERTICAL SCALE 1:1 — thickness exaggerated for clarity`.
- **`git add` explicit paths only** — never `-A`/globs.
- **No `Co-Authored-By` line** in commits.
- **`RELEASE.md [Unreleased]`** gets a bullet as work lands.
- **No `--send` / no `.skp` change** — this is a 2D-only branch.

## Source-of-truth constants (consumed, never restated)

From `src/generators/tbs_constants.py`:
`DRUM_CX` (-400, axis X), `DRUM_CY` (1181, axis Yd), `DRUM_D` (900), `DRUM_R` (450), `DRUM_H_LT` (2250, top Z), `PANEL_FLOOR_GAP` (130, bottom Z), `LT_HOUSING_R` (450), `LT_HOUSING_T` (5, UV-HDPE), `LT_DRUM_OR` (432, Ø864), `LT_DRUM_T` (3.18, 1/8″ HDPE), `LT_CAP_T` (4.76, 3/16″ HDPE), `LT_OPENING_DEG` (80), `DRUM_CAGE_X0` (-890), `DRUM_CAGE_X1` (50), `DRUM_CAGE_YD_L` (700), `DRUM_CAGE_YD_R` (1662), `C_LT_DRUM` (`#E8E0D0`), `DIAGRAM_DPI`, `DIAGRAMS_DIR`.
Spec text (bearings/seals/hardware) from `light-trap-selection.md` §4.1–4.4.

---

## File Structure

- **Rename:** `src/generators/generate_lighttrap_diagram.py` → `generate_ventilation_diagram.py`; `diagrams/lighttrap-sheet1/2.png` → `ventilation-sheet1/2.png`.
- **Create:** `src/generators/generate_lighttrap_diagram.py` (new, 6 sheets). One file — the sheets share a coordinate frame and helper set; splitting would fracture shared scale funcs. Follows the existing multi-sheet single-file pattern (`generate_hingepanel_diagram.py`).
- **Create:** `diagrams/lighttrap-sheet1..6.png` (generator output).
- **Modify (rename sweep, Task 1):** `publish.sh`, `src/generators/setup_docs.py`, `dependencies.yml`, `all-diagrams.md`, `component-dependency-map.md`, `ventilation-report.md`.
- **Modify (new-set registration, Task 8):** `publish.sh`, `setup_docs.py`, `dependencies.yml`, `all-diagrams.md`, `light-trap-selection.md`, `RELEASE.md`.

**Verification model (this domain has no pytest):** a diagram "test" is *render + inspect*. Each drawing task ends by (1) running the generator, (2) confirming the PNG(s) wrote, (3) a rendered crop-zoom visual pass per `skills/skill_tidy_labels.md`, and (4) `python3 src/generators/tidy_labels.py --fix diagrams/lighttrap-sheetN.png` static check. The branch-level gates (`lint.py`, `check_consistency.py`, gallery audit) run in Task 8.

---

## Task 1: Rename the misnamed ventilation diagram set

**Files:**
- Rename: `src/generators/generate_lighttrap_diagram.py` → `src/generators/generate_ventilation_diagram.py`
- Rename: `diagrams/lighttrap-sheet1.png` → `diagrams/ventilation-sheet1.png`; `diagrams/lighttrap-sheet2.png` → `diagrams/ventilation-sheet2.png`
- Modify: `publish.sh:279-280`, `src/generators/setup_docs.py:163-164`, `dependencies.yml:28`, `all-diagrams.md:133,135`, `component-dependency-map.md`, `ventilation-report.md`

**Interfaces:**
- Produces: the freed name `generate_lighttrap_diagram.py` + `diagrams/lighttrap-sheet*.png` for Tasks 2–7.
- Consumes: nothing.

- [ ] **Step 1: Rename the generator and its outputs with `git mv`**

```bash
git mv src/generators/generate_lighttrap_diagram.py src/generators/generate_ventilation_diagram.py
git mv diagrams/lighttrap-sheet1.png diagrams/ventilation-sheet1.png
git mv diagrams/lighttrap-sheet2.png diagrams/ventilation-sheet2.png
```

- [ ] **Step 2: Update the savefig paths inside the renamed generator**

In `generate_ventilation_diagram.py`, change the two savefig basenames:
`"lighttrap-sheet1.png"` → `"ventilation-sheet1.png"`, `"lighttrap-sheet2.png"` → `"ventilation-sheet2.png"` (and the two `print(...)` lines if present). Titles already read "VENTILATION SYSTEM"; leave them.

- [ ] **Step 3: Repoint every registration + embed**

- `publish.sh:279-280`: `"lighttrap-sheet1.png"`→`"ventilation-sheet1.png"`, `"lighttrap-sheet2.png"`→`"ventilation-sheet2.png"`.
- `setup_docs.py:163-164`: same two strings.
- `dependencies.yml:28`: rename the key `lighttrap_diagram` → `ventilation_diagram`, set `script: src/generators/generate_ventilation_diagram.py`, `outputs: [diagrams/ventilation-sheet1.png, diagrams/ventilation-sheet2.png]`. (Leave the `lighttrap:` 3D-model key at line 62 untouched.)
- `all-diagrams.md:133,135`: `assets/lighttrap-sheet1.png`→`assets/ventilation-sheet1.png`, `assets/lighttrap-sheet2.png`→`assets/ventilation-sheet2.png`.
- `component-dependency-map.md`: replace each `lighttrap-sheet1/2` occurrence with `ventilation-sheet1/2` (grep to find them).
- `ventilation-report.md`: replace each `assets/lighttrap-sheet1/2.png` embed with `assets/ventilation-sheet1/2.png`.

- [ ] **Step 4: Regenerate the renamed set to confirm it still builds**

Run: `cd /Users/alvinrichards/dev/tbs && python3 src/generators/generate_ventilation_diagram.py`
Expected: prints two saves; `diagrams/ventilation-sheet1.png` and `ventilation-sheet2.png` exist and are non-empty; no `lighttrap-sheet*.png` regenerated.

- [ ] **Step 5: Verify no dangling references to the old name**

Run: `grep -rn 'lighttrap-sheet' --include='*.md' --include='*.py' --include='*.yml' --include='publish.sh' . ; echo "exit=$?"`
Expected: no matches (grep exit 1). Any hit is a missed repoint — fix it.

- [ ] **Step 6: Commit**

```bash
git add src/generators/generate_ventilation_diagram.py diagrams/ventilation-sheet1.png diagrams/ventilation-sheet2.png publish.sh src/generators/setup_docs.py dependencies.yml all-diagrams.md component-dependency-map.md ventilation-report.md
git commit -m "rename: ventilation diagrams off the misnamed lighttrap-* name"
```

---

## Task 2: New generator scaffold + Sheet 1 (General Arrangement)

**Files:**
- Create: `src/generators/generate_lighttrap_diagram.py`
- Output: `diagrams/lighttrap-sheet1.png`

**Interfaces:**
- Consumes: `tbs_drawing` helpers, `tbs_title_block.title_block`, the constants listed above.
- Produces: module-level `main()` calling `draw_sheet1()..draw_sheet6()`; shared scale funcs `sx(mm)`/`sy(mm)` and the coordinate convention (drum axis at `DRUM_CX`,`DRUM_CY`; Z up) reused by Tasks 3–7.

- [ ] **Step 1: Write the generator scaffold with the shared header + Sheet 1 stub**

```python
#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_lighttrap_diagram.py
TBS-001  Revolving Light-Trap — fabrication blueprint set (6 sheets).

Sheet 1: General Arrangement — vertical section on the drum axis
Sheet 2: Housing cylinder — cut sheet (flat pattern)
Sheet 3: Rotating drum — cut sheet (flat pattern) + caps
Sheet 4: Bearing hub & stub-shaft detail
Sheet 5: Seals & light-path verification
Sheet 6: Drum cage / support frame
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
from tbs_constants import (
    C_OUT, C_CL, C_DIM, C_ALUM, C_STEEL, C_GASKT, C_LT_DRUM,
    DRUM_CX, DRUM_CY, DRUM_D, DRUM_R, DRUM_H_LT, PANEL_FLOOR_GAP,
    LT_HOUSING_R, LT_HOUSING_T, LT_DRUM_OR, LT_DRUM_T, LT_CAP_T, LT_OPENING_DEG,
    DRUM_CAGE_X0, DRUM_CAGE_X1, DRUM_CAGE_YD_L, DRUM_CAGE_YD_R,
    DIAGRAM_DPI, DIAGRAMS_DIR,
)
from tbs_drawing import (
    draw_dim_h, draw_dim_v, draw_rect, draw_circle, draw_cl,
    leader, bolt_holes, hatch_rect, draw_notes,
)
from tbs_title_block import title_block

BG = "white"


def draw_sheet1():
    """General Arrangement — vertical section on the drum axis (looking along +Yd)."""
    raise NotImplementedError  # filled in Step 3


def main():
    draw_sheet1()


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run to confirm the module imports and constants resolve**

Run: `cd /Users/alvinrichards/dev/tbs && python3 -c "import sys; sys.path.insert(0,'src/generators'); import generate_lighttrap_diagram"`
Expected: no ImportError (a `NotImplementedError` only fires when `main()` runs, which it doesn't on import). If a constant name is wrong, fix it against `tbs_constants.py`.

- [ ] **Step 3: Implement Sheet 1 — General Arrangement**

Draw a **vertical section on the drum axis**, view looking along +Yd (Z up, X across). Content:
- Fixed **housing** outline: Ø`DRUM_D` OD, wall `LT_HOUSING_T`, from Z=`PANEL_FLOOR_GAP` to Z=`DRUM_H_LT` (use `draw_rect` for the two wall verticals in section + `hatch_rect` for the wall thickness).
- **Rotating drum** inside: Ø(2·`LT_DRUM_OR`), wall `LT_DRUM_T`, fill `C_LT_DRUM`; 15mm running gap to the housing (label it, value from `LT_HOUSING_R - LT_DRUM_OR - LT_HOUSING_T`).
- **Top + bottom caps** (`LT_CAP_T`), each carrying a **stub shaft** into an **SKF 6215** bearing (draw as a labeled block at each end; spec from §4.2).
- **Grab rail** on the interior face (100mm Ø × 400mm, at 900mm height — leader-labeled).
- Overall dims: height `draw_dim_v` from `PANEL_FLOOR_GAP`→`DRUM_H_LT`; OD `draw_dim_h` = `DRUM_D`; interior clear height `DRUM_H_LT - PANEL_FLOOR_GAP`.
- **Opening orientation** note: two 80° (`LT_OPENING_DEG`) openings 180° apart (exterior + interior-onto-walkway) — small inset plan circle keyed "see Sheet 2/5 for angular detail".
- **BOM table** (draw with `draw_notes` or a text table): Item / Qty / Material / Source — housing skin (5mm UV-HDPE), drum shell (1/8″ HDPE), caps (3/16″ HDPE), SKF 6215-2RS1 ×2, neoprene seals, SS grab rail. Pull material/qty from §4; cite `light-trap-selection.md`.
- Title block:

```python
    title_block(ax, "SHEET 1 OF 6", drawing_title="REVOLVING LIGHT-TRAP",
                subtitle="GENERAL ARRANGEMENT — VERTICAL SECTION ON DRUM AXIS",
                scale_note="ALL DIMS IN mm", doc_id="TBS-001 · Revolving Light-Trap",
                height=0.045, scale=0.75)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "lighttrap-sheet1.png"),
                dpi=DIAGRAM_DPI, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print("  diagrams/lighttrap-sheet1.png saved")
```

Use the fig/ax setup pattern from `generate_hingepanel_diagram.py` Sheet 1 (subplots, `set_aspect("equal")`, `axis("off")`, `subplots_adjust`).

- [ ] **Step 4: Render and verify Sheet 1 wrote**

Run: `cd /Users/alvinrichards/dev/tbs && python3 src/generators/generate_lighttrap_diagram.py`
Expected: prints `diagrams/lighttrap-sheet1.png saved`; file exists, non-empty.

- [ ] **Step 5: Visual + static label pass**

Run: `python3 src/generators/tidy_labels.py --fix diagrams/lighttrap-sheet1.png`
Then Read the PNG and crop-zoom per `skills/skill_tidy_labels.md`: check no overlapping labels, leaders land on edges, dims readable, BOM legible. Fix drawing code and re-render until clean.

- [ ] **Step 6: Commit**

```bash
git add src/generators/generate_lighttrap_diagram.py diagrams/lighttrap-sheet1.png
git commit -m "lighttrap blueprint: Sheet 1 General Arrangement"
```

---

## Task 3: Sheet 2 — Housing cylinder cut sheet (flat pattern)

**Files:**
- Modify: `src/generators/generate_lighttrap_diagram.py` (add `draw_sheet2()`, call it in `main()`)
- Output: `diagrams/lighttrap-sheet2.png`

**Interfaces:**
- Consumes: the scaffold + scale convention from Task 2; `DRUM_D`, `LT_HOUSING_T`, `LT_OPENING_DEG`, `DRUM_H_LT`, `PANEL_FLOOR_GAP`.
- Produces: nothing new for later tasks.

- [ ] **Step 1: Implement `draw_sheet2()` — the housing flat pattern**

Draw the 5mm UV-HDPE housing as a **developed (unrolled) rectangle**:
- Width = developed length = `math.pi * DRUM_D` (label it "DEVELOPED LENGTH π·Ø{DRUM_D}"); import `math`.
- Height = `DRUM_H_LT - PANEL_FLOOR_GAP` (the housing height).
- Two **80° opening cutouts** (`LT_OPENING_DEG`) located along the developed width: each cutout's along-width position = arc length = `(angle/360)·π·DRUM_D`; the two openings are 180° apart (half the developed width). Draw each as a `draw_rect` window, dimension its width (`(LT_OPENING_DEG/360)*math.pi*DRUM_D`) and its start position from the weld seam.
- **Weld seam** at one edge (vertical line, labeled "ROLL + EXTRUSION WELD SEAM").
- Finish notes via `draw_notes`: interior face black-pigmented + flat-black at welds; exterior UV-stabilized, no primer (cite §4.1).
- Because it is a thin wall shown developed (flat), no split-scale needed — it is a true 1:N flat pattern; annotate the scale.
- `title_block(ax, "SHEET 2 OF 6", drawing_title="REVOLVING LIGHT-TRAP", subtitle="HOUSING CYLINDER — CUT SHEET (FLAT PATTERN)", ...)` and savefig `lighttrap-sheet2.png`.

- [ ] **Step 2: Add `draw_sheet2()` to `main()`**

```python
def main():
    draw_sheet1()
    draw_sheet2()
```

- [ ] **Step 3: Render**

Run: `cd /Users/alvinrichards/dev/tbs && python3 src/generators/generate_lighttrap_diagram.py`
Expected: prints Sheet 1 + Sheet 2 saved; `diagrams/lighttrap-sheet2.png` exists.

- [ ] **Step 4: Visual + static label pass**

Run: `python3 src/generators/tidy_labels.py --fix diagrams/lighttrap-sheet2.png`
Read + crop-zoom; verify the developed-length and cutout dims are unambiguous. Fix and re-render until clean.

- [ ] **Step 5: Commit**

```bash
git add src/generators/generate_lighttrap_diagram.py diagrams/lighttrap-sheet2.png
git commit -m "lighttrap blueprint: Sheet 2 housing cut sheet"
```

---

## Task 4: Sheet 3 — Rotating drum cut sheet + caps

**Files:**
- Modify: `src/generators/generate_lighttrap_diagram.py` (add `draw_sheet3()`)
- Output: `diagrams/lighttrap-sheet3.png`

**Interfaces:**
- Consumes: `LT_DRUM_OR`, `LT_DRUM_T`, `LT_CAP_T`, `LT_OPENING_DEG`, `DRUM_H_LT`, `PANEL_FLOOR_GAP`, plus the SKF 6215 bore Ø75 (from §4.2 — reference the report, do not invent).
- Produces: nothing new.

- [ ] **Step 1: Implement `draw_sheet3()` — drum C-shell flat pattern + caps**

- **C-shell flat pattern:** developed length = `math.pi * 2 * LT_DRUM_OR` MINUS the single 80° opening; draw the developed rectangle, cut the one `LT_OPENING_DEG` window, dimension the opening arc `(LT_OPENING_DEG/360)*math.pi*2*LT_DRUM_OR` and the remaining shell. Height = drum body height. Wall `LT_DRUM_T` (1/8″ HDPE). Weld seam labeled.
- **Top + bottom caps:** two plan circles Ø(2·`LT_DRUM_OR`), `LT_CAP_T` (3/16″), each with a central **stub-shaft bore** (label diameter to suit the shaft into the SKF 6215 Ø75 bore) + **circlip groove**. Note "caps cut from housing 46685 offcut — no extra sheet" (from `LT_CAP_T` comment / §4).
- **Shell-to-cap weld map:** callout showing the extrusion weld joining shell OD to cap perimeter; running-gap note (15mm radial to housing).
- `title_block(... "SHEET 3 OF 6" ... subtitle="ROTATING DRUM — CUT SHEET (FLAT PATTERN) + CAPS" ...)`; savefig `lighttrap-sheet3.png`; add `draw_sheet3()` to `main()`.

- [ ] **Step 2: Render**

Run: `cd /Users/alvinrichards/dev/tbs && python3 src/generators/generate_lighttrap_diagram.py`
Expected: Sheets 1–3 saved; `lighttrap-sheet3.png` exists.

- [ ] **Step 3: Visual + static label pass**

Run: `python3 src/generators/tidy_labels.py --fix diagrams/lighttrap-sheet3.png`
Read + crop-zoom; verify shell developed length, opening arc, and cap bores are clear. Fix + re-render.

- [ ] **Step 4: Commit**

```bash
git add src/generators/generate_lighttrap_diagram.py diagrams/lighttrap-sheet3.png
git commit -m "lighttrap blueprint: Sheet 3 drum cut sheet + caps"
```

---

## Task 5: Sheet 4 — Bearing hub & stub-shaft detail

**Files:**
- Modify: `src/generators/generate_lighttrap_diagram.py` (add `draw_sheet4()`)
- Output: `diagrams/lighttrap-sheet4.png`

**Interfaces:**
- Consumes: `LT_CAP_T`, `DRUM_H_LT`, `PANEL_FLOOR_GAP`; SKF 6215-2RS1 spec (Ø75 ID / Ø130 OD / 25 wide, C3) + mounts from §4.2 — reference, cite, no invented numbers.
- Produces: nothing new.

- [ ] **Step 1: Implement `draw_sheet4()` — enlarged bearing-hub sections (thin detail, split scale)**

Two enlarged detail bubbles (upper + lower hub), thickness-exaggerated:
- **Split scale funcs** `sx(mm)=mm/2.0`, `sy(mm)=mm/2.0` or 1:1 detail; annotate "DETAIL — NOT TO SCALE".
- **Upper hub:** cap (`LT_CAP_T`) → stub shaft → SKF 6215 seated in an **isolated aluminum top ring** bolted to the panel top rail (6×M10). Circlip axial retention on the shaft (`draw_circle`/leader).
- **Lower hub:** cap → stub shaft → SKF 6215 in a **welded steel floor collar** (8×M10 into the panel bottom rail). Circlip.
- Dimension the bearing envelope (Ø75/Ø130/25) and the shaft fit; use `hatch_rect` for the steel collar (`C_STEEL`) and aluminum ring (`C_ALUM`).
- Notes (cite §4.2): sealed C3 bearing 0–120°C, 52.7 kN radial rating; isolate upper mount.
- `title_block(... "SHEET 4 OF 6" ... subtitle="BEARING HUB & STUB-SHAFT DETAIL" ...)`; savefig `lighttrap-sheet4.png`; add to `main()`.

- [ ] **Step 2: Render**

Run: `cd /Users/alvinrichards/dev/tbs && python3 src/generators/generate_lighttrap_diagram.py`
Expected: Sheets 1–4 saved; `lighttrap-sheet4.png` exists.

- [ ] **Step 3: Visual + static label pass**

Run: `python3 src/generators/tidy_labels.py --fix diagrams/lighttrap-sheet4.png`
Read + crop-zoom; verify bearing seat, circlip, and bolt callouts read cleanly at the exaggerated scale. Fix + re-render.

- [ ] **Step 4: Commit**

```bash
git add src/generators/generate_lighttrap_diagram.py diagrams/lighttrap-sheet4.png
git commit -m "lighttrap blueprint: Sheet 4 bearing hub detail"
```

---

## Task 6: Sheet 5 — Seals & light-path verification

**Files:**
- Modify: `src/generators/generate_lighttrap_diagram.py` (add `draw_sheet5()`)
- Output: `diagrams/lighttrap-sheet5.png`

**Interfaces:**
- Consumes: `DRUM_D`, `DRUM_R`, `LT_HOUSING_R`, `LT_DRUM_OR`, `LT_HOUSING_T`, `LT_OPENING_DEG`, `C_GASKT`; seal spec from §4.3; light-path argument from §5.
- Produces: nothing new.

- [ ] **Step 1: Implement `draw_sheet5()` — plan section + seal details**

- **Plan section at drum mid-height** (`draw_circle` housing Ø`DRUM_D` + drum Ø(2·`LT_DRUM_OR`)): show both 80° housing openings 180° apart and the single drum opening; overlay two or three drum rotations proving the drum opening **never** aligns with both housing openings simultaneously (the <90° overlap → no straight-through path). This is the drawn form of §5.
- **Seal detail callouts** (`C_GASKT`): 20mm neoprene compression strip closing the 15mm drum-to-panel gap; 12mm neoprene top + bottom wiper strips bonded to cap undersides + silicone bead to the mount plates (§4.3).
- **Light-path note** via `draw_notes`: because each opening is `LT_OPENING_DEG` < 90°, no rotor angle presents a common chord through both openings; black interior kills residual scatter.
- `title_block(... "SHEET 5 OF 6" ... subtitle="SEALS & LIGHT-PATH VERIFICATION" ...)`; savefig `lighttrap-sheet5.png`; add to `main()`.

- [ ] **Step 2: Render**

Run: `cd /Users/alvinrichards/dev/tbs && python3 src/generators/generate_lighttrap_diagram.py`
Expected: Sheets 1–5 saved; `lighttrap-sheet5.png` exists.

- [ ] **Step 3: Visual + static label pass**

Run: `python3 src/generators/tidy_labels.py --fix diagrams/lighttrap-sheet5.png`
Read + crop-zoom; verify the rotation overlay reads clearly and seal callouts don't collide. Fix + re-render.

- [ ] **Step 4: Commit**

```bash
git add src/generators/generate_lighttrap_diagram.py diagrams/lighttrap-sheet5.png
git commit -m "lighttrap blueprint: Sheet 5 seals & light-path"
```

---

## Task 7: Sheet 6 — Drum cage / support frame

**Files:**
- Modify: `src/generators/generate_lighttrap_diagram.py` (add `draw_sheet6()`)
- Output: `diagrams/lighttrap-sheet6.png`

**Interfaces:**
- Consumes: `DRUM_CAGE_X0`, `DRUM_CAGE_X1`, `DRUM_CAGE_YD_L`, `DRUM_CAGE_YD_R`, `DRUM_H_LT`, `PANEL_FLOOR_GAP`, `DRUM_CX`, `DRUM_CY`, `DRUM_D`, `C_STEEL`.
- Produces: nothing new.

- [ ] **Step 1: Implement `draw_sheet6()` — cage plan + elevation**

- **Plan view:** cage footprint from `DRUM_CAGE_X0..X1` (X) × `DRUM_CAGE_YD_L..YD_R` (Yd), with the Ø`DRUM_D` housing centered at (`DRUM_CX`,`DRUM_CY`) inside it; show ~30mm side clearance to the housing (dimension `DRUM_CAGE_YD_L` to housing edge). Members drawn as `C_STEEL` sections.
- **Elevation:** full-depth frame `PANEL_FLOOR_GAP`→`DRUM_H_LT` reacting the bearing loads; **bearing-plate seats** top + bottom; **anchor points** to container floor / panel (leader-labeled).
- Dimensions: cage overall X span (`DRUM_CAGE_X1 - DRUM_CAGE_X0`), Yd span (`DRUM_CAGE_YD_R - DRUM_CAGE_YD_L`), height.
- Note: "cage reacts the drum-revolve bearing loads; full depth per `tbs_constants` cage envelope."
- `title_block(... "SHEET 6 OF 6" ... subtitle="DRUM CAGE / SUPPORT FRAME" ...)`; savefig `lighttrap-sheet6.png`; add to `main()`.

- [ ] **Step 2: Render**

Run: `cd /Users/alvinrichards/dev/tbs && python3 src/generators/generate_lighttrap_diagram.py`
Expected: Sheets 1–6 all saved; `lighttrap-sheet6.png` exists.

- [ ] **Step 3: Visual + static label pass**

Run: `python3 src/generators/tidy_labels.py --fix diagrams/lighttrap-sheet6.png`
Read + crop-zoom; verify plan + elevation align and cage dims read cleanly. Fix + re-render.

- [ ] **Step 4: Commit**

```bash
git add src/generators/generate_lighttrap_diagram.py diagrams/lighttrap-sheet6.png
git commit -m "lighttrap blueprint: Sheet 6 drum cage"
```

---

## Task 8: Register the set, embed in the report, and run branch gates

**Files:**
- Modify: `dependencies.yml`, `publish.sh`, `src/generators/setup_docs.py`, `all-diagrams.md`, `light-trap-selection.md`, `RELEASE.md`

**Interfaces:**
- Consumes: the six PNGs from Tasks 2–7.
- Produces: a fully registered, gate-clean blueprint set.

- [ ] **Step 1: Register the generator → outputs in `dependencies.yml`**

Add under `diagrams:`:
```yaml
  lighttrap_diagram: {script: src/generators/generate_lighttrap_diagram.py, outputs: [diagrams/lighttrap-sheet1.png, diagrams/lighttrap-sheet2.png, diagrams/lighttrap-sheet3.png, diagrams/lighttrap-sheet4.png, diagrams/lighttrap-sheet5.png, diagrams/lighttrap-sheet6.png]}
```

- [ ] **Step 2: Register the six PNGs in `publish.sh` (`DIAG_FILES`) and `setup_docs.py` (`DIAG_IMAGE_FILES`)**

Add `"lighttrap-sheet1.png"` … `"lighttrap-sheet6.png"` to both arrays (near where `ventilation-sheet*` now live).

- [ ] **Step 3: Add the six to `all-diagrams.md`**

Under a "Revolving Light-Trap" section, in sheet order:
```markdown
![TBS-001 Revolving Light-Trap — Sheet 1: General Arrangement](assets/lighttrap-sheet1.png)
```
…through Sheet 6 (General Arrangement, Housing Cut Sheet, Drum Cut Sheet, Bearing Hub Detail, Seals & Light-Path, Drum Cage).

- [ ] **Step 4: Embed the set into `light-trap-selection.md` §9**

Add a new section after §8:
```markdown
## 9. Fabrication Blueprints

![TBS-001 Revolving Light-Trap — Sheet 1: General Arrangement](assets/lighttrap-sheet1.png)
```
…through Sheet 6, each with a one-line caption. (§8 "Source References" stays last only if house style requires; otherwise place §9 before references — match the report's existing section order convention.)

- [ ] **Step 5: Add `RELEASE.md [Unreleased]` bullets**

Under `## [Unreleased]`, add:
```markdown
- Revolving light-trap: new 6-sheet fabrication blueprint set (housing/drum cut sheets, bearing hub, seals & light-path, drum cage); ventilation diagrams renamed off the misnamed `lighttrap-*` name.
```

- [ ] **Step 6: Run the branch gates**

Run: `cd /Users/alvinrichards/dev/tbs && python3 src/generators/lint.py && python3 src/generators/check_consistency.py`
Expected: both clean (license headers, dependencies.yml valid, gallery covers every PNG, no stale literals). Fix any flag.

- [ ] **Step 7: Gallery audit (must be empty)**

Run:
```bash
comm -23 <(ls diagrams/*.png | xargs -n1 basename | sort -u) <(grep -oE 'assets/[^)]+\.png' all-diagrams.md | sed 's|assets/||' | sort -u)
```
Expected: empty output (every diagram PNG is in the gallery).

- [ ] **Step 8: Commit**

```bash
git add dependencies.yml publish.sh src/generators/setup_docs.py all-diagrams.md light-trap-selection.md RELEASE.md
git commit -m "lighttrap blueprint: register set, embed in report §9, changelog"
```

---

## Self-Review

**Spec coverage:** §2 rename → Task 1. §3 sheets 1–6 → Tasks 2–7. §4 doc home (extend `light-trap-selection.md` §9) → Task 8 Step 4. §5 sources-of-truth → Global Constraints + per-task "Consumes". §6 verification → per-task tidy passes + Task 8 gates/gallery. §7 follow-ups → intentionally excluded (documented as deferred). §8 open questions → resolved (extend §9; true flat patterns in Tasks 3–4; 6 sheets). All covered.

**Placeholder scan:** no TBD/TODO; each drawing task names the exact constants, views, dimensions, and callouts. Drawing tasks specify content precisely but not every matplotlib coordinate — coordinates are hand-tuned during rendering against the visual gate (the honest altitude for this domain; the scaffold code, constant names, helper calls, title-block calls, and verification commands are all concrete).

**Type consistency:** function names `draw_sheet1..6`, `main()`, scale funcs `sx/sy`, and savefig basenames `lighttrap-sheet1..6.png` are consistent across tasks. Constant names match `tbs_constants.py` (verified in exploration).
