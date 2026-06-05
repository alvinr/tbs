# Light-Trap Punch-Out Bay — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax. **All work on branch `lighttrap-refactor`; do not merge to `main` without explicit permission.**

**Goal:** Offset the Ø900 personnel light-lock clear of the X=150 film-plane left rail via a forward-protruding "punch-out bay" in the hinged panel (option B2), restoring full symmetric film-plane movement, and re-skin the drum/housing in plastic to shed weight.

**Architecture:** `tbs_constants.py` is the single spatial source of truth read by both the 2D matplotlib generators (`src/generators/`) and the 3D SketchUp generators (`src/models/`). Change constants first; everything ripples from there. Reports + shopping/cost are prose that must be updated in the same pass.

**Tech Stack:** Python 3 (`/usr/bin/python3`, matplotlib), SketchUp Ruby over TCP (`sketchup_client.send_ruby`), MkDocs.

**Verification idioms (this repo has no pytest):**
- `python3 src/generators/check_consistency.py` — stale-literal / 2D↔3D drift audit (run after every constants/geometry change).
- **Byte-identical PNG check** — capture md5 before, regenerate, compare; *only the intended* diagrams should change.
- **Build-check grep** — generate the model `.rb` and grep for expected/absent parts before sending.
- **Live SketchUp verify** — `--send`/`--skp` then query the live model; **always gate on `Sketchup.active_model.path` before any `--send`** (a mis-gated send clobbered a doc earlier in this project).
- **Weight/CG re-run** — `python3 src/generators/generate_weight_analysis.py` + read the printed CG.

**Decisions baked in (from the spec; flagged items need physical/structural sign-off, not code):**
- Offset `DRUM_CX = -400` (interior edge +50, ~100 mm rail clearance).
- `PANEL_SLIDE = 880`. Delete `BRACE_LEFT_DEMOUNT_Y0/Y1`.
- Hybrid skin: metal end-caps/hoops/bearings + **4 mm PP** drum skin, **5 mm UV-HDPE** housing skin (thickness constants; material is a reports/shopping change). Structural sizing of hinges/caster/suspension is modelled + specified here but **flagged for structural sign-off**.

Reference spec: `docs/superpowers/specs/2026-06-05-lighttrap-punchout-bay-design.md`.

---

## Phase 0 — Constants (the source of truth)

### Task 1: Update `tbs_constants.py`

**Files:**
- Modify: `src/generators/tbs_constants.py` (light-lock + sliding-rail + film-plane-brace sections)

- [ ] **Step 1: Capture the pre-change consistency baseline**

Run: `cd <repo> && /usr/bin/python3 src/generators/check_consistency.py | tail -3`
Expected: prints "Audit complete." (note the per-check counts to compare later).

- [ ] **Step 2: Edit the light-lock constants**

In `tbs_constants.py`, change the light-lock center and add the bay geometry:
```python
DRUM_CX    = -400    # light-lock center X (mm) [B2: offset out so housing interior
                     # edge (+50) clears the X=150 film-plane left rail by ~100mm]
# Bay: the hinge-panel center zone is a forward-protruding box enclosing the housing.
BAY_FRONT_X   = DRUM_CX - DRUM_R - 40   # = -890 — bay outer (exterior) face
BAY_BACK_X    = 0                        # bay meets the panel side-zone plane
BAY_WALL_T    = 6                        # bay box wall thickness (mm)
```
(Keep `DRUM_D=900`, `DRUM_R=450`, `DRUM_CY=1181`, `DRUM_H_LT=2200` unchanged.)

- [ ] **Step 3: Update the transport slide**

```python
PANEL_SLIDE  = 880   # transport slide travel (mm) [B2: housing exterior face -890
                     # -> +X clears the door plane; replaces 550]
```

- [ ] **Step 4: Delete the demountable-segment constants**

Remove `BRACE_LEFT_DEMOUNT_Y0` and `BRACE_LEFT_DEMOUNT_Y1` and their comment block (the drum no longer crosses the X=150 rail, so the left rail is continuous in operating mode). Also remove `CARRIAGE_PARK_Y` only if it is referenced by nothing else — check first:
```bash
git grep -n "BRACE_LEFT_DEMOUNT\|CARRIAGE_PARK_Y" -- src docs '*.md'
```
Delete a constant only if the sole remaining reference is its own definition. If still referenced, leave it and let the referencing task remove the use first.

