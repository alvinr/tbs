<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Construction Sequence — TBS-001

## 1. Purpose

This report is the **build order of record** for TBS-001 — the sequence in which the camera
is assembled inside the container, why that order is forced, and the gate that must be met
before each phase begins. The install is **geometry-first**: the large fixed masses (the IBC
totes and their frame) go in first and set the datum everything else is measured from; the
precision optical system goes in last, once the real, as-built space is known.

The sequence is validated by a **phased 3D construction model** (§8) — one scene per phase,
with a click-through that reveals each step in order — so the order can be walked before any
steel is cut.

> **Scaffolding:** this document is a skeleton. Per-step prerequisites, tools/crew, clearances,
> and sign-off criteria are **TBD** and filled as each phase is detailed. Locations stay
> qualitative here; exact coordinates live in the diagrams-of-record.

---

## 2. Build Overview

| Phase | Name | Goal | Exit gate (before next phase) |
|-------|------|------|-------------------------------|
| **1** | Geometry set-out | Install the fixed masses that fix the datum | IBC frame + totes plumbed and square; hinge panel hung |
| **2** | Re-measure | Capture the **as-built** space before committing hard structure | Measured clearances reconciled against the model — TBD |
| **3** | Hard install | Fit the tray, cantilevers, plumbing, film-plane beams, walkway | Walkway + tray in; perimeter structure loaded — TBD |
| **4** | Electrical | Panels, lights, and all wiring runs | Circuits terminated + tested (Blue / Brown / Black) — TBD |
| **5** | Photo system | Film plane, pinhole mechanism, light trap | Camera light-tight and operable — TBD |

---

## 3. Sequencing Principles

_TBD — the "why this order" rationale. Placeholders:_

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
| 1.1 | Install 2× IBC totes on the **pinhole wall** (near column) | — | ☐ |
| 1.2 | Install the **IBC frame** (restraint deep-box) | 1.1 | ☐ |
| 1.3 | Install + **plumb the IBC corridor** through to the walkway line | 1.2 | ☐ |
| 1.4 | Install **Fan A** (exhaust) + its **Cct-A electrical** on the pinhole wall — *before the far IBCs bury it* | 1.2 | ☐ |
| 1.5 | Run the **corridor pump wiring (Cct C)** to the pinhole wall — *before the far IBCs block the wall* | 1.3 | ☐ |
| 1.6 | Install 2× IBC totes on the **far wall** (far column) + **finalize IBC plumbing** | 1.5 | ☐ |
| 1.7 | Install the **hinge panel** (light-trap door — *excluding* the light-trap drum) | 1.2 | ☐ |

**Exit gate:** _TBD — frame square, totes restrained, IBC plumbing pressure-checked._

---

## 5. Phase 2 — Re-measure

**Goal:** capture the **actual** space remaining after the fixed masses are in, before any
hard structure is committed.

| # | Step | Depends on | Status |
|---|------|-----------|:------:|
| 2.1 | **Re-measure the actual space left** — reconcile against the model; note deltas | Phase 1 complete | ☐ |

**Exit gate:** _TBD — as-built clearances confirmed; any cut-lists adjusted to the measured space._

---

## 6. Phase 3 — Hard Install

**Goal:** fit the load-bearing perimeter structure, the processing tray, the remaining
plumbing, the film-plane support, and the walkway.

| # | Step | Depends on | Status |
|---|------|-----------|:------:|
| 3.1 | Install **cantilevers on the far + right walls** | Phase 2 | ☐ |
| 3.2 | Install the **processing tray** | 3.1 | ☐ |
| 3.3 | Install **cantilevers on the near wall** | 3.2 | ☐ |
| 3.4 | **Extend plumbing** to the pinhole-wall panel | 3.3 | ☐ |
| 3.5 | Install the **pinhole filter skid** | 3.4 | ☐ |
| 3.6 | Install the **film-plane beams** | 3.1 | ☐ |
| 3.7 | Install the **left cantilevers** | 3.2 | ☐ |
| 3.8 | Install the **walkway** (grating on all cantilevers) | 3.3, 3.6, 3.7 | ☐ |

