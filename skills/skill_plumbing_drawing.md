---
name: Plumbing pipe drawing conventions
description: How to draw pipes, fittings (elbows, tees, barbs), and hose runs in engineering section/elevation/plan diagrams for TBS water system
type: reference
originSessionId: 54457a84-3dd4-4b25-a419-b2a4e2f11517
---
# Plumbing Pipe Drawing Conventions

## Cardinal Rules

1. **Parallel sides always.** Pipes are drawn as two parallel lines representing the outer wall (OD), with white space between showing the bore. The wall thickness is constant. Pipes NEVER taper, NEVER curve gradually.

2. **Direction changes ONLY at fittings.** A pipe run is composed of: straight section → fitting → straight section → fitting. There are no gradual bends. Every change of direction requires a discrete fitting (elbow, tee, etc.).

3. **Constant OD throughout straight runs.** The two parallel wall lines maintain exact spacing for the entire length of a straight section.

## How to Draw Fittings in Section View

### 90° Elbow
- Two straight pipe stubs meeting at right angles.
- Connected by **concentric arcs** (outer wall arc + inner wall arc) maintaining wall thickness through the curve.
- Standard short-radius elbow: centerline radius = 1× nominal pipe diameter.
- Long-radius elbow: centerline radius = 1.5× nominal pipe diameter.
- The elbow fitting body is slightly thicker-walled than the pipe itself.

### 45° Elbow
- Same as 90° but with a 45° turn.
- Used for gradual direction changes or to avoid obstacles.
- Same concentric arc drawing convention, just a smaller sweep angle.

### Tee (T-joint)
- T-intersection where a branch pipe meets the main run at 90°.
- Rounded internal junction.
- Three openings, each drawn with double parallel walls.

### Straight Coupling
- Short fitting joining two pipe ends.
- Slightly larger OD than the pipe (the pipe slides inside).
- Drawn as a short wider section bridging two pipe ends.

### Pipe End-On (going into/out of page)
- Drawn as **concentric circles**: outer circle (OD), inner circle (bore).
- Wall thickness visible as the annular ring.

## Fittings for the TBS Water System

The TBS-001 water system uses **1" reinforced suction hose** and **1" HDPE pickup tube**. The correct fittings are:

### Barb Fittings (Insert Fittings)
- **How they work:** A tapered cylindrical tube with raised ridges (barbs/sawtooth profile). The hose pushes over the barbed end. Secured with a **stainless steel worm-drive hose clamp**.
- **Materials:** Nylon or polypropylene for chemical resistance (cyanotype chemistry compatibility).

### Fitting Types Used
| Fitting | Use | Drawing Notes |
|---------|-----|---------------|
| 90° barb elbow | Direction changes (wall corner, pickup bend) | Concentric arcs + barb ridges on both ends |
| Straight barb coupling | Hose-to-hose or hose-to-tube joins | Short wider section with barbs |
| Barb tee | Flow splits (e.g., diverter branches) | T-shape with barbs on all 3 ports |
| Barb-to-thread adapter | Connection to threaded pump ports | Hex body, thread on one end, barb on other |

### How to Draw Barb Connections in Section
1. Draw the fitting body with sawtooth barb ridges on the insertion portion.
2. Draw the hose pushed over the barbs (hose OD visible outside the fitting).
3. Draw a narrow rectangular band around the hose exterior = hose clamp.
4. The fitting body typically has a hex or knurled section in the middle for grip.

## Pipe Crossings (Where Pipes Pass Over/Behind Each Other)

Two rules:
1. **Joins**: pipes that connect butt at zero distance — no gap, no dot, seamless.
2. **Crossings**: front pipe (higher zorder) is unbroken. Rear pipe breaks flush against the front pipe's outer wall — zero extra gap.

### Zorder Layering
```python
Z_BLACK = 6    # Layer 1 — back
Z_BROWN = 7    # Layer 2 — middle
Z_BLUE  = 8    # Layer 3 — front
```

### Crossing Implementation
Rear pipe splits into two segments, each ending exactly at the front pipe OD edge:
```python
_gap_half = front_OD / 2.0  # zero extra gap — butt flush to front pipe wall
# Rear pipe: segment BEFORE crossing
draw_pipe_path(ax, [x, x], [z_start, z_cross - _gap_half], rear_OD, rear_WALL, ...)
# Rear pipe: segment AFTER crossing
draw_pipe_path(ax, [x, x], [z_cross + _gap_half, z_end], rear_OD, rear_WALL, ...)
# Front pipe: drawn continuously (no break), higher zorder
```

### What NOT to do
- No bridge arcs / semicircular loops — unreadable at small scales
- No junction dots — unnecessary complexity
- No extra CROSS_GAP padding — makes joins look broken
- No white mask rectangles — creates artifacts

## Drawing Checklist for Pipe Runs

- [ ] All pipe sections have parallel walls (constant OD)
- [ ] No gradual curves — only straight runs and fittings
- [ ] Every direction change has a discrete elbow fitting drawn
- [ ] Elbow fittings show concentric arcs (not sharp corners, not gradual bends)
- [ ] Barb connections show ridged profile + hose clamp band
- [ ] Pipe end-on shown as concentric circles
- [ ] Flow direction arrows inside bore where helpful
