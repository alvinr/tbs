# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
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


# ── GATE: filled fact placeholders match the registry (the fact injector) ──
def gate_fact_blocks() -> tuple[bool, list[str]]:
    r = subprocess.run([sys.executable, os.path.join(HERE, "facts.py"), "--check-blocks"],
                       capture_output=True, text=True)
    return r.returncode == 0, [(r.stdout + r.stderr).strip()]


# ── GATE: parts doc-blocks match parts.py (the registry block injector) ──
def gate_parts_blocks() -> tuple[bool, list[str]]:
    r = subprocess.run([sys.executable, os.path.join(HERE, "parts.py"), "--check-blocks"],
                       capture_output=True, text=True)
    return r.returncode == 0, [(r.stdout + r.stderr).strip()]


# ── GATE: costing's registry-backed section totals == parts.system_total (parts = source of record) ──
def gate_registry_reconcile() -> tuple[bool, list[str]]:
    r = subprocess.run([sys.executable, os.path.join(HERE, "costing.py"), "--check-registry"],
                       capture_output=True, text=True)
    return r.returncode == 0, [(r.stdout + r.stderr).strip()]


# ── GATE: energy doc-blocks match calculate_energy_budget.py (the block injector) ──
def gate_energy_blocks() -> tuple[bool, list[str]]:
    r = subprocess.run([sys.executable, os.path.join(HERE, "calculate_energy_budget.py"), "--check-blocks"],
                       capture_output=True, text=True)
    return r.returncode == 0, [(r.stdout + r.stderr).strip()]


# ── GATE: weight doc-blocks match generate_weight_analysis.py (the block injector) ──
def gate_weight_blocks() -> tuple[bool, list[str]]:
    r = subprocess.run([sys.executable, os.path.join(HERE, "generate_weight_analysis.py"), "--check-blocks"],
                       capture_output=True, text=True)
    return r.returncode == 0, [(r.stdout + r.stderr).strip()]


# ── GATE: dependency-map §1 registry matches tbs_constants.py (the block injector) ──
def gate_depmap_blocks() -> tuple[bool, list[str]]:
    r = subprocess.run([sys.executable, os.path.join(HERE, "inject_dependency_map.py"), "--check-blocks"],
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
                        got = float(m.group(1).replace(",", ""))   # tolerate 2,362 / 1,600
                    except (ValueError, IndexError):
                        continue
                    if abs(got - canon) > 1e-6:
                        line = text.count("\n", 0, m.start()) + 1
                        issues.append(f"{fname}:{line}  {key}={got} (canonical {canon:g}) "
                                      f"-> '{m.group(0).strip()}'")
    return (not issues), (issues or ["all registered facts agree across docs"])


# ── WARNING: editorial-review list covers every published doc (the hand-kept list can silently miss
# one — that's how cost-analysis-report.md was reviewed-complete-but-unlisted). Flags only the
# 'published but unlisted' direction; editorial entries for unpublished docs (§E meta, superseded
# reports pending a retire decision) are intentional and not flagged. ──
def warn_editorial_list() -> tuple[bool, list[str]]:
    pub = open(os.path.join(ROOT, "publish.sh"), encoding="utf-8").read()
    m = re.search(r"MD_FILES=\((.*?)\)", pub, re.DOTALL)
    published = {os.path.basename(f) for f in re.findall(r'"([^"]+\.md)"', m.group(1))} if m else set()
    published.add("project-summary.md")                         # the home page (synced separately)
    todo = open(os.path.join(ROOT, "editorial-review-todo.md"), encoding="utf-8").read()
    listed = {os.path.basename(f) for f in re.findall(r"^- \[[ x]\]\s+(\S+\.md)", todo, re.M)}
    missing = sorted(published - listed)
    issues = [f"{f} is published (publish.sh MD_FILES) but has no editorial-review-todo.md entry"
              for f in missing]
    return (not issues), (issues or ["every published doc has an editorial-review entry"])


# ── WARNING: all-diagrams.md gallery covers every generated diagram PNG. The gallery is a hand-kept
# index, so a NEW SHEET on an existing generator silently misses it (electrical-sheet4/5,
# hingepanel-sheet6 were added to existing generators and never reached the gallery). Flags only the
# 'generated but ungalleried' direction. ──
def warn_gallery_coverage() -> tuple[bool, list[str]]:
    diag = os.path.join(ROOT, "diagrams")
    generated = {f for f in os.listdir(diag) if f.endswith(".png")} if os.path.isdir(diag) else set()
    gallery = open(os.path.join(ROOT, "all-diagrams.md"), encoding="utf-8").read()
    referenced = {os.path.basename(p) for p in re.findall(r"assets/([^)\s]+\.png)", gallery)}
    missing = sorted(generated - referenced)
    issues = [f"{f} is generated (diagrams/) but not in all-diagrams.md" for f in missing]
    return (not issues), (issues or ["every generated diagram PNG is in the all-diagrams gallery"])


# ── WARNING: parts registry reconciles with costing (drift-reduction Phase 5). As systems are
# migrated into parts.py, each must sum to costing.EXPECTED[system]; advisory until Phase 3 flips the
# cost source, then it becomes the authority. ──
def warn_parts_reconcile() -> tuple[bool, list[str]]:
    try:
        import parts
    except Exception as e:                                       # parts.py not present yet
        return True, [f"parts registry not loaded ({e})"]
    errs = parts.self_check()
    n = len(parts.systems())
    return (not errs), (errs or [f"parts registry reconciles with costing ({n} system(s) migrated)"])


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


# ── dependencies.yml — the single script -> output-file graph (deps.py loads it) ──
# The 2D<->3D drift class: a tbs_constants value changes but the generators/models that read it
# aren't re-run, so the diagrams/.rb/.skp go stale. `dependencies.yml` (validated below, can't drift)
# maps each script to the files it WRITES — grep finds which scripts read a changed constant, then
# this map names the SPECIFIC outputs that must be regenerated + staged.
_CONST = os.path.join("src", "generators", "tbs_constants.py")


def _git(args: list[str]) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, cwd=ROOT).stdout


