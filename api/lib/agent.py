import json
from openai import OpenAI
from .config import GROQ_API_KEY, GROQ_MODEL
from .data import build_system_prompt
from .tools import TOOL_DEFINITIONS, dispatch_tool

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)


def chat(messages):
    if not messages:
        return "Hi! Welcome to Eric's Auto Care. How can I help you today?"

    system_prompt = build_system_prompt()
    all_messages = [{"role": "system", "content": system_prompt}] + messages

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=all_messages,
        tools=TOOL_DEFINITIONS,
        tool_choice="auto",
    )

    assistant_msg = response.choices[0].message

    if not assistant_msg.tool_calls:
        return assistant_msg.content or "I'm not sure how to help with that. Could you rephrase?"

    all_messages.append(assistant_msg)

    for tool_call in assistant_msg.tool_calls:
        args = json.loads(tool_call.function.arguments) if isinstance(tool_call.function.arguments, str) else tool_call.function.arguments
        result = dispatch_tool(tool_call.function.name, args)
        all_messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result,
        })

    final_response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=all_messages,
        tools=TOOL_DEFINITIONS,
        tool_choice="none",
    )
    return final_response.choices[0].message.content or "Done! Is there anything else I can help with?"
