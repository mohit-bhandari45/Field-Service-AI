import json
import pickle
from app.config.db import SessionLocal
from app.models.repair_model import RepairLog
from app.services import generate_text_embedding

REPAIR_FILE = "app/seed_repairs/repairs.json"

def seed_repairs():
    db = SessionLocal()
    db.query(RepairLog).delete()
    db.commit()
    print("✅ Deleted all repair logs!")

    try:
        with open(REPAIR_FILE) as f:
            repairs = json.load(f)

        for repair in repairs:
            vector = generate_text_embedding(repair["description"])
            vector_blob = pickle.dumps(vector)

            log = RepairLog(
                equipment_image_id=repair.get("equipment_image_id"),
                description=repair["description"],
                solution_text=repair["solution"],
                vector=vector_blob,
                extra_metadata=repair.get("metadata", {})
            )
            db.add(log)

        db.commit()
        print(f"✅ Seeded {len(repairs)} repairs")
    except Exception as e:
        db.rollback()
        print("❌ Error seeding repairs:", e)
    finally:
        db.close()
