<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# TBS-002 — Mini-TBS Proof-of-Concept Pinhole Camera

## Cyanotype Prints from a Moving Box

A small-scale proof of concept for the [Big Shoebox Project](../index.md). This camera uses the same optics, chemistry, and process as TBS-001 — scaled down to two standard moving boxes. It produces real cyanotype prints on watercolor paper, approximately 14 × 16 inches, suitable for inclusion in proposals, exhibitions, and grant applications.

**Purpose:** Validate the pinhole-to-cyanotype workflow before committing to the full container build. Every technical decision below traces to the same peer-reviewed sources used in the TBS-001 design.

**Design:** Two U-Haul Medium boxes joined end-to-end — a sealed camera box (pinhole + light cone) and a light-sealed prep box (standard photo tray + coating workspace). A backing board (film plane) is permanently hinged at the near rim of a Paterson 12×16" developing tray (the rim closest to the camera box). The prep box end face serves dual duty: it has armholes with attached arm sleeves for sealed operator access, and it is an extraction flap (hinged at the top) that opens in daylight after exposure for print removal. No darkroom required.

![Mini-TBS engineering drawing — two-box design with hinged flap, plan view, and pinhole face](../assets/mini-tbs-sheet1.png)

---

## 1. Box Selection

### Recommended: U-Haul Medium Box

| Parameter | Value |
|-----------|-------|
| Box dimensions | 18 × 18 × 16 inches (457 × 457 × 406mm) |
| Supplier | U-Haul, Home Depot, Lowe's |
| Cost | ~$4–5 |

**Quantity needed:** 2 (one camera box, one prep box).

**Orientation:** Pinhole on one 18 × 16" face. Film plane on the opposite 18 × 16" face. The 18-inch (457mm) dimension becomes the focal length. The second box attaches at the film plane face to serve as the prep/coating area.

**Why this box:**

- 457mm focal length gives a practical f-number and ~10 min exposure in full sun
- 14 × 16" usable print area is large enough to be visually compelling
- Standard item, universally available, inexpensive
- Rigid enough when taped and reinforced
- Two identical boxes mate perfectly at the shared face

### Alternative: U-Haul Large Box

