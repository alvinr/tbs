# The Big Shoebox Project — Claude Code Working Instructions

## Project Identity

- **Project name:** The Big Shoebox Project
- **Camera designation:** TBS-001
- **Parts prefix:** TBS-XXX (e.g. TSB-01, TSB-02…)
- **Container:** 20ft ISO standard shipping container, 2,362mm interior focal depth
- **Image plane:** 5,893 × 2,388 mm
- **Pinhole:** Ø2.17mm, SS-302 shim, f/1088 (Rayleigh formula, λ=550nm)
- **Site:** https://alvinr.github.io/tbs/

---

## Repository Structure

```
/                        ← source: .md reports, .py generator scripts
docs/                    ← MkDocs input — auto-populated by publish.sh (do not edit directly)
docs/assets/             ← images — auto-populated by publish.sh
site/                    ← built output — gitignored, never commit
.claude/                 ← Claude session files — never commit
```

**Key config files:** `mkdocs.yml` (nav + theme), `publish.sh` (sync + deploy), `setup_docs.py` (one-time setup).

---

## Workflow: Adding a New Document

1. Write `<name>.md` in the project root.
2. If drawings are needed: write `generate_<name>.py` → outputs to `diagrams/<name>-sheet1.png`, `diagrams/<name>-sheet2.png`, etc. (all generated PNGs go into `diagrams/`).
3. Register the `.md` in `publish.sh` → `MD_FILES` array.
4. Register any new `.png` files in `publish.sh` → `DIAG_FILES` array (for generated diagrams) or `IMG_FILES` (for root-only images like logos).
5. Register the `.md` in `setup_docs.py` → `MD_FILES` list (controls nav title).
6. Register any new `.png` files in `setup_docs.py` → `DIAG_IMAGE_FILES` list (for generated diagrams) or `ROOT_IMAGE_FILES` (for root-only images).
7. Add a row to the `INDEX_MD` table in `setup_docs.py`.
8. Add a nav entry to `mkdocs.yml` → `nav:` block.
9. Add a row to `docs/index.md` → Documents table.
10. Run `bash publish.sh` to sync and deploy.
11. Commit all source files together: scripts + `.md` + `.png`.

---

## Drawing Style Conventions

Reuse all helpers from `generate_plate_drawing.py`:

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

**Colour palette (white background):**

```python
C_OUT   = "#1A1A1A"   # outlines
C_CL    = "#2060A0"   # centre lines (blue, dashed)
C_DIM   = "#404040"   # dimensions
C_ALUM  = "#C8D8E8"   # aluminium section fill
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
- Shopping lists: 2+ US/SoCal supplier options per major component; include part numbers and current prices.
- Distortion renders: dark background (`PRU_DEEP = "#0F2D5E"`), 800×600px per configuration, 3×3 summary grid as a separate PNG.
- Logo/favicon palette constants live in `generate_logo_final.py` and `generate_favicon.py` — reuse if needed.

---

## Key Optical Constants

| Constant | Value | Derivation |
|----------|-------|-----------|
| Focal length | 2,362 mm | Container interior depth |
| Optimal pinhole Ø | 2.17 mm | Rayleigh: d = 1.9√(fλ), λ=550nm |
| f-number | f/1088 | f / d |
| Container interior | 5,893 × 2,388 mm | Full interior face |
| Film plane (active) | 3,549 × 2,388 mm | X=1,100–4,649mm (shadow-free zone) |
| Pinhole X position | 2,874 mm | Centre of active film plane (1,100 + 3,549/2) |
| Rail left X | 1,100 mm | Left rail / film plane left edge |
| Rail right X | 4,649 mm | Right rail / film plane right edge |
| Rail span | 3,549 mm | RAIL_X_R − RAIL_X_L |
| Board tilt 5° → image shift | 207 mm | 2362 × tan(5°) |
| Film plane max tilt | ±42° | 4-corner mechanism hard stop |
| Film plane max swing | ±31.4° | arctan(2162/3549) — wider rail span vs same Y travel |
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
