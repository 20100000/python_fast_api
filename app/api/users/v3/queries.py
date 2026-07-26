import strawberry
from typing import List
from app.DB.database import AsyncSessionLocal
from app.api.users.v3.services import get
from app.api.users.v3.types import UserType
from app.auth.graphql_guards import IsAuthenticated

@strawberry.type
class UserQuery:

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def all_users(self, skip: int = 0, limit: int = 100) -> List[UserType]:
        async with AsyncSessionLocal() as db:
            users = await get.all_users(db, skip=skip, limit=limit)
            return [UserType.from_model(u) for u in users]

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def user_by_id(self, user_id: int) -> UserType:
        async with AsyncSessionLocal() as db:
            u = await get.by_id(db, user_id=user_id)
            return UserType.from_model(u)
