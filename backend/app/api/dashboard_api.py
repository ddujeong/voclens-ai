from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.review import Review
from collections import Counter
from app.models.product import Product

from app.schemas.dashboard_schema import (
    DashboardKpiResponse,
    DashboardVocResponse,
    VocKeywordResponse,
    ProductReviewStatResponse
)
from app.core.voc_keywords import COMPLAINT_KEYWORDS

router = APIRouter(
    prefix="/admin/dashboard",
    tags=["Dashboard"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/kpi",
    response_model=DashboardKpiResponse
)
def get_dashboard_kpi(
    db: Session = Depends(get_db)
):
    total = db.query(Review).count()

    positive = (
        db.query(Review)
        .filter(Review.sentiment == "positive")
        .count()
    )

    negative = (
        db.query(Review)
        .filter(Review.sentiment == "negative")
        .count()
    )

    neutral = (
        db.query(Review)
        .filter(Review.sentiment == "neutral")
        .count()
    )

    if total == 0:
        return DashboardKpiResponse(
            total_reviews=0,
            positive_reviews=0,
            negative_reviews=0,
            neutral_reviews=0,
            positive_rate=0,
            negative_rate=0,
            neutral_rate=0,
        )

    return DashboardKpiResponse(
        total_reviews=total,

        positive_reviews=positive,
        negative_reviews=negative,
        neutral_reviews=neutral,

        positive_rate=round((positive / total) * 100, 1),
        negative_rate=round((negative / total) * 100, 1),
        neutral_rate=round((neutral / total) * 100, 1),
    )
    
@router.get(
    "/voc",
    response_model=DashboardVocResponse
)
def get_voc_analysis(
    db: Session = Depends(get_db)
):

    reviews = (
        db.query(Review)
        .filter(Review.sentiment == "negative")
        .all()
    )

    counter = Counter()

    for review in reviews:
        for keyword in COMPLAINT_KEYWORDS:
            if keyword in review.content:
                counter[keyword] += 1

    top_keywords = counter.most_common(5)

    return DashboardVocResponse(
        top_complaints=[
            VocKeywordResponse(
                keyword=keyword,
                count=count,
            )
            for keyword, count in top_keywords
        ]
    )
    
@router.get(
    "/products",
    response_model=list[ProductReviewStatResponse]
)
def get_product_review_stats(
    db: Session = Depends(get_db)
):
    products = db.query(Product).all()

    result = []

    for product in products:
        total = (
            db.query(Review)
            .filter(Review.product_id == product.id)
            .count()
        )

        negative = (
            db.query(Review)
            .filter(
                Review.product_id == product.id,
                Review.sentiment == "negative"
            )
            .count()
        )

        negative_rate = 0 if total == 0 else round((negative / total) * 100, 1)

        result.append(
            ProductReviewStatResponse(
                product_id=product.id,
                product_name=product.name,
                total_reviews=total,
                negative_reviews=negative,
                negative_rate=negative_rate,
            )
        )

    return result