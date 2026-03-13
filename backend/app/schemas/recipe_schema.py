from pydantic import BaseModel, Field

from app.schemas.common import ORMBaseSchema


class RecipeDetailBase(BaseModel):
    product_id: int = Field(..., gt=0)
    supply_id: int = Field(..., gt=0)
    supply_quantity: float = Field(..., gt=0)


class RecipeDetailCreate(RecipeDetailBase):
    pass


class RecipeDetailResponse(ORMBaseSchema):
    id: int
    product_id: int
    supply_id: int
    supply_quantity: float
