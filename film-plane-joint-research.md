<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Film-Plane Tilt/Swing Joint — Grounded Mechanism Research

**Branch:** `film-plane-redesign`. Purpose: stop guessing at the corner joint and ground the
tilt/swing mechanism in established engineering. Requirement recap: a **rigid rectangular back
(~2.4 m tall)** that must **tilt and swing to ~±45°** on each axis, **manual** actuation, in a
**corrosion-prone wet environment** (must be stainless / acetal / PTFE — no exposed rolling
bearings). Below: a shortlist of 14 real mechanisms with engineering sources, the factual joint-angle
limits that reframe the whole problem, and a synthesis.

---

## 0. The one fact that reframes everything — documented joint-angle limits

Every ball/spherical/universal element we were chasing is fundamentally an **alignment
compensator**, not a large-swing joint. From bearing standards, catalogs, and Machinery's Handbook:

| Joint element | Documented angle (per axis / side) | Clears ±45°? | Source |
|---|---|---|---|
| **Crossed-pin gimbal / trunnion-yoke** | **~±90° per pin** | **YES** | [Wikipedia: Gimbal](https://en.wikipedia.org/wiki/Gimbal) |
| Rzeppa CV joint | 45–54° (but a *rotating driveline* part) | borderline | [Wikipedia: CV joint](https://en.wikipedia.org/wiki/Constant-velocity_joint) |
| Single Cardan (universal) joint | ~25° preferred, **37.5° hard max** | **No** | [Machinery's Handbook 31e p.1197](https://online.flippingbook.com/view/954046886/1197/) |
| High-misalignment rod end (Aurora HX) | ~±19–22° | **No** | [Timken/Aurora CAD](https://cad.timken.com/item/inch-spherical-bearings/e-series-spherical-bearings-ptfe-liners-availabl/com-4e) |
| Standard rod end (heim joint) | ±13–16° | **No** | [Timken/Aurora SW-4E](https://cad.timken.com/item/al-industrial-rod-ends-spherical-bearings-rod-ends/rod-ends-corrosion-resistant-ptfe-liners-availab-4/sw-4e) |
| Spherical plain bearing (ISO 12240-1) | 6–16° (mid sizes 6–9°) | **No** | [SKF SPB catalog 4400](https://www.rmbearings.co.uk/pictures/pdfs/SKF%20SPHERICAL%20PLAIN%20BEARINGS.pdf) |
| Ball joint (automotive/industrial) | ±15–30° | **No** | [Firgelli: flexible ball joint](https://www.firgelliauto.com/blogs/mechanisms/flexible-ball-joint) |

**This is why the rod-end path kept fighting us.** The 2458K435 (20° swivel) wasn't an outlier —
±13–22° *is* what spherical/rod-end joints do. Even the 60645K591's "47° max" is at the extreme edge
of what any catalog spherical claims, and gets choked further by any surrounding clevis. **The only
element that natively clears ±45° on each axis is two orthogonal pins — a gimbal / trunnion.** That
is a fact from the standards, not an opinion.

---

## 1. Strategic question this raises: central mount vs. four corners

Every established "rigid panel on two axes" system — view-camera rear standard, telescope fork,
heliostat, radar pedestal, ship gimbal — pivots the panel about **one central two-axis mount whose
axes pass through (or near) the panel's center of mass**, so a person fights only *friction*, not
gravity. None of them use four independent corner joints. Our current architecture distributes the
joint to 4 corners because it also buys **focus / rise / shift / back-focus** (the leadscrews). So the
real fork in the road:

- **(i) Keep 4 corners** (keep all the view-camera movements) → then each corner joint must be a
  **crossed-pin gimbal** (§0 says nothing else clears ±45°), on plain PTFE/acetal bearings.
- **(ii) Central 2-axis mount** (tilt/swing only, the classic way) → a **fork/yoke or ring gimbal**
  balanced through the CoM. Far fewer parts, but you'd re-derive focus/rise/shift separately.

Worth deciding before detailing — it's the biggest lever. The mechanisms below serve either path.

---

## 2. Shortlist — 14 established mechanisms with sources

### A · Whole-mechanism two-axis precedents

**1. Fork / yoke mount (searchlight · radar · telescope fork).** A U-fork rotates on a base
(azimuth/swing); the panel hangs between the tines on a coaxial trunnion pair (tilt) — *both axes in
one structure, two-point support*. Marine versions use bronze bushings + stainless pins. Range: az
360°, tilt ~90°. → [US 4,419,721](https://patents.google.com/patent/US4419721A/en) ·
[Keel, "Telescope Mountings"](https://www.pages.astronomy.ua.edu/keel/techniques/mountings.html).
**Verdict: top pick for a central mount** — straddles the panel, two-point trunnion suits a 2.4 m
plane, proven marine corrosion pedigree.

**2. Alt-azimuth pedestal (telescope / radar).** Azimuth base bearing carries all weight + overturning
moment; a fork on top carries the tilt trunnion, *balanced through the CoM so manual tilt fights only
friction* — "fork mounts do not need the large counter-weights." → [Sheffield PHY217, alt-az](https://vikdhillon.staff.shef.ac.uk/teaching/phy217/telescopes/phy217_tel_altaz.html).
**Verdict: the stiff, buildable archetype** for a tall rigid load; put the tilt axis through the CoM.

**3. Ring gimbal / Cardan suspension.** Two nested rings on perpendicular pins; **axes intersect at
one gimbal point** ideally on the CoM. Best corrosion pedigree of all — marine compass gimbals are
bronze + stainless. Range: limited only by ring clearance (~±30–90°). →
[US 6,198,580 "Gimballed optical mount"](https://patents.google.com/patent/US6198580B1/en) ·
[US 4,318,522 "Gimbal mechanism"](https://patents.google.com/patent/US4318522A/en).
**Verdict: the reference if you want both axes on one true center** — this is the "textbook" version
of my earlier gimbal sketch.

**4. Tip-tilt pole + 2 struts + top gimbal (solar TTDAT).** A central top pivot carries the panel's
weight in compression; **two hand-adjustable self-locking struts** set the two tilt components. Bounded
**±45–60° cone — an almost exact match to our spec**, with the fewest corrodible parts. →
[Sinovoltaics: TTDAT](https://sinovoltaics.com/learning-center/csp/tip-tilt-dual-axis-trackers-ttdat/) ·
primary: [Ferdaus et al., *J. Renewable Energy* 2014](https://onlinelibrary.wiley.com/doi/10.1155/2014/629717).
**Verdict: best "cone of motion" match** — 1 pivot bearing + 2 self-locking screws = manual, wet-safe.

**5. Tilt-roll twin-linear-drive heliostat (small scale).** Two axes each set by an independent
**linear drive/strut** (swap the electric actuators for hand-cranked ACME screw jacks or turnbuckles;
screws self-lock). Demonstrated at 0.45 m panel scale. → [Wiley *Energy Technology* 2025](https://onlinelibrary.wiley.com/doi/10.1002/ente.202401051).
**Verdict: most build-friendly actuation** — two struts fully constrain + hold two axes, no brake.

**6. Az-el pedestal + slewing ring.** One **large-diameter ring bearing** reacts a tall panel's
overturning moment in a *single* component (axial + radial + moment together) — efficient swing axis;
elevation trunnion above. → [Sandia SAND92-7009 (heliostat load path)](https://www.osti.gov/servlets/purl/7105290) ·
[US 6,204,823 low-profile az-el positioner](https://patents.google.com/patent/US6204823B1/en).
**Verdict: use a sealed/plastic slew ring for the swing axis** if the panel is tall and off-center.

**7. Nested-gimbal cradle, plain sliding bearings (heliostat thesis).** Panel cradled between two
tilt bearings (CoM on axis → low torque), that cradle on an azimuth ring; explicitly uses **plain
sliding bearings, not rolling elements** — maps straight onto acetal/PTFE bushings. →
[Björkman, *Heliostat Design*, KTH 2014 (full drawings)](https://www.diva-portal.org/smash/get/diva2:769446/FULLTEXT01.pdf).
**Verdict: the closest fully-drawn, plain-bearing, cradle+ring design to copy.**

**8. View-camera base-hinge trunnion + friction clamp.** The *only* classic view-camera movement that
natively reaches ±45° (Sinar P base tilt ±40°; the 3D-printed "Standard 4×5" ±45°): a trunnion pin at
the frame base + a friction clamp knob. Simplest possible corrosion-safe pivot. →
[Sinar ranges](https://en-academic.com/dic.nsf/enwiki/606791) ·
[Standard 4×5 DIY ±45°](https://www.thephoblographer.com/2018/07/31/standard-4x5-modular-diy-large-format-camera/).
**Verdict: the direct-precedent one-axis building block**; stack two (tilt below swing) for both.

**9. X-Y two-horizontal-axis mount (NASA antenna).** Two *perpendicular horizontal* shafts on pillow
blocks — no turntable; both pivots low, accessible, trivially sealed; ±90° each. → [NASA TN D-1697](https://archive.org/details/nasa_techdoc_19660022787).
**Verdict: strong runner-up for buildability** — two simple sealed horizontal journals, no ring.

**10. CNC tilting-rotary (trunnion) table.** Serial 2-axis: a cradle on **two coaxial trunnion
bearings** (a span, not a cantilever) + a rotary platter; manual units have **handwheel + disk-brake
clamp per axis** (±110° tilt). → [US 7,753,629 "Tilt table"](https://patents.google.com/patent/US7753629B1/en).
**Verdict: rigidity + per-axis manual-lock reference** (but cast-iron construction is not
corrosion-suited — borrow the kinematics, not the materials).

### B · Corrosion-safe pivot/bearing building blocks

**11. Dobsonian PTFE-pad friction bearing.** Large-radius arc riding on **virgin PTFE pads against
textured FRP/phenolic laminate** — non-metallic, grease-free, corrosion-immune, and **self-holding by
friction** (static ≈ dynamic on waxed Teflon, µ ≈ 0.05–0.10, no breakaway lurch). Standard set ~3 az +
4 alt pads, 4.8 mm thick. → [Stellafane: Dob bearing materials](https://stellafane.org/tm/dob/resources/bearnings.html) ·
[SVAS ATM engineering PDF](https://svas.org/s17files/Atm_Engineering_Lightweight_Dobsonian_Telescopes.pdf) ·
Kriege & Berry, *The Dobsonian Telescope*.
**Verdict: the standout wet-environment bearing** — a manually-set panel that holds by friction with
zero grease and zero corrodible metal in the bearing. Strongly recommend for at least the tilt axis.

**12. PTFE-lined / acetal-bushed stub trunnion.** A stainless stub shaft in a self-lubricating plain
bush (PTFE-fabric per ISO 12240, or acetal/igus polymer) — compact, sealed, dry-running. →
[SKF TX-line self-lubricating](https://evolution.skf.com/tx-line-spherical-plain-bearings-for-maintenance-free-operation/) ·
[WisDOT PTFE-on-stainless friction report](https://wisconsindot.gov/documents2/research/WisDOT-WHRP-project-0092-08-13-final-report.pdf).
**Verdict: the compact form** of #11's material — use where a full PTFE pad is too bulky.

**13. Heavy 316-stainless pivot set (top + bottom door/gate pivot).** Proven to carry a ~2.4 m rigid
leaf's dead weight on a vertical axis; industrial weld-on stainless spindles rated to thousands of lb;
offered in **316** for marine service. → [Jako SS free-swing pivot (500 kg)](https://www.jakohardware.com/shop/product/jnf-heavy-duty-free-swing-door-pivot-max-1100-lbs-stainless-steel-model-jk05500-13437) ·
[Kiesler heavy-duty 304/316 pivot hinges](https://www.kieslermachine.com/heavy-duty-hinges/pivot-hinges/).
**Verdict: off-the-shelf, load-proven, 316-SS swing-axis hardware** — reuse as the vertical axis of a
two-axis mount instead of fabricating it.

**14. Crossed-pin gimbal block (the joint element itself).** Two orthogonal stainless pins in
acetal/PTFE bushings — the only element that clears ±45° per axis (§0), each axis **independently
lockable** with a detent/clamp. → [Wikipedia: Gimbal](https://en.wikipedia.org/wiki/Gimbal) ·
element angle facts as §0.
**Verdict: if we keep the 4-corner architecture, this is the corner joint** (my study "A").

---

## 3. Design principles the sources agree on (adopt regardless of choice)

1. **Put the tilt axis through the panel's center of mass** — then manual actuation fights only
   friction, no counterweight (view-camera axial, telescope fork, heliostat cradle all say this).
2. **Plain self-lubricating bearings, not rolling elements** — PTFE pad / PTFE-lined / acetal-igus on
   stainless. Corrosion-immune, grease-free (Dobsonian, KTH heliostat, SKF TX, igus).
3. **Hold position by friction or a self-locking drive** — waxed-PTFE friction (Dob), self-locking
   worm/ACME screw (heliostat, Orbix), or an indexed clamp/detent per axis (CNC table, louvers). No
   powered brake.
4. **Support the tilt axis at two spaced points (trunnion/fork), not a cantilever** — a couple across a
   wide base suits a tall rigid plane (trunnion, fork, X-Y, CNC cradle).
5. **Yaw-free stacking: put the tilt axis below the swing axis** — otherwise combined ±45° tilt+swing
   twists the panel (view-camera rule).
6. **Reach ±45° with pins/trunnions, reserve spherical bearings for small self-aligning takeup only**
   (§0 fact).

## 4. Recommendation to detail next

The grounded, convergent answer: **a two-axis fork/gimbal mount, tilt axis through the CoM, on
Dobsonian-style PTFE-pad (or PTFE/acetal-bushed) plain bearings, held by friction or a self-locking
screw** — i.e. mechanisms **1/2/3 + 11**. If we keep the four-corner architecture, each corner becomes
mechanism **14** (crossed-pin gimbal on PTFE/acetal bushings). Either way the rod-end / spherical
bearing is retired — §0 shows it never could have hit ±45°.

*Source confidence: primary/verified — Machinery's Handbook, SKF & Aurora/Timken catalogs, NASA
TN D-1697, Sandia SAND92-7009, KTH thesis, the cited patents (Google Patents HTML mirrors), Stellafane/
SVAS ATM refs, university course notes. Search-synthesized (verify a specific datasheet before quoting a
single number): the igus/ball-joint degree figures and the TTDAT overview link.*
