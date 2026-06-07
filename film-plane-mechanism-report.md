<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Film Plane — Mechanism Design

## 1. Purpose

The configuration the photosensitive film plane is flush against one of the 20ft long-side walls of the container. This report describes a **view-camera-style moveable film plane** — a mechanism with **four independently actuated corners** (TL, TR, BL, BR) carrying a **fixed-size rigid** plane (Option A), allowing tilt, swing, and limited compound movements comparable to a large-format view camera's rear standard.

**System context — container floor plan:**
The floor plan below shows the film plane rail positions (at Y=2262mm, X=150–4649mm) in the context of the complete TBS-001 interior, including left end zone (light trap), processing tray and perimeter walkway in the optical zone, and right end zone (4× IBCs in 2×2 stack, pump manifold and filter skid on equipment panel).

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
| Interior length | 5893mm (19 ft 4 in) | Film plane spans this direction |
| Interior width | 2362mm (7 ft 9 in) | **Optical axis = focal length** |
| Interior height | 2388mm (7 ft 10 in) | Film plane height |
| Pinhole position | Center of one 20ft long-side wall | |
| Nominal film plane | Opposite 20ft long-side wall | flush to wall |
| Structural ribs | Every 457mm (18 in) along length | Rail mounting points |

---

## 3. Movement Axes

The four-corner mechanism supports all view-camera movements. Corners are labeled TL (top-left), TR (top-right), BL (bottom-left), BR (bottom-right) — where left/right refers to the rail span direction and top/bottom to the 7 ft 10 in height direction.

| Axis | Corners Controlled | Max Travel | Effect |
|------|--------------------|-----------|--------|
| **Tilt (top)** | TL + TR together | 100–2262mm | Perspective convergence, keystone |
| **Tilt (bottom)** | BL + BR together | 100–2262mm | Perspective convergence, keystone |
| **Swing (left)** | TL + BL together | 100–2262mm | Left-right perspective skew |
| **Swing (right)** | TR + BR together | 100–2262mm | Left-right perspective skew |
| **Compound (limited)** | Tilt + swing together | 100–2262mm | Combined tilt+swing — limited range; plane stays **flat** (no twist) |
| **Back focus** | All 4 together | 100–2262mm | Uniform magnification change |
| **Rise / Fall** | All 4 together, offset vertically | ±200mm | Horizon shift |
| **Shift** | All 4 together, offset horizontally | ±300mm | Left/right perspective offset |

**Maximum tilt angle** (single-axis): **40°** — set by the cross-slide Z travel (~280mm); the depth rails alone would allow ~65°.

**Maximum swing angle** (single-axis): **28°** — rail-depth limited: asin(1081 / (4499/2)) ≈ 28.7°.

(Swing is the binding limit because the plane is 4499mm wide — the same depth travel over a wider span sweeps the corner further along the rail. Combined tilt+swing is further limited — see §5.)

Because the plane is a **fixed-size rigid rectangle**, its physical height stays **2388mm at every angle** — it does not grow. The earlier scheme stretched it ~40% at max tilt and needed a folding two-panel backing; Option A's corner **cross-slides** absorb the rigid-rotation arc travel instead, so a single rigid backing panel suffices.

---

## 4. Mechanism Design

> **Note (Option A, 2026-06-06):** this describes the **fixed-size rigid plane on floating-corner cross-slides**. The drawings (Sheets 1–6) and distortion renders show **axis tilt/swing** — the rigid plane rotates about its centre and **foreshortens** (it never grows), illustrated about the mid-rail position (the film back-focuses anywhere along the rail; flat-at-far-wall is the max-focal-length extreme). The interactive 3D model `models/film-plane.skp` also reflects Option A.

### Four-Corner Frame

Each corner of the film plane frame rides on its own independent carriage assembly:

![Sheet 6 — System Schematic: Four-Corner Frame Front Elevation](assets/film-plane-sheet6.png)

- **4 depth rails** — HiWin HGR20 profile, 2200mm length, mounted at X=150mm (left pair) and X=4649mm (right pair) on ceiling and floor. Rails run along the 2362mm optical axis direction; their carriages set each corner's **depth** (focus / back-focus).
- **8 depth carriages** — HGH20CA flanged blocks, 2 per rail, joined by an L-bracket at each corner.
- **4 leadscrews** — ¾"-6 Acme, 8 ft (2438mm) length, one per corner (TL, TR, BL, BR). Each turns in a bronze Acme nut fixed to the corner bracket and drives that corner's depth.
- **8 corner cross-slides (Option A)** — a **2-axis X-Z floating stage** at each corner (one X slide + one Z slide, ~300mm travel each, on HGR15 rail + block), bolted on top of the depth carriage. These absorb the small in-plane arc travel that a **rigid** rotation forces on each corner (≈280mm in Z at max tilt, ≈263mm in X at max swing), so the film plane stays a **fixed-size flat rectangle** instead of stretching.
- **Film plane frame** — welded 2"×2"×3/16" aluminum angle, a **FIXED-SIZE rigid rectangle, 4499mm × 2388mm** (rail span × container height). Each corner connects to its cross-slide through a **rod-end spherical bearing** (GIR25-DO or equivalent, 25mm bore), which provides the angular freedom; the cross-slide provides the translation. Together they let the rigid plane tilt and swing without the frame ever changing size. The following diagrams show the range of movements of the film plane.

