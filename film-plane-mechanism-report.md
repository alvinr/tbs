<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Film Plane — Mechanism Design

## 1. Purpose

The configuration the photosensitive film plane is flush against one of the 20ft long-side walls of the container. This report describes a **view-camera-style moveable film plane** — a mechanism with **four corner carriages** (TL, TR, BL, BR) driven in **coordinated pairs**, carrying a **fixed-size rigid** plane that changes only its angle — allowing tilt, swing, and limited combined movements comparable to a large-format view camera's rear standard.

**System context — container floor plan:**
The floor plan below shows the film plane rail positions in the context of the complete TBS-001 interior, including left end zone (light trap), processing tray and perimeter walkway in the optical zone, and right end zone (4× IBCs in 2×2 stack, pump manifold on the Corridor Plumbing Panel and the filter skid on the Pinhole Wall Plumbing Panel).

![TBS-001 Container Floor Plan — All Systems](assets/container-floorplan.png)

<!-- brochure:skip -->
**Interactive 3D model** — the fixed-size rigid film plane on its four slide-and-clamp corner carriages, shown against a ghost of the perimeter walkway and the IBC frame. Drag to orbit, scroll to zoom; the **Movement** and **whole-plane** scenes let you click a corner — or the whole frame — to cycle it through a tilt or swing, and the per-corner detail scenes show each 304 U-channel depth rail, acetal skate, Z/X cross-slide, and the single U-joint.

<div class="sketchfab-embed-wrapper">
  <div style="position:relative;width:100%;padding-bottom:56.25%;">
    <iframe title="TBS-001 Articulated Film Plane Model" frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" execution-while-out-of-viewport execution-while-not-rendered web-share src="https://sketchfab.com/models/572b4aaa2d394de1b8852160d7cdcfc3/embed" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"></iframe>
  </div>
  <p style="font-size: 13px; font-weight: normal; margin: 5px; color: #4A4A4A;"><a href="https://sketchfab.com/3d-models/tbs-001-articulated-film-plane-model-572b4aaa2d394de1b8852160d7cdcfc3?utm_medium=embed&utm_campaign=share-popup&utm_content=572b4aaa2d394de1b8852160d7cdcfc3" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">TBS-001 Articulated Film Plane Model</a> by <a href="https://sketchfab.com/alvin91403?utm_medium=embed&utm_campaign=share-popup&utm_content=572b4aaa2d394de1b8852160d7cdcfc3" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">alvin91403</a> on <a href="https://sketchfab.com?utm_medium=embed&utm_campaign=share-popup&utm_content=572b4aaa2d394de1b8852160d7cdcfc3" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">Sketchfab</a></p>
</div>
<!-- brochure:endskip -->

---

## 2. Container Reference Geometry

| Dimension | Value | Notes |
|-----------|-------|-------|
| Interior length | <!-- BEGIN fact:container_interior_length_mm -->5,893<!-- END fact:container_interior_length_mm -->mm (19 ft 4 in) | Film plane spans this direction |
| Interior width | <!-- BEGIN fact:focal_length_mm -->2,362<!-- END fact:focal_length_mm -->mm (7 ft 9 in) | **Optical axis = focal length** |
| Interior height | <!-- BEGIN fact:film_plane_height_mm -->2,094<!-- END fact:film_plane_height_mm -->mm (6 ft 10 in) | Film plane height |
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

**Maximum tilt angle** (single-axis): **<!-- BEGIN fact:film_plane_max_tilt -->40<!-- END fact:film_plane_max_tilt -->°** — set by the cross-slide Z travel (~250mm); the depth rails alone would allow ~65°.

**Maximum swing angle** (single-axis): **<!-- BEGIN fact:film_plane_max_swing -->28<!-- END fact:film_plane_max_swing -->°** — rail-depth limited ≈ 28.7°.