- [ ] **Step 5: Add the plastic-skin thickness + transport-bracket constants**

```python
DRUM_SKIN_T    = 4    # drum C-shell skin thickness (mm) — 4mm PP over metal hoops
HOUSING_SKIN_T = 5    # housing skin thickness (mm) — 5mm UV-HDPE over metal frame
# Door-end near/far walkway brackets demountable for transport (panel slides past them):
WALKWAY_BRACKET_DEMOUNT_X = (698, 1155)   # bracket X-stations struck for transport
```

- [ ] **Step 6: Verify imports + geometry, then run the audit**

```bash
/usr/bin/python3 - <<'PY'
import sys; sys.path.insert(0,'src/generators'); import tbs_constants as c
assert c.DRUM_CX + c.DRUM_R <= c.RAIL_X_L - 90, "housing interior edge must clear X=150 rail with margin"
assert not hasattr(c, 'BRACE_LEFT_DEMOUNT_Y0'), "demountable segment constants should be gone"
print("housing interior edge X=%d ; rail X=%d ; slide=%d ; OK" % (c.DRUM_CX+c.DRUM_R, c.RAIL_X_L, c.PANEL_SLIDE))
PY
/usr/bin/python3 src/generators/check_consistency.py | tail -3
```
Expected: assertion prints OK; CHECK A may now flag the *old* values 0/550/731/1631 in not-yet-updated generators/reports — that is expected and gets cleared by later tasks (CHECK E may flag the new constants as dead until used — also expected).

- [ ] **Step 7: Commit**

```bash
git add src/generators/tbs_constants.py
git commit -m "B2 constants: offset drum to -400, slide 880, bay geometry, plastic skin, drop demountable segment"
```

---

## Phase 1 — 2D diagrams

> Pattern for every diagram task: capture md5 → edit generator → regenerate → confirm **only the intended** sheets changed → eyeball with Read → commit script+png together. The generators read `tbs_constants`, so most geometry updates automatically; edits are only where values are hardcoded or where the *representation* (e.g., the demountable segment overlay) must change.

### Task 2: `generate_film_plane_mechanism.py` — continuous left rail

**Files:**
- Modify: `src/generators/generate_film_plane_mechanism.py` (the demountable-segment overlay block, ~lines 291–313; the rail-draw loop; any `BRACE_LEFT_DEMOUNT` usage)
- Output: `diagrams/film-plane-sheet1..6.png`

- [ ] **Step 1: Baseline + find usages**
```bash
md5 diagrams/film-plane-sheet*.png > /tmp/fpm_before.txt
git grep -n "BRACE_LEFT_DEMOUNT\|DEMOUNTABLE\|C_DEMOUNT\|demount" src/generators/generate_film_plane_mechanism.py
```

- [ ] **Step 2: Remove the demountable-segment overlay + label**

Delete the demountable-segment overlay block (the `C_DEMOUNT` rectangle at Yd 731–1631 and its leader/label, ~lines 295–313) and any drum-mode note that references "left-rail segment swung clear". The left rail draws as one continuous member from `D_NEAR` to `D_FAR`. Remove the now-unused `C_DEMOUNT` local and any `BRACE_LEFT_DEMOUNT_*` import.

- [ ] **Step 3: Regenerate + confirm scope**
```bash
PATH=/usr/bin:$PATH /usr/bin/python3 src/generators/generate_film_plane_mechanism.py
md5 diagrams/film-plane-sheet*.png > /tmp/fpm_after.txt
diff /tmp/fpm_before.txt /tmp/fpm_after.txt   # expect sheet1 (+ any sheet drawing the segment) changed; others identical
```

- [ ] **Step 4: Eyeball**

Read `diagrams/film-plane-sheet1.png` — confirm the left rail is one continuous member (no amber/red demountable band, no "swung clear" leader).

- [ ] **Step 5: Commit**
```bash
git add src/generators/generate_film_plane_mechanism.py diagrams/film-plane-sheet*.png
git commit -m "film-plane: left rail continuous (demountable segment removed, B2)"
```

### Task 3: `generate_hingepanel_diagram.py` — punch-out bay, hinge upgrade, seals

