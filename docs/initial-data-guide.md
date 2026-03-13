# Carga inicial y puesta en marcha

## Objetivo

Dejar el sistema listo para empezar a operar con usuarios, productos, insumos y recetas base.

## Requisitos previos

- PostgreSQL operativo
- migraciones aplicadas con Alembic
- archivo `backend/.env` configurado
- entorno virtual activo

## Ejecutar datos iniciales

Desde la raiz del proyecto:

```bash
source backend/venv/bin/activate
cd backend
python scripts/seed_data.py
```

## Usuarios de ejemplo

- `admin@reposteria.com`
- `ventas@reposteria.com`
- `produccion@reposteria.com`

Contrasena inicial de ejemplo:

```text
ClaveSegura123
```

## Que carga este script

- usuarios base por rol
- productos iniciales
- insumos iniciales
- recetas de ejemplo para productos

## Recomendacion despues de cargar

- iniciar sesion con el usuario admin
- revisar productos e insumos en frontend
- cambiar las contrasenas iniciales en entorno real
- ajustar stock, precios y recetas a la operacion real de la reposteria
