from pydantic import BaseModel, Field
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=150, description="Nome do produto")
    code: str = Field(..., min_length=2, max_length=50, description="Código único do produto")
    description: str | None = Field(None, description="Descrição detalhada do produto")
    company_id: int = Field(..., description="ID da empresa associada")

# Campos necessários para CRIAR um produto (POST)
class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=150)
    code: str | None = Field(None, min_length=2, max_length=50)
    description: str | None = None
    company_id: int | None = None

class CompanyMinResponse(BaseModel):
    id: int
    name: str
    cnpj: str

    class Config:
        from_attributes = True

# Estrutura de resposta da API (GET / Retorno)
class ProductResponse(ProductBase):
    id: int
    company: CompanyMinResponse | None = None
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True
