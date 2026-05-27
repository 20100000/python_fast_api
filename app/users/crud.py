from sqlalchemy.orm import Session
from app.users import models, schemas

# Buscar usuário por ID
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Buscar usuário por Email (útil para validações)
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Listar todos os usuários (com paginação)
def get_users(db: Session, skip: int = 0, limit: int = 100):
    print(f"LISTA TODOS OS USUARIOS : .")
    return db.query(models.User).offset(skip).limit(limit).all()

# Criar usuário
def create_user(db: Session, user: schemas.UserCreate):
    # Em produção, aplique um hash na senha aqui (ex: bcrypt ou passlib)
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Atualiza o objeto com o ID e datas gerados pelo banco
    return db_user

# Atualizar usuário (parcial ou total)
def update_user(db: Session, user_id: int, user_data: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    # Converte os dados enviados em dicionário, ignorando o que for nulo (None)
    update_data = user_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
        
    db.commit()
    db.refresh(db_user)
    return db_user

# Deletar usuário
def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    db.delete(db_user)
    db.commit()
    return db_user
