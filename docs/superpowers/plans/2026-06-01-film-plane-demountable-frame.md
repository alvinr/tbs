# Film-Plane Demountable Brace Cage — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update the TBS-001 2D engineering generators so the film-plane mechanism is a demountable rigid brace cage that clears the light-trap drum and the walkways, per the approved spec.

**Architecture:** The four corner rails gain a saddle/thumbscrew portal frame at each end (a knock-down rigid box); the left-rail segment across the drum demounts for "drum mode"; the conflicting perimeter walkway is dropped so the cage bottom sits above the walking surface. Changes are to matplotlib diagram generators in `src/generators/`, driven by shared constants in `tbs_constants.py`, plus the report parts list / shopping list / cost breakdown.

**Tech Stack:** Python 3, matplotlib (Agg backend). Generators are standalone scripts that `savefig` PNGs into `diagrams/`. No unit-test harness — verification is "generator runs clean + PNG regenerates + visual check."

**Reference:** Spec at `docs/superpowers/specs/2026-06-01-film-plane-demountable-frame-design.md`. Read it before starting.

---

## File structure

| File | Responsibility | Change |
|---|---|---|
| `src/generators/tbs_constants.py` | Shared spatial constants | Add brace-cage + demount + park constants |
| `src/generators/generate_film_plane_mechanism.py` | 6-sheet mechanism drawings | Draw brace cage (both portals) + demountable left segment + modes + BOM |
| `src/generators/generate_walkway_diagram.py` | Walkway drawings | Remove perimeter sections inside the cage envelope |
| `src/generators/generate_lighttrap_diagram.py` | Light-trap / drum drawing | Show drum-mode clearance + swing-away left rail |
| `src/generators/generate_floorplan_diagram.py` | Floor plan | Reflect dropped walkway + demountable left rail note |
| Film-plane report `.md` (locate) | Parts list | Add brace-cage BOM |
| `master-shopping-list.md` | Shopping list | Add RHS + saddles + thumbscrews/pins, SoCal sourcing |
| `project-cost-breakdown.md` | Cost breakdown | Add brace-cage line items |

**Working branch:** `film-plane-demountable-frame` (already created off `main`). Do not merge or deploy.

---

### Task 1: Add brace-cage constants

**Files:**
- Modify: `src/generators/tbs_constants.py` (append after the film-plane / rail constants block, near `RAIL_OFF`)

- [ ] **Step 1: Read the existing rail/drum constants**

Read `src/generators/tbs_constants.py` and locate `RAIL_X_L`, `RAIL_X_R`, `RAIL_OFF`, `FP_Y`, `FP_Y_MIN`, `DRUM_D`, `DRUM_R`, `C_WID`, `C_HGT`. Confirm: `RAIL_X_L=150`, `RAIL_X_R=4649`, `RAIL_OFF=100`, `FP_Y=2262`, `FP_Y_MIN=100`, `DRUM_R=375`, `C_WID=2362`, `C_HGT=2388`.

- [ ] **Step 2: Add the constants**

Add this block immediately after the rail constants (after the `RAIL_OFF` line):

```python
# ── Film-plane demountable brace cage (rev: rigidity + drum + walkway) ────────
BRACE_RHS   = 50                     # brace member section 50×50×3mm RHS (mm)
BRACE_T     = 3                      # RHS wall thickness (mm)
BRACE_Z_BOT = RAIL_OFF               # 100mm — bottom cross-beam Z (above tray rim)
BRACE_Z_TOP = C_HGT - RAIL_OFF       # 2288mm — top cross-beam Z
# End portals sit at the rail travel limits (already defined): FP_Y_MIN, FP_Y.

# Light-trap drum Yd extent → the left-rail segment that must demount for the drum.
DRUM_CY     = C_WID // 2             # 1181mm — drum centre in Yd (= container width centre)
BRACE_LEFT_DEMOUNT_Y0 = DRUM_CY - DRUM_R   # 806mm — demountable left-rail segment start
BRACE_LEFT_DEMOUNT_Y1 = DRUM_CY + DRUM_R   # 1556mm — demountable left-rail segment end
CARRIAGE_PARK_Y       = FP_Y               # 2262mm — carriage park for drum mode (> 1556 ⇒ clears drum)
```

- [ ] **Step 3: Verify values and clearance relationships**

