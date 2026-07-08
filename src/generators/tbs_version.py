#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
tbs_version.py — single source for the project's released version.

The version is NOT stored anywhere of its own; it is derived from RELEASE.md's
latest `## [X.Y]` header (the same section `release.sh` promotes and tags), so
there is exactly one home for it and it cannot drift. Consumed by the brochure
(footer stamp) and the mkdocs site (via mkdocs_version_hook.py → config.extra.version).
"""

import os
import re

_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
RELEASE_MD = os.path.join(_ROOT, "RELEASE.md")

# First `## [X.Y]` header, skipping `## [Unreleased]` (which isn't digits).
_VER_RE = re.compile(r"^##\s*\[(\d+(?:\.\d+)*)\]")


def current_version(release_md=RELEASE_MD):
    """Return the latest released version (e.g. '0.2') from RELEASE.md, or '' if unknown."""
    try:
        with open(release_md, encoding="utf-8") as f:
            for line in f:
                m = _VER_RE.match(line)
                if m:
                    return m.group(1)
    except OSError:
        pass
    return ""


if __name__ == "__main__":
    print(current_version())
