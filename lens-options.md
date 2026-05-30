<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Lens Options
## A Technical Analysis of Image Quality, Depth of Field, and Exposure Impact

**Camera configuration:** Option B (side-to-side), container interior depth f = 2362mm  
**Image plane (active):** 4499 × 2388mm (~14′ 9″ × 7′ 10″); container interior 5893 × 2388mm  
**Current pinhole:** Ø 2.17mm, f/1088  
**Baseline exposure (Ware New Cyanotype on muslin, f/1088, full sun — no reciprocity correction):** ~30–45 min

---

## The Fundamental Problem

Before specifying any lens, one geometric fact must be understood: **no commercially available photographic lens covers the full 5893 × 2388mm image plane.** The image circle required to cover this format fully is 6358mm in diameter. For comparison, the largest format commonly served by photographic lenses is 8×10 inch (203 × 254mm, diagonal 325mm). Our image plane diagonal is **20 times larger**.

This does not mean a lens is useless here. It means the lens choice determines *which portion* of the image plane receives focused, optically sharp light. The decision matrix is:

| Approach | Image area covered | Quality | Practical availability |
|---|---|---|---|
| Large-format process lens | Central circle, Ø 300–600mm | Excellent within circle | Commercial (used market) |
| Telescope objective (achromat) | Central circle, Ø 100–300mm | Very good within circle | Commercial, new and used |
| Custom single-element optic | Up to full coverage | Moderate — significant aberrations | Custom fabrication |
| Large Fresnel lens | Full or partial coverage | Low — artistic/aberrant character | Commercial (lighting/solar industry) |
| Hybrid: lens + pinholes | Central sharp + full-plane soft | Intentionally mixed | DIY |

Each is analyzed in detail below. All share a common optical framework.

---

## Section 1: The Optics — Specifying a Lens for This Camera

### 1.1 Thin Lens Equation and Focus Distance

The image plane is fixed at 2362mm from the lens position (the pinhole wall). Using the thin lens equation:

```
1/f_L = 1/d_i + 1/d_o
```

Where d_i = 2362mm (fixed), d_o = subject distance, f_L = lens focal length.

Solving for d_o: **d_o = d_i × f_L / (d_i − f_L)**

| Lens focal length (f_L) | Sharp focus distance |
|---|---|
| 1200mm | 2.4 m |
| 1321mm | **3.0 m** |
| 1400mm | 3.4 m |
| 1500mm | 4.1 m |
| 1604mm | **5.0 m** |
| 1800mm | 7.6 m |
| 2000mm | 13.1 m |
| 2362mm | ∞ (infinity) |

**For portrait work at 3–5 m: the required lens focal length is 1300–1600mm.** This is the working specification. No standard photographic lens, enlarger lens, or projector lens operates in this focal length range at the diameters needed for this camera. The sources that do are discussed under each option below.

### 1.2 Adjustable Focus: The Lens Board

A lens mounted rigidly in the pinhole wall can only focus at one fixed distance (set by its focal length). To focus at different distances, the lens is mounted on a sliding board — a simple wooden or aluminum panel that moves forward and backward in the wall aperture, exactly as a view camera bellows extends and contracts.

Moving the lens 1mm toward the subject (increasing d_i by 1mm) shifts focus significantly closer. The sensitivity:

```
Δd_o / Δd_i = −(d_o / d_i)² = −(d_o / 2,362)²
```

At 3.4 m subject distance (d_o = 3438mm): moving the lens 1mm toward subject shifts focus by −(3,438/2,362)² = −2.12 m. Focus is extremely sensitive to lens position at these distances. A fine-thread adjustment screw is essential.

### 1.3 Magnification

**Adding a lens does not change image magnification.** Magnification depends only on image distance and object distance:

```
M = d_i / d_o = 2,362 / d_o
```

This is identical to the pinhole case. A subject at 3.4 m produces an image 0.687× their actual size, regardless of whether the camera uses a pinhole or a lens. The lens determines *sharpness*; geometry determines *size*.

| Subject distance | Magnification | Image height of 1780mm person |
|---|---|---|
| 2.0 m | 1.18× | 2102mm (larger than life) |
| 2.4 m | 0.98× | 1752mm (near life-size) |
| 3.0 m | 0.79× | 1401mm |
| 3.4 m | 0.69× | 1237mm |
| 5.0 m | 0.47× | 841mm |
| 7.6 m | 0.31× | 553mm |
| 10.0 m | 0.24× | 420mm |

