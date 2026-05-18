import asyncio
from dotenv import load_dotenv

load_dotenv()

from lib.agent import chat


def handler(request):
    if request.method == "OPTIONS":
        return {
            "status_code": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            },
            "body": "",
        }

    body = request.json if hasattr(request, "json") else {}
    messages = body.get("messages", [])

    try:
        response = asyncio.get_event_loop().run_until_complete(chat(messages))
    except RuntimeError:
        response = asyncio.run(chat(messages))

    return {
        "status_code": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        "body": {"response": response},
    }
