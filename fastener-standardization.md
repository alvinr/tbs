<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
<!-- Working/internal decision record — NOT published (not registered in publish.sh). -->
# Fastener Standardization — Decision Record (TBS-001)

**Goal:** build and maintain the camera from the fewest distinct fastener
**size × length × material × head** combinations, without compromising any load path.
Fewer thread *families* first; then the fewest *lengths* within each family.

Source of record: `parts.py`. Compiled 2026-09-04 from the `fasteners-hardware` category
plus threads bundled in structural / labor lots. Companion analysis (length ladders +
redesign levers): the [Fastener Standardization artifact](https://claude.ai/code/artifact/3819bc01-d4d8-42a7-8d58-4e90a25fb3d2).

**Status:** decisions made (Alvin, 2026-09-04). Most require blueprint-level re-engineering and are
**gated on the owning drawing set** — see the per-family gate. Executed now on branch `fastener-rework`:
the **M6 nut consolidation** (3 → 2 — the one change needing no new geometry). Every other decision, and the
itemization of the BOM gaps, is captured here for its blueprint round (each blocked on a length dim we should
confirm, not assume).

---

## Target end state

Metric thread families **6 → 4**: **M6 · M8 · M12 · M4** (M5 and M10 both eliminated).
Metric bolt lengths **~12 → ~7** as the grip-stack standardizations land.

## Per-family decisions

### M12 — force the wall joints to one length (Lever B)
The 65/70 split is *grip-justified today* (hanger ~40 mm vs cleat ~54 mm), so it is not a free merge.
**Decision:** standardize the wall-joint grip stacks — uniform backing-plate + flange thicknesses,
designed to the 30 mm-corrugation max — so the hanger / cleat / corner-plate joints share **one grip →
one wall length**; keep **M12×100** for the deep J6 arm joint. Unify the **×65 zinc/SS** material.
Itemize the pivot anchors + hinge brackets (see gaps).
- **Gate:** IBC-frame + walkway blueprints (grip stack + backing-plate thicknesses).
- **Verify:** the single wall length falls out of the standardized grip (likely ×70 + small shim allowance);
  the J2/J7 bar joint (~58 mm) either shares it or gets the crush-sleeve short-grip redesign.

### M10 — eliminate entirely → M12
Every M10 here is *our* choice, not bearing-dictated (the ring/collar taps into our own Ø240 mount plate).
**Decision:** bump the cap-hub (4×, Ø120 PCD), the ring/collar (14×) and the door-frame through-bolt all to
**M12**; delete the M10 family.
- **Nuance:** those M10 joints are *countersunk machine screws*, so M12 gains short CSK variants alongside its
  structural hex bolts — the win is removing a whole thread size (no M10 tap/drill/stock), not a length cut.
- **Gate:** light-trap + hinged-panel (door frame) blueprints.
- **Verify (tight one):** M12 edge-distance on the **8 mm 6061-T6 cap** at the Ø120 hub PCD; re-tap the
  mount plate + hub flange to M12.

### M8 — one hex length, zinc standard with a wet-zone SS exception
The hex M8 is already **×25** everywhere; the only split is material.
**Decision:** **zinc M8×25** as the standard (shelf, stays, edge-channel); **304 SS exception for the wet
film-plane zone** — the **carriage** *and* the ICP-14 **rail-fixing** (`bolt-m8-fixing`, already SS-upgraded
2026-08-13 for the same "film plane wets" reason). The spray-saddle **thumbscrew** and stile-plug **grub
set-screws** are different head classes — they stay.
- **Gate:** film-plane blueprint (carriage material + confirm edge-channel/carriage land on ×25).

### M6 — consolidate the easy axes (Option A) — *doing now*
**Decision:** nuts **3 → 2** — the 4× plain (electrical panel mount) → **nyloc**; keep the serrated **flange**
nut on the tray (it spreads clamp load on the thin 1.5 mm panel). Keep **both lengths** (×16 tray 4 mm lap /
×20 carriage-clamp) and the **316/304 material split** (tray 316 was a deliberate keep — the wash is
chloride-free). Absorbs the retired M5 at ×16.
- **Now:** the nut merge is a registry change (no geometry) — executed on `fastener-rework`.

### M5 — retire the family → M6×16 CSK
M5×16 CSK (film-clamp clips + ply attach, 8 off) is the only M5 in the camera.
**Decision:** retire it into a new **M6×16 countersunk** SKU (flush head — can't protrude into the film).
SKU-neutral, but removes the M5 tap/driver/stock.
- **Gate:** film-plane blueprint (next round).
- **Verify:** the clamp-clip counterbore + edge distance take the bigger M6 CSK head (~12 mm vs ~10 mm).

### M4 — itemize and keep — *itemizing now (clean parts only)*
M4 is not a free choice: the cam-clamp base holes are **vendor-fixed** at M4×0.7 (McMaster 5128A63) and the
pinhole grubs are an optical-precision detail. Not worth a vendor swap + optical redesign for ~31 tiny screws.
**Decision:** close the BOM gap (itemize) and keep the family; merge the two M4 lengths if the grub + cam
screw can share one.
- **Gate:** both lengths are blueprint dims — the grub firms with the optics/pinhole ring counterbore, the
  cam-clamp mount screws with the film-plane carriage mount detail. Itemize per those sheets.

---

## Redesign levers (how a length actually collapses)
- **A · Shim up** *(free)* — buy the longer length, pad thinner joints with washers to a common grip. Already
  the M12 wall-bolt plan ("pad 1–2 washers").
- **B · Standardize the stack** — make clamped members a common thickness so a family lands on one grip.
- **C · Fold a lone size into a neighbor** *(no new part)* — M5×16 → M6×16, ⁵⁄₁₆″ → ¼″.
- **D · Resize a member** — thicken a plate / add a boss / shorten a tube so its bolt hits the standard.

## Related (from the opportunity list, outside the 6 metric families)
- **Ply-mount ⁵⁄₁₆″ → ¼″-20:** the ⁵⁄₁₆″ tee-nut + machine screw exist only for the 3 filter housings.
  Collapse into ¼″-20 (the ply-mount standard) — verify the Pentair 150061 bracket ears take ¼″. *(−2 SKUs)*
- **#14 self-drillers 4 → 2:** unify the two 410-SS structural anchors to one length; unify the two plain TEKs.
- **⅛″ blind rivets:** test whether one grip range spans both the shell-cap and housing-frame laps (2 → 1).

## Itemization — BOM gaps (fasteners used but not discrete SKUs)
Every gap is blocked on the same thing: the **length is a blueprint dim** we should confirm, not assume
(house rule — validate dims vs the datasheet). So itemization firms per its owning sheet; captured here so
the count/cost gap is tracked, not fabricated.

| Thread | Where | Length blocked on |
|--------|-------|-------------------|
| M4 grub ×3 | pinhole retaining ring | the ring counterbore depth (optics detail) |
| M4×0.7 ×24 | cam-clamp bases → carriage | the carriage mount detail (film-plane) |
| M12 anchors ×12 | pivot floor/roof mount plates | the floor cross-member / roof-rail engagement (Sheet 10) |
| M12 ×6 | pivot hinge brackets → jamb | likely an existing M12 length — confirm at blueprint |
| M10 (all) | light-trap + door | **moot** — being eliminated → M12 |

## The model to copy
The M12 *fasteners* are already single-SKU across the whole camera — one plain nut (127 off), one flat washer
(508), one lock washer (127) — because the grips were made to match. Apply that discipline to the lengths and
the end state is ~7 metric bolt lengths (from ~12), ≈ −7 SKUs, M5 + M10 families gone — every change a
grip/load check away, none of it touching a load path it shouldn't.
