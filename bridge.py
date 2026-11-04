#!/usr/bin/env python3
"""NISTOR WoW V3 local-only diagnostic bridge. No account/password endpoints."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json, socket, time

ROOT = Path(__file__).resolve().parent
HOST, PORT = "127.0.0.1", 8765

def tcp_open(port):
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=1):
            return True
    except OSError:
        return False

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/api/status":
            data = {"name": "NISTOR WoW", "bridge": "online",
                    "authserver": tcp_open(3724),
                    "worldserver": tcp_open(8085),
                    "checked_at": int(time.time()),
                    "note": "TCP port checks only; WoW protocol/authentication not implemented"}
            raw = json.dumps(data).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
        elif path in ("/", "/index.html", "/v5-auth-probe.html"):
            try:
                raw = (ROOT / ("v5-auth-probe.html" if path == "/v5-auth-probe.html" else "index.html")).read_bytes()
            except FileNotFoundError:
                self.send_error(404, "index.html missing; download it next to bridge.py")
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
        else:
            self.send_error(404)
            return
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

if __name__ == "__main__":
    print(f"NISTOR WoW local bridge: http://{HOST}:{PORT}")
    print("Only localhost; does not expose server or accept passwords.")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
