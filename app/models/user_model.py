from sqlalchemy import Column, BigInteger, String, DateTime
from datetime import datetime
from app.config.db import Base  

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)  
    created_at = Column(DateTime, default=datetime.utcnow)
