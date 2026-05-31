<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Distortion Renders — Film Plane & Tilt-Swing

This page collects all ray-traced distortion renders for TBS-001. Two independent movement
systems produce image projections — their compound effects interact non-linearly.

Source reports: [Film Plane Mechanism](film-plane-mechanism-report.md) and
[Tilt-Swing Front Board](tilt-swing-board-report.md).

---

## 1. Film Plane Distortion Renders

Four-corner independent actuation of the film plane (TBS-FM01). Each corner moves ±42° tilt
and ±25.7° swing independently, producing Scheimpflug-equivalent projections at pinhole
focal lengths. Seven configurations are shown.

**Summary grid — Film Plane**
![Film Plane Distortion — Summary Grid](assets/film-plane-distortion-summary.png)

Individual configurations:

| Tilt | Swing | Effect | Render |
|---|---|------|------------|
| 0° | 0° | Reference — no shift | ![C0](assets/film-plane-distortion-c0.png) |
| +42° | 0° | Subtle keystone | ![C1](assets/film-plane-distortion-c1.png) |
| −42° | 0° | Dramatic keystone | ![C2](assets/film-plane-distortion-c2.png) |
| 0° |  +20° | Radical perspective break | ![C3](assets/film-plane-distortion-c3.png) |
| 0° | −20° | Inverted max tilt. Bottom rushes forward. Ground-rush effect | ![C4](assets/film-plane-distortion-c4.png) |
| 0° | 0° | Flat plane 2162mm closer than nominal. Uniform magnification boost ~2.3× | ![C5](assets/film-plane-distortion-c5.png) |
| 42.1° | 15° | Diagonal perspective break — no parallel lines | ![C6](assets/film-plane-distortion-c6.png) |

---

## 2. Tilt-Swing Board Distortion Renders

**Summary grid — Tilt & Swing Board**
![Film Plane Distortion — Summary Grid](assets/tilt-swing-board-distortion-summary.png)

| Tilt | Swing | Effect | Render |
|---|---|------|------------|
| 0° | 0° | Reference — no shift | ![C0](assets/tilt-swing-board-distortion-c0.png) |
| +2° | 0° | Subtle vertical steering | ![C1](assets/tilt-swing-board-distortion-c1.png) |
| +5.3° | 0° | Max vertical shift (+207mm) | ![C2](assets/tilt-swing-board-distortion-c2.png) |
| -5.3° | 0° | Max downward shift (-207mm) | ![C3](assets/tilt-swing-board-distortion-c3.png) |
| 0° | +2° | Subtle horizontal steering | ![C4](assets/tilt-swing-board-distortion-c4.png) |
| 0° | +5.3° | Max horizontal shift | ![C5](assets/tilt-swing-board-distortion-c5.png) |
| +3° | +3° | Compound diagonal steering | ![C6](assets/tilt-swing-board-distortion-c6.png) |

---

## 3. Combined Distortion Renders (Film Plane + Tilt-Swing Board)

Compound optical projections when both the film plane mechanism and the tilt-swing
front board (TBS-TS01) are active simultaneously. Nine configurations are shown.
The two systems interact non-linearly — their combined effects cannot be decomposed
into a simple sum of the individual systems' projections.

**Summary grid — all 9 configurations**
![Tilt-Swing Combined Distortion — Summary Grid](assets/tilt-swing-combined-summary.png)

Individual configurations:

| Board/Tilt | Board/Swing | Film/Tilt | Film/Swing | Effect | Render |
|---|---|---|---|------|------------|
| 0° |  0° |   0° |   0° |  Reference All flat | ![C0](assets/tilt-swing-combined-c0.png) |
| 3° |  0° |   0° |   0° |  Board tilt +3° Film flat | ![C1](assets/tilt-swing-combined-c1.png) |
| 0° |  0° |   20° |   0° |  Film tilt +20° Board flat | ![C2](assets/tilt-swing-combined-c2.png) |
| 3° |  0° |   20° |   0° |  Opposing tilt (partially cancelled) | ![C3](assets/tilt-swing-combined-c3.png) |
| 3° |  0° |   -20° |   0° |  Opposing tilt (partially cancelled) | ![C4](assets/tilt-swing-combined-c4.png) |
| 0° |  3° |   0° |   15° |  Both swing + same direction | ![C5](assets/tilt-swing-combined-c5.png) |
| 3° |  3° |   0° |   0° |  Compound board (tilt+swing) flat film | ![C6](assets/tilt-swing-combined-c6.png) |
| 3° |  3° |   20° |   15° |  Full compound both systems (max distortion) | ![C7](assets/tilt-swing-combined-c7.png) |
| -3° |  3° |   20° |   -15° |  Opposing compound (surrealist) | ![C8](assets/tilt-swing-combined-c8.png) |

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*
