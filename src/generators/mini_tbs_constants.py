# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""Shared geometry constants for the TBS-002 (Mini-TBS) classroom camera.

Single source for the two-box pinhole-camera geometry, imported by BOTH the 2D
diagram generator (`generate_mini_tbs_diagram.py`) and the 3D SketchUp model
(`src/models/generate_mini_tbs_model.py`), so the drawing and the model can't
drift. All values in millimeters. Kept separate from the TBS-001
`tbs_constants.py` so the two cameras' geometry stays cleanly apart.
"""

BOX_W = 457    # mm — box width (18")
BOX_D = 457    # mm — box depth / focal length (18")
BOX_H = 406    # mm — box height (16")

FOCAL = BOX_D  # focal length = depth
PH_D = 0.794   # mm — pinhole diameter (1/32" drill bit)
F_NO = round(FOCAL / PH_D)  # f/576

MARGIN = 25    # mm — mounting margin each side
FP_W = BOX_W - 2 * MARGIN   # usable film plane width
FP_H = BOX_H - 2 * MARGIN   # usable film plane height

# Watercolor paper — standard 10 × 14" sheet, mounted landscape (14" across × 10" tall),
# centered on the film-plane panel (which is larger; the paper captures the central print).
PAPER_W = 356  # mm — paper width  (14")
PAPER_H = 254  # mm — paper height (10")

SLEEVE_D = 102        # mm — armhole diameter (4")
SLEEVE_SPACING = 230  # mm — armhole center-to-center spacing

WALL_T = 4        # mm — cardboard wall thickness (schematic)
PANEL_T = WALL_T  # mm — the panel is the box's own cardboard (cut from the prep wall)

# Prep box dimensions (same box model)
PREP_D = BOX_D  # mm — prep box depth (matches camera box)
TOTAL_D = BOX_D + PREP_D

# Panel dimensions — the cut cardboard flap in the prep-box shared wall
PANEL_W = 406   # 16" — panel width, sized to the 14" (landscape) print + margin
PANEL_H = 279   # 11" — panel height, sized to the 10×14" print
HINGE_Y_ABS = (BOX_H - PANEL_H) / 2   # center the panel on the box height -> pinhole aligns with the sheet center
