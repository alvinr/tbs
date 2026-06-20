<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Funding Proposal Outline
## The Big Shoebox: A Deployable Room-Scale Camera

*Proposal outline for arts non-profits, MFA/BFA thesis boards, and artist residency programs.*
*Target funders: NEA, Puffin Foundation, Aperture Foundation, CERF+, Headlands Center for the Arts, Skowhegan School of Painting and Sculpture, university equipment grants.*

---

## 1. The Hook
A standard shipping container sits in a field. Inside, on 116 square feet of cotton fabric, a cyanotype image is forming. The image will be approximately 15 feet wide and 8 feet tall. The people who made it will wade into the image to develop it.

The container is a camera.

Not a reference to a camera. Not a metaphor. A working, optically precise, transportable pinhole camera. The largest operative example documented. Built to produce full-contact-scale cyanotype photographs of whatever landscape, cityscape, or architectural space it is placed in front of.

**The Big Shoebox Project** is the design, fabrication, and operation of that camera.

## 2. Project Overview

### What
TBS-001 is a 20-foot ISO shipping container converted into a functional large-format pinhole camera. The pinhole (<!-- BEGIN fact:pinhole_diameter_mm -->2.17<!-- END fact:pinhole_diameter_mm -->mm, precision laser-drilled, stainless steel) sits at one side of the container. The image plane — a stretched cotton muslin surface spanning the active <!-- BEGIN fact:film_plane_width_mm -->4499<!-- END fact:film_plane_width_mm --> × <!-- BEGIN fact:film_plane_height_mm -->2388<!-- END fact:film_plane_height_mm -->mm film zone — sits at the other. Every exposure produces a latent cyanotype image on approximately 116 square feet of fabric, developed in plain water.

![TBS-001 Container Floor Plan](assets/container-floorplan.png)

