from fastapi import FastAPI
from app.routes import upload_routes
from app.config.db import engine, Base
from sqlalchemy import inspect
from app.models import *

app = FastAPI(title="Field Service AI")

# Including Routes
app.include_router(upload_routes.router, prefix="/upload")
# app.include_router(search.router, prefix="/search")
# app.include_router(repair.router, prefix="/repair")

@app.get("/")
async def home():
    return {"msg": "Field Service AI running"}

# Create tables (if not already created)
@app.on_event("startup")
def on_startup():
    print("🚀 App starting, creating tables if not exist...")
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    print("Tables Created: " , inspector.get_table_names())

@app.on_event("shutdown")
def on_shutdown():
    print("🛑 App shutting down...")