# Electrical / Power System — Focused 3D Model — Design

**Goal:** Build the missing subsystem SketchUp model, **`electrical`**, showing the TBS-001
power system in 3D — solar generation → storage → distribution → loads — with the main
enclosure opened to show its internals, and every circuit routed to its load.

**Architecture:** A new generator `src/models/generate_electrical_model.py` that
`import generate_sketchup_model as ov` and reuses its helpers, scene/camera/send scaffold,
and `tbs_constants`. It builds the electrical content at higher fidelity than the overview's
coarse `ov.electrical()` (which draws the EP as a solid box): a **ghosted enclosure shell +
distinct internals**, the (currently unmodeled) **solar array**, and **color-coded circuit
runs** to ghosted loads. Outputs `models/electrical.skp` + `src/models/electrical.rb`.

**Tech stack:** Python generator emitting Ruby for the SketchUp API, sent to the active
document via the existing `--send` MCP path (`src/models/sketchup_client.py`). Units: mm.

---

## Context

The project has focused 3D models for several subsystems (`overview`, `lighttrap`,
`ibc-stack`, `film-plane`, `walkway`, `spraybar`, `right-cantilever-study`) but **none for
the electrical/power system** — it exists only schematically inside `overview` (the
`electrical()` builder draws the EP + battery + external panel + E-stop + contactor + MC4
bulkheads, and `lighting_and_wiring()` draws the ceiling trunking + Circuit D/G fixtures).

Three things are **not** modeled anywhere today and are the new value of this model:
1. **The solar array** — 3×200 W panels + ground tilt frame + PV run (absent from `overview`).
2. **Enclosure internals** — MPPT, fuse block, busbars, main fuse, disconnect, contactor
   (the EP is a featureless box in `overview`).
3. **Routed circuit runs** — the 7 circuits A–G traced from the fuse block to each load.

The 2D electrical diagrams already cover the one-line schematic, so this model's job is the
**physical spatial layout and power flow**, not the schematic.

### Decisions captured during brainstorming
- **Detail level:** *Both, via scenes* — build detailed enclosure internals, and use scenes
  to toggle a clean system overview vs. a zoomed enclosure-internals view.
- **Solar array:** *Ground tilt frame beside the container* (3×200 W on a 30° frame), PV run
  into the external power panel, positioned clear of the pinhole sightline at X=2399.
- **Circuit runs:** *Full routing to ghosted loads* — all 7 circuits (A–G), color-coded,
  fuse block → ceiling trunking → each load (fans, pumps, cooler+inverter, LED + safelight,
  actuators), with loads shown as faint ghosts so runs terminate visibly.

---

## Approach

### How this is built (not a parallel fan-out)
A single SketchUp model is one tightly-coupled generator file — every part shares the
coordinate system, `tbs_constants`, and reused `ov` helpers, and it is built interactively
against the live SketchUp app (`--send` clears and rebuilds the active document). It does
**not** decompose into independent worktree PRs; there is no CI/PR workflow in this repo
(commit to a branch, deploy via `publish.sh`). Executed as **one coherent build in one
session**.

### Reused from `generate_sketchup_model.py` (as `ov`)
- Helpers: `ruby_box`, `ruby_cylinder`, `ruby_pipe_run`, `component`, `mm`, color constants
  (`C_STEEL`, `C_ALUM`, `C_TRUNK`, `C_EVAP`, the circuit/material palette).
- The `generate_ruby()` Ruby template (tags + scenes + one shared iso camera + idempotent
  rebuild + stale-tag pruning) — copied from `generate_ibc_model.py` and adapted.
- Geometry references for parts kept identical to the overview (battery box from `BA_*`,
  external panel from `PWR_PANEL_*`, inverter from `INVERTER_*`, E-stop/contactor sizing).

### New builders in `generate_electrical_model.py`
- `context()` — full-length ghost container (floor, ceiling, two side walls, pinhole wall)
  at low alpha, plus **faint ghost loads** at their real positions (Fan A `FAN_A_*`, Fan B
  `FAN_B_*`, equipment panel/pumps `EQPANEL_*`, cooler+inverter `EVAP_*`/`INVERTER_*`, LED
  panels + safelight strips) — these are the circuit-run endpoints.
- `solar_array()` — 3×200 W panels (≈1480×680×35 mm each) on a 30° ground tilt frame
  (angle-iron legs + rails), ground-placed (`Z=0`) on the pinhole-wall exterior side
  (`Yd<0`), offset in X clear of the pinhole at X=2399; + a PV cable run (`ruby_pipe_run`)
  from the array up to the external power panel's MC4 bulkheads.
- `power_core()` — a **ghosted IP65 enclosure shell** (low alpha) on the pinhole wall around
  the EP volume, containing distinct internals mounted on a back-plate: **MPPT controller,
  Blue Sea fuse block, + and − busbars, MRBF main fuse, main disconnect switch, battery
  contactor**. Each a named part so the "Power Core" scene reads as "what's inside the box".
- `battery()` — 100 Ah pack (`BA_*`) + ghosted 2nd pack (plug-in expansion).
- `external_panel()` — flush face plate (`PWR_PANEL_*`) + MC4 PV bulkheads, NEMA 5-15R shore
  inlet, **GFCI cooler outlet** (Circuit E, replacing the old DC Deutsch), and the exterior
  E-stop on its yellow collar.
