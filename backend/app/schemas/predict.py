"""Pydantic schemas for prediction endpoints."""

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    """Prediction request body."""
    jumlah_penjualan: int = Field(..., ge=0, examples=[150])
    harga: int = Field(..., ge=0, examples=[50000])
    diskon: int = Field(..., ge=0, le=100, examples=[10])


class PredictResponse(BaseModel):
    """Prediction result response."""
    status: str
    confidence: float
    input_data: dict
