<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# GRP Walkway Grating — Quote Request

Working doc (unpublished) to send a vendor for a molded-FRP grating quote. Not a report.

## Product spec

| Attribute | Value |
|-----------|-------|
| Type | Molded fiberglass (FRP/GRP) grating |
| Grid height | **1″** |
| Mesh | **1½″ × 1½″ square** |
| Resin | **Vinyl-ester** (chemistry-zone corrosion) |
| Surface | **Grit top** (non-slip) |
| Weight | ~2.6 lb/ft² |
| Open area | ~70% |
| Reference SKU | McNichols **MS-S-100** (vinyl-ester = SVF/XVE) · American Grating equivalent |

## Pieces needed (inches)

Walkway = 11.8″ (300mm) wide base strips + two "landing" add-on strips where it widens.

| # | Piece | W × L (in) | ft² | Note |
|---|-------|------------|-----|------|
| 1 | Near walkway | 11.8 × 163.7 | 13.4 | **>144″ — must splice (120 + 43.7)** |
| 2 | Far walkway | 11.8 × 163.7 | 13.4 | **>144″ — must splice (120 + 43.7)** |
| 3 | Right walkway | 11.8 × 93.0 | 7.6 | |
| 4 | Left walkway (removable) | 11.8 × 93.0 | 7.6 | lift-out |
| 5 | Near-wide add | 7.9 × 61.8 | 3.4 | extra width, EP/battery/slit + spray-bar bump (rev 2026-07-23) |
| 6 | Left-wide add | 11.8 × 29.9 | 2.5 | extra width, left landing |
| | **Total** | | **47.9** | excl. drum-exit |

## Panels to order — **2× 36″×120″** ($415 ea = **$830**, min sheets)

1× 48×144 can't do it (163.7″ runs splice anyway, and 47 ft² in 48 ft² = no cutting margin). 2× 36×120 nests with room to spare and is cheaper than 1×48×144 + a second panel.

**Panel A (36×120)** — 3 strips @ 11.8″ × 120″:
- Near-A `11.8 × 120`
- Far-A `11.8 × 120`
- Right `11.8 × 93` (27″ offcut)

**Panel B (36×120)** — 3 strips @ 11.8″ × 120″:
- Left `11.8 × 93` (27″ offcut)
- Near-B `11.8 × 43.7` ┐ splice onto the -A halves → 163.7″
- Far-B `11.8 × 43.7` ┘
- Left-wide `11.8 × 29.9`
- Near-wide `7.9 × 61.8`

![GRP grating cut plan — 2× 36×120 panels](diagrams/grp-cutplan.png)

## Cut coordinates (each panel 36″ W × 120″ L)

**Panel A** — rip at **11.8, 23.6, 35.4″**; crosscut strip 3 at **93″**:

| Piece | Width span (in) | Length span (in) | Size |
|---|---|---|---|
| Near-A | 0 – 11.8 | 0 – 120 | 11.8 × 120 |
| Far-A | 11.8 – 23.6 | 0 – 120 | 11.8 × 120 |
| Right | 23.6 – 35.4 | 0 – 93 | 11.8 × 93 |
| (offcut) | 23.6 – 35.4 | 93 – 120 | 11.8 × 27 |
| (waste edge) | 35.4 – 36 | 0 – 120 | 0.6 × 120 |

**Panel B** — rip at **11.8, 23.6, 35.4″**; crosscuts as noted:

| Piece | Width span (in) | Length span (in) | Size |
|---|---|---|---|
| Left | 0 – 11.8 | 0 – 93 | 11.8 × 93 |
| (offcut) | 0 – 11.8 | 93 – 120 | 11.8 × 27 |
| Near-B | 11.8 – 23.6 | 0 – 43.7 | 11.8 × 43.7 |
| Far-B | 11.8 – 23.6 | 43.7 – 87.4 | 11.8 × 43.7 |
| (offcut) | 11.8 – 23.6 | 87.4 – 120 | 11.8 × 32.6 |
| Left-wide | 23.6 – 35.4 | 0 – 29.9 | 11.8 × 29.9 |
| Near-wide | 23.6 – 31.5 | 29.9 – 91.7 | 7.9 × 61.8 |
| (waste edge) | 35.4 – 36 | 0 – 120 | 0.6 × 120 |

Crosscuts: Panel B strip 1 at 93″; strip 2 at 43.7″ and 87.4″; strip 3 at 29.9″, then rip Near-wide at 31.5″ (width) over length 29.9–91.7 and crosscut at 91.7″.

## Also
- Edge treatment: **Fibergrate Sealing & Bonding Kit** (~$50) — molded FRP cut edges are field-sealed with epoxy, not snap-trimmed.
- Hold-down: 30× SS grating clips (`walkway-holddown-clips`, separate).
- Drum-exit landing (~2.5 ft²): separate line `walkway-drum-exit-grp` (won't nest in the ≤11.8″ offcuts).

## Vendors
- **McNichols** — 877.891.7418 (quote-only, no public pricing)
- **American Grating** — public pricing, identical spec: https://www.americangrating.com/products/1-deep-x-1-12-square-mesh-molded-frp-grating__i-10.aspx
