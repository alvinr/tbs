#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""Unused-import checker (stdlib only — no pyflakes/autoflake dependency).

Detects `import`s whose bound name is never used in the module. Used as a
RELEASE GATE (see release.sh) so unused-import cruft cannot creep back in.

    python3 src/generators/check_unused_imports.py            # report (exit 1 if any)
    python3 src/generators/check_unused_imports.py --fix      # remove them, then report

Detection is AST-based (like pyflakes) with one thing pyflakes lacks: **re-export
awareness**. Some modules (e.g. generate_sketchup_model imported as `ov`,
generate_corridor_water_panel as `cp`) import constants purely so consumers can
reach them via `ov.NAME`. A first pass collects every `alias.NAME` access across
the tree and treats those NAMEs as used in the aliased module — so re-exports are
not flagged (and not wrongly stripped by --fix). Also excludes `from __future__`
imports and names re-exported via `__all__`.
"""
import ast
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCAN_DIRS = ["src/generators", "src/models"]


def _bound_name(alias: ast.alias) -> str:
    """The local name an import binds (`import a.b.c` binds `a`)."""
    return alias.asname or alias.name.split(".")[0]


def _files():
    out = []
    for d in SCAN_DIRS:
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".py"):
                out.append(os.path.join(d, fn))
    return out


def scan_reexports(files):
    """{module_basename: {attrs accessed as `alias.attr` anywhere}} — the re-export map."""
    modnames = {os.path.basename(f)[:-3] for f in files}
    ext: dict[str, set] = {}
    for path in files:
        try:
            tree = ast.parse(open(path, encoding="utf-8").read(), path)
        except SyntaxError:
            continue
        alias2mod = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names:
                    top = a.name.split(".")[0]
                    if top in modnames:
                        alias2mod[a.asname or top] = top
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) \
                    and node.value.id in alias2mod:
                ext.setdefault(alias2mod[node.value.id], set()).add(node.attr)
    return ext


def analyze(path: str, reexported: set):
    src = open(path, encoding="utf-8").read()
    try:
        tree = ast.parse(src, path)
    except SyntaxError as e:
        return src, [], f"SYNTAX ERROR: {e}"

    used: set[str] = set(reexported)  # names other modules reach via alias.NAME
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            used.add(node.id)
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == "__all__" and isinstance(node.value, (ast.List, ast.Tuple)):
                    for elt in node.value.elts:
                        if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                            used.add(elt.value)

    unused = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "__future__":
            continue
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            dead = [a for a in node.names if a.name != "*" and _bound_name(a) not in used]
            if dead:
                unused.append((node, dead))
    return src, unused, None


def fix(src: str, unused) -> str:
    lines = src.splitlines(keepends=True)
    edits = []
    for node, dead in unused:
        keep = [a for a in node.names if a not in dead]
        indent = " " * node.col_offset
        if keep:
            new = ast.Import(names=keep) if isinstance(node, ast.Import) else \
                  ast.ImportFrom(module=node.module, names=keep, level=node.level)
            repl = indent + ast.unparse(new) + "\n"
        else:
            repl = None
        edits.append((node.lineno, node.end_lineno, repl))
    for start, end, repl in sorted(edits, key=lambda e: -e[0]):
        lines[start - 1:end] = ([repl] if repl is not None else [])
    return "".join(lines)


def main():
    do_fix = "--fix" in sys.argv
    os.chdir(ROOT)
    files = _files()
    reexports = scan_reexports(files)

    total, report = 0, []
    for path in files:
        modname = os.path.basename(path)[:-3]
        src, unused, err = analyze(path, reexports.get(modname, set()))
        if err:
            report.append(f"  {path}: {err}")
            continue
        if not unused:
            continue
        if do_fix:
            open(path, "w", encoding="utf-8").write(fix(src, unused))
        for node, dead in unused:
            for a in dead:
                total += 1
                report.append(f"  {path}:{node.lineno}  '{a.asname or a.name}' imported but unused")

    if total:
        nf = len({r.split(':')[0] for r in report})
        print(f"✗ {total} unused import(s) {'removed' if do_fix else 'found'} across {nf} file(s):")
        print("\n".join(report))
        return 0 if do_fix else 1
    print("✓ no unused imports")
    return 0


if __name__ == "__main__":
    sys.exit(main())
