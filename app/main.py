from fastapi import FastAPI
from app.routes import all_routers
from app.config.db import engine, Base
from sqlalchemy import inspect
from app.models import *

app = FastAPI(title="Field Service AI")

# Including Routes
for router, prefix in all_routers:
    app.include_router(router=router, prefix=prefix)

@app.get("/")
async def home():
    return {"msg": "Field Service AI running"}


# Create tables (if not already created)
@app.on_event("startup")
def on_startup():
    print("🚀 App starting, creating tables if not exist...")
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    print("Tables Created: ", inspector.get_table_names())


@app.on_event("shutdown")
def on_shutdown():
    print("🛑 App shutting down...")
