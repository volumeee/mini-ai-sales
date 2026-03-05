"""Prediction service – loads ML model and makes predictions."""

import joblib
import numpy as np

from app.config import settings

_model = None
_encoder = None


def _load_model():
    """Lazy-load model and encoder from disk."""
    global _model, _encoder
    if _model is None:
        _model = joblib.load(settings.MODEL_PATH)
        _encoder = joblib.load(settings.ENCODER_PATH)
    return _model, _encoder


def predict_status(jumlah_penjualan: int, harga: int, diskon: int) -> dict:
    """
    Predict product status (Laris / Tidak) using the trained model.
    Returns predicted label and confidence score.
    """
    model, encoder = _load_model()

    features = np.array([[jumlah_penjualan, harga, diskon]])
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]

    predicted_label = encoder.inverse_transform([prediction])[0]
    confidence = float(max(probabilities))

    return {
        "status": predicted_label,
        "confidence": round(confidence, 4),
        "input_data": {
            "jumlah_penjualan": jumlah_penjualan,
            "harga": harga,
            "diskon": diskon,
        },
    }