def _grep_consumers(name: str) -> list[str]:
    out = subprocess.run(["grep", "-rlw", name, "src"], capture_output=True, text=True, cwd=ROOT).stdout
    return sorted(f for f in out.split()
                  if f.endswith(".py") and "tbs_constants" not in f and "__pycache__" not in f)


def _deps():
    sys.path.insert(0, HERE)
    import deps  # noqa: E402
    return deps


# ── WARNING: dependencies.yml validity (self-check so the single source can't drift) ──
def warn_deps_valid() -> tuple[bool, list[str]]:
    deps = _deps()
    issues = []
    for name, e in deps.ENTRIES.items():
        scr = os.path.join(ROOT, e["script"])
        if not os.path.exists(scr):
            issues.append(f"{name}: script {e['script']} does not exist")
            continue
        txt = open(scr, encoding="utf-8").read()
        for out in e["outputs"]:
            if not os.path.exists(os.path.join(ROOT, out)):
                issues.append(f"{name}: declared output {out} is missing on disk")
            base = os.path.basename(out)
            # The script must reference each output's basename it writes (png stem / .rb). The .skp
            # is built in the SketchUp app, never named in the script — so don't require it there.
            if not base.endswith(".skp") and base not in txt:
                issues.append(f"{name}: script does not write its declared output {base}")
        # Reverse direction — UNDECLARED outputs: a .png/.svg the generator writes but that isn't in
        # the YAML (the gap that hid electrical-sheet1.png + panel-layout-back.png). A line carrying
        # DIAGRAMS_DIR + a filename literal catches every savefig form — f-string, os.path.join, and
        # `out = …`/`savefig(out)`. (Models build one .skp in-app + one .rb already validated above.)
        if e["kind"] == "generator":
            declared = {os.path.basename(o) for o in e["outputs"]}
            written = set()
            for line in txt.splitlines():
                if "DIAGRAMS_DIR" in line:
                    written |= set(re.findall(r"([A-Za-z0-9_.\-]+\.(?:png|svg))", line))
            for w in sorted(written - declared):
                issues.append(f"{name}: writes {w} but it is NOT declared in dependencies.yml")
    return (not issues), (issues or ["dependencies.yml agrees with the filesystem + scripts"])


