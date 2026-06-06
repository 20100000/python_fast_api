import pytest
from app.api.companies import models

def test_read_companies_list(auth_client, db_session):
    company1 = models.Company(name="Compay LTDA", cnpj="2152300000158")
    db_session.add_all([company1])
    db_session.commit()

    response = auth_client.get("/companies/?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Compay LTDA"
    assert data[0]["cnpj"] == "2152300000158"