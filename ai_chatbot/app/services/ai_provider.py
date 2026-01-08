import json
import os
from google import genai
from google.genai import types

# Lazy initialization of Gemini client
_client = None


def get_client():
    """Get or create the Gemini client with API key from environment."""
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is not set. "
                "Please set it using: setx GEMINI_API_KEY \"your-api-key\" "
                "(Note: You may need to restart your terminal/IDE after using setx)"
            )
        _client = genai.Client(api_key=api_key)
    return _client


def _call_gemini(system_prompt: str, user_prompt: str) -> str:
    """
    Low-level Gemini call.
    Returns raw text.
    """

    client = get_client()
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=[
            {"role": "user", "parts": [
                {"text": system_prompt + "\n\n" + user_prompt}
            ]}
        ],
        config=types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=512
        )
    )

    return response.text.strip()


def ask_ai_json(system_prompt: str, user_prompt: str) -> dict:
    """
    Calls Gemini and guarantees JSON output.
    """

    try:
        raw_text = _call_gemini(system_prompt, user_prompt)

        # Extract JSON safely
        start = raw_text.find("{")
        end = raw_text.rfind("}") + 1

        json_text = raw_text[start:end]
        return json.loads(json_text)

    except Exception as e:
        print("AI JSON ERROR:", e)

        # Safe fallback
        return {
            "intent": "unclear",
            "sentiment": "neutral",
            "interest_level": "low",
            "urgency": "low",
            "entities": {}
        }


def ask_ai_text(system_prompt: str, user_prompt: str) -> str:
    """
    Calls Gemini for normal text response.
    """

    try:
        return _call_gemini(system_prompt, user_prompt)

    except Exception as e:
        print("AI TEXT ERROR:", e)
        return "Sorry, I’m having trouble responding right now."
