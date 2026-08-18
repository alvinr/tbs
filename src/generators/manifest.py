# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""manifest.py — the model staleness manifest (source_hash in dependencies.yml).

Replaces the committed .rb as the .skp drift tripwire. For each SketchUp model, the
source_hash is the sha256 of its **regenerated, canonicalized .rb**:

  1. run the generator `--save` (writes the .rb offline — no SketchUp needed),
  2. strip the Sketchfab identity block (name/description/`sketchfab` attr dict) so a
     uid/title change is NOT read as geometry drift — identity lives in the uid field,
  3. normalize every float literal to 4 dp (`:g`) so interpreter/float-formatting noise
     (the reason the old committed-.rb byte-diff went spuriously STALE) can't flip the hash,
  4. sha256 the result.

So the hash changes iff the model's geometry/logic or a consumed constant changes — exactly
"the committed .skp is stale vs source". `lint.py --verify-all` recomputes + compares (a
mismatch = regenerate + re-send the .skp); `manifest.py --update` refreshes the stored hashes
after a legitimate re-send.

    python3 src/generators/manifest.py --check     # nonzero exit if any model hash is stale
    python3 src/generators/manifest.py --update              # recompute + write ALL hashes
    python3 src/generators/manifest.py --update ibc-stack    # scope to one (or more) re-sent model(s)
"""
import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import deps  # noqa: E402

# Lines emitted by generate_sketchup_model.sketchfab_meta_ruby() — identity, not geometry.
_IDENTITY = re.compile(r'^\s*(# ── Sketchfab metadata|model\.name\s*=|model\.description\s*='
                       r'|model\.set_attribute\("sketchfab")')
_FLOAT = re.compile(r'-?\d+\.\d+')


def _canonicalize(rb_text: str) -> str:
    """Drop the identity block and round float literals so the hash is geometry-only and
    immune to interpreter float-formatting noise."""
    kept = [ln for ln in rb_text.split("\n") if not _IDENTITY.match(ln)]
    body = "\n".join(kept)
    return _FLOAT.sub(lambda m: f"{round(float(m.group()), 4):g}", body)


def _rb_output(entry: dict) -> str:
    for o in entry["outputs"]:
        if o.endswith(".rb"):
            return o
    return ""


def compute(name: str) -> str:
    """Regenerate model `name`'s .rb (`--save`, in place) and return its canonical sha256."""
    e = deps.ENTRIES[name]
    rb_rel = _rb_output(e)
    if not rb_rel:
        raise SystemExit(f"manifest: model '{name}' declares no .rb output")
    r = subprocess.run([sys.executable, os.path.join(ROOT, e["script"]), "--save"],
                       capture_output=True, cwd=ROOT, text=True)
    if r.returncode != 0:
        raise SystemExit(f"manifest: '{name}' failed to --save:\n{r.stderr[-2000:]}")
    text = open(os.path.join(ROOT, rb_rel), encoding="utf-8").read()
    return "sha256:" + hashlib.sha256(_canonicalize(text).encode("utf-8")).hexdigest()


def model_names() -> list:
    return [n for n, e in deps.ENTRIES.items() if e["kind"] == "model"]


def check() -> list:
    """Return [(name, stored, computed), …] for every model whose hash is stale."""
    stale = []
    for n in model_names():
        stored = deps.ENTRIES[n].get("source_hash", "")
        got = compute(n)
        if stored != got:
            stale.append((n, stored, got))
    return stale


def update(only=None) -> dict:
    """Recompute model hashes and write them into dependencies.yml (surgical per-line edit — the
    flow file's comments/format are preserved). `only` (a name or iterable of names) scopes the
    write to just those models — use it after re-sending ONE model so the others' hashes (which
    reflect their own last-sent .skp) are NOT silently rewritten. Returns {name: hash}."""
    names = model_names()
    if only is not None:
        only = {only} if isinstance(only, str) else set(only)
        unknown = only - set(names)
        if unknown:
            raise SystemExit(f"manifest: unknown model(s) {sorted(unknown)}; known: {sorted(names)}")
        names = [n for n in names if n in only]
    text = open(deps.YAML_PATH, encoding="utf-8").read()
    written = {}
    for n in names:
        got = compute(n)
        pat = re.compile(r'(^  ' + re.escape(n) + r':\s*\{.*?source_hash:\s*")[^"]*(")', re.M)
        text, k = pat.subn(lambda m: m.group(1) + got + m.group(2), text)
        if k != 1:
            raise SystemExit(f"manifest: expected exactly one source_hash line for '{n}', matched {k}")
        written[n] = got
    open(deps.YAML_PATH, "w", encoding="utf-8").write(text)
    return written


def main() -> int:
    if "--update" in sys.argv:
        # positional args after the flags = the model(s) to scope the write to (default: all)
        only = [a for a in sys.argv[1:] if not a.startswith("-")] or None
        written = update(only=only)
        for n, h in written.items():
            print(f"  updated {n}: {h}")
        scope = "all" if only is None else ", ".join(only)
        print(f"dependencies.yml source_hash refreshed ({scope}).")
        return 0
    if "--check" in sys.argv:
        stale = check()
        if not stale:
            print(f"✓ all {len(model_names())} model source_hash values are current")
            return 0
        print(f"✗ {len(stale)} model(s) STALE vs source (regenerate + re-send the .skp, then --update):")
        for n, stored, got in stale:
            print(f"    {n}\n      stored:   {stored}\n      computed: {got}")
        return 1
    print(__doc__)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
