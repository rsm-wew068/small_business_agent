# Eric's Auto Care — AI Assistant

> A smart, conversational AI assistant for a local auto repair shop. Answers service questions, books appointments, and handles customer inquiries.

**[Live Demo](https://small-business-agent.vercel.app/)** | **[Demo Video](#)** | **[GitHub](https://github.com/rsm-wew068/small_business_agent)**

![QR Code](qr.png)

Scan to try it on your phone.

---

## Tech Stack

- **Frontend:** React + Vite + Tailwind CSS — mobile-first chat interface
- **Backend:** Python serverless functions on Vercel — stateless, no session storage
- **AI:** Groq API (`llama-3.3-70b-versatile`) via OpenAI-compatible SDK with tool use
- **Database:** Supabase (PostgreSQL) — persistent storage for appointments and inquiries

## Architecture

```
User (browser/mobile)
  ↓ sends full message history
React Frontend (Vite + Tailwind)
  ↓ POST /api/chat { messages: [...] }
Vercel Serverless Function (Python)
  ↓ calls with system prompt + tools
Groq API (LLM)
  ↓ may call tools (book_appointment, submit_inquiry)
Supabase (PostgreSQL)
  ↳ appointments table
  ↳ inquiries table
```

- **Stateless backend:** The frontend sends the complete conversation history on each request. No server-side sessions.
- **Tool use:** The LLM decides when to call tools. It collects required info from the user over multiple turns, then fires the tool once it has everything.
- **Graceful validation:** If the LLM calls a tool with missing fields, the tool returns a human-readable follow-up string instead of crashing. The agent loop recovers and asks the user for the missing info.

## Setup Instructions

### Prerequisites
- Node.js 18+
- Python 3.11+
- A [Groq](https://console.groq.com) API key
- A [Supabase](https://supabase.com) project

### 1. Clone and install

```bash
git clone https://github.com/rsm-wew068/small_business_agent.git
cd small_business_agent
npm install
```

### 2. Set up Supabase

Create a new Supabase project, then run this SQL in the SQL Editor:

```sql
CREATE TABLE appointments (
  id BIGSERIAL PRIMARY KEY,
  customer_name TEXT NOT NULL,
  appointment_date DATE NOT NULL,
  appointment_time TIME NOT NULL,
  service TEXT NOT NULL,
  phone TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE inquiries (
  id BIGSERIAL PRIMARY KEY,
  customer_name TEXT NOT NULL,
  message TEXT NOT NULL,
  contact TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE chat_logs (
  id BIGSERIAL PRIMARY KEY,
  session_id TEXT NOT NULL,
  role TEXT NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

```env
# Groq API (LLM)
GROQ_API_KEY=gsk_xxx

# Supabase (database) — use the SERVICE ROLE key, NOT the anon key.
# This key stays server-side only and is never exposed to the frontend.
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJxxx
```

### 4. Run locally

```bash
npm run dev
```

For the backend, use Vercel CLI:

```bash
npx vercel dev
```

Or deploy directly to Vercel (recommended — avoids local dev quirks):

```bash
npx vercel --prod
```

### 5. Run tests

```bash
pip install pytest
pytest tests/
```

## What It Does

- **Answers questions** about services, pricing, hours, location, and policies (from hardcoded business data in the system prompt)
- **Books appointments** — collects customer name, date, time, service, and phone, then inserts into Supabase
- **Submits inquiries** — for fleet services, custom quotes, or anything needing a follow-up
- **Multi-language** — responds in whatever language the customer writes in
- **Analytics dashboard** — tracks messages, sessions, popular services, and daily activity
- **Mobile-friendly** — responsive Tailwind UI that works great on phones

## What I'd Improve With More Time

- **Streaming responses** for snappier UX (Groq is fast, but streaming feels better)
- **Server-side input validation** for dates, phone numbers, and field lengths before database writes
- **Admin authentication** to protect the dashboard and customer data
- **SMS/email confirmations** for booked appointments
- **More comprehensive tests** covering the agent loop, database operations, and chat handler
- **Voice support** via Web Speech API or Twilio
