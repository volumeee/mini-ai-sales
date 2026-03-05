"""Pydantic schemas for prediction endpoints."""

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    """Prediction request body."""
    jumlah_penjualan: float = Field(..., ge=0, le=1000000, examples=[150])
    harga: float = Field(..., ge=0, le=100000000000, examples=[50000])
    diskon: float = Field(..., ge=0, le=100, examples=[10])


class PredictResponse(BaseModel):
    """Prediction result response."""
    status: str
    confidence: float
    input_data: dict
