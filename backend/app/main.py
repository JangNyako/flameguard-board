from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import importlib
import pkgutil

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import engine, Base
from app.db.models import (
    user as user_model,
    session as session_model,
    detection_log as detection_log_model,
)

from fastapi.staticfiles import StaticFiles

def init_db():
    Base.metadata.create_all(bind=engine)

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Welcome to FlameGuard API!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_dir = Path(__file__).parent / "api"

# auto import router
for api in api_dir.iterdir():
    if api.is_dir():  # folder(each endpoint)
        router_module = f"app.api.{api.name}.router"
        try:
            module = importlib.import_module(router_module)
            if hasattr(module, "router"):
                app.include_router(module.router)
                print(f"✅ router added: {router_module}")  # debug
        except ModuleNotFoundError:
            if api.name == "__pycache__" or api.name == "__init__":
                continue
            print(f"⚠️ {router_module} not found (router.py is missing)")

# serve log folder as static files
log_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "log"))

# log 폴더가 없으면 생성
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

app.mount("/log", StaticFiles(directory=log_directory), name="log")
upload_directory = os.path.join(os.path.dirname(__file__), "..", "static", "uploads")
if not os.path.exists(upload_directory):
    os.makedirs(upload_directory)

app.mount("/static/uploads", StaticFiles(directory=upload_directory), name="uploads")