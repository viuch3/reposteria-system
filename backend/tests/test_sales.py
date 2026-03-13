from fastapi.testclient import TestClient


def create_product(client: TestClient, headers: dict[str, str], stock: int) -> int:
    response = client.post(
        "/api/v1/products/",
        headers=headers,
        json={
            "code": f"PAN-{stock}",
            "name": "Pan de Banano",
            "description": "Producto de prueba",
            "category": "panaderia",
            "sale_price": "12.50",
            "cost_price": "5.00",
            "current_stock": stock,
            "min_stock": 1,
            "max_stock": 50,
            "unit_of_measure": "unidad",
            "status": "activo",
        },
    )
    return response.json()["id"]


def test_register_sale_discounts_product_stock(
    client: TestClient,
    admin_auth_headers: dict[str, str],
) -> None:
    product_id = create_product(client, admin_auth_headers, stock=10)

    sale_response = client.post(
        "/api/v1/sales/",
        headers=admin_auth_headers,
        json={
            "sale_date": "2026-03-12",
            "sale_time": "10:30:00",
            "sales_channel": "mostrador",
            "notes": "venta de prueba",
            "details": [
                {
                    "product_id": product_id,
                    "quantity": 2,
                    "unit_price": "12.50",
                }
            ],
        },
    )

    assert sale_response.status_code == 201
    body = sale_response.json()
    assert body["total"] == "25.00"
    assert body["sale_details"][0]["subtotal"] == "25.00"

    stock_response = client.get(
        f"/api/v1/products/{product_id}/stock",
        headers=admin_auth_headers,
    )

    assert stock_response.status_code == 200
    assert stock_response.json()["current_stock"] == 8


def test_sale_fails_when_product_has_insufficient_stock(
    client: TestClient,
    admin_auth_headers: dict[str, str],
) -> None:
    product_id = create_product(client, admin_auth_headers, stock=1)

    sale_response = client.post(
        "/api/v1/sales/",
        headers=admin_auth_headers,
        json={
            "sale_date": "2026-03-12",
            "sale_time": "11:00:00",
            "sales_channel": "mostrador",
            "details": [
                {
                    "product_id": product_id,
                    "quantity": 3,
                    "unit_price": "12.50",
                }
            ],
        },
    )

    assert sale_response.status_code == 400
    assert "Stock insuficiente" in sale_response.json()["detail"]
