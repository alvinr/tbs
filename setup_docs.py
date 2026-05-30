#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
setup_docs.py — One-time setup for the Giant Pinhole Camera MkDocs site.

Run once from the project root:
    python3 setup_docs.py

What it does:
  1. Checks / installs mkdocs and mkdocs-material
  2. Creates the published/ directory structure
  3. Copies .md files and images into published/
  4. Writes mkdocs.yml
  5. Writes a published/index.md landing page
  6. Prints next steps

After running, use publish.sh for subsequent refreshes.
"""

import subprocess
import sys
import shutil
import os
from pathlib import Path

# ── Configuration ────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent.resolve()
DOCS_DIR = PROJECT_ROOT / "published"
ASSETS_DIR = DOCS_DIR / "assets"

SITE_NAME = "The Big Shoebox — Research & Build"
SITE_DESCRIPTION = (
    "A rigorous, source-backed design and build guide for a 20 ft × 7 ft pinhole camera."
)
# Set this to your GitHub Pages URL once the repo is created, e.g.:
#   https://yourusername.github.io/tbs
SITE_URL = "https://alvinr.github.io/tbs"

# Map source filename → (docs subdirectory, nav title)
# Order here controls the sidebar navigation order.
MD_FILES = [
    ("funding-proposal.md",              (".",           "Proposal")),
    ("project-cost-breakdown.md",        (".",           "Cost Breakdown")),
    ("pinhole-optics-report.md",         (".",           "Optics Report")),
    ("pinhole-option-b-optics.md",       (".",           "Container Optics")),
    ("lens-vs-pinhole-exposure.md",      (".",           "Lens vs Pinhole")),
    ("lens-options.md",                  (".",           "Lens Options")),
    ("container-transport-options.md",   (".",           "Transportation")),
    ("pinhole-report.md",                (".",           "Pinhole Report")),
    ("photosensitive-plane-options.md",  (".",           "Photosensitive Materials")),
    ("water-system-report.md",           (".",           "Processing System")),
    ("film-plane-mechanism-report.md",   (".",           "Film Plane Mechanism")),
    ("tilt-swing-board-report.md",       (".",           "Tilt-Swing Front Board")),
    ("tilt-swing-board-analysis.md",     (".",           "Tilt & Swing Distortion Renders")),
    ("pinhole-camera-construction.md",   (".",           "Construction Guide")),
    ("chemistry-shopping-list.md",       (".",           "Chem Shopping List")),
    ("operating-manual.md",             (".",           "Operating Manual")),
    ("electrical-report.md",            (".",           "Electrical & Systems")),
    ("master-shopping-list.md",         (".",           "Master Shopping List")),
    ("licensing.md",                      (".",           "License")),
    ("light-trap-selection.md",           (".",           "Light Trap Selection")),
    ("engineering-diagrams.md",           (".",           "Engineering Diagrams")),
    ("complete-distortion-renders.md",      (".",           "Distortion Renders")),
    ("equipment-layout-report.md",        (".",           "Equipment Layout")),
    ("component-dependency-map.md",       (".",           "Component Dependency Map")),
    ("weight-distribution-report.md",    (".",           "Weight Distribution")),
    ("chemistry-prep-shelves.md",         (".",           "Chemistry Prep Shelves")),
    ("processing-tray-and-spray-bar.md",  (".",           "Processing Tray & Spray Bar")),
    ("hinged-panel-report.md",            (".",           "Hinged Light-Trap Panel")),
    ("ceiling-rail-report.md",            (".",           "Ceiling Rail Suspension")),
    ("ibc-stacking-report.md",            (".",           "IBC Stacking System")),
    ("ventilation-report.md",             (".",           "Ventilation & Cooling")),
    ("walkway-report.md",                 (".",           "Walkway")),
    ("equipment-panel-report.md",         (".",           "Equipment Panel & Plumbing")),
    ("all-diagrams.md",                   (".",           "All Diagrams")),
    ("mini-tbs/mini-tbs-poc.md",          ("mini-tbs",    "Mini-TBS PoC")),
    ("mini-tbs/mini-tbs-shopping-list.md",("mini-tbs",    "Mini-TBS Shopping List")),
]

# Root-only images (not generated into diagrams/)
ROOT_IMAGE_FILES = [
]

# Images stored in assets/ (not root, not diagrams/)
ASSET_IMAGE_FILES = [
    "logo-final.png",
    "favicon.png",
]

# Generated diagram images (all live in diagrams/)
DIAG_IMAGE_FILES = [
    "portrait-camera-schematic.png",
    "portrait-optimal-3m.png",
    "portrait-scale-comparison.png",
    "water-system-sheet1.png",
    "water-system-sheet2.png",
    "water-system-sheet3.png",
    "water-system-sheet4.png",
    "film-plane-sheet1.png",
    "film-plane-sheet2.png",
    "film-plane-sheet3.png",
    "film-plane-sheet4.png",
    "film-plane-sheet5.png",
    "film-plane-distortion-c0.png",
    "film-plane-distortion-c1.png",
    "film-plane-distortion-c2.png",
    "film-plane-distortion-c3.png",
    "film-plane-distortion-c4.png",
    "film-plane-distortion-c5.png",
    "film-plane-distortion-c6.png",
    "film-plane-distortion-summary.png",
    "tilt-swing-board-sheet1.png",
    "tilt-swing-board-sheet2.png",
    "tilt-swing-board-sheet3.png",
    "tilt-swing-combined-c0.png",
    "tilt-swing-combined-c1.png",
    "tilt-swing-combined-c2.png",
    "tilt-swing-combined-c3.png",
    "tilt-swing-combined-c4.png",
    "tilt-swing-combined-c5.png",
    "tilt-swing-combined-c6.png",
    "tilt-swing-combined-c7.png",
    "tilt-swing-combined-c8.png",
    "tilt-swing-combined-summary.png",
    "tilt-swing-sheet1.png",
    "tilt-swing-sheet2.png",
    "electrical-sheet1.png",
    "electrical-sheet2.png",
    "electrical-sheet3.png",
    "power-panel-sheet1.png",
    "lighttrap-sheet1.png",
    "lighttrap-sheet2.png",
    "hingepanel-sheet1.png",
    "hingepanel-sheet2.png",
    "hingepanel-sheet3.png",
    "hingepanel-sheet4.png",
    "container-floorplan.png",
    "container-floorplan-sheet2.png",
    "assembly-overview.png",
    "assembly-overview-fp.png",
    "assembly-overview-plan.png",
    "assembly-fab-sheet1.png",
    "assembly-fab-sheet2.png",
    "line-of-sight.png",
    "plate-drawing-sheet1.png",
    "plate-drawing-sheet2.png",
    "ceiling-rail-sheet1.png",
    "ceiling-rail-sheet2.png",
    "walkway-sheet1.png",
    "walkway-sheet2.png",
    "walkway-sheet3.png",
    "walkway-sheet4.png",
    "walkway-sheet5.png",
    "walkway-sheet6.png",
    "walkway-sheet7.png",
    "walkway-sheet8.png",
    "ibc-stacking-sheet1.png",
    "ibc-stacking-sheet2.png",
    "ibc-stacking-sheet3.png",
    "ibc-stacking-sheet4.png",
    "ibc-stacking-sheet5.png",
    "ibc-frame-sheet1.png",
    "ibc-frame-sheet2.png",
    "ibc-frame-sheet3.png",
    "mini-tbs-sheet1.png",
    "weight-analysis-sheet1.png",
    "weight-analysis-sheet2.png",
    "weight-analysis-sheet3.png",
    "weight-analysis-sheet4.png",
    "shelf-sheet1.png",
    "shelf-sheet2.png",
    "shelf-sheet3.png",
    "pinhole-wall-elevation.png",
    "panel-layout.png",
    "spray-bar-sheet1.png",
    "spray-bar-sheet2.png",
    "spray-bar-sheet3.png",
    "spray-bar-sheet4.png",
    "spray-bar-sheet5.png",
    "spray-bar-sheet6.png",
    "filter-skid-sheet1.png",
    "pump-manifold-sheet1.png",
]

MKDOCS_YML = """\
site_name: "{site_name}"
site_description: "{site_description}"
site_url: "{site_url}"

