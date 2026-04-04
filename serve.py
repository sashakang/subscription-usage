#!/usr/bin/env python3
"""Minimal server for Claude Usage Dashboard.
Serves index.html and /data endpoint (JSONL from usage log)."""

import http.server
import os
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8766
DATA_FILE = os.path.expanduser("~/.openclaw/workspace/usage-logs/claude-usage.jsonl")
HTML_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/data":
            try:
                with open(DATA_FILE, "r") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/x-ndjson")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(content.encode())
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'{"error":"no data file"}')
        elif self.path in ("/", "/index.html"):
            with open(HTML_FILE, "r") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(content.encode())
        else:
            super().do_GET()

    def log_message(self, format, *args):
        pass  # quiet

if __name__ == "__main__":
    server = http.server.HTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Dashboard: http://localhost:{PORT}")
    server.serve_forever()
