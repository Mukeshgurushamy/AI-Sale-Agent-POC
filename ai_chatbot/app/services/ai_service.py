import json
import re
from typing import Dict
from google import genai
from app.core.config import GEMINI_API_KEY


SYSTEM_INSTRUCTION = """
You are a professional B2B sales assistant AI.

Your task is to classify a website visitor's message for SALES QUALIFICATION.

BUSINESS RULES:

INTENT:
- pricing → cost, plans, budget
- demo → demo, meeting, call
- feature → product capabilities
- objection → concerns or hesitation
- casual → greetings or browsing

INTEREST LEVEL:
- high → mentions company, team, department, or pricing for business use
- medium → asking about pricing/features without business context
- low → greetings, browsing, no buying signal

EXAMPLES:
User: "We are looking for pricing for our HR team"
intent: pricing
interest_level: high

User: "What is your pricing?"
intent: pricing
interest_level: medium

User: "Hi"
intent: casual
interest_level: low

Return ONLY valid JSON in this exact format:
{
  "intent": "",
  "sentiment": "",
  "interest_level": "",
  "suggested_reply": ""
}

Rules:
- Output ONLY JSON
- No markdown
- No explanations
- suggested_reply max 2 sentences
"""


class AIService:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def analyze_message(self, user_message: str) -> Dict:
        try:
            full_prompt = f"""
{SYSTEM_INSTRUCTION}

User message:
"{user_message}"
"""

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    {
                        "role": "user",
                        "parts": [{"text": full_prompt}]
                    }
                ],
                config={
                    "temperature": 0.1,
                    "max_output_tokens": 300,
                    "response_mime_type": "application/json"
                }
            )

            # ✅ CORRECT WAY TO READ GEMINI RESPONSE
            raw_text = response.candidates[0].content.parts[0].text
            print("RAW AI TEXT:", raw_text)

            return json.loads(raw_text)

        except Exception as e:
            print("AI ERROR:", e)
            return {
                "intent": "casual",
                "sentiment": "neutral",
                "interest_level": "low",
                "suggested_reply": "Could you please tell me more about what you’re looking for?"
            }