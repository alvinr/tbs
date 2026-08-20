<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->

# Revolving Light-Trap — Fabrication Blueprint Set (Design Spec)

**Branch:** `lighttrap-bp`  ·  **Date:** 2026-08-20  ·  **Scope:** the revolving assembly only

---

## 1. Goal

Produce a **fabrication-grade 2D blueprint set for the revolving light-trap assembly** — the
Ø900 housing, the C-shell rotating drum, top/bottom caps, stub shafts, SKF 6215 bearing hubs,
seals, grab rail, and the drum support cage. A plastics/metal shop builds the assembly from
these sheets. Today this assembly has **no dedicated fabrication drawings**; its 2D coverage is
scattered inside the panel-centric `hingepanel` sheets and is not shop-complete (no flat
patterns, no bearing-hub detail, no seal cross-sections, no drum-cage frame).

The **design is already settled** — `light-trap-selection.md` §4 is the specification of record
(housing, drum, bearings, seals, hardware, suppliers). This effort is a *drawing* effort:
turning that spec into blueprints. No geometry or material decisions are being reopened.

### Out of scope
- The hinge panel, carriage/slide, and Fan B (their own sheets; done separately per Alvin).
- Any change to `tbs_constants.py` geometry. Sheets **consume** existing constants; they do not
  introduce new ones except drawing-only helpers (developed-length labels, etc.).
- The 3D model (`lighttrap.skp`) — unchanged. No `--send`.
- Trimming the drum content already on `hingepanel` sheets 1/2/3/5 — noted as a **follow-up**
  (§7), not part of this branch.

---

## 2. Naming restructure (Option A — approved)

`generate_lighttrap_diagram.py` and `lighttrap-sheet1/2.png` are a **misnomer** — they are the
**ventilation** diagrams (fans + baffle duct). Before drawing anything, rename them to their
true name and free `lighttrap` for the real light trap:

| Old | New |
|-----|-----|
| `src/generators/generate_lighttrap_diagram.py` | `src/generators/generate_ventilation_diagram.py` |
| `diagrams/lighttrap-sheet1.png` | `diagrams/ventilation-sheet1.png` |
| `diagrams/lighttrap-sheet2.png` | `diagrams/ventilation-sheet2.png` |

Then the **new** revolving-assembly generator claims the freed name:
`generate_lighttrap_diagram.py` → `diagrams/lighttrap-sheet1..6.png`.

**Rename touches (sweep, mechanical):** `publish.sh` (`DIAG_FILES`), `setup_docs.py`
(`DIAG_IMAGE_FILES` + nav title), `mkdocs.yml` (nav), `all-diagrams.md` (gallery entries),
`dependencies.yml` (script→output graph + any import edges), `component-dependency-map.md`
(§3 diagram matrix), and **every `.md` that embeds `assets/lighttrap-sheet1/2.png`** — grep first,
repoint each. The internal savefig paths + sheet titles in the renamed generator change to
"VENTILATION SYSTEM" wording (they already say that in the body; only the filename was wrong).

---

## 3. The blueprint sheets (6)

New generator `src/generators/generate_lighttrap_diagram.py`, multi-sheet, house style
(`tbs_drawing.py` helpers, `title_block()` series `TBS-XXX`, white background, standard palette).
All dimensions **read from `tbs_constants.py`** — no numeric literals in labels (constant
cascade rule). Thin cross-sections use split H/V scales with the "thickness exaggerated"
annotation where a wall is much thinner than the part.

