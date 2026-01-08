from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=True)
    email = Column(String(150), nullable=True)
    company = Column(String(150), nullable=True)

    intent_level = Column(String(20), default="low")
    sentiment = Column(String(20), default="neutral")

    score = Column(Integer, default=0)
    status = Column(String(50), default="new")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    summary = Column(Text, nullable=True)
    team_size = Column(Integer, nullable=True)
    budget = Column(String, nullable=True)
    timeline = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    use_case = Column(Text, nullable=True)

    buying_signal = Column(Boolean, default=False)
    objection_type = Column(String, nullable=True)