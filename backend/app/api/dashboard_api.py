from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.review import Review
from app.schemas.dashboard_schema import DashboardKpiResponse

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