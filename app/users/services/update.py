from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.users import schemas
from app.users.services import get
from app.users.services.exceptions import DBRepositoryError

def execute(db: Session, user_id: int, user_data: schemas.UserUpdate):
    db_user = get.by_id(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario nao encontrado."
        )

    try:
        update_data = user_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise DBRepositoryError("Erro ao atualizar registro.") from e
