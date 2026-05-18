TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "book_appointment",
            "description": "Book a service appointment at the auto shop. Use when a customer wants to schedule a visit.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {"type": "string", "description": "Customer's full name"},
                    "date": {"type": "string", "description": "Appointment date in YYYY-MM-DD format"},
                    "time": {"type": "string", "description": "Appointment time in HH:MM 24-hour format"},
                    "service": {"type": "string", "description": "The service needed (e.g. 'oil change', 'brake pad replacement', 'diagnostic scan')"},
                    "phone": {"type": "string", "description": "Customer's phone number"},
                },
                "required": ["customer_name", "date", "time", "service", "phone"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "submit_inquiry",
            "description": "Submit a customer inquiry that needs a follow-up from the business (fleet services, custom quotes, feedback, etc.).",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {"type": "string", "description": "Customer's full name"},
                    "message": {"type": "string", "description": "The customer's inquiry or message"},
                    "contact": {"type": "string", "description": "Customer's phone number or email for follow-up"},
                },
                "required": ["customer_name", "message", "contact"],
            },
        },
    },
]


def dispatch_tool(name, args):
    if name == "book_appointment":
        return _book_appointment(args)
    elif name == "submit_inquiry":
        return _submit_inquiry(args)
    else:
        return f"Unknown tool: {name}"


def _book_appointment(args):
    name = args.get("customer_name", "").strip()
    date = args.get("date", "").strip()
    time = args.get("time", "").strip()
    service = args.get("service", "").strip()
    phone = args.get("phone", "").strip()

    if not name:
        return "I need your name to book the appointment. Could you provide that?"
    if not date:
        return "I need a date for the appointment. What date works for you?"
    if not time:
        return "What time works best? I need a specific time for the booking."
    if not service:
        return "What service do you need? For example, oil change, brake service, diagnostics, etc."
    if not phone:
        return "I need a phone number for the appointment. Could you provide that?"

    try:
        from .database import insert_appointment
        insert_appointment(name, date, time, service, phone)
        return f"Appointment confirmed! {name}, you're booked for {service} on {date} at {time}. We'll call {phone} if anything changes. See you then!"
    except Exception:
        return "I'm sorry, I couldn't complete the booking due to a technical issue. Please try calling us at (555) 842-3678."


def _submit_inquiry(args):
    name = args.get("customer_name", "").strip()
    message = args.get("message", "").strip()
    contact = args.get("contact", "").strip()

    if not name:
        return "I need your name to submit this inquiry. What's your name?"
    if not message:
        return "Could you tell me what your inquiry is about?"
    if not contact:
        return "I need a phone number or email to follow up with you. How can we reach you?"

    try:
        from .database import insert_inquiry
        insert_inquiry(name, message, contact)
        return f"Thanks, {name}! Your inquiry has been submitted. We'll get back to you at {contact} within 24 hours."
    except Exception:
        return "I'm sorry, I couldn't submit your inquiry due to a technical issue. Please email us at service@ericsautocare.com."
