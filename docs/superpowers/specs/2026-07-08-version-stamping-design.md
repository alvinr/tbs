<!-- SPDX-License-Identifier: AGPL-3.0-only -->
<!-- © 2026 Alvin Richards -->
# Version Stamping — Design Spec

**Goal:** show the released version (e.g. `v0.2`) on every PDF page and every mkdocs page, and make a
release update it everywhere automatically.

## Single source (no drift)

The version already lives in **RELEASE.md** (the latest `## [X.Y]` header that `release.sh` promotes
and tags) and the matching git tag. We do **not** introduce a second copy (an early idea to store it in
`mkdocs.yml extra.version` was rejected — that is exactly the drift the project's single-source rule
prevents). Instead every consumer **derives** it:

- `src/generators/tbs_version.py` → `current_version()` — reads RELEASE.md, returns the first
  `## [X.Y]` header (skips `[Unreleased]`). The one place the parse lives.

## Consumers

| Surface | How it reads the version | How it renders |
|---|---|---|
| **Brochure PDF** | imports `current_version()` → `BROCHURE_VERSION` | `footer()`: three overlaid full-width cells — copyright **left**, `v{ver}` **center**, chapter/page **right** |
| **mkdocs site** | build hook `mkdocs_version_hook.py` `on_config` → `config.extra.version` | footer override `overrides/partials/copyright.html`: copyright **left**, `v{ver}` **right** (flex, space-between) |

`mkdocs.yml` gains only `theme.custom_dir: overrides` and a `hooks:` entry — **no** stored version.
Both are mirrored into the `MKDOCS_YML` template in `setup_docs.py` (which regenerates `mkdocs.yml`),
so a setup run won't clobber them.

## Release flow (`release.sh`)

Promoting RELEASE.md **is** the version bump, so there is no separate bump step. The one addition: after
committing the promotion, `release.sh` runs `publish.sh` to deploy the site + regenerate the brochure at
the new version, then tags/pushes and creates the GitHub release. Order:

`gate → promote RELEASE.md → commit → publish (site + brochure @ new version) → tag → push → gh release`

## Invariant

There is exactly one editable home for the version (RELEASE.md). The PDF stamp, the site footer, the git
tag, and the GitHub release all trace back to it; none can disagree.
