# The Big Shoebox Project — Claude Code Working Instructions

## Project Identity

- **Project name:** The Big Shoebox Project
- **Camera designation:** TBS-001
- **Parts prefix:** ICP-XX (e.g. ICP-01, ICP-02…)
- **Container:** 20ft ISO standard shipping container, 2362mm interior focal depth
- **Image plane:** 4499 × 2388mm active (X=150–4649mm); container interior 5893 × 2388mm
- **Pinhole:** Ø2.17mm, SS-302 shim, f/1088 (Rayleigh formula, λ=550nm)
- **Site:** https://alvinr.github.io/tbs/

---

## Repository Structure

```
/                        ← project root: .md reports, config files
src/generators/          ← all .py scripts (diagram generators, helpers, setup)
diagrams/                ← generated PNGs and SVGs (output of generators)
skills/                  ← codified drawing and labeling conventions (read before creating diagrams)
published/               ← MkDocs input — auto-populated by publish.sh (gitignored, never edit directly)
published/assets/        ← images — auto-populated by publish.sh
site/                    ← built output — gitignored, never commit
.claude/                 ← Claude session files — never commit
```

**Key config files:** `mkdocs.yml` (nav + theme), `publish.sh` (sync + deploy), `src/generators/setup_docs.py` (one-time setup).

**Skills** (read these before working on diagrams):
- `skills/skill_diagram_structure.md` — coordinate system, view conventions, multi-sheet generator boilerplate, shared helper catalog
- `skills/skill_label_placement.md` — 57 rules for leader lines, dimensions, notes blocks, and label positioning
- `skills/skill_plumbing_drawing.md` — pipe drawing conventions, fittings, crossings, flow arrows

---

## Workflow: Adding a New Document

1. Write `<name>.md` in the project root.
2. If drawings are needed: write `src/generators/generate_<name>.py` → outputs to `diagrams/<name>-sheet1.png`, `diagrams/<name>-sheet2.png`, etc. (all generated PNGs go into `diagrams/`).
3. Register the `.md` in `publish.sh` → `MD_FILES` array.
4. Register any new `.png` files in `publish.sh` → `DIAG_FILES` array (for generated diagrams) or `IMG_FILES` (for root-only images like logos).
5. Register the `.md` in `src/generators/setup_docs.py` → `MD_FILES` list (controls nav title).
6. Register any new `.png` files in `src/generators/setup_docs.py` → `DIAG_IMAGE_FILES` list (for generated diagrams) or `ROOT_IMAGE_FILES` (for root-only images).
7. Add a row to the `INDEX_MD` table in `setup_docs.py`.
8. Add a nav entry to `mkdocs.yml` → `nav:` block.
9. Add a row to `docs/index.md` → Documents table.
10. Run `bash publish.sh` to sync and deploy.
11. Commit all source files together: scripts + `.md` + `.png`.

---

## Drawing Style Conventions

Reuse all helpers from `tbs_drawing.py`:

```python
draw_dim_h(ax, x1, x2, y, label, ...)   # horizontal dimension
draw_dim_v(ax, x, y1, y2, label, ...)   # vertical dimension
draw_cl(ax, x1, x2, y, ...)             # centre line
draw_circle(ax, cx, cy, r, ...)         # circle with centre marks
draw_rect(ax, x, y, w, h, ...)          # rectangle
leader(ax, x1, y1, x2, y2, label, ...)  # leader line + label
bolt_holes(ax, cx, cy, pcd, n, ...)     # bolt hole pattern
hatch_rect(ax, x, y, w, h, ...)        # cross-hatched section
```

**Color palette (white background):**

```python
C_OUT   = "#1A1A1A"   # outlines
C_CL    = "#2060A0"   # centre lines (blue, dashed)
C_DIM   = "#404040"   # dimensions
C_ALUM  = "#C8D8E8"   # aluminum section fill
C_STEEL = "#B0B0B8"   # steel section fill
C_GASKT = "#5A3020"   # gasket/neoprene fill
```

**Title block:** series `TBS-XXX`. Reference `generate_film_plane_mechanism.py` for multi-sheet layout and `title_block()` helper.

