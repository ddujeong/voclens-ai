from pydantic import BaseModel


class DashboardKpiResponse(BaseModel):
    total_reviews: int

    positive_reviews: int
    negative_reviews: int
    neutral_reviews: int

    positive_rate: float
    negative_rate: float
    neutral_rate: float