### 1.4 Bellows Extension Factor

At portrait distances, the lens-to-image-plane distance (2362mm) is comparable in magnitude to the object distance. This ratio matters for exposure: the closer the subject, the more the effective f-number increases relative to the lens's rated value.

```
Effective f-number = rated f-number × (1 + M)
Exposure correction factor = (1 + M)²
```

| Subject distance | Magnification M | Bellows factor (1+M)² | Exposure increase |
|---|---|---|---|
| 3.0 m | 0.787 | 3.20× | +1.7 stops |
| 3.4 m | 0.695 | 2.87× | +1.5 stops |
| 5.0 m | 0.472 | 2.17× | +1.1 stops |
| 7.6 m | 0.311 | 1.72× | +0.8 stops |
| ∞ | 0 | 1.00× | 0 stops |

A lens rated f/16 at portrait distance (3.4 m) has an effective f-number of f/16 × 1.695 = f/27. All exposure calculations below include this correction.

---

## Section 2: Impact on Exposure Time

The improvement over the pinhole is the most operationally significant quality of any lens. The pinhole at f/1088 requires 43 corrected minutes on ISO 6 paper in full sun. A lens of any practical aperture reduces this to seconds or fractions of a second.

Baseline: Sunny-16 at ISO 6 = 1/6 second at f/16. All times below include bellows extension correction for a subject at 3.4 m (factor 2.87×) and Schwarzschild reciprocity correction (p = 0.85) where applicable.

| Aperture | Effective f-number (3.4m) | Calculated t | Corrected t | Practical description |
|---|---|---|---|---|
| f/8 | f/13.6 | 0.12 sec | **0.12 sec** | Shutter-speed territory — requires a shutter |
| f/11 | f/18.7 | 0.22 sec | **0.22 sec** | Requires a shutter |
| f/16 | f/27.2 | 0.47 sec | **0.47 sec** | Requires a shutter |
| f/22 | f/37.3 | 0.90 sec | **0.90 sec** | Hand-operated shutter (hat/card) just possible |
| f/32 | f/54.3 | 1.90 sec | **2.1 sec** | Hand-operated shutter |
| f/45 | f/76.4 | 3.75 sec | **4.7 sec** | Hand-operated shutter, comfortable |
| f/64 | f/108.5 | 7.6 sec | **10.8 sec** | Comfortable hand operation |
| f/128 | f/217 | 30.4 sec | **55 sec** | Manageable for standing subject |
| f/256 | f/434 | 121 sec | **4.7 min** | Getting difficult; approaches pinhole aesthetics |
| f/512 | f/869 | 486 sec | **24 min** | Near-pinhole behavior |
| f/1088 | f/1844 | 2,193 sec | **~2.4 hr** | Pinhole equivalent (extremely stopped-down lens) |

**Key threshold:** At f/32–f/64, exposures of 2–11 seconds allow subjects to stand still reliably. At f/8–f/22, a mechanical shutter is required — easily fabricated as a sliding black panel operated by hand.

**ISO 6 is the binding constraint.** All times above are for silver gelatin paper or equivalent. For orthochromatic X-ray film at ISO 400 (66× faster), multiply all times by 1/66 — reducing a 10-second exposure to 0.15 seconds, and a 4.7-minute exposure to 4 seconds.

---

## Section 3: Depth of Field

With a pinhole, depth of field is effectively unlimited — the blur circle grows slowly with distance from the optimum, and the variation is small compared to the pinhole's already-modest resolution. With a lens, depth of field is sharply defined and depends on aperture.

The following uses:
- f_L = 1400mm (focused at 3.44 m)
- Circle of confusion c = 3mm (appropriate for a 4499mm wide active image viewed from 5–7 m)
- Hyperfocal distance H = f_L² / (N × c)

| Aperture | Hyperfocal dist. | Near limit | Far limit | DoF span | Portrait suitability |
|---|---|---|---|---|---|
| f/8 | 81.7 m | 3.30 m | 3.59 m | **0.29 m** | Group must be in a single plane |
| f/11 | 59.4 m | 3.25 m | 3.65 m | 0.40 m | Tight — single row, still subject |
| f/16 | 40.8 m | 3.17 m | 3.75 m | 0.58 m | Acceptable for single subject |
| f/22 | 29.7 m | 3.08 m | 3.89 m | 0.81 m | Good for single portrait |
| f/32 | 20.4 m | 2.94 m | 4.13 m | 1.19 m | **Good — small group** |
| f/45 | 14.5 m | 2.78 m | 4.50 m | 1.72 m | Small group, moderate depth |
| f/64 | 10.2 m | 2.57 m | 5.18 m | **2.61 m** | Excellent — full group in depth |
| f/128 | 5.1 m | 2.05 m | 10.53 m | 8.48 m | Very deep — near-pinhole DoF |

