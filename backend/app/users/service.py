from app.users.repository import UserRepository as repo
from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password
from app.core.exception import EmailAlreadyExists,InvalidCrendientials,InvalidRefreshToken
from app.users.models import User
from app.core.security import create_access_token,create_refresh_token
from app.users.schemas import RegisterData,LoginData


class UserService:

    def __init__(self, db: Session):
        self.db = db

    def register(self, userData: RegisterData):

        email = repo.get_by_email(self.db, userData.email)

        if email:
            raise EmailAlreadyExists()

        hash_pwd = hash_password(userData.password)

        user_data = userData.model_dump(exclude="password")
        user = User(**user_data, hash_password=hash_pwd)
        repo.add(self.db,user)
        self.db.commit()

        return user

    def login(self,userData:LoginData):

        user = repo.get_by_email(self.db,userData.email)
       
        if not user or not verify_password(userData.password,user.hash_password):
            
            raise InvalidCrendientials()

        subject = user.id
        user_role = user.user_role

        return create_access_token(subject,user_role),create_refresh_token(subject,user_role)


    def is_user_by_id(self,id:int):
        user = repo.get_by_id(self.db,id)
        if not user:
            raise InvalidRefreshToken()
        return user