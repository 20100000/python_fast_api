from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.api.users import models, schemas
from app.api.users.services import get
from app.util.exceptions import DBRepositoryError
from app.auth.security import hash_password

def execute(db: Session, user: schemas.UserCreate):
    db_user = get.by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ja cadastrado."
        )
    hashed_pwd = hash_password(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_pwd
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise DBRepositoryError("Erro ao persistir novo usuario.") from e
