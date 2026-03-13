from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_active_user, require_roles
from app.models.user_model import User
from app.schemas.recipe_schema import RecipeDetailCreate, RecipeDetailResponse
from app.services.recipe_service import (
    create_recipe_detail,
    delete_recipe_detail,
    get_recipe_detail_by_id,
    list_recipe_details,
    update_recipe_detail_quantity,
)


router = APIRouter(prefix="/recipes", tags=["Recipes"])


class RecipeQuantityUpdate(BaseModel):
    supply_quantity: float = Field(..., gt=0)


@router.get("/products/{product_id}", response_model=list[RecipeDetailResponse])
def get_product_recipe(
    product_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    return list_recipe_details(db, product_id)


@router.post("/", response_model=RecipeDetailResponse, status_code=status.HTTP_201_CREATED)
def create_recipe_item(
    payload: RecipeDetailCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "produccion")),
):
    return create_recipe_detail(db, payload)


@router.patch("/{recipe_detail_id}", response_model=RecipeDetailResponse)
def update_recipe_item(
    recipe_detail_id: int,
    payload: RecipeQuantityUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "produccion")),
):
    recipe_detail = get_recipe_detail_by_id(db, recipe_detail_id)
    if recipe_detail is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Detalle de receta no encontrado.",
        )
    return update_recipe_detail_quantity(db, recipe_detail, payload.supply_quantity)


@router.delete("/{recipe_detail_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe_item(
    recipe_detail_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "produccion")),
):
    recipe_detail = get_recipe_detail_by_id(db, recipe_detail_id)
    if recipe_detail is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Detalle de receta no encontrado.",
        )
    delete_recipe_detail(db, recipe_detail)
