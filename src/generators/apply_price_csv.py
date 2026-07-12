#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""apply_price_csv.py — ingest manually-checked prices from a CSV into the parts registry.

Companion to the periodic manual re-price of the supplier-gated items (McMaster-Carr, Roton,
Grainger, etc.) that the automated web pass can't read (their product pages render prices only
in JavaScript / behind an account). The workflow:

  1. Fill the `new_low` / `new_high` (and optionally `checked_date`, `note`) columns of the CSV
     (see `mcmaster-prices.csv` — one row per part, with its `part_no` and product URL).
  2. Run this script:  `python3 src/generators/apply_price_csv.py mcmaster-prices.csv`
     It rewrites the `low`/`high` band in `parts.py` for every row whose new band is filled AND
     differs from the current one — scoped per `Part("<key>", …)` so it can't touch the wrong line.
  3. It then re-imports the registry and reports the costing reconciliation: any section whose
     total moved is listed, so the `costing.py` EXPECTED/line-items can be squared up. Finish with
     `parts.py --inject` + `lint.py` to cascade the change into the reports + master BOM.

Rows with blank `new_low`/`new_high` are skipped (not yet checked). `--dry-run` shows the diff
without writing.
"""
import argparse
import csv
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import parts  # the registry (source of record)


def _r(x: float) -> str:
    """Render a band value as parts.py does — int literal when whole, else the float."""
    return str(int(x)) if float(x).is_integer() else str(x)


def main() -> int:
    ap = argparse.ArgumentParser(description="Apply manually-checked prices from a CSV into parts.py")
    ap.add_argument("csv", help="CSV with key,new_low,new_high columns (see mcmaster-prices.csv)")
    ap.add_argument("--dry-run", action="store_true", help="show the changes without writing parts.py")
    args = ap.parse_args()

    by_key = {p.key: p for p in parts.PARTS}
    p_path = os.path.join(HERE, "parts.py")
    src = open(p_path, encoding="utf-8").read()

    applied, skipped, errs = [], 0, []
    with open(args.csv, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = (row.get("key") or "").strip()
            nlo, nhi = (row.get("new_low") or "").strip(), (row.get("new_high") or "").strip()
            if not key or not nlo or not nhi:      # not filled in yet
                skipped += 1
                continue
            if key not in by_key:
                errs.append(f"{key}: not a registry key")
                continue
            try:
                nlo_f, nhi_f = float(nlo), float(nhi)
            except ValueError:
                errs.append(f"{key}: new_low/new_high not numeric ({nlo!r}/{nhi!r})")
                continue
            p = by_key[key]
            if (nlo_f, nhi_f) == (p.low, p.high):   # unchanged
                skipped += 1
                continue
            # scoped replacement inside this part's Part(...) block only
            idx = src.find(f'Part("{key}"')
            nxt = src.find("Part(", idx + 5)
            nxt = nxt if nxt > 0 else len(src)
            block = src[idx:nxt]
            seg = f'"{p.unit}", {_r(p.low)}, {_r(p.high)},'
            if block.count(seg) != 1:
                errs.append(f"{key}: band segment {seg!r} found {block.count(seg)}× (expected 1)")
                continue
            new_seg = f'"{p.unit}", {_r(nlo_f)}, {_r(nhi_f)},'
            src = src[:idx] + block.replace(seg, new_seg, 1) + src[nxt:]
            applied.append((key, p.low, p.high, nlo_f, nhi_f, p.system))

    if errs:
        print("ERRORS (nothing written):")
        for e in errs:
            print("  ", e)
        return 1

    print(f"{len(applied)} band(s) to apply, {skipped} row(s) skipped (blank/unchanged):")
    for key, ol, oh, nl, nh, sysn in applied:
        print(f"  {key:<24} {sysn:<11} ${_r(ol)}-{_r(oh)} → ${_r(nl)}-{_r(nh)}")
    if not applied:
        return 0
    if args.dry_run:
        print("\n--dry-run: parts.py NOT modified.")
        return 0

    open(p_path, "w", encoding="utf-8").write(src)
    importlib.reload(parts)
    print("\nparts.py updated. Costing reconciliation (sections whose total moved need squaring up):")
    drift = False
    for s in sorted({a[5] for a in applied}):
        reg = parts.system_total(s)
        try:
            tgt = parts.reconcile_target(s)
        except Exception:
            tgt = None
        ok = tgt is not None and (reg[0], reg[1]) == (tgt[0], tgt[1])
        flag = "OK" if ok else "DRIFT — update costing.py"
        print(f"  {s:<11} registry={reg}  costing_target={tgt}  [{flag}]")
        drift = drift or not ok
    print("\nNext: reconcile costing.py for any DRIFT sections, then "
          "`parts.py --inject` + `costing.py --inject` + `lint.py` to cascade.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
