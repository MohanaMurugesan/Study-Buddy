from sqlalchemy.orm import Session
import uuid
from app.schemas.profile import ProfileCreate,ProfileUpdate
from app.models.profile import Profile
import json

def create_profile(db:Session , user_id : uuid.UUID, profile_data : ProfileCreate):
    existing_profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if existing_profile:
        return None
    
    data = profile_data.model_dump(exclude_unset=True)

    if isinstance(data.get("subjects"),str):
        try:
            data["subjects"] = json.loads(data["subjects"])
        except:
            data["subjects"] = [data["subjects"]]

    if isinstance(data.get("availability"),str):
        try:
            data["availability"] = json.loads(data["availability"])
        except:
            data["availability"] = {}
    
    if isinstance(data.get("preferred_language"),str):
        try:
            data["preferred_language"] = json.loads(data["preferred_language"])
        except:
            data["preferred_language"] = [data["preferred_language"]]


    profile = Profile(user_id = user_id ,**data )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

def get_profile(db:Session,user_id : uuid.UUID):
    return db.query(Profile).filter(Profile.user_id == user_id).first()
    

def update_profile(db:Session,user_id:uuid.UUID,profile_data : ProfileUpdate):
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        return None
    
    for field,value in profile_data.model_dump(exclude_unset=True).items():
        setattr(profile,field,value)

    db.commit()
    db.refresh(profile)
    return profile

def delete_profile(db:Session,user_id:uuid.UUID):
    profile=db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        return None
    
    db.delete(profile)
    db.commit()
    return {"detail":"Profile deleted successfully"}