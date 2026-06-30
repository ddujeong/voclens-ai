from pydantic import BaseModel


class ProductResponse(BaseModel):
    id: int
    name: str
    brand: str
    category: str
    price: int

    average_rating: float
    review_count: int

    class Config:
        from_attributes = True