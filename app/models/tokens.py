from app.database import Base
from sqlalchemy import Column,String,ForeignKey,DateTime,Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime,timezone

class RefreshToken(Base):
    __tablename__="refresh_tokens"

    id = Column(UUID(as_uuid=True),primary_key=True,index=True,default=uuid.uuid4)
    token = Column(String,unique=True,nullable=False)
    user_id = Column(UUID(as_uuid=True),ForeignKey("users.id",ondelete="CASCADE"))
    created_at = Column(DateTime,default=datetime.now(timezone.utc))
    expires_at = Column(DateTime,nullable=False)
    revoked = Column(Boolean,default=False)