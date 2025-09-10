import random
from datetime import datetime, timedelta
from app.config.db import SessionLocal
from app.models.sensor_log_model import SensorLog

def seed_sensors():
    db = SessionLocal()
    db.query(SensorLog).delete()
    db.commit()
    print("✅ Deleted all sensor logs!")

    try:
        for equipment_id in range(1, 5):  # simulate 4 machines
            for i in range(10):  # 10 readings each
                log = SensorLog(
                    equipment_id=equipment_id,
                    sensor_type="temperature",
                    sensor_value=str(random.randint(20, 100)),
                    recorded_at=datetime.utcnow() - timedelta(minutes=i*5),
                    extra_metadata={"unit": "Celsius"}
                )
                db.add(log)

        db.commit()
        print("✅ Seeded sensor logs")
    except Exception as e:
        db.rollback()
        print("❌ Error seeding sensors:", e)
    finally:
        db.close()
