import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Busca a URL do banco configurada no docker-compose
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://tiago:tiago123@db:5432/python_crud")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependência que abre e fecha a sessão do banco por requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