def _changed_constants(staged) -> set:
    """Constants whose VALUE changed (or were added) in the staged tbs_constants diff.
    Comment-only edits are ignored: a constant is 'changed' only if its value expression
    (the RHS with any trailing ` # comment` stripped) differs between the old and new sides,
    or it is newly added. (Strips on `\\s#` so a `#hex` colour value isn't truncated.)"""
    if _CONST not in staged:
        return set()
    diff = _git(["diff", "--cached", "-U0", "--", _CONST])
    old, new = {}, {}
    for ln in diff.splitlines():
        if ln[:3] in ("+++", "---") or ln[:1] not in "+-":
            continue
        m = re.match(r"[+-]\s*([A-Z_][A-Z0-9_]*)\s*(?::[^=]+)?=\s*(.+)", ln)
        if not m:
            continue
        val = re.split(r"\s#", m.group(2), maxsplit=1)[0].strip()   # value expr, inline comment dropped
        (old if ln[0] == "-" else new)[m.group(1)] = val
    return {name for name, v in new.items() if old.get(name) != v}


def warn_missing_cascade() -> tuple[bool, list[str]]:
    staged = set(_git(["diff", "--cached", "--name-only"]).split())
    if _CONST not in staged:
        return True, ["no tbs_constants change staged"]
    changed = _changed_constants(staged) - {"DIAGRAMS_DIR", "PROJECT_ROOT"}   # path constants don't change diagram CONTENT
    if not changed:
        return True, ["tbs_constants staged, but no content-affecting constant changed"]
    deps = _deps()
    # group each changed constant's consumer scripts → (its outputs, the constants that reach it),
    # keeping only scripts with at least one UNstaged output (the ones worth checking).
    scripts = {}
    for c in sorted(changed):
        for scr in _grep_consumers(c):
            e = deps.for_script(scr)
            if e and any(o not in staged for o in e["outputs"]):
                scripts.setdefault(scr, (e["outputs"], set()))[1].add(c)
    # Cost guard: byte-diff regenerates each script (~1–2s). For a wide change (many consumers,
    # e.g. a core geometry constant) skip the regen and fall back to the cheap "not staged" list —
    # the dev regenerates everything for a real geometry change anyway. Narrow refactors (the
    # value-identical case we want to silence) stay under the cap and get the precise byte-diff.
    byte_diff = len(scripts) <= 5
    issues = []
    for scr in sorted(scripts):
        outs, cs = scripts[scr]
        unstaged = [o for o in outs if o not in staged]
        clabel = ", ".join(sorted(cs))
        pngs = [o for o in unstaged if o.endswith((".png", ".svg"))]
        models = [o for o in unstaged if not o.endswith((".png", ".svg"))]
        stale = _regen_diff(scr, pngs) if byte_diff else pngs   # cheap fallback: flag all unstaged
        for o in stale:
            issues.append(f"{o} is stale — regenerate + stage [{clabel}]")
        for o in models:  # .skp built in-app, .rb: can't auto-verify here → advisory
            issues.append(f"{o}: re-save/re-send + stage if affected (model) [{clabel}]")
    return (not issues), (issues or ["every output of the changed constants is up to date or staged"])


def _regen_diff(scr: str, pngs: list[str]) -> list[str]:
    """Regenerate `scr` into a temp DIAGRAMS_DIR (via the TBS_DIAGRAMS_DIR env override) and
    byte-compare each png to the working tree. Returns only the outputs that genuinely differ —
    a value-identical regeneration is byte-for-byte equal and is suppressed. If regeneration
    fails, returns all `pngs` (can't verify → keep flagging)."""
    import tempfile, filecmp
    if not pngs:
        return []
    with tempfile.TemporaryDirectory() as td:
        r = subprocess.run([sys.executable, os.path.join(ROOT, scr)],
                           capture_output=True, cwd=ROOT, env={**os.environ, "TBS_DIAGRAMS_DIR": td})
        if r.returncode != 0:
            return pngs
        stale = []
        for o in pngs:
            fresh, cur = os.path.join(td, os.path.basename(o)), os.path.join(ROOT, o)
            if not (os.path.exists(fresh) and os.path.exists(cur) and filecmp.cmp(fresh, cur, shallow=False)):
                stale.append(o)
    return stale


