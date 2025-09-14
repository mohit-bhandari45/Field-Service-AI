from sqlalchemy import Column, BigInteger, String, DateTime, JSON, Text
from datetime import datetime
from app.config.db import Base
from .vector_type import Vector

class ManualEmbedding(Base):
    __tablename__ = "manual_embeddings"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)  # e.g., "Motor Repair Manual"
    section = Column(String(255), nullable=True)  # e.g., "Section 1"
    content = Column(Text, nullable=False)  # manual chunk text
    vector = Column(Vector(384), nullable=False)  # OpenAI text-embedding-3-large
    extra_metadata = Column("metadata", JSON)
    created_at = Column(DateTime, default=datetime.utcnow)