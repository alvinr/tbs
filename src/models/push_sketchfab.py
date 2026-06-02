#!/usr/bin/env python3
"""Push a logical TBS-001 model to Sketchfab and keep its embed in sync.

Sketchfab's Data API cannot replace an existing model's geometry (PATCH is
metadata-only) and rejects .skp. So each push: exports the live SketchUp model
to Collada (.dae), POSTs a NEW Sketchfab model, rewrites the model UID in the
embed file(s), records the new UID in the registry, and deletes the old model.
The Sketchfab URL changes each time, but the docs embed is updated automatically
so site visitors always see the latest after a deploy.

Registry — models/sketchfab.json — maps each logical model to its current state:
    { "overview": { "name": "...", "uid": "...", "embed_files": ["..."] }, ... }

Credentials come from the environment or the gitignored .env.private:
    SKETCHFAB_API_TOKEN

Usage:
    python3 src/models/push_sketchfab.py [logical_name]      # default: overview
"""
import json
import os
import subprocess
import sys
import time
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REGISTRY = os.path.join(ROOT, "models", "sketchfab.json")
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


def main():
    load_env_private()
    token = os.environ.get("SKETCHFAB_API_TOKEN", "").strip()
    if not token:
        sys.exit("error: SKETCHFAB_API_TOKEN not set (add it to .env.private)")
    name = (sys.argv[1] if len(sys.argv) > 1 else "overview").strip()

    with open(REGISTRY) as f:
        registry = json.load(f)
    if name not in registry:
        sys.exit(f"error: '{name}' not in models/sketchfab.json "
                 f"(known: {', '.join(registry) or 'none'})")
    entry = registry[name]
    old_uid = (entry.get("uid") or "").strip()

    # 1. Export the live SketchUp model to Collada (.dae) — the API rejects .skp.
    dae = os.path.join(ROOT, "models", f"{name}.dae")
    print(f"Exporting live SketchUp model -> models/{name}.dae ...")
    sys.path.insert(0, os.path.dirname(__file__))
    from sketchup_client import send_ruby, SketchupError
    try:
        send_ruby('m=Sketchup.active_model; "exported=#{m.export(' + repr(dae) + ', false)}"')
    except SketchupError as e:
        sys.exit(f"error: could not export from SketchUp ({e}) - is SketchUp open?")
    if not os.path.exists(dae):
        sys.exit(f"error: export did not produce {dae}")

    # 2. POST a NEW Sketchfab model.
    print(f"Uploading new Sketchfab model '{entry['name']}' ...")
    resp = subprocess.run(
        ["curl", "-s", "-X", "POST", "-H", f"Authorization: Token {token}",
         "-F", f"modelFile=@{dae}", "-F", f"name={entry['name']}",
         "-F", "isPublished=true", API],
        capture_output=True, text=True).stdout
    try:
        new_uid = json.loads(resp).get("uid", "")
    except Exception:
        new_uid = ""
    if not new_uid:
        sys.exit(f"  upload failed: {resp[:300]}")
    print(f"  new model uid: {new_uid}")

    # 3. Wait for Sketchfab to finish processing the new geometry.
    print("  processing", end="", flush=True)
    ok = False
    for _ in range(72):
        time.sleep(5)
        print(".", end="", flush=True)
        try:
            st = str((api_get(token, new_uid).get("status") or {}).get("processing", "")).upper()
        except Exception:
            st = "?"
        if st == "SUCCEEDED":
            ok = True
            print(" done.")
            break
        if st == "FAILED":
            sys.exit("\n  processing FAILED on Sketchfab - old model left in place.")
    if not ok:
        print("\n  warning: still processing (continuing anyway).")

    # 4. Rewrite the old UID -> new UID in every embed file (iframe + attribution).
    for rel in entry.get("embed_files", []):
        p = os.path.join(ROOT, rel)
        if old_uid and os.path.exists(p):
            with open(p) as f:
                txt = f.read()
            if old_uid in txt:
                with open(p, "w") as f:
                    f.write(txt.replace(old_uid, new_uid))
                print(f"  updated embed: {rel}")

    # 5. Record the new UID in the registry, then delete the old model.
    entry["uid"] = new_uid
    with open(REGISTRY, "w") as f:
        json.dump(registry, f, indent=2)
        f.write("\n")
    print(f"  registry updated: {name} -> {new_uid}")
    if old_uid and old_uid != new_uid:
        code = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-X", "DELETE",
             "-H", f"Authorization: Token {token}", f"{API}/{old_uid}"],
            capture_output=True, text=True).stdout.strip()
        print(f"  deleted old model {old_uid} (HTTP {code})")

    print(f"  live: https://sketchfab.com/models/{new_uid}")
    print("  -> commit the embed/registry changes and run `bash publish.sh` to publish.")


if __name__ == "__main__":
    main()
