import pytest
from app.api.users.models import User


#Happy
def test_update_user_success(auth_client, db_session):
    """Testa a atualização parcial ou total dos dados do usuário."""
    user = User(name="Marta", email="marta@ex.com", password="1")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    update_payload = {
        "name": "Marta Silva",
        "email": "marta.silva@ex.com"
    }
    response = auth_client.put(f"/users/{user.id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Marta Silva"
    assert response.json()["email"] == "marta.silva@ex.com"
#Sad
def test_update_user_not_faund(auth_client):
    update_payload = {
        "name": "Marta Silva",
        "email": "marta.silva@ex.com"
    }
    response = auth_client.put(f"/users/1000", json=update_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Usurio nao encontrado."
