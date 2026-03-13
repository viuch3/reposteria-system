from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_active_user, require_roles
from app.models.user_model import User
from app.schemas.product_schema import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import (
    create_product,
    deactivate_product,
    get_product_by_id,
    list_products,
    update_product,
)


router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=list[ProductResponse])
def get_products(
    q: str | None = Query(default=None, description="Buscar por nombre o codigo."),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    return list_products(db, q)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_new_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
):
    return create_product(db, payload)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    product = get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado.",
        )
    return product


@router.get("/{product_id}/stock")
def get_product_stock(
    product_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
) -> dict[str, int | float | str]:
    product = get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado.",
        )
    return {
        "product_id": product.id,
        "code": product.code,
        "name": product.name,
        "current_stock": product.current_stock,
        "min_stock": product.min_stock,
        "max_stock": product.max_stock,
        "status": product.status,
    }


@router.patch("/{product_id}", response_model=ProductResponse)
def update_existing_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
):
    product = get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado.",
        )
    return update_product(db, product, payload)


@router.patch("/{product_id}/deactivate", response_model=ProductResponse)
def deactivate_existing_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin")),
):
    product = get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado.",
        )
    return deactivate_product(db, product)