theme:
  name: material
  favicon: assets/favicon.png
  logo: assets/favicon.png
  palette:
    - scheme: default
      primary: black
      accent: deep orange
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: black
      accent: deep orange
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  font:
    text: IBM Plex Sans
    code: IBM Plex Mono
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.top
    - search.suggest
    - search.highlight
    - content.code.copy
    - toc.integrate

markdown_extensions:
  - tables
  - toc:
      permalink: true
  - admonition
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.arithmatex:
      generic: true
  - attr_list
  - md_in_html

extra_javascript:
  - https://polyfill.io/v3/polyfill.min.js?features=es6
  - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js

nav:
  - Home: index.md
{nav_entries}

extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/yourusername/tbs

copyright: "© 2026 Alvin Richards — Released under <a href=\"../licensing/\">GNU AGPLv3</a>"
"""

INDEX_MD = """\
# The Big Shoebox — Project Summary

<div style="text-align:center;">
  <img src="assets/logo-final.png" alt="The Big Shoebox Project" style="width:40%">
</div>

---

## What Is It

A fully operational pinhole camera built inside a standard 20-foot ISO shipping container. It makes photographs — real, large-format photographs — on contact-scale cyanotype prints measuring nearly 20 feet wide by 8 feet tall. It is transportable, deployable in remote locations, and self-sufficient for water and processing. It is not an installation that resembles a camera. It is a camera.

