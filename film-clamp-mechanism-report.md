<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Muslin Clamp System — Mechanism Design

## 1. Purpose

The photosensitive muslin must be held taut against the [film plane frame](film-plane-mechanism-report.md) throughout exposures lasting 30–45 minutes, at any tilt angle up to ±<!-- BEGIN fact:film_plane_max_tilt -->40<!-- END fact:film_plane_max_tilt -->° and any swing angle up to ±<!-- BEGIN fact:film_plane_max_swing -->28<!-- END fact:film_plane_max_swing -->°. Loading and unloading happens under mixed safelight conditions, so the clamp mechanism must provide clear tactile feedback without visual confirmation.

This report describes the **muslin spring-clip system** that secures the muslin to the **2"×2"×3/16" aluminum L-angle** perimeter frame (the film-plane frame — [Film Plane Mechanism §4](film-plane-mechanism-report.md)). Its two 2-inch (≈51mm) legs are the *flat leg* (bonded behind the ACM backing board) and the *upstand* (standing proud toward the pinhole) — each clip mounts on the upstand's inboard face.

---

## 2. Clamp Layout

**88 spring clips** are spaced at 150mm centers around the full perimeter of the <!-- BEGIN fact:film_plane_width_mm -->4,499<!-- END fact:film_plane_width_mm -->mm × <!-- BEGIN fact:film_plane_height_mm -->2,094<!-- END fact:film_plane_height_mm -->mm film plane frame:

| Edge | Length | Clip Count |
|------|--------|-------------|
| Top horizontal | <!-- BEGIN fact:film_plane_width_mm -->4,499<!-- END fact:film_plane_width_mm -->mm | 30 |
| Bottom horizontal | <!-- BEGIN fact:film_plane_width_mm -->4,499<!-- END fact:film_plane_width_mm -->mm | 30 |
| Left vertical | <!-- BEGIN fact:film_plane_height_mm -->2,094<!-- END fact:film_plane_height_mm -->mm | 14 |
| Right vertical | <!-- BEGIN fact:film_plane_height_mm -->2,094<!-- END fact:film_plane_height_mm -->mm | 14 |
| **Total** | | **88** |

---

## 3. Clamp Mechanism

Each clip is a bracket **through-bolted to the angle upstand** (inboard face, nuts on the inside edge) carrying a spring-loaded jaw. A torsion spring provides ~5N, pressing a 60A neoprene pad — and the muslin under it — onto the ACM backing board at the frame edge.

The spring clip gives tactile **snap-open / snap-closed** feedback, critical for loading and unloading muslin in safelight conditions: squeeze the handle to lift the pad, release to snap it closed. The torsion spring holds each clip closed at any tilt angle, so the film plane can be tilted or swung without a clip releasing.

The overall design can be seen in the diagram below and discussed in the following sections

![Muslin clamp detail — Sheet 6](assets/film-plane-sheet6.png)

### 3.1 Muslin Path

The muslin lies over the ACM backing board (the pinhole face); its edge is clamped **onto the board** just inboard of the upstand. Each clip's neoprene pad presses the muslin down onto the board across a ~20mm-deep bite just inboard of the frame edge, providing direct tension — the ACM is the anvil, so no separate hem wrap is needed.

### 3.2 Neoprene Jaw Pad

Each clip jaw is faced with a **25.4 × 20mm pad of 60A neoprene** (6mm / ¼″ thick), self-adhesive (PSA) backed and bonded flat to the jaw plate — see Sheet 6, Panel D. The pads are cut from a 1″ × ¼″ neoprene strip ([McMaster 4568N57](https://www.mcmaster.com/4568N57/), 36″ per strip; 88 pads → 3 strips). The neoprene grips the muslin without damaging the fibers and compensates for slight variations in fabric thickness at the clamped edge.

---

## 4. Parts List

All items ship within the United States. Local Southern California pickup noted where available.

<!-- BEGIN parts:clamp -->
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| Muslin spring clip | Bracket + spring jaw, ~5N, neoprene pad, torsion spring, squeeze handle; through-bolted to the frame upstand (nuts on the inside) | 88 ea | McMaster-Carr / Amazon | $264–$704 |
| [M5×16 countersunk screw, A2-70 SS](https://www.mcmaster.com/91420A326/) (91420A326) | A2-70 stainless flat-head (CSK) — through-bolts the clip bracket to the upstand. $11.54/pack of 100 (91420A = flat-head series; supersedes the socket-head 91292A126). | 176 ea | McMaster-Carr / Bolt Depot | $20 |
| [M5 hex nut, nyloc A2-70 SS](https://www.mcmaster.com/93625A200/) (93625A200) | A2-70 stainless — on the inside edge of the upstand | 176 ea | McMaster-Carr / Bolt Depot | $16 |
| [Neoprene pad strip 60A](https://www.mcmaster.com/4568N57/) (4568N57) | 1" × 1/4" 60A neoprene, PSA-backed, 36"/strip — the clip jaw pad. Cut into 25.4×20mm pads (6mm thick); 88 pads × 20mm = 1,760mm → 3 strips (2 + 1 cutting-waste/spare) | 3 strip | McMaster-Carr / Grainger | $78 |
| **Clamp total** | | | | **$378–$818** |
<!-- END parts:clamp -->

**Clamp system estimated cost:** <!-- BEGIN costing:clamp-system-low -->$378<!-- END costing:clamp-system-low --> (generic spring clips) to <!-- BEGIN costing:clamp-system-high -->$818<!-- END costing:clamp-system-high --> (quality spring clips).

---

## 5. Maintenance

| Interval | Task |
|----------|------|
| Before each session | Inspect muslin clip engagement — all 88 clips snapped closed |
| Monthly | Check neoprene jaw pads for compression set — replace if grip force is noticeably reduced |
| Every 6 months | Inspect torsion springs for fatigue — clips should snap firmly to closed position under gravity at <!-- BEGIN fact:film_plane_max_tilt -->40<!-- END fact:film_plane_max_tilt -->° tilt |
| Annually | Replace neoprene jaw pads (preventive — ~$78 for 3× 4568N57 strips covers all 88 pads) |

---

## 6. Source References

1. [Film Plane Mechanism Report](film-plane-mechanism-report.md) — Parent report: four-corner independent actuation mechanism that the clamp system attaches to.
2. [McMaster-Carr Clamps](https://www.mcmaster.com/products/clamps/) — spring-loaded clamp mechanisms (spring-clip reference).
3. [McMaster-Carr Neoprene Strip](https://www.mcmaster.com/neoprene) — 60A self-adhesive neoprene jaw pad material.
