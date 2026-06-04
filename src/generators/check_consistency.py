#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
check_consistency.py — 2D ↔ 3D ↔ docs consistency audit for TBS-001.

Codifies the recurring drift we keep finding between the matplotlib diagram
generators (src/generators/), the SketchUp model builders (src/models/), and the
reports (*.md). You cannot diff a PNG against a .skp, but almost every real
anomaly traces to one of four root causes, three of which are mechanical:

  1. HARDCODED VALUE that should read tbs_constants.py — a literal/label/comment
     quoting a dimension. When the constant changes, the hardcode goes stale.
     → CHECK A (stale-value scan): the highest-value check.
  2. DRAWING LOGIC didn't follow a design change (shape/projection/feature).
     → not mechanical; see the skill checklist. CHECK D gives a feature inventory.
  3. CHANGE applied to one side only (2D or 3D, not both).
     → CHECK C (git divergence) + CHECK B (constant-import asymmetry).
  4. DOC / NUMBER staleness.
     → CHECK A covers docs too.

Run:  python3 src/generators/check_consistency.py            # all checks
      python3 src/generators/check_consistency.py --scan 750,375   # ad-hoc values
See skills/skill_model_consistency.md for how to read and act on the output.
"""
import os
import re
import subprocess
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GEN_DIR = os.path.join(ROOT, "src", "generators")
MOD_DIR = os.path.join(ROOT, "src", "models")
CONSTS = os.path.join(GEN_DIR, "tbs_constants.py")

# Lines that legitimately quote an old value as HISTORY are not drift — skip them.
HISTORY_RE = re.compile(
    r"\b(was|were|replaces?|replaced|failed|earlier|formerly|previously|"
    r"rev ?\d|history|historical|redesign basis|deleted|old |prior)\b", re.I)
MIN_STALE_VALUE = 100   # only scan distinctive old values (drops common small dims)

# Explicit 2D↔3D subsystem pairings for the divergence + import + inventory checks.
# (The Overview model contains nearly everything, so it is audited per-subsystem
# rather than as one blob.)
PAIRS = {
    "Spray bar":         (["generate_spray_bar_diagram.py"],      "generate_spraybar_model.py"),
    "Light trap / fans": (["generate_lighttrap_diagram.py",
                           "generate_hingepanel_diagram.py"],     "generate_lighttrap_model.py"),
    "IBC stack":         (["generate_ibc_stacking_diagram.py",
                           "generate_ibc_frame_drawing.py"],      "generate_ibc_model.py"),
}

C1, C2 = "\033[91m", "\033[93m"   # red / yellow
C0, CB = "\033[0m", "\033[1m"


def _rel(p):
    return os.path.relpath(p, ROOT)


def _files(exts, *dirs):
    out = []
    for d in dirs:
        for f in sorted(os.listdir(d)):
            if f.endswith(exts) and f != "check_consistency.py":
                out.append(os.path.join(d, f))
    return out


def scan_targets():
    """Every place a stale value could hide: generators, models, .rb, root docs."""
    files = _files((".py",), GEN_DIR, MOD_DIR) + _files((".rb",), MOD_DIR)
    files += [os.path.join(ROOT, f) for f in sorted(os.listdir(ROOT)) if f.endswith(".md")]
    return files


def parse_constants():
    """{NAME: float} for constants assigned a plain numeric literal."""
    out = {}
    for line in open(CONSTS):
        m = re.match(r"^([A-Z][A-Z0-9_]*)\s*=\s*(-?\d+(?:\.\d+)?)\b", line)
        if m:
            out[m.group(1)] = float(m.group(2))
    return out


def prior_values(current):
    """(old_value -> list of "NAME (now=…)") from git history + inline 'was N'."""
    olds = {}

    def add(name, val):
        if current.get(name) != val and abs(val) >= MIN_STALE_VALUE \
                and val not in current.values():           # not a current value of anything
            olds.setdefault(val, set()).add(f"{name} (now={current.get(name, 'gone')})")

    try:
        diff = subprocess.run(["git", "-C", ROOT, "log", "-p", "--", _rel(CONSTS)],
                              capture_output=True, text=True, timeout=60).stdout
        for line in diff.splitlines():
            m = re.match(r"^-\s*([A-Z][A-Z0-9_]*)\s*=\s*(-?\d+(?:\.\d+)?)\b", line)
            if m:
                add(m.group(1), float(m.group(2)))
    except Exception as e:
        print(f"  (git history unavailable: {e})")
    # inline "… was 625 …" comments document a prior value too
    for line in open(CONSTS):
        nm = re.match(r"^([A-Z][A-Z0-9_]*)", line)
        for v in re.findall(r"was [Ø~]?(\d+)", line):
            if nm:
                add(nm.group(1), float(v))
    return olds


def _doc_context(line, start, end):
    """True if the number is in a label/comment/dimension — where stale text hides
    (not a bare code literal, which is usually a coincidental offset)."""
    pre, post = line[:start], line[end:]
    return ("#" in pre                                       # inside a comment
            or (pre.count('"') + pre.count("'")) % 2 == 1     # inside a string literal
            or post[:2].lower() == "mm"                       # NNNmm
            or (start and line[start - 1] in "Ø~"))           # ØNNN


def check_a_stale_values(current):
    print(f"\n{CB}── CHECK A · stale-value scan "
          f"(labels/comments quoting a CHANGED constant's prior value) ──{C0}")
    olds = prior_values(current)
    if not olds:
        print("  no prior numeric values recovered from history.")
        return 0
    print(f"  scanning for {len(olds)} distinctive old values (≥{MIN_STALE_VALUE}): "
          f"{', '.join(str(int(v)) for v in sorted(olds))}")
    by_val = {}
    for path in scan_targets():
        if os.path.samefile(path, CONSTS):
            continue
        for i, line in enumerate(open(path, errors="ignore"), 1):
            if HISTORY_RE.search(line):
                continue                                      # legitimate history note
            for val in olds:
                token = str(int(val)) if val == int(val) else str(val)
                for m in re.finditer(r"(?<![\d.])" + re.escape(token) + r"(?![\d.])", line):
                    if _doc_context(line, m.start(), m.end()):
                        by_val.setdefault(val, []).append((path, i, line.strip()))
                        break
    hits = 0
    for val in sorted(by_val, key=lambda v: len(by_val[v])):  # rarest first = most suspicious
        rows = by_val[val]
        who = "; ".join(sorted(olds[val]))
        v = int(val) if val == int(val) else val
        print(f"  {C2}value {v}{C0}  (old: {who}) — {len(rows)} hit(s)")
        for path, i, txt in rows[:6]:
            print(f"      {_rel(path)}:{i}  {txt[:88]}")
        if len(rows) > 6:
            print(f"      … +{len(rows) - 6} more")
        hits += len(rows)
    print(f"  → {hits} suspect literal(s) in labels/comments. A current dimension "
          f"that happens to equal an old value is a false positive — triage by line.")
    return hits


def _imports(path):
    txt = open(path, errors="ignore").read()
    m = re.search(r"from tbs_constants import\s*\(([^)]*)\)", txt, re.S)
    block = m.group(1) if m else " ".join(
        re.findall(r"from tbs_constants import (.+)", txt))
    return set(re.findall(r"\b([A-Z][A-Z0-9_]+)\b", block))


def check_b_imports():
    print(f"\n{CB}── CHECK B · shared-constant import asymmetry (per pairing) ──{C0}")
    n = 0
    for name, (twods, threed) in PAIRS.items():
        td = _imports(os.path.join(MOD_DIR, threed))
        for d2 in twods:
            p2 = os.path.join(GEN_DIR, d2)
            if not os.path.exists(p2):
                continue
            tw = _imports(p2)
            # flag geometry-ish constants present on one side only (skip C_* colours)
            only3 = sorted(c for c in (td - tw) if not c.startswith("C_"))
            only2 = sorted(c for c in (tw - td) if not c.startswith("C_"))
            if only3 or only2:
                print(f"  {CB}{name}{C0}: {d2} ↔ {threed}")
                if only3:
                    print(f"    {C2}only in 3D:{C0} {', '.join(only3[:14])}")
                if only2:
                    print(f"    {C2}only in 2D:{C0} {', '.join(only2[:14])}")
                n += 1
    print("  → asymmetry can be benign (different views need different consts) — "
          "but a geometry constant on one side only is worth a look.")
    return n


def _shas(path):
    try:
        out = subprocess.run(["git", "-C", ROOT, "log", "--format=%H", "--", _rel(path)],
                             capture_output=True, text=True, timeout=30).stdout
        return set(out.split())
    except Exception:
        return set()


def _subjects(shas):
    if not shas:
        return []
    out = subprocess.run(["git", "-C", ROOT, "show", "--no-patch", "--format=%h %s", *shas],
                         capture_output=True, text=True, timeout=30).stdout
    return [l for l in out.splitlines() if l.strip()]


def check_c_divergence():
    print(f"\n{CB}── CHECK C · git divergence (commits touching one side, not the other) ──{C0}")
    n = 0
    for name, (twods, threed) in PAIRS.items():
        s3 = _shas(os.path.join(MOD_DIR, threed))
        s2 = set().union(*[_shas(os.path.join(GEN_DIR, d)) for d in twods]) if twods else set()
        d3, d2 = s3 - s2, s2 - s3
        print(f"  {CB}{name}{C0}: {threed}  ↔  {', '.join(twods)}")
        for tag, shas in (("3D-only (2D may be behind)", d3), ("2D-only (3D may be behind)", d2)):
            subs = _subjects(shas)
            if subs:
                print(f"    {C2}{tag}:{C0}")
                for s in subs[:8]:
                    print(f"      {s[:92]}")
                n += len(subs)
    print("  → a 3D-only commit that changed geometry/features is the classic "
          "'updated one side' drift (e.g. the spray-bar zip-ties).")
    return n


def check_d_inventory():
    print(f"\n{CB}── CHECK D · part-name vs label inventory (eyeball for missing features) ──{C0}")
    for name, (twods, threed) in PAIRS.items():
        t3 = open(os.path.join(MOD_DIR, threed), errors="ignore").read()
        parts = sorted(set(re.findall(r"ruby_\w+\(\s*f?[\"']([^\"'{]+)", t3)))
        labels = set()
        for d in twods:
            p2 = os.path.join(GEN_DIR, d)
            if os.path.exists(p2):
                t2 = open(p2, errors="ignore").read()
                labels |= set(re.findall(r"[\"']([A-Z][A-Za-z0-9 ./×°\-]{6,}?)[\"']", t2))
        print(f"  {CB}{name}{C0}")
        print(f"    3D parts ({len(parts)}): {', '.join(parts[:22])}"
              + (" …" if len(parts) > 22 else ""))
        print(f"    2D labels ({len(labels)}): {', '.join(sorted(labels)[:18])}"
              + (" …" if len(labels) > 18 else ""))
    print("  → compare the two lists: a 3D part with no matching 2D label (or vice "
          "versa) is a candidate feature gap. (Wording differs — judgment needed.)")
    return 0


def main():
    if "--scan" in sys.argv:
        vals = [float(v) for v in sys.argv[sys.argv.index("--scan") + 1].split(",")]
        for path in scan_targets():
            for i, line in enumerate(open(path, errors="ignore"), 1):
                for v in vals:
                    token = str(int(v)) if v == int(v) else str(v)
                    if re.search(r"(?<![\d.])" + re.escape(token) + r"(?![\d.])", line):
                        print(f"  {_rel(path)}:{i}  {line.strip()[:100]}")
        return
    print(f"{CB}TBS-001 · 2D↔3D↔docs consistency audit{C0}")
    cur = parse_constants()
    print(f"  parsed {len(cur)} numeric constants from tbs_constants.py")
    total = (check_a_stale_values(cur) + check_b_imports()
             + check_c_divergence() + check_d_inventory())
    print(f"\n{CB}Audit complete.{C0} Findings are heuristics, not failures — "
          f"triage against skills/skill_model_consistency.md.")


if __name__ == "__main__":
    main()