![Sheet 1 — Plan view](assets/film-plane-sheet1.png)

Viewed from above, the full range of swing movement can be seen above. Since both side rails allow the same range of movements, it allows the maximum range of creative control.

![Sheet 2 — Elevations](assets/film-plane-sheet2.png)

View from the side, the full range of tilt movement can be seen above. Since both the top and bottom rails allow the same range of movements, it allows the maximum range of creative control.

### Mechanism Components
The master diagram for the components can be see in the diagram below. The following section discuss the details.

![Sheet 3 — Hardware detail](assets/film-plane-sheet3.png)

### Why Rod-End Spherical Bearings + Cross-Slides (Option A)

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

Because the plane is a **fixed-size rigid rectangle**, its physical dimensions never change: the along-plane height stays **2388mm at every tilt angle** (the earlier stretching scheme grew it ~40% and needed a folding backing — no longer required). The arc travel that the rotation forces on each corner is taken up entirely by the **cross-slides** (≈280mm Z at max tilt, ≈263mm X at max swing), not by the frame.

**Single rigid backing panel:** the backing is now **one flat ACM (aluminum composite) sheet, 4499mm × 2388mm**, bonded to the rear of the angle frame. No piano hinge, no folding two-panel system — the panel simply rotates with the rigid plane.

---

## 5. Tilt / Swing Configurations

The plane stays flat at all times, so it is always a single tilt **or** swing (or a limited combination). Corner depths below are about the **mid-rail centre (1181mm)** — add the focus offset to reposition the whole plane. Film height is **constant**.

| Config | Name | TL | TR | BL | BR | Tilt | Swing | Film Height |
|--------|------|----|----|----|----|------|-------|-------------|
| C0 | Flat | 1181 | 1181 | 1181 | 1181 | 0° | 0° | 2388mm |
| C1 | Mild tilt | 953 | 953 | 1409 | 1409 | 11.0° | 0° | 2388mm |
| C2 | Strong tilt | 557 | 557 | 1805 | 1805 | 31.5° | 0° | 2388mm |
| C3 | Max tilt | 414 | 414 | 1948 | 1948 | 40.0° | 0° | 2388mm |
| C4 | Mild swing | 923 | 1439 | 923 | 1439 | 0° | 6.6° | 2388mm |
| C5 | Strong swing | 412 | 1950 | 412 | 1950 | 0° | 20.0° | 2388mm |
| C6 | Max swing | 125 | 2237 | 125 | 2237 | 0° | 28.0° | 2388mm |

*Depths measured from the pinhole wall about the mid-rail centre. Tilt = asin(2·Δd_top-bottom / FP_H) about the plane centre (FP_H=2388); swing = asin(2·Δd_left-right / FP_W) (FP_W=4499). Rail positions: left X=150mm, right X=4649mm.*

**Combined tilt+swing is limited** — the corners must all stay on the 2200mm depth rails, so the full single-axis maxima cannot be used together. The old C7 "compound" config (simultaneous 42° tilt **and** 28° swing) is **not achievable** with a rigid plane: it required a diagonally **twisted ruled surface** (TL/BR near, TR/BL far), which a fixed-size flat rectangle cannot form, and its corners would sweep ~3.4m of depth — past both end walls.

---

## 6. Optical Distortion Summary

The six achievable flat configurations (C0–C5) on a checker grid (D = 8000mm). Because Option A's plane is always flat, each render is a pure tilt or swing; the former compound *twist* is no longer producible:

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
| **Cross-slide rail HGR15 (Option A)** | 300mm, X-Z stage | **8** | Automation Overstock, Gardena CA | McMaster-Carr | $25 |
| **Cross-slide carriage HGH15CA (Option A)** | Flanged block | **8** | Automation Overstock / Amazon | McMaster-Carr | $12 |
| **Cross-slide intermediate plate (Option A)** | ¼" alum., joins X slide to Z slide | **4** | Metal Supermarkets SoCal | Online Metals | $15 |
| Rod-end spherical bearing | GIR25-DO or equiv., 25mm bore | 8 | McMaster-Carr #60645K73 | Amazon Industrial | $22 |
| Pivot pin SS316 | 1" dia × 8" long | 8 | McMaster-Carr #98173A150 | Fastenal (SoCal branches) | $8 |

*Items in **bold** are new for **Option A** — the 2-axis X-Z cross-slide stage at each corner (8 slides total, ≈300mm travel) that lets the **fixed-size rigid** plane tilt/swing without stretching. The two 5893mm T-slot beams of the original two-beam design remain removed.*

### Film Plane Frame

