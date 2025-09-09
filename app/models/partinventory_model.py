from sqlalchemy import Column, BigInteger, String, DateTime, JSON
from datetime import datetime
from app.config.db import Base

# -----------------------------
# Parts Inventory Model
# Stores inventory information about spare parts for equipment
# -----------------------------
class PartInventory(Base):
    __tablename__ = "part_inventory"

    id = Column(BigInteger, primary_key=True, autoincrement=True)       # Unique ID for the part
    part_name = Column(String(255), nullable=False)                     # Name of the part
    part_number = Column(String(100), nullable=False)                   # Manufacturer or internal part number
    quantity_available = Column(BigInteger, default=0)                  # Current stock quantity
    extra_metadata = Column("metadata", JSON)                           # Metadata: compatible equipment, supplier info, warehouse location
    created_at = Column(DateTime, default=datetime.utcnow)              # Timestamp when part was added to DB