**Files:**
- Modify: `src/generators/generate_hingepanel_diagram.py`
- Output: `diagrams/hingepanel-sheet1..N.png`

- [ ] **Step 1: Baseline + inventory the sheets**
```bash
md5 diagrams/hingepanel-sheet*.png > /tmp/hp_before.txt
grep -nE "def draw_sheet|savefig|DRUM_CX|PANEL_SLIDE|protrud|hinge" src/generators/generate_hingepanel_diagram.py | head -40
```

- [ ] **Step 2: Redraw the panel section as a forward bay**

In the plan/section views, draw the center zone (Yd `PANEL_CORNER_YD_L..R`) as a forward-protruding box from `BAY_BACK_X` (0) to `BAY_FRONT_X` (−890), `BAY_WALL_T` walls, with the housing inside at the offset `DRUM_CX`. Side zones stay at the door plane. Update any hardcoded housing X (was centered at 0) to read `DRUM_CX`. Add the bay outline + a dimension to `BAY_FRONT_X`.

- [ ] **Step 3: Upgrade the hinge + add swing-support note**

Replace the "3× 200 mm piano hinge" callout with the heavy-duty hinge callout (e.g., "3× weld-on barrel hinge, rated ≥ leaf load — STRUCTURAL SIGN-OFF") and add the retractable **swing-support caster** at the leaf far-bottom corner in the relevant elevation, plus a note block: "Bay shifts leaf CG forward; hinges carry tipping couple — see structural note."

- [ ] **Step 4: Re-map the seals**

Move the interface-1 (panel-perimeter) + interface-2 (housing-surround) EPDM seal callouts onto the bay geometry (around the bay mouth + housing surround at `BAY_FRONT_X`). Keep IP44 weather note.

- [ ] **Step 5: Regenerate + scope + eyeball**
```bash
PATH=/usr/bin:$PATH /usr/bin/python3 src/generators/generate_hingepanel_diagram.py
md5 diagrams/hingepanel-sheet*.png > /tmp/hp_after.txt; diff /tmp/hp_before.txt /tmp/hp_after.txt
```
Read each changed sheet; confirm the bay reads correctly, hinge callout updated, seals on the bay.

- [ ] **Step 6: Commit**
```bash
git add src/generators/generate_hingepanel_diagram.py diagrams/hingepanel-sheet*.png
git commit -m "hingepanel: punch-out bay + heavy hinge + swing caster + re-mapped seals (B2)"
```

### Task 4: `generate_lighttrap_diagram.py` — offset + bay in the LT sheets

**Files:**
- Modify: `src/generators/generate_lighttrap_diagram.py`
- Output: `diagrams/lighttrap-sheet1..N.png`

- [ ] **Step 1: Baseline**
```bash
md5 diagrams/lighttrap-sheet*.png > /tmp/lt2d_before.txt
grep -nE "DRUM_CX|PANEL_SLIDE|protrud|exterior face|housing" src/generators/generate_lighttrap_diagram.py | head
```

- [ ] **Step 2: Update housing/bay X + transport positions**

Drive housing X from `DRUM_CX` and the protrusion/transport callouts from `PANEL_SLIDE`/`BAY_FRONT_X` (replace any hardcoded −450/550/X≈1000). Update the "drum protrudes …" text to the new ~890 mm and the transport slid position.

- [ ] **Step 3: Regenerate + scope + eyeball + commit**
```bash
PATH=/usr/bin:$PATH /usr/bin/python3 src/generators/generate_lighttrap_diagram.py
md5 diagrams/lighttrap-sheet*.png > /tmp/lt2d_after.txt; diff /tmp/lt2d_before.txt /tmp/lt2d_after.txt
git add src/generators/generate_lighttrap_diagram.py diagrams/lighttrap-sheet*.png
git commit -m "lighttrap 2D: housing offset + bay + new slide (B2)"
```

### Task 5: `generate_floorplan_diagram.py` — drum/bay footprint

**Files:**
- Modify: `src/generators/generate_floorplan_diagram.py`
- Output: `diagrams/floorplan*.png`

- [ ] **Step 1: Baseline + edit**

`md5` the floorplan png(s). Confirm the drum/housing footprint is driven by `DRUM_CX`/`DRUM_R` (update if hardcoded). The freed interior space and the bay protrusion should show.

