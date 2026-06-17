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
from tbs_constants import (
    EP_X, EP_W, EP_H_LO, EP_H_HI, BA_X, BA_W, BA_H_LO, BA_H_HI, BA_D,
    PWR_PANEL_X, PWR_PANEL_W, PWR_PANEL_H, PWR_PANEL_Z,
    INVERTER_X, INVERTER_Z, INVERTER_W, INVERTER_H, INVERTER_D,
    SOLAR_ARRAY_X, SOLAR_ARRAY_YD,    # (the solar array geometry moved to ov.solar_array)
    ENCL_SHELL_D, MPPT_W, MPPT_D, MPPT_H, FUSEBLK_W, FUSEBLK_D, FUSEBLK_H,
    BUSBAR_L, BUSBAR_W, BUSBAR_H, DISCONNECT_D, DISCONNECT_H,
    CONTACTOR_W, CONTACTOR_D, CONTACTOR_H, MRBF_D, MRBF_H,
    EQPANEL_X, EQPANEL_YD, EQPANEL_YD_SPAN, PUMP_H_HI,
    FAN_A_YD, FAN_A_H, FAN_B_YD, FAN_B_H, FAN_BODY_D, DUCT_DEPTH, DUCT_HEIGHT,
    EVAP_W, EVAP_D, EVAP_H, EVAP_DUCT_X,
)

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
ENCL_FRONT_YD = ENCL_SHELL_D + 10                    # risers run up the enclosure front (clears MPPT)
# per-circuit fuse terminal (cable origin) = top-centre of that circuit's blade
FUSE_POS = {c: (_fuse_cx(i), _FUSE_YD + _FUSE_T / 2, FUSE_TOP_Z)
            for i, c in enumerate(FUSE_ORDER)}
TRUNK_YD = 20                  # conductors hug the pinhole-wall ceiling line
TRUNK_Z = ov.C_HGT - 13


# ── Labels (project rule: every .skp gets a Labeled scene) ───────────────────
ELEC_POINT_LABELS = [
    (SOLAR_ARRAY_X + 700, SOLAR_ARRAY_YD - 600, 700,
     "SOLAR ARRAY\n3x 200W (30deg tilt)", -200, -700, 700),
    (EP_X + 90, 40, EP_H_HI - 60, "MPPT 100/50",                 -380, -700, 280),
    (EP_X + 90, 40, FUSE_TOP_Z, "FUSE STACK A-G\n5/5/15/5/40/20/10 A", 420, -700, 240),
    (EP_X + 90, 40, EP_H_LO + 210, "+/- BUSBARS",                 420, -640, -120),
    (EP_X + 240, ENCL_SHELL_D, EP_H_LO + 120, "MAIN DISCONNECT", 360, -760, -260),
    (BA_X + 80, 40, BA_H_HI + 50, "BATTERY CONTACTOR\n+ MRBF main fuse", -300, -760, 900),
    (BA_X + 120, 60, BA_H_LO + 100, "BATTERY 1x 100Ah\n(2nd pack ghosted)", -320, -640, 760),
    (INVERTER_X + INVERTER_W / 2, INVERTER_D / 2, INVERTER_Z + INVERTER_H,
     "CCT-E INVERTER\n12->120V AC (cooler)", -430, -820, 480),
    (PWR_PANEL_X + PWR_PANEL_W / 2, -WALL - 40, PWR_PANEL_Z + PWR_PANEL_H + 20,
     "EXTERNAL PANEL\nMC4 PV / shore / GFCI cooler / E-STOP", 220, -520, 380),
    (EVAP_DUCT_X, -WALL - EVAP_D / 2 - 120, EVAP_H,
     "EVAP COOLER\n(Hessaire MC18M, Cct E)", -260, -520, 520),
    (EQPANEL_X, EQPANEL_YD + EQPANEL_YD_SPAN / 2, PUMP_H_HI - 40,
     "CCT-C PUMP DISTRIBUTION\n5 switches — P-01..P-05 (one at a time)", -350, -700, 250),
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
    return ov.ruby_pipe_run(f"Circuit {cct} ({CCT[cct][1]})", pts, 8, color=CCT[cct][0])


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
                         8, color=col),
        ov.ruby_pipe_run(f"Circuit {cct} ceiling spine ({CCT[cct][1]})",
                         [(min(xs), TRUNK_YD, TRUNK_Z), (max(xs), TRUNK_YD, TRUNK_Z)],
                         8, color=col),
    ]
    for x, yd, z in ends:
        br = _dedup([(x, TRUNK_YD, TRUNK_Z), (x, yd, TRUNK_Z), (x, yd, z)])
        if len(br) > 1:
            p.append(ov.ruby_pipe_run(f"Circuit {cct} drop X{int(x)} ({CCT[cct][1]})",
                                      br, 8, color=col))
    return '\n'.join(p)


