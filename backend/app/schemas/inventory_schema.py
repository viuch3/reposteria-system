from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from app.schemas.common import ORMBaseSchema


class InventoryMovementBase(BaseModel):
    movement_type: str = Field(..., min_length=1, max_length=50)
    product_id: int | None = Field(default=None, gt=0)
    supply_id: int | None = Field(default=None, gt=0)
    quantity: float = Field(..., gt=0)
    reason: str | None = Field(default=None, max_length=255)

    @model_validator(mode="after")
    def validate_target(self) -> "InventoryMovementBase":
        if self.product_id and self.supply_id:
            raise ValueError("El movimiento debe apuntar a producto o insumo, no a ambos.")
        if not self.product_id and not self.supply_id:
            raise ValueError("El movimiento debe apuntar a un producto o a un insumo.")
        return self


class InventoryMovementCreate(InventoryMovementBase):
    pass


class InventoryMovementResponse(ORMBaseSchema):
    id: int
    movement_type: str
    product_id: int | None
    supply_id: int | None
    quantity: float
    reason: str | None
    movement_date: datetime
    user_id: int