**Working aperture recommendation for portraiture: f/32–f/64.** This range gives 1.2–2.6 m of depth (enough for a group of people standing at varying distances from the camera), with exposure times of 2–11 seconds that subjects can hold without assistance.

**The f/8–f/22 range** is appropriate for a single subject in a controlled studio-style setup where precise placement is possible. The extremely shallow depth of field at f/8 (29 cm) would throw background and any secondary subjects sharply out of focus — a dramatic aesthetic, but unforgiving of focus errors.

---

## Section 4: Image Sharpness

### 4.1 Theoretical Limit

| System | Blur disk size | Resolution (theoretical) | Notes |
|---|---|---|---|
| Pinhole (f/1088) | 2.17mm geometric | ~0.23 lp/mm | Diffraction-limited |
| Lens f/8 | 0.011mm Airy | ~47 lp/mm | Diffraction limit only |
| Lens f/16 | 0.021mm Airy | ~23 lp/mm | 100× better than pinhole |
| Lens f/32 | 0.043mm Airy | ~12 lp/mm | 50× better |
| Lens f/64 | 0.086mm Airy | ~6 lp/mm | 26× better |
| Lens f/128 | 0.172mm Airy | ~3 lp/mm | 13× better |
| Lens f/256 | 0.344mm Airy | ~1.5 lp/mm | 6× better |
| Lens f/512 | 0.688mm Airy | ~0.7 lp/mm | 3× better |

These are diffraction limits — the ceiling for any perfect lens. Real lenses fall below this due to aberrations. At f/8 a real-world large-format process lens might achieve 15–25 lp/mm (still 65–110× better than the pinhole). Even a mediocre singlet at f/8 would give 5–10 lp/mm, 20–43× better.

### 4.2 What the Improvement Looks Like on a 4499mm Wide Active Image

The pinhole resolves features of ~2.17mm on the image plane. At 3.4 m subject distance (M = 0.69), this corresponds to resolving features ~3.1mm in the subject — roughly the resolution needed to clearly see eyebrows, lips, and hair texture.

A lens at f/32 resolves ~0.043mm on the image plane — **50× finer**. At the same subject distance this resolves 0.062mm features. On an image viewed from 5 m, the pinhole is already acceptably sharp to the naked eye; the lens at f/32 would appear dramatically, noticeably sharper even at long viewing distances. Individual hairs, fabric texture, and skin pores would be rendered.

However: **sharpness is only real within the image circle of the lens** (see Section 5). Outside that circle, there is no image at all (or the image plane receives no light, or stray light only, depending on construction).

---

## Section 5: Lens Options — Specification, Coverage, and Character

### 5A: Large-Format Process / Repro Lens

These are the highest-quality option within their coverage area. Process lenses (Rodenstock Apo-Ronar, Schneider G-Claron, Nikkor AM-ED) were designed for the commercial printing industry to produce flat-field, low-distortion, high-resolution reproductions. They are optimized for the reproduction ratios (1:1 to 1:10) that coincide with portrait distances at this camera's scale.

**Commercially available examples:**

| Lens | Focal length | Max aperture | Image circle (@ infinity) | Typical used price |
|---|---|---|---|---|
| Rodenstock Apo-Ronar 1200mm | 1200mm | f/14 | ~400mm | $400–$1,200 |
| Nikkor T 1200mm f/11 | 1200mm | f/11 | ~450mm | $600–$1,500 |
| Schneider Apo-Symmar 800mm | 800mm | f/14 | ~500mm | $300–$800 |
| Rodenstock Apo-Ronar 600mm | 600mm | f/9 | ~350mm | $150–$400 |

**For this camera**, the most practical option is the **Rodenstock Apo-Ronar 1200mm or Nikkor T 1200mm** — both focus sharply near 2.4 m (d_i = 2362mm) with a single fixed lens. A 1400mm process lens (custom made or a rare large-format aerial lens) would focus at 3.4 m — more appropriate for portraits.

