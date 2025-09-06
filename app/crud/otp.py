from app.models.user import User
import random
from datetime import datetime,timezone,timedelta
import secrets
from app.utils.hashing import hash_otp,password_context
from app.models.otp import Otp
from app.schemas.otp import OtpVerify

def create_or_update_otp(db,email):
    verify_mail = db.query(User).filter(User.email == email ).first()
    if verify_mail:
        return None
    
    otp_code = str(random.randint(100000,999999))
    expires_at = datetime.now(timezone.utc) + timedelta(minutes = 5)

    token = secrets.token_urlsafe(16)
    hashed_otp = hash_otp(otp_code)
    next_otp_time_interval = 60

    otp_record = db.query(Otp).filter(Otp.email == email).first()

    if otp_record:
        last_otp_request = (datetime.now(timezone.utc) - otp_record.last_requested_time).total_seconds()
        if last_otp_request < next_otp_time_interval:
            return None
        
        otp_record.otp_code = hashed_otp
        otp_record.expires_at = expires_at
        otp_record.is_verified = False
        otp_record.token = token
        otp_record.last_requested_time = datetime.now(timezone.utc)

    else:
        otp_record= Otp(
            email = email,
            otp_code = hashed_otp,
            expires_at = expires_at,
            token = token,
            last_requested_time = datetime.now(timezone.utc)
        )
        db.add (otp_record)


    db.commit()
    return otp_code, token

def verify_otp(db,otp_verify:OtpVerify):
    otp_record = db.query(Otp).filter(Otp.token == otp_verify.token).first()

    if not otp_record:
        return False
    
    if not password_context.verify(otp_verify.otp_code,otp_record.otp_code):
        return False    
    
    if otp_record.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        return False
    
    otp_record.is_verified = True
    db.commit()
    return True