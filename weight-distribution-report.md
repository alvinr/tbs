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
| Container shell (excl. doors) | 1,920 | Full footprint | Hapag-Lloyd 20ft ISO tare (2,200 kg) minus doors (280 kg) |
| Cargo door — near leaf | 140 | Closed: X=−100 to −40 / Open: along near wall | ISO door leaf, ~140 kg each |
| Cargo door — far leaf | 140 | Closed: X=−100 to −40 / Open: along far wall | ISO door leaf, ~140 kg each |

### 3.2 Structural Components

| Component | Weight (kg) | X Range (mm) | Yd Range (mm) | Calculation Basis |
|-----------|------------|-------------|---------------|-------------------|
| Hinged panel | 203 | 0–80 (deployed) / 300–380 (transport) | 0–2,362 | Stepped sandwich: ply+steel corners, RHS center frame. Scaled to 240 kg combined with drum per [Light Trap Selection](light-trap-selection.md) §7 |
| Light trap drum | 37 | 0–40 (deployed) / 300–340 (transport) | 756–1,606 | 1.5mm Al shell Ø750×2,200mm + 3 baffles + bearings |
| Processing tray | 116 | 170–4,629 | 80–2,280 | 304 SS 1.5mm, 2 panels × 58 kg ([Water System Report](water-system-report.md) §4) |
| Near walkway | 78 | 470–4,629 | 0–300 | 10 brackets @ ~2.7 kg + 44 kg/m² grating |
| Far walkway | 78 | 470–4,629 | 2,062–2,362 | Same as near walkway |
| Right walkway | 59 | 4,329–4,629 | 0–2,362 | Ceiling-hung: 2× 25×25×5 bearers + M10 hangers + grating |
| Left walkway | 35 | 170–470 | 0–2,362 | Removable lift-out: grating + 50×50×3 Al bearer beam + 3 legs |
| Ceiling rails | 48 | 0–5,893 | 30–2,332 | 2× HGR20 @ 3.7 kg/m + 8 carriage blocks |
| Container mods | 65 | Distributed | Distributed | Light seal foam + reinforcement plates (estimate) |
| **Structure subtotal** | **719** | | | |

### 3.3 Equipment

| Component | Weight (kg) | X Range (mm) | Yd Range (mm) | Calculation Basis |
|-----------|------------|-------------|---------------|-------------------|
| Electrical panel | 15 | 1,600–1,900 | 0–150 | Wall-mount distribution panel |
| Battery bank | 26 | 1,810–2,310 | 0–150 | 2× 100Ah LiFePO4 @ 13 kg each |
| Solar controller | 2 | 1,700–1,800 | 0–100 | MPPT charge controller |
| Pump manifold | 5 | 2,500–2,800 | 0–150 | 3× 12V diaphragm pumps + manifold |
| Evaporative cooler | 15 | 930–1,530 | 0–350 | Portable evap cooler unit |
| Film plane carriage | 33 | 150–4,649 | 2,212–2,312 | Al angle frame (50.8×50.8×4.8mm) + 92 cam-lever clamps + 4 HGH20CA carriages |
| Tilt-swing board | 30 | 2,089–2,709 | 0–100 | 620×620×45mm Al plate + spherical pivot + screws |
| Fans (A+B) | 4 | End walls | Near corners | 2× 150mm axial panel fans |
| Baffle ducts | 6 | Distributed | Distributed | 2× galvanized steel baffle ducts |
| Blue IBC-1 (tote) | 55 | 4,674–5,893 | 30–1,046 | 600L steel-cage IBC tare (top tier, near) |
| Blue IBC-2 (tote) | 55 | 4,674–5,893 | 1,316–2,332 | 600L steel-cage IBC tare (top tier, far) |
| Brown IBC-3 (tote) | 55 | 4,674–5,893 | 30–1,046 | 600L steel-cage IBC tare (bottom tier, near) |
| Waste IBC-4 (tote) | 55 | 4,674–5,893 | 1,316–2,332 | 600L steel-cage IBC tare (bottom tier, far) |
| IBC stacking frame | 90 | 4,674–5,893 | 0–2,362 | 50×50×3mm RHS mild steel portal frame, wall-to-wall with open plumbing corridor ([Equipment Layout](equipment-layout-report.md) §5) |
| **Equipment subtotal** | **446** | | | |

### 3.4 Dry Weight Summary

| Category | Weight (kg) | % of Dry Total |
|----------|------------|---------------|
| Container (shell + doors) | 2,200 | 65.4% |
| Structure | 719 | 21.4% |
| Equipment | 446 | 13.3% |
| **Total dry** | **3,365** | **100%** |

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
| Blue IBC-1 water | 600 | 600 | X=4,674–5,893, Yd=30–1,046 | Top (Z=1,010–2,020) |
| Blue IBC-2 water | 600 | 600 | X=4,674–5,893, Yd=1,316–2,332 | Top (Z=1,010–2,020) |
| **Total liquid** | **1,200** | **1,200** | | |

**Total loaded weight: 4,565 kg** (3,365 dry + 1,200 liquid)

### 4.2 Materials Exhausted (Ready for Resupply)

After a full session, wash water has been consumed and redistributed.
Blue IBCs are empty; Brown (recycled) and Waste IBCs are full. The
processing tray has been drained — all processed water is in the
Brown/Waste IBCs.

