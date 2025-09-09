from sqlalchemy import Column, BigInteger, String, DateTime, LargeBinary, JSON
from datetime import datetime
from app.config.db import Base

# -----------------------------
# Repair Log Model
# Stores past repair cases, solutions, and optional embeddings
# -----------------------------
class RepairLog(Base):
    __tablename__ = "repair_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)   # Unique ID
    equipment_image_id = Column(BigInteger, nullable=True)          # Optional link to EquipmentImage
    description = Column(String(255), nullable=False)                    # Issue or problem description
    solution_text = Column(String(255), nullable=False)                  # Step-by-step repair solution
    vector = Column(LargeBinary, nullable=True)                     # Optional embedding for RAG or search
    extra_metadata = Column("metadata", JSON)                       # Metadata: technician, tools used, comments
    created_at = Column(DateTime, default=datetime.utcnow)          # Timestamp when the log was created
