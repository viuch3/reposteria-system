from typing import Any

from pydantic import BaseModel, Field


class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Any | None = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: str | None = None
    details: Any | None = None


class ValidationErrorItem(BaseModel):
    field: str = Field(..., description="Campo que fallo en la validacion.")
    message: str = Field(..., description="Mensaje de validacion asociado.")


class ValidationErrorResponse(BaseModel):
    success: bool = False
    message: str = "Error de validacion"
    errors: list[ValidationErrorItem]


class NotFoundResponse(BaseModel):
    success: bool = False
    message: str = "Recurso no encontrado"
