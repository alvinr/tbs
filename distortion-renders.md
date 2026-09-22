<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Distortion Renders — Film Plane

This page collects the ray-traced distortion renders for TBS-001. All perspective and keystone
control comes from one movement system: the film plane (rear standard). The front board is a fixed
[quick-change pinhole disc holder](pinhole-disc-holder-report.md) — a pinhole is a point aperture, so
tilting the board that holds it does not steer or distort the image. Every render below is produced
by film-plane movement alone.

Source report: [Film Plane Mechanism](film-plane-mechanism-report.md).

---

## 1. Film Plane Distortion Renders

Four-corner independent actuation of the film plane. Each corner moves ±<!-- BEGIN fact:film_plane_max_tilt -->40<!-- END fact:film_plane_max_tilt -->° tilt
and ±<!-- BEGIN fact:film_plane_max_swing -->28<!-- END fact:film_plane_max_swing -->° swing independently, producing Scheimpflug-equivalent projections at pinhole
focal lengths. Six configurations are shown.

**Summary grid — Film Plane**
![Film Plane Distortion — Summary Grid](assets/film-plane-distortion-summary.png)

Individual configurations:

The plane is a fixed-size rigid rectangle, so every configuration is a **flat** tilt or swing — a compound *twist* is not producible.

<!-- brochure:skip -->
| Config | Tilt | Effect | Render |
|---|---|------|------------|
| C0 | 0° | Reference — no distortion | ![C0](assets/film-plane-distortion-c0.png) |
| C1 | 11° | Subtle keystone | ![C1](assets/film-plane-distortion-c1.png) |
| C2 | 30° | Strong keystone | ![C2](assets/film-plane-distortion-c2.png) |
| C3 | 40° | Max tilt (design max) — radical perspective break | ![C3](assets/film-plane-distortion-c3.png) |
| C4 | −40° | Inverted max tilt — bottom rushes forward, ground-rush effect | ![C4](assets/film-plane-distortion-c4.png) |
| C5 | 0° (near) | Flat plane 2,162mm closer — uniform magnification boost ~2.3× | ![C5](assets/film-plane-distortion-c5.png) |
<!-- brochure:endskip -->
