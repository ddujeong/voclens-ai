from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    product_id: int | None = None
    category: str | None = None


class RiskProductItem(BaseModel):
    product_id: int
    product_name: str
    category: str
    negative_count: int


class ChatResponse(BaseModel):
    answer: str
    risk_products: list[RiskProductItem] = []
    category: str | None = None
    tags: str | None = None