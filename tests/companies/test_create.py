import pytest

#Happy
def test_create_company_success(auth_client):
    payload = {
        "name": "Teste LTDA",
        "cnpj": "13.347.016/0001-17",
    }
    response = auth_client.post("/companies/", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == payload["name"]
    assert data["cnpj"] == payload["cnpj"]
    assert "id" in data
#Sad
def test_create_company_error(auth_client):
    payload = {
        "name": None,
        "email": "3.347.016/0001-17"
    }
    response = auth_client.post("/companies/", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid string"