| Liquid | Volume (L) | Weight (kg) | Position | Tier |
|--------|-----------|------------|----------|------|
| Brown IBC-3 water | 600 | 600 | X=4,674–5,893, Yd=30–1,046 | Bottom (Z=0–1,010) |
| Waste IBC-4 water | 600 | 600 | X=4,674–5,893, Yd=1,316–2,332 | Bottom (Z=0–1,010) |
| Processing tray | — | 0 | Drained | — |
| **Total liquid** | **1,200** | **1,200** | | |

**Total loaded weight: 4,565 kg** (3,365 dry + 1,200 liquid)

### 4.3 State Comparison

| State | Total (kg) | X_cg (mm) | Yd_cg (mm) | Z_cg (mm) | Front/Rear | Near/Far |
|-------|-----------|-----------|------------|-----------|------------|----------|
| Dry (Transport) | 3,365 | 2,656 | 1,161 | 1,054 | 55.1/44.9% | 50.9/49.1% |
| Camera Ready (Deployed) | 4,565 | 3,372 | 1,167 | 1,176 | 40.6/59.4% | 50.7/49.3% |
| Materials Exhausted (Transport) | 4,565 | 3,346 | 1,167 | 910 | 40.6/59.4% | 50.7/49.3% |

---

## 5. Weight Distribution Diagrams

### 1 — Summary Comparison

Three-state side-by-side comparison with CG positions and summary table.
The dry state is nearly balanced; liquid states shift CG rearward by ~736mm.

![TBS-001 — Weight Analysis: Summary Comparison](assets/weight-analysis-sheet1.png)

### 2 — Dry Weight (Configured for Transport)

All dry components shown at actual footprint positions, color-coded by
category. The hinged panel is retracted 300mm inward on its ceiling rails
(transport position). The right end zone (IBC stack area) is the densest zone.

![TBS-001 — Weight Analysis: Dry — Transport](assets/weight-analysis-sheet2.png)

### 3 — Camera Ready (Panel Deployed)

Weight distribution with full Blue IBCs (top tier) and hinged panel
deployed to its operational position at the cargo door end (X=0–80).
CG marker shows the loaded center of gravity at X=3,350, Yd=1,150.
Quadrant weights show the rear-heavy bias from the IBC stack.

![TBS-001 — Weight Analysis: Camera Ready](assets/weight-analysis-sheet3.png)

### 4 — Materials Exhausted (Configured for Transport)

Water has migrated from top-tier Blue IBCs to bottom-tier Brown/Waste
IBCs. The hinged panel is retracted to transport position (X=300–380).
Total weight is unchanged (closed water system). The vertical
CG drops by 269mm (Z: 1,176 → 907 mm) as water moves to bottom tier.

![TBS-001 — Weight Analysis: Materials Exhausted](assets/weight-analysis-sheet4.png)

---

## 6. Analysis and Findings

### 6.1 ISO Gross Weight Compliance

All three states are well within the ISO 24,000 kg maximum gross weight:

| State | Total (kg) | Margin (kg) | Utilization |
|-------|-----------|------------|-------------|
| Dry | 3,365 | 20,635 | 14.0% |
| Camera Ready | 4,565 | 19,435 | 19.0% |
| Materials Exhausted | 4,565 | 19,435 | 19.0% |

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

The dry/transport state has a front-biased split (55.1/44.9%), with CG at
X=2,656mm. This front bias comes from the cargo doors (280 kg total) being
in their closed position at X≈−70mm, pulling the CG toward the cargo door
end. The hinged panel is also retracted 300mm inward on its ceiling rails.

When liquids are added and the panel and doors are deployed (camera ready),
the CG shifts rearward to X=3,372mm (716mm past the dry CG). The doors
swing open flat against the side walls (X=0–1,221mm), redistributing
280 kg from X≈−70 to X≈610, while 1,200 kg of water loads in the IBC stack
zone (X=4,674–5,893mm). This creates a 40.6/59.4% front/rear split.

**Transport implication:** When loaded for transport (materials exhausted,
doors closed), the container's CG is at 56.7% of the length from the cargo
door end. For trailer placement, the container
should be positioned so the rear (sealed) end sits over or near the trailer
axle(s) to balance the load.

### 6.4 Vertical CG and Self-Stabilizing Design

The most significant finding is the **vertical CG migration** between states:

- **Camera Ready:** Z_cg = 1,176 mm (1,200 kg of water in top-tier IBCs)
- **Materials Exhausted:** Z_cg = 910 mm (1,200 kg of water in bottom-tier IBCs)
- **ΔZ = −266 mm** (CG drops 266mm during a session)

This is an inherent self-stabilizing feature of the 2×2 IBC stack design.
The water system is closed — 1,200 kg of water is loaded into the Blue IBCs
and redistributed during processing. No water is added or lost; it simply
migrates from top-tier Blue IBCs through the processing tray into bottom-tier
Brown/Waste IBCs. Total mass remains constant at 4,565 kg throughout a
session, but the vertical redistribution of 1,200 kg from top tier to
bottom tier drops the center of gravity by 266mm, improving stability.

### 6.5 Walkway Weight Sensitivity

The walkway system contributes 250 kg (7.4% of dry weight), making it the
second-largest structural subsystem after the hinged panel. The weight is
dominated by the grating at 44 kg/m² (McNICHOLS catalog value). If lighter
aluminum grating were used (~20 kg/m²), the walkway weight would drop to
approximately 170 kg, saving ~89 kg. However, galvanized steel grating is
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
