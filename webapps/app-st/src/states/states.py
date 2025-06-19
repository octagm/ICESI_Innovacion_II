from pydantic import BaseModel

from domain.user import User


class AuthState(BaseModel):
    is_authenticated: bool = False
    jwt: str | None = None
    user: User | None = None
