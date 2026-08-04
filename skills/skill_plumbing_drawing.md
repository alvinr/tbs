<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
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

5. **Never route a pipe THROUGH a solid object — route around it (penetrations are the only exception).** A pipe/hose/tube/duct must not pass through any solid body it does not connect to (pumps, valves, accumulators, filters, brackets, structural frames/uprights/rails, the beam wall, etc.). In the 3D models, check for interpenetration: if an obstacle is in the path, detour around it (a bypass lane offset in Yd/Z, or up and over) and keep the routing orthogonal. This has been gotten wrong repeatedly (pipes drawn straight through objects). **Permissible penetrations (granted exceptions):** a pipe MAY pass through an **IBC tank wall** (a tote side/top entry — that *is* the connection) and through a **plywood mounting panel / backing / spine** (a clean bored penetration). Everything else — especially equipment bodies (pumps/valves/tanks) and steel frame members — is OFF-LIMITS; route around them.

5a. **The PROCESSING TRAY is a TOTAL EXCLUSION ZONE — route AROUND the outside of its rim, never through it or over it.** No transport pipe may cross the processing-tray footprint (`x PROC_TRAY_X_L..X_R`, `Yd PROC_TRAY_YD_NEAR..YD_FAR`) at deck level — the basin holds the print and wash water. Run pipes that traverse the optical zone along the **Yd < near-rim strip between the pinhole wall and the tray near rim**, and cross between that strip and the IBC/corridor side **only in the gap past the tray's right edge** (`x > PROC_TRAY_X_R`, before the tote/frame). The ONLY exceptions are the **sump drain** (it connects to the sump well, then must loop UP over the rim and back DOWN *outside* the rim — never straight across the basin) and the **spray bar** (it services the tray by design). `check_interference.py` enforces this with a synthetic tray-footprint exclusion box (the sump drain is the one excluded line). See `generate_corridor_water_panel.py` sump-pickup / `generate_pinhole_water_panel.tap01_supply` for the around-the-rim path, copied from `overview.skp`.

  **Sanctioned exception — the under-walkway pipe RIBBON (rev11+).** The four corridor↔pinhole-wall lines (IBC-3→P-02, filtered return SV-01→DV-01, tray-sump→P-04, Blue trunk→TAP-01) run together as a flat **ribbon** in the dead space **UNDER the right-walkway grate**, in the clear channel BETWEEN the two walkway long beams (above the tray rim, hugged to the outer/IBC edge) — instead of the congested tray↔IBC gap. Where the ribbon meets a walkway cantilever it **loops UP over it** (never through the steel — Rule 5); to enter the corridor it drops and crosses **UNDER the walkway support beam** at Z≈65, through the gap over the tray edge (clear Z16–150). This is a *sanctioned* exception to the tray-exclusion zone (the lines run above the rim, under the grate, clear of the print/water). `check_interference.py` encodes it in the `RIBBON_LINES` set (excluded from the synthetic **tray** + **grate** solids only — still fully checked against every structural member: cantilevers, long beams, frame, equipment). Single-sourced in `generate_corridor_water_panel.ribbon_run()` (lane geometry + loop-over) and `ribbon_supports()` (the welded cross-braces that carry it).

6. **In-line valves go ON a straight run, oriented ALONG it.** A check / one-way valve, ball valve, or any in-line fitting is an **in-line device**: the pipe runs straight THROUGH it, so its body is centered on the pipe centerline and elongated **along the run axis** — placed on a STRAIGHT length of pipe, **never straddling an elbow** and never drawn as a right-angle block off to the side. To meter or protect a port (e.g. an anti-siphon check before a tank entry), put the valve on the straight approach run a short distance before the flange, not at the corner. (3D: a short barrel cylinder, radius ≈ pipe-OD + a little, length ≈ 2× OD, with `axis` = the local run direction.)

