import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.DB.database import Base, get_db
from app.api.users.models import User as UserModel
from app.auth.security import hash_password, create_access_token

# 1. Configura um banco de dados SQLite temporário para os testes
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(name="db_session")
def db_session_fixture():
    """Limpa e recria o banco de dados a cada teste executado"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(name="client")
def client_fixture(db_session):
    """Cria um cliente HTTP deslogado (sem token)"""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

# 🌟 NOVA FIXTURE: Cria um usuário de teste automático no banco
@pytest.fixture(name="test_user")
def test_user_fixture(db_session):
    """Garante que um usuário criptografado exista no banco de testes"""
    user = UserModel(
        name="Usuario Teste TDD",
        email="tdd@email.com",
        password=hash_password("senha123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

# 🌟 NOVA FIXTURE: Cria um cliente HTTP já LOGADO (Injeta o JWT no cabeçalho)
@pytest.fixture(name="auth_client")
def auth_client_fixture(client, test_user):
    """Gera o Token JWT e cria um cliente que já envia o token em cada requisição"""
    token_data = {"sub": test_user.email, "name": test_user.name, "id": test_user.id}
    token = create_access_token(data=token_data)

    # Injeta o cabeçalho de autorização padrão do protocolo HTTP
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
