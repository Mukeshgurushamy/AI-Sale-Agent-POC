from typing import Dict
from app.services.ai_provider import ask_ai_text


SYSTEM_PROMPT = """
You are an AI sales assistant.

Rules:
- Be professional
- Be concise
- Do not hallucinate
- Do not make promises
- Ask smart follow-up questions
"""


def generate_reply(
    user_message: str,
    understanding: Dict,
    decision: Dict,
    conversation_summary: str = ""
) -> str:

    prompt = f"""
Conversation summary:
{conversation_summary}

User message:
{user_message}

Detected intent: {understanding['intent']}
Interest level: {understanding['interest_level']}
Urgency: {understanding['urgency']}

Action: {decision['action']}
Tone: {decision['tone']}

Generate the best possible reply.
"""

    return ask_ai_text(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=prompt
    )
