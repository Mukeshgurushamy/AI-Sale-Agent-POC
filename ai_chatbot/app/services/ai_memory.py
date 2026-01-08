
from app.services.ai_provider import ask_ai_text

SYSTEM_PROMPT = """
You are an AI conversation memory engine.

Your task:
- Update the conversation summary
- Do NOT reply to the user
- Keep summary concise and factual
- Remove repetition
- Capture important details only

Focus on:
- User intent
- Requirements
- Objections
- Decisions made
"""

def update_summary(
    existing_summary: str,
    user_message: str,
    bot_reply: str
) -> str:

    prompt = f"""
Existing summary:
{existing_summary or "None"}

New exchange:
User: {user_message}
Bot: {bot_reply}

Update the summary.
"""

    return ask_ai_text(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=prompt
    )