**What the image looks like:** A sharp circular disk in the centre of the photosensitive surface, approximately 400–500mm in diameter. The remaining ~4099mm width of the active image plane receives no light. The entire portrait must be composed within this central medallion.

**Coverage as percentage of image plane:** 400mm circle / 4499mm active width = **8.9% of image width**. The circular image is a small fraction of the ~116 sq ft active plane. The remainder of the plane is unexposed (black in the final image, or could be utilised by other means).

**Distortion:** Designed for <0.1% distortion across the image circle. Straight lines render straight. Essentially identical to pinhole geometry within the covered area.

**Chromatic aberration:** Apochromatic design (three-wavelength correction). Negligible colour fringing in normal use.

**Exposure at portrait distance (f/14 nominal, bellows factor 2.87):**
Effective f-number = f/14 × 1.695 = f/24
t = (1/6) × (24/16)² = (1/6) × 2.25 = 0.375 sec — a hand-operated shutter is practical.

---

### 5B: Telescope Achromat Objective

Telescope refractor objectives are commercially produced as high-quality achromatic doublets in the 80–200mm aperture range at focal lengths of 500–2000mm. They are designed to form sharp star images — the most demanding test of on-axis sharpness — and perform excellently as camera lenses on axis.

**Useful examples for this camera:**

| Optic | Focal length | Aperture | f-number | Image circle | Price (approx) |
|---|---|---|---|---|---|
| Sky-Watcher 120mm f/8.3 Doublet Apo | 1000mm | 120mm | f/8.3 | ~100–150mm | ~$700 |
| William Optics GT102 | 714mm | 102mm | f/7 | ~80–100mm | ~$900 |
| Explore Scientific ED127 | 952mm | 127mm | f/7.5 | ~120–150mm | ~$800 |
| Takahashi FSQ-130ED | 1000mm | 130mm | f/7.7 | ~180mm | ~$4,500 |
| Custom telescope doublet (150mm f/10) | 1500mm | 150mm | f/10 | ~200–250mm | ~$500–$2,000 (used) |

A 150mm aperture f/10 refractor objective at 1500mm focal length focuses at 5.0 m from the camera wall — ideal for portraits. It covers approximately 200–250mm image circle — still a small central medallion (200/4,499 = **4.4% of active image width**) but of extremely high quality.

These can be sourced as surplus telescope objectives from astronomy retailers (OPT Telescopes, High Point Scientific, Agena Astro) at prices that are far below commercial photographic process lenses of similar quality.

**Key advantage:** Designed for visual and photographic use; straightforward to mount. The objective lens sits in its tube; the tube can be mounted directly in the camera wall with appropriate flanges.

**Distortion:** Minimal — telescope objectives are designed for accurate star-field astrometry, which requires very low geometric distortion. Performance is excellent.

**Chromatic aberration:** Achromatic doublet = corrected for two wavelengths. Residual secondary spectrum. Apochromatic triplet (ED glass) = corrected for three wavelengths, essentially invisible CA. APO models cost more but are recommended for portrait work where skin tone rendering matters.

---

### 5C: Fresnel Lens — Full Coverage, Aberrant Character

Large Fresnel lenses are the only commercially available single elements that could physically cover the full image plane. Fresnel lenses are flat optical elements embossed with concentric prism rings that approximate the focusing power of a conventional curved lens. They are used in overhead projectors, solar concentrators, lighthouse optics, and large theatrical lighting.

**Available specifications:**

| Source / product | Aperture | Focal length | Price |
|---|---|---|---|
| Anchor Optics / Edmund Optics (acrylic) | 280mm × 280mm | 500–2500mm | $40–$200 |
| Plastic focal lens (solar/Fresnel) | 600mm × 600mm | 700–1500mm | $30–$80 |
| Fresnel Technologies surplus acrylic | Up to 1200mm × 900mm | Custom | $200–$500 |
| Glass Fresnel (lighthouse type, antique) | 500–1000mm dia | 300–1000mm | $500–$5,000 |

For this camera: a 600 × 600mm Fresnel lens at 1400mm focal length would cover a 600mm square within the 4499 × 2388mm active image plane — still not full coverage, but significantly more than a process lens. Stacking two side by side (600 × 600mm each) in a 1200 × 600mm assembly would cover about **27% of the active image width**.

A full-width solution would require a 4499 × 2388mm Fresnel element — this does not exist commercially. Custom mylar Fresnel film exists in large formats (used in projection screens) but at extremely low optical quality.

**Optical qualities of Fresnel lenses:**

