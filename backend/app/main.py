"""
Mini AI Sales Prediction System – FastAPI Application
======================================================
Entry point for the backend API server.
"""

import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers import auth, predict, sales

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Mini AI Sales Prediction API",
    description=(
        "REST API untuk mengelola data penjualan dan melakukan prediksi "
        "status produk (Laris / Tidak Laris) menggunakan Machine Learning."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ─── CORS ─────────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Global Exception Handler ────────────────────────────────────────────────


@app.exception_handler(FileNotFoundError)
async def file_not_found_handler(_request: Request, exc: FileNotFoundError):
    """Handle missing ML model or data files gracefully."""
    logger.error("File not found: %s", exc)
    return JSONResponse(
        status_code=503,
        content={"detail": "Model ML belum di-train. Jalankan 'python ml/train_model.py' terlebih dahulu."},
    )


@app.exception_handler(Exception)
async def general_exception_handler(_request: Request, exc: Exception):
    """Catch-all handler for unhandled exceptions."""
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


# ─── Routers ──────────────────────────────────────────────────────────────────

app.include_router(auth.router)
app.include_router(sales.router)
app.include_router(predict.router)


# ─── Health Check ─────────────────────────────────────────────────────────────


@app.get("/", tags=["Health"])
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "message": "Mini AI Sales Prediction API is running"}
