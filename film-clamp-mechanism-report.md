<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Muslin Clamp System — Mechanism Design

## 1. Purpose

The photosensitive muslin must be held taut against the [film plane frame](film-plane-mechanism-report.md) throughout exposures lasting 30–45 minutes, at any tilt angle up to ±<!-- BEGIN fact:film_plane_max_tilt -->40<!-- END fact:film_plane_max_tilt -->° and any swing angle up to ±<!-- BEGIN fact:film_plane_max_swing -->28<!-- END fact:film_plane_max_swing -->°. Loading and unloading happens under mixed safelight conditions, so the clamp mechanism must provide clear tactile feedback without visual confirmation.

This report describes the **muslin clamp system** that secures the muslin to the **2"×2"×1/8" aluminum L-angle** perimeter frame (the film-plane frame — [Film Plane Mechanism §4](film-plane-mechanism-report.md)). Rather than a custom mechanism, it uses **off-the-shelf inert nylon spring clamps** clipped over the frame edge, with an **inert HDPE filler strip** packing the open L channel so each clamp bites a solid full-depth edge. The angle's two 2-inch (≈51mm) legs are the *flat leg* (bonded behind the ACM backing board) and the *upstand* (standing proud toward the pinhole).

---

## 2. Clamp Layout

**58 nylon spring clamps** at 150mm centers grip the muslin on **three edges** of the <!-- BEGIN fact:film_plane_width_mm -->4,499<!-- END fact:film_plane_width_mm -->mm × <!-- BEGIN fact:film_plane_height_mm -->2,094<!-- END fact:film_plane_height_mm -->mm film-plane frame — the top and the two sides. The **bottom edge is left unclamped**: there is no clearance between the raised walkway deck and the board's bottom edge for a clamp body, and leaving it open keeps the swing/tilt envelope clear. The muslin is held taut by the three clamped edges.

| Edge | Length | Clamp Count |
|------|--------|-------------|
| Top horizontal | <!-- BEGIN fact:film_plane_width_mm -->4,499<!-- END fact:film_plane_width_mm -->mm | 30 |
| Left vertical | <!-- BEGIN fact:film_plane_height_mm -->2,094<!-- END fact:film_plane_height_mm -->mm | 14 |
| Right vertical | <!-- BEGIN fact:film_plane_height_mm -->2,094<!-- END fact:film_plane_height_mm -->mm | 14 |
| Bottom horizontal | — | 0 (walkway clearance) |
| **Total** | | **58** |

---

## 3. Clamp Mechanism

Each clamp is an **off-the-shelf inert nylon spring clamp** (Pittsburgh 69289 — a fiberglass body with swivel pads) clipped over the frame edge. Because the clamp must open around the full 2″ angle leg to reach the muslin on the board (leg + ACM + muslin ≈ 55mm), a **≥3″ clamp** is used — a 2″ clamp is too tight. An inert **HDPE filler strip** packs the open L channel so the clamp closes on a solid full-depth sandwich (ALU upstand + HDPE + ACM + muslin) instead of collapsing into the void.

The clamp is **fiberglass/nylon, not steel** — deliberately, for the cyanotype/ferricyanide splash zone where a steel spring would rust. It clips on and off by hand (squeeze the handle), giving clear tactile feedback for loading/unloading muslin under safelight, and its spring holds it closed at any tilt or swing angle. This replaces the earlier custom through-bolted bracket + torsion-spring + neoprene-jaw clip — no fabrication, and chemistry-safe.

![Muslin clamp detail — Sheet 6](assets/film-plane-sheet6.png)

### 3.1 Muslin Path

The muslin lies over the ACM backing board (the pinhole face) and its edge wraps the frame lip. Each clamp grips the whole frame edge as one sandwich — the muslin, the ACM, the HDPE filler, and the ALU upstand — pinning the muslin directly against the rigid ACM/filler stack. The ACM is the anvil; no separate hem wrap is needed.

### 3.2 HDPE Filler Strip

An inert **HDPE strip, 44.1mm deep** (= frame leg 50.8 − ACM 3 − muslin 0.5 − angle 3.2), runs continuously in the L channel along the three clamped edges (~8.7 m). It brings the open channel up to a solid full-depth edge so the clamp's swivel pads bear on solid material rather than air. HDPE is inert (chemistry-safe, the same family as the tray liner), rigid enough to back the clamp, and cut to suit — firm at fabrication.

---

## 4. Parts List

All items ship within the United States. Local Southern California pickup noted where available.

<!-- BEGIN parts:clamp -->
| Item | Spec | Qty | Supplier | Est. cost |
|------|------|-----|----------|-----------|
| [Nylon spring clamp, 3½″ (Pittsburgh 69289)](https://www.harborfreight.com/3-12-in-nylon-spring-clamp-69289.html) (69289) | Inert fiberglass/nylon spring clamp with swivel pads — no corrosion in the cyanotype splash zone (replaces the custom steel-bracket clip). Clips over the filler-filled L-frame edge to grip the muslin; the jaw must clear ~55mm (2" leg + ACM + muslin), so a ≥3" clamp. Top + 2 side edges only (bottom = walkway/swing clearance). Confirm the open-jaw ≥2" at purchase; 2½" 69290 is the smaller-body fallback. | 58 ea | Harbor Freight / Amazon | $115–$173 |
| HDPE filler strip (L-channel packer) | Inert HDPE strip, 44.125mm deep (= frame leg − ACM − muslin − angle), filling the aluminum-angle L channel along the 3 clamped edges (~8.7 m) so the nylon clamp bites a solid full-depth sandwich. Cut to suit; chemistry-safe (same family as the tray liner). Firm at fab. | 1 lot | TAP Plastics / McMaster-Carr | $30–$70 |
| **Clamp total** | | | | **$145–$243** |
<!-- END parts:clamp -->

**Clamp system estimated cost:** <!-- BEGIN costing:clamp-system-low -->$165<!-- END costing:clamp-system-low --> to <!-- BEGIN costing:clamp-system-high -->$223<!-- END costing:clamp-system-high --> (58 nylon clamps + HDPE filler strip).

---

## 5. Maintenance

| Interval | Task |
|----------|------|
| Before each session | Inspect muslin clamp engagement — all 58 clamps clipped on the three edges |
| Monthly | Check each nylon clamp still springs firmly closed; swap out any weak or cracked clamp (inexpensive, off-the-shelf) |
| Every 6 months | Verify the clamps hold the muslin taut under gravity at <!-- BEGIN fact:film_plane_max_tilt -->40<!-- END fact:film_plane_max_tilt -->° tilt; re-seat any that have crept |
| Annually | Inspect the HDPE filler strip for damage; wipe the clamps + filler clean of chemistry residue |

---

## 6. Source References

1. [Film Plane Mechanism Report](film-plane-mechanism-report.md) — Parent report: four-corner independent actuation mechanism that the clamp system attaches to.
2. [Harbor Freight 69289 — 3½″ nylon spring clamp](https://www.harborfreight.com/3-12-in-nylon-spring-clamp-69289.html) — inert fiberglass spring clamp with swivel pads (the muslin clamp).
3. [HDPE sheet — TAP Plastics](https://www.tapplastics.com/product/plastics/cut_to_size_plastic/hdpe_sheet/155) — inert, chemistry-safe L-channel filler material.
