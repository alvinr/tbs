<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Photosensitive Options
## The Big Shoebox Project (TBS-001) — Image Plane Material Selection Guide

**Image plane dimensions (active):** <!-- BEGIN fact:film_plane_width_mm -->4,499<!-- END fact:film_plane_width_mm --> × <!-- BEGIN fact:film_plane_height_mm -->2,094<!-- END fact:film_plane_height_mm -->mm (~14′ 9″ × 7′ 0″)
**Container interior:** <!-- BEGIN fact:container_interior_length_mm -->5,893<!-- END fact:container_interior_length_mm --> × 2,388mm (19′ 4″ × 7′ 10″) — end zones occupied by equipment
**Image plane area:** ~<!-- BEGIN fact:image_area_sqft -->101<!-- END fact:image_area_sqft --> sq ft (9.42 m²)
**Camera configuration:** Option B (side-to-side), f = <!-- BEGIN fact:focal_length_mm -->2,362<!-- END fact:focal_length_mm -->mm, f/<!-- BEGIN fact:f_number -->1088<!-- END fact:f_number -->, pinhole Ø <!-- BEGIN fact:pinhole_diameter_mm -->2.17<!-- END fact:pinhole_diameter_mm -->mm

---

## Summary

Eight photosensitive processes were evaluated for a ~101 sq ft (<!-- BEGIN fact:film_plane_width_mm -->4,499<!-- END fact:film_plane_width_mm --> × <!-- BEGIN fact:film_plane_height_mm -->2,094<!-- END fact:film_plane_height_mm -->mm) active image plane at f/1088 in full sunlight. The analysis covers per-image cost, chemistry sourcing, mounting method, spectral response to natural light, and ISO equivalent — the last being the single most consequential variable for practical operation of this camera.

### The ISO problem

At f/1088, even the fastest non-film material (ISO 6 silver gelatin paper) requires a **corrected exposure of ~43 minutes** in full sun after Schwarzschild reciprocity correction. The slower historic processes extend this to hours or, in the case of gum bichromate, beyond a full day. The ISO spread across these materials is enormous — **3,200:1 from slowest (ISO 0.25) to fastest practical option (ISO 800 orthochromatic X-ray film)**. Material selection is therefore primarily a decision about how long the subject must hold still, and how long the camera must remain vibration-free and weather-stable.

| Process | ISO equiv. | Corrected exposure at f/1088 (full sun) | Per-image cost |
|---|---|---|---|
| Gum bichromate | **~0.25–0.5** | ~8–17 hours | $55–73 |
| Cyanotype (Herschel) | **~1–2** | ~2–4 hours | $30–40 |
| **Cyanotype (Ware formula) ★ selected** | **~2–4** | **~30–45 min** | **~<!-- BEGIN costing:s73-pp-std -->$91<!-- END costing:s73-pp-std -->** |
| Salt print | **~1–3** | ~1.5–4 hours | $251–323 |
| Van Dyke Brown | **~2–6** | ~45 min–2 hours | $111–186 |
| Ilford Multigrade RC paper | **~6** | **~43 min** | $405–480 |
| Liquid Light emulsion | **~6–12** | ~20–43 min | $630–780 |
| X-ray film (blue-sensitive) | **~50–200** | ~2–10 min | $600–900 |
| X-ray film (orthochromatic) | **~200–800** | **~20 sec–2 min** | $600–900 |
| Panchromatic film | ~100–400 | ~1–5 min | $2,000–8,000+ |

*Exposure times calculated from Sunny-16 baseline scaled to ISO, then corrected for Schwarzschild reciprocity failure using p = 0.85. Gum bichromate correction pushes these times beyond the useful Schwarzschild model; values are indicative only.*

### Spectral response: the portrait problem

None of the practical, affordable processes record red wavelengths. All historic processes (cyanotype, gum, salt, Van Dyke) are UV/blue-only — warm skin tones record darker than expected and green foliage goes near-black. Modern silver gelatin paper (Ilford Multigrade, Liquid Light on some formulations) adds green sensitivity, producing more natural skin modeling but still absent in the red. Only panchromatic film covers the full visible spectrum.

For portraiture, the practical ranking for tonal fidelity is: **Ilford Multigrade RC paper > Van Dyke Brown > salt print > cyanotype ≈ Liquid Light > gum bichromate**.

### Recommendations

| Goal | Process | Reason |
|---|---|---|
| **TBS-001 selected process** | Cyanotype (Ware formula) | ~<!-- BEGIN costing:s73-pp-std -->$91<!-- END costing:s73-pp-std -->/print (Standard ½-Ware; <!-- BEGIN costing:s73-pp-range -->$64–173<!-- END costing:s73-pp-range --> by tier); ~30–45 min exposure at f/1088; water development only; no silver, no fixer, no darkroom; archival permanence; iron-based — no reciprocity failure |
| **Best all-round portrait result** | Ilford Multigrade RC paper | ISO 6; ~43 min; best tonal fidelity of non-film options; proven at scale |
| **Lowest cost, repeatable experimentation** | Cyanotype (Ware formula) | ~<!-- BEGIN costing:s73-pp-std -->$91<!-- END costing:s73-pp-std -->/image; no fixer; no darkroom for processing; home chemistry; archival |
| **Shortest exposures, practical subject movement** | Orthochromatic X-ray film | ISO 200–800; sub-2-minute exposures; operationally complex at scale |
| **Most distinctive physical artifact** | Liquid Light on reclaimed wood/concrete | Surface texture visible through image; unrepeatable object |
| **Ruled out at f/1088** | Gum bichromate (solo) | ISO 0.25–0.5; 8–17 hour exposures are not practical for in-camera capture |

The one-time infrastructure cost — ACM backing panels on timber battens bolted to container ribs — is approximately **$900–1,500** and is shared across all processes.

---

## Overview

Covering a 101 sq ft photosensitive plane is not a solved problem in commercial photography. Every process listed below has been documented at large scale or can be extrapolated from known chemistry; costs are calculated per image for the full 101 sq ft surface including chemistry, substrate where applicable, and processing. All chemistry listed under historic/alternative processes can be sourced and mixed in a home or garage darkroom from commercially available reagents.

Processes are ordered roughly by per-image cost (historic processes first, then commercial products). Film is included at the end as the documented outlier.

**Substrate cost basis:** muslin/cotton-fabric lines use the project's **bulk-roll basis — ~$6 per 101 sq ft print** (three 60″ × 150-yd rolls ≈ $300 ÷ a 50-print run; see [Project Cost Breakdown §7.1](project-cost-breakdown.md)). Buying muslin retail for a single image would add ~$75–95. The cyanotype per-print figure is single-sourced to the cost model (Ware New Cyanotype tier).

---

## Process Comparison Table

| Process | Per-Image Cost (est.) | Darkroom for Processing | Home-Makeable Chemistry | Permanence | Development |
|---|---|---|---|---|---|
| **Cyanotype** | **~<!-- BEGIN costing:s73-pp-std -->$91<!-- END costing:s73-pp-std -->** | No | Yes | Excellent (archival) | Water wash only |
| **Gum bichromate** | **$55–$73** | No | Yes | Good (pigment-dependent) | Water wash only |
| **Salt print** | **$251–$323** | Yes (loading) | Yes | Moderate (needs gold toner for archival) | Printing-out, thiosulfate fix |
| **Van Dyke Brown** | **$111–$186** | Yes (loading) | Yes | Good (thiosulfate fixed) | Water + thiosulfate |
| **Ilford RC paper (rolls)** | **$380–$500** | Yes (loading) | No — commercial product | Excellent (RC base) | Dektol / stop / fixer |
| **Liquid Light on custom substrate** | **$430–$628** | Yes (loading + processing) | Partially | Excellent | Dektol / stop / fixer |
| **X-ray film (large sheets)** | **$600–$900** | Yes | No | Excellent | Rapid fixer |
| **Film (sheet/roll)** | **$2,000–$5,000+** | Yes | No | Excellent | C-41 / E-6 / B&W |

