<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Muslin Clamp System — Mechanism Design

## 1. Purpose

The photosensitive muslin must be held taut against the [film plane frame](film-plane-mechanism-report.md) throughout exposures lasting 30–45 minutes, at any tilt angle up to ±42° and any swing angle up to ±25.7°. Loading and unloading happens under safelight (near-dark) conditions, so the clamp mechanism must provide clear tactile feedback without visual confirmation.

This report describes the **cam-lever spring clamp system** that secures the muslin to the aluminum angle perimeter frame.

---

## 2. Clamp Layout

**92 cam-lever spring clamps** are spaced at 150mm centers around the full perimeter of the 4499mm × 2388mm film plane frame:

| Edge | Length | Clamp Count |
|------|--------|-------------|
| Top horizontal | 4499mm | 30 |
| Bottom horizontal | 4499mm | 30 |
| Left vertical | 2388mm | 16 |
| Right vertical | 2388mm | 16 |
| **Total** | | **92** |

---

## 3. Clamp Mechanism

Each clamp uses an **over-center cam mechanism** with a torsion spring to provide ~5N clamping force, gripping the muslin hem against the pinhole-facing leg of the aluminum angle frame through a 60A neoprene jaw pad.

The cam-lever design provides tactile **snap-open / snap-closed** feedback, critical for loading and unloading muslin in safelight (near-dark) conditions. The torsion spring biases each clamp closed at any tilt angle, so the film plane can be tilted or swung without clamps releasing.

### Muslin Wrap Path

The muslin drapes over the pinhole-facing leg of the 2"×2" angle, wraps around the outside corner, and a 100mm hem hangs down the perpendicular leg. The jaw presses the hem against the outer face of the pinhole-facing leg, ~10–15mm from the corner, providing direct tension.

### Neoprene Jaw Pad

Each clamp jaw is faced with a 35mm × 6mm strip of **60A neoprene**, self-adhesive backed. The neoprene provides grip without damaging the muslin fibers and compensates for slight variations in fabric thickness across the hem fold.

---

## 4. Engineering Drawing

![Muslin clamp detail — Sheet 5](assets/film-plane-sheet5.png)

Sheet 5 of the [Film Plane Mechanism](film-plane-mechanism-report.md) drawing set shows the cam-lever spring clamp in cross-section (open and closed positions), plan view of frame attachment, and elevation at 150mm spacing.

---

## 5. Parts List

All items ship within the United States. Local Southern California pickup noted where available.

| Item | Spec | Qty | Source A | Source B | Est. Unit |
|------|------|-----|---------|---------|-----------|
| Cam-lever spring clamp | Toggle-style, ~5N, neoprene jaw | 92 | McMaster-Carr (Destaco equiv.) | Amazon (generic toggle) | $3-8 |
| M5×16 SS socket head bolt | A2-70 stainless | 184 | McMaster-Carr #91292A128 | Bolt Depot | $0.25 |
| M5 SS Nylock nut | A2-70 stainless | 184 | McMaster-Carr #93625A200 | Bolt Depot | $0.08 |
| Neoprene strip 60A | 35mm × 6mm, self-adhesive | 1 roll (10m) | McMaster-Carr #8614K44 | Grainger | $15 |

**Clamp system estimated cost:** $330 (generic toggle clamps) to $790 (Destaco-equivalent quality).

---

## 6. Maintenance

| Interval | Task |
|----------|------|
| Before each session | Inspect muslin clamp engagement — all 92 clamps snapped closed |
| Monthly | Check neoprene jaw pads for compression set — replace if grip force is noticeably reduced |
| Every 6 months | Inspect torsion springs for fatigue — clamps should snap firmly to closed position under gravity at 42° tilt |
| Annually | Replace neoprene jaw pads (preventive — $15 per roll covers all 92 clamps) |

---

## 7. Source References

1. [Film Plane Mechanism Report](film-plane-mechanism-report.md) — Parent report: four-corner independent actuation mechanism that the clamp system attaches to.
2. [McMaster-Carr Toggle Clamps](https://www.mcmaster.com/toggle-clamps) — Destaco-equivalent cam-lever clamp specifications.
3. [McMaster-Carr Neoprene Strip](https://www.mcmaster.com/neoprene) — 60A self-adhesive neoprene jaw pad material.

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*
