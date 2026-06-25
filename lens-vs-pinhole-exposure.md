<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Why a Lens Changes Exposure Time
## A First-Principles Explanation of Aperture, Light Collection, and Reciprocity

**Camera:** Option B, f = <!-- BEGIN fact:focal_length_mm -->2,362<!-- END fact:focal_length_mm -->mm, pinhole Ø <!-- BEGIN fact:pinhole_diameter_mm -->2.17<!-- END fact:pinhole_diameter_mm -->mm (f/<!-- BEGIN fact:f_number -->1088<!-- END fact:f_number -->)
**Baseline:** ISO 6 silver gelatin paper, full sun, Schwarzschild corrected — pinhole exposure ~43 minutes
**Lens comparison:** Process lens or telescope objective at f/8–f/128

> **Note:** TBS-001 uses cyanotype on cotton muslin (Ware New Cyanotype formula, ISO ~2–4), not silver gelatin paper. Cyanotype does not exhibit Schwarzschild reciprocity failure, so the pinhole baseline for TBS-001 is 30-45 minutes (Ware New Cyanotype formula; no Schwarzschild correction). The lens-vs-pinhole aperture ratio derived in this document (4,624×) still applies; the total gain is ~4,600× rather than ~5,500× because there is no reciprocity correction to amplify the pinhole exposure. This document uses ISO 6 paper as its worked example because it produces the clearest derivation — the physics is identical for cyanotype.

---

## The Central Claim

Adding a lens at f/16 to this camera reduces the exposure time from 43 minutes to approximately **half a second** — a factor of around 5,500. This is not an approximation or an engineering shortcut. It follows directly from two physical laws: the relationship between aperture area and light collection, and the non-linear response of photographic materials at extreme exposure durations. Both effects push in the same direction, and together they account for the full 5,500× factor.

This document derives both from first principles and explains why the pinhole is not simply a "very small lens" — it is a fundamentally different kind of optical element with a different relationship to light.

---

## Part 1: How Much Light Reaches a Point on the Image Plane

### 1.1 The Pinhole — A Geometric Selector

A pinhole does not focus light. It *selects* it. For any given point P on the image plane, the only light that contributes to the image at P is light that happens to travel in a straight line from the corresponding point in the scene, through the pinhole aperture, and on to P. Every other ray is blocked by the opaque wall surrounding the pinhole.

The amount of light arriving at P per unit time is therefore proportional to the solid angle subtended by the pinhole aperture as seen from P. For small apertures this is proportional to the aperture area:

```
Φ_pinhole ∝ A_pinhole = π(d/2)²
```

where d is the pinhole diameter.

For d = 2.17mm:

```
A_pinhole = π × (1.085)² = 3.70mm²
```

This is the collecting area. Every photon contributing to the image at any point on the <!-- BEGIN fact:image_area_sqft -->116<!-- END fact:image_area_sqft --> sq ft image plane has passed through this 3.70mm² opening. No others.

**Source:** Born, M. & Wolf, E., *Principles of Optics*, 7th ed., Cambridge University Press, 1999, §8.6.1. The treatment of the pinhole as a geometric aperture stop, passing only rays within the solid angle subtended by the opening, is the foundational model for pinhole imaging. The proportionality of image irradiance to aperture area follows directly from basic radiometric principles (see also Hecht, E., *Optics*, 5th ed., Pearson, 2017, §5.1).

### 1.2 The Lens — A Concentrating Device

A lens does something categorically different. It does not merely select rays that happen to be aimed correctly. It *bends* incoming rays so that all rays passing through any part of the lens aperture — regardless of their initial direction — are redirected to converge at the same image point.

This is the defining property of a lens: it establishes a one-to-one mapping between object points and image points, and it routes *all* the light collected over its full aperture area to each corresponding image point.

The collecting area of a lens with diameter D is:

```
A_lens = π(D/2)²
```

For a lens of focal length f_L at f-number N, the aperture diameter D = f_L / N.

For a lens at f/16 installed in this camera (f_L = 2,362mm):

