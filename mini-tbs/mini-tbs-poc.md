<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Mini-TBS — Proof-of-Concept Pinhole Camera

## Cyanotype Prints from a Moving Box

A small-scale proof of concept for the [Big Shoebox Project](../index.md). This camera uses the same optics, chemistry, and process as TBS-001 — scaled down to two standard moving boxes. It produces real cyanotype prints on watercolor paper, approximately 14 × 16 inches, suitable for inclusion in proposals, exhibitions, and grant applications.

**Purpose:** Validate the pinhole-to-cyanotype workflow before committing to the full container build. Every technical decision below traces to the same peer-reviewed sources used in the TBS-001 design.

**Design:** Two U-Haul Medium boxes joined end-to-end — a sealed camera box (pinhole + light cone) and an open prep box (chemistry + coating workspace). A hinged backing board between them folds down for coating, then folds up to become the film plane for exposure. Armholes on the pinhole face give sealed access to the camera interior.

![Mini-TBS engineering drawing — two-box design with hinged flap, plan view, and pinhole face](../assets/mini-tbs-sheet1.png)

---

## 1. Box Selection

### Recommended: U-Haul Medium Box

| Parameter | Value |
|-----------|-------|
| Box dimensions | 18 × 18 × 16 inches (457 × 457 × 406 mm) |
| Supplier | U-Haul, Home Depot, Lowe's |
| Cost | ~$4–5 |

**Quantity needed:** 2 (one camera box, one prep box).

**Orientation:** Pinhole on one 18 × 16" face. Film plane on the opposite 18 × 16" face. The 18-inch (457 mm) dimension becomes the focal length. The second box attaches at the film plane face to serve as the prep/coating area.

**Why this box:**

- 457 mm focal length gives a practical f-number and ~10 min exposure in full sun
- 14 × 16" usable print area is large enough to be visually compelling
- Standard item, universally available, inexpensive
- Rigid enough when taped and reinforced
- Two identical boxes mate perfectly at the shared face

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

- **Camera box** (left in diagram): Sealed, light-tight. Contains the pinhole, light cone, and film plane. Armholes on the pinhole face for sealed interior access.
- **Prep box** (right in diagram): Open workspace for chemistry, coating, and drying. Contains the chemistry tray.

The shared wall between them is removed and replaced with a **hinged backing board** that serves as the film plane. It folds down into the prep box for coating, then folds up into the camera box for exposure.

**Procedure:**

