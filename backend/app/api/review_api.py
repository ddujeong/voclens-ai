from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.product import Product
from app.models.review import Review
from app.schemas.review_schema import ReviewCreateRequest, ReviewResponse
from app.services.gemini_service import GeminiService

router = APIRouter(
    prefix="/products/{product_id}/reviews",
    tags=["Reviews"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("", response_model=list[ReviewResponse])
def get_reviews(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

    return (
        db.query(Review)
        .filter(Review.product_id == product_id)
        .order_by(Review.created_at.desc())
        .all()
    )


@router.post("", response_model=ReviewResponse)
def create_review(
    product_id: int,
    request: ReviewCreateRequest,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

    try:
        gemini_service = GeminiService()
        sentiment = gemini_service.analyze_review_sentiment(
            request.content
        )
    except Exception:
        sentiment = "neutral"

    review = Review(
        product_id=product_id,
        rating=request.rating,
        content=request.content,
        sentiment=sentiment,
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return review