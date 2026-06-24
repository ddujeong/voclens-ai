from pydantic import BaseModel


class RiskProductResponse(BaseModel):
    product_id: int
    product_name: str
    category: str
    negative_count: int