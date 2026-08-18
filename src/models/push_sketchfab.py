#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""Push a logical TBS-001 model to Sketchfab and keep its embed in sync.

DEFAULT — in-place re-upload (`PUT /v3/models/{uid}`): replaces the model's geometry while
keeping the SAME uid / URL and PRESERVING viewer settings, materials, name (validated
2026-08-18). Nothing else changes — no embed rewrite, no dependencies.yml uid-swap, no
old-model deletion, no viewer-settings reset. This is the leg that used to be the manual
Sketchfab upload; it now runs hands-free (the API rejects .skp, so the LIVE model is exported
to Collada .dae and PUT to the existing uid).

`--new` — the legacy path: POST a NEW model (new uid), rewrite the uid in the embed file(s)
and dependencies.yml, and delete the old model. Use only when you deliberately want a fresh
model (e.g. the first upload of a brand-new model with no uid, or to reset a broken one). This
DOES reset the Sketchfab viewer settings.

SINGLE-WRITER GUARD: the push exports whatever is LIVE in SketchUp, so it REFUSES to run unless
the active doc is the SAVED .skp for the model you named (path basename == "<name>.skp") — you
cannot push the wrong model's geometry onto a uid. Save the .skp first (ALVIN is the sole saver).

Registry — dependencies.yml (`models:` block) — provides each model's `uid` + `embed_files`;
the display name comes from the live model's name (generator SF_TITLE), only used on --new.

Credentials: SKETCHFAB_API_TOKEN (environment or the gitignored .env.private).

Usage:
    python3 src/models/push_sketchfab.py [name]          # in-place PUT (default; name default: overview)
    python3 src/models/push_sketchfab.py [name] --new    # legacy POST-new-model + rewrite + delete
"""
import json
import os
import subprocess
import sys
import time
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src", "generators"))
sys.path.insert(0, os.path.dirname(__file__))
import deps  # noqa: E402 — dependencies.yml is the single model registry (uid + embed_files)
from sketchup_client import send_ruby, SketchupError  # noqa: E402
API = "https://api.sketchfab.com/v3/models"


def load_env_private():
    path = os.path.join(ROOT, ".env.private")
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())


def api_get(token, uid):
    req = urllib.request.Request(f"{API}/{uid}",
                                 headers={"Authorization": f"Token {token}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def poll_processing(token, uid, tries=72):
    """Block until Sketchfab finishes reprocessing the new geometry."""
    print("  processing", end="", flush=True)
    for _ in range(tries):
        time.sleep(5)
        print(".", end="", flush=True)
        try:
            st = str((api_get(token, uid).get("status") or {}).get("processing", "")).upper()
        except Exception:
            st = "?"
        if st == "SUCCEEDED":
            print(" done.")
            return True
        if st == "FAILED":
            print("\n  processing FAILED on Sketchfab.")
            return False
    print("\n  warning: still processing (continuing anyway).")
    return True


def guard_live_is_saved_model(name):
    """REFUSE unless the LIVE SketchUp doc is the saved .skp for `name` — the push exports the
    live model, so this stops the wrong model's geometry landing on `name`'s uid. Returns the title."""
    try:
        info = send_ruby('m=Sketchup.active_model; "#{m.path}|#{m.title}"')
    except SketchupError as e:
        sys.exit(f"error: cannot reach SketchUp ({e}) — is it open with {name}.skp?")
    path, _, title = info.strip().strip('"').partition("|")
    base = os.path.basename(path)
    if base != f"{name}.skp":
        sys.exit(f"REFUSING: live doc is {base or '(unsaved)'!r}, not '{name}.skp'. "
                 f"Open + SAVE {name}.skp first (single-writer), then push.")
    print(f"  live doc = {base} (matches) — safe to export + push.")
    return title


def export_live_dae(name):
    dae = os.path.join(ROOT, "models", f"{name}.dae")
    if os.path.exists(dae):
        os.remove(dae)
    print(f"Exporting live SketchUp model -> models/{name}.dae ...")
    try:
        send_ruby('m=Sketchup.active_model; "e=#{m.export(' + repr(dae) + ', false)}"')
    except SketchupError as e:
        sys.exit(f"error: could not export from SketchUp ({e})")
    if not os.path.exists(dae):
        sys.exit(f"error: export did not produce {dae}")
    print(f"  exported {os.path.getsize(dae) // 1024} KB")
    return dae


def push_in_place(token, name, entry):
    """DEFAULT: PUT the live geometry onto the model's existing uid — same URL, attrs preserved."""
    uid = (entry.get("uid") or "").strip()
    if not uid:
        sys.exit(f"error: '{name}' has no uid in dependencies.yml — use --new to create it first.")
    guard_live_is_saved_model(name)
    dae = export_live_dae(name)
    print(f"PUT -> replacing geometry in place on uid {uid} (same URL; settings/materials/name kept) ...")
    code = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-X", "PUT",
         "-H", f"Authorization: Token {token}",
         "-F", f"modelFile=@{dae}", "-F", "isPublished=true", f"{API}/{uid}"],
        capture_output=True, text=True).stdout.strip()
    if code not in ("200", "201", "202", "204"):
        sys.exit(f"  PUT failed (HTTP {code}) — model unchanged.")
    print(f"  PUT HTTP {code}")
    ok = poll_processing(token, uid)
    os.remove(dae)                                    # the .dae is a transient export — don't leave it
    if not ok:
        sys.exit("  reprocess failed — check the model on Sketchfab.")
    print(f"  live (UNCHANGED url): https://sketchfab.com/models/{uid}")
    print("  -> uid + embeds + dependencies.yml unchanged; nothing to commit for this push.")


