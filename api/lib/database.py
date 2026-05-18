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


def get_appointments():
    client = _get_client()
    result = client.table("appointments").select("*").order("created_at", desc=True).execute()
    return result.data


def get_inquiries():
    client = _get_client()
    result = client.table("inquiries").select("*").order("created_at", desc=True).execute()
    return result.data


def insert_chat_log(session_id, role, content):
    client = _get_client()
    client.table("chat_logs").insert({
        "session_id": session_id,
        "role": role,
        "content": content[:500],
    }).execute()


def get_analytics():
    client = _get_client()
    appointments = client.table("appointments").select("service, created_at").execute().data
    inquiries = client.table("inquiries").select("created_at").execute().data
    chat_logs = client.table("chat_logs").select("session_id, created_at").execute().data

    total_messages = len(chat_logs)
    unique_sessions = len({log["session_id"] for log in chat_logs}) if chat_logs else 0

    service_counts = {}
    for appt in appointments:
        s = appt["service"]
        service_counts[s] = service_counts.get(s, 0) + 1

    dates = [appt["created_at"][:10] for appt in appointments] + [inq["created_at"][:10] for inq in inquiries]
    date_counts = {}
    for d in dates:
        date_counts[d] = date_counts.get(d, 0) + 1

    return {
        "total_appointments": len(appointments),
        "total_inquiries": len(inquiries),
        "total_messages": total_messages,
        "unique_sessions": unique_sessions,
        "services": sorted(service_counts.items(), key=lambda x: -x[1]),
        "daily_activity": sorted(date_counts.items(), reverse=True)[:7],
    }
