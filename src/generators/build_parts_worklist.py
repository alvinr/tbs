#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""build_parts_worklist.py — emit the procurement-identity worklist CSV from the parts registry.

Companion to `apply_parts_csv.py`. Many registry rows — especially generic hardware — carry an
approximate price but NO verified product identity: no part number, no URL, the fit-critical
dimension (bore, thread, wheel Ø) buried in free-text `spec`, and in a few cases a part number
whose format doesn't match the named supplier (a McMaster SKU sitting under a Grainger row). Such
a row can't be priced or ordered as-is — you can't price a ¾"-bore vs ½"-bore handwheel the same.

This scans `parts.py` and writes `parts-worklist.csv`: one row per part that needs a human to
pin down its identity or refresh its price, each tagged with WHY it's on the list (`flags`) and a
`hint`. You (logged in at the supplier, which the automated web pass can't reach for McMaster/
Roton/Grainger) fill the `new_*` columns; `apply_parts_csv.py` writes them back into `parts.py`,
scoped per `Part("<key>", …)` so it can't touch the wrong line.

A row is included when it is not confidently orderable as-is:
  • IDENTIFY   — a fit-critical type (fasteners/bearings/fittings/seals) with NO part number
  • SKU≠SUPP  — part number is McMaster-format but the primary supplier is not McMaster  [defect A]
  • URL-MISSING— has a part number but no explicit URL (one gets auto-synthesized, maybe dead) [defect B]
  • PRICE-VERIFY— primary supplier is manual/JS-gated (McMaster/Roton/Grainger/…), so the price
                  needs a human check even when the SKU is known
  • SOURCE-PRICE— open-web retail row (Amazon or a re-homed specialty channel — Waytek, US
                  Plastic, DripDepot, …) carried as an estimate (no confirmed SKU, or a low–high
                  range) — pin the SKU/URL + a firm price

