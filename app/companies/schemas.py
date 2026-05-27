from datetime import datetime
from pydantic import BaseModel

class CompanyBase(BaseModel):
    name: str
    cnpj: str

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: str | None = None
    cnpj: str | None = None

class CompanyResponse(CompanyBase):
    id: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True
