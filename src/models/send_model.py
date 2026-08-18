#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""Unified send + optional Sketchfab push for ONE logical model — the cascade convenience wrapper.

Maps a logical model name to its generator via dependencies.yml, delegates the build/send to that
generator, then OPTIONALLY pushes the live model to Sketchfab in place (same UID/URL, settings kept).

    python3 src/models/send_model.py <name> --send           # rebuild into the ACTIVE SketchUp doc
    python3 src/models/send_model.py <name> --send --push     # ...then OFFER to push it (after you validate)
    python3 src/models/send_model.py <name> --push            # just push the live model in place
    python3 src/models/send_model.py <name> --send --push -y  # non-interactive: skip the validate prompt
    python3 src/models/send_model.py <name> --push --new      # legacy: POST a fresh model (resets settings)

--push runs the in-place PUT (push_sketchfab.push_in_place): same public URL, viewer settings/materials/name
preserved. It PROMPTS you to validate the model in SketchUp first (unless -y). In a non-interactive shell
(no TTY) it does NOT hang — it skips with a note so you can run the push yourself once you've eyeballed it.
Token-gated: with no SKETCHFAB_API_TOKEN the push is skipped (the --send still runs). The push's own
single-writer guard still applies (the live doc must be the saved <name>.skp).
"""
import argparse
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src", "generators"))
sys.path.insert(0, os.path.dirname(__file__))
import deps            # noqa: E402
import push_sketchfab as pf  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="Send a model to SketchUp and optionally push it to Sketchfab.")
    ap.add_argument("name", help="logical model name (see dependencies.yml models:)")
    ap.add_argument("--save", action="store_true", help="write the model's .rb")
    ap.add_argument("--send", action="store_true", help="build into the ACTIVE SketchUp doc (delegates to the generator)")
    ap.add_argument("--push", action="store_true", help="after --send, offer to push the live model to Sketchfab in place")
    ap.add_argument("--new", action="store_true", help="push as a NEW model (POST) instead of in-place PUT — resets viewer settings")
    ap.add_argument("-y", "--yes", action="store_true", help="skip the validate-then-push confirmation prompt")
    args = ap.parse_args()

    models = {n: e for n, e in deps.ENTRIES.items() if e.get("kind") == "model"}
    if args.name not in models:
        sys.exit(f"error: '{args.name}' not in dependencies.yml models (known: {', '.join(models) or 'none'})")
    entry = models[args.name]
    script = os.path.join(ROOT, entry["script"])

    # 1. Delegate the build/send to the model's own generator (reuse its exact --save/--send).
    flags = [f for f, on in (("--save", args.save), ("--send", args.send)) if on]
    if flags:
        rc = subprocess.run([sys.executable, script, *flags]).returncode
        if rc != 0:
            sys.exit(f"error: {os.path.basename(script)} {' '.join(flags)} failed (rc {rc}).")

    # 2. Optionally push. Token-gated, validate-prompt-gated, and non-interactive-safe (won't hang).
    if not (args.push or args.new):
        return
    pf.load_env_private()
    token = os.environ.get("SKETCHFAB_API_TOKEN", "").strip()
    if not token:
        print("  --push: SKETCHFAB_API_TOKEN not set — skipping Sketchfab push (the --send is done).")
        return
    if not args.yes:
        if not sys.stdin.isatty():
            print(f"  --push: non-interactive shell — NOT pushing automatically. Validate '{args.name}' in "
                  f"SketchUp, then run:  python3 src/models/push_sketchfab.py {args.name}"
                  f"{' --new' if args.new else ''}")
            return
        verb = "POST a NEW model for" if args.new else "push (in-place, same UID)"
        ans = input(f"  Validate '{args.name}' in SketchUp, then {verb} on Sketchfab? [y/N] ")
        if ans.strip().lower() not in ("y", "yes"):
            print("  --push: skipped.")
            return
    (pf.push_new_model if args.new else pf.push_in_place)(token, args.name, entry)


if __name__ == "__main__":
    main()
