import os
import asyncio
import mimetypes
from PIL import Image, UnidentifiedImageError

from app.config.db import SessionLocal
from app.models import EquipmentImage
from app.services import generate_embedding
from app.seed.seed_images.download_image import download_images

# Folder containing your images
IMAGE_FOLDER = "app/seed/seed_images/assets"


async def seed_images() -> bool:
    db = SessionLocal()
    success = False

    # Delete existing records first
    db.query(EquipmentImage).delete()
    db.commit()
    print("✅ Deleted all existing equipment images")

    try:
        # Download missing images if needed
        download_images()

        images_to_add = []
        for filename in os.listdir(IMAGE_FOLDER):
            if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            path = os.path.join(IMAGE_FOLDER, filename)

            try:
                # Open and validate image
                image = Image.open(path).convert("RGB")
            except UnidentifiedImageError:
                print(f"⚠️ Skipping invalid image: {filename}")
                continue

            # Generate embedding vector
            vector = await generate_embedding(image)

            # Ensure correct length (TiDB VECTOR(768))
            if len(vector) != 512:
                print(f"⚠️ Skipping {filename}: expected 512-dim vector, got {len(vector)}")
                continue

            # Guess content type
            content_type, _ = mimetypes.guess_type(path)
            if not content_type and image.format:
                content_type = f"image/{image.format.lower()}"
            if not content_type:
                content_type = "application/octet-stream"

            # Prepare DB object
            equipment = EquipmentImage(
                filename=filename,
                vector=vector,  # 👈 stored directly into VECTOR(768)
                extra_metadata={
                    "filename": filename,
                    "content_type": content_type,
                    "size_bytes": os.path.getsize(path),
                },
            )
            images_to_add.append(equipment)

        # Bulk insert for efficiency
        if images_to_add:
            db.add_all(images_to_add)
            db.commit()
            print(f"✅ Seeded {len(images_to_add)} images into TiDB")
            success = True
        else:
            print("⚠️ No valid images found to seed")

    except Exception as e:
        db.rollback()
        print("❌ Error seeding images:", e)
    finally:
        db.close()

    return success

if __name__ == "__main__":
    asyncio.run(seed_images())