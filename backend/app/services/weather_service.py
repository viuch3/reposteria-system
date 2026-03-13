from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.weather_record_model import WeatherRecord
from app.schemas.weather_schema import WeatherRecordCreate


def get_weather_record_by_id(db: Session, weather_record_id: int) -> WeatherRecord | None:
    return db.get(WeatherRecord, weather_record_id)


def get_weather_record_by_date(db: Session, weather_date: date) -> WeatherRecord | None:
    return db.scalar(
        select(WeatherRecord).where(WeatherRecord.weather_date == weather_date)
    )


def list_weather_records(
    db: Session,
    date_from: date | None = None,
    date_to: date | None = None,
) -> list[WeatherRecord]:
    statement = select(WeatherRecord)
    if date_from is not None:
        statement = statement.where(WeatherRecord.weather_date >= date_from)
    if date_to is not None:
        statement = statement.where(WeatherRecord.weather_date <= date_to)
    statement = statement.order_by(WeatherRecord.weather_date.desc())
    return list(db.scalars(statement).all())


def create_weather_record(db: Session, payload: WeatherRecordCreate) -> WeatherRecord:
    existing_record = get_weather_record_by_date(db, payload.weather_date)
    if existing_record is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un registro de clima para esa fecha.",
        )

    weather_record = WeatherRecord(**payload.model_dump())
    db.add(weather_record)
    db.commit()
    db.refresh(weather_record)
    return weather_record
