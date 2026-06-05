from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.util.exceptions import DBRepositoryError
from app.products.services import get

def execute(db: Session, product_id: int):
    db_product = get.by_id(db, product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto nao encontrado."
        )
    
    try:
        db.delete(db_product)
        db.commit()
        return None
    except SQLAlchemyError as e:
        db.rollback()
        raise DBRepositoryError("Erro ao deletar registro.") from e