# ── WARNING: hardwired literal that should be a tbs_constants reference ──────
# The "should have been a constant" drift class (Phase 4): a generator/model carries a numeric
# literal that equals a tbs_constants value instead of importing it — so when the constant changes,
# the literal silently goes stale (exactly the calculate_energy_budget BLUE_SUPPLY_L=1800 case).
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


# ── DUPLICATION-EQUALITY: two functions that build the SAME part must emit the same geometry ──
# The "NB: keep in sync" drift class (Phase 4): a part is built by two duplicated emitters (the
# overview re-implements the specialised model's geometry inline). Rather than trust a comment, we
# CALL both emitters, record the geometry their helpers emit (monkeypatch ruby_box/cylinder/pipe to
# capture args instead of Ruby text), and compare. Two pairs, two comparison modes:
#   electrical EP core — power_core() vs electrical(): SAME world frame (both use EP_X/constants),
#       so compare ABSOLUTE geometry per canonical part-key (catches dimension/offset/PV-path drift).
#   walkway bracket    — _cantilever_parts(std/wide) vs walkway_brackets(): different frames +
#       a parameterised loop, so compare the position-invariant SET of part SIZE-signatures.
_MODELS = os.path.join(ROOT, "src", "models")
_HELPERS = ("ruby_box", "ruby_cylinder", "ruby_pipe_run", "ruby_flex_run",
            "ruby_flex_duct", "ruby_coil_cord")


def _models_on_path():
    for p in (_MODELS, HERE):
        if p not in sys.path:
            sys.path.insert(0, p)


def _record(run) -> list:
    """Run `run()` with the ov geometry helpers monkeypatched to record (kind, name, nums)."""
    _models_on_path()
    import generate_sketchup_model as ov  # noqa: E402
    rec = []

    def box(name, x, y, z, w, d, h, color=None, alpha=None, both_sides=False):
        rec.append(("box", name, (x, y, z, w, d, h))); return ""

    def cyl(name, cx, cy, cz, radius, height, color=None, alpha=None, **k):
        rec.append(("cyl", name, (cx, cy, cz, radius, height))); return ""

    def pipe(name, waypoints, r, color=None, alpha=None, **k):
        rec.append(("pipe", name, (tuple(tuple(p) for p in waypoints), r))); return ""

    def duct(name, p1, p2, r, color=None, alpha=None, **k):
        rec.append(("pipe", name, ((tuple(p1), tuple(p2)), r))); return ""

    def coil(name, waypoints, r=5.0, color=None, alpha=None, **k):
        rec.append(("pipe", name, (tuple(tuple(p) for p in waypoints), r))); return ""

    stub = {"ruby_box": box, "ruby_cylinder": cyl, "ruby_pipe_run": pipe,
            "ruby_flex_run": pipe, "ruby_flex_duct": duct, "ruby_coil_cord": coil}
    orig = {nm: getattr(ov, nm) for nm in _HELPERS}
    patched = []  # (module, name, original) — helpers are imported by-name into several modules
    for mod in list(sys.modules.values()):
        if not mod:
            continue
        for nm in _HELPERS:
            if getattr(mod, nm, None) is orig[nm]:
                patched.append((mod, nm, orig[nm])); setattr(mod, nm, stub[nm])
    try:
        run()
    finally:
        for mod, nm, o in patched:
            setattr(mod, nm, o)
    return rec


def _geom(kind, nums):
    """Normalise a recorded primitive to a comparable tuple (rounded; color/name dropped)."""
    if kind == "box":
        return ("box",) + tuple(round(v, 1) for v in nums)
    if kind == "cyl":
        return ("cyl",) + tuple(round(v, 1) for v in nums)
    pts, r = nums
    return ("pipe", tuple(tuple(round(c, 1) for c in p) for p in pts), round(r, 1))


