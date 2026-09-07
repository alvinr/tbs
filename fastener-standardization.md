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

Metric thread families **6 today; target 5**: **M4 · M6 · M8 · M10 · M12** once M5 retires — **M5 retirement is
DEFERRED** to the chem-shelf design (now via a flange nut, not an M6×16 CSK); **M10 KEPT** as a justified
single-CSK family (the light-trap's thin hosts preclude M12, see below).
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

### M10 — KEEP as a justified single-CSK family (2026-09-07 host check reversed the earlier "eliminate → M12")
The earlier plan was to bump every M10 → M12. A host-by-host countersink-depth check (2026-09-07) reversed it:
the light-trap's M10 CSK screws seat in **thin hosts that can't take an M12 flat head** —
- **F1 cap→flange (8×) + F4 stile→cap (2×):** flush CSK in the **8 mm 6061-T6 cap** — an M12 CSK (~6.8 mm sink)
  leaves only ~1 mm of aluminum under the cone (M10 leaves ~2.5 mm). Heads MUST be flush — the shell laps over the rim.
- **F7 housing→panel (8×):** CSK in the **5 mm UV-HDPE housing** (M12 CSK sink > host).
- **Bearing end-retainer (1×):** **Ø90 × 4 mm disc**.

Only **F2/F3 (14× ring/collar → 12 mm steel plate)** could take M12 — but bumping just those would NOT remove M10
(F1/F4/F7/bearing all stay) AND would put **two CSK sizes in one bearing-mount subsystem**, which is *worse* than
the current uniform M10. (TBS-001's premise that M10 was "our free choice" holds for the ring/collar, but the
cap/housing/disc hosts are physically sized for M10.)

**Decision (2026-09-07):** **KEEP M10** as the light-trap's single CSK size — a justified family (like M4),
forced by the thin hosts, not a free size to delete. One CSK driver/tap across F1–F7. The metric-family target
is therefore **5, not 4** (M5 still retires into M6×16 CSK).

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
chloride-free). (The earlier plan to absorb the retired M5 at ×16 is moot — M5 retirement is deferred to the
chem-shelf design and now targets a flange nut, not a fold into M6 CSK; see M5 below.)
- **Now:** the nut merge is a registry change (no geometry) — executed on `fastener-rework`.

### M5 — retire the family → DEFERRED to the chem-shelf design (2026-09-07)
The film-clamp "clips" that once shared this screw were retired to off-the-shelf nylon spring clamps, so
M5×16 CSK is now ONLY the **chem-shelf ply-panel attachment** (8 off, countersunk from the shelf frame
underside). There is no shelf blueprint yet, and the diagram's "4 mm frame" reads as unverified/over-spec —
an M6 CSK head (~3.3 mm sink) may not seat in a thin frame leg.
**Decision (2026-09-07):** DEFER the M5 retirement to the **chem-shelf design round**. The intended direction
is NOT an M6×16 CSK but a **flange bolt + nyloc nut under the shelf** (through-bolt — spreads load on the ply,
no tight frame countersink). M5 stays until then; it is the only item still blocking "M5 family gone."
- **Gate:** chem-shelf design (frame section + fastening method).

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
- **Ply-mount ⁵⁄₁₆″ → ¼″-20 — DONE (2026-09-07).** The ⁵⁄₁₆″ tee-nut + machine screw existed only for the 3
  filter housings. The bracket ear already passes ⁵⁄₁₆″, so a ¼″ screw + a ¼″ flat washer (spanning the ear
  bore) clamps fine — retired the ⁵⁄₁₆″-18 family into the ¼″-20 ply-mount standard (¼-20 × 2½″ + washer,
  screw SKU pending). *(−1 SKU; the 5/16 thread family gone.)*
- **#14 self-drillers — the two 410-SS *structural* anchors are grip-justified, NOT merged** (the IBC foot
  needs 3¼″ through 6mm plate + 28mm ply + steel; the walkway leg needs 2″ — different stacks, like the M12
  wall lengths). The two plain **TEKs** (`bracket-tek-screws` + `walkway-arm-holddown`) — **DONE (2026-09-07):**
  unified to one SKU, McMaster **90822A620** (#14×1″ HWH 410-SS), the hold-down adding a 1/4″ SS washer (92141A223).
- **⅛″ blind rivets — consolidation EVALUATED, INFEASIBLE (2026-09-07).** No single 1/8″ grip spans both laps:
  the shell/rim laps are 0.188–0.25″ (97525A425) and the housing/surround laps are 0.313–0.375″ (97525A435),
  and the candidate multigrip 97525A420 is only 0.126–0.187″ (too thin for either). **Both SKUs stay** — the
  two grips are duty-separated, like the M12 wall lengths.
- **Optical-plate mounting bolt — BOM gap CLOSED + head standardized to hex (2026-09-07).** The Optical Plate
  System Item 8 (8× M12×40 on a Ø540 circle) lived only as a drawing label — never in the registry (the survey
  missed it because it wasn't in `parts.py`). Itemized as `optical-plate-bolt` (92314A744) + `optical-plate-washer`
  (93475A290), and its **socket head → hex** to match the structural standard (resolves the optical-plate half of
  the socket-vs-hex question; the tilt-swing board's socket heads are still open for its design chat).

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
| M10 (all) | light-trap + door | **KEPT** (2026-09-07) — the light-trap's single CSK size; already itemized in the `ll-fasteners` lot |

## The model to copy
The M12 *fasteners* are already single-SKU across the whole camera — one plain nut (127 off), one flat washer
(508), one lock washer (127) — because the grips were made to match. Apply that discipline to the lengths and
the end state is ~7 metric bolt lengths (from ~12), ≈ −7 SKUs, the **M5** family gone once the chem-shelf
design lands (M10 stays — its thin light-trap hosts justify it) — every change a grip/load check away, none of
it touching a load path it shouldn't.
