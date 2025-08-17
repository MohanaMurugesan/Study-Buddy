from app.database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import APIRouter,status,HTTPException,Depends
from app.schemas.user import UserCreate,UserResponse
from app.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]


password_context = CryptContext(schemes=["bcrypt"],deprecated="auto")


def hash_password(password:str):
    return password_context.hash(password)


@router.post("/Register",status_code=status.HTTP_201_CREATED)
def create_user(db:db_dependency, create_user_request : UserCreate):
    check_existing_user = db.query(User).filter (User.email == create_user_request.email).first()
    if check_existing_user:
        raise HTTPException(status_code=400,detail="Existing email id")

    new_user = User(
        email = create_user_request.email,
        username = create_user_request.username,
       password= hash_password(create_user_request.password),
       is_verified = True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse.model_validate(new_user)

