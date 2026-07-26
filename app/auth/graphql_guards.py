import strawberry
from strawberry.types import Info
from strawberry.permission import BasePermission

class IsAuthenticated(BasePermission):
    message = "Não autorizado! Token JWT ausente ou inválido."
    def has_permission(self, source: any, info: Info, **kwargs: any) -> bool:
        payload = info.context.token_payload
        if not payload or "sub" not in payload:
            return False
        return True
