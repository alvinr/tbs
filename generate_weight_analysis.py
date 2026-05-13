#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
generate_weight_analysis.py — Weight distribution analysis for TBS-001.

Computes total weight and center-of-gravity position for three operational
states (Dry, Camera Ready, Materials Exhausted). Generates four diagram
sheets showing component positions and weight distribution.

Outputs
-------
diagrams/weight-analysis-sheet1.png  — Component weight map (plan view)
diagrams/weight-analysis-sheet2.png  — Camera Ready state distribution
diagrams/weight-analysis-sheet3.png  — Materials Exhausted state distribution
diagrams/weight-analysis-sheet4.png  — Summary comparison (3 states)
"""

import os
from dataclasses import dataclass, field

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

from tbs_constants import (
    C_LEN, C_WID, C_HGT,
    FP_X_L, FP_X_R, FP_W, FP_Y, FP_H,
    FP_ANGLE_LEG, FP_ANGLE_T, CLAMP_N_TOTAL,
    PH_X, PH_H,
    RAIL_X_L, RAIL_X_R, RAIL_SPAN, RAIL_LEN,
    IBC_COL_X, IBC_W, IBC_D, IBC_H_600, IBC_H_STK,
    BLUE_IBC_Y, BROWN_IBC_Y, IBC_FAR_Y, WASTE_IBC_Y,
    PROC_TRAY_X_L, PROC_TRAY_X_R, PROC_TRAY_W, PROC_TRAY_D,
    PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR, PROC_TRAY_RIM,
    WALKWAY_W, WALKWAY_H, WALKWAY_GRATE_T,
    WALKWAY_BRACKET_H, WALKWAY_BRACKET_T, WALKWAY_BRACKET_SPACING,
    WALKWAY_RIGHT_BOX_X, WALKWAY_RIGHT_BOX_W, WALKWAY_RIGHT_BOX_H,
    WALKWAY_RIGHT_BOX_T, WALKWAY_LEFT_X, WALKWAY_LEFT_SPAN,
    LEFT_WK_BEARER_SIZE, LEFT_WK_BEARER_T, LEFT_WK_LEG_N,
    EVAP_X, EVAP_W, EVAP_Y, EVAP_D,
    EP_X, EP_W, BA_X, BA_W, PUMP_X, PUMP_W,
    PANEL_CORNER_T, PANEL_CENTER_T,
    PANEL_CORNER_YD_L, PANEL_CORNER_YD_R,
    DRUM_D, DRUM_H_LT,
    FAN_DIAM, FAN_A_YD, FAN_B_YD,
    C_OUT, C_DIM, C_STEEL, C_ALUM,
    C_BLUE_IBC, C_BROWN_IBC, C_WASTE_IBC,
    C_EVAP, C_ELEC, C_BATT, C_PUMP,
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

# ── Grating weight ──────────────────────────────────────────────────────────
# 25mm press-locked galvanized steel bar grating, 30×100mm bearing bar pitch.
# Source: McNICHOLS catalog, standard industrial grating.
GRATING_KG_PER_M2 = 44.0

# ── IBC empty weight ────────────────────────────────────────────────────────
# Schutz Ecobulk MX 600L steel-cage IBC: ~55 kg tare.
IBC_EMPTY_KG = 55.0


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
    states: tuple = ("dry", "ready", "exhausted")  # which states include this
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


# ═══════════════════════════════════════════════════════════════════════════
# Weight calculations — all from first principles
# ═══════════════════════════════════════════════════════════════════════════

def _panel_weight():
    """Hinged panel: stepped sandwich construction.
    Corner zones (2×): 18mm ply + 4mm steel + 18mm ply = 40mm thick.
    Center zone: 50×50mm RHS frame + 18mm ply skins = 120mm thick.
    Report value: 220-260 kg combined with drum (light-trap-selection.md line 199).
    Use midpoint 240 kg for panel+drum, then split based on calculation.
    """
    panel_h = C_HGT  # 2388mm
    # Corner zones
    corner_w_near = PANEL_CORNER_YD_L  # 756mm
    corner_w_far = C_WID - PANEL_CORNER_YD_R  # 756mm
    # Each corner: 2 ply skins + 1 steel plate
    ply_vol_corner = 2 * (corner_w_near * panel_h * 18e-9)  # m³ per side, 2 sides
    ply_vol_corner *= 2  # near + far corners
    steel_vol_corner = 2 * (corner_w_near * panel_h * 4e-9)  # 4mm plate, 2 corners
    corner_ply_kg = ply_vol_corner * RHO_PLY
    corner_steel_kg = steel_vol_corner * RHO_STEEL
    # Center zone: RHS frame perimeter + cross members
    # 50×50×3mm RHS: ~4.25 kg/m (steel RHS)
    rhs_kg_per_m = 4 * (50 * 3 - 4 * 3 * 3) * 1e-6 * RHO_STEEL  # ≈ 4.25 kg/m
    # Perimeter: 2 × (850mm + 2388mm) + ~4 cross members × 850mm
    center_frame_length = 2 * (0.850 + 2.388) + 4 * 0.850  # ≈ 9.876 m
    frame_kg = center_frame_length * rhs_kg_per_m
    # Center ply skins: 2 × 850 × 2388 × 18mm
    center_ply_kg = 2 * (0.850 * 2.388 * 0.018) * RHO_PLY
    panel_kg = corner_ply_kg + corner_steel_kg + frame_kg + center_ply_kg
    return panel_kg


def _drum_weight():
    """Revolving light-trap drum: Ø750mm × 2200mm tall.
    1.5mm aluminum shell + 3 internal baffles (1.5mm Al) + bearings.
    """
    # Shell: cylinder surface area × 1.5mm
    shell_area = np.pi * (DRUM_D / 1000) * (DRUM_H_LT / 1000)  # m²
    shell_kg = shell_area * 0.0015 * RHO_ALUM
    # 3 baffles: approximate as flat plates spanning diameter × height
    baffle_kg = 3 * (DRUM_D / 1000) * (DRUM_H_LT / 1000) * 0.0015 * RHO_ALUM
    # Bearings + hardware
    hardware_kg = 8.0
    return shell_kg + baffle_kg + hardware_kg


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
    """Right walkway (IBC end): box section beam + grating."""
    # Box section: 50×40×3mm RHS, spanning 2362mm
    rhs_perim = 2 * (50 + 40) - 4 * 3  # inner perimeter approx
    rhs_area = (2 * (50 + 40) * 3 - 4 * 3 * 3) * 1e-6  # m² cross-section
    beam_kg = rhs_area * (C_WID / 1000) * RHO_STEEL
    # Packer shim: 17mm steel plate, ~300mm wide × 2362mm
    packer_kg = 0.300 * (C_WID / 1000) * 0.017 * RHO_STEEL
    # Grating
    grate_area = (WALKWAY_W / 1000) * (C_WID / 1000)
    grate_kg = grate_area * GRATING_KG_PER_M2
    return beam_kg + packer_kg + grate_kg


def _walkway_left_weight():
    """Left walkway (removable lift-out): grating + bearer beam + legs."""
    # Grating: 300mm × 2362mm
    grate_area = (WALKWAY_W / 1000) * (C_WID / 1000)
    grate_kg = grate_area * GRATING_KG_PER_M2
    # Bearer beam: 50×50×3mm Al RHS, 1762mm
    bearer_perim_area = (2 * (50 + 50) * 3 - 4 * 3 * 3) * 1e-6  # m²
    bearer_kg = bearer_perim_area * (WALKWAY_LEFT_SPAN / 1000) * RHO_ALUM
    # 3 support legs: 25×25×3mm Al SHS, ~75mm tall each + base plates
    leg_area = (4 * 25 * 3 - 4 * 3 * 3) * 1e-6
    leg_kg = LEFT_WK_LEG_N * leg_area * 0.075 * RHO_ALUM
    # Bearing strip: 25×25×3mm Al angle, ~2362mm
    strip_kg = (2 * 25 * 3 - 3 * 3) * 1e-6 * (C_WID / 1000) * RHO_ALUM
    return grate_kg + bearer_kg + leg_kg + strip_kg


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


def _processing_tray_water_kg():
    """Water in processing tray at 6mm flood depth."""
    area_m2 = (PROC_TRAY_W / 1000) * (PROC_TRAY_D / 1000)
    vol_m3 = area_m2 * 0.006  # 6mm flood depth
    return vol_m3 * RHO_WATER  # ≈ 59 kg


def _ceiling_rail_weight():
    """2× HGR20 rails full container length + 8 carriage blocks."""
    # HGR20: ~3.7 kg/m
    rail_kg = 2 * (C_LEN / 1000) * 3.7
    # 8× HGH20CA blocks: ~0.5 kg each
    block_kg = 8 * 0.5
    return rail_kg + block_kg


def _ibc_stacking_frame_weight():
    """Steel tube stacking frame for 2×2 IBC configuration.
    40×40×3mm steel SHS frame supporting top-tier IBCs.
    """
    # Rectangular frame: 2 × (1219 + 2 × 1016) mm in steel SHS
    # Plus 2 cross members
    frame_length = 2 * (IBC_W / 1000) + 4 * (IBC_D / 1000) + 2 * (IBC_W / 1000)
    # 40×40×3mm SHS: ~3.45 kg/m
    shs_kg_per_m = (4 * 40 * 3 - 4 * 3 * 3) * 1e-6 * RHO_STEEL  # ≈ 3.45 kg/m
    return frame_length * shs_kg_per_m


# ═══════════════════════════════════════════════════════════════════════════
# Component inventory
# ═══════════════════════════════════════════════════════════════════════════

def build_components():
    """Build the complete component list with calculated weights."""

    panel_kg = _panel_weight()
    drum_kg = _drum_weight()
    panel_drum_total = panel_kg + drum_kg
    # Scale to match report range (220-260 kg) if our calculation differs
    # Use report midpoint as authoritative
    report_midpoint = 240.0
    if panel_drum_total > 0:
        scale = report_midpoint / panel_drum_total
        panel_kg *= scale
        drum_kg *= scale

    near_far_wk = _walkway_near_far_weight()
    right_wk = _walkway_right_weight()
    left_wk = _walkway_left_weight()

    components = [
        # ── Container ────────────────────────────────────────────────────
        Component("Container shell", "container", 2200.0,
                  0, C_LEN, 0, C_WID, 0, C_HGT, color=C_WALL,
                  calc_note="Hapag-Lloyd 20ft ISO tare weight"),

        # ── Structure ────────────────────────────────────────────────────
        Component("Hinged panel", "structure", panel_kg,
                  0, 80, 0, C_WID, 0, C_HGT, color=C_HINGE_PANEL,
                  calc_note="Stepped sandwich: ply+steel corners, RHS center"),
        Component("Light trap drum", "structure", drum_kg,
                  0, 40, PANEL_CORNER_YD_L, PANEL_CORNER_YD_R,
                  0, DRUM_H_LT, color=C_LT_DRUM,
                  calc_note="1.5mm Al shell + 3 baffles + bearings"),
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
                  WALKWAY_RIGHT_BOX_X, WALKWAY_RIGHT_BOX_X + WALKWAY_W,
                  0, C_WID, 0, WALKWAY_H, color=C_STEEL,
                  calc_note="50×40×3 RHS beam + packer + grating"),
        Component("Left walkway", "structure", left_wk,
                  WALKWAY_LEFT_X, WALKWAY_LEFT_X + WALKWAY_W,
                  0, C_WID, 0, WALKWAY_H, color="#80C080",
                  calc_note="Removable lift-out: grating + bearer + legs"),
        Component("Ceiling rails", "structure", _ceiling_rail_weight(),
                  0, C_LEN, 30, C_WID - 30,
                  C_HGT - 30, C_HGT, color=C_ALUM,
                  calc_note="2× HGR20 @ 3.7 kg/m + 8 carriages"),
        Component("Container mods", "structure", 65.0,
                  0, C_LEN, 0, C_WID, 0, C_HGT, color=C_WALL,
                  calc_note="Light seal foam + reinforcement plates (estimate)"),

        # ── Equipment ────────────────────────────────────────────────────
        Component("Electrical panel", "equipment", 15.0,
                  EP_X, EP_X + EP_W, 0, 150,
                  900, 1500, color=C_ELEC,
                  calc_note="Wall-mount distribution panel"),
        Component("Battery bank", "equipment", 26.0,
                  BA_X, BA_X + BA_W, 0, 150,
                  100, 600, color=C_BATT,
                  calc_note="2× 100Ah LiFePO4 @ 13 kg each"),
        Component("Solar controller", "equipment", 2.0,
                  1700, 1800, 0, 100,
                  1200, 1400, color=C_BATT,
                  calc_note="MPPT charge controller"),
        Component("Pump manifold", "equipment", 4.5,
                  PUMP_X, PUMP_X + PUMP_W, 0, 150,
                  200, 600, color=C_PUMP,
                  calc_note="3× 12V diaphragm pumps + manifold"),
        Component("Evaporative cooler", "equipment", 15.0,
                  EVAP_X, EVAP_X + EVAP_W, EVAP_Y, EVAP_Y + EVAP_D,
                  0, 800, color=C_EVAP,
                  calc_note="Portable evap cooler unit"),
        Component("Film plane carriage", "equipment",
                  _film_plane_carriage_weight(),
                  FP_X_L, FP_X_R, FP_Y - 50, FP_Y + 50,
                  100, C_HGT - 100, color=C_ALUM,
                  calc_note="Al angle frame + 92 clamps + 4 carriages"),
        Component("Tilt-swing board", "equipment", 30.0,
                  PH_X - 200, PH_X + 200, 0, 400,
                  PH_H - 200, PH_H + 200, color="#CC6600",
                  calc_note="Spherical-pivot board + adjustment screws"),
        Component("Fan A (intake)", "equipment", 2.0,
                  C_LEN - 50, C_LEN, FAN_A_YD - 75, FAN_A_YD + 75,
                  525, 675, color=C_FAN,
                  calc_note="150mm axial fan"),
        Component("Fan B (exhaust)", "equipment", 2.0,
                  0, 50, FAN_B_YD - 75, FAN_B_YD + 75,
                  1725, 1875, color=C_FAN,
                  calc_note="150mm axial fan on panel"),
        Component("Baffle ducts", "equipment", 6.0,
                  0, C_LEN, 0, C_WID,
                  400, 800, color=C_FAN,
                  calc_note="2× galvanized steel baffle ducts @ 3 kg"),

        # ── IBC totes (empty) — Blue on top, Brown/Waste on bottom ──────
        Component("Blue IBC-1 (tote)", "equipment", IBC_EMPTY_KG,
                  IBC_COL_X, IBC_COL_X + IBC_W,
                  BLUE_IBC_Y, BLUE_IBC_Y + IBC_D,
                  IBC_H_600, IBC_H_STK, color=C_BLUE_IBC,
                  calc_note="600L steel-cage IBC tare (top tier)"),
        Component("Blue IBC-2 (tote)", "equipment", IBC_EMPTY_KG,
                  IBC_COL_X, IBC_COL_X + IBC_W,
                  IBC_FAR_Y, IBC_FAR_Y + IBC_D,
                  IBC_H_600, IBC_H_STK, color=C_BLUE_IBC,
                  calc_note="600L steel-cage IBC tare (top tier)"),
        Component("Brown IBC-3 (tote)", "equipment", IBC_EMPTY_KG,
                  IBC_COL_X, IBC_COL_X + IBC_W,
                  BROWN_IBC_Y, BROWN_IBC_Y + IBC_D,
                  0, IBC_H_600, color=C_BROWN_IBC,
                  calc_note="600L steel-cage IBC tare (bottom tier)"),
        Component("Waste IBC-4 (tote)", "equipment", IBC_EMPTY_KG,
                  IBC_COL_X, IBC_COL_X + IBC_W,
                  WASTE_IBC_Y, WASTE_IBC_Y + IBC_D,
                  0, IBC_H_600, color=C_WASTE_IBC,
                  calc_note="600L steel-cage IBC tare (bottom tier)"),
        Component("IBC stacking frame", "equipment",
                  _ibc_stacking_frame_weight(),
                  IBC_COL_X, IBC_COL_X + IBC_W,
                  BLUE_IBC_Y, IBC_FAR_Y + IBC_D,
                  IBC_H_600 - 50, IBC_H_600, color=C_STEEL,
                  calc_note="40×40×3mm steel SHS frame"),

        # ── Liquids — Camera Ready state (water in top-tier Blue IBCs) ───
        Component("Blue IBC-1 water", "liquid", 600.0,
                  IBC_COL_X, IBC_COL_X + IBC_W,
                  BLUE_IBC_Y, BLUE_IBC_Y + IBC_D,
                  IBC_H_600, IBC_H_STK, color=C_BLUE_IBC,
                  states=("ready",),
                  calc_note="600L clean wash water (top tier)"),
        Component("Blue IBC-2 water", "liquid", 600.0,
                  IBC_COL_X, IBC_COL_X + IBC_W,
                  IBC_FAR_Y, IBC_FAR_Y + IBC_D,
                  IBC_H_600, IBC_H_STK, color=C_BLUE_IBC,
                  states=("ready",),
                  calc_note="600L clean wash water (top tier)"),
        Component("Tray water (ready)", "liquid", _processing_tray_water_kg(),
                  PROC_TRAY_X_L, PROC_TRAY_X_R,
                  PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR,
                  0, 6, color="#80C0FF",
                  states=("ready",),
                  calc_note="6mm flood depth over tray area"),

        # ── Liquids — Materials Exhausted (water in bottom-tier IBCs) ────
        Component("Brown IBC-3 water", "liquid", 600.0,
                  IBC_COL_X, IBC_COL_X + IBC_W,
                  BROWN_IBC_Y, BROWN_IBC_Y + IBC_D,
                  0, IBC_H_600, color=C_BROWN_IBC,
                  states=("exhausted",),
                  calc_note="600L recycled water (bottom tier)"),
        Component("Waste IBC-4 water", "liquid", 600.0,
                  IBC_COL_X, IBC_COL_X + IBC_W,
                  WASTE_IBC_Y, WASTE_IBC_Y + IBC_D,
                  0, IBC_H_600, color=C_WASTE_IBC,
                  states=("exhausted",),
                  calc_note="600L waste water (bottom tier)"),
        Component("Tray water (exhausted)", "liquid",
                  _processing_tray_water_kg(),
                  PROC_TRAY_X_L, PROC_TRAY_X_R,
                  PROC_TRAY_YD_NEAR, PROC_TRAY_YD_FAR,
                  0, 6, color="#80C0FF",
                  states=("exhausted",),
                  calc_note="6mm flood depth (final processing)"),
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


def _draw_component(ax, c, *, alpha=0.6, show_label=True, fs=5.0,
                    label_offset=None):
    """Draw a component as a colored rectangle."""
    w = c.x_max - c.x_min
    h = c.yd_max - c.yd_min
    if w < 1 or h < 1:
        return
    ax.add_patch(Rectangle((c.x_min, c.yd_min), w, h,
                 fc=c.color, ec=C_OUT, lw=0.6, alpha=alpha, zorder=5))
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

def sheet1(components):
    """Sheet 1: Component Weight Map — plan view with all dry components."""
    dry = [c for c in components
           if c.category != "liquid" and c.name != "Container shell"]

    fig, ax = plt.subplots(figsize=(18, 8))
    _draw_container_outline(ax)

    # Draw each component
    for c in dry:
        _draw_component(ax, c, alpha=0.5, fs=4.5)

    # Labels for small components via leaders
    small = [c for c in dry
             if (c.x_max - c.x_min) < 200 or (c.yd_max - c.yd_min) < 150]
    offsets = {}
    base_y = C_WID + 150
    for i, c in enumerate(small):
        label = f"{c.name}: {c.weight_kg:.1f} kg"
        target_x = c.x_cg
        target_y = c.yd_cg
        # Stagger labels above the container
        lx = 300 + (i % 6) * 900
        ly = base_y + (i // 6) * 200
        ax.annotate(label, xy=(target_x, target_y), xytext=(lx, ly),
                    fontsize=5, color=C_DIM,
                    arrowprops=dict(arrowstyle="-", color="#AAAAAA",
                                   lw=0.5, ls=":"),
                    zorder=15, **_FONT)

    # Axes setup
    ax.set_xlim(-200, C_LEN + 200)
    ax.set_ylim(-1400, C_WID + 600)
    ax.set_aspect("equal")
    ax.set_xlabel("X (mm) — 0 = cargo door end", fontsize=8, **_FONT)
    ax.set_ylabel("Yd (mm) — 0 = pinhole wall", fontsize=8, **_FONT)
    ax.tick_params(labelsize=6)

    # Totals
    total_dry, x_cg, yd_cg, z_cg = compute_cg(filter_state(components, "dry"))
    info = (f"DRY WEIGHT SUMMARY\n"
            f"Container tare: 2,200 kg\n"
            f"Equipment + structure: {total_dry - 2200:,.0f} kg\n"
            f"Total dry: {total_dry:,.0f} kg\n"
            f"CG: X={x_cg:,.0f} mm, Yd={yd_cg:,.0f} mm\n"
            f"ISO max gross: 24,000 kg → margin: {24000 - total_dry:,.0f} kg")
    ax.text(C_LEN + 100, C_WID * 0.5, info, fontsize=7, color=C_OUT,
            va="center", ha="left", **_FONT,
            bbox=dict(fc="white", ec=C_OUT, lw=0.8, pad=6))

    title_block(ax, "SHEET 1 OF 4",
                drawing_title="WEIGHT ANALYSIS",
                subtitle="COMPONENT WEIGHT MAP — PLAN VIEW",
                scale_note="NOT TO SCALE",
                doc_id="TBS-001 · Weight Distribution",
                height=0.065)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "weight-analysis-sheet1.png"),
                dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  Sheet 1: Component Weight Map")


def _draw_state_diagram(ax, components, state, state_label):
    """Helper: draw a weight distribution diagram for one state."""
    active = filter_state(components, state)
    non_container = [c for c in active if c.name != "Container shell"]

    _draw_container_outline(ax)

    # Draw non-liquid components faded
    for c in non_container:
        if c.category != "liquid":
            _draw_component(ax, c, alpha=0.25, show_label=False)

    # Draw liquid components highlighted
    for c in non_container:
        if c.category == "liquid":
            _draw_component(ax, c, alpha=0.6, show_label=True, fs=5.5)

    # CG and quadrants
    total, x_cg, yd_cg, z_cg = compute_cg(active)
    quads = compute_quadrants(active)
    splits = compute_splits(quads, total)

    _draw_cg_marker(ax, x_cg, yd_cg, label=f"CG ({x_cg:,.0f}, {yd_cg:,.0f})")

    # Geometric center for reference
    ax.plot(C_LEN / 2, C_WID / 2, "+", color="#AAAAAA", ms=10, mew=1.5,
            zorder=15)
    ax.text(C_LEN / 2, C_WID / 2 + 100, "GEO\nCENTER", ha="center",
            va="bottom", fontsize=5, color="#AAAAAA", zorder=15, **_FONT)

    _draw_quadrant_labels(ax, quads, total)

    # Edge split labels
    ax.text(C_LEN / 2, -150,
            f"← FRONT {splits['front_pct']:.1f}%  |  REAR {splits['rear_pct']:.1f}% →",
            ha="center", va="top", fontsize=7, color=C_DIM,
            fontweight="bold", zorder=25, **_FONT)
    ax.text(-150, C_WID / 2,
            f"NEAR {splits['near_pct']:.1f}%\n|\nFAR {splits['far_pct']:.1f}%",
            ha="right", va="center", fontsize=7, color=C_DIM,
            fontweight="bold", rotation=0, zorder=25, **_FONT)

    # Title info
    ax.text(C_LEN + 100, C_WID * 0.7,
            f"{state_label}\nTotal: {total:,.0f} kg\n"
            f"CG: X={x_cg:,.0f}, Yd={yd_cg:,.0f}\n"
            f"Z_cg: {z_cg:,.0f} mm",
            fontsize=7, color=C_OUT, va="center", ha="left", **_FONT,
            bbox=dict(fc="white", ec=C_OUT, lw=0.8, pad=6))

    return total, x_cg, yd_cg, z_cg


def sheet2(components):
    """Sheet 2: Camera Ready state distribution."""
    fig, ax = plt.subplots(figsize=(18, 8))
    _draw_state_diagram(ax, components, "ready", "CAMERA READY")

    ax.set_xlim(-400, C_LEN + 500)
    ax.set_ylim(-1400, C_WID + 200)
    ax.set_aspect("equal")
    ax.set_xlabel("X (mm)", fontsize=8, **_FONT)
    ax.set_ylabel("Yd (mm)", fontsize=8, **_FONT)
    ax.tick_params(labelsize=6)

    title_block(ax, "SHEET 2 OF 4",
                drawing_title="WEIGHT ANALYSIS",
                subtitle="WEIGHT DISTRIBUTION — CAMERA READY (FULL BLUE IBCs)",
                scale_note="NOT TO SCALE",
                doc_id="TBS-001 · Weight Distribution",
                height=0.065)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "weight-analysis-sheet2.png"),
                dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  Sheet 2: Camera Ready Distribution")


def sheet3(components):
    """Sheet 3: Materials Exhausted state distribution."""
    fig, ax = plt.subplots(figsize=(18, 8))
    total_ex, x_ex, yd_ex, z_ex = _draw_state_diagram(
        ax, components, "exhausted", "MATERIALS EXHAUSTED")

    # Show CG shift from Camera Ready state
    ready_comps = filter_state(components, "ready")
    _, x_rdy, yd_rdy, z_rdy = compute_cg(ready_comps)
    # X-Yd CG is identical (IBCs stack vertically); highlight Z shift
    dz = z_ex - z_rdy
    note = (f"X-Yd CG unchanged\n"
            f"Vertical CG shift: ΔZ = {dz:+.0f} mm\n"
            f"(water moves top → bottom tier)")
    ax.text(C_LEN + 100, C_WID * 0.3, note,
            fontsize=7, color="orange", va="center", ha="left",
            fontweight="bold", **_FONT,
            bbox=dict(fc="#FFF8F0", ec="orange", lw=1, pad=6))

    ax.set_xlim(-400, C_LEN + 500)
    ax.set_ylim(-1400, C_WID + 200)
    ax.set_aspect("equal")
    ax.set_xlabel("X (mm)", fontsize=8, **_FONT)
    ax.set_ylabel("Yd (mm)", fontsize=8, **_FONT)
    ax.tick_params(labelsize=6)

    title_block(ax, "SHEET 3 OF 4",
                drawing_title="WEIGHT ANALYSIS",
                subtitle="WEIGHT DISTRIBUTION — MATERIALS EXHAUSTED",
                scale_note="NOT TO SCALE",
                doc_id="TBS-001 · Weight Distribution",
                height=0.065)
    fig.savefig(os.path.join(DIAGRAMS_DIR, "weight-analysis-sheet3.png"),
                dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  Sheet 3: Materials Exhausted Distribution")


def sheet4(components):
    """Sheet 4: Summary comparison — three states side by side."""
    from matplotlib.gridspec import GridSpec

    fig = plt.figure(figsize=(20, 10))
    gs = GridSpec(3, 3, figure=fig, height_ratios=[6, 2, 1],
                 hspace=0.35, wspace=0.25)

    # Top row: 3 plan views
    plan_axes = [fig.add_subplot(gs[0, i]) for i in range(3)]
    # Middle row: summary table spanning all columns
    ax_table = fig.add_subplot(gs[1, :])
    # Bottom row: title block spanning all columns
    ax_tb = fig.add_subplot(gs[2, :])

    states = [
        ("dry", "DRY\n(No Liquids)", "#808080"),
        ("ready", "CAMERA READY\n(Full Blue IBCs)", C_BLUE_IBC),
        ("exhausted", "MATERIALS\nEXHAUSTED", C_BROWN_IBC),
    ]

    cg_points = []

    for ax, (state, label, accent) in zip(plan_axes, states):
        active = filter_state(components, state)
        total, x_cg, yd_cg, z_cg = compute_cg(active)
        quads = compute_quadrants(active)
        splits = compute_splits(quads, total)
        cg_points.append((x_cg, yd_cg, z_cg, total))

        # Draw container outline
        ax.add_patch(Rectangle((0, 0), C_LEN, C_WID,
                     fc="#F8F8F8", ec=C_OUT, lw=1.5, zorder=1))
        # Quadrant lines
        ax.plot([C_LEN / 2, C_LEN / 2], [0, C_WID], color="#DDDDDD",
                lw=0.5, ls="--", zorder=2)
        ax.plot([0, C_LEN], [C_WID / 2, C_WID / 2], color="#DDDDDD",
                lw=0.5, ls="--", zorder=2)

        # Draw non-liquid components faded
        non_cont = [c for c in active
                    if c.name != "Container shell" and c.category != "liquid"]
        for c in non_cont:
            w = c.x_max - c.x_min
            h = c.yd_max - c.yd_min
            if w > 0 and h > 0:
                ax.add_patch(Rectangle((c.x_min, c.yd_min), w, h,
                             fc=c.color, ec="none", alpha=0.2, zorder=3))

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
        ax.set_xlim(-100, C_LEN + 100)
        ax.set_ylim(-100, C_WID + 100)
        ax.set_aspect("equal")
        ax.tick_params(labelsize=5)

        # Summary below
        info = (f"Total: {total:,.0f} kg\n"
                f"CG: ({x_cg:,.0f}, {yd_cg:,.0f}, Z={z_cg:,.0f})\n"
                f"F/R: {splits['front_pct']:.1f}/{splits['rear_pct']:.1f}%\n"
                f"N/F: {splits['near_pct']:.1f}/{splits['far_pct']:.1f}%")
        ax.text(C_LEN / 2, -50, info, ha="center", va="top",
                fontsize=6.5, color=C_OUT, **_FONT,
                bbox=dict(fc="white", ec="#CCCCCC", alpha=0.9, pad=3))

    # Summary table in middle axes
    ax_table.set_xlim(0, 1)
    ax_table.set_ylim(0, 1)
    ax_table.axis("off")

    table_lines = [
        "─" * 90,
        f"{'State':<25} {'Total (kg)':>12} {'X_cg (mm)':>12} "
        f"{'Yd_cg (mm)':>12} {'Z_cg (mm)':>12}  {'ISO margin':>14}",
        "─" * 90,
    ]
    for (state, label, _), (x_cg, yd_cg, z_cg, total) in zip(states, cg_points):
        clean_label = label.replace("\n", " ")
        margin = 24000 - total
        table_lines.append(
            f"{clean_label:<25} {total:>12,.0f} {x_cg:>12,.0f} "
            f"{yd_cg:>12,.0f} {z_cg:>12,.0f}  {margin:>14,.0f}")
    table_lines.append("─" * 90)
    table_text = "\n".join(table_lines)
    ax_table.text(0.5, 0.5, table_text, ha="center", va="center",
                  fontsize=7.5, color=C_OUT, **_FONT,
                  bbox=dict(fc="white", ec=C_OUT, lw=0.8, pad=8))

    # Title block in bottom axes
    ax_tb.set_xlim(0, 1)
    ax_tb.set_ylim(0, 1)
    ax_tb.axis("off")
    title_block(ax_tb, "SHEET 4 OF 4",
                drawing_title="WEIGHT ANALYSIS",
                subtitle="WEIGHT DISTRIBUTION SUMMARY — THREE STATES",
                scale_note="NOT TO SCALE",
                doc_id="TBS-001 · Weight Distribution",
                height=0.75)

    fig.savefig(os.path.join(DIAGRAMS_DIR, "weight-analysis-sheet4.png"),
                dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  Sheet 4: Summary Comparison")


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
    for state, label in [("dry", "DRY"), ("ready", "CAMERA READY"),
                         ("exhausted", "MATERIALS EXHAUSTED")]:
        active = filter_state(components, state)
        total, x_cg, yd_cg, z_cg = compute_cg(active)
        quads = compute_quadrants(active)
        splits = compute_splits(quads, total)
        print(f"\n  {label}:")
        print(f"    Total weight:     {total:,.0f} kg")
        print(f"    CG position:      X={x_cg:,.0f} mm, Yd={yd_cg:,.0f} mm, Z={z_cg:,.0f} mm")
        print(f"    Front/Rear split: {splits['front_pct']:.1f}% / "
              f"{splits['rear_pct']:.1f}%")
        print(f"    Near/Far split:   {splits['near_pct']:.1f}% / "
              f"{splits['far_pct']:.1f}%")
        print(f"    ISO 24,000 kg margin: {24000 - total:,.0f} kg "
              f"({100 * (24000 - total) / 24000:.0f}%)")

    # Generate diagrams
    print("\nGenerating diagrams...")
    sheet1(components)
    sheet2(components)
    sheet3(components)
    sheet4(components)
    print("\nDone.")


if __name__ == "__main__":
    main()
