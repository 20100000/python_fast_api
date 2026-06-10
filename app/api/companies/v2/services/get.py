from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.api.companies import models
from app.util.exceptions import DBRepositoryError

async def by_id(db: AsyncSession, company_id: int):
    try:
        stmt = select(models.Company).where(models.Company.id == company_id)
        result = await db.execute(stmt)
        db_company = result.scalar_one_or_none()

        if not db_company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empresa nao encontrado."
            )
        return db_company
    except SQLAlchemyError as e:
        raise DBRepositoryError("Erro ao consultar id no banco.") from e

async def all_companies(db: AsyncSession, skip: int = 0, limit: int = 100):
    try:
        stmt = select(models.Company).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise DBRepositoryError("Erro ao listar registros.") from e

async def get_company_by_cnpj(db: AsyncSession, cnpj: str):
    try:
        query = select(models.Company).where(models.Company.cnpj == cnpj)
        result = await db.execute(query)
        db_company =  result.scalar_one_or_none()

        return db_company
    except SQLAlchemyError as e:
        raise DBRepositoryError("Erro ao consultar id no banco.") from e