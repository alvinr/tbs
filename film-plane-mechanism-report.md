<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Film Plane — Mechanism Design

## 1. Purpose

The configuration the photosensitive film plane is flush against one of the 20ft long-side walls of the container. This report describes a **view-camera-style moveable film plane** — a mechanism with **four independently actuated corners** (TL, TR, BL, BR) carrying a **fixed-size rigid** plane (Option A), allowing tilt, swing, and limited compound movements comparable to a large-format view camera's rear standard.

**System context — container floor plan:**
The floor plan below shows the film plane rail positions in the context of the complete TBS-001 interior, including left end zone (light trap), processing tray and perimeter walkway in the optical zone, and right end zone (4× IBCs in 2×2 stack, pump manifold on the Corridor Plumbing Panel and the filter skid on the Pinhole Wall Plumbing Panel).

![TBS-001 Container Floor Plan — All Systems](assets/container-floorplan.png)

**Interactive 3D model** — the fixed-size rigid film plane on its four floating-corner cross-slide carriages (Option A), posed in an example tilt + swing, with the processing tray and a ghost of the container. Drag to orbit, scroll to zoom; the per-corner detail scenes show each HGR20 rail, carriage, leadscrew, and X/Z cross-slides.

<div class="sketchfab-embed-wrapper">
  <div style="position:relative;width:100%;padding-bottom:56.25%;">
    <iframe title="TBS-001 Film Plane Model" frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" execution-while-out-of-viewport execution-while-not-rendered web-share src="https://sketchfab.com/models/bb5394a8983a491fa541088b901c24f8/embed" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"></iframe>
  </div>
  <p style="font-size: 13px; font-weight: normal; margin: 5px; color: #4A4A4A;"><a href="https://sketchfab.com/3d-models/tbs-001-film-plane-model-bb5394a8983a491fa541088b901c24f8?utm_medium=embed&utm_campaign=share-popup&utm_content=bb5394a8983a491fa541088b901c24f8" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">TBS-001 Film Plane Model</a> by <a href="https://sketchfab.com/alvin91403?utm_medium=embed&utm_campaign=share-popup&utm_content=bb5394a8983a491fa541088b901c24f8" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">alvin91403</a> on <a href="https://sketchfab.com?utm_medium=embed&utm_campaign=share-popup&utm_content=bb5394a8983a491fa541088b901c24f8" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">Sketchfab</a></p>
</div>

---

## 2. Container Reference Geometry

| Dimension | Value | Notes |
|-----------|-------|-------|
| Interior length | <!-- BEGIN fact:container_interior_length_mm -->5,893<!-- END fact:container_interior_length_mm -->mm (19 ft 4 in) | Film plane spans this direction |
| Interior width | <!-- BEGIN fact:focal_length_mm -->2,362<!-- END fact:focal_length_mm -->mm (7 ft 9 in) | **Optical axis = focal length** |
| Interior height | <!-- BEGIN fact:film_plane_height_mm -->2,388<!-- END fact:film_plane_height_mm -->mm (7 ft 10 in) | Film plane height |
| Pinhole position | Center of one 20ft long-side wall | |
| Nominal film plane | Opposite 20ft long-side wall | flush to wall |
| Structural ribs | Every 457mm (18 in) along length | Rail mounting points |

---

## 3. Movement Axes

The four-corner mechanism supports all view-camera movements. Corners are labeled TL (top-left), TR (top-right), BL (bottom-left), BR (bottom-right) — where left/right refers to the rail span direction and top/bottom to the 7 ft 10 in height direction.

| Axis | Corners Controlled | Max Travel | Effect |
|------|--------------------|-----------|--------|
| **Tilt (top)** | TL + TR together | 100–2,262mm | Perspective convergence, keystone |
| **Tilt (bottom)** | BL + BR together | 100–2,262mm | Perspective convergence, keystone |
| **Swing (left)** | TL + BL together | 100–2,262mm | Left-right perspective skew |
| **Swing (right)** | TR + BR together | 100–2,262mm | Left-right perspective skew |
| **Compound (limited)** | Tilt + swing together | 100–2,262mm | Combined tilt+swing — limited range; plane stays **flat** (no twist) |
| **Back focus** | All 4 together | 100–2,262mm | Uniform magnification change |
| **Rise / Fall** | All 4 together, offset vertically | ±200mm | Horizon shift |
| **Shift** | All 4 together, offset horizontally | ±300mm | Left/right perspective offset |