**Thin cross-sections:** for plates that are much wider than they are thick, use separate scale functions to avoid unreadable flat sections:

```python
def sx(mm): return mm / 5.0   # horizontal 1:5
def sy(mm): return mm * 1.0   # vertical 1:1 — thickness exaggerated
```
Always annotate: `HORIZONTAL SCALE 1:5 / VERTICAL SCALE 1:1 — thickness exaggerated for clarity`.

---

## Report Style Conventions

- Every engineering claim links to a citable source: peer-reviewed paper, manufacturer datasheet, or textbook.
- **All source references must include hyperlinks** — no bare titles or catalog names without URLs. Format as `[Source Name](URL)` for standards, datasheets, catalogs, books, and papers.
- **When any engineering drawing specification changes** (dimensions, quantities, materials, bolt patterns, etc.), always update the report's parts list, `master-shopping-list.md`, and `project-cost-breakdown.md` in the same commit.
- Shopping lists: 2+ US/SoCal supplier options per major component; include part numbers and current prices.
- Distortion renders: dark background (`PRU_DEEP = "#0F2D5E"`), 800×600px per configuration, 3×3 summary grid as a separate PNG.
- Logo/favicon palette constants live in `generate_logo_final.py` and `generate_favicon.py` — reuse if needed.
- **Use American English spelling throughout** — e.g. "center" not "centre", "color" not "colour", "aluminum" not "aluminium", "analyze" not "analyse".

---

## Generator ↔ 3D Model Sync

The 2D diagram generators (`src/generators/`) and the SketchUp 3D models
(`src/models/`) both read spatial constants from `tbs_constants.py`, so changes
ripple into both.

- **When a change touches `tbs_constants.py` (or otherwise alters a system
  component's geometry), re-run every SketchUp model that contains the affected
  component** — regenerate, re-send, and re-save it:
  `python3 src/models/generate_sketchup_model.py --save --send` (then commit the
  updated `*.skp` + `*.rb` alongside the diagram/constant change).
- **`component-dependency-map.md` is the source of truth** for which components
  are drawn by which generators and present in which models (§3 diagram matrix,
  §3.1 model list, §4 change-propagation + workflow). **Keep it updated** whenever
  a system component, generator, or model is added or changed.
- Today there is one model (`overview.skp`) containing nearly every component, so
  in practice any `tbs_constants.py` change ⇒ re-run `overview`.

---

## Key Optical Constants

| Constant | Value | Derivation |
|----------|-------|-----------|
| Focal length | 2362mm | Container interior depth |
| Optimal pinhole Ø | 2.17mm | Rayleigh: d = 1.9√(fλ), λ=550nm |
| f-number | f/1088 | f / d |
| Container interior | 5893 × 2388mm | Full interior face |
| Film plane (active) | 4499 × 2388mm | X=150–4649mm (shadow-free zone) |
| Pinhole X position | 2399mm | Center of active film plane (150 + 4499/2) |
| Rail left X | 150mm | Left rail / film plane left edge |
| Rail right X | 4649mm | Right rail / film plane right edge |
| Rail span | 4499mm | RAIL_X_R − RAIL_X_L |
| Board tilt 5° → image shift | 207mm | 2362 × tan(5°) |
| Film plane max tilt | ±42° | 4-corner mechanism hard stop |
| Film plane max swing | ±25.7° | arctan(2162/4499) — wider rail span vs same Y travel |
| Tilt-swing board max | ±5.3° | Screw shoulder hard stop |

---

## Deployment

```bash
bash publish.sh          # sync docs/ + gh-deploy → GitHub Pages
bash publish.sh --local  # local preview: http://127.0.0.1:8000
bash publish.sh --build  # build to site/ only (no push)
```

The script auto-detects whether a git remote is set. If not, it falls back to `--build`.

---

## Git

Standing permission to commit and redeploy on every request in this project.

- Commit all source files together: scripts + `.md` + `.png`.
- Never commit `site/` (gitignored) or `.claude/` session/memory files.
- `docs/` files are auto-generated by `publish.sh` — they can be committed but are not the source of truth.
