from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.users import schemas
from app.users.services import get  # Importa apenas o serviço de busca
from app.users.services.exceptions import DBRepositoryError

def execute(db: Session, user_id: int, user_data: schemas.UserUpdate):
    db_user = get.by_id(db, user_id)
    if not db_user:
        return None
    
    update_data = user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
        
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        raise DBRepositoryError("Erro ao atualizar registro.") from e
