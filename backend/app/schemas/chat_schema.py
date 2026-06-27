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


class VocAnalysis(BaseModel):
    summary: str
    positive: list[str]
    negative: list[str]
    insight: str
    improvements: list[str]


class ChatResponse(BaseModel):
    answer: str
    analysis: VocAnalysis | None = None
    risk_products: list[RiskProductItem] = []
    category: str | None = None
    tag: str | None = None