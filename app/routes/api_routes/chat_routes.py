from fastapi import UploadFile, File, APIRouter
from typing import List

router = APIRouter()

router.post("/start_chat/")
# async def start_chat(files: List[UploadFile] = File(...), top_k: int = 5):
