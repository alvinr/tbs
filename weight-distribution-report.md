<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Weight Distribution Analysis
## TBS-001 — Container Load Assessment and Center-of-Gravity Study

*© 2026 Alvin Richards — Released under [GNU AGPLv3](licensing.md)*

---

## 1. Purpose

This report provides a comprehensive weight analysis of TBS-001, covering:

- Total weight of the container with all equipment installed (dry)
- Total weight with all liquids added (camera ready)
- Weight distribution (front-back, left-right) for three operational states
- Center-of-gravity (CG) position and migration between states
- ISO container gross weight compliance verification

The analysis is essential for transport planning, trailer axle placement,
structural assessment, and understanding how the system's weight distribution
changes during a photographic session.

---

## 2. Container Baseline

| Parameter | Value | Source |
|-----------|-------|--------|
| Container type | 20 ft standard ISO | ISO 668 |
| Tare weight (empty container) | 2,200 kg (4,850 lbs) | Hapag-Lloyd Container Spec |
| Max gross weight | 24,000 kg (52,910 lbs) | ISO 668 |
| Max payload | 21,800 kg (48,060 lbs) | Gross − tare |
| Interior dimensions | 5,893 × 2,362 × 2,388 mm | ISO 668 |

---

## 3. Component Weight Inventory

All weights are calculated from first principles (material density × volume)
unless a specific report value is cited. Material densities used:
mild steel 7,850 kg/m³, 304 SS 7,930 kg/m³, aluminum 2,700 kg/m³,
marine plywood 600 kg/m³, water 1,000 kg/m³.

### 3.1 Container

| Component | Weight (kg) | Position | Calculation Basis |
|-----------|------------|----------|-------------------|
| Container shell | 2,200 | Full footprint | Hapag-Lloyd 20ft ISO tare weight |

### 3.2 Structural Components

| Component | Weight (kg) | X Range (mm) | Yd Range (mm) | Calculation Basis |
|-----------|------------|-------------|---------------|-------------------|
| Hinged panel | 203 | 0–80 | 0–2,362 | Stepped sandwich: ply+steel corners, RHS center frame. Scaled to 240 kg combined with drum per [Light Trap Selection](light-trap-selection.md) §7 |
| Light trap drum | 37 | 0–40 | 756–1,606 | 1.5mm Al shell Ø750×2,200mm + 3 baffles + bearings |
| Processing tray | 116 | 170–4,629 | 80–2,280 | 304 SS 1.5mm, 2 panels × 58 kg ([Water System Report](water-system-report.md) §4) |
| Near walkway | 78 | 470–4,629 | 0–300 | 10 brackets @ ~2.7 kg + 44 kg/m² grating |
| Far walkway | 78 | 470–4,629 | 2,062–2,362 | Same as near walkway |
| Right walkway | 135 | 4,632–4,932 | 0–2,362 | 50×40×3 RHS beam + 17mm packer + grating |
| Left walkway | 35 | 170–470 | 0–2,362 | Removable lift-out: grating + 50×50×3 Al bearer beam + 3 legs |
| Ceiling rails | 48 | 0–5,893 | 30–2,332 | 2× HGR20 @ 3.7 kg/m + 8 carriage blocks |
| Container mods | 65 | Distributed | Distributed | Light seal foam + reinforcement plates (estimate) |
| **Structure subtotal** | **796** | | | |

### 3.3 Equipment

| Component | Weight (kg) | X Range (mm) | Yd Range (mm) | Calculation Basis |
|-----------|------------|-------------|---------------|-------------------|
| Electrical panel | 15 | 1,600–1,900 | 0–150 | Wall-mount distribution panel |
| Battery bank | 26 | 1,810–2,310 | 0–150 | 2× 100Ah LiFePO4 @ 13 kg each |
| Solar controller | 2 | 1,700–1,800 | 0–100 | MPPT charge controller |
| Pump manifold | 5 | 2,500–2,800 | 0–150 | 3× 12V diaphragm pumps + manifold |
| Evaporative cooler | 15 | 930–1,530 | 0–350 | Portable evap cooler unit |
| Film plane carriage | 33 | 150–4,649 | 2,212–2,312 | Al angle frame (50.8×50.8×4.8mm) + 92 cam-lever clamps + 4 HGH20CA carriages |
| Tilt-swing board | 30 | 2,199–2,599 | 0–400 | Spherical-pivot board + adjustment screws |
| Fans (A+B) | 4 | End walls | Near corners | 2× 150mm axial panel fans |
| Baffle ducts | 6 | Distributed | Distributed | 2× galvanized steel baffle ducts |
| Blue IBC-1 (tote) | 55 | 4,674–5,893 | 100–1,116 | 600L steel-cage IBC tare (top tier, near) |
| Blue IBC-2 (tote) | 55 | 4,674–5,893 | 1,141–2,157 | 600L steel-cage IBC tare (top tier, far) |
| Brown IBC-3 (tote) | 55 | 4,674–5,893 | 100–1,116 | 600L steel-cage IBC tare (bottom tier, near) |
| Waste IBC-4 (tote) | 55 | 4,674–5,893 | 1,141–2,157 | 600L steel-cage IBC tare (bottom tier, far) |
| IBC stacking frame | 31 | 4,674–5,893 | 100–2,157 | 40×40×3mm steel SHS frame |
| **Equipment subtotal** | **387** | | | |

