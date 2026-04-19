#!/usr/bin/env python3
"""
setup_docs.py — One-time setup for the Giant Pinhole Camera MkDocs site.

Run once from the project root:
    python3 setup_docs.py

What it does:
  1. Checks / installs mkdocs and mkdocs-material
  2. Creates the docs/ directory structure
  3. Copies .md files and images into docs/
  4. Writes mkdocs.yml
  5. Writes a docs/index.md landing page
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
DOCS_DIR = PROJECT_ROOT / "docs"
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
    ("project-cost-breakdown.md",        (".",           "Cost Breakdown")),
    ("pinhole-optics-report.md",         (".",           "Pinhole Optics Report")),
    ("pinhole-option-b-optics.md",       (".",           "Container Optics")),
    ("lens-options.md",                  (".",           "Lens Options")),
    ("lens-vs-pinhole-exposure.md",      (".",           "Lens vs Pinhole")),
    ("container-transport-options.md",   (".",           "Transportation")),
    ("photosensitive-plane-options.md",  (".",           "Photosensitive Materials")),
    ("water-system-report.md",           (".",           "Processing System")),
    ("film-plane-mechanism-report.md",   (".",           "Film Plane Mechanism")),
    ("pinhole-camera-construction.md",   (".",           "Construction Guide")),
    ("fabrication-drawings.md",          (".",           "Pinhole Fab")),
    ("tilt-swing-board-report.md",       (".",           "Tilt-Swing Front Board")),
    ("chemistry-shopping-list.md",       (".",           "Chem Shopping List")),
    ("funding-proposal.md",              (".",           "Funding Proposal")),

]

# Images to copy into assets/
IMAGE_FILES = [
    "plate-drawing-sheet1.png",
    "plate-drawing-sheet2.png",
    "portrait-camera-schematic.png",
    "portrait-optimal-3m.png",
    "portrait-scale-comparison.png",
    "water-system-sheet1.png",
    "water-system-sheet2.png",
    "logo-final.png",
    "favicon.png",
    "film-plane-sheet1.png",
    "film-plane-sheet2.png",
    "film-plane-sheet3.png",
    "film-plane-sheet4.png",
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

copyright: "The Big Shoebox Project (c) 2026 Alvin Richards"
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
| [Pinhole Optics Report](pinhole-optics-report.md) | Lord Rayleigh formula, f-numbers, exposure calculations |
| [Container Optics](pinhole-option-b-optics.md) | Detailed optics for the shipping container configuration |
| [Construction Guide](pinhole-camera-construction.md) | Light-sealing, pinhole plate fabrication, image plane loading |
| [Lens Options](lens-options.md) | Coverage problem, thin lens equations, DoF, distortion, recommendations |
| [Lens vs Pinhole](lens-vs-pinhole-exposure.md) | Why the exposure difference is ~5,500× — full derivation |
| [Photosensitive Materials](photosensitive-plane-options.md) | All process options, ISO equivalents, spectral response, per-image costs |
| [Processing System](water-system-report.md) | Off-grid three-circuit water system design and Bill of Materials |
| [Film Plane Mechanism](film-plane-mechanism-report.md) | 4-corner independent actuation — design, drawings, shopping list |
| [Fabrication Drawings](fabrication-drawings.md) | Interchangeable plate system — wall frame, pinhole plate, lens plate |
| [Tilt-Swing Front Board](tilt-swing-board-report.md) | Spherical-pivot mechanism — design, drawings, combined distortion renders |
| [Cost Breakdown](project-cost-breakdown.md) | Full itemised build cost — three scenarios, all sources cited |
| [Chem Shopping List](chemistry-shopping-list.md) | 50-print quantities with supplier URLs and confirmed prices |
| [Transportation](container-transport-options.md) | Commercial hire vs. self-haul analysis |
| [Funding Proposal](funding-proposal.md) | Structured pitch outline for arts foundations, MFA boards, residency programs |

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
    print("\n[2/5] Creating docs/ directory structure...")
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
            print(f"  {src_name} → docs/{dst.relative_to(DOCS_DIR)}")
        else:
            print(f"  WARNING: {src_name} not found — skipping")

    # 4. Copy image assets
    print("\n[4/5] Copying image assets...")
    for img_name in IMAGE_FILES:
        src = PROJECT_ROOT / img_name
        if src.exists():
            shutil.copy2(src, ASSETS_DIR / img_name)
            print(f"  {img_name} → docs/assets/{img_name}")
        else:
            print(f"  WARNING: {img_name} not found — skipping")

    # 5. Write mkdocs.yml
    print("\n[5/5] Writing mkdocs.yml and docs/index.md...")

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
    print("  docs/index.md written")

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