- [ ] **Step 2: Regenerate + scope + eyeball + commit**
```bash
PATH=/usr/bin:$PATH /usr/bin/python3 src/generators/generate_floorplan_diagram.py
# diff md5; Read the png; confirm drum footprint moved out, interior freed
git add src/generators/generate_floorplan_diagram.py diagrams/floorplan*.png
git commit -m "floorplan: light-lock footprint offset out (B2)"
```

### Task 6: `generate_walkway_diagram.py` — door-end brackets demountable for transport

**Files:**
- Modify: `src/generators/generate_walkway_diagram.py`
- Output: `diagrams/walkway-sheet*.png`

- [ ] **Step 1: Baseline + edit**

`md5` the walkway sheets. On the top-down sheet, mark the brackets at `WALKWAY_BRACKET_DEMOUNT_X` (698, 1155) on both near + far walls as **demountable for transport** (distinct hatch/color + a note: "struck for transport — panel slides to X≈1000"). Add to the transport-sequence note if present.

- [ ] **Step 2: Regenerate + scope + eyeball + commit**
```bash
PATH=/usr/bin:$PATH /usr/bin/python3 src/generators/generate_walkway_diagram.py
# diff md5; Read changed sheet
git add src/generators/generate_walkway_diagram.py diagrams/walkway-sheet*.png
git commit -m "walkway: mark door-end brackets demountable for transport (B2)"
```

---

## Phase 2 — 3D models

> **CRITICAL:** before every `--send`, run the active-doc gate. Send the operating model only into its own `.skp`. Build into a BLANK doc for any model whose `.skp` you do not want cleared. Pattern:
> ```bash
> path=$(/usr/bin/python3 -c "import sys;sys.path.insert(0,'src/models');from sketchup_client import send_ruby;print(send_ruby('Sketchup.active_model.path'))")
> [[ "$path" == */<expected>.skp ]] && echo GATE-OK || echo "STOP: active=$path"
> ```

### Task 7: `generate_sketchup_model.py` (overview)

**Files:**
- Modify: `src/models/generate_sketchup_model.py` — `film_plane_mechanism()` (continuous left rail: delete the 3-segment split + `C_DEMOUNT`/`BRACE_LEFT_DEMOUNT` use), the light-trap/housing builders (offset `DRUM_CX`, bay box, plastic skin color/thickness), `walkways()`/`walkway_brackets()` (mark the door-end brackets demountable), and the panel/hinge representation (heavy hinge + swing caster).
- Output: `src/models/overview.rb`, `models/overview.skp`

- [ ] **Step 1: Build-check (non-interactive)**
```bash
PATH=/usr/bin:$PATH /usr/bin/python3 src/models/generate_sketchup_model.py --save
rb=src/models/overview.rb
grep -c 'DEMOUNTABLE' $rb        # expect 0 (left-rail segment gone)
grep -c 'FP Rail .L (fixed' $rb  # expect continuous left rails (no 3-way split names)
```

- [ ] **Step 2: Implement** the continuous left rail (single `FP Rail BL`/`TL` per side spanning `y0..y_end`), the bay box around the offset housing, the plastic-colored skin (use a new `C_PLASTIC` or existing drum color + note), and the door-end demountable-bracket tagging.

- [ ] **Step 3: Re-build-check** the `.rb` greps above pass; no Python exception.

- [ ] **Step 4: Gate + send + save + verify**
```bash
# gate on overview.skp, then:
PATH=/usr/bin:$PATH /usr/bin/python3 src/models/generate_sketchup_model.py --send
/usr/bin/python3 -c "import sys;sys.path.insert(0,'src/models');from sketchup_client import send_ruby; import os; \
print(send_ruby('m=Sketchup.active_model; %Q{saved=#{m.save('+repr(os.path.abspath('models/overview.skp'))+')}}'))"
# verify: housing offset, continuous rails (no demountable groups)
```

- [ ] **Step 5: Consistency audit + commit**
```bash
/usr/bin/python3 src/generators/check_consistency.py | sed -n '/CHECK/p'
git add src/models/generate_sketchup_model.py src/models/overview.rb models/overview.skp
git commit -m "overview 3D: B2 bay + continuous left rails + plastic skin + demountable door brackets"
```

