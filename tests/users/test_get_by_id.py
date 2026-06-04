import pytest
from app.users import models
#Happy
def test_read_user_by_id_success(auth_client, db_session):
    """Testa a busca de um usuário específico por ID."""
    user = models.User(name="Carlos", email="carlos@ex.com", password="1")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    response = auth_client.get(f"/users/{user.id}")
    assert response.status_code == 200
    assert response.json()["email"] == "carlos@ex.com"
#Sad
def test_read_user_by_id_not_found(auth_client):
    response = auth_client.get(f"/users/1000")
    assert response.status_code == 404
    assert response.json()["detail"] == "Usurio nao encontrado."
