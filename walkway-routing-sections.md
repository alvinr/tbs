# Right Walkway — Pipe Routing Sections

The corridor plumbing threads a tight zone at the IBC end of the container, where the
**right walkway**, the **processing tray**, the **IBC restraint frame** and the **pump
column** all compete for space. This document is a set of **cross‑sections** that walk
from the pinhole wall across to the plumbing corridor, so the clear routing envelope a
pipe actually has at each depth is legible — and so the points where a pipe shares space
with structure are visible.

These sections are the companion to the [Plumbing](plumbing-report.md) report; the pipe
positions are read off the 3D water model (`water.skp`) and drawn 1:1.

## How to read these

All five sections are **longitudinal X–Z elevations, looking along +Yd** (down the length
of the container), cut at increasing **Yd** depth — so together they scan from the pinhole
wall (Yd 0) across to the plumbing corridor (Yd ≈ 1046–1316):

| Section | Cut (Yd) | What it shows |
|--------|---------|---------------|
| **B‑B** | ≈ 62 (near‑rim strip) | the two supply/return lines running *under* the deck, ducking the support beams |
| **C‑C** | ≈ 523 (mid‑tray) | the tray is a no‑route zone — pipes only *cross* the plane at the gap |
| **D‑D** | ≈ 1066 (near cantilever) | the available space, the foot under the tray, and the four pipes crossing the perimeter/gap |
| **E‑E** | ≈ 1130–1245 (corridor centre) | the four corridor lanes as real in‑plane runs toward the pumps |
| **F‑F** | ≈ 1286 (far cantilever) | the far cantilever, mirroring D‑D |

Coordinate system (per the drawing standard): **X** = length (0 at the cargo‑door end wall,
5893 at the sealed end), **Yd** = depth from the pinhole wall (0) into the container, **Z** =
height above the floor.

## Section B‑B — near‑rim strip, under the walkway

![TBS-001 — Walkway Routing Section B-B: near-rim strip under the right walkway](assets/walkway-sections-sheet1.png)

Cut through the **Yd ≈ 56–69 strip** butted under the tray near rim, where two lines run the
length of the container **beneath the walkway grate**: the **ACC‑01 → spray‑bar blue supply**
(Z40) and the **IBC‑3 → P‑02 brown return** (Z10). Both clear under the deck's two 40 × 40
Yd‑running support beams (Z80–115), and turn up into the corridor at the tray↔IBC gap.

## Section C‑C — midway (pinhole wall ↔ corridor)

![TBS-001 — Walkway Routing Section C-C: midway, mid-tray](assets/walkway-sections-sheet2.png)

The same cut moved to mid‑tray depth (Yd ≈ 523). Here the plane is **inside the processing
tray**, which is a no‑route exclusion zone — so no pipe runs along the length. The only pipes
present are the two that **cross the plane in Yd at the tray↔IBC gap (X4641)**, reading as
cross‑section circles. They are the same two lines that run in‑plane in B‑B.

## Section D‑D — through the near cantilever

![TBS-001 — Walkway Routing Section D-D: through the near cantilever](assets/walkway-sections-sheet3.png)

Cut through the **near cantilever (Yd ≈ 1066)**. The corridor restraint is the deep 4‑leg box:
its **front upright is at X4654** and its **front foot (150 × 150) runs X4604–4754 — extending
25 mm under the tray**. The walkway support (cantilever arm at Z70–115 plus the hatched long
bearers at Z80–115) carries the deck.

Four pipes cross this plane at the perimeter/gap, with the deck between them:

- **Above the deck** — blue filtered return (SV‑01 → DV‑01, Z235) and brown sump return
  (tray sump → P‑04, Z205), riding proud of the grate;
- **Below the deck** — blue → TAP‑01 (Z60) and brown → P‑02 / BV‑03 (Z25), threading the
  **tight 25 mm gap between the tray rim (X4629) and the front upright (X4654)** with only
  ≈ 1.5 mm and ≈ 2.5 mm clearance.

The corridor lanes (blue trunk, grey waste, blue recycle) run *in X* down the corridor at
Yd 1101–1241 — they appear in‑plane in E‑E.

## Section E‑E — corridor centre

![TBS-001 — Walkway Routing Section E-E: corridor centre, between the frame uprights](assets/walkway-sections-sheet4.png)

A thick‑slab section through the **clear span between the frame uprights (Yd ≈ 1130–1245)**,
where the four corridor lanes run in X toward the pump column: the brown P‑04 suction (Z205,
rising into P‑04) and the blue trunk / grey waste / blue recycle (all co‑planar at Z235, drawn
stacked for clarity). No IBC ring rail crosses this span, so the corridor is open above the
bottom rail.

## Section F‑F — through the far cantilever

![TBS-001 — Walkway Routing Section F-F: through the far cantilever](assets/walkway-sections-sheet5.png)

The mirror of D‑D on the far side of the corridor (Yd ≈ 1286): the far cantilever arm and far
foot (again extending under the tray). No under‑deck crossers reach this far — they turn up by
Yd 1132–1170 — so the nearest lane is the blue DV‑01 recycle, ghosted just −Yd of the plane.

## Interference & clearance findings

Drawing these sections at 1:1 against `water.skp` surfaced four tight‑clearance / interference
items that the plan views do not reveal. Each is a **3D‑model follow‑up to verify or resolve**:

1. **Blue TAP‑01 crosser grazes the cantilever‑arm soffit.** At the near cantilever the blue
   supply/TAP‑01 line runs at Z60; its top (Z70.5) meets the cantilever‑arm soffit (Z70). The
   line runs at Z40 in the near‑rim strip (B‑B), so there is headroom to drop it a few mm
   through the gap.
2. **Low crossers pinch the tray‑rim ↔ upright gap.** The two under‑deck lines thread the
   25 mm gap between the tray rim (X4629) and the front upright (X4654) with only ≈ 1.5 mm
   (to the rim) and ≈ 2.5 mm (to the upright).
3. **Front foot + M12 anchor under the tray basin.** The deep‑box front foot (X4604–4754) and
   its inner M12 anchor row (≈ X4629) sit under the tray at X4604–4629 — confirm there is no
   clash with the tray basin.
4. **Stale cantilever‑arm reference.** The right‑walkway cantilever arm reaches X4734
   (`RWK_X_UP`), which references the *old* IBC upright position; the deep‑box frame upright is
   now at X4654. Reconcile the arm's attachment.
