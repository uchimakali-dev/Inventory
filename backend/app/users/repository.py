from sqlalchemy.orm import Session
from app.users.models import User

class UserRepository:

    @staticmethod
    def add(db:Session,user:User):
        db.add(user)
        db.flush()
        return user

    @staticmethod
    def get_by_id(db:Session,id:int):
        return db.get(User,id)

    @staticmethod
    def get_by_email(db:Session,email:str):
        return db.query(User).filter(User.email==email).first()

    

    


    
