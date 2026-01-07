from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.lead import Lead
from app.models.chat_message import ChatMessage
from app.schemas.chat import (
    StartChatResponse,
    ChatMessageRequest,
    ChatMessageResponse
)
from app.services.ai_service import AIService
from app.services.scoring_service import ScoringService

router = APIRouter(prefix="/chat", tags=["Chat"])

ai_service = AIService()
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

    # 1️⃣ Save user message
    user_msg = ChatMessage(
        lead_id=lead.id,
        sender="user",
        message=payload.message
    )
    db.add(user_msg)

    # 2️⃣ AI analysis
    ai_result = ai_service.analyze_message(payload.message)
    print("RAW AI RESULT:", ai_result)


    # 3️⃣ Scoring
    score = scoring_service.calculate_score(
        ai_result["intent"],
        ai_result["interest_level"]
    )
    status = scoring_service.determine_status(score)

    # 4️⃣ Update lead
    lead.intent_level = ai_result["interest_level"]
    lead.sentiment = ai_result["sentiment"]
    lead.score += score
    lead.status = status

    # 5️⃣ Save bot reply
    bot_msg = ChatMessage(
        lead_id=lead.id,
        sender="bot",
        message=ai_result["suggested_reply"]
    )
    db.add(bot_msg)

    db.commit()

    # Print the updated values
    print(f"\n{'='*50}")
    print(f"User Message: {payload.message}")
    print(f"New Score: {lead.score}")
    print(f"Sentiment: {lead.sentiment}")
    print(f"Status: {lead.status}")
    print(f"Intent Level: {lead.intent_level}")
    print(f"{'='*50}\n")

    # 6️⃣ Respond
    return {
        "reply": ai_result["suggested_reply"],
        "intent": ai_result["intent"],
        "sentiment": ai_result["sentiment"],
        "score": lead.score,
        "status": lead.status
    }
