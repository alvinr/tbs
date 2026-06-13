---
name: Label placement skill
description: place_label(), leader(), and draw_notes() in tbs_drawing.py — 12 label/leader/notes/dimension principles distilled from the user's manual "Tidy Labels" corrections across every diagram generator. Each principle carries the concrete numbers; parenthesised (rN) tags trace back to the original per-commit rules.
type: feedback
originSessionId: 54457a84-3dd4-4b25-a419-b2a4e2f11517
---

Use `place_label()` from `tbs_drawing.py` (not raw `ax.text()`) for component labels on P&ID schematics; call `reset_label_registry()` per sheet and `register_pipe()` per segment for collision avoidance. **Never use raw `ax.annotate()` for leaders — always `leader()`** (consistent dotted line + connection). Both take easy overrides (`dx/dy/ha/va` for place_label; `fs/color/ha/va/font` for leader).

**Why this exists:** the user spends real time hand-repositioning labels after generation. The 12 principles below are distilled from ~69 per-commit "Tidy Labels" corrections; the `(rN)` tags point back to the original numbered rules (now in git history) if you need the full failure example. When you generate or edit a diagram, walk these in order — placement first, then formatting.

---

## Self-review FIRST — run this before you show or commit any diagram

The dominant cost on this project is the round-trip: I draw → the user "Tidy labels" → I extract a rule. **Cut it by self-reviewing against the 12 principles before the diagram ever leaves your hands.** This gate is not optional.

1. **Render it and crop-zoom every label cluster.** Never commit a diagram you have only reasoned about — look at the pixels (PIL crop at 2.5–3×). Most of my misses this week (floor-flange "keep it long," spray-bar anchor) came from reasoning instead of looking.
2. **Leaders:** each one shortest into the *nearest* clear pocket (P1), tip on the specific material edge (P3), nothing sitting on geometry/hatch (P2/P9). Sweep the *opposite* side before accepting a long one.
3. **Inverted axis?** (`ax.invert_xaxis()`) → hand-drawn boxes need a **negative** width and offset text needs a leader or a flipped sign+`ha` (P10). This bites every time and is invisible until you look.
4. **Dimensions:** units on **every** one; `offset` ≥8 (≈32–50 in mm-first sheets); anything <30mm gets a leader not a dim; no value both dimensioned *and* restated as a label (P7).
5. **Notes:** ALL-CAPS title + `:`, `ha="left"`, width hugs the longest line (hard-wrap to stay narrow), `fs≥7`, trailing comma on every string (P8).
6. **3D model labels:** does each leader tip land **on the part**, not the bounds-centre / mid-air above an outrigger? (P3 — `overview_labels()` now auto-snaps egregious floats, but still eyeball it.)

If a check fails, fix it *before* rendering the "final" — don't ship it expecting a tidy pass.

---

## 1. Shortest leader into the nearest clear pocket  *(r4, r5, r13, r51, r56, r59, r67, r69)*

The master rule for *where* a callout goes. Keep the tip on the feature; move only the text.

- **Method:** sweep 360° around the tip, drop the text into the *closest* gap in **any** direction (up/down/diagonal, not a habitual side), anchored ~one text-line off the feature edge. *(r67)*
- **Typical reach:** 75–200mm in sparse 2D views; **3–8 data-units** in detail views (≥2:1). *(r13, r56)*
- **Margin reach (200–350+) is the exception**, used only in packed elevations where the only clear space *is* the outer margin. *(r59)*
- **Before keeping a long leader** because the near side is "congested," test the **opposite** side of the feature and the adjacent open face — a clean face beats a closer-but-cluttered margin (e.g. FLOOR FLANGE moved from the dim-packed below-floor band to the open strip just *above* the floor). *(r69)*
- **Tie-break:** prefer the pocket whose leader crosses the **fewest** filled/hatched bodies. *(r67)*
- Near a horizontal pipe run, route diagonally up-and-out, not straight sideways. *(r4, r5)*
- `ax.annotate()` arrow text: keep **≥30 data-units** horizontal from the arrow anchor so tip and text don't crowd. *(r50)*
- **Loop:** pick the gap, anchor one line off, render, push farther only on an *actual* collision. *(r67, r69)*

## 2. Put it where the white space is — never on geometry  *(general, r10, r15, r16, r33, r35, r62)*

- Every label → the quadrant/side with the most white space. Check surrounding geometry; don't assume a default side. *(general, r33)*
- Dimensions follow the same rule — flip `above=`/`right=` to the clear side. *(r16, r62)*
- Section/material callouts: flip the **anchor sign and the side flag together** toward the uncrowded side. *(r62)*
- Pipe annotations sit **between** adjacent parallel runs (e.g. −35mm), and on the **downstream/flow** side. *(r10, r15)*
- If text overlaps geometry, move it (`above=False`, opposite side, larger offset) — never let it sit on top. *(r35)*
- Component defaults: valve labels offset right, level with center; pump labels right + slightly below, closer than default; diverter labels on the side with no pipe exit.

## 3. Leader tip on the specific material edge — and keep it synced  *(r3, r17, r58)*

- Tip terminates **exactly at the component edge**, no floating gap. *(r3)*
- Anchor to the edge of the **specific material** named, not the parent's geometric center (e.g. the SHS edge at 40% height, not frame-center). *(r17)*
- When a part moves (a `tbs_constants` change, relocation, redesign), move the **tip and the text anchor together** in the same edit. Prefer **geometry-anchored** leaders (put the callout in a component-name list so it tracks `bb.center`/`bb.max.z`) over hardcoded points; fall back to an explicit point only when no single component represents the item, and re-verify it on every related change. `check_consistency.py` does **not** catch a leader that resolves to a valid-but-wrong point — a visual check is the backstop. *(r58)*

