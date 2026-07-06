#!/usr/bin/env python3
"""Generate the TBS-001 Electrical / Power System SketchUp model (logical model: electrical).

The missing subsystem model: solar generation -> storage -> distribution -> loads.
REUSES the helpers and conventions from the Overview generator
(generate_sketchup_model.py) — same component/tag/scene structure, shared iso camera,
material-sharing-by-color, and `tbs_constants`. Higher fidelity than the overview's
coarse `ov.electrical()`: a ghosted enclosure + distinct internals, the (otherwise
unmodeled) ground solar array, and color-coded circuit runs to ghosted loads.

Tags / scenes:
    Context        ghost container + faint ghost loads (fans, pumps, LED, safelight)
    Solar Array    3x 200W panels on a 30deg ground tilt frame + PV run
    Power Core     ghosted enclosure + MPPT / fuse block / busbars / disconnect
    Battery        100Ah pack (+ ghost 2nd) + contactor + MRBF main fuse
    External Panel flush face + MC4 / NEMA / GFCI cooler outlet + E-stop
    Inverter       Circuit-E 12->120V inverter
    Circuit Runs   ceiling trunking spine + 7 color-coded circuits A-G to the loads
  Scenes: Combined, Power Core, Distribution, External Panel, Labeled.

Usage:
    python3 src/models/generate_electrical_model.py --save        # write electrical.rb
    python3 src/models/generate_electrical_model.py --save --send # + send to ACTIVE doc

NOTE: --send builds into the ACTIVE SketchUp document (it clears it first). Open a
NEW blank document before sending so the Overview model isn't overwritten, then save
the result as models/electrical.skp.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import generate_sketchup_model as ov   # helpers + conventions (Overview)
from tbs_constants import EP_X, EP_W, EP_H_LO, EP_H_HI, BA_X, BA_W, BA_H_LO, BA_H_HI, BA_D, PWR_PANEL_X, PWR_PANEL_W, PWR_PANEL_H, PWR_PANEL_Z, INVERTER_X, INVERTER_Z, INVERTER_W, INVERTER_H, INVERTER_D, SOLAR_ARRAY_X, SOLAR_ARRAY_YD, ENCL_SHELL_D, MPPT_W, MPPT_D, MPPT_H, FUSEBLK_W, FUSEBLK_D, BUSBAR_L, BUSBAR_W, BUSBAR_H, DISCONNECT_D, DISCONNECT_H, CONTACTOR_W, CONTACTOR_D, CONTACTOR_H, MRBF_D, MRBF_H, EQPANEL_X, EQPANEL_YD, EQPANEL_YD_SPAN, PUMP_H_HI, FAN_A_YD, FAN_A_H, FAN_B_YD, FAN_B_H, FAN_BODY_D, DUCT_DEPTH, DUCT_HEIGHT, EVAP_W, EVAP_D, EVAP_H, EVAP_DUCT_X, PWP_P02_X, PWP_P02_Z0, PWP_P02_H

TAGS = ["Context", "Solar Array", "Power Core", "Battery", "External Panel",
        "Inverter", "Circuit Runs", "Labels"]

WALL = ov.WALL_T

# ── Circuit colors (one per branch A–G) ──────────────────────────────────────
CCT = {
    "A": ("#C0392B", "exhaust fan"),
    "B": ("#E67E22", "intake fan"),
    "C": ("#2980B9", "water pumps"),
    "D": ("#8E44AD", "safelight"),
    "E": ("#16A085", "cooler / inverter"),
    "F": ("#7F8C8D", "actuators (spare)"),
    "G": ("#F1C40F", "white LED"),
}

# ── Load fixtures — geometry MATCHES the overview's lighting_wiring() (the plan) ──
_LED_W, _LED_D = 600, 300
_LED_YD = ov.C_WID / 2 - _LED_D / 2
_RLED_X0 = EQPANEL_X - 150 - _LED_D            # IBC-end LED panel — ROTATED 90°
_RLED_Y0 = ov.C_WID / 2 - _LED_W / 2
# LED panel footprints (x0, y0, w_x, w_yd): two flat + the rotated IBC-end one.
LED_PANELS = [(1000, _LED_YD, _LED_W, _LED_D),
              (2900, _LED_YD, _LED_W, _LED_D),
              (_RLED_X0, _RLED_Y0, _LED_D, _LED_W)]
SAFE_XS = [500, 2250, 4150]
# Circuit-drop endpoints (x, yd, z) — conduit lands per the overview (panel-centre X,
# near-Yd edge); the rotated panel keeps its own Yd so the drop lands on it.
LED_ENDS = [(1000 + _LED_W / 2, _LED_YD, ov.C_HGT - 40),
            (2900 + _LED_W / 2, _LED_YD, ov.C_HGT - 40),
            (_RLED_X0 + _LED_D / 2, _RLED_Y0, ov.C_HGT - 40)]
SAFE_ENDS = [(sx + 20, 100, ov.C_HGT - 25) for sx in SAFE_XS]

# Fan A on the sealed end wall; Fan B terminates at a fixed WALL BOX (the fan itself is
# on the swing panel, reached by a flex connector — not part of the rigid conduit).
_FAN_A_X = (ov.C_LEN - DUCT_DEPTH) + FAN_BODY_D / 2     # 5618
_FAN_A_TOP = FAN_A_H + DUCT_HEIGHT / 2                  # 2100
_FANB_BOX_X = 300

# Representative load endpoint for each single-load circuit (x, yd, z).
LOADS = {
    "A": (_FAN_A_X, FAN_A_YD, _FAN_A_TOP),                          # Fan A, end wall
    "B": (_FANB_BOX_X, 18, FAN_B_H + 45),                          # Fan B wall box
    "C": (EQPANEL_X, EQPANEL_YD + EQPANEL_YD_SPAN / 2, PUMP_H_HI),  # pump zone @ panel
    "E": (INVERTER_X + INVERTER_W / 2, INVERTER_D / 2, INVERTER_Z + INVERTER_H / 2),
    # Circuit F (film-plane actuators) is an OPTIONAL/future provision — "leave fused
    # spare", draws nothing in the manual standard build — so it has NO routed conduit.
}

# Fuse-block reference point (runs originate here) — front face of the block in the EP.
# ── Blade-fuse stack (Blue Sea 5026): a standing row of 7 ATO blade fuses on the block
# base, one per circuit A-G (left→right = the one-line schematic order), each coloured to
# its circuit and rated per the schematic. Every circuit cable leaves the TOP of its OWN
# blade, exits to the enclosure front, then rises — so each fuse→load run is traceable and
# the model conforms to the electrical schematic. ──────────────────────────────────────
FUSE_ORDER = ["A", "B", "C", "D", "E", "F", "G"]
CCT_FUSE = {"A": "5A", "B": "5A", "C": "15A", "D": "5A", "E": "40A", "F": "20A", "G": "10A"}
_FBLK_X0 = EP_X + 15                        # fuse-block left edge (X)
_FBLK_YD = 25                              # block front Yd inside the enclosure
_FBLK_Z0 = EP_H_LO + 270                   # block base bottom Z
_FBASE_H = 28                              # block base height (Z)
_FUSE_W, _FUSE_T, _FUSE_H = 13, 9, 42      # blade fuse: width(X), thickness(Yd), height(Z)
_FUSE_PITCH = FUSEBLK_W / len(FUSE_ORDER)  # blade pitch along the block width
_FUSE_YD = _FBLK_YD + (FUSEBLK_D - _FUSE_T) / 2


def _fuse_cx(i):
    return _FBLK_X0 + (i + 0.5) * _FUSE_PITCH


FUSE_TOP_Z = _FBLK_Z0 + _FBASE_H + _FUSE_H            # cable exits each blade's top terminal
ENCL_FRONT_YD = ENCL_SHELL_D + 10                    # risers run up the enclosure front (MPPT now sits forward of them, clear)
# per-circuit fuse terminal (cable origin) = top-centre of that circuit's blade
FUSE_POS = {c: (_fuse_cx(i), _FUSE_YD + _FUSE_T / 2, FUSE_TOP_Z)
            for i, c in enumerate(FUSE_ORDER)}
TRUNK_YD = 20                  # conductors hug the pinhole-wall ceiling line
TRUNK_Z = ov.C_HGT - 13


# ── Labels (project rule: every .skp gets a Labeled scene) ───────────────────
ELEC_POINT_LABELS = [
    (SOLAR_ARRAY_X + 700, SOLAR_ARRAY_YD - 600, 700,
     "SOLAR ARRAY\n3x 200W (30deg tilt)", -200, -700, 700),
    (EP_X + 90, 40, EP_H_HI - 60, "MPPT 100/50",                 -380, 700, 280),
    (EP_X + 90, 40, FUSE_TOP_Z, "FUSE STACK A-G\n5/5/15/5/40/20/10 A", 420, 700, 240),
    (EP_X + 90, 40, EP_H_LO + 210, "+/- BUSBARS",                 420, 640, -120),
    (EP_X + 240, ENCL_SHELL_D, EP_H_LO + 120, "MAIN DISCONNECT", 360, 760, -260),
    (BA_X + 80, 40, BA_H_HI + 50, "BATTERY CONTACTOR\n+ MRBF main fuse", -300, 760, 900),
    (BA_X + 120, 60, BA_H_LO + 100, "BATTERY 1x 100Ah\n(2nd pack ghosted)", -320, 640, 760),
    (INVERTER_X + INVERTER_W / 2, INVERTER_D / 2, INVERTER_Z + INVERTER_H,
     "CCT-E INVERTER\n12->120V AC (cooler)", -430, 820, 480),
    (PWR_PANEL_X + PWR_PANEL_W / 2, -WALL - 40, PWR_PANEL_Z + PWR_PANEL_H + 20,
     "EXTERNAL PANEL\nMC4 PV / shore / GFCI cooler / E-STOP", 220, -520, 380),
    (EVAP_DUCT_X, -WALL - EVAP_D / 2 - 120, EVAP_H,
     "EVAP COOLER\n(Hessaire MC18M, Cct E)", -260, -520, 520),
    (EQPANEL_X, EQPANEL_YD + EQPANEL_YD_SPAN / 2, PUMP_H_HI - 40,
     "CCT-C PUMP DISTRIBUTION\ndist block → pumps (master sw on EP)", -350, -700, 250),
    (EP_X - 265, 22, EP_H_LO + 385,
     "PV DISCONNECT\n(load-break, array->MPPT)", 300, 560, 320),
    (EP_X + 40, 95, EP_H_LO + 215, "60A CHARGE FUSE\n(MPPT -> battery)", 440, 680, 160),
    (EP_X + EP_W / 2, ENCL_SHELL_D + 38, EP_H_LO + 80,
     "INTERIOR E-STOP\n(EP face, parallel)", -340, 560, -160),
]


def elec_labels():
    rows = []
    for x, y, z, text, dx, dy, dz in ELEC_POINT_LABELS:
        rows.append(
            f'anc = Geom::Point3d.new({ov.mm(x)}, {ov.mm(y)}, {ov.mm(z)})\n'
            f'txt = entities.add_text("{text}", anc, '
            f'Geom::Vector3d.new({ov.mm(dx)}, {ov.mm(dy)}, {ov.mm(dz)}))\n'
            f'txt.layer = model.layers["Labels"] rescue nil')
    return '\n'.join(rows)


def _dedup(pts):
    return [p for i, p in enumerate(pts) if i == 0 or p != pts[i - 1]]


# ── Conductor run, ORTHOGONAL per skill_plumbing_drawing (matches the overview's
# lighting_wiring conduit style): rise out of the enclosure, pull to the pinhole-wall
# trunking line, run ALONG the ceiling, cross out to the load, drop perpendicular.
# Every segment changes exactly ONE axis — no diagonals.
def _run(cct, load):
    lx, lyd, lz = load
    fx, fy, fz = FUSE_POS[cct]
    pts = _dedup([
        (fx, fy, fz),               # this circuit's fuse top terminal (inside enclosure)
        (fx, ENCL_FRONT_YD, fz),    # out to the enclosure front face (Yd) — clears the MPPT
        (fx, ENCL_FRONT_YD, TRUNK_Z),  # rise up the enclosure front to the ceiling (Z)
        (fx, TRUNK_YD, TRUNK_Z),    # pull to the pinhole-wall trunking line (Yd)
        (lx, TRUNK_YD, TRUNK_Z),    # run ALONG the ceiling to the load's X (X)
        (lx, lyd, TRUNK_Z),         # cross out toward the load (Yd)
        (lx, lyd, lz),              # drop perpendicular to the load (Z)
    ])
    return ov.ruby_pipe_run(f"Circuit {cct} ({CCT[cct][1]})", pts, 6, color=CCT[cct][0])


def _multi_run(cct, ends):
    """Circuit feeding MULTIPLE ceiling fixtures (LED / safelight): a fuse-block feed
    onto the ceiling line, a ceiling spine spanning all fixture Xs, and a perpendicular
    cross+drop at EACH fixture (its own Yd) — all orthogonal, so every light connects."""
    col, fx, fy, fz = CCT[cct][0], *FUSE_POS[cct]
    xs = [e[0] for e in ends]
    p = [
        ov.ruby_pipe_run(f"Circuit {cct} feed ({CCT[cct][1]})",
                         _dedup([(fx, fy, fz), (fx, ENCL_FRONT_YD, fz),
                                 (fx, ENCL_FRONT_YD, TRUNK_Z), (fx, TRUNK_YD, TRUNK_Z)]),
                         6, color=col),
        ov.ruby_pipe_run(f"Circuit {cct} ceiling spine ({CCT[cct][1]})",
                         [(min(xs), TRUNK_YD, TRUNK_Z), (max(xs), TRUNK_YD, TRUNK_Z)],
                         6, color=col),
    ]
    for x, yd, z in ends:
        br = _dedup([(x, TRUNK_YD, TRUNK_Z), (x, yd, TRUNK_Z), (x, yd, z)])
        if len(br) > 1:
            p.append(ov.ruby_pipe_run(f"Circuit {cct} drop X{int(x)} ({CCT[cct][1]})",
                                      br, 6, color=col))
    return '\n'.join(p)


def context():
    """Full-length ghost container shell + faint ghost loads (the circuit endpoints
    that aren't modeled as their own components: fans, pump cluster, LED, safelight)."""
    t = WALL
    # Shell reduced to Floor + Ceiling + Pinhole Wall only — the Far (film-plane) wall and both end
    # walls (cargo-door + sealed) are dropped so the model orbits freely without those walls occluding
    # the electrical gear, which all lives on the pinhole wall.
    p = [
        ov.ruby_box("Floor (context)", 0, 0, -t, ov.C_LEN, ov.C_WID, t,
                    color=ov.C_SHELL, alpha=0.22),
        ov.ruby_box("Ceiling (context)", 0, 0, ov.C_HGT, ov.C_LEN, ov.C_WID, t,
                    color=ov.C_SHELL, alpha=0.08),
        ov.ruby_box("Pinhole Wall (context)", 0, -t, 0, ov.C_LEN, t, ov.C_HGT,
                    color=ov.C_SHELL, alpha=0.10),
    ]
    # Ghost loads (faint) — geometry identical to the overview's lighting_wiring().
    p.append(ov.ruby_box("Fan A ghost (exhaust)", _FAN_A_X - 60, FAN_A_YD - 75,
                         FAN_A_H - 75, 120, 150, 150, color=CCT["A"][0], alpha=0.18))
    p.append(ov.ruby_box("Fan B wall box ghost (Cct B)", _FANB_BOX_X - 40, 0,
                         FAN_B_H - 45, 80, 60, 90, color=CCT["B"][0], alpha=0.20))
    # Surround box spans the FULL pump stack — down to the lowest pumps (P-01/P-02,
    # body bottom Z1120) so the lowest outlet is enclosed like the upper ones.
    pz_bot = 1100
    p.append(ov.ruby_box("Pump zone ghost (Cct C)", EQPANEL_X - 140, EQPANEL_YD, pz_bot,
                         150, EQPANEL_YD_SPAN, PUMP_H_HI - pz_bot,
                         color=CCT["C"][0], alpha=0.14))
    for x0, y0, wx, wy in LED_PANELS:                   # white LED (rotated IBC-end)
        p.append(ov.ruby_box("White LED ghost (Cct G)", x0, y0, ov.C_HGT - 40,
                             wx, wy, 30, color=CCT["G"][0], alpha=0.16))
    for sx in SAFE_XS:                                  # safelight strips (Cct D)
        p.append(ov.ruby_box("Safelight ghost (Cct D)", sx, 100, ov.C_HGT - 25,
                             40, ov.C_WID - 200, 16, color=CCT["D"][0], alpha=0.16))
    return '\n'.join(p)


def power_core():
    """EP internals on a PLYWOOD BACKING PANEL, with the DC gear inside a ghosted IP65 enclosure
    (its back IS the plywood): MPPT, fuse block,
    +/- busbars, rotary main disconnect (knob on the face). All components surface-mount
    on the ply; the MPPT sits forward on its own sub-panel to clear the fuse-stack risers."""
    p = []
    ez = EP_H_LO
    eh = EP_H_HI - EP_H_LO
    # Plywood backing panel (18mm) — every EP component surface-mounts on it. STEPPED: full width low
    # down (backs the wide battery bank) but narrowed up top so it clears the back of the external
    # power panel that the full-width board was crossing into. The DC gear sits inside a ghosted IP65
    # enclosure (added below) whose back panel is this plywood.
    _ply_bot = BA_H_LO - 12
    _ply_x0 = BA_X - 12                             # full width low down (battery bank)
    _ply_x0_top = PWR_PANEL_X + PWR_PANEL_W + 10    # narrowed up top to clear the external panel (right edge)
    _ply_step_z = PWR_PANEL_Z - 20                  # step just below the external panel
    _ply_r = EP_X + EP_W + 12
    p.append(ov.ruby_box("EP plywood backing panel (lower, 18mm)", _ply_x0, -18, _ply_bot,
                         _ply_r - _ply_x0, 18, _ply_step_z - _ply_bot, color=ov.C_PLY))
    p.append(ov.ruby_box("EP plywood backing panel (upper, 18mm)", _ply_x0_top, -18, _ply_step_z,
                         _ply_r - _ply_x0_top, 18, (EP_H_HI + 12) - _ply_step_z, color=ov.C_PLY))
    # IP65 enclosure — ghosted weatherproof box over the fuse block + busbars + charge fuse (the DC
    # distribution terminals that need sealing), mounted ON the plywood (its back IS the plywood). The
    # MPPT, main disconnect, battery and inverter mount on the plywood outside it.
    p.append(ov.ruby_box("IP65 enclosure (ghosted, fuse block + busbars)", EP_X + 5, 12, EP_H_LO + 155,
                         185, 140, 210, color=ov.C_STEEL, alpha=0.12))
    p.append(ov.ruby_box("MPPT Controller (100/50)", EP_X + 15, 120,
                         EP_H_HI - MPPT_H - 30, MPPT_W, MPPT_D, MPPT_H, color="#3A5BA0"))
    # Plywood backing panel — extends the EP mounting board FORWARD to the relocated MPPT plane so the
    # MPPT flush-mounts on ply; tall enough to also back the PV-feed riser (Z~1884->1970) so the cable
    # sits flush on the panel. Front face at Yd120 (the MPPT's back).
    p.append(ov.ruby_box("MPPT backing panel (18mm ply)", EP_X + 8, 102,
                         EP_H_HI - MPPT_H - 132, MPPT_W + 20, 18, MPPT_H + 132, color=ov.C_PLY))
    # PV interior feed: external-panel MC4 bulkheads -> MPPT PV input (the conductor from
    # the interior side of the MC4 connectors; the exterior array->panel run is ov.solar_array()).
    # Crosses at the bottom MC4 height (Z≈1884, under the overview's upper transport-stay
    # anchor) and over the fuse block, then rises into the MPPT at Yd 85 (clear of the fuse
    # block at Yd 25-70). Duplicated in the overview's electrical() — keep in sync.
    mc4_x = PWR_PANEL_X + 0.23 * PWR_PANEL_W
    mc4_z = PWR_PANEL_Z + 0.225 * PWR_PANEL_H
    dsx = EP_X - 300              # PV array-disconnect X (on the plywood) — feed runs IN-LINE through it
    p.append(ov.ruby_pipe_run("PV feed (MC4 -> array disconnect -> MPPT)",
                              _dedup([(mc4_x, 22, mc4_z),
                                      (dsx, 22, mc4_z),            # in at the disconnect LINE terminal (array side)
                                      (dsx + 70, 22, mc4_z),       # out the LOAD terminal — in-line THROUGH the isolator
                                      (dsx + 70, 120, mc4_z),      # forward to the MPPT-panel plane
                                      (EP_X + 40, 120, mc4_z),     # across to under the MPPT
                                      (EP_X + 40, 120, EP_H_HI - MPPT_H - 32),   # rise FLUSH up the ply panel (Yd120)
                                      (EP_X + 40, 155, EP_H_HI - MPPT_H - 22)]),  # elbow forward into the MPPT PV input
                              9, color="#2D7A2D"))
    # Blue Sea 5026: the block base + a standing row of 7 blade fuses (one per circuit A-G,
    # coloured to its circuit). Each blade's top is the cable origin for that circuit.
    p.append(ov.ruby_box("Fuse Block base (Blue Sea 5026)", _FBLK_X0, _FBLK_YD, _FBLK_Z0,
                         FUSEBLK_W, FUSEBLK_D, _FBASE_H, color="#2B2B30"))
    for i, c in enumerate(FUSE_ORDER):
        p.append(ov.ruby_box(f"Fuse {c} ({CCT_FUSE[c]} — {CCT[c][1]})",
                             _fuse_cx(i) - _FUSE_W / 2, _FUSE_YD, _FBLK_Z0 + _FBASE_H,
                             _FUSE_W, _FUSE_T, _FUSE_H, color=CCT[c][0]))
    p.append(ov.ruby_box("Busbar (+)", EP_X + 15, 30, ez + 205,
                         BUSBAR_L, BUSBAR_W, BUSBAR_H, color="#C0392B"))
    p.append(ov.ruby_box("Busbar (-)", EP_X + 15, 30, ez + 175,
                         BUSBAR_L, BUSBAR_W, BUSBAR_H, color="#2C2C2C"))
    p.append(ov.ruby_cylinder("Main Disconnect (m-Series)", EP_X + 240, ENCL_SHELL_D,
                              ez + 120, DISCONNECT_D / 2, DISCONNECT_H,
                              color="#D43A2F", axis="y"))
    # Main disconnect → busbar(+) load link: the battery + feed lands on the disconnect
    # LINE terminal (battery()); it exits the LOAD terminal here to the (+) busbar, so the
    # whole bank — and every circuit fed off it — is isolated when the knob is OFF.
    disc_x = EP_X + 240
    p.append(ov.ruby_pipe_run("Main feed (disconnect → busbar +)",
                              _dedup([(disc_x, 170, ez + 120 + 35),     # lands ON the disconnect LOAD terminal (top)
                                      (disc_x, 45, ez + 120 + 35),      # out toward the busbar plane
                                      (disc_x, 45, ez + 205),           # rise to busbar(+) level
                                      (EP_X + 15 + BUSBAR_L, 45, ez + 205)]),  # over to busbar(+) end
                              11, color="#8B1A1A"))
    # MPPT charge-line fuse — 60A on the MPPT battery-output lead, in front of the busbars
    # (D2; protects the 6 AWG charge conductor the 200A main fuse is too large to cover).
    p.append(ov.ruby_box("Charge-line Fuse (60A, MPPT -> battery)",
                         EP_X + 15, 95, ez + 195, 45, 30, 45, color="#222222"))
    # Interior E-stop — red mushroom on the EP (enclosure) face, paralleled with the
    # exterior one so the contactor can be tripped from inside too (D5).
    ies_cx, ies_cz = EP_X + EP_W / 2, EP_H_LO + 80
    p.append(ov.ruby_cylinder("Interior E-stop collar (safety yellow)",
                              ies_cx, ENCL_SHELL_D, ies_cz, 30, 12, color="#F2C200", axis="y"))
    p.append(ov.ruby_cylinder("Interior E-stop button (red mushroom)",
                              ies_cx, ENCL_SHELL_D + 12, ies_cz, 24, 26, color="#C42B1C", axis="y"))
    # E-stop trip wiring (D5): both E-stops sit in the battery-contactor coil loop. A control pair
    # runs from the contactor coil up to the interior E-stop; the two E-stops are then paralleled
    # (interior -> exterior via the external panel) so pressing EITHER drops the contactor.
    # The riser goes up the contactor's LEFT (X1620, clear of the bottom transport-stay anchor at
    # X1695-1895) and crosses ABOVE it (Z650 > the anchor's Z400-600) before dropping to the E-stop.
    _ctc_x, _ctc_z = BA_X + 20 + CONTACTOR_W / 2, BA_H_HI + CONTACTOR_H     # contactor coil top
    _ext_x, _ext_z = PWR_PANEL_X + PWR_PANEL_W / 2, PWR_PANEL_Z + PWR_PANEL_H / 2  # exterior E-stop
    _anchor_clear_z = 650                          # clears the transport-stay anchor top (Z600) + margin
    p.append(ov.ruby_pipe_run("E-stop trip line (contactor coil -> interior E-stop)",
                              _dedup([(_ctc_x, 45, _ctc_z), (_ctc_x, 10, _ctc_z + 20),
                                      (_ctc_x, 10, _anchor_clear_z),        # rise up the contactor's left, clear of the anchor
                                      (ies_cx, 10, _anchor_clear_z),        # cross ABOVE the transport-stay anchor
                                      (ies_cx, 10, ies_cz),
                                      (ies_cx, ENCL_SHELL_D, ies_cz)]),
                              4, color="#586070"))
    p.append(ov.ruby_pipe_run("E-stop parallel link (interior -> exterior E-stop)",
                              _dedup([(ies_cx, ENCL_SHELL_D, ies_cz), (ies_cx, 10, ies_cz),
                                      (ies_cx, 10, _ext_z), (_ext_x, 10, _ext_z),
                                      (_ext_x, -WALL, _ext_z)]),
                              4, color="#586070"))
    return '\n'.join(p)


def battery():
    """100Ah pack (+ ghosted 2nd plug-in) + battery contactor + MRBF main fuse."""
    p = []
    bw = (BA_W - 20) / 2
    for bx, nm, al in [(BA_X, "Battery 1 (12V 100Ah LiFePO4)", 1.0),
                       (BA_X + bw + 20, "Battery 2 (optional 2nd pack, ghosted)", 0.28)]:
        p.append(ov.ruby_box(nm, bx, 0, BA_H_LO, bw, BA_D, BA_H_HI - BA_H_LO,
                             color=ov.C_BATT, alpha=al))
    p.append(ov.ruby_box("Battery Contactor (ML-RBS)", BA_X + 20, 15, BA_H_HI,
                         CONTACTOR_W, CONTACTOR_D, CONTACTOR_H, color="#C42B1C"))
    p.append(ov.ruby_box("MRBF Main Fuse (on + post)", BA_X + CONTACTOR_W + 35, 20,
                         BA_H_HI, MRBF_D, MRBF_D, MRBF_H, color="#222222"))
    # Main battery cables (2/0 AWG) up to the enclosure — orthogonal (rise then over).
    # + leaves via the MRBF fuse and lands on the MAIN DISCONNECT *line* terminal (the
    # disconnect → busbar(+) load link is drawn in power_core(), so the bank is isolated
    # when the knob is OFF); − goes direct to the busbar(−).
    bus_x = EP_X + 20
    disc_x, disc_z = EP_X + 240, EP_H_LO + 120          # main disconnect centre (matches power_core)
    p.append(ov.ruby_pipe_run("Battery + cable (2/0 AWG, MRBF → main disconnect)",
                              _dedup([(BA_X + CONTACTOR_W + 55, 45, BA_H_HI + MRBF_H),
                                      (BA_X + CONTACTOR_W + 55, 45, disc_z - 35),
                                      (disc_x, 45, disc_z - 35),
                                      (disc_x, 170, disc_z - 35)]),   # lands ON the disconnect LINE terminal
                              11, color="#8B1A1A"))
    p.append(ov.ruby_pipe_run("Battery − cable (2/0 AWG)",
                              _dedup([(BA_X + 60, 60, BA_H_HI),
                                      (BA_X + 60, 60, EP_H_LO + 186),
                                      (bus_x + 20, 60, EP_H_LO + 186)]),
                              11, color="#202020"))
    return '\n'.join(p)


def external_panel():
    """Flush external power panel + MC4 PV bulkheads, NEMA shore inlet, GFCI cooler
    outlet (Circuit E), and the exterior E-stop."""
    p = []
    face_y = -WALL - 25
    p.append(ov.ruby_box("Ext. Power Panel (exterior)", PWR_PANEL_X, face_y,
                         PWR_PANEL_Z, PWR_PANEL_W, 25, PWR_PANEL_H,
                         color=ov.C_ALUM, alpha=0.55))
    p.append(ov.ruby_box("Ext. Power Panel (interior face)", PWR_PANEL_X, 0,
                         PWR_PANEL_Z, PWR_PANEL_W, 20, PWR_PANEL_H, color=ov.C_ELEC))

    def px(uf): return PWR_PANEL_X + uf * PWR_PANEL_W
    def pz(vf): return PWR_PANEL_Z + vf * PWR_PANEL_H

    for i, vf in enumerate((0.225, 0.5, 0.775)):
        p.append(ov.ruby_cylinder(f"MC4 PV{i + 1} (+)", px(0.192), face_y - 20, pz(vf),
                                  8, 20, color="#2D7A2D", axis="y"))
        p.append(ov.ruby_cylinder(f"MC4 PV{i + 1} (-)", px(0.275), face_y - 20, pz(vf),
                                  8, 20, color="#9AA0A6", axis="y"))
    p.append(ov.ruby_box("NEMA 5-15R shore inlet", px(0.742) - 30, face_y - 30,
                         pz(0.878) - 22, 60, 30, 45, color="#FFF0CC"))
    p.append(ov.ruby_cylinder("GFCI AC outlet (Cct E cooler)", px(0.767), face_y - 20,
                              pz(0.325), 12, 22, color="#E8884A", axis="y"))
    # E-stop on the exterior face.
    es_cx = PWR_PANEL_X + PWR_PANEL_W / 2
    es_cz = PWR_PANEL_Z + PWR_PANEL_H / 2
    p.append(ov.ruby_cylinder("E-stop collar (safety yellow)", es_cx, face_y - 12,
                              es_cz, 35, 12, color="#F2C200", axis="y"))
    p.append(ov.ruby_cylinder("E-stop button (red mushroom)", es_cx, face_y - 40,
                              es_cz, 26, 28, color="#C42B1C", axis="y"))
    # PV array disconnect — DC load-break isolator on the PV path (array -> MPPT). Brought IN onto the
    # EP plywood (interior, still readily accessible per NEC 690.13) rather than on the external panel.
    p.append(ov.ruby_box("PV Array Disconnect (load-break isolator)",
                         EP_X - 300, 0, EP_H_LO + 350, 70, 45, 70, color="#D43A2F"))

    # Evap cooler (Hessaire MC18M) — external, ground-placed off the pinhole wall — and
    # its 120V AC cord from the panel GFCI outlet (Circuit E). The DC feed (fuse block ->
    # inverter) and the inverter -> panel AC line are in their own components; this closes
    # the Cct E chain: ... GFCI outlet -> cord -> cooler.
    cw, cd, ch = EVAP_W, EVAP_D, EVAP_H
    cx = EVAP_DUCT_X - cw / 2
    cyd = -WALL - cd - 100         # matches the overview's evap_cooler() stand-off
    p.append(ov.ruby_box("Evap Cooler (Hessaire MC18M, external)", cx, cyd, 0,
                         cw, cd, ch, color=ov.C_EVAP))
    gfci_x = PWR_PANEL_X + 0.767 * PWR_PANEL_W
    gfci_z = PWR_PANEL_Z + 0.325 * PWR_PANEL_H
    inx = cx + cw - 80                    # cooler-top inlet
    # SOFT flexible cord — a curly coil draping DIAGONALLY from the GFCI down to the cooler
    # inlet (matches the overview's evap_cooler()); angles clear of the cooler body, with the
    # straight terminating stub doing the plug-in.
    p.append(ov.ruby_coil_cord("Cct E cooler cord (panel GFCI -> cooler, flexible)",
                               [(gfci_x, face_y - 10, gfci_z),
                                (inx, cyd + cd / 2, ch - 70)],
                               r=5, color="#E8884A"))
    return '\n'.join(p)


def inverter():
    """Circuit-E 12->120V inverter, mounted on the EP plywood panel (lower section, below
    the main gear), + its 120V AC output line across to the external panel's GFCI outlet."""
    p = [ov.ruby_box("Cct E Inverter (12->120V AC)", INVERTER_X, 0, INVERTER_Z,
                     INVERTER_W, INVERTER_D, INVERTER_H, color="#404848")]
    gfci_x = PWR_PANEL_X + 0.767 * PWR_PANEL_W
    gfci_z = PWR_PANEL_Z + 0.325 * PWR_PANEL_H
    p.append(ov.ruby_pipe_run("Cct E AC line (inverter -> panel GFCI)",
                              _dedup([(INVERTER_X + INVERTER_W / 2, 30, INVERTER_Z + INVERTER_H),
                                      (INVERTER_X + INVERTER_W / 2, 30, gfci_z),
                                      (gfci_x, 30, gfci_z),
                                      (gfci_x, 18, gfci_z)]),
                              7, color="#E8884A"))
    return '\n'.join(p)


def _pump_circuit():
    """Circuit C: the MASTER pump switch is on the EP (single manual cutoff, upstream of
    everything); the switched feed runs the ceiling trunk to a 12V distribution wireway/block
    on the equipment panel → a 16 AWG branch DIRECTLY to each Shurflo pump. No per-pump switches
    — each pump runs on its internal demand/pressure switch.
    Pump reference positions match panel-layout.png: the four corridor pumps in a SINGLE vertical
    column (AFF base Z, bottom->top P-01/P-04/P-05/P-03) fed from the corridor distribution block;
    P-02 (Brown recycle) lives on the Pinhole-Wall panel and taps the switched feed THERE (§7.3)."""
    col = CCT["C"][0]
    pcol = EQPANEL_YD + 63                              # single corridor pump column (panel-layout)
    # FOUR corridor pumps fed from the corridor distribution block. P-02 is separate (below the loop).
    pumps = [("P-01", pcol, 615), ("P-04", pcol, 940),
             ("P-05", pcol, 1340), ("P-03", pcol, 1740)]
    cy = EQPANEL_YD + EQPANEL_YD_SPAN / 2              # wireway Yd centre
    way_top = PUMP_H_HI                                 # feed enters the top
    way_bot = min(z for _, _, z in pumps) - 20         # extends DOWN past the lowest pump
    # Distribution WIREWAY — a vertical channel down the panel that covers every branch tap.
    p = [ov.ruby_box("Cct C distribution wireway", EQPANEL_X - 25, cy - 35, way_bot,
                     50, 70, way_top - way_bot, color="#2B2B30")]
    # MASTER PUMP SWITCH — on the EP front at the Circuit-C fuse (single cutoff, upstream of
    # everything; relocated from the equipment panel). Red-lever disconnect; the switched feed
    # then runs the ceiling trunk to the wireway.
    mfx, _mfy, mfz = FUSE_POS["C"]
    p.append(ov.ruby_box("Master pump switch (Cct C, on EP)", mfx - 25, ENCL_FRONT_YD, mfz - 44,
                         50, 46, 84, color="#202020"))
    p.append(ov.ruby_box("Master switch lever (OFF cutoff)", mfx - 8, ENCL_FRONT_YD + 46, mfz - 4,
                         16, 34, 16, color="#C0202A"))
    p.append(_run("C", (EQPANEL_X, cy, way_top - 25)))   # switched feed → top of the wireway
    for nm, yd, z in pumps:
        # branch taps the wireway at THIS pump's level → straight to the pump (no per-pump switch)
        br = _dedup([(EQPANEL_X, cy, z + 60), (EQPANEL_X, yd, z + 60)])
        p.append(ov.ruby_pipe_run(f"Cct C branch {nm}", br, 6, color=col))
    # P-02 (Brown recycle) is on the PINHOLE-WALL panel (X~3058, high with the 3-stage filter skid) —
    # NOT the corridor distribution block (which is at EQPANEL_X~4874). It taps the switched Circuit-C
    # feed where the ceiling trunk passes over it (electrical-report §7.3); the feed runs the ceiling
    # from the EP master switch to the corridor block, so it IS overhead here. X/Z match the
    # pinhole-water-panel model + pinhole-wall-elevation.
    p02x, p02_yd, p02z0, p02z1 = PWP_P02_X, 100, PWP_P02_Z0, PWP_P02_Z0 + PWP_P02_H
    p.append(ov.ruby_box("P-02 (Brown recycle - Pinhole-Wall filter pump)",
                         p02x - 25, p02_yd - 30, p02z0, 50, 60, p02z1 - p02z0, color="#6B4423"))
    p.append(ov.ruby_pipe_run("Cct C branch P-02 (taps ceiling feed - Pinhole-Wall panel)",
                              _dedup([(p02x, TRUNK_YD, TRUNK_Z), (p02x, p02_yd, TRUNK_Z),
                                      (p02x, p02_yd, p02z1)]), 6, color=col))
    return '\n'.join(p)


def circuit_runs():
    """Ceiling cable-trunking spine + the 7 color-coded circuits A-G to their loads.
    Single-load circuits (A,B,C,E,F) trace fuse-block→load; the lighting circuits
    (G white LED, D safelight) fan out to ALL three of their ceiling fixtures."""
    # Trunking spans only the circuit range (door-end first tap → Fan A), so there is
    # no dead-end grey stub past the last drop.
    cxs = [LOADS[c][0] for c in ("A", "B", "C", "E")] + \
          [e[0] for e in LED_ENDS + SAFE_ENDS] + [_FBLK_X0, _FBLK_X0 + FUSEBLK_W]
    tx0, tx1 = min(cxs) - 40, max(cxs) + 40
    p = [ov.ruby_box("Cable Trunking (40x25 PVC)", tx0, 0, ov.C_HGT - 25, tx1 - tx0, 40,
                     25, color=ov.C_TRUNK)]
    for cct in ("A", "B", "E"):
        p.append(_run(cct, LOADS[cct]))
    p.append(_pump_circuit())              # Cct C: master switch + distribution block → pumps
    p.append(_multi_run("G", LED_ENDS))    # 3× white LED (incl. rotated IBC-end panel)
    p.append(_multi_run("D", SAFE_ENDS))   # 3× safelight
    # Fan B flexible connector (wall box -> fan on the swing panel) — the SOFT jumper that is
    # unplugged before the panel swings; a curly coil cord (matches the overview's lighting_wiring()).
    p.append(ov.ruby_coil_cord("Fan B flex connector (box -> fan, Cct B)",
                               [(_FANB_BOX_X, 55, FAN_B_H), (60, FAN_B_YD, FAN_B_H)],
                               r=5, color=CCT["B"][0]))
    return '\n'.join(p)


def generate_ruby():
    comps = [
        ov.component("Container (ghost)", "Context", context()),
        ov.component("Solar Array", "Solar Array", ov.solar_array()),
        ov.component("Power Core", "Power Core", power_core()),
        ov.component("Battery Bank", "Battery", battery()),
        ov.component("External Power Panel", "External Panel", external_panel()),
        ov.component("Circuit-E Inverter", "Inverter", inverter()),
        ov.component("Circuit Runs", "Circuit Runs", circuit_runs()),
    ]
    body = '\n'.join(comps)
    tags_ruby = '\n'.join(
        f'  model.layers.add("{t}") unless model.layers["{t}"]' for t in TAGS)
    keep_tags_ruby = '[' + ', '.join(f'"{t}"' for t in TAGS) + ']'

    comp_tags = [t for t in TAGS if t != "Labels"]
    scenes = [
        ("Overview", comp_tags),
        ("Power Core", ["Power Core", "Battery", "Inverter"]),
        ("Distribution", ["Circuit Runs", "Power Core", "Battery"]),
        ("External Panel", ["External Panel", "Solar Array"]),
        ("Labeled", TAGS),
    ]
    scenes_ruby = '[' + ', '.join(
        '["%s", [%s]]' % (n, ', '.join(f'"{t}"' for t in tags))
        for n, tags in scenes) + ']'
    # Scenes that get a tight per-scene camera on a sub-volume (else shared extents).
    zoom = {"Power Core": (EP_X + EP_W / 2, 90, (EP_H_LO + EP_H_HI) / 2, 1400),
            "External Panel": (PWR_PANEL_X + PWR_PANEL_W / 2, -WALL - 25,
                               PWR_PANEL_Z + PWR_PANEL_H / 2, 1600)}
    zoom_ruby = '{' + ', '.join(
        '"%s" => [%s, %s, %s, %s]' % (n, ov.mm(x), ov.mm(y), ov.mm(z), ov.mm(d))
        for n, (x, y, z, d) in zoom.items()) + '}'

    sf_meta = ov.sketchfab_meta_ruby(
        "TBS-001 Electrical Model",
        "There are a number of discrete systems, color-coded in the diagram below. This view is "
        "shown from the optical axis, looking through the container wall. Each of these sub-systems, "
        "has a detailed breakdown of construction, schematic and other diagrams to show how each "
        "system it built, installed, used and maintained. The 3d model below provides a simply way "
        "to view the whole system.",
        "6930c96be025469fb8ef702393d7c35f", "sketchup")

    return f'''model = Sketchup.active_model
model.start_operation("TBS-001 Electrical", true)
entities = model.active_entities

opts = model.options["UnitsOptions"]
opts["LengthUnit"] = 2
opts["LengthFormat"] = 0
opts["LengthPrecision"] = 1

# ── Idempotent rebuild: clear prior groups/instances/text ──
to_erase = entities.to_a.select {{ |e|
  e.is_a?(Sketchup::Group) || e.is_a?(Sketchup::ComponentInstance) || e.is_a?(Sketchup::Text)
}}
entities.erase_entities(to_erase) unless to_erase.empty?
model.definitions.purge_unused
model.pages.to_a.each {{ |p| model.pages.erase(p) }}

{sf_meta}
# ── Tags ──
{tags_ruby}

# ── Subsystems ──
{body}

# ── In-model labels (Labels tag; visible only in the "Labeled" scene) ──
{elec_labels()}

{ov.license_note()}

model.definitions.purge_unused
model.materials.purge_unused

# ── Remove stale tags from earlier versions ──
keep_tags = {keep_tags_ruby}
default_layer = model.layers[0]
model.layers.to_a.each {{ |l|
  next if l == default_layer || keep_tags.include?(l.name)
  model.layers.remove(l, true) rescue nil
}}

# ── Scenes ── shared iso camera, with a tighter eye for the zoom scenes. ──
model.layers.each {{ |l| l.visible = (l.name != "Labels") }}
bb = model.bounds
ctr = bb.center
dir = Geom::Vector3d.new(0.72, -0.7, 0.5); dir.normalize!
eye = ctr.offset(dir, bb.diagonal * 1.5)
model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
model.active_view.zoom_extents

zoom = {zoom_ruby}
{scenes_ruby}.each {{ |name, tags|
  model.layers.each {{ |l| l.visible = (l == default_layer || l.name == "Context" || tags.include?(l.name)) }}
  # A Page captures the active_view camera at add-time (Page has no camera= setter),
  # so set the camera FIRST — zoomed for the detail scenes, shared otherwise.
  if zoom[name]
    zx, zy, zz, zd = zoom[name]
    tgt = Geom::Point3d.new(zx, zy, zz)
    zeye = tgt.offset(dir, zd)
    model.active_view.camera = Sketchup::Camera.new(zeye, tgt, Z_AXIS)
  else
    model.active_view.camera = Sketchup::Camera.new(eye, ctr, Z_AXIS)
  end
  page = model.pages.add(name)
  page.use_camera = true
}}
model.layers.each {{ |l| l.visible = true }}

model.commit_operation
{{ success: true, model: "Electrical",
   components: model.entities.grep(Sketchup::ComponentInstance).length,
   tags: model.layers.count, scenes: model.pages.count }}.to_json
'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate the TBS-001 Electrical SketchUp model")
    parser.add_argument("--save", action="store_true",
                        help="Write Ruby to src/models/electrical.rb")
    parser.add_argument("--send", action="store_true",
                        help="Send to the ACTIVE SketchUp document "
                             "(clears it first - open a NEW blank doc before sending)")
    args = parser.parse_args()

    ruby = generate_ruby()

    if args.save:
        out = os.path.join(os.path.dirname(__file__), "electrical.rb")
        with open(out, "w") as f:
            f.write(ruby)
        print(f"  {out} saved ({len(ruby)} bytes)")

    if args.send:
        from sketchup_client import send_ruby, SketchupError
        try:
            print(f"  SketchUp: {send_ruby(ruby)}")
        except SketchupError as e:
            print(f"  error: {e}", file=sys.stderr)
            sys.exit(1)

    if not args.save and not args.send:
        print(ruby)
