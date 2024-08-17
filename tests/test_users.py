import pytest
import jwt
from app import schemas
from app.config import settings


def test_create_user(client):
    res = client.post("/users/", json={"email": "cokkancs@cokkancs.hu",
                                       "password": "Cokkancs123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "cokkancs@cokkancs.hu"
    assert res.status_code == 201


def test_login_user(test_user, client):
    res = client.post("/login", data={"username": test_user['email'],
                                      "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code, expected_detail", [
    ('wrongemail@gmail.com', 'Cokkancs123', 403, 'Invalid credentials'),
    ('sanjeev@gmail.com', 'wrongpassword', 403, 'Invalid credentials'),
    ('wrongemail@gmail.com', 'wrongpassword', 403, 'Invalid credentials'),
    (None, 'password123', 422, 'Field required'),
    ('cokkancs@cokkancs.hu', None, 422, 'Field required')
])
def test_incorrect_login(test_user, client, email, password, status_code, expected_detail):
    res = client.post("/login", data={'username': email, 'password': password})

    assert res.status_code == status_code
    if status_code == 403:
        assert res.json().get('detail') == 'Invalid credentials'
    elif status_code == 422:
        assert res.json()['detail'][0]['msg'] == expected_detail
