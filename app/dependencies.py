from fastapi.security import OAuth2PasswordBearer
from app.routers.auth import db_dependency
from app.utils.jwt import verify_access_token
from fastapi import HTTPException,Depends
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "auth/login")


def get_current_user(
        db: db_dependency,
        token:str = Depends(oauth2_scheme)
):
    user_id = verify_access_token(token)
    if not user_id:
        raise HTTPException(
            status_code = 401,
            detail = "Invalid authentication credentials"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code = 401,
            detail="User not found"
        )
    
    return user

