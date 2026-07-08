# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
mkdocs build hook — expose the released version to templates without storing it.

Registered in mkdocs.yml `hooks:`. On build it derives the version from RELEASE.md
(via tbs_version.current_version) and sets config.extra.version, which the footer
override (overrides/partials/copyright.html) renders. Keeps RELEASE.md the single
source — nothing version-shaped is hand-maintained in mkdocs.yml.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tbs_version import current_version  # noqa: E402


def on_config(config, **kwargs):
    extra = config.get("extra") or {}
    extra["version"] = current_version()
    config["extra"] = extra
    return config
