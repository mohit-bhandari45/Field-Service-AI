from sqlalchemy import Column, BigInteger, String, DateTime, JSON, ForeignKey
from datetime import datetime
from app.config.db import Base
from .vector_type import Vector

# -----------------------------
# Equipment Image Model
# -----------------------------
class EquipmentImage(Base):
    __tablename__ = "equipment_embeddings"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    # ✅ Store embedding as TiDB native VECTOR(512)
    vector = Column(Vector(512), nullable=False)  # not 768

    extra_metadata = Column("metadata", JSON)
    chat_session_id = Column(BigInteger, ForeignKey("chat_sessions.id"))