Swing is the binding limit because the plane is <!-- BEGIN fact:film_plane_width_mm -->4,499<!-- END fact:film_plane_width_mm -->mm wide — the same depth travel over a wider span sweeps the corner further along the rail. Combined tilt+swing is further limited — see §5.

Because the plane is a **fixed-size rigid rectangle**, its physical height stays **2,094mm at every angle** — it does not grow. Corner **cross-slides** absorb the rigid-rotation arc travel instead, so a single rigid backing panel suffices.

---

## 4. Mechanism Design

> **Note:** The drawings (Sheets 1–8) and distortion renders show **axis tilt/swing** — the rigid plane rotates about its center and **foreshortens** (it never grows), illustrated about the mid-rail position (the film back-focuses anywhere along the rail; flat-at-far-wall is the max-focal-length extreme). The interactive 3D model `models/film-plane-mechanism.skp` also reflects this.

### Four-Corner Frame

Each corner of the film plane frame rides on its own carriage assembly (driven in coordinated pairs, not independently — a rigid plane cannot warp):

![Sheet 7 — Four-Corner Frame Front Elevation](assets/film-plane-sheet7.png)

- **4 depth rails** — 3×1½" (76×38mm) **304 stainless U-channel** (McMaster 1262T21), one at each corner, running wall-to-wall along the <!-- BEGIN fact:focal_length_mm -->2,362<!-- END fact:focal_length_mm -->mm optical axis. An acetal skate rides inside each; sliding it sets that corner's **depth** (focus / back-focus). The **right** rails (X=4,649mm) are permanently flanged to their wall seats; the **left** rails (X=150mm) are transport drop-ins that lift out.
- **4 acetal skates** — a 4-wheel skate per corner: **Ø32 acetal load rollers** gravity-seated on the channel's bottom flange plus **Ø20 keeper rollers** captive under the top flange, all on **Ø10 316 axles**, carrying the corner's carriage plate.
- **12 cam clamps** — three per corner. Each corner is slid by hand into position, then a **cam-lever rail brake** locks the skate to the U-channel — there are no leadscrews. The lock holds for the exposure and for transport.
- **8 corner cross-slides** — a **Z (tilt)** slide plus an **X (swing)** slide at each corner, each a **316 stainless flat bar (¼"×1½")** captured on **UHMW self-lube pads** with an adjustable brass-tip **gib**. The Z slide (~250mm) and X slide (~260mm) absorb the in-plane arc travel that a **rigid** rotation forces on each corner (≈245mm in Z at max tilt, ≈263mm in X at max swing), so the film plane stays a **fixed-size flat rectangle** instead of stretching; the gib drag holds the gravity-loaded vertical axis while the clamp is set.
- **Film plane frame** — welded 2"×2"×3/16" anodized-6061 aluminum angle, kept as an **expendable part** (in the splash-not-immersed cyanotype zone anodized 6061 corrodes slowly — inspect annually, replace on pitting; chosen over 304 SS to save ~32 kg and ~$1.5k, with the ACM backing carrying the flatness), a **FIXED-SIZE rigid rectangle, <!-- BEGIN fact:film_plane_width_mm -->4,499<!-- END fact:film_plane_width_mm -->mm × <!-- BEGIN fact:film_plane_height_mm -->2,094<!-- END fact:film_plane_height_mm -->mm** (rail span × film-plane height). Each corner connects to its cross-slide stack through a **single universal joint** (Ruland USKC12-6-6-SS, 303 stainless, twist-locked, nitrile-booted): the U-joint supplies the two angular degrees of freedom (tilt + swing) while the cross-slides supply the translation. The joint bolts to the frame through a **304 stainless corner plate** (detailed below) and to the X-slide carriage on 3/8" 304 stub shafts held in McMaster 4040N12 supports (see Sheet 3). Together they let the rigid plane tilt and swing without the frame ever changing size. The following diagrams show the range of movements of the film plane.

![Sheet 1 — Plan view](assets/film-plane-sheet1.png)

