"""Prediction routes."""

from fastapi import APIRouter, Depends

from app.controllers.predict_controller import handle_predict
from app.dependencies import get_current_user
from app.schemas.predict import PredictRequest, PredictResponse

router = APIRouter(prefix="/api", tags=["Prediction"])


@router.post("/predict", response_model=PredictResponse, summary="Predict product status")
def predict(
    body: PredictRequest,
    _user: dict = Depends(get_current_user),
):
    return handle_predict(body)
