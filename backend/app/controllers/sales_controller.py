"""Controller for sales data – bridges HTTP layer with sales service."""

from app.schemas.sales import SalesResponse
from app.services.sales_service import get_sales


def handle_list_sales(page: int, limit: int, search: str | None) -> SalesResponse:
    """Fetch paginated sales data from service layer."""
    return get_sales(page=page, limit=limit, search=search)
