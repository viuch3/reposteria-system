from datetime import date

from pydantic import BaseModel, Field, field_validator

from app.schemas.common import ORMBaseSchema


class ProductionBase(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity_produced: float = Field(..., gt=0)
    production_date: date
    batch: str = Field(..., min_length=1, max_length=100)
    expiration_date: date | None = None
    notes: str | None = Field(default=None, max_length=255)
    user_id: int = Field(..., gt=0)

    @field_validator("batch")
    @classmethod
    def validate_batch(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("El lote no puede estar vacio.")
        return value


class ProductionCreate(ProductionBase):
    pass


class ProductionResponse(ORMBaseSchema):
    id: int
    product_id: int
    quantity_produced: float
    production_date: date
    batch: str
    expiration_date: date | None
    notes: str | None
    user_id: int