## 4. Clearance scales with symbol size  *(r1, r2, r20, r38)*

- Small symbols (end caps, check valves, circles): **multiply** the radius (1.5–2×), don't add a fixed offset. *(r1)*
- Plan-view end-on pipe circles: **2.5–3× radius** clearance (−45mm, not −18mm). *(r20)*
- Symbols smaller than ~40mm: label **outside**, in the symbol's own color — never text inside. *(r38)*
- Diverter/junction labels: shift the anchor further from the junction center (~40mm). *(r2)*

## 5. Shape the text's wrapping to the gap  *(r18, r30, r66)*

- Add `\n` to go **narrow-and-tall** through a horizontally crowded spot; remove `\n` to go **wide-and-short** where there's room. *(r66)*
- Practical thresholds: >~30 chars → wrap at a natural phrase break (destination on line 1, system id on line 2); ≤25 chars → one line. *(r18, r30)*

## 6. Managing stacked / multiple callouts  *(r48, r63)*

- Tight cross-sections: route **all** component leaders to one side as a single vertical column. *(r48)*
- Give stacked callouts ≥1 line of vertical clearance; emit them in anchor order (top-down). *(r63)*

## 7. Dimensions  *(r6, r34, r36, r37, r39, r43, r44, r49, r52, r53, r55, r60)*

- **`offset=`:** min **8**; in mm-first sheets **25–80** (default ~50; mm elevation sheets ~**32**); detail views bigger than the main elevation. *(r36, r43, r6)*
- **Dimension-line position:** ≥50mm off the geometry but **≤250mm** from the drawing edge; pull close after a mm-conversion; stack rows ~**60mm** apart. *(r39, r52, r44, r55)*
- Always include **units** (`300mm`, not `300`). *(r49)*
- Harmonize font size across same-tier dimensions. *(r53)*
- A measured distance **<30mm** won't fit between extension lines → use a `leader()` with the value in the label text instead. *(r37)*
- Don't repeat a dimension across views, and don't restate a dimensioned value as a separate floating label. *(r34, r60)*

## 8. Notes block  *(r19, r21, r22, r23, r24, r25, r26, r32, r40, r41, r42, r47, r68)*

- First string = **ALL-CAPS title ending in `:`**; **no blank line** after it (`draw_notes` already spaces the bold title). *(r26, r21)*
- Numbered `"1. "` (space after the period), never bullets. *(r22)*
- `ha="left"` almost always. *(r25)*
- **Width hugs the longest line** (≈30–50% of the panel range, never 60–70%); err narrow — a tight box looks intentional, an oversized one looks broken. *(r24, r40)*
- Keep it narrow by **hard-wrapping items into hanging-indent continuation lines** (leading spaces, no number) rather than widening the box. *(r23, r68)*
- Spacing compact (the minimum that avoids touching). *(r41)*
- ≥50 data-units inward from the axes edge. *(r42)*
- Font **≥7**. *(r19, r32)*
- **Trailing comma on every string** — without it Python concatenates adjacent strings with no space. *(r47)*

## 9. Text legibility on fills  *(r11, r12, r31, r45, r46, r54, r61)*

- Minimum annotation font **4.0**. *(r11)*
- **Black on light/medium fills; white ONLY on dark** (navy/black/dark-gray). Never color text to match its own fill. *(r45)*
- Frame/equipment labels go **inside** the outline (well in, not floating above). *(r12, r46)*
- Thin structural fills (ceiling/floor/wall bars): `fs=5`. *(r54)*
- **Drop `bbox`** in detail views (white boxes eat tight space); reserve a white bbox for the main elevation where labels cross pipes/hatch. *(r31)*
- A label/leader crossing filled geometry needs an explicit **high `zorder`** so it isn't occluded. *(r61)*

## 10. The inverted-axis trap  *(r64, r65)* — genuinely unique; read in full

On an `ax.invert_xaxis()` sheet, increasing data-x is **screen-left** while `ha="left"` text still flows **screen-right** — so naive boxes and offset labels land on the *wrong* side of their content.

- **Hand-drawn background box** (legend/key/note panel): give it a **negative width** so it grows the way the text flows (`leg_box_x = leg_x + sx(75); leg_box_w = -sx(880)`). `draw_notes()` already does this via `ax.get_xlim()`; any hand-rolled box must replicate the sign. Crop-zoom the render to confirm it encloses its content. *(r64)*
- **Offset text label:** `ax.text(comp_x + offset, z, lbl, ha="left")` flows the text back **across** the component. Preferred fix: a `leader()` with the tip on the part and the text routed to the correct side, sign derived from the axis (`inv = ax.get_xlim()[0] > ax.get_xlim()[1]`). Cheaper fix: flip the offset sign **and** `ha` together. Skip the leader for empty labels (it draws a stray arrow); for clustered symbols route each leader into the large empty body, never the crowded center. *(r65)*

## 11. Flow arrows (P&ID)  *(r8, r9, r14)*

- Place direction arrows **well out** along long runs (+1400–1600mm from the component), where there's open space — not next to the valve. *(r8)*
- **Every** pipe leaving the view gets a direction arrow. *(r14)*
- Center a run label at a **weighted** midpoint, not `(A+B)/2`: 0.50–0.52 when a component crowds the exit, 0.55–0.61 on a long open run. *(r9)*

## 12. Title block  *(r7, r27, r57)*

- Height scales with content: **0.04** single-panel, **0.05** two-panel, **0.06** three-panel / long notes. *(r7)*
- Keep it small enough not to overlap notes positioned below. *(r27)*
- In detail views, inset the title/subtitle text **10–15 data-units** from the viewport top. *(r57)*
