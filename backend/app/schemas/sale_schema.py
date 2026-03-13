from datetime import date, time
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator, model_validator

from app.schemas.common import ORMBaseSchema


class SaleDetailBase(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: float = Field(..., gt=0)
    unit_price: Decimal = Field(..., gt=0)


class SaleDetailCreate(SaleDetailBase):
    pass


class SaleDetailResponse(ORMBaseSchema):
    id: int
    product_id: int
    quantity: float
    unit_price: Decimal
    subtotal: Decimal


class SaleBase(BaseModel):
    sale_date: date
    sale_time: time
    sales_channel: str | None = Field(default=None, max_length=50)
    notes: str | None = Field(default=None, max_length=255)

    @field_validator("sales_channel", "notes")
    @classmethod
    def normalize_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        return value or None


class SaleCreate(SaleBase):
    details: list[SaleDetailCreate] = Field(..., min_length=1)

    @model_validator(mode="after")
    def validate_details(self) -> "SaleCreate":
        if not self.details:
            raise ValueError("La venta debe incluir al menos un producto.")
        return self


class SaleResponse(ORMBaseSchema):
    id: int
    sale_date: date
    sale_time: time
    total: Decimal
    sales_channel: str | None
    notes: str | None
    user_id: int
    sale_details: list[SaleDetailResponse] = []