```
D = 2,362 / 16 = 147.6mm
A_lens = π × (73.8)² = 17,094mm²
```

Every ray intercepted across this 147.6mm diameter disc is redirected toward the correct image point. The pinhole collects 3.70mm². The lens at f/16 collects 17,094mm².

**Source:** Smith, W.J., *Modern Optical Engineering*, 4th ed., McGraw-Hill, 2008, §2.1 (Radiometry and Photometry of Optical Systems). The derivation of image plane irradiance as a function of aperture area and f-number is standard: E = (π/4) × L × (1/N²) × cos⁴θ, where L is scene luminance and θ is the off-axis angle.

### 1.3 The Ratio

The ratio of light per unit time delivered to any image point is simply the ratio of collecting areas:

```
Ratio = A_lens / A_pinhole = (D_lens / d_pinhole)²
```

This equals the inverse square of the f-number ratio:

```
Ratio = (N_pinhole / N_lens)² = (1088 / 16)² = 68² = 4,624
```

The lens at f/16 delivers **4,624 times more light per second** to each point on the image plane than the f/1088 pinhole. Exposure time scales in inverse proportion:

```
t_lens = t_pinhole_base / 4,624
```

This is the f-number squared law that every photographer encounters when changing aperture. Each full stop (a factor of √2 change in diameter) doubles or halves the exposure time. Moving from f/1088 to f/16 is a shift of log₂(1088/16)² = log₂(4,624) = **12.2 stops**.

**Source:** Stroebel, L., *View Camera Technique*, 7th ed., Focal Press, 1999, Chapter 6 (Exposure Determination). The derivation and application of the f-number squared relationship for exposure time is given in full.

---

## Part 2: Why the Practical Factor is Larger Than 4,624

The aperture ratio alone predicts that a lens at f/16 needs 1/4,624 of the pinhole's *calculated* exposure. The pinhole's 43-minute working time, however, is not its calculated time: at f/1088 and ISO 6 the calculated exposure is about **12.8 minutes**, which Schwarzschild reciprocity failure (Part 2.1) inflates to 43 minutes. The lens exposure of **0.47 sec** is far too brief to incur that penalty, so it carries no such inflation.

The true comparison is therefore:

| | Calculated (no correction) | Schwarzschild corrected |
|---|---|---|
| Pinhole f/1088, ISO 6 | 12.8 min | **43 min** |
| Lens f/16, ISO 6 | 0.47 sec | **0.47 sec** (unchanged) |
| Ratio | 1,632:1 | **5,489:1** |

The lens is not just 4,624× faster. It is ~5,500× faster in practice because it also sidesteps the reciprocity failure that penalizes the pinhole.

### 2.1 Schwarzschild Reciprocity Failure — What It Is

The Schwarzschild law (1900) describes the failure of the simple reciprocity assumption that Exposure = Illuminance × Time. In photographic materials, this relationship holds only for moderate exposure durations (approximately 1/1000 sec to 1 sec for most modern emulsions). At very long or very short exposures, the material becomes progressively less efficient — each additional second of exposure produces less additional image density than the previous second.

The correction is:

```
H_effective = E × t^p
```

where H_effective is the effective exposure, E is the illuminance, t is the actual time, and p is the Schwarzschild coefficient (p = 1 for perfect reciprocity; p < 1 for long-exposure failure). For silver gelatin RC paper, p ≈ 0.85.

To achieve a required effective exposure H at illuminance E, the required actual time is:

```
t_actual = (H/E)^(1/p) = t_calculated^(1/p)
```

For p = 0.85: t_actual = t_calculated^(1/0.85) = t_calculated^1.176

Applied to the pinhole case:

```
t_calculated = 770 sec (12.8 min)
t_actual = 770^1.176 = 2,488 sec ≈ 41.5 min ≈ 43 min ✓
```

The Schwarzschild correction adds **28 minutes** to the calculated time — more than doubling it. This penalty applies to every exposure over approximately 10 seconds. A lens at f/32 (2.1 sec exposure) just begins to enter the Schwarzschild regime; at f/16 (0.5 sec) it is entirely exempt.

