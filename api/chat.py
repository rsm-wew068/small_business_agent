import json
import asyncio
from http.server import BaseHTTPRequestHandler
from dotenv import load_dotenv

load_dotenv()

from lib.agent import chat


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(content_length)) if content_length else {}
        messages = body.get("messages", [])

        try:
            response = asyncio.get_event_loop().run_until_complete(chat(messages))
        except RuntimeError:
            response = asyncio.run(chat(messages))

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"response": response}).encode("utf-8"))