| Item | Spec | Qty | Source A | Source B | Est. Unit |
|------|------|-----|---------|---------|-----------|
| Aluminum angle 2"×2"×3/16" | 8 ft lengths | 10 | Metal Supermarkets SoCal | Online Metals | $22 |
| Dibond ACM panel 4mm | 4 ft × 8 ft sheets — **single rigid backing**, 4499×2388mm | 6 | Grimco, City of Industry CA | Signwarehouse | $85 |
| Black EPDM foam tape 1"×½" | 50 ft rolls | 3 | McMaster-Carr #8614K84 | Grainger | $28 |
| Rosco Duvetyne | 60" wide, 10 yd | 1 | B&H Photo | Rosco direct | $95 |
| 6-mil black poly sheeting | 10 ft × 100 ft | 1 | Home Depot (local, all SoCal) | Uline | $65 |
| 2" black Gorilla Tape | 35 yd rolls | 6 | Home Depot / Target (local) | Amazon | $12 |

### Demountable Brace Cage

Two rectangular end portals of 50×50×3mm RHS mild steel brace the four-corner rail assembly, giving lateral rigidity while remaining fully demountable for transport. Joints use saddle clamps tightened by M8 thumbscrews.

**Transport mode.** The film-plane left rail is now **continuous** — there is no demountable center segment. Under rev 9 / B2 the light lock (Ø900 housing + drum) is offset (`DRUM_CX = −400`) and exits through the hinge-panel punch-out bay rather than rotating within the rail span, so the rail no longer has to part for drum operation. For *transport*, the hinged panel slides **~880mm** inward and sweeps through X=150, so the **entire film-plane left rail, the brace cage, and the muslin screen are struck first** — see [Hinged Panel Report](hinged-panel-report.md) §5.4 for the conversion sequence.

| Item | ICP # | Spec | Qty | Source A | Source B | Est. Unit |
|------|-------|------|-----|---------|---------|-----------|
| Mild steel RHS square tube | ICP-11 | 50×50×3mm, cut to length — 4 verticals @ 2188mm + 4 cross-beams @ 4499mm = 26.75 m net; order ~30 m to allow saw kerf + saddle-seat cuts | 30 m | [Metal Supermarkets SoCal](https://www.metalsupermarkets.com/product/mild-steel-square-tube-structural-welded/) | [Online Metals — 50mm×3mm sq. tube](https://www.onlinemetals.com/en/buy/carbon-steel/50mm-x-3mm-carbon-steel-square-tube-1018-metric-60-length/pid/22489) | ~$7/ft (~$23/m) est. |
| Saddle clamp for 50mm RHS | ICP-12 | Two-piece bolt-together saddle — seats one tube over another at a joint; compatible with 50×50mm square tube | 16 | [McMaster-Carr — tube clamps](https://www.mcmaster.com/products/steel-tube-clamps/) | [Amazon — square tube clamps](https://www.amazon.com/2-square-tube-clamp/s?k=2%22+square+tube+clamp) | ~$8–12 est. |
| M8 knurled thumbscrew DIN 464 | ICP-13 | M8×20mm, stainless steel 303, high-type knurled head — 2 per saddle clamp joint | 40 | [Amazon — DIN 464 M8 knurled SS](https://www.amazon.com/knurled-thumb-screws-din-464/s?k=knurled+thumb+screws+din+464) | [Maedler North America — DIN 464 M8×20 SS](https://maedlernorthamerica.com/partshop/knurled-thumb-screw-din-464-m8-x-20mm-long-stainless-steel-1-4305-pn-65499225/) | ~$2–5 est. |
| Quick-release ball-lock pin | ICP-14 | Ø10mm, 50mm usable length, stainless steel — retains demountable left-rail segment (2 joints × 2 pins = 4 off, plus 4 spares) | 8 | [McMaster-Carr — ball lock pins](https://www.mcmaster.com/products/ball-lock-pins/) | [Amazon — quick-release ball lock pins](https://www.amazon.com/quick-release-ball-lock-pins/s?k=quick+release+ball+lock+pins) | ~$6–10 est. |

*Quantities basis: 4 verticals (2× portals × 2 sides, 2188mm each, Z 100–2288mm) + 4 cross-beams (2× portals × top+bottom, 4499mm each, X 150–4649mm) = 26.75 m net RHS; 30 m ordered for waste. 16 saddle clamps: 4 corners per portal × 2 clamps per corner × 2 portals = 16. 40 thumbscrews: 2 per clamp × 16 clamps = 32, plus 8 spares. 8 ball-lock pins: 2 joints on demountable left-rail segment × 2 pins + 4 spares.*

### Muslin Clamp System

See [Muslin Clamp System — Mechanism Design](film-clamp-mechanism-report.md) for the full clamp specification, parts list, and engineering drawing.

### Optional Electric Actuation

| Item | Spec | Qty | Source A | Source B | Est. Unit |
|------|------|-----|---------|---------|-----------|
| PA-14 linear actuator | 12V, 20" stroke, 150 lb | **4** | Progressive Automations | Amazon | $185 |
| 12V 30A power supply | Enclosed | 1 | Mouser | Digi-Key | $55 |
| DPDT momentary rocker | Panel-mount, 20A | **4** | Mouser | Grainger | $8 |

**Estimated materials total (manual actuation, incl. brace cage + Option A cross-slides): ~$3,200**  
*Excludes fasteners, fabrication labour, and electric actuation option.*  
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