1. **Chromatic aberration — severe.** A single-element Fresnel has no colour correction. The focal point for blue light is shorter than for red by approximately f_L / V where V = Abbe number of acrylic (~57): Δf = 1,400 / 57 ≈ 25mm. Visible as colour fringing — a rainbow halo on high-contrast edges, most prominent at the image periphery. On silver gelatin paper (blue/green sensitive), this manifests as softer blue channel focus vs. green, producing a slightly warm-tinted blur. On panchromatic film, coloured fringes would be fully visible.

2. **Zone diffraction artifacts.** The stepped Fresnel ring structure creates diffraction rings around point sources. In a portrait, this appears as a soft halo or glow around specular highlights (eyes, jewellery, white clothing). Can be aesthetically pleasant or distracting.

3. **Edge image quality.** Fresnel lenses perform best on-axis and deteriorate rapidly toward the edges due to zone spacing errors and oblique incidence effects. A 600mm Fresnel covering a 600mm field: the centre 200mm may be acceptable; the outer zone will be softer and more aberrant.

4. **Scatter and flare.** The stepped surface scatters more light than a smooth lens, reducing contrast and producing a slight veiling flare across the image. Characteristic of the aesthetic.

**Aesthetic character:** A Fresnel lens portrait would have a soft, glowing, impressionistic quality — sharp in the centre, dissolving to aberrant chromatic softness toward the edges, with subtle diffraction haloes. This is a strong, distinctive look — reminiscent of early 20th-century soft-focus portrait lenses or Pictorialist photography. Whether it is desirable is an artistic decision, not a technical one.

**Exposure:** At a Fresnel lens aperture of f/7 (600mm lens / ~85mm working aperture at f/7):
Effective at 3.4 m: f/7 × 1.695 = f/12
t = (1/6) × (12/16)² = 0.047 sec ≈ 1/21 sec — requires a mechanical shutter.

---

### 5D: Custom Single-Element Optic

A biconvex or plano-convex glass or acrylic lens of approximately 1400mm focal length can be custom-fabricated by specialist optical workshops. This is the route for larger image coverage with more controlled quality than a Fresnel.

**Specification for a custom singlet covering ~1000mm image circle:**

For crown glass (n = 1.52), a symmetric biconvex lens with equal radii:
- Focal length 1400mm → radius of curvature each surface: R = 2(n−1)f = 2 × 0.52 × 1,400 = **1456mm**
- Aperture required: at f/16, d = 1,400/16 = 87.5mm. At f/8: 175mm.
- Physical diameter: 200–300mm is practical for fabrication; covers ~250–400mm image circle

**To cover the full 4499mm active image plane** as a single element, the lens would need to be at least 700mm in diameter — a single glass element of 0.7 metre diameter, 1.4 m focal length. This is within the realm of custom optics for scientific instruments but the cost is extreme ($30,000–$200,000+). Acrylic is cheaper to fabricate at large size but optically inferior.

**Realistic custom singlet:** A 200–300mm diameter, 1400mm focal length crown glass singlet is fabricatable by companies such as Optical Surfaces Ltd (UK), II-VI Optical Systems, or local optical fabrication shops. Cost: approximately **$2,000–$8,000** depending on surface quality specification. This covers a ~300–500mm circle.

**Aberrations of a singlet at f/8:**
- Spherical aberration: significant — a biconvex singlet at f/8 has a spherical aberration blur of approximately f_L × (d/f_L)³ / (8(n−1)) ≈ several mm. This degrades the image significantly.
- Stopping down to f/22–f/32 reduces spherical aberration dramatically; quality at f/32 is acceptable for portrait work.
- Chromatic aberration: same as Fresnel (~25mm longitudinal CA for crown glass). Achromatic doublet (cemented two-element) eliminates this; cost approximately 2–3× more than singlet.

---

## Section 6: The Field Geometry Problem — Why No Lens Covers the Full Plane Well

This is the fundamental optical constraint of this camera that no lens choice can fully resolve.

The active image plane is 4499 × 2388mm, centered on the pinhole (X=2399mm) — giving half-width 2250mm and half-height 1194mm. The distance from the lens to the center of the image plane is 2362mm. The distance from the lens to the active image plane corners and edges:

```
d_mid-width = √(2,362² + 2,250²) = 3262mm   [half-width of active plane]
d_corner    = √(2,362² + 2,250² + 1,194²) = 3474mm   [half-diagonal of active plane]
```

