import pytest
from app.users import models

def test_read_users_empty(client):
    """Testa a listagem de usuários quando o banco está vazio."""
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == []

def test_read_users_list(client, db_session):
    """Testa o retorno de múltiplos usuários na listagem."""
    user1 = models.User(name="User 1", email="u1@ex.com", password="1")
    user2 = models.User(name="User 2", email="u2@ex.com", password="2")
    db_session.add_all([user1, user2])
    db_session.commit()

    response = client.get("/users/?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["email"] == "u1@ex.com"
