from datetime import datetime
from pydantic import BaseModel


class ReviewCreateRequest(BaseModel):
    rating: int
    content: str


class ReviewResponse(BaseModel):
    id: int
    product_id: int
    rating: int
    content: str
    sentiment: str | None
    created_at: datetime

    class Config:
        from_attributes = True