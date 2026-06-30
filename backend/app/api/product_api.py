from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
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
    rows = (
        db.query(
            Product.id.label("id"),
            Product.name.label("name"),
            Product.brand.label("brand"),
            Product.category.label("category"),
            Product.price.label("price"),
            func.coalesce(func.avg(Review.rating), 0).label("average_rating"),
            func.count(Review.id).label("review_count"),
        )
        .outerjoin(Review, Review.product_id == Product.id)
        .group_by(
            Product.id,
            Product.name,
            Product.brand,
            Product.category,
            Product.price,
        )
        .all()
    )

    return [
        {
            "id": row.id,
            "name": row.name,
            "brand": row.brand,
            "category": row.category,
            "price": row.price,
            "average_rating": round(float(row.average_rating), 1),
            "review_count": row.review_count,
        }
        for row in rows
    ]


@router.get("/{product_id}")
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