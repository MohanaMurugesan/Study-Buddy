from pydantic import BaseModel,EmailStr
from uuid import UUID
from datetime import datetime


class UserCreate(BaseModel):

    token : str
    username : str
    password : str

class LoginUser(BaseModel):
    
    username : str
    password : str

class UserResponse(BaseModel):

    id : UUID
    email : EmailStr
    username : str
    created_at : datetime 

    model_config = { "from_attributes" : True }