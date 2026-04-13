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
DOCS_DIR="$SCRIPT_DIR/docs"
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
    error "docs/ directory not found. Run: python3 setup_docs.py"
fi

# ── Sync markdown files ───────────────────────────────────────────────────────
info "Syncing markdown files to docs/..."

MD_FILES=(
    "pinhole-optics-report.md"
    "pinhole-option-b-optics.md"
    "pinhole-camera-construction.md"
    "lens-options.md"
    "lens-vs-pinhole-exposure.md"
    "photosensitive-plane-options.md"
    "chemistry-shopping-list.md"
)

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
info "Syncing image assets to docs/assets/..."

mkdir -p "$ASSETS_DIR"

IMG_FILES=(
    "plate-drawing-sheet1.png"
    "plate-drawing-sheet2.png"
    "portrait-camera-schematic.png"
    "portrait-optimal-3m.png"
    "portrait-scale-comparison.png"
)

for f in "${IMG_FILES[@]}"; do
    src="$SCRIPT_DIR/$f"
    dst="$ASSETS_DIR/$f"
    if [[ ! -f "$src" ]]; then
        warn "$f not found — skipping"
        continue
    fi
    if [[ ! -f "$dst" ]] || [[ "$src" -nt "$dst" ]]; then
        cp "$src" "$dst"
        echo "    updated: $f"
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