### How
The optical specification follows the Lord Rayleigh formula for optimal pinhole diameter (d = 1.9√(fλ), λ = 550 nm), yielding an f-number of f/1088 and a baseline exposure of approximately 30–45 minutes in direct sunlight using the *Mike Ware New Cyanotype formula* on cotton muslin. Every design decision — aperture, image plane materials, exposure calculation, process chemistry — traces to a peer-reviewed source or manufacturer datasheet. The full technical documentation is publicly available at [alvinr.github.io/tbs](https://alvinr.github.io/tbs/).

The camera is transportable by commercial hire truck (no Commercial Drivers License required) and operates off-grid via a self-contained water system that supports ~13 full-size prints between resupply runs.

### Why Now
The history of large-format photography is a history of increasing precision in decreasing size. The view camera shrank from room to studio to field. The Big Shoebox inverts that trajectory: it scales a camera back up to architectural dimensions, not as spectacle, but as instrument. The container is not incidental to the work — it is the camera body. The constraint of the container's interior geometry is the optical specification. Site, transport, and access become compositional decisions.

## 3. Technical Innovation
The project incorporates two independent movement systems — equivalent to the front and rear standards of a view camera — operating at pinhole focal lengths. No camera of this type is known to exist.

### Front Board: Tilt and Swing (±<!-- BEGIN fact:front_board_max_deg -->5.3<!-- END fact:front_board_max_deg -->°)
A spherical-pivot adapter plate mounts in the same wall-frame interface as the vanilla pinhole plate. A GE50-DO-2RS spherical plain bearing (PTFE-lined, maintenance-free) allows the pinhole to pivot up to ±5.3° in both tilt and swing. Four M8×1.0 fine-pitch adjustment screws with 36-detent knurled knobs provide 0.012° per click resolution.

**Effect:** every 5° of board tilt steers the projected image 207mm across the film plane (2,362 × tan 5°). Used for compositional placement — shifting what part of the scene falls where on the print without moving the camera.

### Film Plane: 4-Corner Independent Actuation (±<!-- BEGIN fact:film_plane_max_tilt -->40<!-- END fact:film_plane_max_tilt -->° tilt, ±<!-- BEGIN fact:film_plane_max_swing -->28<!-- END fact:film_plane_max_swing -->° swing)
Four independently-driven corners allow the fixed-size rigid image plane (Option A) to be tilted and swung — including limited combined tilt-and-swing — about its center. Each corner is driven by a 3/4"-6 Acme leadscrew via an 8" handwheel; a 2-axis cross-slide and rod-end spherical bearing (GIR25-DO) at each corner absorb the rigid-rotation arc travel, so the plane rotates without stretching or twisting.

**Effect:** Scheimpflug-equivalent movements at pinhole focal lengths — not to adjust focus (pinholes have infinite depth of field) but to control perspective, convergence, and geometric projection.

### Combined Operation
The two systems interact non-linearly. When both are engaged simultaneously, the resulting optical projection cannot be predicted by either system alone and cannot be produced by any other camera type. A front board tilt combined with an opposing film plane tilt partially cancels the image shift while introducing a subtle S-curve geometric distortion. Full compound operation — both axes of both systems simultaneously — produces images where no lines remain parallel in any axis.

![Combined tilt-swing distortion renders — all configurations](assets/tilt-swing-combined-summary.png)

These interactions are modeled and documented in the [combined distortion renders](tilt-swing-board-report.md), produced from a two-step ray-tracing projection model derived from first principles.

### Design Rigor
All specifications are citable. Optical derivations reference Rayleigh (1891), Smith's *Modern Optical Engineering*, and the Schwarzschild reciprocity failure model. Mechanical specifications reference SKF bearing datasheets, McMaster-Carr part numbers, and manufacturer tolerance standards. The full documentation — 12 technical reports, 3-sheet engineering drawings per mechanism, Python source for all optical simulations — is open and free to reuse.

## 4. Artistic Vision
The pinhole camera's defining property is infinite depth of field: near and far are equally sharp. Every element of a scene — a blade of grass at three feet, a mountain at thirty miles — records at the same clarity. This is not a limitation to work around. It is the medium's fundamental statement about attention: everything matters equally.

The movement systems add a second layer. The front board and film plane allow the photographer to place the image precisely on the print surface, to compress or expand perspective, to make the geometry of the scene converge or diverge. But unlike a view camera's Scheimpflug movements, which are used to adjust focus, these movements have no focus to adjust. They are purely compositional.

**The result:** a camera with infinite depth of field and view-camera-level geometric control, operating at a scale where the print becomes an environment. Viewers do not stand in front of the image. They enter it. A nearly 15-foot-wide cyanotype print on fabric can be stretched across a gallery wall, suspended from a ceiling, or laid on the ground. The scale changes the relationship between image and the viewer.

The cyanotype process connects the work to the deepest history of photography. Anna Atkins made the first photographic book in 1843 using the cyanotype process — iron salts exposed to UV, developed in plain water. (Atkins used the classical ferric-ammonium-citrate formula; TBS-001 uses the modern, far more UV-sensitive Mike Ware ammonium-iron(III)-oxalate variant of the same process.) The blue-white palette of cyanotype — Prussian blue base, white highlights — is one of the most immediately recognizable photographic aesthetics. Working at this scale in this process is a deliberate claim about what photography was before the silver-gelatin era standardized it.

The camera is deployable. It comes to the subject. A landscape that could never be brought to a studio is instead surrounded by the camera. The field, the parking structure, the salt flat, the housing development — each becomes not just the subject but the site of the printing, developed there in plain water and hung to dry in the same air that made the exposure.

## 5. Process and Sustainability

### Chemistry
Cyanotype uses the **Mike Ware New Cyanotype formula** — ammonium iron(III) oxalate and potassium ferricyanide, with an optional trace of ammonium dichromate (0.1–0.4%) for added contrast. The two base reagents require no DEA registration, hazmat shipping, or special disposal; only the trace dichromate needs careful handling — at a tiny fraction of the bulk quantities used by dichromate-sensitized processes. Development is plain cold water. The chemistry is mixed on-site; the substrate (unbleached cotton muslin) is coated by brush or roller in two wet-on-wet coats, dried, and loaded in darkness. The Ware formula is 4–8× more UV-sensitive than the classical Herschel formula, reducing baseline exposure from ~2 hours to ~30–45 minutes in full sun.

Per-print cost: approximately <!-- BEGIN costing:fund-perprint -->$33<!-- END costing:fund-perprint --> (chemistry + fabric + water) at the Standard sensitizer strength — ranging <!-- BEGIN costing:fund-perprint-range -->$24–60<!-- END costing:fund-perprint-range --> by tier, to be pinned by post-build sensitizer trials. A 50-print run costs approximately <!-- BEGIN costing:fund-50run -->$1,650<!-- END costing:fund-50run -->. By comparison, the next cheapest alternative (gum bichromate) costs ~$49 per print and depends on bulk dichromate as its primary sensitizer, with full hazmat handling and disposal.

### Water System
A self-contained three-circuit water system — Blue (wash), Brown (recycle), and Black (waste) — provides off-grid processing capability. Four 1000L IBC totes in a 2×2 stack, 12V DC pumps (P-01/P-02/P-04 supply + filter + sump, plus P-05/P-03 drain pumps; corridor-mounted), check valves on all external lines, and a 3-stage filtration skid. Capacity: ~13 full prints between resupply. Water recycling: approximately 40% of used wash water is recovered and reused. Power: 12V DC from a 100Ah LiFePO4 battery (expandable to 200Ah with an optional second pack; ~2–3 prints per charge), with a 600W solar array for field recharging — the system is solar-positive in sun, so it runs indefinitely — plus shore-power input for overnight top-up.

The system was designed for remote deployments: no municipal water connection required.

### Transportation
The container moves by commercial hire tilt-bed truck. No CDL is required for the operator (the trucking company provides the driver). No oversize or overweight permit is required for an empty 20ft standard container on Interstate highways. Local deployment: $300–$500 per move. Short regional haul (30–100 miles): $500–$1,200.

## 6. Budget and Use of Funds
All figures are drawn from the [full cost breakdown](project-cost-breakdown.md). Per-item procurement details with supplier URLs are in the [master shopping list](master-shopping-list.md). Three funding levels are presented to allow partial or phased support.

### Level 1 — Core Build (~<!-- BEGIN costing:fund-l1-total -->$27,518<!-- END costing:fund-l1-total -->, Standard scenario)
Everything required to operate the camera for a first deployment. Figures are the Standard (Mid) column of the [cost breakdown](project-cost-breakdown.md); Low–High scenarios span ~<!-- BEGIN costing:fund-scenario-span -->$20,000–$32,000<!-- END costing:fund-scenario-span -->.

<!-- BEGIN costing:funding-level1 -->
| Item | Cost |
|------|------|
| 20ft container (Cargo Worthy grade) + delivery | $3,300 |
| Interior conversion (light-seal, paint, image-plane backing) | $1,138 |
| Pinhole plate (precision laser-drilled, SS-302, interchangeable frame) | $165 |
| Film plane mechanism (4-corner Option A, manual actuation) | $3,813 |
| Tilt-swing front board mechanism | $1,470 |
| Housed revolving-door light trap (plastic-skin Ø900 housing + C-shell drum, bearings, seals, fabrication) | $1,802 |
| Processing water system (tray, spray bar, 3-stage filtration, IBC stacking frame) | $5,085 |
| Power & electrical (600W solar · LiFePO4 · MPPT · distribution · protection · lighting) | $2,265 |
| Ventilation & cooling (2 fans · evap cooler + 12V→120V inverter · light-safe ducting) | $884 |
| Perimeter walkway (4 sections + drum-exit punch-out) | $2,214 |
| Panel swing pivot (Ø89 post + bearings + cage + wall stays) | $1,232 |
| Cyanotype chemistry + muslin substrate (50-print run, Standard tier) | $1,650 |
| Contingency (10%) | ~$2,500 |
| **Level 1 total** | **~$27,518** |
<!-- END costing:funding-level1 -->

### Level 2 — First Deployment (+$1,350–2,800)
Transport, permits, and water resupply for a single public deployment:

| Item | Cost |
|------|------|
| Commercial transport (short haul, 30–100 miles, round trip) | $1,000–2,400 |
| Location permit (public land, non-commercial art use) | $0–300 |
| Water resupply (~420 gal / 1,600L Blue tank ≈ 13 prints) | $25–50 |
| **Level 2 total** | **~$1,350–2,800** |

### Level 3 — Documentation (+$2,000–4,000)
Video documentation, process photography, and initial publication:

| Item | Cost |
|------|------|
| Videography (1–2 deployment days) | $1,000–2,500 |
| Photography (behind-the-scenes, prints) | $500–1,000 |
| Publication design (zine or catalogue, print run) | $500–1,500 |
| **Level 3 total** | **~$2,000–4,000** |

**Combined (Levels 1+2+3):** ~<!-- BEGIN costing:fund-combined -->$30,868–34,318<!-- END costing:fund-combined --> for a complete first-year program with three public deployments, 50-print edition, and full documentation.

## 7. Timeline
A 12-month build and deployment program:

| Month | Milestone |
|-------|-----------|
| 1–2 | Container acquisition, delivery, initial light-sealing |
| 2–4 | Interior conversion: paint, backing panels, ventilation, door seals |
| 4–5 | Mechanism fabrication: film plane, tilt-swing front board, water system |
| 5–6 | Fit-out, calibration, test exposures (dark frame verification) |
| 6 | First public deployment — test shoot, process documentation |
| 7–9 | Second and third deployments (target: distinct landscape/urban/architectural) |
| 9–11 | Print edition: 50 cyanotype prints on fabric, archival storage |
| 11–12 | Exhibition (prints + documentation + open documentation site) |

## 8. Dissemination and Impact

### Public Deployments (minimum 3 in funding period)
Each deployment is a public event. The container is placed on-site; visitors can observe or participate in the coating, exposure, and development process. Invitations extended to local schools, photography programs, and community organizations at each site.

### Archival Print Edition
50 cyanotype prints on cotton muslin, each approximately <!-- BEGIN fact:film_plane_width_mm -->4499<!-- END fact:film_plane_width_mm --> × <!-- BEGIN fact:film_plane_height_mm -->2388<!-- END fact:film_plane_height_mm -->mm (~14'9" × 7'10"). Numbered, signed, with full exposure metadata. Available for acquisition by institutions and private collectors.

### Open Documentation Site
All design files, optical derivations, engineering drawings, and Python simulation source code are published openly at [alvinr.github.io/tbs](https://alvinr.github.io/tbs/) under a permissive license. Any institution or practitioner who wants to build a similar camera has everything required to do so — without starting from scratch.

This is intentional. The project is as much a contribution to the field as it is a body of work. The permissive license encourages others to tweak and modify this design, contributing back to improve the body of knowledge for all.

### Educational Programming
- Workshops at each deployment site: optics, cyanotype chemistry, large-format process
- Open submission to alternative process photography publications (*Photovision*, *VIEW Camera*, *Pictorial*)
- Public lecture/presentation at host institution or adjacent MFA program

## 9. Artist Statement / Bio
Photography taught me patience before anything else. As a teenager I would drop film at the post office and wait — two weeks, sometimes three — before I knew whether the image I had imagined, had indeed materialized. That interval, between exposure and knowledge, was the first version of what this project is. Like the slow food movement today, this was slow photography.

At Nottingham Trent University I encountered the pinhole camera and understood immediately that something both maddening and transformative was possible with it. I graduated with a First in Photography in 1998 — my dissertation, *Deeds of War*, was acquired by the NTU library, and my photographs were selected for exhibition by the Royal Photographic Society.

Through the late 1990s I worked as a photojournalist with the International Committee of the Red Cross, documenting people inside conflicts the world was not watching. It was there I encountered Alistair Thain's large-format photographs made in Sarajevo during the siege, and understood that the gravity of a slow process is not a constraint. It was the point. That work was about witness — about making visible what others could not, or would not, see. It put a thought deep in the the back of my mind... why I had not taken the 5x4 camera I had constructed into that same environment?

My practice since has moved between classical portraiture and abstract color in found industrial spaces — shot on film, in darkrooms I have built. The through-line: a fascination with applying old processes to the contemporary world, to see what they can still reveal. The Big Shoebox Project is where that becomes architecture — a camera built to make a single image in 45 minutes of sun, to stretch time, distort it, and make it visible. This is modern analog slow photography.

## 10. Appendix

### Camera Specification Summary
| Parameter | Value |
|-----------|-------|
| Container | 20ft ISO standard (6,058 × 2438 × 2591mm exterior) |
| Focal length | 2362mm |
| Image plane (active) | <!-- BEGIN fact:film_plane_width_mm -->4499<!-- END fact:film_plane_width_mm --> × <!-- BEGIN fact:film_plane_height_mm -->2388<!-- END fact:film_plane_height_mm -->mm (~14'9" × 7'10") |
| Container interior | 5893 × 2388mm (~19'4" × 7'10") |
| Image area | ~116 sq ft |
| Optimal pinhole | Ø2.17mm (Rayleigh formula, λ=550nm) |
| f-number | f/1088 |
| Baseline exposure | ~30–45 min (Ware New Cyanotype on muslin, f/1088, full sun — no reciprocity correction) |
| Film plane movement | ±40° tilt, ±28° swing, 4-corner independent (Option A rigid plane) |
| Front board movement | ±5.3° tilt and swing, 0.012°/click resolution |
| Process | Cyanotype (Ware formula) on cotton muslin |
| Water system | Self-contained, ~13 prints per resupply, off-grid capable |
| Transport | Commercial hire tilt-bed, no CDL required |

### Full Documentation
All technical reports, fabrication drawings, optical simulations, and shopping lists:
**[alvinr.github.io/tbs](https://alvinr.github.io/tbs/)**

### Sample Optical Renders
The combined distortion renders (see [Tilt-Swing Front Board report](tilt-swing-board-report.md)) demonstrate the range of optical projections available from the combined movement systems — from an undistorted reference frame to compound diagonal projections where no lines remain parallel. These are not post-processing effects. They are the direct optical output of the camera's movement systems, modeled from first principles and replicable in the physical instrument.