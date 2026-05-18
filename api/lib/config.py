import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

_missing = [k for k in ("GROQ_API_KEY", "SUPABASE_URL", "SUPABASE_KEY") if not os.environ.get(k)]
if _missing:
    raise RuntimeError(f"Missing required environment variables: {', '.join(_missing)}")
