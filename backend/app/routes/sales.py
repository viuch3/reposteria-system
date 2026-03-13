from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_active_user, require_roles
from app.models.user_model import User
from app.schemas.sale_schema import SaleCreate, SaleResponse
from app.services.sale_service import create_sale, get_sale_by_id, list_sales


router = APIRouter(prefix="/sales", tags=["Sales"])


@router.get("/", response_model=list[SaleResponse])
def get_sales(
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    return list_sales(db, date_from=date_from, date_to=date_to)


@router.post("/", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def register_sale(
    payload: SaleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "vendedor")),
):
    return create_sale(db, payload, current_user)


@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    sale = get_sale_by_id(db, sale_id)
    if sale is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada.",
        )
    return sale
