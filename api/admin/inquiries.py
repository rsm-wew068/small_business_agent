from dotenv import load_dotenv

load_dotenv()

from lib.database import get_inquiries


def handler(request):
    if request.method == "OPTIONS":
        return {
            "status_code": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            },
            "body": "",
        }

    data = get_inquiries()
    return {
        "status_code": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        "body": {"inquiries": data},
    }
