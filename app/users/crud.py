from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.users import models, schemas

# Buscar usuario por ID
def get_user(db: Session, user_id: int):
    try:
        stmt = select(models.User).where(models.User.id == user_id)
        return db.execute(stmt).scalar_one_or_none()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao consultar o usuario no banco de dados."
        )

# Buscar usuario por Email
def get_user_by_email(db: Session, email: str):
    try:
        stmt = select(models.User).where(models.User.email == email)
        return db.execute(stmt).scalar_one_or_none()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao verificar o email no banco de dados."
        )

# Listar todos os usuarios (com paginacao)
def get_users(db: Session, skip: int = 0, limit: int = 100):
    try:
        print("LISTA TODOS OS USUARIOS : .")
        stmt = select(models.User).offset(skip).limit(limit)
        return db.execute(stmt).scalars().all()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar os usuarios do banco de dados."
        )

# Criar usuario
def create_user(db: Session, user: schemas.UserCreate):
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
    except SQLAlchemyError:
        db.rollback()  # Garante rollback correto de forma sincrona
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Falha critica ao tentar salvar o usuario."
        )

# Atualizar usuario
def update_user(db: Session, user_id: int, user_data: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
        
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Falha critica ao tentar atualizar o usuario."
        )

# Deletar usuario
def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    try:
        db.delete(db_user)
        db.commit()
        return db_user
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Falha critica ao tentar deletar o usuario."
        )
