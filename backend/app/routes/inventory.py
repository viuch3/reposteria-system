from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_active_user, require_roles
from app.models.user_model import User
from app.schemas.inventory_schema import (
    InventoryMovementCreate,
    InventoryMovementResponse,
)
from app.services.inventory_service import (
    create_inventory_movement,
    list_inventory_movements,
)


router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.get("/movements", response_model=list[InventoryMovementResponse])
def get_inventory_movements(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    return list_inventory_movements(db)


@router.post("/movements", response_model=InventoryMovementResponse, status_code=status.HTTP_201_CREATED)
def register_inventory_movement(
    payload: InventoryMovementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "produccion")),
):
    return create_inventory_movement(db, payload, current_user)
