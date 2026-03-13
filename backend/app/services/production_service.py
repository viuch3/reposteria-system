from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inventory_movement_model import InventoryMovement
from app.models.product_model import Product
from app.models.production_model import Production
from app.models.recipe_detail_model import RecipeDetail
from app.models.supply_model import Supply
from app.models.user_model import User
from app.schemas.production_schema import ProductionCreate


def list_productions(
    db: Session,
    production_date: date | None = None,
) -> list[Production]:
    statement = select(Production).order_by(
        Production.production_date.desc(),
        Production.id.desc(),
    )
    if production_date is not None:
        statement = statement.where(Production.production_date == production_date)
    return list(db.scalars(statement).all())


def create_production(db: Session, payload: ProductionCreate, user: User) -> Production:
    product = db.get(Product, payload.product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado.",
        )

    recipe_details = list(
        db.scalars(
            select(RecipeDetail).where(RecipeDetail.product_id == payload.product_id)
        ).all()
    )
    if not recipe_details:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El producto no tiene una receta configurada.",
        )

    for recipe_detail in recipe_details:
        supply = db.get(Supply, recipe_detail.supply_id)
        if supply is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Insumo con id {recipe_detail.supply_id} no encontrado.",
            )
        required_quantity = recipe_detail.supply_quantity * payload.quantity_produced
        if supply.current_stock < required_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insumos insuficientes para producir {product.name}.",
            )

    production = Production(
        product_id=payload.product_id,
        quantity_produced=payload.quantity_produced,
        production_date=payload.production_date,
        batch=payload.batch,
        expiration_date=payload.expiration_date,
        notes=payload.notes,
        user_id=user.id,
    )
    db.add(production)

    for recipe_detail in recipe_details:
        supply = db.get(Supply, recipe_detail.supply_id)
        required_quantity = recipe_detail.supply_quantity * payload.quantity_produced
        supply.current_stock -= required_quantity
        db.add(
            InventoryMovement(
                movement_type="salida",
                supply_id=supply.id,
                quantity=required_quantity,
                reason=f"Produccion de lote {payload.batch} para producto {product.name}",
                user_id=user.id,
            )
        )

    product.current_stock += payload.quantity_produced
    db.add(
        InventoryMovement(
            movement_type="entrada",
            product_id=product.id,
            quantity=payload.quantity_produced,
            reason=f"Ingreso por produccion de lote {payload.batch}",
            user_id=user.id,
        )
    )

    db.commit()
    db.refresh(production)
    return production
