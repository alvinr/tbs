<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Mini-TBS — Proof-of-Concept Pinhole Camera

## Cyanotype Prints from a Moving Box

A small-scale proof of concept for the [Big Shoebox Project](../index.md). This camera uses the same optics, chemistry, and process as TBS-001 — scaled down to a standard moving box. It produces real cyanotype prints on cotton muslin, approximately 14 × 16 inches, suitable for inclusion in proposals, exhibitions, and grant applications.

**Purpose:** Validate the pinhole-to-cyanotype workflow before committing to the full container build. Every technical decision below traces to the same peer-reviewed sources used in the TBS-001 design.

![Mini-TBS cross-section and plan](../assets/mini-tbs-sheet1.png)

---

## 1. Box Selection

### Recommended: U-Haul Medium Box

| Parameter | Value |
|-----------|-------|
| Box dimensions | 18 × 18 × 16 inches (457 × 457 × 406 mm) |
| Supplier | U-Haul, Home Depot, Lowe's |
| Cost | ~$4–5 |

**Orientation:** Pinhole on one 18 × 16" face. Film plane on the opposite 18 × 16" face. The 18-inch (457 mm) dimension becomes the focal length.

**Why this box:**

- 457 mm focal length gives a practical f-number and ~10 min exposure in full sun
- 14 × 16" usable print area is large enough to be visually compelling
- Standard item, universally available, inexpensive
- Rigid enough when taped and reinforced

### Alternative: U-Haul Large Box