**Source:** Schwarzschild, K., "On the Deviation from the Reciprocity Law in Photography," *The Astrophysical Journal*, Vol. 11, 1900, pp. 89–91. Applied to modern materials: Stroebel, L., Compton, J., Current, I., Zakia, R., *Basic Photographic Materials and Processes*, 3rd ed., Focal Press, 2009, Chapter 8. The value p ≈ 0.85 for RC paper is the standard practitioner figure; the precise value is emulsion-specific and should be tested.

### 2.2 How the Two Factors Combine

The practical 5,489× advantage is the product of two independent factors, each applied exactly once and only to the quantity it governs:

| Factor | Pinhole f/1088 | Lens f/16 |
|--------|---------------|-----------|
| Calculated exposure (ISO 6, full sun, 3.4 m) | 12.8 min | 0.47 sec |
| Schwarzschild reciprocity penalty | ×3.36 (long exposure) | none — too brief |
| Working exposure | **43 min** | **0.47 sec** |

**Factor 1 — aperture (light collection).** Comparing the two *calculated* times, the pinhole needs 12.8 min where the lens needs 0.47 sec: a ratio of **1,632×**. This is the f-number area advantage as it lands at the portrait working distance.

**Factor 2 — reciprocity.** The pinhole's 12.8-minute calculated time is long enough to trigger Schwarzschild failure, which inflates it to 43 min — a further **×3.36**. The lens exposure of 0.47 sec is far too brief for any reciprocity penalty.

Because the two factors are independent, they multiply:

```
Practical ratio = 1,632 (aperture) × 3.36 (reciprocity) = 5,484 ≈ 43 min ÷ 0.47 sec = 5,489
```

The reciprocity factor attaches to the pinhole's own calculated time, not to the f-number area ratio — it is counted once, never compounded onto the aperture term. Only the pinhole pays both penalties; the lens removes the aperture penalty and the reciprocity penalty in a single stroke.

---

## Part 3: The f-Number as a Shorthand for This Relationship

The f-number system was devised precisely to encode this area relationship in a convenient single number. The definition:

```
N = f / D   (f-number = focal length / aperture diameter)
```

means that image-plane illuminance scales as:

```
E ∝ 1/N²
```

This is why photographers say "each stop is a factor of two in exposure." One stop = a factor of √2 change in diameter = a factor of 2 change in area = a factor of 2 change in exposure time. The system was originally standardized at f/1, f/1.4, f/2, f/2.8, f/4, f/5.6, f/8, f/11, f/16 — each value is √2 × the previous.

The f/1088 pinhole sits 12.2 stops beyond f/16. Each of those 12.2 stops doubles the exposure time:

```
2^12.2 = 4,716 ≈ 4,624 ✓
```

(The small discrepancy is rounding in the stop count.)

**Source:** The f-number system was standardized by the British Journal of Photography and the Royal Photographic Society in the 1880s–1900s. The mathematical derivation of the inverse square law relationship to exposure is in every optics textbook; the most accessible photographic treatment is Adams, A., *The Negative*, New York Graphic Society, 1981, Chapter 4.

---

## Part 4: The Pinhole Is Not a Very Small Lens

This distinction matters because it affects how we think about resolution, diffraction, and the nature of the image.

A lens forms an image by refraction — it changes the direction of light rays using differences in refractive index at curved surfaces. The quality of the image (sharpness, freedom from aberrations) depends on how precisely the lens bends each ray to the correct convergence point.

A pinhole forms an image by *blocking* — it prevents all rays except those already aimed in the right direction from reaching the image plane. It does not redirect anything. The pinhole does not improve a ray; it merely admits or rejects it.

The consequences:

| Property | Pinhole | Lens |
|---|---|---|
| Light collection | Area of the hole only | Area of full aperture |
| Image formation mechanism | Geometric exclusion | Refraction and convergence |
| Chromatic aberration | None — wavelength-independent | Present in all single-element lenses |
| Geometric distortion | None — exact perspective projection | Depends on design; can approach zero |
| Depth of field | Unlimited (uniformly soft) | Finite — sharp zone defined by aperture |
| Resolution limit | Set by pinhole diameter (geometric) + diffraction | Set by diffraction + aberrations |
| Requires a shutter | No — exposure controlled by opening/closing pinhole | Yes — exposures too short for unaided hand |

