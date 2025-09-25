from pydantic import BaseModel
from datetime import datetime
import uuid

class MessageBase(BaseModel):
    message: str

class SenderInfo(BaseModel):
    username : str

class MessageCreate(MessageBase):
    community_id: uuid.UUID

class MessageResponse(MessageBase):
    id: uuid.UUID
    sender_id: uuid.UUID
    community_id: uuid.UUID
    created_at: datetime
    sender: SenderInfo 



    model_config = {
    "from_attributes": True,
    "json_encoders": {
        uuid.UUID: str
        }
    }


    @classmethod
    def from_orm(cls, obj):

    # Convert ORM object to response schema with nested sender info

        data = {
        "id": obj.id,
        "sender_id": obj.sender_id,
        "community_id": obj.community_id,
        "message": obj.message,
        "created_at": obj.created_at,
        "sender": {"username": obj.sender.username} if getattr(obj, "sender", None) else {"username": ""}
        }

        return cls(**data)