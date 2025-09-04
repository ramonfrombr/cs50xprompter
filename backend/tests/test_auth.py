import jwt
from datetime import datetime, timedelta, timezone
from app.models import User
from app.auth import SECRET_KEY


def test_register_success(client, session):
    response = client.post("/auth/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "secret"
    })
    assert response.status_code == 200
    assert response.get_json()["message"] == "User registered successfully"

    user = User.query.filter_by(username="alice").first()
    assert user is not None
    assert user.check_password("secret")


def test_register_duplicate_username(client, session):
    user = User(username="bob", email="bob@example.com")
    user.set_password("test")
    session.add(user)
    session.commit()

    response = client.post("/auth/register", json={
        "username": "bob",
        "email": "new@example.com",
        "password": "1234"
    })
    assert response.status_code == 400
    assert "Username already exists" in response.get_json()["error"]


def test_register_duplicate_email(client, session):
    user = User(username="carol", email="carol@example.com")
    user.set_password("test")
    session.add(user)
    session.commit()

    response = client.post("/auth/register", json={
        "username": "newcarol",
        "email": "carol@example.com",
        "password": "1234"
    })
    assert response.status_code == 400
    assert "Email already exists" in response.get_json()["error"]


def test_login_success(client, session):
    user = User(username="dave", email="dave@example.com")
    user.set_password("mypassword")
    session.add(user)
    session.commit()

    response = client.post("/auth/login", json={
        "username": "dave",
        "password": "mypassword"
    })
    assert response.status_code == 200
    token = response.get_json()["token"]
    assert token is not None

    # decode token to check payload
    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    assert decoded["user_id"] == user.id


def test_login_invalid_credentials(client):
    response = client.post("/auth/login", json={
        "username": "ghost",
        "password": "wrong",
    })
    assert response.status_code == 401
    assert "Invalid username or password" in response.get_json()["error"]


def test_protected_with_valid_token(client, session):
    user = User(username="erin", email="erin@example.com")
    user.set_password("pass")
    session.add(user)
    session.commit()

    # issua a valid token
    exp = datetime.now(timezone.utc) + timedelta(hours=1)
    payload = {"user_id": user.id, "exp": int(exp.timestamp())}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    response = client.get(
        "/auth/protected", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert f"Hello {user.username}" in response.get_json()["message"]


def test_protected_missing_token(client):
    response = client.get("/auth/protected")
    assert response.status_code == 401
    assert "Token is missing" in response.get_json()["error"]


def test_protected_invalid_token(client):
    response = client.get(
        "/auth/protected", headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 401
    assert "Token is invalid" in response.get_json()["error"]


def test_protected_token_expired(client, session):
    user = User(username="frank", email="frank@example.com")
    user.set_password("pw")
    session.add(user)
    session.commit()

    exp = datetime.now(timezone.utc) - timedelta(hours=1)
    payload = {"user_id": user.id, "exp": int(exp.timestamp())}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    response = client.get(
        "/auth/protected", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert "Token has expired" in response.get_json()["error"]
