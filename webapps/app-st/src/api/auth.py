import httpx
from pydantic import BaseModel

from domain.user import User
from states.auth import AuthState, set_auth


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    errors: list[str] = []
    jwt: str


def login(**kwargs):
    req = LoginRequest(**kwargs)
    
    # temp
    # httpx.post()
    USERNAME = "admin"
    PASSWORD = "pass"
    if req.username == USERNAME and req.password == PASSWORD:
        jwt = "demo_jwt"
        username = req.username
    else:
        raise Exception("invalid credentials")
    # temp
    
    set_auth(AuthState(
        is_authenticated=True,
        jwt=jwt,
        user=User(username=username),
    ))
