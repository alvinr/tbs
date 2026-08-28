<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Design — Hinged Panel: HDPE Surround Fabrication Set (`hingepanel-bp`)

**Date:** 2026-08-27
**Branch:** `hingepanel-bp`
**Status:** approved for planning

## 1. Purpose

The hinged light-trap panel already has a 6-sheet blueprint set + report (`hinged-panel-report.md`,
`src/generators/generate_hingepanel_diagram.py`). This round completes the **HDPE surround** — the
1/8″ HDPE that wraps the panel center zone around the Ø800 revolving-door housing — which currently
has **no fabrication cut sheets**, reads as **disconnected from the steel frame** in the 3D model,
and carries **stale drum geometry** left by the earlier Ø900→Ø800 / drum-height resize.

## 2. Background / current geometry (verified)

- Center zone: **1,056mm wide × 120mm thick**, framed in 2×2×0.120″ (50.8mm) steel RHS, skinned both
  faces in **1/8″ HDPE**.
- The **Ø800 housing** (`DRUM_D=800`, `DRUM_R=400`) is larger than the 120mm zone, so the drum
  **overhangs both panel faces** (~850mm exterior, ~210mm interior per Sheet 2).
- The **surround** = the HDPE that closes the center-zone opening around that bulging drum: the
  front + back skins (each with the Ø836 aperture, `APERTURE_R = HOUSING_R + 18 = 418`), plus the
  **upper and lower "floor"** — the horizontal HDPE caps that close the top and bottom of the
  exterior/interior drum bulge where they meet the Ø800 housing. The drum's **cylindrical faces stay
  exposed** (it revolves; operators walk through) — the floor is only the horizontal top/bottom cap.
- **Frame connection method (decided):** **SS blind rivets**, matching the light-trap shell→cap
  lap-joint convention (`LT_RIVET_D=3.18`, hole Ø3.3, McMaster 97525A4xx), lapped + sealant for
  light-tightness.

### Stale geometry to reconcile (found during design)
- `generate_hingepanel_diagram.py:58` hardcodes `DRUM_H = 2200` instead of importing `DRUM_H_LT`
  (now **2100**) — every hingepanel sheet draws the drum/clear-height ~100mm too tall.
- `tbs_constants.py:358` (`DRUM_R … # 450`) and `:366` (`LT_HOUSING_R = DRUM_R # 450`) carry stale
  `# 450` inline comments (value is 400 / Ø800).
- `src/models/generate_lighttrap_model.py` carries stale `Ø900` comments at lines 74, 122, 205, 299,
  348 (`housing_surround_seal()` docstring names the Ø900 housing).

## 3. Deliverables

### D1 — Surround flat-pattern cut sheets (NEW Sheet 7)
1/8″ HDPE surround pieces laid **flat and fully dimensioned**: front skin + back skin (each with the
Ø836 aperture), and the upper/lower floor developments (curved edge meeting the Ø800 housing OD).
Cut lines, aperture Ø, and the blind-rivet hole pattern to the frame. All geometry **single-sourced**
off `LT_HOUSING_R` / `DRUM_D` / `APERTURE_R` / `LT_RIVET_*` so it cannot drift from light-trap Sheet 2
(housing cut sheet).

### D2 — Surround→housing floor-join detail (NEW Sheet 8, part A)
Section through the **upper and lower floor** where each meets the Ø800 housing OD — the light-tight
transition/seal. Coordinated with **light-trap Sheet 2** (housing cut sheet) so the surround↔housing
interface is single-sourced.

### D3 — Surround→frame connection (NEW Sheet 8, part B) + 3D
SS blind-rivet pattern; section showing the surround edge **lapped and riveted** to the steel frame
flange with sealant. **Add the connection to the 3D model** (`generate_lighttrap_model.py`) so the
surround is no longer floating; reconcile 2D↔3D↔report. Follow `skills/skill_fastener_convention.md`
for the rivet callouts and `skills/skill_model_consistency.md` after the model change.

### D4 — Reconciliations (same round)
- Fix `DRUM_H` → import `DRUM_H_LT` (2200→2100); regen **all** hingepanel sheets; verify only the
  affected sheets change.
- Clean the stale `# 450` / `Ø900` comments listed in §2.
- **De-dup `hingepanel-sheet6`** vs the new light-trap sheets (TODO L53-61): each detail owned by ONE
  blueprint — keep it on the light-trap sheet, cross-reference from the hingepanel report, remove the
  duplicate; **renumber** the set accordingly.

## 4. Cascade / registration (per CLAUDE.md workflow)
- New PNGs → `all-diagrams.md`, `publish.sh` (`DIAG_FILES`), `setup_docs.py` (`DIAG_IMAGE_FILES`),
  `dependencies.yml`.
- Report: new **§2.6 HDPE Surround Fabrication** embedding Sheets 7 & 8; frame-connection resolution
  into **§2.2**; §3.1 drum-top Z reconciled to `DRUM_H_LT`.
- Parts/cost: add the surround blind rivets (+ any added HDPE area) to `parts.py` → `--inject`
  cascade to master BOM / `project-cost-breakdown.md` / report §8.
- Gates: `lint.py`, `lint.py --cascade DRUM_H_LT` / `DRUM_D`, `check_consistency.py`, gallery audit,
  `manifest.py --check` / `--update` if the `.skp` is re-sent.
- `RELEASE.md [Unreleased]` bullet as work lands.

## 5. Approach decisions
- **2 new sheets** (7 = flat-pattern cut, 8 = join + rivet details) appended to the existing
  generator; set renumbers to 8 (or fewer if sheet6 de-dup retires content). Rejected: one crowded
  combined sheet (cut pattern + details don't share a scale) and 4 micro-sheets (over-fragmented).
- **Blind rivets** for surround→frame (decided) over U-channel / tee-nuts / bonded — matches the
  light-trap lap-joint family already in the BOM.

## 6. Out of scope
- No change to the drum/housing design itself (owned by the light-trap set) — this round only draws
  the surround that wraps it and the interfaces to frame + housing.
- No re-price beyond the added rivets/HDPE (full re-price is the deferred Aug-2026 sweep).

## 7. Success criteria
- Sheets 7 & 8 render, fully dimensioned, geometry single-sourced (no hardcoded drum literals).
- 3D surround is connected to the frame (rivets modeled); `check_consistency.py` clean.
- `DRUM_H` single-sourced; all stale `# 450` / `Ø900` comments gone.
- `hingepanel-sheet6` duplication resolved; every detail single-owned.
- All gates green; gallery audit empty; parts/cost cascaded.
