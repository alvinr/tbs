<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Plywood Cut Sheets — TBS-001

## 1. Purpose

Plywood recurs across the build — the IBC-corridor plumbing panel and pump-mount shirt, the
pinhole-wall filter-skid backing, the interior EP electrical backboard, the hinged light-trap
panel's Fan-B mount band and fold-down light-seal aprons, and the chemistry-prep shelf. Each was
previously cut ad hoc on its own subsystem drawing. This document is the **single cut sheet** the
buyer and fabricator work from: every plywood part in one schedule, grouped by grade and thickness
so same-stock parts nest on one sheet.

The cut dimensions are **single-sourced**. Geometry-driven pieces — the pinhole-wall panel width,
the fold-down apron widths and heights, the chem-shelf board — derive from `tbs_constants` and
cannot drift from the model (marked with a ᴰ on the schedule); the rest are spec/report literals.
Cost, supplier, and SKU stay in `parts.py`, keyed on each part's registry entry, so the money can't
drift from the procurement record. Fabrication detail for a given piece — hole positions, edge seal,
hinge line — stays on its owning subsystem sheet; this document is the stock and cut index, not the
fab detail.

## 2. Schedule

Every plywood cut piece, grouped by stock. The ᴰ marker flags a dimension derived from a
`tbs_constants` value; the `parts.py` key under each part is where its cost and supplier live.

![Plywood schedule](assets/plywood-cutsheets-sheet1.png)

## 3. Nesting layout

Each stock sheet with its pieces shelf-packed to scale on the 4×8. The packing is illustrative, not
optimized for yield; shaded pieces are fixed (non-fold).

![Plywood nesting](assets/plywood-cutsheets-sheet2.png)

## 4. Stock groups

| Group | Thickness | Grade | Parts | Stock sheets |
|---|---|---|---|---|
| A | 18mm (23/32") | RTD Southern Yellow Pine exterior sheathing | corridor plumbing panel, pump-mount shirt, pinhole-wall backing | 4 |
| B | 18mm | SANDEPLY Sande hardwood | EP electrical backboard | 1 |
| C | 18mm (¾") | CC pressure-treated pine | Fan-B mount band + cooler stowage base | 1 |
| D | 18mm | UV-coated white hardwood (Swaner) | chem-prep shelf board | 1 |
| E | 12mm | exterior BC | fold-down light aprons + baffle + pivot stub | 1 |

Group A's three parts share one SKU and may nest at cut; they are carried as separate sheets for cut
margin, and the pinhole-wall backing exceeds a single sheet's width so it is cut as two butt-jointed
halves. The pressure-treated sheet also yields the evap-cooler stowage base. Standard exterior grade
throughout except the SANDEPLY backboard and the UV-coated shelf surface — no marine ply, since no
plywood part carries a water-immersion load.

## 5. Source references

- Cut geometry — [`tbs_constants.py`](src/generators/tbs_constants.py) (single source), drawn by
  [`generate_plywood_cutsheets.py`](src/generators/generate_plywood_cutsheets.py).
- Cost / supplier / SKU — [`parts.py`](src/generators/parts.py) (`timber-ply` registry entries).
- Fabrication detail per piece — the owning subsystem reports: [Plumbing](plumbing-report.md),
  [Electrical](electrical-report.md), [Hinged Light-Trap Panel](hinged-panel-report.md),
  [Chemistry Prep Shelves](chemistry-prep-shelves.md).
