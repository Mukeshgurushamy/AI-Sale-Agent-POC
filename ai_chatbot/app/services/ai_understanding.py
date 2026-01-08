from typing import Dict
from app.services.ai_provider import ask_ai_json


SYSTEM_PROMPT = """
You are an AI sales intelligence engine.

Your task:
- Deeply understand the user's message
- Extract structured business intelligence
- DO NOT reply to the user
- ONLY return valid JSON

Classify:

intent:
pricing, demo, support, objection, greeting, goodbye, casual, unclear

sentiment:
positive, neutral, negative

interest_level:
low, medium, high

urgency:
low, medium, high

Extract entities (if present):
- team_size (number)
- budget (number or range)
- timeline (e.g. immediate, 1 month, 3 months)
- industry
- use_case

Detect buying_signals:
- true or false

Detect objection_type (if intent = objection):
- price
- trust
- features
- timing
- none

Rules:
- If pricing, demo, or budget is mentioned → buying_signals = true
- If message is vague → interest_level = low
- If timeline is urgent → urgency = high

Return ONLY JSON.
"""


def understand_message(message: str) -> Dict:
    prompt = f"""
User message:
\"\"\"{message}\"\"\"

Return JSON only.
"""

    return ask_ai_json(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=prompt
    )
