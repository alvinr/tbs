---
name: diagram-structure
description: Coordinate system, view conventions, multi-sheet patterns, shared helpers, and generator boilerplate for all TBS engineering diagrams
metadata:
  type: reference
---

## Coordinate System

All TBS diagrams use a right-hand coordinate system based on the 20ft ISO shipping container interior:

| Axis | Direction | Origin | Range |
|------|-----------|--------|-------|
| **X** | Along container length (left–right in elevation) | Left wall interior face | 0–5893mm |
| **Yd** | Depth from pinhole wall into container | Pinhole wall interior face | 0–2362mm |
| **Z** | Height above finished floor | Container floor | 0–2388mm |

**Key reference points:**
- Pinhole aperture: X=2399mm, Yd=0, Z≈1194mm (center of active film plane)
- Film plane active zone: X=150–4649mm (4499mm span)
- Walkway deck: Z=75–100mm (varies by section)

All constants live in `src/generators/tbs_constants.py` — never hardcode spatial positions.

## View Conventions

### Interior elevations (looking at pinhole wall from inside)

The standard interior elevation looks at the Yd=0 wall from inside the container. The viewer faces the pinhole wall, so high-X equipment appears on the LEFT. To achieve this:

```python
ax.invert_xaxis()
```

Call this **after** setting axis limits. All drawing code uses normal X coordinates; the axis flip handles the mirror. This convention is used by:
- Combined assembly elevation
- Filter skid elevation
- Pump manifold elevation
- Pinhole wall elevation

### Plan views (looking down)

Plan views show X (horizontal) vs Yd (vertical, Yd=0 at top). Near wall (pinhole) is at the top of the drawing.

### Cross-sections

Cross-sections specify the cut plane in their title. Common cuts:
- **Yd–Z sections**: cut perpendicular to X, show depth vs height
- **X–Z sections**: cut perpendicular to Yd, show length vs height
- **Along-axle sections**: cut along a component axis (e.g., sheet 5 spray bar)

## Shared Helper Libraries

### `tbs_constants.py` — Single source of truth

All spatial positions, dimensions, and colors. Import what you need:

```python
from tbs_constants import (
    C_LEN, C_WID, C_HGT,           # container interior dimensions
    RAIL_X_L, RAIL_X_R,             # film plane rail endpoints
    DIAGRAMS_DIR, SVG_DIR,          # output paths (absolute)
    C_OUT, C_CL, C_DIM,            # drawing palette
    C_ALUM, C_STEEL, C_GASKT,      # material fills
    C_PUMP, C_BLUE_IBC, C_WALL,    # component colors
)
```

Never hardcode positions or colors that exist in `tbs_constants.py`.

### `tbs_drawing.py` — Drawing primitives

| Function | Purpose |
|----------|---------|
| `draw_dim_h(ax, x1, x2, y, label)` | Horizontal dimension line with ticks |
| `draw_dim_v(ax, x, y1, y2, label)` | Vertical dimension line with ticks |
| `leader(ax, x_tip, y_tip, x_txt, y_txt, label)` | Leader line from component to label |
| `place_label(ax, x, y, label)` | Auto-positioned component label (collision-aware) |
| `register_pipe(x1, y1, x2, y2)` | Register pipe segment for label collision avoidance |
| `reset_label_registry()` | Clear pipe registry at start of each sheet |
| `draw_cl(ax, cx, cy, r)` | Center line cross |
| `draw_cl_h(ax, x1, x2, y)` | Horizontal center line |
| `draw_cl_v(ax, x, y1, y2)` | Vertical center line |
| `draw_circle(ax, cx, cy, r)` | Circle with center marks |
| `draw_rect(ax, x, y, w, h)` | Rectangle |
| `bolt_holes(ax, cx, cy, bc_r, n, d_r)` | Bolt hole pattern on PCD |
| `hatch_rect(ax, x, y, w, h)` | Cross-hatched section fill |
| `draw_notes(ax, notes, x, y_top, spacing)` | Formatted notes block with title |
| `draw_legend(ax, items, x, y)` | Color legend block |

