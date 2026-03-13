from fastapi.testclient import TestClient


def test_login_and_read_current_user(client: TestClient) -> None:
    bootstrap_response = client.post(
        "/api/v1/auth/bootstrap-admin",
        json={
            "name": "Admin Principal",
            "email": "admin@reposteria.com",
            "password": "ClaveSegura123",
            "role": "admin",
            "is_active": True,
        },
    )

    assert bootstrap_response.status_code == 201
    assert bootstrap_response.json()["role"] == "admin"

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "admin@reposteria.com",
            "password": "ClaveSegura123",
        },
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    assert token

    me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert me_response.status_code == 200
    assert me_response.json()["email"] == "admin@reposteria.com"
