<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# TBS-001 — Light-Trap Punch-Out Bay (Design Spec)

> **Status:** Draft for review · **Date:** 2026-06-05 · **Branch:** `lighttrap-refactor`
> Brainstorm output. No implementation until this spec is approved; all implementation lands on `lighttrap-refactor` and is kept off `main` until ready to merge.

## 1. Problem

The rev-8 personnel light-lock is a **fixed Ø900 housing + revolving C-shell drum** at the cargo-door end (drum center X=0, Yd center 1181, Z 80–2280). Two interferences were flagged against the film plane:

1. Does the drum + fan duct shadow the light cone?
2. In the "camera" position, does the drum block the film-plane rails and limit tilt/swing/shift?

### 1.1 Analysis findings (ray-trace + geometry, against `tbs_constants`)

- **#1 — shadow: RULED OUT.** The pinhole sits at X=2399 and the film plane spans X=150–4649, so the imaging cone fans out entirely on the **+X side**. The drum is centered at **X=0** — off to the side. Ray-trace: **0 % of the film plane is shadowed**; the leftmost ray (to X=150) clears the drum center by **869 mm** against a 450 mm radius (419 mm margin). A film point would need X ≈ −1000 for its ray to graze the drum — outside the plane. The fan duct is also at X≈0 → clears. Holds at every film-plane depth (rays angle toward X=2399, never going "straight back" past the drum).
- **#2 — rail / tilt-swing interference: REAL and significant.** The Ø900 housing interior reaches **X=+450**; the left film-plane rail is at **X=150** — a **300 mm overlap** across the drum's Yd band (731–1631). The left film-plane corners cannot enter that band, so at the nominal Yd=2262: left-side forward travel **631 mm** vs the right side's full 2162 mm, and **left-edge swing is capped at ~8° vs the ~25.7° design max — ~69 % of the swing-toward-drum lost.**

## 2. Goal

