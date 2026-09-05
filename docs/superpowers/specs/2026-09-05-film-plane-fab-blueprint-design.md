<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Film Plane — Fabrication Blueprint (design spec)

**Date:** 2026-09-05
**Status:** design approved (audit + scope), pending spec review → implementation plan
**Owner:** Alvin Richards

## 1. Purpose

Elevate the film-plane drawing set from *mechanism-design* level (how it moves,
key joints) to a **shop-buildable fabrication blueprint** — the same standard the
hinged-panel (16 sheets) and light-trap sets already reached. A metal shop and a
carpenter should be able to build every film-plane part from the sheets alone: cut
lengths, section profiles, hole tables, weld schedules, fastener callouts with edge
distances.

The mechanism **design is settled** and is NOT reopened here: fixed-size rigid 6061
frame, four acetal skates on 6061 U-channel depth rails, 2-axis 304 cross-slides on
UHMW pads with brass-tip gibs, one Belden SSNBUJ750x3/8KB U-joint per corner through
a 304 corner plate. This spec adds *fabrication detail*, reconciles the existing
sheets, and clears the open audit flags. No geometry change is intended; if triage
forces one, it is handled through the normal constant→cascade→3D path with Alvin's
sign-off.

## 2. Current state (audit, 2026-09-05)

- **11 sheets** on `main` (`film-plane-sheet1–11`), one generator
  `src/generators/generate_film_plane_mechanism.py` (~158 KB): plan/elevation GA
  (1,2,7), corner mechanism master (3), U-joint sections (4), movement+BOM (5),
  muslin clamp (6), frame↔cross-slide (8), frame↔U-joint↔X-slide (9), corner load
  case (10), far-left rail bracket (11).
- **3D model** `film-plane-mechanism.skp` (UID 572b4aaa…), model generator
  `src/models/generate_film_plane_mechanism_model.py`, refined through 2026-09-04.
- **27 film parts** in `parts.py` (mostly firm-priced); 5 supporting reports.
- All part dimensions already exist as constants in `tbs_constants.py`
  (`FP_RAIL_*`, `SKATE_*`, `XSLIDE_*`, `UJOINT_*`, `CAM_CLAMP_*`, `CARRIAGE_*`,
  `FP_CORNER_SEAT_*`, `CLAMP_*`).

**Open flags this blueprint closes:**

1. **4 dead constants** (`SKATE_AXLE_LEN`, `SKATE_ROLLER_W`, `UJOINT_YOKE_L`,
   `XSLIDE_STROKE`) — defined with real values but drawn nowhere. The new detail
   sheets consume them; the `check_consistency.py` flag clears.
2. **~164 OPEN interference flags** in the corner mechanism (U-rail↔depth-rail,
   cross-slides, gibs, UHMW pads, skate/U-joint) — triaged seated-vs-real here.
3. **Frame-corner bolt 7<9 edge-distance** in the X-slide shaft support.
4. **Label defects**: 10 over-reaching labels on the mechanism sheets +
   `CARRIAGE_YD_CENTER` label landing outside its section panel.
5. **Stale comment literals** in `tbs_constants.py` (`FP_W = 4499`, `PH_X = 2399`,
   `RAIL_SPAN = 4499` — superseded by the 4389 / 2454 pivot-hub revision).
6. **`film-plane-mechanism-analysis.md`** scope note ("PROSE DONE, BOM GATED");
   **EPDM foam-tape** qty revisit.

## 3. Scope decisions (locked with Alvin)

- **One generator** — extend `generate_film_plane_mechanism.py` with sheets 12+
  (continuous numbering, shared helpers, one `dependencies.yml` output group).
  Function names track sheet numbers (`sheet12()` draws "SHEET 12").
- **Triage in-scope** — the ~164-flag interference triage is Phase 0 of this run.
- **One part per sheet** — big weldments/parts each get their own sheet; genuinely
  small hardware may share a sheet with Detail A–F callouts where that reads better.

## 4. Sheet set

Existing 1–11 are retained and reconciled. New per-part fabrication sheets, ordered
by build sequence:

