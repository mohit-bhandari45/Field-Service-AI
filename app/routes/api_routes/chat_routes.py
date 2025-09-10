from fastapi import APIRouter

router = APIRouter()

router.post("/start_chat/")
# async def start_chat(files: List[UploadFile] = File(...), top_k: int = 5)