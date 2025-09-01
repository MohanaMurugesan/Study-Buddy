from sqlalchemy.orm import Session
from app.models.otp import Otp
from datetime import datetime,timezone,timedelta
from app.models.user import User
from app.utils.hashing import hash_password,password_context
from app.models.tokens import RefreshToken

def verify_otp(db:Session,token:str):
    return db.query(Otp).filter(Otp.token == token,
                                Otp.expires_at > datetime.now(timezone.utc),
                                Otp.is_verified == True).first()


def get_user_by_email (db:Session,email:str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_username (db:Session,username:str):
    return db.query(User).filter(User.username == username).first()

def create_user(db:Session,email:str,username:str,password:str):
    new_user = User(
        email = email,
        username = username,
        password = hash_password(password),
        is_verified = True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def verify_password(password:str,hashed_password:str):
    return password_context.verify(password,hashed_password)

def save_refresh_token(db:Session,token:str,user_id:str,expiry:timedelta):
    refresh_token=RefreshToken(
        token = token,
        user_id = user_id,
        expires_at = datetime.now(timezone.utc)+expiry
    )
    db.add(refresh_token)
    db.commit()
    return refresh_token

def get_valid_refresh_token(db:Session,token:str):
    return db.query(RefreshToken).filter(
        RefreshToken.token == token,
        RefreshToken.revoked == False,
        RefreshToken.expires_at > datetime.now(timezone.utc)
    ).first()

def revoke_refresh_token(db: Session,token : str):
    db_token = db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if db_token:
        db_token.revoked = True
        db_token.expires_at = datetime.now(timezone.utc)
        db.commit()