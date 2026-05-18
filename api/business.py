import json
from http.server import BaseHTTPRequestHandler
from lib.data import BUSINESS, SERVICES, FAQ


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({
            "business": BUSINESS,
            "services": SERVICES,
            "faq": FAQ,
        }).encode("utf-8"))
