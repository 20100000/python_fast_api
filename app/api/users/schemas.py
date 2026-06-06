from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str
    admin: bool | None = False

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None

class UserResponse(UserBase):
    id: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True