### 3.4 Dry Weight Summary

| Category | Weight (kg) | % of Dry Total |
|----------|------------|---------------|
| Container shell | 2,200 | 65.1% |
| Structure | 796 | 23.5% |
| Equipment | 387 | 11.4% |
| **Total dry** | **3,382** | **100%** |

**Grating weight assumption:** 25mm press-locked galvanized steel bar grating
at 30×100mm bearing bar pitch weighs approximately 44 kg/m² (McNICHOLS
catalog). This is the dominant weight contributor to the walkway system and
the single largest source of uncertainty in the structural weight.

---

## 4. Liquid States

### 4.1 Camera Ready (Full Blue IBCs)

All wash water loaded in the two top-tier Blue IBCs. Bottom-tier Brown and
Waste IBCs are empty. Processing tray is empty (water is pumped to the tray
during processing, not pre-loaded).

| Liquid | Volume (L) | Weight (kg) | Position | Tier |
|--------|-----------|------------|----------|------|
| Blue IBC-1 water | 600 | 600 | X=4,674–5,893, Yd=100–1,116 | Top (Z=1,010–2,020) |
| Blue IBC-2 water | 600 | 600 | X=4,674–5,893, Yd=1,141–2,157 | Top (Z=1,010–2,020) |
| **Total liquid** | **1,200** | **1,200** | | |

**Total loaded weight: 4,582 kg** (3,382 dry + 1,200 liquid)

### 4.2 Materials Exhausted (Ready for Resupply)

After a full session, wash water has been consumed and redistributed.
Blue IBCs are empty; Brown (recycled) and Waste IBCs are full. The
processing tray has been drained — all processed water is in the
Brown/Waste IBCs.

| Liquid | Volume (L) | Weight (kg) | Position | Tier |
|--------|-----------|------------|----------|------|
| Brown IBC-3 water | 600 | 600 | X=4,674–5,893, Yd=100–1,116 | Bottom (Z=0–1,010) |
| Waste IBC-4 water | 600 | 600 | X=4,674–5,893, Yd=1,141–2,157 | Bottom (Z=0–1,010) |
| Processing tray | — | 0 | Drained | — |
| **Total liquid** | **1,200** | **1,200** | | |

**Total loaded weight: 4,582 kg** (3,382 dry + 1,200 liquid)

### 4.3 State Comparison

| State | Total (kg) | X_cg (mm) | Yd_cg (mm) | Z_cg (mm) | Front/Rear | Near/Far |
|-------|-----------|-----------|------------|-----------|------------|----------|
| Dry | 3,382 | 2,892 | 1,159 | 1,033 | 50.7/49.3% | 51.0/49.0% |
| Camera Ready | 4,582 | 3,518 | 1,151 | 1,159 | 37.4/62.6% | 51.3/48.7% |
| Materials Exhausted | 4,582 | 3,518 | 1,151 | 895 | 37.4/62.6% | 51.3/48.7% |

---

## 5. Weight Distribution Diagrams

### Sheet 1 — Component Weight Map

All dry components shown at actual footprint positions, color-coded by
category. The right end zone (IBC stack area) is the densest zone.

![TBS-001 — Weight Analysis: Component Weight Map](assets/weight-analysis-sheet1.png)

### Sheet 2 — Camera Ready Distribution

Weight distribution with full Blue IBCs (top tier) and flooded processing
tray. CG marker shows the loaded center of gravity at X=3,518, Yd=1,151.
Quadrant weights show the rear-heavy bias from the IBC stack.

