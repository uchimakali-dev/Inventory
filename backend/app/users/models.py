from app.db.base import Base
from sqlalchemy import Column,Integer,String,DateTime,func,Enum
from app.users.schemas import UserRole
class User(Base):

    __tablename__="users"

    id=Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String(50),unique=True)
    email=Column(String(255),unique=True,nullable=False)
    phone=Column(String(20))
    hash_password=Column(String(255),nullable=False)
    user_role = Column(Enum(UserRole),nullable=False,default=UserRole.shop)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
