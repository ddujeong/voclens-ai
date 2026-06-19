from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.review import Review
from app.schemas.chat_schema import (
    ChatRequest,
    ChatResponse,
)
from app.services.admin_chat_service import (
    AdminChatService,
)

router = APIRouter(
    prefix="/admin/chat",
    tags=["Admin Chat"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):

    reviews = (
        db.query(Review)
        .filter(Review.sentiment == "negative")
        .all()
    )

    answer = (
        AdminChatService.analyze_top_complaint(
            reviews
        )
    )

    return ChatResponse(
        answer=answer
    )