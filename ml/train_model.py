"""
ML Training Script - Sales Product Status Prediction
=====================================================
Trains a Random Forest classifier to predict product status (Laris/Tidak)
based on: jumlah_penjualan, harga, diskon.
"""

import os

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# ─── Constants ────────────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "sales_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model.joblib")
ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder.joblib")
REPORT_PATH = os.path.join(BASE_DIR, "evaluation_report.txt")

FEATURE_COLUMNS = ["jumlah_penjualan", "harga", "diskon"]
TARGET_COLUMN = "status"
TEST_SIZE = 0.2
RANDOM_STATE = 42


# ─── Data Loading & Preprocessing ────────────────────────────────────────────

def load_data(path: str) -> pd.DataFrame:
    """Load CSV data and perform basic validation."""
    df = pd.read_csv(path)

    required_cols = FEATURE_COLUMNS + [TARGET_COLUMN]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df


def preprocess(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, LabelEncoder]:
    """Clean data and prepare features/target arrays."""
    df = df.dropna(subset=FEATURE_COLUMNS + [TARGET_COLUMN])
    df = df.copy()

    # Ensure numeric feature columns
    for col in FEATURE_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=FEATURE_COLUMNS)

    X = df[FEATURE_COLUMNS].values

    le = LabelEncoder()
    y = le.fit_transform(df[TARGET_COLUMN])

    return X, y, le


# ─── Training ────────────────────────────────────────────────────────────────

def train(X: np.ndarray, y: np.ndarray) -> tuple[RandomForestClassifier, dict]:
    """Train Random Forest and return model + evaluation metrics."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    metrics = {
        "accuracy": accuracy,
        "classification_report": report,
        "confusion_matrix": cm,
        "train_size": len(X_train),
        "test_size": len(X_test),
    }

    return model, metrics


# ─── Save / Report ───────────────────────────────────────────────────────────

def save_artifacts(model: RandomForestClassifier, le: LabelEncoder, metrics: dict):
    """Persist model, encoder, and evaluation report to disk."""
    joblib.dump(model, MODEL_PATH)
    joblib.dump(le, ENCODER_PATH)

    with open(REPORT_PATH, "w") as f:
        f.write("=" * 60 + "\n")
        f.write("  Sales Prediction Model – Evaluation Report\n")
        f.write("=" * 60 + "\n\n")
        f.write("Model           : Random Forest Classifier\n")
        f.write(f"Features        : {FEATURE_COLUMNS}\n")
        f.write(f"Train samples   : {metrics['train_size']}\n")
        f.write(f"Test samples    : {metrics['test_size']}\n")
        f.write(f"Accuracy        : {metrics['accuracy']:.4f}\n\n")
        f.write("Classification Report:\n")
        f.write(metrics["classification_report"])
        f.write("\n\nConfusion Matrix:\n")
        f.write(str(metrics["confusion_matrix"]))
        f.write("\n")

    print(f"✅ Model saved to: {MODEL_PATH}")
    print(f"✅ Encoder saved to: {ENCODER_PATH}")
    print(f"✅ Report saved to: {REPORT_PATH}")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("📊 Loading data...")
    df = load_data(DATA_PATH)
    print(f"   Loaded {len(df)} records")

    print("🔧 Preprocessing...")
    X, y, le = preprocess(df)
    print(f"   Features shape: {X.shape}")
    print(f"   Classes: {list(le.classes_)}")

    print("🤖 Training model...")
    model, metrics = train(X, y)
    print(f"   Accuracy: {metrics['accuracy']:.4f}")

    print("\n📋 Classification Report:")
    print(metrics["classification_report"])

    save_artifacts(model, le, metrics)
    print("\n🎉 Training complete!")


if __name__ == "__main__":
    main()
