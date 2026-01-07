from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.lead import Lead
from app.models.chat_message import ChatMessage

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/leads")
def get_all_leads(db: Session = Depends(get_db)):
    leads = db.query(Lead).order_by(Lead.created_at.desc()).all()

    return [
        {
            "id": lead.id,
            "name": lead.name,
            "email": lead.email,
            "intent_level": lead.intent_level,
            "sentiment": lead.sentiment,
            "score": lead.score,
            "status": lead.status,
            "created_at": lead.created_at
        }
        for lead in leads
    ]

@router.get("/leads/{lead_id}/chats")
def get_lead_chats(lead_id: int, db: Session = Depends(get_db)):
    chats = (
        db.query(ChatMessage)
        .filter(ChatMessage.lead_id == lead_id)
        .order_by(ChatMessage.created_at)
        .all()
    )

    return [
        {
            "sender": chat.sender,
            "message": chat.message,
            "created_at": chat.created_at
        }
        for chat in chats
    ]