from app import app


def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_version_endpoint():
    client = app.test_client()
    response = client.get("/version")

    assert response.status_code == 200
    assert "version" in response.get_json()

