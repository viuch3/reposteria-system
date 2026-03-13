# Reposteria System

Sistema web para la gestion operativa de una reposteria. El objetivo es registrar ventas, productos, insumos, produccion e inventario desde el dia 1, y dejar preparada la base tecnica para habilitar prediccion cuando exista suficiente historico.

## Estado actual

El proyecto se construira por fases para mantener entregables pequenos, claros y faciles de subir con `git push`.

En esta etapa ya existe la estructura base del proyecto y el entorno virtual inicial del backend.

## Roadmap de trabajo

1. Fase 0: documentacion inicial del MVP y stack tecnico.
2. Fase 1: estructura base del proyecto e inicializacion del repositorio.
3. Fase 2: configuracion de PostgreSQL y variables de entorno.
4. Fase 3 en adelante: backend, base de datos, frontend, reportes y despliegue.

## Documentacion

- [Alcance MVP](/Users/viuch3/Documents/reposteria-system/docs/mvp-scope.md)
- [Stack tecnico](/Users/viuch3/Documents/reposteria-system/docs/technical-stack.md)

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
│   ├── requirements.txt
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

La aplicacion FastAPI se creara en la siguiente fase. Cuando exista `backend/app/main.py`, el comando esperado sera:

```bash
source backend/venv/bin/activate
uvicorn app.main:app --reload
```
