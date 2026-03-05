"""Controller for prediction – bridges HTTP layer with prediction service."""

from app.schemas.predict import PredictRequest, PredictResponse
from app.services.predict_service import predict_status


def handle_predict(body: PredictRequest) -> PredictResponse:
    """Run ML prediction and return formatted result."""
    result = predict_status(
        jumlah_penjualan=body.jumlah_penjualan,
        harga=body.harga,
        diskon=body.diskon,
    )
    return result
