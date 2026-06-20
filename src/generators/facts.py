"""facts.py — loads the facts.yml single-source registry (Phase 2 of drift-reduction-plan.md).

facts.yml is the editable source of truth. This module reads it with a TINY dependency-free
YAML-subset parser (PyYAML isn't installed, and the pre-commit linter must stay dependency-free),
resolves any `constant:` reference from tbs_constants (so the registry can never disagree with the
code), and exposes FACTS = {name: {value, unit, owner, constant, aliases}} for lint.py.

The parser handles exactly this file's shape: top-level fact keys, 2-space scalar fields
(`key: value`), and an `aliases:` list of single-quoted `- 'regex'` items. Nothing fancier.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tbs_constants as K  # noqa: E402

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))     # repo root (where the .md docs live)
YAML_PATH = os.path.join(_HERE, "facts.yml")


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
            v = v.split(" #", 1)[0]            # strip an inline ' # comment' (scalar fields only)
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
            "display": f.get("display"),     # optional: 'comma' for thousands separators
            "aliases": f["aliases"],
        }
    return facts


FACTS = _resolve()


# ── Fact injector — fill `<!-- BEGIN fact:KEY -->value<!-- END fact:KEY -->` placeholders so a prose
# number is a true OUTPUT of the registry (generated, not just policed). Mirrors costing.py's inline
# blocks. The unit/sign live in the prose ("±<!-- BEGIN fact:... -->40<!-- END ... -->° tilt"); the
# injector fills only the number. The linter gate (gate_fact_blocks) blocks a commit if any filled
# value diverges from the registry. The alias-scan still polices UN-marked restatements.
def _fmt(fact: dict) -> str:
    v = fact["value"]
    if fact.get("display") == "comma":
        return f"{int(round(v)):,}"
    if float(v).is_integer():
        return str(int(round(v)))
    return "%g" % v


def _md_files() -> list:
    """Every source .md (root + subdirs like mini-tbs/), excluding build/output + system dirs."""
    skip = {"published", "site", ".venv", ".git", "node_modules", "__pycache__", ".claude"}
    out = []
    for dp, dns, fns in os.walk(_ROOT):
        dns[:] = [d for d in dns if d not in skip]
        out += [os.path.relpath(os.path.join(dp, f), _ROOT) for f in fns if f.endswith(".md")]
    return sorted(out)


def _fact_pat(key: str) -> "re.Pattern":
    return re.compile(r"(<!-- BEGIN fact:" + re.escape(key) + r" -->)([^\n]*?)"
                      r"(<!-- END fact:" + re.escape(key) + r" -->)")


def inject(write: bool = True) -> list:
    """Fill every fact marker across the docs. Returns (file, key, 'ok'|'STALE')."""
    results = []
    for fn in _md_files():
        path = os.path.join(_ROOT, fn)
        text = open(path, encoding="utf-8").read()
        new_text = text
        for key, fact in FACTS.items():
            pat = _fact_pat(key)
            for m in pat.finditer(text):
                results.append((fn, key, "ok" if m.group(2) == _fmt(fact) else "STALE"))
            new_text = pat.sub(lambda m, fact=fact: m.group(1) + _fmt(fact) + m.group(3), new_text)
        if write and new_text != text:
            open(path, "w", encoding="utf-8").write(new_text)
    return results


def check_blocks() -> list:
    """Linter helper: list of fact markers whose filled value is stale vs the registry."""
    return [f"{fn}  fact:{key} -> {st}" for fn, key, st in inject(write=False) if st != "ok"]


if __name__ == "__main__":
    if "--inject" in sys.argv:
        for fn, key, st in inject(True):
            print(f"  [{st:>5}] {fn}  fact:{key}")
    elif "--check-blocks" in sys.argv:
        probs = check_blocks()
        if probs:
            print("✗ fact blocks out of sync with the registry (run: facts.py --inject):")
            for p in probs:
                print("   -", p)
            sys.exit(1)
        print("✓ all fact blocks match the docs")
    else:                                    # default: dump the registry
        for name, f in FACTS.items():
            src = f"constant {f['constant']}" if f["constant"] else "literal"
            print(f"{name} = {f['value']:g} {f['unit']}  ({src}; {len(f['aliases'])} aliases)")
