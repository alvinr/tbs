#!/usr/bin/env python3
"""inject_dependency_map.py — make the §1 Component Registry in
component-dependency-map.md a true OUTPUT of tbs_constants.py.

The registry lists a `Value` next to each `tbs_constants` `Constant`; those values
were hand-typed and drifted (WALKWAY_GRATE_T 25→15, PROC_TRAY_DRAIN_X 2,399→4,550,
DRUM_CX 0→-400, BA_X/BA_W, PUMP_X/D …). This injector fills every
`<!-- BEGIN cdm:CONST -->value<!-- END cdm:CONST -->` marker with the current
constant value, so the registry can't drift from the source. Dependency-free (only
imports tbs_constants, which is pure) so lint.py can gate it via subprocess.

Mirrors facts.py / costing.py / calculate_energy_budget.py / generate_weight_analysis.py.
CLI:  --inject   fill the markers      --check-blocks   gate (non-zero on stale/missing)
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tbs_constants as C  # noqa: E402

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_DOC = os.path.join(_ROOT, "component-dependency-map.md")


def fmt(const: str) -> str:
    """Render a constant the way the registry prints it: comma thousands, plain
    for small ints, %g for non-integer floats. Unit/prefix (mm, Ø, ±) live in the
    prose outside the marker."""
    v = getattr(C, const)
    if isinstance(v, float) and not float(v).is_integer():
        return f"{v:g}"
    return f"{int(round(v)):,}"


def _pat(const: str) -> "re.Pattern":
    return re.compile(r"(<!-- BEGIN cdm:" + re.escape(const) + r" -->)([^<]*)"
                      r"(<!-- END cdm:" + re.escape(const) + r" -->)")


def inject(write: bool = True) -> list:
    """Fill every cdm marker. Returns [(const, 'ok'|'STALE'|'MISSING'), …]."""
    text = open(_DOC, encoding="utf-8").read()
    consts = re.findall(r"<!-- BEGIN cdm:([A-Z_][A-Z0-9_]*) -->", text)
    new, results = text, []
    for const in consts:
        if not hasattr(C, const):
            results.append((const, "MISSING"))
            continue
        val = fmt(const)
        for m in _pat(const).finditer(text):
            results.append((const, "ok" if m.group(2) == val else "STALE"))
        new = _pat(const).sub(lambda m, val=val: m.group(1) + val + m.group(3), new)
    if write and new != text:
        open(_DOC, "w", encoding="utf-8").write(new)
    return results


def check_blocks() -> list:
    return [f"cdm:{c} -> {st}" for c, st in inject(write=False) if st != "ok"]


if __name__ == "__main__":
    if "--inject" in sys.argv:
        for c, st in inject(True):
            print(f"  [{st:>7}] cdm:{c}")
    elif "--check-blocks" in sys.argv:
        probs = check_blocks()
        if probs:
            print("✗ dependency-map registry out of sync (run: inject_dependency_map.py --inject):")
            for p in probs:
                print("   -", p)
            sys.exit(1)
        print("✓ all dependency-map registry blocks match tbs_constants")
    else:
        print("usage: inject_dependency_map.py [--inject | --check-blocks]")
