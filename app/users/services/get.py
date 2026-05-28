from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.users import models
from app.users.services.exceptions import DBRepositoryError

def by_id(db: Session, user_id: int):
    try:
        stmt = select(models.User).where(models.User.id == user_id)
        return db.execute(stmt).scalar_one_or_none()
    except SQLAlchemyError as e:
        raise DBRepositoryError("Erro ao consultar id no banco.") from e

def by_email(db: Session, email: str):
    try:
        stmt = select(models.User).where(models.User.email == email)
        return db.execute(stmt).scalar_one_or_none()
    except SQLAlchemyError as e:
        raise DBRepositoryError("Erro ao consultar email no banco.") from e

def all_users(db: Session, skip: int = 0, limit: int = 100):
    try:
        stmt = select(models.User).offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()
    except SQLAlchemyError as e:
        raise DBRepositoryError("Erro ao listar registros.") from e
