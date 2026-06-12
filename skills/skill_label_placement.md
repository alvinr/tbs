---
name: Label placement skill
description: place_label(), leader(), and draw_notes() in tbs_drawing.py — label/leader/notes positioning rules extracted from user's manual "Tidy Labels" and "Tidy notes" corrections across all diagram generators
type: feedback
originSessionId: 54457a84-3dd4-4b25-a419-b2a4e2f11517
---
Use `place_label()` from `tbs_drawing.py` instead of raw `ax.text()` for component labels on P&ID schematics. Call `reset_label_registry()` at the start of each sheet and `register_pipe()` for each pipe segment to enable collision avoidance.

**Why:** The user spends significant time hand-repositioning labels after diagram generation. Patterns below are extracted from the user's "Tidy Labels" commits on both the filter skid diagram (5e95ad3) and the pinhole wall elevation (2ae2cb0, 22f8c02).

**How to apply:** When generating new diagrams or modifying existing ones, use `place_label()` for component labels and `leader()` for leader lines. Both are in `tbs_drawing.py`. Never use raw `ax.annotate()` for leaders — always use `leader()` which provides consistent dotted linestyle and connection behavior. The functions support easy overrides (`dx=`, `dy=`, `ha=`, `va=` for place_label; `fs=`, `color=`, `ha=`, `va=`, `font=` for leader). Apply these rules when placing labels:

### General positioning rules
- Valve labels: offset right and level with center, away from pipes
- Pump labels: offset right and slightly below center, closer to symbol than default
- Diverter labels: placed on the side with no pipe exit
- All labels: placed in the quadrant with the most white space

### Pipe annotation rules (from pinhole wall elevation "Tidy Labels")

8. **Flow arrows on long runs, far from components** — Place flow direction arrows well out along the long horizontal pipe run (e.g., +1400–1600mm offsets from manifold), not near the valve/component. Arrows need open space to be visible.

9. **Weighted midpoint for label centering** — On long pipe runs, use a weighted midpoint instead of arithmetic midpoint `(A + B) / 2`. The weight depends on available space: use `0.50–0.52` when the frame/component is close to the pipe exit (pump manifold), `0.55–0.61` when there's a long open run (pinhole wall elevation). Denser surroundings push the weight closer to 0.50.

10. **Labels between parallel pipe runs** — Pipe annotation text goes between adjacent parallel runs (e.g., `-35mm` offset placing text between Brown and Black pipes), not above or below both of them.

11. **Minimum annotation font size is 4.0** — No pipe or component annotation should use fontsize below 4.0. The user consistently bumped 2.5→4.5 and 3.5→4.0 across all annotations.

12. **Frame/container labels go inside the frame** — Labels like "PUMP MANIFOLD" and "FILTER SKID FRAME" belong well inside their outlines (e.g., 225–530mm below top), not above the frame. Placing labels above clutters the pipe routing space.

13. **Don't over-extend leaders** — Leaders should be short enough to clearly associate with the component. A leader that extends 350mm into empty space is too long; 75–200mm is typical. The user consistently shortened over-extended leaders.

14. **Every pipe run exiting the view needs a flow arrow** — If a pipe leaves the drawing edge toward IBCs or other equipment, it must have a directional arrow showing flow direction. The user added missing arrows on pipe exits (e.g., DV-01 waste output).

15. **Labels on same side as flow direction** — Pipe labels should be positioned on the side the pipe is flowing toward (downstream), not upstream near the component.

### Learned from filter skid "Tidy Labels" commit

1. **Small symbol clearance** — Labels near small symbols (end caps, check valves, circles) need more clearance than just edge-offset. Multiply the symbol radius (e.g., 1.5–2×) rather than adding a fixed pixel offset.

2. **Diverter junction anchoring** — Labels for diverters at multi-pipe junctions need their anchor point shifted further from the junction center (e.g., 40mm below the component center in drawing coords).

3. **Leader tips touch the component** — Leader arrow tips should terminate exactly at the component edge, not floating with an offset gap.

4. **Vertical separation near horizontal runs** — Leaders near horizontal pipe runs need more vertical separation. Route them diagonally up-and-out rather than straight sideways.

