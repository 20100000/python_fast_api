import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.DB.database import Base, get_db

# 1. Configura o banco de dados SQLite em memória para testes rápidos e isolados
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool, # Permite o uso do banco em memória por múltiplas threads do teste
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Cria as tabelas antes de cada teste e apaga depois."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Fornece uma sessão de banco limpa para interações diretas nos testes."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="module")
def client():
    """Injeta a sessão de teste no FastAPI e retorna o TestClient."""
    def _get_test_db():
        try:
            database = TestingSessionLocal()
            yield database
        finally:
            database.close()

    # Sobrescreve a dependência original do FastAPI pela de teste
    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as test_client:
        yield test_client
    # Limpa as sobrescritas após o término dos testes do módulo
    app.dependency_overrides.clear()
