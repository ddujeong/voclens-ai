from fastapi import FastAPI

from app.api.product_api import router as product_router
from app.core.database import Base, engine
from app.models import Product, Review

Base.metadata.create_all(bind=engine)

app = FastAPI(title="VOCLens AI API")

app.include_router(product_router)


@app.get("/")
def health_check():
    return {"message": "VOCLens AI backend is running"}