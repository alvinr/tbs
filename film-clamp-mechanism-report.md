<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Muslin Clamp System — Mechanism Design

## 1. Purpose

The photosensitive muslin must be held taut against the [film plane frame](film-plane-mechanism-report.md) throughout exposures lasting 30–45 minutes, at any tilt angle up to ±<!-- BEGIN fact:film_plane_max_tilt -->40<!-- END fact:film_plane_max_tilt -->° and any swing angle up to ±<!-- BEGIN fact:film_plane_max_swing -->28<!-- END fact:film_plane_max_swing -->°. Loading and unloading happens under mixed safelight conditions, so the clamp mechanism must provide clear tactile feedback without visual confirmation.

This report describes the **cam-lever spring clamp system** that secures the muslin to the **2"×2"×3/16" aluminum L-angle** perimeter frame (the welded film-plane frame — [Film Plane Mechanism §4](film-plane-mechanism-report.md)). Its two 2-inch (≈51mm) legs are what the clamp sections below call the *pinhole-facing leg* and the *perpendicular leg*.

---

## 2. Clamp Layout

**92 cam-lever spring clamps** are spaced at 150mm centers around the full perimeter of the <!-- BEGIN fact:film_plane_width_mm -->4,499<!-- END fact:film_plane_width_mm -->mm × <!-- BEGIN fact:film_plane_height_mm -->2,388<!-- END fact:film_plane_height_mm -->mm film plane frame:

| Edge | Length | Clamp Count |
|------|--------|-------------|
| Top horizontal | <!-- BEGIN fact:film_plane_width_mm -->4,499<!-- END fact:film_plane_width_mm -->mm | 30 |
| Bottom horizontal | <!-- BEGIN fact:film_plane_width_mm -->4,499<!-- END fact:film_plane_width_mm -->mm | 30 |
| Left vertical | <!-- BEGIN fact:film_plane_height_mm -->2,388<!-- END fact:film_plane_height_mm -->mm | 16 |
| Right vertical | <!-- BEGIN fact:film_plane_height_mm -->2,388<!-- END fact:film_plane_height_mm -->mm | 16 |
| **Total** | | **92** |

---

## 3. Clamp Mechanism

Each clamp uses an **over-center cam mechanism** with a torsion spring to provide ~5N clamping force, gripping the muslin hem against the pinhole-facing leg of the aluminum angle frame through a 60A neoprene jaw pad.

The cam-lever design provides tactile **snap-open / snap-closed** feedback, critical for loading and unloading muslin in safelight conditions. The torsion spring biases each clamp closed at any tilt angle, so the film plane can be tilted or swung without clamps releasing.

The overall design can be seen in the diagram below and discussed in the following sections

![Muslin clamp detail — Sheet 5](assets/film-plane-sheet5.png)

### 3.1 Muslin Wrap Path

The muslin drapes over the pinhole-facing leg of the 2"×2" angle, wraps around the outside corner, and a 100mm hem hangs down the perpendicular leg. The jaw presses the hem against the outer face of the pinhole-facing leg, ~10–15mm from the corner, providing direct tension.

### 3.2 Neoprene Jaw Pad

Each clamp jaw is faced with a 35mm × 6mm strip of **60A neoprene**, self-adhesive backed. The neoprene provides grip without damaging the muslin fibers and compensates for slight variations in fabric thickness across the hem fold.

---

## 4. Parts List

All items ship within the United States. Local Southern California pickup noted where available.

| Item | Spec | Qty | Source A | Source B | Est. Unit |
|------|------|-----|---------|---------|-----------|
| Cam-lever spring clamp | Toggle-style, ~5N, neoprene jaw | 92 | McMaster-Carr (Destaco equiv.) | Amazon (generic toggle) | $3-8 |
| M5×16 SS socket head bolt | A2-70 stainless | 184 | McMaster-Carr #91292A128 | Bolt Depot | $0.25 |
| M5 SS Nylock nut | A2-70 stainless | 184 | McMaster-Carr #93625A200 | Bolt Depot | $0.08 |
| Neoprene strip 60A | 35mm × 6mm, self-adhesive | 1 roll (10m) | McMaster-Carr #8614K44 | Grainger | $15 |

**Clamp system estimated cost:** <!-- BEGIN costing:clamp-system-low -->$346<!-- END costing:clamp-system-low --> (generic toggle clamps) to <!-- BEGIN costing:clamp-system-high -->$806<!-- END costing:clamp-system-high --> (Destaco-equivalent quality).

---

## 5. Maintenance

| Interval | Task |
|----------|------|
| Before each session | Inspect muslin clamp engagement — all 92 clamps snapped closed |
| Monthly | Check neoprene jaw pads for compression set — replace if grip force is noticeably reduced |
| Every 6 months | Inspect torsion springs for fatigue — clamps should snap firmly to closed position under gravity at <!-- BEGIN fact:film_plane_max_tilt -->40<!-- END fact:film_plane_max_tilt -->° tilt |
| Annually | Replace neoprene jaw pads (preventive — $15 per roll covers all 92 clamps) |

---

## 6. Source References

1. [Film Plane Mechanism Report](film-plane-mechanism-report.md) — Parent report: four-corner independent actuation mechanism that the clamp system attaches to.
2. [McMaster-Carr Toggle Clamps](https://www.mcmaster.com/toggle-clamps) — Destaco-equivalent cam-lever clamp specifications.
3. [McMaster-Carr Neoprene Strip](https://www.mcmaster.com/neoprene) — 60A self-adhesive neoprene jaw pad material.

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*
