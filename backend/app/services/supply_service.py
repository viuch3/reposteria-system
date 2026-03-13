from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.supply_model import Supply
from app.schemas.supply_schema import SupplyCreate, SupplyUpdate


def get_supply_by_id(db: Session, supply_id: int) -> Supply | None:
    return db.get(Supply, supply_id)


def list_supplies(db: Session, low_stock_only: bool = False) -> list[Supply]:
    statement = select(Supply)
    if low_stock_only:
        statement = statement.where(Supply.current_stock <= Supply.min_stock)
    statement = statement.order_by(Supply.created_at.desc())
    return list(db.scalars(statement).all())


def create_supply(db: Session, payload: SupplyCreate) -> Supply:
    supply = Supply(**payload.model_dump())
    db.add(supply)
    db.commit()
    db.refresh(supply)
    return supply


def update_supply(db: Session, supply: Supply, payload: SupplyUpdate) -> Supply:
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(supply, field, value)

    db.add(supply)
    db.commit()
    db.refresh(supply)
    return supply


def update_supply_expiration(
    db: Session,
    supply: Supply,
    expiration_date: date | None,
) -> Supply:
    supply.expiration_date = expiration_date
    db.add(supply)
    db.commit()
    db.refresh(supply)
    return supply