Viewed from above, the full range of swing movement can be seen above. Since both side rails allow the same range of movements, it allows the maximum range of creative control.

![Sheet 2 — Elevations](assets/film-plane-sheet2.png)

View from the side, the full range of tilt movement can be seen above. Since both the top and bottom rails allow the same range of movements, it allows the maximum range of creative control.

### Mechanism Components
The master diagram for the components can be see in the diagram below. The following section discuss the details.

![Sheet 3 — Hardware detail](assets/film-plane-sheet3.png)

### Why a U-Joint + Cross-Slides

The film plane is a **fixed-size rigid rectangle**; tilt and swing are a true **rigid-body rotation** of that rectangle. A rigid rotation moves each corner along an arc — partly along its depth rail (handled by the acetal skate) and partly *across* it (in X and Z). The **2-axis cross-slide** absorbs that across-rail travel, and the **single universal joint** (Ruland USKC12-6-6-SS, 45° per axis) takes up the angular change so nothing binds. This pairing is what lets a rigid plane tilt and swing **without stretching**, and keeps the plane a single flat rectangle at every angle.

Each corner connects to that mechanism through a **304 stainless corner plate**: the 6061 angle frame bolts to the plate, the plate carries the U-joint, and the U-joint's other yoke mounts on the **X (swing) slide** — so the corner is *carried by* the slide **through** the U-joint, never bolted to it directly. The plate is steel (not the expendable aluminum) because the U-joint funnels the whole corner load into a few bolts, and stainless for a galvanic/wet-zone match to the 303 SS U-joint. Sheet 9 details this connection square-on and in section.

![Sheet 9 — Frame + ACM ↔ U-joint ↔ X-slide connection detail](assets/film-plane-sheet9.png)

### Positioning

Each corner is set by hand: roll the acetal skate along its U-channel to the target depth, slide the Z and X cross-slides to take up the rotation arc, then throw the **cam clamp** to lock the skate to the rail. The gib drag holds the vertical (Z) axis while the clamp is set, and the U-joint's twist-lock holds the angle.

**Named movement modes:**
- **Pure tilt**: slide the two top corners (TL + TR) together to one depth; slide the two bottom corners (BL + BR) together to another.
- **Pure swing**: slide TL and BL together; slide TR and BR together.
- **Back focus**: slide all four corners by the same amount.
- **Compound (limited)**: set all four to a coordinated set of depths — the rigid plane stays flat (no twist).

All four corners lock independently on their own cam clamps, so a set position holds through the exposure and through transport.

### Fixed-Size Plane — No Variable Geometry

Because the plane is a **fixed-size rigid rectangle**, its physical dimensions never change: the along-plane height stays **2,094mm at every tilt angle**. The arc travel that the rotation forces on each corner is taken up entirely by the **cross-slides** (≈245mm Z at max tilt, ≈263mm X at max swing), not by the frame.

**Single rigid backing panel:** the backing is **one flat ACM (aluminum composite) sheet, <!-- BEGIN fact:film_plane_width_mm -->4,499<!-- END fact:film_plane_width_mm -->mm × <!-- BEGIN fact:film_plane_height_mm -->2,094<!-- END fact:film_plane_height_mm -->mm**, bonded to the rear of the angle frame — the panel simply rotates with the rigid plane.

### Light Sealing

A tilted or swung plane opens gaps at its edges where the frame no longer sits flush against the wall. Two measures close them, both on the maintenance schedule (§8):

- **Primary seal** — a 1"×½" black EPDM foam strip bonded to all four frame edges, compressing to seal at the low angles.
- **Secondary seal** — Rosco Duvetyne blackout curtains hung from the frame perimeter and weighted, draping to seal at the larger tilt/swing angles where the foam no longer reaches.

The EPDM foam tape and Duvetyne curtains are itemized in the §7 parts list.

---

## 5. Tilt / Swing Configurations

