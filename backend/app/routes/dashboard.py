from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user_model import User
from app.services.dashboard_service import (
    get_dashboard_summary,
    get_low_stock_items,
    get_recent_sales,
    get_sales_last_days,
    get_top_products,
)


router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
def read_dashboard_summary(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    return get_dashboard_summary(db)


@router.get("/sales-overview")
def read_sales_overview(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    return get_sales_last_days(db)


@router.get("/low-stock")
def read_low_stock(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    return get_low_stock_items(db)


@router.get("/recent-sales")
def read_recent_sales(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    return get_recent_sales(db)


@router.get("/top-products")
def read_top_products(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    return get_top_products(db)
