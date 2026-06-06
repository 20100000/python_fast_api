from sqlalchemy.orm import Session
from app.api.companies.models import Company

def seed_companies(db: Session):
    companies_data = [
        {"name": "Tech Corp Brasil", "cnpj": "12345678000199"},
        {"name": "Logística Express", "cnpj": "98765432000188"}
    ]

    for comp_info in companies_data:
        exists = db.query(Company).filter(Company.cnpj == comp_info["cnpj"]).first()
        if not exists:
            db_company = Company(**comp_info)
            db.add(db_company)
            print(f"🌱 Seed: Empresa {comp_info['name']} criada com sucesso.")
    db.commit()
