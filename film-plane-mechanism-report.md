<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Film Plane — Mechanism Design

## 1. Purpose

The configuration the photosensitive film plane is flush against one of the 20ft long-side walls of the container. This report describes a **view-camera-style moveable film plane** — a mechanism with **four independently actuated corners** (TL, TR, BL, BR), allowing full tilt, swing, and compound tilt+swing movements comparable to a large-format view camera's rear standard.

**System context — container floor plan:**
The floor plan below shows the film plane rail positions (at Y=2262mm, X=150–4649mm) in the context of the complete TBS-001 interior, including left end zone (light trap), processing tray and perimeter walkway in the optical zone, and right end zone (4× IBCs in 2×2 stack, pump manifold and filter skid on equipment panel).

![TBS-001 Container Floor Plan — All Systems](assets/container-floorplan.png)

---

## 2. Container Reference Geometry

| Dimension | Value | Notes |
|-----------|-------|-------|
| Interior length | 5893mm (19 ft 4 in) | Film plane spans this direction |
| Interior width | 2362mm (7 ft 9 in) | **Optical axis = focal length** |
| Interior height | 2388mm (7 ft 10 in) | Film plane height |
| Pinhole position | Centre of one 20ft long-side wall | |
| Nominal film plane | Opposite 20ft long-side wall | flush to wall |
| Structural ribs | Every 457mm (18 in) along length | Rail mounting points |

---

## 3. Movement Axes

The four-corner mechanism supports all view-camera movements. Corners are labelled TL (top-left), TR (top-right), BL (bottom-left), BR (bottom-right) — where left/right refers to the rail span direction and top/bottom to the 7 ft 10 in height direction.

| Axis | Corners Controlled | Max Travel | Effect |
|------|--------------------|-----------|--------|
| **Tilt (top)** | TL + TR together | 100–2262mm | Perspective convergence, keystone |
| **Tilt (bottom)** | BL + BR together | 100–2262mm | Perspective convergence, keystone |
| **Swing (left)** | TL + BL together | 100–2262mm | Left-right perspective skew |
| **Swing (right)** | TR + BR together | 100–2262mm | Left-right perspective skew |
| **Compound** | All 4 independently | 100–2262mm | Twisted plane — no lines remain parallel |
| **Back focus** | All 4 together | 100–2262mm | Uniform magnification change |
| **Rise / Fall** | All 4 together, offset vertically | ±200mm | Horizon shift |
| **Shift** | All 4 together, offset horizontally | ±300mm | Left/right perspective offset |

**Maximum tilt angle** (top vs bottom): arctan((2,262 − 100) / 2,388) ≈ **42°**

**Maximum swing angle** (left vs right): arctan((2,262 − 100) / 4,499) ≈ **25.7°**

(Swing angle is smaller than tilt angle because the active film plane is 4499mm wide — the left rail sits at X=150mm and the right rail at X=4649mm. The same Y-axis depth difference over a wider span produces a shallower angle.)

When tilted at maximum, the film plane's physical height increases from 2268mm to approximately **3180mm** — 40% longer than when flat. The backing panel accommodates this with the hinged two-panel system described below.

---

## 4. Mechanism Design

### Four-Corner Frame

Each corner of the film plane frame rides on its own independent carriage assembly:

![Sheet 6 — System Schematic: Four-Corner Frame Front Elevation](assets/film-plane-sheet6.png)

- **4 linear rails** — HiWin HGR20 profile, 2200mm length, mounted at X=150mm (left pair) and X=4649mm (right pair) on ceiling and floor. Rails run along the 2362mm optical axis direction.
- **8 carriages** — HGH20CA flanged blocks, 2 per rail, joined by an L-bracket at each corner. Each corner moves as a single independent unit.
- **4 leadscrews** — ¾"-6 Acme, 8 ft (2438mm) length, one per corner (TL, TR, BL, BR). Each turns in a bronze Acme nut fixed to the corner bracket.
- **Film plane frame** — welded 2"×2"×3/16" aluminum angle, **4499mm × 2388mm** (rail span × container height). Connected to each corner bracket via a **rod-end spherical bearing** (GIR25-DO or equivalent, 25mm bore) to allow free rotation in all axes when the plane is twisted. The following diagrams show the range of movements of the film plane.

![Sheet 1 — Plan view](assets/film-plane-sheet1.png)

Viewed from above, the full range of swing movement can be seen above. Since both side rails allow the same range of movements, it allows the maximum range of creative control.

