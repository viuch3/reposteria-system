from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_active_user, require_roles
from app.models.user_model import User
from app.schemas.production_schema import ProductionCreate, ProductionResponse
from app.services.production_service import create_production, list_productions


router = APIRouter(prefix="/productions", tags=["Productions"])


@router.get("/", response_model=list[ProductionResponse])
def get_productions(
    production_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    return list_productions(db, production_date=production_date)


@router.post("/", response_model=ProductionResponse, status_code=status.HTTP_201_CREATED)
def register_production(
    payload: ProductionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "produccion")),
):
    return create_production(db, payload, current_user)
