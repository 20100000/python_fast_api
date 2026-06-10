from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.api.companies.v2.services import get
from app.util.exceptions import DBRepositoryError

async def execute(db: AsyncSession, company_id: int):
    db_company = await get.by_id(db, company_id)
    if not db_company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa nao encontrado."
        )
    
    try:
        await db.delete(db_company)
        await db.commit()
        return None
    except SQLAlchemyError as e:
        await db.rollback()
        raise DBRepositoryError("Erro ao deletar registro.") from e
