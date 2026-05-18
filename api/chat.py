import sys
import os
import json
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

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
        session_id = body.get("session_id", "unknown")

        try:
            from lib.database import insert_chat_log
            last = messages[-1] if messages else None
            if last and last.get("role") == "user":
                insert_chat_log(session_id, "user", last["content"])
        except Exception:
            pass

        response = chat(messages)

        try:
            from lib.database import insert_chat_log
            insert_chat_log(session_id, "assistant", response)
        except Exception:
            pass

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"response": response}).encode("utf-8"))
