from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)

    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)

    sender = Column(String(20))  # user / bot
    message = Column(String(1000))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
