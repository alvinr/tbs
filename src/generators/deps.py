# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""deps.py — loads dependencies.yml, the single structured script -> output-file graph.

dependencies.yml replaced the machine tables that used to live in component-dependency-map.md
(§3.1 model->output, §4 cascade); that doc now holds only the human design rationale and points
here. This module reads the YAML with a TINY dependency-free reader (PyYAML isn't installed, and the
pre-commit linter must stay dependency-free) — it only understands this file's flow style:

    generators:
      <name>: {script: <path>, outputs: [<path>, <path>]}
    models:
      <name>: {script: <path>, outputs: [<path>], uid: <hex>, embed_files: [<path>], source_hash: "sha256:<h>"}

Model entries additionally carry the Sketchfab identity (uid + the docs that embed it)
and a source_hash — the staleness manifest (sha256 of the model's regenerated, identity-
stripped .rb) that replaces the committed .rb as the .skp drift tripwire. Generators carry
only script/outputs.

Exposes ENTRIES = {name: {"script": str, "outputs": [str], "kind": "generator"|"model",
and for models: "uid": str, "embed_files": [str], "source_hash": str}}.
lint.py validates it (deps_valid) and the missing-cascade check consumes it.
"""
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
YAML_PATH = os.path.join(_ROOT, "dependencies.yml")


def _flow_list(s: str) -> list:
    return [x.strip() for x in s.strip().lstrip("[").rstrip("]").split(",") if x.strip()]


def _flow_entry(rest: str) -> dict:
    """Parse a flow mapping `{script: <p>, outputs: [<p>, <p>], uid: <hex>,
    embed_files: [<p>], source_hash: "<h>"}` (the value after `name:`).

    Splits into top-level fields on commas at bracket depth 0 (so a `[a, b]` list
    value stays intact), then key:value each. `[..]` values become lists; everything
    else is a scalar (surrounding quotes stripped). `script`/`outputs` always present;
    `uid`/`embed_files`/`source_hash` are optional (models carry them, generators don't)."""
    body = rest.strip()
    if body.startswith("{"):
        body = body[1:]
    if body.endswith("}"):
        body = body[:-1]
    fields, cur, depth = [], "", 0
    for ch in body:
        if ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        if ch == "," and depth == 0:
            fields.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        fields.append(cur)
    out: dict = {"script": "", "outputs": []}
    for f in fields:
        if ":" not in f:
            continue
        k, _, v = f.partition(":")
        k, v = k.strip(), v.strip()
        out[k] = _flow_list(v) if v.startswith("[") else v.strip("\"'")
    return out


def _load(path: str = YAML_PATH) -> dict:
    entries: dict = {}
    section = None
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[0] not in " \t" and line.rstrip().endswith(":"):
            section = line.rstrip()[:-1]
            continue
        if section in ("generators", "models") and ":" in line:
            name, rest = line.strip().split(":", 1)
            e = _flow_entry(rest)
            e["kind"] = "generator" if section == "generators" else "model"
            entries[name.strip()] = e
    return entries


ENTRIES = _load()


def for_script(script_path: str) -> dict:
    """The entry whose `script` is this path (repo-relative), or None."""
    for e in ENTRIES.values():
        if e["script"] == script_path:
            return e
    return None


if __name__ == "__main__":   # quick dump to sanity-check the file loads
    g = [n for n, e in ENTRIES.items() if e["kind"] == "generator"]
    m = [n for n, e in ENTRIES.items() if e["kind"] == "model"]
    print(f"{len(g)} generators + {len(m)} models, "
          f"{sum(len(e['outputs']) for e in ENTRIES.values())} declared outputs")
    for n, e in ENTRIES.items():
        print(f"  [{e['kind'][:3]}] {n}: {e['script']} -> {len(e['outputs'])} outputs")
