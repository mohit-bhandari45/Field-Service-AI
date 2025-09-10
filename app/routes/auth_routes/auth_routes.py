from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
async def login():
    return {"msg": "Login route"}

@router.post("/signup")
async def signup():
    return {"msg": "Signup route"}