The corner is **1112mm further from the lens than the center.** The left/right mid-edge point is 3262mm from the lens (900mm further than center). This means:

**A lens focused on the center (d_i = 2362mm) is focused on a subject at ~3.4 m. At the left/right edges of the active image plane, the equivalent focused subject distance would be ~3.4 × (3,262/2,362) = 4.7 m. At the corners, ~3.4 × (3,474/2,362) = 5.0 m.**

This is not a focus error in the traditional sense — it is the geometric consequence of projecting a wide-angle perspective onto a flat plane. A person standing 3.4 m in front of the centre of the camera would be rendered sharply in the centre and soft in the corners, because at the corners the image plane is optically further from the lens. The only way to have the full image plane in sharp focus simultaneously would be:

1. Stop down to a very small aperture (deep depth of focus on the image side)
2. Curve the image plane to match the focal surface (discussed below)
3. Use a telephoto lens design that manages field curvature over this extreme angular range

**This is not a problem unique to adding a lens.** The cos⁴ illumination falloff and field geometry are intrinsic to the camera's 102° × 45° field of view. The pinhole avoids the focus problem entirely because its resolution is low enough that the field geometry doesn't create a *visible* focus variation — the centre and corners are both equally soft. A lens makes the focus variation visible precisely because it is sharp in the first place.

### 6.1 Illumination Falloff — cos⁴ Law

Both the pinhole and any lens suffer the same physical law: illumination falls as the fourth power of the cosine of the off-axis angle.

| Image position | Angle from axis | cos⁴ factor | Illumination vs. centre | Stops darker |
|---|---|---|---|---|
| Centre | 0° | 1.000 | 100% | 0 |
| Mid-height edge | 26.8° | 0.634 | 63% | 0.7 stops |
| Mid-width edge | 43.6° | 0.273 | 27% | 1.9 stops |
| Corner | 47.1° | 0.215 | 22% | 2.2 stops |

The corners of the active image plane receive 22% of the light falling on the center — approximately **2.2 stops less exposure**. This is present with the pinhole and with any lens; it is a property of the field angle, not the optical system. Because the active image plane (4499mm wide) is substantially narrower than the full container interior (5893mm), the field angle is less extreme than a full-container analysis would suggest — the corner penalty improves from ~3 stops (full container) to ~2.2 stops (active plane). The effect on the final image: a natural vignette, darkening from center to corners. At 35 minutes or at 2 seconds, the corner of the image is always about 2 stops darker than the center.

On silver gelatin paper, 2.2 stops of underexposure in the corners means the corner areas may not reach adequate density in a correctly-exposed center. Exposure must account for this — either the center will be slightly overexposed to ensure the corners have sufficient density, or the corners are accepted as darker (which, for a portrait centered in the frame, may be desirable — a natural vignette framing the subject).

### 6.2 The Curved Image Plane Option

If the photosensitive substrate is mounted on a concave backing panel curved to match the focal surface (a sphere of radius 2362mm centred on the lens), the field geometry problem is eliminated. Every point on the curved surface is equidistant from the lens. The image plane would need to curve forward (toward the lens) at the edges by approximately:

```
Δz at mid-width edge = 3,262 − 2,362 = 900mm
Δz at corner = 3,474 − 2,362 = 1112mm
```

This is still substantial curvature — the active image plane would bow forward at the sides by ~900mm. Constructing this with ACM panel is not feasible, but constructing it with fabric (canvas or muslin) stretched over a curved timber frame absolutely is. The curved frame would need to be CNC-machined or steam-bent to a precise 2362mm radius sphere section. Note: the bow is significantly more manageable than for a full-container-width image plane (which would require 1414mm of forward bow at the mid-width edge).

For a process lens or telescope objective (covering only a 300–600mm circle in the centre), this is irrelevant — the field curvature is only noticeable at extreme field angles beyond the lens's image circle. Only relevant if full-field coverage is attempted with a large Fresnel or custom element.

---

## Section 7: Distortion

**Pinhole:** Zero geometric distortion by definition. The pinhole is a mathematical point and projects a perfect central perspective. Straight lines in the subject are rendered as straight lines in the image. This is a significant aesthetic quality of pinhole photography.

**Lens distortion depends on design:**

| Lens type | Distortion character | Magnitude | Practical appearance |
|---|---|---|---|
| Large-format process lens (Apo-Ronar, G-Claron) | Essentially zero | <0.1% | Indistinguishable from pinhole |
| Telescope achromat objective | Very low | 0.1–0.3% | Negligible in portraits |
| Custom singlet, symmetric biconvex | Low (symmetric design nulls distortion) | 0.2–0.5% | Negligible |
| Fresnel lens | Barrel distortion at edges | 1–5% at margins | Visible but not severe |
| Simple plano-convex singlet (stop offset) | Barrel or pincushion | 1–3% | Visible |

For the image areas covered by each option (central circle, 300–600mm diameter), even moderate distortion percentages produce very small absolute pixel displacements. A 1% barrel distortion on a 500mm image circle shifts the edge by 5mm — visible in architectural photography, invisible in a portrait.

---

## Section 8: Chromatic Aberration

**Pinhole:** Zero chromatic aberration. All wavelengths focus at the same point (the pinhole) and arrive at the image plane with identical geometry. This is not a small advantage — it is fundamental. The pinhole is the only optical element with perfect color rendering.

**Lens chromatic aberration by type:**

| Lens type | Longitudinal CA | Lateral CA | On image | Remedy |
|---|---|---|---|---|
| Singlet crown glass, f_L = 1400mm | ~25mm | Significant | Colour fringing on edges | Achromatic doublet |
| Singlet flint glass | ~18mm | Significant | Less than crown | Achromatic doublet |
| Achromatic doublet (crown + flint) | ~1–3mm | Minimal | Very slight colour fringing | — or APO |
| Apochromatic triplet (telescope APO) | <0.5mm | Negligible | Invisible in practice | — |
| Process lens (Apo-Ronar, G-Claron) | <0.3mm | Negligible | Invisible | — |

For silver gelatin paper (blue + green sensitive), longitudinal chromatic aberration manifests as a slight softening of the focus in the blue channel relative to green. The paper does not record red, so the red focal shift does not contribute. On panchromatic film, full RGB CA is visible as colored halos around high-contrast edges.

For portrait work, an apochromatic lens (telescope APO objective or process lens) eliminates chromatic aberration as a concern. A singlet is workable but noticeably color-fringed at the edges of the covered image circle.

---

## Section 9: The Hybrid Approach

The most interesting option for this camera may be to combine a lens with the pinhole rather than replace it. Several configurations are possible:

### 9A: Central Lens, Peripheral Pinhole Array

Mount a 300mm process lens in the centre of the pinhole wall. Drill a series of 2.17mm pinholes at regular intervals across the remainder of the wall (e.g., a 5 × 2 grid of pinholes spaced 1000mm apart). Each pinhole projects a complete, soft image of the full scene onto the image plane, overlapping with each other and with the lens image.

Result: a central sharp-focus portrait medallion surrounded by a web of overlapping, offset soft pinhole images — a unique artefact that could not be produced any other way.

### 9B: Sequential Exposure — Sharp Portrait + Pinhole Landscape

Make two exposures on the same piece of paper. First: lens exposed for 2–5 seconds with subject present. Second: switch to pinhole (block the lens, unblock the pinhole), expose for 20–40 minutes with subject having left the scene. The result is a sharp portrait superimposed over a soft, long-exposed landscape. The portrait would appear as a sharp ghost within the broader pinhole context.

### 9C: Zone-Focus Grid Lens Array

Install multiple lenses (e.g., 6 large magnifying glass elements, 200mm diameter each) across the pinhole wall in a 3 × 2 grid, each focused at a different distance. Each lens covers approximately a 300mm circle of the image plane, with the circles designed to tile adjacent areas. The total covered area is 6 × π(150)² ≈ 424000mm² — still only about 3.9% of the 10743612mm² active image plane, but arranged across the full width. The effect: a grid of sharp circular windows with dark/pinhole gaps between them.

---

## Section 10: Summary and Recommendation

### What Changes When You Add a Lens

