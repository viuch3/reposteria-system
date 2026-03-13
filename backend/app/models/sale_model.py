from datetime import date, time
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sale_date: Mapped[date] = mapped_column(Date, nullable=False)
    sale_time: Mapped[time] = mapped_column(Time, nullable=False)
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    sales_channel: Mapped[str | None] = mapped_column(String(50), nullable=True)
    notes: Mapped[str | None] = mapped_column(String(255), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    user = relationship("User", back_populates="sales")
    sale_details = relationship(
        "SaleDetail", back_populates="sale", cascade="all, delete-orphan"
    )
