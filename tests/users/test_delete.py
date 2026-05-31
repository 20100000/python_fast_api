import pytest
from app.users import models
#Happy
def test_delete_user_success(client, db_session):
    """Testa a exclusão de um usuário existente."""
    user = models.User(name="Roberto", email="roberto@ex.com", password="1")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    response = client.delete(f"/users/{user.id}")
    assert response.status_code == 204

    # Verifica se o usuário foi deletado tentando buscá-lo novamente
    check_response = client.get(f"/users/{user.id}")
    assert check_response.status_code == 404
#Sad
def test_delete_user_not_found(client, db_session):

    response = client.delete(f"/users/100")
    assert response.status_code == 404

    check_response = client.get(f"/users/100")
    assert check_response.status_code == 404
    assert response.json()["detail"] == "Usurio nao encontrado."
