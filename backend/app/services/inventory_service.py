from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inventory_movement_model import InventoryMovement
from app.models.product_model import Product
from app.models.supply_model import Supply
from app.models.user_model import User
from app.schemas.inventory_schema import InventoryMovementCreate


ALLOWED_MOVEMENT_TYPES = {"entrada", "salida", "merma"}


def list_inventory_movements(db: Session) -> list[InventoryMovement]:
    statement = select(InventoryMovement).order_by(InventoryMovement.movement_date.desc())
    return list(db.scalars(statement).all())


def _apply_stock_movement(
    current_stock: float,
    movement_type: str,
    quantity: float,
) -> float:
    if movement_type == "entrada":
        return current_stock + quantity
    if movement_type in {"salida", "merma"}:
        if current_stock < quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No hay stock suficiente para registrar este movimiento.",
            )
        return current_stock - quantity
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="movement_type debe ser entrada, salida o merma.",
    )


def create_inventory_movement(
    db: Session,
    payload: InventoryMovementCreate,
    user: User,
) -> InventoryMovement:
    movement_type = payload.movement_type.strip().lower()
    if movement_type not in ALLOWED_MOVEMENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="movement_type debe ser entrada, salida o merma.",
        )

    if payload.product_id is not None:
        product = db.get(Product, payload.product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado.",
            )
        product.current_stock = _apply_stock_movement(
            product.current_stock,
            movement_type,
            payload.quantity,
        )

    if payload.supply_id is not None:
        supply = db.get(Supply, payload.supply_id)
        if supply is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Insumo no encontrado.",
            )
        supply.current_stock = _apply_stock_movement(
            supply.current_stock,
            movement_type,
            payload.quantity,
        )

    movement = InventoryMovement(
        movement_type=movement_type,
        product_id=payload.product_id,
        supply_id=payload.supply_id,
        quantity=payload.quantity,
        reason=payload.reason,
        user_id=user.id,
    )
    db.add(movement)
    db.commit()
    db.refresh(movement)
    return movement
