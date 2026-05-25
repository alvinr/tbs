#!/usr/bin/env bash
# publish.sh — Sync docs and redeploy to GitHub Pages.
#
# Usage:
#   bash publish.sh            # sync + deploy
#   bash publish.sh --local    # sync + serve locally only (no deploy)
#   bash publish.sh --build    # sync + build to site/ only (no deploy)
#
# Run from the project root (same directory as mkdocs.yml).
# Requires: mkdocs, mkdocs-material (run setup_docs.py first).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_DIR="$SCRIPT_DIR/published"
ASSETS_DIR="$DOCS_DIR/assets"

MODE="deploy"
if [[ "${1:-}" == "--local" ]]; then MODE="local"; fi
if [[ "${1:-}" == "--build" ]]; then MODE="build"; fi

# ── Colours ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
info()    { echo -e "${GREEN}[+]${NC} $*"; }
warn()    { echo -e "${YELLOW}[!]${NC} $*"; }
error()   { echo -e "${RED}[✗]${NC} $*"; exit 1; }

# ── Preflight checks ─────────────────────────────────────────────────────────
info "Preflight checks..."

if ! python3 -m mkdocs --version &>/dev/null; then
    error "mkdocs not found. Run: /usr/bin/python3 -m pip install mkdocs mkdocs-material"
fi

if [[ ! -f "$SCRIPT_DIR/mkdocs.yml" ]]; then
    error "mkdocs.yml not found. Run: python3 setup_docs.py"
fi

if [[ ! -d "$DOCS_DIR" ]]; then
    error "published/ directory not found. Run: python3 setup_docs.py"
fi

# ── Sync markdown files ───────────────────────────────────────────────────────
info "Syncing markdown files to published/..."

MD_FILES=(
    "pinhole-optics-report.md"
    "pinhole-option-b-optics.md"
    "pinhole-camera-construction.md"
    "lens-options.md"
    "lens-vs-pinhole-exposure.md"
    "photosensitive-plane-options.md"
    "chemistry-shopping-list.md"
    "container-transport-options.md"
    "water-system-report.md"
    "film-plane-mechanism-report.md"
    "project-cost-breakdown.md"
    "fabrication-drawings.md"
    "tilt-swing-board-report.md"
    "funding-proposal.md"
    "operating-manual.md"
    "electrical-report.md"
    "master-shopping-list.md"
    "licensing.md"
    "light-trap-selection.md"
    "engineering-diagrams.md"
    "distortion-renders.md"
    "equipment-layout-report.md"
    "component-dependency-map.md"
    "weight-distribution-report.md"
    "chemistry-prep-shelves.md"
    "mini-tbs/mini-tbs-poc.md"
    "mini-tbs/mini-tbs-shopping-list.md"
)

# ── Home page: sync project-summary.md → docs/index.md ───────────────────────
info "Syncing home page (project-summary.md → published/index.md)..."
SUMMARY_SRC="$SCRIPT_DIR/project-summary.md"
INDEX_DST="$DOCS_DIR/index.md"
if [[ ! -f "$SUMMARY_SRC" ]]; then
    warn "project-summary.md not found — home page not updated"
elif [[ ! -f "$INDEX_DST" ]] || [[ "$SUMMARY_SRC" -nt "$INDEX_DST" ]]; then
    cp "$SUMMARY_SRC" "$INDEX_DST"
    echo "    updated: published/index.md"
fi

mkdir -p "$DOCS_DIR/mini-tbs"

CHANGED=0
for f in "${MD_FILES[@]}"; do
    src="$SCRIPT_DIR/$f"
    dst="$DOCS_DIR/$f"
    if [[ ! -f "$src" ]]; then
        warn "$f not found in project root — skipping"
        continue
    fi
    # Copy only if source is newer or destination doesn't exist
    if [[ ! -f "$dst" ]] || [[ "$src" -nt "$dst" ]]; then
        cp "$src" "$dst"
        echo "    updated: $f"
        CHANGED=$((CHANGED + 1))
    fi
done

# ── Sync image assets ─────────────────────────────────────────────────────────
info "Syncing image assets to published/assets/..."

mkdir -p "$ASSETS_DIR"

# Images stored in assets/ (not root, not diagrams/)
ASSET_FILES=(
    "logo-final.png"
    "favicon.png"
)

for f in "${ASSET_FILES[@]}"; do
    src="$SCRIPT_DIR/assets/$f"
    dst="$ASSETS_DIR/$f"
    if [[ ! -f "$src" ]]; then
        warn "assets/$f not found — skipping"
        continue
    fi
    if [[ ! -f "$dst" ]] || [[ "$src" -nt "$dst" ]]; then
        cp "$src" "$dst"
        echo "    updated: assets/$f"
        CHANGED=$((CHANGED + 1))
    fi
done