**Maximum tilt angle** (single-axis): **<!-- BEGIN fact:film_plane_max_tilt -->40<!-- END fact:film_plane_max_tilt -->°** — set by the cross-slide Z travel (~280mm); the depth rails alone would allow ~65°.

**Maximum swing angle** (single-axis): **<!-- BEGIN fact:film_plane_max_swing -->28<!-- END fact:film_plane_max_swing -->°** — rail-depth limited ≈ 28.7°.

Swing is the binding limit because the plane is <!-- BEGIN fact:film_plane_width_mm -->4,499<!-- END fact:film_plane_width_mm -->mm wide — the same depth travel over a wider span sweeps the corner further along the rail. Combined tilt+swing is further limited — see §5.

Because the plane is a **fixed-size rigid rectangle**, its physical height stays **2,388mm at every angle** — it does not grow. Corner **cross-slides** absorb the rigid-rotation arc travel instead, so a single rigid backing panel suffices.

---

## 4. Mechanism Design

> **Note:** The drawings (Sheets 1–6) and distortion renders show **axis tilt/swing** — the rigid plane rotates about its center and **foreshortens** (it never grows), illustrated about the mid-rail position (the film back-focuses anywhere along the rail; flat-at-far-wall is the max-focal-length extreme). The interactive 3D model `models/film-plane.skp` also reflects this.

### Four-Corner Frame

Each corner of the film plane frame rides on its own independent carriage assembly:

![Sheet 6 — System Schematic: Four-Corner Frame Front Elevation](assets/film-plane-sheet6.png)

- **4 depth rails** — HiWin HGR20 profile, 2,200mm length, mounted at X=150mm (left pair) and X=4,649mm (right pair) on ceiling and floor. Rails run along the 2,362mm optical axis direction; their carriages set each corner's **depth** (focus / back-focus).
- **8 depth carriages** — HGH20CA flanged blocks, 2 per rail, joined by an L-bracket at each corner.
- **4 leadscrews** — ¾"-6 Acme, 8 ft (2,438mm) length, one per corner (TL, TR, BL, BR). Each turns in a bronze Acme nut fixed to the corner bracket and drives that corner's depth.
- **8 corner cross-slides (Option A)** — a **2-axis X-Z floating stage** at each corner (one X slide + one Z slide, ~300mm travel each, on HGR15 rail + block), bolted on top of the depth carriage. These absorb the small in-plane arc travel that a **rigid** rotation forces on each corner (≈280mm in Z at max tilt, ≈263mm in X at max swing), so the film plane stays a **fixed-size flat rectangle** instead of stretching.
- **Film plane frame** — welded 2"×2"×3/16" aluminum angle, a **FIXED-SIZE rigid rectangle, <!-- BEGIN fact:film_plane_width_mm -->4,499<!-- END fact:film_plane_width_mm -->mm × <!-- BEGIN fact:film_plane_height_mm -->2,388<!-- END fact:film_plane_height_mm -->mm** (rail span × container height). Each corner connects to its cross-slide through a **rod-end spherical bearing** (GIR25-DO or equivalent, 25mm bore), which provides the angular freedom; the cross-slide provides the translation. Together they let the rigid plane tilt and swing without the frame ever changing size. The following diagrams show the range of movements of the film plane.

![Sheet 1 — Plan view](assets/film-plane-sheet1.png)

Viewed from above, the full range of swing movement can be seen above. Since both side rails allow the same range of movements, it allows the maximum range of creative control.

![Sheet 2 — Elevations](assets/film-plane-sheet2.png)

View from the side, the full range of tilt movement can be seen above. Since both the top and bottom rails allow the same range of movements, it allows the maximum range of creative control.

### Mechanism Components
The master diagram for the components can be see in the diagram below. The following section discuss the details.

![Sheet 3 — Hardware detail](assets/film-plane-sheet3.png)

### Why Rod-End Spherical Bearings + Cross-Slides

