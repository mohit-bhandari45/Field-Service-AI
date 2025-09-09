from sqlalchemy import Column, BigInteger, String, DateTime, LargeBinary, JSON, Text
from datetime import datetime
from app.config.db import Base

# -----------------------------
# Manual Chunk Model
# Stores PDF/text manual chunks and their embeddings for RAG
# -----------------------------
class ManualChunk(Base):
    __tablename__ = "manual_chunks"

    id = Column(BigInteger, primary_key=True, autoincrement=True)  # Unique ID
    manual_name = Column(String(255), nullable=False)              # Manual or PDF file name
    chunk_text = Column(Text, nullable=False)                      # ✅ Use Text for long content
    vector = Column(LargeBinary, nullable=False)                   # Embedding of the chunk for similarity search
    extra_metadata = Column("metadata", JSON)                      # Metadata: page number, section, version
    created_at = Column(DateTime, default=datetime.utcnow)         # Timestamp when added to DB