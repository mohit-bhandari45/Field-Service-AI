from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image, UnidentifiedImageError
import io
from sqlalchemy.orm import Session
from app.config.db import SessionLocal
from app.services import generate_embedding, search_similar_images
from app.models import ChatSession
from app.models.equipment_model import EquipmentImage

router = APIRouter()


@router.post("/")
async def search_image(file: UploadFile = File(...), top_k: int = 5):
    # Step 1: Validate and read image
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid image file")

    # Step 2: Generate embedding (async)
    query_vector = await generate_embedding(image)

    # Step 3: Search similar images in DB (native TiDB vector search)
    results = await search_similar_images(query_vector, top_k)

    # Step 4: Prepare docs for LLM
    retrieved_docs = [
        {
            "filename": img.filename,
            "metadata": img.extra_metadata,
            "similarity": float(score),
        }
        for img, score in results
    ]

    # Step 5: Mock repair plan (replace with LLM RAG later)
    repair_plan = "Hate me!"

    # Step 6: Store chat + uploaded image
    db: Session = SessionLocal()
    try:
        chat = ChatSession(
            context=[
                {"role": "user", "content": "Uploaded equipment image"},
                {"role": "assistant", "content": repair_plan},
            ]
        )
        db.add(chat)
        db.commit()
        db.refresh(chat)

        chat_id = chat.id

        image_record = EquipmentImage(
            filename=file.filename,
            vector=query_vector,  # ✅ store raw list into VECTOR(512)
            extra_metadata={
                "size": len(image_bytes),
                "content_type": file.content_type,
            },
            chat_session_id=chat_id,
        )

        db.add(image_record)
        db.commit()
    finally:
        db.close()

    # Step 7: Return response
    return {
        "status": "success",
        "length": len(retrieved_docs),
        "chat_id": chat_id,
        "repair_guide": repair_plan,
        "top_matches": retrieved_docs,
    }
