from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.lead import Lead
from app.models.chat_message import ChatMessage
from app.schemas.chat import (
    StartChatResponse,
    ChatMessageRequest,
    ChatMessageResponse
)

from app.services.ai_understanding import understand_message
from app.services.ai_decision import decide_next_action
from app.services.ai_response import generate_reply
from app.services.ai_memory import update_summary
from app.services.scoring_service import ScoringService


router = APIRouter(prefix="/chat", tags=["Chat"])

scoring_service = ScoringService()


@router.post("/start", response_model=StartChatResponse)
def start_chat(db: Session = Depends(get_db)):

    lead = Lead()
    db.add(lead)
    db.commit()
    db.refresh(lead)

    return {"lead_id": lead.id}


@router.post("/message", response_model=ChatMessageResponse)
def send_message(payload: ChatMessageRequest, db: Session = Depends(get_db)):

    lead = db.query(Lead).filter(Lead.id == payload.lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Invalid lead_id")

    # 1️⃣ Save USER message
    user_msg = ChatMessage(
        lead_id=lead.id,
        sender="user",
        message=payload.message
    )
    db.add(user_msg)

    # 2️⃣ UNDERSTAND the message
    understanding = understand_message(payload.message)
    print("UNDERSTANDING:", understanding)

    entities = understanding.get("entities", {})

    lead.team_size = entities.get("team_size") or lead.team_size
    lead.budget = entities.get("budget") or lead.budget
    lead.timeline = entities.get("timeline") or lead.timeline
    lead.industry = entities.get("industry") or lead.industry
    lead.use_case = entities.get("use_case") or lead.use_case

    lead.buying_signal = understanding.get("buying_signals", False)
    lead.objection_type = understanding.get("objection_type")

    # 3️⃣ DECIDE next action
    decision = decide_next_action(
        understanding=understanding,
        lead_score=lead.score
    )
    print("DECISION:", decision)

    # 4️⃣ SCORING
    score_delta = scoring_service.calculate_score(
        understanding["intent"],
        understanding["interest_level"]
    )

    lead.score += score_delta
    lead.status = scoring_service.determine_status(lead.score)
    lead.intent_level = understanding["interest_level"]
    lead.sentiment = understanding["sentiment"]

    # 5️⃣ GENERATE BOT reply (USES MEMORY)
    bot_reply = generate_reply(
        user_message=payload.message,
        understanding=understanding,
        decision=decision,
        conversation_summary=lead.summary or ""
    )

    # 6️⃣ Save BOT message
    bot_msg = ChatMessage(
        lead_id=lead.id,
        sender="bot",
        message=bot_reply
    )
    db.add(bot_msg)

    # 7️⃣ UPDATE CONVERSATION MEMORY (⭐ STEP 2 CORE)
    lead.summary = update_summary(
        existing_summary=lead.summary,
        user_message=payload.message,
        bot_reply=bot_reply
    )

    # 8️⃣ COMMIT EVERYTHING TO DB
    db.commit()

    # 🔍 DEBUG LOG
    print("\n" + "=" * 60)
    print("USER:", payload.message)
    print("INTENT:", understanding["intent"])
    print("INTEREST:", understanding["interest_level"])
    print("ACTION:", decision["action"])
    print("SCORE:", lead.score)
    print("STATUS:", lead.status)
    print("SUMMARY:", lead.summary)
    print("=" * 60 + "\n")

    # 9️⃣ RESPOND TO FRONTEND
    return {
        "reply": bot_reply,
        "intent": understanding["intent"],
        "sentiment": understanding["sentiment"],
        "score": lead.score,
        "status": lead.status
    }
