import pytest
from app.users import models
#Happy
def test_create_user_success(client):
    """Testa a criação de um usuário com dados válidos."""
    payload = {
        "name": "João Silva",
        "email": "joao@example.com",
        "password": "senha_segura_123"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert "id" in data
#Sad
def test_create_user_email_already_exists(client, db_session):
    """Testa o bloqueio de cadastro para e-mails já existentes."""
    existing_user = models.User(name="Ana", email="ana@example.com", password="123")
    db_session.add(existing_user)
    db_session.commit()

    payload = {
        "name": "Ana Maria",
        "email": "ana@example.com",
        "password": "outra_senha"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email ja cadastrado."

def test_create_user_error(client):
    payload = {
        "name": None,
        "email": "ana@example.com",
        "password": "outra_senha"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid string"

