from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.review_classifier_service import review_classifier_service


router = APIRouter(
    prefix="/ml",
    tags=["ML Test"],
)


class MlPredictRequest(BaseModel):
    text: str = Field(min_length=1)


@router.post("/predict")
def predict_review(request: MlPredictRequest):
    return review_classifier_service.predict(
        request.text
    )