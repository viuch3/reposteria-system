from dataclasses import dataclass, field
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    project_name: str = "Reposteria System API"
    project_version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://reposteria_user:tu_password_segura@localhost:5432/reposteria_db",
    )
    secret_key: str = os.getenv("SECRET_KEY", "change-me")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )
    allowed_origins: list[str] = field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5500",
            "http://127.0.0.1:5500",
        ]
    )


settings = Settings()
