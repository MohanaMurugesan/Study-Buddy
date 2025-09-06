from pydantic import BaseModel,Field
from typing import Optional,List
from datetime import datetime
import uuid
from app.enums import CommunityRole,Status

class CommunityCreate(BaseModel):
    community_name : str = Field(max_length=30)
    subject : str = Field(max_length=30)
    goals : Optional[str] = Field(None,max_length=250)
    description : Optional[str] = None
    is_private : Optional[bool] 

class CommunityUpdate(BaseModel):
    community_name : Optional[str] = Field(default=None,max_length=30)
    subject : Optional[str] = Field(default=None,max_length=30)
    goals : Optional[str] = Field(default=None,max_length=250)
    description : Optional[str] = None
    is_private : Optional[bool] = None

class MemberInfo(BaseModel):
    id : uuid.UUID
    username : str
    role : CommunityRole
    status : Status

    model_config = {
        "from_attributes" : True
    }
class CommunityResponse(BaseModel):
    id : uuid.UUID
    community_name : str
    subject : str
    is_private: bool
    created_at : datetime
    updated_at : datetime
    goals : Optional[str]
    description: Optional[str]
    membership : List[MemberInfo] = Field(default_factory=list,exclude=True)

    model_config = {
        "from_attributes" : True
    }


class MembershipCreate(BaseModel):
    community_id : uuid.UUID

class MembershipResponse(BaseModel):
    community_id : uuid.UUID
    member : MemberInfo
    role : CommunityRole
    joined_at : datetime
    status : Status

    model_config = {
        "from_attributes" : True
    }

class CommunitiesOfMember(BaseModel):
    id : uuid.UUID
    community_name : str
    role : str
