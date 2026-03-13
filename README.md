# Reposteria System

Sistema web para la gestion operativa de una reposteria. El objetivo es registrar ventas, productos, insumos, produccion e inventario desde el dia 1, y dejar preparada la base tecnica para habilitar prediccion cuando exista suficiente historico.

## Estado actual

El proyecto se construira por fases para mantener entregables pequenos, claros y faciles de subir con `git push`.

En esta etapa ya existe la estructura base del proyecto, el entorno virtual inicial del backend y una aplicacion FastAPI arrancable.

## Roadmap de trabajo

1. Fase 0: documentacion inicial del MVP y stack tecnico.
2. Fase 1: estructura base del proyecto e inicializacion del repositorio.
3. Fase 2: configuracion de PostgreSQL y variables de entorno.
4. Fase 3: estructura profesional del backend y arranque de FastAPI.
5. Fase 4 en adelante: modelado de base de datos, frontend, reportes y despliegue.

## Documentacion

- [Alcance MVP](/Users/viuch3/Documents/reposteria-system/docs/mvp-scope.md)
- [Stack tecnico](/Users/viuch3/Documents/reposteria-system/docs/technical-stack.md)
- [Configuracion PostgreSQL](/Users/viuch3/Documents/reposteria-system/docs/postgresql-setup.md)

## Forma de trabajo

Cada fase debe cerrar con:

- entregable funcional o documentado
- validacion basica
- commit detallado
- `git push` antes de pasar a la siguiente fase

## Estructura actual

```text
reposteria-system/
├── backend/
│   ├── app/
│   ├── requirements.txt
│   ├── test_db.py
│   └── venv/
├── docs/
├── frontend/
├── .gitignore
└── README.md
```

## Como activar el entorno virtual

Desde la raiz del proyecto:

### macOS o Linux

```bash
source backend/venv/bin/activate
```

### Windows

```bash
backend\venv\Scripts\activate
```

## Como instalar dependencias

Si necesitas reconstruir el entorno desde cero:

```bash
python3 -m venv backend/venv
source backend/venv/bin/activate
pip install -r backend/requirements.txt
```

## Como levantar el backend

Desde la raiz del proyecto:

```bash
source backend/venv/bin/activate
cd backend
uvicorn app.main:app --reload
```

Rutas base disponibles despues de iniciar:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/api/v1/health/`
- `http://127.0.0.1:8000/docs`

## Configuracion de entorno

Antes de conectar la base de datos:

```bash
cp backend/.env.example backend/.env
```

Despues ajusta `DATABASE_URL` con tus credenciales reales y prueba la conexion:

```bash
cd backend
python test_db.py
```
