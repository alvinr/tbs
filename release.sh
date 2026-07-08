#!/usr/bin/env bash
# release.sh — cut a versioned release for TBS-001.
#
# THE GATE: refuses to run if RELEASE.md's [Unreleased] section is empty, so no release
# ever ships without a changelog entry.
#
#   bash release.sh 0.2
#
# Steps: verify [Unreleased] has content -> promote it to "## [X.Y] — <date>" (leaving a
# fresh empty [Unreleased]) -> commit RELEASE.md -> tag X.Y -> push -> gh release create X.Y.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VERSION="${1:-}"
if [[ -z "$VERSION" ]]; then
    echo "usage: bash release.sh <version>    e.g.  bash release.sh 0.2" >&2
    exit 1
fi
RL="RELEASE.md"
[[ -f "$RL" ]] || { echo "error: $RL not found" >&2; exit 1; }

if git rev-parse -q --verify "refs/tags/$VERSION" >/dev/null 2>&1; then
    echo "error: tag '$VERSION' already exists" >&2; exit 1
fi

# ── GATE: no unused imports (code hygiene must not drift back in) ─────────────
if ! python3 src/generators/check_unused_imports.py >/dev/null 2>&1; then
    echo "GATE FAILED — unused imports present. Run to fix:" >&2
    echo "    python3 src/generators/check_unused_imports.py --fix" >&2
    python3 src/generators/check_unused_imports.py >&2 || true
    exit 1
fi

# ── GATE: the [Unreleased] section must carry real content ────────────────────
unreleased="$(awk '/^## \[Unreleased\]/{f=1; next} f && /^## /{exit} f{print}' "$RL" \
    | sed '/^[[:space:]]*$/d; /^_.*_[[:space:]]*$/d')"     # drop blank lines + the italic placeholder
if [[ -z "$unreleased" ]]; then
    echo "GATE FAILED — RELEASE.md [Unreleased] is empty; nothing to release." >&2
    echo "Add a bullet per notable change under [Unreleased], then re-run." >&2
    exit 1
fi

echo "Changes queued for release $VERSION:"
echo "$unreleased" | sed 's/^/    /'
read -r -p "Promote, tag, and publish GitHub release $VERSION? [y/N] " ans
[[ "$ans" == [yY] ]] || { echo "aborted."; exit 1; }

DATE="$(date +%Y-%m-%d)"
# ── Promote [Unreleased] -> [VERSION] — DATE, leaving a fresh empty [Unreleased] ──
tmp="$(mktemp)"
awk -v ver="$VERSION" -v d="$DATE" '
    /^## \[Unreleased\]/ {
        print "## [Unreleased]"; print "";
        print "_Nothing yet — add a bullet per notable change here as work lands._"; print "";
        print "## [" ver "] — " d;
        next
    }
    { print }
' "$RL" > "$tmp" && mv "$tmp" "$RL"

git add "$RL"
git commit -q -m "release $VERSION"

# Publish the new-version site + brochure. The version is DERIVED from the just-promoted
# RELEASE.md (single source, via tbs_version), so the site footer + PDF stamp pick up $VERSION
# automatically — nothing else to bump.
echo "Publishing site + brochure at $VERSION ..."
PATH=/usr/bin:$PATH bash publish.sh

git tag -a "$VERSION" -m "Release $VERSION"
git push origin HEAD --follow-tags

# ── GitHub release; notes = the just-promoted version section ──────────────────
notes="$(awk -v ver="$VERSION" 'index($0,"## ["ver"]")==1{f=1;next} f&&/^## /{exit} f{print}' "$RL")"
gh release create "$VERSION" --title "$VERSION" --notes "$notes"
echo "✓ Released $VERSION — https://github.com/alvinr/tbs/releases/tag/$VERSION"