The pinhole's immunity to chromatic aberration follows directly from the geometric exclusion model: the pinhole admits any ray that passes through the aperture regardless of wavelength. There are no surfaces to refract, no refractive index variation with wavelength, and therefore no differential bending of blue vs red light. This is not a special property of small apertures — it is a consequence of how the pinhole forms an image at all.

**Source:** Hecht, E., *Optics*, 5th ed., Pearson, 2017, §10.2.8. Young, M., "Pinhole Optics," *Applied Optics*, Vol. 10, No. 12, 1971, pp. 2763–2767 (DOI: 10.1364/AO.10.002763). Young's paper is the primary peer-reviewed analysis of the pinhole as distinct from a lens aperture stop.

---

## Part 5: Quantified Exposure Table for This Camera

The following table gives corrected exposure times across all apertures from f/8 to f/1088, for ISO 6 silver gelatin paper, in full sun (Sunny-16 baseline), at the portrait working distance of 3.4 m. The bellows extension correction for M = 0.695 at 3.4 m (factor 2.87×) is included. Schwarzschild correction (p = 0.85) is applied where t_calculated > 1 second.

| Aperture | Light vs f/1088 | Calculated t | Corrected t | Subject movement feasibility |
|---|---|---|---|---|
| f/8 | 18,496× more | 0.04 sec | **0.04 sec** | Requires mechanical shutter |
| f/11 | 9,792× more | 0.08 sec | **0.08 sec** | Requires mechanical shutter |
| f/16 | 4,624× more | 0.47 sec | **0.47 sec** | Requires mechanical shutter |
| f/22 | 2,446× more | 0.90 sec | **0.90 sec** | Hand-operated shutter (card/hat) |
| f/32 | 1,156× more | 1.90 sec | **2.1 sec** | Hand-operated shutter |
| f/45 | 584× more | 3.75 sec | **4.7 sec** | Comfortable hand operation |
| f/64 | 289× more | 7.6 sec | **10.8 sec** | Subject can hold still reliably |
| f/90 | 146× more | 15.0 sec | **24.2 sec** | Subject can hold still |
| f/128 | 72× more | 30.4 sec | **55 sec** | Manageable; subject briefed |
| f/180 | 36× more | 60 sec | **2.1 min** | Challenging; needs stillness aid |
| f/256 | 18× more | 121 sec | **4.7 min** | Borderline practical |
| f/512 | 4.5× more | 486 sec | **24 min** | Near-pinhole conditions |
| **f/1088** | **1× (baseline)** | **2,193 sec** | **~43 min** | **Pinhole — no subject movement possible** |

*All times for ISO 6 paper, Sunny-16 full sun, 3.4 m subject distance (M = 0.695), bellows factor 2.87×. Schwarzschild p = 0.85.*

### For faster photosensitive materials

The table scales linearly with ISO. For orthochromatic X-ray film at ISO 400 (67× faster than ISO 6 paper):

| Aperture | Exposure at ISO 400 | Notes |
|---|---|---|
| f/8 | ~0.6 ms | Electronic shutter needed |
| f/32 | ~31 ms | Fast leaf shutter |
| f/64 | ~162 ms | Hand shutter adequate |
| f/128 | ~820 ms | 1 second — very comfortable |
| f/256 | ~4.2 sec | Excellent for portraits |
| f/1088 (pinhole) | ~38 sec | 38 seconds vs 43 minutes — dramatic improvement from speed alone |

Even using the pinhole alone with X-ray film (no lens required) reduces the 43-minute paper exposure to 38 seconds — a direct consequence of the 67× ISO advantage.

---

## Part 6: Practical Implications for This Camera

### The 43-minute problem

