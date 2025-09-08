from fastapi import APIRouter, UploadFile, File
from PIL import Image
import io
from app.services.embedding import generate_embedding
from app.services.tidb import store_vector

router = APIRouter()


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    #  Reading image
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    # Generate embedding
    vector = await generate_embedding(image)

    # Storing embedding + metadata in TiDB
    metadata = {"filename": file.filename}
    await store_vector(vector, metadata)

    return {"filename": file.filename, "vector_length": len(vector)}
