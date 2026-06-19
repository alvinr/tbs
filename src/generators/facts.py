"""facts.py — loads the facts.yml single-source registry (Phase 2 of drift-reduction-plan.md).

facts.yml is the editable source of truth. This module reads it with a TINY dependency-free
YAML-subset parser (PyYAML isn't installed, and the pre-commit linter must stay dependency-free),
resolves any `constant:` reference from tbs_constants (so the registry can never disagree with the
code), and exposes FACTS = {name: {value, unit, owner, constant, aliases}} for lint.py.

The parser handles exactly this file's shape: top-level fact keys, 2-space scalar fields
(`key: value`), and an `aliases:` list of single-quoted `- 'regex'` items. Nothing fancier.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tbs_constants as K  # noqa: E402

YAML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "facts.yml")


def _unquote(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "'\"":
        s = s[1:-1]
    return s.replace("''", "'")


def _scalar(v: str):
    v = _unquote(v)
    try:
        return int(v)
    except ValueError:
        try:
            return float(v)
        except ValueError:
            return v


def _load(path: str) -> dict:
    out: dict = {}
    cur = None
    in_aliases = False
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        s = line.strip()
        if indent == 0 and s.endswith(":"):
            cur = s[:-1]
            out[cur] = {"aliases": []}
            in_aliases = False
        elif s == "aliases:":
            in_aliases = True
        elif in_aliases and s.startswith("- "):
            out[cur]["aliases"].append(_unquote(s[2:]))
        elif ":" in s:
            k, v = s.split(":", 1)
            out[cur][k.strip()] = _scalar(v)
            in_aliases = False
    return out


def _resolve() -> dict:
    facts = {}
    for name, f in _load(YAML_PATH).items():
        value = getattr(K, f["constant"]) if "constant" in f else f["value"]
        facts[name] = {
            "value": float(value),
            "unit": f.get("unit"),
            "owner": f.get("owner"),
            "constant": f.get("constant"),
            "aliases": f["aliases"],
        }
    return facts


FACTS = _resolve()


if __name__ == "__main__":   # quick dump to sanity-check the registry loads + resolves
    for name, f in FACTS.items():
        src = f"constant {f['constant']}" if f["constant"] else "literal"
        print(f"{name} = {f['value']:g} {f['unit']}  ({src}; {len(f['aliases'])} aliases)")