### `tbs_title_block.py` — Standard title block

```python
from tbs_title_block import title_block

ax_tb = fig.add_axes([0.04, 0.005, 0.92, 0.045])
ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis("off")
title_block(ax_tb, "SHEET 1 OF 3",
            drawing_title="ASSEMBLY NAME",
            subtitle="VIEW DESCRIPTION",
            scale_note="SCALE 1:10 — ALL DIMS IN mm")
```

## Multi-Sheet Generator Pattern

Every diagram generator follows this structure:

```python
#!/usr/bin/env python3
import os, sys
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
from tbs_constants import DIAGRAMS_DIR, ...
from tbs_drawing import draw_dim_h, draw_dim_v, leader, ...
from tbs_title_block import title_block

TOTAL_SHEETS = 3
C_BG = "#FAFAFA"
FONT = {"fontfamily": "monospace"}

def _save(fig, stem):
    os.makedirs(DIAGRAMS_DIR, exist_ok=True)
    png = os.path.join(DIAGRAMS_DIR, f"{stem}.png")
    fig.savefig(png, dpi=150, bbox_inches="tight", facecolor=C_BG)
    plt.close(fig)
    print(f"  {png} saved")

def draw_sheet1():
    fig = plt.figure(figsize=(20, 14))
    fig.patch.set_facecolor(C_BG)
    ax = fig.add_axes([0.05, 0.06, 0.90, 0.88])
    ax.set_facecolor(C_BG)
    ax.axis("off")
    # ... drawing code ...
    # Title block
    ax_tb = fig.add_axes([0.04, 0.005, 0.92, 0.045])
    ax_tb.set_xlim(0, 1); ax_tb.set_ylim(0, 1); ax_tb.axis("off")
    title_block(ax_tb, f"SHEET 1 OF {TOTAL_SHEETS}", ...)
    _save(fig, "assembly-name-sheet1")

def draw_sheet2():
    ...

if __name__ == "__main__":
    draw_sheet1()
    draw_sheet2()
```

**Naming convention:** `generate_<name>_diagram.py` → outputs `diagrams/<name>-sheet1.png`, `diagrams/<name>-sheet2.png`, etc.

## Scale Functions

Most generators define local scale functions to convert mm to drawing units:

```python
SC = 10.0  # 1:10 scale
OX = 3.0   # origin offset X
OZ = 2.0   # origin offset Z

def sx(x_mm): return OX + x_mm / SC
def sz(z_mm): return OZ + z_mm / SC
```

For thin cross-sections where plate thickness would be invisible at uniform scale, use split scaling:

```python
def sx(mm): return mm / 5.0   # horizontal 1:5
def sy(mm): return mm * 1.0   # vertical 1:1 (exaggerated)
```

Always annotate exaggerated scales in the title block or subtitle.

## Pipe Drawing

`draw_pipe_path()` is defined locally in each generator that needs plumbing (not yet in `tbs_drawing.py`). It draws parallel-wall pipes with fill color and wall thickness. See `generate_filter_skid_diagram.py:285` for the reference implementation.

Pipe color conventions:
- Blue supply system: `"#2979B8"`
- Brown recycle system: `"#8B5E3C"`
- Black/waste system: `"#555555"`

See `skills/skill_plumbing_drawing.md` for detailed pipe crossing and fitting conventions.

## Registration Checklist

After creating a new diagram generator, register its outputs in:

1. `publish.sh` → `MD_FILES` (if new report) and `DIAG_FILES` (PNG names)
2. `src/generators/setup_docs.py` → `MD_FILES`, `DIAG_IMAGE_FILES`, `INDEX_MD`
3. `mkdocs.yml` → `nav:` block
4. `engineering-diagrams.md` → diagram index table
