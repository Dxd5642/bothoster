from tests.conftest import client


async def test_root_endpoint(client):
    """Проверка эндпоинта /"""
    response = await client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}

async def test_health_endpoint(client):
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}