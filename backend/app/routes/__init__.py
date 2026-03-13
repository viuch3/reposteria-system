from fastapi import APIRouter

from app.routes.auth import router as auth_router
from app.routes.health import router as health_router
from app.routes.inventory import router as inventory_router
from app.routes.products import router as products_router
from app.routes.productions import router as productions_router
from app.routes.recipes import router as recipes_router
from app.routes.sales import router as sales_router
from app.routes.supplies import router as supplies_router
from app.routes.users import router as users_router


api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(health_router, prefix="/health", tags=["Health"])
api_router.include_router(inventory_router)
api_router.include_router(products_router)
api_router.include_router(productions_router)
api_router.include_router(recipes_router)
api_router.include_router(sales_router)
api_router.include_router(supplies_router)
api_router.include_router(users_router)
