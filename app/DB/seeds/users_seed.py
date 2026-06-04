from sqlalchemy.orm import Session
from app.users.models import User
from app.auth.security import hash_password

def seed_users(db: Session):
    # Lista de dados que você quer inserir
    hashed_pwd = hash_password('test')
    users_data = [
        {"name": "Tiago Administrador", "email": "admin@gmail.com", "password": hashed_pwd},
        {"name": "Maria Silva", "email": "maria@email.com", "password": hashed_pwd},
        {"name": "João Souza", "email": "joao@email.com", "password": hashed_pwd}
    ]

    for user_info in users_data:
        # Verifica se o email já existe para não duplicar dados ao reiniciar o Docker
        exists = db.query(User).filter(User.email == user_info["email"]).first()
        if not exists:
            db_user = User(**user_info)
            db.add(db_user)
            print(f"Seed: Usuário {user_info['name']} criado com sucesso.")
    
    db.commit()
