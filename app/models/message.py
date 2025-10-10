from app.database import Base
from sqlalchemy import Column,UUID,ForeignKey,Text,DateTime
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime,timezone

class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4,index=True)
    sender_id = Column(UUID(as_uuid=True),ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    community_id = Column(UUID(as_uuid=True),ForeignKey("community.id",ondelete="CASCADE"),nullable=False)
    message=Column(Text)
    created_at = Column(DateTime,default=datetime.now(timezone.utc),nullable=False)

    sender = relationship("User", back_populates="messages")
    community = relationship("Community",back_populates="messages")
    attachments = relationship("Attachment",back_populates="message")