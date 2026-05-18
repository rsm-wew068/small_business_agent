from .config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client


def insert_appointment(customer_name, appointment_date, appointment_time, service, phone):
    client = _get_client()
    result = client.table("appointments").insert({
        "customer_name": customer_name,
        "appointment_date": appointment_date,
        "appointment_time": appointment_time,
        "service": service,
        "phone": phone,
    }).execute()
    return result.data[0] if result.data else None


def insert_inquiry(customer_name, message, contact):
    client = _get_client()
    result = client.table("inquiries").insert({
        "customer_name": customer_name,
        "message": message,
        "contact": contact,
    }).execute()
    return result.data[0] if result.data else None
