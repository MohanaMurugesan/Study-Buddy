from fastapi import APIRouter,status,HTTPException,BackgroundTasks
from app.routers.auth import db_dependency
from app.models.user import User
from app.schemas.otp import EmailVerification,OtpVerify
import random
from datetime import datetime,timezone,timedelta
from app.models.otp import Otp
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import secrets
from app.utils.hashing import hash_otp,password_context


router = APIRouter(
    prefix="/otp",
    tags=["otp"]
)

load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_otp_mail(email:str,otp_code:str):
    subject = "Study Buddy OTP"
    body = f"Your OTP is {otp_code}"
    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = email

    try:
        with smtplib.SMTP("smtp.gmail.com",587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e :
        print(f"Failed to send otp email:{str(e)}")


@router.post("/registration",status_code=status.HTTP_201_CREATED)
def send_registration_otp(db:db_dependency,
                          email_verification : EmailVerification,
                          background_task:BackgroundTasks):
    verify_mail = db.query(User).filter(User.email == email_verification.email ).first()
    if verify_mail:
        raise HTTPException(status_code=400,detail="Email already exists")
    
    otp_code = str(random.randint(100000,999999))
    expires_at = datetime.now(timezone.utc) + timedelta(minutes = 5)

    token = secrets.token_urlsafe(16)
    hashed_otp = hash_otp(otp_code)
    next_otp_time_interval = 60

    otp_record = db.query(Otp).filter(Otp.email == email_verification.email).first()

    if otp_record:
        last_otp_request = (datetime.now(timezone.utc) - otp_record.last_requested_time).total_seconds()
        if last_otp_request < next_otp_time_interval:
            raise HTTPException(
                status_code=429,
                detail=f"OTP already sent,please wait {int(next_otp_time_interval - last_otp_request)} seconds."
            )
        otp_record.otp_code = hashed_otp
        otp_record.expires_at = expires_at
        otp_record.is_verified = False
        otp_record.token = token
        otp_record.last_requested_time = datetime.now(timezone.utc)

    else:
        otp_record= Otp(
            email = email_verification.email,
            otp_code = hashed_otp,
            expires_at = expires_at,
            token = token,
            last_requested_time = datetime.now(timezone.utc)
        )
        db.add (otp_record)


    db.commit()


    background_task.add_task(send_otp_mail,email_verification.email,otp_code)

    return {"message":"OTP sent successfully","token":token}


@router.post("/verify-otp",status_code=status.HTTP_200_OK)
def verify_otp(db:db_dependency,otp_verify:OtpVerify):
    otp_record = db.query(Otp).filter(Otp.token == otp_verify.token).first()

    if not otp_record:
        raise HTTPException(status_code=404,detail="OTP not found")
    
    if not password_context.verify(otp_verify.otp_code,otp_record.otp_code):
        raise HTTPException(status_code=400,detail="Invalid OTP")
    
    if otp_record.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=400,detail="OTP expired")
    
    otp_record.is_verified = True
    db.commit()
    
        

    return {"message": "OTP verified successfully","verified_token":otp_record.token}









    
    