def _ep_key(name: str):
    """Canonical key for an EP-core part shared by power_core() and electrical(). Battery-side parts
    (cables, MRBF) are NOT shared — exclude them. Feeds are matched before their endpoint words
    (a 'PV feed -> MPPT' / 'main feed -> disconnect' name mentions the endpoint but isn't it)."""
    n = name.lower().strip()
    if any(x in n for x in ("battery", "cable", "mrbf")):
        return None
    if "pv feed" in n:
        return "pv-feed"
    if "main feed" in n:
        return "main-feed"
    if n.startswith("enclosure") or "ep enclosure" in n:
        return "enclosure"
    if n.startswith("mppt"):
        return "mppt"
    if "fuse block" in n:
        return "fuseblock"
    m = re.search(r"\bfuse ([a-g])\b", n)
    if m:
        return "fuse-" + m.group(1)
    if "busbar (+)" in n:
        return "busbar+"
    if "busbar (-)" in n:
        return "busbar-"
    if "main disconnect" in n:
        return "disconnect"
    return None


def _check_electrical() -> list[str]:
    _models_on_path()
    import generate_sketchup_model as ov
    import generate_electrical_model as em
    P = {_ep_key(n): _geom(k, g) for k, n, g in _record(em.power_core) if _ep_key(n)}
    E = {_ep_key(n): _geom(k, g) for k, n, g in _record(ov.electrical) if _ep_key(n)}
    issues = []
    for key in sorted(P):
        if key not in E:
            issues.append(f"electrical EP core: power_core emits '{key}' but electrical() does not")
        elif P[key] != E[key]:
            issues.append(f"electrical EP core: '{key}' geometry differs — "
                          f"power_core {P[key]} vs electrical() {E[key]}")
    return issues


def _sizesig(rec) -> set:
    """Position-invariant set of distinct part SIZE-signatures (box w×d×h sorted, cyl r×h, pipe r)."""
    sig = set()
    for k, n, g in rec:
        if k == "box":
            sig.add(("box",) + tuple(sorted(round(v, 1) for v in g[3:6])))
        elif k == "cyl":
            sig.add(("cyl", round(g[3], 1), round(g[4], 1)))
        else:
            sig.add(("pipe", round(g[1], 1)))
    return sig


def _check_walkway() -> list[str]:
    _models_on_path()
    import generate_sketchup_model as ov
    import generate_walkway_model as wm
    src = _sizesig(_record(lambda: [
        wm._cantilever_parts("Std", wm.CT_STD_X, 0, +1, wm.WK_W, False),
        wm._cantilever_parts("Wide", wm.CT_WIDE_X, 0, +1, wm.WK_NEAR_WIDE_W, True)]))
    ovr = _sizesig(_record(ov.walkway_brackets))
    issues = []
    for s in sorted(src - ovr, key=str):
        issues.append(f"walkway bracket: walkway-model emits size {s} that overview omits")
    for s in sorted(ovr - src, key=str):
        issues.append(f"walkway bracket: overview emits size {s} not in the walkway model")
    return issues


# Each pair: (label, check-fn, trigger-files, staged_warn, accepted). `staged_warn` gates the
# pre-commit warning (True only for a PRECISE same-frame equality with no false positives).
# `accepted` documents an EXPECTED, signed-off difference: the overview deliberately simplifies the
# walkway bracket's fab detail (a whole-system level-of-detail choice, like the 2D thin-section
# scale exaggeration), so --duplication reports it as expected, not drift, and it never warns.
_DUP_PAIRS = [
    ("electrical EP core (power_core ↔ electrical)", _check_electrical,
     ["src/models/generate_electrical_model.py", "src/models/generate_sketchup_model.py"], True, None),
    ("walkway bracket (_cantilever_parts ↔ walkway_brackets)", _check_walkway,
     ["src/models/generate_walkway_model.py", "src/models/generate_sketchup_model.py"], False,
     "overview is a simplified whole-system view — it omits the exterior reinforcing plates + "
     "full-length through-bolts the dedicated walkway model shows (intentional LOD, 2026-06)"),
]


def _duplication_findings(pairs) -> list[str]:
    out = []
    for label, fn, *_ in pairs:
        try:
            found = fn()
        except Exception as e:  # a model refactor broke the harness — surface it, don't crash the hook
            out.append(f"{label}: check could not run ({type(e).__name__}: {e})")
            continue
        out += [f"{label}: {m.split(': ', 1)[1]}" if ': ' in m else f"{label}: {m}" for m in found]
    return out


