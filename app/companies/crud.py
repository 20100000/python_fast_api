from sqlalchemy.orm import Session
from app.companies import models, schemas

def get_company(db: Session, company_id: int):
    return db.query(models.Company).filter(models.Company.id == company_id).first()

def get_company_by_cnpj(db: Session, cnpj: str):
    return db.query(models.Company).filter(models.Company.cnpj == cnpj).first()

def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Company).offset(skip).limit(limit).all()

def create_company(db: Session, company: schemas.CompanyCreate):
    db_company = models.Company(name=company.name, cnpj=company.cnpj)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def update_company(db: Session, company_id: int, company_data: schemas.CompanyUpdate):
    db_company = get_company(db, company_id)
    if not db_company:
        return None
    update_data = company_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_company, key, value)
    db.commit()
    db.refresh(db_company)
    return db_company

def delete_company(db: Session, company_id: int):
    db_company = get_company(db, company_id)
    if not db_company:
        return None
    db.delete(db_company)
    db.commit()
    return db_company
