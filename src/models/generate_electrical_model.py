#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""Generate the TBS-001 Electrical / Power System SketchUp model (logical model: electrical).

The missing subsystem model: solar generation -> storage -> distribution -> loads.
REUSES the helpers and conventions from the Overview generator
(generate_sketchup_model.py) — same component/tag/scene structure, shared iso camera,
material-sharing-by-color, and `tbs_constants`. Higher fidelity than the overview's
coarse `ov.electrical()`: a ghosted enclosure + distinct internals, the (otherwise
unmodeled) ground solar array, and color-coded circuit runs to ghosted loads.

Tags / scenes:
    Context        ghost container + faint ghost loads (fans, pumps, LED, safelight)
                   + transport-stay locks (wall anchors) + chem-prep shelf (clearance refs)
    Solar Array    3x 200W panels on a 30deg ground tilt frame + PV run
    Power Core     ghosted enclosure + MPPT / fuse block / busbars / disconnect
    Battery        100Ah pack (+ ghost 2nd) + contactor + MRBF main fuse
    External Panel penetration box + MC4 / NEMA inlet / WR cooler outlet + E-stop
    Inverter       Circuit-E 12->120V inverter
    Circuit Runs   ceiling trunking spine + 7 color-coded circuits A-G to the loads
  Scenes: Overview, Power Core, Distribution, External Panel, Labeled.

Usage:
    python3 src/models/generate_electrical_model.py --save        # write electrical.rb
    python3 src/models/generate_electrical_model.py --save --send # + send to ACTIVE doc