| Parameter | Value |
|-----------|-------|
| Box dimensions | 24 × 18 × 18 inches (610 × 457 × 457 mm) |
| Focal length | 457 mm (same — use the 18" depth) |
| Film plane | 24 × 18" (610 × 457 mm) |
| Usable area | ~20 × 16" (~2.2 sq ft) |
| Cost | ~$6–8 |

The Large box gives a bigger print but the same f-number (same 18" depth). Use it if you want a more dramatic print for a proposal.

---

## 2. Optical Specification

All derivations use the **Lord Rayleigh formula** for optimal pinhole diameter:

$$d = 1.9 \sqrt{f \lambda}$$

where *f* is focal length in mm and *λ* = 0.00055 mm (550 nm green light).

**Source:** Rayleigh, J.W.S., "On Pin-hole Photography," *Philosophical Magazine*, Ser. 5, Vol. 31, 1891, pp. 87–99. Applied identically to the TBS-001 specification in the [Pinhole Optics Report](../pinhole-optics-report.md).

### Mini-TBS Optical Parameters

| Parameter | Mini-TBS (PoC) | TBS-001 (Container) | Derivation |
|-----------|---------------|---------------------|------------|
| Focal length (f) | 457 mm | 2,362 mm | Box depth / container width |
| Rayleigh optimal d | 0.95 mm | 2.17 mm | 1.9 × √(f × 0.00055) |
| Drill bit used | 1/32" (0.794 mm) | Laser-drilled SS | Closest Home Depot standard |
| Actual pinhole Ø | ~0.80 mm | 2.17 mm | Drill bit through aluminum can |
| f-number | f/575 | f/1088 | f / d |
| Film plane | 406 × 457 mm | 4,499 × 2,388 mm | Box face / container face |
| Usable image area | 356 × 406 mm | 4,499 × 2,388 mm | After mounting margins |
| Angle of view (diag.) | ~53° | ~56° | 2 × arctan(half-diag / f) |

**Pinhole undersizing note:** The 1/32" drill bit produces a hole 16% smaller than the Rayleigh optimal. This means slightly less light throughput (longer exposure by ~10%) but slightly sharper image — the geometric blur circle is smaller while the diffraction blur increases only marginally. At this scale, the trade is favorable. (Renner, E., *Pinhole Photography*, 4th ed., Focal Press, 2009, Ch. 2.)

### Resolution

Using the Rayleigh resolution criterion (see [Pinhole Optics Report](../pinhole-optics-report.md) §7):

$$\text{Resolution} = \frac{d}{2 \times 1.22 \times \lambda \times f}$$

For Mini-TBS: 0.794 / (2 × 1.22 × 0.00055 × 457) ≈ **1.3 lp/mm**

This is sufficient for a contact print viewed at arm's length — cyanotype on muslin does not resolve finer detail than this.

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

### 4.1 Light-Sealing the Box

The box must be completely light-tight. Even a pinprick leak will fog the print.

**Materials:** Black gaffer tape (Polyken 510 or equivalent — not duct tape, which leaves residue and can delaminate).

**Procedure:**

1. Assemble the box per manufacturer instructions. Close and tape all flaps.
2. Seal every external seam with a full strip of black gaffer tape. Pay special attention to:
   - All four flap edges on both open faces
   - Every corner where two panels meet
   - The manufacturer's glued seam (usually one long edge)
3. Cut 2-inch squares of cardboard and tape them over every 3-plane corner junction (where three panels meet). These are the worst light-leak points — a flat tape strip cannot seal a 3D corner.
4. Apply a second layer of tape on all internal seams.
5. **Light-leak test:** Take the sealed box into a completely dark room. Sit with the box for 5 minutes to dark-adapt your eyes. Place a bright flashlight (phone light) inside the box, seal it, and inspect every seam and corner from the outside. Mark any visible light with a marker. Seal those points.

### 4.2 Pinhole Fabrication

**Materials:**
- Aluminum beverage can (empty, clean, dry)
- 400-grit and 600-grit sandpaper
- 1/32" (0.794 mm) drill bit
- Pin vise (hand-held chuck for small drill bits — ~$5 at Home Depot)

**Procedure:**

1. Cut a 3 × 3 inch piece from the flat side wall of an aluminum beverage can using scissors. Avoid the curved top and bottom.
2. Sand both sides with 400-grit sandpaper to remove the printed coating and any burrs. The aluminum should be clean bare metal, approximately 0.1 mm thick.
3. Place the aluminum on a firm surface (hardwood or a book — not glass, which can chip the bit).
4. Insert the 1/32" drill bit into the pin vise. Center the bit on the aluminum piece.
5. **Drill slowly** — rotate the pin vise by hand with light pressure. Do not use a power drill (the bit will wander and the hole will be oversized or oblong).
6. After the bit breaks through, flip the aluminum and lightly sand the exit side with 600-grit to remove the raised burr collar.
7. Hold the finished pinhole up to a light source and inspect with a magnifying glass or loupe. The hole should be:
   - Round (not oblong)
   - Clean-edged (no ragged burrs)
   - Centered on the plate
8. **Drill 3–4 test pinholes.** Select the cleanest, most circular one.

**Mounting:**

1. Cut a 2 × 2 inch square hole in the center of the pinhole face of the box (the 18 × 16" face you've designated).
2. Center the aluminum pinhole plate over this hole on the inside of the box.
3. Tape all four edges with black gaffer tape. The tape must be light-tight — overlap the aluminum by at least 1/2 inch on all sides.
4. The pinhole is now the only light path into the box.

### 4.3 Shutter

A simple flap shutter:

1. Cut a 4 × 4 inch piece of stiff black cardboard (or 4 layers of black gaffer tape on regular cardboard).
2. Tape the top edge of the flap to the box exterior, directly above the pinhole. The flap hangs down covering the pinhole.
3. **To expose:** Lift the flap and tape it open above the pinhole. Start the timer.
4. **To end exposure:** Untape the flap, let it drop. Smooth it flat over the pinhole.

### 4.4 Arm Sleeves (Changing-Bag Access)

For coating the muslin inside the sealed box in darkness.

**Materials:**
- Black opaque fabric (cotton knit from a black t-shirt works well)
- Heavy-duty rubber bands or elastic hair ties
- Black gaffer tape

**Procedure:**

1. Choose one of the 18 × 18" side faces (not the pinhole face, not the film plane face).
2. Cut two armholes, each approximately 4 inches in diameter. Space them 10 inches apart horizontally, centered vertically on the face.
3. Cut two sleeve tubes from black fabric: each approximately 18 inches long and 6 inches in diameter (circumference ~19 inches). A t-shirt sleeve, cut at the shoulder seam, gives roughly the right dimensions.
4. Insert one end of each sleeve tube into an armhole from the inside. Fold the fabric edge over the cardboard edge and tape it down with black gaffer tape, overlapping at least 2 inches on all sides.
5. The outer end of each sleeve remains open. When in use, insert your arms and cinch rubber bands around your forearms to seal the sleeve openings.
6. **Test:** With the box sealed, insert your arms and verify you can reach the opposite face (the film plane) with both hands. You need to be able to stretch muslin, apply sensitizer with a brush, and mount binder clips by feel.

**Alternative approach (simpler for first prints):**

Coat the muslin outside the box on a table in a darkened room (red LED safelight only), allow it to tack-dry, then load the coated muslin into the box in darkness. This eliminates the need for arm sleeves entirely. The arm sleeves become useful only for repeat sessions where you want to coat and load without leaving the darkened room.

### 4.5 Film Plane

**Materials:**
- Foam-core board or stiff cardboard (cut to 16 × 18" — snug fit inside the box)
- Binder clips (1-inch, ~20 per print)
- Pre-washed unbleached cotton muslin

**Procedure:**

1. Cut the backing board to fit snugly against the face opposite the pinhole. It should press flat against the box wall with no gaps.
2. Pre-cut muslin pieces to approximately 18 × 20 inches (2 inches of excess on each edge for folding over the backing board).
3. After coating and tack-drying the muslin (see §5), stretch it over the backing board. Fold the excess over all four edges.
4. Clip with binder clips every 2 inches along all four edges. The muslin must be taut and wrinkle-free — wrinkles produce soft zones in the print.
5. Insert the loaded backing board into the box, muslin face toward the pinhole. Press it firmly against the back wall.

---

## 5. Chemistry

### Ware New Cyanotype Formula

The same formula used for TBS-001. Source: Ware, M., *Cyanotype: The History, Science and Art of Photographic Printing in Prussian Blue*, Science Museum, 1999. Full details in the [Chemistry Shopping List](../chemistry-shopping-list.md).

### Stock Solutions

**Part A — Ammonium Iron(III) Oxalate:**

| Ingredient | Quantity |
|------------|----------|
| Ammonium iron(III) oxalate | 30 g |
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

**Materials:** Foam brush (2-inch), mixing cup, coated muslin pieces pre-cut to 18 × 20 inches.

**Procedure (from [Operating Manual](../operating-manual.md) §2.3):**

1. Lay a pre-washed, pre-cut muslin piece flat on a clean table.
2. Pour ~4 ml of mixed sensitizer into a shallow tray or cup.
3. Load the foam brush evenly (not dripping).
4. **First pass:** Brush horizontally, left to right, with 50% overlap between strokes. Work from top to bottom.
5. **Second pass:** Brush vertically, top to bottom, with 50% overlap. This cross-direction pass ensures even coverage.
6. **Edges:** Check all four edges — foam brushes tend to undercoat the last inch. Touch up by hand.
7. **Tack-dry:** Allow 15–20 minutes in the darkened room with gentle air movement (not direct fan). The sensitizer changes from wet-glossy to matte tack-dry.
8. **Test:** Lightly touch a corner with a gloved fingertip. If no transfer — the muslin is ready to load.

**Humidity notes (from [Operating Manual](../operating-manual.md) §1.5):**

| Humidity | Action |
|----------|--------|
| Below 30% | Lightly mist muslin with plain water 5 min before coating |
| 30–65% | Coat normally |
| Above 70% | Delay — risk of fogging under safelight |

---

## 7. Exposure Procedure

1. Mount the tack-dry coated muslin on the backing board (see §4.5).
2. Load the backing board into the sealed box, muslin facing the pinhole.
3. Ensure the shutter flap is closed.
4. Carry the box outside. Position it on a stable surface (table, chair, ground) with the pinhole facing the subject.
5. **Subject selection:** For the first test, choose a high-contrast scene — a sunlit building against blue sky, or a bright landscape with distinct shapes. Avoid scenes dominated by shadow.
6. Open the shutter. Start the timer.
7. **Do not move the box** during exposure. Do not stand in front of the pinhole or allow shadows to cross it.
8. At the calculated exposure time, close the shutter.
9. Bring the box inside or into shade.

---

## 8. Development

**Cyanotype develops in plain cold water.** No fixer, no stop bath, no chemicals beyond water.

**Procedure (from [Operating Manual](../operating-manual.md) §4.2):**

1. Remove the muslin from the backing board. (After exposure, cyanotype is no longer light-sensitive — a few seconds of indoor light during removal is acceptable.)
2. **Wash 1:** Submerge in cold water for 5 minutes. Agitate gently. The water will turn yellow-green as unreacted sensitizer clears. This is normal and non-toxic.
3. **Wash 2:** Transfer to fresh cold water for 5 minutes.
4. **Wash 3:** Final rinse in fresh cold water for 5 minutes.
5. **Visual check after wash 2:** The image should be clearly visible as deep Prussian blue shadows against white/off-white highlights.
   - If faint: underexposed → increase time by 50% on next print
   - If dark with no highlight detail: overexposed → reduce time by 30%
   - If pale when wet: may darken significantly on drying — wait before judging

### Drying

1. Hang the print flat (horizontal preferred — vertical hanging can cause drip marks and uneven drying).
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
| Muslin wrinkled in print | Slack mounting | Pull muslin tighter on backing board. Clip every 2" minimum. |
| Pinhole hole is oblong | Drill bit wandered or too much pressure | Drill a new pinhole on fresh aluminum. Use lighter pressure, slower rotation. |

---

## 10. Comparison to TBS-001

| Parameter | Mini-TBS (PoC) | TBS-001 (Container) |
|-----------|---------------|---------------------|
| Camera body | Cardboard moving box | 20ft ISO shipping container |
| Focal length | 457 mm | 2,362 mm |
| Pinhole | 0.80 mm (drill bit) | 2.17 mm (laser-drilled SS) |
| f-number | f/575 | f/1088 |
| Image area | ~1.0 sq ft | ~116 sq ft |
| Exposure (full sun) | ~10 min | ~30–45 min |
| Tilt/swing movements | None (fixed) | ±42° tilt, ±25.7° swing |
| Process | Ware New Cyanotype | Ware New Cyanotype |
| Chemistry | Identical formula | Identical formula |
| Development | 3× cold water wash | 3× cold water wash |
| Per-print cost | ~$2–3 | ~$38 |
| Build cost | ~$69–120 | ~$15,500 |

The optical physics, chemistry, and process are identical. The Mini-TBS validates all three at a scale that fits on a kitchen table.

---

## 11. Bill of Materials

See the [Mini-TBS Shopping List](mini-tbs-shopping-list.md) for the complete itemized list with suppliers, prices, and quantities for 20 prints.

**Budget summary:**

| Category | Low | High |
|----------|-----|------|
| Box + construction | $18 | $24 |
| Pinhole materials | $8 | $15 |
| Chemistry | $25 | $45 |
| Substrate (muslin) | $3 | $6 |
| Tools | $8 | $14 |
| Processing (wash basins) | $3 | $9 |
| Safelight | $4 | $7 |
| **Total** | **$69** | **$120** |

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
