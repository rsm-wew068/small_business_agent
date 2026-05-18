from lib.data import BUSINESS, SERVICES, FAQ


def handler(request):
    return {
        "status_code": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json",
        },
        "body": {
            "business": BUSINESS,
            "services": SERVICES,
            "faq": FAQ,
        },
    }