---

## The Scale

| Parameter | Value |
|-----------|-------|
| Image plane | 5,893 × 2,388 mm (~19'4" × 7'10") |
| Image area | ~140 sq ft |
| Focal length | 2,362 mm (container interior depth) |
| Optimal pinhole | Ø2.17 mm (Lord Rayleigh formula, λ = 550 nm) |
| f-number | f/1088 |
| Baseline exposure | ~43 min (ISO 6 paper, full sun, Schwarzschild-corrected) |
| Process | Cyanotype — water-based, non-toxic, no silver |
| Per-print cost | ~$57 |
| 50-print run | ~$2,842 |

---

## The Technology

Two independent movement systems work in series, stacking their effects non-linearly:

**Front board — tilt and swing (±5°)**
The pinhole itself pivots on a spherical plain bearing, steering the image cone across the film plane. Every 5° of tilt shifts the projected image 207 mm. Used for compositional placement — not correction, not distortion, but deliberate image steering.

**Film plane — 4-corner independent actuation (±42° tilt, ±20° swing)**
Four corners of the image plane move independently via handwheels, enabling view-camera-style geometric control at pinhole focal lengths. Scheimpflug-equivalent movements, compound twisted-plane projections, convergence manipulation — the full vocabulary of large-format photography, applied to a pinhole.

**Combined:** the two systems interact non-linearly. Their compound optical projections produce images that no other camera type can make.

Every specification traces to a peer-reviewed source or manufacturer datasheet. The optics are not approximated.

**Off-grid capable:** a self-contained three-circuit water system supports 8–10 full-size prints between resupply runs, with 40% water recycling. 12V DC operation. Deployable without mains connection.

---

## The Process

Cyanotype on cotton muslin. The sensitiser (ferric ammonium citrate + potassium ferricyanide) is coated onto fabric, exposed by contact with the image-plane, and developed in plain cold water. No silver, no hazardous chemistry, no darkroom registration required.

The container travels by commercial hire truck. No CDL required for the operator. No oversize permits required for an empty 20ft standard container on Interstate highways.

---

## Documents

| Document | Description |
|----------|-------------|
| [Proposal](funding-proposal.md) | Structured pitch outline for arts foundations, MFA boards, residency programs |
| [Pinhole Optics Report](pinhole-optics-report.md) | Lord Rayleigh formula, f-numbers, exposure calculations |
| [Container Optics](pinhole-option-b-optics.md) | Detailed optics for the shipping container configuration |
| [Lens vs Pinhole](lens-vs-pinhole-exposure.md) | Why the exposure difference is ~5,500× — full derivation |
| [Lens Options](lens-options.md) | Coverage problem, thin lens equations, DoF, distortion, recommendations |
| [Lens vs Pinhole](lens-vs-pinhole-exposure.md) | Why the exposure difference is ~5,500× — full derivation |
| [Photosensitive Materials](photosensitive-plane-options.md) | All process options, ISO equivalents, spectral response, per-image costs |
| [Processing System](water-system-report.md) | Off-grid three-circuit water system design and Bill of Materials |
| [Film Plane Mechanism](film-plane-mechanism-report.md) | 4-corner independent actuation — design, drawings, shopping list |
| [Tilt-Swing Front Board](tilt-swing-board-report.md) | Spherical-pivot mechanism — design, drawings, combined distortion renders |
| [Tilt & Swing Distortion Renders](tilt-swing-board-analysis.md) | Ray-traced projection renders for all combined board + film plane configurations |
| [Pinhole Report](pinhole-report.md) | Interchangeable plate system — wall frame, pinhole plate, lens plate |
| [Construction Guide](pinhole-camera-construction.md) | Light-sealing, pinhole plate fabrication, image plane loading |
| [Pinhole Report](pinhole-report.md) | Interchangeable plate system — wall frame, pinhole plate, lens plate |
| [Cost Breakdown](project-cost-breakdown.md) | Full itemized build cost — three scenarios, all sources cited |
| [Chem Shopping List](chemistry-shopping-list.md) | 50-print quantities with supplier URLs and confirmed prices |
| [Transportation](container-transport-options.md) | Commercial hire vs. self-haul analysis |
| [Operating Manual](operating-manual.md) | Single-operator step-by-step workflow — coating, exposure, development, cleanup |
| [Electrical & Systems](electrical-report.md) | Power architecture, light trap vestibule, lighting, wiring diagrams |
| [Ventilation & Cooling](ventilation-report.md) | Fan system, evaporative cooler, light-safe baffle ducts, shade canopy, and operating modes |
| [Master Shopping List](master-shopping-list.md) | All components consolidated by build area — electrical, water, chemistry, vestibule, cooling |
| [License](licensing.md) | GNU AGPLv3 — © 2026 Alvin Richards |
| [Light Trap Selection](light-trap-selection.md) | Revolving light trap options, pricing, and custom fabrication specification |
| [Engineering Diagrams](engineering-diagrams.md) | All TBS-001 construction drawings — assembly overview, fabrication, subsystems |
| [Distortion Renders](complete-distortion-renders.md) | Ray-traced projections for all film-plane and tilt-swing configurations |
| [Equipment Layout](equipment-layout-report.md) | Shadow-free end-zone layout — optical clearance proof, IBC Y-stacking, new rail positions |
| [Component Dependency Map](component-dependency-map.md) | System component registry, diagram index, and change propagation guide |
| [Weight Distribution](weight-distribution-report.md) | Container weight analysis — dry, camera ready, materials exhausted — CG positions and ISO compliance |
| [Chemistry Prep Shelves](chemistry-prep-shelves.md) | Two fold-down shelves on pinhole wall for cyanotype chemistry mixing and materials staging |
| [Processing Tray & Spray Bar](processing-tray-and-spray-bar.md) | 304 SS processing tray and telescoping spray bar gantry — construction, operation, and parts list |
| [Hinged Light-Trap Panel](hinged-panel-report.md) | Stepped cargo-door panel with revolving drum light trap, sliding carriage, and light seal design |
| [Ceiling Rail Suspension](ceiling-rail-report.md) | HGR20 ceiling-mounted linear rails suspending hinged panel with 80 mm floor gap for processing tray clearance |
| [IBC Stacking System](ibc-stacking-report.md) | 2×2 IBC stack with welded stacking frame, external plumbing panel, and internal pipe routing |
| [Perimeter Walkway](walkway-report.md) | 4-section removable walkway system — wall-cantilevered, ceiling-hung, and lift-out designs with zero tray contact |
| [Equipment Panel & Plumbing](equipment-panel-report.md) | Equipment panel in IBC corridor with 5 pumps, 3-stage filter skid, accumulator, valves, and pipe routing |
| [All Diagrams](all-diagrams.md) | Complete visual gallery of every TBS-001 engineering diagram on a single page |

"""

# ── Helpers ──────────────────────────────────────────────────────────────────

def run(cmd, check=True):
    print(f"  $ {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"  ERROR: {result.stderr.strip()}")
        sys.exit(1)
    return result


def pip_install(package):
    run([sys.executable, "-m", "pip", "install", "--quiet", "--upgrade", package])


def check_package(package):
    result = subprocess.run(
        [sys.executable, "-m", "pip", "show", package],
        capture_output=True, text=True
    )
    return result.returncode == 0


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  Giant Pinhole Camera — MkDocs Setup")
    print("=" * 60)

    # 1. Install dependencies
    print("\n[1/5] Checking Python dependencies...")
    for pkg in ("mkdocs", "mkdocs-material"):
        if check_package(pkg):
            print(f"  {pkg} already installed — OK")
        else:
            print(f"  Installing {pkg}...")
            pip_install(pkg)
            print(f"  {pkg} installed.")

    # 2. Create directory structure
    print("\n[2/5] Creating published/ directory structure...")
    DOCS_DIR.mkdir(exist_ok=True)
    ASSETS_DIR.mkdir(exist_ok=True)
    print(f"  {DOCS_DIR}")
    print(f"  {ASSETS_DIR}")

    # 3. Copy markdown files
    print("\n[3/5] Copying markdown files...")
    for src_name, (subdir, _title) in MD_FILES:
        src = PROJECT_ROOT / src_name
        if subdir == ".":
            dst = DOCS_DIR / src_name
        else:
            target_dir = DOCS_DIR / subdir
            target_dir.mkdir(parents=True, exist_ok=True)
            dst = target_dir / src_name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  {src_name} → published/{dst.relative_to(DOCS_DIR)}")
        else:
            print(f"  WARNING: {src_name} not found — skipping")

    # 4. Copy image assets
    print("\n[4/5] Copying image assets...")
    for img_name in ASSET_IMAGE_FILES:
        src = PROJECT_ROOT / "assets" / img_name
        if src.exists():
            shutil.copy2(src, ASSETS_DIR / img_name)
            print(f"  assets/{img_name} → published/assets/{img_name}")
        else:
            print(f"  WARNING: assets/{img_name} not found — skipping")
    for img_name in DIAG_IMAGE_FILES:
        src = PROJECT_ROOT / "diagrams" / img_name
        if src.exists():
            shutil.copy2(src, ASSETS_DIR / img_name)
            print(f"  diagrams/{img_name} → published/assets/{img_name}")
        else:
            print(f"  WARNING: diagrams/{img_name} not found — skipping")

    # 5. Write mkdocs.yml
    print("\n[5/5] Writing mkdocs.yml and published/index.md...")

    nav_entries = []
    for src_name, (subdir, title) in MD_FILES:
        if subdir == ".":
            path = src_name
        else:
            path = f"{subdir}/{src_name}"
        nav_entries.append(f'  - "{title}": {path}')

    yml_content = MKDOCS_YML.format(
        site_name=SITE_NAME,
        site_description=SITE_DESCRIPTION,
        site_url=SITE_URL,
        nav_entries="\n".join(nav_entries),
    )
    (PROJECT_ROOT / "mkdocs.yml").write_text(yml_content)
    print("  mkdocs.yml written")

    (DOCS_DIR / "index.md").write_text(INDEX_MD)
    print("  published/index.md written")

    # Done
    print("\n" + "=" * 60)
    print("  Setup complete.")
    print("=" * 60)
    print("""
Next steps:

  Preview locally (hot-reload):
    mkdocs serve
    → open http://127.0.0.1:8000

  Build static site:
    mkdocs build
    → output goes to site/

  Deploy to GitHub Pages (requires git remote set up):
    mkdocs gh-deploy
    → pushes to gh-pages branch; live at your SITE_URL

  Refresh after editing .md files:
    bash publish.sh

  Edit SITE_URL in this script once your GitHub repo is created.
""")


if __name__ == "__main__":
    main()
