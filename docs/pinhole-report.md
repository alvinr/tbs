<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Pinhole Wall & Front-Board Mount

## 1. Purpose

The pinhole wall is the far (scene-facing) end wall of the container — the plane that carries the camera's aperture. This report covers the **wall interface**: the aperture cut through the container wall and the flat **wall-frame adapter** that the front board bolts to. The front board itself — the interchangeable pinhole/lens mount — is the [Pinhole Disc Holder](pinhole-disc-holder-report.md); the pinhole optics are in the [Pinhole Optics Report](pinhole-optics-report.md).

> The former standard **Ø600 interchangeable pinhole/lens plate** (8× M12 on a Ø540 wall frame, with separate pinhole and lens plates) was **retired**. The compact Ø80-carrier disc holder now does both jobs — a pinhole board or a large-format lens board (Copal/Compur 0/1/3) — from one small mount, and focus for a lens is set at the **film plane** (the rear standard's depth rail), so no lens-plate focus tube is needed.

---

## 2. Wall Aperture

The far end wall is corrugated ISO container steel. A circular aperture is cut through the corrugation on the optical axis (pinhole center: X = <!-- BEGIN fact:pinhole_x_mm -->2,454<!-- END fact:pinhole_x_mm -->mm on the long axis). The cut clears the front board's Ø110 scene-side taper bore with margin; it is not a precision feature — the flat adapter over it provides all the alignment datum.

---

## 3. Wall-Frame Adapter

Because corrugated steel cannot seat a machined plate, a flat steel **adapter plate** is welded (or bolted) over the corrugation to present a flat, machined datum face concentric with the aperture. It carries:

- the **4× M6 tapped holes on a Ø150 circle** that the Ø180 front plate bolts to (matching the disc holder — see its report),
- a flat sealing face for the front-board gasket / O-ring, and
- an opening larger than the Ø110 taper bore.

The adapter is the only component welded to the container; every optical-alignment reference originates from its machined face. Its bolt pattern and aperture are single-sourced from the [Pinhole Disc Holder](pinhole-disc-holder-report.md) (§2/§6).

---

## 4. Front Board (the mount)

The interchangeable pinhole/lens mount is the **[Pinhole Disc Holder](pinhole-disc-holder-report.md)** — a compact Ø180 front plate that bolts to the adapter and clamps an interchangeable **Ø80 carrier** (a pinhole board, or a Copal/Compur lens board) with a retaining ring and four thumb screws. Changeover between pinhole and lens is a seconds-long carrier swap; see that report for the mechanism, drawings, tolerances and BOM.

---

## 5. Sealing & Light Integrity

Two joints seal the wall:

- **Adapter → container wall:** continuous weld (or a bead of sealant under a bolted adapter) around the aperture — no light path around the adapter.
- **Front board → adapter:** a thin gasket (or an O-ring in the adapter face) compressed by the 4× M6 mount bolts, backed by a perimeter light-trap step, so any light passing the gasket must navigate a labyrinth before reaching the interior.

The carrier itself (pinhole or lens) is the only intended opening; its seal against the front plate is covered in the disc-holder report §5.

---

## 6. See Also

- [Pinhole Disc Holder (Front Board)](pinhole-disc-holder-report.md) — the interchangeable pinhole/lens mount (Ø80 carrier, retaining ring, thumb screws) that bolts to the adapter.
- [Pinhole Optics Report](pinhole-optics-report.md) — pinhole diameter, f-number, exposure.
- [Lens Options](lens-options.md) — large-format lens choices and coverage.
- [Film Plane Mechanism](film-plane-mechanism-report.md) — the rear standard, where focus (for a lens) and all perspective movements live.

---

## 7. Source References

1. [Rayleigh Criterion for Pinhole Cameras](https://en.wikipedia.org/wiki/Pinhole_camera#Selection_of_pinhole_size) — optimal aperture formula d = 1.9√(fλ).
2. [Intrepid Camera — Large-Format Lens Explorer](https://intrepidcamera.co.uk/blogs/guides/the-large-format-lens-explorer) — Copal/Compur lens-board hole diameters for the carrier.
3. [McMaster-Carr](https://www.mcmaster.com) — mount bolts, gasket / O-ring cord, weld consumables.