5. **Horizontal reach past dense structure** — Leaders pointing toward dense areas need a longer horizontal reach to land the text in clear space.

6. **Detail view dimension offsets > elevation offsets** — Detail views at larger scale (e.g., 1:2) need bigger dimension offsets than the main elevation (e.g., 0.5 vs 0.33 drawing units).

7. **Title block height scales with complexity** — Title block height should increase with the number of panels and notes lines: `height=0.04` for simple single-panel, `0.05` for two-panel, `0.06` for three-panel figures with long notes sections. The user bumped pump manifold from 0.04→0.06.

### Learned from pump manifold "Tidy Labels" commit

16. **Dimensions on the clear side** — Place dimension lines on the side of the component with more white space. The user moved pump body width dims from below (`Z - 30`) to above (`Z + 30`) the pumps because pipes and the walkway crowded the space below.

17. **Leader tips touch the actual material** — Leader tips should anchor to the edge of the specific material being called out, not the geometric center of the parent structure. E.g., the frame SHS leader tip was moved from frame center-bottom to the left SHS edge at 40% height. This ensures the leader clearly identifies *which* material it refers to.

18. **Long pipe annotations should wrap** — Single-line pipe annotations that exceed ~30 characters should be split with `\n` at a natural phrase break (e.g., "TO SPRAY BAR\n(BLUE DISCHARGE)"), keeping the main destination on line 1 and the system identifier on line 2.

19. **Notes block: large font, left-aligned** — The notes section at the bottom of the sheet should use fontsize 8 (not 6), be left-aligned at `x=0.15` (not centered at 0.35), and have adequate vertical start (`y=0.075`). Notes are reference material and must be easily readable.

20. **Plan view labels need extra clearance from end-on pipe symbols** — In plan views, labels near pipe-end-on concentric circles need 2.5–3× the symbol radius as clearance (e.g., `-45mm` not `-18mm`). The small circles make labels crowd easily at normal offsets.

### Notes block rules (from "Tidy notes" commit)

21. **No blank lines after the title** — Never insert an empty string `""` between the title line (e.g., `"NOTES:"`) and the first numbered item. `draw_notes()` already renders the title in bold with appropriate spacing — an extra blank line wastes vertical space and looks wrong.

22. **Use numbered lists, not bullets** — Notes items use `"1. "`, `"2. "`, `"3. "` etc. — never `"• "` or `"- "` prefixes. Always include a space after the period (`"1. Text"` not `"1.Text"`).

23. **Wrap long notes to keep the box narrow** — If a note line is too long for the target notes width, manually wrap it into continuation strings (no leading number). Priority is tight box width (rule 24/40) over one-string-per-note. But do NOT split into semantically separate entries — the continuation line should be an unnumbered continuation of the same note. Example: `"5. Anti-rotation lip: 5mm plate fillet welded to beam top face. Retains",` + `"IBC pallet perimeter.",`. Never split a single thought into two numbered items.

24. **Width should tightly fit the text, not fill the panel** — Set `width=` just wide enough to contain the longest note line at the given font size. Do NOT size width as a percentage of the axes (e.g., `width=sx(W_RANGE * 1.3)` is far too wide). Typical widths are 30–50% of the panel data range, not 60–70%. When in doubt, start narrow — a tight box looks intentional; an oversized box looks broken. Widths I had to fix: 60–70% ratios → 30–40%; absolute values cut by 30–50%.

25. **Prefer ha="left"** — Notes blocks should almost always use `ha="left"`. Only use `ha="right"` when the notes are anchored to the right edge of the axes AND there is genuinely no space to the left. The user changed several `ha="right"` blocks to `ha="left"` with repositioned x-coordinates.

26. **Every notes block needs a title line** — The first string must be an all-caps title ending with a colon: `"NOTES:"`, `"CONSTRUCTION NOTES:"`, `"TRANSPORT MODE"`, etc. Never start a notes list with a numbered item. `draw_notes()` renders this line in bold.

