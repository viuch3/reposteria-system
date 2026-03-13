# Configuracion de PostgreSQL

## Objetivo

Preparar la base de datos local para el sistema de reposteria y dejar lista la conexion desde el backend.

## Opcion recomendada para desarrollo

Usar PostgreSQL instalado localmente o mediante Docker. Para esta etapa, cualquiera de las dos opciones funciona siempre que puedas conectarte desde `DATABASE_URL`.

## Base de datos sugerida

```sql
CREATE DATABASE reposteria_db;
CREATE USER reposteria_user WITH PASSWORD 'tu_password_segura';
GRANT ALL PRIVILEGES ON DATABASE reposteria_db TO reposteria_user;
```

## Variables de entorno del backend

Crear el archivo `backend/.env` tomando como base `backend/.env.example`.

Contenido esperado:

```env
DATABASE_URL=postgresql://reposteria_user:tu_password_segura@localhost:5432/reposteria_db
SECRET_KEY=una_clave_secreta_larga
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Probar conexion desde Python

Con el entorno virtual activado:

```bash
cd backend
python test_db.py
```

Si todo esta bien configurado, el script debe responder con un mensaje de conexion exitosa.

## Resultado esperado de esta fase

- PostgreSQL instalado y operativo
- base de datos `reposteria_db` creada
- archivo `backend/.env` configurado localmente
- conexion validada con `backend/test_db.py`