# Generated diagram images (all live in diagrams/)
DIAG_FILES=(
    "portrait-camera-schematic.png"
    "portrait-optimal-3m.png"
    "portrait-scale-comparison.png"
    "water-system-sheet1.png"
    "water-system-sheet2.png"
    "film-plane-sheet1.png"
    "film-plane-sheet2.png"
    "film-plane-sheet3.png"
    "film-plane-sheet4.png"
    "film-plane-sheet5.png"
    "film-plane-distortion-c0.png"
    "film-plane-distortion-c1.png"
    "film-plane-distortion-c2.png"
    "film-plane-distortion-c3.png"
    "film-plane-distortion-c4.png"
    "film-plane-distortion-c5.png"
    "film-plane-distortion-c6.png"
    "film-plane-distortion-summary.png"
    "tilt-swing-board-sheet1.png"
    "tilt-swing-board-sheet2.png"
    "tilt-swing-board-sheet3.png"
    "tilt-swing-combined-c0.png"
    "tilt-swing-combined-c1.png"
    "tilt-swing-combined-c2.png"
    "tilt-swing-combined-c3.png"
    "tilt-swing-combined-c4.png"
    "tilt-swing-combined-c5.png"
    "tilt-swing-combined-c6.png"
    "tilt-swing-combined-c7.png"
    "tilt-swing-combined-c8.png"
    "tilt-swing-combined-summary.png"
    "electrical-sheet1.png"
    "electrical-sheet2.png"
    "electrical-sheet3.png"
    "power-panel-sheet1.png"
    "lighttrap-sheet1.png"
    "lighttrap-sheet2.png"
    "hingepanel-sheet1.png"
    "hingepanel-sheet2.png"
    "hingepanel-sheet3.png"
    "hingepanel-sheet4.png"
    "container-floorplan.png"
    "container-floorplan-sheet2.png"
    "assembly-overview.png"
    "assembly-overview-fp.png"
    "assembly-overview-plan.png"
    "assembly-fab-sheet1.png"
    "assembly-fab-sheet2.png"
    "line-of-sight.png"
    "plate-drawing-sheet1.png"
    "plate-drawing-sheet2.png"
    "ceiling-rail-sheet1.png"
    "ceiling-rail-sheet2.png"
    "walkway-sheet1.png"
    "walkway-sheet2.png"
    "walkway-sheet3.png"
    "walkway-sheet4.png"
    "walkway-sheet5.png"
    "walkway-sheet6.png"
    "ibc-stacking-sheet1.png"
    "ibc-stacking-sheet2.png"
    "ibc-stacking-sheet3.png"
    "ibc-stacking-sheet4.png"
    "ibc-stacking-sheet5.png"
    "ibc-frame-sheet1.png"
    "ibc-frame-sheet2.png"
    "ibc-frame-sheet3.png"
    "water-system-sheet3.png"
    "water-system-sheet4.png"
    "mini-tbs-sheet1.png"
    "weight-analysis-sheet1.png"
    "weight-analysis-sheet2.png"
    "weight-analysis-sheet3.png"
    "weight-analysis-sheet4.png"
    "shelf-sheet1.png"
    "shelf-sheet2.png"
    "shelf-sheet3.png"
    "pinhole-wall-elevation.png"
    "panel-layout.png"
    "spray-bar-sheet1.png"
    "spray-bar-sheet2.png"
    "spray-bar-sheet3.png"
    "spray-bar-sheet4.png"
    "spray-bar-sheet5.png"
    "spray-bar-sheet6.png"
)

for f in "${DIAG_FILES[@]}"; do
    src="$SCRIPT_DIR/diagrams/$f"
    dst="$ASSETS_DIR/$f"
    if [[ ! -f "$src" ]]; then
        warn "diagrams/$f not found — skipping"
        continue
    fi
    if [[ ! -f "$dst" ]] || [[ "$src" -nt "$dst" ]]; then
        cp "$src" "$dst"
        echo "    updated: diagrams/$f"
        CHANGED=$((CHANGED + 1))
    fi
done

if [[ $CHANGED -eq 0 ]]; then
    info "No files changed since last sync."
else
    info "$CHANGED file(s) updated."
fi

# ── Build / deploy ────────────────────────────────────────────────────────────
cd "$SCRIPT_DIR"

case "$MODE" in
    local)
        info "Starting local preview server..."
        echo ""
        echo "  Open: http://127.0.0.1:8000"
        echo "  Hot-reload is active — edit .md files and the browser updates."
        echo "  Press Ctrl-C to stop."
        echo ""
        python3 -m mkdocs serve
        ;;
    build)
        info "Building static site..."
        python3 -m mkdocs build --clean
        info "Built to: $SCRIPT_DIR/site/"
        echo ""
        echo "  Open site/index.html in a browser to preview."
        ;;
    deploy)
        # Check we're in a git repo with a remote before attempting deploy
        if ! git -C "$SCRIPT_DIR" rev-parse --git-dir &>/dev/null; then
            warn "Not a git repository. Falling back to --build mode."
            warn "To deploy to GitHub Pages, initialise a git repo and add a remote:"
            warn "  git init && git remote add origin https://github.com/you/tbs.git"
            python3 -m mkdocs build --clean
            info "Built to: $SCRIPT_DIR/site/"
        else
            REMOTE=$(git -C "$SCRIPT_DIR" remote get-url origin 2>/dev/null || echo "")
            if [[ -z "$REMOTE" ]]; then
                warn "No git remote 'origin' set. Falling back to --build mode."
                python3 -m mkdocs build --clean
                info "Built to: $SCRIPT_DIR/site/"
            else
                info "Deploying to GitHub Pages (gh-pages branch)..."
                python3 -m mkdocs gh-deploy --clean --force
                info "Deployed. Site will be live within ~60 seconds at your SITE_URL."
            fi
        fi
        ;;
esac

# -- Generate brochure PDF ----------------------------------------------------
if [[ "$MODE" != "local" ]]; then
    if python3 -c "import fpdf, markdown, yaml" 2>/dev/null; then
        info "Generating brochure PDF..."
        if python3 "${SCRIPT_DIR}/generate_brochure.py"; then
            info "PDF -> tbs-brochure.pdf"
        else
            warn "PDF generation failed -- check generate_brochure.py output above"
        fi
    else
        warn "fpdf2 / markdown / pyyaml not installed -- skipping PDF generation"
        warn "  Install: python3 -m pip install --user fpdf2 markdown pyyaml"
    fi
fi
