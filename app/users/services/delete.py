from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.users.services import get
from app.users.services.exceptions import DBRepositoryError

def execute(db: Session, user_id: int):
    db_user = get.by_id(db, user_id)
    if not db_user:
        return None
    
    try:
        db.delete(db_user)
        db.commit()
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise DBRepositoryError("Erro ao deletar registro.") from e
