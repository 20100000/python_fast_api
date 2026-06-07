from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.api.users import models
from app.util.exceptions import DBRepositoryError

async def by_id(db: AsyncSession, user_id: int):
    try:
        stmt = select(models.User).where(models.User.id == user_id)
        result = await db.execute(stmt)
        db_user = result.scalar_one_or_none()

        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usurio nao encontrado."
            )
        return db_user
    except SQLAlchemyError as e:
        raise DBRepositoryError("Erro ao consultar id no banco.") from e

async def by_email(db: AsyncSession, email: str):
    try:
        stmt = select(models.User).where(models.User.email == email)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        raise DBRepositoryError("Erro ao consultar email no banco.") from e

async def all_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    try:
        stmt = select(models.User).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise DBRepositoryError("Erro ao listar registros.") from e
