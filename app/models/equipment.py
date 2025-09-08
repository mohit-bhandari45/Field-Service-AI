from sqlalchemy import Column, BigInteger, String, DateTime, LargeBinary, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class EquipmentEmbedding(Base):
    __tablename__ = "equipment_embeddings"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    vector = Column(LargeBinary, nullable=False)
    metadata = Column(JSON)