<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Film-Plane Tilt/Swing — Grounded Mechanism Research

**Branch:** `film-plane-redesign`. The problem, stated correctly: a **fixed-size rigid rectangular
panel** (the film plane) is **positioned at its four corners** by four moving carriages (X–Z
cross-slide + depth leadscrew each); driving the corners tilts and swings the whole rigid plane to
~±45°. This is a **parallel-kinematics** problem, and the literature is unanimous about what's wrong
with it and how it's solved. Manual actuation, corrosion-prone wet environment (stainless/acetal/PTFE).

---

## The finding, in one line

**Driving a rigid panel at four rigid corners is textbook _over-constraint_ — the wobbly-four-legged-
table.** A rigid body has 6 degrees of freedom and needs _exactly_ 6 constraints; four rigidly-located
corners is statically indeterminate, so it **rocks, racks, binds, and warps** from the tiniest mismatch.
**That is the root cause of the corner joint "fighting" — not the joint part, the architecture.** The
established fix: **drive 3 corners, let the 4th float.**

---

## 1. Why it fights — over-constraint (root cause, from precision-engineering canon)

- A free rigid body has **6 DOF**; each ideal support removes one → `DOF = 6 − N`. Locating it needs
  **exactly 6 constraints**. Fewer = loose; **more = over-constrained** → binding, locked-in strain,
  and non-repeatable "settles wherever the highest contacts are" seating. (Maxwell's kinematic principle.)
- **Three non-collinear points fully define a plane.** A rigid plane's out-of-plane pose — one
  piston (normal translation) + two tilts (= our **tilt and swing**) — is exactly **3 DOF**, set
  determinately by **3 driven corners**. The **4th corner is mathematically redundant**: the four can't
  all sit true unless the frame is perfect, so it rocks between diagonals, or if clamped, warps to reach.
- This is literally the "wobbly 4-legged table vs. stable 3-legged stool," and it's why machine tools
  and precision tables are leveled on **3** points, not 4.
- Sources: [Practical Precision — The Principle of Kinematic Constraint](https://practicalprecision.com/kinematic-constraint/) ·
  [MIT 2.76 — Exact-Constraint Design (Reading L3)](https://ocw.mit.edu/courses/2-76-multi-scale-system-design-fall-2004/3aa5862a1724b75c3e4aa7a6fee6c511_reading_l3.pdf) ·
  Blanding, *Exact Constraint: Machine Design Using Kinematic Principles* (ASME 1999) — [ASME](https://asmedigitalcollection.asme.org/ebooks/book/219/Exact-ConstraintMachine-Design-Using-Kinematic) ·
  Hale, *Principles and Techniques for Designing Precision Machines* (PhD thesis, MIT/LLNL 1999) — [full PDF](https://digital.library.unt.edu/ark:/67531/metadc784803/m2/1/high_res_d/8431.pdf) ·
  [Practical Machinist — kinematic support of machine tools (3-point)](https://www.practicalmachinist.com/forum/threads/kinematic-support-of-major-machine-tool-components.365853/).

## 2. The fix — exact constraint (what to do instead)

| Option | Constraint status | When to choose |
|---|---|---|
| **Drive 3 corners; 4th unsupported** | Exact constraint (determinate) | Cleanest — if the panel is stiff enough to not sag between the 3 |
| **3 driving corners + 1 _astatic/floating_ 4th** (spring/counterweight/ball-in-slot follower — carries load, sets no position) | Pseudo-kinematic (6 real constraints, 4 carriages) | **Best for us** — keeps 4-corner load support, no over-constraint |
| **All 4 corners deliberately & equally compliant** | Elastic averaging | Heavy panel, robustness > precision |
| **4 rigid driven corners (current design)** | **Over-constrained — avoid** | Never (this is the binding we've been fighting) |

- The theory is unanimous: **never four rigid locating corners.** Purists (Blanding/Hale/Slocum) say
  drop to 3 or add real freedoms with flexures; the elastic-averaging school (Awtar/Slocum) says
  over-constrain _on purpose_ but only with matched distributed compliance. Both kill the fight.
- **"Support with many, locate with 3, and never let a support become a locator."** Load-spread the
  corners as much as you like; only **3** may _define position_.
- Sources: [Blanding (above)](https://asmedigitalcollection.asme.org/ebooks/book/219/Exact-ConstraintMachine-Design-Using-Kinematic) ·
  Awtar & Slocum, *Elastic Averaging in Flexure Mechanisms* (ASME 2010) — [UMich PSDL PDF](https://psdl.engin.umich.edu/pdf/DETC2006-99752.pdf) ·
  Furman (SJSU), *Kinematic Design Principles* — [PDF](https://www.gotstogo.com/misc/engineering_info/ME250kinematic_design_BFurman.pdf) ·
  [3-point vs 4-point bed leveling](https://drmrehorst.blogspot.com/2017/07/3-point-print-bed-leveling-vs-4-point.html).

## 3. The corner joint itself — a moment-free two-force member

- In a Stewart–Gough platform (the canonical "rigid platform on moving legs"), each leg gets a
  **spherical (ball) joint at the platform end** so the leg is a **pure axial strut — transmits force,
  never a bending moment.** That decoupling is what stops the legs from bending the platform or fighting
  each other. A rigid/pinned corner joint would add redundant constraints → over-constraint.
- **Each locked leg = exactly one constraint** (it fixes the distance between its ball centers). Count
  to six. (Grübler–Kutzbach mobility.)
- Sources: [Modern Robotics §2.2 — DOF / Stewart platform](https://modernrobotics.northwestern.edu/nu-gm-book-resource/2-2-degrees-of-freedom-of-a-robot/) ·
  [Passive Stewart-Gough platform w/ preloaded Cardan joints (PMC 2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12899874/) ·
  [Firgelli — Stewart platform explained](https://www.firgelliauto.com/blogs/mechanisms/stewart-platform-hexapod).

## 4. The ±45° reality — it lives in the JOINT, not the kinematics

Every documented parallel tilt platform is capped near **±30–40°**, and the limit is the **ball-joint
cone angle**, not the mechanism. Plain spherical/rod-end bearings simply don't clear ±45°:

| Joint element | Documented angle | Clears ±45°? |
|---|---|---|
| **Universal (Cardan) / gimbal / two-pin** | ±37–52° (AMiBA hexapod U-joints hit **±52°**) | **Yes** |
| High-misalignment rod end (Aurora HX) | ±19–22° | No |
| Standard rod end / spherical plain bearing | ±6–16° | No |
| Best documented 3-leg parallel tilt (3-PRS) | **±40°** | edge |

- To honestly reach ±45° you must use a **universal/gimbal joint** (or a large purpose-built one, as
  AMiBA did), **not** a plain spherical bearing — or adopt the view-camera **axis-tilt gimbal cradle**
  (pivots through the plane center; no ball-in-socket cone limit).
- Sources: [Machinery's Handbook 31e p.1197 (Cardan ~37.5° max)](https://online.flippingbook.com/view/954046886/1197/) ·
  [Aurora high-misalignment rod ends (19–22°)](https://chassisshop.com/products/aurora-high-misalignment-rod-end-teflon-lined) ·
  [3-PRS ±40° (arXiv 2405.08418)](https://arxiv.org/html/2405.08418v1) ·
  [AMiBA hexapod (±52° U-joints)](https://arxiv.org/pdf/0902.2335) ·
  [NHBB — rod-end misalignment](https://www.nhbb.com/knowledge-center/engineering-reference/rod-end-spherical-bearings/misalignment).

## 5. Precedents that do exactly this (rigid panel positioned at 3 driven points)

1. **Keck segmented primary mirror** — each **rigid** hexagonal segment is piston/tip/tilt-controlled
   by **exactly 3 actuators**, with a **whiffletree** spreading each actuator's force over many pads.
   Support (many pads) and location (3 actuators) are cleanly separated. This is the direct template. →
   [Keck position actuators (LBNL/OSTI PDF)](https://www.osti.gov/servlets/purl/6377486) ·
   [CELT Green Book Ch.5](https://celt.ucolick.org/greenbook/ch05.pdf).
2. **3-PRS parallel head** (Sprint Z3 / Exechon machine-tool class) — a rigid plate given **piston + 2
   tilts on 3 actuated legs**, documented to **±40°**; ball joint at the plate, actuator on a base rail. →
   [3-PRS stiffness/workspace (arXiv 2405.08418)](https://arxiv.org/html/2405.08418v1).
3. **Whiffletree / Hindle mount & astatic levers** — load a big rigid plate at many points that all
   cascade to **3 hard locating points**; astatic (force-controlled) levers "float" the extra supports
   so they carry weight without setting position — the textbook way to make the **4th corner** legal. →
   [Whiffletree history](https://mechanicsandmachines.com/?p=456) ·
   [Cruxis mirror-cell design](https://www.cruxis.com/scope/scope1100_mirrorcell.htm).
4. **Machine-tool / print-bed 3-point leveling** — the shop-floor confirmation that 3 points locate a
   plane and a 4th must be a _force_ support (equalized wedge), never a new locating point. →
   [Practical Machinist](https://www.practicalmachinist.com/forum/threads/kinematic-support-of-major-machine-tool-components.365853/).
5. **View-camera rear standard (axis tilt)** — the manual 2-DOF classical analog: a rigid film-plane
   frame on a yaw-pitch **gimbal cradle**, tilt about a horizontal axis + swing about a vertical axis,
   each pivot through the plane center (focus-preserving), locked by a knob. → [Tobias Key — camera movements](https://www.tobiaskey.com/camera-movements/).

## 6. Wet-environment joints (corrosion)

PTFE-lined stainless spherical bearings (run dry, wash-down tolerant), all-plastic **igus igubal**
(iglidur ball + stainless sleeve, corrosion-free), stainless pins in acetal/PTFE bushings, or **flexures**
(no sliding contact at all). → [igus igubal rod ends](https://www.igus.com/spherical-bearings/rod-ends) ·
[SKF TX self-lubricating spherical](https://evolution.skf.com/tx-line-spherical-plain-bearings-for-maintenance-free-operation/).

---

## 7. What this means for our design

The current mechanism **drives all four corners** and hangs a rigid plane between them — which the
theory says is **over-constrained by construction** (up to 12 driven inputs for a 6-DOF body). That is
almost certainly the real reason the corner joint has been so hard: no joint can fix an over-constrained
architecture. The grounded redesign options, in order of how established they are:

- **(A) Drive 3 corners; make the 4th an astatic/floating follower.** Minimal change to the current
  layout — keep three leadscrew corners as the locating set, convert the fourth to a load-only support
  (spring/counterweight or ball-in-slot). Each driven corner gets a **wide-angle joint** (gimbal/universal,
  not plain spherical) to clear ±45°. Precedent: Keck, machine-tool leveling.
- **(B) 3-leg parallel tilt platform (3-PRS-style).** Purpose-built for exactly "tilt+swing+piston of a
  rigid plate on 3 legs," documented to ±40°. A cleaner-sheet version of (A).
- **(C) Central axis-tilt gimbal (view-camera rear standard).** Abandon the corner-drive entirely; pivot
  the rigid plane on a 2-axis gimbal through its center. Fewest parts, cleanest ±45°, but re-derives
  focus/rise/shift separately (they were the reason for the 4 leadscrews).

**Bottom line:** the rod-end/spherical path is retired (can't do ±45°), _and_ the four-rigid-corner
architecture is the deeper problem. Whatever we build, the rule is **locate on 3, float the 4th, use a
wide-angle (gimbal/universal) joint at each driven corner** — grounded in Keck, Stewart-Gough, and 100
years of kinematic-design theory.

*Source confidence: exact-constraint theory (Blanding, Hale thesis, MIT OCW, Slocum, Practical Precision),
Modern Robotics, the 3-PRS ±40° arXiv paper, Keck LBNL/OSTI report, and the machining/telescope-cell refs
were retrieved and on-topic. Some journal PDFs bot-block automated fetch — their numbers are corroborated
via search + the standard mobility results. Rod-end/Cardan angle figures are page-verified from Aurora/
NHBB/Machinery's Handbook.*
