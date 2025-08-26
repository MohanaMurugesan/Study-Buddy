from datetime import timedelta,datetime,timezone
from jose import jwt,JWTError
from dotenv import load_dotenv
import os
from fastapi import HTTPException,status


load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")


def create_access_token(user_id:int,expires_at: timedelta):
    to_encode = {'sub': str(user_id),
              'iat':int(datetime.now(timezone.utc).timestamp()),
              'type':'access'
                }
    expires=int((datetime.now(timezone.utc)+expires_at).timestamp())
    to_encode.update({"exp":expires})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def decode_access_token(token:str):

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate":"Bearer"}
        )
    
def create_refresh_token(user_id:int,expires_at:timedelta):
    to_encode = {
        "sub":str(user_id),
        "iat": int(datetime.now(timezone.utc).timestamp()),
        "type":"refresh",
    }
    expires=int((datetime.now(timezone.utc)+expires_at).timestamp())
    to_encode.update({"exp":expires})

    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)


def verify_access_token(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        if payload.get("type") != "access":
            raise HTTPException(
                status_code=401,
                detail="Invalid token type"
            )
    
        exp = payload.get("exp")

        if exp is None or datetime.fromtimestamp(exp,tz=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(
                status_code = 401,
                detail = "Token expired"
            )
        
        return payload.get("sub")
    
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )