from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import os


def main() -> None:
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise SystemExit(
            "DATABASE_URL no esta definida. Crea backend/.env a partir de backend/.env.example."
        )

    engine = create_engine(database_url)

    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        value = result.scalar_one()
        print(f"Conexion exitosa a PostgreSQL. Resultado de prueba: {value}")


if __name__ == "__main__":
    main()
