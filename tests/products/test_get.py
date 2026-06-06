import pytest
from app.api.products import models

def test_read_products_list(auth_client, db_session):
    product1 = models.Product(name="Mesa", code="P0001", description="Madeira", company_id=1)
    product2 = models.Product(name="Porta", code="P0002", description="Ferro", company_id=1)
    db_session.add_all([product1, product2])
    db_session.commit()

    response = auth_client.get("/products/?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Mesa"
    assert data[1]["name"] == "Porta"
    assert data[1]["company_id"] == 1