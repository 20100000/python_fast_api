from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.api.companies import schemas
from app.api.companies.v2.services import get
from app.util.exceptions import DBRepositoryError

async def execute(db: AsyncSession, company_id: int, company_data: schemas.CompanyUpdate):
    db_company = await get.by_id(db, company_id)
    if not db_company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa nao encontrado."
        )

    try:
        update_data = company_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_company, key, value)
        await db.commit()
        await db.refresh(db_company)
        return db_company
    except SQLAlchemyError as e:
        await db.rollback()
        raise DBRepositoryError("Erro ao atualizar registro.") from e