1. Assemble both boxes per manufacturer instructions. Close and tape all flaps on both boxes.
2. Stand the boxes end-to-end so that two 18 × 16" faces are adjacent.
3. Remove the adjacent face from both boxes (cut away the cardboard panels). This creates one long enclosure (36" deep × 18" wide × 16" high).
4. Tape the two boxes together at the junction using gaffer tape on all four edges — floor, ceiling, and both side walls. The taped joint must be rigid.

### 4.2 Light-Sealing the Camera Box

Only the camera box needs to be light-tight. The prep box remains open (it is used under safelight conditions only).

**Materials:** Black gaffer tape (Polyken 510 or equivalent — not duct tape, which leaves residue and can delaminate).

**Procedure:**

1. Seal every external seam on the camera box with a full strip of black gaffer tape. Pay special attention to:
   - All four flap edges on the pinhole face
   - Every corner where two panels meet
   - The manufacturer's glued seam (usually one long edge)
2. Cut 2-inch squares of cardboard and tape them over every 3-plane corner junction. These are the worst light-leak points.
3. Apply a second layer of tape on all internal seams.
4. **Light-leak test:** In a dark room, place a bright flashlight inside the sealed camera box (with the hinged flap upright). Inspect every seam from outside. Mark and seal any visible light.

### 4.3 Hinged Backing Board (Film Plane / Coating Surface)

The backing board serves dual duty: it is the coating surface when folded down, and the film plane when folded up.

**Materials:**
- Foam-core board, 20 × 30" sheet (cut to fit)
- Duct tape (for the hinge — duct tape is more durable than gaffer tape for a working hinge)
- Binder clips (1-inch, ~12 per print)

**Procedure:**

1. Cut a foam-core board panel to fit snugly inside the box opening at the camera/prep junction: approximately 17.5 × 15.5 inches (allowing clearance for the hinge to fold freely).
2. **Hinge:** Attach the bottom edge of the backing board to the bottom edge of the junction using a full-width strip of duct tape, applied to both sides. The tape must wrap continuously around the bottom edge — this is a working hinge that will be folded repeatedly.
3. **Folded-down position:** The board lies flat on the prep box floor, coating surface facing up. This is the position for coating the substrate with sensitizer.
4. **Upright position:** The board stands vertical at the junction, substrate facing the pinhole. In this position it is the film plane. Use a binder clip or gaffer tape tab at the top edge to hold it upright during exposure.
5. **Test the hinge:** Fold the board up and down 10–15 times. It should move freely without binding. The duct tape hinge should not crack or separate.

### 4.4 Pinhole Fabrication

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
7. Hold the finished pinhole up to a light source and inspect with a magnifying glass or loupe. The hole should be round, clean-edged, and centered.
8. **Drill 3–4 test pinholes.** Select the cleanest, most circular one.

**Mounting:**

1. Cut a 2 × 2 inch square hole in the center of the pinhole face (the 18 × 16" face), between the two armholes.
2. Center the aluminum pinhole plate over this hole on the inside of the box.
3. Tape all four edges with black gaffer tape. The tape must be light-tight — overlap the aluminum by at least 1/2 inch on all sides.

### 4.5 Shutter

A simple flap shutter:

1. Cut a 4 × 4 inch piece of stiff black cardboard (or 4 layers of black gaffer tape on regular cardboard).
2. Tape the top edge of the flap to the box exterior, directly above the pinhole. The flap hangs down covering the pinhole.
3. **To expose:** Lift the flap and tape it open above the pinhole. Start the timer.
4. **To end exposure:** Untape the flap, let it drop. Smooth it flat over the pinhole.

### 4.6 Arm Sleeves (on Pinhole Face)

The armholes are on the pinhole face, flanking the pinhole. This gives sealed arm access to the camera interior for mounting paper onto the backing board, checking tack-dry, or making adjustments — without opening the hinged flap or breaking the light seal.

**Materials:**
- Black opaque fabric (cotton knit from a black t-shirt works well)
- Heavy-duty rubber bands or elastic hair ties
- Black gaffer tape

**Procedure:**

1. Cut two armholes on the pinhole face, each approximately 4 inches (102 mm) in diameter. Space them 9 inches (230 mm) apart center-to-center, centered horizontally on the face, flanking the pinhole. The pinhole and its aluminum plate sit between them.
2. Cut two sleeve tubes from black fabric: each approximately 18 inches long and 6 inches in diameter. A t-shirt sleeve, cut at the shoulder seam, gives roughly the right dimensions.
3. Insert one end of each sleeve into an armhole from the inside. Fold the fabric edge over the cardboard edge and tape it down with black gaffer tape, overlapping at least 2 inches on all sides.
4. When in use, insert your arms and cinch rubber bands around your forearms to seal the sleeve openings.
5. **Test:** With the flap upright and sealed, insert your arms through the sleeves and verify you can reach the backing board with both hands.

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

**Materials:** Foam brush (2-inch), mixing cup, watercolor paper pre-cut to 17.5 × 19.5 inches.

**Using the prep box:** Fold the hinged backing board down into the prep box. Clip the watercolor paper to the board. The board lies flat at floor level — a convenient, stable coating surface.

**Procedure (from [Operating Manual](../operating-manual.md) §2.3):**

1. Clip the pre-cut watercolor paper to the backing board (folded down in the prep box).
2. Pour ~4 ml of mixed sensitizer into a shallow tray or cup.
3. Load the foam brush evenly (not dripping).
4. **First pass:** Brush horizontally, left to right, with 50% overlap between strokes. Work from top to bottom.
5. **Second pass:** Brush vertically, top to bottom, with 50% overlap. This cross-direction pass ensures even coverage.
6. **Edges:** Check all four edges — foam brushes tend to undercoat the last inch. Touch up by hand.
7. **Tack-dry:** Allow 15–20 minutes in the prep box with the room dark. Watercolor paper dries faster than fabric — check after 10 minutes. The sensitizer changes from wet-glossy to matte tack-dry.
8. **Test:** Lightly touch a corner with a gloved fingertip. If no transfer — fold the backing board up into the camera position.

**Humidity notes (from [Operating Manual](../operating-manual.md) §1.5):**

| Humidity | Action |
|----------|--------|
| Below 30% | Lightly mist paper with plain water 5 min before coating |
| 30–65% | Coat normally |
| Above 70% | Delay — risk of fogging under safelight |

---

## 7. Exposure Procedure

1. After the coated paper is tack-dry on the backing board, fold the board up into the camera position (paper facing the pinhole). Secure the top edge with a binder clip or gaffer tape tab.
2. Seal the prep box opening — lay a dark cloth or cardboard panel over the top to block light from reaching the camera through the prep side.
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

1. Fold the backing board down into the prep box. Unclip the paper from the board. (After exposure, cyanotype is no longer light-sensitive — indoor light during removal is acceptable.)
2. **Wash 1:** Submerge in cold water for 5 minutes. Agitate gently. The water will turn yellow-green as unreacted sensitizer clears. This is normal and non-toxic.
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
| Light leak through prep box | Prep box not sealed during exposure | Cover prep box opening with dark cloth or cardboard before exposing. |
| Pinhole hole is oblong | Drill bit wandered or too much pressure | Drill a new pinhole on fresh aluminum. Use lighter pressure, slower rotation. |

---

## 10. Comparison to TBS-001

| Parameter | Mini-TBS (PoC) | TBS-001 (Container) |
|-----------|---------------|---------------------|
| Camera body | Two cardboard moving boxes | 20ft ISO shipping container |
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
| Boxes + construction (×2) | $22 | $28 |
| Pinhole materials | $8 | $15 |
| Chemistry | $25 | $45 |
| Substrate (watercolor paper) | $10 | $18 |
| Tools | $8 | $14 |
| Processing (wash basins) | $3 | $9 |
| Safelight | $4 | $7 |
| **Total** | **$80** | **$136** |

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
