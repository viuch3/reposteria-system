from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_active_user, require_roles
from app.models.user_model import User
from app.schemas.weather_schema import WeatherRecordCreate, WeatherRecordResponse
from app.services.weather_service import (
    create_weather_record,
    get_weather_record_by_id,
    list_weather_records,
)


router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("/", response_model=list[WeatherRecordResponse])
def get_weather_records(
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    return list_weather_records(db, date_from=date_from, date_to=date_to)


@router.post("/", response_model=WeatherRecordResponse, status_code=status.HTTP_201_CREATED)
def create_new_weather_record(
    payload: WeatherRecordCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "produccion")),
):
    return create_weather_record(db, payload)


@router.get("/{weather_record_id}", response_model=WeatherRecordResponse)
def get_weather_record(
    weather_record_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    weather_record = get_weather_record_by_id(db, weather_record_id)
    if weather_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de clima no encontrado.",
        )
    return weather_record