### Task 8: `generate_lighttrap_model.py` (operating)

**Files:**
- Modify: `src/models/generate_lighttrap_model.py` — `drum()`/housing (offset + plastic skin), `hinge_panel()` (the bay box + heavy hinge + caster), `film_plane_left()` (rewrite to continuous rails — see Step 2), the housing-surround seal (follow the bay offset), and the `door_frame()`/EPDM seal positions.
- Output: `src/models/lighttrap.rb`, `models/lighttrap.skp`

- [ ] **Step 1: Build-check** `--save`; grep the `.rb` for the bay parts + offset (housing groups at negative X around `DRUM_CX`).
- [ ] **Step 2: Rewrite `film_plane_left()` to continuous rails.** Delete the `d0/d1` demountable-segment split, the `demount` parameter, and the amber `C_DEMOUNT` segment logic entirely (the `BRACE_LEFT_DEMOUNT*` constants are gone). It now builds one full-length `FP Rail BL` + one `FP Rail TL` (`yN..yF`) plus the brace beams/posts. Update the lt caller from `film_plane_left(demount=True)` to `film_plane_left()`. Then implement the bay, offset, plastic skin, heavy hinge + caster, and re-map the housing-surround seal onto the offset housing.
- [ ] **Step 3: Gate on `lighttrap.skp` → `--send --skp` → verify** (housing groups offset to ~−400; left rails continuous; bay present).
- [ ] **Step 4: Commit** `git add` the generator + `.rb` + `.skp`; `-m "lighttrap 3D: punch-out bay + offset + continuous rails + plastic skin (B2)"`.

### Task 9: `generate_lighttrap_transport_model.py` (transport)

**Files:**
- Modify: `src/models/generate_lighttrap_transport_model.py` — the slide (`SLIDE = ov.PANEL_SLIDE` is now 880 automatically), drop the `Film-Plane Rails` component (rails struck for transport), drop the door-end walkway brackets, and let the deeper slide follow from the new constant.
- Output: `src/models/lighttrap-transport.rb`, `models/lighttrap-transport.skp`