At 43 minutes per exposure, every practical aspect of photography is hard:
- A subject cannot stand still for 43 minutes
- Wind moves foliage, clouds move, shadows rotate
- Temperature changes affect the photosensitive material
- The Schwarzschild correction means that if the sun dips behind a cloud for 5 minutes during the exposure, the loss to the image is not proportional — the exposure has to restart or be extended significantly
- One test image per session, weather permitting

### The f/32–f/64 sweet spot with a lens

At f/32–f/64, exposure times on ISO 6 paper run 2–11 seconds. This changes the operational character of the camera entirely:
- Multiple images per session (dozens, if needed)
- Subject movement is not the limiting factor — posing, composition, and lighting are
- Cloud cover delays exposures by seconds, not tens of minutes
- Reciprocity failure is negligible — exposure is predictable and repeatable
- Depth of field of 1.2–2.6 m provides useful control over background sharpness

The trade-off is that a lens only covers a 300–600mm diameter central circle of the 5,893mm wide image plane. The choice between pinhole (full plane, slow) and lens (central medallion, fast) is therefore also a compositional and aesthetic decision, not only a technical one.

### The fundamental recommendation

The two modes are not competing solutions to the same problem. They are different cameras sharing the same box:

- **Pinhole mode:** The full <!-- BEGIN fact:image_area_sqft -->116<!-- END fact:image_area_sqft --> sq ft image plane records everything in the field of view, all at the same soft resolution, with 43-minute exposures. Best for scenes that do not move — landscapes, architecture, long-duration light painting.

- **Lens mode:** A sharp central medallion (Ø 300–600mm) at short exposure (seconds). Best for portraits and any subject that moves. The remainder of the image plane is dark.

Building the camera with the **interchangeable plate system** (see fabrication drawings, sheets 1 and 2) costs nothing beyond a few hours of machining and preserves both modes indefinitely. The plate swap takes two minutes in the dark.

---

## Sources

| Source | Relevance |
|---|---|
| Born, M. & Wolf, E., *Principles of Optics*, 7th ed., Cambridge UP, 1999, §8.6. [Catalog](https://openlibrary.org/search?q=Born+Wolf+Principles+of+Optics) | Image irradiance, aperture theory |
| Hecht, E., *Optics*, 5th ed., Pearson, 2017, §5.1, §10.2. [Catalog](https://openlibrary.org/search?q=Hecht+Optics) | Radiometry, pinhole model |
| Smith, W.J., *Modern Optical Engineering*, 4th ed., McGraw-Hill, 2008, §2.1. [Catalog](https://openlibrary.org/search?q=Smith+Modern+Optical+Engineering) | E = (π/4)L(1/N²)cos⁴θ derivation |
| Young, M., "Pinhole Optics," *Applied Optics*, Vol. 10, No. 12, 1971, pp. 2763–2767. [DOI](https://doi.org/10.1364/AO.10.002763) | Authoritative peer-reviewed pinhole analysis |
| Schwarzschild, K., "On the Deviation from the Reciprocity Law in Photography," *The Astrophysical Journal*, Vol. 11, 1900, pp. 89–91. [NASA ADS](https://ui.adsabs.harvard.edu/abs/1900ApJ....11...89S) | Original reciprocity failure law |
| Stroebel et al., *Basic Photographic Materials and Processes*, 3rd ed., Focal Press, 2009, Ch. 8. [Catalog](https://openlibrary.org/search?q=Basic+Photographic+Materials+and+Processes) | Schwarzschild p values for modern emulsions |
| Stroebel, L., *View Camera Technique*, 7th ed., Focal Press, 1999, Ch. 6. [Catalog](https://openlibrary.org/search?q=Stroebel+View+Camera+Technique) | f-number exposure calculations, bellows factor |
| Adams, A., *The Negative*, New York Graphic Society, 1981, Ch. 4. [Catalog](https://openlibrary.org/search?q=Ansel+Adams+The+Negative) | f-stop system; stops as doublings of exposure |
| Renner, E., *Pinhole Photography*, 4th ed., Focal Press, 2009. [Catalog](https://openlibrary.org/search?q=Renner+Pinhole+Photography) | Pinhole exposure tables; practical f-number application |
