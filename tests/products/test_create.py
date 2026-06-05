import pytest
from fastapi import status

#Happy
def test_create_product_success(auth_client):
    payload = {
        "name": "Cadeira",
        "code": "C1110",
        "description": "cadeira de madeira",
        "company_id": 1
    }
    response = auth_client.post("/products/", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == payload["name"]
    assert data["code"] == payload["code"]
    assert "id" in data
#Sad
def test_create_product_error(auth_client):
    payload = {
        "name": None
    }
    response = auth_client.post("/products/", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid string"

def test_create_product_unauthorized(client):
    payload = {
        "name": "Cadeira",
        "code": "C1110",
        "description": "cadeira de madeira",
        "company_id": 1
    }
    response = client.post("/products/", json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED