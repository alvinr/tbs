<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Depth of Field, Magnification & Minimum Focal Distance
### 20-foot Standard Container, Side-to-Side Orientation

**Preceding documents:** pinhole-optics-report.md, pinhole-camera-construction.md  
**Date:** April 2026

---

## Camera Parameters (Option B)

All calculations on this page use these fixed values, derived from the 20-foot standard container in Orientation B (pinhole on one long wall, image plane on opposite long wall):

| Parameter | Value | Source |
|-----------|-------|--------|
| Focal length (f) | **2,362 mm (7 ft 9 in)** | ISO 668 interior width |
| Rayleigh optimal pinhole (d) | **2.17 mm** | d = 1.9 × √(f × 0.00055); Rayleigh, *Phil. Mag.* 1891 |
| F-number (N) | **f/1088** | N = f/d |
| Image plane width | 5,893 mm (19 ft 4 in) | Container interior length |
| Image plane height | 2,388 mm (7 ft 10 in) | Container interior height |
| Wavelength (λ) | 0.00055 mm (550 nm) | Green light reference |

---

## Part 1: The Geometry of Blur in a Pinhole Camera

### Why Pinhole Cameras Don't Truly Have Infinite Depth of Field

The claim that pinhole cameras have "infinite depth of field" is a useful shorthand but physically incomplete. The truth is more nuanced, and it matters enormously at the scale of this camera.

**What is actually true:** A pinhole camera has no lens, so there is no focus plane — no single distance at which the camera is "focused." Every subject distance projects an image. However, the *sharpness* of that image varies with distance.

**What varies with distance:** At any subject distance u, a point source of light does not project to a perfect point on the image plane. It projects to a disk — called the **blur circle** or **circle of confusion** — whose diameter depends on the subject distance and the pinhole size.

**The physical cause:** The pinhole has finite diameter d. Light from a point source at distance u passes through the entire width of the pinhole. Rays entering through the top edge of the pinhole and rays entering through the bottom edge both reach the image plane, but they arrive at slightly different positions — separated by the geometry of the cone of light. The total spread of these rays on the image plane is the blur circle.

**Source:** Young, M., "Pinhole Optics," *Applied Optics*, Vol. 10, No. 12, 1971. DOI: [10.1364/AO.10.002763](https://doi.org/10.1364/AO.10.002763)  
"Pinhole cameras lose sharpness as the subject gets close to the pinhole due to simple geometry — diverging light rays from close objects produce larger spots at the image plane than more nearly parallel rays from distant objects." — [Photrio.com forum thread on CoC for pinhole cameras](https://www.photrio.com/forum/threads/circle-of-confusion-and-hyperfocal-distance-of-a-pinhole-camera.15715/)

---

## Part 2: The Blur Diameter Formula

For a pinhole of diameter d with focal length f, the blur circle diameter at subject distance u is derived from simple geometry (similar triangles):

```
B = d × (u + f) / u
```

Or equivalently:

```
B = d × (1 + f/u)
```

**Where:**
- `B` = blur circle diameter on the image plane (mm)
- `d` = pinhole diameter (mm)
- `f` = focal length — pinhole to image plane (mm)
- `u` = subject distance — subject to pinhole (mm)

**Source:** Born, M. & Wolf, E., *Principles of Optics*, 7th ed., Cambridge University Press, 1999, §8.6. The geometric derivation of the pinhole image circle from similar triangles is treated here in the context of diffraction theory.

### Key Observations from the Formula

1. **As u → ∞:** B → d. The blur circle never gets smaller than the pinhole diameter itself. The minimum possible blur is 2.17 mm (at infinity).

2. **As u → 0:** B → ∞. Very close subjects produce extremely large blur circles.

3. **At u = f:** B = d × (f + f)/f = **2d** — exactly twice the pinhole diameter.

4. **The pinhole is always "soft"** by the standards of lens-based photography. A 2.17 mm blur circle at f/1088 would be unacceptable on a 4×5 inch print. On a 19-foot print viewed from 6 meters, it is invisible.

### Diffraction Added to Geometric Blur

At infinity, the geometric blur = d = 2.17 mm. But diffraction also contributes a spread of:

```
B_diffraction = 2.44 × λ × f / d = 2.44 × 0.00055 × 2362 / 2.17 = 1.47 mm
```

The Rayleigh optimal pinhole was chosen precisely so that these two contributions are balanced. The total blur at infinity is approximately:

```
B_total = √(d² + B_diffraction²) = √(2.17² + 1.47²) = √(4.71 + 2.16) = √6.87 = 2.62 mm
```

This is the **absolute minimum blur** for this camera — occurring at infinity.

At finite distances, geometric blur dominates over diffraction blur, so the formula B = d × (1 + f/u) gives a good practical estimate for u > 5 m.

---

## Part 3: Blur at Every Distance — The Full Table

| Subject Distance (u) | Blur Circle (B) | B / d ratio | Equivalent in Subject Space at 5 m viewing |
|---------------------|----------------|-------------|---------------------------------------------|
| 0.5 m | **12.4 mm** | 5.7× | Visible smear at all viewing distances |
| 1.0 m | **7.3 mm** | 3.4× | Visible softness at any viewing distance |
| 2.0 m | **4.7 mm** | 2.2× | Soft; visible from 3 m viewing distance |
| 3.0 m | **3.9 mm** | 1.8× | Marginally visible from 5 m |
| 5.0 m | **3.2 mm** | 1.5× | Essentially invisible from 10 m |
| 10.0 m | **2.7 mm** | 1.2× | Invisible from 10+ m |
| 20.0 m | **2.4 mm** | 1.1× | Invisible from any normal viewing distance |
| 50.0 m | **2.3 mm** | 1.06× | Indistinguishable from infinity |
| 100.0 m | **2.2 mm** | 1.02× | Indistinguishable from infinity |
| ∞ | **2.17 mm** | 1.00× | Theoretical minimum |

**Formula applied:** B = 2.17 × (1 + 2362/u), where u is in mm.

---

## Part 4: Depth of Field

### Definition for a Pinhole Camera

For a lens camera, depth of field (DoF) is the range of distances where the blur circle is smaller than the maximum acceptable circle of confusion (CoC = c). For a pinhole camera, the blur is always ≥ d, so DoF is defined as:

- **Far limit:** Always infinity (blur approaches d as u → ∞)
- **Near limit:** The minimum distance where B ≤ c

```
Near DoF limit: u_near = d × f / (c − d)   [valid only when c > d]
```

If c ≤ d: the criterion can never be met — the camera always exceeds this blur at every distance.

### What Is the Right CoC for This Camera?

The circle of confusion criterion is set by the intended **viewing distance and print size**, not by the camera alone. For a 19'4" × 7'10" print:

**Rule:** At viewing distance D, the human eye resolves features subtending ~1 arcminute (1/3438 radians):

```
Minimum resolvable feature at distance D = D / 3438
```

| Viewing Distance | Minimum Resolvable Feature | CoC = c | Near DoF Limit |
|-----------------|---------------------------|---------|----------------|
| 1 m | 0.29 mm | 0.29 mm | c < d — **never sharp at this CoC** |
| 3 m | 0.87 mm | 0.87 mm | c < d — **never sharp at this CoC** |
| 5 m | 1.45 mm | 1.45 mm | c < d — **never sharp at this CoC** |
| 8 m | 2.33 mm | 2.33 mm | u_near = 2.17×2362/(2.33−2.17) = **31.9 m** |
| 10 m | 2.91 mm | 2.91 mm | u_near = 2.17×2362/(2.91−2.17) = **6.9 m** |
| 15 m | 4.37 mm | 4.37 mm | u_near = 2.17×2362/(4.37−2.17) = **2.3 m** |
| 20 m | 5.82 mm | 5.82 mm | u_near = 2.17×2362/(5.82−2.17) = **1.4 m** |

**Reading this table:** A viewer standing 10 meters from the finished 19-foot print can resolve features down to 2.91 mm on the print surface. Since our minimum blur is 2.17 mm (at ∞), subjects must be at least 6.9 meters from the camera for their image to be indistinguishable from infinity by this viewer. Subjects closer than 6.9 meters appear measurably softer.

### The Practical Rule of Thumb

A commonly cited rule for pinhole cameras is: **subjects closer than 3–10× the focal length show noticeable softness.**

For our focal length of 2,362 mm:
- **3× f = 7.1 m (23 ft)** — softness starts to become apparent
- **10× f = 23.6 m (77 ft)** — essentially indistinguishable from infinity

**Source:** Stinson Photography, "Pinhole Pro and the Optics of Pinhole Cameras," 2018. [stinsonphotography.wordpress.com](https://stinsonphotography.wordpress.com/2018/07/16/pinhole-pro-and-the-optics-of-pinhole-cameras/)

### DoF Summary for Option B

| Zone | Distance Range | Sharpness |
|------|---------------|-----------|
| Zone 1 | 0 – 2 m | Severe blur; soft, impressionistic |
| Zone 2 | 2 – 7 m | Noticeable softness; painterly quality |
| Zone 3 | 7 – 24 m | Slight softness; detail present |
| Zone 4 | 24 m – ∞ | **Effectively sharp**; blur within visual noise of the emulsion |

> **For this project:** Any subject more than ~24 meters from the camera can be considered "in focus." At the scale of landscape or architectural photography — the natural subject matter for a fixed outdoor camera — virtually everything of interest (buildings, horizons, skylines) falls into Zone 4. The "infinite depth of field" characterization is valid for the vast majority of practical use cases.

---

## Part 5: Image Magnification

### The Magnification Formula

For a pinhole camera, the lateral magnification M is purely geometric — the ratio of image size to subject size:

```
M = f / u
```

**Where:**
- `M` = lateral magnification (dimensionless)
- `f` = focal length = 2,362 mm
- `u` = subject distance from pinhole (mm)

The image is **inverted** (upside down and mirror-reversed). The magnitude |M| gives the size ratio.

| Subject Distance (u) | Magnification (M) | Image / Subject Relationship |
|---------------------|-------------------|-----------------------------|
| 0.5 m | **4.72×** | Image is 4.72× larger than subject |
| 1.0 m | **2.36×** | Image is 2.36× larger |
| **2.36 m (= 1×f)** | **1.00×** | **1:1 — image equals subject size** |
| 3.0 m | 0.787× | Image is 79% of subject size |
| 5.0 m | **0.472×** | Image is 47% of subject size |
| 7.75 m (= focal length in ft) | 0.305× | — |
| 10.0 m | **0.236×** | Image is 24% of subject size |
| 20.0 m | 0.118× | Image is 12% of subject size |
| 50.0 m | 0.047× | Image is 4.7% of subject size |
| 100.0 m | 0.024× | Image is 2.4% of subject size |

### What Magnification Means for Subject Framing

The image plane is 5,893 mm wide × 2,388 mm tall. For a given subject distance, the portion of the real world captured within that frame is:

```
Scene width captured = image width / M = image width × (u / f)
Scene height captured = image height × (u / f)
```

| Subject Distance | Scene Width in Frame | Scene Height in Frame |
|-----------------|---------------------|----------------------|
| 2 m | 5.0 m (16 ft) | 2.0 m (6.6 ft) |
| 5 m | 12.5 m (41 ft) | 5.1 m (16.7 ft) |
| 10 m | 24.9 m (82 ft) | 10.1 m (33 ft) |
| 20 m | 49.9 m (164 ft) | 20.2 m (66 ft) |
| 50 m | 124.7 m (409 ft) | 50.6 m (166 ft) |
| 100 m | 249.4 m (818 ft) | 101.1 m (331 ft) |

**Example:** A building 15 meters tall at 50 meters from the camera:
- Image height = 15,000 mm × (2362/50000) = 15,000 × 0.0472 = **708 mm (2.3 ft)** on the image plane
- This building fills 708/2388 = **30% of the image height**

**Example:** A person 1.8 m tall at 5 meters:
- Image height = 1,800 mm × (2362/5000) = 1,800 × 0.4724 = **850 mm (2.8 ft)**
- Fills 850/2388 = **36% of the image height**

### The 1:1 Point — Where Subjects Are Life-Size in the Image

At u = f = 2,362 mm (approximately **7 ft 9 in**), subjects project at exactly life-size onto the image plane. A person standing 7'9" from the outside of the container wall appears life-size on the opposite interior wall.

This has creative implications: subjects between 0.5 m and 2.36 m from the camera project at **larger than life scale** on the image plane — they are magnified. Objects directly pressed against the outside of the container wall approach macro photography scales.

---

## Part 6: Minimum Focal Distance

"Minimum focal distance" requires a definition. For a pinhole camera there are three distinct interpretations, each giving a different answer.

### Definition 1: Physical Minimum (Absolute)

The pinhole is in the container wall. The subject is outside. The minimum physical distance is zero — a subject can be pressed directly against the outside wall, immediately adjacent to the pinhole.

**At u → 0:** Magnification → ∞, blur → ∞. The image becomes a vast, extremely blurred field of light. Not useful photographically, but physically possible.

**Practical physical minimum:** The container's corrugated steel wall protrudes ~38 mm (1.5 inches) at the ridges. A subject can realistically be within ~50 mm of the pinhole. At that distance, M ≈ 47× — an extreme macro regime.

### Definition 2: Minimum for Recognizable Image (Practical)

The subject must be far enough that some identifiable image structure exists — not just a wash of light. Based on the blur table in Part 3:

- At **2 m:** B = 4.7 mm, M = 1.18×. A recognizable if soft image of a person or object forms.
- At **1 m:** B = 7.3 mm, M = 2.36×. Heavy softness; impressionistic but not unrecognizable.

**Practical minimum for a recognizable image: ~1–2 m** from the pinhole.

### Definition 3: Minimum for Acceptable Sharpness (Photographic)

This is the classical DoF near limit from Part 4. It depends on the viewing distance of the final print:

| Intended Viewing Distance | Max Acceptable CoC | Min Focal Distance |
|--------------------------|-------------------|--------------------|
| 5 m (casual gallery) | 1.45 mm | c < d; **no minimum satisfies this** |
| 8 m (large gallery) | 2.33 mm | **31.9 m (105 ft)** |
| 10 m (outdoor/billboard) | 2.91 mm | **6.9 m (22.7 ft)** |
| 15 m (across a plaza) | 4.37 mm | **2.3 m (7.5 ft)** |

**Reading this table:** If the final print is intended to be examined closely (5 m), no subject is ever "acceptably sharp" by lens-camera standards — the pinhole always produces a blur larger than what a close viewer can resolve. If the print hangs in a large outdoor space and viewers approach no closer than 15 m, subjects 2.3 m or farther from the camera are within the acceptable sharpness range.

### Definition 4: Minimum for Subject to Fit Within Frame

A fourth practical constraint: the subject must be far enough that they fit within the image plane boundaries.

For a person 1.8 m (71 inches) tall to fit within the 2,388 mm image height:

```
1,800 × M ≤ 2,388
1,800 × (2362/u) ≤ 2,388
u ≥ 1,800 × 2362 / 2388
u ≥ 1,780 mm ≈ 1.78 m (5.8 ft)
```

For a vehicle 4.5 m tall (truck/bus) to fit in frame:

```
u ≥ 4,500 × 2362/2388 ≈ 4,451 mm ≈ 4.45 m (14.6 ft)
```

For a building 10 m tall to fit in frame:

```
u ≥ 10,000 × 2362/2388 ≈ 9,891 mm ≈ 9.9 m (32.4 ft)
```

---

## Part 7: Consolidated Minimum Focal Distance Table

Combining all four definitions for Option B (20-ft container, f = 2,362 mm, d = 2.17 mm):

| Criterion | Minimum Distance | Notes |
|-----------|-----------------|-------|
| Physical (absolute) | ~50 mm (2 in) | Subject touching exterior wall |
| Recognizable image | **~1 m (3.3 ft)** | Heavily blurred but identifiable |
| Person fits in frame (1.8 m tall) | **1.8 m (5.9 ft)** | Magnification ≤ image height |
| Acceptable sharpness at 10 m viewing | **6.9 m (22.7 ft)** | B ≤ 2.91 mm |
| Acceptable sharpness at 8 m viewing | **31.9 m (104.7 ft)** | B ≤ 2.33 mm |
| Sharp by any standard (B ≤ 1.1d) | **~24 m (78 ft)** | B within 10% of minimum |

**Recommended operating minimum:** For subjects intended to appear sharp in the final print (viewed from a normal gallery distance of 5–10 m), position the primary subject at **a minimum of 7–10 meters from the container wall** where the pinhole is located.

For deliberate soft/blurred foreground elements — a creative technique — subjects can be placed at any distance from the camera.

---

## Part 8: Comparison of All Four Proposals — DoF and Magnification

The container width is the same for both 20-ft and 40-ft standard containers (7'9" = 2,362 mm). Therefore **Proposals 1, 2, and 4 all have identical depth of field, magnification, and minimum focal distance.** Only Proposal 3 (end-to-end, f = 12,013 mm) differs.

| Parameter | Proposals 1, 2, 4 (f = 2,362 mm) | Proposal 3 (f = 12,013 mm) |
|-----------|----------------------------------|---------------------------|
| Pinhole diameter | 2.17 mm | 4.87 mm |
| F-number | f/1088 | f/2467 |
| Minimum blur (at ∞) | **2.17 mm** | **4.87 mm** |
| 1:1 magnification distance | **2.36 m** | **12.0 m** |
| Near DoF (c=3mm) | **6.2 m** | Not achievable (3 < 4.87) |
| Near DoF (c=10mm) | **0.65 m** | **12.4 m** |
| Near DoF (c=6mm) | **1.5 m** | **25.8 m** |
| Practical "all sharp" distance | **~24 m** | **~120 m** |

**Key takeaway on Proposal 3 (end-to-end):** With a 4.87 mm minimum blur, subjects must be over 120 meters from the camera for the blur to drop within 10% of its minimum value. The depth of field is effectively the middle distance and beyond. Close and mid-range subjects appear dramatically softer than in Proposals 1/2.

---

## Part 9: Visual Summary

```
OPTION B — DEPTH OF FIELD ZONES (f = 2362 mm, d = 2.17 mm)

Distance from pinhole:
│
0 m ─── PHYSICAL MINIMUM (subject at wall)
│         Blur: extreme; Magnification: extreme
│
1 m ─── Recognizable image minimum
│         Blur: 7.3 mm; Magnification: 2.4×
│
2.36 m ─ 1:1 MAGNIFICATION (life-size image)
│         Blur: 4.7 mm; Magnification: 1.0×
│
5 m ───  Person fits in frame (1.8m tall person = 36% frame height)
│         Blur: 3.2 mm; Magnification: 0.47×
│
7 m ───  MINIMUM FOCAL DISTANCE (10m viewing, 2.91mm CoC)
│         Blur: 2.9 mm; Magnification: 0.34×
│
24 m ──  "EFFECTIVELY SHARP" BEGINS
│         Blur: 2.4 mm (10% above minimum)
│
∞  ────  Maximum sharpness
          Blur: 2.17 mm (minimum possible)
```

---

## Citations

| Source | Application |
|--------|-------------|
| Rayleigh, J.W.S., *Philosophical Magazine* Ser. 5, Vol. 31, 1891 | Pinhole diameter formula; basis for d = 2.17 mm |
| Born, M. & Wolf, E., *Principles of Optics*, 7th ed., Cambridge UP, 1999, §8.6 | Geometric derivation of blur circle from similar triangles |
| Young, M., *Applied Optics*, Vol. 10, No. 12, 1971. DOI: [10.1364/AO.10.002763](https://doi.org/10.1364/AO.10.002763) | Depth of field behavior in pinhole cameras |
| Stinson Photography, "Pinhole Pro and the Optics of Pinhole Cameras," 2018. [stinsonphotography.wordpress.com](https://stinsonphotography.wordpress.com/2018/07/16/pinhole-pro-and-the-optics-of-pinhole-cameras/) | 3–10× focal length rule of thumb for DoF |
| [Photrio.com — CoC and hyperfocal distance for pinhole cameras](https://www.photrio.com/forum/threads/circle-of-confusion-and-hyperfocal-distance-of-a-pinhole-camera.15715/) | Practical CoC discussion; minimum focus distance concepts |
| ISO 668:2020 | Container interior dimensions (source of f = 2,362 mm) |