**Exit gate:** _TBD — walkway decked, tray sealed, perimeter proof-loaded._

---

## 7. Phase 4 — Electrical

**Goal:** install the power panels, lighting, and all wiring runs.

| # | Step | Depends on | Status |
|---|------|-----------|:------:|
| 4.1 | Install the **electrical panel** (interior) | Phase 3 | ☐ |
| 4.2 | Install the **external electrical panel** | 4.1 | ☐ |
| 4.3 | **Hang the lights** | Phase 3 | ☐ |
| 4.4 | **Run / wire the electrical paths** — IBC pumps, filter, lights, fans, etc. (circuits Blue / Brown / Black) | 4.1, 4.2, 4.3 | ☐ |

**Exit gate:** _TBD — every circuit terminated, continuity + insulation tested, E-stops verified._

---

## 8. Phase 5 — Photo System

**Goal:** install the precision optical elements last, into the known as-built space.

| # | Step | Depends on | Status |
|---|------|-----------|:------:|
| 5.1 | Install the **film plane + carriages** | Phase 3 (beams) | ☐ |
| 5.2 | Install the **pinhole mechanism** | 5.1 | ☐ |
| 5.3 | Install the **light trap** (drum into the hinge panel) | Phase 1 (panel), 5.1 | ☐ |

**Exit gate:** _TBD — plane travels through its full tilt/swing envelope; camera confirmed light-tight._

---

## 9. Construction Model (3D, phased)

The build order is verified by a dedicated **phased 3D model** — the same component builders
as the Overview 3D model, staged by install order:

- **One scene per phase** (Phase 1 … Phase 5) — the model shown at the end of that phase.
- **Click-to-build within a scene** — a Dynamic Component reveals each step's geometry in
  order on click, so the assembly can be watched building up and the sequence checked for
  trapped work / access conflicts before the real build.

**Interactive 3D model** — `construction.skp` (`generate_construction_model.py`), reusing the
Overview component builders. Each phase is a **click-to-build Dynamic Component**: with the
Interact tool, click a phase's assembly and each click reveals the next sub-step in install order.
The model defaults to **fully built**, so any phase scene shows the prior phases complete — clicking
a phase replays *its* build while the phases before it stay done. Drag to orbit, scroll to zoom.

_Phases 1 and 3 are click-to-build DCs (the IBC totes split near/far, the wall brackets split
near/far, and the film-plane rails/beams split from the plane, so the step order matches this
report). Phases 4–5 are next._

<!-- brochure:skip -->
<div class="sketchfab-embed-wrapper">
  <div style="position:relative;width:100%;padding-bottom:56.25%;">
    <iframe title="TBS-001 Construction Sequence" frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" execution-while-out-of-viewport execution-while-not-rendered web-share src="https://sketchfab.com/models/dcc54fb3d02e46c3ab070dd49adc5d1e/embed" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"></iframe>
  </div>
  <p style="font-size: 13px; font-weight: normal; margin: 5px; color: #4A4A4A;"><a href="https://sketchfab.com/3d-models/tbs-001-construction-sequence-dcc54fb3d02e46c3ab070dd49adc5d1e?utm_medium=embed&utm_campaign=share-popup&utm_content=dcc54fb3d02e46c3ab070dd49adc5d1e" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">TBS-001 Construction Sequence</a> by <a href="https://sketchfab.com/alvin91403?utm_medium=embed&utm_campaign=share-popup&utm_content=dcc54fb3d02e46c3ab070dd49adc5d1e" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">alvin91403</a> on <a href="https://sketchfab.com?utm_medium=embed&utm_campaign=share-popup&utm_content=dcc54fb3d02e46c3ab070dd49adc5d1e" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">Sketchfab</a></p>
</div>
<!-- brochure:endskip -->

---

## 10. Source References

_TBD — cross-links to the owning subsystem reports (IBC, plumbing, walkway, electrical,
film-plane, light-trap) and any install-specific standards as the phases are detailed._
