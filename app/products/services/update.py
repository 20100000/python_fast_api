from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.products import schemas
from app.products.services import get
from app.util.exceptions import DBRepositoryError

def execute(db: Session, product_id: int, product_data: schemas.ProductUpdate):
    db_product = get.by_id(db, product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto nao encontrado."
        )

    try:
        update_data = product_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
        return db_product
    except SQLAlchemyError as e:
        db.rollback()
        raise DBRepositoryError("Erro ao atualizar registro.") from e
