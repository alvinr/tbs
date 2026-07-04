<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# The Big Shoebox — Project Summary

<div style="text-align:center;">
  <img src="assets/logo-final.png" alt="The Big Shoebox Project" style="width:40%">
</div>

---

## What Is It

A fully operational pinhole camera built inside a standard 20-foot ISO shipping container. It makes photographs — real, large-format photographs — on contact-scale cyanotype prints measuring approximately 15 feet wide by 8 feet tall. It is transportable, deployable in remote locations, and self-sufficient for water and processing. It is not an installation that resembles a camera. It is a camera.

<div class="sketchfab-embed-wrapper">
  <div style="position:relative;width:100%;padding-bottom:56.25%;">
    <iframe title="TBS-001 Overview" frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" execution-while-out-of-viewport execution-while-not-rendered web-share src="https://sketchfab.com/models/e624e210bf3d4de08b1a7b7261a66c45/embed" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"></iframe>
  </div>
  <p style="font-size: 13px; font-weight: normal; margin: 5px; color: #4A4A4A;"><a href="https://sketchfab.com/3d-models/tbs-001-overview-e624e210bf3d4de08b1a7b7261a66c45?utm_medium=embed&utm_campaign=share-popup&utm_content=e624e210bf3d4de08b1a7b7261a66c45" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">TBS-001 Overview</a> by <a href="https://sketchfab.com/alvin91403?utm_medium=embed&utm_campaign=share-popup&utm_content=e624e210bf3d4de08b1a7b7261a66c45" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">alvin91403</a> on <a href="https://sketchfab.com?utm_medium=embed&utm_campaign=share-popup&utm_content=e624e210bf3d4de08b1a7b7261a66c45" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">Sketchfab</a></p>
</div>

---

## The Scale