---

## 1. Cyanotype

**Estimated per-image cost: ~<!-- BEGIN costing:s73-pp-std -->$91<!-- END costing:s73-pp-std --> (Standard ½-Ware; <!-- BEGIN costing:s73-pp-range -->$64–173<!-- END costing:s73-pp-range --> by tier)**
**Darkroom required for processing: No**
**Home-makeable chemistry: Yes**

### Background

Invented by Sir John Herschel in 1842 and documented in *Philosophical Transactions of the Royal Society of London* (1842). One of the oldest surviving photographic processes. Used by Anna Atkins to produce the world's first photographically illustrated book (1843). The iron-based chemistry contains no silver, requires no darkroom for processing, and develops in plain water.

**Source:** Herschel, J.F.W., "On the Action of the Rays of the Solar Spectrum on Vegetable Colors," *Philosophical Transactions of the Royal Society of London*, 1842. Modern technical analysis: Getty Conservation Institute, *Atlas of Analytical Signatures of Photographic Processes — Cyanotype*, 2013 (available: getty.edu).

### Chemistry

**Mike Ware New Cyanotype formula (primary — recommended for TBS-001):**
- Part A: 200 g ammonium iron(III) oxalate (AmFe) dissolved in 300 ml warm water (50–60°C) — stir until clear
- Part B: 100 g potassium ferricyanide + 10 g ammonium dichromate dissolved in 1,150 ml water
- Mix equal volumes of A and B immediately before coating
- Apply to substrate in subdued light; allow to dry completely before exposure
- Develop: soak in plain cold water 5–10 minutes, agitating gently; image clears in highlights
- No fixer required
- **4–8× faster than Herschel formula** — baseline exposure ~30–45 min vs 2–3 hr at f/1088

**Source:** Ware, M., *Cyanotype: The History, Science and Art of Photographic Printing in Prussian Blue*, Science Museum, 1999. ISBN: 0901805831. Full formula and technical notes freely available at mikeware.co.uk.

**Traditional Herschel formula (alternative — simpler preparation, slower):**
- Solution A: 20 g ferric ammonium citrate (FAC, green grade) dissolved in 100 ml distilled water (room temp)
- Solution B: 8.1 g potassium ferricyanide dissolved in 100 ml distilled water
- Mix equal volumes A and B immediately before use; baseline exposure ~2–3 hr at f/1088

### Chemistry Quantities for 101 sq ft

Coverage on **muslin (cotton)** is **~120 ml/m²/coat** (sourced: AlternativePhotography ~123, Jacquard ~183 → plausible range 100–180; unmeasured on our pre-washed muslin — [sensitizer-trials §T1](sensitizer-trials.md) pending). Double coat for density → ~240 ml/m² × 9.42 m² ≈ 2.3 L of mixed solution per print. Fabric over-deposits ~8× vs rod-coated paper, so the volumes are much higher than a paper print.

| Reagent | Quantity (double coat) | Unit cost (2026) | Subtotal |
|---|---|---|---|
| Ferric ammonium oxalate (AmFe) — Ware | ~342 g | ~$99/454 g | **~$75** |
| Potassium ferricyanide | ~114 g | ~$6.17/100 g | ~$7 |
| Ammonium dichromate | ~2.5 g | ~$8/100 g | ~$0.20 |
| Distilled water | 2–3 liters | Negligible | — |
| **Chemistry total (Ware, Standard ½-Ware)** | | | **~$82/print** |

_Reconciled 2026-07-26 to the cost model (`costing.py` TIERS, Standard ½-Ware = 15 g/100 ml at 120 ml/m²/coat × 2 × 9.42 m² → **342 g AmFe / 114 g ferricyanide per print**, Ware's 3:1 ratio). The prior 179 g / 90 g figures under-counted the fabric coverage._

**Source:** Photographers' Formulary and Bostick & Sullivan (photoformulary.com, bostick-sullivan.com). AmFe ~$98.95/lb (Photographers' Formulary, firm 2026-07-26).
**Source for potassium ferricyanide:** Photographers' Formulary; $139.95/5 lb = $61.71/kg (firm 2026-07-26).

### Substrate Options and Costs

| Substrate | Cost per sq ft | Total (101 sq ft) | Notes |
|---|---|---|---|
| Unbleached muslin (100% cotton) | ~$0.05 (bulk roll) | **~$6** | Best absorption; bulk 50-print basis (~$300 ÷ 50); retail single sheet ~$70–112; same as The Great Picture substrate |
| Pre-washed cotton canvas | ~$0.80–1.20 | $100–151 | Heavier; more dimensional stability; good for large panels |
| Heavyweight cartridge/watercolor paper | ~$1.50–2.50 | $188–314 | Requires taping joins; difficult to handle at this scale |
| Hanji/Japanese tissue on backing | ~$2.00–4.00 | $251–502 | Exceptional tonal range; fragile at scale |

**Recommended substrate: unbleached muslin.** This matches the documented approach used in The Great Picture (2006) for their gelatin emulsion application; muslin absorbs cyanotype sensitizer evenly and is manageable as a continuous panel at 13-foot widths.

### Mounting and Preparation Method

1. **Pre-wash substrate** twice in hot water without detergent; dry fully. This removes sizing (starch filler) that repels sensitizer.
2. **Cut panels** to slightly oversize (e.g., 5,950 × 2,450mm). For full coverage, one continuous roll of 60" (1,524mm) wide muslin folded/overlapped at join, or two lengths of 120" wide drop cloth fabric joined with a single flat seam at center.
3. **Coat in subdued indoor light.** Lay fabric flat on clean plastic sheeting. Apply sensitizer with a foam roller or large Japanese hake brush. Work in two passes (horizontal, then vertical crossing) for even coverage.
4. **Dry completely** in a dark or very dimly lit space before loading. A fan speeds drying; heat is acceptable (sensitizer is stable when dry).
5. **Mount in camera:** Stretch fabric over a rigid backing panel — ACM (aluminum composite) sheet or plywood — using a staple gun or binder clips on a timber batten frame. The backing panel attaches to the structural ribs of the container interior. Fabric must be taut and flat; wrinkles will show in the final image.
6. **After exposure:** Remove panel in complete darkness or in the dark camera itself. Carry to a water source. Submerge or sluice with running water 5–10 minutes. No chemicals required. Image appears as deep Prussian blue on white/cream background.
7. **Dry flat** on clean surface. Cyanotype on fabric can be displayed as a hanging textile, stretched on a frame, or backed with rigid board.

### Important Constraints

- **UV sensitivity:** Cyanotype requires UV light (300–400 nm range). Direct sunlight provides adequate UV. The long exposure times this camera produces (30–60+ minutes at f/1088) are well within the range needed for cyanotype in full outdoor sunlight — this is actually the **most compatible process** with the camera's exposure characteristics.
- **Color:** Result is Prussian blue only. Cannot be converted to neutral or warm tone without toning chemistry (tannin toning produces a warm olive/black).
- **Moisture sensitivity when wet:** During processing, avoid excessive agitation which can lift sensitizer from poorly prepared fabric.

### Total Per-Image Cost (cyanotype on muslin)
| Item | Cost |
|---|---|
| AmFe + potassium ferricyanide (Ware, Standard ½-Ware) | ~$82 |
| Muslin (101 sq ft, bulk-roll basis ~$300 ÷ 50 prints) | ~$6 |
| Water / processing consumables | ~$3 |
| **Total per print (Standard tier; ~<!-- BEGIN costing:s73-pp-range -->$64–173<!-- END costing:s73-pp-range --> by tier)** | **~<!-- BEGIN costing:s73-pp-std -->$91<!-- END costing:s73-pp-std -->** |

