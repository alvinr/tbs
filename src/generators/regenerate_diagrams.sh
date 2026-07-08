#!/usr/bin/env bash
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
#
# regenerate_diagrams.sh — re-run every diagram generator that draws a title block, so the version
# stamp (left cell, read from RELEASE.md via tbs_version) is current. Run after a RELEASE.md version
# bump (release.sh calls this) or after a title_block change. Uses /usr/bin/python3 (matplotlib).
#
#   bash src/generators/regenerate_diagrams.sh
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="${PY:-/usr/bin/python3}"

fail=0
for f in "$SCRIPT_DIR"/generate_*.py; do
    grep -q "title_block" "$f" || continue          # only title-block diagrams carry the version
    name="$(basename "$f")"
    if "$PY" "$f" >/dev/null 2>&1; then
        echo "  ok   $name"
    else
        echo "  FAIL $name"; fail=1
    fi
done
[ "$fail" -eq 0 ] && echo "✓ all title-block diagrams regenerated" || { echo "✗ some generators failed"; exit 1; }
