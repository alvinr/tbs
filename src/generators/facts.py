"""facts.py — single source of truth for cross-referenced NUMBERS restated across many MD docs.

Phase 2 of drift-reduction-plan.md. Realized as a Python module (not YAML) so the pre-commit
linter stays DEPENDENCY-FREE — PyYAML isn't installed, and a dict registry serves the same
single-source purpose. If we later want literal YAML, a tiny parser can read this shape.

Each fact carries:
  value     — the canonical value (read FROM a tbs_constants constant where one exists, so the
              registry can never disagree with the code; else a literal with its derivation noted)
  unit, owner — the unit and the one doc that owns/derives the fact
  aliases   — SPECIFIC regexes for the shapes the number takes in prose; group(1) captures the
              value. lint.py's facts-agreement check flags any doc whose captured value != `value`.

Keep aliases tight (low false-positive). Add facts as we find more restated numbers.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tbs_constants as K  # noqa: E402


FACTS = {
    # The Option-A film-plane envelope — drifted across 6 docs this session (±42/±25.7/±28.3).
    "film_plane_max_tilt": {
        "value": K.MAX_TILT_DEG, "unit": "deg", "constant": "MAX_TILT_DEG",
        "owner": "film-plane-mechanism-report.md",
        "aliases": [
            r"±(\d+(?:\.\d+)?)°\s*tilt,\s*±\d+(?:\.\d+)?°\s*swing",   # combined form (film-plane only)
            r"[Ff]ilm plane max tilt\s*\|\s*±(\d+(?:\.\d+)?)°",       # CLAUDE.md constants table
            r"tilt angle[s]?\s*up to\s*±(\d+(?:\.\d+)?)°",            # film-clamp report
        ],
    },
    "film_plane_max_swing": {
        "value": K.MAX_SWING_DEG, "unit": "deg", "constant": "MAX_SWING_DEG",
        "owner": "film-plane-mechanism-report.md",
        "aliases": [
            r"±\d+(?:\.\d+)?°\s*tilt,\s*±(\d+(?:\.\d+)?)°\s*swing",
            r"[Ff]ilm plane max swing\s*\|\s*±(\d+(?:\.\d+)?)°",
            r"swing angle[s]?\s*up to\s*±(\d+(?:\.\d+)?)°",
        ],
    },
    # Prints between resupply — drifted 10 vs 13 across README/summary/water/cost-breakdown.
    # Aliases match the OPERATIONAL claim only (the "supports/Provides ~N prints" form). They
    # deliberately do NOT match the water-report's "8–10 ... on fresh Blue alone" no-recycle
    # baseline, nor "≈N prints per charge" (battery) — those are different, legitimate facts.
    "prints_per_resupply": {
        "value": 13, "unit": "prints", "constant": None,
        "owner": "water-system-report.md",
        "aliases": [
            r"(?:supports|Provides) ~?(\d+)\s+full-size prints",
            r"~?(\d+)\s+prints per resupply",
        ],
    },
    # NOTE: camera focal length (2362mm), f/1088 and pinhole Ø2.17mm are intentionally NOT here —
    # the lens-options / option-B / exposure-comparison docs legitimately discuss OTHER focal
    # lengths and pinhole sizes, so a global "must always equal X" scan false-positives. Add such
    # facts only with aliases specific enough to isolate the camera's own value.
}
