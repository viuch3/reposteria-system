from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Production(Base):
    __tablename__ = "productions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), nullable=False, index=True
    )
    quantity_produced: Mapped[float] = mapped_column(nullable=False)
    production_date: Mapped[date] = mapped_column(Date, nullable=False)
    batch: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    expiration_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = mapped_column(String(255), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    product = relationship("Product", back_populates="productions")
    user = relationship("User", back_populates="productions")
