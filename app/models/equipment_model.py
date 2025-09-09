from sqlalchemy import Column, BigInteger, String, DateTime, LargeBinary, JSON
from datetime import datetime
from app.config.db import Base

# -----------------------------
# Equipment Image Model
# Stores uploaded equipment images and their embeddings
# -----------------------------
class EquipmentImage(Base):
    __tablename__ = "equipment_embeddings"  # Table name in DB

    id = Column(BigInteger, primary_key=True, autoincrement=True)  # Unique ID
    filename = Column(String(255), nullable=False)                 # Original file name
    uploaded_at = Column(DateTime, default=datetime.utcnow)        # Timestamp of upload
    vector = Column(LargeBinary, nullable=False)                   # Image embedding (serialized)
    extra_metadata = Column("metadata", JSON)                      # Additional info (size, content type, equipment type)