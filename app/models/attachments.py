from app.database import Base
from sqlalchemy import Column,UUID,String,Integer,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
import uuid


class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4,index=True)
    message_id = Column(UUID(as_uuid=True),ForeignKey("messages.id",ondelete="CASCADE"),nullable=False)
    file_path = Column(String,nullable=False)
    file_name = Column(String,nullable=False)
    file_type = Column(String,nullable=False)
    file_size = Column(Integer,nullable=False)
    created_at = Column(DateTime,default=datetime.now(timezone.utc),nullable=False)
    user_id = Column(UUID(as_uuid=True),ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    community_id = Column(UUID(as_uuid=True),ForeignKey("community.id",ondelete="CASCADE"),nullable=False)

    user = relationship("User",back_populates="attachments")
    community = relationship("Community",back_populates="attachments")
    message = relationship("Message",back_populates="attachments")