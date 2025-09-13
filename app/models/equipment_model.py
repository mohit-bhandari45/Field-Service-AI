from sqlalchemy import Column, BigInteger, String, DateTime, JSON, ForeignKey
from sqlalchemy.types import UserDefinedType
from datetime import datetime
from app.config.db import Base


# -----------------------------
# Custom Vector Type for TiDB
# -----------------------------
class Vector(UserDefinedType):
    def __init__(self, dimensions: int):
        self.dimensions = dimensions

    def get_col_spec(self, **kw):
        return f"VECTOR({self.dimensions})"

    def bind_processor(self, dialect):
        def process(value):
            if value is None:
                return None
            # ✅ Convert list of floats → string "[0.1, 0.2, ...]"
            return "[" + ",".join(str(float(x)) for x in value) + "]"
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            # TiDB usually returns as a string like "[0.1,0.2,...]"
            if isinstance(value, str):
                return list(map(float, value.strip("[]").split(",")))
            return value
        return process

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