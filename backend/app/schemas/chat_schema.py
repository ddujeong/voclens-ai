from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    product_id: int | None = None
    category: str | None = None


class ChatResponse(BaseModel):
    answer: str