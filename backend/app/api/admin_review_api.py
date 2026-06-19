from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.product import Product
from app.models.review import Review
from app.schemas.review_schema import (
    AdminReviewSearchResponse,
)

router = APIRouter(
    prefix="/admin/reviews",
    tags=["Admin Reviews"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/search",
    response_model=list[AdminReviewSearchResponse],
)
def search_reviews(
    keyword: str = Query(...),
    db: Session = Depends(get_db),
):
    results = (
        db.query(Review, Product)
        .join(Product, Review.product_id == Product.id)
        .filter(
            Review.content.ilike(f"%{keyword}%")
        )
        .all()
    )

    return [
        AdminReviewSearchResponse(
            id=review.id,
            product_id=review.product_id,
            product_name=product.name,
            rating=review.rating,
            content=review.content,
            sentiment=review.sentiment,
            created_at=review.created_at,
        )
        for review, product in results
    ]