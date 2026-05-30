from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.users import models, schemas
from app.users.services import get
from app.users.services.exceptions import DBRepositoryError

def execute(db: Session, user: schemas.UserCreate):
    db_user = get.by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ja cadastrado."
        )
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise DBRepositoryError("Erro ao persistir novo usuario.") from e
