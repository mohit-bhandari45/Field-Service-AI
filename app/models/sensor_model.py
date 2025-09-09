from sqlalchemy import Column, BigInteger, String, DateTime, JSON
from datetime import datetime
from app.config.db import Base

# -----------------------------
# Sensor Log Model
# Stores readings from IoT sensors attached to equipment
# -----------------------------
class SensorLog(Base):
    __tablename__ = "sensor_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)       # Unique ID for each sensor reading
    equipment_id = Column(BigInteger, nullable=False)                   # Link to equipment (can map to EquipmentImage or a separate Equipment table)
    sensor_type = Column(String(50), nullable=False)                    # Type of sensor (vibration, temperature, humidity, etc.)
    sensor_value = Column(String(50), nullable=False)                   # Sensor reading (stored as string for flexibility)
    recorded_at = Column(DateTime, default=datetime.utcnow)             # Timestamp of the reading
    extra_metadata = Column("metadata", JSON)                            # Additional info: unit, sensor location, calibration data, etc.