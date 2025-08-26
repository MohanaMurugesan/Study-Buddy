from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"],deprecated="auto")


def hash_password(password:str):
    return password_context.hash(password)


def hash_otp (otp : int):
    return password_context.hash(otp)
