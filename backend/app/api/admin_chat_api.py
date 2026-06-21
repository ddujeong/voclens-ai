from fastapi import APIRouter, Depends, HTTPException
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
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="질문을 입력해주세요.",
        )
    answer = AdminChatService.answer_with_rag(
        question=request.question,
        db=db,
    )

    return ChatResponse(
        answer=answer
    )