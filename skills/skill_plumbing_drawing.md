---
name: Plumbing pipe drawing conventions
description: How to draw and model pipes, fittings (elbows, tees, barbs), hose/duct runs, and right-angle connections to boxes/manifolds/penetrations — for both 2D TBS diagrams and the 3D SketchUp models
type: reference
originSessionId: 54457a84-3dd4-4b25-a419-b2a4e2f11517
---
# Plumbing Pipe Drawing Conventions

## Cardinal Rules

1. **Parallel sides always.** Pipes are drawn as two parallel lines representing the outer wall (OD), with white space between showing the bore. The wall thickness is constant. Pipes NEVER taper, NEVER curve gradually.

2. **Direction changes ONLY at fittings.** A pipe run is composed of: straight section → fitting → straight section → fitting. There are no gradual bends. Every change of direction requires a discrete fitting (elbow, tee, etc.).

3. **Constant OD throughout straight runs.** The two parallel wall lines maintain exact spacing for the entire length of a straight section.

4. **Connect at right angles.** A pipe, hose, tube, or duct must meet any fitting, manifold/box, appliance port, or wall penetration **perpendicular to that face**. The final segment before the connection is normal (90°) to the face it enters — never a diagonal or grazing approach. To reach a port from an off-axis source, route with orthogonal legs joined by elbows (e.g. riser → 90° elbow → horizontal stub into the port), not a single slanted segment.

5. **Never route a pipe THROUGH another object — route around it.** A pipe/hose/tube/duct must not pass through any solid body it does not connect to (ball joints, sockets, brackets, frames, the beam wall except at a fitting, tanks, etc.). In the 3D models, check for interpenetration: if an obstacle is in the path, detour around it (a bypass lane offset in Yd/Z, or up and over) and keep the routing orthogonal. This has been gotten wrong repeatedly (pipes drawn straight through objects).

6. **In-line valves go ON a straight run, oriented ALONG it.** A check / one-way valve, ball valve, or any in-line fitting is an **in-line device**: the pipe runs straight THROUGH it, so its body is centered on the pipe centerline and elongated **along the run axis** — placed on a STRAIGHT length of pipe, **never straddling an elbow** and never drawn as a right-angle block off to the side. To meter or protect a port (e.g. an anti-siphon check before a tank entry), put the valve on the straight approach run a short distance before the flange, not at the corner. (3D: a short barrel cylinder, radius ≈ pipe-OD + a little, length ≈ 2× OD, with `axis` = the local run direction.)

## Right-Angle Connections (applies to 2D diagrams AND 3D models)

This is the rule most often gotten wrong — it has had to be fixed repeatedly. Whenever a line (pipe / flex hose / corrugated duct / irrigation tube) terminates at a **box, manifold, fitting, appliance, or wall penetration**, the terminating segment must be a short stub that is **perpendicular to the face it enters**.

- **Orthogonal routing:** runs are axis-aligned; every change of direction is a discrete elbow fitting (2D: concentric arcs; 3D: a swept-torus elbow body). No diagonals except a genuinely flexible run following a support.
- **Flexible runs are the one exception — but only mid-span.** A flex hose or flex duct may sag/follow a pole or rail diagonally along its length, **but the connection into a box/fitting/penetration at each end must still be a perpendicular stub** (drop straight into a top face, or come in level into a side face). Add a short normal segment / elbow at the port.
- **3D model helpers (`src/models/generate_sketchup_model.py`):** use `ruby_pipe_run(waypoints, …)` for rigid pipe (axis-aligned waypoints + `ruby_elbow` swept-torus bends) and `ruby_flex_run(waypoints, …)` for corrugated flex duct (same elbows, ribbed straights). Do **not** draw a single `ruby_pipe`/`ruby_flex_duct` diagonally from a source straight into a port.
- **2D diagram helper (`src/generators/tbs_drawing.py`):** the parallel-wall pipe-run + concentric-arc elbow geometry has **one canonical implementation** — `draw_pipe_path(ax, x_pts, z_pts, od_mm, wall_mm, fc, *, ec, bore_fc, elbow_r, zorder, lw, sx, sz)` and `draw_pipe_end(...)`. **Never re-inline this algorithm** into a generator (it used to be copy-pasted into ~6 of them and drifted cosmetically). A generator keeps only a thin local wrapper that injects its scale functions (`sx=`/`sz=`, default identity) and per-diagram style (`lw`, colors) and delegates. `check_consistency.py` **CHECK F** flags any re-inlined copy (top-level or nested).

**Recurring fixes — learn from these:**
- **Evap cooler duct:** a single diagonal flex run was drawn from the cooler to the wall inlet. Fixed to a **vertical riser → 90° elbow → horizontal stub** into the Ø200 wall inlet, meeting both the cooler outlet and the wall at right angles.
- **Spray-bar feed manifold:** the supply hose entered the manifold box at a shallow angle. Fixed to a **vertical drop into the manifold top** (perpendicular). The hose still follows the push-pole diagonally above that, which is fine (flexible mid-span), but the box entry is now a right angle.
- **Spray-bar feed tubes through the ball joint (Rule 5):** irrigation tubes ran straight from the manifold to feed points and **passed through the ball-joint socket**. Fixed by detouring those tubes along the beam **back edge** (a bypass lane offset in Yd) so they go *around* the socket, plus nudging the centre feed clear of the socket footprint.

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
- [ ] Every connection to a box / manifold / fitting / penetration is a perpendicular stub (right-angle entry), not a diagonal — in 2D and 3D alike
- [ ] In-line valves (check / one-way / ball) sit ON a straight run, body oriented ALONG the pipe axis — not a right-angle block, not on an elbow
- [ ] No pipe/tube/duct passes through a solid object it doesn't connect to — detour around obstacles (check the 3D model for interpenetration)
- [ ] Elbow fittings show concentric arcs (not sharp corners, not gradual bends)
- [ ] Barb connections show ridged profile + hose clamp band
- [ ] Pipe end-on shown as concentric circles
- [ ] Flow direction arrows inside bore where helpful
