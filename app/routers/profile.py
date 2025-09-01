from fastapi import APIRouter,status,Depends,status
from app.routers.auth import db_dependency
from app.dependencies import get_current_user
from typing import Annotated
from app.schemas.profile import ProfileResponse,ProfileCreate,ProfileUpdate
from app.crud import profile as profile_crud

router = APIRouter(
    prefix="/profiles",
    tags=["profiles"]
)

user_dependency = Annotated[dict,Depends(get_current_user)]

@router.post("/",response_model=ProfileResponse,status_code=status.HTTP_201_CREATED)
def create_user(profile:ProfileCreate,db:db_dependency,user:user_dependency):
    return  profile_crud.create_profile(db,user.id,profile)

@router.get("/me",response_model=ProfileResponse,status_code=status.HTTP_200_OK)
def get_profile(db:db_dependency,user:user_dependency):
    return profile_crud.get_profile(db,user.id)

@router.put("/me",status_code=status.HTTP_200_OK)
def update_profile(profile:ProfileUpdate,db:db_dependency,user:user_dependency):
    return profile_crud.update_profile(db,user.id,profile)

@router.delete("/me",status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(db:db_dependency,user:user_dependency):
    return profile_crud.delete_profile(db,user.id)