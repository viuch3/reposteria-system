from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.inventory_movement_model import InventoryMovement
from app.models.product_model import Product
from app.models.production_model import Production
from app.models.sale_detail_model import SaleDetail
from app.models.sale_model import Sale
from app.models.supply_model import Supply


def _decimal_to_float(value: Decimal | None) -> float:
    if value is None:
        return 0.0
    return float(value)


def get_dashboard_summary(db: Session) -> dict:
    today = date.today()
    month_start = today.replace(day=1)

    sales_today = _decimal_to_float(
        db.scalar(select(func.sum(Sale.total)).where(Sale.sale_date == today))
    )
    sales_month = _decimal_to_float(
        db.scalar(select(func.sum(Sale.total)).where(Sale.sale_date >= month_start))
    )
    productions_today = db.scalar(
        select(func.count(Production.id)).where(Production.production_date == today)
    ) or 0
    low_stock_products = db.scalar(
        select(func.count(Product.id)).where(Product.current_stock <= Product.min_stock)
    ) or 0
    average_ticket = _decimal_to_float(
        db.scalar(
            select(func.avg(Sale.total)).where(Sale.sale_date == today)
        )
    )

    return {
      "sales_today": sales_today,
      "sales_month": sales_month,
      "productions_today": productions_today,
      "low_stock_products": low_stock_products,
      "average_ticket": average_ticket,
    }


def get_sales_last_days(db: Session, days: int = 7) -> list[dict]:
    start_date = date.today() - timedelta(days=days - 1)
    rows = db.execute(
        select(Sale.sale_date, func.sum(Sale.total))
        .where(Sale.sale_date >= start_date)
        .group_by(Sale.sale_date)
        .order_by(Sale.sale_date.asc())
    ).all()

    totals_by_date = {row[0]: _decimal_to_float(row[1]) for row in rows}
    return [
        {
            "date": (start_date + timedelta(days=index)).isoformat(),
            "total": totals_by_date.get(start_date + timedelta(days=index), 0.0),
        }
        for index in range(days)
    ]


def get_low_stock_items(db: Session) -> list[dict]:
    products = db.execute(
        select(Product.id, Product.name, Product.current_stock, Product.min_stock, Product.unit_of_measure)
        .where(Product.current_stock <= Product.min_stock)
        .order_by(Product.current_stock.asc())
        .limit(5)
    ).all()

    supplies = db.execute(
        select(Supply.id, Supply.name, Supply.current_stock, Supply.min_stock, Supply.unit_of_measure)
        .where(Supply.current_stock <= Supply.min_stock)
        .order_by(Supply.current_stock.asc())
        .limit(5)
    ).all()

    items = [
        {
            "type": "product",
            "id": row[0],
            "name": row[1],
            "current_stock": row[2],
            "min_stock": row[3],
            "unit_of_measure": row[4],
        }
        for row in products
    ] + [
        {
            "type": "supply",
            "id": row[0],
            "name": row[1],
            "current_stock": row[2],
            "min_stock": row[3],
            "unit_of_measure": row[4],
        }
        for row in supplies
    ]

    return items[:6]


def get_recent_sales(db: Session, limit: int = 5) -> list[dict]:
    rows = db.execute(
        select(Sale.id, Sale.sale_date, Sale.sale_time, Sale.total, Sale.sales_channel)
        .order_by(Sale.sale_date.desc(), Sale.sale_time.desc())
        .limit(limit)
    ).all()

    return [
        {
            "id": row[0],
            "sale_date": row[1].isoformat(),
            "sale_time": row[2].isoformat(),
            "total": _decimal_to_float(row[3]),
            "sales_channel": row[4] or "sin canal",
        }
        for row in rows
    ]


def get_top_products(db: Session, limit: int = 5) -> list[dict]:
    rows = db.execute(
        select(Product.name, func.sum(SaleDetail.quantity).label("quantity_sold"))
        .join(SaleDetail, SaleDetail.product_id == Product.id)
        .group_by(Product.name)
        .order_by(func.sum(SaleDetail.quantity).desc())
        .limit(limit)
    ).all()

    return [
        {"name": row[0], "quantity_sold": row[1]}
        for row in rows
    ]


def get_sales_report(
    db: Session,
    date_from: date | None = None,
    date_to: date | None = None,
) -> list[dict]:
    statement = select(Sale.id, Sale.sale_date, Sale.sale_time, Sale.total, Sale.sales_channel)
    if date_from is not None:
        statement = statement.where(Sale.sale_date >= date_from)
    if date_to is not None:
        statement = statement.where(Sale.sale_date <= date_to)
    statement = statement.order_by(Sale.sale_date.desc(), Sale.sale_time.desc())

    rows = db.execute(statement).all()
    return [
        {
            "id": row[0],
            "sale_date": row[1].isoformat(),
            "sale_time": row[2].isoformat(),
            "total": _decimal_to_float(row[3]),
            "sales_channel": row[4] or "sin canal",
        }
        for row in rows
    ]


def get_inventory_report(db: Session, limit: int = 20) -> list[dict]:
    rows = db.execute(
        select(
            InventoryMovement.id,
            InventoryMovement.movement_date,
            InventoryMovement.movement_type,
            InventoryMovement.product_id,
            InventoryMovement.supply_id,
            InventoryMovement.quantity,
            InventoryMovement.reason,
            InventoryMovement.user_id,
        )
        .order_by(InventoryMovement.movement_date.desc())
        .limit(limit)
    ).all()

    return [
        {
            "id": row[0],
            "movement_date": row[1].isoformat(),
            "movement_type": row[2],
            "product_id": row[3],
            "supply_id": row[4],
            "quantity": row[5],
            "reason": row[6],
            "user_id": row[7],
        }
        for row in rows
    ]


def get_production_report(
    db: Session,
    date_from: date | None = None,
    date_to: date | None = None,
) -> list[dict]:
    statement = select(
        Production.id,
        Production.product_id,
        Production.quantity_produced,
        Production.production_date,
        Production.batch,
        Production.expiration_date,
    )
    if date_from is not None:
        statement = statement.where(Production.production_date >= date_from)
    if date_to is not None:
        statement = statement.where(Production.production_date <= date_to)
    statement = statement.order_by(Production.production_date.desc(), Production.id.desc())

    rows = db.execute(statement).all()
    return [
        {
            "id": row[0],
            "product_id": row[1],
            "quantity_produced": row[2],
            "production_date": row[3].isoformat(),
            "batch": row[4],
            "expiration_date": row[5].isoformat() if row[5] else None,
        }
        for row in rows
    ]
