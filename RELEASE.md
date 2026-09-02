<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Release Log — The Big Shoebox Project (TBS-001)

Version history for the project. Each tagged [GitHub release](https://github.com/alvinr/tbs/releases)
has a dated section below summarizing what changed since the previous release. Versioning is
informal `MAJOR.MINOR` — this is a design + documentation repository, not shipped software.

## How releases work — the gate

Between releases, **jot every notable change under [Unreleased]** as it lands (one bullet per
change). That running list is the source we curate from. **Cutting a release is gated on this
file** — a release must not ship without a changelog entry:

1. Make sure **[Unreleased]** captures everything since the last tag.
2. Promote it: rename `## [Unreleased]` → `## [X.Y] — YYYY-MM-DD` and start a fresh empty
   **[Unreleased]** above it.
3. Commit, tag, and create the GitHub release from that section's notes.

**`bash release.sh X.Y`** automates steps 2–3 (promote → commit → tag → `gh release create`) and
**refuses to proceed if [Unreleased] is empty**, which is what enforces the gate.

---

## [Unreleased]

- **Hinged panel — Sheet 2 zero-drift reconcile with the 3D (drum/cage/frame depth).** Sheet 2 was
  recomputing the drum/cage depth locally (drum center −450, cage −875..−25) instead of using the shared
  constants the 3D model uses. Re-based the plan depth on the PANEL exterior and single-sourced from
  `DRUM_CX` + `DRUM_CAGE_X0/X1` (`+PANEL_EXT` offset), so the drum, cage extent, and cage→frame relation
  now match the lighttrap model exactly. The cage back posts now **land inside the frame jambs** (welded
  along the embedded overlap — weld ticks), replacing the earlier bracket-across-a-gap. Also drew the
  opening as **two distinct members** — the 40mm container wall AND the 50×20×3 RHS door frame — per the
  3D (was one 40mm block mislabeled as the frame). EXT overhang auto-updates to 760mm; the (now N/A)
  interior-overhang dim removed. Per Alvin: "both the 2D and 3D represent the same factual world. Zero drift."

- **Hinged panel — feedback round (Sheets 2/9/10/14 + global mm).** Sheet 9/10: removed the Fan-B
  plywood band and the drum/cage envelope so the steel-frame GA reads as frame only (drum detailed on
  Light-Trap Sheet 7, Fan-B ply on Sheet 12). Sheet 14 Detail A: the fan-flange bolts now thread into a
  captive **tee-nut** set in the ply (matching Detail B), not a separate backing plate + nuts. Sheet 2:
  re-scaled the blind-rivet glyphs — the front + side rivets were 3–5× oversized (read as bolts); now a
  realistic Ø6mm-body / ~12mm-head consistent across both. **Standing rule:** every dimension label now
  carries an explicit `mm` suffix (f-string + literal), applied across all 17 sheets.
  Sheet 2 cage→frame: replaced the thin 14mm weld-tie (read as a bolt) with a full-width **welded
  bracket + gusset plate** at each interior cage corner post, fillet-welded both ends, with a callout.
  Sheet 3 "RHS" confirmed = Rectangular Hollow Section (not a side designation) — left as-is per Alvin.

- **Hinged panel — tidy-label pass (Sheet 9/10) + stale cross-ref fixes.** Sheet 9/10 left margin
  de-crowded: tightened the U-FRAME and cam-latch STRIKE-PLATE notes, widened the margin, and moved the
  "1225 fan band" dimension clear of them (fix applies symmetrically to the exterior mirror). Fixed two
  sheet cross-references the Sheet-10 renumber had missed: Sheet 11's frame→hub note now points to
  **SHEET 15** (Frame → Pivot-Post Connection, was 14) and Sheet 12's attachment note to **SHEET 14**
  (was 13, and it contradicted the same sheet's own subtitle). Corrected stale value-comments surfaced by
  `check_consistency.py` (Fan-B ply-band top 1125→**1225**/`PANEL_FAN_BAND_Z`; drum-axis −400→**−420**;
  Sheet-2 depth-center derivation −400→**−450** for DRUM_R 450→400). Re-saved `lighttrap.skp` (Alvin).

- **Hinged panel — 2D fixes + generator function rename.** Sheet 14 Detail A: moved the fan bottom bolt so
  it clears the Ø150 housing symmetrically with the top. Sheet 13 Detail A: re-drew the cam latch as a
  proper plan section — the clamp shaft is vertical through the RIGHT (panel) stile (end-on = a circle) and
  its right-angle latch spans LEFT to the strike on the jamb stile. Sheet 2: added the missing front-face
  HDPE→corner-post rivets (the side skins already had them). Renamed the generator's `sheetN()` functions
  to match the sheet numbers they draw (Sheet 9/10 share `_frame_ga(mirror)` via thin wrappers).
  Follow-up pass: Sheet 14 Detail A bottom flange plate widened to match the top (symmetric); Sheet 2
  front-face rivets set flush to the HDPE surface + drawn to scale (d=11) and spread clear of the corner
  rivets, with the leader routed clear of the "PUNCH-OUT BAY" and side-skin labels; the container
  cargo-door frame drawn on Sheet 2 (solid, matching Sheet 9/10) and Sheet 9's cargo frame recolored to
  the same solid `#5A5E66` used on the Sheet 10 mirror.

- **Hinged panel — Sheet 10: exterior mirror of the frame GA.** Added a mirror of Sheet 9 viewed from
  OUTSIDE the cargo door toward the drum (x-axis reversed, so the geometry flips left↔right while the text
  stays upright — pivot post now on the left + drawn behind the frame, opening/U-frame/Fan-B on the right).
  **Inserted as Sheet 10** (right after Sheet 9); the former Sheets 10–16 shift to 11–17 (set is now "OF 17")
  — cascaded the renumber through the generator, gallery, registrations, the hinged-panel report, and the
  hingepanel sheet cross-references in the models/constants/parts. Also added the container cargo-door frame
  to Sheet 9 (full ghosted perimeter + M10 anchors) and Sheet 2 (merged with the former "end wall").

- **Container cargo-door frame re-specced lighter + attachment specified.** Now that the pivot post carries
  the hinge panel's weight, the door frame is no longer structural — only seal-compression + cam-latch load.
  Dropped it from **2×2×0.120in SHS → 50×20×3 RHS** (`DOOR_FRAME_FACE`/`DOOR_FRAME_DEPTH`; 50mm face keeps the
  seal landing, ~30% lighter), **reusing the IBC retaining-bar section** so it needs no bespoke order.
  Specified the attachment: the frame **bolts M10 @ ~300** into the container's steel door opening
  (reversible), and the opening-edge **U-channel welds to the door-frame left stile**. Cascaded through the
  3D `door_frame()` (+ M10 anchors), **Sheet 9** (door-frame stile drawn ghosted with anchors + the U-frame
  welding to it), `parts.py`/`costing.py`, and the container / equipment-layout / cost-breakdown reports
  (also fixed the stale "4× Southco at corners" latch note → 2× cam latch on the opening edge).

- **Hinged panel — 3D review round (pivot corner, cam latches, HDPE L-angle framing).** Stripped the
  redundant travelling **pivot-corner ply/frame** (it read as a plywood panel jammed between the leaf
  stile and the pivot post) down to just the structural **pivot-edge stile** the hub brackets weld to,
  and extended the swung leaf's **far-corner HDPE skin continuously to the pivot line** so the door face
  is skinned by the same panel material (no separate ply panel) with the stile behind it — closing the
  gap that had briefly left the stile/hub detached from the leaf. Redrew the two **cam latches**
  (1619A74) with the T-handle valve-body pattern (barrel-through + interior lift-and-turn lever, olive
  C_VALVE) and repositioned them for comfortable standing operation (top lowered 2168→1900, bottom
  raised 220→500). Added **L-angle framing** (30×30×3) securing the HDPE bay walls to the cage at the
  panel-plane lap (2D Sheet 2 detail applied in 3D); flagged the design gaps — the bay's forward ~890mm
  mouth has no steel to rivet to (needs a mouth frame ring), and the bottom angle crowds the tray rim.
  Began **frame-by-frame** detailing of each bay wall: the **far wall** (pivot / film-plane side) now
  carries a full-tunnel-depth drum-side L-angle at the mouth edge, plus **top + bottom 50×50 beams running
  in Yd from the drum cage across to the pivot frame** (the horizontal beams of Sheet 9), with rivet lines
  to the beams and the drum-side edge. Added a **"Steel · Pivot · Frame · Cage"** review scene that hides
  the HDPE skins / EPDM / Fan-B / drum shell so the framing reads. Dropped the **far-corner HDPE/apron
  split** on the pivot side from the 282 step down to the bottom-beam top (`FAR_CORNER_BOT` = 190) so the
  bottom-beam rivets land on HDPE rather than the fold-down apron plywood — the far apron (UP + folded +
  chamfer) reduced to suit; near corner keeps its 282 step. (2D Sheet 16/9/15 apron reconcile deferred.)
  Added a **fixed (non-folding) plywood stub** closing the corner gap between the far apron's far edge and
  the pivot post (a fold-down flap there would foul the post + floor plate; the fixed stub at X28–40 clears
  both). Reconciled the **near wall** (pinhole side): added its missing top + bottom 50×50 beams running
  in Yd from the drum cage to the near frame edge, symmetric to the far wall. Then completed the near wall
  to match: drum-side L-angle at the mouth + rivet lines, the fold-down near apron dropped to the same
  split as the left, and the Fan-B ply band extended down to it so the near beam's rivets land on fixed
  skin. Renamed the split constant `FAR_CORNER_BOT` → `CORNER_BOT` (now both sides, 190). Added the near
  side's missing **vertical opening-edge stile** (Sheet 9 "left swing stile") tying the top + bottom beams
  at the frame edge — the far side's equivalent is the pivot post/stile. Rebuilt the fixed opening-edge
  member (`near_leaf`) from a solid block into a **welded box section** (thin exterior + interior flanges
  for the HDPE + plywood skins, a swing-facing web) welded to the door frame on the container-wall side,
  and located the two **cam-latch strike plates** on the web. **Sheet 9** now draws the fixed opening-edge
  structure as that **welded U-channel** (web at the Yd180 joint facing the swing panel + carrying the
  strike plates; flanges wrapping back and welded to the container door frame) instead of a ghosted strip. Moved all four bay beams + the
  near stile to the **flush-front datum (X0–50)** — they were set back 40mm behind the skin, lapping the
  cage post only 10mm; now they sit on the door plane like the cage posts + jambs (full 50mm cage lap).
- **Hinged panel — HDPE surround fabrication set.** Added the two missing surround blueprints:
  **Sheet 7** (flat-pattern cut sheets for all six 1/8" HDPE pieces — the two center-zone face skins,
  the two B2-bay side walls, and the upper/lower floor caps) and **Sheet 8** (the floor-cap→Ø800-housing
  extrusion-weld join and the surround→steel-frame blind-rivet lap details). Resolved the surround's
  **frame connection** as a blind-riveted lap (1/8" 18-8 SS @ 60mm + DP8010 sealant bead) and modeled it
  in 3D so the surround reads as fastened, not floating (+$29 panel). Reconciled the stale **Ø900→Ø800 /
  DRUM_H 2200→2100** drum geometry across the hingepanel generator, the lighttrap model, costing, and the
  assembly generators; hinged-panel report §2.6 added, §3.1 drum-top Z corrected to the 2,100mm cap top.
- **Hinged panel — steel-frame + hardware blueprint set (Sheets 9–14).** Added the frame general
  arrangement (Sheet 9, noting the welded drum cage), the frame→pivot-post connection + full pivot-post
  spec (Sheet 10 + report §5.5), the plywood cut sheet with Fan-B mount and IBC-style metal-tab/tee-nut
  frame fixings (Sheet 11), the frame hardware attachments (Sheet 12: cam latch, transport lock, brush
  strip), the frame→hub weldment detail (Sheet 13/14), and the pivot-jamb elevations (Sheet 1/14).
- **Hinged panel — cam-latch reselection + inward-opening reconcile.** Swapped the recessed compression
  latch for a **McMaster 1619A74 lift-and-turn cam latch** (adjustable 1¾–2⅛", 150 lbf) mounted through
  the tubular steel jamb (over-bore + box-spanner + light-tight plug for the captive nut) latching a
  **welded keeper on the steel-framed stub wall**; the panel now **opens INWARD only** against a frame
  stop (aged-out 180° outward swing removed across Sheet 1, the report, and equipment-layout §9). Net
  panel cost **+$47/$33/$19** (cam latch).
- **Hinged panel — fold-down light aprons close the raised floor gap (new Sheet 16).** The 217mm floor gap
  is light-sealed by two **bottom-hinged fold-down plywood aprons** at the corner zones (the far one minus a
  measured **200mm fixed stub** that clears the Ø220 pivot mount plate) + a **fixed center baffle** under the
  drum bay. Stand up + seal in operation; fold flat into the container for the transport swing. New **Sheet 16**
  (fold action + elevation + baffle detail); built into the lighttrap 3D as DC children that fold in transport
  mode (visibility-swap on `PanelSwing!swing`), plywood (`C_PLY`); the obsolete full-width threshold brush is
  retired. +$95/123/150 panel; report §5.3/§6 reconciled. Joint seal detail (foam + lapping board) still TBD.
- **Hinged panel — drum-bay light seals + reduced side gap.** Closed the residual light paths around the
  swinging drum cage: the fold-down aprons now **extend inboard** past the center-zone step line to a 12mm
  brush gap off the cage sides (`APRON_CAGE_GAP`, `APRON_IN_L/R`) — cutting the old 47mm side slot to 12mm —
  with a **vertical strip brush** on each apron inner edge, and a **horizontal strip brush** on the center
  baffle top edge bridging the 10mm up to the swept cage bottom. Center baffle trimmed to the apron edges.
  Built into the lighttrap 3D and Sheet 16 (elevation + Detail D). `APRON_FIX_W` single-sourced to constants.
  3D review round: each fold-down apron is now ONE notched plywood panel (single stepped cut, not two
  abutting boxes); all four now-redundant bottom EPDM strips (both fixed leaves + the swing panel's trimmed
  L/R) were removed — the fold-down apron + its top brush seal that leaf-bottom interface now.
  Further review round: the pivot-side plywood is now ONE full-height fixed 200mm strip (Yd2162–2362) —
  the old 75mm upper leaf + the fold-down-zone stub merged into a single panel covering the Ø89 pivot-post
  corner; the swinging panel's plywood ends at Yd2162 and hinges to the post behind it. EPDM (compression)
  and the brush seals now render in DISTINCT colors (brown EPDM vs green brush, previously two greens).
  **Fan B raised 100mm** (`FAN_B_H` 600→700, ply mount band top 1125→1225). Added **Sheet 16 Detail E** —
  the plywood↔plywood 45° chamfer (scarf) joint TYP of every moving plywood interface: EPDM bonded to the
  FIXED face, the moving panel sweeps off without binding, the diagonal lap blocks the straight light path
  (apron top↔leaf, apron side↔stub/jamb, swing-panel↔leaves, apron↔baffle). 3D: the far apron↔full-height
  strip joint is cut for real (chamfered strip prism + matching apron wedge + EPDM scarf seal, `CHAM=40`)
  as the pattern; the remaining three joints follow once the look is confirmed.
  Review fixes: added top+bottom **connection beams** tying the swinging panel frame to the Ø89 pivot post
  (it read as floating); extended the **bay HDPE walls down to the cage bottom** (Z217→Z140) to close a
  light gap at the housing openings. **Plywood rebuilt at true 12mm** on the interior face of the 40mm frame
  zone (`PLY_T`/`PLY_X0`), with the 45° chamfer now a full-thickness 12mm scarf (`CHAM=12`); the swing
  panel's corner zones now step up to Z282 like the frame + aprons, which removes the fold-down-flap↔leaf
  overlap and clears the walkway cantilever in the swing. Review follow-ups: frame + ply set OPAQUE so the
  frame no longer reads through the ply; the bay HDPE walls moved onto the drum-cage faces (Yd700/1662,
  riveted flush, no gap) instead of the wider panel-zone lines. Explicit **45° top-edge chamfer** cut on
  each fold-down apron (moving-flap scarf that sweeps off the fixed leaf's EPDM — Detail E); the near leaf
  bottom stepped up to Z282 to meet the flap top. Remaining chamfer joints cut: the center **baffle ends**
  (45° where the apron inner edges meet it) and the **near-leaf inboard edge** (swing-panel↔leaf joint) —
  all four plywood↔plywood joints now carry the explicit 45° scarf. The **entire film-plane left rig**
  (parked carriage + brackets + stub + saddles + plates + welds) now hides in transport — it's the
  shared-pivot film-plane hardware, not the light-trap door, and was reading as floating plates once the
  panel swung. Wired as a **swing-DC child** (not a root component — a root `_hidden_formula` doesn't
  recompute when the parent DC animates; only children do) so it actually vanishes at `swing>0.5`.
- **Hinged panel — pivot corner resolved as a travelling leaf.** Reversed the fixed-jamb approach at the
  Ø89 pivot: the pivot-corner plywood now TRAVELS with the swinging leaf (built in the swing DC), wrapping
  to the pivot LINE (not past it) — a CLEAN rectangular 12mm ply on a 40mm frame (no wedge/notch; the
  door-plane ply is inboard-clear of the fixed post). Frame→post connection is the inboard pivot hub; no
  fixed jamb, no swept cutout. The former full-height fixed far strip is retired.
- **Hinged panel — frame→post securing reconciled (2D + 3D).** The swinging leaf is tied to the fixed Ø89
  post by the moving hub (thrust + journal bearings) and **3 hinge brackets fillet-welded to the leaf's
  travelling PIVOT-EDGE STILE** (2×2 RHS) — hub + leaf frame + drum cage as one weldment. Sheets 10/14
  relabelled from "center jamb" to the pivot-edge stile (travels + carries the pivot-corner plywood);
  Sheet 16's obsolete "200 fixed stub" now reads as the travelling pivot-corner leaf. 3D: added the
  pivot-edge stile so the hub brackets land on steel, and deleted the wrong door-plane connect beams.
- **Hinged panel — 2D review fixes.** Sheet 13 Detail A: drew the Ø150 fan air CUTOUT through the ply +
  flange (fan now 150 at 1:1); Sheet 13: taller page so the rotated-90° companion clears the title block;
  Sheet 8 Detail B: centered the front rivet on the full stack so its head butts the HDPE; Sheet 2: added an
  enlarged **HDPE side-skin → L-angle → frame** detail (the HDPE rivets to an L-angle on the post, not
  through the beam). 3D: the hub hinge brackets now align with the leaf pivot-edge stile (per Sheet 14).
- **Hinged panel — floor gap raised 130→217 for the transport-swing clearance.** Confirmed (2D + live 3D)
  that in the transport swing the drum's lower cage sweeps across the container over the FIXED processing
  tray and the LEFT walkway's floor-leg cantilever posts. The posts (top Z115, they stay bolted) govern —
  taller than the tray rim (Z70). Raised `PANEL_FLOOR_GAP` 130→217 so the drum-cage underside (Z130) clears
  the Z115 posts by 15 mm (and the Z70 tray by 60 mm); the lower hub, `PANEL_FLOOR_GAP_SIDE` (→282), and the
  drum interior (1970→1883, still clears a 1780 operator by 103) all derive from it. **Sheet 15** reworked
  into the transport-swing clearance section (drum cage vs fixed posts/tray + panel vs wall brackets);
  light-trap-selection, hinged-panel §5.3, and walkway reports reconciled; weight/costing re-injected.
  3D: lighttrap re-sent + verified (cage bottom Z130, panel corners Z282); overview + construction pending.
- **Hinged panel — stepped bottom propagated into the 2D set.** Single-sourced the derived bottom step
  (`PANEL_FLOOR_GAP_SIDE` = 195, `PANEL_BOTTOM_STEP` = 65 in `tbs_constants.py`) and drew it on **Sheet 9**
  (frame GA — the bottom rail is now three segments: center at Z0 over the tray, both corner rails stepped
  up 65 mm, with the member schedule + step risers/dim updated) and **Sheet 1** (elevation — frame, skin,
  fan-mount band, EPDM seal and fixed strips all follow the stepped bottom, with a callout). Sheet 15 now
  reads the same constant. Next: push the step into the 3D `hinge_panel()`.
- **Hinged panel — Sheet 15: bottom clearance cross-section (new).** Added a Yd–Z clearance-envelope
  section (walkway grate lifted out for transport) that reconciles the 2D set with the **stepped frame
  bottom** in the 3D model. It shows the near/far **side-wall cantilever brackets** (vertical legs Z180
  std / Z200 widened), the **left lift-out floor-leg cantilevers** (×5, top Z115), the tray, and the
  **stepped panel bottom profile** derived from a 15 mm clearance rule: **Z130 across the center**
  (clears the Z115 arms/posts) **stepping up to Z195 at both side corners** (clears the Z180 std bracket
  legs), with the widened-Z200 case flagged for the swing-arc check. This is the hard-limit envelope for
  the panel frame bottom. Registered in all four generator-index files + the gallery; sheet count 14→15.
- **Hinged panel — Sheet 13 fastener details.** Fixed Detail A so the Fan-B mounting bolts **butt the
  flange plate + backing plate faces** (were floating clear of them), and reworked Detail B: the plywood→frame
  bolt now uses the standard section bolt glyph (hex head on the tab upstand, shank into the ply tee-nut),
  moved clear of the weld tab, plus a **rotated-90° companion view** that proves the bolt seats in the welded
  tab — not through the frame RHS.
- **Hinged panel — cam latches 4→2 + 2D dimension/detail round.** Reduced the cam latches from 4 corners
  to **2 on the opening edge** (the pivot edge is hinged; a frame stop takes the outward direction) — parts
  registry qty 4→2, **−$61** panel; reconciled the count across the report, the mass table, and
  light-trap-selection (which also still named the retired Southco C2-33 and the wrong pivot edge). Drawing
  fixes: Sheet 1 (2 latches, opening edge); Sheet 2 (cage **top perimeter rails** shown; side HDPE laps +
  rivets the corner posts; bottom skin width = frame; side rivets drawn as fasteners, not end-on circles);
  Sheet 7 (personnel-cutout height + locating dims); Sheet 8 (side rivet butted to the surfaces); Sheet 9
  (drum drawn as a **vertical cylinder**, not a face-on circle; full dimension set); Sheet 10 (pivot-post
  Ø + length dims); Sheet 12 Detail C (brush screw head on the exposed holder face); Sheet 13 (Fan-B mount
  redrawn **to scale** — the panel fan bolts through its **flange plate**, not the fan body — plus dims).
- **Hinged panel — 2D fastener/buildability refinements.** Reworked the detail drawings so every fastener
  is buildable: nuts land against the inside tube wall, hollow beams show their bore, side rivets bite
  steel backing (not the HDPE skin), tee-nuts pass through the tab face, full-height pivot beams, and the
  frame→hub brackets are **fully welded** (no bolts through closed tube). Swapped the panel-swing pull
  handle to the **same off-the-shelf McMaster 1871A65** as the interior drum handle (screwed into jamb
  rivnuts), **−$64/$74/$84** panel.

## [0.9] — 2026-08-27

- **Lighttrap Revoloving Drum detaile design and blueprint**
The lighttrap had a light-weight design that defined the major parameters. What was missing was a deatiled design down to the fabrication blueprints for the deatils of the mechanism.
  - **Design:** the drum end **caps are 8mm 6061-T6 aluminum** (bolted 4×M10 stub-shaft flanges), the **shell->cap and housing->frame joints are lap-and-fasten** (rolled 25×25×3 Al rim-angle + 1/8" 18-8 SS blind rivets @ ~60mm + 3M DP8010 bond/light-seal, superseding the extrusion weld), and a **steel welded box cage integrated with the swing-panel weldment** carries the bearings and the fixed outer skin (free HDPE opening edges stiffened by bonded Al U-channels in place of jamb posts). The **drum was resized Ø900->Ø800** (Ø764 drum, ~Ø758 bore) and re-centered to fit the transport-fixed cage; **interior 1,970mm clear** (`DRUM_H_LT` 2,100; cage top 2,217).
  - **Hub (both ends, Sheets 5/6):** cap -> **Ø160 steel stub-shaft flange** -> **Ø75 shaft** -> **SKF 6215-2RS1** -> **Ø240 bearing ring** (upper, isolated Al) / **collar** (lower, steel) -> **Ø240×12 steel mount plate** (ring/collar bolted 6/8×M10 CSK; plate welded to the beam) -> **50×50 axle beam**. The drum **hangs** from the upper bearing (above its cap, below the top beam); the lower bearing **floats** above the bottom beam. Axial retention: inner race by DIN 471 shaft circlips (+ a bolted Ø90×4 **end-retainer plate** on the upper load-bearing shaft); outer race **located** (upper - Ø122 shoulder + DIN 472 ring) / **floating** (lower - plain Ø130 H7 bore).
  - **Seals:** the ≈13mm running gap is closed circumferentially by **4× #4 (3/16") nylon strip brushes** (anodized-Al straight-flange holders DP8010-bonded + riveted to the drum OD at 93° spacing) and axially by **cap<->frame neoprene wiper + silicone bead** top and bottom; a Sheet 7 light-path study proves no straight-through or over-the-top path at any rotation. - **Interior pull handle** (off-the-shelf McMaster 1871A65) bolts to a steel stile that plugs + M10-CSK-bolts to the two Al caps - the pull load lands in the caps, with no fastener through the HDPE wall.

- **Film-plane corner wall-mounts + IBC foot ↔ tray clash.** Resolved
  the film-plane left-bracket + tray/IBC cluster. **Tray clash:** the two FRONT IBC floor feet were shifted
  outboard (derived from the tray edge) so their plate + anchors clear the processing-tray basin — the plate
  spec is unchanged, only the station moves. **Left film-rail wall mounts:** restored the budgeted wall-seat
  **saddles** the redesign had dropped — seat + gusset + **upstand** on the container-facing face (rail bears
  on the inside face, not the outer edge), back-plate lengthened so the gusset welds fully, and the rail ends
  trimmed to butt the plate. The two far-LEFT ends land on the
  Ø89 **pivot post** (it carries their weight) so they get a lighter flange **tie** (interior flange + exterior
  plate + 4× M12) instead — sized to clear the post + roof-mount plate. All wall-bolt **heads sit outside**.

## [0.8] — 2026-08-19

- **Walkway blueprint.** Reworked the walkway into a full fabrication blueprint set. Reworked the cantilevers so the near and far ones use the same fabrication. Added floor bolts to the right cantilevers, clearing the processing tray. Reworked the shared container-wall plates with the film-plane beam and walkway beam. Performed structural validation + IBC/OSHA bracket analysis, which required upgrading the cantilever arms to conform to the standards. Added a grate cut-sheet plan.

- **Walkway F1 → water re-route (branch `walkway-bp`).** Shortening the right walkway (F1) moved the outer
  long beam inboard into the under-walkway pipe channel. Fixed the two clashes it caused: **#1** the 4 ribbon
  lanes (`RIBBON_LANE_X`) were hardcoded for the old wider channel — now **derived** from the inner-outboard..
  outer-inboard beam gap so they can't drift again; **#2** the near-corner SV-01/DV-02 risers were speared by
  the end-beam butt-line inset — the **near RWk end beam is un-inset to Yd0** to clear them. (Two pre-existing
  under-corridor clashes — recycle×J6-plate, lines×IBC-frame-rail — are logged in TODO, not from this work.)

- **Sketchfab re-upload automated (in-place, hands-free).** The manual "re-upload each `.skp` to Sketchfab"
  step at the end of every model cascade is now scripted. `push_sketchfab.py` uses `PUT /v3/models/{uid}` to
  replace a model's geometry **in place** — same URL, viewer settings/materials/name preserved — instead of the
  old create-new-model-and-delete-old dance (which reset viewer settings each time). A single-writer guard
  refuses to push unless the live doc is the saved `<name>.skp`; legacy behavior stays available behind `--new`.
  Validated end-to-end (a scratch box→box+cylinder lifecycle and a real overview push to its existing UID).
  A wrapper — `send_model.py <name> --send --push` — combines the rebuild + push in one command: it delegates
  the build to the model's generator, then (token-gated) offers to push *after you validate*. It prompts in a
  terminal and skips safely with a note in a non-interactive shell, so an agent can't push unvalidated geometry.

- **3D models: single-owner dedup pass + a ratchet gate.** Components were being re-implemented in more than
  one model generator (the drift behind "the detail is right in one model, wrong in another"). Added a `lint.py`
  **ratchet gate** — no component name may be emitted as a `ruby_*` literal in >1 model file — and consolidated
  4 clusters to a single owning builder each that the other models call: **electrical** (em owns cable trunking,
  inverter box, master switch — overview's full-length trunking corrected to em's fitted extent), **Fan B box**
  (lighttrap), **processing tray** (overview owns the sloped pan; the spray-bar model now shows the *same* tray
  ghosted instead of a flat copy), **walkway Far/Near decks** (walkway model). 17 cross-file duplicates → 5,
  and the 5 are documented (2 permanent context ghosts + 3 real drifts the audit surfaced: cargo-door panel
  thickness 120 vs 40 mm, sump-pickup Yd 155 vs 104, and the mini-tbs scale-toy wall — all tracked in TODO).

- **Process: attack the orientation-rework class (retro follow-up).** A two-release retro found the biggest
  rework driver is fastener **orientation/interface** — bolts dimensionally correct but pointed the wrong way,
  through the wrong face, wrong length, or too near an edge (the J2/J7 3 mm-edge flaw, "bolts projecting past
  the plates"), caught only when a render was eyeballed. Three concrete fixes: (1) **`check_interference.py
  --bolts`** — a read-only lint that, for every structural grip bolt, finds the members its centerline pierces
  and flags EDGE (< 1.5·D), FLOATING, PROJECT (prototype; 15 flags on overview incl. a real J6 top-bolt edge);
  (2) **`skills/skill_fastener_convention.md`** — codifies the `ruby_bolt` axis/head/nut sign convention + the
  edge-distance/grip/accessibility rules so builders stop guessing; (3) **`manifest --update <name>`** now scopes
  to the named model(s) instead of rewriting every hash (it twice clobbered un-sent models' hashes this session).

- **3D-model hygiene (post-0.7).** Three drift/readability items off the tracker: (1) **retired the dead
  `ibc_rack()`** — the old single-portal frame builder (X4734), dead in the live model but a drift risk, moved
  out of `generate_sketchup_model.py` into its sole consumer (the archived right-cantilever study) so overview
  can't silently revert to the pre-redesign frame; (2) **fixed the real J6 clash** — the walkway cantilever-arm
  rear backing plate dipped ~10 cm³ into the corridor bottom X-rail at each front upright; raised its bottom to
  butt the rail top (Z62.8), moment joint untouched, `--solids`-verified gone on the live model; (3) the RWk end
  beam↔long-beam butt was already resolved — narrowed the remaining seam-audit sliver (long-beam ends ↔ wall
  cleat) for a walkway-open pass. Cascade: `ibc_cantilever_arms` re-sent to all 5 models (ibc-stack / walkway /
  construction / water / overview — saved + uploaded); `manifest --check` clean.

## [0.7] — 2026-08-17

- **IBC bar-restraint redesign — J2/J7 L-cleats + single horizontal M12×65 (edge-distance fix), full cascade.**
  The front retaining bars previously bolted VERTICALLY through the 20 mm-wide face of the 50×20 RHS, leaving a
  Ø14 hole only ~3 mm of edge. Redesigned **both** bar ends (corridor J2 + wall J7) to the same detail: the bar
  **drops into an 8 mm-plate L-angle** (welded to the upright / wall backing plate) and a **single horizontal
  M12×65** runs through the L's vertical leg + the bar's tall 50 mm web — ~18 mm edge. Retaining bars doubled to
  **2 per tier (8 total)** for the EN 12195-1 loaded-transport case; wall hangers **inside-aligned** to the
  corridor face (not the back surface); D-rings repitched **clear of the cleat legs**; **16 nut-side backing
  plates** added. Cascaded end-to-end: frame Sheets 1–6 + the Plate Fabrication Schedule, all **five** SketchUp
  models (ibc-stack / water / overview / construction / film-plane re-sent + uploaded), `parts.py` (M12×65 ×16 +
  `ibcf-cleat-backing` ×16), `costing.py`, and `ibc-stacking-report.md`. Interference re-audit against the live
  model confirms the redesign **adds no new clash** (all 10 remaining are pre-existing pipe-routing).

- **J6 walkway-arm → corridor-upright joint firmed.** The cantilever-arm end connection went from 4 bolts to
  **2 (a central vertical column)** on a **65×130 end-plate** with a simple 5 mm fillet all round, and the arm
  uprights now seat on their foot plates. Flagged the one **real** residual clash — the lower J6 bolt vs the
  corridor bottom X-rail — for a post-release 3D fix (notch the rail / drop its start).

- **IBC 2D diagram-standard pass — units, leaders, and outlines.** Swept the whole IBC frame + plate set to the
  drawing standards: **`mm` on every dimension** (de-crowded the sub-30 mm micro-dims to notes), **re-targeted
  Sheet 1 leaders** after the 2-bars-per-tier change (they had anchored in the empty gap between the paired
  bars), redrew the **container wall as a full-height ghost outline** (matching the tote outlines) and dropped
  the stray beam-tip wall boxes on Sheet 6, plus an editorial + tidy-labels tidy across the set.

- **IBC Frame Blueprints (rollup).** The above sits on a broader blueprint push over this cycle: bar-end cleats
  moved to the outside edge, the 2-ring / 8-weld map (Sheet 6), notch-TEK detail (Sheet 5), the member cut
  list, and TEK screws securing the cantilevers to the walkway frame.

- **NEW tooling — 3D readability seam audits (`check_interference.py --solids / --pipes / --seams`).**
  Two READ-ONLY, advisory passes against the live model that surface a *drawing* defect (distinct parts
  rendering as one fused piece because no seam shows), distinct from a clash. `--solids` lists same-color
  solid↔solid interpenetrations (3-axis overlap — a member run *through* another, not a butt) above a
  volume threshold, each tagged `weld` (leave) or `BUTT?` (bolted/cleated → butt at the mating face).
  `--pipes` flags pipes driven through the full thickness of a panel/wall/plate slab with no drilled-hole
  seam (fix: collar ring, or split to butt). The butt-vs-weld convention is codified in
  `skills/skill_model_consistency.md`. (The per-hit geometry fixes are a triaged follow-on — TODO.md.)

- **Half-lap hold-down — #14 TEK screw per lap (Sheet 5 detail + model + parts).** The long beams sat on the
  arm's bearing seat by gravity only; added a positive fastener so they're secured. One **#14 self-drilling TEK
  screw per half-lap** (4 total: 2 arms × 2 crossings), driven **from the underside** through a Ø7 clearance
  hole in the beam, self-tapping into the **solid arm** above (anti-lift/anti-slide; the head sits in the
  ~6.6 mm gap and clears the traveling spray beam). New **HALF-LAP HOLD-DOWN section** on Sheet 5 (hatched arm
  on top / beam with the hole below / screw from underside), 3D model gains the 4 screws, `parts.py` +
  `walkway-arm-holddown` (4× #14 TEK + washer), costing +$2/$3/$4, report §3.4 note.

- **Walkway cantilever arm → SOLID 2×1 flat bar + rebalanced half-lap notch (structural fix + full cascade).**
  A review flagged the arm's half-lap notch as dangerously thin. Root cause: the arm half-laps over **both**
  right-walkway long beams, and a notched **hollow** tube opens into a weak channel (the un-notched LEFT
  cantilevers can stay tube; this one can't). Added the missing check — `ibc_frame_load.arm_notch_check()`
  computes the moment at each notch (worst case = full arm load at the tip): outer notch **334 N·m**, inner
  **31 N·m**. Fix: the arm becomes a **solid 2×1 flat bar**, and the notch is **rebalanced to the moment** —
  deep arm notch at the tip (low moment, arm keeps 5.4 mm / inner beam keeps 20), and at the post end the
  **outer beam** takes the deep notch so the arm keeps 16 mm (**SF ≈ 1.6**). A continuous-beam check
  (`outer_beam_frame_check`) firmed the outer beam: its thin 9.4 mm notch is a **bearing seat** (a thin
  channel can't carry the support hogging), so the beam spans simply-supported on its **full section — SF ≈ 7,
  ~2 mm** deflection under a person. Cascade: 3D model (`_rwk_xbeam` solid X-segments + per-crossing
  split, `_rwk_long_beam` split param, `ibc_cantilever_arms` J6 clamp→end-plate), `parts.py` (arm split out
  as solid bar + J6 end-plate hardware: 8× M12×100, 4 plates, 8 crush sleeves; −4 clamp bolts), costing
  reconciled (+$62/$85/$108 walkway), Sheet 5 + report §3.4 updated. (3D `.skp` re-send to follow.)

- **Fix — walkway Sheet 6 (floor-leg cantilever): post drawn over the anchor holes.** In both VIEW A
  (section) and VIEW B (plan) one of the two M10 anchor columns fell under the 50×50 post footprint —
  unbuildable (can't drive a floor anchor through the post). Both anchor columns now sit **outboard of the
  post** in each view, using one shared formula (`fx0+14`, `fx0+fl-post-14`) so the section and plan agree.

- **NEW — IBC frame Sheet 5: walkway cantilever-arm fabrication (`ibc-frame-sheet5.png`).** The 2 walkway
  cantilever arms that hang off the IBC front uprights are now drawn as a fabrication sheet in the IBC-frame set
  (keeping all the IBC-frame metal together rather than deferring to a separate walkway blueprint). The arm
  crosses **both** right-walkway long beams (`RWK_BEARER_XS`), so it has **two** half-lap notches, not one.
  Three views: a fully-dimensioned VIEW A side elevation (notch widths + gaps 50.8 / 198.4 / 50.8 / 25 → reach
  325, half-lap depth 20 notched of the 25.4), a PLAN VIEW showing each notch as a full-width half-lap (beam
  width 50.8), and an END-PLATE / rear-backing-plate detail (70 × 130, 4× Ø13 for M12 at 30 × 90 pitch, with the
  arm weld footprint shadow-marked). Sheet count bumped to OF 5; registered in the gallery / publish.sh /
  setup_docs / dependencies.yml and embedded in report §3.5 + §8. The two "detailed in the walkway blueprint"
  notes re-scoped to point at Sheet 5. (2D only; the 3D ibc-stack arm + full model cascade to follow.)

- **NEW — IBC frame load-case sheet (`ibc-frame-load-case.png`).** `ibc_frame_load.py` gained a `--png` render:
  a one-page load-case drawing — the transport load-path elevation with the EN 12195-1 arrows (0.8 g fwd /
  1.0 g down / 0.5 g lateral), the method box (coefficients, f_s, μ, the blocking inequality, both fill
  states), and the full demand/capacity/**SF matrix** for every restraint element (bars with/without the mat,
  wall-hanger + cleat bolts, wall bearing, lash strap, walkway-arm clamp, upright) — all driven from the same
  `compute()` the validation table uses. Registered + embedded in report §3.4. Completes the IBC-frame
  blueprint's visual set (the film-plane Sheet 10 analogue).

- **Rear-panel + pipe-run brackets: welds → TEK screws (W6/W7 → J8/J9).** The two light bracket-to-post
  joints are no longer welded — they attach with **2× #14 self-drilling TEK screws** each, so the brackets
  bolt onto a **pre-welded, pre-painted frame with no hot work** and stay adjustable (they carry only light
  static loads; the load-bearing bar cleat stays welded, W3). Weld schedule drops W6/W7 (W8 ribbon-beam →
  W6); fastener schedule gains **J8** (rear-panel bracket, 12) + **J9** (pipe-run L, 24); Detail D/E redrawn
  with the TEK screws; Plate 5/6 "weld leg" → "screw leg". Added a `bracket-tek-screws` part (36× #14, 410 SS,
  +$11/$20); the two bracket specs de-welded; costing reconciled.

- **Plate schedule — fuller hole dimensioning, Plate 3 redrawn, stock standardized, J7 reverted to 1.**
  Plates 4/5/6 carry BOTH L-legs' outside lengths on the L-section end view + a hole-center dim on the
  drilled-leg face; Plate 2 gains a hole-center-to-edge dim; the Plate 5/6 hole-size note moved to Sheet 2.
  **Plate 3 (wall-hanger pocket) redrawn** into two proper **FACE views** — back-plate + seat/fillet face
  with the drill holes dimensioned. The pocket **back-plate + seat standardized to 60 mm** to reuse the
  Plate 2 backing stock (were 67/59). **J7 reverted to 1 centered bolt/bar** (from 2, 16→8 M12×40, −$12):
  the 2nd was redundancy not strength, and at the wall the pocket + the fixed 2-bolt corridor cleat already
  stop the bar rotating — one centered bolt also clears the seat edges cleanly. Detail A + report §3.5 + costing updated.

- **IBC frame Sheet 4 — detail-correction sweep (B/D/F + tone).** DETAIL D redrawn per Alvin's sketch as a
  welded **L-bracket** off the post with the rear panel bolted to its upstand via an **M8 hex + washer into a
  pronged tee-nut** — and the tee-nut moved to the ply **back face** (bolt tension pulls the flange against the
  wood, the correct orientation). DETAIL B cleat bolts now span the bar+cleat stack exactly so head/nut seat
  **flush** (no exposed shank). DETAIL F elevation bolts shortened to bear on the clamp-plate faces (were
  projecting past the plates). Steel fills **lightened to sheet 3's tone** for readability.

- **NEW — IBC Plate Fabrication Schedule (2 sheets).** `generate_ibc_plate_schedule.py` draws every plate in
  the IBC/corridor metal **1:1** (with a 100 mm scale bar) so a shop can cut and drill each: Sheet 1 —
  structural plates (IBC foot 150×150×12 / 4× Ø14 @ 100 sq PCD; wall-hanger backing 60×205×8 / 2× Ø14 @ 169;
  wall-hanger pocket, folded 4 mm, J3 + J7 holes); Sheet 2 — angle brackets (bar-end cleat, rear-panel tab,
  side-panel pipe-run L), each as an L-section end + a drilled-leg face with hole Ø, center positions from a
  datum edge, thickness, material, and qty. Hole positions are the diagram-of-record; sizes trace to the foot
  constants + the current corridor model (deliberately NOT the shared `FP_CORNER_SEAT_*`, which is the film-plane
  corner-seat spec). Registered in the gallery / publish.sh / setup_docs / dependencies.yml and embedded in
  report §8.

- **IBC frame Sheet 4 — DETAIL F: walkway arm → front-upright connection.** Added the sixth detail inset:
  how each right-walkway cantilever arm attaches to a front corridor upright. Corrected from an assumed
  weld to the ACTUAL design (per `ibc_cantilever_arms`) — a **bolted clamp**: 2 clamp plates wrap the
  upright + 2× M12 through-bolts at two Z levels (no weld). Reclassified the connection across the whole
  blueprint: `ibc_frame_load.py` now checks it as a 2-bolt clamp (couple over the ~37 mm bolt spacing,
  **SF 3.8**, up from the SF 3.3 weld estimate); report §3.4 (clamp, not weld), §3.5 (new fastener **J6**;
  **W9 removed** from the weld schedule), and §8 (Sheet 4 now A–F). Clamp hardware is procured with the
  walkway-arm assembly (walkway blueprint), not double-counted in this frame's BOM.

- **IBC detail sheets consolidated + corrected per review.** Fabrication details now live on a single sheet
  (`ibc-frame-sheet4`), reworked per feedback: DETAIL A hanger as a SECTION (bolts through the backing
  plate + wall + pocket — not the bar; vertical pair 50 mm clear; standard bolt-in-section symbols),
  DETAIL B cleat as a section with vertical bolts, DETAIL C two lash rings each on its weld plate with
  ring-pitch/bar-end dims + a jagged bar break, DETAILS D/E captive tee-nut as a rectangle + countersunk
  screw. `ibc-stacking-sheet2` repurposed from duplicate fastening details to a **securing arrangement**
  (the 8 lash-point locations + strap routing — the rigger's plan; construction → Frame Sheet 4), dropping
  the operational ratchet-buckle close-up.

- **IBC equipment panel top dropped to open the Fan A air path.** The corridor equipment panel (18mm
  rear ply + 25mm pump-mount shirt) was capped at Z2191/2256, blocking airflow through the panel to the
  sealed-end Fan A exhaust. Dropped **both plies to Z1900** — the underside of the Fan A baffle window
  (Z1900–2100) — so the corridor is open across the fan. New driftproof `PANEL_TOP_Z = FAN_A_H −
  DUCT_HEIGHT/2` (was a stale `DV_Z + DVB` tie to a DV-02 that Phase-2 relocated to the pinhole-wall
  skid). The **top pair of welded frame bolt-tabs** ("Rear-panel bracket") dropped 2176→1780 to sit
  under the new panel top. Also corrected the rear-panel ply label marine→exterior (dry backing, per the
  plywood rule). In the water model the corridor panel is now drawn **solid in every scene** (un-muted +
  the redundant "solid" LOD duplicate dropped, its orphan tag purged) so the shirt/backing read as a
  solid backdrop rather than the faint 0.18-alpha ghost. Re-sent the 6 models that draw the shared
  corridor frame/panel (overview, water, walkway, construction, film-plane-mechanism, ibc-stack). No
  BOM/cost change (same sheets, cut shorter).

## [0.6] — 2026-08-13

- **Film-plane LEFT edge pulled inboard of the pivot hub (`FP_X_L` 150→260).** Resolved a hard
  clash found once the detailed corner was in the light-trap: the backing-side carriage rode straight into
  the swing-pivot hub. Resolved by bringing the film plane inside the swing-pivot.
  Costs ~110mm image width (`FP_W` 4499→4389, active area 101→99 sq ft); the
  now-asymmetric plane re-centers the pinhole (`PH_X` 2399→2454, +55mm). Cascaded to facts/CLAUDE.md optics
  table, 11 diagram generators, and 8 SketchUp models. NB: the removable-rail lift-out STAYS — the inboard
  move clears the pivot region but the panel's long swing arc still crosses the rail in the near/removable
  zone (Yd ~1950–2066), so that section must still lift out for transport.

- **Film-plane corner mechanism — definitive engineering blueprint (milestone template, branch
  `corner-eng-design`).** Upgraded one corner from arrangement-schematic to fabricator-ready, driven
  from `tbs_constants` so it can't drift: sheets 3/4/8/9 dimensioned (skate roller ODs + 40mm pitch;
  rail wall-flange bolt pattern; cross-slide bar section/travel/gib/UHMW; U-joint envelope Ø19.1/68/bore
  9.53/±45°, J5 hole pattern, L-plate 6×8 bend); **J1–J5 fastener schedule with torque/class/washer/locker**
  (M8 24 N·m, M6 10 N·m, setscrews ~2.5 N·m); a **datum + tolerance scheme** (datums A/B/C + GD&T). Firmed
  the load (162 N/corner, section SF 4.5/27) and, to hold ±40°/±28°, grew the cross-slide bar (+$135 film).

- **Stainless-grade reconciliation (304 vs 316) — system-wide policy.** The cyanotype wash has no
  chloride, so 316's pitting resistance is unused → **304 (A2) is the default** for all wet structural
  stainless; 316 is metallurgically unneeded (kept only on the tray seam bolt by choice). Codified as a
  policy block in the `parts.py` registry header. The actual corrosion gap was zinc fasteners in wet zones,
  so upgraded `bolt-m6x20` (×2) + `bolt-m8-fixing` → 304 A2-70; the M12 structural through-bolts keep
  Grade 8.8 zinc (strength + exterior inspectable heads). 410 self-drillers + chrome-steel bearing kept.

- **Film-plane corner — Phase-1c load case computed + decided → Sheet 10.** New `fp_corner_load.py` (driven from
  `tbs_constants`, renders `film-plane-sheet10.png`). **C2** verifies the cross-slide travel: Z (tilt ±40°)
  = 245mm and X (swing ±28°) = 257mm exactly match `XSLIDE_Z/X_TRAVEL`. **C1** the per-corner load (W/4 =
  124N) → X-slide bending safety factor — bar orientation is decisive, **DEEP** (38.1mm in the load
  direction) SF≈10, **FLAT** a marginal 1.7 (fails at ×2). **DEEP** was chosen on this basis.

- **Film-plane blueprint: Sheet 7 upgraded from system-arrangement to fabricator-grade GA.** Added the
  frame-fabrication content a shop needs: DETAIL A corner joint (45° miter + TIG fillet, per the joint
  decision) with the 2"×2"×3/16" 6061-T6 angle callout; the ACM backing strip layout (4 vertical Dibond
  strips, 3× 1219 + 1× 732 mm, 3 butt seams, splice-battened); and the 58× nylon-spring-clamp stations
  @ 150 mm (top + 2 sides).

- **Model `.rb` retired from git → `dependencies.yml` source_hash manifest; Sketchfab UID
  consolidated.** The 10 generated SketchUp `.rb` were committed only as a diff/staleness proxy for
  the binary `.skp`; they're now gitignored, replaced by a per-model `source_hash` in
  `dependencies.yml` — `sha256` of the regenerated, identity-stripped, float-normalized `.rb`
  (`src/generators/manifest.py`; `lint.py --verify-all` recomputes + compares, `manifest.py --update`
  refreshes). Same drift tripwire, no expanded Ruby in the repo, and immune to the float-noise that
  spuriously flagged the old byte-diff. Also folded the model registry into `dependencies.yml`: each
  model now carries its `uid` + `embed_files` there as the single home (generators read the uid via
  `ov.model_uid()` instead of hardcoding it; `push_sketchfab.py` reads/rewrites it), resolving the
  UID drift (it lived in both the generators and the 6-of-10 `models/sketchfab.json`, which is now
  retired). New `lint.py` gate: models must declare a valid uid/embed_files/source_hash.

- **Pump-run support-detail fabrication sheet (#29 follow-up).** New `generate_support_detail.py`
  → `support-detail-sheet1/2.png`. Sheet 1 = face-on board elevations (far / near / near-upper —
  18mm ply, 4 L-brackets each, risers + P-clip rows, fully dimensioned); Sheet 2 = the L-bracket
  flush-mount plan section (post inner face → 6mm weld leg → 45mm landing leg → ply seated flush,
  fastened with an M6 countersunk flat-head screw into a captive pronged tee-nut), a P-clip
  cross-section, and a fabrication schedule (3 boards / 12 brackets /
  39 clips). Geometry imported from the `cp` model constants so it can't drift. Embedded in
  plumbing-report §5.3; registered in the gallery, publish, setup_docs, and dependencies.yml.

- **Pump-run support boards in the IBC plumbing corridor (#29 follow-up).** The cantilevered pump
  risers on the two corridor side walls now land on **three 18mm ply boards** (far wall + lower and
  upper near-wall boards), each recessed **flush**
  in the window between the front & rear side-posts (399mm wide) on **welded steel L-brackets** (one
  leg welded to each post inner face, the ply bolted to the landing leg — the rear-panel method), with
  the risers held by **cushioned P-clips**. The **same P-clip method was extended** to the **drain-riser spine**
  (the 3 gray waste risers — X4 waste / DV-02 / DV-01→merge) and the **filter-skid panel** (the
  3 vertical runs — DV-02→F1 + tray-sump→P-04, F3→SV-01 already there —
  plus the horizontal runs: brown ± ACC-02 flush, and standoff clamps on the blue ± SV-01 and the
  brown DV-02 row). **Operability + review pass:** BV-03 handle rotated to −X (cargo door); a second
  **upper near board (Z1260–1950)** backs BV-02/BV-06 + the brown P-05 (Z1300) and gray P-03 (Z1902)
  horizontals; BV-02/BV-06 handles rotated +Yd into the corridor and their loops pulled to the
  **walkway edge (X4770)** for reach, labels moved to the valve centers on the operator side;
  spine far-side X-port lines (P-05→X3, P-03→X4) clamped; the DV-01→IBC-3 tote entry dropped to
  Z1080 with the flange seated on the cage edge and the run simplified (straight in, no drop-jog).
  **BOM/cost:** 3 ply side boards (cut from the
  corridor 4×8 offcut — no added ply), 12 welded L-brackets, 39 cushioned 3/4" P-clips →
  **+$33/$46/$61 water** (grand total $26,024/$30,492/$37,028).

- **SketchUp `--send` memory-bloat investigation (tooling, not published).** Ran a full investigation
  into the SketchUp process ballooning over repeated `--send` (TODO tooling item). Falsified the
  "Ruby allocations not freed" hypothesis empirically (isolated `TOPLEVEL_BINDING.dup`, flat Ruby heap
  across 12 re-sends, zero globals/constants/closures, `purge_unused` clean); root cause is SketchUp's
  **C++ allocator retaining freed pages** (not reclaimed by GC/purge/File>New — only a restart clears
  it). No code fix; mitigation is workflow (restart during heavy send sessions). Written up in
  `sketchup-memory-investigation.md` (repo-internal, not a TBS artifact). Follow-up hardening:
  added `materials.purge_unused` to the two water builders that lacked it (now standard across
  all 11 generators, self-cleaning orphan materials each rebuild); `layers.purge_unused`
  deliberately not added (the existing `keep_tags` prune is stricter and scene-safe).

- **Spray-beam removal cycle (#28) closed as no-lift / park-and-roll.** Decided against a lift-out
  mechanism: the muslin loads by parking the gantry at the near end and rolling the beam back over
  the laid fabric (report §4.2), and beam service is via the right-walkway grate (§4.3). Verified the
  **9mm beam-to-floor gap** from the constants (Ø32 wheel radius 16 − 7mm bracket drop, constant across
  the traverse) → **~8.5mm over the 0.5mm muslin**, wheels running outboard on bare floor.

- **Structural sections re-specced to stock imperial tube (#26) + mid-span support confirmed (#27).**
  The walkway/floor-leg/IBC/brace members were carried in metric-nominal sizes that aren't sold in the
  US. Re-specced to confirmed stock: the shaved right-walkway long beams, the 2 mid-span center arms,
  and the 5 floor-leg arms → **2×1×0.120in steel** (2×⅞ is non-stock — MetalsDepot/Metal Supermarkets
  carry only 2×1; $6.35/ft bulk); the IBC frame, film-plane brace, floor-leg posts, and swing/hinged-panel
  frames → **2×2×0.120in** (50→50.8); the tray bearer → **2×2×0.125in 6061 Al**. 2×1 is *deeper* than
  2×⅞, so the arms get **stronger** (SF≈2.5 vs 2.1) — Option B keeps the deck height, trading 3.4mm of
  spray-beam clearance (15→11.6mm). Real 2×1 pricing corrected the RWK frame (+$107/+$123
  walkway; the old $28–40 was a guess for a non-stock section); grand total → $25,991/$30,446/$36,967.
  8 diagrams + 6 model `.rb` regenerated (`.skp` re-send pending).

- **Braided flex on both ports of every pump (#29).** Extended vibration isolation from inlet-only
  to **both the suction and discharge** of all five pumps — a braided ½" jumper de-couples each pump
  from the rigid PVC run so vibration can't fatigue-crack a solvent-weld joint (P-04's suction is the
  1" tray-drain hose → 9 new ½" jumpers). Shown on the water-system P&ID (a flex coil on both ports
  of P-01…P-05); BOM adds the 3rd braided length + **18× ½" barb couplings** (Rain Bird BC50-20) +
  **18× SS clamps** (Everbilt 671255E), **+$55** water. Plumbing-report §5.2 made explicit.

- **Ball-valve sourcing + BV-05 spray selector re-designed as two 1/2″ valves.** The five 1/2″ 2-way
  isolation valves (BV-01/02/03/04/06) re-sourced Banjo V050FP → **Grainger 803HZ1 at $24.14** (from
  US Plastic $44.27, **−$120**). No 1/2″ 3-way L-port is stocked (only 3/4″ Banjo V075BL $72.88 +
  reducers), so **BV-05 became two 1/2″ valves**: **BV-05a** (3-way Blue/Brown selector, reuse the
  #22365 divert valve) + **BV-05b** (2-way spray on/off, **wall-mounted** above the selector, off the
  moving spray-bar pole) — all 1/2″, no reducers, no L-port OFF-detent risk, ~$37 under the L-port
  (net water cost this pair: **−$96**). Modeled in all four 3D models (water/overview/construction/
  ibc-stack); plumbing report §4.1 rewritten. The **overview** opening camera was also turned 180° to
  look into the container from the far wall.

- **Sump→P-04 suction re-routed off the pinhole wall.** The tray-drain suction ran as a tall riser
  straight up the pinhole wall (a clash); it now rises only ~150 mm above the walkway deck, turns 90°
  toward the skid, runs above the walkway, then a second 90° turn up into P-04 at the skid.

- **Muslin re-cut to fit the washable tray; spray-beam lift-out resolved operationally.** The muslin
  is now cut to the **washable tray area** — **4,359 × 2,000 mm** (`MUSLIN_CUT_W/H`), narrower AND
  shorter than the film-plane ACM+frame (4,499 × 2,094) so it lies flat clear of the side rims and the
  near-rim sump well; the tray, not the optics, is the size constraint (captured print ~94 of the
  101 sq ft plane; muslin yardage 388→360 yd, still 3 rolls, no cost change).

- **Spray-bar + processing-tray redesign — full-width beam, center-draining tray.** The spray beam
  went to a **full-width 1½×1½×0.062″ square tube with 44 nozzles** (from the short 40×25 section);
  the tray floor was re-sloped to a **Yd-only 1:200 fall** (far rim high → near rim low, level across X)
  feeding a **near-rim gutter that itself falls 1:200 in X to a single center sump well at X=2399**
  (replacing the old IBC-corner drain). The sump pickup **pops up through the walkway on a vertical
  riser**. Cascaded through the constants, every 2D sheet, and re-sent every affected 3D model
  (overview / spraybar / walkway / construction / ibc-stack / water).

- **Walkway support shaved to 2×⅞″ for spray-beam clearance.** The right-walkway long-beam and the
  left floor-leg arms dropped 40×40 → **2×⅞″** (soffit Z80/75 → Z93) so the full-width beam clears by
  ≥15 mm. (Follow-up mid-span stiffening is tracked in `TODO.md`.)

- **Phase-2 water topology — the tray drain now feeds the filter train.** Re-plumbed so tray-drain
  water is **filtered before returning to the totes**: **P-04 (tray-drain) relocated from the corridor
  to the pinhole-wall filter skid** (P-04 → SV-02 → 3W-DV-02 → F1/F2/F3 → SV-01 → 3W-DV-01 → IBC-3
  recycle / IBC-4 waste), and **P-02 (recycled-spray) took P-04's corridor slot** (P-02 → ACC-02 →
  3W-BV-05 spray selector). Blue supply isolated; the recycle loop closed. The Sheet-1 P&ID schematic
  was redrawn to match, and water.skp rebuilt (skid-panel reorg, ribbons routed onto the ply,
  3W-BV-05 dropped clear of the aperture).

- **BOM / cost reconciliation.** Added **ACC-02** and the **pinhole-wall filter-skid backing ply**
  (exterior grade, not marine) to the registry; reconciled the `project-cost-breakdown.md` §5
  water-system table to `costing.WATER` (fixed a positional-fill row-shift that broke the table
  arithmetic). Single-sourced the skid constants, SV-01's raised height, and the muslin cut size.

- **Tooling / process hardening.**
  - **Cascade tracking now follows the module-import graph** — a model that reuses another module's
    builders (e.g. `water.skp` via `import generate_sketchup_model`) inherits its constant deps, so
    the `--cascade` re-run list catches builder-reuse models the old grep scan missed.
  - **Pipe-crossing audit enforced by a lint gate** — `check_interference.py` detects crossings by
    centerline distance (no more join false-positives) and a commit gate blocks a reroute unless the
    interference report is refreshed.
  - **Water model normalized** — `--save` now writes a committed, deterministic `water.rb`, so
    `lint --verify-all` byte-verifies it like the other nine models instead of nagging "re-send
    manually" every run.

- **Materials.** Black ACM (dibond) re-sourced to Central Coast Plastics after Curbell couldn't
  supply (price TBC). Muslin set to the image plane exactly (no hem).

## [0.5] — 2026-08-02

- **Part/SKU reconciliation.** Major rework and reconcilaition of all the parts that need to be ordered to construction the poject. This required some rework of systems to accomodate what could be ordered vs. what is theoretically possible. All priced and firmed up in the registry to get a more concrete costing. Until we have a full set of blueprints, the fabrication estimates will need to wait, so this is still an unknown in the overall costing.

- **Fastener BOM decomposed into bolts / washers / nuts for ordering.** Split the 11 bundled
  "bolt + nut + washer" kit lines into separate component parts, using **shared keys** so nuts and
  washers total **by size + type across the whole build** (M12 flat washers **220**, M12 plain nuts
  **110**, M5×16 CSK screws **184**, …) while bolts stay itemized **by size × length**. The master
  BOM's fastener section now reads as a purchasing block.

- **Muslin clip re-design**. Removed the bespoke clamp design and replaced it with off the shelf spring loaded quick-grips.

- **Right-walkway muslin-rod / beam clash resolved by cranking the inner cantilever beam.** The muslin's
  rigid bottom rod must drop straight down at the tray edge through the muslin-drop notch,
  but the inner long beam of the cantilever rectangle sits directly under it. Rather than cut the beam at
  mid-span of its ~1.1m end bay, the inner beam is **cranked outboard 100mm** (the full notch depth) over
  the notch with ~100mm angled ramps each side. Sheet 3 (Detail A) shows the crank + rod
  slot; report §4.1 + docstring updated. No new parts.

- **Walkway decks reworked to continuous cut pieces** — bump-out & punch-out now integral, not
  butt-jointed add-ons.** The near-walkway EP/battery bump-out and the left lift-out's drum-exit
  punch-out were each modeled as a *separate* box butt-jointed onto the deck — which reads as
  "needs its own support." Both are now **one continuous L-cut** (new shared `near_fixed_deck_grate`
  + `left_liftout_grate` prism helpers), matching how they're cut from flat GRP stock: no mid-deck
  joint at either widening. The muslin-drop notch folds into the same left piece. Only the four
  corner joins and the **one unavoidable near/far sheet seam** (molded GRP tops out at 3′×10′, and
  the near run is ~3.9m) remain as joints — the seam is placed away from the bump shoulders. The
  bump-out itself is carried by the deeper 500mm-arm wall-cantilever brackets at 457mm rib centers.

- **Light-lock plastics firmed — one weld-compatible HDPE.**
  Priced all four light-lock/panel plastic parts to actual [US Plastics](https://www.usplastic.com/)
  sheet: the Ø900 housing to **3/16″ HDPE** ([46685](https://www.usplastic.com/catalog/item.aspx?itemid=136962&catid=705),
  3 sheets = $555) and the drum, panel skins, and B2 bay to **1/8″ HDPE**
  ([46684](https://www.usplastic.com/catalog/item.aspx?itemid=136961&catid=705), $123.34/sheet).
  This consolidated the drum/skins/bay off the nominal *4mm PP* onto HDPE — all light-lock plastic is
  now **one weld-compatible material** (PP↔HDPE won't extrusion-weld). Booked the real **1/8″ (3.18mm)**
  thickness through the constants + weight model (`LT_DRUM_T`/`PANEL_SKIN_T`/`BAY_WALL_T` → 3.18), cutting
  the swinging-panel assembly **~12 kg** (panel 171→161, drum 38→36; structure 584→572, dry 3,238→3,226).
  The drum's 2 **end caps stay 3/16″** (`LT_CAP_T`, thicker than the 1/8″ shell) — they carry the stub
  shafts into the SKF 6215 bearings, so the hub load path keeps its stiffness; cut from the housing offcut.

- **Wall through-bolts finalized: partial-thread, right-sized to the container-wall grip.** A grip
  analysis against the ISO container spec (side-wall corrugation ~25–30mm, not the ~38mm the prose
  assumed) showed the M12×80/×90 through-bolts were oversized. Re-sized every wall bolt. Designed for the **30mm worst-case grip**
  with a flat-washer shim allowance (2→4 M12 washers/bolt) so the bolt spec is robust across 25–30mm
  corrugation with **no container measurement needed** — pad to suit. Added `CONTAINER_CORRUGATION_DEPTH`
  constant.

- **Film-plane seal parts sourced; parts-identity lint fully clear.** Swapped the EPDM foam tape to
  [McMaster 8694K88](https://www.mcmaster.com/8694K88/) (1"×½", 25 ft rolls) and right-sized the qty
  to **2 rolls (50 ft)** against the ~43 ft film-plane perimeter — the old 3×50 ft = 150 ft was ~3.5×
  over (provisional).

- **IBC transport lashing → weld-on tie-down rings.** Sourced the restraint lashing points to
  [McMaster 3028T31](https://www.mcmaster.com/3028t31/) — a 1½" ID × ½" thick, 6,600 lb WLL,
  zinc-plated-steel **weld-on** ring — replacing the plain-D-ring + separate-mounting-plate approach
  with a single integrated weld-on part (fillet-welded straight to the front retaining bars, no
  plate, no retainer). The 6,600 lb ring far exceeds the 25mm-strap-limited 1,100 kg assembly WLL,
  so the full spec holds with no downrating. Report §4.1 + Sheet 1 label + BOM + the IBC frame cost
  band updated (−$15/−$30).

- **Fix: 4 gallery diagrams were broken images on the site** — the film-plane corner-joint study
  diagrams (`film-joint-options`, `film-joint-study-gimbal`, `film-joint-study-ujoint`,
  `film-corner-gimbal`) were listed in `all-diagrams.md` but not registered in `publish.sh` /
  `setup_docs.py`, so their PNGs never synced to `published/assets/` (404 on the live gallery). Added
  them to both sync registries and re-published. (Shipped broken in 0.4 — the lint gallery-gate checks
  the markdown lists every PNG but not that each is wired for syncing.)

## [0.4] — 2026-07-20

- **Film Plane Redesign** - Major rebuild of how the film plane pivots around the four corners. A new 3d model was created **`film-plane-mechanism.skp`** and `film-plane.skp` was retired along with its generator. The design centers around a U-Joint on each corner along with 2 slides per corner for articulation. The U-joint funnels
  the whole corner into a **304 stainless corner plate**. Parts are SKU's all reconciled along with the budget estimate.

- **Light-trap door top/bottom seals → strip brush** — the two horizontal door-frame seals the
  swinging panel edge *sweeps across* were changed from a steel seal-lip + EPDM compression to a
  **nylon-filament strip brush**. The panel/drum-box top edge's deliberate ~30mm overlap is now recorded
  as intended bristle engagement, **not** a clash.

- **Film-plane muslin clamp: cam-lever → spring clip** — retired the cam-lever toggle for a spring
  clip: a fixed jaw bolted to the ALU frame upstand (countersunk bolts, nuts on the inside) + a
  spring-loaded jaw that pinches the muslin + a neoprene pad onto the ACM board, squeeze-to-open
  (torsion spring holds closed).

- **TBS-002 "Mini-TBS" classroom camera** — the proof-of-concept two-box cardboard pinhole
  camera was recast as an educational design (Part I teaching / Part II build) and refined
  throughout: the film plane became a cut-cardboard flap (no foam board), push-pin paper
  mounting, a pin-load-seal-coat-dry coating sequence done by feel in the sealed box (no
  safelight), a single wash tray, a re-centered pinhole, and — the key fix — print extraction
  through the boxes' **own top flaps** (built flaps-up) instead of a custom-cut wall. Added an
  interactive **Sketchfab 3D model** (ghosted boxes joined with gray tape; clickable shutter,
  film-plane panel, and top flaps) embedded in the doc, generated from a new
  `generate_mini_tbs_model.py` with geometry single-sourced from `mini_tbs_constants.py`.

- **Site footer + theme overrides** — the footer now reads inline as
  `© 2026 Alvin Richards — Released under GNU AGPLv3. Version v0.3` instead of dropping the bare
  `v0.3` onto its own right-justified line (which wrapped and read oddly), and the Material theme
  overrides moved from `overrides/` to **`src/overrides/`** (`custom_dir` updated in `mkdocs.yml` +
  `setup_docs.py`; the footer partial is `src/overrides/partials/copyright.html`).

## [0.3] — 2026-07-09

- **Fix: an arch-broken heavy dep no longer blocks commits** — the weight generator guarded optional
  numpy/matplotlib with `except ModuleNotFoundError`, which does NOT catch a wrong-arch/ABI `dlopen`
  failure (a *bare* `ImportError`), so an arm64 numpy under an x86_64 python crashed the `weight` lint
  gate and blocked check-in. Broadened the guards to `except ImportError` (degrade to the math path),
  added a `lint.py` check that flags the narrow pattern, and documented the rule (CLAUDE.md § Optional
  Heavy Dependencies).
- **2d label cleanup** - pass to clean up messy and unreadable labels on all 2d diagrams
- **IBC report — diagrams inline** — the IBC stacking report embedded its 8 construction sheets only in
  the §8 gallery; each sheet now also appears **inline next to the section it illustrates** (cross-section
  + frame elevations in §3, fastening details in §4, bulkhead ports in §6, internal plumbing in §7),
  matching the other reports. The §8 gallery stays on the site but is `brochure:skip`-ped so the PDF
  shows the inline set only (no double-embed).
- **Brochure reconciliation** — Reduced dead space in the document (e.g. heading spacing, diagram size), removed sections that were not required (e.g. operating manual), followed format style of github site, and general re-organization of the PDF content.
- **3D overview scene + label pass** — reworked the per-subsystem scenes so each reads cleanly: the
  Ventilation scene gains the Fan A/B power cables (own tag) routed back to the EP, drops the
  plumbing-panel pump wiring, and shows only the evap-cooler (Cct E) circuit at the external panel — the
  PV + E-stop runs split onto a new "EP Ext Wiring" tag, kept in the Electrical scene. Labeled-scene
  leaders fixed (Fan B exits the cargo-door end, the filter-skid leader lands on the filters) and the
  solar array is ghosted so the exterior labels read through it.
- **Spray-bar supply hose** — added the flexible coiled feed from BV-05 (90° elbow → coil) up to the
  raised spray-bar feed pole, in both the overview and water models.
- **Spray-bar carriage bolts** — the tray-facing clamp-bolt heads are now drawn **countersunk** (a flush
  frustum seated in the clamp underside, top nut still proud) in the 3D model, matching the 2D detail.
- **Walkway top-rail brackets** — restored the film-plane **top-rail wall-seat saddle brackets**
  (interior back-plate + exterior through-bolted plate, at both the near and far walls) that the walkway
  model had dropped; the bottom rail stays on the shared combined corner plate.
- **Electrical focus model** — dropped the ghost ceiling so the model orbits freely without it occluding
  the gear, and added the two fan-feed callouts (Cct-A → Fan A at the sealed end; Cct-B → Fan B wall box
  + flex jumper) to the Labeled scene.
- **Water model cleanup** — the pinhole-wall water model drops the external EP panel + evap cooler, adds
  the spray bar for context, removes the green PV / gray E-stop EP cables, and reconnects the purple
  Cct-C pump feed to the panel's own master switch.
- **Non-destructive Sketchfab metadata** — the in-model metadata stamp is now fill-only-if-blank, so a
  regenerate / re-send never overwrites a model's saved title, description, tags, or stable UID.

## [0.2] — 2026-07-07
- **Electrical Panel Redesign** — the EP was reorganized into a tall narrow **vertical column** (battery
  packs re-stacked vertically, gear above, PV array disconnect dropped to operator reach) to fit the one
  clear wall band between the pinhole, chem shelf, and transport-stay anchors; the layout is formalized
  into `tbs_constants`. The 5026 fuse block and the IP65
  enclosure was corrected to its real datasheet footprint. The overview's EP now **delegates to the electrical model's builders**, eliminating
  the hand-maintained duplicate that kept drifting. Cascaded to the 2D (battery drawn as the stacked pair;
  Sheet-5 panel layout redrawn as the full column) and the weight CG. The near-walkway 500mm **widened
  access band** was then re-worked around the EP + chem shelf. The **EP column relocated left**
  to fit inside it, and the **chem-shelf
  depth trimmed 300→225** for walk-around clearance (275mm past the shelf, 328mm behind the EP).
- **Reconcile part dimensions** - resolved a number of drifts from the actual part dimensions vs. what had been
  codified and drawn in 2d and 3d models. Some parts rectified were evap cooler, skate wheels, film plane pivot, saddle straps etc.
- **Drift-tooling hardening** — added `lint.py --verify-all`, a staging-independent full sweep that
  regenerates every model `.rb` and byte-compares it against the working tree, catching **committed-stale**
  outputs that the staged-diff missing-cascade check can miss; wired it into the `publish.sh` deploy gate.
  Promoted the release-only `check_unused_imports` to a per-commit `lint.py` advisory and cleaned the 14 imports
  the EP re-lay had orphaned.
- **Single-source facts audit** — registered 5 previously-unpoliced system constants as `facts.yml` facts
  (corridor width, container rib spacing, IBC stack height, widened near-walkway, clamp spacing), each a
  `constant:` reference with a tight, verified alias, so a future prose restatement of these now trips the
  drift gate; wrapped the corridor-width restatements in `plumbing-report §3.2` as auto-updating placeholders.
- **Distortion-render de-duplication** — `tilt-swing-board-analysis §4` re-embedded the same nine C0–C8
  combined renders that `distortion-renders §3` (the dedicated gallery) already owns; §4 now points to the
  gallery and keeps only its unique content — the projection model and per-configuration optical analysis
  (renamed "Combined Distortion Analysis").
- **Walkway grating corrected 15mm → 25mm** — the 15mm molded-FRP grate was a **bogus spec**: the thinnest
  molded FRP made is 1"/25mm. Corrected to 25mm; the extra 10mm is absorbed **upward**, verified against the full 56° hinge-panel swing arc (arc only crosses the removable lift-out decks + open tray). Cascaded: film-plane
  bottom rail `RAIL_OFF_BOT` 150→160
  (−10mm image, FP wall anchors move), battery + evap-stow +10mm, grate weight 11→12.7 kg/m²



## [0.1] — 2026-07-03

Initial release of the basic design of all system components, and their integration
