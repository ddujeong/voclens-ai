from pydantic import BaseModel


class DashboardKpiResponse(BaseModel):
    total_reviews: int

    positive_reviews: int
    negative_reviews: int
    neutral_reviews: int

    positive_rate: float
    negative_rate: float
    neutral_rate: float
    
class VocKeywordResponse(BaseModel):
    keyword: str
    count: int


class DashboardVocResponse(BaseModel):
    top_complaints: list[VocKeywordResponse]

class ProductReviewStatResponse(BaseModel):
    product_id: int
    product_name: str
    total_reviews: int
    negative_reviews: int
    negative_rate: float