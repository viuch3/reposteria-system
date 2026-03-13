from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class RecipeDetail(Base):
    __tablename__ = "recipe_details"
    __table_args__ = (
        UniqueConstraint("product_id", "supply_id", name="uq_recipe_product_supply"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), nullable=False, index=True
    )
    supply_id: Mapped[int] = mapped_column(
        ForeignKey("supplies.id"), nullable=False, index=True
    )
    supply_quantity: Mapped[float] = mapped_column(nullable=False)

    product = relationship("Product", back_populates="recipe_details")
    supply = relationship("Supply", back_populates="recipe_details")
