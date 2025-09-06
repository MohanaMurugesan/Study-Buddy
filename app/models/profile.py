from app.database import Base
from sqlalchemy import Column,ForeignKey,String,DateTime,JSON,Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime,timezone
from sqlalchemy.orm import relationship

class Profile(Base):

    __tablename__ = "user_profile"

    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4,index=True)
    user_id = Column(UUID(as_uuid=True),ForeignKey("users.id",ondelete="CASCADE"),unique=True,index=True)
    bio = Column(Text,nullable=True)
    subjects = Column(JSON,nullable = True)
    availability = Column(JSON,nullable= True)
    profile_picture=Column(String,nullable=True)
    study_goals=Column(Text,nullable=True)
    location = Column(String,nullable=True)
    preferred_language = Column(JSON,nullable = True)
    created_at = Column(DateTime , default=lambda: datetime.now(timezone.utc))
    updated_at=Column(DateTime,default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User",back_populates="profile")