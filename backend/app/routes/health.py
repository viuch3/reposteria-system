from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def api_healthcheck() -> dict[str, str]:
    return {"status": "ok", "service": "reposteria-system"}