def context():
    """Full-length ghost container shell + faint ghost loads (the circuit endpoints
    that aren't modeled as their own components: fans, pump cluster, LED, safelight)."""
    t = WALL
    p = [
        ov.ruby_box("Floor (context)", 0, 0, -t, ov.C_LEN, ov.C_WID, t,
                    color=ov.C_SHELL, alpha=0.22),
        ov.ruby_box("Ceiling (context)", 0, 0, ov.C_HGT, ov.C_LEN, ov.C_WID, t,
                    color=ov.C_SHELL, alpha=0.08),
        ov.ruby_box("Pinhole Wall (context)", 0, -t, 0, ov.C_LEN, t, ov.C_HGT,
                    color=ov.C_SHELL, alpha=0.10),
        ov.ruby_box("Far Wall (context)", 0, ov.C_WID, 0, ov.C_LEN, t, ov.C_HGT,
                    color=ov.C_SHELL, alpha=0.14),
        ov.ruby_box("End Wall door (context)", -t, 0, 0, t, ov.C_WID, ov.C_HGT,
                    color=ov.C_SHELL, alpha=0.14),
        ov.ruby_box("End Wall sealed (context)", ov.C_LEN, 0, 0, t, ov.C_WID, ov.C_HGT,
                    color=ov.C_SHELL, alpha=0.14),
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
    """Ghosted IP65 enclosure around the EP volume + its internals: MPPT, fuse block,
    +/- busbars, rotary main disconnect (knob on the face)."""
    p = []
    ez = EP_H_LO
    eh = EP_H_HI - EP_H_LO
    p.append(ov.ruby_box("Enclosure (IP65, ghosted)", EP_X - 12, 0, ez - 12,
                         EP_W + 24, ENCL_SHELL_D + 6, eh + 24,
                         color=ov.C_STEEL, alpha=0.12))
    p.append(ov.ruby_box("MPPT Controller (100/50)", EP_X + 15, 25,
                         EP_H_HI - MPPT_H - 30, MPPT_W, MPPT_D, MPPT_H, color="#3A5BA0"))
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
    # Main battery cables (2/0 AWG) up to the enclosure busbars — orthogonal
    # (rise then over). + leaves via the MRBF fuse; − direct off the pack.
    bus_x = EP_X + 20
    p.append(ov.ruby_pipe_run("Battery + cable (2/0 AWG, via MRBF)",
                              _dedup([(BA_X + CONTACTOR_W + 55, 45, BA_H_HI + MRBF_H),
                                      (BA_X + CONTACTOR_W + 55, 45, EP_H_LO + 216),
                                      (bus_x + 20, 45, EP_H_LO + 216)]),
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
    cf = -WALL - 55                       # cord stand-off plane outside the wall
    inx = cx + cw - 80                    # cooler-top inlet
    p.append(ov.ruby_pipe_run("Cct E cooler cord (panel GFCI -> cooler)",
                              _dedup([(gfci_x, face_y - 10, gfci_z),
                                      (gfci_x, cf, gfci_z),
                                      (gfci_x, cf, ch - 100),
                                      (inx, cf, ch - 100),
                                      (inx, cyd + cd / 2, ch - 100)]),
                              8, color="#E8884A"))
    return '\n'.join(p)


def inverter():
    """Circuit-E 12->120V inverter on the pinhole wall, below the EP, + its 120V AC
    output line across to the external power panel's GFCI outlet (interior)."""
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
    """Circuit C: feed → drop to a 12V distribution block on the equipment panel →
    5 individual pump switches → the 5 Shurflo pumps (one at a time). Per the
    Equipment Panel report: left column P-01/P-04, right column P-02/P-03/P-05."""
    col = CCT["C"][0]
    lcol, rcol = EQPANEL_YD + 63, EQPANEL_YD + 207     # column centres (panel report)
    pumps = [("P-01", lcol, 1229), ("P-04", lcol, 1487),
             ("P-02", rcol, 1229), ("P-03", rcol, 1487), ("P-05", rcol, 1855)]
    cy = EQPANEL_YD + EQPANEL_YD_SPAN / 2              # wireway Yd centre
    way_top = PUMP_H_HI                                 # feed enters the top
    way_bot = min(z for _, _, z in pumps) - 20         # extends DOWN past the lowest pump
    # Distribution WIREWAY — a vertical channel down the panel that covers every branch
    # tap (the 5 power drops), instead of a single block floating above them.
    p = [ov.ruby_box("Cct C distribution wireway", EQPANEL_X - 25, cy - 35, way_bot,
                     50, 70, way_top - way_bot, color="#2B2B30")]
    p.append(_run("C", (EQPANEL_X, cy, way_top - 25)))   # feed → top of the wireway
    for nm, yd, z in pumps:
        swx = EQPANEL_X - 120                           # switch on the panel face (-X)
        p.append(ov.ruby_box(f"Pump switch {nm} (Cct C)", swx - 20, yd - 20, z + 40,
                             40, 40, 40, color="#202020"))
        # branch taps the wireway at THIS pump's level → switch → pump (orthogonal)
        br = _dedup([(EQPANEL_X, cy, z + 60), (swx, cy, z + 60), (swx, yd, z + 60)])
        p.append(ov.ruby_pipe_run(f"Cct C branch {nm}", br, 6, color=col))
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
    p.append(_pump_circuit())              # Cct C: distribution block + 5 pump switches
    p.append(_multi_run("G", LED_ENDS))    # 3× white LED (incl. rotated IBC-end panel)
    p.append(_multi_run("D", SAFE_ENDS))   # 3× safelight
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
        ("Combined", comp_tags),
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