Run:
```bash
cd /Users/alvinrichards/dev/tbs && python3 -c "
import sys; sys.path.insert(0,'src/generators')
import tbs_constants as c
assert (c.BRACE_RHS, c.BRACE_T) == (50, 3)
assert c.BRACE_Z_BOT == 100 and c.BRACE_Z_TOP == 2288
assert c.DRUM_CY == 1181
assert c.BRACE_LEFT_DEMOUNT_Y0 == 806 and c.BRACE_LEFT_DEMOUNT_Y1 == 1556
assert c.CARRIAGE_PARK_Y > c.BRACE_LEFT_DEMOUNT_Y1   # park clears drum
# left rail (X=150) intersects drum where |Yd-1181| <= sqrt(375^2-150^2)=343.7 -> 837..1525
import math; half = math.sqrt(c.DRUM_R**2 - c.RAIL_X_L**2)
assert c.BRACE_LEFT_DEMOUNT_Y0 <= 1181-half and c.BRACE_LEFT_DEMOUNT_Y1 >= 1181+half  # demount span covers conflict
print('constants OK')
"
```
Expected: `constants OK`

- [ ] **Step 4: Commit**

```bash
git add src/generators/tbs_constants.py
git commit -m "constants: add film-plane brace-cage + demount + carriage-park values"
```

---

### Task 2: Draw the brace cage on the film-plane mechanism sheets

The brace cage = at each end portal (pinhole Yd=`FP_Y_MIN`=100, film Yd=`FP_Y`=2262): left vertical at `RAIL_X_L`, right vertical at `RAIL_X_R` (Z `BRACE_Z_BOT`→`BRACE_Z_TOP`), a top cross-beam at `BRACE_Z_TOP` and a bottom cross-beam at `BRACE_Z_BOT`, each spanning `RAIL_X_L`→`RAIL_X_R`. Members are `BRACE_RHS` (50mm) RHS.

**Files:**
- Modify: `src/generators/generate_film_plane_mechanism.py`

- [ ] **Step 1: Read the generator and identify the views that must show the cage**

Read `src/generators/generate_film_plane_mechanism.py`. Note the sheet functions:
- Sheet 1 `def …` — plan view (top-down, X vs Yd): the two end portals appear as the two transverse (bottom/top cross-beam) lines at Yd=100 and Yd=2262 spanning X 150→4649, plus the four rails.
- Sheet 2 — side elevation (X vs Z, tilt) and plan cross-section (swing): the portal verticals + top/bottom beams appear in the X-Z elevation as a rectangle at each end.
- Sheet 6 — four-corner frame **front elevation** (Yd-Z or X-Z): this is the primary place to show the full rectangular brace cage.

Confirm which helper primitives the file already uses for steel members (e.g. `Rectangle`, `draw_dim_h`, `draw_dim_v`, `leader`, the `RAIL`/`STRUCT` colors). You will reuse them.

- [ ] **Step 2: Import the new constants**

In the `from tbs_constants import (…)` block at the top of the file, add:
`BRACE_RHS, BRACE_T, BRACE_Z_BOT, BRACE_Z_TOP, RAIL_X_L, RAIL_X_R` (omit any already imported).

- [ ] **Step 3: Add a brace-cage drawing helper**

Add a module-level helper near the other drawing helpers. It draws one rectangular portal (left/right verticals + top/bottom beams) in an X-vs-Z axes, using the existing steel color and the file's `Rectangle` import:

```python
def draw_brace_portal(ax, color, *, lw=1.4, alpha=0.9, z=6):
    """Rectangular brace portal in an X-Z axes: verticals at the rail X's,
    top/bottom cross-beams. Members are BRACE_RHS square in section."""
    s = BRACE_RHS
    # Verticals (full height between cross-beam centres)
    for xv in (RAIL_X_L, RAIL_X_R):
        ax.add_patch(Rectangle((xv, BRACE_Z_BOT), s, BRACE_Z_TOP - BRACE_Z_BOT,
                               fc=color, ec=WHITE, lw=lw, alpha=alpha, zorder=z))
    # Top and bottom cross-beams (span between the verticals)
    for zb in (BRACE_Z_BOT, BRACE_Z_TOP - s):
        ax.add_patch(Rectangle((RAIL_X_L, zb), RAIL_X_R - RAIL_X_L, s,
                               fc=color, ec=WHITE, lw=lw, alpha=alpha, zorder=z))
```
(If the relevant axes is Yd-Z rather than X-Z, mirror the same logic with the file's Yd scale — match the existing sheet's coordinate handling.)

