#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
tbs_title_block.py — Shared title block for all TBS-001 engineering diagrams.

Standard 3-column layout at the bottom of the axes in axes-fraction coordinates.
Reference: generate_hingepanel_diagram.py sheet 1 (18×14, PAD_B=500).

Usage
-----
    from tbs_title_block import title_block

    title_block(ax, "SHEET 1 OF 2",
                drawing_title="HINGED LIGHT-TRAP PANEL",
                subtitle="FRONT ELEVATION — EXTERIOR VIEW",
                scale_note="SCALE 1:20")
"""

from matplotlib.patches import FancyBboxPatch

# ── Palette (matches all TBS drawing helpers) ────────────────────────────────
_C_OUT = "#1A1A1A"
_C_DIM = "#404040"
_FONT  = {"fontfamily": "monospace"}


def title_block(ax, sheet_label, *, drawing_title="", subtitle="",
                scale_note="", doc_id="", height=0.045, portrait=False,
                top=False):
    """Draw a standard 3-column title block at the bottom (or top) of *ax*.

    Parameters
    ----------
    ax : matplotlib Axes
    sheet_label : str       e.g. "SHEET 1 OF 4"
    drawing_title : str     main drawing name (center cell top row)
    subtitle : str          center cell middle row (e.g. "FRONT ELEVATION")
    scale_note : str        center cell bottom row; if empty → "ALL DIMS IN mm"
    doc_id : str            left cell middle row (e.g. "TBS-001 · Hinged Panel")
    height : float          axes-fraction box height (0.045 landscape, ≥0.07 portrait)
    portrait : bool         smaller fonts for narrow portrait figures
    top : bool              place at the top of the axes instead of the bottom
    """
    t = ax.transAxes
    y0 = (0.997 - height) if top else 0.003
    h  = height
    y1 = y0 + h
    row_top = y0 + h * 0.80
    row_mid = y0 + h * 0.48
    row_bot = y0 + h * 0.18

    # Font sizes — scale down for narrow portrait figures
    if portrait:
        fs_title = 6.0
        fs_body  = 5.0
        fs_small = 4.5
        fs_sheet = 7.0
    else:
        fs_title = 7.5
        fs_body  = 6.5
        fs_small = 5.5
        fs_sheet = 7.5

    # Column boundaries (axes-fraction)
    col_L = 0.005
    div_1 = 0.30
    div_2 = 0.75
    col_R = 0.995
    cx_left   = (col_L + div_1) / 2
    cx_center = (div_1 + div_2) / 2
    cx_right  = (div_2 + col_R) / 2

    # Clip boxes — prevent text overflow between cells
    clip_left   = FancyBboxPatch((col_L, y0), div_1 - col_L, h,
                                 boxstyle="square,pad=0", transform=t)
    clip_center = FancyBboxPatch((div_1, y0), div_2 - div_1, h,
                                 boxstyle="square,pad=0", transform=t)
    clip_right  = FancyBboxPatch((div_2, y0), col_R - div_2, h,
                                 boxstyle="square,pad=0", transform=t)

    # White box with border
    ax.add_patch(FancyBboxPatch((col_L, y0), col_R - col_L, h,
                 boxstyle="square,pad=0", fc="white", ec=_C_OUT, lw=1.2,
                 transform=t, zorder=20))
    # Vertical dividers
    ax.plot([div_1, div_1], [y0, y1], color=_C_OUT, lw=0.6,
            transform=t, zorder=21)
    ax.plot([div_2, div_2], [y0, y1], color=_C_OUT, lw=0.6,
            transform=t, zorder=21)

    # ── Left cell: project info ──────────────────────────────────────────────
    left_rows = [
        ("THE BIG SHOEBOX PROJECT", row_top, fs_title,
         dict(fontweight="bold", color=_C_OUT)),
        (doc_id or "TBS-001", row_mid, fs_body, dict(color=_C_DIM)),
        ("© 2026 Alvin Richards — GNU AGPLv3", row_bot, fs_small,
         dict(color=_C_DIM, style="italic")),
    ]
    for txt, yy, fs, kw in left_rows:
        t_obj = ax.text(cx_left, yy, txt, transform=t, fontsize=fs,
                        ha="center", va="center", zorder=21, **_FONT, **kw)
        t_obj.set_clip_path(clip_left)

    # ── Center cell: drawing title ───────────────────────────────────────────
    center_top = drawing_title
    if center_top and sheet_label:
        center_top = f"{drawing_title} — {sheet_label}"
    elif not center_top:
        center_top = sheet_label

    scale_text = f"Scale: {scale_note}" if scale_note else "ALL DIMS IN mm"

    center_rows = [
        (center_top, row_top, fs_title + 0.5,
         dict(fontweight="bold", color=_C_OUT)),
        (subtitle, row_mid, fs_body, dict(color=_C_DIM)),
        (scale_text, row_bot, fs_body, dict(color=_C_DIM)),
    ]
    for txt, yy, fs, kw in center_rows:
        t_obj = ax.text(cx_center, yy, txt, transform=t, fontsize=fs,
                        ha="center", va="center", zorder=21, **_FONT, **kw)
        t_obj.set_clip_path(clip_center)

    # ── Right cell: sheet number + units ─────────────────────────────────────
    t1 = ax.text(cx_right, row_top, sheet_label, transform=t,
                 color=_C_OUT, fontsize=fs_sheet, fontweight="bold",
                 ha="center", va="center", zorder=21, **_FONT)
    t1.set_clip_path(clip_right)
    t2 = ax.text(cx_right, row_bot, "ALL DIMS IN mm", transform=t,
                 color=_C_DIM, fontsize=fs_body,
                 ha="center", va="center", zorder=21, **_FONT)
    t2.set_clip_path(clip_right)
