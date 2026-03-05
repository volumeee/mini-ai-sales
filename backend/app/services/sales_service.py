"""Sales data service – reads and queries sales data from CSV."""

import math
import threading

import pandas as pd

from app.config import settings

_sales_df: pd.DataFrame | None = None
_lock = threading.Lock()

def _get_dataframe() -> pd.DataFrame:
    """Lazy-load and cache the sales DataFrame with column validation."""
    global _sales_df
    if _sales_df is None:
        with _lock:
            if _sales_df is None:
                df = pd.read_csv(settings.CSV_PATH)
                # Validate columns
                required = ["product_id", "product_name", "jumlah_penjualan", "harga", "diskon", "status"]
                missing = [col for col in required if col not in df.columns]
                if missing:
                    raise ValueError(f"CSV missing columns: {', '.join(missing)}")
                _sales_df = df
    return _sales_df


def get_sales(
    page: int = 1,
    limit: int = 20,
    search: str | None = None,
) -> dict:
    """
    Get paginated sales data with optional search filter.
    Search matches against product_id and product_name.
    """
    df = _get_dataframe()

    if search:
        mask = (
            df["product_id"].str.contains(search, case=False, na=False)
            | df["product_name"].str.contains(search, case=False, na=False)
        )
        df = df[mask]

    total = len(df)
    total_pages = math.ceil(total / limit) if limit > 0 else 1

    start = (page - 1) * limit
    end = start + limit
    page_data = df.iloc[start:end]

    records = page_data.to_dict(orient="records")

    return {
        "data": records,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
    }
