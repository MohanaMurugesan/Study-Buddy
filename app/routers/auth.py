from typing import Annotated
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter,status,HTTPException,Depends,Response,Request
from app.schemas.user import UserCreate,UserResponse
from datetime import datetime,timezone
from app.utils.jwt import create_access_token,create_refresh_token
from datetime import timedelta
from jose import jwt,JWTError
from dotenv import load_dotenv
import os
from app.models.tokens import RefreshToken
from fastapi.security import OAuth2PasswordRequestForm
from app.crud import auth as crud_auth

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM=os.getenv("JWT_ALGORITHM")


db_dependency = Annotated[Session,Depends(get_db)]


@router.post("/create-user",status_code=status.HTTP_201_CREATED)
def create_user(db:db_dependency, create_user_request : UserCreate):
    
    # check whether it is the verified user

    otp_record = crud_auth.verify_otp(db,create_user_request.token)

    if not otp_record:
        raise HTTPException(status_code=400,detail="Invalid")
    
    email = otp_record.email

    # check whether the user already created a account or not
    
    if crud_auth.get_user_by_email(db,email):
        raise HTTPException(status_code=400,detail="Existing email id")
    
    # check whether the username exist
    if crud_auth.get_user_by_username(db,create_user_request.username):
        raise HTTPException(status_code=400,detail="username already exist")

    new_user = crud_auth.create_user(db,
                                     email,
                                     create_user_request.username,
                                     create_user_request.password)

    return UserResponse.model_validate(new_user)

@router.post("/login",status_code=status.HTTP_200_OK)
def login(db:db_dependency,response:Response,form_data:OAuth2PasswordRequestForm = Depends()):
    user = crud_auth.get_user_by_username(db,form_data.username)

    if not user or not crud_auth.verify_password(form_data.password,user.password):
        raise HTTPException(status_code=401,detail="Invalid username or password")
    
    access_token = create_access_token(user.id,timedelta(minutes=20))
    refresh_token = create_refresh_token(user.id,timedelta(days=7))
    
    crud_auth.save_refresh_token(db,refresh_token,user.id,timedelta(days=7))

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        path="/"
    )

    return {
        'access_token':access_token,
        'token_type':'bearer'
        }

@router.post("/refresh")
def refresh_access_token(db:db_dependency,request: Request,response:Response):
    refresh_cookie_token = request.cookies.get("refresh_token")

    if not refresh_cookie_token :
        raise HTTPException(status_code=401,detail="Missing refresh token")
    
    db_token=crud_auth.get_valid_refresh_token(db,refresh_cookie_token) 

    if not db_token:
        raise HTTPException(status_code=401,detail="Invalid or expired refresh token")

    try:
        payload = jwt.decode(refresh_cookie_token,SECRET_KEY,algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401,detail="Invalid token type")
        
        user_id = payload.get("sub")
        new_access_token=create_access_token(user_id,timedelta(minutes=20))

        # Rotate refresh token
        new_refresh_jwt=create_refresh_token(user_id,timedelta(days=7))
        db_token.token = new_refresh_jwt
        db_token.expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        db.commit()


        response.set_cookie(
            key = "refresh_token",
            value=new_refresh_jwt,
            httponly=True,
            secure=True,
            samesite="strict",
            path="/"
        )

        return {
            "access_token":new_access_token,
            "token_type":"bearer"
        }
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token"
        )


@router.post("/logout",status_code=status.HTTP_200_OK)
def logout(request:Request,db:db_dependency,response:Response):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401,detail="Refresh token missing")


    db_token=db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    crud_auth.revoke_refresh_token(db,refresh_token)

    response.delete_cookie(
            key = "refresh_token",
            path="/"
        )
    

    return {"message" : "Logged out successfully"}