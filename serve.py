#!/usr/bin/env python3
"""Minimal server for Claude Usage Dashboard.
Serves index.html only — no directory listing, no file fallthrough."""

import http.server
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8766
HTML_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            try:
                with open(HTML_FILE, "r") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode())
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Dashboard not built yet. Run: claude-usage-build")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # quiet

if __name__ == "__main__":
    server = http.server.HTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Dashboard: http://localhost:{PORT}")
    server.serve_forever()
