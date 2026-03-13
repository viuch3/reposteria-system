from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.product_model import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate


def get_product_by_id(db: Session, product_id: int) -> Product | None:
    return db.get(Product, product_id)


def get_product_by_code(db: Session, code: str) -> Product | None:
    return db.scalar(select(Product).where(Product.code == code))


def list_products(db: Session, query: str | None = None) -> list[Product]:
    statement = select(Product)
    if query:
        search = f"%{query.strip()}%"
        statement = statement.where(
            or_(Product.name.ilike(search), Product.code.ilike(search))
        )
    statement = statement.order_by(Product.created_at.desc())
    return list(db.scalars(statement).all())


def create_product(db: Session, payload: ProductCreate) -> Product:
    existing_product = get_product_by_code(db, payload.code)
    if existing_product is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un producto con ese codigo.",
        )

    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product: Product, payload: ProductUpdate) -> Product:
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(product, field, value)

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def deactivate_product(db: Session, product: Product) -> Product:
    product.status = "inactivo"
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
