"""lint.py — TBS-001 commit-time drift linter (Phase 3 of drift-reduction-plan.md).

Runs the DETERMINISTIC drift checks as a pre-commit gate. Keep this file low-false-positive:
only hard, reproducible gates belong here — a noisy gate gets disabled. Heuristic/advisory
scans stay in `check_consistency.py` (the on-demand audit). Add a check to CHECKS each time we
trap a new drift class (the way the labeling rules grew): costing reconciliation today; table
arithmetic, facts-registry agreement, prose-vs-constant, and the 2D<->3D dependency checks next.

Exit 0 = clean, 1 = drift found.  Pre-commit blocks the commit; bypass with `git commit --no-verify`.
Run by hand any time:  python3 src/generators/lint.py
"""
from __future__ import annotations

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def _run(script: str, *args: str) -> tuple[bool, str]:
    r = subprocess.run([sys.executable, os.path.join(ROOT, script), *args],
                       capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def check_costing() -> tuple[bool, str]:
    """Phase 1: every cost total matches its computed source (costing.py)."""
    return _run("costing.py", "--check")


# Register checks here as they are built. (name, callable -> (ok, message))
CHECKS = [
    ("costing reconciliation", check_costing),
]


def main() -> int:
    print("TBS-001 drift linter")
    failed = []
    for name, fn in CHECKS:
        ok, msg = fn()
        print(f"  [{'OK  ' if ok else 'FAIL'}] {name}")
        if not ok:
            failed.append(name)
            for line in msg.splitlines():
                print("         " + line)
    if failed:
        print(f"\n✗ {len(failed)} drift check(s) failed: {', '.join(failed)}")
        print("  Commit blocked. Fix the drift, or bypass with: git commit --no-verify")
        return 1
    print("\n✓ all drift checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
