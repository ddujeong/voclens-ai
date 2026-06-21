from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.services.review_rag_service import (
    ReviewRagService,
)

router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/search")
def rag_search(
    question: str,
    db: Session = Depends(get_db),
):
    result = ReviewRagService.search(
        question,
        db,
    )

    return [
        {
            "review_id": row.review_id,
            "score": row.score,
            "content": row.content,
        }
        for row in result
    ]