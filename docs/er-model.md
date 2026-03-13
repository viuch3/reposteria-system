# Modelo entidad-relacion inicial

## Objetivo

Definir la estructura minima de datos para soportar usuarios, productos, insumos, ventas, inventario, produccion, recetas y registros de clima.

## Entidades principales

- `users`: usuarios del sistema con rol y estado.
- `products`: catalogo de productos terminados.
- `supplies`: insumos usados en produccion.
- `sales`: encabezado de ventas registradas por usuario.
- `sale_details`: detalle de productos vendidos por venta.
- `inventory_movements`: auditoria de entradas, salidas y mermas sobre productos o insumos.
- `productions`: lotes producidos por producto y usuario.
- `recipe_details`: relacion entre producto e insumo para definir recetas.
- `weather_records`: tabla preparada para registrar clima manual por fecha.

## Relaciones clave

- Un `user` puede registrar muchas `sales`.
- Un `user` puede registrar muchos `inventory_movements`.
- Un `user` puede registrar muchas `productions`.
- Una `sale` tiene muchos `sale_details`.
- Un `product` puede aparecer en muchos `sale_details`.
- Un `product` puede tener muchas `productions`.
- Un `product` puede tener muchos `recipe_details`.
- Un `supply` puede aparecer en muchos `recipe_details`.
- Un `product` o un `supply` puede participar en `inventory_movements`.

## Reglas de modelado inicial

- Correos de usuario unicos.
- Codigo de producto unico.
- Cantidades y precios no negativos.
- `inventory_movements` permite apuntar a producto o insumo, pero no exige ambos.
- Las recetas se modelan como detalle por producto e insumo.
- El clima se deja desacoplado para futura correlacion con ventas.

## Diagrama

```mermaid
erDiagram
    users ||--o{ sales : registers
    users ||--o{ inventory_movements : performs
    users ||--o{ productions : records
    sales ||--|{ sale_details : contains
    products ||--o{ sale_details : sold_in
    products ||--o{ inventory_movements : affects
    supplies ||--o{ inventory_movements : affects
    products ||--o{ productions : produced_as
    products ||--o{ recipe_details : has
    supplies ||--o{ recipe_details : uses

    users {
        int id PK
        string name
        string email UK
        string password_hash
        string role
        boolean is_active
        datetime created_at
    }

    products {
        int id PK
        string code UK
        string name
        string description
        string category
        decimal sale_price
        decimal cost_price
        float current_stock
        float min_stock
        float max_stock
        string unit_of_measure
        string status
        datetime created_at
    }

    supplies {
        int id PK
        string name
        string category
        float current_stock
        float min_stock
        float max_stock
        string unit_of_measure
        decimal unit_cost
        string supplier
        date expiration_date
        datetime created_at
    }

    sales {
        int id PK
        date sale_date
        time sale_time
        decimal total
        string sales_channel
        string notes
        int user_id FK
    }

    sale_details {
        int id PK
        int sale_id FK
        int product_id FK
        float quantity
        decimal unit_price
        decimal subtotal
    }

    inventory_movements {
        int id PK
        string movement_type
        int product_id FK
        int supply_id FK
        float quantity
        string reason
        datetime movement_date
        int user_id FK
    }

    productions {
        int id PK
        int product_id FK
        float quantity_produced
        date production_date
        string batch
        date expiration_date
        string notes
        int user_id FK
    }

    recipe_details {
        int id PK
        int product_id FK
        int supply_id FK
        float supply_quantity
    }

    weather_records {
        int id PK
        date weather_date
        float temperature_c
        float humidity
        float rainfall_mm
        string weather_description
    }
```