---

<!-- brochure:skip -->

## 2. Gum Bichromate

**Estimated per-image cost: ~$55–73 total (single coat)**
**Darkroom required for processing: No**
**Home-makeable chemistry: Yes**

### Background

Developed in the 1850s–1890s as a pictorialist alternative to silver processes. Uses chromate salts to harden gum arabic (a natural tree resin) in proportion to UV exposure; unexposed gum is washed away with water. Any watercolor pigment can be used, producing images in any hue.

**Source:** Crawford, W., *The Keepers of Light: A History and Working Guide to Early Photographic Processes*, Morgan & Morgan, 1979, pp. 143–167. ISBN: 0871000725. This is the standard practitioner reference for historic processes.

### Chemistry

- Solution A: 15 g ammonium or potassium dichromate dissolved in 100 ml water (sensitizer)
- Solution B: gum arabic solution, 1:1 water to 14° Baumé gum arabic syrup (binder)
- Pigment: watercolor, mixed into gum solution at 1–3% by volume
- Combine A + B + pigment immediately before coating
- Develop: warm water wash, 5–15 min; unexposed areas lift and rinse away
- No fixer required — the process creates a stable, non-light-sensitive chromium-oxide/gum matrix

### Key Considerations

Gum bichromate is a **pigment process** — the image is formed by watercolor pigment embedded in hardened gum. It is **not a silver process** and requires no darkroom for development. It is, however, significantly lower in contrast than silver processes and requires multiple coats (4–8 passes) to build density and shadow detail.

For in-camera capture at f/1088 and the exposure times this camera produces, gum bichromate is viable — ammonium dichromate is approximately 2–3× more UV-sensitive than the standard potassium version.

**Multiple-coat implication:** Each coat requires drying, recoating, and re-exposure to a precise registration. For a 13-foot image, registration between coats is an engineering problem — mechanical pin registration or projection registration will be needed.

### Chemistry Quantities and Costs (single coat, 101 sq ft)

| Reagent | Quantity | Unit cost | Subtotal |
|---|---|---|---|
| Ammonium dichromate | 179–224 g | ~$8–12/100 g | ~$18 |
| Gum arabic powder (makes syrup) | 448–672 g | ~$12–18/lb (~$28–40/kg) | ~$13–22 |
| Watercolor pigment (tube or powder) | 45–90 ml/g | Varies widely; ~$15–30 | ~$18–27 |
| **Chemistry total (single coat)** | | | **~$49–67** |

For 4-coat image: multiply chemistry by 4 = ~$196–268 chemistry alone. **Caution: costs escalate sharply with multiple coats.**

### Substrate and Mounting

Same options as cyanotype; cotton fabric or heavy watercolor paper. The gum arabic binder adheres to fabric well. Mounting identical to cyanotype (stretched over ACM backing).

### Total Per-Image Cost (single coat, gum bichromate on muslin)
| Item | Cost |
|---|---|
| Chemistry (single coat) | ~$49–67 |
| Muslin (101 sq ft, bulk-roll basis) | ~$6 |
| **Total** | **~$55–73** |

*Note: 4-coat image builds to ~$202–274. Single coat may be sufficient for a graphic, high-contrast aesthetic.*

---

## 3. Salt Print

**Estimated per-image cost: ~$251–$323 total (silver-dominated)**
**Darkroom required for processing: Yes (for loading; processing can be done in subdued light)**
**Home-makeable chemistry: Yes**

### Background

Invented by William Henry Fox Talbot, 1834–1840. The first negative-positive photographic process. One of the most studied historic photographic media.

**Source:** Schaaf, L.J., *Out of the Shadows: Herschel, Talbot and the Invention of Photography*, Yale University Press, 1992. Technical data: Reilly, J.M., *The Albumen and Salted Paper Book*, Light Impressions, 1980.

### Chemistry

**Two-bath process:**
1. **Salting bath:** 2% sodium chloride (table salt, w/v) in water. Soak or brush onto substrate; dry.
2. **Sensitizing bath:** 10–15% silver nitrate (w/v) in water. Brush onto salted substrate in subdued red/orange light or near-darkness. Silver chloride forms in situ.
3. **Exposure:** Printing-out process — image appears during exposure without development. No developer required.
4. **Fix:** 20–25% sodium thiosulfate ("hypo") solution, 5–10 minutes. Rinse thoroughly in running water, 30 minutes minimum.
5. **Optional:** Gold toner (sodium gold chloride, 0.1%) applied between exposure and fixation significantly improves archival stability and shifts color to red-brown/neutral.

### Chemistry Quantities and Costs for 101 sq ft

**Silver nitrate requirement:** ~5–10 ml of 12% solution per sq ft = 628–1,255 ml total. At 12% concentration: 75–151 g of AgNO₃.

| Reagent | Quantity | Unit cost | Subtotal |
|---|---|---|---|
| Silver nitrate (AgNO₃) | 90–152 g | ~$260/100 g (Chem-Impex) | **$233–$396** |
| Sodium chloride (table salt) | 90–179 g | Negligible (~$1) | ~$1 |
| Sodium thiosulfate (fixer) | 0.9–1.8 kg | ~$5–10/kg (bulk) | ~$9 |
| **Chemistry total** | | | **~$242–$406** |

**Source for silver nitrate pricing:** Chem-Impex catalog (chem-impex.com); ~$260.69/100g for reagent-grade AgNO₃ (2026). Photographers' Formulary also supplies it via B&H Photo at comparable pricing.

**Note:** Silver nitrate pricing makes the salt print process moderately expensive and introduces safety and regulatory considerations — AgNO₃ permanently stains skin, clothing, and surfaces black. Nitrile gloves and good ventilation are required.

### Substrate

Heavy cotton rag paper (90–300 gsm) or unsized cotton/linen fabric. Paper requires pre-soaking in the salting bath; fabric can be brushed. Sizing must be removed from commercial fabrics.

### Mounting and Preparation

Identical to cyanotype in principle. Sensitized sheets/panels must be loaded in near-darkness. The two-bath chemistry means the substrate can be salted (step 1) in daylight; only the silver nitrate sensitizing step (step 2) and loading must occur in darkness.

### Total Per-Image Cost (salt print on rag cotton)
| Item | Cost |
|---|---|
| Silver nitrate (~117 g) | ~$303 |
| All other chemistry | ~$13 |
| Cotton muslin (101 sq ft, bulk-roll basis) | ~$6 |
| **Total** | **~$251–$323** (silver nitrate is the driver) |

*This is higher than the initial table estimate due to silver nitrate quantities at scale. Recalibrated from chemistry volumes above.*

---

## 4. Van Dyke Brown

**Estimated per-image cost: ~$111–$186 total**
**Darkroom required for processing: Yes (loading)**
**Home-makeable chemistry: Yes**

### Background

Developed in the 1890s as a simplified, lower-cost silver process. Named for the warm brown tones resembling Van Dyck paintings. Uses ferric ammonium citrate (same as cyanotype) but adds silver nitrate for a silver-based image.

**Source:** Crawford, W., *The Keepers of Light*, Morgan & Morgan, 1979, pp. 133–141. Formulary: Reilly, J.M., op. cit.

### Chemistry (Standard Vandyke Formula)

- 25 g ferric ammonium citrate (green)
- 2.5 g tartaric acid
- 10 g silver nitrate
- Dissolve each in ~35 ml water separately, combine in order listed, make up to 100 ml
- Apply to substrate in subdued light; dry
- Expose to UV; develop in running water 3–5 min; fix in 25% sodium thiosulfate 2–5 min; wash 20 min

### Chemistry Quantities and Costs for 101 sq ft

Coverage: approximately the same as cyanotype, 2 ml/sq ft. For 101 sq ft: 244 ml of sensitizer.

