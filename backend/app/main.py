from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routes import api_router


app = FastAPI(
    title=settings.project_name,
    version=settings.project_version,
    description="API base para la gestion operativa del sistema de reposteria.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/", tags=["Root"])
def read_root() -> dict[str, str]:
    return {
        "message": "Reposteria System API en funcionamiento",
        "docs": "/docs",
        "api_base": settings.api_v1_prefix,
    }


@app.get("/health", tags=["Health"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
