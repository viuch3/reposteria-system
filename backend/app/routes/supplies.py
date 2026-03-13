from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_active_user, require_roles
from app.models.user_model import User
from app.schemas.supply_schema import SupplyCreate, SupplyResponse, SupplyUpdate
from app.services.supply_service import (
    create_supply,
    get_supply_by_id,
    list_supplies,
    update_supply,
    update_supply_expiration,
)


router = APIRouter(prefix="/supplies", tags=["Supplies"])


class SupplyExpirationUpdate(BaseModel):
    expiration_date: date | None = None


@router.get("/", response_model=list[SupplyResponse])
def get_supplies(
    low_stock: bool = Query(default=False, description="Filtrar insumos con stock bajo."),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    return list_supplies(db, low_stock_only=low_stock)


@router.get("/low-stock", response_model=list[SupplyResponse])
def get_low_stock_supplies(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    return list_supplies(db, low_stock_only=True)


@router.post("/", response_model=SupplyResponse, status_code=status.HTTP_201_CREATED)
def create_new_supply(
    payload: SupplyCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
):
    return create_supply(db, payload)


@router.get("/{supply_id}", response_model=SupplyResponse)
def get_supply(
    supply_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    supply = get_supply_by_id(db, supply_id)
    if supply is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insumo no encontrado.",
        )
    return supply


@router.patch("/{supply_id}", response_model=SupplyResponse)
def update_existing_supply(
    supply_id: int,
    payload: SupplyUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
):
    supply = get_supply_by_id(db, supply_id)
    if supply is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insumo no encontrado.",
        )
    return update_supply(db, supply, payload)


@router.patch("/{supply_id}/expiration", response_model=SupplyResponse)
def update_supply_expiration_date(
    supply_id: int,
    payload: SupplyExpirationUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
):
    supply = get_supply_by_id(db, supply_id)
    if supply is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insumo no encontrado.",
        )
    return update_supply_expiration(db, supply, payload.expiration_date)
