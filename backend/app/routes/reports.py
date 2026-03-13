from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user_model import User
from app.services.dashboard_service import (
    get_inventory_report,
    get_production_report,
    get_sales_report,
)


router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/sales")
def read_sales_report(
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    return get_sales_report(db, date_from=date_from, date_to=date_to)


@router.get("/inventory")
def read_inventory_report(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    return get_inventory_report(db)


@router.get("/productions")
def read_production_report(
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    return get_production_report(db, date_from=date_from, date_to=date_to)
