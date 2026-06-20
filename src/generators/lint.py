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


# ── WARNING: hardwired literal that should be a tbs_constants reference ──────
# The "should have been a constant" drift class (Phase 4): a generator/model carries a numeric
# literal that equals a tbs_constants value instead of importing it — so when the constant changes,
# the literal silently goes stale (exactly the calculate_energy_budget BLUE_SUPPLY_L=1600 case).
# Two tiers:
#   HIGH  — a module assignment `NAME = <lit>` where NAME *is* a constant and the file doesn't import
#           it: a re-declaration that shadows/duplicates the source. Near-zero false positive.
#   MAYBE — a bare literal equal to a DISTINCTIVE constant value (uniquely-owned, |v|>=50, and NOT a
#           round multiple of 10) in a file that already works with tbs_constants. The round-number
#           filter is the key precision lever: coincidental matches cluster on round values (90, 400,
#           1000), while genuine "should-be-a-constant" dimensions are oddly specific (1016, 114, 2362).
_INFRA = {"tbs_constants.py", "lint.py", "facts.py", "costing.py", "check_consistency.py", "setup_docs.py"}


def _constants() -> tuple[dict, dict]:
    sys.path.insert(0, HERE)
    import tbs_constants as K  # noqa: E402
    by_name, by_val = {}, {}
    for n in dir(K):
        if n.startswith("_") or not n.isupper():
            continue
        v = getattr(K, n)
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            continue
        by_name[n] = float(v)
        by_val.setdefault(round(float(v), 5), []).append(n)
    distinctive = {v: names[0] for v, names in by_val.items()
                   if len(names) == 1 and abs(v) >= 50 and v % 10 != 0}   # non-round → specific
    return by_name, distinctive


def _scan_files() -> list[str]:
    out = []
    for base in ("generators", "models"):
        d = os.path.join(ROOT, "src", base)
        if os.path.isdir(d):
            out += [os.path.join(d, f) for f in sorted(os.listdir(d))
                    if f.endswith(".py") and f not in _INFRA]
    return out


def _imported_from_constants(text: str) -> set[str]:
    names = set()
    for m in re.finditer(r"from\s+tbs_constants\s+import\s+([^\n#]+(?:\\\n[^\n#]+)*)", text):
        for part in m.group(1).replace("(", " ").replace(")", " ").replace("\\", " ").split(","):
            base = part.strip().split(" as ")[0].strip()
            if base:
                names.add(base)
    return names


def _num(tok_string: str):
    s = tok_string.replace("_", "")
    try:
        return float(int(s))
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return None


def _scan_hardwired(paths: list[str]) -> list[str]:
    import tokenize
    by_name, distinctive = _constants()
    issues = []
    for path in paths:
        rel = os.path.relpath(path, ROOT)
        text = open(path, encoding="utf-8").read()
        imported = _imported_from_constants(text)
        uses_module = bool(re.search(r"import\s+tbs_constants", text))
        # Tier HIGH — `NAME = <lit>` re-declaring a same-named constant the file doesn't import.
        for i, line in enumerate(text.splitlines(), 1):
            m = re.match(r"\s*([A-Z_][A-Z0-9_]*)\s*=\s*(-?\d+(?:\.\d+)?)\s*(?:#.*)?$", line)
            if m and m.group(1) in by_name and m.group(1) not in imported:
                if abs(_num(m.group(2)) - by_name[m.group(1)]) < 1e-6:
                    issues.append(f"{rel}:{i}  [HIGH] re-declares `{m.group(1)}` = {m.group(2)} "
                                  f"(== tbs_constants.{m.group(1)}) — import it, don't copy")
        # Tier MAYBE — bare literal == a distinctive constant value, in a constant-aware file.
        if not uses_module:
            continue
        try:
            with open(path, "rb") as fb:
                for tok in tokenize.tokenize(fb.readline):
                    if tok.type != tokenize.NUMBER:
                        continue
                    val = _num(tok.string)
                    if val is None:
                        continue
                    name = distinctive.get(round(val, 5))
                    if name and name not in tok.line:        # not already cross-referenced on the line
                        issues.append(f"{rel}:{tok.start[0]}  [maybe] literal {tok.string} == "
                                      f"tbs_constants.{name} — reference the constant?")
        except (tokenize.TokenError, IndentationError, SyntaxError):
            pass
    return issues


def warn_hardwired_literals() -> tuple[bool, list[str]]:
    """Pre-commit warning — scoped to STAGED files so it flags hardwiring at the point you add it,
    not the whole pre-existing backlog on every commit. Use `lint.py --literals` for a full scan."""
    staged = set(_git(["diff", "--cached", "--name-only"]).split())
    paths = [p for p in _scan_files() if os.path.relpath(p, ROOT) in staged]
    if not paths:
        return True, ["no generator/model files staged"]
    issues = _scan_hardwired(paths)
    return (not issues), (issues or ["no hardwired literals in the staged files"])


GATES = [
    ("costing reconciliation", gate_costing),
    ("costing doc-blocks (generated == doc)", gate_blocks),
]
WARNINGS = [
    ("facts-registry agreement", warn_facts),
    ("table arithmetic (TOTAL = sum of column)", warn_arithmetic),
    ("missing cascade (constant changed, outputs not regenerated)", warn_missing_cascade),
    ("hardwired literal in staged file (should reference a constant)", warn_hardwired_literals),
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


def _literals_report() -> int:
    """Full-repo backlog scan (on demand) — every generator/model, not just staged files."""
    issues = _scan_hardwired(_scan_files())
    high = [m for m in issues if "[HIGH]" in m]
    maybe = [m for m in issues if "[maybe]" in m]
    print(f"Hardwired-literal scan — {len(high)} HIGH (re-declarations) + {len(maybe)} maybe:\n")
    for m in high + maybe:
        print("  " + m)
    if not issues:
        print("  none — no generator/model literal matches a tbs_constants value")
    return 0


def main() -> int:
    if "--literals" in sys.argv:
        return _literals_report()
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