| Parameter | Value |
|-----------|-------|
| Image plane (active) | <!-- BEGIN fact:film_plane_width_mm -->4,499<!-- END fact:film_plane_width_mm --> × <!-- BEGIN fact:film_plane_height_mm -->2,388<!-- END fact:film_plane_height_mm -->mm (~14'9" × 7'10") |
| Container interior | <!-- BEGIN fact:container_interior_length_mm -->5,893<!-- END fact:container_interior_length_mm --> × <!-- BEGIN fact:container_height_mm -->2,388<!-- END fact:container_height_mm -->mm (~19'4" × 7'10") |
| Image area | ~<!-- BEGIN fact:image_area_sqft -->116<!-- END fact:image_area_sqft --> sq ft |
| Focal length | <!-- BEGIN fact:focal_length_mm -->2,362<!-- END fact:focal_length_mm -->mm (container interior depth) |
| Optimal pinhole | Ø<!-- BEGIN fact:pinhole_diameter_mm -->2.17<!-- END fact:pinhole_diameter_mm -->mm (Lord Rayleigh formula, λ = 550 nm) |
| f-number | f/<!-- BEGIN fact:f_number -->1088<!-- END fact:f_number --> |
| Baseline exposure | ~30–45 min (Ware New Cyanotype on muslin, f/1088, full sun — no reciprocity correction) |
| Process | Cyanotype (Ware formula) — water-based, non-toxic, no silver |
| Per-print cost | ~<!-- BEGIN costing:summary-perprint -->$33<!-- END costing:summary-perprint --> |
| 50-print run | ~<!-- BEGIN costing:summary-50run -->$1,650<!-- END costing:summary-50run --> |
| License | [GNU AGPLv3](licensing.md) — © 2026 Alvin Richards |

---

## The Technology

Two independent movement systems work in series, stacking their effects non-linearly:

**Front board — tilt and swing (±<!-- BEGIN fact:front_board_max_deg -->5.3<!-- END fact:front_board_max_deg -->°)**
The pinhole itself pivots on a spherical plain bearing, steering the image cone across the film plane. Every 5° of tilt shifts the projected image <!-- BEGIN fact:image_shift_per_5deg -->207<!-- END fact:image_shift_per_5deg -->mm. Used for compositional placement — not correction, not distortion, but deliberate image steering.

**Film plane — 4-corner independent actuation (±<!-- BEGIN fact:film_plane_max_tilt -->40<!-- END fact:film_plane_max_tilt -->° tilt, ±<!-- BEGIN fact:film_plane_max_swing -->28<!-- END fact:film_plane_max_swing -->° swing)**
Four corners of the image plane move independently via handwheels, enabling view-camera-style geometric control at pinhole focal lengths. Scheimpflug-equivalent movements, compound twisted-plane projections, convergence manipulation — the full vocabulary of large-format photography, applied to a pinhole.

**Combined:** the two systems interact non-linearly. Their compound optical projections — modeled and documented in the [distortion renders](tilt-swing-board-report.md) — produce images that no other camera type can make.

Every specification traces to a peer-reviewed source or manufacturer datasheet. The optics are not approximated.

**Off-grid capable:** a self-contained three-circuit water system supports ~<!-- BEGIN fact:prints_per_resupply -->14<!-- END fact:prints_per_resupply --> full-size prints between resupply runs, with 40% water recycling. 12V DC operation. Deployable without power connection.

---

## The Process

Cyanotype on cotton muslin using the **Mike Ware New Cyanotype formula** (ammonium iron(III) oxalate + potassium ferricyanide). Baseline exposure 30–45 minutes in full sun at f/1088 — 4–8× faster than the traditional Herschel formula. Developed in plain cold water, no silver or hazardous chemistry required.

The container travels by commercial hire truck. No CDL required for the operator. No oversize permits required for an empty 20ft standard container on Interstate highways.

---

## Documents

| Document | Description |
|----------|-------------|
| [Pinhole Optics Report](pinhole-optics-report.md) | Lord Rayleigh formula, f-numbers, exposure calculations |
| [Container Optics](pinhole-option-b-optics.md) | Detailed optics for the shipping container configuration |
| [Container Selection & Construction](container-report.md) | Container options, US transport compliance, interior conversion, light-sealing |
| [Lens Options](lens-options.md) | Coverage problem, thin lens equations, DoF, distortion, recommendations |
| [Lens vs Pinhole](lens-vs-pinhole-exposure.md) | Why the exposure difference is ~5,500× — full derivation |
| [Photosensitive Materials](photosensitive-plane-options.md) | All process options, ISO equivalents, spectral response, per-image costs |
| [Processing System](water-system-report.md) | Off-grid three-circuit water system design and Bill of Materials |
| [Film Plane Mechanism](film-plane-mechanism-report.md) | 4-corner independent actuation — design, drawings, shopping list |
| [Film Clamp Mechanism](film-clamp-mechanism-report.md) | Cam-lever spring clamp system — 92 clamps at 150mm spacing, parts list |
| [Pinhole Report](pinhole-report.md) | Interchangeable plate system — wall frame, pinhole plate, lens plate |
| [Tilt-Swing Front Board](tilt-swing-board-report.md) | Spherical-pivot mechanism — design, drawings, combined distortion renders |
| [Cost Breakdown](project-cost-breakdown.md) | Full itemized build cost — three scenarios, all sources cited |
| [Chem Shopping List](chemistry-shopping-list.md) | 50-print quantities with supplier URLs and confirmed prices |
| [Transportation](container-transport-options.md) | Commercial hire vs. self-haul analysis |
| [Operating Manual](operating-manual.md) | Single-operator step-by-step workflow — coating, exposure, development, cleanup |
| [Electrical & Systems](electrical-report.md) | Power architecture, revolving drum light trap, lighting, wiring diagrams |
| [Ventilation & Cooling](ventilation-report.md) | Fan system, evaporative cooler, light-safe baffle ducts, shade canopy, and operating modes |
| [Master Shopping List](master-shopping-list.md) | All components consolidated by build area — electrical, water, chemistry, drum light trap, cooling |
| [License](licensing.md) | GNU AGPLv3 — © 2026 Alvin Richards |
| [Light Trap Selection](light-trap-selection.md) | Revolving light trap options, pricing, and custom fabrication specification |
| [Engineering Diagrams](engineering-diagrams.md) | All TBS-001 construction drawings — assembly overview, fabrication, subsystems |
| [All Diagrams](all-diagrams.md) | Complete visual gallery of every engineering diagram on a single page |
| [Distortion Renders](distortion-renders.md) | Ray-traced projections for all film-plane and tilt-swing configurations |
| [Equipment Layout](equipment-layout-report.md) | Shadow-free end-zone layout — optical clearance proof, IBC Y-stacking, new rail positions |
