"""Sales data routes."""

from fastapi import APIRouter, Depends, Query

from app.controllers.sales_controller import handle_list_sales
from app.dependencies import get_current_user
from app.schemas.sales import SalesResponse

router = APIRouter(prefix="/api", tags=["Sales"])


@router.get("/sales", response_model=SalesResponse, summary="Get sales data")
def list_sales(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    search: str | None = Query(None, description="Search by product_id or product_name"),
    _user: dict = Depends(get_current_user),
):
    return handle_list_sales(page=page, limit=limit, search=search)