| Quality | Pinhole | Process lens | Telescope APO | Fresnel lens |
|---|---|---|---|---|
| Coverage of image plane | ~116 sq ft (active) | Ø ~400mm circle | Ø ~150–200mm circle | Ø ~600mm circle |
| Sharpness (within covered area) | 0.23 lp/mm | 15–25 lp/mm | 20–40 lp/mm | 2–8 lp/mm |
| Depth of field | Unlimited (all soft) | f/32: 1.2 m span | f/32: 1.2 m span | Shallow (soft) |
| Exposure time (Ware cyanotype, ISO ~2–4) | ~35 min | ~1.5 sec | ~6 sec | ~0.4 sec |
| Geometric distortion | Zero | <0.1% | ~0.2% | 1–3% |
| Chromatic aberration | Zero | <0.3mm (APO) | <0.5mm (APO) | ~25mm (severe) |
| Image magnification | M = d_i/d_o | M = d_i/d_o (same) | M = d_i/d_o (same) | M = d_i/d_o (same) |
| Cost (lens only) | — | $400–$1,500 | $700–$4,500 | $30–$200 |
| Aesthetic character | Soft, unlimited DoF, perfect geometry | Sharp medallion, exact perspective | Very sharp medallion | Soft, chromatic, glowing |
| Shutter required | No | Yes (hand shutter adequate) | Yes | Yes |

### Recommended Lens Specification for Portrait Work

If a lens is added for portrait work with the goal of maximising image quality:

**Primary choice:** A **Rodenstock Apo-Ronar 1200mm f/14** or **Nikkor T 1200mm f/11** mounted on an adjustable focus board in the pinhole wall. Both are available on the used market for $400–$1,500. The 1200mm focal length focuses at 2.4 m from the wall — slightly close for comfortable portrait work; extending the lens board ~80mm forward (toward the subject) re-focuses the system to approximately 3.4 m. These lenses provide:

- f/14 maximum aperture → effective f/24 at 3.4 m → 0.4 second exposure on ISO 6 paper
- <0.1% distortion (designed for reprographic work)
- Apochromatic correction — no visible colour fringing
- Ø ~400mm image circle — a large, centred medallion portrait
- Extremely well-documented optical performance

**For broader coverage at the cost of aberrant character:** A **600 × 600mm acrylic Fresnel lens at 1400mm focal length** (available from Edmund Optics or solar optics suppliers for $40–$120). Covers a 600mm circle with characteristic soft-centre/chromatic-edge quality. Interesting artistic choice; very cheap to test.

**For maximum sharpness in the smallest area:** A **150mm aperture apochromatic telescope doublet** (1200–1500mm focal length). Sky-Watcher or William Optics 150mm f/8–f/10 APO objectives, purchased as bare objectives without focuser from surplus telescope suppliers. These deliver the finest image quality available at this price point ($800–$2,000) and can be experimentally swapped with the pinhole plate.

### The Fundamental Trade-Off

| | Pinhole | Lens |
|---|---|---|
| Image area | ~116 sq ft (active) | 0.7–4% of total (within image circle) |
| Subject holds still | ~35 min | 1.5–10 seconds |
| Geometric character | Perfect perspective, unlimited DoF | Sharp focus zone, controllable DoF |
| Background | Soft but rendered | Sharp (at working aperture) or shallow-DoF blur |
| Aesthetic | Documentary/impressionistic | Conventional photographic |
| Cost to try | $0 (already built) | $400–$1,500 for quality option |

The pinhole gives the whole image, slowly. The lens gives a sharp central circle, quickly. The most complete approach is to build the camera as a pinhole camera first — which is the current plan — and provision the pinhole wall with a **removable plate** system: the Ø 2.17mm pinhole drilled in one plate, the lens mount in a second plate of identical dimensions. Swapping plates converts the camera between modes without any other modification. This is structurally trivial to implement during construction and preserves all options.

---

## Sources

| Source | Relevance |
|---|---|
| Hecht, E., *Optics*, 5th ed., Pearson, 2017, §6.3–6.6 | Thin lens equation, aberration theory, DoF formulas |
| Born, M. & Wolf, E., *Principles of Optics*, 7th ed., Cambridge UP, 1999, §8.6 | Airy disk, diffraction limits, cos⁴ law derivation |
| Stroebel, L., *View Camera Technique*, 7th ed., Focal Press, 1999 | Bellows extension factor, large-format lens practice |
| Renner, E., *Pinhole Photography*, 4th ed., Focal Press, 2009 | Pinhole-to-lens comparison; practical exposure guidance |
| Rodenstock product data sheets (rodenstock-photo.de) | Apo-Ronar focal length / image circle specifications |
| Nikon / Nikkor large format lens specifications | T-ED series 1200mm data |
| Edmund Optics (edmundoptics.com) | Fresnel lens specifications, acrylic singlet availability |
| Sky-Watcher / William Optics product pages | APO refractor objective specifications |
| Ray, S., *Applied Photographic Optics*, 3rd ed., Focal Press, 2002, §15 | Field curvature, cos⁴ falloff, large-format lens design |
