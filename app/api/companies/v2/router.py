from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.DB.database import get_async_db
from app.api.companies import schemas
from app.api.companies.v2.services import update, create, get, delete
from app.auth.security import get_current_user
from app.api.users.models import User as UserModel


router = APIRouter(
    prefix="/v2/companies",
    tags=["companies v2 (Async"]
)

@router.post("/", response_model=schemas.CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company_v2(company: schemas.CompanyCreate, db: AsyncSession = Depends(get_async_db), current_user: UserModel = Depends(get_current_user)):
    return await create.execute(db=db, company=company)

@router.get("/", response_model=List[schemas.CompanyResponse])
async def read_company_v2(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_db), current_user: UserModel = Depends(get_current_user)):
    return await get.all_companies(db, skip=skip, limit=limit)

@router.get("/{company_id}", response_model=schemas.CompanyResponse)
async def read_company_v2(company_id: int, db: AsyncSession = Depends(get_async_db), current_user: UserModel = Depends(get_current_user)):
    return await get.by_id(db, company_id=company_id)

@router.put("/{company_id}", response_model=schemas.CompanyResponse)
async def update_company_v2(company_id: int, company_data: schemas.CompanyUpdate, db: AsyncSession = Depends(get_async_db), current_user: UserModel = Depends(get_current_user)):
    return await update.execute(db, company_id=company_id, company_data=company_data)

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company_v2(company_id: int, db: AsyncSession = Depends(get_async_db), current_user: UserModel = Depends(get_current_user)):
    return await delete.execute(db, company_id=company_id)

