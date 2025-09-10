from sqlalchemy import Column, BigInteger, String, DateTime, LargeBinary, JSON, ForeignKey
from datetime import datetime
from app.config.db import Base

# -----------------------------
# Equipment Image Model
# Stores uploaded equipment images and their embeddings
# -----------------------------
class EquipmentImage(Base):
    __tablename__ = "equipment_embeddings"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    vector = Column(LargeBinary, nullable=False)
    extra_metadata = Column("metadata", JSON)

    chat_session_id = Column(BigInteger, ForeignKey("chat_sessions.id"))