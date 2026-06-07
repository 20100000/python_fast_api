from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.api.users import schemas
from app.api.users.v2.services import get
from app.util.exceptions import DBRepositoryError

async def execute(db: AsyncSession, user_id: int, user_data: schemas.UserUpdate):
    db_user = await get.by_id(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario nao encontrado."
        )

    try:
        update_data = user_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        await db.rollback()
        raise DBRepositoryError("Erro ao atualizar registro.") from e
