from fastapi import APIRouter,Depends
from app.models.user import User
from app.dependencies import get_current_user

router=APIRouter()

@router.get("/me")
def get_profile(user : User = Depends(get_current_user)):
    return user