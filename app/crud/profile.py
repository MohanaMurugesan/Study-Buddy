from sqlalchemy.orm import Session
import uuid
from app.schemas.profile import ProfileCreate,ProfileUpdate
from app.models.profile import Profile
from fastapi import HTTPException


def create_profile(db:Session , user_id : uuid.UUID, profile_data : ProfileCreate):
    existing_profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if existing_profile:
        raise HTTPException(status_code=400,detail="Profile already exist")
    
    profile = Profile(user_id = user_id , **profile_data.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

def get_profile(db:Session,user_id : uuid.UUID):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404,detail="Profile not found")
    return profile


def update_profile(db:Session,user_id:uuid.UUID,profile_data : ProfileUpdate):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404,detail="Profile not found")
    
    for field,value in profile_data.model_dump(exclude_unset=True).items():
        setattr(profile,field,value)

    db.commit()
    db.refresh(profile)
    return profile

def delete_profile(db:Session,user_id:uuid.UUID):
    profile=db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404,detail="Profile not found")
    
    db.delete(profile)
    db.commit()
    return {"detail":"Profile deleted successfully"}