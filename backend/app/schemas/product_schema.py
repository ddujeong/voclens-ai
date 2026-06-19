from pydantic import BaseModel


class ProductResponse(BaseModel):
    id: int
    name: str
    brand: str
    category: str
    price: int

    class Config:
        from_attributes = True