from datetime import date
from decimal import Decimal
from pathlib import Path
import sys

from sqlalchemy import select

sys.path.append(str(Path(__file__).resolve().parents[1]))

import app.models
from app.core.security import get_password_hash
from app.db.database import SessionLocal
from app.models.product_model import Product
from app.models.recipe_detail_model import RecipeDetail
from app.models.supply_model import Supply
from app.models.user_model import User


def ensure_user(session, name, email, password, role):
    user = session.scalar(select(User).where(User.email == email))
    if user:
        return user

    user = User(
        name=name,
        email=email,
        password_hash=get_password_hash(password),
        role=role,
        is_active=True,
    )
    session.add(user)
    session.flush()
    return user


def ensure_product(session, **data):
    product = session.scalar(select(Product).where(Product.code == data["code"]))
    if product:
        return product

    product = Product(**data)
    session.add(product)
    session.flush()
    return product


def ensure_supply(session, name, **data):
    supply = session.scalar(select(Supply).where(Supply.name == name))
    if supply:
        return supply

    supply = Supply(name=name, **data)
    session.add(supply)
    session.flush()
    return supply


def ensure_recipe_detail(session, product_id, supply_id, supply_quantity):
    recipe_detail = session.scalar(
        select(RecipeDetail).where(
            RecipeDetail.product_id == product_id,
            RecipeDetail.supply_id == supply_id,
        )
    )
    if recipe_detail:
        return recipe_detail

    recipe_detail = RecipeDetail(
        product_id=product_id,
        supply_id=supply_id,
        supply_quantity=supply_quantity,
    )
    session.add(recipe_detail)
    session.flush()
    return recipe_detail


def main():
    session = SessionLocal()
    try:
        ensure_user(
            session,
            name="Admin Principal",
            email="admin@reposteria.com",
            password="ClaveSegura123",
            role="admin",
        )
        ensure_user(
            session,
            name="Caja Mostrador",
            email="ventas@reposteria.com",
            password="ClaveSegura123",
            role="vendedor",
        )
        ensure_user(
            session,
            name="Produccion Obrador",
            email="produccion@reposteria.com",
            password="ClaveSegura123",
            role="produccion",
        )

        torta = ensure_product(
            session,
            code="TORTA-001",
            name="Torta de Chocolate",
            description="Torta clasica para vitrina",
            category="Tortas",
            sale_price=Decimal("45000.00"),
            cost_price=Decimal("28000.00"),
            current_stock=4,
            min_stock=2,
            max_stock=12,
            unit_of_measure="unidad",
            status="activo",
        )
        brownie = ensure_product(
            session,
            code="BROWNIE-001",
            name="Brownie x6",
            description="Caja de brownies",
            category="Brownies",
            sale_price=Decimal("18000.00"),
            cost_price=Decimal("9000.00"),
            current_stock=8,
            min_stock=3,
            max_stock=20,
            unit_of_measure="unidad",
            status="activo",
        )

        harina = ensure_supply(
            session,
            name="Harina premium",
            category="Secos",
            current_stock=12,
            min_stock=5,
            max_stock=25,
            unit_of_measure="kg",
            unit_cost=Decimal("4500.00"),
            supplier="Molinos del Valle",
            expiration_date=date(2026, 6, 30),
        )
        chocolate = ensure_supply(
            session,
            name="Chocolate 70%",
            category="Reposteria",
            current_stock=6,
            min_stock=3,
            max_stock=15,
            unit_of_measure="kg",
            unit_cost=Decimal("19000.00"),
            supplier="Cacao House",
            expiration_date=date(2026, 5, 30),
        )
        huevos = ensure_supply(
            session,
            name="Huevos",
            category="Frescos",
            current_stock=90,
            min_stock=30,
            max_stock=180,
            unit_of_measure="unidad",
            unit_cost=Decimal("650.00"),
            supplier="Granja Santa Ana",
            expiration_date=date(2026, 3, 25),
        )

        ensure_recipe_detail(session, torta.id, harina.id, 1.5)
        ensure_recipe_detail(session, torta.id, chocolate.id, 1.0)
        ensure_recipe_detail(session, torta.id, huevos.id, 12)
        ensure_recipe_detail(session, brownie.id, harina.id, 0.8)
        ensure_recipe_detail(session, brownie.id, chocolate.id, 0.6)
        ensure_recipe_detail(session, brownie.id, huevos.id, 6)

        session.commit()
        print("Datos iniciales cargados correctamente.")
        print("Usuarios ejemplo: admin@reposteria.com, ventas@reposteria.com, produccion@reposteria.com")
        print("Contrasena inicial sugerida: ClaveSegura123")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