| Parameter | Value |
|-----------|-------|
| Box dimensions | 24 × 18 × 18 inches (610 × 457 × 457mm) |
| Focal length | 457mm (same — use the 18" depth) |
| Film plane | 24 × 18" (610 × 457mm) |
| Usable area | ~20 × 16" (~2.2 sq ft) |
| Cost | ~$6–8 |

The Large box gives a bigger print but the same f-number (same 18" depth). Use it if you want a more dramatic print for a proposal.

---

## 2. Optical Specification

All derivations use the **Lord Rayleigh formula** for optimal pinhole diameter:

$$d = 1.9 \sqrt{f \lambda}$$

where *f* is focal length in mm and *λ* = 0.00055mm (550 nm green light).

**Source:** Rayleigh, J.W.S., "On Pin-hole Photography," *Philosophical Magazine*, Ser. 5, Vol. 31, 1891, pp. 87–99. Applied identically to the TBS-001 specification in the [Pinhole Optics Report](../pinhole-optics-report.md).

### Mini-TBS Optical Parameters

| Parameter | TBS-002 (Mini-TBS) | TBS-001 (Container) | Derivation |
|-----------|---------------|---------------------|------------|
| Focal length (f) | 457mm | 2362mm | Box depth / container width |
| Rayleigh optimal d | 0.95mm | 2.17mm | 1.9 × √(f × 0.00055) |
| Drill bit used | 1/32" (0.794mm) | Laser-drilled SS | Closest Home Depot standard |
| Actual pinhole Ø | ~0.80mm | 2.17mm | Drill bit through aluminum can |
| f-number | f/575 | f/1088 | f / d |
| Film plane | 406 × 457mm | <!-- BEGIN fact:film_plane_width_mm -->4499<!-- END fact:film_plane_width_mm --> × <!-- BEGIN fact:film_plane_height_mm -->2388<!-- END fact:film_plane_height_mm -->mm | Box face / container face |
| Usable image area | 356 × 406mm | <!-- BEGIN fact:film_plane_width_mm -->4499<!-- END fact:film_plane_width_mm --> × <!-- BEGIN fact:film_plane_height_mm -->2388<!-- END fact:film_plane_height_mm -->mm | After mounting margins |
| Angle of view (diag.) | ~53° | ~56° | 2 × arctan(half-diag / f) |

**Pinhole undersizing note:** The 1/32" drill bit produces a hole 16% smaller than the Rayleigh optimal. This means slightly less light throughput (longer exposure by ~10%) but slightly sharper image — the geometric blur circle is smaller while the diffraction blur increases only marginally. At this scale, the trade is favorable. (Renner, E., *Pinhole Photography*, 4th ed., Focal Press, 2009, Ch. 2.)

### Resolution

Using the Rayleigh resolution criterion (see [Pinhole Optics Report](../pinhole-optics-report.md) §7):

$$\text{Resolution} = \frac{d}{2 \times 1.22 \times \lambda \times f}$$

For Mini-TBS: 0.794 / (2 × 1.22 × 0.00055 × 457) ≈ **1.3 lp/mm**

This is sufficient for a contact print viewed at arm's length — cyanotype on watercolor paper does not resolve finer detail than this.

---

## 3. Exposure Calculation

### Baseline

The TBS-001 baseline exposure is **30–45 minutes at f/1088** on Ware New Cyanotype (see [Operating Manual](../operating-manual.md) §3.1). Exposure scales as the square of the f-number ratio:

$$t_{\text{PoC}} = t_{\text{TBS}} \times \left(\frac{f_{\text{PoC}}}{f_{\text{TBS}}}\right)^2$$

Using 37.5 min as the midpoint baseline:

$$t_{\text{PoC}} = 37.5 \times \left(\frac{575}{1088}\right)^2 = 37.5 \times 0.279 = \textbf{10.5 minutes}$$

### Reciprocity Failure

**No correction required.** Cyanotype is an iron-based process and does not exhibit classical Schwarzschild reciprocity failure. The response is linear at long exposures. (See [Pinhole Optics Report](../pinhole-optics-report.md) §6, Table: "Cyanotype | Minimal | Iron-based process — does not exhibit classical Schwarzschild failure.")

This is one of the key advantages of cyanotype for pinhole photography. A silver gelatin paper at f/575 would require Schwarzschild correction (p ≈ 0.85), extending the exposure by ~2×.

### Exposure Adjustment Table

Same multipliers as TBS-001 ([Operating Manual](../operating-manual.md) §3.1):

| Condition | Multiplier | Mini-TBS exposure |
|-----------|-----------|-------------------|
| Full direct sun (10:00–14:00, summer) | ×1.0 | ~10 min |
| Thin haze / milky sky | ×1.5 | ~16 min |
| Broken cloud (50% coverage) | ×2.0 | ~21 min |
| Heavy overcast | ×4.0 | ~42 min |
| Early morning / late afternoon | ×2.0 | ~21 min |
| Winter sun at mid-latitude | ×1.5 | ~16 min |

For compound conditions, multiply factors: thin haze + early morning = ×3.0 → ~32 min.

**Recommendation for first session:** Choose a clear-sky day between 10:00 and 14:00. Make three exposures: one at calculated time (10 min), one at +50% (15 min), one at -25% (8 min). This brackets the exposure and compensates for any local UV variation.

---

## 4. Construction

### 4.1 Two-Box Assembly

The Mini-TBS uses two identical U-Haul Medium boxes joined end-to-end:

- **Camera box** (left in diagram): Sealed, light-tight. Contains the pinhole and light cone. The backing board forms the film plane when upright.
- **Prep box** (right in diagram): Light-sealed workspace for chemistry, coating, and drying. Contains the Paterson 12×16" developing tray. The end face is an extraction flap (hinged at top) for removing exposed prints in daylight.

The shared wall between the boxes is removed. A **permanently hinged backing board** serves as the film plane. It is hinged at the near rim of the photo tray (camera side) with duct tape, so it swings up into the camera box opposite the pinhole. Arm sleeves on the prep box end face give the operator sealed access for coating and mounting paper.

**Procedure:**

1. Assemble both boxes per manufacturer instructions. Close and tape all flaps on both boxes.
2. Stand the boxes end-to-end so that two 18 × 16" faces are adjacent.
3. Remove the adjacent face from both boxes (cut away the cardboard panels). This creates one long enclosure (36" deep × 18" wide × 16" high).
4. Tape the two boxes together at the junction using duct tape on all four edges — floor, ceiling, and both side walls. The taped joint must be rigid.

### 4.2 Light-Sealing the Camera Box

Only the camera box needs to be light-tight. The prep box remains open (it is used under safelight conditions only).

**Materials:** Black duct tape, 2" × 30 yd (one roll covers all sealing, hinging, and light-proofing for the entire build).

**Procedure:**

1. Seal every external seam on the camera box with a full strip of black duct tape. Pay special attention to:
   - All four flap edges on the pinhole face
   - Every corner where two panels meet
   - The manufacturer's glued seam (usually one long edge)
2. Cut 2-inch squares of cardboard and tape them over every 3-plane corner junction. These are the worst light-leak points.
3. Apply a second layer of tape on all internal seams.
4. **Light-leak test:** In a dark room, place a bright flashlight inside the sealed camera box (with the hinged flap upright). Inspect every seam from outside. Mark and seal any visible light.

### 4.3 Photo Tray and Hinged Backing Board

A standard Paterson 12×16" developing tray (PTP326) sits inside the prep box, against the camera-box wall. The backing board is permanently hinged at the tray's near rim (the rim closest to the camera box) with duct tape. When the board folds up, it swings into the camera box to serve as the film plane opposite the pinhole. The board has two armholes (4" diameter, 9" apart) cut into it, with arm sleeves attached on the prep side. When upright, the board serves as the film plane; when folded down, it extends past the tray into the remaining prep space for mounting paper.

**Materials:**
- Paterson 12×16" developing tray (PTP326 or equivalent — available from B&H Photo, Adorama, or Freestyle Photo)
- Foam-core board, 20 × 30" sheet (cut to ~17.5 × 15.5")
- Duct tape (same roll used for all sealing and hinging)
- Binder clips (1-inch, ~12 per print)

**Procedure:**

1. Place the Paterson tray inside the prep box, against the camera-box wall. Orient it with the 12" dimension (305mm) along the depth axis and the 16" dimension (406mm) across the width. The tray should sit flat on the prep box floor.
2. Cut a foam-core board panel: approximately 17.5 × 13 inches (443 × 333mm). The board spans from the tray rim height to the camera box ceiling interior — it does not extend to the floor because the hinge is at the tray rim (69mm above the floor).
3. **Hinge:** Attach the bottom edge of the backing board to the near rim of the tray (the rim closest to the camera box) using a full-width strip of duct tape, applied to both sides. The tape must wrap continuously around the rim — this is a permanent working hinge that will be folded repeatedly.
4. **Folded-down position (prep):** The board lies flat, extending from the near rim of the tray over the tray and into the remaining prep space. The board clears the tray because the hinge is at the rim height. This is the position for mounting coated paper.
5. **Exposure position:** Fold the board up from the tray hinge so it swings into the camera box. The board stands upright inside the camera box with the paper facing the pinhole. Use a binder clip or duct tape tab at the top edge to hold it upright.
6. **Test the hinge:** Fold the board up and down 10–15 times. It should move freely without binding. The duct tape hinge should not crack or separate.

### 4.4 Pinhole Fabrication

**Materials:**
- Aluminum beverage can (empty, clean, dry)
- 400-grit and 600-grit sandpaper
- 1/32" (0.794mm) drill bit
- Pin vise (hand-held chuck for small drill bits — ~$5 at Home Depot)

**Procedure:**

1. Cut a 3 × 3 inch piece from the flat side wall of an aluminum beverage can using scissors. Avoid the curved top and bottom.
2. Sand both sides with 400-grit sandpaper to remove the printed coating and any burrs. The aluminum should be clean bare metal, approximately 0.1mm thick.
3. Place the aluminum on a firm surface (hardwood or a book — not glass, which can chip the bit).
4. Insert the 1/32" drill bit into the pin vise. Center the bit on the aluminum piece.
5. **Drill slowly** — rotate the pin vise by hand with light pressure. Do not use a power drill (the bit will wander and the hole will be oversized or oblong).
6. After the bit breaks through, flip the aluminum and lightly sand the exit side with 600-grit to remove the raised burr collar.
7. Hold the finished pinhole up to a light source and inspect with a magnifying glass or loupe. The hole should be round, clean-edged, and centered.
8. **Drill 3–4 test pinholes.** Select the cleanest, most circular one.

**Mounting:**

1. Cut a 2 × 2 inch square hole in the center of the pinhole face (the 18 × 16" face).
2. Center the aluminum pinhole plate over this hole on the inside of the box.
3. Tape all four edges with black duct tape. The tape must be light-tight — overlap the aluminum by at least 1/2 inch on all sides.

### 4.5 Shutter

A simple flap shutter:

1. Cut a 4 × 4 inch piece of stiff black cardboard (or 4 layers of black duct tape on regular cardboard).
2. Tape the top edge of the flap to the box exterior, directly above the pinhole. The flap hangs down covering the pinhole.
3. **To expose:** Lift the flap and tape it open above the pinhole. Start the timer.
4. **To end exposure:** Untape the flap, let it drop. Smooth it flat over the pinhole.

### 4.6 Arm Sleeves (on Prep Box End Face)

The armholes are on the prep box end face — the operator's face. They are centered on the face, spaced 9 inches (230mm) apart. This gives sealed arm access for coating paper in the tray, checking tack-dry, and mounting paper onto the backing board — all without opening the box or breaking the light seal. This is what makes the Mini-TBS usable in the field without a darkroom.

**Materials:**
- Black opaque fabric (cotton knit from a black t-shirt works well)
- Heavy-duty rubber bands or elastic hair ties
- Black duct tape

**Procedure** (see armhole detail in the engineering drawing):

1. Cut two armholes in the prep box end face, each approximately 4 inches (102mm) in diameter. Space them 9 inches (230mm) apart center-to-center, centered on the face. Use a compass to trace the circle, then cut with a box cutter. Sand or trim any rough edges — the fabric will fold over this edge.
2. Cut two sleeve tubes from black fabric: each approximately 18 inches (450mm) long and 6 inches in diameter (circumference ~19 inches). A t-shirt sleeve, cut at the shoulder seam, gives roughly the right dimensions.
3. **Attach the sleeve to the wall (see detail cross-section):**
   - Insert the sleeve through the armhole from the outside.
   - Pull approximately 2 inches (50mm) of fabric through the hole and fold it back onto the inside surface of the cardboard wall. The fabric wraps over the cut edge of the hole, creating a smooth, sealed transition.
   - Tape the fold-back down with a full ring of 2-inch black duct tape on the inside surface, covering the folded fabric completely. Press firmly — this is the primary light seal.
   - Apply a second ring of duct tape on the outside surface where the sleeve exits the wall, overlapping the fabric and cardboard by at least 1 inch (25mm). This prevents the sleeve from pulling away under tension.
4. **Wrist seal:** When in use, insert your arms through the sleeves and cinch heavy-duty rubber bands or elastic hair ties around your forearms to seal the openings. The cinch point should be snug enough to block light but not restrict circulation.
5. **Test:** Insert your arms through the sleeves and verify you can reach the tray, the backing board, and manipulate binder clips with both hands. In a darkened room, shine a flashlight at the armhole from outside — check for any light leaks around the tape seal rings. Re-tape any gaps.

### 4.8 Extraction Flap

The prep box end face (the face farthest from the pinhole) is an extraction flap, hinged at the top with duct tape. After exposure, the cyanotype print is no longer UV-sensitive and can be handled in full daylight. The extraction flap opens to allow the operator to remove the exposed print, unfold it from the board, and wash it externally — no need to disassemble the camera or break the light seal on the camera box.

**Procedure:**

1. Score the prep box end face along the top edge, leaving 1 inch of cardboard attached at the top as a natural hinge line.
2. Reinforce the hinge with a full-width strip of duct tape on both the inside and outside, spanning the hinge line.
3. Seal the flap edges (bottom and both sides) with duct tape strips that overlap the flap and the box walls by at least 1 inch. These strips act as light-seal gaskets when the flap is closed.
4. **To open:** Peel the bottom and side tape strips, swing the flap up. Reach in to remove the exposed print.
5. **To close:** Swing the flap down and re-seal the edges with fresh duct tape strips.

**Note:** The extraction flap only needs to be light-tight during coating, tack-drying, and mounting (safelight operations). After exposure, the print is daylight-safe, so the flap can remain open during print removal and washing.

### 4.7 Substrate: Watercolor Paper

**Why watercolor paper instead of muslin?**

The TBS-001 full-scale camera uses cotton muslin because of the scale — no paper is manufactured 4.5 meters wide. For the 14 × 16" PoC prints, watercolor paper is the superior substrate:

| | Watercolor paper | Cotton muslin |
|---|---|---|
| Pre-treatment | None | Pre-wash twice, line dry, iron flat |
| Lies flat | Yes — naturally rigid | Requires stretching and clipping |
| Coating evenness | Excellent — consistent absorption | Variable — depends on tension and sizing |
| Failure modes | Few | Wrinkles, uneven sizing, slack mounting |
| Availability | Any art supply store | Fabric store, requires cutting |
| Traditional substrate? | Yes — the original cyanotype medium | Used for large-format only |

**Recommended paper:** Arches Aquarelle hot-press, 140 lb (300 gsm), 100% cotton. Available in 22 × 30" sheets at Blick Art Materials, Joann, or Amazon. Cut each sheet to 16 × 18" (one print per sheet with trim to spare).

**Alternative:** Fabriano Artistico hot-press, 140 lb (300 gsm). Also 100% cotton.

**Requirements:**
- **Weight:** 140 lb / 300 gsm minimum. Lighter paper curls severely when wet.
- **Fiber:** 100% cotton (rag paper). Wood-pulp paper degrades in the iron chemistry.
- **Surface:** Hot-press (smooth). Cold-press texture interferes with fine detail at this resolution.

**Mounting the paper:**

1. Cut a sheet to fit the backing board with 1-inch overlap on all sides (approximately 17.5 × 19.5 inches).
2. After coating and tack-drying (see §6), fold the overlap over the board edges.
3. Clip with binder clips every 3 inches along all four edges. The paper will lie flat naturally — much simpler than stretching muslin.
4. Fold the backing board up into the camera position, paper face toward the pinhole.

---

## 5. Chemistry

### Ware New Cyanotype Formula

The same formula used for TBS-001. Source: Ware, M., *Cyanotype: The History, Science and Art of Photographic Printing in Prussian Blue*, Science Museum, 1999. Full details in the [Chemistry Shopping List](../chemistry-shopping-list.md).

### Stock Solutions

**Part A — Ammonium Iron(III) Oxalate:**

| Ingredient | Quantity |
|------------|----------|
| Ammonium iron(III) oxalate (ferric ammonium oxalate) | 30 g |
| Warm water (50–60°C) | 75 ml |

Dissolve AmFe in warm water (not boiling) with continuous stirring, 3–5 minutes, until clear pale yellow-green solution. Cool to room temperature. Store in a dark bottle. Shelf life: 6–8 weeks.

**Part B — Potassium Ferricyanide:**

| Ingredient | Quantity |
|------------|----------|
| Potassium ferricyanide | 8 g |
| Room-temperature water | 100 ml |

Dissolve with stirring until bright orange-red. Store in a dark bottle, away from Part A. Shelf life: 6–8 weeks.

**Note:** Ammonium dichromate (contrast enhancer, ~1 g per batch) is used in the full TBS formula but is **optional for the PoC.** It is a Category 1A carcinogen and costs $12 for the minimum order. The prints will work without it — contrast will be slightly lower but adequate for proof-of-concept purposes.

### Working Sensitizer

Mix equal volumes of Part A and Part B **immediately before use.** The mixed solution is UV-sensitive — work under red LED safelight only.

**Per print:** ~4 ml working sensitizer (2 ml Part A + 2 ml Part B), double-coated.

**For 20 prints + 25% overage:** 100 ml total working sensitizer (50 ml Part A + 50 ml Part B).

Working life: 4–6 hours after mixing. Discard unused mixed solution.

---

## 6. Coating Procedure

**Environment:** Darkened room. Red LED safelight only. No daylight, no white or blue LED light.

**Materials:** Foam brush (2-inch), mixing cup, watercolor paper pre-cut to 17.5 × 19.5 inches.

**Using the photo tray:** The paper is coated in the Paterson 12×16" developing tray inside the prep box. The paper (16 × 18") is slightly larger than the tray interior (12 × 16") — the edges overhang the tray rim during brush coating. This is standard practice for cyanotype; the tray catches drips and provides a stable work surface. Access the tray through the arm sleeves on the prep box end face (see §4.6).

**Procedure (from [Operating Manual](../operating-manual.md) §2.3):**

1. Place the pre-cut watercolor paper in the tray. The paper overhangs the 12" edges slightly — this is fine for brush coating.
2. Pour ~4 ml of mixed sensitizer into a shallow cup (not directly into the tray).
3. Load the foam brush evenly (not dripping).
4. **First pass:** Brush horizontally, left to right, with 50% overlap between strokes. Work from top to bottom.
5. **Second pass:** Brush vertically, top to bottom, with 50% overlap. This cross-direction pass ensures even coverage.
6. **Edges:** Check all four edges — foam brushes tend to undercoat the last inch. Touch up by hand.
7. **Tack-dry:** Allow 15–20 minutes in the prep box (light-sealed). Watercolor paper dries faster than fabric — check after 10 minutes. The sensitizer changes from wet-glossy to matte tack-dry.
8. **Mount:** Through the arm sleeves on the end face, remove the tack-dried paper from the tray. Fold the backing board down from the upright position (it lies flat over the tray into the prep space). Clip the paper to the board with binder clips. Fold the board back up into the camera box. Paper faces the pinhole.

**Humidity notes (from [Operating Manual](../operating-manual.md) §1.5):**

| Humidity | Action |
|----------|--------|
| Below 30% | Lightly mist paper with plain water 5 min before coating |
| 30–65% | Coat normally |
| Above 70% | Delay — risk of fogging under safelight |

---

## 7. Exposure Procedure

1. After mounting the coated paper on the backing board (see §6, step 8), verify the board is upright in the exposure position with the paper facing the pinhole. Secure the top edge with a binder clip or duct tape tab.
2. Ensure the extraction flap on the prep box end face is closed and sealed. The prep box should be light-tight.
3. Ensure the shutter flap is closed.
4. Carry the entire assembly outside. Position it on a stable surface (table, ground) with the pinhole facing the subject.
5. **Subject selection:** For the first test, choose a high-contrast scene — a sunlit building against blue sky, or a bright landscape with distinct shapes. Avoid scenes dominated by shadow.
6. Open the shutter. Start the timer.
7. **Do not move the assembly** during exposure. Do not stand in front of the pinhole or allow shadows to cross it.
8. At the calculated exposure time, close the shutter.
9. Bring the assembly inside or into shade.

---

## 8. Development

**Cyanotype develops in plain cold water.** No fixer, no stop bath, no chemicals beyond water.

**Procedure (from [Operating Manual](../operating-manual.md) §4.2):**

1. Open the extraction flap on the prep box end face (see §4.8). After exposure, cyanotype is no longer light-sensitive — full daylight during removal is safe. Fold the backing board down from the upright position, unclip the paper from the board, and remove the print through the extraction flap.
2. **Wash 1:** Submerge in cold water in a photo tray for 5 minutes. Agitate gently. The water will turn yellow-green as unreacted sensitizer clears. This is normal and non-toxic.
3. **Wash 2:** Transfer to fresh cold water for 5 minutes.
4. **Wash 3:** Final rinse in fresh cold water for 5 minutes.
5. **Visual check after wash 2:** The image should be clearly visible as deep Prussian blue shadows against white/off-white highlights.
   - If faint: underexposed → increase time by 50% on next print
   - If dark with no highlight detail: overexposed → reduce time by 30%
   - If pale when wet: may darken significantly on drying — wait before judging

### Drying

1. Lay the print flat on a clean surface (horizontal — watercolor paper stays flat naturally). Alternatively, hang with clips from one edge.
2. Drying time: 20–60 minutes depending on temperature and airflow.
3. **The final blue color appears approximately 30 minutes after the surface feels dry.** The Prussian blue pigment continues to oxidize and deepen in air. Do not judge the final density until the print has dried completely.

---

## 9. Troubleshooting

| Problem | Likely cause | Fix |
|---------|-------------|-----|
| Entire print is pale/white | Massive underexposure or sensitizer degraded | Double the exposure time. Check sensitizer age (>6 hours after mixing = discard). |
| Print is fogged (blue overall, no contrast) | Light leak in box | Re-test all seams in a dark room with a flashlight inside. Seal leaks. |
| Streaky or uneven coating | Insufficient brush overlap or over-dry brush | Use more sensitizer per stroke. Ensure 50% overlap on both passes. |
| Image is sharp in center, soft at edges | Normal for pinhole — expected | No fix needed. Pinhole illumination falls off at edges (cos⁴ law). |
| Image is very dark, no whites | Overexposure | Reduce exposure by 30%. Wash longer (5th wash cycle may help clear highlights). |
| Paper curled during wash | Paper too thin | Use 140 lb (300 gsm) minimum. Let the paper relax flat during final wash. |
| Light leak through prep box | Extraction flap or arm sleeves not sealed during exposure | Ensure extraction flap edges are fully taped and arm sleeves on end face are cinched. |
| Pinhole hole is oblong | Drill bit wandered or too much pressure | Drill a new pinhole on fresh aluminum. Use lighter pressure, slower rotation. |

---

## 10. Comparison to TBS-001

| Parameter | TBS-002 (Mini-TBS) | TBS-001 (Container) |
|-----------|---------------|---------------------|
| Camera body | Two moving boxes + photo tray | 20ft ISO shipping container |
| Focal length | 457mm | 2362mm |
| Pinhole | 0.80mm (drill bit) | 2.17mm (laser-drilled SS) |
| f-number | f/575 | f/1088 |
| Image area | ~1.0 sq ft | ~116 sq ft |
| Exposure (full sun) | ~10 min | ~30–45 min |
| Tilt/swing movements | None (fixed) | ±42° tilt, ±25.7° swing |
| Process | Ware New Cyanotype | Ware New Cyanotype |
| Chemistry | Identical formula | Identical formula |
| Development | 3× cold water wash | 3× cold water wash |
| Per-print cost | ~$2–3 | ~$38 |
| Build cost | ~$94–148 | ~$15,500 |

The optical physics, chemistry, and process are identical. The Mini-TBS validates all three at a scale that fits on a kitchen table.

---

## 11. Bill of Materials

See the [Mini-TBS Shopping List](mini-tbs-shopping-list.md) for the complete itemized list with suppliers, prices, and quantities for 20 prints.

**Budget summary:**

| Category | Low | High |
|----------|-----|------|
| Boxes + construction (×2) | $11 | $16 |
| Pinhole materials | $8 | $15 |
| Chemistry | $25 | $45 |
| Substrate (watercolor paper) | $10 | $18 |
| Tools + consumables | $8 | $14 |
| Photo trays (Paterson 12×16", ×3) | $28 | $33 |
| Safelight + light-seal | $4 | $7 |
| **Total** | **$94** | **$148** |

---

## 12. References

All sources cited here are the same peer-reviewed references used throughout the TBS-001 documentation:

1. Rayleigh, J.W.S., "On Pin-hole Photography," *Philosophical Magazine*, Ser. 5, Vol. 31, 1891, pp. 87–99.
2. Ware, M., *Cyanotype: The History, Science and Art of Photographic Printing in Prussian Blue*, Science Museum, 1999. ISBN: 0901805831.
3. Renner, E., *Pinhole Photography*, 4th ed., Focal Press, 2009.
4. Born, M. & Wolf, E., *Principles of Optics*, 7th ed., Cambridge UP, 1999, §8.6.
5. Schwarzschild, K., "On the Deviation from the Reciprocity Law in Photography," *The Astrophysical Journal*, Vol. 11, 1900, pp. 89–91.
6. Stroebel, L., Compton, J., Current, I., Zakia, R., *Basic Photographic Materials and Processes*, 3rd ed., Focal Press, 2009.
7. Getty Conservation Institute, *Atlas of Analytical Signatures of Photographic Processes — Cyanotype*, 2013.
