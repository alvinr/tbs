<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->

# Spray-Bar + Tray-Drainage Redesign — Plan of Record (2026-08-03)

Working record (repo-only, not published) for the closeout cascade. Captures the locked
spec, the decision chain (seeds the processing-tray report's "why this design" section),
the file-by-file cascade map, and the staging. Delete once the cascade is merged.

## 1. Decision chain (why this design)

1. **Goal.** Let the spray beam lift clear for maintenance **and** for sliding the muslin under
   during loading — without a slit through the walkway (which would let it flex).
2. **Nozzles run the full width.** 90° down-jets fire *down* onto the print; the walkway grate is
   *above* the beam, so spraying under it is not a problem → the beam/nozzles span the full tray
   width (X200–4599, **4,399mm**), not just the open zone.
3. **Full-width span forces a stiffer beam.** At 4,399mm the old 40×25×1.6 SS beam sags **25mm**
   wet (L/175) — it drags on the 9mm spray gap. Up-sized to **1½×1½×0.062" 304 SS** → **11mm**
   sag (L/395), which the ~12mm pre-camber flattens. (2×2 was rejected: it foul­ed the walkway
   support arms and is 2.9kg heavier to lift out, for zero spray benefit once cambered.)
4. **The 1:200 slope was the real clash.** The tray's **dual-axis** slope (to a single corner sump
   at the near-right) tilts the rigid beam's **left end up ~24mm** into the *level* left walkway
   arm. The old beam fouled here too — it was only ever checked at the low corner.
5. **Fix the slope, not the symptom.** Make the **surface fall in Yd only** (far→near) so it is
   **level across X** → the beam stays level and clears the arms (~2–3mm residual). Drainage is
   preserved by a **near-rim gutter that falls 1:200 inward to a single center pickup** — so it
   self-drains (no squeegee), and gravity runs *toward the operator* on the sweep. Simple to fab.
6. **Close the residual with margin.** Shave the walkway long-beams to a shallow section and add
   one arm → **≥15mm** clearance at **~1mm** bounce (stiffer than today). See §3.
7. **Result.** Full-width direct spray + effortless self-drainage + a solid walkway + a trivial
   straight-up lift-out — the original goal, reached by fixing the tray geometry.

## 2. Locked spec

| Item | Value |
|---|---|
| Spray beam | **1½×1½×0.062" (38.1×38.1×1.575mm) 304 SS**, single **17'4"** length — Metals Depot **$183** |
| Beam span | X200–4599 = **4,399mm** (full tray width, `PROC_TRAY_X ± 30`) |
| Beam Z | bottom rise 9mm; top rise 47.1mm (top ≈ Z67 at the near/low rim) |
| Sag / camber | ~11mm wet (L/395) / ~12mm pre-camber → runs flat |
| Nozzles | **44 @ 100mm**, full beam width, 90° down-jets |
| Tray surface slope | **Yd-only**, 1:200, falls far(Z31)→near(Z20), **level across X** |
| Near-rim gutter | full width, floor falls **1:200 inward to center pickup** (X2399); ~7mm deep at ends → ~18mm at center; within the existing 20mm sump budget |
| Drain / pickup | relocated **X4550 (near-right) → X2399 (near-center)**; pop-out-of-walkway design retained, run **under the walkway to the IBC end** to rejoin the ribbon pipes |
| Beam near-park | stops **~70mm short** of the gutter (wheels stay on solid floor) |
| Right walkway long-beam | **2×¾×0.065" rect (50.8×19)** — Metal Supermarkets — **+1 added cantilever arm** → ~18mm clearance, ~1mm bounce |
| Left walkway floor-leg arms | mirror the shave + spacing |

## 3. Right-walkway shave vs bounce (100kg point, steel)

| Section (depth) | Underside | Clearance | Bounce @1014mm | @507mm (+1 arm) |
|---|---|---|---|---|
| 40×40 (today) | Z75 | foul | 1.1mm | — |
| 2×1 (25.4) | Z90 | +11.5mm | 4.1mm | 0.5mm |
| **2×¾ (19)** | **Z96** | **+17.9mm** | 7.9mm ⚠ | **1.0mm ✅** |

Shave alone is too bouncy at the current span; **shave + one added arm** is the fix.

## 4. Cascade map (Alvin's 9 items → work)

1. **Slope → all 2D/3D** — `tray_floor_z()` dual-axis→Yd-only; regen tray/spray/walkway 2D + overview/spraybar/water/walkway 3D.
2. **Drain pickup → all 2D/3D** — `PROC_TRAY_DRAIN_X` 4550→2399 + gutter constants; regen the same set + water.skp.
3. **Cantilever → all 2D/3D** — RWK long-beam section + added arm (and left mirror); walkway 2D + walkway/overview 3D.
4. **Sump pickup relocation** — near-center; keep the pop-out-of-walkway design; route the tube **under the walkway to the IBC end** to rejoin the ribbon lane. Water-system geometry + plumbing report.
5. **BoM / shopping / prices** — `parts.py`: beam ($183), nozzles (5×10-pk / 44), 2×¾ long-beam, added arm, drain fittings; `costing.py` reconcile; master-shopping-list + project-cost-breakdown cascade.
6. **New section diagrams** — the plan + A-A/B-B slope sections, near-rim fall-off, gutter X-slope (from this session) → registered generators + gallery.
7. **Processing-tray report** — add a **"Why this design"** section (from §1) + update slope/beam/nozzle/drain prose.
8. **Beam full-width + new dims + nozzles** — constants + report §3.2/3.3/3.7/3.8 + parts (folded into 1 & 5).
9. **Stale-reference sweep** — grep every `.md` for stale slope/sump/beam/nozzle refs after the cascade.

## 5. Staging (gated commits) + handoffs

- **Commit A — beam + nozzles** (constants → spray 2D → report §3 → parts → cost → weight → `.rb`).
- **Commit B — tray slope + gutter + drain relocation** (`tray_floor_z` → tray/spray/walkway 2D → new section diagrams → reports → parts → cost → water geometry).
- **Commit C — walkway shave + added arm** (RWK/left constants → walkway 2D → report → parts → cost).
- **Commit D — report "why" section + BoM/price rollup + stale-ref sweep.**
- **`.skp` re-sends** (overview / spraybar / water / walkway) handed to Alvin after each affected commit: I `--save` the `.rb` and verify the live doc matches before any `--send`; **Alvin saves + re-uploads to Sketchfab**, then I commit the `.skp`.

## 6. Geometry still to finalize during the cascade

- Exact gutter cross-section (width, wall/lip) + center pickup well footprint at X2399.
- Beam near-travel limit constant (Yd ≈150) and any nozzle-coverage note for the near ~70mm.
- Left floor-leg arm count/spacing to hold ~1mm bounce at the shaved depth.
