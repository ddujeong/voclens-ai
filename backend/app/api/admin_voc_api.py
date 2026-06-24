from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.voc_insight_service import (
    VocInsightService,
)

router = APIRouter(
    prefix="/admin/voc",
    tags=["VOC Insight"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/risk-products")
def risk_products(
    category: str,
    tag: str,
    db: Session = Depends(get_db),
):
    rows = VocInsightService.get_risk_products(
        category=category,
        tag=tag,
        db=db,
    )

    return [
        {
            "product_id": row.id,
            "product_name": row.name,
            "category": row.category,
            "negative_count": row.negative_count,
        }
        for row in rows
    ]