- [ ] **Step 4: Call the cage on Sheet 6 (front elevation) and annotate**

In the Sheet 6 function, after the rails/frame are drawn, call `draw_brace_portal(ax, <steel color>)` for the front portal and add a `leader(...)` labeling it `"DEMOUNTABLE BRACE CAGE / 50×50×3 RHS / saddle + thumbscrew joints"`. Follow the existing label style in that function.

- [ ] **Step 5: Show the portals on Sheet 1 (plan) and Sheet 2 (elevation)**

- Sheet 1 (plan, X-Yd): draw the two end cross-beams as RHS-width bands at Yd=`FP_Y_MIN` and Yd=`FP_Y` spanning X `RAIL_X_L`→`RAIL_X_R`, using the existing rail-drawing style; label one `"END PORTAL (typ. 2)"`.
- Sheet 2 (X-Z elevation): call `draw_brace_portal` once (the two end portals coincide in this projection); label `"BRACE PORTAL (both ends)"`.

- [ ] **Step 6: Run the generator and verify it produces all 6 sheets**

Run:
```bash
cd /Users/alvinrichards/dev/tbs && python3 src/generators/generate_film_plane_mechanism.py && ls -la diagrams/film-plane-sheet1.png diagrams/film-plane-sheet6.png
```
Expected: no traceback; the two PNGs listed with a fresh timestamp.

- [ ] **Step 7: Visual check**

Open `diagrams/film-plane-sheet6.png` (and sheet1/sheet2). Confirm a complete rectangle (two verticals + top + bottom beam) now frames the rails, labeled as the demountable brace cage. STOP and have the reviewer confirm before continuing.

- [ ] **Step 8: Commit**

```bash
git add src/generators/generate_film_plane_mechanism.py diagrams/film-plane-sheet1.png diagrams/film-plane-sheet2.png diagrams/film-plane-sheet6.png
git commit -m "film-plane: draw demountable brace cage portals on plan/elevation/front sheets"
```

---

### Task 3: Demountable left-rail segment + two operating modes

**Files:**
- Modify: `src/generators/generate_film_plane_mechanism.py`

- [ ] **Step 1: Import demount/park constants**

Add to the import block: `BRACE_LEFT_DEMOUNT_Y0, BRACE_LEFT_DEMOUNT_Y1, CARRIAGE_PARK_Y, DRUM_CY` and `DRUM_R` (and `DRUM_CX` if needed).

- [ ] **Step 2: On Sheet 1 (plan), mark the demountable left-rail segment + drum**

In the Sheet 1 function, on the **left rail** (X=`RAIL_X_L`), render the span Yd `BRACE_LEFT_DEMOUNT_Y0`→`BRACE_LEFT_DEMOUNT_Y1` in a distinct style (e.g. dashed outline / different alpha) from the rest of the rail. Draw the drum footprint as a circle/wedge at (X=`DRUM_CX`, Yd=`DRUM_CY`) radius `DRUM_R` in a ghost style. Add a `leader` labeling the segment `"DEMOUNTABLE LEFT-RAIL SEGMENT / swings clear for DRUM MODE"`.

- [ ] **Step 3: Add an operating-modes note block**

