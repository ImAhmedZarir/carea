#!/usr/bin/env python3
"""Minimal self-owned sample target server (`pulse-timer`) for carea walkthroughs."""

from __future__ import annotations

import argparse
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def clamp_status(duration_ms: int, elapsed_ms: int, state: str = "paused") -> dict[str, object]:
    if duration_ms < 1000 or duration_ms > 86400000:
        return {"error": "invalid_duration"}
    remaining = max(0, duration_ms - max(0, elapsed_ms))
    next_state = "completed" if remaining == 0 else state
    return {
        "state": next_state,
        "duration_ms": duration_ms,
        "remaining_ms": remaining,
        "warning_active": next_state == "running" and remaining <= 10000,
    }


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/" or self.path == "/index.html":
            body = (ROOT / "index.html").read_bytes()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == "/api/timer/status":
            payload = json.dumps(clamp_status(60000, 18000, state="paused")).encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        return


def main() -> int:
    parser = argparse.ArgumentParser(description="Run pulse-timer sample target")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=4173)
    args = parser.parse_args()
    srv = HTTPServer((args.host, args.port), Handler)
    print(f"pulse-timer listening on http://{args.host}:{args.port}/")
    srv.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
