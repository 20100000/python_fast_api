from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.api.users import models, schemas
from app.api.users.v2.services import get
from app.util.exceptions import DBRepositoryError
from app.auth.security import hash_password

async def execute(db: AsyncSession, user: schemas.UserCreate):
    db_user = await get.by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ja cadastrado."
        )
    hashed_pwd = hash_password(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        admin=user.admin | False,
        password=hashed_pwd
    )
    try:
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        await db.rollback()
        raise DBRepositoryError("Erro ao persistir novo usuario.") from e
