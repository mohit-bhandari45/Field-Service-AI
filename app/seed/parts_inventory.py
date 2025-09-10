import csv
from app.config.db import SessionLocal
from app.models.part_inventory_model import PartInventory

PARTS_FILE = "app/seed_parts/parts.csv"

def seed_parts():
    db = SessionLocal()
    db.query(PartInventory).delete()
    db.commit()
    print("✅ Deleted all parts!")

    try:
        with open(PARTS_FILE, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                part = PartInventory(
                    part_name=row["part_name"],
                    part_number=row["part_number"],
                    quantity_available=int(row["quantity_available"]),
                    extra_metadata={"supplier": row.get("supplier", "unknown")}
                )
                db.add(part)

        db.commit()
        print(f"✅ Seeded parts from {PARTS_FILE}")
    except Exception as e:
        db.rollback()
        print("❌ Error seeding parts:", e)
    finally:
        db.close()