The film plane is a **fixed-size rigid rectangle**; tilt and swing are a true **rigid-body rotation** of that rectangle. A rigid rotation moves each corner along an arc — partly along its depth rail (handled by the leadscrew carriage) and partly *across* it (in X and Z). The **2-axis cross-slide** absorbs that across-rail travel, and the **rod-end spherical bearing** (±45° freedom in all axes) takes up the angular change so nothing binds. This pairing is what lets a rigid plane tilt/swing **without stretching** — the earlier scheme instead let the frame twist into a ruled surface and grow, which a fixed-size plane does not do.

### Actuation

Each of the four leadscrews is turned by an **8" cast aluminum handwheel** (¾" bore). One turn of the ¾"-6 screw = **4.2mm travel**. A SS316 locking collar on each screw holds position during exposure.


**Named movement modes:**
- **Pure tilt**: turn TL and TR handwheels together by the same amount; turn BL and BR by the same amount (different from TL/TR).
- **Pure swing**: turn TL and BL together; turn TR and BR together.
- **Back focus**: turn all four handwheels by the same amount.
- **Compound**: turn all four independently.

**Optional electric actuation:** replace the handwheels with **Progressive Automations PA-14** 12V linear actuators (20" / 508mm stroke, 150 lb force rating). Four actuators, one per corner, each controlled by a panel-mount DPDT momentary switch. A labeled panel outside the container allows full repositioning without entry.

### Fixed-Size Plane — No Variable Geometry

Because the plane is a **fixed-size rigid rectangle**, its physical dimensions never change: the along-plane height stays **2,388mm at every tilt angle**. The arc travel that the rotation forces on each corner is taken up entirely by the **cross-slides** (≈280mm Z at max tilt, ≈263mm X at max swing), not by the frame.

**Single rigid backing panel:** the backing is **one flat ACM (aluminum composite) sheet, <!-- BEGIN fact:film_plane_width_mm -->4,499<!-- END fact:film_plane_width_mm -->mm × <!-- BEGIN fact:film_plane_height_mm -->2,388<!-- END fact:film_plane_height_mm -->mm**, bonded to the rear of the angle frame — the panel simply rotates with the rigid plane.

---

## 5. Tilt / Swing Configurations

The plane stays flat at all times, so it is always a single tilt **or** swing (or a limited combination). Corner depths below are about the **mid-rail center (1,181mm)** — add the focus offset to reposition the whole plane. Film height is **constant**.

| Config | Name | TL | TR | BL | BR | Tilt | Swing | Film Height |
|--------|------|----|----|----|----|------|-------|-------------|
| C0 | Flat | 1181 | 1181 | 1181 | 1181 | 0° | 0° | 2,388mm |
| C1 | Mild tilt | 953 | 953 | 1409 | 1409 | 11.0° | 0° | 2,388mm |
| C2 | Strong tilt | 557 | 557 | 1805 | 1805 | 31.5° | 0° | 2,388mm |
| C3 | Max tilt | 414 | 414 | 1948 | 1948 | 40.0° | 0° | 2,388mm |
| C4 | Mild swing | 923 | 1439 | 923 | 1439 | 0° | 6.6° | 2,388mm |
| C5 | Strong swing | 412 | 1950 | 412 | 1950 | 0° | 20.0° | 2,388mm |
| C6 | Max swing | 125 | 2237 | 125 | 2237 | 0° | 28.0° | 2,388mm |

*Depths measured from the pinhole wall about the mid-rail center. Tilt = asin(2·Δd_top-bottom / FP_H) about the plane center (FP_H=2388); swing = asin(2·Δd_left-right / FP_W) (FP_W=4499). Rail positions: left X=150mm, right X=4,649mm.*

**Combined tilt+swing is limited** — the corners must all stay on the rails, so the full single-axis maxima cannot be used together.

---

## 6. Optical Distortion Summary

The six achievable flat configurations (C0–C5) on a checker grid (D = 8,000mm). Because Option A's plane is always flat, each render is a pure tilt or swing; the former compound *twist* is no longer producible (the C0–C5 labels here index the render set only — independent of the §5 mechanism configuration numbers):

![Distortion summary](assets/film-plane-distortion-summary.png)

A detailed analysis of the optical distortions can be found [here](distortion-renders.md#1-film-plane-distortion-renders).

---

## 7. Parts List

All items ship within the United States. Local Southern California pickup noted where available.

<!-- BEGIN parts:film -->
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| Linear guide rail HGR20 (5901T777) | 2,200mm | 4 ea | Automation Overstock / McMaster-Carr | $180 |
| Rail carriage HGH20CA | Flanged block | 8 ea | Automation Overstock / McMaster-Carr | $144 |
| Acme leadscrew ¾"-6 (6289K36) | 8 ft length | 4 ea | Roton Products / McMaster-Carr | $380 |
| Acme nut bronze ¾"-6 (6289K512) | — | 4 ea | Roton Products / McMaster-Carr | $48 |
| Handwheel 8" dia (6440K64) | ¾" bore, cast aluminum | 4 ea | Grainger / McMaster-Carr | $140 |
| Locking collar SS316 (6436K12) | ¾" bore | 4 ea | McMaster-Carr / Fastenal | $48 |
| Corner bracket L-plate | ¼" alum. plate, 6"×8" | 4 ea | Metal Supermarkets / Online Metals | $80 |
| Cross-slide rail HGR15 (Option A) | 300mm, X-Z stage | 8 ea | Automation Overstock / McMaster-Carr | $200 |
| Cross-slide carriage HGH15CA (Option A) | Flanged block | 8 ea | Automation Overstock / McMaster-Carr | $96 |
| Cross-slide intermediate plate (Option A) | ¼" alum., joins X slide to Z slide | 4 ea | Metal Supermarkets / Online Metals | $60 |
| Rod-end spherical bearing (60645K73) | GIR25-DO or equiv., 25mm bore | 8 ea | McMaster-Carr / Amazon Industrial | $176 |
| Pivot pin SS316 (98173A150) | 1" dia × 8" long | 8 ea | McMaster-Carr / Fastenal | $64 |
| Aluminum angle 2"×2"×3/16" | 8 ft lengths | 10 ea | Metal Supermarkets / Online Metals | $220 |
| Dibond ACM panel 4mm | 4 ft × 8 ft sheets — single rigid backing, <!-- BEGIN fact:film_plane_width_mm -->4,499<!-- END fact:film_plane_width_mm -->×<!-- BEGIN fact:film_plane_height_mm -->2,388<!-- END fact:film_plane_height_mm -->mm | 6 sheet | Grimco / Signwarehouse | $510 |
| Black EPDM foam tape 1"×½" (8614K84) | 50 ft rolls | 3 roll | McMaster-Carr / Grainger | $84 |
| Rosco Duvetyne | 60" wide, 10 yd | 1 ea | B&H Photo / Rosco direct | $95 |
| 6-mil black poly sheeting | 10 ft × 100 ft | 1 roll | Home Depot / Uline | $65 |
| 2" black Gorilla Tape | 35 yd rolls | 6 roll | Home Depot / Amazon | $72 |
| Mild steel plate 8mm (laser/plasma cut + welded) | ICP-11: back-plate + exterior plate + seat + gusset per saddle; ~21 kg over 6 saddles | 6 ea | Metal Supermarkets / Online Metals | $318 |
| M12×90mm hex through-bolt + nut + washers, SS | ICP-12: wall sandwich through-bolt; 4/saddle ×6 + 4 spare | 28 ea | McMaster-Carr / Amazon | $70 |
| M8×25mm knurled thumbscrew DIN 464 | ICP-13: left-rail drop-in hold-down; 2/saddle ×4 left + 4 spare | 12 ea | Amazon / Maedler | $36 |
| M8 hex fixing bolt + nut, SS | ICP-14: right-rail permanent fixing; 2/saddle ×2 TR + spare | 8 ea | McMaster-Carr / Amazon | $16 |
| **Film total** | | | | **$3,102** |
<!-- END parts:film -->

*The cross-slide rails/carriages/intermediate plates (HGR15) are the **Option A** additions — the
2-axis X–Z cross-slide stage at each corner (8 slides total, ≈300mm travel) that lets the
**fixed-size rigid** plane tilt/swing without stretching. The two 5,893mm T-slot beams of the
original two-beam design remain removed. The wall-seat saddles (ICP-11–14) are itemized in the
table above; see below for their design.*

### Wall-Seat Saddles

Each of the **8 rail ends** anchors to the container — **6 of them** with a standalone **IBC-style wall-seat saddle** (a back-plate + horizontal seat the rail end rests on + triangular gusset, dims reused from the IBC frame wall seats, **through-bolted with a 4-bolt pattern to an exterior wall plate**), and **the 2 bottom-right ends (BR, near + far)** with a **combined corner plate shared with the right walkway** (see below). The container shell carries the lateral rigidity, so no cross-cage is needed; this also frees the near/far Yd footprint and removes the near-wall equipment clash. Costs ~110mm of carriage travel at each end (immaterial to the design). The rails now run the full width **saddle-to-saddle** (Yd 0 → C_WID).

**Right vs left.** The **right** rails (X 4649, TR + BR) are **permanently bolted** into place. The **left** rails (X 150, TL + BL) drop into their saddles on **knurled thumb screws** so they lift out for transport.

**Combined corner plate (rev 12).** At each bottom-right corner (near and far) the film plane and the right walkway terminate at the same wall station, so a single **10mm combined corner plate** seats both — the **bottom film rail (BR) on a 150mm seat** and the **right walkway long beam on a 70mm seat** — bolted through the wall with a shared interior/exterior plate pair. This **replaces the 2 BR wall-seat saddles**. The plate is single-sourced in the overview generator (`fp_combined_corner_plate`) and reused by both the film-plane and walkway 3D models; the film-plane model skips the BR saddle and draws the combined plate instead. See [Walkway Report](walkway-report.md) §4.3.

**Transport mode.** The film-plane left rail is **continuous** (no demountable center segment): the light lock (Ø900 housing + drum) is offset (`DRUM_CX = −400`) and exits through the hinge-panel punch-out bay rather than rotating within the rail span. For *transport*, the panel + drum **SWING ~56°** about the pivot and the drum cage transitions X=150, so the **two left film rails (TL + BL) and the muslin screen are struck first** — the left rails lift out of their thumb-screw saddles and re-seat to the film datum on re-deployment — see [Hinged Panel Report](hinged-panel-report.md) §5.4 for the conversion sequence.



*Quantities: 6 standalone saddles + 2 combined corner plates = 4 rail corners × near + far wall. The 2 bottom-right (BR) ends use the combined corner plate (carried in the walkway BoM), leaving 6 standalone saddles here. Each saddle: 1 back-plate + 1 exterior plate + 1 seat + 1 gusset (8mm plate) + 4× M12 through-bolts. Hold-downs: thumb screws on the 4 left saddles (8), hex fixing bolts on the 2 TR saddles (4). Subtotal ~$440 (6 saddles) — roughly cost-neutral with the retired brace cage (the combined plates shift ~$130 of plate/bolt cost into the walkway BoM).*

### Muslin Clamp System

See [Muslin Clamp System — Mechanism Design](film-clamp-mechanism-report.md) for the full clamp specification, parts list, and engineering drawing.

### Optional Electric Actuation

| Item | Spec | Qty | Source A | Source B | Est. Unit |
|------|------|-----|---------|---------|-----------|
| PA-14 linear actuator | 12V, 20" stroke, 150 lb | **4** | Progressive Automations | Amazon | $185 |
| 12V 30A power supply | Enclosed | 1 | Mouser | Digi-Key | $55 |
| DPDT momentary rocker | Panel-mount, 20A | **4** | Mouser | Grainger | $8 |

**Estimated materials total (manual actuation, incl. wall-seat saddles + Option A cross-slides): ~<!-- BEGIN costing:film-total -->$3,454<!-- END costing:film-total -->** (rev 12: the 2 BR saddles move to the walkway's combined corner plates)
*Excludes fasteners, fabrication labor, and electric actuation option.*
*Option A net change vs the earlier four-corner design: added 8 cross-slide rails +$200, 8 cross-slide carriages +$96, 4 intermediate plates +$60 (= +$356); removed the folding-backing piano hinge –$56 → net +$300. The single rigid ACM backing replaces the hinged two-panel system.*

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
