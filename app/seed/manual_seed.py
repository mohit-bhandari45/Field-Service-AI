import os
import asyncio
from app.config.db import SessionLocal
from app.models.manual_model import ManualEmbedding
from app.services import generate_text_embedding
from app.utils.pdf_utils import extract_chunks_from_pdf
from app.seed.seed_manuals.download import download_pdfs

MANUALS_FOLDER = "app/seed/seed_manuals/assets"

async def seed_manual_chunks():
    db = SessionLocal()
    db.query(ManualEmbedding).delete()
    db.commit()
    print("✅ Deleted all manual chunks!")
    success = False

    # Download PDFs (make sure folder exists)
    download_pdfs(MANUALS_FOLDER)

    try:
        for filename in os.listdir(MANUALS_FOLDER):
            if not filename.endswith(".pdf"):
                continue

            path = os.path.join(MANUALS_FOLDER, filename)

            # Skip files that do not exist
            if not os.path.exists(path):
                print(f"⚠️ Skipping missing file: {filename}")
                continue

            # Optionally skip empty PDFs
            if os.path.getsize(path) == 0:
                print(f"⚠️ Skipping empty PDF: {filename}")
                continue

            # Split into chunks
            try:
                chunks = extract_chunks_from_pdf(path)  # returns list of (chunk_text, page_no)
            except Exception as e:
                print(f"❌ Failed to extract chunks from {filename}: {e}")
                continue

            for idx, (chunk_text, page_no) in enumerate(chunks):
                vector = await generate_text_embedding(chunk_text)
                if vector is None:
                    print(f"⚠️ Skipping chunk {idx} from {filename} (no embedding)")
                    continue

                metadata = {
                    "manual_name": filename,
                    "page": page_no,
                }

                manual_entry = ManualEmbedding(
                    title=filename,
                    section=f"Page {page_no}, Chunk {idx}",
                    content=chunk_text,
                    vector=vector,
                    extra_metadata=metadata,
                )
                db.add(manual_entry)

        db.commit()
        print(f"✅ Seeded manuals from {MANUALS_FOLDER}")
        success = True

    except Exception as e:
        db.rollback()
        print("❌ Error seeding manuals:", e)
    finally:
        db.close()

    return success

if __name__ == "__main__":
    asyncio.run(seed_manual_chunks())