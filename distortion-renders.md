<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Distortion Renders — Film Plane & Tilt-Swing

This page collects all ray-traced distortion renders for TBS-001. Two independent movement
systems produce image projections — their compound effects interact non-linearly.

Source reports: [Film Plane Mechanism](film-plane-mechanism-report.md) and
[Tilt-Swing Front Board](tilt-swing-board-report.md).

---

## 1. Film Plane Distortion Renders

Four-corner independent actuation of the film plane. Each corner moves ±<!-- BEGIN fact:film_plane_max_tilt -->40<!-- END fact:film_plane_max_tilt -->° tilt
and ±<!-- BEGIN fact:film_plane_max_swing -->28<!-- END fact:film_plane_max_swing -->° swing independently, producing Scheimpflug-equivalent projections at pinhole
focal lengths. Six configurations are shown.

**Summary grid — Film Plane**
![Film Plane Distortion — Summary Grid](assets/film-plane-distortion-summary.png)

Individual configurations:

The plane is a fixed-size rigid rectangle, so every configuration is a **flat** tilt or swing — a compound *twist* is not producible.

| Config | Tilt | Effect | Render |
|---|---|------|------------|
| C0 | 0° | Reference — no distortion | ![C0](assets/film-plane-distortion-c0.png) |
| C1 | 11° | Subtle keystone | ![C1](assets/film-plane-distortion-c1.png) |
| C2 | 30° | Strong keystone | ![C2](assets/film-plane-distortion-c2.png) |
| C3 | 40° | Max tilt (design max) — radical perspective break | ![C3](assets/film-plane-distortion-c3.png) |
| C4 | −40° | Inverted max tilt — bottom rushes forward, ground-rush effect | ![C4](assets/film-plane-distortion-c4.png) |
| C5 | 0° (near) | Flat plane 2,162mm closer — uniform magnification boost ~2.3× | ![C5](assets/film-plane-distortion-c5.png) |

---

## 2. Tilt-Swing Board Distortion Renders

**Summary grid — Tilt & Swing Board**
![Film Plane Distortion — Summary Grid](assets/tilt-swing-board-distortion-summary.png)

| Tilt | Swing | Effect | Render |
|---|---|------|------------|
| 0° | 0° | Reference — no shift | ![C0](assets/tilt-swing-board-distortion-c0.png) |
| +2° | 0° | Subtle vertical steering | ![C1](assets/tilt-swing-board-distortion-c1.png) |
| +5.3° | 0° | Max vertical shift (+<!-- BEGIN fact:front_board_max_shift_mm -->219<!-- END fact:front_board_max_shift_mm -->mm) | ![C2](assets/tilt-swing-board-distortion-c2.png) |
| -5.3° | 0° | Max downward shift (-<!-- BEGIN fact:front_board_max_shift_mm -->219<!-- END fact:front_board_max_shift_mm -->mm) | ![C3](assets/tilt-swing-board-distortion-c3.png) |
| 0° | +2° | Subtle horizontal steering | ![C4](assets/tilt-swing-board-distortion-c4.png) |
| 0° | +5.3° | Max horizontal shift | ![C5](assets/tilt-swing-board-distortion-c5.png) |
| +3° | +3° | Compound diagonal steering | ![C6](assets/tilt-swing-board-distortion-c6.png) |

---

## 3. Combined Distortion Renders (Film Plane + Tilt-Swing Board)

Compound optical projections when both the film plane mechanism and the tilt-swing
front board are active simultaneously. Nine configurations are shown.
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
| 3° |  0° |   20° |   0° |  Opposing tilt (partially canceled) | ![C3](assets/tilt-swing-combined-c3.png) |
| 3° |  0° |   -20° |   0° |  Opposing tilt (partially canceled) | ![C4](assets/tilt-swing-combined-c4.png) |
| 0° |  3° |   0° |   15° |  Both swing + same direction | ![C5](assets/tilt-swing-combined-c5.png) |
| 3° |  3° |   0° |   0° |  Compound board (tilt+swing) flat film | ![C6](assets/tilt-swing-combined-c6.png) |
| 3° |  3° |   20° |   15° |  Full compound both systems (max distortion) | ![C7](assets/tilt-swing-combined-c7.png) |
| -3° |  3° |   20° |   -15° |  Opposing compound (surrealist) | ![C8](assets/tilt-swing-combined-c8.png) |

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*