![Sheet 2 — Elevations](assets/film-plane-sheet2.png)

View from the side, the full range of tilt movement can be seen above. Since both the top and bottom rails allow the same range of movements, it allows the maximum range of creative control.

### Mechanism Components
The master diagram for the components can be see in the diagram below. The following section discuss the details.

![Sheet 3 — Hardware detail](assets/film-plane-sheet3.png)

### Why Rod-End Spherical Bearings

With four-corner independence, the film frame can twist — the plane through the four corners is no longer flat. A simple pin joint has only one rotational degree of freedom; a rod-end spherical bearing has ±45° freedom in all axes, accommodating any combination of tilt and swing without binding.

### Actuation

Each of the four leadscrews is turned by an **8" cast aluminum handwheel** (¾" bore). One turn of the ¾"-6 screw = **4.2mm travel**. A SS316 locking collar on each screw holds position during exposure.


**Named movement modes:**
- **Pure tilt**: turn TL and TR handwheels together by the same amount; turn BL and BR by the same amount (different from TL/TR).
- **Pure swing**: turn TL and BL together; turn TR and BR together.
- **Back focus**: turn all four handwheels by the same amount.
- **Compound**: turn all four independently.

**Optional electric actuation:** replace the handwheels with **Progressive Automations PA-14** 12V linear actuators (20" / 508mm stroke, 150 lb force rating). Four actuators, one per corner, each controlled by a panel-mount DPDT momentary switch. A labelled panel outside the container allows full repositioning without entry.

### Variable Geometry Accommodation

As the film plane tilts (tilt axis), its along-plane height grows from 2268mm at 0° to approximately 3180mm at maximum 42° tilt. Swing has a smaller effect on plane size (the container is much longer than it is tall).

**Hinged two-panel ACM system:**

The backing panel is two equal ACM (aluminum composite material) sections, each ~1600mm × 2388mm, joined along the horizontal centerline with a full-width 2" aluminum piano hinge. When flat, the panels lie flush. As the plane tilts, the upper panel folds back on the hinge, maintaining full coverage at any tilt angle.

For compound tilt+swing, the film plane is a ruled surface (slightly twisted, not flat). The backing panels accommodate this because the hinge allows both fore-aft fold and a small amount of left-right twist.

---

## 5. Tilt Configurations

| Config | Name | TL | TR | BL | BR | Tilt | Swing | Film Height |
|--------|------|----|----|----|----|------|-------|-------------|
| C0 | Flat | 2262 | 2262 | 2262 | 2262 | 0° | 0° | 2388mm |
| C1 | Mild tilt | 1800 | 1800 | 2262 | 2262 | 11.0° | 0° | 2434mm |
| C2 | Strong tilt | 800 | 800 | 2262 | 2262 | 31.5° | 0° | 2724mm |
| C3 | Max tilt | 100 | 100 | 2262 | 2262 | 42.1° | 0° | 3184mm |
| C4 | Mild swing | 2262 | 1800 | 2262 | 1800 | 0° | 6.6° | 2388mm |
| C5 | Strong swing | 2262 | 800 | 2262 | 800 | 0° | 20.0° | 2388mm |
| C6 | Max swing | 2262 | 100 | 2262 | 100 | 0° | 28.3° | 2388mm |
| C7 | Compound | 100 | 2262 | 2262 | 100 | 42.1° | 28.3° | — |

*All depths measured from the pinhole wall. Swing angles calculated for 4499mm rail span (arctan(Δd/span)). Rail positions: left X=150mm, right X=4649mm.*

The compound config (C7) places TL and BR at near position, TR and BL at far — a diagonal twist. The film plane is no longer a flat rectangle; it is a ruled surface. No lines in the scene project to straight parallel lines anywhere in the image.

---

## 6. Optical Distortion Summary

All seven configurations on a checker grid (D = 8000mm):

![Distortion summary](assets/film-plane-distortion-summary.png)

A detailed analysis of the optical distortions can be found [here](complete-distortion-renders.md#1-film-plane-distortion-renders).

---

## 7. Parts List

All items ship within the United States. Local Southern California pickup noted where available.

### Structural & Rails

| Item | Spec | Qty | Source A | Source B | Est. Unit |
|------|------|-----|---------|---------|-----------|
| Linear guide rail HGR20 | 2200mm | 4 | Automation Overstock, Gardena CA | McMaster-Carr #5901T777 | $45 |
| Rail carriage HGH20CA | Flanged block | 8 | Automation Overstock / Amazon | McMaster-Carr | $18 |
| Acme leadscrew ¾"-6 | 8 ft length | **4** | Roton Products (LA area) | McMaster-Carr #6289K36 | $95 |
| Acme nut bronze ¾"-6 | — | 4 | Roton Products | McMaster-Carr #6289K512 | $12 |
| Handwheel 8" dia | ¾" bore, cast aluminum | **4** | Grainger (Anaheim / LA / SD) | McMaster-Carr #6440K64 | $35 |
| Locking collar SS316 | ¾" bore | **4** | McMaster-Carr #6436K12 | Fastenal (SoCal) | $12 |
| Corner bracket L-plate | ¼" alum. plate, 6"×8" | 4 | Metal Supermarkets SoCal | Online Metals | $20 |
| Rod-end spherical bearing | GIR25-DO or equiv., 25mm bore | 8 | McMaster-Carr #60645K73 | Amazon Industrial | $22 |
| Pivot pin SS316 | 1" dia × 8" long | 8 | McMaster-Carr #98173A150 | Fastenal (SoCal branches) | $8 |

*Items in **bold** changed quantity vs the earlier two-beam design. The two 5893mm T-slot beams have been removed.*

### Film Plane Frame

| Item | Spec | Qty | Source A | Source B | Est. Unit |
|------|------|-----|---------|---------|-----------|
| Aluminum angle 2"×2"×3/16" | 8 ft lengths | 10 | Metal Supermarkets SoCal | Online Metals | $22 |
| Dibond ACM panel 4mm | 4 ft × 8 ft sheets | 6 | Grimco, City of Industry CA | Signwarehouse | $85 |
| Black EPDM foam tape 1"×½" | 50 ft rolls | 3 | McMaster-Carr #8614K84 | Grainger | $28 |
| Rosco Duvetyne | 60" wide, 10 yd | 1 | B&H Photo | Rosco direct | $95 |
| Aluminum piano hinge 72" | 2" wide, 1/16" leaf | 2 | McMaster-Carr #1580A51 | Grainger | $28 |
| 6-mil black poly sheeting | 10 ft × 100 ft | 1 | Home Depot (local, all SoCal) | Uline | $65 |
| 2" black Gorilla Tape | 35 yd rolls | 6 | Home Depot / Target (local) | Amazon | $12 |

### Demountable Brace Cage

Two rectangular end portals of 50×50×3mm RHS mild steel brace the four-corner rail assembly, giving lateral rigidity while remaining fully demountable for transport. Joints use saddle clamps tightened by M8 thumbscrews; the left-rail segment that swings clear for drum mode is retained with quick-release ball-lock pins.

| Item | ICP # | Spec | Qty | Source A | Source B | Est. Unit |
|------|-------|------|-----|---------|---------|-----------|
| Mild steel RHS square tube | ICP-11 | 50×50×3mm, cut to length — 4 verticals @ 2188mm + 4 cross-beams @ 4499mm = 26.75 m net; order ~30 m to allow saw kerf + saddle-seat cuts | 30 m | [Metal Supermarkets SoCal](https://www.metalsupermarkets.com/product/mild-steel-square-tube-structural-welded/) | [Online Metals — 50mm×3mm sq. tube](https://www.onlinemetals.com/en/buy/carbon-steel/50mm-x-3mm-carbon-steel-square-tube-1018-metric-60-length/pid/22489) | ~$7/ft (~$23/m) est. |
| Saddle clamp for 50mm RHS | ICP-12 | Two-piece bolt-together saddle — seats one tube over another at a joint; compatible with 50×50mm square tube | 16 | [McMaster-Carr — tube clamps](https://www.mcmaster.com/products/steel-tube-clamps/) | [Amazon — square tube clamps](https://www.amazon.com/2-square-tube-clamp/s?k=2%22+square+tube+clamp) | ~$8–12 est. |
| M8 knurled thumbscrew DIN 464 | ICP-13 | M8×20mm, stainless steel 303, high-type knurled head — 2 per saddle clamp joint | 40 | [Amazon — DIN 464 M8 knurled SS](https://www.amazon.com/knurled-thumb-screws-din-464/s?k=knurled+thumb+screws+din+464) | [Maedler North America — DIN 464 M8×20 SS](https://maedlernorthamerica.com/partshop/knurled-thumb-screw-din-464-m8-x-20mm-long-stainless-steel-1-4305-pn-65499225/) | ~$2–5 est. |
| Quick-release ball-lock pin | ICP-14 | Ø10mm, 50mm usable length, stainless steel — retains demountable left-rail segment (2 joints × 2 pins = 4 off, plus 4 spares) | 8 | [McMaster-Carr — ball lock pins](https://www.mcmaster.com/products/ball-lock-pins/) | [Amazon — quick-release ball lock pins](https://www.amazon.com/quick-release-ball-lock-pins/s?k=quick+release+ball+lock+pins) | ~$6–10 est. |

*Quantities basis: 4 verticals (2× portals × 2 sides, 2188mm each, Z 100–2288mm) + 4 cross-beams (2× portals × top+bottom, 4499mm each, X 150–4649mm) = 26.75 m net RHS; 30 m ordered for waste. 16 saddle clamps: one at each of the 8 vertical-to-cross-beam corners per portal × 2 portals. 40 thumbscrews: 2 per clamp × 16 clamps = 32, plus 8 spares. 8 ball-lock pins: 2 joints on demountable left-rail segment × 2 pins + 4 spares.*

### Muslin Clamp System

See [Muslin Clamp System — Mechanism Design](film-clamp-mechanism-report.md) for the full clamp specification, parts list, and engineering drawing.

### Optional Electric Actuation

| Item | Spec | Qty | Source A | Source B | Est. Unit |
|------|------|-----|---------|---------|-----------|
| PA-14 linear actuator | 12V, 20" stroke, 150 lb | **4** | Progressive Automations | Amazon | $185 |
| 12V 30A power supply | Enclosed | 1 | Mouser | Digi-Key | $55 |
| DPDT momentary rocker | Panel-mount, 20A | **4** | Mouser | Grainger | $8 |

**Estimated materials total (manual actuation, incl. brace cage): ~$2,900**  
*Excludes fasteners, fabrication labour, and electric actuation option.*  
*Net change vs two-beam design: removed 2× T-slot beams (–$416), added 2 leadscrews +$190, 2 handwheels +$70, 4 rod-end bearings +$88, 4 corner brackets +$80, 2 locking collars +$24, brace cage +$500 (est.) → net +$536.*

### Local SoCal Metal Sourcing

- **Metal Supermarkets** — Anaheim (714-630-8463), Van Nuys (818-988-1301), San Diego (619-280-7600). Will cut to length on-site, no minimum order.
- **Grimco** — City of Industry, CA. Sign-industry ACM panel supplier, large sheet stock.
- **Automation Overstock** — Gardena, CA. Industrial surplus linear motion components; walk-in available.
- **Grainger** — branches throughout LA, Orange County, San Diego. Same-day local pickup.
- **Roton Products** — ships from the LA area; Acme screw stock cut to length.

---

## 8. Maintenance

| Interval | Task |
|----------|------|
| Before each session | Inspect muslin clamp engagement — see [Clamp System](film-clamp-mechanism-report.md) |
| Before each session | Verify all four locking collars are tight after repositioning |
| Before each session | Check EPDM foam edge seal for tears or compression set |
| Monthly | Lubricate HGR20 rails and HGH20CA carriage blocks (lithium grease) |
| Monthly | Inspect Acme leadscrew threads and bronze nuts for wear |
| Every 6 months | Check rod-end spherical bearings for play — replace if radial slop exceeds 0.2mm |
| Every 6 months | Inspect Duvetyne blackout curtains for light leaks (pinholes, fraying) |
| Annually | Check ACM panel hinge pins for corrosion; replace if stiff |
| Annually | Verify rail mounting bolts for torque at all four rail positions |
| Before transport | Lock all four corners at matching depth; tighten locking collars |

---

## 9. Source References

1. [HIWIN HGR20 Linear Guideway](https://hiwin.com/products/linear-guideways/) — 20mm profile linear guide rail and HGH20CA carriage block specifications.
2. [McMaster-Carr GIR25-DO Rod-End Bearing](https://www.mcmaster.com/rod-end-bearings) — Spherical rod-end bearing specifications (25mm bore).
3. [Progressive Automations PA-14](https://www.progressiveautomations.com/products/linear-actuator-pa-14) — 12V linear actuator specifications (optional electric actuation).
4. [Tilt-Swing Front Board Report](tilt-swing-board-report.md) — Front board mechanism for combined distortion analysis.
5. [Equipment Layout Report](equipment-layout-report.md) — Rail positions and shadow-free zone verification.

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*
