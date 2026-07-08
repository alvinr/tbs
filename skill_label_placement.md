<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Label Placement Skill — TBS Diagram Generation

## Purpose

This document codifies label placement rules for P&ID schematics and engineering diagrams in the TBS project. Rules are derived from manual corrections to auto-generated diagrams and will be refined as more examples are gathered.

---

## Core Principles

1. **Labels must never overlap pipes.** If a label sits on a pipe path, the diagram is unreadable.
2. **Labels belong to the clearest quadrant** around their component — the direction with the most white space.
3. **Consistency within a component type** matters more than absolute position. All valve labels should follow the same offset pattern; all pump labels likewise.
4. **Override anything.** The auto-placement is a starting point. Every parameter (`dx`, `dy`, `ha`, `va`) accepts an explicit override per call.

---

## Implementation

The helper function `place_label()` lives in `tbs_drawing.py`. Supporting functions:

| Function | Purpose |
|----------|---------|
| `place_label(ax, x, y, label, ...)` | Place a label with auto-positioning |
| `register_pipe(x1, y1, x2, y2)` | Record a pipe segment for collision avoidance |
| `reset_label_registry()` | Clear registries at the start of each sheet |

### Usage pattern

```python
from tbs_drawing import place_label, register_pipe, reset_label_registry

# Start of each sheet
reset_label_registry()

# Register pipe segments as you draw them
register_pipe(2.4, 7.0, 2.4, 6.3)

# Auto-place (picks best quadrant):
place_label(ax, 2.4, 7.0, "BV-01", component='valve', color=C_BLUE)

# Override one axis:
place_label(ax, 2.4, 7.0, "BV-01", component='valve', dx=0.35)

# Full manual:
place_label(ax, 2.4, 7.0, "BV-01", dx=-0.2, dy=0.15, ha='right')
```

---

## Rules by Component Type

### Valves (ball valves: BV-xx)

- **Symbol radius:** 0.096 (size=0.06 * 1.6)
- **Default offset:** right of symbol, level with center
- **Preferred position:** on the side with no pipe passing through
- **Alignment:** `ha='left'` (label reads away from symbol)
- **Font:** 6pt, system color

| Pipe direction | Label goes |
|---|---|
| Vertical pipe through valve | Right (+X), level |
| Horizontal pipe through valve | Above (+Y) or below (-Y), centered |
| Both pipes visible | Whichever side has more white space |

**Observed corrections:**
- BV-02: shifted right +0.30 from pipe axis to clear vertical pipe
- BV-03: shifted right +0.15 to clear vertical pipe
- BV-05: shifted right +0.07 to clear riser
- BV-06: shifted right +0.30 to clear vertical pipe and black crossing
- BV-08: shifted up +0.10 to clear horizontal pipe

### Pumps (P-xx)

- **Symbol radius:** 0.1125
- **Default offset:** right and slightly below center
- **Preferred position:** beside the symbol, baseline dropped ~0.05–0.10
- **Alignment:** `ha='left'`
- **Font:** 6pt, pump color (C_PUMP)
- **Multi-line:** typical format is `"P-01\n12VDC\n3.5 GPM"`

**Key rule:** bring the label *closer* to the symbol than you'd think. The original auto-generated labels were too far out (0.35 offset). Hand corrections consistently pulled them in to 0.15–0.20.

**Observed corrections:**
- P-01: X offset reduced from 0.35 to 0.20, Y dropped -0.10
- P-02: X offset reduced from 0.35 to 0.20, Y dropped -0.10
- P-03: X offset reduced from 0.35 to 0.15, Y dropped -0.05
- P-04: X offset reduced from 0.35 to 0.20, Y dropped -0.05
- P-05: X offset reduced from 0.35 to 0.15, Y dropped -0.10

### Diverter Valves (3W-DV-xx)

- **Symbol radius:** 0.12 (size=0.075 * 1.6)
- **Default offset:** to the side with no pipe exit
- **Alignment:** `ha='center'`
- **Font:** 6pt, dark gray (#444)

**Key rule:** diverter valves have 3 pipe connections. Place the label on the remaining clear side.

**Observed corrections:**
- DV-01: dropped Y by -0.10 to clear the black pipe exiting right
- DV-02: moved from below-center to beside (+0.40 X) to clear the black pipe exiting downward

### External Ports (X1–X4)

- **Symbol radius:** 0.12 (hexagon)
- **Default offset:** above center
- **Alignment:** `ha='center'`, `va='bottom'`
- **Font:** 5.5pt, italic, system color

### Filters (F1–F3)

- **Symbol:** pentagon, size 0.126, height 0.162
- **Default offset:** description text beside and below
- **Label inside symbol:** 6.4pt bold, centered
- **Description text:** separate `ax.text()` call, not managed by `place_label()`

---

## Collision Avoidance Algorithm

The quadrant scoring system in `place_label()`:

1. **Generate 8 candidates** — four quadrants (NE, NW, SE, SW) plus four cardinal directions (N, S, E, W), using the component type's default offset magnitude.
2. **Add symbol radius** to the offset so the label clears the symbol edge.
3. **Score each candidate** by scanning within `scan_r` (default 0.5 units):
   - Penalty for each nearby pipe segment (inversely proportional to distance)
   - Penalty for each previously placed label (inversely proportional to distance)
4. **Pick lowest score** — the position with the most clear space.

### Improving the algorithm over time

- Register more pipe segments → better avoidance
- Adjust `scan_r` per sheet if the component density varies
- Add zone boundary awareness (labels shouldn't cross zone fills)
- Add label-to-label minimum spacing constraints
- Consider text bounding box dimensions for multi-line labels

---

## Dashed vs Solid Pipe Conventions (related)

These affect label positioning because labels should never sit on top of any pipe, including dashed ones:

| Style | Meaning |
|---|---|
| Solid | Supply / forward flow |
| Dashed (`--`) | Return / fill / recycle flow |
| Bridge humps must match parent pipe style | Use `style=` parameter on `pipe_bridge()` |
| Arrow overlays on dashed pipes | Keep arrows short (~0.3 units) to avoid masking dashes |

---

## Revision Log

| Date | Change |
|------|--------|
| 2026-05-17 | Initial codification from water-system-sheet1 hand corrections (13 label adjustments) |
