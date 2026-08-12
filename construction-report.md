<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Construction Sequence — TBS-001

## 1. Purpose

This report is the **build order of record** for TBS-001 — the sequence in which the camera
is assembled inside the container, why that order is forced, and the gate that must be met
before each phase begins. The install is **geometry-first**: the large fixed masses (the IBC
totes and their frame) go in first and set the datum everything else is measured from; the
precision optical system goes in last, once the real, as-built space is known. Fabrication and
ordering for subsequent phases of the install can only be performed one the **geometry is established**.

The sequence is validated by a **phased 3D construction model** (§8) — one scene per phase,
with a click-through that reveals each step in order — so the order can be walked before any
components, steel is cut, etc.

---

## 2. Build Overview

| Phase | Name | Goal | To Be Completed               |
|-------|------|------|-------------------------------|
| **1** | Geometry set-out | Install the fixed masses that fix the datum | IBC frame + totes plumbed and square; hinge panel hung |
| **2** | Re-measure | Capture the **as-built** space before committing hard structure | Measured clearances reconciled against the mode; refactor the design based on availbale space |
| **3** | Framing | Fit the tray, cantilevers, plumbing, film-plane beams, walkway | Walkway + tray in; perimeter structure loaded |
| **4** | Electrical | Panels, lights, and all wiring runs | Circuits terminated + tested (Blue / Brown / Black) |
| **5** | Photo system | Film plane, pinhole mechanism, light trap | Camera light-tight and operable |

---

## 3. Sequencing Principles

- **Geometry-first.** The IBC stack + frame are the heaviest, least-movable elements and
  define the corridor and walkway datums; everything downstream references them.
- **Measure twice (Phase 2).** Container internal dimensions vary unit-to-unit; the hard
  structure is cut to the **as-built** space, not the nominal model.
- **Work from the walls inward, optics last.** Structure and services are installed while the
  tray zone is open; the film plane / pinhole / light trap go in last to stay clean and true.
- **No trapped work.** Each step leaves access for the next (e.g. plumb before the walkway
  caps the corridor). Dependency conflicts surface in the §8 click-through, not on site.

---

## 4. Phase 1 — Geometry Set-Out

**Goal:** install the fixed masses that establish the camera's internal datum.

| # | Step | Depends on | Status |
|---|------|-----------|:------:|
| 1.1 | Install the **IBC frame posts** (upright skeleton + feet) + **plumbing-panel backing** | — | ☐ |
| 1.2 | Install 2× IBC totes on the **pinhole wall** (near column) — dropped into the post skeleton | 1.1 | ☐ |
| 1.3 | Install the **panel equipment** (pumps/filters/valves) + **plumb the IBC corridor** (corridor lines only — *sump + supports → 3.2*) + run the filter skid's **blue recycle** and **gray waste** corridor lines to the IBC panel + run the **purple Cct-C corridor pump wiring** to the pinhole wall (*EP drop connected in 4.3*) | 1.2 | ☐ |
| 1.4 | Install **Fan A** (exhaust) + run its **Cct-A cable** along the pinhole-wall trunk and **down to the EP drop** (EP itself lands in Phase 4) — *before the far IBCs bury it* | 1.2 | ☐ |
| 1.5 | Install 2× IBC totes on the **far wall** (far column), then fit the **frame rails + retaining bars** to trap all totes | 1.4 | ☐ |
| 1.6 | Install the **hinge panel** (light-trap door — *excluding* the light-trap drum) | 1.2 | ☐ |

**Exit gate:** frame square, totes restrained, IBC plumbing pressure-checked.

---

## 5. Phase 2 — Re-measure

**Goal:** capture the **actual** space remaining after the fixed masses are in, before any
hard structure is committed.

| # | Step | Depends on | Status |
|---|------|-----------|:------:|
| 2.1 | **Re-measure the actual space left** — reconcile against the model; note deltas | Phase 1 complete | ☐ |

**Exit gate:** as-built clearances confirmed; designs refined; any cut-lists adjusted to the measured space.

---

## 6. Phase 3 — Framing

**Goal:** fit the load-bearing perimeter structure, the processing tray, the remaining
plumbing, the film-plane support, and the walkway.

