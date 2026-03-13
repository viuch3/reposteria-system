from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator, model_validator

from app.schemas.common import ORMBaseSchema


class SupplyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    category: str | None = Field(default=None, max_length=100)
    current_stock: float = Field(default=0, ge=0)
    min_stock: float = Field(default=0, ge=0)
    max_stock: float = Field(default=0, ge=0)
    unit_of_measure: str = Field(default="unidad", min_length=1, max_length=30)
    unit_cost: Decimal = Field(..., ge=0)
    supplier: str | None = Field(default=None, max_length=120)
    expiration_date: date | None = None

    @field_validator("name", "unit_of_measure")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Este campo no puede estar vacio.")
        return value

    @field_validator("category", "supplier")
    @classmethod
    def normalize_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        return value or None

    @model_validator(mode="after")
    def validate_stock_limits(self) -> "SupplyBase":
        if self.max_stock and self.max_stock < self.min_stock:
            raise ValueError("stock_maximo no puede ser menor que stock_minimo.")
        return self


class SupplyCreate(SupplyBase):
    pass


class SupplyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    category: str | None = Field(default=None, max_length=100)
    current_stock: float | None = Field(default=None, ge=0)
    min_stock: float | None = Field(default=None, ge=0)
    max_stock: float | None = Field(default=None, ge=0)
    unit_of_measure: str | None = Field(default=None, min_length=1, max_length=30)
    unit_cost: Decimal | None = Field(default=None, ge=0)
    supplier: str | None = Field(default=None, max_length=120)
    expiration_date: date | None = None


class SupplyResponse(ORMBaseSchema):
    id: int
    name: str
    category: str | None
    current_stock: float
    min_stock: float
    max_stock: float
    unit_of_measure: str
    unit_cost: Decimal
    supplier: str | None
    expiration_date: date | None
    created_at: datetime
