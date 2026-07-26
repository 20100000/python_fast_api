import strawberry
from strawberry.fastapi import GraphQLRouter, BaseContext
from fastapi import Request
import jwt
from typing import Optional
from app.auth.security import SECRET_KEY, ALGORITHM

from app.api.users.v3.queries import UserQuery
from app.api.users.v3.mutations import UserMutation

class CustomContext(BaseContext):
    def __init__(self, token_payload: Optional[dict]):
        super().__init__()
        self.token_payload = token_payload

async def get_graphql_context(request: Request) -> CustomContext:
    token_payload = None
    auth_header = request.headers.get("Authorization")

    if auth_header and auth_header.startswith("Bearer "):
        try:
            token = auth_header.split(" ")[1]
            token_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except (jwt.PyJWTError, IndexError):
            pass

    return CustomContext(token_payload=token_payload)

@strawberry.type
class Query(
    UserQuery
    # CompanyQuery,
    # ProductQuery
):
    pass

@strawberry.type
class Mutation(
    UserMutation
    # CompanyMutation,
    # ProductMutation
):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_router = GraphQLRouter(schema, context_getter=get_graphql_context)