def warn_duplication() -> tuple[bool, list[str]]:
    """Pre-commit warning — only the PRECISE pairs (staged_warn=True), and only when one of their
    files is staged. The LOD-ambiguous walkway pair is `lint.py --duplication` (on-demand) only."""
    staged = set(_git(["diff", "--cached", "--name-only"]).split())
    pairs = [p for p in _DUP_PAIRS if p[3] and staged.intersection(p[2])]
    if not pairs:
        return True, ["no precise duplicated-geometry source files staged"]
    issues = _duplication_findings(pairs)
    return (not issues), (issues or ["staged duplicated emitters agree"])


def warn_unused_imports() -> tuple[bool, list[str]]:
    """A generator/model that imports a name it no longer uses — code cruft that
    check_unused_imports.py (a release gate) strips with --fix. Surfaced here as a per-commit
    advisory so it's caught at commit time, not only at release (the EP re-lay orphaned 14 that
    slipped through). Re-export-aware: a name reached via `ov.NAME` counts as used, so hub
    re-exports aren't false-flagged."""
    sys.path.insert(0, HERE)
    import check_unused_imports as cui  # noqa: E402
    cwd = os.getcwd()
    os.chdir(ROOT)
    try:
        files = cui._files()
        reexports = cui.scan_reexports(files)
        issues = []
        for path in files:
            modname = os.path.basename(path)[:-3]
            _src, unused, err = cui.analyze(path, reexports.get(modname, set()))
            if err:
                issues.append(f"{path}: {err}")
                continue
            for node, dead in unused:
                for a in dead:
                    issues.append(f"{path}:{node.lineno} '{a.asname or a.name}' imported but unused "
                                  f"— run: python3 src/generators/check_unused_imports.py --fix")
    finally:
        os.chdir(cwd)
    return (not issues), (issues or ["no unused imports in generators/models"])


def warn_narrow_dep_guard() -> tuple[bool, list[str]]:
    """Optional numpy/matplotlib imports must be guarded with `except ImportError`, NOT
    `except ModuleNotFoundError`. A heavy dep installed for the WRONG arch/ABI (e.g. an arm64
    numpy .so loaded by an x86_64 python) fails `dlopen` with a *bare* ImportError — which
    ModuleNotFoundError does NOT catch — so the "runs dependency-free" fallback crashes instead of
    degrading. The value gates (weight/energy) must fall back to math, not crash, on a broken dep.
    (Broke a commit 2026-07-08: arm64 numpy under an x86_64 .venv python.)"""
    import re
    pat = re.compile(r"try:\s*\n(.*?)\n[ \t]*except\s+ModuleNotFoundError\b", re.DOTALL)
    issues = []
    for path in _scan_files():
        try:
            src = open(path, encoding="utf-8").read()
        except OSError:
            continue
        for m in pat.finditer(src):
            if re.search(r"(?m)^\s*(import|from)\s+(numpy|matplotlib)\b", m.group(1)):
                ln = src.count("\n", 0, m.start()) + 1
                issues.append(f"{os.path.relpath(path, ROOT)}:{ln} numpy/matplotlib guarded with "
                              f"`except ModuleNotFoundError` — use `except ImportError` "
                              f"(also catches a wrong-arch/ABI dlopen failure)")
    return (not issues), (issues or ["optional numpy/matplotlib guards use except ImportError"])


def gate_license_headers() -> tuple[bool, list[str]]:
    """Every tracked .py / .rb / .md must carry the SPDX license header (AGPL-3.0-only + ©).
    Protects each source file at the source, independent of the rendered footer. Deterministic —
    a file either contains the SPDX marker or it does not (zero false positives)."""
    import subprocess
    cwd = os.getcwd(); os.chdir(ROOT)
    try:
        files = subprocess.check_output(
            ["git", "ls-files", "*.py", "*.rb", "*.md"]).decode().split()
        missing = []
        for f in files:
            try:
                if "SPDX-License-Identifier" not in open(f, encoding="utf-8").read():
                    missing.append(f)
            except OSError:
                pass
    finally:
        os.chdir(cwd)
    if missing:
        msgs = []
        for f in missing:
            if f.endswith(".rb"):
                msgs.append(f"{f} — generated .rb: add the header to its generator's Ruby preamble, then regenerate")
            elif f.endswith(".md"):
                msgs.append(f"{f} — add at top: <!-- SPDX-License-Identifier: AGPL-3.0-only --> / <!-- © 2026 Alvin Richards -->")
            else:
                msgs.append(f"{f} — add after the shebang: # SPDX-License-Identifier: AGPL-3.0-only / # © 2026 Alvin Richards")
        msgs.append("Rule: every .py/.rb/.md carries the license header (CLAUDE.md § License Headers).")
        return False, msgs
    return True, [f"all {len(files)} tracked .py/.rb/.md carry the license header"]