- [ ] **Step 1: Build-check** `--save`; grep: moving-tag parts translate by `880.mm`; no `FP Rail` groups (struck); no door-end bracket groups.
- [ ] **Step 2: Implement** — remove the `Film-Plane Rails (left, partial)` component + its tag from the transport assembly (rails struck for transport); have `walkways_partial()` omit the door-end brackets at `WALKWAY_BRACKET_DEMOUNT_X` (or note they aren't drawn in this partial); the slide picks up 880 from `lt.PANEL_SLIDE`. Keep the ghost-container `x_far` crop aligned.
- [ ] **Step 3: Gate on a BLANK doc (do NOT clobber lighttrap/overview) → `--send --skp` → verify** the slid envelope reaches ~X=1000 and clears (no left rails, no door-end brackets present).
- [ ] **Step 4: Commit** generator + `.rb` + `.skp`; `-m "lighttrap-transport 3D: deeper slide, left rails + door-end brackets struck (B2)"`.

---

## Phase 3 — Reports, weight/CG, shopping & cost

### Task 10: `hinged-panel-report.md`

**Files:** Modify: `hinged-panel-report.md`

- [ ] **Step 1:** Add a "Punch-out bay (rev 9)" subsection: the bay geometry (offset −400, bay to `BAY_FRONT_X`), why (clears the X=150 rail), the freed interior space.
- [ ] **Step 2:** Update the hinge spec (heavy-duty, ~316 kg leaf + tipping couple), add the swing-support caster, the three load cases (hung cantilever / swung open / slide), and an explicit "STRUCTURAL SIGN-OFF REQUIRED" note for hinge + suspension + caster sizing.
- [ ] **Step 3:** Update the protrusion table (was 295–450 mm → ~890 mm) and the transport slide (550 → 880) + the door-end-bracket-demount + left-rails-struck transport steps.
- [ ] **Step 4:** Update embedded diagram references if sheet content moved. Add hyperlinked sources for any new spec'd hardware. **Use American spelling.**
- [ ] **Step 5: Commit** `-m "hinged-panel-report: punch-out bay, heavy hinge, swing caster, new transport sequence (B2)"`.

### Task 11: `light-trap-selection.md` — plastic-skin material

**Files:** Modify: `light-trap-selection.md`

- [ ] **Step 1:** Add the hybrid-skin decision (metal end-caps/hoops/bearings + 4 mm PP drum / 5 mm UV-HDPE housing skins), with the caveats from spec §4.5 (stiffness via hoops, thermal running-clearance, light-tightness, UV/creep/FR). Link datasheets (hyperlinked sources).
- [ ] **Step 2: Commit** `-m "light-trap-selection: hybrid plastic-skinned drum/housing (B2)"`.

### Task 12: `weight-distribution-report.md` + `generate_weight_analysis.py` — re-run CG

**Files:** Modify: `src/generators/generate_weight_analysis.py`, `weight-distribution-report.md`; Output: `diagrams/weight-analysis-sheet*.png`

- [ ] **Step 1:** In the mass model, update the hinged-panel + drum entries: lighter skins (drum 63 → ~45 kg, housing line ~36 → ~25 kg, first-principles per spec §4.5), add the bay structure (~+15 kg) + heavier hinges/caster (~+20 kg), and the new deployed/transport X positions (deployed bay forward, transport slid to ~X=1000).
- [ ] **Step 2:** Regenerate; read the printed CG; confirm operating shift toward the door < ~25 mm and transport shift rearward < ~25 mm (spec §4.8). If a number moves materially, reconcile the report's §6 CG/axle narrative.
- [ ] **Step 3:** `md5`-diff the weight-analysis sheets (expect changes); update the report's CG table + narrative + any quoted figures.
- [ ] **Step 4: Commit** generator + report + sheets; `-m "weight-distribution: re-run CG for B2 bay + lighter plastic skins"`.

### Task 13: `master-shopping-list.md` + `project-cost-breakdown.md` + structural note

**Files:** Modify: `master-shopping-list.md`, `project-cost-breakdown.md`; (optional) add a short structural note to `hinged-panel-report.md` or a new `docs`-level note.

- [ ] **Step 1:** Shopping list: swap aluminum drum/housing skin → PP/HDPE sheet (qty m², 2+ SoCal suppliers, part #s, current prices, hyperlinked); add heavy-duty hinges, the swing caster, demountable-bracket hardware (quick-release pins); drop the demountable-segment ball-lock pins.
- [ ] **Step 2:** Cost-breakdown: reconcile the light-trap + film-plane lines and subtotals to match the shopping list (spec rule: any drawing-spec change updates parts list + shopping + cost in the same pass). Note net weight/cost delta.
- [ ] **Step 3: Commit** `-m "shopping + cost: plastic skins, heavy hinges, swing caster, demountable brackets (B2)"`.

---

## Phase 4 — Audit, full regen, publish

### Task 14: Consistency audit, diagram sweep, publish

- [ ] **Step 1: Consistency audit** — `/usr/bin/python3 src/generators/check_consistency.py`. CHECK A must be clear of the *old* literals (0/550/731/1631/−450) in labels/comments; CHECK E must show no newly-dead constants (the new ones are now used); CHECK F clean. Fix any flagged stragglers.
- [ ] **Step 2: Full diagram sweep** — regenerate every `generate_*.py` that writes to `diagrams/`; `git status --short -- '*.png'` should show **only** the B2-affected sheets changed. Investigate any unexpected change.
- [ ] **Step 3: Update `component-dependency-map.md`** — drum/bay geometry, continuous rails, the three models, the new transport sequence.
- [ ] **Step 4: Publish** — `PATH=/usr/bin:$PATH bash publish.sh`; confirm "Deployed".
- [ ] **Step 5: Final commit** of any map/doc stragglers; leave `lighttrap-refactor` ready for review. **Do not merge to `main` without explicit permission.**

---

## Notes for the implementer
- The drum/housing **plastic skins, hinge, suspension, and swing caster are modelled + specified here but require structural sign-off** before fabrication — the plan produces the design representation, not the FEA. Flag these clearly in the reports.
- Re-confirm the **exact offset** with the project owner if the ~890 mm protrusion proves awkward at the site (300 mm is the geometric minimum; 400 mm offset is the nominal here).
- Sketchfab re-uploads of the changed `.skp`s are the owner's **manual** step (overview, lighttrap, lighttrap-transport).