27. **Title block height should not overlap notes** — When notes are positioned below the drawing, ensure the `title_block()` `height=` parameter is small enough not to overlap. Typical values: `0.04`–`0.05` for sheets with notes below. The user reduced several from `0.06`→`0.04` and `0.09`→`0.05`.

### Learned from spray bar / walkway "Tidy labels" commit

30. **Condense multi-line dimension labels** — Merge two-line dimension labels (`"100mm\nDECK"`) into single lines (`"100mm DECK"`) when the combined text is ≤25 characters and doesn't collide with adjacent geometry. Only use `\n` when the single-line version would exceed ~25 chars or overlap something.

31. **Drop `bbox` in detail views** — Do not pass `bbox=` to `leader()` calls in zoomed detail views (Detail A, cross section, etc.). White background boxes eat into tight spaces at larger scales. Reserve `bbox` for the main elevation where labels may cross pipe runs or hatched sections.

32. **Minimum notes fontsize is 7** — Notes fontsize should be at least 7, not 5 or 5.5. Notes are reference material and must be readable at print scale. (Updates rule 19 — previous minimum of 8 was for the main notes block; 7 is acceptable for secondary/auxiliary notes.)

33. **Leaders on the clear side of features** — Place leaders on whichever side of a feature has the most white space, even if that means routing to the opposite side from the default. Don't assume right-side is default — check surrounding geometry first. (Extends rule 16 from dimensions to leaders.)

34. **Avoid repeating dimensions across views** — If a dimension is already shown in another detail view at the same or larger scale, don't repeat it in a second detail view. Each dimension should appear exactly once.

35. **Reposition labels to avoid geometry overlap** — When a label or dimension overlaps geometry (beam lines, walkway deck, pipe runs), move it: use `above=False` for dimensions, shift to the opposite side, or offset farther from the feature. Never let text sit on top of drawing geometry.

### Dimension and width rules (from second "Tidy labels" commit)

36. **Dimension offset minimum is 8** — `offset=` values of 5 in `draw_dim_h()` / `draw_dim_v()` are too tight — dimension text overlaps extension lines. Use `offset=8` as the minimum, `offset=10` for larger scale factors or crowded areas. The user bumped 5→8/9/10 across 18 dimension calls in ibc-frame and ibc-stacking.

37. **Short dimensions need leaders** — Any `draw_dim_v()` or `draw_dim_h()` where the measured distance is under 30mm should be replaced with a `leader()` call instead. The dimension text won't fit between the extension lines at that scale — it either overlaps or becomes unreadable. Use a leader from the midpoint of the feature to clear space, with the measurement as part of the label text (e.g., `"20mm SUMP DEPTH"`).

38. **Labels outside small symbols** — Do not place text inside symbols smaller than ~40mm (plan-view circles, small valve boxes, etc.). The text is unreadable at that scale. Instead, place the label beside the symbol in the symbol's own color. Example: P-04 on a 20mm plan circle — label moved outside in `color="#E8884A"` instead of white text inside.

39. **Dimension lines need 50mm+ clearance from geometry** — I consistently place `draw_dim_v` / `draw_dim_h` too close to the feature being dimensioned (15–30mm offsets in drawing coords). The user pushes them to 50–100mm+ for readability. Use at least 50mm offset from the nearest geometry edge; use 100mm+ when there's ample white space. This is about the placement position of the dimension line itself (the `x` or `y` argument), not the `offset=` parameter.

40. **Notes width: err tight, never overshoot** — When adjusting notes border width, I have consistently overshot (set too wide) and the user has reduced them in two consecutive "Tidy" commits. The correct width hugs the longest text line closely. If unsure, keep the existing value or increase by at most 20% — never double or add 50%+. A border that's 10% too narrow is better than one that's 50% too wide.

### Learned from "Tidy label and notes" commit (2026-05-25)

41. **Notes spacing should be compact** — `spacing=` in `draw_notes()` should be the minimum that keeps lines from touching. The user consistently reduces spacing: `100`→`80`, `88`→`60`, `sb(7)`→`sb(5)`. Don't pad vertical space between note lines — tight is better.

