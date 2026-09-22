from tests.conftest import client
from random import randint

async def test_register_success(client):
    id_user = randint(1, 10000)
    response = await client.post(
        "/api/v1/auth/registration",
        json={
            "username": f"test{id_user}Username",
            "email": f"test{id_user}@example.com",
            "password": "StrongPassord123!"
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data['status'] == True

async def test_registr_dublicate(client):
    payload = {
        "username": "testDublicateUsername",
        "email": "testDublicate@example.com",
        "password": "StrongPassord123!"
    }

    first = await client.post("/api/v1/auth/registration", json=payload)
    second = await client.post("/api/v1/auth/registration", json=payload)

    assert first.status_code == 201
    assert second.status_code == 409

async def test_login_client_by_username(client):
    await client.post(
        "/api/v1/auth/registration",
        json={
            "username": "testLoginByUsername",
            "email": "testLoginByUsername@example.com",
            "password": "StrongPassord123!"
        },
    )

    response = await client.post(
        "/api/v1/auth/login",
        json={
            "login": "testLoginByUsername",
            "password": "StrongPassord123!",
        },
    )


    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "testLoginByUsername@example.com"
    assert "password" not in data
    assert "password_hash" not in data

    assert "session_id" in response.cookies

    cookies = response.cookies.get("session_id")
    assert cookies

    profile_response = await client.get('/api/v1/user/')

    assert profile_response.status_code == 200
    assert profile_response.json().get("user_username") == "testLoginByUsername"


async def test_login_client_by_email(client):
    await client.post(
        "/api/v1/auth/registration",
        json={
            "username": "testLoginByEmail",
            "email": "testLoginByEmail@example.com",
            "password": "StrongPassord123!"
        },
    )

    response = await client.post(
        "/api/v1/auth/login",
        json={
            "login": "testLoginByEmail@example.com",
            "password": "StrongPassord123!",
        },
    )


    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "testLoginByEmail"
    assert "password" not in data
    assert "password_hash" not in data

    assert "session_id" in response.cookies

    cookies = response.cookies.get("session_id")
    assert cookies

    profile_response = await client.get('/api/v1/user/')

    assert profile_response.status_code == 200
    assert profile_response.json().get("user_username") == "testLoginByEmail"

async def test_login_unclient(client):
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "login": "testLoginUsernameFalse",
            "password": "StrongPassord123!",
        },
    )

    assert response.status_code == 401

