from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.products import models
from app.util.exceptions import DBRepositoryError
from sqlalchemy.orm import joinedload

def by_id(db: Session, product_id: int):
    try:
        stmt = select(models.Product).options(joinedload(models.Product.company)).where(models.Product.id == product_id)
        db_product = db.execute(stmt).scalar_one_or_none()

        if not db_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto nao encontrado."
            )
        return db_product
    except SQLAlchemyError as e:
        raise DBRepositoryError("Erro ao consultar id no banco.") from e

def all_products(db: Session, skip: int = 0, limit: int = 100):
    try:
        stmt = select(models.Product).options(joinedload(models.Product.company)).offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()
    except SQLAlchemyError as e:
        raise DBRepositoryError("Erro ao listar registros.") from e