42. **Notes need edge margin** — Position notes at least 50 data-units inward from axes padding boundaries. Flush-to-edge positioning (`X_LO + 30`) clips or looks cramped — bump to `X_LO + 50` minimum. Similarly for Y: `Z_LO + 30` → `Z_LO + 300` when notes were being clipped below.

43. **Dimension `offset=` in mm-first diagrams** — After converting to mm-first coordinates, `offset=` values for `draw_dim_h`/`draw_dim_v` must be recalibrated. Old draw-unit values like `107` become literal mm and are far too large. Use `offset=25`–`80` in mm-first sheets, with `50` as a good default. The user changed `107`→`50`/`80` across multiple diagrams.

44. **Dimension positions: pull closer after mm conversion** — Dimension line X/Y positions that were computed with draw-unit padding (e.g., `C_LEN + 400`, `DIM_RIGHT`, `DIM_R`) often end up too far from geometry after mm conversion. Pull them closer: `C_LEN + 400` → `C_LEN + 200`, `DIM_RIGHT` → `DIM_RIGHT - 225`, `DIM_R` → `DIM_R - 150`. Dimensions should be close to the geometry they measure.

45. **Text color readability on fills** — White text is only readable on dark fills (navy, black, dark gray). On medium-value fills (orange, blue, green), use black text. Never color text to match its parent fill — e.g., `color=C_BLUE_IBC` on a blue IBC rectangle is unreadable. The user changed equipment panel labels from white→black on orange, and removed IBC-colored text in favor of default black.

46. **Annotation labels go inside their parent box** — Height/size annotations for equipment rectangles belong inside the rectangle (offset inward from the top edge), not floating above. The user moved IBC "2020mm tall" labels from `y + IBC_D + 55` (above) to `y + IBC_D - 55` (inside, near top edge). Labels above the box clutter surrounding space.

47. **Multi-line string concatenation: trailing commas** — In Python note arrays, multi-line strings that should include a space between them need an explicit trailing comma. Without the comma, Python silently concatenates adjacent strings (no space). Always end each note string with a comma, even when the list continues on the next line. The user fixed two note entries where missing commas caused garbled text.

### Learned from tilt-swing sheet 2 "Tidy labels" commit (2026-05-29)

48. **Align all leaders on one side in cross-sections** — In cross-section views where horizontal space is tight, route ALL component leaders to the same side (typically the right/interior side), stacking them vertically. Don't split leaders between left and right — the user moved the ICP-03 bearing leader from the left side (`brg_left - 10`) to the right, aligning all 5 component leaders in a single column at `lx_r + 20`. A consistent vertical column of text is cleaner than labels scattered on both sides.

49. **Dimension labels must include units** — All dimension text should include the unit suffix: `'300mm'` not `'300'`, `'40mm'` not `'40'`. The user added `mm` to every dimension label in the commit. Never rely on the title block's "ALL DIMS IN mm" note — make each dimension self-documenting.

50. **Annotation arrow text needs ≥30 units horizontal offset** — When using `ax.annotate()` with arrows pointing to geometry, place the text at least 30 drawing-units horizontally from the arrow anchor point. The user changed `wall_x - 10` → `wall_x - 30`. Text too close to the arrow tip crowds both and makes the annotation unreadable.

### Learned from film plane sheet 6 "Tidy labels" commits (2026-05-30)

51. **Leaders route away from crowded edges, into open interior** — When the area near a drawing edge (ceiling, floor, wall) is dense with structure, route leaders diagonally into the interior space rather than outward past the edge. The user moved all four right-side leaders from pointing upward above the ceiling (competing with rails and wall) to pointing downward into the film plane interior where there was open space. The leader tip stays on the component; only the text anchor moves.

52. **Vertical dimension lines ≤250mm from the drawing edge** — I placed vertical dim lines 500–550mm from the container wall; the user pulled them to 250mm on both sides. Dimension lines that float far from the geometry they measure look disconnected. Keep them within ~250mm of the nearest drawing edge. (Strengthens rule 44.)

53. **Harmonize font size across same-tier dimensions** — When multiple dimension lines are at the same hierarchy level (e.g., rail span + left end zone + right end zone), they must all use the same font size. Don't make one dimension larger than its peers — the user reduced the rail span fs from 7 → 6 to match the end zone dimensions.

