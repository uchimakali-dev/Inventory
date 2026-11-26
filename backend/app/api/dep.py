from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from app.users.repository import UserRepository as repo
from fastapi import Depends,HTTPException,Cookie,status
from app.users.service import UserService
from app.core.security import decode_token
import jwt


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(access_token:str | None = Cookie(default=None),db:Session=Depends(get_db)):
    
    credentials_error=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Authenticated")

    if not access_token:
        raise credentials_error

    try:
        payload = decode_token(access_token,expected_type="access")
        
    except jwt.PyJWTError as e:
        
        raise credentials_error

    user = repo.get_by_id(db,int(payload["sub"]))
    
    if not user:
        raise credentials_error

    return user


def get_user_service(db:Session=Depends(get_db)):
    return UserService(db)