GATES = [
    ("license headers on every .py/.rb/.md", gate_license_headers),
    ("costing reconciliation", gate_costing),
    ("costing doc-blocks (generated == doc)", gate_blocks),
    ("fact placeholders (generated == doc)", gate_fact_blocks),
    ("energy doc-blocks (generated == doc)", gate_energy_blocks),
    ("weight doc-blocks (generated == doc)", gate_weight_blocks),
    ("dependency-map registry (generated == doc)", gate_depmap_blocks),
    ("parts doc-blocks (generated == doc)", gate_parts_blocks),
    ("section totals reconcile with parts registry (source of record)", gate_registry_reconcile),
]
WARNINGS = [
    ("facts-registry agreement", warn_facts),
    ("editorial-review list covers every published doc", warn_editorial_list),
    ("all-diagrams gallery covers every generated diagram PNG", warn_gallery_coverage),
    ("parts registry reconciles with costing (migrated systems)", warn_parts_reconcile),
    ("dependencies.yml valid (script→output map matches reality)", warn_deps_valid),
    ("table arithmetic (TOTAL = sum of column)", warn_arithmetic),
    ("missing cascade (constant changed, outputs not regenerated)", warn_missing_cascade),
    ("hardwired literal in staged file (should reference a constant)", warn_hardwired_literals),
    ("duplicated geometry in sync (staged emitters)", warn_duplication),
    ("unused imports in generators/models (check_unused_imports --fix)", warn_unused_imports),
    ("optional dep guards use except ImportError (arch/ABI-safe)", warn_narrow_dep_guard),
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


def _duplication_report() -> int:
    """Full on-demand run — checks every known duplicated-geometry pair, regardless of staging."""
    print("Duplicated-geometry equality — calling both emitters, comparing what they build:\n")
    any_drift = False
    for label, fn, _files, _warn, accepted in _DUP_PAIRS:
        issues = _duplication_findings([(label, fn)])
        if not issues:
            print(f"  ✓ {label}: in sync")
        elif accepted:
            print(f"  ≈ {label}: EXPECTED difference — {accepted}")
            for m in issues:
                print("      " + m.split(': ', 1)[1])
        else:
            any_drift = True
            print(f"  ✗ {label}: DRIFT")
            for m in issues:
                print("      " + m.split(': ', 1)[1])
    print("\n✗ unexpected drift found" if any_drift else "\nno unexpected drift (accepted differences noted above)")
    return 0


def _cascade_report(const: str) -> int:
    """Computed replacement for the old component-dependency-map.md §4 table: given a constant,
    list the scripts that read it (grep) and the outputs each writes (dependencies.yml)."""
    deps = _deps()
    cons = _grep_consumers(const)
    print(f"`{const}` is read by {len(cons)} script(s) — re-run these and stage their outputs:\n")
    for scr in cons:
        e = deps.for_script(scr)
        outs = e["outputs"] if e else ["(no registered outputs — not a diagram/model generator)"]
        print(f"  {scr}")
        for o in outs:
            print(f"      → {o}")
    if not cons:
        print("  (no src/ script references this constant — doc-only or unused)")
    return 0


def _verify_all_report(diagrams: bool) -> int:
    """Staging-INDEPENDENT full sweep — the automated version of a manual regenerate-everything.
    `warn_missing_cascade` only diffs the STAGED tree, so a constant committed WITHOUT its full cascade
    regenerated slips through (its stale outputs are byte-clean vs HEAD). This regenerates every
    registered output and byte-compares vs the working tree, catching committed-stale. Models (.rb,
    deterministic Ruby) give a clean signal and are ALWAYS checked; PNGs (opt-in `--diagrams`) are noisier
    (matplotlib/env render drift) so they're reported separately and never block. Model .rb are
    regenerated IN PLACE (their path can't be redirected like TBS_DIAGRAMS_DIR), so a stale .rb is left
    freshly regenerated — review + commit it + re-send the .skp. Run on a CLEAN tree (pre-merge / publish)."""
    deps = _deps()
    print("Full-sweep output verification (staging-independent) — regenerating every registered output:\n")
    dirty = [f for f in _git(["status", "--porcelain", "--", "src/models"]).splitlines()
             if f.strip().endswith(".rb")]
    if dirty:
        print("  ⚠ src/models has uncommitted .rb edits before the sweep — commit/stash first for a clean signal.\n")

    # ── models: regenerate each --save IN PLACE, then git-diff the .rb (deterministic → real signal) ──
    model_scripts = sorted({e["script"] for e in deps.ENTRIES.values()
                            if any(o.endswith(".rb") for o in e["outputs"])})
    print(f"  Models ({len(model_scripts)}):")
    fails = []
    for scr in model_scripts:
        r = subprocess.run([sys.executable, os.path.join(ROOT, scr), "--save"], capture_output=True, cwd=ROOT)
        print(f"    {'ok ' if r.returncode == 0 else 'ERR'} {os.path.basename(scr)}")
        if r.returncode != 0:
            fails.append(scr)
    stale_rb = sorted(f for f in _git(["diff", "--name-only", "--", "src/models"]).split() if f.endswith(".rb"))
    skp_only = sorted(os.path.basename(e["script"]) for e in deps.ENTRIES.values()
                      if any(o.endswith(".skp") for o in e["outputs"])
                      and not any(o.endswith(".rb") for o in e["outputs"]))   # e.g. water.skp — no .rb to compare

    # ── diagrams (opt-in): regenerate each generator to a temp DIAGRAMS_DIR, byte-compare PNGs ──
    stale_png = []
    if diagrams:
        gen = sorted((n, e) for n, e in deps.ENTRIES.items()
                     if any(o.endswith((".png", ".svg")) for o in e["outputs"]))
        print(f"\n  Diagrams ({len(gen)}) — env/render drift is expected noise:")
        for n, e in gen:
            d = _regen_diff(e["script"], [o for o in e["outputs"] if o.endswith((".png", ".svg"))])
            stale_png += d
            print(f"    {'STALE' if d else 'ok   '} {os.path.basename(e['script'])}")

    print()
    if fails:
        print(f"  ✗ {len(fails)} model(s) FAILED to regenerate: {', '.join(os.path.basename(f) for f in fails)}")
    if stale_rb:
        print(f"  ✗ {len(stale_rb)} STALE model .rb (regenerated in place — review + commit + re-send the .skp):")
        for f in stale_rb:
            print(f"      {f}")
    if skp_only:
        print(f"  · {len(skp_only)} model(s) build the .skp directly (no .rb) — can't byte-verify, re-send manually: {', '.join(skp_only)}")
    if diagrams and stale_png:
        print(f"  ⚠ {len(stale_png)} diagram(s) differ (triage: real geometry change vs env/render drift):")
        for f in sorted(set(stale_png)):
            print(f"      {f}")
    if not (fails or stale_rb or stale_png):
        print("  ✓ all registered outputs are up to date" + (" (models + diagrams)" if diagrams else " (models)"))
    return 1 if (fails or stale_rb) else 0   # models block; diagram drift is advisory


def main() -> int:
    if "--literals" in sys.argv:
        return _literals_report()
    if "--duplication" in sys.argv:
        return _duplication_report()
    if "--cascade" in sys.argv:
        i = sys.argv.index("--cascade")
        if i + 1 >= len(sys.argv):
            print("usage: lint.py --cascade <CONSTANT_NAME>")
            return 2
        return _cascade_report(sys.argv[i + 1])
    if "--verify-all" in sys.argv:
        return _verify_all_report("--diagrams" in sys.argv)
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
