from datetime import date
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.product_model import Product
from app.models.sale_detail_model import SaleDetail
from app.models.sale_model import Sale
from app.models.user_model import User
from app.schemas.sale_schema import SaleCreate


def get_sale_by_id(db: Session, sale_id: int) -> Sale | None:
    statement = (
        select(Sale)
        .options(selectinload(Sale.sale_details))
        .where(Sale.id == sale_id)
    )
    return db.scalar(statement)


def list_sales(
    db: Session,
    date_from: date | None = None,
    date_to: date | None = None,
) -> list[Sale]:
    statement = select(Sale).options(selectinload(Sale.sale_details))

    if date_from is not None:
        statement = statement.where(Sale.sale_date >= date_from)
    if date_to is not None:
        statement = statement.where(Sale.sale_date <= date_to)

    statement = statement.order_by(Sale.sale_date.desc(), Sale.sale_time.desc())
    return list(db.scalars(statement).all())


def create_sale(db: Session, payload: SaleCreate, user: User) -> Sale:
    sale = Sale(
        sale_date=payload.sale_date,
        sale_time=payload.sale_time,
        total=Decimal("0.00"),
        sales_channel=payload.sales_channel,
        notes=payload.notes,
        user_id=user.id,
    )

    total = Decimal("0.00")

    for item in payload.details:
        product = db.get(Product, item.product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con id {item.product_id} no encontrado.",
            )
        if product.status != "activo":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El producto {product.name} no esta activo.",
            )
        if product.current_stock < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente para el producto {product.name}.",
            )

        subtotal = (item.unit_price * Decimal(str(item.quantity))).quantize(
            Decimal("0.01")
        )

        product.current_stock -= item.quantity
        sale.sale_details.append(
            SaleDetail(
                product_id=product.id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                subtotal=subtotal,
            )
        )
        total += subtotal

    sale.total = total.quantize(Decimal("0.01"))
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return get_sale_by_id(db, sale.id) or sale
