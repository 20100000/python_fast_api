from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.api.users.v2.services import get
from app.util.exceptions import DBRepositoryError

async def execute(db: AsyncSession, user_id: int):
    db_user = await get.by_id(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario nao encontrado."
        )
    
    try:
        await db.delete(db_user)
        await db.commit()
        return None
    except SQLAlchemyError as e:
        await db.rollback()
        raise DBRepositoryError("Erro ao deletar registro.") from e
