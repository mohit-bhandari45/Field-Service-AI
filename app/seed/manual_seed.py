import os
import pickle
import asyncio
from app.config.db import SessionLocal
from app.models.manual_model import ManualChunk
from app.services import generate_text_embedding  # you need a text embedding generator
from app.utils.pdf_utils import extract_chunks_from_pdf  # custom function
from app.seed.seed_manuals.download import download_pdfs

MANUALS_FOLDER = "app/seed_manuals/assets"

async def seed_manual_chunks():
    db = SessionLocal()
    db.query(ManualChunk).delete()
    db.commit()
    print("✅ Deleted all manual chunks!")

    download_pdfs()
    try:
        for filename in os.listdir(MANUALS_FOLDER):
            if filename.endswith(".pdf"):
                path = os.path.join(MANUALS_FOLDER, filename)

                # Split into chunks
                chunks = extract_chunks_from_pdf(path)  # returns list of (chunk_text, page_no)

                for chunk_text, page_no in chunks:
                    vector = await generate_text_embedding(chunk_text)
                    vector_blob = pickle.dumps(vector)

                    metadata = {
                        "manual_name": filename,
                        "page": page_no,
                    }

                    chunk = ManualChunk(
                        manual_name=filename,
                        chunk_text=chunk_text,
                        vector=vector_blob,
                        extra_metadata=metadata
                    )
                    db.add(chunk)

        db.commit()
        print(f"✅ Seeded manuals from {MANUALS_FOLDER}")
    except Exception as e:
        db.rollback()
        print("❌ Error seeding manuals:", e)
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(seed_manual_chunks())