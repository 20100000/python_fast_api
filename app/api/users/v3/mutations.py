import strawberry
from app.DB.database import AsyncSessionLocal
from app.api.users.v3.services import create, update, delete
from app.api.users.v3.types import UserType, UserCreateInput, UserUpdateInput

from app.auth.graphql_guards import IsAuthenticated

@strawberry.type
class UserMutation:

    @strawberry.mutation
    async def create_user(self, input: UserCreateInput) -> UserType:
        async with AsyncSessionLocal() as db:
            u = await create.execute(db=db, user=input)
            return UserType.from_model(u)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def update_user(self, user_id: int, input: UserUpdateInput) -> UserType:
        async with AsyncSessionLocal() as db:
            u = await update.execute(db=db, user_id=user_id, user_data=input)
            return UserType.from_model(u)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def delete_user(self, user_id: int) -> str:
        async with AsyncSessionLocal() as db:
            await delete.execute(db=db, user_id=user_id)
            return f"Usuário {user_id} deletado com sucesso"
