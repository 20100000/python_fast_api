import pytest
from app.api.users.models import User


#Happy
def test_delete_user_success(auth_client, db_session):
    """Testa a exclusão de um usuário existente."""
    user = User(name="Roberto", email="roberto@ex.com", password="1")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    response = auth_client.delete(f"/users/{user.id}")
    assert response.status_code == 204

    # Verifica se o usuário foi deletado tentando buscá-lo novamente
    check_response = auth_client.get(f"/users/{user.id}")
    assert check_response.status_code == 404
#Sad
def test_delete_user_not_found(auth_client):

    response = auth_client.delete(f"/users/100")
    assert response.status_code == 404

    check_response = auth_client.get(f"/users/100")
    assert check_response.status_code == 404
    assert response.json()["detail"] == "Usurio nao encontrado."