At 10 g AgNO₃ per 100 ml solution: **25 g silver nitrate** for single coat.

| Reagent | Quantity | Unit cost | Subtotal |
|---|---|---|---|
| Silver nitrate | 27–54 g (single/double coat) | ~$260/100 g | ~$70–$140 |
| Ferric ammonium citrate | 63–90 g | ~$15/100 g | ~$13–$18 |
| Tartaric acid | 6–9 g | ~$8–12/100 g | ~$4 |
| Sodium thiosulfate | 448 g | ~$5/kg | ~$3 |
| **Chemistry total** | | | **~$90–$165** |

### Total Per-Image Cost (Van Dyke on muslin)
| Item | Cost |
|---|---|
| Chemistry | ~$90–$165 |
| Muslin (101 sq ft, bulk-roll basis) | ~$6 |
| Misc (water, containers, gloves) | ~$15 |
| **Total** | **~$111–$186** |

*Significantly cheaper than salt print due to lower silver nitrate concentration — the ferric iron does most of the photochemical work.*

---

## 5. Commercial Silver Gelatin Paper — Ilford Multigrade RC Rolls

**Estimated per-image cost: $380–$520 total**
**Darkroom required for processing: Yes (loading and development)**
**Home-makeable chemistry: No — commercial product**

### Product Specification

Ilford Multigrade V RC Deluxe is the industry-standard enlarging paper and the most widely used product for this application globally. Available in roll form specifically for large-scale work.

