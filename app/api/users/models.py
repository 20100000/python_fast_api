from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.DB.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    admin = Column(Boolean, server_default="false", default=False, nullable=False)
    createdAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updatedAt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # docker compose exec fastapi_app alembic revision --autogenerate -m "add_admin_to_user"
    # docker compose run --rm web alembic revision --autogenerate -m "add_admin_to_user"
    # docker compose exec fastapi_app alembic revision --autogenerate -m "add_admin_to_user"


