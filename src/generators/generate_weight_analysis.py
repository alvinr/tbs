#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_weight_analysis.py — Weight distribution analysis for TBS-001.

Computes total weight and center-of-gravity position for four operational
states (Dry, Camera Ready, Materials Exhausted, Loaded Transport). Generates
five diagram sheets showing component positions and weight distribution.

Outputs
-------
diagrams/weight-analysis-sheet1.png  — Summary comparison (4 states)
diagrams/weight-analysis-sheet2.png  — Dry, configured for transport
diagrams/weight-analysis-sheet3.png  — Camera Ready state distribution
diagrams/weight-analysis-sheet4.png  — Materials Exhausted state distribution
diagrams/weight-analysis-sheet5.png  — Loaded Transport (full Blue IBCs)
"""

import os
from dataclasses import dataclass, field

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
import numpy as np

from tbs_drawing import leader
from tbs_constants import (
    C_LEN, C_WID, C_HGT,
    FP_X_L, FP_X_R, FP_W, FP_Y, FP_H,
    FP_ANGLE_LEG, FP_ANGLE_T, CLAMP_N_TOTAL,
    PH_X, PH_H,
    RAIL_X_L, RAIL_X_R, RAIL_SPAN, RAIL_LEN,
    IBC_COL_X, IBC_W, IBC_D, IBC_H_600, IBC_H_STK,
    IBC_H_1000, IBC_H_STK_1000, IBC_PALLET_H,
    BLUE_IBC_Y, BROWN_IBC_Y, IBC_FAR_Y, WASTE_IBC_Y,
    PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_W, PROC_TRAY_D,
    PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR, PROC_TRAY_RIM,
    WALKWAY_W, WALKWAY_H, WALKWAY_GRATE_T,
    WALKWAY_BRACKET_H, WALKWAY_BRACKET_T, WALKWAY_BRACKET_SPACING,
    WALKWAY_RIGHT_W,
    WALKWAY_RIGHT_X, WALKWAY_LEFT_X, WALKWAY_LEFT_SPAN,
    WALKWAY_LEFT_WIDE_W, WALKWAY_LEFT_WIDE_YD_L, WALKWAY_LEFT_WIDE_YD_R,
    LEFT_WK_CANT_LEG_X, LEFT_WK_CANT_LEG_YDS, LEFT_WK_CANT_POST, LEFT_WK_CANT_POST_T,
    LEFT_WK_CANT_FOOT, LEFT_WK_CANT_FOOT_BOLT_N,
    LEFT_WK_CANT_STD_REACH, LEFT_WK_CANT_WIDE_REACH,
    SHELF_X_L, SHELF_X_R, SHELF_W, SHELF_DEPTH, SHELF_H, SHELF_T,
    SHELF_YD_NEAR, SHELF_STOW_TOP_Z,
    EP_X, EP_W, EP_H_LO, EP_H_HI, BA_X, BA_W, PUMP_X, PUMP_W,
    PUMP_D, PUMP_H_LO, PUMP_H_HI, CORRIDOR_YD_NEAR,
    PANEL_CORNER_T, PANEL_CENTER_T, PANEL_CENTER_W, PANEL_FLOOR_GAP,
    PANEL_CORNER_YD_L, PANEL_CORNER_YD_R, PANEL_SKIN_T, PANEL_FAN_BAND_Z,
    PIVOT_X, PIVOT_YD, SWING_LOCK_DEG,
    DRUM_D, DRUM_R, DRUM_H_LT,
    LT_HOUSING_R, LT_HOUSING_T, LT_DRUM_OR, LT_DRUM_T, LT_OPENING_DEG,
    BAY_FRONT_X, BAY_BACK_X, DRUM_CAGE_YD_L, DRUM_CAGE_YD_R,
    FAN_DIAM, FAN_A_YD, FAN_B_YD,
    C_OUT, C_DIM, C_STEEL, C_ALUM,
    C_BLUE_IBC, C_BROWN_IBC, C_WASTE_IBC,
    C_ELEC, C_BATT, C_PUMP,
    C_HINGE_PANEL, C_LT_DRUM, C_PROC_ZONE,
    C_WALL, C_FAN,
    DIAGRAMS_DIR,
    CONTAINER_RIB_SPACING,
)
from tbs_title_block import title_block

# ── Material densities (kg/m³) ──────────────────────────────────────────────
RHO_STEEL  = 7850     # mild / Corten steel
RHO_SS304  = 7930     # 304 stainless steel
RHO_ALUM   = 2700     # aluminum 6061
RHO_PLY    = 600      # marine plywood (typical)
RHO_WATER  = 1000     # fresh water at ~20°C
RHO_HDPE   = 950      # UV-stabilized HDPE sheet (light-trap housing skin, rev 9 / B2)
RHO_PP     = 905      # polypropylene sheet (light-trap drum skin, rev 9 / B2)

# ── Grating weight ──────────────────────────────────────────────────────────
# 5/8" (15mm) molded fiberglass (GRP) grating, vinyl-ester resin, grit top.
# Corrosion-proof in the wet photo-chemistry environment; the 15mm depth is kept
# so the lowered deck + spray-bar clearance are unchanged (a 1"/25mm GRP would
# force a deck-height redesign). Source: McNICHOLS / Grating Pacific FRP catalogs.
GRATING_KG_PER_M2 = 11.0   # molded GRP ~11 kg/m² (was 26 for 15mm galvanized steel)

# ── IBC empty weight ────────────────────────────────────────────────────────
# ibc-reconfig-v2: all four positions are 275-gal (≈1000 L) caged composite totes
# (1219×1016×1168mm) — ~65 kg tare each (HDPE bottle + galvanized cage + steel pallet).
IBC_EMPTY_KG = 65.0
# Bottle fillable column: ≈1L per mm of height above the pallet base (a 1000L bottle
# fills ~1000mm of the 1168mm tote above its 168mm pallet). Used to place water CG.
IBC_BOTTLE_FILL_PER_L = 1.0   # mm of water column per liter (1000L → ~1000mm)


# ═══════════════════════════════════════════════════════════════════════════
# Component data model
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class Component:
    """Single equipment or structural component with weight and position."""
    name: str
    category: str       # "container", "structure", "equipment", "liquid"
    weight_kg: float
    x_min: float        # footprint bounds (mm)
    x_max: float
    yd_min: float
    yd_max: float
    z_min: float = 0.0  # vertical bounds (mm) — 0 = floor
    z_max: float = 0.0  # z_max = 0 means floor-level item
    color: str = C_STEEL
    states: tuple = ("dry", "ready", "exhausted", "loaded_transport")  # which states include this
    calc_note: str = ""  # brief description of weight derivation

    @property
    def x_cg(self):
        return (self.x_min + self.x_max) / 2

    @property
    def yd_cg(self):
        return (self.yd_min + self.yd_max) / 2

    @property
    def z_cg(self):
        return (self.z_min + self.z_max) / 2

    @property
    def area_m2(self):
        return (self.x_max - self.x_min) * (self.yd_max - self.yd_min) / 1e6


def swing_bbox(x0, x1, y0, y1, deg=SWING_LOCK_DEG):
    """Axis-aligned bounding box of an (X, Yd) footprint after the cargo panel
    swings `deg` about the Ø89 pivot post (PIVOT_X, PIVOT_YD). Used to place the
    transport-state panel/drum at their SWUNG position (rev10 — no slide)."""
    t = np.radians(deg); c, s = np.cos(t), np.sin(t)
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    xs = [PIVOT_X + (px - PIVOT_X) * c - (py - PIVOT_YD) * s for px, py in pts]
    ys = [PIVOT_YD + (px - PIVOT_X) * s + (py - PIVOT_YD) * c for px, py in pts]
    return min(xs), max(xs), min(ys), max(ys)


# ═══════════════════════════════════════════════════════════════════════════
# Weight calculations — all from first principles
# ═══════════════════════════════════════════════════════════════════════════

def _panel_weight():
    """Hinged panel: stepped framed construction (rev 11 skins).
    Corner zones (2×): 4mm PP skin + 3mm ALUMINUM core + 4mm PP skin (40mm
    framed envelope). The Fan B corner keeps an 18mm PLYWOOD band (panel bottom
    up to PANEL_FAN_BAND_Z) for rigid fan/duct mounting; the rest is PP.
    Center zone: 50×50mm steel RHS frame + 4mm PP skins, PANEL_CENTER_W wide.
    First-principles only — no scaling pin (the fixed Ø900 housing is added
    separately in build_components, since it bolts into the panel center).
    """
    panel_h = C_HGT  # 2388mm
    ts = PANEL_SKIN_T * 1e-9                       # 4mm PP skin factor (mm²→m³)
    # Corner zones (near + far are symmetric at PANEL_CORNER_YD_L each)
    corner_w_near = PANEL_CORNER_YD_L              # = 653mm
    corner_w_far = C_WID - PANEL_CORNER_YD_R       # = 653mm
    corner_area = (corner_w_near + corner_w_far) * panel_h          # mm²
    # Fan B corner keeps an 18mm ply band over the near-corner width, bottom→band-top
    fan_band_area = corner_w_near * (PANEL_FAN_BAND_Z - PANEL_FLOOR_GAP)
    corner_band_kg = 2 * fan_band_area * 18e-9 * RHO_PLY           # 2× 18mm ply faces
    corner_skin_kg = 2 * (corner_area - fan_band_area) * ts * RHO_PP  # 2× 4mm PP faces
    alum_vol_corner = corner_area * 3e-9            # 3mm Al core (unchanged)
    corner_plate_kg = alum_vol_corner * RHO_ALUM
    corner_ply_kg = corner_band_kg + corner_skin_kg  # (mixed ply band + PP skin)
    # Center zone: steel RHS frame perimeter + cross members.
    # 50×50×3 SHS section area = 50² − 44² = 564 mm² → 4.43 kg/m (EN 10219
    # table 4.35; first-principles used here). [was an approx 456 mm²/3.58 kg/m]
    rhs_kg_per_m = (50**2 - 44**2) * 1e-6 * RHO_STEEL
    cw = PANEL_CENTER_W / 1000.0                   # = 1.056 m
    center_frame_length = 2 * (cw + 2.388) + 4 * cw
    frame_kg = center_frame_length * rhs_kg_per_m
    # Center skins: 2 × center_w × 2388 × 4mm PP (rev11; was 18mm ply)
    center_ply_kg = 2 * (cw * 2.388 * (PANEL_SKIN_T / 1000.0)) * RHO_PP
    return corner_ply_kg + corner_plate_kg + frame_kg + center_ply_kg


def _lighttrap_weight():
    """Housed revolving-door light lock (rev 9 / B2): a fixed Ø900 housing plus a
    single-opening C-shell drum, now a HYBRID PLASTIC SKIN — 5mm UV-HDPE housing
    + 4mm PP drum (was 3mm 5052-H32 aluminum), NO internal baffles. Suspended at
    Z=PANEL_FLOOR_GAP so its effective height is shorter. Steel is retained only
    where it must be: the stub shafts (bearing fit). The plastic skin roughly
    halves the assembly mass and removes the aluminum↔steel galvanic couple.
    Returns (drum_kg, housing_kg) — drum rotates; housing bolts to the panel.
    """
    H = (DRUM_H_LT - PANEL_FLOOR_GAP) / 1000.0     # ≈ 2.12 m tall (suspended)
    open_frac = LT_OPENING_DEG / 360.0             # 80° opening fraction
    # Rotating drum: PP C-shell Ø864 (one 80° opening) + 2 C-shaped caps
    t_d = LT_DRUM_T / 1000.0
    drum_circ = np.pi * (2 * LT_DRUM_OR / 1000.0)
    drum_shell_kg = drum_circ * (1 - open_frac) * H * t_d * RHO_PP
    cap_area = np.pi * (LT_DRUM_OR / 1000.0) ** 2 * (1 - open_frac)
    drum_cap_kg = 2 * cap_area * t_d * RHO_PP
    # Steel stub shafts (Ø75×150, bearing fit) + 2 sealed bearings; plastic
    # edge stiffeners on the opening + grab rail + brush seals
    shaft_kg = 2 * np.pi * (0.0375 ** 2) * 0.150 * RHO_STEEL
    edge_stiff_kg = 2 * H * 0.30            # 2× PP edge stiffener (~0.30 kg/m)
    drum_hw_kg = shaft_kg + 2 * 1.3 + edge_stiff_kg + 4.0
    drum_kg = drum_shell_kg + drum_cap_kg + drum_hw_kg
    # Fixed UV-HDPE housing: Ø900 cylinder minus two 80° openings
    t_h = LT_HOUSING_T / 1000.0
    house_circ = np.pi * (2 * LT_HOUSING_R / 1000.0)
    housing_kg = house_circ * (1 - 2 * open_frac) * H * t_h * RHO_HDPE
    housing_kg += 6.0   # steel bolt flange/hub inserts + bearing mounts + isolation
    return drum_kg, housing_kg


def _walkway_near_far_weight():
    """Weight of one long-wall walkway (near or far).
    Brackets: 8mm steel plate gussets at 457mm centers.
    Grating: 25mm galvanized press-locked, 300mm wide.
    """
    walkway_length = PROC_TRAY_X_R - 470  # X=470 to X=4629 = 4159mm
    # Number of brackets
    n_brackets = int(walkway_length / WALKWAY_BRACKET_SPACING) + 1  # ≈ 10
    # Each bracket: right triangle 150mm vert × 300mm horiz, 8mm plate
    # Area ≈ 0.5 × 150 × 300 + 150 × 300 (vertical leg is rectangular)
    # Vertical leg: 150 × 200mm (arbitrary width for bolt area) × 8mm
    # Simplified: each bracket ≈ 0.5 × 0.15 × 0.30 × 0.008 × 7850 + fasteners
    bracket_vol = (0.5 * 0.150 * 0.300 + 0.150 * 0.100) * 0.008  # m³
    bracket_kg = bracket_vol * RHO_STEEL  # ≈ 2.7 kg per bracket
    total_bracket_kg = n_brackets * bracket_kg
    # Grating
    grate_area = (walkway_length / 1000) * (WALKWAY_W / 1000)  # m²
    grate_kg = grate_area * GRATING_KG_PER_M2
    return total_bracket_kg + grate_kg


def _walkway_right_weight():
    """Right walkway (IBC end): rev12 CANTILEVER-rectangle support (replaces the ceiling
    hangers). A closed rectangle (2 long + 2 end beams) + 2 center cantilever arms off the
    IBC uprights, all 40×40×3 SHS; wall cleats (left corners) + COMBINED corner plates
    (right corners, shared with the bottom film rail); grating."""
    shs_kg_m = (40 ** 2 - 34 ** 2) * 1e-6 * RHO_STEEL          # 40×40×3 SHS ≈ 3.48 kg/m
    # rectangle: 2 long beams (full width) + 2 end beams (300mm) + 2 center arms (405mm)
    frame_len = 2 * (C_WID / 1000) + 2 * (WALKWAY_RIGHT_W / 1000) + 2 * 0.405
    frame_kg = frame_len * shs_kg_m
    # 2 wall cleats (left corners): back-plate + ext plate + shelf, 8-10mm
    cleat_kg = 2 * (2 * (0.090 * 0.065 * 0.008) + 0.090 * 0.055 * 0.010) * RHO_STEEL
    # 2 combined corner plates (right): interior + exterior 150×150×10 + 2 seats each
    plate_kg = 2 * (2 * (0.150 * 0.167 * 0.010) + 2 * (0.150 * 0.055 * 0.012)) * RHO_STEEL
    bolt_kg = 2.0                                              # M12 through-bolts + clamps
    grate_area = (WALKWAY_RIGHT_W / 1000) * (C_WID / 1000)
    grate_kg = grate_area * GRATING_KG_PER_M2
    return frame_kg + cleat_kg + plate_kg + bolt_kg + grate_kg


def _walkway_left_weight():
    """Left walkway (removable lift-out): grating + drum-exit punch-out grating + 5
    FLOOR-LEG CANTILEVER brackets (post + foot plate + arm; the 3 punch-out brackets get
    extended arms) (rev 2026-06-07 — floor-leg cantilevers replace the edge beam)."""
    # Grating: 300mm × 2362mm + punch-out extension (300mm × 760mm).
    grate_area = (WALKWAY_W / 1000) * (C_WID / 1000)
    punch_len = (WALKWAY_LEFT_WIDE_YD_R - WALKWAY_LEFT_WIDE_YD_L) / 1000.0
    punch_grate_area = ((WALKWAY_LEFT_WIDE_W - WALKWAY_W) / 1000.0) * punch_len
    grate_kg = (grate_area + punch_grate_area) * GRATING_KG_PER_M2
    # 5 steel floor-leg cantilever brackets.
    n_brk = len(LEFT_WK_CANT_LEG_YDS)
    P, PT = LEFT_WK_CANT_POST, LEFT_WK_CANT_POST_T
    post_area = (4 * P * PT - 4 * PT * PT) * 1e-6          # 50×50×3 SHS section, m²
    post_h = (WALKWAY_H - WALKWAY_GRATE_T) / 1000.0        # 0.115 m — floor to grate bottom
    post_kg = n_brk * post_area * post_h * RHO_STEEL
    fl, fw, ft = LEFT_WK_CANT_FOOT                          # 128×60×8 plate
    foot_kg = n_brk * (fl / 1000 * fw / 1000 * ft / 1000) * RHO_STEEL
    # Arms (40×40×3 SHS): 2 standard (reach to X470) + 3 punch-out (extended to X770).
    arm_x0 = LEFT_WK_CANT_LEG_X + P / 2
    std_reach = (LEFT_WK_CANT_STD_REACH - arm_x0) / 1000.0
    wide_reach = (LEFT_WK_CANT_WIDE_REACH - arm_x0) / 1000.0
    n_wide = sum(1 for y in LEFT_WK_CANT_LEG_YDS
                 if WALKWAY_LEFT_WIDE_YD_L <= y <= WALKWAY_LEFT_WIDE_YD_R)
    n_std = n_brk - n_wide
    arm_area = (4 * 40 * 3 - 4 * 9) * 1e-6                 # 40×40×3 SHS arm, m²
    arm_kg = arm_area * (n_std * std_reach + n_wide * wide_reach) * RHO_STEEL
    anchors_kg = n_brk * LEFT_WK_CANT_FOOT_BOLT_N * 0.05   # 4× M10 ≈ 50 g each per foot
    return grate_kg + post_kg + foot_kg + arm_kg + anchors_kg


def _shelf_weight():
    """Chemistry-prep fold-down shelf (rev13): 18mm phenolic-ply work surface in a
    2" aluminum angle perimeter frame + 15mm spill lip, continuous steel piano hinge,
    and 2 folding stays. Self-weight only — the ~25 kg deployed mixing load is a
    transient prep case (film plane parked, container stationary), not a modeled
    transport/exposure state, so it is not added to any state. Geometry from
    chemistry-prep-shelves.md §3."""
    w, d = SHELF_W / 1000.0, SHELF_DEPTH / 1000.0          # 0.600 × 0.300 m
    ply_kg = w * d * 0.018 * RHO_PLY                        # 18mm phenolic ply
    # 2"×2"×3mm Al angle around the 1800mm perimeter + 15mm×3mm spill lip on 3 free edges.
    angle_area = (2 * 50 * 3 - 3 * 3) * 1e-6               # 50×50×3 angle section, m²
    frame_kg = (2 * (w + d)) * angle_area * RHO_ALUM
    lip_kg = (w + 2 * d) * (15 * 3 * 1e-6) * RHO_ALUM      # 15mm lip, 3 free edges
    frame_kg += lip_kg + 0.3                               # + corner gussets
    hinge_kg = 0.7                                         # continuous 600mm steel piano hinge
    stay_kg = 2 * 1.0                                      # 2 folding stays/struts
    hw_kg = 0.5                                            # M5 screws + wall anchors
    return ply_kg + frame_kg + hinge_kg + stay_kg + hw_kg


def _film_plane_carriage_weight():
    """Film plane carriage: Al angle frame + 92 cam-lever clamps + carriages."""
    # Perimeter frame: 2"×2"×3/16" Al angle (50.8×50.8×4.8mm)
    perimeter = 2 * (FP_W + FP_H) / 1000  # m
    angle_area = (2 * FP_ANGLE_LEG * FP_ANGLE_T - FP_ANGLE_T**2) * 1e-6  # m²
    frame_kg = perimeter * angle_area * RHO_ALUM
    # 92 cam-lever clamps: ~0.15 kg each
    clamp_kg = CLAMP_N_TOTAL * 0.15
    # 4× HGH20CA carriage blocks: ~0.5 kg each
    carriage_kg = 4 * 0.5
    return frame_kg + clamp_kg + carriage_kg

def _bay_weight():
    """B2 punch-out bay carried on the swinging leaf: a 6mm marine-ply 4-wall
    tube (2 sides + top + bottom) plus the exterior front face (Ø900 housing
    opening deducted), enclosing the offset light-trap housing. First-principles
    from the bay/cage footprint constants — supersedes the old 12 kg placeholder."""
    depth = (BAY_BACK_X - BAY_FRONT_X) / 1000.0          # ≈ 0.890 m (X protrusion)
    width = (DRUM_CAGE_YD_R - DRUM_CAGE_YD_L) / 1000.0   # ≈ 0.962 m (Yd)
    height = (DRUM_H_LT - PANEL_FLOOR_GAP) / 1000.0      # ≈ 2.12 m
    aperture = np.pi * (LT_HOUSING_R / 1000.0) ** 2      # Ø900 opening in front face
    area = 2 * (depth * height) + 2 * (depth * width) + max(width * height - aperture, 0)
    return area * (PANEL_SKIN_T / 1000.0) * RHO_PP        # rev11: 4mm PP (was 6mm ply); ≈ 25 kg, weight-neutral


def _swing_hardware_weight():
    """rev10 rotation transport hardware — replaces the retired HGR20 ceiling-rail
    slide (the pivot reuses the film far-left Ø89 upright, so no new post). Reconciled
    against the firmed Stage-4 BOM (master-shopping-list.md §7a, 2026-06-10):
      bearings ~4 kg (12in turntable thrust ~2 + 2× 89mm bronze sleeve ~1),
      pivot hub + thrust collar (machined steel block) ~10 kg, drum support cage
      (40×40×3 SHS, ~4m) ~15 kg, top+bottom wall stays + 4-bolt anchor plates ~5 kg,
      4× drop-in rail saddles ~4 kg. Sum ≈ 38 kg (unchanged from the prior estimate —
      bearings lighter, machined hub heavier, net wash)."""
    return 4 + 10 + 15 + 5 + 4   # ≈ 38 kg, concentrated at the cargo-door end


def _ibc_stacking_frame_weight():
    """Steel 50×50×3mm RHS RESTRAINT-ONLY frame for the direct-stacked 2×2 IBC
    stack (ibc-reconfig-v2).

    The 1000L caged totes stack cage-on-cage (no room for a load-bearing deck —
    ~52mm headroom), so the frame only RESTRAINS:
      • full-height corridor uprights (6) + 2 front-bay uprights, ~2.30m, 50×50×3 RHS
      • longitudinal ties (2 lines × 2 levels) along X
      • front retaining bars (4: 2 columns × 2 heights) + short frame ties
      • 8 floor flange feet, 150×150×12mm + ~40 M12 anchors
      • 4 Simpson-style wall joist hangers (carry the front-bar wall ends),
        through-bolted to 4 exterior backing plates (100×135×8mm) + 16 M12 bolts
      • forward panel-mount frame (2 uprights + top rail + floor beam) — this frame
        also carries the right walkway (replaces the old IBC-upright cantilever)
    Total ≈ 175 kg.
    """
    rhs = 4.25                                    # 50×50×3 RHS, kg/m
    up_h = (IBC_H_STK_1000 - 40) / 1000.0         # 2.296 m full-height upright
    uprights_kg = 8 * up_h * rhs                  # 6 corridor + 2 front
    ties_kg = 4 * 1.28 * rhs                      # 2 lines × 2 levels, ~1.28m
    front_bars_kg = 4 * 1.1 * rhs + 4 * 0.4 * rhs # 4 bars + short frame ties
    feet_kg = 8 * (0.150 * 0.150 * 0.012) * RHO_STEEL
    hangers_kg = 4 * 1.1                          # folded 4mm-plate joist hangers
    ext_plates_kg = 4 * (0.100 * 0.135 * 0.008) * RHO_STEEL  # exterior wall backing plates
    anchors_kg = (40 + 16) * 0.10                 # floor anchors + 16 M12 wall through-bolts
    panel_frame_kg = (2 * 2.30 + 0.27 + 0.27) * rhs
    return (uprights_kg + ties_kg + front_bars_kg + feet_kg
            + hangers_kg + ext_plates_kg + anchors_kg + panel_frame_kg)


# ═══════════════════════════════════════════════════════════════════════════
# Component inventory
# ═══════════════════════════════════════════════════════════════════════════

def build_components():
    """Build the complete component list with calculated weights."""

    # First-principles weights (no scaling pin). The fixed Ø900 housing is
    # welded into the panel center zone, so its mass is carried by the panel;
    # only the C-shell drum rotates.
    drum_kg, housing_kg = _lighttrap_weight()
    # rev 10: the only B2 hardware still carried on the swinging leaf is the
    # punch-out bay (first-principles below). The barrel hinges (9 kg), steel
    # hinge post (8 kg) and retractable swing caster (3 kg) were RETIRED with the
    # slide — the leaf now rotates on the Ø89 pivot post + bearings + wall stays,
    # which are accounted in _swing_hardware_weight(), not here. [was 12+9+8+3=32]
    b2_hardware_kg = _bay_weight()            # ≈ 25 kg (bay only)
    panel_kg = _panel_weight() + housing_kg + b2_hardware_kg

    near_far_wk = _walkway_near_far_weight()
    right_wk = _walkway_right_weight()
    left_wk = _walkway_left_weight()

    components = [
        # ── Container ────────────────────────────────────────────────────
        Component("Container shell", "container", 1920.0,
                  0, C_LEN, 0, C_WID, 0, C_HGT, color=C_WALL,
                  calc_note="Hapag-Lloyd 20ft ISO tare (2,200 kg) minus doors (280 kg)"),

        # ── Cargo doors (2 leaves, ~140 kg each = 280 kg total) ─────
        # Closed (transport): both leaves at X≈-50 (exterior face), full Yd span
        # Open (camera ready): each leaf swung flat against a side wall
        Component("Cargo door (near)", "container", 140.0,
                  -WALL_T - DOOR_T, -WALL_T, 0, C_WID / 2,
                  0, C_HGT, color=C_DOOR,
                  states=("dry", "exhausted", "loaded_transport"),
                  calc_note="ISO door leaf ~140 kg, closed position"),
        Component("Cargo door (far)", "container", 140.0,
                  -WALL_T - DOOR_T, -WALL_T, C_WID / 2, C_WID,
                  0, C_HGT, color=C_DOOR,
                  states=("dry", "exhausted", "loaded_transport"),
                  calc_note="ISO door leaf ~140 kg, closed position"),
        Component("Cargo door (near)", "container", 140.0,
                  0, C_WID / 2 + WALL_T,
                  -WALL_T - DOOR_T, -WALL_T,
                  0, C_HGT, color=C_DOOR,
                  states=("ready",),
                  calc_note="ISO door leaf ~140 kg, open against near wall"),
        Component("Cargo door (far)", "container", 140.0,
                  0, C_WID / 2 + WALL_T,
                  C_WID + WALL_T, C_WID + WALL_T + DOOR_T,
                  0, C_HGT, color=C_DOOR,
                  states=("ready",),
                  calc_note="ISO door leaf ~140 kg, open against far wall"),

        # ── Structure ────────────────────────────────────────────────────
        # Panel + drum: transport position — SWUNG ~56° about the pivot (rev10, no slide).
        # swing_bbox() rotates the deployed footprint, biasing the mass toward the far side.
        Component("Hinged panel", "structure", panel_kg,
                  *swing_bbox(0, 80, 0, C_WID), 0, C_HGT,
                  color=C_HINGE_PANEL,
                  states=("dry", "exhausted", "loaded_transport"),
                  calc_note="Framed panel: 4mm-PP skins (18mm-ply Fan-B mount band) + 3mm-Al corner cores, steel RHS center + 5mm-HDPE Ø900 housing + 4mm-PP B2 bay. Transport: swung 56° about the pivot"),
        Component("Light trap drum", "structure", drum_kg,
                  *swing_bbox(0, 40, PANEL_CORNER_YD_L, PANEL_CORNER_YD_R),
                  PANEL_FLOOR_GAP, DRUM_H_LT, color=C_LT_DRUM,
                  states=("dry", "exhausted", "loaded_transport"),
                  calc_note="4mm PP C-shell drum (Ø864, no baffles) + steel shaft/bearings. Transport: swung 56° about the pivot"),
        # Panel + drum: deployed position (at cargo door end) for camera ready
        Component("Hinged panel", "structure", panel_kg,
                  0, 80, 0, C_WID, 0, C_HGT, color=C_HINGE_PANEL,
                  states=("ready",),
                  calc_note="Framed panel: 4mm-PP skins (18mm-ply Fan-B mount band) + 3mm-Al corner cores, steel RHS center + 5mm-HDPE Ø900 housing + 4mm-PP B2 bay"),
        Component("Light trap drum", "structure", drum_kg,
                  0, 40, PANEL_CORNER_YD_L, PANEL_CORNER_YD_R,
                  0, DRUM_H_LT, color=C_LT_DRUM,
                  states=("ready",),
                  calc_note="4mm PP C-shell drum (Ø864, no baffles) + steel shaft/bearings"),
        Component("Processing tray", "structure", 116.0,
                  PROC_TRAY_X_L, PROC_TRAY_X_R,
                  PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR,
                  0, PROC_TRAY_RIM, color=C_PROC_ZONE,
                  calc_note="304 SS 1.5mm, 2 panels × 58 kg (water-system-report.md)"),
        Component("Near walkway", "structure", near_far_wk,
                  470, PROC_TRAY_X_R, 0, WALKWAY_W,
                  0, WALKWAY_H, color=C_STEEL,
                  calc_note=f"Brackets + {GRATING_KG_PER_M2} kg/m² grating"),
        Component("Far walkway", "structure", near_far_wk,
                  470, PROC_TRAY_X_R, C_WID - WALKWAY_W, C_WID,
                  0, WALKWAY_H, color=C_STEEL,
                  calc_note=f"Brackets + {GRATING_KG_PER_M2} kg/m² grating"),
        Component("Right walkway", "structure", right_wk,
                  WALKWAY_RIGHT_X, WALKWAY_RIGHT_X + WALKWAY_W,
                  0, C_WID, 0, WALKWAY_H, color=C_STEEL,
                  calc_note=f"Cantilever rectangle (rev12): 40×40×3 SHS frame + 2 arms + cleats + combined plates + grating"),
        Component("Left walkway", "structure", left_wk,
                  WALKWAY_LEFT_X, WALKWAY_LEFT_X + WALKWAY_W,
                  0, C_WID, 0, WALKWAY_H, color="#80C080",
                  calc_note="Removable lift-out: grating + bearer + legs + drum-exit punch-out"),
        Component("Swing pivot + cage hardware", "structure", _swing_hardware_weight(),
                  0, 400, 700, 2287,
                  0, C_HGT, color=C_ALUM,
                  calc_note="rev10 rotation transport hardware (replaces retired HGR20 ceiling rails): pivot bearings + collar + drum cage + wall stays + rail saddles, at the cargo-door end. Estimate — refine vs Stage-4 BOM"),
        Component("Container mods", "structure", 65.0,
                  0, C_LEN, 0, C_WID, 0, C_HGT, color=C_WALL,
                  calc_note="Light seal foam + reinforcement plates (estimate)"),
        # Chem-prep fold-down shelf (rev13): STOWED in every modeled state — folded up
        # flat against the pinhole wall (Yd≈0, Z = SHELF_H..SHELF_STOW_TOP_Z). It is only
        # deployed (horizontal, Yd0–300, +~25 kg chemistry) during the transient mixing
        # prep with the film plane parked; that is not a transport/exposure state.
        Component("Chem-prep shelf (stowed)", "structure", _shelf_weight(),
                  SHELF_X_L, SHELF_X_R, SHELF_YD_NEAR, SHELF_YD_NEAR + SHELF_T,
                  SHELF_H, SHELF_STOW_TOP_Z, color=C_ALUM,
                  calc_note="Fold-down shelf: 18mm phenolic ply + 2\" Al angle frame + piano hinge + 2 stays. Stowed vertical vs pinhole wall; deployed-with-chemistry (+25 kg) is a transient prep case, not modeled"),

        # ── Equipment ────────────────────────────────────────────────────
        Component("Fan B (intake)", "equipment", 2.0,
                  0, 50, FAN_B_YD - 75, FAN_B_YD + 75,
                  525, 675, color=C_FAN,
                  calc_note="150mm axial fan on panel, low"),
        Component("Electrical panel", "equipment", 15.0,
                  EP_X, EP_X + EP_W, 0, 150,
                  EP_H_LO, EP_H_HI, color=C_ELEC,
                  calc_note="Wall-mount distribution panel (Z from EP_H_LO/HI; rev11 dropped 150 for brace-beam clearance)"),
        Component("Battery bank", "equipment", 13.0,
                  BA_X, BA_X + BA_W, 0, 150,
                  100, 600, color=C_BATT,
                  calc_note="1× 100Ah LiFePO4 @ 13 kg (standard build; +13 kg for the optional 2nd pack)"),
        Component("Film plane carriage", "equipment",
                  _film_plane_carriage_weight(),
                  FP_X_L, FP_X_R, FP_Y - 50, FP_Y + 50,
                  100, C_HGT - 100, color=C_ALUM,
                  calc_note="Al angle frame + 92 clamps + 4 carriages"),
        Component("Solar controller", "equipment", 2.0,
                  1700, 1800, 0, 100,
                  1200, 1400, color=C_BATT,
                  calc_note="MPPT charge controller"),
        Component("Pump manifold", "equipment", 4.5,
                  PUMP_X, PUMP_X + PUMP_W,
                  CORRIDOR_YD_NEAR, CORRIDOR_YD_NEAR + PUMP_D,
                  PUMP_H_LO, PUMP_H_HI, color=C_PUMP,
                  calc_note="4× 12V diaphragm pumps on equipment panel"),
        Component("Tilt-swing board", "equipment", 30.0,
                  PH_X - 310, PH_X + 310, 0, 100,
                  PH_H - 310, PH_H + 310, color="#CC6600",
                  calc_note="620×620×45mm Al plate + spherical pivot + screws"),
        Component("Fan A (exhaust)", "equipment", 2.0,
                  C_LEN - 50, C_LEN, FAN_A_YD - 75, FAN_A_YD + 75,
                  2125, 2275, color=C_FAN,
                  calc_note="150mm axial fan, high (above IBC)"),
        Component("Baffle ducts", "equipment", 6.0,
                  0, C_LEN, 0, C_WID,
                  400, 800, color=C_FAN,
                  calc_note="2× galvanized steel baffle ducts @ 3 kg"),

        # ── IBC totes (empty) — Blue on top, Brown/Waste on bottom (v2: 1000L
        #    caged composite, direct-stacked to 2336mm) ──────────────────
        Component("Blue IBC-1 (tote)", "equipment", IBC_EMPTY_KG,
                  IBC_COL_X, IBC_COL_X + IBC_W,
                  BLUE_IBC_Y, BLUE_IBC_Y + IBC_D,
                  IBC_H_1000, IBC_H_STK_1000, color=C_BLUE_IBC,
                  calc_note="1000L caged composite tare (top tier)"),
        Component("Blue IBC-2 (tote)", "equipment", IBC_EMPTY_KG,
                  IBC_COL_X, IBC_COL_X + IBC_W,
                  IBC_FAR_Y, IBC_FAR_Y + IBC_D,
                  IBC_H_1000, IBC_H_STK_1000, color=C_BLUE_IBC,
                  calc_note="1000L caged composite tare (top tier)"),
        Component("Brown IBC-3 (tote)", "equipment", IBC_EMPTY_KG,
                  IBC_COL_X, IBC_COL_X + IBC_W,
                  BROWN_IBC_Y, BROWN_IBC_Y + IBC_D,
                  0, IBC_H_1000, color=C_BROWN_IBC,
                  calc_note="1000L caged composite tare (bottom tier)"),
        Component("Waste IBC-4 (tote)", "equipment", IBC_EMPTY_KG,
                  IBC_COL_X, IBC_COL_X + IBC_W,
                  WASTE_IBC_Y, WASTE_IBC_Y + IBC_D,
                  0, IBC_H_1000, color=C_WASTE_IBC,
                  calc_note="1000L caged composite tare (bottom tier)"),
        Component("IBC restraint frame", "equipment",
                  _ibc_stacking_frame_weight(),
                  IBC_COL_X, IBC_COL_X + IBC_W,
                  BLUE_IBC_Y, IBC_FAR_Y + IBC_D,
                  0, IBC_H_STK_1000 - 40, color=C_STEEL,
                  calc_note="50×50×3mm RHS restraint frame: uprights + ties + "
                            "feet + front bars + wall hangers + panel frame"),

        # ── Liquids — Camera Ready state (water in top-tier Blue IBCs) ───
        # v2: Blue holds 1600L TOTAL across the two top totes, by design neither
        # full (~800L each). Water column sits in the lower ~800mm of the bottle
        # (base = tote base + 168mm pallet) — this is the high-CG case.
        Component("Blue IBC-1 water", "liquid", 800.0,
                  IBC_COL_X, IBC_COL_X + IBC_W,
                  BLUE_IBC_Y, BLUE_IBC_Y + IBC_D,
                  IBC_H_1000 + IBC_PALLET_H,
                  IBC_H_1000 + IBC_PALLET_H + 800 * IBC_BOTTLE_FILL_PER_L,
                  color=C_BLUE_IBC,
                  states=("ready", "loaded_transport"),
                  calc_note="800L clean wash water (top tier, 1600L Blue total)"),
        Component("Blue IBC-2 water", "liquid", 800.0,
                  IBC_COL_X, IBC_COL_X + IBC_W,
                  IBC_FAR_Y, IBC_FAR_Y + IBC_D,
                  IBC_H_1000 + IBC_PALLET_H,
                  IBC_H_1000 + IBC_PALLET_H + 800 * IBC_BOTTLE_FILL_PER_L,
                  color=C_BLUE_IBC,
                  states=("ready", "loaded_transport"),
                  calc_note="800L clean wash water (top tier, 1600L Blue total)"),
        # ── Liquids — Materials Exhausted (the 1600L of Blue has been processed
        #    down into the bottom-tier Brown (recycle) + Waste totes) ────
        Component("Brown IBC-3 water", "liquid", 800.0,
                  IBC_COL_X, IBC_COL_X + IBC_W,
                  BROWN_IBC_Y, BROWN_IBC_Y + IBC_D,
                  IBC_PALLET_H, IBC_PALLET_H + 800 * IBC_BOTTLE_FILL_PER_L,
                  color=C_BROWN_IBC,
                  states=("exhausted",),
                  calc_note="800L recycled water (bottom tier; 1600L recovered, split)"),
        Component("Waste IBC-4 water", "liquid", 800.0,
                  IBC_COL_X, IBC_COL_X + IBC_W,
                  WASTE_IBC_Y, WASTE_IBC_Y + IBC_D,
                  IBC_PALLET_H, IBC_PALLET_H + 800 * IBC_BOTTLE_FILL_PER_L,
                  color=C_WASTE_IBC,
                  states=("exhausted",),
                  calc_note="800L waste water (bottom tier; 1600L recovered, split)"),
        # Processing tray is empty in exhausted state — all water has been
        # processed and drained into Brown/Waste IBCs.
    ]
    return components


# ═══════════════════════════════════════════════════════════════════════════
# Analysis functions
# ═══════════════════════════════════════════════════════════════════════════

def filter_state(components, state):
    """Return components active in the given state."""
    return [c for c in components if state in c.states]


def compute_cg(components):
    """Compute total weight and center-of-gravity (X, Yd, Z)."""
    total = sum(c.weight_kg for c in components)
    if total == 0:
        return 0, 0, 0, 0
    x_cg = sum(c.weight_kg * c.x_cg for c in components) / total
    yd_cg = sum(c.weight_kg * c.yd_cg for c in components) / total
    z_cg = sum(c.weight_kg * c.z_cg for c in components) / total
    return total, x_cg, yd_cg, z_cg


def compute_quadrants(components):
    """Compute weight in each quadrant (front/rear × near/far).

    Divides at X_mid = C_LEN/2 and Yd_mid = C_WID/2.
    Components spanning boundaries get proportional allocation.
    """
    x_mid = C_LEN / 2
    yd_mid = C_WID / 2
    quads = {"front_near": 0, "front_far": 0,
             "rear_near": 0, "rear_far": 0}
    for c in components:
        # Fraction in front (X < x_mid) vs rear
        x_span = c.x_max - c.x_min
        if x_span == 0:
            f_front = 1.0 if c.x_cg < x_mid else 0.0
        else:
            front_len = max(0, min(c.x_max, x_mid) - c.x_min)
            f_front = front_len / x_span
        f_rear = 1.0 - f_front

        # Fraction in near (Yd < yd_mid) vs far
        yd_span = c.yd_max - c.yd_min
        if yd_span == 0:
            f_near = 1.0 if c.yd_cg < yd_mid else 0.0
        else:
            near_len = max(0, min(c.yd_max, yd_mid) - c.yd_min)
            f_near = near_len / yd_span
        f_far = 1.0 - f_near

        w = c.weight_kg
        quads["front_near"] += w * f_front * f_near
        quads["front_far"]  += w * f_front * f_far
        quads["rear_near"]  += w * f_rear * f_near
        quads["rear_far"]   += w * f_rear * f_far
    return quads


def compute_splits(quads, total):
    """Compute front/rear and near/far percentage splits."""
    front = quads["front_near"] + quads["front_far"]
    rear = quads["rear_near"] + quads["rear_far"]
    near = quads["front_near"] + quads["rear_near"]
    far = quads["front_far"] + quads["rear_far"]
    return {
        "front_pct": 100 * front / total if total else 0,
        "rear_pct": 100 * rear / total if total else 0,
        "near_pct": 100 * near / total if total else 0,
        "far_pct": 100 * far / total if total else 0,
    }


# ═══════════════════════════════════════════════════════════════════════════
# Diagram helpers
# ═══════════════════════════════════════════════════════════════════════════

_FONT = {"fontfamily": "monospace"}

# Scale: 1mm → 1 data unit (plan view uses mm directly)
def _draw_container_outline(ax):
    """Draw container outline and axes."""
    ax.add_patch(Rectangle((0, 0), C_LEN, C_WID,
                 fc="white", ec=C_OUT, lw=2, zorder=1))
    # Quadrant dividers
    x_mid = C_LEN / 2
    yd_mid = C_WID / 2
    ax.plot([x_mid, x_mid], [0, C_WID], color="#CCCCCC", lw=0.5,
            ls="--", zorder=2)
    ax.plot([0, C_LEN], [yd_mid, yd_mid], color="#CCCCCC", lw=0.5,
            ls="--", zorder=2)


WALL_T = 40   # container end-wall thickness (mm)
DOOR_T = 60   # ISO door leaf thickness (schematic, mm)
C_DOOR = "#9CA0A8"  # door fill color


def _draw_cargo_doors(ax, closed=True):
    """Draw ISO cargo doors at X=0 end — closed or open against sides."""
    if closed:
        # Two door leaves closed across the opening
        ax.add_patch(Rectangle((-WALL_T - DOOR_T, 0), DOOR_T, C_WID / 2,
                     fc=C_DOOR, ec=C_OUT, lw=1.0, zorder=4))
        ax.add_patch(Rectangle((-WALL_T - DOOR_T, C_WID / 2), DOOR_T,
                     C_WID / 2,
                     fc=C_DOOR, ec=C_OUT, lw=1.0, zorder=4))
        ax.text(-WALL_T - DOOR_T / 2, C_WID / 2,
                "DOORS\nCLOSED", ha="center", va="center",
                fontsize=5, color=C_OUT, fontweight="bold", zorder=5,
                **_FONT)
    else:
        # Doors swung open flat against the container side walls
        # Near-side door (Yd < 0)
        ax.add_patch(Rectangle((0, -WALL_T - DOOR_T),
                     C_WID / 2 + WALL_T, DOOR_T,
                     fc=C_DOOR, ec=C_OUT, lw=1.0, zorder=4))
        # Far-side door (Yd > C_WID)
        ax.add_patch(Rectangle((0, C_WID + WALL_T),
                     C_WID / 2 + WALL_T, DOOR_T,
                     fc=C_DOOR, ec=C_OUT, lw=1.0, zorder=4))
        ax.text(-60, C_WID / 2, "DOORS\nOPEN", ha="right", va="center",
                fontsize=5, color=C_DIM, style="italic", zorder=3, **_FONT)
    # Wall thickness at cargo door end
    ax.add_patch(Rectangle((-WALL_T, 0), WALL_T, C_WID,
                 fc=C_WALL, ec=C_OUT, lw=0.8, alpha=0.5, zorder=3))


def _draw_component(ax, c, *, alpha=0.6, show_label=True, fs=5.0,
                    label_offset=None, zorder=5):
    """Draw a component as a colored rectangle."""
    w = c.x_max - c.x_min
    h = c.yd_max - c.yd_min
    if w < 1 or h < 1:
        return
    ax.add_patch(Rectangle((c.x_min, c.yd_min), w, h,
                 fc=c.color, ec=C_OUT, lw=0.6, alpha=alpha, zorder=zorder))
    if show_label:
        label = f"{c.name}\n{c.weight_kg:.0f} kg"
        # Only show label if rectangle is big enough
        if w > 200 and h > 150:
            ax.text(c.x_cg, c.yd_cg, label, ha="center", va="center",
                    fontsize=fs, color=C_OUT, zorder=10, **_FONT)


def _draw_cg_marker(ax, x, yd, *, color="red", size=80, label=None, fs=7):
    """Draw a CG crosshair marker."""
    ax.plot(x, yd, "x", color=color, ms=size / 10, mew=2.5, zorder=20)
    ax.plot(x, yd, "o", color=color, ms=size / 8, mew=1.5,
            fillstyle="none", zorder=20)
    if label:
        ax.text(x, yd - 120, label, ha="center", va="top",
                fontsize=fs, color=color, fontweight="bold",
                zorder=20, **_FONT)


def _draw_quadrant_labels(ax, quads, total):
    """Label each quadrant with weight and percentage."""
    x_mid = C_LEN / 2
    yd_mid = C_WID / 2
    positions = {
        "front_near": (x_mid * 0.35, yd_mid * 0.25),
        "front_far":  (x_mid * 0.35, yd_mid + yd_mid * 0.75),
        "rear_near":  (x_mid + x_mid * 0.65, yd_mid * 0.25),
        "rear_far":   (x_mid + x_mid * 0.65, yd_mid + yd_mid * 0.75),
    }
    labels = {
        "front_near": "FRONT\nNEAR",
        "front_far":  "FRONT\nFAR",
        "rear_near":  "REAR\nNEAR",
        "rear_far":   "REAR\nFAR",
    }
    for key, (x, y) in positions.items():
        w = quads[key]
        pct = 100 * w / total if total else 0
        txt = f"{labels[key]}\n{w:,.0f} kg\n({pct:.1f}%)"
        ax.text(x, y, txt, ha="center", va="center",
                fontsize=7, color=C_DIM, fontweight="bold",
                zorder=25, **_FONT,
                bbox=dict(fc="white", ec="#CCCCCC", alpha=0.85, pad=3))


# ═══════════════════════════════════════════════════════════════════════════
# Sheet generators
# ═══════════════════════════════════════════════════════════════════════════

def sheet_dry(components):
    """Sheet 2: Weight Distribution — Dry, configured for transport."""
    fig, ax = plt.subplots(figsize=(18, 10))
    total_dry, x_cg, yd_cg, z_cg = _draw_state_diagram(
        ax, components, "dry", "DRY (TRANSPORT)")

    # Leader labels for ALL non-container/non-liquid components
    dry = [c for c in filter_state(components, "dry")
           if c.category not in ("liquid", "container")]
    near_comps = sorted([c for c in dry if c.yd_cg < C_WID / 2],
                        key=lambda c: c.x_cg)
    far_comps = sorted([c for c in dry if c.yd_cg >= C_WID / 2],
                       key=lambda c: c.x_cg)

    # Near-side labels below the container
    tip_x_nudge = {"Near walkway": 0.05}
    base_y_below = -125
    n_near = max(len(near_comps), 1)
    spacing_near = min(C_LEN / n_near, 800)
    start_near = (C_LEN - spacing_near * (n_near - 1)) / 2
    for i, c in enumerate(near_comps):
        lbl = f"{c.name}: {c.weight_kg:.0f} kg"
        tip_x = c.x_cg + tip_x_nudge.get(c.name, 0) * C_LEN
        lx = start_near + i * spacing_near
        ly = base_y_below - (i % 3) * 125
        leader(ax, tip_x, c.yd_cg, lx, ly, lbl,
               fs=5, color=C_DIM, ha="center", va="top", lw=0.5)

    # Far-side labels above the container
    base_y_above = C_WID + 125
    n_far = max(len(far_comps), 1)
    spacing_far = min(C_LEN / n_far, 800)
    start_far = (C_LEN - spacing_far * (n_far - 1)) / 2
    for i, c in enumerate(far_comps):
        lbl = f"{c.name}: {c.weight_kg:.0f} kg"
        lx = start_far + i * spacing_far
        ly = base_y_above + (i % 3) * 125
        leader(ax, c.x_cg, c.yd_cg, lx, ly, lbl,
               fs=5, color=C_DIM, ha="center", va="bottom", lw=0.5)

    # Replace the default info box with a more detailed summary
    # (draw over the one placed by _draw_state_diagram)
    info = (f"DRY WEIGHT SUMMARY\n"
            f"Container tare: 2,200 kg\n"
            f"Equipment + structure: {total_dry - 2200:,.0f} kg\n"
            f"Total dry: {total_dry:,.0f} kg\n"
            f"CG: X={x_cg:.0f}, Yd={yd_cg:.0f}\n"
            f"Z_cg: {z_cg:.0f}mm\n"
            f"ISO max gross: 24,000 kg → margin: {24000 - total_dry:,.0f} kg")
    ax.text(C_LEN + 100, C_WID * 0.5, info, fontsize=7, color=C_OUT,
            va="center", ha="left", **_FONT,
            bbox=dict(fc="white", ec=C_OUT, lw=0.8, pad=6))

    ax.set_xlim(-400, C_LEN + 500)
    ax.set_ylim(-1000, C_WID + 500)
    ax.set_aspect("equal")
    ax.set_xlabel("X (mm) — 0 = cargo door end", fontsize=8, **_FONT)
    ax.set_ylabel("Yd (mm) — 0 = pinhole wall", fontsize=8, **_FONT)
    ax.tick_params(labelsize=6)

    title_block(ax, "SHEET 2 OF 5",
                drawing_title="WEIGHT ANALYSIS",
                subtitle="WEIGHT DISTRIBUTION — DRY (CONFIGURED FOR TRANSPORT)",
                scale_note="NOT TO SCALE",
                doc_id="TBS-001 · Weight Distribution",
                height=0.065)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "weight-analysis-sheet2.png"),
                dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  Sheet 2: Dry — Configured for Transport")


def _draw_state_diagram(ax, components, state, state_label):
    """Helper: draw a weight distribution diagram for one state."""
    active = filter_state(components, state)
    non_container = [c for c in active if c.category != "container"]

    _draw_container_outline(ax)
    _draw_cargo_doors(ax, closed=(state != "ready"))

    # Draw non-liquid components faded; panel/drum slightly more visible
    highlight_names = {"Hinged panel", "Light trap drum"}
    # Draw panel first, then drum on top (higher zorder), then everything else
    others = [c for c in non_container
              if c.category != "liquid" and c.name not in highlight_names]
    panel = [c for c in non_container
             if c.category != "liquid" and c.name == "Hinged panel"]
    drum = [c for c in non_container
            if c.category != "liquid" and c.name == "Light trap drum"]
    for c in panel:
        if state in ("dry", "exhausted"):
            # transport: draw the SWUNG panel band (polygon), not the swung-bbox rectangle
            t = np.radians(SWING_LOCK_DEG); cs, sn = np.cos(t), np.sin(t)
            def _sw(x, y):
                return (PIVOT_X + (x - PIVOT_X) * cs - (y - PIVOT_YD) * sn,
                        PIVOT_YD + (x - PIVOT_X) * sn + (y - PIVOT_YD) * cs)
            poly = [_sw(0, 0), _sw(80, 0), _sw(80, C_WID), _sw(0, C_WID)]
            ax.add_patch(mpatches.Polygon(poly, closed=True, fc=c.color,
                         ec=C_OUT, lw=1.0, alpha=0.5, zorder=6))
        else:
            _draw_component(ax, c, alpha=0.5, show_label=False)
    for c in drum:
        # Draw drum as circle (plan view of Ø900 housing)
        # Position: panel face + half center-zone thickness (swung for transport)
        if state in ("dry", "exhausted"):
            t = np.radians(SWING_LOCK_DEG); cs, sn = np.cos(t), np.sin(t)
            dx, dy = PANEL_CENTER_T / 2, C_WID / 2
            cx = PIVOT_X + (dx - PIVOT_X) * cs - (dy - PIVOT_YD) * sn
            cy = PIVOT_YD + (dx - PIVOT_X) * sn + (dy - PIVOT_YD) * cs
        else:
            cx, cy = PANEL_CENTER_T / 2, C_WID / 2  # deployed
        ax.add_patch(Circle((cx, cy), DRUM_R,
                     fc=C_LT_DRUM, ec=C_OUT, lw=1.2, alpha=0.7, zorder=7))
    for c in others:
        _draw_component(ax, c, alpha=0.25, show_label=False)

    # Draw liquid components highlighted
    for c in non_container:
        if c.category == "liquid":
            _draw_component(ax, c, alpha=0.6, show_label=True, fs=5.5)

    # CG and quadrants
    total, x_cg, yd_cg, z_cg = compute_cg(active)
    quads = compute_quadrants(active)
    splits = compute_splits(quads, total)

    _draw_cg_marker(ax, x_cg, yd_cg, label=f"CG ({x_cg:.0f}, {yd_cg:.0f})")

    # Geometric center for reference
    ax.plot(C_LEN / 2, C_WID / 2, "+", color="#AAAAAA", ms=10, mew=1.5,
            zorder=15)
    ax.text(C_LEN / 2, C_WID / 2 + 100, "GEO\nCENTER", ha="center",
            va="bottom", fontsize=5, color="#AAAAAA", zorder=15, **_FONT)

    _draw_quadrant_labels(ax, quads, total)

    # Edge split labels
    ax.text(C_LEN / 2, C_WID * 1.05,
            f"← FRONT {splits['front_pct']:.1f}%  |  REAR {splits['rear_pct']:.1f}% →",
            ha="center", va="top", fontsize=6, color=C_DIM,
            fontweight="bold", zorder=25, **_FONT)
    ax.text(-120, C_WID * 0.75,
            f"FAR {splits['far_pct']:.1f}%\n\nNEAR {splits['near_pct']:.1f}%",
            ha="right", va="center", fontsize=6, color=C_DIM,
            fontweight="bold", rotation=0, zorder=25, **_FONT)

    # Title info
    ax.text(C_LEN + 100, C_WID * 0.7,
            f"{state_label}\nTotal: {total:,.0f} kg\n"
            f"CG: X={x_cg:.0f}, Yd={yd_cg:.0f}\n"
            f"Z_cg: {z_cg:.0f}mm",
            fontsize=7, color=C_OUT, va="center", ha="left", **_FONT,
            bbox=dict(fc="white", ec=C_OUT, lw=0.8, pad=6))

    return total, x_cg, yd_cg, z_cg


def sheet_ready(components):
    """Sheet 3: Camera Ready state distribution."""
    fig, ax = plt.subplots(figsize=(18, 8))
    _draw_state_diagram(ax, components, "ready", "CAMERA READY")

    ax.set_xlim(-400, C_LEN + 500)
    ax.set_ylim(-500, C_WID + 200)
    ax.set_aspect("equal")
    ax.set_xlabel("X (mm)", fontsize=8, **_FONT)
    ax.set_ylabel("Yd (mm)", fontsize=8, **_FONT)
    ax.tick_params(labelsize=6)

    title_block(ax, "SHEET 3 OF 5",
                drawing_title="WEIGHT ANALYSIS",
                subtitle="WEIGHT DISTRIBUTION — CAMERA READY (PANEL DEPLOYED)",
                scale_note="NOT TO SCALE",
                doc_id="TBS-001 · Weight Distribution",
                height=0.065)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "weight-analysis-sheet3.png"),
                dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  Sheet 3: Camera Ready Distribution")


def sheet_exhausted(components):
    """Sheet 4: Materials Exhausted state distribution."""
    fig, ax = plt.subplots(figsize=(18, 8))
    total_ex, x_ex, yd_ex, z_ex = _draw_state_diagram(
        ax, components, "exhausted", "MATERIALS EXHAUSTED")

    # Show CG shift from Camera Ready state
    ready_comps = filter_state(components, "ready")
    _, x_rdy, yd_rdy, z_rdy = compute_cg(ready_comps)
    # Highlight Z shift and tray drainage
    dz = z_ex - z_rdy
    dx = x_ex - x_rdy
    note = (f"Tray drained (−59 kg)\n"
            f"CG shift: ΔX = {dx:+.0f}, ΔZ = {dz:+.0f}mm\n"
            f"(water moves top → bottom tier)")
    ax.text(C_LEN + 100, C_WID * 0.3, note,
            fontsize=7, color="orange", va="center", ha="left",
            fontweight="bold", **_FONT,
            bbox=dict(fc="#FFF8F0", ec="orange", lw=1, pad=6))

    ax.set_xlim(-400, C_LEN + 500)
    ax.set_ylim(-500, C_WID + 200)
    ax.set_aspect("equal")
    ax.set_xlabel("X (mm)", fontsize=8, **_FONT)
    ax.set_ylabel("Yd (mm)", fontsize=8, **_FONT)
    ax.tick_params(labelsize=6)

    title_block(ax, "SHEET 4 OF 5",
                drawing_title="WEIGHT ANALYSIS",
                subtitle="WEIGHT DISTRIBUTION — MATERIALS EXHAUSTED (FOR TRANSPORT)",
                scale_note="NOT TO SCALE",
                doc_id="TBS-001 · Weight Distribution",
                height=0.065)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "weight-analysis-sheet4.png"),
                dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  Sheet 4: Materials Exhausted Distribution")


def sheet_loaded_transport(components):
    """Sheet 5: Loaded Transport — camera-ready water load in transport config.

    Heaviest top-tier case while configured for the road: full Blue IBCs
    (1,200 kg) with the panel swung in and the cargo doors closed.
    """
    fig, ax = plt.subplots(figsize=(18, 8))
    total_lt, x_lt, yd_lt, z_lt = _draw_state_diagram(
        ax, components, "loaded_transport", "LOADED TRANSPORT (BLUE FULL)")

    # Same transport config as Materials Exhausted, but water is in the TOP
    # tier — so the same X-CG with a much higher vertical CG (worst transport Z).
    exh_comps = filter_state(components, "exhausted")
    _, _, _, z_exh = compute_cg(exh_comps)
    note = (f"Full Blue IBCs (1,200 kg, TOP tier) in\n"
            f"transport config (panel swung in, doors closed).\n"
            f"Highest-CG transport case — governs\n"
            f"road-transport stability.\n"
            f"ΔZ vs Materials Exhausted = {z_lt - z_exh:+.0f}mm\n"
            f"(top tier vs bottom tier)")
    ax.text(C_LEN + 100, C_WID * 0.3, note,
            fontsize=7, color="#1A6FB0", va="center", ha="left",
            fontweight="bold", **_FONT,
            bbox=dict(fc="#F0F6FC", ec="#1A6FB0", lw=1, pad=6))

    ax.set_xlim(-400, C_LEN + 500)
    ax.set_ylim(-500, C_WID + 200)
    ax.set_aspect("equal")
    ax.set_xlabel("X (mm)", fontsize=8, **_FONT)
    ax.set_ylabel("Yd (mm)", fontsize=8, **_FONT)
    ax.tick_params(labelsize=6)

    title_block(ax, "SHEET 5 OF 5",
                drawing_title="WEIGHT ANALYSIS",
                subtitle="WEIGHT DISTRIBUTION — LOADED TRANSPORT (FULL BLUE IBCs)",
                scale_note="NOT TO SCALE",
                doc_id="TBS-001 · Weight Distribution",
                height=0.065)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "weight-analysis-sheet5.png"),
                dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  Sheet 5: Loaded Transport (Full Blue IBCs)")


def sheet_summary(components):
    """Sheet 1: Summary comparison — three states side by side."""
    from matplotlib.gridspec import GridSpec

    fig = plt.figure(figsize=(26, 8))
    gs = GridSpec(3, 4, figure=fig, height_ratios=[6, 2, 1],
                 hspace=0.15, wspace=0.25)

    # Top row: 4 plan views
    plan_axes = [fig.add_subplot(gs[0, i]) for i in range(4)]
    # Middle row: summary table spanning all columns
    ax_table = fig.add_subplot(gs[1, :])
    # Bottom row: title block spanning all columns
    ax_tb = fig.add_subplot(gs[2, :])

    states = [
        ("dry", "DRY\n(Transport)", "#808080"),
        ("loaded_transport", "LOADED TRANSPORT\n(Full Blue IBCs)", "#1A6FB0"),
        ("ready", "CAMERA READY\n(Full Blue IBCs)", C_BLUE_IBC),
        ("exhausted", "MATERIALS\nEXHAUSTED (Transport)", C_BROWN_IBC),
    ]

    cg_points = []

    for ax, (state, label, accent) in zip(plan_axes, states):
        active = filter_state(components, state)
        total, x_cg, yd_cg, z_cg = compute_cg(active)
        quads = compute_quadrants(active)
        splits = compute_splits(quads, total)
        cg_points.append((x_cg, yd_cg, z_cg, total))

        # Draw container outline and cargo doors
        _draw_container_outline(ax)
        _draw_cargo_doors(ax, closed=(state != "ready"))

        # Quadrant lines
        ax.plot([C_LEN / 2, C_LEN / 2], [0, C_WID], color="#DDDDDD",
                lw=0.5, ls="--", zorder=2)
        ax.plot([0, C_LEN], [C_WID / 2, C_WID / 2], color="#DDDDDD",
                lw=0.5, ls="--", zorder=2)

        # Draw non-liquid, non-container components faded
        # Separate panel and drum for special rendering
        highlight_names = {"Hinged panel", "Light trap drum"}
        non_cont = [c for c in active
                    if c.category not in ("container", "liquid")]
        for c in non_cont:
            if c.name in highlight_names:
                continue
            w = c.x_max - c.x_min
            h = c.yd_max - c.yd_min
            if w > 0 and h > 0:
                ax.add_patch(Rectangle((c.x_min, c.yd_min), w, h,
                             fc=c.color, ec="none", alpha=0.2, zorder=3))

        # Draw panel — swung band for transport states, box when deployed
        _swung = state in ("dry", "exhausted", "loaded_transport")
        _t = np.radians(SWING_LOCK_DEG); _cs, _sn = np.cos(_t), np.sin(_t)
        def _swpt(x, y):
            return (PIVOT_X + (x - PIVOT_X) * _cs - (y - PIVOT_YD) * _sn,
                    PIVOT_YD + (x - PIVOT_X) * _sn + (y - PIVOT_YD) * _cs)
        for c in non_cont:
            if c.name == "Hinged panel":
                if _swung:
                    poly = [_swpt(0, 0), _swpt(80, 0), _swpt(80, C_WID), _swpt(0, C_WID)]
                    ax.add_patch(mpatches.Polygon(poly, closed=True, fc=c.color,
                                 ec=C_OUT, alpha=0.4, lw=0.6, zorder=4))
                else:
                    w = c.x_max - c.x_min
                    h = c.yd_max - c.yd_min
                    if w > 0 and h > 0:
                        ax.add_patch(Rectangle((c.x_min, c.yd_min), w, h,
                                     fc=c.color, ec=C_OUT, alpha=0.4, lw=0.6,
                                     zorder=4))

        # Draw drum as circle (swung center for transport)
        for c in non_cont:
            if c.name == "Light trap drum":
                if _swung:
                    cx, cy = _swpt(PANEL_CENTER_T / 2, C_WID / 2)
                else:
                    cx, cy = PANEL_CENTER_T / 2, C_WID / 2
                ax.add_patch(Circle((cx, cy), DRUM_R,
                             fc=C_LT_DRUM, ec=C_OUT, lw=1.2, alpha=0.7,
                             zorder=5))

        # Draw liquids
        liquids = [c for c in active if c.category == "liquid"]
        for c in liquids:
            w = c.x_max - c.x_min
            h = c.yd_max - c.yd_min
            if w > 0 and h > 0:
                ax.add_patch(Rectangle((c.x_min, c.yd_min), w, h,
                             fc=c.color, ec=C_OUT, alpha=0.5, lw=0.8,
                             zorder=5))

        # CG marker
        _draw_cg_marker(ax, x_cg, yd_cg, color=accent, size=60)

        # Geometric center
        ax.plot(C_LEN / 2, C_WID / 2, "+", color="#CCCCCC", ms=8, mew=1,
                zorder=10)

        ax.set_title(label, fontsize=9, fontweight="bold", color=C_OUT,
                     **_FONT)
        ax.set_xlim(-450, C_LEN + 100)
        ax.set_ylim(-250, C_WID + 250)
        ax.set_aspect("equal")
        ax.tick_params(labelsize=5)

        # Summary below
        info = (f"Total: {total:,.0f} kg\n"
                f"CG: ({x_cg:.0f}, {yd_cg:.0f}, Z={z_cg:.0f})\n"
                f"F/R: {splits['front_pct']:.1f}/{splits['rear_pct']:.1f}%\n"
                f"N/F: {splits['near_pct']:.1f}/{splits['far_pct']:.1f}%")
        ax.text(C_LEN / 2, -650, info, ha="center", va="top",
                fontsize=6.5, color=C_OUT, **_FONT,
                bbox=dict(fc="white", ec="#CCCCCC", alpha=0.9, pad=3))

    # Summary table in middle axes
    ax_table.set_xlim(0, 1)
    ax_table.set_ylim(0, 1)
    ax_table.axis("off")

    hdr = (f"{'State':<36}  {'Total (kg)':>10}  {'X_cg (mm)':>10}  "
           f"{'Yd_cg (mm)':>10}  {'Z_cg (mm)':>10}  {'ISO margin':>12}")
    rule = "-" * len(hdr)
    table_lines = [rule, hdr, rule]
    for (state, label, _), (x_cg, yd_cg, z_cg, total) in zip(states, cg_points):
        clean_label = label.replace("\n", " ")
        margin = 24000 - total
        table_lines.append(
            f"{clean_label:<36}  {total:>10,.0f}  {x_cg:>10,.0f}  "
            f"{yd_cg:>10,.0f}  {z_cg:>10,.0f}  {margin:>12,.0f}")
    table_lines.append(rule)
    table_text = "\n".join(table_lines)
    ax_table.text(0.5, 0.5, table_text, ha="center", va="center",
                  fontsize=7.5, color=C_OUT, **_FONT,
                  bbox=dict(fc="white", ec=C_OUT, lw=0.8, pad=8))

    # Title block in bottom axes
    ax_tb.set_xlim(0, 1)
    ax_tb.set_ylim(0, 1)
    ax_tb.axis("off")
    title_block(ax_tb, "SHEET 1 OF 5",
                drawing_title="WEIGHT ANALYSIS",
                subtitle="WEIGHT DISTRIBUTION SUMMARY — FOUR STATES",
                scale_note="NOT TO SCALE",
                doc_id="TBS-001 · Weight Distribution",
                height=0.75)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "weight-analysis-sheet1.png"),
                dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  Sheet 1: Summary Comparison")


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    os.makedirs(DIAGRAMS_DIR, exist_ok=True)

    components = build_components()

    # Print weight summary
    print("\nTBS-001 Weight Analysis")
    print("=" * 70)

    # Group by category
    categories = {}
    for c in components:
        if c.category not in categories:
            categories[c.category] = []
        categories[c.category].append(c)

    for cat in ["container", "structure", "equipment", "liquid"]:
        if cat not in categories:
            continue
        items = categories[cat]
        print(f"\n{cat.upper()}")
        print("-" * 70)
        for c in items:
            states_str = ", ".join(c.states)
            print(f"  {c.name:<30} {c.weight_kg:>8.1f} kg  "
                  f"X={c.x_min:.0f}–{c.x_max:.0f}  "
                  f"Yd={c.yd_min:.0f}–{c.yd_max:.0f}  [{states_str}]")
        cat_total = sum(c.weight_kg for c in items
                        if "dry" in c.states or cat != "liquid")
        if cat != "liquid":
            print(f"  {'SUBTOTAL':<30} {cat_total:>8.1f} kg")

    # State summaries
    print("\n" + "=" * 70)
    print("STATE SUMMARIES")
    print("=" * 70)
    for state, label in [("dry", "DRY (Transport)"), ("ready", "CAMERA READY"),
                         ("exhausted", "MATERIALS EXHAUSTED (Transport)"),
                         ("loaded_transport", "LOADED TRANSPORT (Full Blue IBCs)")]:
        active = filter_state(components, state)
        total, x_cg, yd_cg, z_cg = compute_cg(active)
        quads = compute_quadrants(active)
        splits = compute_splits(quads, total)
        print(f"\n  {label}:")
        print(f"    Total weight:     {total:,.0f} kg")
        print(f"    CG position:      X={x_cg:.0f}mm, Yd={yd_cg:.0f}mm, Z={z_cg:.0f}mm")
        print(f"    Front/Rear split: {splits['front_pct']:.1f}% / "
              f"{splits['rear_pct']:.1f}%")
        print(f"    Near/Far split:   {splits['near_pct']:.1f}% / "
              f"{splits['far_pct']:.1f}%")
        print(f"    ISO 24,000 kg margin: {24000 - total:,.0f} kg "
              f"({100 * (24000 - total) / 24000:.0f}%)")

    # Generate diagrams
    print("\nGenerating diagrams...")
    sheet_summary(components)
    sheet_dry(components)
    sheet_ready(components)
    sheet_exhausted(components)
    sheet_loaded_transport(components)
    print("\nDone.")


if __name__ == "__main__":
    main()
