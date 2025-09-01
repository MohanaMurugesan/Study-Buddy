from fastapi import APIRouter, status, BackgroundTasks
from app.routers.auth import db_dependency
from app.schemas.otp import EmailVerification, OtpVerify
from app.crud import otp as otp_crud
from app.utils.email import send_otp_mail

router = APIRouter(
    prefix="/otp",
    tags=["otp"]
)


@router.post("/registration", status_code=status.HTTP_201_CREATED)
def send_registration_otp(
    db: db_dependency,
    email_verification: EmailVerification,
    background_task: BackgroundTasks
    ):
    otp_code, token = otp_crud.create_or_update_otp(db, email_verification.email)

    background_task.add_task(send_otp_mail, email_verification.email, otp_code)

    return {"message": "OTP sent successfully", "token": token}


@router.post("/verify-otp", status_code=status.HTTP_200_OK)
def verify_otp(
    db: db_dependency,
    otp_verify: OtpVerify
    ):
    otp_crud.verify_otp(db, otp_verify)
    return {"message": "OTP verified successfully", "verified_token": otp_verify.token}