The plane stays flat at all times, so it is always a single tilt **or** swing (or a limited combination). Corner depths below are about the **mid-rail center (1,181mm)** — add the focus offset to reposition the whole plane. Film height is **constant**.

| Config | Name | TL | TR | BL | BR | Tilt | Swing | Film Height |
|--------|------|----|----|----|----|------|-------|-------------|
| C0 | Flat | 1181 | 1181 | 1181 | 1181 | 0° | 0° | 2,094mm |
| C1 | Mild tilt | 977 | 977 | 1385 | 1385 | 11.0° | 0° | 2,094mm |
| C2 | Strong tilt | 622 | 622 | 1740 | 1740 | 31.5° | 0° | 2,094mm |
| C3 | Max tilt | 494 | 494 | 1868 | 1868 | 40.0° | 0° | 2,094mm |
| C4 | Mild swing | 923 | 1439 | 923 | 1439 | 0° | 6.6° | 2,094mm |
| C5 | Strong swing | 412 | 1950 | 412 | 1950 | 0° | 20.0° | 2,094mm |
| C6 | Max swing | 125 | 2237 | 125 | 2237 | 0° | 28.0° | 2,094mm |

*Depths measured from the pinhole wall about the mid-rail center. Tilt = asin(2·Δd_top-bottom / FP_H) about the plane center (FP_H=2094); swing = asin(2·Δd_left-right / FP_W) (FP_W=4499). Rail positions: left X=150mm, right X=4,649mm.*

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
| [304 U-channel depth rail 3×1½" (76×38mm)](https://www.mcmaster.com/1262T21/) (1262T21) | 4 depth rails, one per corner, running wall-to-wall (~2,362mm, Yd0→C_WID) along the optical axis — an acetal skate rides inside each to set that corner's depth/focus. $362.12/6ft firm. NOTE: a 2,362mm rail exceeds a 6ft (1,829mm) length, and the skate can't cross a splice — so buy 8ft lengths (4 rails) or confirm the continuous-length SKU/price at order. Qty 6× 6ft here is the conservative $-estimate. | 6 ea | McMaster-Carr | $2,172 |
| [Ruland USKC12-6-6-SS U-joint (keyway+clamp, 303 SS)](https://www.ruland.com/us12-6-6-ss.html) (USKC12-6-6-SS) | One per corner — supplies the tilt+swing angular DOF (45°/axis); 3/8" bores, 303 stainless (wet zone), twist-locked. $276 ea firm — INTERIM part; a cheaper joint is under research (see TODO). The U-joint alone is $276×4 = $1,104. | 4 ea | Ruland | $1,104 |
| [Ruland UBOOT12/19-NI-KIT nitrile boot](https://www.ruland.com/uboot12-19-ni-kit.html) (UBOOT12/19-NI-KIT) | Nitrile boot over each U-joint — keeps cyanotype splash out of the joint. | 4 ea | Ruland | $122 |
| [McMaster 4040N12 304 shaft support](https://www.mcmaster.com/4040N12/) (4040N12) | Two-piece 304 clamp securing the U-joint INPUT stub to the X (swing) slide, one per corner. $58 ea firm. | 4 ea | McMaster-Carr | $232 |
| [3/8" 304/304L SS rod — U-joint stub shafts (1× 3 ft)](https://www.mcmaster.com/89535K87/) (89535K87) | Input + output stub shafts into the U-joint (2/corner ×4 = 8 short stubs, ~60–80mm each ≈ 560–640mm + kerf). ONE 3 ft (914mm) length ($13.25 firm) yields all 8 with margin. Plain 304 rod — the USKC clamp grips it (keyway optional). | 1 lot | McMaster-Carr | $13 |
| Acetal 4-wheel skate — Ø32 load + Ø20 keeper rollers, Ø10 316 axles + carriage plate | One skate per corner rides inside the U-channel: Ø32 acetal load rollers gravity-seated on the bottom flange + Ø20 keeper rollers captive under the top flange, all on Ø10 316 axles carrying the carriage plate (same acetal-on-316 skate as the spray bar). 10mm 316 axle rod $33–50/ft. Firm the wheel/fab price at order (est.). | 4 set | McMaster-Carr / Local fab | $220–$360 |
| 316 flat-bar Z (tilt) + X (swing) cross-slides + UHMW pad + gib | One 2-axis cross-slide stack per corner — 316 flat-bar Z and X slides on UHMW pads with an adjustable gib, absorbing the across-rail rotation travel. UHMW $23–93/sheet; 316 flat bar cut to length. Firm at order (est.). | 4 set | Metal Supermarkets / McMaster-Carr | $180–$380 |
| Cam-lever rail brake (skate lock) | Three per corner — a cam-lever brake locks the acetal skate to the U-channel after the corner is slid to depth (no leadscrews); holds for the exposure + transport. Firm SKU/price at order (est.). | 12 ea | McMaster-Carr / Amazon | $96–$180 |
| Corner plate 304 SS (U-joint mount) | ¼" 304 SS plate, ~6"×8" L-bracket — the frame-corner ↔ U-joint mount. Carries the concentrated U-joint corner load in STEEL, not aluminum; stainless for the cyanotype splash zone + galvanic match to the 303 SS U-joint. NOT expendable (the perimeter angle stays expendable 6061). | 4 ea | Metal Supermarkets / Online Metals | $152–$208 |
| Aluminum angle 2"×2"×3/16" (6061, anodized) | 6061-T6 angle, clear-anodized, 8 ft lengths — the film-plane PERIMETER FRAME, an EXPENDABLE part. In the splash (not immersed) cyanotype zone anodized 6061 corrodes slowly; treated as inspect-annually / replace-on-pitting to save ~32 kg + ~$1.5k vs 304 SS (the ACM backing does the flatness work, so Al's lower stiffness is acceptable). | 10 ea | Metal Supermarkets / Online Metals | $220 |
| Dibond ACM panel 4mm | 4 ft × 8 ft sheets — single rigid backing, <!-- BEGIN fact:film_plane_width_mm -->4,499<!-- END fact:film_plane_width_mm -->×<!-- BEGIN fact:film_plane_height_mm -->2,094<!-- END fact:film_plane_height_mm -->mm | 6 sheet | Grimco / Signwarehouse | $510 |
| [Black EPDM foam tape 1"×½"](https://www.mcmaster.com/8694K88/) (8694K88) | 25 ft rolls — 2 (50 ft) cover the ~43 ft film-plane perimeter primary seal | 2 roll | McMaster-Carr / Grainger | $45 |
| Rosco Duvetyne | 60" wide, 10 yd | 1 ea | B&H Photo / Rosco direct | $95 |
| 6-mil black poly sheeting | 10 ft × 100 ft | 1 roll | Home Depot / Uline | $66–$70 |
| 2" black Gorilla Tape | 35 yd rolls | 6 roll | Home Depot / Amazon | $54–$78 |
| Mild steel plate 8mm (laser/plasma cut + welded) | ICP-11: back-plate + exterior plate + seat + gusset per saddle; ~21 kg over 6 saddles | 6 ea | Metal Supermarkets / Online Metals | $318 |
| [M12×65 hex through-bolt, Grade 8.8 zinc, partial-thread](https://www.mcmaster.com/91280A728/) (91280A728) | ICP-12: wall-sandwich through-bolt (4/saddle ×6 + 4 spare), sized for the 30mm-corrugation grip (~50mm), partial thread. $15.95/pack of 10 → 3 packs for 28. Pad with 1–2 M12 flat washers if the actual container corrugation is <30mm. | 28 ea | McMaster-Carr | $45 |
| [M12 hex nut, plain](https://www.mcmaster.com/90591A181/) (90591A181) | Plain hex nut — M12×65 wall-sandwich bolts (+ split lock washer). $12.78/pack of 50. | 28 ea | McMaster-Carr | $7 |
| [M12 flat washer, zinc](https://www.mcmaster.com/91166a290/) (91166A290) | Flat washers, M12×65 wall-sandwich bolts — 2 functional + 2 shim/bolt (shims pad the grip if corrugation <30mm). $9.71/pack of 100. | 112 ea | McMaster-Carr | $11 |
| [M12 split lock washer, zinc](https://www.mcmaster.com/91202A246/) (91202A246) | Split lock washer under each nut — M12×65 wall-sandwich bolts (plain nut + split = locked). $11.97/pack of 100. | 28 ea | McMaster-Carr | $3 |
| M8×25mm knurled thumbscrew DIN 464 | ICP-13: left-rail drop-in hold-down; 2/saddle ×4 left + 4 spare | 12 ea | Amazon / Maedler | $36 |
| M8 hex bolt, SS — ~M8×30 (pending 1262T21 web thickness) | ICP-14: right depth-rail end flange → wall seat hold-down (does NOT cross the wall — the M12 ICP-12 does the sandwich). Grip = 1262T21 channel base web + 10mm seat ≈ 13mm → ~M8×30, pending the 1262T21 web thickness (McMaster PDF). 2/saddle ×2 TR + spare. | 8 ea | McMaster-Carr / Amazon | $15 |
| [M8×1.25 hex nut, plain SS](https://www.mcmaster.com/90591A161/) (90591A161) | Plain hex nut — M8 right-rail fixing. Pitch M8×1.25 (coarse, baseline — confirm vs SKU PDF, must match the bolt). $7.53/pack of 100. | 8 ea | McMaster-Carr | $1 |
| **Film total** | | | | **$5,717–$6,225** |
<!-- END parts:film -->

*The corner-mechanism hardware (U-channel depth rails, acetal skates, Z/X cross-slides, and the
per-corner U-joint) and the wall-seat saddles (ICP-11–14) are itemized in the table above; the
saddle design is described below.*

### Wall-Seat Saddles

Each of the **8 rail ends** anchors to the container — **6 of them** with a standalone **IBC-style wall-seat saddle** (a back-plate + horizontal seat the rail end rests on + triangular gusset, dims reused from the IBC frame wall seats, **through-bolted with a 4-bolt pattern to an exterior wall plate**), and **the 2 bottom-right ends (BR, near + far)** with a **combined corner plate shared with the right walkway** (see below). The container shell carries the lateral rigidity, so no cross-cage is needed; this also frees the near/far Yd footprint and removes the near-wall equipment clash. Costs ~110mm of carriage travel at each end (immaterial to the design). The rails now run the full width **saddle-to-saddle** (Yd 0 → C_WID).

**Right vs left.** The **right** rails (X 4649, TR + BR) are **permanently bolted** into place. The **left** rails (X 150, TL + BL) drop into their saddles on **knurled thumb screws** so they lift out for transport.

**Combined corner plate (rev 12).** At each bottom-right corner (near and far) the film plane and the right walkway terminate at the same wall station, so a single **10mm combined corner plate** seats both — the **bottom film rail (BR) on a 150mm seat** and the **right walkway long beam on a 70mm seat** — bolted through the wall with a shared interior/exterior plate pair. This **replaces the 2 BR wall-seat saddles**. The plate is single-sourced in the overview generator (`fp_combined_corner_plate`) and reused by both the film-plane and walkway 3D models; the film-plane model skips the BR saddle and draws the combined plate instead. See [Walkway Report](walkway-report.md) §4.3.

**Transport mode.** The film-plane left rail is **continuous** (no demountable center segment): the light lock (Ø900 housing + drum) is offset (`DRUM_CX = −400`) and exits through the hinge-panel punch-out bay rather than rotating within the rail span. For *transport*, the panel + drum **SWING ~56°** about the pivot and the drum cage transitions X=150, so the **two left film rails (TL + BL) and the muslin screen are struck first** — the left rails lift out of their thumb-screw saddles and re-seat to the film datum on re-deployment — see [Hinged Panel Report](hinged-panel-report.md) §5.4 for the conversion sequence.



*Quantities: 6 standalone saddles + 2 combined corner plates = 4 rail corners × near + far wall. The 2 bottom-right (BR) ends use the combined corner plate (carried in the walkway BoM), leaving 6 standalone saddles here. Each saddle: 1 back-plate + 1 exterior plate + 1 seat + 1 gusset (8mm plate) + 4× M12 through-bolts. Hold-downs: thumb screws on the 4 left saddles (8), hex fixing bolts on the 2 TR saddles (4). Subtotal ~$440 (6 saddles) — roughly cost-neutral with the retired brace cage (the combined plates shift ~$130 of plate/bolt cost into the walkway BoM).*

### Muslin Clamp System

See [Muslin Clamp System — Mechanism Design](film-clamp-mechanism-report.md) for the full clamp specification, parts list, and engineering drawing.

**Estimated materials total (incl. wall-seat saddles): ~<!-- BEGIN costing:film-total -->$6,103<!-- END costing:film-total -->** (the 2 bottom-right saddles move to the walkway's combined corner plates)
*Excludes fasteners and fabrication labor.*

### Local SoCal Metal Sourcing

- **Metal Supermarkets** — Anaheim (714-630-8463), Van Nuys (818-988-1301), San Diego (619-280-7600). Cut-to-length 304 U-channel, 316 flat bar, and aluminum angle on-site, no minimum order.
- **Grimco** — City of Industry, CA. Sign-industry ACM panel supplier, large sheet stock.
- **McMaster-Carr** — U-channel (1262T21), 304 shaft supports, acetal rollers, 316 axle rod, and cam clamps; ships nationally.
- **Ruland** — universal joints (USKC12-6-6-SS) and nitrile boot kits; ships nationally.
- **Grainger** — branches throughout LA, Orange County, San Diego. Same-day local pickup.

---

## 8. Maintenance

| Interval | Task |
|----------|------|
| Before each session | Inspect muslin clamp engagement — see [Clamp System](film-clamp-mechanism-report.md) |
| Before each session | Verify all four cam clamps are locked after repositioning |
| Before each session | Check EPDM foam edge seal for tears or compression set |
| Monthly | Wipe the U-channel rails clean of grit — the acetal skate and UHMW pads run **dry** (no lubricant) |
| Monthly | Inspect the acetal rollers and UHMW slide pads for wear or embedded grit |
| Every 6 months | Check each U-joint for play and its nitrile boot for tears — replace the boot if split |
| Every 6 months | Inspect Duvetyne blackout curtains for light leaks (pinholes, fraying) |
| Annually | Inspect the anodized-6061 frame angle and corner L-brackets for pitting; replace on pitting (expendable) |
| Annually | Verify rail mounting bolts for torque at all four rail positions |
| Before transport | Lock all four corners at matching depth; set all four cam clamps |

---

## 9. Source References

1. [McMaster-Carr 304 Stainless U-Channel](https://www.mcmaster.com/stainless-steel-u-channels) — 3×1½" (76×38mm) 304 stainless U-channel (1262T21), the depth rail the acetal skate runs in.
2. [Ruland USKC12-6-6-SS Universal Joint](https://www.ruland.com/us12-6-6-ss.html) — single universal joint, 3/8" bores, 303 stainless, 45° per axis — the per-corner tilt+swing joint (nitrile boot UBOOT12/19-NI-KIT).
3. [Tilt-Swing Front Board Report](tilt-swing-board-report.md) — Front board mechanism for combined distortion analysis.
4. [Equipment Layout Report](equipment-layout-report.md) — Rail positions and shadow-free zone verification.