| Spec | Value |
|---|---|
| Max roll width | **127 cm (50")** |
| Roll length | 30.5 m (100 ft) |
| ISO equivalent | ~ISO 6 |
| Base | Resin-coated (RC) polyethylene — waterproof, dimensionally stable |
| Contrast | Variable (multigrade, but without enlarger filter = approximately Grade 2) |
| Tone | Neutral-cool (neutral developer) or warm-neutral (dilute developer) |

**Source:** Ilford Photographic product pages (ilfordphoto.com). Adorama listing: 42" × 98' and 50" × 98' roll formats confirmed in stock.

### Coverage Calculation

Active image plane: 4,499mm wide × 2,094mm tall.
Paper roll width: 1,270mm (50").
Number of strips needed: ⌈4,499 / 1,270⌉ = **4 strips** (covers 5,080mm — 581mm spare).
Each strip height: 2,094mm (~6.87 ft), cut from the 30.5 m roll.
Strips from one roll: ⌊30,500 / 2,094⌋ = **14 strips per roll** → **3 complete images per roll** (with ~1,184mm of roll remaining).

### Material Cost

A 50" × 100' roll of Ilford Multigrade V RC Deluxe retails at approximately **$600–750** (B&H Photo, Freestyle Photographic, 2026 pricing). At 2 images per roll: **~$300–375 per image in paper cost.**

### Processing Chemistry (101 sq ft)

Floor-tray or in-camera processing required; standard silver gelatin chemistry.

| Chemical | Volume needed | Product | Approx. cost |
|---|---|---|---|
| Developer (Dektol 1:2 dilution) | 12–15 liters | Kodak Dektol 1.8 kg powder (makes 37L stock) | ~$45 |
| Stop bath (1% acetic acid) | 5 liters | Kodak indicator stop bath, diluted | ~$10 |
| Rapid fixer | 15–20 liters | Ilford Rapid Fixer, diluted 1:4 | ~$30 |
| **Chemistry total** | | | **~$85** |

*Chemistry can be reused across multiple images with replenishment; per-image cost drops significantly at volume.*

### Seam Management

Five vertical strips require four seams across the image. Options:
1. **Accept seam lines** as a design feature — horizontal bands visible at 1,270mm intervals across width.
2. **Butt-join on flat backing with black photographic tape** applied to the back; front surface is continuous but slight ridges may be visible.
3. **Overlap joins in shadow areas** of the composition — position seams deliberately to fall in dark background, minimizing visibility.
4. **Single-emulsion coating** on a seamless substrate (see Liquid Light below) avoids seams entirely.

### Mounting Method

1. Pre-cut five strips to 2,450mm (allowing overlap/trim) in complete darkness or under dark cloth in a light-tight changing tent.
2. Lay ACM backing panel flat on the floor (camera interior or adjacent dark space). Adhere strips to backing using repositionable photographic mounting adhesive or double-sided photo-safe tape on the back face.
3. Butt strips together or overlap by 10mm. Tape reverse side seams with 2" black photographic tape.
4. Load backing panel into camera, emulsion side inward, and secure to container structural ribs.
5. Entire loading process must occur in complete darkness.

### Total Per-Image Cost (Ilford RC paper)
| Item | Cost |
|---|---|
| Paper (50"×100' roll ÷ 2) | ~$300–375 |
| Developer (Dektol) | ~$45 |
| Stop + Fixer | ~$40 |
| Misc (tape, backing material) | ~$20 |
| **Total** | **~$405–480** |

---

## 6. Liquid Light Gelatin Emulsion on Custom Substrate

**Estimated per-image cost: $430–$628 total**
**Darkroom required for processing: Yes (loading and processing)**
**Home-makeable chemistry: Partially — commercial emulsion on custom substrate**

### Product

Rockland Colloid Liquid Light (LLE series) is a liquid silver gelatin emulsion that can be applied to any surface including wood, metal, fabric, concrete, glass, and ceramics. It is the most widely available product of this type.

| Spec | Value |
|---|---|
| Coverage | ~1.5 sq ft per fluid oz (single coat) |
| Surfaces | Porous and non-porous; works on wood, canvas, ACM board, cement board |
| Contrast | Medium-high (~equivalent to Grade 3) |
| ISO equivalent | Similar to photographic paper (~ISO 6–12) |
| Processing | Standard silver gelatin developer/stop/fixer |

**Source:** Rockland Colloid product documentation (rockaloid.com); B&H Photo product page (B&H item # ROLLE8).

### Coverage and Cost

For 101 sq ft at 1.5 sq ft/oz (single coat): **~81 oz required**.
Double coat (recommended for density): **~168 oz**.

Liquid Light retail: approximately **$25–30 per 8 oz (237 ml) bottle**.
For double coat: 168 oz ÷ 8 oz/bottle = 21 bottles → **~$525–630 in emulsion alone**.

This is the most expensive material option and is primarily justified by the unique aesthetic possibilities of the substrate (see below).

### Substrate Options

| Substrate | Aesthetic | Cost per sq ft | Total (101 sq ft) |
|---|---|---|---|
| Pre-primed canvas (artist canvas roll) | Neutral; flexible | ~$0.80–1.20 | $100–151 |
| ACM aluminum composite panel | Industrial; rigid; planar | ~$2.00–3.00 | $251–377 |
| Plywood (birch, sanded) | Wood grain visible through image | ~$0.50–0.80 | $63–100 |
| Reclaimed barn board planks | Strong texture; art object | Variable; often free–$1/sq ft | $0–126 |
| Cement board (Hardiebacker) | Concrete surface texture | ~$0.60–0.80 | $75–100 |

### Preparation and Mounting

1. **Prime substrate** — porous surfaces (wood, canvas, cement) must be sealed with diluted gesso (2 coats) or PhotoFlo wetting agent in water. Smooth surfaces (metal, ACM) benefit from a light sanding to improve adhesion.
2. **Warm emulsion** to 40–50°C (Liquid Light gels at room temperature) in a water bath; do not microwave.
3. **Apply in complete darkness** with a foam roller or brush in two passes. Apply second coat when first is just set.
4. **Allow to cool** and fully gel (~5 min at room temp). Expose within 24 hours or refrigerate in dark.
5. **Mount** — rigid substrates bolt to container ribs; canvas panels can be stretched over a timber frame and attached to ribs. Multiple ACM panels can tile the image plane with butt joints.
6. **Process** using standard Dektol developer (same chemistry as Ilford paper); developer must be brought to substrate in floor-tray method or the container interior drainage system.

### Total Per-Image Cost (Liquid Light on reclaimed wood planks)
| Item | Cost |
|---|---|
| Liquid Light emulsion (double coat, ~168 oz) | ~$525–630 |
| Substrate (reclaimed wood — near free) | ~$0–45 |
| Developer + Stop + Fixer | ~$85 |
| Misc (gesso primer, brushes) | ~$20 |
| **Total** | **~$630–780** |

*(On canvas substrate, substrate cost adds ~$103 but emulsion cost dominates.)*

**Design note:** Liquid Light on wood planks or cement board produces a photograph that is simultaneously an art object — the surface texture of the substrate merges with the photographic image, creating an artifact that cannot be replicated by any print-on-demand process. This is the highest-cost option but the highest uniqueness value.

---

## 7. X-Ray Film (Large Format)

**Estimated per-image cost: $600–$900 total**
**Darkroom required for processing: Yes (loading and processing)**
**Home-makeable chemistry: Partially (standard B&W chemistry)**

### Product

Industrial and medical X-ray film is available in very large sheet formats, unlike photographic film. Green-sensitive (orthochromatic) double-sided emulsion. Sensitive to both X-ray and visible light.

| Spec | Value |
|---|---|
| Available sizes | Up to 14"×17" (355×432mm) standard medical; industrial film to 36"×48" (914×1,219mm) and larger |
| ISO equivalent | Approximately ISO 400–800 (much faster than paper) |
| Base | Polyester; dimensionally stable; blue-gray tint |
| Emulsion | Double-sided silver halide; blue/green sensitive |

At approximately $5–8 per 14"×17" sheet, covering 101 sq ft would require roughly 131–175 sheets depending on layout, at a material cost of $654–$1,393. Large-format industrial X-ray film in continuous rolls is available from medical/NDT suppliers, but ordering in custom widths is typical.

The significantly higher ISO rating means exposure times at f/1088 would be 5–8× shorter than with paper — approximately 5–10 minutes versus 40+ minutes for paper in full sun. This is an operationally significant advantage.

### Processing

Standard B&W film developer (D-76, HC-110, or Kodak Rapid X-Ray developer) and rapid fixer. Sheets can be developed face-up on plastic sheeting using the floor-tray method.

### Practical Limitation

X-ray film is double-coated — emulsion on both sides. Wet processing produces a dimensionally stable but somewhat delicate large sheet. Handling and tiling 135+ sheets in complete darkness is a significant operational challenge. A continuous roll format would be far preferable but difficult to source. **For this reason X-ray film is rated as viable but operationally complex.**

---

## 8. Film (Sheet/Roll) — Cost Outlier

**Estimated per-image cost: $2,000–$8,000+**
**Included for completeness; not recommended as primary medium**

Covering 101 sq ft with photographic film at any standard format produces costs that are an order of magnitude higher than paper-based options:

| Format | Sheets needed | Cost/sheet | Material cost |
|---|---|---|---|
| 8×10 in | ~314 sheets | $8–15 (Ilford HP5/FP4) | $2,512–$4,710 |
| 11×14 in | ~152 sheets | $15–25 | $2,280–$3,800 |
| 20×24 in | ~54 sheets | $40–80 (specialty) | $2,160–$4,320 |

Processing adds C-41 or B&W chemistry at additional cost. 8×10 sheet film in continuous rolls is not commercially available. Handling and tiling 314+ sheets of 8×10 in complete darkness is impractical.

Film is included here for completeness and to confirm the user's instinct: **film is categorically the wrong medium for a <!-- BEGIN fact:image_area_sqft -->101<!-- END fact:image_area_sqft --> sq ft image plane**, both on cost and operational grounds.

---

<!-- brochure:endskip -->

## 9. Mounting System Summary

Regardless of process, the image plane requires a flat rigid backing. Corrugated container walls are not flat and cannot serve as a direct mounting surface.

### Recommended Backing System

**Aluminum Composite Material (ACM / Dibond) panels, 3mm thick:**
- Available in 4×8 ft (1,220×2,440mm) sheets; approximately 16 sheets needed to tile 101 sq ft
- ACM is completely flat, dimensionally stable, lightweight (~3 lb/sq ft), and mounts by bolting through panel edge to timber battens or directly to container rib flanges
- Chemical-resistant (developer, fixer do not damage aluminum face)
- Cost: ~$40–60 per 4×8 sheet × 16 sheets = **$640–960 for the backing system** (one-time infrastructure cost, reusable)

**Alternative: 3/4" plywood sheets** — cheaper (~$40–50 per 4×8 sheet), but heavier and requires sealing against moisture before use with chemistry.

### Panel Attachment to Container

Timber battens (2×4 lumber) are bolted to the container's internal structural ribs (the vertical corrugation flanges). ACM panels then attach to the timber battens with stainless steel screws. Total system adds approximately $200–400 in lumber and hardware (one-time cost).

### Photosensitive Material Attachment to Backing Panel

| Material type | Attachment method |
|---|---|
| Fabric (muslin, canvas) | Staple gun to timber battens at edges; tension tight |
| Rigid paper sheets | Double-sided photo-safe tape to ACM; butt joints taped on reverse |
| Liquid Light on ACM | Directly applied; no secondary mounting needed |
| Liquid Light on wood planks | Planks hung on French cleats (wall-mount rail system) bolted to container ribs |
| X-ray film sheets | Repositionable aerosol mounting adhesive on ACM backing |

---

## Recommendation by Use Case

| Goal | Recommended Process | Reason |
|---|---|---|
| **Lowest cost, most repeatable** | Cyanotype on muslin | ~<!-- BEGIN costing:s73-pp-std -->$91<!-- END costing:s73-pp-std --> per image; no silver; no darkroom for processing; scales to any size; archivally stable; home-makeable chemistry |
| **Richest tonal range, conventional photograph look** | Ilford RC paper | Industry-standard; predictable; support widely available; ~$420 per image |
| **Most unique physical artifact** | Liquid Light on reclaimed wood or concrete | Surface texture merges with image; unrepeatable object; highest cost |
| **Fastest exposure time** | X-ray film | ~ISO 400–800 vs ISO 6 for paper; 5–10 min exposures possible; operationally complex |
| **Cheapest repeated experimentation** | Gum bichromate on muslin | ~$55–73 single coat; fully repeatable; any color; no silver |
| **Historic authenticity** | Salt print or Van Dyke on cotton rag | Talbot-era processes; warm brown tones; moderate cost |

---

## Appendix A: Spectral Response to Natural Light

This appendix analyzes how each process renders a natural daylight scene. The same questions are answered for every material: what wavelengths does it respond to, how does sunlight translate into tonal values, and what does that mean specifically for outdoor portrait work — the primary intended use of this camera.

The central variable is the **spectral sensitivity** of each photosensitive material. Sunlight is broadband: it contains UV, blue, green, yellow, and red in roughly equal photon flux across the visible range. A material that cannot see red will render warm skin tones, red objects, and much of the subtlety of autumn foliage as dark or black. A material that cannot see green will compress mid-tone separation. Understanding these limits is not academic — they determine whether a portrait looks natural, pallid, graphic, or completely alien.

---

### A.1 Cyanotype

**Sensitive wavelengths:** UV (300–400 nm) and short-wave blue (400–450 nm) only.
**Blind to:** Green (500–565 nm), yellow, orange, red.
**Safelight:** Yellow-green (Wratten OC or equivalent) is safe; red is safe.
**ISO equivalent:** ~1–2 (Herschel standard formula); ~2–4 (Ware improved formula).
**Corrected exposure at f/1088, full sun:** ~30–45 min (Ware formula, selected) to ~2–4 hours (Herschel).

**Source for ISO figures:** Practitioner consensus documented across pinhole photography literature, including Renner, E., *Pinhole Photography*, 4th ed., Focal Press, 2009, and Ware, M., *Cyanotype*, 1999. Cyanotype ISO is highly UV-condition-dependent — hazy sky, low sun angle, or high latitude dramatically increases actual exposure time beyond calculated values. ISO figures assume direct overhead summer sun.

**Source for spectral sensitivity:** Ware, M., *Cyanotype*, 1999, Chapter 3 ("The Spectral Sensitivity of Cyanotype"). The ferric ammonium citrate / potassium ferricyanide system has its peak absorption in the UV and falls to near-zero by 500 nm.

#### Tonal Rendering in Sunlight

| Subject | Rendered tone |
|---|---|
| Blue sky (high UV + blue content) | **Very bright — prone to overexposure** |
| White clouds | Bright — similar to sky, low separation |
| Green foliage | **Very dark — near black** |
| Human skin (warm tones) | Dark to mid-gray — red/yellow components not recorded |
| Red objects | **Black** |
| Yellow/orange | Near-black |
| White surfaces | Bright |
| Deep shadow | Black — no shadow detail separation |

#### Portrait Implications

Cyanotype renders faces in a distinctive, flattening way. The warm chromatic content of skin (red-yellow wavelengths) is entirely absent from the exposure. What registers is the UV/blue component of reflected light from the face — pale tones record, but flush cheeks, lips, and the warmth of an outdoor complexion disappear. The result is a slightly mask-like, high-graphic rendering. This is historically characteristic — Anna Atkins' cyanotype portraits have exactly this quality.

Blue sky behind a subject will overexpose aggressively. Overcast or open shade lighting is strongly preferred: it eliminates the sky problem and provides a soft, diffuse UV source that gives more even coverage across the face.

#### Contrast

Cyanotype has a relatively compressed tonal range (short scale). It produces strong deep blues in shadows and clear whites in highlights, with limited mid-tone separation. Multiple coats or the improved Ware formula improve shadow density but the core contrast characteristic does not change fundamentally.

---

<!-- brochure:skip -->

### A.2 Gum Bichromate

**Sensitive wavelengths:** UV (300–400 nm) and short-wave blue (400–460 nm).
**Blind to:** Green, yellow, orange, red.
**Safelight:** Red safelight is safe; yellow-green safe at low intensity.
**ISO equivalent:** ~0.25–0.5 (potassium dichromate); ~0.5–1 (ammonium dichromate, which is 2–3× more sensitive).
**Corrected exposure at f/1088, full sun:** ~8–17 hours (potassium dichromate); ~4–8 hours (ammonium dichromate).

**Practical implication: gum bichromate is not viable as a primary in-camera process at f/1088.** At 8–17 hours, a single exposure spans daylight, sunset, and astronomical darkness — the illumination changes are uncontrollable and the accumulated exposure across the full period would be chaotic. Gum bichromate is retained in this report because it is an excellent option for contact printing from a negative made on one of the faster materials, and because a larger pinhole (reducing the f-number) could bring exposure times into range. At f/300 (achievable with a ~8mm pinhole), ISO 0.5 gum bichromate would require ~40 minutes — fully workable, though at the cost of a larger blur circle.

**Source for ISO figures:** Crawford, W., *The Keepers of Light*, 1979; practitioner documentation at alternativephotography.com. Ammonium dichromate speed advantage: Ware, M., *Cyanotype*, 1999, Appendix (comparative sensitizer analysis).

#### Tonal Rendering in Sunlight

Identical spectral blindness to cyanotype — both processes are sensitized by the same chromate/iron UV absorption mechanism. The tonal rendering table is the same: blue sky overexposes, foliage goes dark, warm skin tones flatten.

**One important difference from cyanotype:** gum bichromate renders in whatever watercolor pigment is chosen. A portrait done in raw umber or sepia pigment will have a warm brown palette regardless of what wavelengths the process responds to. The *color* of the image is decoupled from the *tonal scale*. This means the alien quality of missing warm skin tones can be partially compensated by choosing a warm pigment — the shadows and mid-tones read as "warm" even though the exposure was UV-only.

#### Contrast

Lower inherent contrast than most silver processes. A single coat of gum bichromate produces a soft, low-contrast image — sometimes described as "impressionistic." Multiple coats build density and contrast. For a strong outdoor portrait with good shadow detail, expect to make 4–6 coats with precise registration between passes.

---

### A.3 Salt Print

**Sensitive wavelengths:** UV (300–400 nm) and blue (400–480 nm).
**Blind to:** Green, yellow, orange, red.
**Safelight:** Red safelight is safe.
**ISO equivalent:** ~1–3.
**Corrected exposure at f/1088, full sun:** ~1.5–4 hours.

Salt print is a printing-out process — the image forms during exposure without a developer. This absence of development amplification keeps the effective speed low despite silver being the active compound. Speed varies with silver nitrate concentration at coating: higher concentration (15% vs. 10%) yields a modest speed increase at the cost of more AgNO₃ consumption.

**Source for ISO figures:** Reilly, J.M., *The Albumen and Salted Paper Book*, Light Impressions, 1980; Renner, E., *Pinhole Photography*, 4th ed., Focal Press, 2009.

**Source:** Reilly, J.M., *The Albumen and Salted Paper Book*, Light Impressions, 1980, Chapter 2. Silver chloride (AgCl) is the active compound. Its absorption edge is approximately 470–480 nm; it responds to UV and blue, not to green or red. This is the characteristic that made early Daguerreotype and Talbotype portraits require subjects to wear specific colors.

#### Tonal Rendering in Sunlight

| Subject | Rendered tone |
|---|---|
| Blue sky | Very bright — overexposes readily |
| Green foliage | Dark mid-gray to near-black |
| Human skin | **Noticeably darker/flatter than expected** — critical issue for portraits |
| Red objects | Black |
| Blue eyes | Light — the one feature that renders distinctively well |
| Hair (dark brown) | Black — no differentiation in dark warm tones |
| White shirt | Bright |

#### Portrait Implications

Salt prints of people made in the 1840s–1860s have a characteristic look that is often described as "ghostly" — subjects with warm complexions appear much darker than we would expect, and the subtlety of facial modeling (warm highlights vs. cooler shadows) is compressed. This was the era's technical reality; it is now a historical aesthetic. For this project, whether this quality is desirable depends on the artistic intent.

**Critical practical issue:** Subjects must remain absolutely still during exposure. Salt prints are slower than cyanotype (silver chloride is marginally faster than the iron process but both require minutes at f/1088). At 30–60 minutes exposure time, any movement will produce blur. This is not a process for candid portraiture.

#### Contrast and Tone

Salt prints have a characteristic warm red-brown image tone (silver image color depends on particle size and fixing). With standard sodium thiosulfate fixing, the tone is warm red-brown. Gold toning before fixation shifts the image to a purple-black or neutral, and significantly improves permanence.

---

### A.4 Van Dyke Brown

**Sensitive wavelengths:** UV and blue (300–480 nm), nearly identical to salt print.
**Blind to:** Green, yellow, orange, red.
**Safelight:** Red safelight is safe.
**ISO equivalent:** ~2–6.
**Corrected exposure at f/1088, full sun:** ~45 min–2 hours.

Van Dyke Brown is the fastest of the iron/silver UV processes. The two-stage mechanism (iron absorbs UV → reduces silver ion to silver metal) benefits from development amplification unlike the printing-out salt print: unexposed areas are washed away in water, so the image is formed by developed-out silver, not just printed-out silver. This gives it a meaningful speed advantage — roughly 2–3× faster than salt print and faster than standard cyanotype, putting it within practical range of the camera at its slower end.

**Source for ISO figures:** Crawford, W., *The Keepers of Light*, 1979; practitioner data from Photrio.com (vandyke brown in-camera tests, multiple contributors). ISO 2–6 is consistent with a developed-out iron-silver process at standard formulation.

**Source:** Crawford, W., *The Keepers of Light*, 1979, p. 135. The sensitization mechanism begins with ferric iron absorbing UV/blue, which reduces to ferrous; ferrous then reduces silver nitrate to metallic silver. The initial UV absorption step is the sensitivity-limiting stage.

#### Tonal Rendering in Sunlight

Identical spectral response to salt print. The tonal rendering table is the same. Van Dyke Brown will produce:
- Blue sky: bright, potentially blown out
- Green foliage: dark
- Warm skin: darker than expected, flattened modeling
- Red objects: black

**Difference from salt print:** Van Dyke Brown has a longer tonal scale (more mid-tone separation) than either cyanotype or salt print. It handles the transition from shadows to mid-tones more gracefully, making it somewhat better suited to outdoor portraiture despite the same spectral limitations.

The image color is warm red-brown (similar to, and named after, Van Dyck paintings). Fixed with sodium thiosulfate.

---

### A.5 Ilford Multigrade RC Paper (Silver Gelatin, Enlarging Paper)

**Sensitive wavelengths:** Blue (400–500 nm) and green (500–565 nm).
**Blind to:** Orange (>580 nm) and red.
**Safelight:** Red/amber (Ilford 902 or equivalent) is safe.
**ISO equivalent:** ~6.
**Corrected exposure at f/1088, full sun:** ~43 minutes (Schwarzschild corrected, p = 0.85).

ISO 6 is the well-established community standard for silver gelatin enlarging paper used in pinhole cameras and is consistent with the exposure calculations in the main body of this report. Ilford does not publish an in-camera ISO for their paper (it is designed for enlarger use), but ISO 6 is reproduced across Renner (2009), and practitioner tests on Photrio and the Large Format Photography Forum. Development time and developer dilution affect effective speed by approximately ±½ stop; Dektol 1:2 at 68°F/20°C for 90 seconds is the reference condition.

**Source:** Ilford Technical Data Sheet, Multigrade V RC Deluxe (available: ilfordphoto.com/downloads). Ilford Multigrade paper uses a dual-emulsion variable contrast system: one emulsion layer is blue-sensitive (responds to Grade 5 type contrast when exposed to blue light) and a second layer is green-sensitive (responds to Grade 0 type contrast when exposed to green light). Used in-camera without filtration, both layers expose together and the result is approximately Grade 2 contrast.

#### Tonal Rendering in Sunlight

This is the most broadly sensitive of the iron/UV processes and significantly better than cyanotype or salt print for natural light photography. The addition of green sensitivity means foliage, mid-green skin tones, and daylight shadows are all recorded.

| Subject | Rendered tone |
|---|---|
| Blue sky | **Bright — still prone to overexposure** vs. panchromatic film |
| White clouds | Good separation from sky (cloud diffuses UV, sky transmits it) |
| Green foliage | **Mid-gray to light gray — recorded naturally** |
| Human skin | **Better than UV-only processes, but warm reds still absent** — slight pallor |
| Red objects | Dark gray to near-black (no red sensitivity) |
| Yellow | Mid-gray (only blue component registers) |
| Blue eyes | Light |
| Brown/dark hair | Dark — better than UV-only processes |
| Deep blue sky with clouds | Limited separation — both read bright |

#### Portrait Implications

For outdoor portraiture, Ilford Multigrade paper is markedly better than cyanotype, gum, salt, or Van Dyke. The green sensitivity captures the green component of skin tones, which provides natural-looking mid-tone modeling. However, red is still absent — warm rosy cheeks, warm-toned skin in golden-hour light, and red clothing all render darker than they would on panchromatic film.

The practical effect in a portrait: faces look natural in shade or overcast light where the illumination is cool/neutral. In warm directional sunlight (golden hour), the image will flatten — the warmth that makes the scene beautiful to the eye does not register.

**Blue sky overexposure** is the most consistent practical problem. For a portrait with sky in the frame at f/1088 with a 40-minute exposure, the sky will likely be a pure white field. A deep yellow or orange filter (Wratten 8 or 15) placed over the pinhole would balance sky/skin by reducing blue transmission — but this also cuts overall exposure, lengthening times further. More practical: position subjects against non-sky backgrounds, or use the sky's blown-out quality as an intentional design element.

#### Contrast

Grade 2 in-camera (both emulsion layers exposing together). Good shadow/highlight separation. Long scale relative to all alternative processes listed above. The most "photographic" looking of the non-film options.

---

### A.6 Liquid Light Gelatin Emulsion (Rockland Colloid)

**Sensitive wavelengths:** Blue (400–500 nm) and UV.
**Blind to:** Green (limited response), yellow, orange, red.
**Safelight:** Red/amber safelight is safe.
**ISO equivalent:** ~6–12.
**Corrected exposure at f/1088, full sun:** ~20–43 minutes.

The speed range reflects variation by substrate — porous substrates (wood, unprimed canvas) absorb part of the emulsion layer, effectively reducing silver density and therefore speed. A properly sealed, primed surface achieves the upper end of the range (~ISO 12). Applying two coats increases silver density and pushes speed slightly higher; it also improves maximum black density and shadow detail. The manufacturer specifies comparable speed to photographic paper (ISO 6), which is the conservative baseline.

**Source:** Rockland Colloid product documentation. Liquid Light is a silver halide emulsion of older formulation than modern variable-contrast enlarging papers — it uses a simpler, non-spectrally-sensitized silver bromide/chloride emulsion without the dye-sensitization that gives modern papers their green sensitivity.

#### Tonal Rendering vs. Ilford RC Paper

This is the critical distinction between Liquid Light and Ilford Multigrade paper: **Liquid Light lacks the green sensitization** that makes modern enlarging papers more capable in daylight. It behaves more like a UV/blue-sensitive material — closer to cyanotype and salt print in tonal character than to Ilford Multigrade.

| Subject | Liquid Light | Ilford Multigrade |
|---|---|---|
| Green foliage | Dark (near UV-process) | Mid-gray (green-sensitized) |
| Skin tones | Flatter/darker | More natural |
| Blue sky | Very bright | Bright |
| Red | Near-black | Dark gray |

For outdoor portraits, Liquid Light will produce a more graphic, higher-contrast, slightly alien rendering compared to Ilford paper. This may be desirable or not depending on the artistic intent — applied to wood grain or concrete, the graphic high-contrast quality may complement the substrate texture.

#### Contrast

Equivalent to approximately Grade 3 (manufacturer specification). Higher inherent contrast than Ilford Multigrade at Grade 2. Shadows will block up more readily. A compensating developer (Dektol 1:4 or Rodinal 1:50) can pull contrast down; normal Dektol 1:2 will give very punchy results.

---

### A.7 X-Ray Film

*Full analysis already presented in the body of this document (Section 7). Summary below for comparison.*

**Sensitive wavelengths:** UV and blue (blue-sensitive type) or UV, blue, and green (orthochromatic/green-sensitive type).
**Blind to:** Red (and orange in blue-sensitive type).
**ISO equivalent:** ~50–200 (blue-sensitive, direct exposure); ~200–800 (orthochromatic/green-sensitive screen-type).
**Corrected exposure at f/1088, full sun:** ~2–10 min (blue-sensitive); ~20 sec–2 min (orthochromatic).

The speed range within X-ray film is wider than across all the other materials combined. Screen-type orthochromatic X-ray film is designed to expose via the light emitted by a rare-earth intensifying screen (which fluoresces green) and is therefore optimized for that narrow spectral band — but it still responds to broadband daylight. At ISO 200–800, exposures at f/1088 drop below 2 minutes, which transforms the operational challenge entirely: a subject can hold still for 90 seconds far more reliably than for 43 minutes, and camera vibration from wind is not a meaningful concern over that duration.

The trade-off is product specificity: **not all X-ray film is the same**. Medical green-sensitive film (e.g. Fujifilm HR-T, Agfa Curix Ortho) is orthochromatic and fast. Medical blue-sensitive film (older type, some still available as NDT/industrial film) is slower. Direct-exposure X-ray film (no screen required, used for dental or industrial NDT) is slower still (~ISO 25–100) and better suited to this application because it is designed for direct light exposure rather than screen fluorescence.

**Source for ISO figures:** Renner, E., *Pinhole Photography*, 4th ed., Focal Press, 2009 (x-ray film in pinhole cameras discussed); practitioner documentation on Photrio.com (multiple threads on x-ray film pinhole photography, 2018–2024). Specific product ISOs vary; verify against the manufacturer data sheet of the specific film procured.

The critical additions beyond the earlier analysis:

- **Double emulsion halation** is most visible in natural light against bright backgrounds — window frames, sky at horizon, sun-lit white walls. Plan compositions to avoid sharp bright/dark transitions.
- **High inherent contrast** (gamma ~2.5–3.5) means highlights compress quickly. For portraiture in direct sun, the face will be two-dimensional unless the light is soft and diffuse (overcast, open shade, or north-facing light).
- **The speed advantage** (ISO 400–800) significantly outweighs the spectral and contrast disadvantages for practical operation: 5–10 minute exposures vs. 40+ minutes mean far lower risk of subject movement blur and camera vibration during exposure.

---

<!-- brochure:endskip -->

### Appendix A Summary: Spectral Sensitivity and Speed Comparison

| Process | ISO equiv. | Exposure at f/1088 (full sun, corrected) | UV | Blue | Green | Red | Portrait skin rendering |
|---|---|---|---|---|---|---|---|
| Gum bichromate | ~0.25–0.5 | **8–17 hours — impractical** | ✓ | ✓ (short) | ✗ | ✗ | Flat — mitigated by warm pigment |
| Cyanotype (Herschel) | ~1–2 | 2–4 hours | ✓ | ✓ (short) | ✗ | ✗ | Flat, dark, pallid |
| **Cyanotype (Ware) ★** | **~2–4** | **30–45 min** | ✓ | ✓ (short) | ✗ | ✗ | Flat, dark, pallid |
| Salt print | ~1–3 | 1.5–4 hours | ✓ | ✓ | ✗ | ✗ | Flat, notably darker than expected |
| Van Dyke Brown | ~2–6 | 45 min–2 hours | ✓ | ✓ | ✗ | ✗ | Flat, slightly better mid-tone scale than salt |
| **Ilford Multigrade RC** | **~6** | **~43 min** | ✓ | ✓ | **✓** | ✗ | **Best of non-film options — natural mid-tones** |
| Liquid Light | ~6–12 | 20–43 min | ✓ | ✓ | ✗ (limited) | ✗ | Similar to salt print — graphic, high contrast |
| X-ray film (blue-sensitive) | ~50–200 | 2–10 min | ✓ | ✓ | ✗ | ✗ | Flat and pallid, like UV-only processes |
| X-ray film (orthochromatic) | ~200–800 | **20 sec–2 min** | ✓ | ✓ | ✓ | ✗ | Similar to Ilford paper — natural mid-tones |
| Panchromatic film | ~100–400 | 1–5 min | ✓ | ✓ | ✓ | ✓ | Full tonal fidelity — cost outlier |

#### Dual Ranking for Outdoor Portrait Work

**By tonal fidelity (how natural a face looks):**

1. Panchromatic film — full spectrum; not practical at this scale
2. Ilford Multigrade RC paper / Orthochromatic X-ray film — tied; blue + green; reds absent but skin otherwise natural
3. Van Dyke Brown — UV/blue only, but longest tonal scale of the iron processes
4. Salt print — UV/blue, compressed scale, warm tone
5. Liquid Light — UV/blue, high contrast, graphic
6. Cyanotype — UV/blue, flat; well-loved aesthetic quality
7. Gum bichromate — UV/blue, flat; partially offset by warm pigment choice

**By practical operability at f/1088 (shorter exposure = more reliable result):**

1. Orthochromatic X-ray film (ISO 200–800) — 20 sec–2 min; subject can hold still; vibration not an issue
2. Ilford Multigrade RC paper (ISO 6) — 43 min; borderline for a standing subject in still air
3. Liquid Light (ISO 6–12) — 20–43 min
4. Van Dyke Brown (ISO 2–6) — 45 min–2 hours; requires cooperative conditions
5. **Cyanotype Ware formula (ISO 2–4) — 30–45 min; viable across most seasons in good sun ★ selected**
6. Cyanotype Herschel (ISO 1–2) — 2–4 hours; requires exceptional UV conditions
7. Salt print (ISO 1–3) — 1.5–4 hours; at limit of practical outdoor portraiture
8. Gum bichromate (ISO 0.25–0.5) — 8–17 hours; **not viable for in-camera portraiture at f/1088**

**Practical recommendation:** The intersection of tonal quality and practical operability points clearly to **Ilford Multigrade RC paper** as the primary medium. At ISO 6, 43-minute exposures are achievable in practice with a cooperative subject and calm conditions. For situations where exposure time is the binding constraint (wind, moving subjects, overcast days reducing available UV), **orthochromatic X-ray film** is the correct solution — the spectral response is equivalent to Ilford paper, the tonal rendering is similar, and the 30:1 speed advantage transforms the operational logistics entirely.

---

## Sources

| Source | Relevance |
|---|---|
| Herschel, J.F.W., *Phil. Trans. Royal Society*, 1842. [NASA ADS](https://ui.adsabs.harvard.edu/abs/1842RSPT..132..181H) | Original cyanotype chemistry |
| Ware, M., *Cyanotype*, Science Museum UK, 1999. [mikeware.co.uk](https://www.mikeware.co.uk/mikeware/New_Cyanotype_Process.html) | Improved formula; technical analysis |
| Getty Conservation Institute, *Atlas of Cyanotype*, 2013. [getty.edu](https://www.getty.edu/conservation/publications_resources/pdf_publications/atlas.html) | Archival properties and stability data |
| Crawford, W., *The Keepers of Light*, Morgan & Morgan, 1979. [Catalog](https://openlibrary.org/search?q=Crawford+Keepers+of+Light) | Van Dyke, salt print, gum bichromate formulae |
| Reilly, J.M., *The Albumen and Salted Paper Book*, Light Impressions, 1980. [Catalog](https://openlibrary.org/search?q=Reilly+Albumen+and+Salted+Paper) | Salt print technical data |
| Schaaf, L.J., *Out of the Shadows*, Yale University Press, 1992. [Catalog](https://openlibrary.org/search?q=Schaaf+Out+of+the+Shadows) | Talbot/salt print historical documentation |
| Rockland Colloid product data. [rockaloid.com](https://rockaloid.com/) | Liquid Light coverage and substrate compatibility |
| Ilford product pages. [ilfordphoto.com](https://www.ilfordphoto.com/photographic-paper) | RC paper roll formats, dimensions |
| Chem-Impex catalog. [chem-impex.com](https://www.chem-impex.com/) | Silver nitrate pricing (~$260.69/100g, 2026) |
| Photographers' Formulary. [photoformulary.com](https://stores.photoformulary.com/) | FAC pricing (~$14.95/100g, 2026); KFe pricing |
| "The Great Picture," Wikipedia. [en.wikipedia.org/wiki/The_Great_Picture](https://en.wikipedia.org/wiki/The_Great_Picture) | Precedent for muslin substrate at very large scale |