Restore **full, symmetric film-plane movement** (recover the lost tilt/swing/shift) **without reducing the film-plane image size** (the project's core goal), and ideally **simplify** the mechanism.

## 3. Options considered

| Option | Verdict |
|---|---|
| **A** — reduce film-plane size | **Ruled out** — defeats the project's core goal. |
| **B** — offset the whole assembly + extend the ceiling rails externally past the doors | Viable, but the **closed-door transport** requirement forces a *removable external rail section* — a new failure point, a setup chore, and a light/weather gap to seal. Superseded by B2. |
| **B2** — light-trap **punch-out bay** | **CHOSEN.** Achieves the offset via a forward-protruding bay in the panel; rails stay internal; structure localized to the panel. |
| **C** — cap the film-plane forward travel at the drum | **Documented fallback only.** Simplest, but cuts focus/tilt travel to **29 %** of range (631 mm of 2162 mm). Use only if B2's bay/hinge structure proves infeasible. |

## 4. Chosen design — B2 + hybrid plastic-skinned drum/housing

### 4.1 Geometry
- Drum center **0 → −400 mm** (key tunable: ≥300 mm to clear the rail, ~400 mm for ~100 mm working margin). Housing X-span becomes **−850 … +50**; interior edge **+50** clears the X=150 left rail by **~100 mm**.
- The bay protrudes **~850 mm** past the door plane (vs ~450 mm today). **Panel side zones stay at the door plane.**
- The hinged panel's **center zone becomes a forward-protruding rigid box (the bay)** enclosing the housing.

### 4.2 Film-plane rails — the "removable" concept splits cleanly
- **Operating:** left rails (TL + BL) are **continuous** — the demountable drum-zone *segment* (Yd 731–1631) is **deleted** (the drum no longer touches X=150). Full-length rails, full travel, simpler than today.
- **Transport:** the **whole left rails (TL + BL) lift out** as part of the film-plane knock-down, so the panel can slide deep past X=150. A teardown step, not an operating burden.

### 4.3 Bay structure — three load cases, one answer
The bay / panel / hinge / suspension must carry:
1. **Hung from the rails** with the forward cantilever — ~99 kg core ~400 mm forward ≈ **40 kg·m** moment.
2. **Swung open on the hinges** — ~316 kg leaf, 2.3 m wide, 180°: sag + a forward-tipping couple the bay's forward offset aggravates.
3. **The transport slide.**

Shared answer: a **torsionally stiff bay box** continuous with the panel frame, a **reinforced hinge stile**, a **stiffer suspension reaction** (brackets / tie-back / bottom roller — selected in structural analysis, §5 item 2), and a **swing-support caster**.

### 4.4 Hinge & swing-out
- Current: **3× 200 mm SS ball-bearing piano hinges, left edge (Yd=0), 180° outward swing** (loading access + emergency egress).
- The bay adds mass + a forward offset → **upgrade the hinges** (heavy-duty barrel/strap, sized for ~316 kg + the tipping couple; the 3× piano hinges may already be marginal pre-bay), add a **retractable swing-support caster** at the leaf's far-bottom / bay corner to take sag + tip off the hinges, and optionally a **gas-strut/counterbalance** so one person can swing a ~285–316 kg leaf.

### 4.5 Drum/housing material — hybrid plastic skin
- **Keep metal:** end caps, stub shafts, SKF 6215 bearings, 1–2 hoops (structure, rotating precision, bearing mounts).
- **Swap the curved skin to 4–6 mm opaque black plastic:** UV-stabilized (carbon-black) HDPE/PP for the weather-exposed housing; HDPE/PP or ABS for the drum. Ø432–450 mm radius cold-forms/thermoforms easily and bolts/rivets to the hoops or hot-air welds — simpler and cheaper than rolling + welding aluminum.
- **Weight:** ~36 kg off the skins; net **~25–35 kg** after hoop support → light-trap core ~99 → **~65–75 kg**, easing all three load cases (lighter swing leaf, smaller cantilever moment, lighter hinge/caster duty).

### 4.6 Transport
- Sequence: strike the film plane (brace cage + left rails out) → slide panel+bay deep (**~850–900 mm**) so the bay clears behind the door plane → **cargo doors close**.
- `PANEL_SLIDE` **550 → ~880**.
- **Transport-envelope interference check** (panel+bay slid to X≈30–1000, Z 80–2300, full Yd; housing central Yd 731–1631). Cleared: batteries / electrical / solar (all X≥1600, past the envelope), processing tray + near/far walkway gratings (housing passes *over* them on the 80 mm floor gap, as today), evap-cooler duct penetration (X≈1200). **One conflict:** the near/far **walkway cantilever brackets** — first legs at **X=698** (Z 0–150). The *current* slide stops at X≈670, deliberately just shy of them; B2's deeper slide passes them, so the panel's lower wall-edge corners would clip the bracket legs. **Resolution:** make the door-end near/far brackets (X≈698, possibly 1155) **demountable for transport** — a small addition to the existing transport teardown (film plane + left rails + left walkway already come out). Alternative: notch the panel's lower wall corners (Z 80–150) — rejected unless the bracket-removal proves awkward, because it complicates the panel bottom seal.

### 4.7 Sealing
- Light-tight + IP44 weather wrap follows the deeper bay; the fixed door-frame and the interface-1 (panel-perimeter) + interface-2 (housing-surround) EPDM seals re-map onto the bay geometry.

### 4.8 Centre of gravity
- The light-trap core is ~99 kg (lighter with plastic) of **3,386 kg dry**. First-order: operating CG shifts **~15–20 mm toward the cargo door**; transport CG shifts **~20 mm rearward** (deeper slide, mildly favorable vs the current front bias). Both **< 25 mm**, well within the existing ~685 mm state-to-state migration the axle placement already absorbs. **Not a blocker.** Re-run the full weight/CG model during implementation.

## 5. Open engineering tasks (resolve during implementation / structural analysis)
1. **Exact offset** (300 mm min / ~400 mm nominal) and bay dimensions.
2. **Suspension reaction** for the cantilever moment — stiffer brackets vs upper tie-back vs bottom guide roller.
3. **Hinge sizing + swing-support caster** for the ~316 kg leaf and tipping couple; optional strut assist.
4. **Plastic skin** — thickness, grade (UV + FR), hoop spacing, **thermal running-clearance** (CTE ~10× aluminum across Ø900), light-tight joints + **darkroom light-tightness test**.
5. **Re-run weight/CG** with the bay + lighter core + heavier hinges/caster.
6. **Transport-envelope interference** — make the door-end near/far walkway brackets (X≈698, possibly 1155) demountable for transport (see §4.6); confirm no clip against the panel's lower wall corners across the full slide.

## 6. Change footprint (implementation scope)
- **Constants (`tbs_constants.py`):** `DRUM_CX` 0→−400, `PANEL_SLIDE` 550→~880, **delete `BRACE_LEFT_DEMOUNT_Y0/Y1`**, add bay-geometry constants (and possibly drum/housing material + thickness), seal positions.
- **3D models:** `lighttrap`, `lighttrap-transport`, `overview` (bay, continuous left rails, deeper slide, lighter material).
- **2D diagrams:** `film-plane-mechanism` (continuous rails), `hingepanel` (the bay), `lighttrap`, `floorplan`, `walkway` (door-end brackets demountable for transport).
- **Reports / lists:** `hinged-panel-report`, `light-trap-selection`, `weight-distribution-report` (re-run CG), a structural note on the bay cantilever + hinge, `master-shopping-list` + `project-cost-breakdown` (plastic skin, heavy hinges, caster).

## 7. Verification
- `check_consistency.py` after each geometry/constant change.
- Re-render affected 2D diagrams (byte-compare unaffected ones); rebuild affected SketchUp models — **gate on the active-doc path before every `--send`** (lesson from this session).
- Re-run the weight/CG analysis and update the report.
- Reason through (and test) light-tightness for the plastic skin joints + the re-mapped bay seals.

## 8. Out of scope / explicitly unchanged
- **Film-plane (image) size** — unchanged (this is the whole point).
- **Optical constants** — pinhole Ø/position, focal length, f-number.
- **Options A and C** — A is rejected; C remains a documented fallback only.
