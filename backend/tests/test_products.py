from fastapi.testclient import TestClient


def test_create_product_as_admin(
    client: TestClient,
    admin_auth_headers: dict[str, str],
) -> None:
    response = client.post(
        "/api/v1/products/",
        headers=admin_auth_headers,
        json={
            "code": "TORTA-001",
            "name": "Torta de Chocolate",
            "description": "Torta clasica",
            "category": "tortas",
            "sale_price": "45.00",
            "cost_price": "25.00",
            "current_stock": 10,
            "min_stock": 2,
            "max_stock": 20,
            "unit_of_measure": "unidad",
            "status": "activo",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["code"] == "TORTA-001"
    assert body["name"] == "Torta de Chocolate"
