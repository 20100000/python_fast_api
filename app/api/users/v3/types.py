import strawberry
from datetime import datetime
from typing import Optional

# ----------------------------------------------------
# 1. TIPOS DE RETORNO (Equivalente ao UserResponse)
# ----------------------------------------------------
@strawberry.type
class UserType:
    id: int
    name: str
    email: str
    admin: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_model(cls, u):
        c_at = getattr(u, "created_at", getattr(u, "createdAt", None)) or datetime.now()
        u_at = getattr(u, "updated_at", getattr(u, "updatedAt", None)) or datetime.now()

        return cls(
            id=u.id,
            name=u.name,
            email=u.email,
            admin=bool(getattr(u, "admin", False)),
            created_at=c_at,
            updated_at=u_at
        )

# ----------------------------------------------------
# 2. INPUTS DE ENTRADA (Equivalente ao UserCreate e UserUpdate)
# ----------------------------------------------------
@strawberry.input
class UserCreateInput:
    name: str
    email: str
    password: str
    admin: Optional[bool] = False

@strawberry.input
class UserUpdateInput:
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    admin: Optional[bool] = False