54. **Embedded structural labels use smaller font** — Labels placed inside thin structural fills (container ceiling bar, floor bar, wall sections) should use fs=5, not the standard 6. These fills are narrow and the text must fit without clipping. The user reduced "CONTAINER CEILING" from fs=6 → fs=5.

55. **Tighten dimension row spacing to match content** — When stacking two rows of horizontal dimensions below a drawing, place them closer together than the initial layout. The user moved the second dim row from y=-340 to y=-300 (40mm closer). White space between dimension rows wastes vertical real estate and pushes the title block further down.

### Learned from spray bar sheet 5 "Tidy labels" commit (2026-05-31)

56. **Detail view leaders stay close to features** — In detail views (scale ≥ 2:1), don't push leader label endpoints to the viewport edges. Labels should be just 3–8 data-units from their anchor point horizontally, not 12–26 units. I repeatedly placed labels at `w_xr - 1` / `w_xl + 1` (flush with viewport edge); the user pulled them inward to `w_xr - 8` through `w_xr - 25` and `w_xl + 5` through `w_xl + 10`, halving leader lengths across the board. Longer label text (2+ lines, 15+ chars) needs the most inset — "CARRIAGE PLATE" went from `w_xr - 1` to `w_xr - 25`. At detail scale, over-long leaders make it hard to associate label with feature. (Strengthens rule 13 specifically for detail views.)

57. **Title text well inside viewport top** — Section titles and subtitles in detail views should be inset at least 10–15 data-units from the viewport top edge, not 1–4 units. The user moved the title from `w_yt - 1` → `w_yt - 10` and the subtitle from `w_yt - 4` → `w_yt - 14`. Titles placed 1 unit from the top edge look crammed against the boundary; breathing room makes them read as proper drawing titles.

### Learned from overview 3D-model label drift (2026-06-11)

58. **A label leader must always point at the thing it names — prefer geometry-anchored leaders over hardcoded coordinates.** When a component moves (a `tbs_constants` change, a relocation, or a redesign), its label leader MUST move to the new location in the same edit. A stale anchor leaves the leader pointing at empty space or, worse, at an unrelated part — e.g. the rev13 chem shelf moved to X1180–1780 but its 3D leader stayed at the old rev12 X3429 anchor, landing on the swing-panel transport-lock stay plate. **Prevent the whole class of bug by anchoring on the geometry, not a literal point:** in 3D models (`overview_labels()` and the per-model `*_labels()`), put the callout in the component-name list (`OVERVIEW_LABELS`) so it anchors on the live instance bounds (`bb.center`, `bb.max.z`) and tracks the part automatically. Only fall back to an explicit `(x, y, z)` point label when no single component represents the item (e.g. the two fans live in one component spanning both container ends) — and when you do, re-verify that point against the current geometry every time the part or a related constant moves. The same discipline applies to 2D `leader()` calls: when a part's coordinates change, update the leader tip **and** the label anchor together — never let one drift from the other. Run `check_consistency.py` after geometry changes, but note it does **not** catch a leader that still resolves to a valid (wrong) coordinate — a visual check of the labeled scene is the backstop.

### Learned from hingepanel "Tidy labels" commits (2026-06-11)

59. **Dense / 3D-style elevations: push leader text well out into the margin (200–350+ data-units of reach).** When the geometry fills the frame (panel front elevations, drum sections), labels can't sit near their feature without colliding — route the leader far into the surrounding margin. In one tidy pass the user enlarged ~14 leader/label offsets, all outward: `PW+180`→`PW+325`, `D_XR+150`→`D_XR+350`, `D_XL−120`→`D_XL−320`, `−HINGE_W−70`→`−HINGE_W−425`, `PIVOT_PX+185`→`PIVOT_PX+225`. This deliberately exceeds the 75–200mm "don't over-extend" of **rule 13** — that rule is for sparse 2D views; in a packed elevation the only clear space *is* the outer margin, so reach for it. Keep the leader **tip on the feature**; only the text anchor travels far out.

