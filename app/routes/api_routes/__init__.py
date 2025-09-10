# routes/api_routes/__init__.py
from fastapi import APIRouter
from .search_routes import router as search_router
from .upload_routes import router as upload_router
from .chat_routes import router as chat_router

router = APIRouter()
router.include_router(search_router, prefix="/search")
router.include_router(upload_router, prefix="/upload")
router.include_router(chat_router, prefix="/chat")