Add (reuse the file's `draw_notes`) a note block near Sheet 1 or Sheet 4 (the spec/BOM sheet):

```
OPERATING MODES (left-rail / drum interlock)
1. FILM MODE: left-rail segment locked in. Carriage free over full travel
   (Yd 100–2262) for tilt/swing. Drum static.
2. DRUM MODE: left-rail segment swung clear (Yd 806–1556). Carriage parked
   at film end (Yd 2262). Drum free to rotate for entry/exit.
INTERLOCK: drum rotates only with carriage parked AND left segment cleared.
```

- [ ] **Step 4: Run + verify**

Run:
```bash
cd /Users/alvinrichards/dev/tbs && python3 src/generators/generate_film_plane_mechanism.py && echo OK
```
Expected: `OK`, no traceback.

- [ ] **Step 5: Visual check**

Open `diagrams/film-plane-sheet1.png`. Confirm the left rail shows a distinct demountable segment overlapping the drum footprint, with the modes note legible. STOP for reviewer confirmation.

- [ ] **Step 6: Commit**

```bash
git add src/generators/generate_film_plane_mechanism.py diagrams/film-plane-sheet1.png diagrams/film-plane-sheet4.png
git commit -m "film-plane: demountable left-rail segment + drum-mode interlock notes"
```

---

### Task 4: Drop the conflicting walkway sections

**Files:**
- Modify: `src/generators/generate_walkway_diagram.py`

- [ ] **Step 1: Read the walkway generator**

Read `src/generators/generate_walkway_diagram.py`. Identify where each perimeter section is drawn (near `WALKWAY_NEAR_YD`, far `WALKWAY_FAR_YD`, left `WALKWAY_LEFT_X`, right `WALKWAY_RIGHT_X`) and the film-mechanism envelope it overlaps (X 150–4649, Yd 100–2262).

- [ ] **Step 2: Remove / mark-removed the sections inside the cage envelope**

For the sections that fall inside the film-mechanism envelope, either delete their draw calls or render them as a ghosted "REMOVED — film-mechanism clearance" outline (prefer ghosted outline so the drawing documents *why* they're gone). Add a `leader`/note: `"WALKWAY DROPPED IN FILM-MECHANISM ZONE — see film-plane mechanism dwg; access from container ends"`.

- [ ] **Step 3: Run + verify**

Run:
```bash
cd /Users/alvinrichards/dev/tbs && python3 src/generators/generate_walkway_diagram.py && echo OK
```
Expected: `OK`, no traceback; `diagrams/walkway-sheet1.png` … regenerate.

- [ ] **Step 4: Visual check + commit**

Open the walkway sheets; confirm the conflicting sections are gone/ghosted with the clearance note. Then:
```bash
git add src/generators/generate_walkway_diagram.py diagrams/walkway-sheet*.png
git commit -m "walkway: drop perimeter sections inside the film-mechanism envelope"
```

---

### Task 5: Drum-mode clearance on light-trap + floor plan

**Files:**
- Modify: `src/generators/generate_lighttrap_diagram.py`
- Modify: `src/generators/generate_floorplan_diagram.py`

- [ ] **Step 1: Light-trap — show the swing-away left rail and clearance**

In `generate_lighttrap_diagram.py`, add an annotation/ghost showing the film-plane left rail's demountable segment relative to the drum, with a note: `"FILM LEFT-RAIL SEGMENT SWINGS CLEAR FOR DRUM ROTATION (drum mode)"`. Keep the existing drum geometry unchanged.

- [ ] **Step 2: Floor plan — reflect dropped walkway + left-rail note**

In `generate_floorplan_diagram.py`, update the left-zone / walkway depiction so the dropped walkway sections match Task 4, and add a note that the film left-rail segment demounts for the drum. Reuse existing label helpers.

- [ ] **Step 3: Run + verify both**

Run:
```bash
cd /Users/alvinrichards/dev/tbs && python3 src/generators/generate_lighttrap_diagram.py && python3 src/generators/generate_floorplan_diagram.py && echo OK
```
Expected: `OK`, no traceback.

- [ ] **Step 4: Visual check + commit**

Open `diagrams/lighttrap-sheet1.png` and `diagrams/container-floorplan*.png`; confirm the drum-mode clearance and dropped-walkway notes read correctly. Then:
```bash
git add src/generators/generate_lighttrap_diagram.py src/generators/generate_floorplan_diagram.py diagrams/lighttrap-sheet*.png diagrams/container-floorplan*.png
git commit -m "lighttrap/floorplan: drum-mode left-rail clearance + dropped-walkway notes"
```

---

### Task 6: Update report parts list, shopping list, and cost breakdown

Per CLAUDE.md, drawing-spec changes must propagate to the owning report's parts list, `master-shopping-list.md`, and `project-cost-breakdown.md` in the same effort. New parts introduced by this change: **50×50×3 RHS** (brace members — 2 portals × [2 verticals + 2 beams] ≈ compute lengths), **saddle clamps** (rail-to-portal joints), **thumbscrews / locking pins** (demountable joints, incl. the left-segment swing/lock).

**Files:**
- Modify: film-plane mechanism report `.md` (locate)
- Modify: `master-shopping-list.md`
- Modify: `project-cost-breakdown.md`

- [ ] **Step 1: Locate the owning report**

Run:
```bash
cd /Users/alvinrichards/dev/tbs && grep -il "film.plane\|four-corner\|tilt.*swing" *.md
```
Use the matching report as the owning document for the mechanism parts list.

- [ ] **Step 2: Compute the brace BOM quantities**

Brace members (all 50×50×3 RHS):
- Verticals: 2 portals × 2 sides × (`BRACE_Z_TOP`−`BRACE_Z_BOT` = 2188mm) = 4 × 2188mm.
- Cross-beams: 2 portals × 2 (top+bottom) × (`RAIL_X_R`−`RAIL_X_L` = 4499mm) = 4 × 4499mm.
- Total RHS ≈ (4×2188 + 4×4499) = 26,748mm ≈ **26.8 m of 50×50×3 RHS** (round up for cuts/saddles).
Joints: count saddle clamps (≥ one per rail/beam intersection — 8 rail ends + 8 beam ends ≈ 16) and thumbscrews/locking pins (2 per demountable joint + the left-segment swing hardware).

- [ ] **Step 3: Add the parts list rows to the report**

Add brace-cage rows (ICP-XX part numbers following the existing scheme) to the report's parts table: RHS stock, saddle clamps, thumbscrews/locking pins, with quantities from Step 2 and a one-line description.

- [ ] **Step 4: Add shopping-list rows with SoCal sourcing**

In `master-shopping-list.md`, add the new parts with **2+ US/SoCal supplier options each, part numbers, and current prices** (per project rule; e.g. metal supermarkets / online metals for RHS, McMaster / fastener supplier for saddles + thumbscrews). Use real catalog links (hyperlinked, per the source-link rule).

- [ ] **Step 5: Add cost-breakdown line items**

In `project-cost-breakdown.md`, add the brace-cage line items (RHS by length, saddles, fasteners) with extended costs, and update any affected subtotal/total.

- [ ] **Step 6: Verify cross-consistency**

Run:
```bash
cd /Users/alvinrichards/dev/tbs && grep -n "RHS\|saddle\|thumbscrew\|brace" master-shopping-list.md project-cost-breakdown.md
```
Confirm the same quantities/part numbers appear in the report, shopping list, and cost breakdown.

- [ ] **Step 7: Commit**

```bash
git add <report>.md master-shopping-list.md project-cost-breakdown.md
git commit -m "reports: add brace-cage BOM to parts list, shopping list, and cost breakdown"
```

---

### Task 7: Regenerate everything, build, and final review

**Files:** none (verification only)

- [ ] **Step 1: Regenerate all affected diagrams**

Run:
```bash
cd /Users/alvinrichards/dev/tbs && for g in film_plane_mechanism walkway_diagram lighttrap_diagram floorplan_diagram; do python3 src/generators/generate_$g.py || echo "FAIL $g"; done
```
Expected: no `FAIL` lines, no tracebacks.

- [ ] **Step 2: Build the docs site locally (no deploy — feature branch)**

Run:
```bash
cd /Users/alvinrichards/dev/tbs && bash publish.sh --build
```
Expected: builds to `site/` without error. Do NOT run `bash publish.sh` (which deploys) — this is a feature branch and merge/deploy is not authorized.

- [ ] **Step 3: Final visual + spec coverage review**

Re-open the spec and the regenerated sheets side by side. Confirm: (1) brace cage on the mechanism sheets, (2) demountable left segment + modes/interlock, (3) dropped walkway, (4) drum-mode clearance on lighttrap/floorplan, (5) parts/shopping/cost updated. STOP for reviewer sign-off.

- [ ] **Step 4: Commit any regenerated PNGs not already committed**

```bash
git add diagrams/*.png && git commit -m "diagrams: regenerate after brace-cage redesign" || echo "nothing to commit"
```

---

## Notes / out of scope

- **Do not merge or deploy.** Stay on `film-plane-demountable-frame`; integration is the user's call.
- **3D Overview model re-apply** (Film Plane Mechanism + Walkway + Ceiling Rail components on the `3d-models` branch) is tracked separately — see the resume memory.
- **Walkway-accessibility reconciliation** (where operators stand once the film-zone walkway is dropped) is flagged in the spec's Dependencies; if it needs a real redesign rather than a note, raise it before finalizing Task 4.
- Right-side IBC clearance is ~25mm — if Task 2's drawing shows it tighter than acceptable, raise it before committing.