| Sheet | Part | Draws from | Notes |
|-------|------|-----------|-------|
| **12** | Depth rail (3×1½ 6061 U-channel) | `FP_RAIL_WEB/FLANGE`, `RAIL_LEN` | Cut length + section; two variants — fixed-R flanged, drop-in-L; wall-seat flange hole pattern |
| **13** | Acetal skate | `SKATE_ROLLER_OD/KEEPER_OD/W`, `SKATE_AXLE_OD/LEN`, `SKATE_ROLLER_SP`, `CARRIAGE_*` | 4-wheel roller/axle layout; carriage-plate bores. **Wires `SKATE_AXLE_LEN`, `SKATE_ROLLER_W`** |
| **14** | Cam clamp / rail brake | `CAM_CLAMP_BASE_W/D`, `CAM_CLAMP_HOLE_SP`, `CAM_CLAMP_N` | Cam-lever detail, 2× M4 base holes, ×3/corner |
| **15** | Cross-slide stack (Z + X) | `XSLIDE_*_BAR_LEN`, `XSLIDE_BAR_W/T`, `XSLIDE_GIB_*`, `XSLIDE_UHMW_T`, `XSLIDE_CARR_WALL`, `XSLIDE_STROKE` | Deep-mount orientation (load-case decision); gib + UHMW pads. **Wires `XSLIDE_STROKE`** |
| **16** | U-joint install | `UJOINT_OD/LEN/YOKE_L/HUB_L/BOOT_*`, `UJOINT_STUB_OD` | Belden SSNBUJ750x3/8KB; 3/8 stub keyseat, 4040N12 supports, keys. **Wires `UJOINT_YOKE_L`** |
| **17** | 304 corner plate + carriage plates L/R | `CARRIAGE_PLATE_W/H/T`, `CARRIAGE_AXLE_ROW_SP` | Hole pattern, thickness, plate geometry |
| **18** | Film-plane frame weldment | `FP_W`, `FP_H`, `FP_ANGLE_*`, `DIBOND_T` | 2×2×1/8 6061 angle, coped corners, weld schedule, ACM backing, corner-plate bolt holes |
| **19** | Wall-seat saddles | `FP_CORNER_SEAT_*` | 8/10 mm plate cuts + weld; flange hole pattern |
| **20** | Assembly / exploded + fastener schedule | (all) | Full fastener callouts with edge distances (M4/M6/M8/M12) |

Muslin clamp fab detail is folded into a **reconcile of existing Sheet 6** (add cut
list / clamp-spacing table) rather than a new sheet, to avoid duplication.

Total after this run: ~20 sheets.

## 5. Approach

**Phase 0 — Groundwork**
Read the 6 diagram/report skills. Confirm the 4 dead-constant values against the
subsystem reports, wire them into the new sheets. Triage the ~164 interference flags
(seated → annotate; real → fix, escalating any that need a geometry change). Resolve
the bolt 7<9 edge-distance. Sweep the stale comment literals in `tbs_constants.py`.

**Phase 1 — Per-part sheets (12–20)**
For each: draw purely from constants (no hardcoded literals in labels; every
`draw_dim_*` carries an explicit `mm`), verify the drawn geometry against the live
`film-plane-mechanism.skp` via read-only `eval_ruby` bounds/position queries, then
`tidy_labels.py --fix` + a rendered crop-zoom visual pass. Fasteners follow
`skill_fastener_convention` (rivnut/bolt sign convention, edge distance, grip).

**Phase 2 — Reconcile 1–11**
Fix the 10 over-reaching labels + `CARRIAGE_YD_CENTER` overflow; unify title blocks
across the enlarged set; cross-reference the new detail sheets from the GA sheets;
update the report narrative (analysis scope note, EPDM qty); single-source any new
dimension as a constant/fact where it would otherwise be restated.

**Phase 3 — Cascade & register**
`parts.py` new fab lines under the material-now/fab-later rule → `--inject` /
`--check`; `costing.py --check-registry`; register the new PNGs in
`dependencies.yml`, `all-diagrams.md` (gallery audit must come back empty),
`mkdocs.yml`, `setup_docs.py`, `docs/index.md`, `publish.sh`. Run `lint.py`,
`editorial_lint.py`, `check_consistency.py`, `check_interference.py --bolts`,
`tidy_labels`. Add a `RELEASE.md [Unreleased]` bullet.

**Phase 4 — 3D + publish**
Only if a triage fix changed a constant/geometry: drive re-runs from
`lint.py --cascade <CONST>`, regenerate `film-plane-mechanism` **and** `overview`,
`--send` focus-first into the film-plane doc (verify the live doc matches first;
Alvin saves + re-uploads to Sketchfab), `manifest.py --update`, commit the `.skp`
after Alvin confirms "saved + uploaded". Then `publish.sh`.

## 6. Testing / verification

- **Per sheet:** renders clean; labels pass `tidy_labels` static + visual gate;
  every dimension carries `mm`; no numeric literal in a label that should reference a
  constant; SPDX header present.
- **Gates (all must pass before commit):** `lint.py` (cascade, dependencies,
  license, missing-cascade byte-diff), `editorial_lint.py`, `check_consistency.py`,
  `check_interference.py --bolts`, gallery audit `comm` returns empty.
- **Registry invariant:** `parts.py --check` and `costing.py --check-registry` both
  green.
- **3D:** each new detail sheet's dimensions reconciled against live-model bounds
  (read-only) before the sheet is called done.

## 7. Out of scope

- No redesign of the mechanism (design settled).
- No new 3D geometry unless a triage fix demands it (then constant→cascade→send with
  Alvin's sign-off; `.skp` is single-writer — Alvin saves).
- Fab-labor quotes stay deferred (material-now/fab-later); this blueprint is what
  unblocks them later.

## 8. Risks / open questions

- **Interference triage volume** (~164 flags) could surface a real clash needing a
  geometry change mid-run — that upgrades a slice to a 3D cascade. Handled by
  escalating to Alvin, not by silently editing the live model.
- **Sheet 6 muslin** reconcile vs a dedicated sheet — decide once the clamp cut list
  is drawn; fall back to a new sheet only if Sheet 6 gets too dense.
- **`XSLIDE_STROKE` (300) vs computed travel** (Z 245 / X 263) — confirm the 300
  spec is the intended drawn stroke on Sheet 15, not a stale over-spec.