Clean rows (verified SKU + URL + consistent supplier + open-web price) are omitted — nothing to do.
"""
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import parts  # the registry (source of record)

OUT = os.path.normpath(os.path.join(HERE, "..", "..", "parts-worklist.csv"))

MM_FMT = re.compile(r"^\d+[A-Z]\d+$")          # McMaster SKU format, e.g. 6440K64
FIT_TYPES = {"fasteners-hardware", "bearings-motion", "plumbing-fittings", "seals-gaskets"}
# suppliers whose live prices the automated web pass can't read (JS / account / bot-blocked)
GATED = {"McMaster-Carr", "Roton Products", "Grainger", "Grimco", "Automation Overstock",
         "Bearing World", "VXB", "JME Sales", "Fastenal"}
# Cut-to-order metal/plastic SERVICE CENTERS — priced by spec (indicative until quoted). A catalog
# SKU isn't strictly required (they cut to order), but the price must still be verified so these
# raw-stock rows don't hide from the worklist the way alu-angle-2x2 did.
SPEC_STOCK = {"Metal Supermarkets", "Online Metals", "Bobco Metals", "TAP Plastics",
              "Central Coast Plastics", "Curbell Plastics"}
# Open-web RETAIL sourcing channels — Amazon + the specialty stores commodity rows were re-homed
# to (a part is *findable/filterable* here, unlike Amazon for e.g. DC voltage). A not-firm row at
# one of these needs a listing pinned. Deliberately excludes fab/quote/service ("Local fab",
# container, chemistry, Home Depot aisle) — those aren't sourced by picking a listing.
RETAIL_SOURCE = {"Amazon", "Waytek Wire", "US Plastic Corp", "DripDepot", "Barn Door Ag",
                 "Fresh Water Systems", "Powerwerx", "Signature Solar", "Super Bright LEDs", "Digi-Key"}

COLS = [
    # identity (reference — do not edit)
    "key", "desc", "system", "type", "qty", "unit", "flags", "hint",
    # current registry values (reference)
    "cur_supplier", "cur_part_no", "cur_url", "cur_dims", "cur_spec", "cur_low", "cur_high",
    # fill these in (blank = leave unchanged); apply_parts_csv.py writes them back
    "new_supplier", "new_part_no", "new_url", "new_dims", "new_low", "new_high",
    "checked_date", "note",
]


def _firm(p) -> bool:
    """A row is firm when it carries a confirmed SKU and a single (non-range) price."""
    return bool((p.part_no or "").strip()) and p.low == p.high


def flags_for(p) -> list[str]:
    pn = (p.part_no or "").strip()
    url = (p.url or "").strip()
    f = []
    # A fit-critical part with no SKU needs identifying ONLY when it's ordered by part number
    # from a spec-driven supplier. Amazon/Home-Depot commodity (buy-by-the-aisle) is left generic.
    if not pn and p.type in FIT_TYPES and p.supplier in GATED:
        f.append("IDENTIFY")
    if pn and MM_FMT.match(pn) and "McMaster" not in (p.supplier or ""):
        f.append("SKU≠SUPP")
    if pn and not url:
        f.append("URL-MISSING")
    if p.supplier in GATED or p.supplier in SPEC_STOCK:
        f.append("PRICE-VERIFY")
    # Open-web retail rows carried as an estimate (no confirmed listing, or only a low–high
    # range) at a NON-gated, NON-spec-stock supplier — Amazon, or a specialty channel a
    # commodity was re-homed to (Waytek, US Plastic, DripDepot, Barn Door Ag, …). Orderable in
    # principle, but the exact SKU/price isn't pinned — source it directly + fill an SKU/URL + price.
    if not _firm(p) and p.supplier in RETAIL_SOURCE:
        f.append("SOURCE-PRICE")
    return f


def hint_for(p, flags) -> str:
    bits = []
    if "SKU≠SUPP" in flags:
        bits.append(f'part_no {p.part_no} is McMaster-format but supplier is "{p.supplier}" — '
                    f'either supply the {p.supplier} SKU or switch the supplier to McMaster-Carr')
    if "IDENTIFY" in flags:
        bits.append("pin an exact SKU + capture the fit-critical dims (bore/thread/Ø) in new_dims")
    if "URL-MISSING" in flags and "SKU≠SUPP" not in flags:
        bits.append("add the product URL (the CSV auto-guesses mcmaster.com/<sku> otherwise)")
    if "SOURCE-PRICE" in flags:
        bits.append(f"source at {p.supplier}: pin the listing (SKU/ASIN + URL) + confirm a firm "
                    f"price (single value, not a range) in new_low/new_high")
    if not bits and "PRICE-VERIFY" in flags:
        bits.append("refresh the price at the supplier")
    return "; ".join(bits)


FILL = ("new_supplier", "new_part_no", "new_url", "new_dims", "new_low", "new_high",
        "checked_date", "note")


def _existing_fills() -> dict:
    """Carry forward any values already typed into the worklist so a re-run (to refresh cur_*/flags
    as the registry evolves) never clobbers in-progress fills."""
    if not os.path.exists(OUT):
        return {}
    out = {}
    with open(OUT, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if not r.get("key"):
                continue
            filled = {c: (r.get(c) or "") for c in FILL if (r.get(c) or "").strip()}
            if filled:                        # only carry rows that actually have a fill
                out[r["key"]] = filled
    return out


def main() -> int:
    prior = _existing_fills()
    carried = 0
    rows = []
    for p in parts.PARTS:
        flags = flags_for(p)
        if not flags:
            continue
        r = {
            "key": p.key, "desc": p.desc, "system": p.system, "type": p.type,
            "qty": _n(p.qty), "unit": p.unit, "flags": " ".join(flags), "hint": hint_for(p, flags),
            "cur_supplier": p.supplier, "cur_part_no": p.part_no, "cur_url": p.url,
            "cur_dims": p.dims, "cur_spec": p.spec, "cur_low": _n(p.low), "cur_high": _n(p.high),
            "new_supplier": "", "new_part_no": "", "new_url": "", "new_dims": "",
            "new_low": "", "new_high": "", "checked_date": "", "note": "",
        }
        if p.key in prior:
            r.update(prior[p.key])
            carried += 1
        rows.append(r)
    rows.sort(key=lambda r: (r["flags"], r["system"], r["key"]))
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)

    from collections import Counter
    fc = Counter(fl for r in rows for fl in r["flags"].split())
    print(f"wrote {os.path.relpath(OUT, os.path.join(HERE, '..', '..'))}: {len(rows)} rows"
          + (f" ({carried} with carried-over fills)" if carried else ""))
    for fl, n in fc.most_common():
        print(f"  {n:>3}  {fl}")
    return 0


def _n(x) -> str:
    return str(int(x)) if float(x).is_integer() else str(x)


if __name__ == "__main__":
    sys.exit(main())
