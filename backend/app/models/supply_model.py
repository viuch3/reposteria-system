from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Supply(Base):
    __tablename__ = "supplies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    current_stock: Mapped[float] = mapped_column(nullable=False, default=0)
    min_stock: Mapped[float] = mapped_column(nullable=False, default=0)
    max_stock: Mapped[float] = mapped_column(nullable=False, default=0)
    unit_of_measure: Mapped[str] = mapped_column(String(30), nullable=False, default="unidad")
    unit_cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    supplier: Mapped[str | None] = mapped_column(String(120), nullable=True)
    expiration_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    inventory_movements = relationship("InventoryMovement", back_populates="supply")
    recipe_details = relationship("RecipeDetail", back_populates="supply")
