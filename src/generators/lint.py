"""lint.py — TBS-001 commit-time drift linter (Phase 3 of drift-reduction-plan.md).

Two tiers so we can add rules safely (the labeling-rules pattern):
  GATES    — deterministic, zero-false-positive checks. Failure BLOCKS the commit.
  WARNINGS — heuristic checks that surface drift candidates. Printed, but do NOT block.
             A warning graduates to a GATE once it is proven clean + low-false-positive.

Exit 0 = no gate failed, 1 = a gate failed.  Pre-commit blocks on exit 1 (bypass: --no-verify).
Heuristic *advisory* scans that aren't drift-gates live in check_consistency.py (on-demand audit).

Run by hand any time:  python3 src/generators/lint.py
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, cwd=HERE).stdout.strip() or os.path.join(HERE, "..", "..")


def _md_files() -> list[str]:
    return sorted(f for f in os.listdir(ROOT) if f.endswith(".md"))


# ── GATE: costing reconciliation ─────────────────────────────────────────────
def gate_costing() -> tuple[bool, list[str]]:
    r = subprocess.run([sys.executable, os.path.join(HERE, "costing.py"), "--check"],
                       capture_output=True, text=True)
    return r.returncode == 0, [(r.stdout + r.stderr).strip()]


# ── GATE: doc cost-tables match their costing.py generator (the block injector) ──
def gate_blocks() -> tuple[bool, list[str]]:
    r = subprocess.run([sys.executable, os.path.join(HERE, "costing.py"), "--check-blocks"],
                       capture_output=True, text=True)
    return r.returncode == 0, [(r.stdout + r.stderr).strip()]


# ── WARNING: facts-registry agreement (facts.py vs every doc) ────────────────
def warn_facts() -> tuple[bool, list[str]]:
    sys.path.insert(0, HERE)
    import facts  # noqa: E402
    issues = []
    for fname in _md_files():
        text = open(os.path.join(ROOT, fname), encoding="utf-8").read()
        for key, fact in facts.FACTS.items():
            canon = float(fact["value"])
            for pat in fact["aliases"]:
                for m in re.finditer(pat, text):
                    try:
                        got = float(m.group(1))
                    except (ValueError, IndexError):
                        continue
                    if abs(got - canon) > 1e-6:
                        line = text.count("\n", 0, m.start()) + 1
                        issues.append(f"{fname}:{line}  {key}={got} (canonical {canon:g}) "
                                      f"-> '{m.group(0).strip()}'")
    return (not issues), (issues or ["all registered facts agree across docs"])


# ── WARNING: markdown table arithmetic (every declared TOTAL = sum of its column) ──
_MONEY = re.compile(r"^\*{0,2}~?\$?([\d,]+)\*{0,2}$")


def _money(cell: str):
    m = _MONEY.match(cell.strip())
    if not m:
        return None
    try:
        return int(m.group(1).replace(",", ""))
    except ValueError:
        return None


def _cells(row: str) -> list[str]:
    return [c.strip() for c in row.strip().strip("|").split("|")]


def _check_table(fname, start, block, issues):
    rows = [_cells(r) for r in block]
    tot_idx = next((k for k, r in enumerate(rows)
                    if r and re.search(r"\btotal\b", r[0], re.I)), None)
    if tot_idx is None:
        return
    data = [r for k, r in enumerate(rows)
            if k != tot_idx and not all(set(c) <= set("-: ") for c in r)]
    if len(data) < 2:                                    # need a header + >=1 data row
        return
    for col in range(1, len(rows[tot_idx])):
        tot = _money(rows[tot_idx][col])
        if tot is None:
            continue
        vals, ok = [], True
        for r in data[1:]:                               # data[0] is the header row
            v = _money(r[col]) if col < len(r) else None
            if v is None:                                # ambiguous cell -> skip column (no FP)
                ok = False
                break
            vals.append(v)
        if not ok or not vals:
            continue
        s = sum(vals)
        if abs(s - tot) > max(round(0.01 * tot), 15):    # tolerance absorbs '~$' rounding
            issues.append(f"{fname}:{start + tot_idx + 1}  col{col}: TOTAL ${tot:,} "
                          f"!= sum ${s:,} (Δ${abs(s - tot):,})")


def warn_arithmetic() -> tuple[bool, list[str]]:
    issues = []
    for fname in _md_files():
        lines = open(os.path.join(ROOT, fname), encoding="utf-8").read().splitlines()
        i = 0
        while i < len(lines):
            if not lines[i].lstrip().startswith("|"):
                i += 1
                continue
            j = i
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                j += 1
            _check_table(fname, i, lines[i:j], issues)
            i = j
    return (not issues), (issues or ["all declared TOTAL rows reconcile with their columns"])


# ── WARNING: missing cascade (constant changed but outputs not regenerated) ──
# The 2D<->3D drift class: a tbs_constants value changes but the generators/models that read it
# aren't re-run, so the diagrams/.rb/.skp go stale. Fires only when constant-value lines are
# STAGED with no regenerated outputs also staged. Consumers are auto-derived by grep (no
# hand-maintained dependency table needed — Phase 4 can formalise it later).
_CONST = os.path.join("src", "generators", "tbs_constants.py")


def _git(args: list[str]) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, cwd=ROOT).stdout


def _grep_consumers(name: str) -> list[str]:
    out = subprocess.run(["grep", "-rlw", name, "src"], capture_output=True, text=True, cwd=ROOT).stdout
    return sorted(f for f in out.split()
                  if f.endswith(".py") and "tbs_constants" not in f and "__pycache__" not in f)


def warn_missing_cascade() -> tuple[bool, list[str]]:
    staged = _git(["diff", "--cached", "--name-only"]).split()
    if _CONST not in staged:
        return True, ["no tbs_constants change staged"]
    diff = _git(["diff", "--cached", "-U0", "--", _CONST])
    changed = set()
    for ln in diff.splitlines():
        if ln[:1] in "+-" and ln[:3] not in ("+++", "---"):
            m = re.match(r"[+-]\s*([A-Z_][A-Z0-9_]*)\s*(?::[^=]+)?=\s*\S", ln)
            if m:
                changed.add(m.group(1))
    if not changed:
        return True, ["tbs_constants staged, but no constant-value lines changed"]
    outputs_staged = [f for f in staged
                      if f.startswith("diagrams/") or f.endswith((".rb", ".skp", ".png", ".svg"))]
    issues = []
    if not outputs_staged:
        issues.append(f"{len(changed)} constant(s) changed ({', '.join(sorted(changed))}) but NO "
                      f"regenerated outputs (diagrams/*.png, *.rb, *.skp) are staged — re-run the "
                      f"affected generators/models and stage their output?")
        for c in sorted(changed):
            cons = _grep_consumers(c)
            if cons:
                issues.append(f"    {c} -> {', '.join(cons)}")
    return (not issues), (issues or ["constants change has regenerated outputs staged"])


GATES = [
    ("costing reconciliation", gate_costing),
    ("costing doc-blocks (generated == doc)", gate_blocks),
]
WARNINGS = [
    ("facts-registry agreement", warn_facts),
    ("table arithmetic (TOTAL = sum of column)", warn_arithmetic),
    ("missing cascade (constant changed, outputs not regenerated)", warn_missing_cascade),
]


def _run(checks):
    failed = []
    for name, fn in checks:
        ok, msgs = fn()
        print(f"  [{'OK  ' if ok else 'FAIL'}] {name}")
        if not ok:
            failed.append(name)
            for m in msgs:
                for line in str(m).splitlines():
                    print("         " + line)
    return failed


def main() -> int:
    print("TBS-001 drift linter — GATES (block on failure):")
    gate_fail = _run(GATES)
    print("\nTBS-001 drift linter — WARNINGS (advisory):")
    warn_fail = _run(WARNINGS)

    if gate_fail:
        print(f"\n✗ {len(gate_fail)} gate(s) failed: {', '.join(gate_fail)}")
        print("  Commit blocked. Fix the drift, or bypass with: git commit --no-verify")
        return 1
    if warn_fail:
        print(f"\n⚠ {len(warn_fail)} warning(s) — review the drift candidates above (commit allowed).")
    else:
        print("\n✓ all drift checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
