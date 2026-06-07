import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.config import settings

# --- NOVA Infraestrutura Assíncrona (Para a V2) ---
async_engine = None
AsyncSessionLocal = None

#PARA O CI: Se estiver rodando testes, ignora completamente a engine assíncrona
IS_TESTING = "pytest" in sys.modules or "pytest" in "".join(sys.argv)

if not IS_TESTING and settings.DATABASE_URL and not settings.DATABASE_URL.startswith("sqlite"):
    try:
        ASYNC_DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
        async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=False)
        AsyncSessionLocal = async_sessionmaker(
            bind=async_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
    except Exception:
        pass

# Busca a URL do banco configurada no docker-compose
DATABASE_URL = settings.DATABASE_URL

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

# Dependência Assíncrona para ser injetada nas rotas V2
async def get_async_db():
    if AsyncSessionLocal is None:
        raise RuntimeError("O motor assíncrono não está disponível neste ambiente (modo teste ativo).")
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
