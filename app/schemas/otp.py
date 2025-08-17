from pydantic import BaseModel,EmailStr


class EmailVerification(BaseModel):
    email : EmailStr


class OtpVerify(BaseModel):
    email : EmailStr
    otp_code : str

    



