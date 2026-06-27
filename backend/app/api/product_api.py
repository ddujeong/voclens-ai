from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.product import Product
from app.schemas.product_schema import ProductResponse
from app.models.review import Review
from app.services.gemini_service import GeminiService

router = APIRouter(prefix="/products", tags=["Products"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

    return product

@router.get("/{product_id}/summary")
def get_product_summary(
    product_id: int,
    db: Session = Depends(get_db),
):
    reviews = (
        db.query(Review)
        .filter(Review.product_id == product_id)
        .all()
    )

    review_texts = [
        review.content
        for review in reviews
    ]

    if not review_texts:
        return {
            "summary": "아직 요약할 리뷰가 없습니다.",
            "positive": [],
            "negative": [],
        }

    return GeminiService().generate_product_summary(
        review_texts
    )