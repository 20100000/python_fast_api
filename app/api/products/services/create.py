from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.api.products import schemas, models
from app.util.exceptions import DBRepositoryError

def execute(db: Session, product: schemas.ProductCreate):
    
    db_product = models.Product(
        name=product.name,
        code=product.code,
        description=product.description,
        company_id=product.company_id
    )
    try:
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        db.refresh(db_product, attribute_names=["company"])
        return db_product
    except SQLAlchemyError as e:
        db.rollback()
        raise DBRepositoryError("Erro ao persistir novo usuario.") from e
