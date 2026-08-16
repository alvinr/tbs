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
    error "mkdocs.yml not found. Run: python3 src/generators/setup_docs.py"
fi

if [[ ! -d "$DOCS_DIR" ]]; then
    error "published/ directory not found. Run: python3 src/generators/setup_docs.py"
fi

# ── Publish gate: full-sweep model verification (deploy only — it regenerates all 7 model .rb,
#    ~1 min). Catches committed-stale outputs that lint's staged-diff missing-cascade check misses
#    (the film-plane-model slip). Regenerates IN PLACE, so a stale .rb is left fresh — commit + re-send. ──
if [[ "$MODE" == "deploy" ]]; then
    info "Publish gate: verifying no stale model outputs (lint --verify-all)..."
    if ! /usr/bin/python3 "$SCRIPT_DIR/src/generators/lint.py" --verify-all; then
        error "Stale model outputs (regenerated in place above) — commit them + re-send the affected .skp, then re-run."
    fi
fi

# ── Sync markdown files ───────────────────────────────────────────────────────
info "Syncing markdown files to published/..."

MD_FILES=(
    "container-report.md"
    "pinhole-optics-report.md"
    "pinhole-option-b-optics.md"
    "lens-options.md"
    "lens-vs-pinhole-exposure.md"
    "photosensitive-plane-options.md"
    "chemistry-shopping-list.md"
    "sensitizer-trials.md"
    "container-transport-options.md"
    "water-system-report.md"
    "film-plane-mechanism-report.md"
    "film-plane-mechanism-analysis.md"
    "film-clamp-mechanism-report.md"
    "project-cost-breakdown.md"
    "cost-analysis-report.md"
    "tray-research.md"
    "pinhole-report.md"
    "tilt-swing-board-report.md"
    "tilt-swing-board-analysis.md"
    "funding-proposal.md"
    "operating-manual.md"
    "electrical-report.md"
    "electrical-safety-report.md"
    "daily-energy-report.md"
    "master-shopping-list.md"
    "licensing.md"
    "light-trap-selection.md"
    "engineering-diagrams.md"
    "distortion-renders.md"
    "equipment-layout-report.md"
    "component-dependency-map.md"
    "component-dimension-audit.md"
    "weight-distribution-report.md"
    "chemistry-prep-shelves.md"
    "processing-tray-and-spray-bar.md"
    "hinged-panel-report.md"
    "walkway-report.md"
    "right-walkway-cantilever-study.md"
    "process-comparison.md"
    "plumbing-report.md"
    "walkway-routing-sections.md"
    "ibc-stacking-report.md"
    "ventilation-report.md"
    "all-diagrams.md"
    "construction-report.md"
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

# ── Prune orphaned docs: drop published/*.md no longer listed in MD_FILES ──────
# publish.sh only ever COPIES MD_FILES into published/; without this a retired or
# renamed doc lingers there and mkdocs builds it as an unlisted (orphan) page that
# stays reachable by URL. index.md is the generated home page, so it is kept.
KEEP_LIST="index.md"
for f in "${MD_FILES[@]}"; do KEEP_LIST="$KEEP_LIST"$'\n'"$f"; done
while IFS= read -r existing; do
    rel="${existing#"$DOCS_DIR"/}"
    if ! grep -qxF -- "$rel" <<<"$KEEP_LIST"; then
        rm -f "$existing"
        echo "    pruned (retired — not in MD_FILES): $rel"
        CHANGED=$((CHANGED + 1))
    fi
done < <(find "$DOCS_DIR" -name '*.md' -type f)

# ── Write the tablesort init (makes every doc table click-sortable) ───────────
mkdir -p "$DOCS_DIR/javascripts"
cat > "$DOCS_DIR/javascripts/tablesort.js" <<'JS'
// Make every plain markdown table click-sortable (Material instant-loading aware), with
// money-aware numeric sorting so the BOM "Est. cost" / "Qty" columns sort by value, not as text
// (otherwise "$1,170" lands before "$30"). A money/number cell sorts by its first number; a range
// like "$30–$50" sorts by its low value.
if (window.Tablesort) {
  Tablesort.extend("money",
    function (item) { return /^\s*[~$]?\s*-?[\d,]+/.test(item); },
    function (a, b) {
      function num(s) {
        var m = String(s).replace(/,/g, "").match(/-?\d+(\.\d+)?/);
        return m ? parseFloat(m[0]) : 0;
      }
      return num(a) - num(b);
    });
}
// A total / subtotal row is a footer, not data — move it to <tfoot> so tablesort (which only ever
// sorts <tbody> rows) leaves it pinned at the bottom instead of shuffling it into the sort. Detect it
// by CONTENT, not formatting: the BOM total rows have every middle column (Qty/Supplier/Systems) blank;
// the summary/scenario total rows fill every column but are labelled "total" in the first cell.
function isFooterRow(row) {
  var c = row.cells, n = c.length;
  if (!n) return false;
  if (n >= 3) {
    var middleBlank = true;
    for (var i = 1; i < n - 1 && middleBlank; i++) middleBlank = c[i].textContent.trim() === "";
    if (middleBlank) return true;
  }
  return /total/i.test(c[0].textContent);   // "...total" / "...subtotal" / "TOTAL"
}
document$.subscribe(function () {
  document.querySelectorAll("article table:not([class])").forEach(function (table) {
    var tbody = table.tBodies[0];
    if (tbody) {
      Array.prototype.slice.call(tbody.rows).forEach(function (row) {
        if (isFooterRow(row)) (table.tFoot || table.createTFoot()).appendChild(row);
      });
    }
    if (!table.dataset.sortInit) { table.dataset.sortInit = "1"; new Tablesort(table); }
  });
});
JS

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
    "film-plane-sheet6.png"
    "film-plane-sheet7.png"
    "film-plane-sheet8.png"
    "film-plane-sheet9.png"
    "film-plane-sheet10.png"
    "film-joint-options.png"
    "film-joint-study-gimbal.png"
    "film-joint-study-ujoint.png"
    "film-corner-gimbal.png"
    "film-plane-distortion-c0.png"
    "film-plane-distortion-c1.png"
    "film-plane-distortion-c2.png"
    "film-plane-distortion-c3.png"
    "film-plane-distortion-c4.png"
    "film-plane-distortion-c5.png"
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
    "tilt-swing-board-distortion-c0.png"
    "tilt-swing-board-distortion-c1.png"
    "tilt-swing-board-distortion-c2.png"
    "tilt-swing-board-distortion-c3.png"
    "tilt-swing-board-distortion-c4.png"
    "tilt-swing-board-distortion-c5.png"
    "tilt-swing-board-distortion-c6.png"
    "tilt-swing-board-distortion-summary.png"
    "tilt-swing-sheet1.png"
    "tilt-swing-sheet2.png"
    "electrical-sheet1.png"
    "electrical-sheet2.png"
    "electrical-sheet3.png"
    "electrical-sheet4.png"
    "electrical-sheet5.png"
    "electrical-sheet6.png"
    "electrical-sheet7.png"
    "lighttrap-sheet1.png"
    "lighttrap-sheet2.png"
    "hingepanel-sheet1.png"
    "hingepanel-sheet2.png"
    "hingepanel-sheet3.png"
    "hingepanel-sheet4.png"
    "hingepanel-sheet5.png"
    "hingepanel-sheet6.png"
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
    "walkway-sheet1.png"
    "grp-cutplan.png"
    "walkway-sheet2.png"
    "walkway-sheet3.png"
    "walkway-sheet4.png"
    "walkway-sheet5.png"
    "walkway-sheet6.png"
    "walkway-sheet7.png"
    "walkway-sheet8.png"
    "walkway-sheet9.png"
    "ibc-stacking-sheet1.png"
    "ibc-stacking-sheet2.png"
    "ibc-stacking-sheet3.png"
    "ibc-stacking-sheet4.png"
    "ibc-stacking-sheet5.png"
    "ibc-frame-sheet1.png"
    "ibc-frame-sheet2.png"
    "ibc-frame-sheet3.png"
    "ibc-frame-sheet4.png"
    "ibc-frame-sheet5.png"
    "ibc-frame-load-case.png"
    "ibc-plate-schedule-sheet1.png"
    "ibc-plate-schedule-sheet2.png"
    "water-system-sheet3.png"
    "water-system-sheet4.png"
    "mini-tbs-sheet1.png"
    "weight-analysis-sheet1.png"
    "weight-analysis-sheet2.png"
    "weight-analysis-sheet3.png"
    "weight-analysis-sheet4.png"
    "weight-analysis-sheet5.png"
    "shelf-sheet1.png"
    "shelf-sheet2.png"
    "shelf-sheet3.png"
    "pinhole-wall-elevation.png"
    "panel-layout.png"
    "support-detail-sheet1.png"
    "support-detail-sheet2.png"
    "pinhole-panel.png"
    "panel-spine-view-a.png"
    "panel-spine-view-b.png"
    "walkway-sections-sheet1.png"
    "walkway-sections-sheet2.png"
    "walkway-sections-sheet3.png"
    "walkway-sections-sheet4.png"
    "walkway-sections-sheet5.png"
    "walkway-sections-sheet6.png"
    "spray-bar-sheet1.png"
    "spray-bar-sheet2.png"
    "spray-bar-sheet3.png"
    "spray-bar-sheet4.png"
    "spray-bar-sheet5.png"
    "spray-bar-sheet6.png"
    "spray-bar-sheet7.png"
    "spray-bar-sheet8.png"
    "tray-redesign-sheet1.png"
    "tray-redesign-sheet2.png"
    "tray-slope-sheet1.png"
    "tray-slope-sheet2.png"
    "tray-slope-sheet3.png"
    "tray-slope-sheet4.png"
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

# ── Classroom brochure PDF (hosted for download) ──────────────────────────────
# Build the TBS-002 booklet and stage it in published/assets/ BEFORE the site
# build, so the "Printable Instructions" links (Educational Program nav + the
# TBS-002 page) resolve to a downloadable PDF. Must precede the build so mkdocs
# copies it into the deployed site.
if python3 -c "import fpdf, markdown, yaml" 2>/dev/null; then
    info "Generating TBS-002 classroom brochure (hosted for download)..."
    if python3 "${SCRIPT_DIR}/src/generators/generate_brochure.py" --edition tbs002; then
        cp "${SCRIPT_DIR}/tbs-002-brochure.pdf" "${ASSETS_DIR}/tbs-002-brochure.pdf"
        info "PDF -> published/assets/tbs-002-brochure.pdf"
    else
        warn "TBS-002 brochure generation failed -- Printable Instructions link will 404"
    fi
else
    warn "fpdf2 / markdown / pyyaml not installed -- TBS-002 brochure not staged (link will 404)"
fi

# ── Build / deploy ────────────────────────────────────────────────────────────
cd "$SCRIPT_DIR"

case "$MODE" in
    local)
        info "Starting local preview server..."
        echo ""
        echo "  Open: http://127.0.0.1:8000"
        echo "  Hot-reload is active — edits to root .md files auto-sync to published/."
        echo "  Press Ctrl-C to stop."
        echo ""
        # Background loop: re-sync root .md and diagrams → published/ every 2 seconds.
        # Uses rsync --update so only changed files trigger mkdocs hot-reload.
        (
            while true; do
                for f in "${MD_FILES[@]}"; do
                    [[ -f "$SCRIPT_DIR/$f" ]] && rsync -q --update "$SCRIPT_DIR/$f" "$DOCS_DIR/$f" 2>/dev/null || true
                done
                [[ -f "$SUMMARY_SRC" ]] && rsync -q --update "$SUMMARY_SRC" "$INDEX_DST" 2>/dev/null || true
                for f in "${DIAG_FILES[@]}"; do
                    [[ -f "$SCRIPT_DIR/$f" ]] && rsync -q --update "$SCRIPT_DIR/$f" "$ASSETS_DIR/$(basename "$f")" 2>/dev/null || true
                done
                sleep 2
            done
        ) &
        SYNC_PID=$!
        trap "kill $SYNC_PID 2>/dev/null" EXIT
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
            warn "To deploy to GitHub Pages, initialize a git repo and add a remote:"
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

# -- Generate the TBS-001 brochure PDF ----------------------------------------
# (The TBS-002 classroom booklet is built + staged for download before the site
# build, above.) The TBS-001 prospectus is a local artifact only, not hosted.
if [[ "$MODE" != "local" ]]; then
    if python3 -c "import fpdf, markdown, yaml" 2>/dev/null; then
        info "Generating TBS-001 brochure PDF..."
        if python3 "${SCRIPT_DIR}/src/generators/generate_brochure.py"; then
            info "PDF -> tbs-brochure.pdf (TBS-001)"
        else
            warn "PDF generation failed (TBS-001) -- check src/generators/generate_brochure.py output above"
        fi
    else
        warn "fpdf2 / markdown / pyyaml not installed -- skipping PDF generation"
        warn "  Install: python3 -m pip install --user fpdf2 markdown pyyaml"
    fi
fi

# Note: the 3D-model -> Sketchfab push lives in the model workflow, not here.
# It needs SketchUp open (to export .dae) and must rewrite the embed UID *before*
# the site builds, so run it as part of updating the model:
#   python3 src/models/generate_sketchup_model.py --save --send --sketchfab
# then `bash publish.sh` deploys the updated embed (project-summary.md).
