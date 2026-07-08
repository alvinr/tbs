<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
<!-- Working/internal TODO — NOT registered in publish.sh (not published). -->
# TODO — unused-import cleanup (deferred from the 2026-06 import audit) — ✅ DONE 2026-07-05

**✅ RESOLVED.** Removed **181** unused imports across 31 generator/model files with the new stdlib
tool `src/generators/check_unused_imports.py` (`--fix`), verified every generator (2D) and model
(`--save`) runs clean with zero false positives, all drift gates green, no output changed. The tool is
now a **release gate** (`release.sh`) — re-export-aware (a name reached via `alias.NAME`, e.g. `ov.X`,
counts as used), so cruft cannot drift back in. Run `python3 src/generators/check_unused_imports.py`
to check, `--fix` to clean. *(Original note below, for history.)*

**Re-run 2026-07-07:** the EP reach re-lay + the overview→`power_core` delegation orphaned **14** imports —
`BA_X` in the electrical model, and 13 EP constants (`MPPT_*`, `FUSEBLK_W/D`, `BUSBAR_*`, `DISCONNECT_*`,
`CONTACTOR_W`, `MRBF_D/H`) in the overview hub (no longer used there since electrical's `power_core` owns
the EP internals). `--fix` removed them; all 7 models regenerate **byte-identical** (no re-send). Since the
check was only a *release* gate, these slipped past the per-commit lint — so it's now **also a `lint.py`
advisory warning** (`warn_unused_imports`, re-export-aware) that fires at commit time with the file:line + `--fix` hint.

---

`pyflakes` found **215 'imported but unused'** warnings across **29 files**. These are code-hygiene cruft (the *opposite* of a missing import — nothing is broken), deferred from the import audit so the audit could stay focused on real gaps. Clear them when convenient.

## ⚠ Read before deleting anything

Some "unused" imports are **intentional re-exports** — removing them WOULD break a consumer pyflakes can't see:

- **`src/models/generate_sketchup_model.py`** (the `ov` hub) imports constants partly to **re-export** them to the sub-models (`generate_lighttrap_model`, `generate_walkway_model`, etc. read `ov.NAME`). E.g. `PANEL_CORNER_T` is "unused" in `ov` itself but is consumed by the light-trap model via `ov.PANEL_CORNER_T`. **Verify each before removing.**

**Safe procedure per file:** remove the unused name(s) → `python3 src/generators/lint.py` (duplication + deps checks still green) → for the `ov` hub, also confirm the sub-models still import (`python3 src/models/generate_<sub>_model.py --save` runs clean) → commit.

Regenerate this list any time:

```bash
find src -name '*.py' -not -path '*__pycache__*' -print0 \
  | xargs -0 python3 -m pyflakes 2>&1 | grep 'imported but unused'
```

## Worklist (by file)

- [ ] `src/models/generate_sketchup_model.py` (42)  ⚠ **re-export hub — verify each**
      `C_WALL`, `C_PROC_ZONE`, `FP_Y_MIN`, `RAIL_LEN`, `BRACE_RHS`, `BRACE_Z_BOT`, `BRACE_Z_TOP`, `BAY_FRONT_X`, `BAY_BACK_X`, `BAY_WALL_T`, `PANEL_CORNER_T`, `PANEL_CORNER_YD_R`, `PIVOT_X`, `PIVOT_YD`, `SWING_LOCK_DEG`, `PANEL_CUT_YD`, `FAR_STRIP_YD0`, `PIVOT_POST_OD`, `PIVOT_POST_T`, `DRUM_CAGE_X0`, `DRUM_CAGE_X1`, `DRUM_CAGE_YD_L`, `DRUM_CAGE_YD_R`, `WALKWAY_NEAR_LIFTOUT_X_R`, `SPRAY_BAR_BEAM`, `SPRAY_BAR_Z_BOT`, `PUMP_X`, `PUMP_YD`, `FSKID_X`, `FSKID_YD`, `IBC_WBKT_GUSSET_H`, `PANEL_FRAME_X`, `DRUM_CX`, `DRUM_CY`, `DRUM_R`, `DRUM_H_LT`, `LT_HOUSING_R`, `LT_HOUSING_T`, `LT_DRUM_OR`, `LT_DRUM_T`, `LT_OPENING_DEG`, `FUSEBLK_H`
- [ ] `src/generators/generate_film_plane_mechanism.py` (23)
      `Polygon`, `Line2D`, `patheffects as pe`, `PH_H as PH_H_C`, `RAIL_SPAN`, `FP_ANGLE_LEG`, `FP_ANGLE_T`, `CLAMP_SPACING`, `CLAMP_BASE_W`, `CLAMP_BASE_H`, `CLAMP_BASE_T`, `CLAMP_LEVER_L`, `CLAMP_JAW_W`, `CLAMP_JAW_H`, `CLAMP_JAW_T`, `CLAMP_OPEN_GAP`, `CLAMP_SPRING_F`, `CLAMP_N_HORIZ`, `CLAMP_N_VERT`, `CLAMP_N_TOTAL`, `BRACE_RHS`, `BRACE_T`, `hatch_rect`
- [ ] `src/generators/generate_ibc_stacking_diagram.py` (20)
      `math`, `numpy as np`, `FancyArrowPatch`, `patches as mpatches`, `BROWN_IBC_Y`, `WASTE_IBC_Y`, `WALKWAY_H`, `WALKWAY_GRATE_T`, `PROC_TRAY_RIM`, `EXT_PANEL_YD`, `PANEL_FRAME_TOP_Z`, `IBC_WBKT_PLATE_T`, `IBC_WBKT_SEAT_PROJ`, `IBC_WBKT_SEAT_T`, `IBC_WBKT_GUSSET_H`, `PUMP_D`, `PUMP_YD`, `PUMP_YD_SPAN`, `FSKID_YD`, `WALL_T`
