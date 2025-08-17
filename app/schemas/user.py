from pydantic import BaseModel,EmailStr
from uuid import UUID
from datetime import datetime


class UserCreate(BaseModel):

    email : EmailStr
    username : str
    password : str

class UserResponse(BaseModel):

    id : UUID
    email : str
    username : str
    created_at : datetime 

    model_config = { "from_attributes" : True }