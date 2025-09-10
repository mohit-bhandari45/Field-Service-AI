import os
import pickle
import asyncio
from PIL import Image
from app.config.db import SessionLocal
from app.models import EquipmentImage
from app.services import generate_embedding  # your embedding function
from app.seed.seed_images.download_image import download_images
import mimetypes

# Folder containing your images
IMAGE_FOLDER = "app/seed_images/assets";

async def seed_images():
    db = SessionLocal()

    # Delete existing first
    db.query(EquipmentImage).delete()
    db.commit()
    print(f"✅ Deleted All files!")

    try:
        download_images()  # Download all images if not exist

        for filename in os.listdir(IMAGE_FOLDER):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                path = os.path.join(IMAGE_FOLDER, filename)

                # Open and validate image
                image = Image.open(path).convert("RGB")

                # Generate embedding vector
                vector = await generate_embedding(image)

                # Prepare metadata
                content_type, _ = mimetypes.guess_type(path)
                if not content_type and image.format:
                    content_type = f"image/{image.format.lower()}"
                if not content_type:
                    content_type = "application/octet-stream"  # last fallback

                metadata = {
                    "filename": filename,
                    "content_type": content_type,
                    "size_bytes": os.path.getsize(path),
                }

                # Serialize vector
                vector_blob = pickle.dumps(vector)

                # Create DB entry
                equipment = EquipmentImage(
                    filename=filename,
                    vector=vector_blob,
                    extra_metadata=metadata
                )
                db.add(equipment)
        
        # Commit all at once
        db.commit()
        print(f"✅ Seeded {len(os.listdir(IMAGE_FOLDER))} images.")
    
    except Exception as e:
        db.rollback()
        print("❌ Error seeding images:", e)
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(seed_images())