from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class WeatherRecord(Base):
    __tablename__ = "weather_records"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    weather_date: Mapped[date] = mapped_column(Date, nullable=False, unique=True, index=True)
    temperature_c: Mapped[float | None] = mapped_column(nullable=True)
    humidity: Mapped[float | None] = mapped_column(nullable=True)
    rainfall_mm: Mapped[float | None] = mapped_column(nullable=True)
    weather_description: Mapped[str | None] = mapped_column(String(255), nullable=True)
