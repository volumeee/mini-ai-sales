"""Pydantic schemas for sales data endpoints."""

from pydantic import BaseModel


class SalesItem(BaseModel):
    """Single sales record."""
    product_id: str
    product_name: str
    jumlah_penjualan: int
    harga: int
    diskon: int
    status: str


class SalesResponse(BaseModel):
    """Paginated sales data response."""
    data: list[SalesItem]
    total: int
    page: int
    limit: int
    total_pages: int