![TBS-001 — Weight Analysis: Camera Ready](assets/weight-analysis-sheet2.png)

### Sheet 3 — Materials Exhausted Distribution

Water has migrated from top-tier Blue IBCs to bottom-tier Brown/Waste
IBCs. Total weight is unchanged (closed water system). The vertical
CG drops by 264mm (Z: 1,159 → 895 mm) as water moves to bottom tier.

![TBS-001 — Weight Analysis: Materials Exhausted](assets/weight-analysis-sheet3.png)

### Sheet 4 — Summary Comparison

Three-state side-by-side comparison with CG positions and summary table.
The dry state is nearly balanced; liquid states shift CG rearward by ~626mm.

![TBS-001 — Weight Analysis: Summary Comparison](assets/weight-analysis-sheet4.png)

---

## 6. Analysis and Findings

### 6.1 ISO Gross Weight Compliance

All three states are well within the ISO 24,000 kg maximum gross weight:

| State | Total (kg) | Margin (kg) | Utilization |
|-------|-----------|------------|-------------|
| Dry | 3,382 | 20,618 | 14.1% |
| Camera Ready | 4,582 | 19,418 | 19.1% |
| Materials Exhausted | 4,582 | 19,418 | 19.1% |

The container operates at less than 20% of its rated capacity in all states.
There is no structural concern from a gross weight perspective.

### 6.2 Left-Right Balance (Near/Far)

The near/far split is nearly balanced in all states (51/49%). This is by
design: equipment on the pinhole wall (near side) is lightweight (electrical
panel, batteries, pumps totaling ~73 kg), and the IBC stack is centered
across the container width. The film plane carriage contributes ~33 kg to
the far side but is offset by the tilt-swing board and cooler on the near
side.

### 6.3 Front-Rear Balance

The dry state is nearly balanced front/rear (50.7/49.3%), with CG at
X=2,892mm (just past the container midpoint of 2,947mm).

When liquids are added, the CG shifts rearward to X=3,518mm (626mm past
the dry CG). This creates a 37.4/62.6% front/rear split. The rear bias
is caused by 1,200 kg of water concentrated in the IBC stack zone
(X=4,674–5,893mm).

**Transport implication:** When loaded, the container's CG is at 59.7%
of the length from the cargo door end. For trailer placement, the container
should be positioned so the rear (sealed) end sits over or near the trailer
axle(s) to balance the load.

### 6.4 Vertical CG and Self-Stabilizing Design

The most significant finding is the **vertical CG migration** between states:

- **Camera Ready:** Z_cg = 1,159 mm (1,200 kg of water in top-tier IBCs)
- **Materials Exhausted:** Z_cg = 895 mm (1,200 kg of water in bottom-tier IBCs)
- **ΔZ = −264 mm** (CG drops 264mm during a session)

This is an inherent self-stabilizing feature of the 2×2 IBC stack design.
The water system is closed — 1,200 kg of water is loaded into the Blue IBCs
and redistributed during processing. No water is added or lost; it simply
migrates from top-tier Blue IBCs through the processing tray into bottom-tier
Brown/Waste IBCs. Total mass remains constant at 4,582 kg throughout a
session, but the vertical redistribution of 1,200 kg from top tier to
bottom tier drops the center of gravity by 264mm, improving stability.

### 6.5 Walkway Weight Sensitivity

The walkway system contributes 327 kg (9.7% of dry weight), making it the
second-largest structural subsystem after the hinged panel. The weight is
dominated by the grating at 44 kg/m² (McNICHOLS catalog value). If lighter
aluminum grating were used (~20 kg/m²), the walkway weight would drop to
approximately 175 kg, saving ~152 kg. However, galvanized steel grating is
specified for durability and chemical resistance in the wet processing
environment.

---

## 7. References

1. ISO 668:2020 — Series 1 freight containers: Classification, dimensions and ratings
2. Hapag-Lloyd Container Specification — 20ft Standard Dry Container
3. McNICHOLS — Press-Locked Steel Bar Grating, 25mm depth, weight tables
4. Schutz Ecobulk MX 600L — IBC tote specifications
5. [Water System Report](water-system-report.md) — Processing tray weight (§4), IBC layout (§5)
6. [Light Trap Selection](light-trap-selection.md) — Panel + drum weight (§7)
