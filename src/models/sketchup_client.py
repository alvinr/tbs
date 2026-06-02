#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# © 2026 Alvin Richards
"""
sketchup_client.py — Send Ruby code straight to the SketchUp MCP plugin.

The sketchup-mcp Python package is only a relay: it forwards newline-framed
JSON-RPC `tools/call` requests to the Ruby extension listening on
127.0.0.1:9876 and reads back a single JSON line. This module speaks that
protocol directly, so models can be pushed into SketchUp without depending on
the MCP bridge being wired into the current Claude Code session.

Usage
-----
    python3 src/models/sketchup_client.py path/to/model.rb   # send a file
    cat model.rb | python3 src/models/sketchup_client.py      # send stdin
    python3 src/models/sketchup_client.py -c '1 + 1'          # inline ping

The Ruby script's return value (its last expression) is printed.

Importable:
    from sketchup_client import send_ruby
    print(send_ruby('Sketchup.active_model.entities.length'))
"""

import sys
import json
import socket
import argparse

HOST = "127.0.0.1"
PORT = 9876


class SketchupError(RuntimeError):
    """Raised when the plugin reports an error or cannot be reached."""


def send_ruby(code, host=HOST, port=PORT, timeout=30.0):
    """Evaluate Ruby in the running SketchUp and return its result string.

    Sends one JSON-RPC `tools/call` (name=eval_ruby) and reads the single
    newline-framed JSON response the plugin writes back. Returns the text of
    the Ruby script's return value. Raises SketchupError on a refused
    connection, a timeout, or a plugin-reported error.
    """
    request = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {"name": "eval_ruby", "arguments": {"code": code}},
        "id": 1,
    }

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
    except (ConnectionRefusedError, OSError) as e:
        raise SketchupError(
            f"Could not connect to SketchUp at {host}:{port} ({e}). "
            "Is SketchUp running with the MCP extension loaded?"
        ) from e

    try:
        sock.sendall(json.dumps(request).encode("utf-8") + b"\n")

        # The plugin replies with exactly one JSON object terminated by '\n'.
        # Accumulate until the buffer parses as JSON (handles chunked recv).
        buf = b""
        while True:
            try:
                chunk = sock.recv(8192)
            except socket.timeout as e:
                raise SketchupError(
                    "Timed out waiting for SketchUp. A stale connection can "
                    "wedge the plugin's read loop — try: pkill -f sketchup_mcp"
                ) from e
            if not chunk:
                break
            buf += chunk
            try:
                response = json.loads(buf.decode("utf-8"))
                break
            except json.JSONDecodeError:
                continue
        else:
            response = None
    finally:
        sock.close()

    if not buf:
        raise SketchupError("SketchUp closed the connection with no response.")
    if response is None:
        response = json.loads(buf.decode("utf-8"))

    if "error" in response:
        raise SketchupError(f"JSON-RPC error: {response['error']}")

    result = response.get("result", {})
    if result.get("isError"):
        text = _result_text(result)
        raise SketchupError(f"SketchUp eval error: {text}")

    return _result_text(result)


def _result_text(result):
    """Pull the text payload out of a tools/call result envelope."""
    content = result.get("content")
    if isinstance(content, list) and content:
        return content[0].get("text", "")
    return str(result)


def main():
    parser = argparse.ArgumentParser(
        description="Send Ruby to the running SketchUp via the MCP plugin socket.")
    parser.add_argument("file", nargs="?",
                        help="Ruby file to send (omit to read stdin)")
    parser.add_argument("-c", "--code", help="Inline Ruby string to send")
    parser.add_argument("--host", default=HOST)
    parser.add_argument("--port", type=int, default=PORT)
    args = parser.parse_args()

    if args.code is not None:
        code = args.code
    elif args.file:
        with open(args.file) as f:
            code = f.read()
    else:
        code = sys.stdin.read()

    if not code.strip():
        parser.error("no Ruby code provided")

    try:
        print(send_ruby(code, host=args.host, port=args.port))
    except SketchupError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