- `inverter()` — the Circuit-E 12→120 V inverter box (`INVERTER_*`), wall-mounted below the EP.
- `circuit_runs()` — the 40×25 ceiling cable-trunking spine + 7 **color-coded** circuit
  conductors (`ruby_pipe_run`, thin) from the fuse block out to each ghost load. One color
  per circuit (A exhaust fan, B intake fan, C pumps, D safelight, E cooler/inverter,
  F actuators, G white LED).

### Tags
`Context`, `Solar Array`, `Power Core`, `Battery`, `External Panel`, `Inverter`,
`Circuit Runs`, `Labels`.

### Scenes (shared iso camera; per-scene camera where a zoom is noted)
| Scene | Shows | Camera |
|-------|-------|--------|
| `Combined` | the whole system | shared extents |
| `Power Core` | enclosure internals + battery | zoomed on the EP volume |
| `Distribution` | fuse block + the 7 circuit runs to loads | shared extents |
| `External Panel` | exterior face + PV/shore/cooler connectors + E-stop | zoomed on the panel |
| `Labeled` | all components + the Labels tag | shared extents |

(Project rule: every `.skp` gets a `Labeled` scene. The Labels tag is hidden in the others.)

### In-model labels (Labels tag, project-standard leader callouts)
Anchored point/instance callouts fanned clear of each other, e.g.: `SOLAR ARRAY 3×200W`,
`MPPT 100/50`, `FUSE BLOCK (Cct A–G)`, `MAIN DISCONNECT + MRBF FUSE`, `BATTERY CONTACTOR`,
`BATTERY 1×100Ah (+ghost 2nd)`, `CCT-E INVERTER 12→120V`, `EXTERNAL PANEL / GFCI + MC4 + E-STOP`,
and one per circuit color in the Distribution scene.

---

## New constants (added to `tbs_constants.py`)

Grouped and commented; exact values finalized during implementation, but the design fixes
these as the additions (everything else reuses existing `EP_*`, `BA_*`, `PWR_PANEL_*`,
`INVERTER_*`, `FAN_*`, `EQPANEL_*`, `EVAP_*`):

**Solar array** — `SOLAR_PANEL_L` (~1480), `SOLAR_PANEL_W` (~680), `SOLAR_PANEL_T` (~35),
`SOLAR_N` (3), `SOLAR_TILT_DEG` (30), `SOLAR_ARRAY_X` / `SOLAR_ARRAY_YD` (negative, exterior)
/ `SOLAR_ARRAY_Z` (0, ground) — array origin clear of the pinhole sightline.

**Enclosure internals** — `ENCL_*` shell dims/origin (the IP65 box around the EP volume), and
size constants for the internal parts: `MPPT_W/D/H`, `FUSEBLK_W/D/H`, `BUSBAR_L/W`,
`DISCONNECT_D` (knob), `CONTACTOR_W/D/H`, plus their mount offsets on the back-plate. Placed
within the existing `EP_X`/`EP_W`/`EP_H_LO`/`EP_H_HI` envelope.

These are model-display constants (like `EVAP_*`/`INVERTER_*`), consumed by the new model
(and available to the overview later if its `electrical()` is ever upgraded).

---

## Files

- **Create:** `src/models/generate_electrical_model.py`
- **Create (outputs):** `models/electrical.skp`, `src/models/electrical.rb`
- **Modify:** `src/generators/tbs_constants.py` — add the solar + enclosure-internals
  constants (grouped near the existing `INVERTER_*` / `EP_*` block).
- **Modify:** `component-dependency-map.md` — add the `electrical` row to the §3.1 model list
  (reuses `ov` helpers + electrical/inverter/panel geometry; rebuild when `tbs_constants`
  electrical/solar values or `ov` change) and note the new constants in §4.

---

## Verification (e2e — same pattern as every TBS 3D model; no automated test)

1. **Build-check (non-interactive):** `python3 src/models/generate_electrical_model.py --save`,
   then import the module + call `generate_ruby()` and grep the Ruby for every expected
   part — `Solar Panel` (×3), `Tilt Frame`, `MPPT`, `Fuse Block`, `Busbar`, `MRBF Fuse`,
   `Main Disconnect`, `Battery Contactor`, `Battery`, `Cct E Inverter`, `External Panel`,
   `GFCI`, `Circuit A`…`Circuit G`, and the `(ghost)` container — with no exception.
2. **Interactive (in SketchUp):** open a **blank** document (so `overview.skp` isn't
   clobbered), `--save --send`, then visually confirm: solar array beside the container with
   PV run to the panel; the enclosure reads as opened with MPPT/fuse/busbar/disconnect/
   contactor inside; the battery + ghost 2nd; the inverter; the 7 color-coded circuits
   reaching their ghost loads; and the 5 scenes (esp. `Power Core` zoom + `Labeled`) frame
   correctly. Save as `models/electrical.skp`.
3. Commit the generator + `.rb` + `.skp` + the `tbs_constants.py` and dependency-map edits.
   (Sketchfab upload of the new model is the user's manual step.)

---

## Out of scope (YAGNI)
- No change to `overview`'s `electrical()` (no refactor to share builders — this model owns
  its higher-fidelity electrical geometry; revisit only if drift becomes a problem).
- No new 2D diagrams (the electrical one-line + power-panel sheets already exist).
- No wiring-gauge/fuse-rating accuracy beyond visual representation (the reports are
  authoritative for those).