| # | Sheet | Content |
|---|-------|---------|
| 1 | **General Arrangement** | Full vertical section through the assembly on the drum axis: fixed housing (`DRUM_D`/`LT_HOUSING_T`), rotating drum (`LT_DRUM_OR`/`LT_DRUM_T`), top + bottom caps (`LT_CAP_T`), both SKF 6215 bearings, stub shafts, grab rail, cage envelope. Overall height span `PANEL_FLOOR_GAP`→`DRUM_H_LT`, Ø900 footprint, opening orientation (exterior + interior-onto-walkway, 180° apart). Part callouts keyed to a **BOM table** (item, qty, material, source-ref). |
| 2 | **Housing cylinder — cut sheet** | 5mm UV-HDPE rolled cylinder as a **flat pattern**: developed length = π·`DRUM_D`, height, weld-seam location, the two 80° (`LT_OPENING_DEG`) opening cutouts dimensioned by arc position + width, exterior-UV / interior-black finish notes. Roll + extrusion-weld callout. |
| 3 | **Rotating drum — cut sheet** | 1/8″ (`LT_DRUM_T`) HDPE C-shell **flat pattern** (single 80° opening; developed length = π·2·`LT_DRUM_OR`) **and** top/bottom 3/16″ (`LT_CAP_T`) caps with stub-shaft bore + circlip groove. Shell-to-cap **weld map**, running-gap note (15mm radial to housing). |
| 4 | **Bearing hub & stub-shaft detail** | SKF 6215-2RS1 seat (Ø75 ID / Ø130 OD / 25 wide), stub shaft captured in the cap, circlip axial retention, upper isolated housing ring vs lower welded steel floor collar (8×M10 / 6×M10), fits + tolerances. Section + enlarged detail bubble. |
| 5 | **Seals & light-path verification** | Drum↔housing running gap closed by 20mm neoprene compression strip; 12mm neoprene top + bottom wiper strips with silicone bead; the **<90° opening-overlap geometry** proving no straight-through light path at any rotation (the §5 argument, drawn). |
| 6 | **Drum cage / support frame** | The structural cage `DRUM_CAGE_X0/X1/YD_L/YD_R` (full-depth `PANEL_FLOOR_GAP`→`DRUM_H_LT`) that reacts the bearing loads: member layout, bearing-plate seats top + bottom, anchor points to container/panel, plan + elevation. |

**Shop-detail decision (default, flag for review):** cut sheets 2 & 3 carry **true flat-pattern
developed geometry** (roll-and-weld) — a plastics shop needs the developed length and cutout
arc positions, not a foreshortened cylinder view. If you'd rather have sectioned-cylinder views
with arc dimensions, say so and sheets 2/3 change.

---

## 4. Documentation home (recommendation — confirm on review)

Two viable homes for embedding the six sheets:

- **Recommended: extend `light-trap-selection.md`** with a new **"§9 Fabrication Blueprints"**
  section that embeds sheets 1–6. That report already owns the light-trap design narrative and
  already embeds illustrative panel sheets — the fabrication set is its natural continuation,
  and it keeps one source of record for the assembly.
- **Alternative: a new report** `light-trap-fabrication.md`. Cleaner separation of
  "why this design" from "how to build it," but a whole new nav entry + registration for a set
  that logically belongs with the selection report.

Either way the six PNGs are registered per the "Adding a New Document" checklist (steps 4, 6, 7,
9 as applicable) and **added to `all-diagrams.md`** under a Light-Trap section.

---

## 5. Sources of truth (no drift)

- Geometry: `tbs_constants.py` (`DRUM_*`, `LT_*`, `PANEL_FLOOR_GAP`) — referenced, never
  restated as literals in labels.
- Spec/BOM text: `light-trap-selection.md` §4 (bearings, seals, hardware, suppliers) and
  `parts.py` for any purchasable item costs. If the blueprint BOM needs a part not yet in the
  registry, add it to `parts.py` (procurement source of record) rather than hardcoding a price.
- Design rationale for the light-path (§5) stays in `light-trap-selection.md`; Sheet 5 *draws*
  it, doesn't re-argue it in prose.

---

## 6. Verification

- `dependencies.yml` updated for the renamed + new generator; `lint.py` (incl. license-header
  gate, missing-cascade byte-diff) clean.
- Gallery audit command from CLAUDE.md step 7 returns empty (every PNG in `all-diagrams.md`).
- `check_consistency.py` clean (no stale literals, no 2D↔3D divergence introduced).
- Rendered visual pass per `skills/skill_tidy_labels.md` on each new sheet before shipping.
- `RELEASE.md [Unreleased]` gets bullets (rename + new blueprint set) as the work lands.

---

## 7. Follow-ups (explicitly deferred, not this branch)

1. Trim/repoint the drum content on `hingepanel` sheets 1/2/3/5 so the new set is the single
   source of record for drum fabrication (the panel sheets keep only what's panel-specific).
2. Reconcile any drum BOM line into `parts.py` if new.

---

## 8. Open questions for review

1. **Doc home** — extend `light-trap-selection.md` §9 (recommended) or new
   `light-trap-fabrication.md`?
2. **Cut-sheet depth** — true flat patterns (default) or sectioned-cylinder-with-arcs?
3. **Sheet count** — is 6 right, or merge 5+6 / split a plan view out to 7?
