from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image, UnidentifiedImageError
import io
from app.services import generate_embedding
from app.utils.store_vector_utils import store_vector

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Read & validate image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid image file")

    # Generate embedding (ensure it's a list[float])
    vector = (await generate_embedding(image)).tolist()

    # Metadata
    metadata = {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(image_bytes),
    }

    # Store in TiDB and get ID back
    embedding_id = await store_vector(vector, metadata)

    return {
        "status": "success",
        "id": embedding_id,
        "filename": file.filename,
        "vector_length": len(vector),
    }