60. **Delete a same-view label that merely restates a dimension.** Rule 34 bans repeating a dimension *across views*; this bans the redundancy *within* a view. The user removed the floating "40mm CORNER / 120mm CENTER / 40mm CORNER" zone callouts because the adjacent dimension chain already read 40/120/40mm — the colored labels were noise on top of the numbers. If a value is already dimensioned on the sheet, don't also spell it out as a separate label.

61. **Give a label (and its leader) that crosses filled geometry an explicit high `zorder`.** A callout routed over patches/hatch must sit above them or it reads as broken/occluded. The user added `zorder=24` to a section callout drawn over the drum body. Set the text and arrow zorder above every patch they cross — don't rely on default draw order.

62. **Route section/material callouts and their dimensions to the *uncrowded* side — flip the anchor sign and the `above=`/`right=` flag together.** When one side of a thin feature is busy, anchor on the other: the user flipped material labels from `Y0 + T/2` (above the layer) to `Y0 − T/2` (below) and added `above=False` to the matching `draw_dim_h`, and flipped a `draw_dim_v` from `right=True` to `right=False`. Choose the side with white space and set the helper's side flag to match (extends rules 16/33/35 specifically to layered section/material callouts).

63. **Spread near-touching stacked callouts, and emit them in anchor order (top-down).** Two leaders landing at almost the same height read as one tangled block. The user separated a pair of top-seal callouts (`CY(62)/CY(96)` → `CY(82)/CY(68)`) and reordered the calls so the higher-anchored label comes first. Give each stacked callout ≥1 line of vertical clearance and list them top-to-bottom (extends rule 48's single-column alignment to vertical spacing).

### Learned from ibc-stacking sheet 5 inverted-axis legend box (2026-06-11)

64. **A hand-drawn background box (legend/key/note panel) must match the axis direction — flip the width sign on an inverted axis.** A `Rectangle((x, y), w, h)` drawn with a positive `w` extends toward *increasing data-x*; on an `ax.invert_xaxis()` sheet that is **screen-left**, while `ha="left"` text from the same anchor renders **screen-right** (toward decreasing data-x). So a box sized to wrap left-aligned content ends up parked on the *opposite* side of it — exactly what happened to the sheet-5 pipe-type legend (box left of the swatches, text spilling out the right). Fix: on an inverted axis, anchor the box just past the content's near edge and give it a **negative width** (e.g. `leg_box_x = leg_x + sx(75); leg_box_w = -sx(880)`) so it grows in the same direction the text flows. The shared `draw_notes()` already does this automatically (it reads `ax.get_xlim()` and applies a `sign`); any **hand-rolled** box must replicate that sign logic. Whenever you draw a manual box on a mirrored/inverted view, verify it actually encloses its content (crop-zoom the render) rather than assuming the positive-width default is correct.

65. **An offset text label on an inverted axis flows back over its component — give it a leader (or flip the offset sign *and* `ha`).** The companion to rule 64, for text instead of boxes. `ax.text(comp_x + offset, z, lbl, ha="left")` assumes a normal axis: the anchor lands beside the part and the text reads away from it. On an `invert_xaxis()` sheet the same anchor lands on the *opposite* screen side and `ha="left"` flows the text screen-right **back across the component** — on ibc-stacking sheet 5 the pipe cross-sections rendered `← P-04 [circle] TRAY SUMP` with the circle buried mid-label. **Preferred fix:** draw the label on a `leader()` whose tip is on the part and whose text is routed to the correct screen side — derive the sign from the axis itself, e.g. `inv = ax.get_xlim()[0] > ax.get_xlim()[1]; ddir = (-1 if inv else 1) * (1 if screen_right else -1)` (this is what `pipe_stub_x` now does). **Cheaper fix:** flip the offset sign together with `ha` so the anchor lands on the intended screen side and the text reads outward. Either way: skip the leader entirely for empty labels (an empty `leader()` draws a stray arrow), and for *clustered* symbols route each leader to the open side — into a large empty body, never the crowded centre where neighbours collide (the two blue OUTLET labels first both pointed into the corridor and overlapped; they had to be flipped to point into their IBC bodies).
