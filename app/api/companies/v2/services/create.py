from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.api.companies import models, schemas
from app.util.exceptions import DBRepositoryError
from app.api.companies.v2.services import get

async def execute(db: AsyncSession, company: schemas.CompanyCreate):
    try:
        db_company = await get.get_company_by_cnpj(db, cnpj=company.cnpj)
        if db_company:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CNPJ ja cadastrado."
            )
        db_company = models.Company(name=company.name, cnpj=company.cnpj)
        db.add(db_company)
        await db.commit()
        await  db.refresh(db_company)
        return db_company
    except SQLAlchemyError as e:
        await db.rollback()
        raise DBRepositoryError("Erro ao persistir novo usuario.") from e