| # | Step | Depends on | Status |
|---|------|-----------|:------:|
| 3.1 | Install the **pinhole-wall ply backing** (mounts the filter skid; shown as a semi-transparent, plywood-colored backdrop for the plumbing build — ghosts like all prior geometry from Phase 4 on) | Phase 2 | ☐ |
| 3.2 | Install **cantilevers on the far + right walls** | Phase 2 | ☐ |
| 3.3 | Install **cantilevers on the near wall** | 3.2 | ☐ |
| 3.4 | Lay the **under-grate ribbons** (sump line + skid ribbon legs — tray-sump→P-04 suction, DV-02 waste, P-02→ACC-02 — + pipe support beams) **and install the pinhole filter skid** (F-1..F-3 + P-04/SV-02/DV-02 + ACC-02 + skid-side plumbing; mounts to the 3.1 backing; connects to the recycle→IBC-3 + waste returns from 1.3) — *span the space, so after the beams and both cantilever sets, before the grate*; Note: Before the pipes can be glued, the walkway has to be test-fitted to locate the holes for the pipe bump-through. | 3.1, 3.2, 3.3 | ☐ |
| 3.5 | **Extend plumbing** to the pinhole-wall panel | 3.4 | ☐ |
| 3.6 | Install the **processing tray** | 3.2 | ☐ |
| 3.7 | Install the **film-plane beams** + **combined corner plates** (FP ↔ right-walkway) | 3.2 | ☐ |
| 3.8 | Install the **left cantilevers** | 3.4 | ☐ |
| 3.9 | Install the **walkway** (grating on all cantilevers) | 3.3, 3.4, 3.7, 3.8 | ☐ |

**Exit gate:** walkway decked, tray sealed, perimeter proof-loaded.

---

## 7. Phase 4 — Electrical

**Goal:** install the power panels, lighting, and all wiring runs.

| # | Step | Depends on | Status |
|---|------|-----------|:------:|
| 4.1 | Mount the **external power panel** (PV + E-stop) | Phase 3 | ☐ |
| 4.2 | Install the **interior electrical panel** + batteries | 4.1 | ☐ |
| 4.3 | **Connect the Cct-C corridor wiring to the EP** (the corridor run was pre-installed to the pinhole wall in 1.3 — this closes the EP drop) | 4.2 | ☐ |
| 4.4 | **Hang the lights** | Phase 3 | ☐ |
| 4.5 | **Run / wire the electrical paths** — IBC pumps, filter, lights, fans, etc. (circuits Blue / Brown / Black) | 4.2, 4.3, 4.4 | ☐ |

**Exit gate:** every circuit terminated, continuity + insulation tested, E-stops verified.

---

## 8. Phase 5 — Photo System

**Goal:** install the precision optical elements last, into the known as-built space.

| # | Step | Depends on | Status |
|---|------|-----------|:------:|
| 5.1 | Install the **pinhole mechanism** (plate + aperture) | Phase 3 | ☐ |
| 5.2 | Install the **film plane + carriages** | Phase 3 (beams), 5.1 | ☐ |
| 5.3 | Install the **light trap** (drum into the hinge panel) | Phase 1 (panel), 5.2 | ☐ |
| 5.4 | Install the **spray bar** (over the processing tray) | Phase 3 (tray) | ☐ |

**Exit gate:** plane travels through its full tilt/swing envelope; spray bar moveemnt is free; camera confirmed light-tight.

---

## 9. Construction Model (3D, phased)

The build order is verified by a dedicated **phased 3D model** — the same component builders
as the Overview 3D model, staged by install order:

- **One scene per phase** (Phase 1 … Phase 5) — the model shown at the end of that phase.
- **Click-to-build within a scene** — a Dynamic Component reveals each step's geometry in
  order on click, so the assembly can be watched building up and the sequence checked for
  trapped work / access conflicts before the real build.

With the Interact tool, each phase scene opens showing only its first step; each click reveals the
next in install order (drag to orbit, scroll to zoom). Model-generation internals are documented in
[component-dependency-map.md](component-dependency-map.md) §3.1 (the `construction` model row).

<!-- brochure:skip -->
<div class="sketchfab-embed-wrapper">
  <div style="position:relative;width:100%;padding-bottom:56.25%;">
    <iframe title="TBS-001 Construction Sequence" frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" execution-while-out-of-viewport execution-while-not-rendered web-share src="https://sketchfab.com/models/dcc54fb3d02e46c3ab070dd49adc5d1e/embed" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"></iframe>
  </div>
  <p style="font-size: 13px; font-weight: normal; margin: 5px; color: #4A4A4A;"><a href="https://sketchfab.com/3d-models/tbs-001-construction-sequence-dcc54fb3d02e46c3ab070dd49adc5d1e?utm_medium=embed&utm_campaign=share-popup&utm_content=dcc54fb3d02e46c3ab070dd49adc5d1e" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">TBS-001 Construction Sequence</a> by <a href="https://sketchfab.com/alvin91403?utm_medium=embed&utm_campaign=share-popup&utm_content=dcc54fb3d02e46c3ab070dd49adc5d1e" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">alvin91403</a> on <a href="https://sketchfab.com?utm_medium=embed&utm_campaign=share-popup&utm_content=dcc54fb3d02e46c3ab070dd49adc5d1e" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">Sketchfab</a></p>
</div>
<!-- brochure:endskip -->

