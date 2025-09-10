# app/models/chat_model.py
from sqlalchemy import Column, BigInteger, JSON, DateTime
from datetime import datetime
from app.config.db import Base

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    context = Column(JSON)  # List of messages [{"role": "user/assistant", "content": "..."}]