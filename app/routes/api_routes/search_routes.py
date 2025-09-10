from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image, UnidentifiedImageError
import io

from app.services import generate_embedding
from app.services import search_similar_images
# from app.services.llm_service import generate_repair_instructions  # RAG + LLM

router = APIRouter()


@router.post("/")
async def search_image(file: UploadFile = File(...), top_k: int = 5):
    # Step 1: Validate and read image
    print("Mohit")
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid image file")

    # Step 2: Generate embedding (async)
    query_vector = await generate_embedding(image)

    # Step 3: Search similar images in DB (async)
    results = await search_similar_images(query_vector, top_k)

    # Step 4: Prepare data for LLM
    retrieved_docs = [
        {
            "filename": img.filename,
            "metadata": img.extra_metadata,
            "similarity": float(score)
        }
        for img, score in results
    ]

    # Step 5: Generate repair instructions (RAG + LLM)
    # repair_plan = await generate_repair_instructions(query_vector, retrieved_docs)

    # Step 6: Return full response
    return {
        "status": "success",
        "uploaded_filename": file.filename,
        "top_matches": retrieved_docs,
        # "repair_plan": repair_plan
    }