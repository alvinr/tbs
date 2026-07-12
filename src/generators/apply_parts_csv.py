#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""apply_parts_csv.py — write manually-verified procurement identities + prices back into the registry.

Companion to `build_parts_worklist.py`. That script emits `parts-worklist.csv` — the rows whose
identity/price the automated web pass can't settle (McMaster/Roton/Grainger are JS-/bot-gated). You
fill the `new_*` columns from your logged-in supplier session; this script writes each filled value
back into the matching `Part("<key>", …)` call in `parts.py`, scoped to that one call so it can't
touch the wrong line. It round-trips FIVE things (any subset per row; blank = leave unchanged):

    new_supplier   → the primary-supplier positional argument
    new_part_no    → the part_no="…" keyword (set if present, else inserted)
    new_url        → the url="…" keyword
    new_dims       → the dims="…" keyword (fit-critical size, e.g. a ¾" bore — quote-safe)
    new_low/new_high → the unit-cost band (both must be given together to change the band)

Edits are atomic: if ANY field on ANY row can't be located unambiguously, nothing is written and the
offending rows are reported. After a successful write it re-imports the registry and prints the
costing reconciliation (sections whose total moved). Finish with `parts.py --inject` +
`costing.py --inject` + `lint.py` to cascade into the reports + master BOM.

  python3 src/generators/apply_parts_csv.py parts-worklist.csv            # apply
  python3 src/generators/apply_parts_csv.py parts-worklist.csv --dry-run  # preview only
"""
import argparse
import csv
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import parts  # the registry (source of record)


def _r(x) -> str:
    """Render a band value as parts.py does — int literal when whole, else the float."""
    return str(int(x)) if float(x).is_integer() else str(x)


def _pystr(s: str) -> str:
    """A Python string literal for s, choosing quotes so an inch-mark (") needs no escaping."""
    if '"' not in s:
        return '"' + s + '"'
    if "'" not in s:
        return "'" + s + "'"
    return '"' + s.replace('"', '\\"') + '"'


def _call_span(src: str, key: str):
    """(start, open_paren_idx, close_paren_idx) of the Part("<key>", …) call — paren-matched,
    string-literal-aware so section-comment parens can't fool it. None if not found."""
    m = src.find(f'Part("{key}"')
    if m < 0:
        return None
    i = src.find("(", m)
    depth, q, j = 0, None, i
    while j < len(src):
        c = src[j]
        if q:
            if c == "\\":
                j += 2
                continue
            if c == q:
                q = None
        elif c in "\"'":
            q = c
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return (m, i, j)
        j += 1
    return None


def _set_kw(call: str, kw: str, cur: str, new: str) -> tuple[str, str]:
    """Set keyword `kw` to `new` inside a Part(...) call string. Replaces an existing
    `kw="cur"` (double-quoted) or inserts before the closing paren. Returns (new_call, error)."""
    lit = _pystr(new)
    if cur:                                   # replace existing double-quoted value
        old = f'{kw}="{cur}"'
        if call.count(old) != 1:
            return call, f'{kw}: existing {old!r} found {call.count(old)}× (expected 1)'
        return call.replace(old, f"{kw}={lit}", 1), ""
    # insert before the final ')'
    inner = call[:-1].rstrip()
    sep = "" if inner.endswith(",") else ","
    return inner + sep + f" {kw}={lit})", ""


def main() -> int:
    ap = argparse.ArgumentParser(description="Apply verified identities/prices from a worklist CSV into parts.py")
    ap.add_argument("csv", help="worklist CSV (see build_parts_worklist.py / parts-worklist.csv)")
    ap.add_argument("--dry-run", action="store_true", help="show the changes without writing parts.py")
    args = ap.parse_args()

    by_key = {p.key: p for p in parts.PARTS}
    p_path = os.path.join(HERE, "parts.py")
    src = open(p_path, encoding="utf-8").read()

    applied, skipped, errs = [], 0, []
    with open(args.csv, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = (row.get("key") or "").strip()
            g = lambda k: (row.get(k) or "").strip()
            ns, npn, nurl, ndim = g("new_supplier"), g("new_part_no"), g("new_url"), g("new_dims")
            nlo, nhi = g("new_low"), g("new_high")
            if not key or not any((ns, npn, nurl, ndim, nlo, nhi)):
                skipped += 1
                continue
            if key not in by_key:
                errs.append(f"{key}: not a registry key")
                continue
            p = by_key[key]
            changes = []

            # price band — both bounds required together
            if nlo or nhi:
                if not (nlo and nhi):
                    errs.append(f"{key}: need BOTH new_low and new_high to change the band")
                    continue
                try:
                    nlo_f, nhi_f = float(nlo), float(nhi)
                except ValueError:
                    errs.append(f"{key}: band not numeric ({nlo!r}/{nhi!r})")
                    continue
                if (nlo_f, nhi_f) != (p.low, p.high):
                    changes.append(("band", (p.low, p.high), (nlo_f, nhi_f)))
            if ns and ns != p.supplier:
                changes.append(("supplier", p.supplier, ns))
            if npn and npn != p.part_no:
                changes.append(("part_no", p.part_no, npn))
            if nurl and nurl != p.url:
                changes.append(("url", p.url, nurl))
            if ndim and ndim != p.dims:
                changes.append(("dims", p.dims, ndim))
            if not changes:
                skipped += 1
                continue

            span = _call_span(src, key)
            if span is None:
                errs.append(f"{key}: Part(...) call not found")
                continue
            m, _, jc = span
            call = src[m:jc + 1]
            row_err = ""

            # price + supplier both live in the '"unit", low, high, "supplier"' region — do together
            band = next((c for c in changes if c[0] == "band"), None)
            sup = next((c for c in changes if c[0] == "supplier"), None)
            if band or sup:
                lo, hi = (band[2] if band else (p.low, p.high))
                price_old = f'"{p.unit}", {_r(p.low)}, {_r(p.high)},'
                if sup:
                    old = price_old + f' "{p.supplier}"'
                    new = f'"{p.unit}", {_r(lo)}, {_r(hi)}, "{sup[2]}"'
                else:
                    old, new = price_old, f'"{p.unit}", {_r(lo)}, {_r(hi)},'
                if call.count(old) != 1:
                    row_err = f'{key}: price/supplier anchor {old!r} found {call.count(old)}× (expected 1)'
                else:
                    call = call.replace(old, new, 1)

            for kw in ("part_no", "url", "dims"):
                if row_err:
                    break
                c = next((c for c in changes if c[0] == kw), None)
                if c:
                    call, e = _set_kw(call, kw, c[1], c[2])
                    row_err = e

            if row_err:
                errs.append(row_err)
                continue
            src = src[:m] + call + src[jc + 1:]
            applied.append((key, p.system, changes))

    if errs:
        print("ERRORS (nothing written):")
        for e in errs:
            print("  ", e)
        return 1

    print(f"{len(applied)} row(s) to apply, {skipped} row(s) skipped (blank/unchanged):")
    for key, sysn, changes in applied:
        for what, old, new in changes:
            print(f"  {key:<22} {sysn:<11} {what:<9} {old!r} → {new!r}")
    if not applied:
        return 0
    if args.dry_run:
        print("\n--dry-run: parts.py NOT modified.")
        return 0

    open(p_path, "w", encoding="utf-8").write(src)
    importlib.reload(parts)
    moved = sorted({s for _, s, ch in applied if any(c[0] == "band" for c in ch)})
    if moved:
        print("\nparts.py updated. Costing reconciliation (sections whose band moved):")
        for s in moved:
            reg = parts.system_total(s)
            try:
                tgt = parts.reconcile_target(s)
            except Exception:
                tgt = None
            ok = tgt is not None and (reg[0], reg[1]) == (tgt[0], tgt[1])
            print(f"  {s:<11} registry={reg}  costing_target={tgt}  [{'OK' if ok else 'DRIFT — update costing.py'}]")
    else:
        print("\nparts.py updated (identity only — no band moved, costing unaffected).")
    print("\nNext: reconcile costing.py for any DRIFT, then `parts.py --inject` + `costing.py --inject` + `lint.py`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
