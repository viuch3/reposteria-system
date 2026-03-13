from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class InventoryMovement(Base):
    __tablename__ = "inventory_movements"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    movement_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    product_id: Mapped[int | None] = mapped_column(
        ForeignKey("products.id"), nullable=True, index=True
    )
    supply_id: Mapped[int | None] = mapped_column(
        ForeignKey("supplies.id"), nullable=True, index=True
    )
    quantity: Mapped[float] = mapped_column(nullable=False)
    reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    movement_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    product = relationship("Product", back_populates="inventory_movements")
    supply = relationship("Supply", back_populates="inventory_movements")
    user = relationship("User", back_populates="inventory_movements")