7. **Minimize connections — every joint is an integrity/leak risk.** Each fitting (elbow, tee, cross, coupling, union, threaded joint) is a potential leak and failure point, so among valid orthogonal routings prefer the one with the **FEWEST fittings**. Concretely: a longer straight run beats a short run + two elbows + a jog; **align a junction/fitting to its incoming run so the pipe enters straight (one elbow), not offset into it (an offset = two elbows + a dead jog)**; place a tee/cross/manifold **ON** the line that feeds it. When a *small* move of a junction or component deletes a fitting, make the move (it's worth re-positioning the fitting to save the joint). *Example:* the X1 fill cross was shifted onto the blue-recycle riser's Yd (`X1_TEE_Y`) so the recycle rises **straight** into the cross's −X port — one elbow, replacing the old rise → −Yd jog → elbow (two fittings + a stub).

## Right-Angle Connections (applies to 2D diagrams AND 3D models)

This is the rule most often gotten wrong — it has had to be fixed repeatedly. Whenever a line (pipe / flex hose / corrugated duct / irrigation tube) terminates at a **box, manifold, fitting, appliance, or wall penetration**, the terminating segment must be a short stub that is **perpendicular to the face it enters**.

- **Orthogonal routing:** runs are axis-aligned; every change of direction is a discrete elbow fitting (2D: concentric arcs; 3D: a swept-torus elbow body). No diagonals except a genuinely flexible run following a support.
- **Flexible runs are the one exception — but only mid-span.** A flex hose or flex duct may sag/follow a pole or rail diagonally along its length, **but the connection into a box/fitting/penetration at each end must still be a perpendicular stub** (drop straight into a top face, or come in level into a side face). Add a short normal segment / elbow at the port.
- **3D model helpers (`src/models/generate_sketchup_model.py`):** use `ruby_pipe_run(waypoints, …)` for rigid pipe (axis-aligned waypoints + `ruby_elbow` swept-torus bends) and `ruby_flex_run(waypoints, …)` for corrugated flex duct (same elbows, ribbed straights). Do **not** draw a single `ruby_pipe`/`ruby_flex_duct` diagonally from a source straight into a port.
- **2D diagram helper (`src/generators/tbs_drawing.py`):** the parallel-wall pipe-run + concentric-arc elbow geometry has **one canonical implementation** — `draw_pipe_path(ax, x_pts, z_pts, od_mm, wall_mm, fc, *, ec, bore_fc, elbow_r, zorder, lw, sx, sz)` and `draw_pipe_end(...)`. **Never re-inline this algorithm** into a generator (it used to be copy-pasted into ~6 of them and drifted cosmetically). A generator keeps only a thin local wrapper that injects its scale functions (`sx=`/`sz=`, default identity) and per-diagram style (`lw`, colors) and delegates. `check_consistency.py` **CHECK F** flags any re-inlined copy (top-level or nested).

**Recurring fixes — learn from these:**
- **Evap cooler duct:** a single diagonal flex run was drawn from the cooler to the wall inlet. Fixed to a **vertical riser → 90° elbow → horizontal stub** into the Ø200 wall inlet, meeting both the cooler outlet and the wall at right angles.
- **Spray-bar feed manifold:** the supply hose entered the manifold box at a shallow angle. Fixed to a **vertical drop into the manifold top** (perpendicular). The hose still follows the push-pole diagonally above that, which is fine (flexible mid-span), but the box entry is now a right angle.
- **Spray-bar feed tubes through the ball joint (Rule 5):** irrigation tubes ran straight from the manifold to feed points and **passed through the ball-joint socket**. Fixed by detouring those tubes along the beam **back edge** (a bypass lane offset in Yd) so they go *around* the socket, plus nudging the center feed clear of the socket footprint.

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

### Tee (T-connector)
A molded/cast tee fitting (e.g. a US-Plastics 1" socket tee) — **three ports**: a straight
**RUN** (two collinear ports) plus one **BRANCH** port at 90° to the run, meeting at a common
center. Codified geometry:

- **Body is one fitting, fatter than the pipe.** The run + branch are a single fitting body whose
  OD is larger than the pipe OD (the pipe sockets *into* the fitting). Don't draw a tee as a plain
  box, and don't draw it as three pipes butted together — it is one fatter fitting body.
- **Run is straight through.** The two run ports are collinear (one axis); the pipe passes straight
  through. The **branch is perpendicular**, leaving the run centerline at 90° — never a Y, never a
  slanted branch.
- **Socket cuff at each of the 3 ends** — a short, slightly-larger raised ring (the socket the pipe
  inserts into), so the fitting reads as a tee and not a coupling/cross.
- **Pick the orientation so two of the three flows are collinear** (they become the run) and the odd
  one out is the branch. A junction where all three legs are mutually perpendicular is an
  *elbow-with-branch*, not a tee — re-route so two legs line up before placing the tee.
- **2D section:** three openings each with double parallel walls; the run walls continue straight
  through; the branch walls meet the run with a small rounded fillet at the internal corner.
- **3D model:** use the `tee(nm, cx, cy, cz, run, branch, color)` helper in
  `generate_corridor_water_panel.py` — `run` = the through axis (`"x"|"y"|"z"`), `branch` = the branch
  port as axis+sign (e.g. `"x-"`, `"y+"`). It draws the run body + perpendicular branch body
  (both pipe-OD + a margin) and a socket cuff at all three ends. (Reuse it; don't draw tees as
  `ruby_box` cubes.)

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
- [ ] **Ran `python3 src/models/check_interference.py` against the LIVE model** — it reports pipe-vs-solid clashes AND pipe-on-pipe **crossings** (two runs whose centerlines pass within `r_a+r_b`, i.e. actually sharing space — a clean Z-staggered over/under does NOT flag). Eyeballing renders is NOT enough — hand-routed waypoints in dense spaces reintroduce collisions every time. Run it after EVERY routing change and drive fixes from its coordinates (never by hand-tracing). Permitted penetrations (IBC tank walls, ply panels) and end-to-end joins are already excluded.
- [ ] **Refreshed the committed audit artifact:** `python3 src/models/check_interference.py --write && git add interference-report.txt`. A **lint GATE** (`gate_interference_report`) blocks the commit if a routing generator is staged and `interference-report.txt`'s `routing-sources-sha` doesn't match the sources being committed — so a reroute can't land without the audit having been re-run. This is the enforcement; it replaces "remember to run it."
- [ ] Parallel pipes that must run together (a manifold) each get their OWN depth lane (distinct X or Yd) — a riser to one device's port must not pass through a neighbouring device's port/body that shares the same lane.
- [ ] Under-deck / under-walkway crossings sit in a Z-band that clears BOTH the structure below (frame bottom ring) AND the cantilever beams above — check the actual member Z-ranges, don't assume.
- [ ] No pipe/tube/duct passes through a solid object it doesn't connect to — detour around obstacles (check the 3D model for interpenetration)
- [ ] Elbow fittings show concentric arcs (not sharp corners, not gradual bends)
- [ ] Barb connections show ridged profile + hose clamp band
- [ ] Pipe end-on shown as concentric circles
- [ ] Flow direction arrows inside bore where helpful

## Refactoring the 3D plumbing efficiently (corridor congestion)

The `pinhole-wall-mount` branch took **84 commits** (≈31 position tweaks + 24 reroutes + 15 interference fixes) to detail the IBC plumbing corridor. Most of that churn is avoidable. Rules, learned the hard way:

1. **Parameterize every position a pipe references; pipes reference the constant, never a literal.** A component/fitting/lane position is a named module constant (`DV02X`, `SUCT_XLANE`, `SUCT_SURF_Z`, `X1_TEE_X/Z` in `generate_corridor_water_panel.py`). Then "move it 75 mm" is a *one-line* edit and every connecting pipe follows. A bare literal in a waypoint (the `1960` feed jog, the `bz` entry) is a latent move/derivation bug — the same lesson as the generator-label literals in CLAUDE.md, applied to coordinates.
2. **Single-source a shared lane.** Pipes that run parallel/stacked share ONE lane constant + a fixed per-pipe offset (brown `SUCT_SURF_Z`, blue `+30`, grey `+60`; all at `SUCT_XLANE`). They then move together and can't drift into each other.
3. **Derive a position from the part's REAL extents — and verify against the built model.** The brown drain entered the *blue* tote because `bz` used `pallet + full-unit-height` instead of the brown bottle's actual top (`IBC_H_1000 − 20 = 1148`). When a value must sit inside/above/below a part, compute it from that part's queried z-extent and spot-check (`check_interference` + a one-off bounds query), don't trust an ad-hoc formula.
4. **Run the pipe-on-pipe check after EVERY routing change.** `check_interference.py` now reports pipe-vs-solid AND pipe-on-pipe (two runs overlapping that don't share a junction). Solid-only checking read "0" for many commits while real crossings piled up unseen — the slowest kind of rework.
5. **In a saturated zone, allocate lanes FIRST (a pipe rack); don't thread reactively.** The win came when the three pipes that can't pass under the IBC/grate were committed to one stacked surface-perimeter route — each its own Z (brown 205 / blue 235 / grey 262), shared X/Yd. Decide each pipe's lane/height up front; reactive one-pipe-at-a-time threading is where the commits piled up.
6. **Locate the problem before a structural change.** The P-01↔ACC-01 swap was a hunch; the check showed the crossings were elsewhere (gap/wall, not the column), and the swap created a *new* tight ACC clearance. Measure where the contention actually is (the checker's coordinates) before moving structure.
7. **Moving a connected fitting = one constant + its feed + every leg.** Parameterize the fitting position; the feed/legs jog to it. DV-02 → `DV02X` carried its feed and both diverter legs in one edit.
8. **Verify with `view.zoom_extents` or `view.zoom(group_array)`, not hand-set `camera.set(eye,target)`.** Manual eye/target cameras repeatedly rendered empty and burned iterations; zoom-to-geometry is reliable.
