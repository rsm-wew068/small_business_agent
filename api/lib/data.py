BUSINESS = {
    "name": "Eric's Auto Care",
    "tagline": "Your Trusted Neighborhood Auto Shop",
    "phone": "(555) 842-3678",
    "email": "service@ericsautocare.com",
    "address": "789 Industrial Blvd, Springfield, IL 62704",
    "hours": {
        "monday": "7:30 AM – 6:00 PM",
        "tuesday": "7:30 AM – 6:00 PM",
        "wednesday": "7:30 AM – 6:00 PM",
        "thursday": "7:30 AM – 6:00 PM",
        "friday": "7:30 AM – 5:00 PM",
        "saturday": "8:00 AM – 2:00 PM",
        "sunday": "Closed",
    },
    "about": "Eric's Auto Care is a family-owned auto repair shop serving Springfield since 2005. ASE-certified mechanics, honest pricing, and fast turnaround. We handle everything from oil changes to engine rebuilds.",
}

SERVICES = [
    {
        "name": "Oil Change",
        "description": "Full synthetic or conventional oil change with new filter. Includes 21-point inspection.",
        "price": "$50 – $80",
        "duration": "30 min",
        "tags": ["popular", "maintenance"],
    },
    {
        "name": "Brake Pad Replacement",
        "description": "Brake pad and rotor inspection, replacement if needed. Front or rear axle.",
        "price": "$200 – $400",
        "duration": "1–2 hours",
        "tags": ["popular", "safety"],
    },
    {
        "name": "Tire Rotation",
        "description": "Rotate all four tires. Extends tire life and improves handling.",
        "price": "$30",
        "duration": "20 min",
        "tags": ["maintenance"],
    },
    {
        "name": "State Inspection",
        "description": "Licensed state inspection station. Quick and thorough.",
        "price": "$50",
        "duration": "30 min",
        "tags": ["required"],
    },
    {
        "name": "Diagnostic Scan",
        "description": "OBD-II scan and full diagnostic report. Find out what's causing that check engine light.",
        "price": "$100",
        "duration": "30 min",
        "tags": ["diagnostic"],
    },
    {
        "name": "Fleet Maintenance",
        "description": "Custom maintenance plans for business fleets of any size. Discounted rates available.",
        "price": "Custom quote",
        "duration": "Varies",
        "tags": ["fleet", "business"],
    },
]

FAQ = [
    {"q": "Do I need an appointment?", "a": "Appointments are recommended but not required. Walk-ins are welcome, but wait times may be longer. You can book through our assistant here!"},
    {"q": "What brands do you service?", "a": "We service all makes and models — domestic and imported. Toyota, Honda, Ford, Chevy, BMW, you name it."},
    {"q": "Do you offer a warranty on repairs?", "a": "Yes! All repairs come with a 12-month / 12,000-mile warranty, whichever comes first."},
    {"q": "Can I wait while my car is being serviced?", "a": "Absolutely. We have a comfortable waiting area with free Wi-Fi, coffee, and TV. For longer jobs, we can arrange a shuttle."},
    {"q": "Do you provide loaner cars?", "a": "We have a limited number of loaner vehicles for jobs over 4 hours. Ask when you book — first come, first served."},
    {"q": "What payment methods do you accept?", "a": "We accept cash, all major credit cards, and offer financing through Affirm for repairs over $500."},
    {"q": "How quickly can you get me in?", "a": "For routine maintenance, usually within 1–2 business days. For urgent issues, call us and we'll do our best to fit you in same-day."},
    {"q": "Can I bring my own parts?", "a": "We prefer to use our own parts for warranty coverage, but we're happy to discuss it. Note that our warranty won't cover customer-supplied parts."},
    {"q": "Do you offer fleet services?", "a": "Yes! We offer discounted rates for fleet vehicles. Submit an inquiry through our chat and we'll put together a custom plan for your business."},
    {"q": "Are your mechanics certified?", "a": "Yes, all our mechanics are ASE-certified with an average of 15 years of experience."},
]


def build_system_prompt():
    from datetime import date
    today = date.today().isoformat()

    services_text = "\n".join(
        f"- {s['name']}: {s['description']} ({s['price']}, ~{s['duration']}) [{', '.join(s['tags'])}]"
        for s in SERVICES
    )
    faq_text = "\n".join(f"Q: {f['q']}\nA: {f['a']}" for f in FAQ)
    hours_text = "\n".join(f"{day.title()}: {time}" for day, time in BUSINESS["hours"].items())

    return f"""You are the friendly AI assistant for {BUSINESS['name']}, a local auto repair shop.

## Your Role
Help customers with service questions, appointment booking, and general inquiries. Be warm, professional, and helpful — like a knowledgeable service advisor.

## Business Info
- Name: {BUSINESS['name']}
- Tagline: {BUSINESS['tagline']}
- Address: {BUSINESS['address']}
- Phone: {BUSINESS['phone']}
- Email: {BUSINESS['email']}
- About: {BUSINESS['about']}

## Hours
{hours_text}

## Services
{services_text}

## FAQ
{faq_text}

## Important Rules
- When booking appointments, always convert dates to YYYY-MM-DD and times to HH:MM (24-hour format). Today's date is {today}.
- If a customer wants to book an appointment, collect their name, preferred date, time, service needed, and phone number. Call the book_appointment tool IMMEDIATELY as soon as you have all five pieces of information. Do NOT ask for confirmation or repeat the details back — just call the tool.
- If a customer has an inquiry that needs a follow-up (like fleet services, custom quotes, feedback), collect their name, message, and contact info. Call the submit_inquiry tool IMMEDIATELY once you have all three pieces of information. Do NOT ask for confirmation.
- If you're missing required information for a tool, ask the customer for it — do NOT make up values.
- Be conversational and natural. Don't sound robotic.
- Keep responses concise — a few sentences is usually enough.
"""
