from fastapi import HTTPException, status


class UserNotFound(HTTPException):
    def __init__(self, detail: str = "User not found."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class UsernameAlreadyExists(HTTPException):
    def __init__(self, detail: str = "This username is already taken."):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)
        
class InvalidCrendientials(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED,detail="incorrect password or username")

class UserNotFount(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")

class InvalidRefreshToken(HTTPException):
    def __init__(self, ):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid refresh token")
        
class NoRefreshToken(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="No refresh Token")

class EmailAlreadyExists(HTTPException):
    def __init__(self, detail: str = "An account with this email already exists."):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class DealerNotFound(HTTPException):
    def __init__(self, detail: str = "Dealer not found."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ProductNotFound(HTTPException):
    def __init__(self, detail: str = "Product not found."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)