NOTE: --send builds into the ACTIVE SketchUp document (it clears it first). Open a
NEW blank document before sending so the Overview model isn't overwritten, then save
the result as models/electrical.skp.
"""
import math
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import generate_sketchup_model as ov   # helpers + conventions (Overview)
import tbs_draw as draw                          # shared drawing/material primitives
from tbs_constants import SOLAR_ARRAY_Z, SOLAR_GAP, SOLAR_N, SOLAR_PANEL_L, SOLAR_PANEL_T, SOLAR_PANEL_W, SOLAR_TILT_DEG, WALL_T, C_LEN, FAN_DIAM, EP_X, EP_W, EP_H_LO, EP_H_HI, EP_COL_W, BA_STACK_Z2, BA_STACK_TOP, EP_POST_Z, EP_RISE_X_M, PV_DISC_X, PV_DISC_Z, EP_DISC_Z, BA_W, BA_H_LO, BA_H_HI, BA_D, PWR_PANEL_X, PWR_PANEL_W, PWR_PANEL_H, PWR_PANEL_Z, PWR_PANEL_D, PWR_PANEL_CUTOUT_W, PWR_PANEL_CUTOUT_H, PWR_PANEL_BOX_D, PWR_PANEL_SHROUD_T, INVERTER_X, INVERTER_Z, INVERTER_W, INVERTER_H, INVERTER_D, SOLAR_ARRAY_X, SOLAR_ARRAY_YD, ENCL_SHELL_D, MPPT_W, MPPT_D, MPPT_H, FUSEBLK_W, FUSEBLK_D, BUSBAR_L, BUSBAR_W, BUSBAR_H, DISCONNECT_D, DISCONNECT_H, CONTACTOR_W, CONTACTOR_D, CONTACTOR_H, MRBF_D, MRBF_H, EQPANEL_X, EQPANEL_YD, EQPANEL_YD_SPAN, PUMP_H_HI, FAN_A_YD, FAN_A_H, FAN_B_YD, FAN_B_H, FAN_BODY_D, DUCT_DEPTH, DUCT_HEIGHT, EVAP_W, EVAP_D, EVAP_H, EVAP_DUCT_X, PULL_CORD_BOTTOM_Z

TAGS = ["Context", "Solar Array", "Power Core", "Battery", "External Panel",
        "Inverter", "Circuit Runs", "Lighting", "Labels"]

WALL = ov.WALL_T

# WR duplex cooler-outlet vertical position on the panel face (fraction of
# PWR_PANEL_H). Single-sourced: the outlet body, its in-use cover, and the two
# cooler-cord connection points all key off this so they move together.
_OUTLET_VF = 0.4292     # raised 25mm from 0.325 (0.325 + 25/240)

# Interior PV bus/feed geometry — single-sourced so external_panel()'s inner buses and
# power_core()'s PV feed take-offs stay aligned. The + and − buses run OUTBOARD of their
# own stub columns (+ bus left of 0.192, − bus right of 0.275) and on separate Yd lanes,
# so the green (+) and grey (−) collector never crowd each other at the bottom string pair.
MC4_PLUS_X  = PWR_PANEL_X + 0.192 * PWR_PANEL_W + 6      # + bus X (just inboard of the + stubs — off the box side wall)
MC4_MINUS_X = PWR_PANEL_X + 0.275 * PWR_PANEL_W + 16     # − bus X (outboard-right of the − stubs)
MC4_PLUS_Y, MC4_MINUS_Y = 22, 46                         # +/− bus Yd lanes (feeds inherit these)
MC4_PAIR_VF = (0.36, 0.5, 0.64)                          # the 3 string-pair heights (fraction of PWR_PANEL_H),
                                                         # tightened about center to leave clear margin top & bottom
MC4_BOT_Z   = PWR_PANEL_Z + MC4_PAIR_VF[0] * PWR_PANEL_H  # bottom string pair Z (feed take-off, = bus bottom)
MC4_FEED_Z  = PWR_PANEL_Z + 0.225 * PWR_PANEL_H           # the feeds drop to this height for their horizontal run —
                                                         # below the bottom pair AND below the orange AC crossover

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
# White LED (Cct G): 4 COB strips — 3 over the tray (X≈600/2350 parallel to the drum-side
# reds + 1 at the tray's X-center), + 1 rotated 90° running the IBC/plumbing corridor length.
# The 3rd tray run takes Circuit G to ~8.8A, so its feed is rewired 14→12 AWG on a 15A fuse.
# (x0,y0,w_x,w_yd)
_TRAY_CX = (ov.PROC_TRAY_X_L + ov.PROC_TRAY_X_R) // 2   # 2454 — processing-tray X center
LED_PANELS = [(600, 100, 40, ov.C_WID - 200),
              (2350, 100, 40, ov.C_WID - 200),
              (_TRAY_CX, 100, 40, ov.C_WID - 200),
              (ov.IBC_COL_X, EQPANEL_YD - 20, ov.C_LEN - ov.IBC_COL_X - 43, 40)]
SAFE_XS = [500, 2250, 4150]
# Circuit-drop endpoints (x, yd, z) — conduit lands per the overview.
LED_ENDS = [(620, 100, ov.C_HGT - 40),
            (2370, 100, ov.C_HGT - 40),
            (_TRAY_CX + 20, 100, ov.C_HGT - 40),
            (ov.IBC_COL_X + 60, EQPANEL_YD, ov.C_HGT - 40)]
SAFE_ENDS = [(sx + 20, 100, ov.C_HGT - 25) for sx in SAFE_XS]
# Ceiling pull-cord switches (D, G) — in the ~80mm clear band ahead of the pinhole wall, left of the
# EP + transport-stay anchor. Single-sourced so electrical + overview draw the SAME switches.
PULL_SW_X = (950, 1030)
PULL_SW_YD = 45

# Fan A on the sealed end wall; Fan B terminates at a fixed WALL BOX (the fan itself is
# on the swing panel, reached by a flex connector — not part of the rigid conduit).
_FAN_A_X = (ov.C_LEN - DUCT_DEPTH) + FAN_BODY_D / 2     # 5618
_FAN_A_TOP = FAN_A_H + DUCT_HEIGHT / 2                  # 2100
_FANB_BOX_X = 420   # Fan B wall-box X — shifted +120mm toward the pinhole to clear the film-plane beams (box + flex + the Cct-B run all key off this; lt.fan_b_box matches)

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
CCT_FUSE = {"A": "5A", "B": "5A", "C": "15A", "D": "5A", "E": "40A", "F": "20A", "G": "15A"}
_FBLK_X0 = EP_X + 15                        # fuse-block left edge (X)
_FBLK_YD = 25                              # block front Yd inside the enclosure
_FBLK_Z0 = EP_H_LO + 40                    # block base bottom Z — near the enclosure floor (reach re-lay)
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
# Each circuit runs at its OWN Yd across the width of the 40mm trunk, so they lie SIDE BY SIDE (a cable
# bundle) instead of coincident on one centerline (which read as crossings). F is a spare (no run).
_CCT_RUN = ["A", "B", "C", "D", "E", "G"]
CCT_TRUNK_YD = {c: 10 + i * 6 for i, c in enumerate(_CCT_RUN)}   # A=10 … G=40, 6mm apart
CCT_WIRE_R = 2.5               # thin 12V conductor (was 6 — too fat; made the bundle read as one pipe)
EP_CTRL_FACE_YD = 100   # EP access-panel front face Yd — the E-stop + master switch SURFACE-MOUNT here (wired from behind)
MASTER_SW_POS = (EP_X + 130, EP_CTRL_FACE_YD, EP_DISC_Z + 84)   # master pump switch REAR terminal (on the access-panel front, rear-wired)


# ── Labels (project rule: every .skp gets a Labeled scene) ───────────────────
ELEC_POINT_LABELS = [
    (SOLAR_ARRAY_X + 700, SOLAR_ARRAY_YD - 600, 700,
     "SOLAR ARRAY\n3x 200W (30deg tilt)", -200, -700, 700),
    (EP_X + 90, 40, EP_H_HI - 60, "MPPT 100/50",                 -380, 700, 280),
    (EP_X + 90, 40, FUSE_TOP_Z, "FUSE STACK A-G\n5/5/15/5/40/20/10 A", 420, 700, 240),
    (EP_X + 90, 40, EP_H_LO + 160, "+/- BUSBARS",                 420, 640, -120),
    (EP_X + 55, 0, EP_DISC_Z, "MAIN DISCONNECT", 360, 760, -260),
    (EP_X + 60, 40, EP_POST_Z + 60, "BATTERY CONTACTOR\n+ MRBF main fuse", -300, 760, 900),
    (EP_X + 150, 60, BA_H_LO + 100, "BATTERY 1x 100Ah\n(2nd pack ghosted)", -320, 640, 760),
    (INVERTER_X + INVERTER_W / 2, INVERTER_D / 2, INVERTER_Z + INVERTER_H,
     "CCT-E INVERTER\n12->120V AC (cooler)", -430, 820, 480),
    (PWR_PANEL_X + PWR_PANEL_W / 2, -WALL - 40, PWR_PANEL_Z + PWR_PANEL_H + 20,
     "EXTERNAL PANEL\nMC4 PV / shore / WR cooler / E-STOP", 220, -520, 380),
    (EVAP_DUCT_X, -WALL - EVAP_D / 2 - 120, EVAP_H,
     "EVAP COOLER\n(Hessaire MC18M, Cct E)", -260, -520, 520),
    (EQPANEL_X, EQPANEL_YD + EQPANEL_YD_SPAN / 2, PUMP_H_HI - 40,
     "CCT-C PUMP DISTRIBUTION\ndist block → pumps (master sw on EP)", -350, -700, 250),
    (PV_DISC_X + 35, 22, PV_DISC_Z + 35,
     "PV DISCONNECT\n(load-break, array->MPPT)", 300, 560, 320),
    (EP_X + 40, 95, EP_H_LO + 155, "60A CHARGE FUSE\n(MPPT -> battery)", 440, 680, 160),
    (EP_X + 270, 20, EP_DISC_Z + 20,
     "INTERIOR E-STOP\n(parallel)", -340, 560, -160),
    (_FANB_BOX_X, 30, FAN_B_H, "FAN B FEED (Cct B)\nwall box -> flex jumper", 320, 650, 760),
    (_FAN_A_X, FAN_A_YD, FAN_A_H, "FAN A FEED (Cct A)\nexhaust, sealed end", 400, -550, -400),
]


def elec_labels():
    rows = []
    for x, y, z, text, dx, dy, dz in ELEC_POINT_LABELS:
        rows.append(
            f'anc = Geom::Point3d.new({draw.mm(x)}, {draw.mm(y)}, {draw.mm(z)})\n'
            f'txt = entities.add_text("{text}", anc, '
            f'Geom::Vector3d.new({draw.mm(dx)}, {draw.mm(dy)}, {draw.mm(dz)}))\n'
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
    tyd = CCT_TRUNK_YD[cct]         # this circuit's OWN lane across the trunk width (side-by-side bundle)
    pts = _dedup([
        (fx, fy, fz),               # this circuit's fuse top terminal (inside enclosure)
        (fx, ENCL_FRONT_YD, fz),    # out to the enclosure front face (Yd) — clears the MPPT
        (fx, ENCL_FRONT_YD, TRUNK_Z),  # rise up the enclosure front to the ceiling (Z)
        (fx, tyd, TRUNK_Z),         # pull to this circuit's trunk lane (Yd)
        (lx, tyd, TRUNK_Z),         # run ALONG the ceiling to the load's X (X)
        (lx, lyd, TRUNK_Z),         # cross out toward the load (Yd)
        (lx, lyd, lz),              # drop perpendicular to the load (Z)
    ])
    run = draw.ruby_pipe_run(f"Circuit {cct} ({CCT[cct][1]})", pts, CCT_WIRE_R, color=CCT[cct][0])
    # P-clips on the out-of-trunk part — the cross off the trunk lane + the drop to the load (the
    # Fan A far-end cross/drop, the Fan B wall drop). The along-ceiling leg sits in the trunk.
    clips = draw.ruby_clip_run(f"Circuit {cct}", pts[4:], spacing=450)
    return run + ("\n" + clips if clips else "")


def _multi_run(cct, ends):
    """Circuit feeding MULTIPLE ceiling fixtures (LED / safelight): a fuse-block feed
    onto the ceiling line, a ceiling spine spanning all fixture Xs, and a perpendicular
    cross+drop at EACH fixture (its own Yd) — all orthogonal, so every light connects."""
    col, fx, fy, fz = CCT[cct][0], *FUSE_POS[cct]
    tyd = CCT_TRUNK_YD[cct]         # this circuit's OWN lane across the trunk width
    xs = [e[0] for e in ends]
    p = [
        draw.ruby_pipe_run(f"Circuit {cct} feed ({CCT[cct][1]})",
                         _dedup([(fx, fy, fz), (fx, ENCL_FRONT_YD, fz),
                                 (fx, ENCL_FRONT_YD, TRUNK_Z), (fx, tyd, TRUNK_Z)]),
                         CCT_WIRE_R, color=col),
        draw.ruby_pipe_run(f"Circuit {cct} ceiling spine ({CCT[cct][1]})",
                         [(min(xs), tyd, TRUNK_Z), (max(xs), tyd, TRUNK_Z)],
                         CCT_WIRE_R, color=col),
    ]
    for x, yd, z in ends:
        br = _dedup([(x, tyd, TRUNK_Z), (x, yd, TRUNK_Z), (x, yd, z)])
        if len(br) > 1:
            p.append(draw.ruby_pipe_run(f"Circuit {cct} drop X{int(x)} ({CCT[cct][1]})",
                                      br, CCT_WIRE_R, color=col))
            # Clip only the LONG drops (the corridor light's cable crosses the corridor off the trunk);
            # the tray/safelight fixtures sit at the ceiling so their stubs need no support.
            if abs(yd - tyd) > 200:
                p.append(draw.ruby_clip_run(f"Circuit {cct} drop", br, spacing=450))
    return '\n'.join(p)


def context():
    """Full-length ghost container shell + faint ghost loads (the circuit endpoints
    that aren't modeled as their own components: fans, pump cluster, LED, safelight)."""
    t = WALL
    # Shell reduced to Floor + Pinhole Wall only — the ceiling, the Far (film-plane) wall, and both end
    # walls (cargo-door + sealed) are dropped so the model orbits freely without them occluding the
    # electrical gear, which all lives on the pinhole wall.
    p = [
        draw.ruby_box("Floor (context)", 0, 0, -t, ov.C_LEN, ov.C_WID, t,
                    color=draw.C_SHELL, alpha=0.22),
        draw.ruby_box("Pinhole Wall (context)", 0, -t, 0, ov.C_LEN, t, ov.C_HGT,
                    color=draw.C_SHELL, alpha=0.10),
    ]
    # Ghost loads (faint) — geometry identical to the overview's lighting_wiring().
    p.append(draw.ruby_box("Fan A ghost (exhaust)", _FAN_A_X - 60, FAN_A_YD - 75,
                         FAN_A_H - 75, 120, 150, 150, color=CCT["A"][0], alpha=0.18))
    p.append(draw.ruby_box("Fan B wall box ghost (Cct B)", _FANB_BOX_X - 40, 0,
                         FAN_B_H - 45, 80, 60, 90, color=CCT["B"][0], alpha=0.20))
    # (The Cct-C pump-zone ghost was removed: circuit_runs() now draws the REAL corridor pump
    # distribution via pw.panel_power() — dist block + bus + branches — so the ghost was both
    # redundant and stale, sitting at the retired EQPANEL_X layout rather than the real cp pumps.)
    # (The LED + safelight strips are now REAL fixtures — light_fixtures() — not ghosts; the fan
    # loads below stay ghosted since those fixtures live in other models.)
    return '\n'.join(p)


def master_switch():
    """The Cct-C master pump cutoff — body + red OFF lever — on the EP, in the reachable disconnect
    cluster (grouped with the main + PV disconnects). SINGLE OWNER — power_core() and the water
    plumbing-panel's standalone view both call this. `MASTER_SW_POS` is its top feed terminal."""
    _msx, _msz = EP_X + 130, EP_DISC_Z
    return '\n'.join([
        draw.ruby_box("Master pump switch (Cct C, on EP)", _msx - 25, EP_CTRL_FACE_YD, _msz, 50, 46, 84, color="#202020"),   # SURFACE-mounted on the access-panel front
        draw.ruby_box("Master switch lever (OFF cutoff)", _msx - 8, EP_CTRL_FACE_YD + 46, _msz + 40, 16, 20, 16, color="#C0202A"),
    ])


def power_core(external_links=True, links_only=False):
    """EP internals on a PLYWOOD BACKING PANEL, with the DC gear inside a ghosted IP65 enclosure
    (its back IS the plywood): MPPT, fuse block,
    +/- busbars, rotary main disconnect (knob on the face). All components surface-mount
    on the ply; the MPPT sits forward on its own sub-panel to clear the fuse-stack risers."""
    p = []
    ez = EP_H_LO
    eh = EP_H_HI - EP_H_LO
    # EP access/control panel band (item: controls separated from wiring) — a ply fascia at the E-stop
    # height spanning the two EP side lips; the E-stop, master lever + disconnect handle poke through it.
    _ACCESS_YB, _ACCESS_YF = EP_CTRL_FACE_YD - 18, EP_CTRL_FACE_YD   # fascia back + front Yd (controls surface-mount on the front)
    _ACCESS_Z0, _ACCESS_Z1 = EP_H_LO - 150, EP_H_LO - 5   # just below the enclosure, centered on the E-stop height
    # Plywood backing panel (18mm) — a single tall NARROW board (the panel is now a skinny column in
    # the clear band, right of the external panel, so no step is needed). The DC gear sits inside a
    # ghosted IP65 enclosure (added below) whose back panel is this plywood.
    _ply_x0 = EP_X - 12
    _ply_r = EP_X + EP_COL_W + 12
    _ply_h = (EP_H_HI + 12) - (BA_H_LO - 12)
    # Cross members (the MPPT mount + the access/control panel) each SPAN the two EP side lips and seat
    # in a 9mm rebate in each lip — the MPPT and the controls surface-mount on these full-width members.
    _xm_reb = 9
    _xm_l = _ply_x0 + 18 - _xm_reb
    _xm_r = (_ply_r - 18) + _xm_reb
    p.append(draw.ruby_box("EP plywood backing panel (18mm)", _ply_x0, -18, BA_H_LO - 12,
                         _ply_r - _ply_x0, 18, _ply_h, color=draw.C_PLY, alpha=0.3))   # transparent — see the gear mounted on it
    # 100mm wooden LIPS (returns) down both vertical sides — a mounting surface for the switches +
    # stiffens the skinny board.
    p.append(draw.ruby_box("Plywood side lip (left, 18mm)", _ply_x0, 0, BA_H_LO - 12, 18, 100, _ply_h, color=draw.C_PLY, alpha=0.3))
    p.append(draw.ruby_box("Plywood side lip (right, 18mm)", _ply_r - 18, 0, BA_H_LO - 12, 18, 100, _ply_h, color=draw.C_PLY, alpha=0.3))
    # IP65 enclosure — ghosted weatherproof box over the fuse block + busbars + charge fuse (the DC
    # distribution terminals that need sealing), mounted ON the plywood (its back IS the plywood). The
    # MPPT, main disconnect, battery and inverter mount on the plywood outside it.
    p.append(draw.ruby_box("IP65 enclosure (ghosted, fuse block + busbars)", EP_X + 5, 12, EP_H_LO,
                         200, 140, 220, color=draw.C_STEEL, alpha=0.12))
    # MPPT mounts on a plywood CROSS MEMBER that SPANS the two EP side lips (housed in a 9mm rebate in
    # each), exactly like the access panel below — NOT its own little sub-panel. Transparent, so the gear
    # behind reads through; the MPPT body surface-mounts on its front face (Yd = EP_CTRL_FACE_YD).
    _sp_z0, _sp_h = EP_H_HI - MPPT_H - 30, MPPT_H + 30
    p.append(draw.ruby_box("MPPT cross-member (18mm ply, spans EP sides, rebated)",
                         _xm_l, _ACCESS_YB, _sp_z0, _xm_r - _xm_l, 18, _sp_h, color=draw.C_PLY, alpha=0.3))
    p.append(draw.ruby_box("MPPT Controller (100/50)", EP_X + 15, EP_CTRL_FACE_YD,
                         EP_H_HI - MPPT_H, MPPT_W, MPPT_D, MPPT_H, color="#3A5BA0"))
    # PV interior feed: external-panel MC4 bulkheads -> MPPT PV input (the conductor from
    # the interior side of the MC4 connectors; the exterior array->panel run is ov.solar_array()).
    # Crosses at the bottom MC4 height (Z≈1884, under the overview's upper transport-stay
    # anchor) and over the fuse block, then rises into the MPPT at Yd 85 (clear of the fuse
    # block at Yd 25-70). Duplicated in the overview's electrical() — keep in sync.
    # PV feed: MC4 (external) -> across ABOVE the chem shelf into the column -> down THROUGH the array
    # disconnect (now at operator height) -> up to the MPPT PV input.
    _pvx = PV_DISC_X + 35   # box center — the green cables land aligned in the disconnect box
    _pvd_rz = PV_DISC_Z + 35                      # PV-disconnect REAR terminal Z = box MID-height (rear-wired)
    # The green PV feed + the grey E-stop link below are the two circuits that run OUT to the external
    # panel; collect them into ext_links so the overview can draw them on a SEPARATE tag.
    # Both land on the disconnect REAR, centered on the box mid (X = _pvx) and SEPARATED ±18mm.
    # Each feed takes off from the bottom of ITS OWN collector bus (MC4_PLUS_*/MC4_MINUS_*) and runs its
    # horizontal leg at MC4_FEED_Z — well inside the box (above the bottom cutout edge, below the string
    # pairs + orange AC crossover). The two runs stay clear on their own Yd lanes: green shallow (22),
    # grey deep (46); both sit INSIDE the box, not along the bottom edge.
    ext_links = []
    _pvp1 = _dedup([(MC4_PLUS_X, MC4_PLUS_Y, MC4_BOT_Z),
                    (MC4_PLUS_X, MC4_PLUS_Y, MC4_FEED_Z),        # drop to the feed-run height, on the shallow Yd lane
                    (_pvx - 18, MC4_PLUS_Y, MC4_FEED_Z),         # run +x INSIDE the box, parallel to the grey feed, out the +x side toward the pinhole
                    (_pvx - 18, MC4_PLUS_Y, _pvd_rz),
                    (_pvx - 18, EP_CTRL_FACE_YD, _pvd_rz)])     # land LEFT of the box mid, on the REAR
    ext_links.append(draw.ruby_pipe_run("PV feed (MC4 -> array disconnect, top)", _pvp1, 6, color="#2D7A2D"))
    _pvp2 = _dedup([(_pvx + 18, EP_CTRL_FACE_YD, _pvd_rz),      # off the disconnect REAR, RIGHT of the box mid
                    (_pvx + 18, 45, _pvd_rz),                   # back BEHIND the panel (leaves the switch from the rear, like the MC4 feed)
                    (_pvx + 18, 45, EP_H_HI - MPPT_H + 40),     # up behind, to the MPPT height
                    (_pvx - 4, 45, EP_H_HI - MPPT_H + 40),      # −X behind, to the MPPT X
                    (_pvx - 4, EP_CTRL_FACE_YD, EP_H_HI - MPPT_H + 40)])   # forward into the MPPT back (single clean entry)
    ext_links.append(draw.ruby_pipe_run("PV feed (array disconnect -> MPPT, top)", _pvp2, 6, color="#2D7A2D"))
    # PV − feed (grey): the array negative from the MC4 − bus up to the MPPT PV− input (parallels the
    # green +, on its own −Yd lane so the pair reads clearly; the − is continuous, not switched).
    _pvm = _dedup([(MC4_MINUS_X, MC4_MINUS_Y, MC4_BOT_Z),
                   (MC4_MINUS_X, MC4_MINUS_Y, MC4_FEED_Z),      # drop to the clear feed-run height (below the orange AC line)
                   (_pvx - 42, MC4_MINUS_Y, MC4_FEED_Z),
                   (_pvx - 42, MC4_MINUS_Y, EP_H_HI - MPPT_H + 70),
                   (_pvx - 20, MC4_MINUS_Y, EP_H_HI - MPPT_H + 70),
                   (_pvx - 20, EP_CTRL_FACE_YD, EP_H_HI - MPPT_H + 70)])
    ext_links.append(draw.ruby_pipe_run("PV- feed (MC4 -> MPPT -)", _pvm, 6, color="#9AA0A6"))
    # P-clips on the interior PV feeds (routed behind the EP panel) — ~350mm centres.
    for _lbl, _pp in (("PV+ feed", _pvp1), ("PV+ feed", _pvp2), ("PV- feed", _pvm)):
        ext_links.append(draw.ruby_clip_run(_lbl, _pp, spacing=350))
    # Blue Sea 5026: the block base + a standing row of 7 blade fuses (one per circuit A-G,
    # coloured to its circuit). Each blade's top is the cable origin for that circuit.
    p.append(draw.ruby_box("Fuse Block base (Blue Sea 5026)", _FBLK_X0, _FBLK_YD, _FBLK_Z0,
                         FUSEBLK_W, FUSEBLK_D, _FBASE_H, color="#2B2B30"))
    for i, c in enumerate(FUSE_ORDER):
        p.append(draw.ruby_box(f"Fuse {c} ({CCT_FUSE[c]} — {CCT[c][1]})",
                             _fuse_cx(i) - _FUSE_W / 2, _FUSE_YD, _FBLK_Z0 + _FBASE_H,
                             _FUSE_W, _FUSE_T, _FUSE_H, color=CCT[c][0]))
    # (Per-fuse circuit conductors are drawn by circuit_runs() — each circuit A-G leaves the TOP of its
    # own colored blade and routes to its load — so no separate pigtail stub is needed here.)
    # MASTER PUMP SWITCH — Cct-C single cutoff on the EP, at the Circuit-C fuse (red-lever disconnect,
    # mounted on the panel at Yd0). The switched Cct-C feed runs the ceiling trunk to the pump wireway.
    p.append(master_switch())
    p.append(draw.ruby_box("Busbar (+)", EP_X + 15, 30, ez + 170,
                         BUSBAR_L, BUSBAR_W, BUSBAR_H, color="#C0392B"))
    p.append(draw.ruby_box("Busbar (-)", EP_X + 15, 30, ez + 140,
                         BUSBAR_L, BUSBAR_W, BUSBAR_H, color="#2C2C2C"))
    p.append(draw.ruby_cylinder("Main Disconnect (m-Series)", EP_X + 55, _ACCESS_YF,
                              EP_DISC_Z, DISCONNECT_D / 2, DISCONNECT_H,   # SURFACE-mounted on the access panel, body on the front
                              color="#D43A2F", axis="y"))
    # Main disconnect → busbar(+) load link: the battery + feed lands on the disconnect LINE terminal
    # (battery()); it exits the LOAD terminal here to the (+) busbar. Both terminals are at the
    # disconnect REAR (Yd = EP_CTRL_FACE_YD) and the links run BEHIND the access panel.
    disc_x = EP_X + 55
    p.append(draw.ruby_pipe_run("Main feed (disconnect → busbar +)",
                              _dedup([(disc_x, _ACCESS_YF, EP_DISC_Z + 20),   # off the disconnect LOAD terminal (rear)
                                      (disc_x, 30, EP_DISC_Z + 20),           # back behind the panel to the busbar plane
                                      (disc_x, 30, ez + 170)]),                # straight up onto the (+) busbar at X1884 (busbar spans X1844-1964) — no −X traverse that fouls the fan-feed riser
                              11, color="#8B1A1A"))
    # MPPT charge-line fuse — 60A on the MPPT battery-output lead, in front of the busbars
    # (D2; protects the 6 AWG charge conductor the 200A main fuse is too large to cover).
    p.append(draw.ruby_box("Charge-line Fuse (60A, MPPT -> battery)",
                         EP_X + 15, 95, ez + 155, 45, 30, 45, color="#222222"))
    # Charge-line conductors so the 60A fuse isn't floating: MPPT battery output -> fuse -> (+) busbar.
    _clf_x = EP_X + 15 + 22                                        # charge-fuse center X
    p.append(draw.ruby_pipe_run("Charge line (MPPT -> charge fuse)",
                              _dedup([(_clf_x, 110, EP_H_HI - MPPT_H),       # off the MPPT battery-output (bottom)
                                      (_clf_x, 110, ez + 200)]),              # down into the charge-fuse TOP terminal
                              5, color="#8B1A1A"))
    p.append(draw.ruby_pipe_run("Charge line (charge fuse -> busbar +)",
                              _dedup([(_clf_x, 95, ez + 181),                # out the fuse BACK face, at the (+) busbar level (no fold back up through the fuse)
                                      (EP_X + 21, 95, ez + 181),             # −X clear of the fan-feed riser (X1868)
                                      (EP_X + 21, 40, ez + 181)]),            # straight back onto the (+) busbar (above the − busbar)
                              5, color="#8B1A1A"))
    # Interior E-stop — red mushroom on the panel, paralleled with the exterior one (D5). Relocated to
    # a CLEAR spot (left-center, in the gap between the contactor top ~Z714 and the inverter ~Z1180,
    # left of the wiring risers) so it isn't buried under the cables.
    ies_cx, ies_cz = EP_X + 270, EP_DISC_Z + 20
    # EP access/control panel: a SINGLE ply fascia spanning the two EP side lips, housed in a 9mm rebate
    # in each lip, at the E-stop height. The E-stop, master lever + disconnect handle poke through its
    # front; all are WIRED FROM THE REAR (behind the fascia) — controls separated from the distribution
    # wiring, which stays in the enclosure above.
    _acc_reb = 9
    _acc_l = _ply_x0 + 18 - _acc_reb                 # seat 9mm into the left side lip
    _acc_r = (_ply_r - 18) + _acc_reb                # seat 9mm into the right side lip
    p.append(draw.ruby_box("EP access panel (18mm ply, rebated to EP sides)",
                         _acc_l, _ACCESS_YB, _ACCESS_Z0, _acc_r - _acc_l,
                         _ACCESS_YF - _ACCESS_YB, _ACCESS_Z1 - _ACCESS_Z0, color=draw.C_PLY, alpha=0.3))   # transparent — see the wiring behind
    p.append(draw.ruby_cylinder("Interior E-stop collar (safety yellow)",
                              ies_cx, _ACCESS_YF, ies_cz, 30, 18, color="#F2C200", axis="y"))   # SURFACE-mounted base on the panel front
    p.append(draw.ruby_cylinder("Interior E-stop button (red mushroom)",
                              ies_cx, _ACCESS_YF + 18, ies_cz, 24, 26, color="#C42B1C", axis="y"))
    # E-stop trip wiring (D5): both E-stops sit in the battery-contactor coil loop. A control pair
    # runs from the contactor coil up to the interior E-stop; the two E-stops are then paralleled
    # (interior -> exterior via the external panel) so pressing EITHER drops the contactor.
    # In the skinny column the contactor sits at X1920-2040 (right of the transport anchor X1695-1895),
    # so the trip line runs straight up the column to the interior E-stop — no anchor dodge needed.
    _ctc_x, _ctc_z = EP_X + 10 + CONTACTOR_W / 2, EP_POST_Z + CONTACTOR_H    # contactor coil top (skinny column)
    _ext_x, _ext_z = PWR_PANEL_X + PWR_PANEL_W / 2, PWR_PANEL_Z + PWR_PANEL_H / 2  # exterior E-stop
    _est1 = _dedup([(_ctc_x, 45, _ctc_z), (_ctc_x, 45, _ctc_z + 20),   # straight UP off the contactor coil (no angled entry)
                    (_ctc_x, 10, _ctc_z + 20),                           # then −Yd (right-angle turn)
                    (ies_cx, 10, _ctc_z + 20), (ies_cx, 10, ies_cz),
                    (ies_cx, _ACCESS_YB, ies_cz)])               # land on the E-stop REAR terminal (behind the access panel)
    ext_links.append(draw.ruby_pipe_run("E-stop trip line (contactor coil -> interior E-stop)", _est1, 4, color="#586070"))
    _est2 = _dedup([(ies_cx, _ACCESS_YB, ies_cz), (ies_cx, 10, ies_cz),
                    (ies_cx, 10, _ext_z - 75),               # rise 25mm lower than the GFCI jog
                    (ies_cx, 5, _ext_z - 75),                # tuck to Yd5 (clears the green PV feed at Yd22 + the orange jog at Yd18)
                    (_ext_x, 5, _ext_z - 75),                # across at Yd5
                    (_ext_x, 5, _ext_z), (_ext_x, -WALL, _ext_z)])
    ext_links.append(draw.ruby_pipe_run("E-stop parallel link (interior -> exterior E-stop)", _est2, 4, color="#586070"))
    # P-clips on the interior E-stop feeds along the EP wall — ~350mm centres.
    for _lbl, _pp in (("E-stop trip line", _est1), ("E-stop link", _est2)):
        ext_links.append(draw.ruby_clip_run(_lbl, _pp, spacing=350))
    # ext_links = the two circuits OUT to the external panel (green PV + grey E-stop). links_only returns
    # JUST them (the overview's separate "EP Ext Wiring" component); external_links=False omits them
    # entirely (the water model); external_links=True folds them back inline (legacy default).
    if links_only:
        return '\n'.join(ext_links)
    if external_links:
        p.extend(ext_links)
    return '\n'.join(p)


def battery():
    """2x 100Ah packs RE-STACKED vertically in the skinny column (2nd ghosted) + contactor + MRBF
    above the stack. The + 2/0 cable rises left-of-centre to the main disconnect in the reach cluster
    (clear of the interior E-stop at the cluster's right end); the − cable runs up EP_RISE_X_M to the
    (−) busbar. Skinny-panel prototype — see SK_* above."""
    p = []
    for bz, nm, al in [(BA_H_LO, "Battery 1 (12V 100Ah LiFePO4)", 1.0),
                       (BA_STACK_Z2, "Battery 2 (optional 2nd pack, ghosted)", 0.28)]:
        p.append(draw.ruby_box(nm, EP_X, 0, bz, BA_W, BA_D, (BA_H_HI - BA_H_LO), color=draw.C_BATT, alpha=al))
    p.append(draw.ruby_box("Battery Contactor (ML-RBS)", EP_X + 10, 15, EP_POST_Z,
                         CONTACTOR_W, CONTACTOR_D, CONTACTOR_H, color="#C42B1C"))
    _mrbf_x = EP_X + CONTACTOR_W + 30
    p.append(draw.ruby_box("MRBF Main Fuse (on + post)", _mrbf_x, 20, EP_POST_Z,
                         MRBF_D, MRBF_D, MRBF_H, color="#222222"))
    # Battery + path INTO the MRBF (so it isn't a pipe-to-nowhere): battery + terminal -> contactor ->
    # MRBF; the red Battery+ cable below then runs MRBF -> main disconnect.
    p.append(draw.ruby_pipe_run("Battery + link (battery -> contactor)",
                              _dedup([(EP_X + 40, 45, BA_STACK_TOP),
                                      (EP_X + 40, 45, EP_POST_Z + 20)]), 11, color="#8B1A1A"))
    p.append(draw.ruby_pipe_run("Battery + link (contactor -> MRBF)",
                              _dedup([(EP_X + 10 + CONTACTOR_W, 40, EP_POST_Z + 20),
                                      (_mrbf_x + MRBF_D / 2, 40, EP_POST_Z + 20)]), 11, color="#8B1A1A"))
    disc_x, disc_z = EP_X + 55, EP_DISC_Z               # main disconnect centre (matches power_core cluster)
    bus_x = EP_X + 20
    # + leaves the MRBF, rises just BELOW the cluster row, then runs LEFT to the disconnect LINE terminal.
    # The disc moved to the cluster's LEFT end, so the riser stays left-of-centre — clear of the interior
    # E-stop at the cluster's RIGHT end (X+270) that the old right-lane route used to cover.
    p.append(draw.ruby_pipe_run("Battery + cable (2/0 AWG, MRBF → main disconnect)",
                              _dedup([(_mrbf_x + MRBF_D / 2, 45, EP_POST_Z + MRBF_H),
                                      (_mrbf_x + MRBF_D / 2, 45, disc_z - 35),         # up at Yd45 (clears the orange AC line at Yd15)
                                      (_mrbf_x + MRBF_D / 2, 35, disc_z - 35),         # drop to Yd35 for the −X run
                                      (disc_x, 35, disc_z - 35),                       # −X to the disc (clears the battery − riser at Yd49-71)
                                      (disc_x, EP_CTRL_FACE_YD, disc_z - 20)]),   # lands on the disconnect LINE terminal (rear, behind the panel)
                              11, color="#8B1A1A"))
    p.append(draw.ruby_pipe_run("Battery − cable (2/0 AWG)",
                              _dedup([(EP_X + 40, 60, BA_STACK_TOP - 55),   # DOWN into the battery − terminal (connects; was starting on the top surface, reading as open-ended)
                                      (EP_X + 40, 60, BA_STACK_TOP),
                                      (EP_RISE_X_M, 60, BA_STACK_TOP),
                                      (EP_RISE_X_M, 60, EP_H_LO + 150),
                                      (bus_x + 110, 60, EP_H_LO + 150),    # land near the (−) busbar +X END — SHORT horizontal, clear of the fan-feed + Cct-C risers it used to span
                                      (bus_x + 110, 38, EP_H_LO + 150)]),   # jog FORWARD onto the (−) busbar (Yd30-50)
                              11, color="#202020"))
    return '\n'.join(p)


def external_estop():
    """The exterior E-stop (safety-yellow collar + red mushroom button) on the panel face.
    Broken out so the construction sequence can reveal it WITH the interior EP rather than
    with the empty panel shell."""
    face_y = -WALL - 25
    es_cx = PWR_PANEL_X + PWR_PANEL_W / 2
    es_cz = PWR_PANEL_Z + PWR_PANEL_H / 2
    return '\n'.join([
        draw.ruby_cylinder("E-stop collar (safety yellow)", es_cx, face_y - 12,
                         es_cz, 35, 12, color="#F2C200", axis="y"),
        draw.ruby_cylinder("E-stop button (red mushroom)", es_cx, face_y - 40,
                         es_cz, 26, 28, color="#C42B1C", axis="y"),
    ])


def pv_disconnect():
    """PV array disconnect — red DC load-break isolator on the PV path (array -> MPPT), on
    the skinny column at OPERATOR REACH (PV_DISC_Z), with a red switch LEVER on its face so
    it reads as a switch (NEC 690.13). Broken out so the construction model reveals it with
    the interior EP rather than with the empty panel shell."""
    return '\n'.join([
        draw.ruby_box("PV Array Disconnect (load-break isolator)",
                    PV_DISC_X, EP_CTRL_FACE_YD, PV_DISC_Z, 70, 45, 70, color="#D43A2F"),   # SURFACE-mounted on the access panel
        draw.ruby_box("PV disconnect lever (red switch)", PV_DISC_X + 28, EP_CTRL_FACE_YD + 45, PV_DISC_Z + 20,
                    14, 40, 14, color="#C0202A"),
    ])


def external_panel(include_estop=True, include_disconnect=True):
    """Fabricated wall-penetration box (exterior flange front face + shroud open to the
    interior) + MC4 PV bulkheads, NEMA weatherproof shore inlet, WR duplex cooler outlet
    (Circuit E) under an in-use cover, the exterior E-stop, and the PV disconnect.
    include_estop / include_disconnect = False omit those devices (the construction model
    reveals them a step later, with the interior EP)."""
    p = []
    face_y = -WALL - 25                       # exterior surface of the box front face (flange)
    # ── Fabricated penetration box: front-face flange (exterior, components mount to it)
    #    + a shroud OPEN to the interior (4 side walls, no back) so it is wired from inside.
    p.append(draw.ruby_box("EP box front face (flange)", PWR_PANEL_X, face_y,
                         PWR_PANEL_Z, PWR_PANEL_W, PWR_PANEL_D, PWR_PANEL_H,
                         color=draw.C_STEEL))
    _cx0 = PWR_PANEL_X + (PWR_PANEL_W - PWR_PANEL_CUTOUT_W) / 2     # wall-opening corner
    _cz0 = PWR_PANEL_Z + (PWR_PANEL_H - PWR_PANEL_CUTOUT_H) / 2
    _sy0 = face_y + PWR_PANEL_D               # shroud starts behind the flange
    _t   = PWR_PANEL_SHROUD_T
    p.append(draw.ruby_box("EP box shroud (left)", _cx0 - _t, _sy0, _cz0 - _t,
                         _t, PWR_PANEL_BOX_D, PWR_PANEL_CUTOUT_H + 2 * _t, color=draw.C_STEEL))
    p.append(draw.ruby_box("EP box shroud (right)", _cx0 + PWR_PANEL_CUTOUT_W, _sy0, _cz0 - _t,
                         _t, PWR_PANEL_BOX_D, PWR_PANEL_CUTOUT_H + 2 * _t, color=draw.C_STEEL))
    p.append(draw.ruby_box("EP box shroud (bottom)", _cx0 - _t, _sy0, _cz0 - _t,
                         PWR_PANEL_CUTOUT_W + 2 * _t, PWR_PANEL_BOX_D, _t, color=draw.C_STEEL))
    p.append(draw.ruby_box("EP box shroud (top)", _cx0 - _t, _sy0, _cz0 + PWR_PANEL_CUTOUT_H,
                         PWR_PANEL_CUTOUT_W + 2 * _t, PWR_PANEL_BOX_D, _t, color=draw.C_STEEL))

    def px(uf): return PWR_PANEL_X + uf * PWR_PANEL_W
    def pz(vf): return PWR_PANEL_Z + vf * PWR_PANEL_H

    # MC4 PV bulkheads — 3 pairs (+ green, − gray), bare (no cover). Drawn on BOTH faces: the exterior
    # stubs mate the array; the INTERIOR stubs carry the + / − pigtails that bundle to the PV feed.
    # The two collector buses sit OUTBOARD of their own stub columns (+ bus left, − bus right) on
    # separate Yd lanes (MC4_PLUS_*/MC4_MINUS_*), so green and grey never crowd at the bottom pair.
    for i, vf in enumerate(MC4_PAIR_VF):
        p.append(draw.ruby_cylinder(f"MC4 PV{i + 1} (+)", px(0.192), face_y - 20, pz(vf),
                                  8, 20, color="#2D7A2D", axis="y"))
        p.append(draw.ruby_cylinder(f"MC4 PV{i + 1} (-)", px(0.275), face_y - 20, pz(vf),
                                  8, 20, color="#9AA0A6", axis="y"))
        # interior stubs (inner face) + pigtails bending OUTWARD to each string's own-column bus
        p.append(draw.ruby_cylinder(f"MC4 PV{i + 1} (+) inner", px(0.192), 0, pz(vf), 8, 18, color="#2D7A2D", axis="y"))
        p.append(draw.ruby_cylinder(f"MC4 PV{i + 1} (-) inner", px(0.275), 0, pz(vf), 8, 18, color="#9AA0A6", axis="y"))
        p.append(draw.ruby_pipe_run(f"PV+ pigtail {i + 1} (MC4 -> + bus)",
                                  _dedup([(px(0.192), 18, pz(vf)), (px(0.192), MC4_PLUS_Y, pz(vf)), (MC4_PLUS_X, MC4_PLUS_Y, pz(vf))]),
                                  CCT_WIRE_R, color="#2D7A2D"))
        p.append(draw.ruby_pipe_run(f"PV- pigtail {i + 1} (MC4 -> - bus)",
                                  _dedup([(px(0.275), 18, pz(vf)), (px(0.275), MC4_MINUS_Y, pz(vf)), (MC4_MINUS_X, MC4_MINUS_Y, pz(vf))]),
                                  CCT_WIRE_R, color="#9AA0A6"))
    # + / − bus bars collecting the 3 strings; the PV +/− feeds take off from the bottom of each bus
    p.append(draw.ruby_pipe_run("PV+ bus (3 strings)", _dedup([(MC4_PLUS_X, MC4_PLUS_Y, pz(MC4_PAIR_VF[0])), (MC4_PLUS_X, MC4_PLUS_Y, pz(MC4_PAIR_VF[-1]))]), CCT_WIRE_R, color="#2D7A2D"))
    p.append(draw.ruby_pipe_run("PV- bus (3 strings)", _dedup([(MC4_MINUS_X, MC4_MINUS_Y, pz(MC4_PAIR_VF[0])), (MC4_MINUS_X, MC4_MINUS_Y, pz(MC4_PAIR_VF[-1]))]), CCT_WIRE_R, color="#9AA0A6"))
    # NEMA 5-15 weatherproof shore inlet + its translucent flip-cover, mounted proud
    p.append(draw.ruby_box("NEMA 5-15 shore inlet", px(0.742) - 30, face_y - 30,
                         pz(0.878) - 22, 60, 30, 45, color="#FFF0CC"))
    p.append(draw.ruby_box("NEMA inlet weatherproof cover", px(0.742) - 36, face_y - 42,
                         pz(0.878) - 28, 72, 12, 57, color="#D6E6F5", alpha=0.5))
    # Cooler AC feed — Leviton W5320 WR duplex under a 5981-UCL bubble in-use cover
    p.append(draw.ruby_box("WR duplex outlet (Cct E cooler)", px(0.767) - 23, face_y - 22,
                         pz(_OUTLET_VF) - 30, 46, 22, 60, color="#FFF0CC"))
    p.append(draw.ruby_box("WR duplex in-use cover", px(0.767) - 29, face_y - 36,
                         pz(_OUTLET_VF) - 36, 58, 14, 72, color="#D6E6F5", alpha=0.5))
    # E-stop on the exterior face.
    if include_estop:
        p.append(external_estop())
    # PV array disconnect on the skinny column.
    if include_disconnect:
        p.append(pv_disconnect())

    # Evap cooler BODY + its Cct-E 120V cooler cord (GFCI -> cooler) — SINGLE OWNER (cooler()),
    # also composed by the overview's evap_cooler(). The DC feed + inverter->GFCI AC line are
    # their own components; this closes the Cct E chain: GFCI outlet -> cord -> cooler.
    p.append(cooler())
    return '\n'.join(p)


def cooler():
    """SINGLE OWNER of the external evap-cooler BODY + its Cct-E 120V cooler cord (panel GFCI ->
    cooler). external_panel() and the overview's evap_cooler() both call this, so neither can
    drift — the overview had a ported copy whose GFCI height had gone stale (0.325 vs _OUTLET_VF),
    so its cord didn't reach the real outlet. The Ø200 supply duct stays with the overview (no
    ventilation sub-model owns it)."""
    cw, cd, ch = EVAP_W, EVAP_D, EVAP_H
    cx = EVAP_DUCT_X - cw / 2
    cyd = -WALL - cd - 100         # ground stand-off off the pinhole wall
    face_y = -WALL - 25            # exterior face of the EP box
    gfci_x = PWR_PANEL_X + 0.767 * PWR_PANEL_W
    gfci_z = PWR_PANEL_Z + _OUTLET_VF * PWR_PANEL_H
    inx = cx + cw - 80                    # cooler-top inlet
    p = [draw.ruby_box("Evap Cooler (Hessaire MC18M, external)", cx, cyd, 0,
                       cw, cd, ch, color=draw.C_EVAP)]
    p.append(draw.ruby_coil_cord("Cct E cooler cord (panel GFCI -> cooler, flexible)",
                               [(gfci_x, face_y - 10, gfci_z),
                                (inx, cyd + cd / 2, ch - 70)],
                               r=5, color="#E8884A"))
    return '\n'.join(p)


def inverter_box():
    """The Cct-E 12->120V inverter BODY on the EP ply. SINGLE OWNER — inverter() + the overview
    model both call this, so the box can't drift between models."""
    return draw.ruby_box("Cct E Inverter (12->120V AC)", INVERTER_X, 0, INVERTER_Z,
                       INVERTER_W, INVERTER_D, INVERTER_H, color="#404848")


def inverter():
    """Circuit-E 12->120V inverter, mounted on the EP plywood panel (lower section, below
    the main gear), + its 120V AC output line across to the external panel's GFCI outlet."""
    p = [inverter_box()]
    gfci_x = PWR_PANEL_X + 0.767 * PWR_PANEL_W
    gfci_z = PWR_PANEL_Z + _OUTLET_VF * PWR_PANEL_H
    _ac_lane_x = EP_X + 249                    # clear riser slot between the PV riser (X≤2067) and the interior E-stop (X2099)
    _ac_top_z = EP_H_HI + 40                   # above the EP column top edge + clear of the cross-member top (penetrates the TOP, not the side)
    _inv_top = INVERTER_Z + INVERTER_H
    _ac_pts = _dedup([(INVERTER_X + INVERTER_W / 2, 15, _inv_top),   # off the inverter at Yd15 (clear of the battery+ cable at Yd45)
                      (_ac_lane_x, 15, _inv_top),                    # +X to the riser slot
                      (_ac_lane_x, 15, EP_H_LO + 150),               # up at Yd15
                      (_ac_lane_x, 45, EP_H_LO + 150),               # shift to Yd45 (X clears the E-stop at X2099 by 21mm)
                      (_ac_lane_x, 45, _ac_top_z),                   # up and out the EP top
                      (_ac_lane_x, 85, _ac_top_z),                   # shift to Yd85 (clear of EVERY EP-top riser at Yd≤65: fan-feed, Cct-C, PV)
                      (gfci_x, 85, _ac_top_z),                       # across the top (over the cross member) to the GFCI X
                      (gfci_x, 85, gfci_z),                          # up to the GFCI height (Yd85 clears the green MC4 feed at Yd22)
                      (gfci_x, 18, gfci_z)])                         # jog to the GFCI terminal (above the green)
    p.append(draw.ruby_pipe_run("Cct E AC line (inverter -> panel GFCI)", _ac_pts, 7, color="#E8884A"))
    # P-clips along the orange AC line, incl. where it lands at the GFCI inside the external EP.
    p.append(draw.ruby_clip_run("Cct E AC line", _ac_pts, spacing=350))
    return '\n'.join(p)


def light_fixtures():
    """Physical lighting hardware — white LED strips (Cct G), red safelight strips (Cct D), and the two
    ceiling pull-cord switches (with beaded pull cords). SINGLE OWNER — electrical + overview both draw
    this (from the shared LED_PANELS/SAFE_XS/PULL_SW_* data), so the fixtures can't drift. The circuit
    CONDUCTORS to them are _multi_run('G'/'D')."""
    cz = ov.C_HGT
    p = []
    for x0, y0, wx, wyd in LED_PANELS:
        p.append(draw.ruby_box("White LED Strip (Cct G)", x0, y0, cz - 25, wx, wyd, 18,
                             color=draw.C_LED_W, alpha=0.4))
    for sx in SAFE_XS:
        p.append(draw.ruby_box("Safelight Strip (Cct D)", sx, 100, cz - 25, 40, 1667, 18,
                             color=draw.C_SAFE, alpha=0.4))
    for swx in PULL_SW_X:
        p.append(draw.ruby_box("Pull Switch (ceiling)", swx, PULL_SW_YD, cz - 40, 40, 40, 40, color=draw.C_SWITCH))
        cordx, cordy = swx + 20, PULL_SW_YD + 20
        z0, z1 = PULL_CORD_BOTTOM_Z, cz - 40             # bottom clears the deployed chem shelf below
        nb = max(8, int((z1 - z0) / 20)); bh = (z1 - z0) / nb
        for k in range(nb):
            rr = 3.5 if k % 2 == 0 else 2.0
            p.append(draw.ruby_cylinder("Pull Cord", cordx, cordy, z0 + k * bh, rr, bh, color=draw.C_CORD, axis="z", n=8))
        p.append(draw.ruby_cylinder("Pull Cord Knob", cordx, cordy, z0 - 16, 6, 16, color=draw.C_CORD, axis="z", n=10))
    return '\n'.join(p)


# _pump_circuit() RETIRED (Phase: circuit_runs reconciliation) — the Cct-C pump distribution
# is single-sourced from pw.panel_power() (the water model owns the corridor pump panel);
# circuit_runs() now draws cct_c_feed() + pw.panel_power(include_switch=False).


def cct_c_feed():
    """Cct C feed: fuse C -> master switch. The X-traverse runs fully at the switch-rear Yd (behind the
    Cct-E feed + battery cables), so it clears the cluster at the disconnect level. SINGLE OWNER —
    _pump_circuit() (electrical) and the overview both call this, so the fuse-C→switch leg can't drift
    between models. (The switched feed onward to the pumps is _pump_circuit() / pw.panel_power.)"""
    fcx, fcy, fcz = FUSE_POS["C"]
    msx, msy, msz = MASTER_SW_POS
    return draw.ruby_pipe_run("Cct C feed (fuse C -> master switch)",
                            _dedup([(fcx, fcy, fcz), (fcx, fcy, msz),
                                    (fcx, msy, msz), (msx, msy, msz)]), 6, color=CCT["C"][0])




def cable_trunking():
    """The 40x25 PVC ceiling trunk bundling every circuit. SINGLE OWNER — circuit_runs() + the
    overview model both call this. Spans ONLY the circuit range (door-end first tap → Fan A) so
    there is no dead-end grey stub past the last drop (the overview used to draw it full-length)."""
    cxs = [LOADS[c][0] for c in ("A", "B", "C", "E")] + \
          [e[0] for e in LED_ENDS + SAFE_ENDS] + [_FBLK_X0, _FBLK_X0 + FUSEBLK_W]
    tx0, tx1 = min(cxs) - 40, max(cxs) + 40
    return draw.ruby_box("Cable Trunking (40x25 PVC)", tx0, 0, ov.C_HGT - 25, tx1 - tx0, 40,
                       25, color=draw.C_TRUNK)


def conduit_clips():
    """FIRST PASS — P-clip / saddle supports for the electrical conduits + cables, mirroring the
    plumbing-panel pipe-support-clips (cushioned straps, #55575e). Trunk saddle straps fix the PVC
    ceiling trunk to the pinhole wall at ~500mm centres; drop P-clips carry the long vertical
    wall-drops (the Cct-B feed down to the Fan-B box) back to the wall at ~450mm centres. Review
    target: spacing + which runs to add next (EP backboard cables, battery cable)."""
    C_CLIP = "#55575e"
    p = []
    cxs = [LOADS[c][0] for c in ("A", "B", "C", "E")] + \
          [e[0] for e in LED_ENDS + SAFE_ENDS] + [_FBLK_X0, _FBLK_X0 + FUSEBLK_W]
    tx0, tx1 = min(cxs) - 40, max(cxs) + 40
    # Ceiling cable-trunk saddle straps — ~500mm centres, wrapping the 40x25 PVC trunk to the wall.
    n = max(2, round((tx1 - tx0) / 500.0) + 1)
    for i in range(n):
        sx = tx0 + (tx1 - tx0) * i / (n - 1)
        p.append(draw.ruby_box("Trunk saddle clip", sx - 6, -4, ov.C_HGT - 28,
                               12, 48, 31, color=C_CLIP))
    # (The circuit DROP clips — Fan A far-end cross/drop, Fan B wall drop — are emitted by _run()
    # itself, on the run's own point-list, so they can't drift off the conductor.)
    return '\n'.join(p)


def cct_e_feed():
    """Cct E DC feed: fuse E -> inverter DC input. The inverter sits right BELOW the fuse block, so
    this is a short local DOWN-feed — NOT the ceiling _run route (which looped back down through the
    busbar/disconnect cluster and fouled the Main feed + Battery+ cable). SINGLE OWNER — circuit_runs()
    and the overview's evap section both call this, so the Cct-E DC leg can't drift between models."""
    fex, fey, fez = FUSE_POS["E"]
    invx = INVERTER_X + INVERTER_W / 2
    return draw.ruby_pipe_run("Cct E feed (fuse E -> inverter)",
                            _dedup([(fex, fey, fez), (fex, 55, fez),
                                    (fex, 55, INVERTER_Z + INVERTER_H + 10),
                                    (invx, 55, INVERTER_Z + INVERTER_H + 10),
                                    (invx, 55, INVERTER_Z + INVERTER_H)]), 5, color=CCT["E"][0])


def solar_array():
    """3x 200W panels on a 30deg ground tilt frame, exterior of the pinhole wall,
    door-end so the right edge clears the pinhole sightline; + PV run to the panel.
    Shared with the focused electrical model (generate_electrical_model.py)."""
    p = []
    th = math.radians(SOLAR_TILT_DEG)
    pitch = SOLAR_PANEL_W + SOLAR_GAP
    for i in range(SOLAR_N):
        x = SOLAR_ARRAY_X + i * pitch
        p.append(draw.tilted_slab(f"Solar Panel {i + 1} (200W)", x, SOLAR_ARRAY_YD,
                             SOLAR_ARRAY_Z + 120, SOLAR_PANEL_W, SOLAR_PANEL_L,
                             SOLAR_PANEL_T, SOLAR_TILT_DEG, "#1B3A6B", alpha=0.3))
    span = (SOLAR_N - 1) * pitch + SOLAR_PANEL_W
    back_yd = SOLAR_ARRAY_YD - SOLAR_PANEL_L * math.cos(th)
    top_z = SOLAR_ARRAY_Z + 120 + SOLAR_PANEL_L * math.sin(th)
    p.append(draw.ruby_box("Tilt Frame front rail", SOLAR_ARRAY_X, SOLAR_ARRAY_YD - 20,
                      SOLAR_ARRAY_Z, span, 40, 120, color=draw.C_STEEL))
    p.append(draw.ruby_box("Tilt Frame back rail", SOLAR_ARRAY_X, back_yd - 20,
                      SOLAR_ARRAY_Z, span, 40, 60, color=draw.C_STEEL))
    for x in (SOLAR_ARRAY_X, SOLAR_ARRAY_X + span - 40):
        p.append(draw.ruby_box("Tilt Frame back leg", x, back_yd - 20, SOLAR_ARRAY_Z,
                          40, 40, top_z - SOLAR_ARRAY_Z, color=draw.C_STEEL))
    # PV run: array junction -> up to the external power panel MC4 bulkheads.
    # A PV feed is a +/- PAIR, drawn as a BONDED ("siamese") pair of curly coil cords: the two
    # conductors run together (coiled, ~16mm apart with a tightened curl so they read as one
    # twisted pair, not a tangle) for the whole length, and FAN OUT only at the ends — straight
    # stubs at the array terminals and to the panel's two MC4 columns (+ at _px 0.192, - at 0.275).
    # The short end-legs fall under ruby_coil_cord's straight-stub threshold, so the fans render as
    # clean straight leads while the long middle legs coil. Coil cords mark the SOFT connector (vs
    # the rigid orthogonal conduit); the bonded run drapes DIAGONALLY up to the panel so it stays
    # right of + clear of the evap cooler (X720-1280) — an angle a rigid conduit can't take.
    jx = SOLAR_ARRAY_X + span / 2
    mc4_z = MC4_BOT_Z                               # land on the BOTTOM MC4 pair (PV1) — single-sourced
    pmid = PWR_PANEL_X + 0.2335 * PWR_PANEL_W          # midpoint of the two MC4 columns
    PAIR, FAN = 8, 18                                  # bonded half-spacing / array-end fan-out
    for s, panel_uf, col, sym in ((-1, 0.192, "#2D7A2D", "+"),     # (+) -> left MC4 column, green
                                  (+1, 0.275, "#1A1A1A", "-")):    # (-) -> right MC4 column, black
        p.append(draw.ruby_coil_cord(f"PV cord ({sym}) (array -> panel MC4, bonded pair)",
                                [(jx + s * FAN,  SOLAR_ARRAY_YD - 20, SOLAR_ARRAY_Z + 60),  # array terminal (fanned)
                                 (jx + s * PAIR, SOLAR_ARRAY_YD - 50, SOLAR_ARRAY_Z + 60),  # converge into the pair
                                 (jx + s * PAIR, -WALL_T - 30,        SOLAR_ARRAY_Z + 60),  # bonded run toward panel
                                 (pmid + s * PAIR, -WALL_T - 30,      mc4_z),               # bonded, diagonal up
                                 (PWR_PANEL_X + panel_uf * PWR_PANEL_W, -WALL_T - 30, mc4_z)],  # split to its MC4 column
                                r=5, coil_r=13, color=col))
    return '\n'.join(p)


def circuit_runs():
    """Ceiling cable-trunking spine + the 7 color-coded circuits A-G to their loads.
    Single-load circuits (A,B,C,E,F) trace fuse-block→load; the lighting circuits
    (G white LED, D safelight) fan out to ALL three of their ceiling fixtures."""
    p = [cable_trunking()]
    for cct in ("A", "B"):
        p.append(_run(cct, LOADS[cct]))
    p.append(cct_e_feed())                 # Cct E: short fuse-E → inverter DC feed (local, not a ceiling loop)
    # Cct C: fuse → master switch (shared leg), then the switched feed to the CORRIDOR PUMP PANEL is
    # single-sourced from the water model (pw.panel_power) — the SAME pump distribution the overview +
    # construction draw, so electrical can't drift to a stale pump layout (retired em._pump_circuit).
    p.append(cct_c_feed())
    import generate_pinhole_water_panel as pw   # late: pw owns the Cct-C pump distribution (water panel)
    p.append(pw.panel_power(include_switch=False))
    p.append(_multi_run("G", LED_ENDS))    # 3× white LED (incl. rotated IBC-end panel)
    p.append(_multi_run("D", SAFE_ENDS))   # 3× safelight
    p.append(fan_b_flex())
    return '\n'.join(p)


def fan_b_flex():
    """SINGLE OWNER of the Fan B flexible connector — the SOFT jumper (curly coil cord) from the
    fixed wall box out to Fan B on the swinging panel, unplugged before the panel swings. em owns
    the Cct-B conductor; the overview + construction models call THIS rather than keep a copy, so
    the flex can't drift from the box (`_FANB_BOX_X`) the way it did (overview at 420, em at 300)."""
    return draw.ruby_coil_cord("Fan B flex connector (box -> fan, Cct B)",
                               [(_FANB_BOX_X, 55, FAN_B_H), (60, FAN_B_YD, FAN_B_H)],
                               r=5, color=CCT["B"][0])


# ── Ventilation fans + light-safe baffle ducts (Phase 1: owner = electrical; Cct A/B) ──
def fans(which="both"):
    """Cross-ventilation fans + light-safe baffle ducts on OPPOSITE end walls,
    diagonal low-in / high-out:
      Fan A (exhaust) — sealed/IBC end wall (X=C_LEN), in the plumbing corridor
        directly BELOW the X1 fill port (Yd=1181, Z=2000) — the only full-height
        clear channel past the 1000L direct-stack.
      Fan B (intake)  — cargo-door panel (X=0, left), low (Z=600).

    Each fan sits at the INTERIOR mouth of a box-section baffle duct bolted to
    the wall interior: DUCT_DEPTH (300mm, along the fan axis) x DUCT_W (200mm,
    Yd) x DUCT_HEIGHT (200mm, Z), translucent galvanized steel. Inside, two
    150x150mm flat baffle plates are offset top/bottom at 1/3 and 2/3 depth to
    break the line of sight (light-safe S-path) while passing full airflow.
    """
    # Fan A: far end wall (X=C_LEN, exterior on +X); duct projects -X into container.
    # Fan B: cargo-door panel (X=0, exterior on -X); duct projects +X into container.
    # `which`: "both" (default), "A", or "B" — the construction model installs Fan A early
    # (before the far IBC column buries it) and Fan B later.
    out = []
    if which in ("both", "A"):
        out += fan_duct("Fan A (exhaust)", C_LEN, +1, FAN_A_YD, FAN_A_H)
    if which in ("both", "B"):
        out += fan_duct("Fan B (intake)", 0, -1, FAN_B_YD, FAN_B_H)
    return '\n'.join(out)


def fan_duct(tag, wall_x, ext, yc, zc):
    """One axial panel fan + light-safe baffle duct opening into the container.

    `ext` = +1 if the exterior is on +X, -1 on -X. The duct projects from the
    wall interior face into the container; the fan sits at the interior mouth.
    Returns a list of ruby strings. Shared single source of truth for the
    Overview fans() and the focused Light-Trap model (Fan B on the hinge panel).
    """
    r, bd = FAN_DIAM / 2, FAN_BODY_D          # Ø150, 50mm fan body
    dd, dh = DUCT_DEPTH, DUCT_HEIGHT          # 300 deep (axis), 200 tall (Z)
    dw = DUCT_HEIGHT                          # 200 wide (Yd) — square section
    bf, bft = 125, 8                          # baffle plates: FULL height (Z, welded top +
                                              # bottom) × 125 wide (Yd) — leaves a 75mm airflow
                                              # gap on one SIDE; the two plates take opposite
                                              # sides so air winds left↔right (horizontal S-path)
                                              # while the overlap blocks the line of sight
    flo, flt = 30, 5                          # flange overhang past the duct, + plate thickness
    gld, glh = 40, int(dh * 0.65)             # louvre grille depth + height

    if True:
        mouth_x = wall_x - ext * dd
        x0 = min(wall_x, mouth_x)
        out = [draw.ruby_box(f"{tag} baffle duct", x0, yc - dw / 2, zc - dh / 2,
                        dd, dw, dh, color=draw.C_DUCT, alpha=0.5)]
        # baffle plates — full height (welded top + bottom), offset left/right in Yd,
        # leaving a 75mm airflow gap on one side each (horizontal S-path)
        out.append(draw.ruby_box(f"{tag} baffle plate 1", x0 + dd / 3 - bft / 2,
                            yc - dw / 2, zc - dh / 2, bft, bf, dh, color=draw.C_FAN))
        out.append(draw.ruby_box(f"{tag} baffle plate 2", x0 + 2 * dd / 3 - bft / 2,
                            yc + dw / 2 - bf, zc - dh / 2, bft, bf, dh, color=draw.C_FAN))
        # ── axial panel fan at the interior mouth (matches 2D Sheet 2):
        #    square housing frame around the Ø150 bore + motor hub + 4-blade
        #    impeller, body set inside the duct ──
        fan_x = mouth_x if ext > 0 else mouth_x - bd   # interior face of fan body
        fr_y0, fr_y1 = yc - dw / 2, yc + dw / 2
        fr_z0, fr_z1 = zc - dh / 2, zc + dh / 2
        out.append(draw.ruby_box(f"{tag} fan frame top", fan_x, fr_y0, zc + r,
                            bd, dw, fr_z1 - (zc + r), color=draw.C_FAN))
        out.append(draw.ruby_box(f"{tag} fan frame bottom", fan_x, fr_y0, fr_z0,
                            bd, dw, (zc - r) - fr_z0, color=draw.C_FAN))
        out.append(draw.ruby_box(f"{tag} fan frame left", fan_x, fr_y0, zc - r,
                            bd, (yc - r) - fr_y0, 2 * r, color=draw.C_FAN))
        out.append(draw.ruby_box(f"{tag} fan frame right", fan_x, yc + r, zc - r,
                            bd, fr_y1 - (yc + r), 2 * r, color=draw.C_FAN))
        hub_r = r * 0.26
        out.append(draw.ruby_cylinder(f"{tag} fan hub", fan_x, yc, zc, hub_r, bd,
                                 color=draw.C_STEEL, axis="x"))
        bt, bw = 6, 30                                 # impeller blade thickness/width
        bx, bl = fan_x + bd * 0.45, r * 0.88 - hub_r   # blade plane + length
        out.append(draw.ruby_box(f"{tag} fan blade up", bx, yc - bw / 2, zc + hub_r,
                            bt, bw, bl, color=draw.C_ALUM))
        out.append(draw.ruby_box(f"{tag} fan blade down", bx, yc - bw / 2,
                            zc - hub_r - bl, bt, bw, bl, color=draw.C_ALUM))
        out.append(draw.ruby_box(f"{tag} fan blade left", bx, yc - hub_r - bl,
                            zc - bw / 2, bt, bl, bw, color=draw.C_ALUM))
        out.append(draw.ruby_box(f"{tag} fan blade right", bx, yc + hub_r,
                            zc - bw / 2, bt, bl, bw, color=draw.C_ALUM))
        # ── wall mounting flange: 5mm plate on the interior wall face, overhanging
        #    the duct opening, with 4 M10 bolts into the wall ──
        out.append(draw.ruby_box(f"{tag} wall flange",
                            wall_x - (flt if ext > 0 else 0), yc - dw / 2 - flo,
                            zc - dh / 2 - flo, flt, dw + 2 * flo, dh + 2 * flo,
                            color=draw.C_STEEL))
        for fy in (yc - dw / 2 - flo / 2, yc + dw / 2 + flo / 2):
            for fz in (zc - dh / 2 - flo / 2, zc + dh / 2 + flo / 2):
                out.append(draw.ruby_bolt(f"{tag} flange bolt M10",
                            wall_x - (flt + 8) / 2, fy, fz, flt + 8, radius=5,
                            axis="x", color="#3A3A42", head="base", nut="far"))
        # ── weatherproof louvre grille on the exterior wall face (slatted) ──
        gx0 = wall_x if ext > 0 else wall_x - gld
        out.append(draw.ruby_box(f"{tag} louvre grille", gx0, yc - dw / 2,
                            zc - glh / 2, gld, dw, glh, color=draw.C_DUCT, alpha=0.55))
        for s in range(5):
            sz = zc - glh / 2 + (s + 0.5) * glh / 5
            out.append(draw.ruby_box(f"{tag} louvre slat", gx0 + 2, yc - dw / 2 + 4,
                                sz - 1.5, gld - 4, dw - 8, 3, color=draw.C_STEEL))
        return out


def generate_ruby():
    import generate_lighttrap_model as lt   # transport-stay wall anchors (the transport "locks")
    comps = [
        draw.component("Container (ghost)", "Context", context()),
        draw.component("Transport Locks (context)", "Context", lt.wall_anchors()),
        draw.component("Chem Prep Shelf (context)", "Context", ov.shelf()),
        draw.component("Solar Array", "Solar Array", solar_array()),
        draw.component("Power Core", "Power Core", power_core()),
        draw.component("Battery Bank", "Battery", battery()),
        draw.component("External Power Panel", "External Panel", external_panel()),
        draw.component("Circuit-E Inverter", "Inverter", inverter()),
        draw.component("Circuit Runs", "Circuit Runs", circuit_runs()),
        draw.component("Conduit Clips", "Clips", conduit_clips()),
        draw.component("Lighting Fixtures", "Lighting", light_fixtures()),
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
        '"%s" => [%s, %s, %s, %s]' % (n, draw.mm(x), draw.mm(y), draw.mm(z), draw.mm(d))
        for n, (x, y, z, d) in zoom.items()) + '}'

    sf_meta = draw.sketchfab_meta_ruby(
        "TBS-001 Electrical Model",
        "There are a number of discrete systems, color-coded in the diagram below. This view is "
        "shown from the optical axis, looking through the container wall. Each of these sub-systems, "
        "has a detailed breakdown of construction, schematic and other diagrams to show how each "
        "system it built, installed, used and maintained. The 3d model below provides a simply way "
        "to view the whole system.",
        draw.model_uid("electrical"), "sketchup")

    return f'''# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
# Generated from src/models/ — do not edit this .rb directly.
model = Sketchup.active_model
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

{draw.license_note()}

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
