from datetime import date

from pydantic import BaseModel, Field

from app.schemas.common import ORMBaseSchema


class WeatherRecordBase(BaseModel):
    weather_date: date
    temperature_c: float | None = None
    humidity: float | None = Field(default=None, ge=0, le=100)
    rainfall_mm: float | None = Field(default=None, ge=0)
    weather_description: str | None = Field(default=None, max_length=255)


class WeatherRecordCreate(WeatherRecordBase):
    pass


class WeatherRecordResponse(ORMBaseSchema):
    id: int
    weather_date: date
    temperature_c: float | None
    humidity: float | None
    rainfall_mm: float | None
    weather_description: str | None
