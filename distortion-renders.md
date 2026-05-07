<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Distortion Renders — Film Plane & Tilt-Swing
## TBS-001 — Compound Optical Projections

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*

---

This page collects all ray-traced distortion renders for TBS-001. Two independent movement
systems produce image projections — their compound effects interact non-linearly.

Source reports: [Film Plane Mechanism](film-plane-mechanism-report.md) and
[Tilt-Swing Front Board](tilt-swing-board-report.md).

---

## 1. Film Plane Distortion Renders

Four-corner independent actuation of the film plane (TBS-FM01). Each corner moves ±42° tilt
and ±25.7° swing independently, producing Scheimpflug-equivalent projections at pinhole
focal lengths. Seven configurations are shown.

**Summary grid — all 7 configurations**
![Film Plane Distortion — Summary Grid](assets/film-plane-distortion-summary.png)

Individual configurations:

| Config | Render |
|--------|--------|
| C0 — Flat | ![C0](assets/film-plane-distortion-c0.png) |
| C1 — Tilt +42° | ![C1](assets/film-plane-distortion-c1.png) |
| C2 — Tilt −42° | ![C2](assets/film-plane-distortion-c2.png) |
| C3 — Swing +20° | ![C3](assets/film-plane-distortion-c3.png) |
| C4 — Swing −20° | ![C4](assets/film-plane-distortion-c4.png) |
| C5 — Twisted (tilt+swing) | ![C5](assets/film-plane-distortion-c5.png) |
| C6 — Full compound | ![C6](assets/film-plane-distortion-c6.png) |

---

## 2. Combined Distortion Renders (Film Plane + Tilt-Swing Board)

Compound optical projections when both the film plane mechanism and the tilt-swing
front board (TBS-TS01) are active simultaneously. Nine configurations are shown.
The two systems interact non-linearly — their combined effects cannot be decomposed
into a simple sum of the individual systems' projections.

**Summary grid — all 9 configurations**
![Tilt-Swing Combined Distortion — Summary Grid](assets/tilt-swing-combined-summary.png)

Individual configurations:

| Config | Render |
|--------|--------|
| C0 — Both flat | ![C0](assets/tilt-swing-combined-c0.png) |
| C1 | ![C1](assets/tilt-swing-combined-c1.png) |
| C2 | ![C2](assets/tilt-swing-combined-c2.png) |
| C3 | ![C3](assets/tilt-swing-combined-c3.png) |
| C4 | ![C4](assets/tilt-swing-combined-c4.png) |
| C5 | ![C5](assets/tilt-swing-combined-c5.png) |
| C6 | ![C6](assets/tilt-swing-combined-c6.png) |
| C7 | ![C7](assets/tilt-swing-combined-c7.png) |
| C8 — Full compound | ![C8](assets/tilt-swing-combined-c8.png) |
