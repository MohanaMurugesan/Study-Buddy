from pydantic import BaseModel,Field,StringConstraints
import uuid
from datetime import datetime
from typing import Annotated

MimeStr = Annotated[str, StringConstraints(pattern=r"^[A-Za-z0-9.+-]+/[A-Za-z0-9.+-]+$")]
class AttachmentUpload(BaseModel):
    file_path : str
    file_name : str
    file_type : MimeStr
    file_size :int = Field(gt=0 ,lt=26214400)
    community_id : uuid.UUID
    created_at : datetime
    user_id : uuid.UUID

    class Config:
        from_attributes = True

class DocumentListItem(BaseModel):
    id: str
    file_name: str
    file_type: MimeStr
    file_size: int
    created_at: datetime
    user_id: str

    class Config:
        from_attributes = True