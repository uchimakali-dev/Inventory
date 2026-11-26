from pydantic import BaseModel,ConfigDict,EmailStr
import enum

class UserRole(str,enum.Enum):
    shop="owner"

class RegisterData(BaseModel):
    username:str
    email:EmailStr
    password:str
    phone:str

class LoginData(BaseModel):
    email:str
    password:str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)   
    id: int
    username: str
    user_role:str
    email: EmailStr
