from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.DB.database import get_db
from app.companies import crud, schemas
from app.users.models import User as UserModel
from app.auth.security import get_current_user

router = APIRouter(
    prefix="/companies",
    tags=["companies"]
)


@router.post("/", response_model=schemas.CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_company = crud.get_company_by_cnpj(db, cnpj=company.cnpj)
    if db_company:
        raise HTTPException(status_code=400, detail="CNPJ já cadastrado.")
    return crud.create_company(db=db, company=company)

@router.get("/", response_model=List[schemas.CompanyResponse])
def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    return crud.get_companies(db, skip=skip, limit=limit)

@router.get("/{company_id}", response_model=schemas.CompanyResponse)
def read_company(company_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_company = crud.get_company(db, company_id=company_id)
    if not db_company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")
    return db_company

@router.put("/{company_id}", response_model=schemas.CompanyResponse)
def update_company(company_id: int, company_data: schemas.CompanyUpdate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_company = crud.update_company(db, company_id=company_id, company_data=company_data)
    if not db_company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")
    return db_company

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(company_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_company = crud.delete_company(db, company_id=company_id)
    if not db_company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada.")
    return None
