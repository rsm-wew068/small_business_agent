from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import asyncio

load_dotenv()

from api.lib.agent import chat
from api.lib.data import BUSINESS, SERVICES, FAQ

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/chat")
async def chat_endpoint(body: dict):
    messages = body.get("messages", [])
    response = await chat(messages)
    return {"response": response}


@app.get("/api/business")
async def business_endpoint():
    return {"business": BUSINESS, "services": SERVICES, "faq": FAQ}


@app.get("/api/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