def push_new_model(token, name, entry):
    """LEGACY: POST a NEW model, rewrite the uid in embeds + dependencies.yml, delete the old.
    Resets Sketchfab viewer settings — use only to (re)create a model deliberately."""
    old_uid = (entry.get("uid") or "").strip()
    title = guard_live_is_saved_model(name)
    title = (title or name).strip()
    dae = export_live_dae(name)
    print(f"POST -> creating a NEW Sketchfab model '{title}' (new uid; RESETS viewer settings) ...")
    resp = subprocess.run(
        ["curl", "-s", "-X", "POST", "-H", f"Authorization: Token {token}",
         "-F", f"modelFile=@{dae}", "-F", f"name={title}",
         "-F", "isPublished=true", API], capture_output=True, text=True).stdout
    try:
        new_uid = json.loads(resp).get("uid", "")
    except Exception:
        new_uid = ""
    if not new_uid:
        sys.exit(f"  upload failed: {resp[:300]}")
    print(f"  new model uid: {new_uid}")
    poll_processing(token, new_uid)

    for rel in entry.get("embed_files", []):
        p = os.path.join(ROOT, rel)
        if old_uid and os.path.exists(p):
            txt = open(p).read()
            if old_uid in txt:
                open(p, "w").write(txt.replace(old_uid, new_uid))
                print(f"  updated embed: {rel}")
    dt = open(deps.YAML_PATH, encoding="utf-8").read()
    if old_uid and old_uid in dt:
        open(deps.YAML_PATH, "w", encoding="utf-8").write(dt.replace(old_uid, new_uid, 1))
        print(f"  dependencies.yml updated: {name} uid -> {new_uid}")
    else:
        print(f"  WARNING: old uid not found in dependencies.yml — set {name} uid to {new_uid} by hand")
    if old_uid and old_uid != new_uid:
        code = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-X", "DELETE",
             "-H", f"Authorization: Token {token}", f"{API}/{old_uid}"],
            capture_output=True, text=True).stdout.strip()
        print(f"  deleted old model {old_uid} (HTTP {code})")
    print(f"  live: https://sketchfab.com/models/{new_uid}")
    print("  -> commit the embed + dependencies.yml changes and run `bash publish.sh`.")


def main():
    load_env_private()
    token = os.environ.get("SKETCHFAB_API_TOKEN", "").strip()
    if not token:
        sys.exit("error: SKETCHFAB_API_TOKEN not set (add it to .env.private)")
    pos = [a for a in sys.argv[1:] if not a.startswith("-")]
    name = (pos[0] if pos else "overview").strip()
    new = "--new" in sys.argv

    models = {n: e for n, e in deps.ENTRIES.items() if e.get("kind") == "model"}
    if name not in models:
        sys.exit(f"error: '{name}' not in dependencies.yml models (known: {', '.join(models) or 'none'})")
    entry = models[name]
    (push_new_model if new else push_in_place)(token, name, entry)


if __name__ == "__main__":
    main()