- [ ] `src/generators/generate_weight_analysis.py` (17)
      `field`, `FancyBboxPatch`, `RAIL_X_L`, `RAIL_X_R`, `RAIL_SPAN`, `RAIL_LEN`, `IBC_H_600`, `IBC_H_STK`, `PROC_TRAY_W`, `PROC_TRAY_D`, `WALKWAY_BRACKET_H`, `WALKWAY_BRACKET_T`, `WALKWAY_LEFT_SPAN`, `PANEL_CORNER_T`, `DRUM_D`, `FAN_DIAM`, `CONTAINER_RIB_SPACING`
- [ ] `src/generators/generate_water_system.py` (15)
      `patches as mpatches`, `FancyArrowPatch`, `Arc`, `Line2D`, `C_WID`, `IBC_W`, `IBC_D`, `IBC_H_1000`, `IBC_H_STK_1000`, `PH_X`, `BROWN_IBC_Y`, `WASTE_IBC_Y`, `PUMP_H_HI`, `PROC_TRAY_SHIM_N`, `C_WALL`
- [ ] `src/generators/generate_pinhole_wall_elevation.py` (14)
      `math`, `C_WID`, `PH_D`, `WALKWAY_BRACKET_H`, `PROC_TRAY_SUMP_D`, `PROC_TRAY_D`, `PROC_TRAY_PITCH`, `RAIL_OFF`, `FAN_B_H`, `FAN_B_YD`, `FAN_DIAM`, `C_WALL`, `EQPANEL_X`, `EQPANEL_W`
- [ ] `src/generators/generate_assembly_overview.py` (11)
      `PUMP_X`, `PUMP_W`, `PUMP_H_LO`, `PUMP_H_HI`, `IBC_D`, `BLUE_IBC_Y`, `BROWN_IBC_Y`, `IBC_FAR_Y`, `FAN_DIAM`, `cone_left`, `cone_right`
- [ ] `src/generators/generate_walkway_diagram.py` (10)
      `FancyBboxPatch`, `Line2D`, `C_HGT`, `WALKWAY_RIGHT_W`, `WALKWAY_LEFT_SPAN`, `IBC_H_600`, `CONTAINER_RIB_SPACING`, `LEFT_WK_CANT_POST_T`, `EVAP_H`, `patches as mpatches`
- [ ] `src/generators/generate_shelf_diagram.py` (9)
      `numpy as np`, `C_WID`, `C_HGT`, `BA_H_LO`, `BA_H_HI`, `EP_H_LO`, `EP_H_HI`, `C_STEEL`, `C_CL`
- [ ] `src/generators/generate_electrical_diagram.py` (8)
      `numpy as np`, `Arc`, `C_WASTE_IBC`, `C_BROWN_IBC`, `EQPANEL_X`, `BROWN_IBC_Y`, `DRUM_CX`, `C_LT_DRUM`
- [ ] `src/generators/generate_hingepanel_diagram.py` (6)
      `Polygon`, `Wedge`, `Line2D`, `WALKWAY_W`, `WALKWAY_BRACKET_H`, `hatch_rect`
- [ ] `src/generators/generate_ibc_frame_drawing.py` (5)
      `Polygon`, `FancyArrowPatch`, `patches as mpatches`, `C_LEN`, `hatch_rect`
- [ ] `src/generators/generate_logos.py` (5)
      `patches as mpatches`, `Wedge`, `Path`, `patheffects as pe`, `transforms`
- [ ] `src/generators/generate_lighttrap_diagram.py` (4)
      `FancyBboxPatch`, `draw_circle`, `math`, `math`
- [ ] `src/generators/generate_line_of_sight.py` (3)
      `math`, `FP_Y_MIN`, `WASTE_IBC_Y`
- [ ] `src/generators/generate_panel_layout.py` (3)
      `math`, `C_CL`, `hatch_rect`
- [ ] `src/generators/generate_spray_bar_diagram.py` (3)
      `FancyArrowPatch`, `C_ALUM`, `SPRAY_BAR_HOLE_SP`
- [ ] `src/models/generate_spraybar_model.py` (3)
      `SPRAY_BAR_BEAM_T`, `SPRAY_BAR_BORE`, `SPRAY_BAR_FEED_Z`
- [ ] `src/generators/generate_assembly_fabrication.py` (2)
      `IBC_FAR_Y`, `FAN_A_YD`
- [ ] `src/generators/generate_floorplan_diagram.py` (2)
      `FancyArrowPatch`, `Line2D`
- [ ] `src/generators/generate_tilt_swing_diagram.py` (2)
      `bolt_holes`, `hatch_rect`
- [ ] `src/generators/generate_film_plane_distortion.py` (1)
      `Rectangle`
- [ ] `src/generators/generate_logo_final.py` (1)
      `Arc`
- [ ] `src/generators/generate_mini_tbs_diagram.py` (1)
      `numpy as np`
- [ ] `src/generators/generate_plate_drawing.py` (1)
      `hatch_rect`
- [ ] `src/generators/generate_portrait_viz.py` (1)
      `os`
- [ ] `src/generators/generate_schematic.py` (1)
      `os`
- [ ] `src/generators/setup_docs.py` (1)
      `os`
- [ ] `src/models/generate_electrical_model.py` (1)
      `FUSEBLK_H`

*Related lower-priority hygiene from the same pyflakes run (not import-related): 126 empty f-strings (`f"..."` with no `{}`), 18 redefinitions. Out of scope here.*
