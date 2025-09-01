from pydantic import BaseModel,HttpUrl
from typing import Optional,List,Dict
import uuid
from datetime import datetime
 

class ProfileBase(BaseModel):
    profile_picture : Optional[str] = None
    bio : Optional[str] = None
    location : Optional[str] = None
    preferred_language : Optional[str] = None
    subjects: Optional[List[str]] = None
    availability : Optional[Dict[str,str]] = None
    study_goals :Optional[str] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    id : uuid.UUID
    user_id : uuid.UUID
    created_at : datetime
    updated_at:datetime

    model_config={
        "from_attributes" : True
    }