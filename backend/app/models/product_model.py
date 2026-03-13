from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    sale_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    cost_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    current_stock: Mapped[float] = mapped_column(nullable=False, default=0)
    min_stock: Mapped[float] = mapped_column(nullable=False, default=0)
    max_stock: Mapped[float] = mapped_column(nullable=False, default=0)
    unit_of_measure: Mapped[str] = mapped_column(String(30), nullable=False, default="unidad")
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="activo")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    sale_details = relationship("SaleDetail", back_populates="product")
    inventory_movements = relationship("InventoryMovement", back_populates="product")
    productions = relationship("Production", back_populates="product")
    recipe_details = relationship("RecipeDetail", back_populates="product")
