from typing import Dict


def decide_next_action(understanding: Dict, lead_score: int) -> Dict:
    intent = understanding["intent"]
    interest = understanding["interest_level"]
    urgency = understanding["urgency"]

    action = "continue_conversation"
    tone = "neutral"

    if intent == "pricing" and interest in ["medium", "high"]:
        tone = "sales"
        action = "qualify_and_offer_pricing"

    elif intent == "demo":
        tone = "sales"
        action = "schedule_demo"

    elif intent == "support":
        tone = "helpful"
        action = "support_response"

    elif intent == "goodbye":
        tone = "polite"
        action = "close_conversation"

    elif intent == "unclear":
        tone = "clarify"
        action = "ask_clarifying_question"

    return {
        "action": action,
        "tone": tone
    }
