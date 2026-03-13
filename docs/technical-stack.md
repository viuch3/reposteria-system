# Stack tecnico propuesto

## Backend

- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pydantic
- Uvicorn
- python-dotenv
- passlib con bcrypt
- python-jose para JWT

## Frontend

- HTML
- CSS
- JavaScript
- Bootstrap o CSS propio segun evolucione la interfaz
- Chart.js para graficas

## Utilidades de desarrollo

- Git
- GitHub
- Postman o Insomnia
- pgAdmin o DBeaver
- Visual Studio Code

## Criterios de seleccion

- FastAPI permite construir una API clara, rapida y con documentacion automatica
- PostgreSQL ofrece una base robusta para inventario, ventas y trazabilidad
- SQLAlchemy y Alembic facilitan modelado y control de cambios en base de datos
- Pydantic ayuda a validar entradas y respuestas desde etapas tempranas
- HTML, CSS y JavaScript permiten construir un frontend ligero y controlado
- Chart.js cubre el dashboard inicial sin complejidad innecesaria

## Decision inicial

Se adopta una arquitectura separada por carpetas:

- `backend/` para API, modelos, migraciones y logica de negocio
- `frontend/` para interfaz web
- `docs/` para alcance, decisiones tecnicas y documentacion funcional

## Consideraciones futuras

- La prediccion quedara desacoplada para habilitarse cuando exista historico suficiente
- El frontend puede mantenerse estatico al inicio y evolucionar despues si el proyecto lo necesita
- El despliegue puede resolverse mas adelante con Render, Railway, VPS o una integracion propia
