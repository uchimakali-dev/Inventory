# app/core/security.py
import bcrypt
from app.core.config import settings
from datetime import datetime,timezone,timedelta
import jwt


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt() 
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )

def _create_token(subject: str,user_role, token_type: str, expires_delta: timedelta) -> str:
    now = datetime.now(timezone.utc)
    
    payload = {"sub": str(subject),"user_role":user_role,"type": token_type, "iat": now, "exp": now + expires_delta}
    
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(subject: str,user_role:str) -> str:
    return _create_token(subject,user_role,"access",timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

def create_refresh_token(subject: str,user_role) -> str:
    return _create_token(subject,user_role,"refresh",timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

def decode_token(token: str, expected_type: str) -> dict:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    if payload.get("type") != expected_type:
        raise jwt.InvalidTokenError("Wrong token type")
    return payload
