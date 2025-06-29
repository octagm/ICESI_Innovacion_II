import sqlite3
from hashlib import sha256
from pydantic import BaseModel
from jose import jwt
import datetime

from domain.user import User
from states.auth import AuthState, set_auth

# Configuración del JWT
SECRET_KEY = "MLd3pl0y!M0d3ls"  # cámbiala en producción
ALGORITHM = "HS256"
DB_PATH = "users.db"

class LoginRequest(BaseModel):
    username: str
    password: str

def hash_password(password: str) -> str:
    return sha256(password.encode()).hexdigest()

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def user_exists(username: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists

def authenticate(username: str, password: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row and row[0] == hash_password(password)

def create_jwt(username: str) -> str:
    payload = {
        "sub": username,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def register_user(username: str, password: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
    conn.commit()
    conn.close()

def login(username: str, password: str):
    init_db()

    if not user_exists(username):
        raise Exception("no_user")

    if not authenticate(username, password):
        raise Exception("invalid_password")

    token = create_jwt(username)

    set_auth(AuthState(
        is_authenticated=True,
        jwt=token,
        user=User(username=username),
    ))

def logout():
    set_auth(AuthState(is_authenticated=False, jwt="", user=None))
