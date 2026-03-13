from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator, model_validator

from app.schemas.common import ORMBaseSchema


class ProductBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=255)
    category: str | None = Field(default=None, max_length=100)
    sale_price: Decimal = Field(..., gt=0)
    cost_price: Decimal = Field(..., ge=0)
    current_stock: float = Field(default=0, ge=0)
    min_stock: float = Field(default=0, ge=0)
    max_stock: float = Field(default=0, ge=0)
    unit_of_measure: str = Field(default="unidad", min_length=1, max_length=30)
    status: str = Field(default="activo", min_length=1, max_length=30)

    @field_validator("code", "name", "unit_of_measure", "status")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Este campo no puede estar vacio.")
        return value

    @field_validator("category", "description")
    @classmethod
    def normalize_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        return value or None

    @model_validator(mode="after")
    def validate_stock_limits(self) -> "ProductBase":
        if self.max_stock and self.max_stock < self.min_stock:
            raise ValueError("stock_maximo no puede ser menor que stock_minimo.")
        return self


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=255)
    category: str | None = Field(default=None, max_length=100)
    sale_price: Decimal | None = Field(default=None, gt=0)
    cost_price: Decimal | None = Field(default=None, ge=0)
    current_stock: float | None = Field(default=None, ge=0)
    min_stock: float | None = Field(default=None, ge=0)
    max_stock: float | None = Field(default=None, ge=0)
    unit_of_measure: str | None = Field(default=None, min_length=1, max_length=30)
    status: str | None = Field(default=None, min_length=1, max_length=30)


class ProductResponse(ORMBaseSchema):
    id: int
    code: str
    name: str
    description: str | None
    category: str | None
    sale_price: Decimal
    cost_price: Decimal
    current_stock: float
    min_stock: float
    max_stock: float
    unit_of_measure: str
    status: str
    created_at: datetime
