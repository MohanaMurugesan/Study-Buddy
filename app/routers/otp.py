from fastapi import APIRouter,status,HTTPException
from app.routers.auth import db_dependency
from app.models.user import User
from app.schemas.otp import EmailVerification,OtpVerify
import random
from datetime import datetime,timezone,timedelta
from app.models.otp import Otp
import smtplib
from email.mime.text import MIMEText


router = APIRouter(
    prefix="/otp",
    tags=["otp"]
)



@router.post("/registration",status_code=status.HTTP_201_CREATED)
def registration_with_otp(db:db_dependency,email_verification : EmailVerification):
    verify_mail = db.query(User).filter(User.email == email_verification.email ).first()
    if verify_mail:
        raise HTTPException(status_code=400,detail="Email already exist")
    
    otp_code = str(random.randint(100000,999999))
    expires_at = datetime.now(timezone.utc) + timedelta(minutes = 5)

    otp_record = db.query(Otp).filter(Otp.email == email_verification.email).first()

    if otp_record:
        otp_record.otp_code = otp_code
        otp_record.expires_at = expires_at
        otp_record.is_verified = False

    else:
        otp_record= Otp(
            email = email_verification.email,
            otp_code = otp_code,
            expires_at = expires_at
        )
        db.add (otp_record)

    db.commit()

    subject = "Study Buddy OTP"
    body = f"Your OTP is {otp_code}"
    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = "studybuddyyy01@gmail.com"
    msg["To"] = email_verification.email


    with smtplib.SMTP("smtp.gmail.com",587) as server:
        server.starttls()
        server.login("studybuddyyy01@gmail.com","punz qibe weuh cxvj")
        server.send_message(msg)


@router.post("/verify-otp",status_code=status.HTTP_201_CREATED)
def verify_otp(db:db_dependency,otp_verify:OtpVerify):
    otp_record = db.query(Otp).filter(Otp.email == otp_verify.email).first()

    if not otp_record:
        raise HTTPException(status_code=404,detail="OTP not found")
    
    if otp_record.otp_code != otp_verify.otp_code:
        raise HTTPException(status_code=400,detail="Invalid OTP")
    
    if otp_record.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(statuscode=400,detail="OTP expired")
    
    otp_record.is_verified = True
    db.commit()
    
        

    return {"message": "OTP verified successfully"}









    
    
