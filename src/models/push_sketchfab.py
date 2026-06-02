#!/usr/bin/env python3
"""Push models/overview.skp to Sketchfab, updating the existing model IN PLACE.

A PATCH to the model's UID re-uploads the geometry while keeping the same model
URL and embed, so the docs-site embed stays valid — no re-embedding needed.

Credentials are read from the environment, falling back to the gitignored
`.env.private` at the repo root (never committed):
    SKETCHFAB_API_TOKEN   — Sketchfab API token (Settings -> Password & API)
    SKETCHFAB_MODEL_UID   — UID of the model to update

Usage:
    python3 src/models/push_sketchfab.py [--wait]

    --wait  poll until Sketchfab finishes (re)processing the model.
"""
import json
import os
import subprocess
import sys
import time
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SKP = os.path.join(ROOT, "models", "overview.skp")
API = "https://api.sketchfab.com/v3/models"


def load_env_private():
    """Populate env vars from .env.private (KEY=VALUE lines) if not already set."""
    path = os.path.join(ROOT, ".env.private")
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())


def poll_status(token, uid):
    req = urllib.request.Request(f"{API}/{uid}",
                                 headers={"Authorization": f"Token {token}"})
    print("  waiting for processing", end="", flush=True)
    for _ in range(60):
        time.sleep(5)
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                data = json.load(r)
            status = str((data.get("status") or {}).get("processing", "")).upper()
        except Exception:
            status = "?"
        print(".", end="", flush=True)
        if status == "SUCCEEDED":
            print("\n  done — model is live.")
            return
        if status == "FAILED":
            print("\n  processing FAILED on Sketchfab — check the model page.")
            return
    print("\n  still processing (polling timed out); check the model page.")


def main():
    load_env_private()
    token = os.environ.get("SKETCHFAB_API_TOKEN", "").strip()
    uid = os.environ.get("SKETCHFAB_MODEL_UID", "").strip()
    if not token:
        sys.exit("error: SKETCHFAB_API_TOKEN not set (add it to .env.private)")
    if not uid:
        sys.exit("error: SKETCHFAB_MODEL_UID not set (add it to .env.private)")
    if not os.path.exists(SKP):
        sys.exit(f"error: {SKP} not found — save the model first")

    print(f"Pushing {os.path.relpath(SKP, ROOT)} -> Sketchfab model {uid} ...")
    # curl handles the multipart upload robustly; capture only the HTTP code.
    code = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
         "-X", "PATCH",
         "-H", f"Authorization: Token {token}",
         "-F", f"modelFile=@{SKP}",
         f"{API}/{uid}"],
        capture_output=True, text=True).stdout.strip()

    if code == "204":
        print("  upload accepted (HTTP 204) - Sketchfab is re-processing the model.")
    else:
        hint = {"401": "invalid/expired token", "403": "token lacks permission",
                "402": "plan does not allow API upload", "404": "model UID not found"}
        sys.exit(f"  upload failed (HTTP {code} - {hint.get(code, 'see Sketchfab API docs')}).")

    if "--wait" in sys.argv:
        poll_status(token, uid)
    else:
        print("  (pass --wait to block until processing completes.)")


if __name__ == "__main__":
    main()
