from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product_model import Product
from app.models.recipe_detail_model import RecipeDetail
from app.models.supply_model import Supply
from app.schemas.recipe_schema import RecipeDetailCreate


def list_recipe_details(db: Session, product_id: int) -> list[RecipeDetail]:
    statement = (
        select(RecipeDetail)
        .where(RecipeDetail.product_id == product_id)
        .order_by(RecipeDetail.id.asc())
    )
    return list(db.scalars(statement).all())


def get_recipe_detail_by_id(db: Session, recipe_detail_id: int) -> RecipeDetail | None:
    return db.get(RecipeDetail, recipe_detail_id)


def create_recipe_detail(db: Session, payload: RecipeDetailCreate) -> RecipeDetail:
    product = db.get(Product, payload.product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado.",
        )

    supply = db.get(Supply, payload.supply_id)
    if supply is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Insumo no encontrado.",
        )

    existing_recipe_detail = db.scalar(
        select(RecipeDetail).where(
            RecipeDetail.product_id == payload.product_id,
            RecipeDetail.supply_id == payload.supply_id,
        )
    )
    if existing_recipe_detail is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ese insumo ya esta asociado a la receta del producto.",
        )

    recipe_detail = RecipeDetail(**payload.model_dump())
    db.add(recipe_detail)
    db.commit()
    db.refresh(recipe_detail)
    return recipe_detail


def update_recipe_detail_quantity(
    db: Session,
    recipe_detail: RecipeDetail,
    supply_quantity: float,
) -> RecipeDetail:
    recipe_detail.supply_quantity = supply_quantity
    db.add(recipe_detail)
    db.commit()
    db.refresh(recipe_detail)
    return recipe_detail


def delete_recipe_detail(db: Session, recipe_detail: RecipeDetail) -> None:
    db.delete(recipe_detail)
    db.commit()
