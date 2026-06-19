from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.product_api import router as product_router
from app.api.review_api import router as review_router
from app.api.dashboard_api import router as dashboard_router
from app.api.admin_review_api import router as admin_review_router
from app.api.admin_chat_api import router as admin_chat_router

from app.core.database import Base, engine
from app.models import Product, Review

Base.metadata.create_all(bind=engine)

app = FastAPI(title="VOCLens AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_router)
app.include_router(review_router)
app.include_router(dashboard_router)
app.include_router(admin_review_router)
app.include_router(admin_chat_router)

@app.get("/")
def health_check():
    return {"message": "VOCLens AI backend is running"}