from fastapi import FastAPI
from app.routes import upload

app = FastAPI(title="Field Service AI")

# Including Routes
app.include_router(upload.router, prefix="/upload")
# app.include_router(search.router, prefix="/search")
# app.include_router(repair.router, prefix="/repair")

@app.get("/")
async def home():
    return {"msg": "Field Service AI running"}
