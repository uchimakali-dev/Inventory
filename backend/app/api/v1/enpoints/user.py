from fastapi import APIRouter,Depends,Response,Cookie
from app.users.schemas import UserResponse,RegisterData,LoginData
from app.users.service import UserService
from app.core.security import decode_token,create_access_token,create_refresh_token
from app.core.cookie import set_auth_cookies,clear_auth_cookies
from app.core.exception import UsernameAlreadyExists,NoRefreshToken,InvalidCrendientials
from app.api.dep import get_user_service,get_current_user

router = APIRouter(prefix="/users",tags=["users"])


@router.post("/register",response_model=UserResponse)
def register(userData:RegisterData,service:UserService=Depends(get_user_service)):
    try:
        return service.register(userData)
    except Exception as e:
        raise UsernameAlreadyExists()

@router.post("/login")
def login(userData:LoginData,response:Response,service:UserService=Depends(get_user_service)):
    try:
        access_token,refresh_token=service.login(userData)
    except Exception as e:
        
        raise InvalidCrendientials()

    set_auth_cookies(response,access_token,refresh_token)

    return {"Message":"Logged In"}

@router.get("/me",response_model=UserResponse)
def current(current_user=Depends(get_current_user)):
    return current_user

@router.post("/refresh")
def refresh(response:Response,refresh_token:str | None=Cookie(default=None),service:UserService=Depends(get_user_service)):
    
    if not refresh_token:
        raise NoRefreshToken()

    payload=decode_token(refresh_token,"refresh")

    user = service.is_user_by_id(int(payload["sub"]))
    subject = str(payload["sub"])
    set_auth_cookies(response,create_access_token(subject,user.user_role),create_refresh_token(subject,user.user_role))
    return {
        "message":"token refreshed"
    }

    

    