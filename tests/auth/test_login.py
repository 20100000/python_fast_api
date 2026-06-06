import pytest
from fastapi import status
from app.api.users.models import User as UserModel
from passlib.context import CryptContext
from app.auth.security import hash_password

@pytest.fixture
def create_user_login(db_session):
    newUser = UserModel(
        name="User Teste Login",
        email="login@teste.com",
        password=hash_password("tiago123")
    )
    db_session.add(newUser)
    db_session.commit()
    db_session.refresh(newUser)
    return newUser


# Happy
def test_login_sucess(client, create_user_login):
    form_data = {
        "username": "login@teste.com",
        "password": "tiago123"
    }

    response = client.post("/auth/login", data=form_data)

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    assert "access_token" in response_data
    assert "user" in response_data
    assert response_data["token_type"] == "bearer"

    assert "user" in response_data
    assert response_data["user"]["email"] == "login@teste.com"
    assert "password" not in response_data["user"]


#Sad
def test_login_incorrect_password(client):
    form_data = {
        "username": "login@teste.com",
        "password": "senha_errada"
    }

    response = client.post("/auth/login", data=form_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "E-mail ou senha incorretos"

def test_login_incorrect_email_not_exists(client):
    form_data = {
        "username": "nao_existo@teste.com",
        "password": "qualquer_senha"
    }

    response = client.post("/auth/login", data=form_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "E-mail ou senha incorretos"
