from pydantic import BaseModel,EmailStr


class EmailVerification(BaseModel):
    email : EmailStr


class OtpVerify(BaseModel):
    token : str
    otp_code : str

    



